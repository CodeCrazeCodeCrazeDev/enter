# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration and verification test suite
for the 100 new research papers (IDs 301-400), 100% zero-overlap audit across all 400 papers,
extracted transferable principles, Research OS literature review integration, and runtime component enhancements.
"""

import os
import yaml
import pytest
from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.research_os.statistical_validation import standard_normal_ppf, standard_normal_cdf, calculate_dsr


def test_400_paper_zero_overlap_audit():
    """Verify that all 400 papers (1-400 across 3 databases) have 100% unique titles and DOIs."""
    db1_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    db2_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    db3_path = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"

    assert os.path.exists(db1_path)
    assert os.path.exists(db2_path)
    assert os.path.exists(db3_path)

    with open(db1_path, "r", encoding="utf-8") as f:
        db1 = yaml.safe_load(f)
    with open(db2_path, "r", encoding="utf-8") as f:
        db2 = yaml.safe_load(f)
    with open(db3_path, "r", encoding="utf-8") as f:
        db3 = yaml.safe_load(f)

    papers1 = db1.get("papers", [])
    papers2 = db2.get("papers", [])
    papers3 = db3.get("papers", [])

    assert len(papers1) == 200
    assert len(papers2) == 100
    assert len(papers3) == 100

    titles = []
    dois = []

    for p in papers1 + papers2 + papers3:
        meta = p["metadata"]
        titles.append(meta["title"].lower().strip())
        if "doi" in meta and meta["doi"]:
            dois.append(meta["doi"].lower().strip())

    assert len(titles) == 400
    assert len(set(titles)) == 400, "Found duplicate titles in 400-paper corpus!"
    assert len(dois) == 200  # DB1 has 0 DOIs, DB2 has 100, DB3 has 100 = 200 total DOIs
    assert len(set(dois)) == 200, "Found duplicate DOIs in 400-paper corpus!"


def test_principle_registration_and_research_os_review():
    """Test principle registration and ResearchOS literature review querying over 400-paper principles."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 5
    assert "hawkes_non_gaussian_stability" in principles
    assert "island_map_elites_migration" in principles
    assert "clipped_advantage_preference_margins" in principles
    assert "budget_decayed_efe_routing" in principles

    ros = ResearchOS()
    review = ros.conduct_literature_review("Market Microstructure")
    assert review["reviewed_citations_count"] == 400
    assert "Non-Gaussian Hawkes Self-Excitation Stability Guard" in review["matching_corpus_principles"]


def test_code_rewrite_engine_hawkes_ast_depth_veto(tmp_path):
    """Test Papers 301-320 Hawkes AST recursion depth check in CodeRewriteEngine."""
    allowed_dir = str(tmp_path)
    engine = CodeRewriteEngine(allowed_paths=[allowed_dir], max_ast_depth=3)

    # Valid non-recursive snippet
    valid_code = "def process_data(x):\n    return x * 2\n"
    prop_valid = engine.propose_rewrite(
        filepath=os.path.join(allowed_dir, "test.py"),
        original_snippet="",
        proposed_snippet=valid_code,
        rationale="Normal snippet"
    )
    assert engine.verify_proposal_ast(prop_valid) is True

    # Snippet exceeding max allowed recursion call depth (4 calls > max 3)
    recursive_code = (
        "def recursive_fn(n):\n"
        "    if n <= 0: return 0\n"
        "    a = recursive_fn(n - 1)\n"
        "    b = recursive_fn(n - 2)\n"
        "    c = recursive_fn(n - 3)\n"
        "    d = recursive_fn(n - 4)\n"
        "    return a + b + c + d\n"
    )
    prop_invalid = engine.propose_rewrite(
        filepath=os.path.join(allowed_dir, "test.py"),
        original_snippet="",
        proposed_snippet=recursive_code,
        rationale="Exceeds recursion depth"
    )
    assert engine.verify_proposal_ast(prop_invalid) is False


def test_genetic_workflow_optimizer_island_migration():
    """Test Papers 341-360 Island MAP-Elites migration gateways."""
    optimizer = GeneticWorkflowOptimizer(population_size=4, mutation_rate=0.1, num_islands=2)
    optimizer.initialize_population(
        base_template="Base execution prompt",
        base_params={"learning_rate": 0.01}
    )

    # Assign fitness scores
    optimizer.population[0].fitness_score = 0.90
    optimizer.population[1].fitness_score = 0.80
    optimizer.population[2].fitness_score = 0.30
    optimizer.population[3].fitness_score = 0.20

    migrated_count = optimizer.perform_island_migration(min_fitness_threshold=0.50)
    assert migrated_count > 0


def test_sft_preference_collector_clipped_margin():
    """Test Papers 361-380 clipped advantage margin in trajectory DPO compilation."""
    collector = SFTPreferenceCollector(discount_factor=0.95, max_advantage_margin=3.0)

    steps_a = [
        TrajectoryStep(action="a1", predicted_expectation=0.0, actual_outcome=10.0, reward=10.0),
        TrajectoryStep(action="a2", predicted_expectation=0.0, actual_outcome=20.0, reward=20.0)
    ]
    steps_b = [
        TrajectoryStep(action="b1", predicted_expectation=0.0, actual_outcome=0.1, reward=0.1)
    ]

    pair = collector.compile_dpo_preference_pair("Optimize portfolio", steps_a, steps_b)
    assert pair["margin"] == 3.0  # Clipped to max_advantage_margin (3.0)
    assert pair["raw_margin"] > 3.0


def test_learnable_routing_dispatcher_budget_decay():
    """Test Papers 381-400 budget-decayed EFE routing gate dispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0, decay_rate=0.10)
    agent_a = SpecializedAgentProfile(agent_id="cheap", domain_specialty="Market Microstructure", cost_per_token=0.001)
    agent_b = SpecializedAgentProfile(agent_id="expensive", domain_specialty="Market Microstructure", cost_per_token=0.05)

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    # Low budget spent -> routes to best EFE agent
    selected_1 = dispatcher.route_task(task_complexity=10.0, domain="Market Microstructure")
    assert selected_1 in {"cheap", "expensive"}

    # Spend budget
    dispatcher.update_routing_parameters("expensive", success=True, cost_incurred=9.5)
    selected_2 = dispatcher.route_task(task_complexity=10.0, domain="Market Microstructure")
    assert selected_2 == "cheap"  # Fallback to cheap agent due to budget boundaries


def test_statistical_validation_bounds():
    """Test statistical validation inverse normal PPF clamping and safe DSR."""
    # PPF at boundaries (p=0 and p=1 should be safely clamped without raising ValueError)
    val_low = standard_normal_ppf(0.0)
    val_high = standard_normal_ppf(1.0)
    assert isinstance(val_low, float)
    assert isinstance(val_high, float)

    # DSR calculation with 1 return observation
    dsr = calculate_dsr(sharpe=1.5, trials=5, returns_length=1)
    assert 0.0 <= dsr <= 1.0
