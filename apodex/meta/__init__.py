"""
Apodex self-improving meta-layer components.
"""

from __future__ import annotations

from apodex.meta.experience_db import (
    ExecutionTrace,
    FailureSignature,
    DistilledLesson,
    ExperienceDatabase,
)
from apodex.meta.safety_manager import (
    DiffProposal,
    ValidationReport,
    SafetyGuardrailManager,
)
from apodex.meta.harness_loop import HarnessLoopController
from apodex.meta.research_loop import (
    TrialConfig,
    TrialResult,
    ResearchLoopController,
)

__all__ = [
    "ExecutionTrace",
    "FailureSignature",
    "DistilledLesson",
    "ExperienceDatabase",
    "DiffProposal",
    "ValidationReport",
    "SafetyGuardrailManager",
    "HarnessLoopController",
    "TrialConfig",
    "TrialResult",
    "ResearchLoopController",
]
