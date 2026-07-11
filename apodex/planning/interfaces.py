from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IStrategicPlanner(ABC):
    """Interface for generating strategic milestone roadmaps and resource allocation requirements."""

    @abstractmethod
    async def generate_strategies(self, goal: str, constraints: Dict[str, Any]) -> List[Any]:
        """Generate alternative execution plans to satisfy a high-level strategic target."""
        pass

    @abstractmethod
    async def optimize_plan(self, plan: Any, feedback: Dict[str, Any]) -> Any:
        """Refine and adjust plan parameters based on execution metrics or historical learning."""
        pass
