"""
Pydantic schemas for Module 2: AI B2B Proposal Generator
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date


class ProposalRequest(BaseModel):
    """Request schema for B2B proposal generation."""
    
    client_name: str = Field(..., description="Name of the client company", min_length=1)
    budget_limit: float = Field(..., description="Maximum budget in currency units", gt=0)
    requirements: str = Field(..., description="Client requirements and needs", min_length=10)
    delivery_date: Optional[date] = Field(None, description="Expected delivery date")
    priorities: List[str] = Field(
        default=[],
        description="Sustainability priorities (e.g., plastic-free, local-sourcing)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "client_name": "GreenTech Corp",
                "budget_limit": 50000,
                "requirements": "Office supplies for 200 employees, focus on plastic reduction",
                "delivery_date": "2026-04-15",
                "priorities": ["plastic-free", "recycled-content", "local-sourcing"]
            }
        }


class ProductItem(BaseModel):
    """Individual product in a proposal."""
    
    product_id: str
    product_name: str
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    total_price: float = Field(..., gt=0)
    sustainability_impact: str
    category: Optional[str] = None


class BudgetAllocation(BaseModel):
    """Budget allocation breakdown."""
    
    total_budget: float
    allocated: float
    remaining: float
    utilization_percentage: float


class CostBreakdown(BaseModel):
    """Detailed cost breakdown."""
    
    products: float
    shipping: float = 0.0
    taxes: float = 0.0
    discount: float = 0.0


class ImpactSummary(BaseModel):
    """Sustainability impact summary."""
    
    plastic_avoided_kg: float
    trees_saved: int
    carbon_offset_kg: float
    local_suppliers_count: int
    key_message: str


class AIProposalOutput(BaseModel):
    """AI output schema for proposal generation."""
    
    product_mix: List[ProductItem] = Field(..., description="Curated list of products")
    total_cost: float = Field(..., description="Total cost of all products")
    impact_highlights: List[str] = Field(..., description="Key sustainability benefits")
    reasoning: Optional[str] = Field(None, description="Rationale for product selection")
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_mix": [
                    {
                        "product_id": "prod_789",
                        "product_name": "Recycled Paper Notebooks",
                        "quantity": 250,
                        "unit_price": 12.50,
                        "total_price": 3125.00,
                        "sustainability_impact": "100% recycled content, saves 1.2 trees per unit"
                    }
                ],
                "total_cost": 48750.00,
                "impact_highlights": [
                    "Eliminates 125kg of plastic waste",
                    "Saves 45 trees through recycled content",
                    "Supports 3 local suppliers"
                ],
                "reasoning": "Selected products prioritize plastic-free alternatives while maximizing budget efficiency"
            }
        }


class ProposalResponse(BaseModel):
    """Complete proposal response."""
    
    proposal_id: str
    client_name: str
    generated_at: datetime
    product_mix: List[ProductItem]
    budget_allocation: BudgetAllocation
    cost_breakdown: CostBreakdown
    impact_summary: ImpactSummary
    status: str = "draft"
    
    class Config:
        json_schema_extra = {
            "example": {
                "proposal_id": "prop_abc123",
                "client_name": "GreenTech Corp",
                "generated_at": "2026-03-04T10:30:00Z",
                "product_mix": [],
                "budget_allocation": {
                    "total_budget": 50000,
                    "allocated": 48750,
                    "remaining": 1250,
                    "utilization_percentage": 97.5
                },
                "cost_breakdown": {
                    "products": 48750,
                    "shipping": 0,
                    "taxes": 0
                },
                "impact_summary": {
                    "plastic_avoided_kg": 125,
                    "trees_saved": 45,
                    "carbon_offset_kg": 230,
                    "local_suppliers_count": 3,
                    "key_message": "This proposal eliminates 125kg of plastic waste"
                },
                "status": "draft"
            }
        }


class ProposalUpdateRequest(BaseModel):
    """Request to update proposal status."""
    
    status: str = Field(..., description="New status (draft, sent, accepted, rejected)")


class ProposalListResponse(BaseModel):
    """Response for listing proposals."""
    
    proposals: List[ProposalResponse]
    total_count: int
    page: int
    page_size: int
