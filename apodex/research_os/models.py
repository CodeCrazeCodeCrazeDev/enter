"""Domain models for the AlphaAlgo Research Operating System (Research OS).

Pydantic models representing strongly-typed metadata, configurations, and results
with canonical serialization and SHA-256 hashing.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


def compute_config_hash(config_dict: Dict[str, Any]) -> str:
    """Serialize a dictionary to a sorted canonical JSON string and compute its SHA-256 hash."""
    canonical_json = json.dumps(config_dict, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


class Hypothesis(BaseModel):
    """Scientific research hypothesis."""

    hypothesis_id: str = Field(description="Unique ID for the hypothesis")
    research_question_id: str = Field(description="Link to the target research question")
    title: str = Field(description="Descriptive title of the hypothesis")
    description: str = Field(description="Detailed scientific description of the claim")
    economic_rationale: str = Field(description="Causal or economic rationale (e.g., MICROSTRUCTURE, BEHAVIORAL)")
    null_hypothesis: str = Field(description="Definition of criteria under which the claim is false")
    target_variable: str = Field(description="Variable the signal claims to predict")
    registered_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Dataset(BaseModel):
    """Metadata for an immutable, versioned dataset snapshot."""

    dataset_id: str = Field(description="Unique ID of the dataset version")
    version: str = Field(description="Version string (e.g., v1.0)")
    raw_source: str = Field(description="Origin source URI or path")
    ingestion_pipeline_hash: str = Field(description="SHA-256 hash of the ingestion pipeline code")
    registered_at: datetime = Field(default_factory=datetime.utcnow)
    data_quality_report: Dict[str, Any] = Field(default_factory=dict, description="Captured temporal & PIT quality checks")


class Feature(BaseModel):
    """Metadata for a versioned mathematical feature."""

    feature_id: str = Field(description="Unique ID for the feature")
    name: str = Field(description="Feature name")
    formula: str = Field(description="Mathematical expression of the feature")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Hyperparameters used to generate the feature")
    lineage_dataset_id: str = Field(description="ID of the dataset snapshot used for calculation")
    stationarity_p_value: Optional[float] = Field(None, description="P-value from ADF stationarity test")
    registered_at: datetime = Field(default_factory=datetime.utcnow)


class Experiment(BaseModel):
    """Metadata and outcomes of an executed backtest or simulation."""

    experiment_id: str = Field(description="Unique ID of the experiment")
    hypothesis_id: str = Field(description="Link to the pre-registered hypothesis")
    dataset_id: str = Field(description="Link to the dataset snapshot used")
    feature_ids: List[str] = Field(default_factory=list, description="Features used in the model")
    hyperparameters: Dict[str, Any] = Field(default_factory=dict, description="Model hyperparameters and code specs")
    config_hash: str = Field("", description="SHA-256 configuration hash (computed over inputs)")
    status: str = Field("PENDING", description="PENDING | RUNNING | COMPLETED | FAILED")
    reproducibility_package: Dict[str, Any] = Field(
        default_factory=dict,
        description="Frozen package lock, OS, Python version, git commit, seed, etc."
    )
    metrics: Dict[str, float] = Field(default_factory=dict, description="Backtest metrics (Sharpe, drawdown, ROI, etc.)")
    returns_time_series: List[float] = Field(default_factory=list, description="Time series of daily or step returns")
    error_log: Optional[str] = Field(None, description="Captured traceback if status is FAILED")
    registered_at: datetime = Field(default_factory=datetime.utcnow)

    def calculate_config_hash(self) -> str:
        """Compute the SHA-256 configuration hash over all input configurations."""
        inputs = {
            "hypothesis_id": self.hypothesis_id,
            "dataset_id": self.dataset_id,
            "feature_ids": sorted(self.feature_ids),
            "hyperparameters": self.hyperparameters,
            "seed": self.reproducibility_package.get("seed", 42),
        }
        return compute_config_hash(inputs)


class ValidationReport(BaseModel):
    """Statistical validation report evaluating significance and overfitting."""

    validation_id: str = Field(description="Unique ID for the validation report")
    experiment_id: str = Field(description="Link to the evaluated experiment")
    raw_sharpe_ratio: float = Field(description="Raw Sharpe Ratio from the backtest")
    deflated_sharpe_ratio: float = Field(description="Deflated Sharpe Ratio (DSR) adjusting for trials and overfitting")
    p_value: float = Field(description="Statistical p-value of the returns")
    adjusted_p_value: float = Field(description="Adjusted p-value after multiple hypothesis correction")
    correction_method: str = Field(description="Adjustment method applied (e.g., BONFERRONI, HOLM, BH)")
    probability_of_backtest_overfitting: float = Field(description="Probability of Backtest Overfitting (PBO)")
    bootstrap_sharpe_quantile_5: float = Field(description="5th percentile Sharpe Ratio from block bootstrap")
    is_statistically_significant: bool = Field(description="True if DSR and adjusted p-value meet targets")
    validated_at: datetime = Field(default_factory=datetime.utcnow)


class Model(BaseModel):
    """Metadata for a promoted, production-ready trading model."""

    model_id: str = Field(description="Unique ID of the promoted model")
    experiment_id: str = Field(description="Link to the source experiment")
    decision_record_id: str = Field(description="Link to the peer-review decision record")
    version: str = Field(description="Version identifier (e.g., v1.0.0)")
    capacity_limit_usd: float = Field(description="Estimated maximum liquidity-based capacity limit")
    correlation_to_portfolio: float = Field(description="Historical correlation to active portfolio")
    status: str = Field("PROMOTED", description="PROMOTED | LIVE | REJECTED | SUSPENDED")
    promoted_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DecisionRecord(BaseModel):
    """Immutable peer-review decision record."""

    decision_id: str = Field(description="Unique UUID")
    experiment_id: str = Field(description="Link to the candidate experiment")
    reviewers: List[str] = Field(default_factory=list, description="Names or IDs of reviewers")
    approvals: Dict[str, bool] = Field(default_factory=dict, description="Approvals/votes mapping")
    status: str = Field("APPROVED", description="APPROVED | REJECTED | REQUEST_REVISIONS")
    metrics_summary: Dict[str, float] = Field(default_factory=dict, description="DSR, Sharpe, drawdown, etc.")
    rejection_rationales: List[str] = Field(default_factory=list)
    previous_log_hash: str = Field("", description="SHA-256 hash of the previous audit log entry")
    entry_hash: str = Field("", description="SHA-256 hash over this entry + previous_log_hash")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def calculate_entry_hash(self) -> str:
        """Compute the unique cryptographically-chained entry hash."""
        fields = {
            "decision_id": self.decision_id,
            "experiment_id": self.experiment_id,
            "reviewers": sorted(self.reviewers),
            "status": self.status,
            "previous_log_hash": self.previous_log_hash,
        }
        return compute_config_hash(fields)
