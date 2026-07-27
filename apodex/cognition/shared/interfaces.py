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
