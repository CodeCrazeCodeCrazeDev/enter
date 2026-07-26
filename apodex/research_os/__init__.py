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
    ContradictionNode,
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
