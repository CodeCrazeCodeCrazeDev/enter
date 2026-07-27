"""Scientific Discovery & Agent Evolution Engines for EIOS.

Enables continuous hypothesis discovery, RCT conjoint designs, and genetic
agent tournaments to mutate and select the best policies.
"""

from __future__ import annotations

from .scientific_discovery import ScientificDiscoveryEngine, Hypothesis, ScientificTheory
from .agent_evolution import AgentEvolutionEngine, EvolvingAgent

__all__ = [
    "ScientificDiscoveryEngine",
    "Hypothesis",
    "ScientificTheory",
    "AgentEvolutionEngine",
    "EvolvingAgent"
]
