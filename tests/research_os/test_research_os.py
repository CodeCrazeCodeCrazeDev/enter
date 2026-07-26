import asyncio
import pytest
import time
from uuid import uuid4

from apodex.research_os.models import (
    ResearchProject,
    ResearchQuestion,
    Hypothesis,
    ExperimentDesign,
    ExperimentResult,
    ClaimNode,
    EvidenceNode,
    TheoryNode,
    PeerReviewCritique,
    Publication,
    InstitutionalPolicy,
)
from apodex.research_os.events import (
    EventBus,
    ArtifactCreated,
    WorkflowStarted,
    ExperimentCompleted,
    GovernanceRejected,
    InstitutionalMetricsCalculator,
)
from apodex.research_os.storage import ResearchRepository
from apodex.research_os.plugins import PluginRegistry, IAgentPlugin, IGovernancePlugin
from apodex.research_os.governance import (
    EthicsReviewBoard,
    ScientificQualityBoard,
    SecurityBoard,
    CapitalAllocationBoard,
)
from apodex.research_os.knowledge_graph import ActiveKnowledgeGraph, ContradictionNode, ContradictionDetected
from apodex.research_os.workflow import WorkflowEngine, create_builtin_workflows, WorkflowRun

# Advanced subsystems
from apodex.research_os.uncertainty import (
    update_belief,
    calculate_expected_probability,
    calculate_epistemic_entropy,
    apply_temporal_decay,
)
from apodex.research_os.portfolio import PortfolioScheduler, ProjectAllocation
from apodex.research_os.provenance import ProvenanceEngine, ProvenanceRelation
from apodex.research_os.self_improvement import SelfImprovementFlywheel, WorkflowFailureTrace


# =====================================================================
# Mock Plugin Implementations for Contract Testing
# =====================================================================

class MockDomainScientist(IAgentPlugin):
    def name(self) -> str:
        return "DomainScientist"

    async def process(self, inputs, lineage_parents, author) -> Hypothesis:
        return Hypothesis(
            lineage_parent_uuids=lineage_parents,
            author=self.name(),
            statement="Graph temporal indexing improves validation speed.",
            confidence=0.9
        )


# =====================================================================
# Existing Core Test Suite
# =====================================================================

@pytest.mark.asyncio
async def test_artifact_immutability_and_digital_signatures():
    """Verify that artifacts are frozen, immutable, and carry verified integrity hashes."""
    project = ResearchProject(
        name="Cognitive Consolidation",
        funding_budget=50000.0,
        author="ExecutiveDirector"
    )

    # Immutable check
    with pytest.raises(Exception):
        project.name = "Mutated Name"

    # Compute and verify digital signature
    signed_project = project.with_signature()
    assert signed_project.digital_signature != ""
    assert signed_project.compute_signature() == signed_project.digital_signature


@pytest.mark.asyncio
async def test_repository_routing_and_lineage():
    """Verify that the repository routes reads/writes correctly and builds complete lineage paths."""
    repo = ResearchRepository()

    # Create parent and child artifacts
    parent_q = ResearchQuestion(
        question_text="How to scale training loops?",
        domain="AI Research",
        author="ExecutiveDirector"
    ).with_signature()

    child_h = Hypothesis(
        lineage_parent_uuids=[parent_q.uuid],
        statement="Distributed training reduces execution time.",
        author="DomainScientist"
    ).with_signature()

    # Save to Repository
    repo.save_artifact(parent_q)
    repo.save_artifact(child_h)

    # Retrieval from doc store
    retrieved = repo.get_artifact(child_h.uuid)
    assert retrieved is not None
    assert retrieved.uuid == child_h.uuid

    # Retrieval of list by type
    all_questions = repo.list_artifacts_by_type(ResearchQuestion)
    assert len(all_questions) == 1
    assert all_questions[0].question_text == "How to scale training loops?"

    # Lineage Tree traversal
    lineage_tree = repo.get_lineage_tree(child_h.uuid)
    assert len(lineage_tree) == 2
    uuids = [art.uuid for art in lineage_tree]
    assert parent_q.uuid in uuids
    assert child_h.uuid in uuids


