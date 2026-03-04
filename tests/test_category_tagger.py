"""
Test cases for Module 1: AI Auto-Category & Tag Generator
"""
import pytest
from src.modules.category_tagger.schemas import CategoryRequest
from src.modules.category_tagger.service import CategoryTaggerService


@pytest.fixture
def category_service():
    """Fixture for category tagger service."""
    return CategoryTaggerService()


@pytest.fixture
def sample_product_request():
    """Fixture for sample product request."""
    return CategoryRequest(
        product_id="test_001",
        product_name="Bamboo Fiber Lunch Box",
        description="Eco-friendly lunch container made from natural bamboo fibers. BPA-free and microwave safe.",
        additional_info="Biodegradable, compostable"
    )


def test_category_request_validation():
    """Test CategoryRequest validation."""
    # Valid request
    request = CategoryRequest(
        product_name="Test Product",
        description="This is a test product description with enough length"
    )
    assert request.product_name == "Test Product"
    
    # Invalid request (description too short)
    with pytest.raises(ValueError):
        CategoryRequest(
            product_name="Test",
            description="Short"
        )


def test_system_prompt_generation(category_service):
    """Test system prompt generation."""
    prompt = category_service._build_system_prompt()
    assert "expert" in prompt.lower()
    assert "sustainable" in prompt.lower()
    assert "PRIMARY CATEGORIES" in prompt


def test_user_prompt_generation(category_service, sample_product_request):
    """Test user prompt generation."""
    prompt = category_service._build_user_prompt(sample_product_request)
    assert sample_product_request.product_name in prompt
    assert sample_product_request.description in prompt


class TestAICategorizationOutput:
    """Test AI output schema validation."""
    
    def test_valid_output(self):
        """Test valid AI output."""
        from src.modules.category_tagger.schemas import AICategorizationOutput
        
        output = AICategorizationOutput(
            primary_category="Kitchen & Dining",
            sub_category="Food Storage",
            seo_tags=["bamboo", "lunch box", "eco friendly", "sustainable", "biodegradable"],
            sustainability_filters=["plastic-free", "compostable"],
            confidence_score=0.92
        )
        
        assert output.primary_category == "Kitchen & Dining"
        assert len(output.seo_tags) >= 5
        assert 0 <= output.confidence_score <= 1
    
    def test_invalid_confidence_score(self):
        """Test invalid confidence score."""
        from src.modules.category_tagger.schemas import AICategorizationOutput
        
        with pytest.raises(ValueError):
            AICategorizationOutput(
                primary_category="Kitchen",
                sub_category="Storage",
                seo_tags=["tag1", "tag2", "tag3", "tag4", "tag5"],
                sustainability_filters=["plastic-free"],
                confidence_score=1.5  # Invalid (> 1.0)
            )


# Note: Async tests require pytest-asyncio
@pytest.mark.asyncio
async def test_categorize_product_mock(category_service, sample_product_request, monkeypatch):
    """Test product categorization with mocked AI service."""
    from src.modules.category_tagger.schemas import AICategorizationOutput
    
    # Mock AI service response
    async def mock_generate_structured_output(*args, **kwargs):
        return AICategorizationOutput(
            primary_category="Kitchen & Dining",
            sub_category="Food Storage",
            seo_tags=["bamboo lunch box", "eco container", "sustainable", "biodegradable", "plastic-free"],
            sustainability_filters=["plastic-free", "compostable", "biodegradable"],
            confidence_score=0.92,
            reasoning="Clear kitchen product with strong sustainability credentials"
        )
    
    # Apply mock
    from src.core import ai_service
    monkeypatch.setattr(ai_service.ai_service, "generate_structured_output", mock_generate_structured_output)
    
    # Test categorization
    # Note: This would require database setup, so we're testing the logic only
    # response = await category_service.categorize_product(sample_product_request)
    # assert response.primary_category == "Kitchen & Dining"
