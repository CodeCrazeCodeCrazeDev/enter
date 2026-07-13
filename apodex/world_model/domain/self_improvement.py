from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class EngineeringFinding(BaseModel):
    """An audit finding, code smell, security risk, or performance bottleneck."""
    finding_id: UUID = Field(default_factory=uuid4)
    severity: str = "MEDIUM"  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    category: str  # "CODE_SMELL", "SECURITY_VULNERABILITY", "PERFORMANCE", "CIRCULAR_DEPENDENCY"
    file_path: str
    line_number: Optional[int] = None
    description: str
    suggested_fix: str
    detected_at: datetime = Field(default_factory=datetime.utcnow)


class BenchmarkReport(BaseModel):
    """Execution benchmarking comparing before vs after states on key dimensions."""
    report_id: UUID = Field(default_factory=uuid4)
    latency_delta_ms: float = 0.0
    token_cost_delta_usd: float = 0.0
    accuracy_score_delta: float = 0.0
    maintainability_index_delta: float = 0.0
    is_regression: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)


class SelfImprovementProposal(BaseModel):
    """An engineering change recommendation compiled by the multi-agent flywheel."""
    proposal_id: UUID = Field(default_factory=uuid4)
    title: str
    summary: str
    research_citations: List[str] = Field(default_factory=list)
    proposed_diff: str
    risks_analysis: str
    rollback_instructions: str
    status: str = "DRAFT"  # "DRAFT", "EVALUATED", "APPROVED", "REJECTED"
    associated_finding_id: Optional[UUID] = None
    benchmark_report: Optional[BenchmarkReport] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    reviewed_at: Optional[datetime] = None


class AgentRoleMetadata(BaseModel):
    """Metadata describing a specialized engineering agent in the flywheel."""
    role_id: str
    agent_name: str
    focus_areas: List[str] = Field(default_factory=list)
    active_policies: List[str] = Field(default_factory=list)
