from __future__ import annotations
import time
from uuid import UUID, uuid4
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from .models import (
    BaseArtifact,
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
    PeerReviewCritique,
    Publication,
    CitationGraph,
    ResearchRoadmap,
)
from .events import (
    EventBus,
    WorkflowStarted,
    ArtifactCreated,
    ExperimentCompleted,
    GovernanceRejected,
    PublicationAccepted,
)
from .storage import ResearchRepository
from .plugins import PluginRegistry

# =====================================================================
# Declarative WDL Models
# =====================================================================

class TransitionCondition(BaseModel):
    condition: str  # e.g., "success", "p_value < 0.05", "approved"
    next_stage: str


class FailurePolicy(BaseModel):
    retry_count: int = 3
    on_exhausted: str = "escalate"  # "escalate" | "fail" | "retry_with_fallback"


class StageDefinition(BaseModel):
    id: str
    type: str  # "ingestion" | "generation" | "design" | "experiment" | "analysis" | "review" | "archive"
    agent: Optional[str] = None
    provider: Optional[str] = None
    backend: Optional[str] = None
    required_artifacts: List[str] = Field(default_factory=list)
    produced_artifacts: List[str] = Field(default_factory=list)
    governance_gates: List[str] = Field(default_factory=list)
    transition_conditions: List[TransitionCondition] = Field(default_factory=list)
    failure_policy: FailurePolicy = Field(default_factory=FailurePolicy)


class WorkflowDefinition(BaseModel):
    id: str
    domain: str
    version: str = "1.0.0"
    stages: List[StageDefinition] = Field(default_factory=list)


# =====================================================================
# Workflow Engine
# =====================================================================

class WorkflowRun(BaseModel):
    run_id: UUID = Field(default_factory=uuid4)
    workflow_id: str
    project_uuid: UUID
    current_stage: str
    artifacts: Dict[str, UUID] = Field(default_factory=dict)  # artifact_type_name -> UUID
    history: List[str] = Field(default_factory=list)  # trace of stages executed
    status: str = "RUNNING"  # "RUNNING" | "COMPLETED" | "FAILED" | "SUSPENDED"
    timestamp_started: float = Field(default_factory=time.time)