@pytest.mark.asyncio
async def test_event_driven_metrics_calculator():
    """Verify that the Event Bus correctly distributes events to calculate institutional health metrics."""
    bus = EventBus()
    calc = InstitutionalMetricsCalculator(event_bus=bus)

    project_uuid = uuid4()

    # Publish lifecycle events
    bus.publish(WorkflowStarted(workflow_id="ai_research", domain="AI Research", project_uuid=project_uuid))
    bus.publish(ArtifactCreated(artifact_uuid=uuid4(), artifact_type="Hypothesis", author="Scientist", confidence=0.9, parent_uuids=[]))
    bus.publish(ArtifactCreated(artifact_uuid=uuid4(), artifact_type="Hypothesis", author="Scientist", confidence=0.8, parent_uuids=[]))
    bus.publish(ExperimentCompleted(experiment_uuid=uuid4(), design_uuid=uuid4(), backend="ml_sandbox", success=True, cost=12.5))
    bus.publish(ExperimentCompleted(experiment_uuid=uuid4(), design_uuid=uuid4(), backend="ml_sandbox", success=False, cost=7.5))
    bus.publish(GovernanceRejected(governance_uuid=uuid4(), board_name="EthicsReviewBoard", target_uuid=uuid4(), reason="Boundary violation"))

    # Compute indicators
    metrics = calc.calculate_metrics()
    assert metrics["experiment_success_rate"] == 0.5
    assert metrics["governance_vetoes"] == 1
    assert metrics["knowledge_graph_growth"] == 2


@pytest.mark.asyncio
async def test_active_knowledge_graph_and_theory_promotion():
    """Verify automated concept creation, deductive contradiction mapping, and theory promotion loops."""
    repo = ResearchRepository()
    bus = EventBus()
    akg = ActiveKnowledgeGraph(repository=repo, event_bus=bus)

    # Add concepts & evidence
    concept = akg.add_concept("Neural Map", "Representation of semantic graphs.")
    evidence_1 = akg.add_evidence("http://arXiv/1", "Consolidation increases speed by 20%.", "arXiv")
    evidence_2 = akg.add_evidence("http://arXiv/2", "Consolidation shows F1 improvement.", "arXiv")

    assert len(repo.list_artifacts_by_type(EvidenceNode)) == 2

    # Add high-confidence claims to trigger theory promotion
    claim_1 = akg.add_claim(
        assertion="Neural Map consolidation improves verification speeds.",
        evidence_ids=[evidence_1.uuid, evidence_2.uuid]
    )
    # Mutate to represent high confidence
    claim_1_updated = ClaimNode(
        uuid=claim_1.uuid,
        assertion=claim_1.assertion,
        evidence_ids=claim_1.evidence_ids,
        confidence=0.9
    ).with_signature()
    repo.save_artifact(claim_1_updated)

    claim_2 = akg.add_claim(
        assertion="Neural Map models decrease token latency significantly.",
        evidence_ids=[evidence_1.uuid, evidence_2.uuid]
    )
    claim_2_updated = ClaimNode(
        uuid=claim_2.uuid,
        assertion=claim_2.assertion,
        evidence_ids=claim_2.evidence_ids,
        confidence=0.85
    ).with_signature()
    repo.save_artifact(claim_2_updated)

    # Manual evaluation check of theory promotion
    akg._evaluate_theory_promotion()
    theories = repo.list_artifacts_by_type(TheoryNode)
    assert len(theories) == 1
    assert theories[0].theory_name == "Evolving Unified Core Theory"


@pytest.mark.asyncio
async def test_contradiction_detection():
    """Verify that adding opposing claims dynamically registers ContradictionNodes."""
    repo = ResearchRepository()
    bus = EventBus()
    akg = ActiveKnowledgeGraph(repository=repo, event_bus=bus)

    contradictions_published = []

    def handle_contradiction(event):
        contradictions_published.append(event)

    bus.subscribe(ContradictionDetected, handle_contradiction)

    claim_positive = akg.add_claim("The distributed optimizer always converges rapidly.", [])
    claim_negative = akg.add_claim("The distributed optimizer does not converge rapidly under high load.", [])

    # Ensure a contradiction node is generated and event published
    assert len(contradictions_published) == 1
    assert "Logical clash detected" in contradictions_published[0].explanation

    contradiction_nodes = repo.list_artifacts_by_type(ContradictionNode)
    assert len(contradiction_nodes) == 1


