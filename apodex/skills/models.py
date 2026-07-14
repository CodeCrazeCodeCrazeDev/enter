from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class KnowledgeType(str, Enum):
    """Specifies whether the knowledge is stable/long-term or fast-changing/live."""
    EVERGREEN = "EVERGREEN"
    DECAYING = "DECAYING"


class CostTier(str, Enum):
    """Specifies the cost tier for execution, matching the framework's tier structures."""
    CHEAP = "CHEAP"
    EXPENSIVE = "EXPENSIVE"


class BusinessSkill(BaseModel):
    """Schema defining a specific operational or cognitive capability."""
    name: str
    domain: str
    description: str
    knowledge_type: KnowledgeType
    cost_tier: CostTier = CostTier.CHEAP
    base_cost_credits: int = 10
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)


class ProtocolStep(BaseModel):
    """A single step in a declarative protocol chain."""
    skill_name: str
    parameter_mappings: Dict[str, str] = Field(default_factory=dict)
    # E.g., {"product_id": "step_0.product_id"} to wire outputs to subsequent inputs.


class BusinessProtocol(BaseModel):
    """Declarative chain or pipeline of multiple business skills."""
    name: str
    description: str
    steps: List[ProtocolStep] = Field(default_factory=list)
    budget_cap_credits: int
    downshift_enabled: bool = True
    halt_on_failure: bool = True


class SkillExecutionLog(BaseModel):
    """Immutable audit trail for executions of a business skill."""
    log_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    tenant_id: str
    venture_id: str
    skill_name: str
    protocol_name: Optional[str] = None
    step_index: Optional[int] = None
    cost_estimated: int
    cost_actual: int
    tier_used: CostTier
    status: str  # SUCCESS, REJECTED, INFRA_ERROR, BUDGET_HALTED
    output_payload: Dict[str, Any] = Field(default_factory=dict)
    anchors_hit: List[str] = Field(default_factory=list)
    metrics_lift: Dict[str, float] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SkillScorecard(BaseModel):
    """Aggregated performance metrics and ROI scores for a business skill."""
    skill_name: str
    success_count: int = 0
    failure_count: int = 0
    average_cost_actual: float = 0.0
    average_lift: Dict[str, float] = Field(default_factory=dict)


class ProtocolScorecard(BaseModel):
    """Aggregated performance scorecard for a full playbook / protocol."""
    protocol_name: str
    success_count: int = 0
    failure_count: int = 0
    average_cost_actual: float = 0.0
