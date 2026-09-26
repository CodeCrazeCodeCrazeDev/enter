# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite verifying the 200-paper corpus
(IDs 301-500) schema validity, 0% duplicate overlap against existing papers (1-300),
corpus principle registration, Research OS literature review querying, and runtime component enhancements.
"""

import os
import yaml
import pytest
from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
    ALPHAALGO_200_PRINCIPLES,
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_200_paper_corpus_schema_and_zero_overlap():
    """Verify that the 200-paper corpus YAML exists, has 200 papers (301-500), and has 0% duplicate overlap."""
    yaml_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(yaml_path), f"YAML file missing: {yaml_path}"

    with open(yaml_path, "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    papers = db.get("papers", [])
    assert len(papers) == 200, f"Expected 200 papers, found {len(papers)}"
    assert papers[0]["id"] == 301, f"Expected start ID 301, got {papers[0]['id']}"
    assert papers[-1]["id"] == 500, f"Expected end ID 500, got {papers[-1]['id']}"

    # Verify zero duplicates in detection matrix
    duplicate_matrix = db.get("duplicate_detection_matrix", [])
    assert len(duplicate_matrix) == 200
    flagged = [row for row in duplicate_matrix if row["status"] == "FLAGGED DUPLICATE"]
    assert len(flagged) == 0, f"Found {len(flagged)} flagged duplicate papers!"


def test_corpus_principle_registration():
    """Verify that register_200_paper_corpus_principles returns registered principles for AEAN, EOS, EIOS, and ResearchOS."""
    principles = register_200_paper_corpus_principles()
    assert len(principles) == 4
    subsystems = {p["target_subsystem"] for p in principles}
    assert subsystems == {"AEAN", "EOS", "EIOS", "ResearchOS"}


def test_research_os_literature_review_integration():
    """Verify that ResearchOS.conduct_literature_review queries registered corpus principles accurately."""
    ros = ResearchOS()
    res_aean = ros.conduct_literature_review("AEAN")
    assert res_aean["reviewed_citations_count"] >= 18
    assert len(res_aean["matched_principles"]) == 1
    assert res_aean["matched_principles"][0]["target_subsystem"] == "AEAN"

    res_eos = ros.conduct_literature_review("EOS")
    assert len(res_eos["matched_principles"]) == 1
    assert res_eos["matched_principles"][0]["target_subsystem"] == "EOS"


def test_code_rewrite_engine_hawkes_recursion_bound():
    """Verify CodeRewriteEngine Hawkes non-Gaussian recursive AST call depth limit."""
    engine = CodeRewriteEngine(allowed_paths=["."])

    # Valid rewrite
    valid_code = "def add(a, b):\n    return a + b\n"
    prop_valid = engine.propose_rewrite("test.py", "a", "b", "testing valid AST")
    prop_valid.proposed_snippet = valid_code
    assert engine.verify_proposal_ast(prop_valid) is True

    # Deeply recursive function exceeding max_recursion_depth (default 10)
    recursive_code = "def rec_fn(n):\n" + "\n".join([f"    rec_fn({i})" for i in range(15)])
    prop_invalid = engine.propose_rewrite("test.py", "a", "b", "testing recursive AST")
    prop_invalid.proposed_snippet = recursive_code
    assert engine.verify_proposal_ast(prop_invalid) is False


def test_genetic_workflow_optimizer_map_elites():
    """Verify GeneticWorkflowOptimizer island population initialization and crossover."""
    optimizer = GeneticWorkflowOptimizer(population_size=12, mutation_rate=0.3, island_count=3)
    optimizer.initialize_population(
        base_template="Analyze task.",
        base_params={"lr": 0.01, "max_tokens": 100}
    )
    assert len(optimizer.population) == 12

    # Verify score evaluation and generation crossover
    optimizer.evaluate_generation(lambda g: len(g.prompt_template) + g.parameters.get("max_tokens", 0))
    optimizer.perform_crossover_and_mutation()
    assert len(optimizer.population) == 12


def test_sft_preference_collector_margin_clipping():
    """Verify SFTPreferenceCollector clips trajectory advantage margins."""
    collector = SFTPreferenceCollector(discount_factor=0.95, max_advantage_margin=3.0)

    steps_a = [TrajectoryStep(action="a1", predicted_expectation=1.0, actual_outcome=10.0, reward=10.0)]
    steps_b = [TrajectoryStep(action="b1", predicted_expectation=1.0, actual_outcome=0.0, reward=0.0)]

    pref = collector.compile_dpo_preference_pair("Prompt test", steps_a, steps_b)
    assert pref["margin"] <= 3.0
    assert pref["raw_margin"] > 3.0


def test_learnable_routing_gate_efe():
    """Verify LearnableRoutingGateDispatcher Expected Free Energy routing and parameter updating."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    dispatcher.register_subagent(SpecializedAgentProfile(
        agent_id="agent_fast",
        domain_specialty="EIOS",
        cost_per_token=0.001,
        historical_success_rate=0.9,
        epistemic_curiosity=0.8
    ))

    selected = dispatcher.route_task(task_complexity=100.0, domain="EIOS")
    assert selected == "agent_fast"

    dispatcher.update_routing_parameters("agent_fast", success=True, cost_incurred=0.10)
    agent = dispatcher.agents["agent_fast"]
    assert agent.epistemic_curiosity < 0.8
