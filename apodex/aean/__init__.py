"""AEAN — Autonomous Economic Actor Network.

A runnable implementation of the AEAN "unified economic organism": an Economic
Knowledge Graph (EKG) substrate, four economic engines (PAEAN, ADE, ARE, AVIE),
two coordination systems (Hive Mind, Research), a constitutional governance
layer, and the compounding flywheel that ties them together.

Quick start::

    from apodex.aean import Organism

    organism = Organism(initial_capital_cents=100_000_00, seed=7)
    organism.run(cycles=20)
    print(organism.snapshot()["cumulative_roi"])
"""
from __future__ import annotations

from .coordination.hive_mind import HiveMind
from .coordination.research import ResearchEngine
from .ekg import EconomicKnowledgeGraph
from .engines.ade import AutonomousDemandEngine
from .engines.are import AutonomousRevenueEngine
from .engines.avie import AutonomousVisualIntelligenceEngine
from .engines.paean import PAEAN, ThompsonBandit
from .flywheel import Organism
from .governance import ConstitutionalFilter, ConstitutionalRules
from .llm import LLMAdapter

__all__ = [
    "Organism",
    "EconomicKnowledgeGraph",
    "PAEAN",
    "ThompsonBandit",
    "AutonomousDemandEngine",
    "AutonomousRevenueEngine",
    "AutonomousVisualIntelligenceEngine",
    "HiveMind",
    "ResearchEngine",
    "ConstitutionalFilter",
    "ConstitutionalRules",
    "LLMAdapter",
]
