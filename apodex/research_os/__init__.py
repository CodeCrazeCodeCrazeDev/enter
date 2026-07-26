"""Research Operating System (Research OS) core exports."""

from __future__ import annotations

from .models import (
    BaseArtifact,
    ResearchProject,
    ResearchProposal,
    ResearchAgenda,
    ResearchQuestion,
    LiteratureCorpus,
    KnowledgeGapAnalysis,
    Hypothesis,
    ExperimentDesign,
    ExperimentResult,
    ReproducibilityReport,
    BenchmarkResult,
    DecisionRecord,
    GovernanceDecision,
    PeerReviewCritique,
    Publication,
    CitationGraph,
    ResearchRoadmap,
    InstitutionalPolicy,
    ConceptNode,
    TheoryNode,
    ClaimNode,
    EvidenceNode,
    ContradictionNode,
)

from .events import (
    BaseEvent,
    WorkflowStarted,
    ArtifactCreated,
    ExperimentCompleted,
    ReviewFailed,
    GovernanceRejected,
    PublicationAccepted,
    HypothesisFalsified,
    EventBus,
    InstitutionalMetricsCalculator,
)

from .storage import (
    ResearchRepository,
    DocumentStore,
    VectorDB,
    RelationalDB,
    ArtifactStore,
    PhysicalKnowledgeGraph,
)

from .plugins import (
    IAgentPlugin,
    IGovernancePlugin,
    IExperimentBackend,
    IEvidenceProvider,
    PluginRegistry,
)

from .governance import (
    EthicsReviewBoard,
    ScientificQualityBoard,
    SecurityBoard,
    CapitalAllocationBoard,
)

from .knowledge_graph import (
    ActiveKnowledgeGraph,
    ContradictionDetected,
)

from .workflow import (
    TransitionCondition,
    FailurePolicy,
    StageDefinition,
    WorkflowDefinition,
    WorkflowRun,
    WorkflowEngine,
    create_builtin_workflows,
)

from .uncertainty import (
    update_belief,
    calculate_expected_probability,
    calculate_epistemic_entropy,
    apply_temporal_decay,
)

from .portfolio import (
    ProjectAllocation,
    PortfolioScheduler,
)

from .provenance import (
    ProvenanceRelation,
    ProvenanceEngine,
)

from .self_improvement import (
    WorkflowFailureTrace,
    SelfImprovementFlywheel,
)