class WorkflowEngine:
    """
    Event-driven Research OS Workflow Engine.
    Handles parallel paths, feedback loops, concurrency, and declarative execution.
    """

    def __init__(
        self,
        repository: ResearchRepository,
        event_bus: EventBus,
        plugin_registry: PluginRegistry
    ) -> None:
        self.repo = repository
        self.bus = event_bus
        self.plugins = plugin_registry
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.active_runs: Dict[UUID, WorkflowRun] = {}

        # Subscribe to artifact creations to drive event-driven execution
        self.bus.subscribe(ArtifactCreated, self.on_artifact_created)

    def register_workflow(self, definition: WorkflowDefinition) -> None:
        self.workflows[definition.id] = definition

    def start_run(self, workflow_id: str, project_uuid: UUID) -> UUID:
        """Starts a new declarative workflow run, publishing the starting event."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow '{workflow_id}' is not registered.")

        wdl = self.workflows[workflow_id]
        first_stage = wdl.stages[0].id

        run = WorkflowRun(
            workflow_id=workflow_id,
            project_uuid=project_uuid,
            current_stage=first_stage,
            history=[first_stage]
        )
        self.active_runs[run.run_id] = run

        self.bus.publish(WorkflowStarted(
            workflow_id=workflow_id,
            domain=wdl.domain,
            project_uuid=project_uuid
        ))

        # Trigger execution of the first stage
        import asyncio
        asyncio.create_task(self._execute_current_stage(run.run_id))

        return run.run_id

    def on_artifact_created(self, event: ArtifactCreated) -> None:
        """Reactive task scheduling. When an artifact is created, drive workflow stages."""
        # Find active runs waiting for this artifact
        for run_id, run in list(self.active_runs.items()):
            if run.status != "RUNNING":
                continue

            wdl = self.workflows[run.workflow_id]
            stage = self._get_stage(wdl, run.current_stage)
            if not stage:
                continue

            # Record artifact in run context
            run.artifacts[event.artifact_type] = event.artifact_uuid

            # Check if all required artifacts for the current stage are available
            has_requirements = True
            for req in stage.required_artifacts:
                if req not in run.artifacts:
                    has_requirements = False
                    break

            if has_requirements:
                import asyncio
                asyncio.create_task(self._execute_current_stage(run_id))

    def _get_stage(self, wdl: WorkflowDefinition, stage_id: str) -> Optional[StageDefinition]:
        for stage in wdl.stages:
            if stage.id == stage_id:
                return stage
        return None

    async def _execute_current_stage(self, run_id: UUID) -> None:
        """Coordinates execution of the active stage, handling agents, backends, and governance."""
        run = self.active_runs.get(run_id)
        if not run or run.status != "RUNNING":
            return

        wdl = self.workflows[run.workflow_id]
        stage = self._get_stage(wdl, run.current_stage)
        if not stage:
            return

        # 1. Enforce Governance Gates before execution
        for gate in stage.governance_gates:
            gov_plugin = self.plugins.get_governance(gate)
            if gov_plugin:
                # Audit the context or most recent artifact
                last_artifact_uuid = list(run.artifacts.values())[-1] if run.artifacts else run.project_uuid
                last_artifact = self.repo.get_artifact(last_artifact_uuid)
                if last_artifact:
                    decision = await gov_plugin.audit(last_artifact)
                    self.repo.save_artifact(decision)

                    if decision.decision_outcome == "REJECT":
                        run.status = "FAILED"
                        self.bus.publish(GovernanceRejected(
                            board_name=gate,
                            target_uuid=last_artifact.uuid,
                            reason=decision.reason
                        ))
                        return
                    elif decision.decision_outcome == "REQUEST_REVISION":
                        # Loop back to previous stage as requested by governance
                        run.current_stage = wdl.stages[max(0, wdl.stages.index(stage) - 1)].id
                        run.history.append(run.current_stage)
                        return

        # 2. Retrieve required input artifacts
        inputs: Dict[str, BaseArtifact] = {}
        lineage_parents: List[UUID] = []
        for req in stage.required_artifacts:
            art_uuid = run.artifacts.get(req)
            if art_uuid:
                art = self.repo.get_artifact(art_uuid)
                if art:
                    inputs[req] = art
                    lineage_parents.append(art_uuid)

        # 3. Invoke plugin or high-fidelity simulator fallback
        produced: List[BaseArtifact] = []

        # If a specific agent plugin is designated
        if stage.agent and self.plugins.get_agent(stage.agent):
            agent_plugin = self.plugins.get_agent(stage.agent)
            try:
                out = await agent_plugin.process(inputs, lineage_parents, stage.agent)
                produced.append(out)
            except Exception as e:
                print(f"Agent plugin error: {e}")

        # If an experiment backend is designated
        elif stage.backend and self.plugins.get_experiment_backend(stage.backend):
            backend_plugin = self.plugins.get_experiment_backend(stage.backend)
            design_art = inputs.get("ExperimentDesign")
            if design_art and isinstance(design_art, ExperimentDesign):
                try:
                    res = await backend_plugin.run(design_art)
                    produced.append(res)
                    self.bus.publish(ExperimentCompleted(
                        experiment_uuid=res.uuid,
                        design_uuid=design_art.uuid,
                        backend=stage.backend,
                        success=res.success,
                        metrics=res.metrics
                    ))
                except Exception as e:
                    print(f"Backend execution error: {e}")

        # Fallback high-fidelity simulator to guarantee runnable out of the box
        else:
            simulated_arts = self._simulate_stage_production(stage, inputs, lineage_parents)
            produced.extend(simulated_arts)
            for p in simulated_arts:
                if isinstance(p, ExperimentResult):
                    self.bus.publish(ExperimentCompleted(
                        experiment_uuid=p.uuid,
                        design_uuid=p.design_uuid,
                        backend=stage.backend or "sim_sandbox",
                        success=p.success,
                        metrics=p.metrics
                    ))

        # 4. Save produced artifacts and emit creation events
        for p in produced:
            signed_art = p.with_signature()
            self.repo.save_artifact(signed_art)
            run.artifacts[p.__class__.__name__] = signed_art.uuid

            self.bus.publish(ArtifactCreated(
                artifact_uuid=signed_art.uuid,
                artifact_type=p.__class__.__name__,
                author=stage.agent or "system_scheduler",
                confidence=p.confidence,
                parent_uuids=lineage_parents
            ))

        # 5. Evaluate transition conditions to route execution (handles branching and loops)
        next_stage_id = None
        for cond in stage.transition_conditions:
            # Simple condition matching based on produced results or metrics
            if cond.condition == "success":
                next_stage_id = cond.next_stage
                break
            elif cond.condition == "p_value < 0.05" or cond.condition == "approved":
                # Extract statistical reporting or review decisions to route
                has_passed = True
                for p in produced:
                    if isinstance(p, PeerReviewCritique) and not p.approved:
                        has_passed = False
                    if p.__class__.__name__ == "StatisticalReport":
                        # Sim rating or p-value check
                        p_val = p.confidence  # simulated mapping
                        if p_val >= 0.05:
                            has_passed = False
                if has_passed:
                    next_stage_id = cond.next_stage
                    break
            elif cond.condition == "p_value >= 0.05" or cond.condition == "not PeerReviewCritique.approved":
                # Trigger loops/feedback routing
                has_failed = False
                for p in produced:
                    if isinstance(p, PeerReviewCritique) and not p.approved:
                        has_failed = True
                if has_failed:
                    next_stage_id = cond.next_stage
                    break

        if next_stage_id:
            # Transition to next stage
            run.current_stage = next_stage_id
            run.history.append(next_stage_id)
            # Re-execute immediately if requirements are satisfied
            import asyncio
            asyncio.create_task(self._execute_current_stage(run_id))
        else:
            # No matching condition, mark as completed if this is the last stage
            if stage.id == wdl.stages[-1].id:
                run.status = "COMPLETED"
                # Publish validation outcome
                self.bus.publish(PublicationAccepted(
                    publication_uuid=run.artifacts.get("Publication", uuid4()),
                    citation_graph_uuid=run.artifacts.get("CitationGraph", uuid4()),
                    project_uuid=run.project_uuid,
                    timestamp_started=run.timestamp_started
                ))

    def _simulate_stage_production(
        self,
        stage: StageDefinition,
        inputs: Dict[str, BaseArtifact],
        parents: List[UUID]
    ) -> List[BaseArtifact]:
        """High-fidelity generation of mock immutable artifacts when plugins are offline."""
        produced: List[BaseArtifact] = []

        for prod_type in stage.produced_artifacts:
            if prod_type == "ResearchProposal":
                produced.append(ResearchProposal(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "ExecutiveDirector",
                    project_uuid=uuid4(),
                    proposal_title="A Novel Neural Representation Framework",
                    proposal_abstract="This proposal introduces cognitive-map based semantic graph overlays."
                ))
            elif prod_type == "ResearchAgenda":
                produced.append(ResearchAgenda(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "ExecutiveDirector",
                    prioritized_proposals=parents
                ))
            elif prod_type == "ResearchQuestion":
                produced.append(ResearchQuestion(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "ExecutiveDirector",
                    question_text="How can graph neural embeddings optimize memory consolidated networks?",
                    domain="AI Research"
                ))
            elif prod_type == "LiteratureCorpus":
                produced.append(LiteratureCorpus(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "LiteratureScientist",
                    query="graph embedding consolidation",
                    paper_titles=["Towards Memory Consolidation", "Neural Graphs and Embeddings"],
                    abstracts=["We propose structural graphs for short-term memory", "A survey of neural embedding networks."]
                ))
            elif prod_type == "KnowledgeGapAnalysis":
                produced.append(KnowledgeGapAnalysis(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "LiteratureScientist",
                    corpus_uuid=parents[0] if parents else uuid4(),
                    gaps=["Lack of multi-scale temporal indexing", "Insufficient verification bounds."]
                ))
            elif prod_type == "Hypothesis":
                produced.append(Hypothesis(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "DomainScientist",
                    statement="Temporal graph indexing improves memory consolidation retention rate by >=15%.",
                    predicted_expectations={"retention_improvement": 0.15, "f1_score": 0.88}
                ))
            elif prod_type == "ExperimentDesign":
                produced.append(ExperimentDesign(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "ExperimentScientist",
                    hypothesis_uuid=parents[0] if parents else uuid4(),
                    parameters={"epochs": 50, "learning_rate": 0.001, "layers": [128, 64]},
                    code_snippet="def run_trial(model):\n    return model.train()",
                    execution_backend=stage.backend or "ml_sandbox"
                ))
            elif prod_type == "ExperimentResult":
                produced.append(ExperimentResult(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "ExperimentScientist",
                    design_uuid=parents[0] if parents else uuid4(),
                    success=True,
                    metrics={"retention_improvement_observed": 0.18, "f1_observed": 0.91, "epochs_run": 50},
                    logs=["Initialization complete", "Training epoch 10/50...", "Evaluation complete."]
                ))
            elif prod_type == "ReproducibilityReport":
                produced.append(ReproducibilityReport(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "Statistician",
                    experiment_uuid=parents[0] if parents else uuid4(),
                    reproducibility_rate=0.95,
                    reproduced=True
                ))
            elif prod_type == "BenchmarkResult":
                produced.append(BenchmarkResult(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "Statistician",
                    experiment_uuid=parents[0] if parents else uuid4(),
                    benchmark_name="GLUE_V2",
                    score=0.89
                ))
            elif prod_type == "PeerReviewCritique":
                # Simulated critique: approved with high confidence
                produced.append(PeerReviewCritique(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "PeerReviewCommittee",
                    approved=True,
                    comment="The methodology is sound and the results support the hypothesis."
                ))
            elif prod_type == "Publication":
                produced.append(Publication(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "PublicationEditor",
                    title="Temporal Consolidated Graphs",
                    content="Full text details of temporal consolidated graph neural networks.",
                    citation_graph_uuid=uuid4()
                ))
            elif prod_type == "CitationGraph":
                produced.append(CitationGraph(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "KnowledgeLibrarian",
                    citations={"Temporal Consolidated Graphs": ["Towards Memory Consolidation"]}
                ))
            elif prod_type == "ResearchRoadmap":
                produced.append(ResearchRoadmap(
                    lineage_parent_uuids=parents,
                    author=stage.agent or "ResearchPlanner",
                    milestones=["Phase 1: Graph Embeddings", "Phase 2: Validation", "Phase 3: Production Release"]
                ))

        return produced


# =====================================================================
# Factory of Built-In Declarative Domain Workflows
# =====================================================================

def create_builtin_workflows() -> List[WorkflowDefinition]:
    """Generates the seven built-in declarative configurations."""
    workflows = []

    # 1. AI Research Workflow
    workflows.append(WorkflowDefinition(
        id="ai_research",
        domain="AI Research",
        stages=[
            StageDefinition(
                id="literature_review",
                type="ingestion",
                provider="semantic_scholar",
                required_artifacts=["ResearchQuestion"],
                produced_artifacts=["LiteratureCorpus"],
                transition_conditions=[TransitionCondition(condition="success", next_stage="hypothesis_generation")]
            ),
            StageDefinition(
                id="hypothesis_generation",
                type="generation",
                agent="DomainScientist",
                required_artifacts=["LiteratureCorpus"],
                produced_artifacts=["Hypothesis"],
                governance_gates=["EthicsReviewBoard"],
                transition_conditions=[TransitionCondition(condition="success", next_stage="experiment_design")]
            ),
            StageDefinition(
                id="experiment_design",
                type="design",
                agent="ExperimentScientist",
                required_artifacts=["Hypothesis"],
                produced_artifacts=["ExperimentDesign"],
                transition_conditions=[TransitionCondition(condition="success", next_stage="execution")]
            ),
            StageDefinition(
                id="execution",
                type="experiment",
                backend="ml_training_sandbox",
                required_artifacts=["ExperimentDesign"],
                produced_artifacts=["ExperimentResult"],
                transition_conditions=[TransitionCondition(condition="success", next_stage="statistical_analysis")]
            ),
            StageDefinition(
                id="statistical_analysis",
                type="analysis",
                agent="Statistician",
                required_artifacts=["ExperimentResult"],
                produced_artifacts=["ReproducibilityReport", "BenchmarkResult"],
                transition_conditions=[TransitionCondition(condition="success", next_stage="peer_review")]
            ),
            StageDefinition(
                id="peer_review",
                type="review",
                agent="PeerReviewCommittee",
                required_artifacts=["ReproducibilityReport"],
                produced_artifacts=["PeerReviewCritique"],
                transition_conditions=[TransitionCondition(condition="approved", next_stage="publication")]
            ),
            StageDefinition(
                id="publication",
                type="archive",
                agent="PublicationEditor",
                required_artifacts=["PeerReviewCritique"],
                produced_artifacts=["Publication", "CitationGraph"]
            )
        ]
    ))

    # 2. Quantitative Finance Workflow
    workflows.append(WorkflowDefinition(
        id="quant_finance",
        domain="Quantitative Finance",
        stages=[
            StageDefinition(
                id="data_ingestion",
                type="ingestion",
                provider="market_provider",
                required_artifacts=["ResearchQuestion"],
                produced_artifacts=["LiteratureCorpus"],
                transition_conditions=[TransitionCondition(condition="success", next_stage="alpha_hypothesis")]
            ),
            StageDefinition(
                id="alpha_hypothesis",
                type="generation",
                agent="DomainScientist",
                required_artifacts=["LiteratureCorpus"],
                produced_artifacts=["Hypothesis"],
                transition_conditions=[TransitionCondition(condition="success", next_stage="backtest_design")]
            ),
            StageDefinition(
                id="backtest_design",
                type="design",
                agent="ExperimentScientist",
                required_artifacts=["Hypothesis"],
                produced_artifacts=["ExperimentDesign"],
                transition_conditions=[TransitionCondition(condition="success", next_stage="backtest_execution")]
            ),
            StageDefinition(
                id="backtest_execution",
                type="experiment",
                backend="backtest_sandbox",
                required_artifacts=["ExperimentDesign"],
                produced_artifacts=["ExperimentResult"],
                transition_conditions=[TransitionCondition(condition="success", next_stage="risk_audit")]
            ),
            StageDefinition(
                id="risk_audit",
                type="analysis",
                agent="Statistician",
                required_artifacts=["ExperimentResult"],
                produced_artifacts=["ReproducibilityReport"],
                governance_gates=["CapitalAllocationBoard"],
                transition_conditions=[TransitionCondition(condition="success", next_stage="peer_review")]
            ),
            StageDefinition(
                id="peer_review",
                type="review",
                agent="PeerReviewCommittee",
                required_artifacts=["ReproducibilityReport"],
                produced_artifacts=["PeerReviewCritique"],
                transition_conditions=[TransitionCondition(condition="approved", next_stage="archive_model")]
            ),
            StageDefinition(
                id="archive_model",
                type="archive",
                agent="PublicationEditor",
                required_artifacts=["PeerReviewCritique"],
                produced_artifacts=["Publication"]
            )
        ]
    ))

    # 3-7. Other declarative layouts (Systems Engineering, Robotics, Biology, Economics, General Research)
    for other_domain in ["Systems Engineering", "Robotics", "Biology", "Economics", "General Scientific Research"]:
        code = other_domain.lower().replace(" ", "_")
        workflows.append(WorkflowDefinition(
            id=code,
            domain=other_domain,
            stages=[
                StageDefinition(
                    id="literature",
                    type="ingestion",
                    provider="generic_provider",
                    required_artifacts=["ResearchQuestion"],
                    produced_artifacts=["LiteratureCorpus"],
                    transition_conditions=[TransitionCondition(condition="success", next_stage="hypothesis")]
                ),
                StageDefinition(
                    id="hypothesis",
                    type="generation",
                    agent="DomainScientist",
                    required_artifacts=["LiteratureCorpus"],
                    produced_artifacts=["Hypothesis"],
                    transition_conditions=[TransitionCondition(condition="success", next_stage="design")]
                ),
                StageDefinition(
                    id="design",
                    type="design",
                    agent="ExperimentScientist",
                    required_artifacts=["Hypothesis"],
                    produced_artifacts=["ExperimentDesign"],
                    transition_conditions=[TransitionCondition(condition="success", next_stage="execution")]
                ),
                StageDefinition(
                    id="execution",
                    type="experiment",
                    backend="generic_sandbox",
                    required_artifacts=["ExperimentDesign"],
                    produced_artifacts=["ExperimentResult"],
                    transition_conditions=[TransitionCondition(condition="success", next_stage="review")]
                ),
                StageDefinition(
                    id="review",
                    type="review",
                    agent="PeerReviewCommittee",
                    required_artifacts=["ExperimentResult"],
                    produced_artifacts=["PeerReviewCritique"],
                    transition_conditions=[TransitionCondition(condition="approved", next_stage="publish")]
                ),
                StageDefinition(
                    id="publish",
                    type="archive",
                    agent="PublicationEditor",
                    required_artifacts=["PeerReviewCritique"],
                    produced_artifacts=["Publication"]
                )
            ]
        ))

    return workflows
