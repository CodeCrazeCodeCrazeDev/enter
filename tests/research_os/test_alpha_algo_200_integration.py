# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite verifying 200-paper research corpus (IDs 301-500),
zero duplicate overlap against papers 1-300, principle registration, Research OS literature synthesis,
and subsystem integration across AEAN, EOS, EIOS, and Research OS.
"""

import os
import yaml
import pytest
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    RewriteProposal,
    ResearchToSystemBridge
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.aean.coordination.hive_mind import HiveMind


def test_200_paper_corpus_integrity_and_zero_duplicate_overlap():
    """Verifies that 200 papers exist in ALPHA_ALGO_200_NEW_RESEARCH.yaml with 0% duplicate overlap."""
    db_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(db_path), f"File {db_path} must exist."

    with open(db_path, "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    papers = db.get("papers", [])
    assert len(papers) == 200, f"Expected 200 papers, got {len(papers)}"

    # Check IDs 301 to 500
    p_ids = [p["id"] for p in papers]
    assert min(p_ids) == 301
    assert max(p_ids) == 500

    # Cross-database duplicate title check against papers 1-300
    existing_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]
    seen_titles = set()
    for path in existing_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                prev_db = yaml.safe_load(f)
                for prev_p in prev_db.get("papers", []):
                    seen_titles.add(prev_p["metadata"]["title"].lower().strip())

    for p in papers:
        t = p["metadata"]["title"].lower().strip()
        assert t not in seen_titles, f"Duplicate paper title detected: '{t}'"


def test_principle_registration_and_literature_review():
    """Verifies principle registration and ResearchOS literature review querying."""
    principles = register_200_paper_corpus_principles()
    assert len(principles) == 200

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")

    assert review["domain"] == "Active Inference"
    assert review["matched_principles_count"] >= 10
    assert len(review["synthesized_trends"]) > 0


def test_subsystem_enhancements_runtime():
    """Verifies CodeRewriteEngine, GeneticWorkflowOptimizer, SFTPreferenceCollector, and LearnableRoutingGateDispatcher."""
    # 1. CodeRewriteEngine AST verification
    engine = CodeRewriteEngine(allowed_paths=["."])
    proposal = engine.propose_rewrite(
        filepath="test_file.py",
        original_snippet="x = 1",
        proposed_snippet="x = 2",
        rationale="Optimize constant"
    )
    assert engine.verify_proposal_ast(proposal) is True

    dangerous_proposal = engine.propose_rewrite(
        filepath="test_file.py",
        original_snippet="x = 1",
        proposed_snippet="eval('import os; os.system(\"rm -rf /\")')",
        rationale="Dangerous code injection"
    )
    assert engine.verify_proposal_ast(dangerous_proposal) is False

    # 2. GeneticWorkflowOptimizer MAP-Elites sorting
    optimizer = GeneticWorkflowOptimizer(population_size=5)
    optimizer.initialize_population(
        base_template="Task execution prompt",
        base_params={"lr": 0.01, "mode": True}
    )
    evaluated = optimizer.evaluate_generation(lambda g: sum(g.parameters.values()) if isinstance(g.parameters.get("lr"), (int, float)) else 0.5)
    assert len(evaluated) == 5
    assert evaluated[0].fitness_score >= evaluated[-1].fitness_score

    # 3. SFTPreferenceCollector advantage clipping
    collector = SFTPreferenceCollector(discount_factor=0.95)
    steps_a = [
        TrajectoryStep(action="a1", predicted_expectation=0.5, actual_outcome=1.0, reward=1.0),
        TrajectoryStep(action="a2", predicted_expectation=0.8, actual_outcome=1.2, reward=1.2)
    ]
    steps_b = [
        TrajectoryStep(action="b1", predicted_expectation=0.5, actual_outcome=0.2, reward=-0.5),
        TrajectoryStep(action="b2", predicted_expectation=0.1, actual_outcome=0.1, reward=-0.2)
    ]
    pair = collector.compile_dpo_preference_pair("Solve task", steps_a, steps_b)
    assert pair["chosen"] is not None
    assert pair["margin"] > 0.0

    # 4. LearnableRoutingGateDispatcher EFE task routing
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=100.0)
    agent = SpecializedAgentProfile(agent_id="agent_1", domain_specialty="Active Inference", cost_per_token=0.01)
    dispatcher.register_subagent(agent)
    selected = dispatcher.route_task(task_complexity=10.0, domain="Active Inference")
    assert selected == "agent_1"


def test_cross_layer_closed_loop_integration():
    """Verifies end-to-end active inference state handoffs across ResearchOS, EOSEngine, EIOSKernel, AEAN HiveMind."""
    ros = ResearchOS()
    eos = EOSEngine()
    kernel = EIOSKernel()
    hm = HiveMind(token_budget=100)

    # 1. Register hypothesis in Research OS
    hyp = ros.register_hypothesis(
        title="Hawkes Order Toxicity Estimation",
        description="Self-exciting process modeling order toxicity under stress",
        null_hypothesis="No correlation with order imbalance",
        target_metric="toxicity_index"
    )

    # 2. Bridge handoff
    bridge = ResearchToSystemBridge(ros, eos, kernel, hm)
    result = bridge.handoff_validated_hypothesis(hyp.hypothesis_id)

    assert result["eos_ingested"] is True
    assert result["eios_registered"] is True
    assert result["hive_mind_grant"].granted is True

    # 3. EIOS anomaly sensing
    signals = [1.0, 1.1, 0.9, 1.2, 5.5, 1.0, 0.8]  # Signal at index 4 is anomaly (z > 2.0)
    anomalies = kernel.sense_opportunity_anomalies(signals)
    assert len(anomalies) == 1
    assert anomalies[0]["signal_index"] == 4

    # 4. EOS Engine hypothesis inspection
    assert len(eos.active_hypotheses) == 1
    assert eos.active_hypotheses[0].title == "Hawkes Order Toxicity Estimation"

    # 5. HiveMind task grant history
    assert len(hm.granted_history) == 1
