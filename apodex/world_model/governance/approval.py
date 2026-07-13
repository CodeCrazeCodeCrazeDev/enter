from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ApprovalRequest(BaseModel):
    """An escalation requesting human authorization for a high-risk or policy-violating action."""
    request_id: UUID = Field(default_factory=uuid4)
    tenant_id: str
    stage: int  # 1: Advisory, 2: Supervised, 3: Autonomous, 4: Strategic
    payload_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    reason: str
    status: str = "PENDING"  # "PENDING", "APPROVED", "REJECTED"
    reviewer_id: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    cryptographic_signature: Optional[str] = None

    def approve(self, reviewer_id: str, signature: str) -> None:
        """Approve and sign off on this escalation."""
        self.status = "APPROVED"
        self.reviewer_id = reviewer_id
        self.reviewed_at = datetime.utcnow()
        self.cryptographic_signature = signature
