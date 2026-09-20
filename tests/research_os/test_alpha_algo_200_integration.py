# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite for the 200-paper research corpus (IDs 301-500),
extracted transferable principles, and cross-layer cognitive OS runtime enhancements.
"""

import os
import yaml
import pytest
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_301_500_paper_corpus_principles,
    ALPHAALGO_301_500_PRINCIPLES,
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    ProgramGenome,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    ResearchToSystemBridge
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_500_paper_corpus_zero_overlap():
    """Verify zero title/DOI overlap across all 500 research papers (1-200, 201-300, 301-500)."""
    db_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    ]

    all_papers = []
    seen_titles = set()
    seen_dois = set()

    for path in db_paths:
        assert os.path.exists(path), f"Research database {path} missing"
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            papers = data.get("papers", [])
            all_papers.extend(papers)

    assert len(all_papers) == 500, f"Expected 500 papers total, found {len(all_papers)}"

    for p in all_papers:
        title = p["metadata"]["title"].strip().lower()
        doi = p.get("metadata", {}).get("doi", p.get("doi", "")).strip().lower()

        assert title not in seen_titles, f"Duplicate paper title found: {title}"
        if doi:
            assert doi not in seen_dois, f"Duplicate paper DOI found: {doi}"
            seen_dois.add(doi)

        seen_titles.add(title)


def test_principle_registration_and_literature_review():
    """Verify registration of 200-paper corpus principles and literature review querying."""
    principles = register_301_500_paper_corpus_principles()
    assert len(principles) >= 6
    assert "multi_agent_swarm_bidding" in principles
    assert "active_inference_continuous_sensing" in principles

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")

    assert review["domain"] == "Active Inference"
    assert review["matching_principles_count"] > 0
    assert len(review["synthesized_trends"]) > 0


def test_code_rewrite_engine_hawkes_ast_check(tmp_path):
    """Verify AST syntax linting and Hawkes non-Gaussian recursive call depth checks in CodeRewriteEngine."""
    engine = CodeRewriteEngine(allowed_paths=[str(tmp_path)], max_recursion_depth=3)

    # 1. Valid proposal
    valid_snippet = "def calculate_sum(a, b):\n    return a + b"
    proposal = engine.propose_rewrite(
        filepath=os.path.join(str(tmp_path), "test.py"),
        original_snippet="",
        proposed_snippet=valid_snippet,
        rationale="Add simple sum helper function"
    )
    assert engine.verify_proposal_ast(proposal) is True

    # 2. Veto proposal with excessive recursion
    recursive_snippet = (
        "def runaway_func(n):\n"
        "    if n > 0:\n"
        "        runaway_func(n-1)\n"
        "        runaway_func(n-1)\n"
        "        runaway_func(n-1)\n"
        "        runaway_func(n-1)\n"
        "    return n"
    )
    bad_proposal = engine.propose_rewrite(
        filepath=os.path.join(str(tmp_path), "test_bad.py"),
        original_snippet="",
        proposed_snippet=recursive_snippet,
        rationale="Unsafe runaway recursive function"
    )
    assert engine.verify_proposal_ast(bad_proposal) is False


def test_map_elites_island_migration():
    """Verify island MAP-Elites migration gates in GeneticWorkflowOptimizer."""
    island_a = GeneticWorkflowOptimizer(population_size=5)
    island_b = GeneticWorkflowOptimizer(population_size=5)

    island_a.initialize_population("Base template A", {"param_a": 1.0})
    island_b.initialize_population("Base template B", {"param_b": 2.0})

    island_a.evaluate_generation(lambda g: float(g.parameters.get("param_a", 0.0) * 10))

    initial_b_size = len(island_b.population)
    migrated_count = island_a.apply_island_migration_gate(island_b, fitness_percentile=0.8)

    assert migrated_count > 0
    assert len(island_b.population) == initial_b_size + migrated_count


def test_sft_preference_collector_clipped_advantage():
    """Verify clipped trajectory advantage margin in SFTPreferenceCollector."""
    collector = SFTPreferenceCollector(margin_bounds=(-2.0, 2.0))

    run_a = [
        TrajectoryStep(action="action_a1", predicted_expectation=1.0, actual_outcome=10.0, reward=10.0),
        TrajectoryStep(action="action_a2", predicted_expectation=1.0, actual_outcome=10.0, reward=10.0)
    ]
    run_b = [
        TrajectoryStep(action="action_b1", predicted_expectation=5.0, actual_outcome=0.0, reward=0.0),
        TrajectoryStep(action="action_b2", predicted_expectation=5.0, actual_outcome=0.0, reward=0.0)
    ]

    pair = collector.compile_dpo_preference_pair("Prompt string", run_a, run_b)

    assert "chosen" in pair
    assert "rejected" in pair
    assert pair["margin"] <= 2.0
    assert pair["margin"] >= -2.0


def test_learnable_routing_gate_budget_decay():
    """Verify budget decay penalty scaling in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_cheap = SpecializedAgentProfile(agent_id="agent_cheap", domain_specialty="nlp", cost_per_token=0.001)
    agent_expert = SpecializedAgentProfile(agent_id="agent_expert", domain_specialty="nlp", cost_per_token=0.05)

    dispatcher.register_subagent(agent_cheap)
    dispatcher.register_subagent(agent_expert)

    chosen_agent = dispatcher.route_task(task_complexity=100.0, domain="nlp")
    assert chosen_agent in {"agent_cheap", "agent_expert"}

    dispatcher.budget_spent = 9.5
    cheapest_chosen = dispatcher.route_task(task_complexity=100.0, domain="nlp")
    assert cheapest_chosen == "agent_cheap"


def test_cross_layer_state_handoff_bridge():
    """Verify ResearchToSystemBridge handoffs across Layer 1 to Layer 4 components."""

    class MockKernel:
        def __init__(self):
            self.registered = []
        def register_research_hypothesis(self, rec):
            self.registered.append(rec)

    class MockEOS:
        def __init__(self):
            self.ingested = []
        def ingest_validated_research(self, rec):
            self.ingested.append(rec)

    class MockHiveMind:
        def __init__(self):
            self.insights = []
        def register_research_insight(self, rec):
            self.insights.append(rec)

    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Test Bridge Hypothesis",
        description="Hypothesis description",
        null_hypothesis="Null statement",
        target_metric="accuracy"
    )
    hyp.status = "validated"

    kernel = MockKernel()
    eos = MockEOS()
    hive_mind = MockHiveMind()

    bridge = ResearchToSystemBridge(ros, kernel, eos, hive_mind)
    record = bridge.promote_validated_hypothesis(hyp.hypothesis_id)

    assert record["title"] == "Test Bridge Hypothesis"
    assert len(kernel.registered) == 1
    assert len(eos.ingested) == 1
    assert len(hive_mind.insights) == 1
