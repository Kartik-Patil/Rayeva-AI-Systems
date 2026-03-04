"""
Mock product catalog for B2B proposal generation.
In production, this would be fetched from a real product database.
"""
from typing import List, Dict, Any


# Mock product catalog with sustainable products
PRODUCT_CATALOG = [
    {
        "product_id": "prod_001",
        "product_name": "Recycled Paper Notebooks (A5)",
        "category": "Office Supplies",
        "unit_price": 12.50,
        "stock": 1000,
        "sustainability": {
            "plastic_free": True,
            "recycled_content": 100,
            "trees_saved_per_unit": 0.05,
            "carbon_offset_g": 120
        },
        "impact": "100% recycled content, saves trees"
    },
    {
        "product_id": "prod_002",
        "product_name": "Bamboo Pen Set (Pack of 10)",
        "category": "Office Supplies",
        "unit_price": 8.00,
        "stock": 500,
        "sustainability": {
            "plastic_free": True,
            "biodegradable": True,
            "carbon_offset_g": 30
        },
        "impact": "Plastic-free alternative, biodegradable"
    },
    {
        "product_id": "prod_003",
        "product_name": "Jute Tote Bag",
        "category": "Fashion & Accessories",
        "unit_price": 15.00,
        "stock": 800,
        "sustainability": {
            "plastic_free": True,
            "natural_materials": True,
            "reusable": True,
            "local_sourcing": True
        },
        "impact": "Replaces single-use plastic bags, locally sourced"
    },
    {
        "product_id": "prod_004",
        "product_name": "Bamboo Fiber Lunch Box",
        "category": "Kitchen & Dining",
        "unit_price": 25.00,
        "stock": 300,
        "sustainability": {
            "plastic_free": True,
            "compostable": True,
            "carbon_offset_g": 200
        },
        "impact": "Compostable, BPA-free alternative"
    },
    {
        "product_id": "prod_005",
        "product_name": "Recycled Cardboard File Folders (Set of 25)",
        "category": "Office Supplies",
        "unit_price": 18.00,
        "stock": 400,
        "sustainability": {
            "recycled_content": 100,
            "recyclable": True,
            "trees_saved_per_unit": 0.08
        },
        "impact": "100% recycled, fully recyclable"
    },
    {
        "product_id": "prod_006",
        "product_name": "Stainless Steel Water Bottle (500ml)",
        "category": "Kitchen & Dining",
        "unit_price": 22.00,
        "stock": 600,
        "sustainability": {
            "plastic_free": True,
            "reusable": True,
            "carbon_offset_g": 150,
            "plastic_avoided_per_year_kg": 5.2
        },
        "impact": "Eliminates single-use plastic bottles"
    },
    {
        "product_id": "prod_007",
        "product_name": "Organic Cotton Desk Pad",
        "category": "Office Supplies",
        "unit_price": 30.00,
        "stock": 200,
        "sustainability": {
            "organic": True,
            "natural_materials": True,
            "local_sourcing": True
        },
        "impact": "Organic cotton, supports local artisans"
    },
    {
        "product_id": "prod_008",
        "product_name": "Plantable Seed Paper Greeting Cards (Pack of 10)",
        "category": "Gift Items",
        "unit_price": 12.00,
        "stock": 500,
        "sustainability": {
            "biodegradable": True,
            "recycled_content": 80,
            "compostable": True
        },
        "impact": "Cards grow into plants, fully biodegradable"
    },
    {
        "product_id": "prod_009",
        "product_name": "Biodegradable Bamboo Toothbrush",
        "category": "Personal Care",
        "unit_price": 6.00,
        "stock": 1000,
        "sustainability": {
            "plastic_free": True,
            "biodegradable": True,
            "compostable": True,
            "plastic_avoided_g": 18
        },
        "impact": "Eliminates plastic toothbrush waste"
    },
    {
        "product_id": "prod_010",
        "product_name": "Reusable Cotton Produce Bags (Set of 5)",
        "category": "Home & Living",
        "unit_price": 14.00,
        "stock": 400,
        "sustainability": {
            "plastic_free": True,
            "organic": True,
            "reusable": True
        },
        "impact": "Replaces single-use plastic bags"
    },
    {
        "product_id": "prod_011",
        "product_name": "Solar-Powered Desk Calculator",
        "category": "Office Supplies",
        "unit_price": 28.00,
        "stock": 150,
        "sustainability": {
            "carbon_neutral": True,
            "no_batteries": True
        },
        "impact": "Solar-powered, eliminates battery waste"
    },
    {
        "product_id": "prod_012",
        "product_name": "Recycled Glass Water Carafe (1L)",
        "category": "Kitchen & Dining",
        "unit_price": 35.00,
        "stock": 250,
        "sustainability": {
            "plastic_free": True,
            "recycled_content": 75,
            "reusable": True
        },
        "impact": "75% recycled glass, reduces plastic use"
    },
    {
        "product_id": "prod_013",
        "product_name": "Cork Desk Organizer",
        "category": "Office Supplies",
        "unit_price": 40.00,
        "stock": 180,
        "sustainability": {
            "natural_materials": True,
            "sustainable_harvest": True,
            "biodegradable": True
        },
        "impact": "Sustainably harvested cork"
    },
    {
        "product_id": "prod_014",
        "product_name": "Beeswax Food Wraps (Set of 3)",
        "category": "Kitchen & Dining",
        "unit_price": 18.00,
        "stock": 350,
        "sustainability": {
            "plastic_free": True,
            "reusable": True,
            "compostable": True,
            "plastic_avoided_per_year_kg": 2.5
        },
        "impact": "Replaces plastic wrap, fully compostable"
    },
    {
        "product_id": "prod_015",
        "product_name": "Handmade Paper Calendar",
        "category": "Office Supplies",
        "unit_price": 20.00,
        "stock": 200,
        "sustainability": {
            "recycled_content": 90,
            "handmade": True,
            "local_sourcing": True,
            "trees_saved_per_unit": 0.03
        },
        "impact": "Supports local artisans, 90% recycled"
    }
]


