from __future__ import annotations
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class EngineConfig(BaseModel):
    """Configuration options for a single WMC Engine."""
    enabled: bool = True
    execution_tier: str = "CHEAP"  # "CHEAP" or "EXPENSIVE"
    model_provider: str = "openai"
    model_name: str = "gpt-4o-mini"
    max_retries: int = 3
    timeout_seconds: float = 30.0
    extra_params: Dict[str, str] = Field(default_factory=dict)


class RealityEngineConfig(EngineConfig):
    """Specific configuration for the Reality Engine."""
    ingestion_sources: List[str] = Field(default_factory=list)
    credibility_threshold: float = 0.7
    auto_assert_beliefs: bool = False


class SimulationEngineConfig(EngineConfig):
    """Specific configuration for the Simulation Engine."""
    max_timeline_depth: int = 100
    parallel_execution_limit: int = 10
    default_step_size_hours: float = 24.0
    enable_causal_validation: bool = True


class CognitiveEngineConfig(EngineConfig):
    """Specific configuration for the Human Cognition Engine."""
    enable_cognitive_biases: bool = True
    simulated_agents_limit: int = 500
    precision_scale: float = 1.0


class AudienceEngineConfig(EngineConfig):
    """Specific configuration for the Audience Intelligence Engine."""
    tracking_cohorts: List[str] = Field(default_factory=list)
    fatigue_decay_constant: float = 0.05
    attention_window_hours: float = 72.0


class MediaEngineConfig(EngineConfig):
    """Specific configuration for the Generative Media Engine."""
    image_model: str = "flux-dev"
    video_model: str = "luma-dream-machine"
    audio_model: str = "elevenlabs"
    rendering_max_cost_usd: float = 10.0


class GovernanceConfig(BaseModel):
    """Configuration for WMC security and governance protocols."""
    enforce_tenant_isolation: bool = True
    ethical_filter_enabled: bool = True
    legal_compliance_enabled: bool = True
    brand_integrity_enabled: bool = True
    human_approval_stage: int = 2  # 1: Advisory, 2: Supervised, 3: Autonomous, 4: Strategic
    audit_trail_immutable: bool = True


class WorldModelCreatorConfig(BaseModel):
    """Global configuration for the World Model Creator suite."""
    tenant_id: str
    active_environment: str = "development"
    debug_mode: bool = False
    max_budget_limit_usd: float = 100.0

    # Engine Configs
    reality_engine: RealityEngineConfig = Field(default_factory=RealityEngineConfig)
    simulation_engine: SimulationEngineConfig = Field(default_factory=SimulationEngineConfig)
    cognitive_engine: CognitiveEngineConfig = Field(default_factory=CognitiveEngineConfig)
    audience_engine: AudienceEngineConfig = Field(default_factory=AudienceEngineConfig)
    media_engine: MediaEngineConfig = Field(default_factory=MediaEngineConfig)

    governance: GovernanceConfig = Field(default_factory=GovernanceConfig)