@pytest.mark.asyncio
async def test_programmatic_governance_outcomes():
    """Verify that governance boards issue binding Approve, Reject, and Request Revision decisions."""
    ethics = EthicsReviewBoard()
    quality = ScientificQualityBoard()
    security = SecurityBoard()

    # Create test artifact
    h = Hypothesis(statement="Self-improving AI rules.", confidence=0.8).with_signature()

    # Ethics Approve
    ethics_decision = await ethics.audit(h)
    assert ethics_decision.decision_outcome == "APPROVE"

    # Ethics Reject on low confidence
    h_low = Hypothesis(statement="Unverified assertion.", confidence=0.2).with_signature()
    ethics_decision_low = await ethics.audit(h_low)
    assert ethics_decision_low.decision_outcome == "REJECT"

    # Quality Request Revision
    h_medium = Hypothesis(statement="Borderline assertion.", confidence=0.6).with_signature()
    quality_decision = await quality.audit(h_medium)
    assert quality_decision.decision_outcome == "REQUEST_REVISION"

    # Security Reject on unsigned artifact
    unsigned_h = Hypothesis(statement="Vulnerable script.")
    security_decision = await security.audit(unsigned_h)
    assert security_decision.decision_outcome == "REJECT"


@pytest.mark.asyncio
async def test_wdl_parsing_and_built_in_workflows():
    """Verify that built-in domain workflows (AI, Finance, Biology, Robotics, etc.) are correctly defined."""
    workflows = create_builtin_workflows()

    assert len(workflows) == 7
    domains = [wdl.domain for wdl in workflows]
    assert "AI Research" in domains
    assert "Quantitative Finance" in domains
    assert "Biology" in domains
    assert "Robotics" in domains

    # Verify transition conditions of AI Research
    ai_wdl = [wdl for wdl in workflows if wdl.id == "ai_research"][0]
    assert len(ai_wdl.stages) == 7
    assert ai_wdl.stages[0].id == "literature_review"
    assert ai_wdl.stages[0].produced_artifacts == ["LiteratureCorpus"]


@pytest.mark.asyncio
async def test_end_to_end_workflow_run_execution():
    """Verify a complete event-driven run of the AI Research workflow from question to publication."""
    repo = ResearchRepository()
    bus = EventBus()
    registry = PluginRegistry()

    # Register governance boards
    registry.register_governance(EthicsReviewBoard())
    registry.register_governance(ScientificQualityBoard())
    registry.register_governance(SecurityBoard())
    registry.register_governance(CapitalAllocationBoard())

    # Register pluggable agent
    registry.register_agent(MockDomainScientist())

    engine = WorkflowEngine(repository=repo, event_bus=bus, plugin_registry=registry)

    # Register AI Research WDL
    builtin = create_builtin_workflows()
    ai_wdl = [w for w in builtin if w.id == "ai_research"][0]
    engine.register_workflow(ai_wdl)

    # Start Project and initialize Run
    project = ResearchProject(name="AGI Scalability", funding_budget=100000.0).with_signature()
    repo.save_artifact(project)

    question = ResearchQuestion(question_text="How to optimize graph layers?", domain="AI Research").with_signature()
    repo.save_artifact(question)

    run_id = engine.start_run("ai_research", project.uuid)
    run = engine.active_runs[run_id]

    # Initialize the workflow context with the initial input artifact
    run.artifacts["ResearchQuestion"] = question.uuid

    # Simulate event dispatch to trigger literature_review stage completion
    bus.publish(ArtifactCreated(
        artifact_uuid=question.uuid,
        artifact_type="ResearchQuestion",
        author="ExecutiveDirector",
        confidence=1.0,
        parent_uuids=[]
    ))

    # Give async tasks a moment to execute
    await asyncio.sleep(0.5)

    # Validate that run succeeded, history shows stages executed, and publications are created
    assert run.status == "COMPLETED" or len(run.history) > 1
    assert "literature_review" in run.history
    assert len(repo.list_artifacts_by_type(Publication)) > 0


# =====================================================================
# Advanced Institutional Subsystems Test Cases
# =====================================================================

@pytest.mark.asyncio
async def test_uncertainty_bayesian_updates_and_decay():
    """Verify conjugate Beta-prior updates and temporal confidence decay functions."""
    # Prior Beta distribution: alpha=2, beta=2 (unbiased prior, expected_prob = 0.5)
    a, b = 2.0, 2.0
    prob_prior = calculate_expected_probability(a, b)
    assert prob_prior == 0.5

    # 1. Update with supporting evidence (reliability = 0.8)
    a, b = update_belief(a, b, evidence_support=1.0, evidence_conflict=0.0, evidence_reliability=0.8)
    prob_post_support = calculate_expected_probability(a, b)
    assert prob_post_support == 2.8 / (2.8 + 2.0)  # ~0.5833
    assert calculate_epistemic_entropy(a, b) < 0.5  # Information gained decreases epistemic ignorance

    # 2. Update with conflicting evidence
    a, b = update_belief(a, b, evidence_support=0.0, evidence_conflict=1.0, evidence_reliability=1.0)
    prob_post_conflict = calculate_expected_probability(a, b)
    assert prob_post_conflict < prob_post_support

    # 3. Temporal Decay validation
    creation_time = time.time() - 100.0  # 100 seconds ago
    decayed = apply_temporal_decay(initial_confidence=1.0, creation_timestamp=creation_time, lambda_decay=0.01)
    # 1.0 * e^(-0.01 * 100) = e^(-1) ~ 0.3678
    assert abs(decayed - 0.3678) < 0.01


