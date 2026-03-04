# B2B Proposal module initialization
from .service import b2b_proposal_service
from .schemas import ProposalRequest, ProposalResponse

__all__ = ["b2b_proposal_service", "ProposalRequest", "ProposalResponse"]
