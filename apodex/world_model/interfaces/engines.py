from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from apodex.world_model.domain.entities import Entity
from apodex.world_model.domain.relationships import Relationship
from apodex.world_model.domain.beliefs import Belief
from apodex.world_model.domain.timelines import Timeline, WorldGraphDelta
from apodex.world_model.domain.cognition import CognitiveProfile, AudienceCohort
from apodex.world_model.domain.environments import EnvironmentVector
from apodex.world_model.domain.simulation import SimulationRunContext


class IRealityEngine(ABC):
    """1. Ingests real-world metrics, updates facts, and computes trend correlations."""

    @abstractmethod
    async def ingest_stream(self, source_url: str, raw_payload: str) -> List[WorldGraphDelta]:
        """Parse external stream payloads and generate graph modifications."""
        pass

    @abstractmethod
    async def assert_belief(self, target_id: UUID, initial_probability: float, evidence: List[str]) -> Belief:
        """Create or update a Bayesian belief node with explicit evidence tracking."""
        pass


class IWorldSimulationEngine(ABC):
    """2. Models non-linear temporal dynamics, timeline branching, rollbacks, and causal consistency."""

    @abstractmethod
    async def create_branch(self, parent_timeline_id: UUID, name: str, branch_time: datetime) -> Timeline:
        """Initialize an isolated timeline branch representing a hypothetical scenario."""
        pass

    @abstractmethod
    async def step_simulation(self, context: SimulationRunContext) -> List[WorldGraphDelta]:
        """Advance a timeline simulation forward and return the resulting graph updates."""
        pass


class IHumanCognitionEngine(ABC):
    """3. Simulates human attention, emotions, motivation, biases, and choice dynamics."""

    @abstractmethod
    async def project_behavior(self, profile: CognitiveProfile, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """Compute predicted human actions, belief mutations, and emotional responses."""
        pass


class IAudienceIntelligenceEngine(ABC):
    """4. Models aggregate cohort trends, cultural adaptation, language shifts, and content fatigue."""

    @abstractmethod
    async def update_cohort_state(self, cohort_id: str, feedback_signals: Dict[str, Any]) -> AudienceCohort:
        """Process real-world audience metrics to adjust aggregate cohort parameters."""
        pass

    @abstractmethod
    async def calculate_fatigue(self, cohort: AudienceCohort, asset_id: UUID) -> float:
        """Estimate the content fatigue level for a specific creative asset."""
        pass


class ICreativeIntelligenceEngine(ABC):
    """5. Scores concept candidates prior to asset generation to optimize conversion and metrics."""

    @abstractmethod
    async def evaluate_candidate(self, concept_id: UUID, target_cohort_ids: List[str]) -> Dict[str, float]:
        """Pre-evaluate creative scores (engagement, conversion, risk, memorability)."""
        pass


class IGenerativeMediaEngine(ABC):
    """6. Model-agnostic media asset orchestration layer (images, video, sound, editing)."""

    @abstractmethod
    async def compile_generation_plan(self, concept_id: UUID, formats: List[str]) -> Dict[str, Any]:
        """Compile execution nodes, constraints, and route configurations."""
        pass

    @abstractmethod
    async def execute_generation(self, plan_id: UUID) -> List[Dict[str, Any]]:
        """Coordinate with external LLMs and graphics APIs to render assets."""
        pass


class IDistributionIntelligenceEngine(ABC):
    """7. Optimizes platform distribution, dynamic scheduling, and cross-channel optimization."""

    @abstractmethod
    async def recommend_strategy(self, asset_ids: List[UUID]) -> Dict[str, Any]:
        """Generate optimal publication schedule, localization and distribution plans."""
        pass


class IEconomicIntelligenceEngine(ABC):
    """8. Projects CAC, LTV, pricing elasticities, and capital/R&D allocations."""

    @abstractmethod
    async def simulate_economics(self, scenario_id: UUID, budget_usd: float) -> Dict[str, float]:
        """Evaluate unit economics, capital yields, and opportunity costs."""
        pass


class IEvolutionEngine(ABC):
    """9. Optimizes prompts, strategies, and heuristics without catastrophic forgetting."""

    @abstractmethod
    async def optimize_heuristics(self, performance_metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run continual learning updates over prompt configurations and model routing rules."""
        pass


class IMetaWorldEngine(ABC):
    """10. Civilization-scale model tracking geopolitical shifts, fashion trends, and cultural waves."""

    @abstractmethod
    async def get_global_context(self) -> EnvironmentVector:
        """Fetch civilization-level context frame and risk variables."""
        pass
