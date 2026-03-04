# API Usage Examples

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Run the Application

```bash
python main.py
```

API will be available at `http://localhost:8000`

---

## Module 1: AI Auto-Category & Tag Generator

### Generate Categorization

**Endpoint**: `POST /api/v1/category/generate`

**Headers**:
```
X-API-Key: rayeva_dev_key_12345
Content-Type: application/json
```

**Request Body**:
```json
{
  "product_id": "prod_123",
  "product_name": "Bamboo Fiber Lunch Box",
  "description": "Eco-friendly lunch container made from natural bamboo fibers. BPA-free, microwave safe, and biodegradable.",
  "additional_info": "Compostable, plastic-free alternative"
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/category/generate" \
  -H "X-API-Key: rayeva_dev_key_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Bamboo Fiber Lunch Box",
    "description": "Eco-friendly lunch container made from natural bamboo fibers"
  }'
```

**Python Example**:
```python
import requests

url = "http://localhost:8000/api/v1/category/generate"
headers = {
    "X-API-Key": "rayeva_dev_key_12345",
    "Content-Type": "application/json"
}
data = {
    "product_name": "Bamboo Fiber Lunch Box",
    "description": "Eco-friendly lunch container made from natural bamboo fibers"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

**Response**:
```json
{
  "product_id": "prod_abc123",
  "product_name": "Bamboo Fiber Lunch Box",
  "primary_category": "Kitchen & Dining",
  "sub_category": "Food Storage",
  "seo_tags": [
    "bamboo lunch box",
    "biodegradable container",
    "eco friendly lunch box",
    "plastic-free food storage",
    "sustainable kitchen",
    "zero waste lunch"
  ],
  "sustainability_filters": [
    "biodegradable",
    "compostable",
    "natural-materials",
    "plastic-free"
  ],
  "confidence_score": 0.94,
  "processing_timestamp": "2026-03-04T10:15:30.123456",
  "database_id": "cat_xyz789"
}
```

### Retrieve Categorization

**Endpoint**: `GET /api/v1/category/{product_id}`

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/v1/category/prod_abc123" \
  -H "X-API-Key: rayeva_dev_key_12345"
```

### Batch Categorization

**Endpoint**: `POST /api/v1/category/batch`

**Request Body**:
```json
{
  "products": [
    {
      "product_name": "Bamboo Toothbrush",
      "description": "Sustainable toothbrush with bamboo handle and soft bristles"
    },
    {
      "product_name": "Reusable Cotton Bags",
      "description": "Set of 5 organic cotton shopping bags"
    }
  ]
}
```

---

## Module 2: AI B2B Proposal Generator

### Generate Proposal

**Endpoint**: `POST /api/v1/b2b/generate-proposal`

**Headers**:
```
X-API-Key: rayeva_dev_key_12345
Content-Type: application/json
```

**Request Body**:
```json
{
  "client_name": "GreenTech Corp",
  "budget_limit": 50000,
  "requirements": "Office supplies for 200 employees. Need notebooks, pens, water bottles, and lunch boxes. Focus on eliminating plastic waste.",
  "delivery_date": "2026-04-15",
  "priorities": ["plastic-free", "recycled-content", "local-sourcing"]
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/b2b/generate-proposal" \
  -H "X-API-Key: rayeva_dev_key_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "GreenTech Corp",
    "budget_limit": 50000,
    "requirements": "Office supplies for 200 employees",
    "priorities": ["plastic-free", "recycled-content"]
  }'
```

**Python Example**:
```python
import requests

url = "http://localhost:8000/api/v1/b2b/generate-proposal"
headers = {
    "X-API-Key": "rayeva_dev_key_12345",
    "Content-Type": "application/json"
}
data = {
    "client_name": "GreenTech Corp",
    "budget_limit": 50000,
    "requirements": "Office supplies for 200 employees, focus on plastic reduction",
    "priorities": ["plastic-free", "recycled-content"]
}

response = requests.post(url, json=data, headers=headers)
proposal = response.json()
print(f"Proposal ID: {proposal['proposal_id']}")
print(f"Total Cost: ${proposal['budget_allocation']['allocated']:,.2f}")
print(f"Products: {len(proposal['product_mix'])}")
```

