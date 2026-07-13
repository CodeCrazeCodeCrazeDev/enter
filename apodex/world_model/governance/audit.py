from __future__ import annotations
from datetime import datetime
from hashlib import sha256
from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class AuditLedgerBlock(BaseModel):
    """An immutable, cryptographically chained record block inside the system audit log."""
    block_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    actor_id: str
    action: str
    payload_hash: str
    previous_block_hash: str
    current_block_hash: str


class ImmutableAuditLedger:
    """Manages appending and cryptographically linking audit log records."""

    def __init__(self) -> None:
        self.chain: List[AuditLedgerBlock] = []

    def append_record(self, actor_id: str, action: str, payload: Dict[str, Any]) -> AuditLedgerBlock:
        """Appends a new securely hashed and chained block to the audit ledger."""
        payload_str = str(sorted(payload.items()))
        p_hash = sha256(payload_str.encode('utf-8')).hexdigest()

        prev_hash = "0" * 64
        if self.chain:
            prev_hash = self.chain[-1].current_block_hash

        block_str = f"{actor_id}{action}{p_hash}{prev_hash}"
        curr_hash = sha256(block_str.encode('utf-8')).hexdigest()

        block = AuditLedgerBlock(
            actor_id=actor_id,
            action=action,
            payload_hash=p_hash,
            previous_block_hash=prev_hash,
            current_block_hash=curr_hash
        )
        self.chain.append(block)
        return block
