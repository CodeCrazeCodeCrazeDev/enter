from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IEconomicReasoningEngine(ABC):
    """Interface for evaluating trade-offs, opportunity costs, and expected utilities."""

    @abstractmethod
    def evaluate_expected_utility(self, strategy: Any, market_conditions: Dict[str, Any]) -> float:
        """Compute the expected utility (EV) of a given strategy under specific market parameters."""
        pass

    @abstractmethod
    def compute_opportunity_cost(self, chosen: Any, alternatives: List[Any]) -> float:
        """Calculate the opportunity cost of selecting a chosen strategy relative to alternatives."""
        pass


class IMarketSimulator(ABC):
    """Interface for sandbox-testing strategies against simulated competitors and market dynamics."""

    @abstractmethod
    async def simulate_market_run(self, strategy: Any, agent_count: int) -> Dict[str, Any]:
        """Execute a Monte Carlo simulation run for a business or marketing strategy."""
        pass
