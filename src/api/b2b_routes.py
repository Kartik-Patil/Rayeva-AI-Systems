"""
API routes for Module 2: AI B2B Proposal Generator
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional

from ..modules.b2b_proposal.schemas import (
    ProposalRequest,
    ProposalResponse,
    ProposalUpdateRequest,
    ProposalListResponse
)
from ..modules.b2b_proposal.service import b2b_proposal_service


router = APIRouter(prefix="/api/v1/b2b", tags=["B2B Proposals"])


@router.post("/generate-proposal", response_model=ProposalResponse, status_code=status.HTTP_201_CREATED)
async def generate_proposal(request: ProposalRequest):
    """
    Generate AI-powered B2B proposal with product recommendations.
    
    - **client_name**: Name of the client company (required)
    - **budget_limit**: Maximum budget in currency units (required)
    - **requirements**: Client requirements and needs (required)
    - **delivery_date**: Expected delivery date (optional)
    - **priorities**: Sustainability priorities (optional)
    
    Returns complete proposal with product mix, budget allocation, and impact summary.
    """
    try:
        return await b2b_proposal_service.generate_proposal(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate proposal: {str(e)}"
        )


@router.get("/proposals/{proposal_id}", response_model=ProposalResponse)
async def get_proposal(proposal_id: str):
    """
    Retrieve a specific proposal by ID.
    
    - **proposal_id**: Unique proposal identifier
    
    Returns the complete proposal or 404 if not found.
    """
    result = await b2b_proposal_service.get_proposal(proposal_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal not found: {proposal_id}"
        )
    
    return result


@router.put("/proposals/{proposal_id}", response_model=dict)
async def update_proposal_status(proposal_id: str, request: ProposalUpdateRequest):
    """
    Update the status of a proposal.
    
    - **proposal_id**: Unique proposal identifier
    - **status**: New status (draft, sent, accepted, rejected)
    
    Returns success message or 404 if proposal not found.
    """
    # Validate status
    valid_statuses = ["draft", "sent", "accepted", "rejected"]
    if request.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    success = await b2b_proposal_service.update_proposal_status(proposal_id, request.status)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal not found: {proposal_id}"
        )
    
    return {
        "message": "Proposal status updated successfully",
        "proposal_id": proposal_id,
        "new_status": request.status
    }


@router.get("/proposals", response_model=ProposalListResponse)
async def list_proposals(
    client_name: Optional[str] = Query(None, description="Filter by client name"),
    status: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Results per page")
):
    """
    List all proposals with optional filters and pagination.
    
    - **client_name**: Filter by client name (partial match)
    - **status**: Filter by status (exact match)
    - **page**: Page number (default: 1)
    - **page_size**: Results per page (default: 20, max: 100)
    
    Returns paginated list of proposals.
    """
    return await b2b_proposal_service.list_proposals(
        client_name=client_name,
        status=status,
        page=page,
        page_size=page_size
    )
