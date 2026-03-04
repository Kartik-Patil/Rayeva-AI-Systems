"""
Predefined taxonomies and constants for category tagging.
"""
from typing import Dict, List, Set


# Predefined primary categories
PRIMARY_CATEGORIES = [
    "Kitchen & Dining",
    "Personal Care",
    "Home & Living",
    "Fashion & Accessories",
    "Office Supplies",
    "Baby & Kids",
    "Outdoor & Garden",
    "Gift Items",
    "Cleaning Supplies",
    "Food & Beverages"
]


# Sub-categories mapped to primary categories
SUB_CATEGORIES: Dict[str, List[str]] = {
    "Kitchen & Dining": [
        "Food Storage",
        "Cookware",
        "Cutlery & Utensils",
        "Drinkware",
        "Lunch Boxes",
        "Kitchen Accessories"
    ],
    "Personal Care": [
        "Oral Care",
        "Hair Care",
        "Skin Care",
        "Bath Products",
        "Hygiene Products"
    ],
    "Home & Living": [
        "Decor",
        "Textiles",
        "Storage Solutions",
        "Lighting",
        "Furniture"
    ],
    "Fashion & Accessories": [
        "Bags & Backpacks",
        "Jewelry",
        "Clothing",
        "Footwear",
        "Watches"
    ],
    "Office Supplies": [
        "Stationery",
        "Paper Products",
        "Writing Instruments",
        "Desk Accessories",
        "Organization"
    ],
    "Baby & Kids": [
        "Baby Care",
        "Toys",
        "Clothing",
        "Feeding",
        "Safety Products"
    ],
    "Outdoor & Garden": [
        "Garden Tools",
        "Planters",
        "Outdoor Furniture",
        "Camping Gear",
        "Sports Equipment"
    ],
    "Gift Items": [
        "Gift Sets",
        "Hampers",
        "Decorative Items",
        "Personalized Gifts"
    ],
    "Cleaning Supplies": [
        "Cleaning Tools",
        "Eco-Friendly Cleaners",
        "Laundry Products",
        "Waste Management"
    ],
    "Food & Beverages": [
        "Organic Food",
        "Beverages",
        "Snacks",
        "Condiments",
        "Specialty Foods"
    ]
}


# Available sustainability filters
SUSTAINABILITY_FILTERS = [
    "plastic-free",
    "compostable",
    "biodegradable",
    "vegan",
    "organic",
    "recycled-content",
    "recyclable",
    "natural-materials",
    "zero-waste",
    "fair-trade",
    "local-sourcing",
    "carbon-neutral",
    "handmade",
    "cruelty-free",
    "non-toxic",
    "reusable",
    "upcycled"
]


# Keywords for sustainability filter detection
SUSTAINABILITY_KEYWORDS: Dict[str, Set[str]] = {
    "plastic-free": {"plastic-free", "no plastic", "without plastic", "plastic free"},
    "compostable": {"compostable", "compost", "home compostable"},
    "biodegradable": {"biodegradable", "biodegrades", "naturally decompose"},
    "vegan": {"vegan", "plant-based", "no animal products"},
    "organic": {"organic", "certified organic", "organically grown"},
    "recycled-content": {"recycled", "post-consumer", "recycled materials"},
    "recyclable": {"recyclable", "can be recycled", "recyclability"},
    "natural-materials": {"natural", "bamboo", "wood", "cotton", "jute", "hemp"},
    "zero-waste": {"zero waste", "zero-waste", "waste-free"},
    "fair-trade": {"fair trade", "fair-trade", "ethically sourced"},
    "local-sourcing": {"local", "locally sourced", "made in india", "indigenous"},
    "carbon-neutral": {"carbon neutral", "carbon-neutral", "carbon offset"},
    "handmade": {"handmade", "hand-crafted", "artisan", "hand made"},
    "cruelty-free": {"cruelty-free", "not tested on animals", "no animal testing"},
    "non-toxic": {"non-toxic", "chemical-free", "safe", "bpa-free"},
    "reusable": {"reusable", "reuse", "multi-use", "re-usable"},
    "upcycled": {"upcycled", "upcycle", "repurposed"}
}
