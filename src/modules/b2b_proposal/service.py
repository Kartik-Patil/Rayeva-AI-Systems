"""
Service layer for Module 2: AI B2B Proposal Generator
"""
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, desc

from .schemas import (
    ProposalRequest, ProposalResponse, ProductItem,
    BudgetAllocation, CostBreakdown, ImpactSummary,
    AIProposalOutput, ProposalListResponse
)
from .product_catalog import (
    get_products_by_filter,
    calculate_product_impact,
    PRODUCT_CATALOG
)
from ...core.ai_service import ai_service
from ...core.database import get_db_session
from ...core.logging_service import logging_service
from ...models.database_models import B2BProposal


class B2BProposalService:
    """Service for AI-powered B2B proposal generation."""
    
    def __init__(self):
        self.logger = logging_service.get_logger("b2b_proposal")
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for AI proposal generation."""
        return """You are an expert B2B sustainability consultant and proposal specialist.

Your task is to create optimized product recommendations for clients based on their:
- Budget constraints
- Specific requirements
- Sustainability priorities

GUIDELINES:
1. Stay within budget (ideally 90-98% utilization)
2. Prioritize products matching client's sustainability preferences
3. Select appropriate quantities based on requirements
4. Provide clear sustainability impact for each product
5. Create a balanced mix addressing all client needs
6. Justify your selections with reasoning

OUTPUT REQUIREMENTS:
- product_mix: Array of recommended products with quantities
- total_cost: Sum of all product costs
- impact_highlights: 3-5 key sustainability benefits
- reasoning: Brief explanation of product selection strategy
"""
    
    def _build_user_prompt(self, request: ProposalRequest, available_products: List[dict]) -> str:
        """Build user prompt with client requirements and product catalog."""
        products_info = []
        for p in available_products[:30]:  # Limit to top 30 to avoid token limits
            products_info.append(
                f"- {p['product_name']} (ID: {p['product_id']}): "
                f"${p['unit_price']}/unit, Stock: {p['stock']}, "
                f"Impact: {p['impact']}"
            )
        
        products_text = "\n".join(products_info)
        
        priorities_text = ", ".join(request.priorities) if request.priorities else "None specified"
        
        prompt = f"""
CLIENT: {request.client_name}
BUDGET: ${request.budget_limit:,.2f}
REQUIREMENTS: {request.requirements}
SUSTAINABILITY PRIORITIES: {priorities_text}

AVAILABLE PRODUCTS:
{products_text}

Create an optimized product proposal that:
1. Maximizes budget utilization (aim for 90-98%)
2. Addresses client requirements
3. Prioritizes requested sustainability attributes
4. Includes realistic quantities based on requirements

