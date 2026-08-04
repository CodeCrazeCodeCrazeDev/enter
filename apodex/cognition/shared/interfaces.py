from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from apodex.cognition.shared.schemas import (
    CognitiveContext,
    Recommendation,
    VerificationResult,
    HealthStatus,
    Lesson
)


class ICognitiveModule(ABC):
    """
    Uniform Interface exposed by every single module inside the Cognitive Operating System.
    This architecture rule simplifies orchestration, testing, and replacement.
    """

    @abstractmethod
    async def observe(self, context: CognitiveContext, data: Dict[str, Any]) -> None:
        """Observe environmental, user, or execution data and update module state/context."""
        pass

    @abstractmethod
    async def analyze(self, context: CognitiveContext) -> Dict[str, Any]:
        """Analyze the current context to identify gaps, risks, or opportunities."""
        pass

    @abstractmethod
    async def plan(self, context: CognitiveContext) -> Optional[Any]:
        """Create plans, strategic structures, or procedural workflows depending on module role."""
        pass

    @abstractmethod
    async def recommend(self, context: CognitiveContext) -> List[Recommendation]:
        """Provide candidate recommendations with associated confidence levels."""
        pass

    @abstractmethod
    async def verify(self, context: CognitiveContext) -> VerificationResult:
        """Verify the integrity, safety, consistency, or compliance of the current context/action."""
        pass

    @abstractmethod
    async def learn(self, context: CognitiveContext, lessons: List[Lesson]) -> None:
        """Absorb outcome results or distilled insights to optimize internal heuristics/policies."""
        pass

    @abstractmethod
    async def health(self) -> HealthStatus:
        """Report execution health, cache metrics, latency percentiles, and errors."""
        pass


# =====================================================================
# Canonical 5-Plane Cognitive Subsystem Interfaces (Decoupled Abstractions)
# =====================================================================

class IStrategicPlanner(ABC):
    """Canonical Interface for L8 Planning Layer (Control Plane)."""
    @abstractmethod
    async def create_roadmap(self, overall_goal: str) -> Any:
        """Decompose a high-level goal recursively into sequentially verified steps."""
        pass


class ICausalWorldModel(ABC):
    """Canonical Interface for L6 World Model Layer (Cognitive Plane)."""
    @abstractmethod
    async def run_causal_inference(self, cause_id: str, effect_id: str) -> float:
        """Calculate transition probabilities and intervention effects using causal do-calculus."""
        pass


class IUnifiedMemoryService(ABC):
    """Canonical Interface for L5 Memory Layer (Cognitive Plane)."""
    @abstractmethod
    async def store_episode(self, episode_id: str, trajectory: Any) -> None:
        """Durable persistence of planning and execution episodes across sessions."""
        pass


class IExecutionEngine(ABC):
    """Canonical Interface for L11 Execution Layer (Execution Plane)."""
    @abstractmethod
    async def dispatch_isolated_task(self, step_id: str, action: Any) -> Any:
        """Orchestrate worker agents to execute an isolated tool call / command."""
        pass


class IEvaluationEngine(ABC):
    """Canonical Interface for L12 Evaluation Layer (Control Plane)."""
    @abstractmethod
    def assign_credit(self, trajectory: Any, is_success: bool) -> Any:
        """Execute step-level credit assignment over completed traces."""
        pass


class ISelfImprovementEngine(ABC):
    """Canonical Interface for L13 Self-Improvement Layer (Control Plane)."""
    @abstractmethod
    async def mine_weaknesses(self, episodes: List[Any]) -> List[Dict[str, Any]]:
        """Extract bottleneck trace signatures and propose prompt/parameter optimizations."""
        pass


class IGovernanceGateway(ABC):
    """Canonical Interface for L14 Governance Layer (Control Plane)."""
    @abstractmethod
    def check_invariant(self, proposed_action: Any) -> Any:
        """Audit candidate actions against system-wide immutable safety constraints."""
        pass


class IScheduler(ABC):
    """Canonical Interface for Core Control Plane Task Scheduling."""
    @abstractmethod
    async def schedule_task(self, task_id: str, dependency_dag: Any) -> Any:
        """Topological sequencing and resource-constrained scheduling of DAG jobs."""
        pass
