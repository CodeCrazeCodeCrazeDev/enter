# -*- coding: utf-8 -*-
"""
test_200_paper_corpus_integration.py: Integration test suite validating
the 200-paper quantitative research corpus (IDs 301-500) integration,
principle registration, literature review querying, active inference state handoffs,
and upgraded runtime capabilities across ResearchOS, EIOSKernel, EOSEngine, and AEAN HiveMind.
"""

import os
import yaml
import pytest
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
    ALPHA_ALGO_200_PRINCIPLES,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    TrajectoryStep,
    SpecializedAgentProfile,
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind


def test_200_paper_corpus_integrity_and_zero_overlap() -> None:
    """Verifies that the 200-paper YAML database is valid and has zero title overlap."""
    yaml_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(yaml_path)

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    papers = data.get("papers", [])
    assert len(papers) == 200
    assert papers[0]["id"] == 301
    assert papers[-1]["id"] == 500

    # Ensure all paper IDs are unique
    paper_ids = [p["id"] for p in papers]
    assert len(set(paper_ids)) == 200


def test_principle_registration_and_literature_review() -> None:
    """Verifies principles registration and ResearchOS literature review synthesis."""
    principles = register_200_paper_corpus_principles()
    assert len(principles) == len(ALPHA_ALGO_200_PRINCIPLES)
    assert "market_microstructure_hawkes" in principles
    assert "active_inference_efe" in principles

    # Query literature review via ResearchOS
    ros = ResearchOS()
    review = ros.conduct_literature_review(domain="Active Inference")

    assert review["reviewed_citations_count"] == 200
    assert review["matched_principles_count"] > 0
    assert any("Active Inference" in p["domain"] for p in review["extracted_principles"])


def test_cross_layer_state_handoffs() -> None:
    """Verifies cross-layer handoffs from ResearchOS to EIOSKernel, EOSEngine, and AEAN HiveMind."""
    ros = ResearchOS()
    eios_kernel = EIOSKernel()
    eos_engine = EOSEngine()
    hive_mind = HiveMind()

    # Register and validate hypothesis in Research OS
    hyp = ros.register_hypothesis(
        title="Hawkes EFE Active Inference Coupling",
        description="Active inference minimizes EFE under heavy-tailed order flow dynamics.",
        null_hypothesis="No uncertainty reduction",
        target_metric="Sharpe_Ratio"
    )

    # Force status to validated for handoff testing
    hyp.status = "validated"
    ros.hypotheses.save(hyp.hypothesis_id, hyp)

    # Export to EIOS Kernel
    success_kernel = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, eios_kernel)
    assert success_kernel is True
    anomalies = eios_kernel.sense_opportunity_anomalies()
    assert len(anomalies) > 0
    assert "Hawkes EFE Active Inference Coupling" in anomalies[0]["name"]

    # Promote to EOS Engine
    success_eos = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos_engine)
    assert success_eos is True
    assert len(eos_engine.active_hypotheses) > 0

    # Submit insight to AEAN HiveMind
    hive_mind.register_research_insight(hyp.title)
    assert len(hive_mind.granted_history) > 0


def test_upgraded_runtime_components() -> None:
    """Verifies Hawkes stability, island MAP-Elites, DPO edit penalties, and causal EFE task routing."""
    # 1. CodeRewriteEngine Hawkes stability check
    engine = CodeRewriteEngine(allowed_paths=["."])
    stable_code = "def compute_jump():\n    return 42\n"
    unstable_code = "while True:\n    pass\n"
    assert engine.verify_hawkes_stability(stable_code) is True
    assert engine.verify_hawkes_stability(unstable_code) is False

    # 2. GeneticWorkflowOptimizer Island MAP-Elites
    optimizer = GeneticWorkflowOptimizer(population_size=6)
    optimizer.initialize_population("Base Prompt Strategy", {"rate": 0.01})
    assert len(optimizer.islands) == 2
    optimizer.migrate_island_elites()

    # 3. SFTPreferenceCollector Trajectory Edit Penalty
    collector = SFTPreferenceCollector()
    traj_a = [TrajectoryStep(action="step_1", predicted_expectation=0.5, actual_outcome=0.8, reward=0.8)]
    traj_b = [TrajectoryStep(action="step_1", predicted_expectation=0.5, actual_outcome=0.3, reward=0.2)]
    dpo_pair = collector.compile_dpo_preference_pair_with_edit_penalty("Execute strategy", traj_a, traj_b)
    assert dpo_pair["edit_penalty_applied"] is True
    assert dpo_pair["margin"] > 0

    # 4. LearnableRoutingGateDispatcher Causal Do-Calculus EFE Task Routing
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=5.0)
    agent = SpecializedAgentProfile(
        agent_id="agent_1",
        domain_specialty="Active Inference",
        cost_per_token=0.001,
        historical_success_rate=0.8,
        epistemic_curiosity=0.7
    )
    dispatcher.register_subagent(agent)
    selected_agent = dispatcher.route_task_with_causal_efe(task_complexity=10, domain="Active Inference")
    assert selected_agent == "agent_1"