def get_products_by_filter(
    categories: List[str] = None,
    max_price: float = None,
    sustainability_priorities: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Filter products based on criteria.
    
    Args:
        categories: List of categories to include
        max_price: Maximum unit price
        sustainability_priorities: List of sustainability attributes to prioritize
        
    Returns:
        Filtered list of products
    """
    filtered = PRODUCT_CATALOG.copy()
    
    if categories:
        filtered = [p for p in filtered if p["category"] in categories]
    
    if max_price:
        filtered = [p for p in filtered if p["unit_price"] <= max_price]
    
    # Sort by sustainability match if priorities provided
    if sustainability_priorities:
        def sustainability_score(product):
            score = 0
            for priority in sustainability_priorities:
                priority_key = priority.replace("-", "_")
                if priority_key in product["sustainability"]:
                    score += 1
            return score
        
        filtered.sort(key=sustainability_score, reverse=True)
    
    return filtered


def calculate_product_impact(product: Dict[str, Any], quantity: int) -> Dict[str, float]:
    """
    Calculate sustainability impact for a product quantity.
    
    Args:
        product: Product data
        quantity: Quantity purchased
        
    Returns:
        Impact metrics
    """
    sustainability = product["sustainability"]
    
    return {
        "plastic_avoided_kg": sustainability.get("plastic_avoided_per_year_kg", 0) * quantity,
        "plastic_avoided_g": sustainability.get("plastic_avoided_g", 0) * quantity / 1000,
        "trees_saved": sustainability.get("trees_saved_per_unit", 0) * quantity,
        "carbon_offset_kg": sustainability.get("carbon_offset_g", 0) * quantity / 1000,
        "is_local": sustainability.get("local_sourcing", False)
    }