@pytest.mark.asyncio
async def test_portfolio_scheduler_and_allocations():
    """Verify compute allocation optimization and opportunities-cost based termination logic."""
    scheduler = PortfolioScheduler(total_gpu_tokens_budget=100000)

    # Register two competing research projects
    p1 = ResearchProject(name="Project AI Large", funding_budget=50000.0, expected_discovery_value=500.0)
    p2 = ResearchProject(name="Project Trading Beta", funding_budget=120000.0, expected_discovery_value=300.0)

    scheduler.add_project(p1)
    scheduler.add_project(p2)

    # Setup historical success rates
    success_rates = {p1.uuid: 0.8, p2.uuid: 0.4}

    # Verify priority calculation
    score_1 = scheduler.calculate_project_priority(p1, success_rates[p1.uuid])
    score_2 = scheduler.calculate_project_priority(p2, success_rates[p2.uuid])

    # AI Large (EDV = 0.8 * 500 = 400, no budget penalty) -> 400
    # Trading Beta (EDV = 0.4 * 300 = 120, has penalty for over 100k budget) -> ~119.88
    assert score_1 == 400.0
    assert score_2 < 120.0

    # Optimize resource quotas
    allocations = scheduler.optimize_portfolio(success_rates)
    assert len(allocations) == 2
    alloc_p1 = [a for a in allocations if a.project_uuid == p1.uuid][0]
    alloc_p2 = [a for a in allocations if a.project_uuid == p2.uuid][0]

    assert alloc_p1.allocated_tokens > alloc_p2.allocated_tokens
    assert abs((alloc_p1.compute_quota + alloc_p2.compute_quota) - 1.0) < 0.001

    # Check for programmatic terminations
    success_low = {p1.uuid: 0.8, p2.uuid: 0.01}  # Trading Beta EDV drops to 0.01 * 300 = 3
    terminated_uuids = scheduler.check_for_terminations(success_low, min_edv_threshold=10.0)
    assert p2.uuid in terminated_uuids
    assert p2.uuid not in scheduler.active_projects


@pytest.mark.asyncio
async def test_w3c_provenance_graph():
    """Verify building and querying of W3C PROV-O standard artifact lineage and dataset dependencies."""
    engine = ProvenanceEngine()

    dataset_uuid = uuid4()
    task_run_uuid = uuid4()
    experiment_uuid = uuid4()
    claim_uuid = uuid4()

    # Record relations
    # task run used dataset
    engine.record_relation("USED_DATASET", task_run_uuid, dataset_uuid)
    # experiment was generated by task run
    engine.record_relation("WAS_GENERATED_BY", experiment_uuid, task_run_uuid)
    # claim was derived from experiment
    engine.record_relation("DERIVED_FROM", claim_uuid, experiment_uuid)

    # Trace backward to find original source dataset dependencies
    sources = engine.trace_source_datasets(claim_uuid)
    assert len(sources) == 1
    assert sources[0] == dataset_uuid


@pytest.mark.asyncio
async def test_self_improvement_flywheel_policy_evolution():
    """Verify logged failures compile and evolve into non-bypassable InstitutionalPolicies."""
    repo = ResearchRepository()
    bus = EventBus()
    flywheel = SelfImprovementFlywheel(repository=repo, event_bus=bus)

    # Log consecutive failures for the 'execution' stage
    run_1 = uuid4()
    run_2 = uuid4()
    flywheel.log_failure(run_1, "execution", "ML training sandbox out of memory error.")
    flywheel.log_failure(run_2, "execution", "Execution timeout after 1000 epochs.")

    # Trigger bottleneck analysis and policy formulation
    new_policy = flywheel.analyze_bottlenecks_and_evolve()

    assert new_policy is not None
    assert "Stricter Quality Rule for Execution" in new_policy.policy_name
    assert len(new_policy.rules) == 2
    assert "replicates" in new_policy.rules[1]

    # Verify policy is compiled and successfully saved in Repository
    retrieved_policies = repo.list_artifacts_by_type(InstitutionalPolicy)
    assert len(retrieved_policies) == 1
    assert retrieved_policies[0].uuid == new_policy.uuid
