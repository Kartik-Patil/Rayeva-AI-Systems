"""
Service layer for Module 1: AI Auto-Category & Tag Generator
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import select

from .schemas import CategoryRequest, AICategorizationOutput, CategoryResponse
from .taxonomy import PRIMARY_CATEGORIES, SUB_CATEGORIES, SUSTAINABILITY_FILTERS, SUSTAINABILITY_KEYWORDS
from ...core.ai_service import ai_service
from ...core.database import get_db_session
from ...core.logging_service import logging_service
from ...models.database_models import CategoryResult


class CategoryTaggerService:
    """Service for AI-powered product categorization and tagging."""
    
    def __init__(self):
        self.logger = logging_service.get_logger("category_tagger")
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for AI categorization."""
        return f"""You are an expert in sustainable product categorization and e-commerce SEO.

Your task is to analyze product information and provide structured categorization.

AVAILABLE PRIMARY CATEGORIES:
{', '.join(PRIMARY_CATEGORIES)}

AVAILABLE SUSTAINABILITY FILTERS:
{', '.join(SUSTAINABILITY_FILTERS)}

INSTRUCTIONS:
1. Choose the MOST appropriate primary category from the list above
2. Suggest a relevant sub-category (can be creative if needed)
3. Generate 5-10 SEO-optimized tags (mix of:
   - Product type keywords
   - Material keywords
   - Use case keywords
   - Sustainability keywords)
4. Identify applicable sustainability filters from the list above
5. Assign a confidence score (0-1) based on description quality
6. Provide brief reasoning for your choices

IMPORTANT:
- Only use categories from the predefined list
- Tags should be lowercase, hyphenated phrases
- Only assign sustainability filters you're confident about
- If description is vague, reflect lower confidence
"""
    
    def _build_user_prompt(self, request: CategoryRequest) -> str:
        """Build user prompt with product details."""
        prompt = f"""
Product Name: {request.product_name}
Description: {request.description}
"""
        if request.additional_info:
            prompt += f"\nAdditional Info: {request.additional_info}"
        
        prompt += "\n\nProvide categorization in JSON format."
        return prompt
    
    def _validate_and_enhance(self, ai_output: AICategorizationOutput, request: CategoryRequest) -> AICategorizationOutput:
        """
        Validate AI output against business rules and enhance with additional logic.
        
        Args:
            ai_output: Raw AI categorization output
            request: Original request
            
        Returns:
            Validated and enhanced output
        """
        # Validate primary category
        if ai_output.primary_category not in PRIMARY_CATEGORIES:
            self.logger.warning(f"Invalid category '{ai_output.primary_category}', defaulting to 'Home & Living'")
            ai_output.primary_category = "Home & Living"
            ai_output.confidence_score *= 0.8  # Reduce confidence
        
        # Validate sustainability filters
        valid_filters = [f for f in ai_output.sustainability_filters if f in SUSTAINABILITY_FILTERS]
        ai_output.sustainability_filters = valid_filters
        
        # Enhance with keyword-based filter detection
        full_text = f"{request.product_name} {request.description}".lower()
        if request.additional_info:
            full_text += f" {request.additional_info}".lower()
        
        detected_filters = set(ai_output.sustainability_filters)
        for filter_name, keywords in SUSTAINABILITY_KEYWORDS.items():
            if any(keyword in full_text for keyword in keywords):
                detected_filters.add(filter_name)
        
        ai_output.sustainability_filters = sorted(list(detected_filters))
        
        # Ensure tag count is within range
        if len(ai_output.seo_tags) < 5:
            # Add generic tags if needed
            ai_output.seo_tags.append(f"{request.product_name.lower()}")
            ai_output.seo_tags.append("sustainable product")
        
        ai_output.seo_tags = ai_output.seo_tags[:10]  # Max 10 tags
        
        # Normalize tags (lowercase, no duplicates)
        ai_output.seo_tags = sorted(list(set([tag.lower() for tag in ai_output.seo_tags])))
        
        return ai_output
    
    async def categorize_product(self, request: CategoryRequest) -> CategoryResponse:
        """
        Categorize a single product using AI.
        
        Args:
            request: Product categorization request
            
        Returns:
            Categorization response with database ID
            
        Raises:
            ValueError: If AI generation fails
        """
        self.logger.info(f"Categorizing product: {request.product_name}")
        
        # Generate product ID if not provided
        product_id = request.product_id or f"prod_{uuid.uuid4().hex[:8]}"
        
        # Build prompts
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(request)
        
        # Call AI service
        ai_output = await ai_service.generate_structured_output(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            schema=AICategorizationOutput
        )
        
        # Validate and enhance
        validated_output = self._validate_and_enhance(ai_output, request)
        
        # Store in database
        async with get_db_session() as session:
            db_record = CategoryResult(
                product_id=product_id,
                product_name=request.product_name,
                product_description=request.description,
                primary_category=validated_output.primary_category,
                sub_category=validated_output.sub_category,
                seo_tags=validated_output.seo_tags,
                sustainability_filters=validated_output.sustainability_filters,
                confidence_score=validated_output.confidence_score,
                raw_ai_response=validated_output.model_dump()
            )
            session.add(db_record)
            await session.commit()
            await session.refresh(db_record)
            
            db_id = db_record.id
        
        self.logger.info(
            f"Successfully categorized product {product_id}",
            extra={"data": {
                "category": validated_output.primary_category,
                "confidence": validated_output.confidence_score,
                "tags_count": len(validated_output.seo_tags)
            }}
        )
        
        # Build response
        return CategoryResponse(
            product_id=product_id,
            product_name=request.product_name,
            primary_category=validated_output.primary_category,
            sub_category=validated_output.sub_category,
            seo_tags=validated_output.seo_tags,
            sustainability_filters=validated_output.sustainability_filters,
            confidence_score=validated_output.confidence_score,
            processing_timestamp=datetime.utcnow(),
            database_id=db_id
        )
    
    async def get_categorization(self, product_id: str) -> Optional[CategoryResponse]:
        """
        Retrieve stored categorization for a product.
        
        Args:
            product_id: Product identifier
            
        Returns:
            Categorization response or None if not found
        """
        async with get_db_session() as session:
            result = await session.execute(
                select(CategoryResult).where(CategoryResult.product_id == product_id)
            )
            record = result.scalar_one_or_none()
            
            if not record:
                return None
            
            return CategoryResponse(
                product_id=record.product_id,
                product_name=record.product_name,
                primary_category=record.primary_category,
                sub_category=record.sub_category,
                seo_tags=record.seo_tags,
                sustainability_filters=record.sustainability_filters,
                confidence_score=record.confidence_score,
                processing_timestamp=record.created_at,
                database_id=record.id
            )


# Global service instance
category_tagger_service = CategoryTaggerService()
