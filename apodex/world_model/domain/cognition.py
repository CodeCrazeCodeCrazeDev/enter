from __future__ import annotations
from typing import Dict, List
from pydantic import BaseModel, Field


class CognitiveProfile(BaseModel):
    """Psychological configuration and current emotional state of simulated actors."""
    attention_matrix: Dict[str, float] = Field(default_factory=dict)  # Attention weights per topic [0, 1]
    belief_vector: Dict[str, float] = Field(default_factory=dict)  # Personal belief alignments
    emotional_state: Dict[str, float] = Field(default_factory=dict)  # Basic Plutchik emotion scales
    cognitive_biases: Dict[str, float] = Field(default_factory=dict)  # Active biases & thresholds
    value_system: List[str] = Field(default_factory=list)  # Prioritized values list


class AudienceCohort(BaseModel):
    """Aggregate target community segment modeling demographics and attention dynamics."""
    cohort_id: str
    name: str
    demographics: Dict[str, str] = Field(default_factory=dict)
    psychographics: List[str] = Field(default_factory=list)
    content_fatigue_curves: Dict[str, float] = Field(default_factory=dict)
    trust_matrices: Dict[str, float] = Field(default_factory=dict)
