"""Command schemas for orchestrating state transitions within the AI-EOS operating system."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class DomainCommand(BaseModel):
    """Base schema for all domain commands in AI-EOS."""
    command_id: UUID = Field(default_factory=uuid4)


class CreateVentureCellCommand(DomainCommand):
    name: str
    namespace: str
    allocated_capital_cents: int


class RegisterHypothesisCommand(DomainCommand):
    title: str
    description: str
    null_hypothesis: str
    target_metric: str
    significance_alpha: float = 0.05


class ExecuteExperimentCommand(DomainCommand):
    hypothesis_id: UUID
    seed: int = 42


class RunPortfolioOptimizationCommand(DomainCommand):
    available_capital_cents: int
