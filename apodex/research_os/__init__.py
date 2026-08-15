"""AlphaAlgo Research Operating System (Research OS).

Redesigned quantitative research platform incorporating institutional scientific
research standards.
"""
from __future__ import annotations

from .interfaces import (
    IHypothesisRegistry,
    IDatasetRegistry,
    IFeatureRegistry,
    IExperimentRegistry,
    IModelRegistry,
    IStatisticalValidator,
    IGovernanceGateway,
)
from .models import (
    Hypothesis,
    Dataset,
    Feature,
    Experiment,
    Model,
    ValidationReport,
    DecisionRecord,
    compute_config_hash,
)
from .registries import (
    HypothesisRegistry,
    DatasetRegistry,
    FeatureRegistry,
    ExperimentRegistry,
    ModelRegistry,
)
from .statistical_validation import (
    adjust_p_values,
    calculate_dsr,
    walk_forward_split,
    block_bootstrap,
)
from .reproducibility import (
    capture_environment_fingerprint,
    verify_reproducibility,
)
from .pipeline import (
    StatisticalValidator,
    GovernanceGateway,
    ResearchPipelineOrchestrator,
)
from .research_ingestion import (
    ResearchIngestionPipeline,
)

from ..ai_eos.research.integration import (
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
)

__all__ = [
    "CodeRewriteEngine",
    "GeneticWorkflowOptimizer",
    "SFTPreferenceCollector",
    "LearnableRoutingGateDispatcher",
    "IHypothesisRegistry",
    "IDatasetRegistry",
    "IFeatureRegistry",
    "IExperimentRegistry",
    "IModelRegistry",
    "IStatisticalValidator",
    "IGovernanceGateway",
    "Hypothesis",
    "Dataset",
    "Feature",
    "Experiment",
    "Model",
    "ValidationReport",
    "DecisionRecord",
    "compute_config_hash",
    "HypothesisRegistry",
    "DatasetRegistry",
    "FeatureRegistry",
    "ExperimentRegistry",
    "ModelRegistry",
    "adjust_p_values",
    "calculate_dsr",
    "walk_forward_split",
    "block_bootstrap",
    "capture_environment_fingerprint",
    "verify_reproducibility",
    "StatisticalValidator",
    "GovernanceGateway",
    "ResearchPipelineOrchestrator",
    "ResearchIngestionPipeline",
]
