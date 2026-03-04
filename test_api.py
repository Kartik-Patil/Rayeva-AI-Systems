#!/usr/bin/env python
"""Quick test script for Module 1 & 2 APIs"""
import requests
import json

BASE_URL = "http://localhost:8000"
API_KEY = "rayeva_dev_key_12345"
HEADERS = {'X-API-Key': API_KEY}

print("=" * 60)
print("RAYEVA AI SYSTEMS - API TEST")
print("=" * 60)

# Test Module 1: Category Tagger
print("\n1️⃣  Testing Module 1: Category Tagger with Gemini AI")
print("-" * 60)

category_data = {
    'product_name': 'Bamboo Water Bottle',
    'description': 'Eco-friendly reusable water bottle made from sustainable bamboo. Keeps beverages cool for 12 hours.'
}

try:
    print("Sending request to Gemini API...")
    r = requests.post(f'{BASE_URL}/api/v1/category/generate', json=category_data, headers=HEADERS, timeout=60)
    
    if r.status_code == 201:
        result = r.json()
        print("✓ SUCCESS!")
        print(f"\n  Product: {result['product_name']}")
        print(f"  Primary Category: {result['primary_category']}")
        print(f"  Sub-Category: {result['sub_category']}")
        print(f"  SEO Tags: {', '.join(result['seo_tags'])}")
        print(f"  Sustainability Filters: {result['sustainability_filters']}")
        print(f"  Confidence Score: {result['confidence_score']:.2f}")
    else:
        print(f"✗ Error {r.status_code}")
        print(r.text)
except Exception as e:
    print(f"✗ Error: {str(e)}")

# Test Module 2: B2B Proposal Generator
print("\n\n2️⃣  Testing Module 2: B2B Proposal Generator with Gemini AI")
print("-" * 60)

proposal_data = {
    'client_name': 'EcoRetail Inc',
    'product_category': 'Home & Living',
    'budget_usd': 5000,
    'sustainability_requirements': ['Carbon Neutral', 'Recycled Materials']
}

try:
    print("Sending request to Gemini API...")
    r = requests.post(f'{BASE_URL}/api/v1/b2b/generate-proposal', json=proposal_data, headers=HEADERS, timeout=60)
    
    if r.status_code == 201:
        result = r.json()
        print("✓ SUCCESS!")
        print(f"\n  Proposal ID: {result['proposal_id']}")
        print(f"  Client: {result['client_name']}")
        print(f"  Budget: ${result['total_price']:.2f} / ${result['budget_usd']:.2f}")
        print(f"  Items: {len(result['proposed_items'])} products selected")
        print(f"  Impact Impact:")
        if 'environmental_impact' in result:
            impact = result['environmental_impact']
            print(f"    - Plastic Reduced: {impact.get('plastic_saved_kg', 0)} kg")
            print(f"    - Trees Saved: {impact.get('trees_saved', 0)}")
            print(f"    - Carbon Offset: {impact.get('carbon_offset_kg', 0)} kg")
    else:
        print(f"✗ Error {r.status_code}")
        print(r.text)
except Exception as e:
    print(f"✗ Error: {str(e)}")

print("\n" + "=" * 60)
print("API TESTS COMPLETE")
print("=" * 60)
