"""
Test cases for Module 2: AI B2B Proposal Generator
"""
import pytest
from src.modules.b2b_proposal.schemas import ProposalRequest, ProductItem
from src.modules.b2b_proposal.service import B2BProposalService
from src.modules.b2b_proposal.product_catalog import get_products_by_filter, calculate_product_impact


@pytest.fixture
def proposal_service():
    """Fixture for B2B proposal service."""
    return B2BProposalService()


@pytest.fixture
def sample_proposal_request():
    """Fixture for sample proposal request."""
    return ProposalRequest(
        client_name="GreenTech Corp",
        budget_limit=50000.0,
        requirements="Office supplies for 200 employees, focus on plastic reduction",
        priorities=["plastic-free", "recycled-content", "local-sourcing"]
    )


def test_proposal_request_validation():
    """Test ProposalRequest validation."""
    # Valid request
    request = ProposalRequest(
        client_name="Test Company",
        budget_limit=10000.0,
        requirements="Basic office supplies needed"
    )
    assert request.client_name == "Test Company"
    assert request.budget_limit == 10000.0
    
    # Invalid request (negative budget)
    with pytest.raises(ValueError):
        ProposalRequest(
            client_name="Test",
            budget_limit=-1000.0,
            requirements="Test requirements"
        )


def test_product_catalog_filtering():
    """Test product catalog filtering."""
    # Filter by max price
    affordable_products = get_products_by_filter(max_price=20.0)
    assert all(p["unit_price"] <= 20.0 for p in affordable_products)
    
    # Filter by category
    office_products = get_products_by_filter(categories=["Office Supplies"])
    assert all(p["category"] == "Office Supplies" for p in office_products)
    
    # Filter by sustainability priorities
    plastic_free = get_products_by_filter(
        sustainability_priorities=["plastic-free"]
    )
    assert len(plastic_free) > 0


def test_impact_calculation():
    """Test product impact calculation."""
    sample_product = {
        "product_id": "test_001",
        "sustainability": {
            "plastic_avoided_per_year_kg": 5.0,
            "trees_saved_per_unit": 0.05,
            "carbon_offset_g": 150,
            "local_sourcing": True
        }
    }
    
    impact = calculate_product_impact(sample_product, quantity=10)
    
    assert impact["plastic_avoided_kg"] == 50.0
    assert impact["trees_saved"] == 0.5
    assert impact["carbon_offset_kg"] == 1.5
    assert impact["is_local"] == True


def test_system_prompt_generation(proposal_service):
    """Test system prompt generation."""
    prompt = proposal_service._build_system_prompt()
    assert "B2B" in prompt
    assert "sustainability" in prompt.lower()
    assert "budget" in prompt.lower()


def test_budget_constraint_validation(proposal_service):
    """Test budget constraint validation."""
    from src.modules.b2b_proposal.schemas import AIProposalOutput, ProductItem
    
    # Valid proposal (within budget)
    valid_output = AIProposalOutput(
        product_mix=[
            ProductItem(
                product_id="prod_001",
                product_name="Test Product",
                quantity=10,
                unit_price=100.0,
                total_price=1000.0,
                sustainability_impact="Test impact"
            )
        ],
        total_cost=1000.0,
        impact_highlights=["Sustainable"]
    )
    
    assert proposal_service._validate_budget_constraint(valid_output, 1500.0) == True
    
    # Invalid proposal (exceeds budget)
    invalid_output = AIProposalOutput(
        product_mix=[
            ProductItem(
                product_id="prod_001",
                product_name="Test Product",
                quantity=10,
                unit_price=200.0,
                total_price=2000.0,
                sustainability_impact="Test impact"
            )
        ],
        total_cost=2000.0,
        impact_highlights=["Sustainable"]
    )
    
    assert proposal_service._validate_budget_constraint(invalid_output, 1500.0) == False


class TestProductItem:
    """Test ProductItem schema."""
    
    def test_valid_product_item(self):
        """Test valid product item creation."""
        item = ProductItem(
            product_id="prod_001",
            product_name="Test Product",
            quantity=5,
            unit_price=10.0,
            total_price=50.0,
            sustainability_impact="Reduces plastic waste"
        )
        
        assert item.quantity > 0
        assert item.unit_price > 0
        assert item.total_price == item.quantity * item.unit_price
    
    def test_invalid_quantity(self):
        """Test invalid quantity."""
        with pytest.raises(ValueError):
            ProductItem(
                product_id="prod_001",
                product_name="Test",
                quantity=0,  # Invalid
                unit_price=10.0,
                total_price=0.0,
                sustainability_impact="Test"
            )


# Note: Async tests require pytest-asyncio and database setup
@pytest.mark.asyncio
async def test_generate_proposal_mock(proposal_service, sample_proposal_request, monkeypatch):
    """Test proposal generation with mocked AI service."""
    from src.modules.b2b_proposal.schemas import AIProposalOutput, ProductItem
    
    # Mock AI service response
    async def mock_generate_structured_output(*args, **kwargs):
        return AIProposalOutput(
            product_mix=[
                ProductItem(
                    product_id="prod_001",
                    product_name="Recycled Paper Notebooks",
                    quantity=250,
                    unit_price=12.50,
                    total_price=3125.0,
                    sustainability_impact="100% recycled content"
                )
            ],
            total_cost=3125.0,
            impact_highlights=[
                "Reduces plastic waste",
                "Saves trees",
                "Supports local suppliers"
            ],
            reasoning="Selected products match sustainability priorities"
        )
    
    # Apply mock
    from src.core import ai_service
    monkeypatch.setattr(ai_service.ai_service, "generate_structured_output", mock_generate_structured_output)
    
    # Test would require database setup
    # response = await proposal_service.generate_proposal(sample_proposal_request)
    # assert response.client_name == "GreenTech Corp"