**Response**:
```json
{
  "proposal_id": "prop_def456",
  "client_name": "GreenTech Corp",
  "generated_at": "2026-03-04T10:30:00Z",
  "product_mix": [
    {
      "product_id": "prod_001",
      "product_name": "Recycled Paper Notebooks (A5)",
      "quantity": 250,
      "unit_price": 12.50,
      "total_price": 3125.00,
      "sustainability_impact": "100% recycled content, saves trees",
      "category": "Office Supplies"
    },
    {
      "product_id": "prod_002",
      "product_name": "Bamboo Pen Set (Pack of 10)",
      "quantity": 25,
      "unit_price": 8.00,
      "total_price": 200.00,
      "sustainability_impact": "Plastic-free alternative, biodegradable",
      "category": "Office Supplies"
    },
    {
      "product_id": "prod_006",
      "product_name": "Stainless Steel Water Bottle (500ml)",
      "quantity": 200,
      "unit_price": 22.00,
      "total_price": 4400.00,
      "sustainability_impact": "Eliminates single-use plastic bottles",
      "category": "Kitchen & Dining"
    }
  ],
  "budget_allocation": {
    "total_budget": 50000,
    "allocated": 48725,
    "remaining": 1275,
    "utilization_percentage": 97.45
  },
  "cost_breakdown": {
    "products": 48725,
    "shipping": 0,
    "taxes": 0,
    "discount": 0
  },
  "impact_summary": {
    "plastic_avoided_kg": 1040.5,
    "trees_saved": 12,
    "carbon_offset_kg": 358.5,
    "local_suppliers_count": 2,
    "key_message": "This proposal eliminates 1040.5kg of plastic waste, saves 12 trees, supports 2 local suppliers"
  },
  "status": "draft"
}
```

### Get Proposal

**Endpoint**: `GET /api/v1/b2b/proposals/{proposal_id}`

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/v1/b2b/proposals/prop_def456" \
  -H "X-API-Key: rayeva_dev_key_12345"
```

### Update Proposal Status

**Endpoint**: `PUT /api/v1/b2b/proposals/{proposal_id}`

**Request Body**:
```json
{
  "status": "sent"
}
```

**cURL Example**:
```bash
curl -X PUT "http://localhost:8000/api/v1/b2b/proposals/prop_def456" \
  -H "X-API-Key: rayeva_dev_key_12345" \
  -H "Content-Type: application/json" \
  -d '{"status": "sent"}'
```

### List Proposals

**Endpoint**: `GET /api/v1/b2b/proposals`

**Query Parameters**:
- `client_name` (optional): Filter by client name
- `status` (optional): Filter by status
- `page` (optional, default: 1): Page number
- `page_size` (optional, default: 20): Results per page

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/v1/b2b/proposals?client_name=GreenTech&status=draft&page=1&page_size=10" \
  -H "X-API-Key: rayeva_dev_key_12345"
```

---

## Health Check & Monitoring

### Health Check

**Endpoint**: `GET /api/v1/health`

```bash
curl http://localhost:8000/api/v1/health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": 1709550930.123,
  "environment": "development",
  "database": "connected",
  "ai_service": "ready"
}
```

### Metrics

**Endpoint**: `GET /api/v1/metrics`

```bash
curl http://localhost:8000/api/v1/metrics
```

---

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Explore all available endpoints
- Test APIs directly from the browser
- View request/response schemas
- See example data

---

## Error Handling

### Common Error Responses

**401 Unauthorized** (Invalid API Key):
```json
{
  "error": "Invalid or missing API key",
  "status_code": 401
}
```

**400 Bad Request** (Validation Error):
```json
{
  "error": "Proposal exceeds budget: $55,000.00 > $50,000.00",
  "status_code": 400
}
```

**404 Not Found** (Resource Not Found):
```json
{
  "error": "Proposal not found: prop_invalid",
  "status_code": 404
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

---

## Rate Limiting

Current rate limit: **100 requests per minute** per API key.

Exceeding the rate limit will result in a `429 Too Many Requests` response.

---

## Best Practices

### 1. API Key Management
- Store API keys securely in environment variables
- Never commit API keys to version control
- Rotate API keys regularly

### 2. Error Handling
- Always check response status codes
- Implement retry logic with exponential backoff
- Log errors for debugging

### 3. Request Optimization
- Use batch endpoints when processing multiple items
- Cache frequently accessed data
- Monitor API usage to avoid rate limits

### 4. Data Validation
- Validate input data before sending requests
- Handle validation errors gracefully
- Provide clear error messages to users

---

## Support

For issues or questions:
- Check logs in `logs/` directory
- Review API documentation at `/docs`
- Verify environment configuration in `.env`

---

**Built for Rayeva AI Systems Assignment**
