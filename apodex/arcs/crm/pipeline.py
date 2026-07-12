from __future__ import annotations
import logging
import uuid
from typing import Any, Dict, List
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.crm.pipeline")


class CRMLead(BaseModel):
    lead_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: str
    company_name: str
    stage: str = "lead"  # lead, qualified, proposal, closed, lost
    budget_cents: int
    score: float = 0.0
    needs: List[str] = Field(default_factory=list)


class CRMPipeline:
    """Enterprise-grade CRM pipeline tracking customer acquisition states and qualified scoring."""

    def __init__(self) -> None:
        self.leads: Dict[uuid.UUID, CRMLead] = {}

    def register_lead(self, email: str, company: str, budget_cents: int, needs: List[str]) -> CRMLead:
        lead = CRMLead(email=email, company_name=company, budget_cents=budget_cents, needs=needs)
        self.leads[lead.lead_id] = lead
        logger.info(f"[CRM] Registered lead: {company} ({email}) - Budget: {budget_cents} cents")
        return lead

    def score_lead(self, lead_id: uuid.UUID) -> float:
        if lead_id not in self.leads:
            raise KeyError("Lead not found.")

        lead = self.leads[lead_id]
        score = 0.0

        # Score based on budget criteria
        if lead.budget_cents >= 1000000:  # $10k+
            score += 0.5
        elif lead.budget_cents >= 100000:  # $1k+
            score += 0.3

        # Score based on defined requirements/needs alignment
        if lead.needs:
            score += min(0.5, len(lead.needs) * 0.15)

        lead.score = score
        logger.info(f"[CRM] Scored Lead '{lead.company_name}': {score:.2f}")

        # Auto-promote to qualified if score crosses threshold
        if score >= 0.50:
            lead.stage = "qualified"
            logger.info(f"[CRM] Auto-qualified Lead '{lead.company_name}'")

        return score

    def transition_stage(self, lead_id: uuid.UUID, new_stage: str) -> None:
        if lead_id not in self.leads:
            raise KeyError("Lead not found.")
        allowed_stages = ["lead", "qualified", "proposal", "closed", "lost"]
        if new_stage not in allowed_stages:
            raise ValueError(f"Invalid CRM stage: {new_stage}")

        lead = self.leads[lead_id]
        logger.info(f"[CRM] Transitioning '{lead.company_name}': {lead.stage} -> {new_stage}")
        lead.stage = new_stage
