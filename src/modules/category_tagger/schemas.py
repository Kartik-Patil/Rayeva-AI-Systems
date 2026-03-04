"""
Pydantic schemas for Module 1: AI Auto-Category & Tag Generator
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CategoryRequest(BaseModel):
    """Request schema for product categorization."""
    
    product_id: Optional[str] = Field(None, description="Optional product ID for tracking")
    product_name: str = Field(..., description="Name of the product", min_length=1)
    description: str = Field(..., description="Product description", min_length=10)
    additional_info: Optional[str] = Field(None, description="Additional product information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "prod_123",
                "product_name": "Bamboo Fiber Lunch Box",
                "description": "Eco-friendly lunch container made from natural bamboo fibers",
                "additional_info": "BPA-free, microwave safe, biodegradable"
            }
        }


class AICategorizationOutput(BaseModel):
    """AI output schema for categorization (validated structure)."""
    
    primary_category: str = Field(..., description="Main product category")
    sub_category: str = Field(..., description="Sub-category within primary category")
    seo_tags: List[str] = Field(..., description="5-10 SEO-optimized tags", min_items=5, max_items=10)
    sustainability_filters: List[str] = Field(..., description="Applicable sustainability attributes")
    confidence_score: float = Field(..., description="AI confidence score (0-1)", ge=0.0, le=1.0)
    reasoning: Optional[str] = Field(None, description="Brief explanation of categorization")
    
    class Config:
        json_schema_extra = {
            "example": {
                "primary_category": "Kitchen & Dining",
                "sub_category": "Food Storage",
                "seo_tags": [
                    "bamboo lunch box",
                    "eco friendly container",
                    "sustainable food storage",
                    "biodegradable lunch box",
                    "zero waste kitchen"
                ],
                "sustainability_filters": [
                    "plastic-free",
                    "compostable",
                    "natural-materials",
                    "biodegradable"
                ],
                "confidence_score": 0.92,
                "reasoning": "Product clearly fits Kitchen & Dining due to lunch box function, with strong sustainability credentials"
            }
        }


class CategoryResponse(BaseModel):
    """Response schema for categorization endpoint."""
    
    product_id: str
    product_name: str
    primary_category: str
    sub_category: str
    seo_tags: List[str]
    sustainability_filters: List[str]
    confidence_score: float
    processing_timestamp: datetime
    database_id: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "prod_123",
                "product_name": "Bamboo Fiber Lunch Box",
                "primary_category": "Kitchen & Dining",
                "sub_category": "Food Storage",
                "seo_tags": ["bamboo lunch box", "eco friendly container"],
                "sustainability_filters": ["plastic-free", "compostable"],
                "confidence_score": 0.92,
                "processing_timestamp": "2026-03-04T10:15:30.123456",
                "database_id": "cat_abc123"
            }
        }


class BatchCategoryRequest(BaseModel):
    """Request schema for batch categorization."""
    
    products: List[CategoryRequest] = Field(..., max_items=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "products": [
                    {
                        "product_id": "prod_1",
                        "product_name": "Bamboo Toothbrush",
                        "description": "Sustainable toothbrush with bamboo handle"
                    },
                    {
                        "product_id": "prod_2",
                        "product_name": "Reusable Cotton Bags",
                        "description": "Set of organic cotton shopping bags"
                    }
                ]
            }
        }


class BatchCategoryResponse(BaseModel):
    """Response schema for batch categorization."""
    
    results: List[CategoryResponse]
    total_processed: int
    total_failed: int
    processing_time_ms: int
