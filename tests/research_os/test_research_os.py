from __future__ import annotations
import pytest
import uuid
import datetime

from apodex.research_os.wdl import WorkflowExecutionEngine, WDLWorkflow
from apodex.research_os.uncertainty import UncertaintyAnalyzer, EvidenceCard, TheoryNode
from apodex.research_os.provenance import ProvenanceEngine, PROVEntity, PROVActivity
from apodex.research_os.self_improvement import ResearchSelfImprovementEngine, BottleneckFailure
from apodex.research_os.portfolio import ResearchPortfolioScheduler, ResearchProject
from apodex.research_os.governance import MultiBoardGovernanceGateway, GovernanceProposal


@pytest.mark.asyncio
async def test_wdl_workflow_engine() -> None:
    engine = WorkflowExecutionEngine()

    raw_wdl = {
        "research_project": "dynamic_learning_rate_optimization",
        "hypothesis": {
            "target_variable": "model_accuracy",
            "null_hypothesis": "modifying learning rates has no effect.",
            "alternative_hypothesis": "adaptive learning rates increase accuracy by 5%."
        },
        "tasks": [
            {
                "name": "generate_raw_traces",
                "executor": "data_agent",
                "sandbox_constraints": {
                    "max_memory_gb": 2.0,
                    "timeout_seconds": 120,
                    "allow_network": False
                },
                "inputs": {"size": 500}
            },
            {
                "name": "train_model",
                "executor": "training_agent",
                "sandbox_constraints": {
                    "max_memory_gb": 8.0,
                    "timeout_seconds": 600,
                    "allow_network": True
                }
            }
        ]
    }

    workflow = engine.parse_workflow(raw_wdl)
    assert workflow.research_project == "dynamic_learning_rate_optimization"
    assert len(workflow.tasks) == 2
    assert workflow.tasks[0].sandbox_constraints.max_memory_gb == 2.0

    # Run the execution simulation
    result = await engine.execute_workflow_steps(workflow)
    assert result["status"] == "success"
    assert result["evidence_registered"] is True
    assert len(result["task_outcomes"]) == 2


def test_uncertainty_analyzer() -> None:
    analyzer = UncertaintyAnalyzer(decay_rate=0.05)

    # 1. Entropy calculation
    entropy = analyzer.calculate_epistemic_entropy(10.0, 10.0)
    assert entropy > 0.0

    # 2. Update with decay
    # Decays alpha=11 and beta=11 over 20 days: e^(-0.05*20) = e^(-1) ≈ 0.3678
    # 10 successes, 0 failures added
    new_alpha, new_beta = analyzer.update_beliefs_with_decay(
        prior_alpha=11.0,
        prior_beta=11.0,
        successes=10,
        failures=0,
        elapsed_days=20.0
    )
    # Expected alpha excess = 10 * 0.3678 = 3.678. New alpha = 1 + 3.678 + 10 = 14.678
    assert pytest.approx(new_alpha, abs=1e-2) == 14.678
    assert pytest.approx(new_beta, abs=1e-2) == 4.678

    # 3. Theory promotion and contradiction detection
    hyp_id = uuid.uuid4()
    evidence = EvidenceCard(
        hypothesis_id=hyp_id,
        empirical_mean=0.85,
        replications_count=3,
        sample_size=150
    )

    theory = analyzer.promote_to_theory("lr_effect", evidence)
    assert theory is not None
    assert theory.name == "lr_effect"
    assert theory.expected_value == 0.85

    # Test contradiction detection with opposing evidence (empirical mean = 0.40)
    opposing_evidence = EvidenceCard(
        hypothesis_id=hyp_id,
        empirical_mean=0.40
    )
    contradictions = analyzer.detect_contradictions(opposing_evidence)
    assert len(contradictions) == 1
    assert contradictions[0]["status"] == "critical_contradiction"


def test_provenance_engine() -> None:
    engine = ProvenanceEngine()

    # Record entities, activities, and agents
    dataset = engine.record_entity({"name": "mnist_raw_dataset"})
    training = engine.record_activity({"name": "train_neural_network"})
    agent = engine.record_agent({"name": "system_training_bot"})

    # Map relationships
    # training 'used' dataset
    engine.assert_relation(training.id, dataset.id, "used")
    # training 'wasAssociatedWith' agent
    engine.assert_relation(training.id, agent.id, "wasAssociatedWith")

    lineage = engine.query_lineage(training.id)
    assert len(lineage) == 2
    assert any(item["ancestor_id"] == dataset.id for item in lineage)
    assert any(item["ancestor_id"] == agent.id for item in lineage)


def test_self_improvement_engine() -> None:
    engine = ResearchSelfImprovementEngine()

    failure = BottleneckFailure(
        task_name="train_model",
        error_signature="TimeoutError in parallel compilation steps"
    )

    policy = engine.compile_failure_to_policy(failure)
    assert policy.target_pattern == "train_model"
    assert "parallel execution" in policy.remedy_instruction

    # Verify prompt optimization
    base_prompt = "You are a machine learning agent."
    optimized = engine.optimize_system_prompts(base_prompt, "train_model")
    assert "Self-Improvement Policy" in optimized
    assert "Enforce batch-size reduction" in optimized


def test_portfolio_scheduler() -> None:
    scheduler = ResearchPortfolioScheduler()

    proj_1 = ResearchProject(
        name="lr_tuning",
        expected_discovery_value_usd=5000.0,
        cost_estimate_tokens=1000000,
        probability_of_success=0.6,
        epistemic_information_gain=1.5
    )

    proj_2 = ResearchProject(
        name="architecture_search",
        expected_discovery_value_usd=10000.0,
        cost_estimate_tokens=15000000,  # very high cost
        probability_of_success=0.3,
        epistemic_information_gain=0.8
    )

    prioritized = scheduler.prioritize_projects([proj_1, proj_2])
    assert len(prioritized) == 2
    # proj_1 should rank higher because high cost of proj_2 penalizes its utility index
    assert prioritized[0][0].name == "lr_tuning"


def test_governance_gateway() -> None:
    gateway = MultiBoardGovernanceGateway(complexity_budget=40)

    # 1. Compliant proposal
    prop_ok = GovernanceProposal(
        target_capability="parallel_optimization",
        risk_score=0.2,
        code_complexity=20
    )
    result_ok = gateway.evaluate_proposal(prop_ok)
    assert result_ok["approved"] is True
    assert result_ok["status"] == "APPROVED"
    assert result_ok["boards"]["ethics"]["approved"] is True
    assert result_ok["boards"]["capital"]["allocated_tokens"] == 800

    # 2. Non-compliant proposal (violates complexity budget)
    prop_bad = GovernanceProposal(
        target_capability="heavy_mutation",
        risk_score=0.1,
        code_complexity=100  # violates complexity limit of 40
    )
    result_bad = gateway.evaluate_proposal(prop_bad)
    assert result_bad["approved"] is False
    assert result_bad["status"] == "REJECTED"
    assert result_bad["boards"]["security"]["approved"] is False
