from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class StepSpec(BaseModel):
    step_id: str
    skill_name: str
    input_mapping: Dict[str, str] = Field(default_factory=dict)
    output_mapping: Dict[str, str] = Field(default_factory=dict)
    anchors_to_hit: List[str] = Field(default_factory=list)


class ProtocolSpec(BaseModel):
    protocol_id: str
    name: str
    steps: List[StepSpec] = Field(default_factory=list)

    # Adaptive / Progress Config overrides
    k_steps: int = 5
    downshift_after_steps_without_progress: int = 3
    halt_after_steps_without_progress: int = 5
    progress_rate_threshold: float = 0.2
