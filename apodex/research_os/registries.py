"""In-memory thread-safe implementation of AlphaAlgo Research OS registries.

Guarantees immutability (overwrites are forbidden) and fast lookups.
"""
from __future__ import annotations

import threading
from typing import Dict, List, Optional
from .interfaces import (
    IHypothesisRegistry,
    IDatasetRegistry,
    IFeatureRegistry,
    IExperimentRegistry,
    IModelRegistry,
)
from .models import Hypothesis, Dataset, Feature, Experiment, Model


class HypothesisRegistry(IHypothesisRegistry):
    """Thread-safe, immutable Hypothesis Registry."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._store: Dict[str, Hypothesis] = {}

    def register_hypothesis(self, hypothesis: Hypothesis) -> None:
        with self._lock:
            if hypothesis.hypothesis_id in self._store:
                raise ValueError(f"Hypothesis with ID '{hypothesis.hypothesis_id}' already exists. Overwrites are forbidden.")
            self._store[hypothesis.hypothesis_id] = hypothesis

    def get_hypothesis(self, hypothesis_id: str) -> Optional[Hypothesis]:
        with self._lock:
            return self._store.get(hypothesis_id)

    def list_hypotheses(self) -> List[Hypothesis]:
        with self._lock:
            return list(self._store.values())


class DatasetRegistry(IDatasetRegistry):
    """Thread-safe, immutable Dataset Registry."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._store: Dict[str, Dataset] = {}

    def register_dataset(self, dataset: Dataset) -> None:
        with self._lock:
            if dataset.dataset_id in self._store:
                raise ValueError(f"Dataset with ID '{dataset.dataset_id}' already exists. Overwrites are forbidden.")
            self._store[dataset.dataset_id] = dataset

    def get_dataset(self, dataset_id: str) -> Optional[Dataset]:
        with self._lock:
            return self._store.get(dataset_id)


class FeatureRegistry(IFeatureRegistry):
    """Thread-safe, immutable Feature Registry."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._store: Dict[str, Feature] = {}

    def register_feature(self, feature: Feature) -> None:
        with self._lock:
            if feature.feature_id in self._store:
                raise ValueError(f"Feature with ID '{feature.feature_id}' already exists. Overwrites are forbidden.")
            self._store[feature.feature_id] = feature

    def get_feature(self, feature_id: str) -> Optional[Feature]:
        with self._lock:
            return self._store.get(feature_id)


class ExperimentRegistry(IExperimentRegistry):
    """Thread-safe, immutable Experiment Registry with configuration hash caching."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._store: Dict[str, Experiment] = {}
        self._hash_store: Dict[str, Experiment] = {}

    def register_experiment(self, experiment: Experiment) -> None:
        with self._lock:
            existing = self._store.get(experiment.experiment_id)
            if existing and existing.status != "FAILED":
                raise ValueError(f"Experiment with ID '{experiment.experiment_id}' already exists and is immutable.")

            # Compute configuration hash if not already set
            if not experiment.config_hash:
                experiment.config_hash = experiment.calculate_config_hash()

            self._store[experiment.experiment_id] = experiment
            self._hash_store[experiment.config_hash] = experiment

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        with self._lock:
            return self._store.get(experiment_id)

    def get_experiment_by_hash(self, config_hash: str) -> Optional[Experiment]:
        with self._lock:
            return self._hash_store.get(config_hash)

    def list_experiments(self) -> List[Experiment]:
        with self._lock:
            return list(self._store.values())


class ModelRegistry(IModelRegistry):
    """Thread-safe, immutable Model Registry."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._store: Dict[str, Model] = {}

    def register_model(self, model: Model) -> None:
        with self._lock:
            if model.model_id in self._store:
                raise ValueError(f"Model with ID '{model.model_id}' already exists.")
            self._store[model.model_id] = model

    def get_model(self, model_id: str) -> Optional[Model]:
        with self._lock:
            return self._store.get(model_id)
