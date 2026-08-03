"""Interfaces for the AlphaAlgo Research Operating System (Research OS).

Defines stable, decoupled interface contracts for each stage of the canonical
research pipeline lifecycle.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .models import (
    Hypothesis,
    Dataset,
    Feature,
    Experiment,
    Model,
    ValidationReport,
    DecisionRecord,
)


class IHypothesisRegistry(ABC):
    """Interface for registering and managing scientific hypotheses."""

    @abstractmethod
    def register_hypothesis(self, hypothesis: Hypothesis) -> None:
        """Register a new hypothesis under a unique ID."""
        ...

    @abstractmethod
    def get_hypothesis(self, hypothesis_id: str) -> Optional[Hypothesis]:
        """Retrieve a registered hypothesis by ID."""
        ...

    @abstractmethod
    def list_hypotheses(self) -> List[Hypothesis]:
        """List all registered hypotheses."""
        ...


class IDatasetRegistry(ABC):
    """Interface for registering and versioning raw and processed datasets."""

    @abstractmethod
    def register_dataset(self, dataset: Dataset) -> None:
        """Register a new dataset snapshot with temporal verification."""
        ...

    @abstractmethod
    def get_dataset(self, dataset_id: str) -> Optional[Dataset]:
        """Retrieve a registered dataset by ID."""
        ...


class IFeatureRegistry(ABC):
    """Interface for managing mathematical feature pipelines."""

    @abstractmethod
    def register_feature(self, feature: Feature) -> None:
        """Register a new mathematical feature with lineage metadata."""
        ...

    @abstractmethod
    def get_feature(self, feature_id: str) -> Optional[Feature]:
        """Retrieve a feature by ID."""
        ...


class IExperimentRegistry(ABC):
    """Interface for the immutable tracking of all trial and simulation runs."""

    @abstractmethod
    def register_experiment(self, experiment: Experiment) -> None:
        """Register a completed experiment run."""
        ...

    @abstractmethod
    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        """Retrieve an experiment record by ID."""
        ...

    @abstractmethod
    def get_experiment_by_hash(self, config_hash: str) -> Optional[Experiment]:
        """Retrieve an experiment by its configuration SHA-256 hash."""
        ...

    @abstractmethod
    def list_experiments(self) -> List[Experiment]:
        """List all tracked experiments."""
        ...


class IModelRegistry(ABC):
    """Interface for managing promoted, production-ready trading models."""

    @abstractmethod
    def register_model(self, model: Model) -> None:
        """Register a model that has passed all promotion gates."""
        ...

    @abstractmethod
    def get_model(self, model_id: str) -> Optional[Model]:
        """Retrieve a promoted model by ID."""
        ...


class IStatisticalValidator(ABC):
    """Interface for applying significance and multiple hypothesis testing corrections."""

    @abstractmethod
    def validate_experiment(self, experiment: Experiment, all_trials: List[Experiment]) -> ValidationReport:
        """Evaluate an experiment's metrics, adjusting for multiple testing and DSR."""
        ...


class IGovernanceGateway(ABC):
    """Interface for non-bypassable promotion gates and peer-review auditing."""

    @abstractmethod
    def evaluate_promotion(
        self,
        experiment: Experiment,
        report: ValidationReport,
        reviewers: List[str],
        approvals: Dict[str, bool],
    ) -> DecisionRecord:
        """Perform final compliance, risk, and peer-review audits to promote a model."""
        ...
