"""
API routes for Module 1: AI Auto-Category & Tag Generator
"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional

from ..modules.category_tagger.schemas import (
    CategoryRequest,
    CategoryResponse,
    BatchCategoryRequest,
    BatchCategoryResponse
)
from ..modules.category_tagger.service import category_tagger_service


router = APIRouter(prefix="/api/v1/category", tags=["Category Tagging"])


@router.post("/generate", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def generate_category(request: CategoryRequest):
    """
    Generate AI-powered categorization for a product.
    
    - **product_name**: Name of the product (required)
    - **description**: Detailed product description (required)
    - **additional_info**: Optional additional product information
    - **product_id**: Optional product ID for tracking
    
    Returns structured categorization with SEO tags and sustainability filters.
    """
    try:
        return await category_tagger_service.categorize_product(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate categorization: {str(e)}"
        )


@router.get("/{product_id}", response_model=CategoryResponse)
async def get_category(product_id: str):
    """
    Retrieve stored categorization for a product.
    
    - **product_id**: Product identifier
    
    Returns the stored categorization or 404 if not found.
    """
    result = await category_tagger_service.get_categorization(product_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categorization not found for product: {product_id}"
        )
    
    return result


@router.post("/batch", response_model=BatchCategoryResponse)
async def batch_generate_categories(request: BatchCategoryRequest):
    """
    Generate categorizations for multiple products in batch.
    
    **Note**: This endpoint processes up to 50 products at once.
    Failed categorizations are logged but don't stop the batch process.
    """
    import time
    start_time = time.time()
    
    results = []
    failed_count = 0
    
    for product_request in request.products:
        try:
            result = await category_tagger_service.categorize_product(product_request)
            results.append(result)
        except Exception as e:
            failed_count += 1
            # Log error but continue processing
            print(f"Failed to categorize {product_request.product_name}: {str(e)}")
    
    processing_time_ms = int((time.time() - start_time) * 1000)
    
    return BatchCategoryResponse(
        results=results,
        total_processed=len(results),
        total_failed=failed_count,
        processing_time_ms=processing_time_ms
    )