Provide response in JSON format with product_mix, total_cost, impact_highlights, and reasoning.
"""
        return prompt
    
    def _validate_budget_constraint(self, ai_output: AIProposalOutput, budget_limit: float) -> bool:
        """Validate that proposal stays within budget."""
        if ai_output.total_cost > budget_limit:
            self.logger.warning(
                f"AI proposal exceeds budget: ${ai_output.total_cost:,.2f} > ${budget_limit:,.2f}"
            )
            return False
        return True
    
    def _calculate_impact_metrics(self, product_items: List[ProductItem]) -> ImpactSummary:
        """
        Calculate aggregated sustainability impact metrics.
        
        Args:
            product_items: List of products in the proposal
            
        Returns:
            Aggregated impact summary
        """
        total_plastic_avoided = 0.0
        total_trees_saved = 0.0
        total_carbon_offset = 0.0
        local_suppliers = set()
        
        for item in product_items:
            # Find product in catalog
            product = next(
                (p for p in PRODUCT_CATALOG if p["product_id"] == item.product_id),
                None
            )
            
            if product:
                impact = calculate_product_impact(product, item.quantity)
                total_plastic_avoided += impact["plastic_avoided_kg"] + impact["plastic_avoided_g"]
                total_trees_saved += impact["trees_saved"]
                total_carbon_offset += impact["carbon_offset_kg"]
                
                if impact["is_local"]:
                    local_suppliers.add(item.product_id)
        
        # Generate key message
        highlights = []
        if total_plastic_avoided > 0:
            highlights.append(f"{total_plastic_avoided:.1f}kg of plastic avoided")
        if total_trees_saved > 0:
            highlights.append(f"{int(total_trees_saved)} trees saved")
        if local_suppliers:
            highlights.append(f"{len(local_suppliers)} local suppliers supported")
        
        key_message = "This proposal " + ", ".join(highlights) if highlights else "Sustainable product selection"
        
        return ImpactSummary(
            plastic_avoided_kg=round(total_plastic_avoided, 2),
            trees_saved=int(total_trees_saved),
            carbon_offset_kg=round(total_carbon_offset, 2),
            local_suppliers_count=len(local_suppliers),
            key_message=key_message
        )
    
    async def generate_proposal(self, request: ProposalRequest) -> ProposalResponse:
        """
        Generate B2B proposal using AI.
        
        Args:
            request: Proposal generation request
            
        Returns:
            Complete proposal response
            
        Raises:
            ValueError: If budget validation fails or AI generation fails
        """
        self.logger.info(f"Generating proposal for {request.client_name}, budget: ${request.budget_limit:,.2f}")
        
        # Get relevant products from catalog
        available_products = get_products_by_filter(
            max_price=request.budget_limit / 10,  # Reasonable unit price limit
            sustainability_priorities=request.priorities
        )
        
        if not available_products:
            raise ValueError("No products available matching criteria")
        
        # Build prompts
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(request, available_products)
        
        # Call AI service
        ai_output = await ai_service.generate_structured_output(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            schema=AIProposalOutput,
            temperature=0.8  # Slightly higher for creative proposals
        )
        
        # Validate budget constraint
        if not self._validate_budget_constraint(ai_output, request.budget_limit):
            raise ValueError(
                f"Proposal exceeds budget: ${ai_output.total_cost:,.2f} > ${request.budget_limit:,.2f}"
            )
        
        # Calculate budget allocation
        budget_allocation = BudgetAllocation(
            total_budget=request.budget_limit,
            allocated=ai_output.total_cost,
            remaining=request.budget_limit - ai_output.total_cost,
            utilization_percentage=round((ai_output.total_cost / request.budget_limit) * 100, 2)
        )
        
        # Calculate cost breakdown
        cost_breakdown = CostBreakdown(
            products=ai_output.total_cost,
            shipping=0.0,  # Could be calculated based on weight/distance
            taxes=0.0,     # Could be calculated based on location
            discount=0.0
        )
        
        # Calculate impact summary
        impact_summary = self._calculate_impact_metrics(ai_output.product_mix)
        
        # Generate proposal ID
        proposal_id = f"prop_{uuid.uuid4().hex[:12]}"
        
        # Store in database
        async with get_db_session() as session:
            db_record = B2BProposal(
                id=proposal_id,
                client_name=request.client_name,
                budget_limit=request.budget_limit,
                requirements=request.requirements,
                priorities=request.priorities,
                product_mix=[item.model_dump() for item in ai_output.product_mix],
                budget_allocation=budget_allocation.model_dump(),
                cost_breakdown=cost_breakdown.model_dump(),
                impact_summary=impact_summary.model_dump(),
                status="draft",
                raw_ai_response=ai_output.model_dump()
            )
            session.add(db_record)
            await session.commit()
        
        self.logger.info(
            f"Successfully generated proposal {proposal_id}",
            extra={"data": {
                "client": request.client_name,
                "products_count": len(ai_output.product_mix),
                "total_cost": ai_output.total_cost,
                "budget_utilization": budget_allocation.utilization_percentage
            }}
        )
        
        # Build response
        return ProposalResponse(
            proposal_id=proposal_id,
            client_name=request.client_name,
            generated_at=datetime.utcnow(),
            product_mix=ai_output.product_mix,
            budget_allocation=budget_allocation,
            cost_breakdown=cost_breakdown,
            impact_summary=impact_summary,
            status="draft"
        )
    
    async def get_proposal(self, proposal_id: str) -> Optional[ProposalResponse]:
        """
        Retrieve stored proposal by ID.
        
        Args:
            proposal_id: Proposal identifier
            
        Returns:
            Proposal response or None if not found
        """
        async with get_db_session() as session:
            result = await session.execute(
                select(B2BProposal).where(B2BProposal.id == proposal_id)
            )
            record = result.scalar_one_or_none()
            
            if not record:
                return None
            
            # Reconstruct ProductItem objects
            product_items = [ProductItem(**item) for item in record.product_mix]
            
            return ProposalResponse(
                proposal_id=record.id,
                client_name=record.client_name,
                generated_at=record.created_at,
                product_mix=product_items,
                budget_allocation=BudgetAllocation(**record.budget_allocation),
                cost_breakdown=CostBreakdown(**record.cost_breakdown),
                impact_summary=ImpactSummary(**record.impact_summary),
                status=record.status
            )
    
    async def update_proposal_status(self, proposal_id: str, new_status: str) -> bool:
        """
        Update proposal status.
        
        Args:
            proposal_id: Proposal identifier
            new_status: New status value
            
        Returns:
            True if updated successfully, False if not found
        """
        async with get_db_session() as session:
            result = await session.execute(
                select(B2BProposal).where(B2BProposal.id == proposal_id)
            )
            record = result.scalar_one_or_none()
            
            if not record:
                return False
            
            record.status = new_status
            record.updated_at = datetime.utcnow()
            await session.commit()
            
            self.logger.info(f"Updated proposal {proposal_id} status to {new_status}")
            return True
    
    async def list_proposals(
        self,
        client_name: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> ProposalListResponse:
        """
        List proposals with optional filters and pagination.
        
        Args:
            client_name: Filter by client name
            status: Filter by status
            page: Page number (1-indexed)
            page_size: Number of results per page
            
        Returns:
            Paginated list of proposals
        """
        async with get_db_session() as session:
            query = select(B2BProposal).order_by(desc(B2BProposal.created_at))
            
            if client_name:
                query = query.where(B2BProposal.client_name.contains(client_name))
            if status:
                query = query.where(B2BProposal.status == status)
            
            # Get total count
            count_result = await session.execute(query)
            all_records = count_result.scalars().all()
            total_count = len(all_records)
            
            # Apply pagination
            offset = (page - 1) * page_size
            query = query.limit(page_size).offset(offset)
            
            result = await session.execute(query)
            records = result.scalars().all()
            
            # Convert to response objects
            proposals = []
            for record in records:
                product_items = [ProductItem(**item) for item in record.product_mix]
                proposals.append(ProposalResponse(
                    proposal_id=record.id,
                    client_name=record.client_name,
                    generated_at=record.created_at,
                    product_mix=product_items,
                    budget_allocation=BudgetAllocation(**record.budget_allocation),
                    cost_breakdown=CostBreakdown(**record.cost_breakdown),
                    impact_summary=ImpactSummary(**record.impact_summary),
                    status=record.status
                ))
            
            return ProposalListResponse(
                proposals=proposals,
                total_count=total_count,
                page=page,
                page_size=page_size
            )


# Global service instance
b2b_proposal_service = B2BProposalService()
