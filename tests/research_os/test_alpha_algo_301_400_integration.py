# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Verification test suite for Papers 301-400 corpus,
extracted transferable principles registration, literature review querying, enhanced runtime
components, and remediation of architectural/runtime flaws in AlphaAlgo.
"""

import os
import yaml
import pytest
import tempfile
from apodex.ai_eos.research.integration import (
    ALPHAALGO_301_400_PRINCIPLES,
    register_301_400_paper_corpus_principles,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_papers_301_400_corpus_integrity_and_zero_overlap():
    """Verify that Papers 301-400 dataset exists, contains 100 papers, and has zero title/DOI overlap."""
    yaml_path = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    bib_path = "docs/research/papers/ALPHA_ALGO_301_400_BIBLIOGRAPHY.md"

    assert os.path.exists(yaml_path), f"YAML file missing: {yaml_path}"
    assert os.path.exists(bib_path), f"Bibliography markdown missing: {bib_path}"

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    papers = data.get("papers", [])
    assert len(papers) == 100, f"Expected 100 papers, found {len(papers)}"

    # Load papers 1-300
    existing_titles = []
    existing_dois = set()
    for ep in ["docs/research/papers/AI_EOS_RESEARCH_DB.yaml", "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"]:
        if os.path.exists(ep):
            with open(ep, "r", encoding="utf-8") as f:
                db = yaml.safe_load(f)
            for p in db.get("papers", []):
                meta = p.get("metadata", {})
                existing_titles.append(meta.get("title", "").lower())
                if "doi" in meta:
                    existing_dois.add(meta["doi"].lower())

    # Check zero overlap for 301-400
    for p in papers:
        meta = p.get("metadata", {})
        title = meta.get("title", "").lower()
        doi = meta.get("doi", "").lower()

        assert doi not in existing_dois, f"DOI collision detected: {doi}"

        p_tokens = set(title.split())
        for ext in existing_titles:
            ext_tokens = set(ext.split())
            if not p_tokens or not ext_tokens:
                continue
            intersection = p_tokens.intersection(ext_tokens)
            union = p_tokens.union(ext_tokens)
            score = len(intersection) / len(union)
            assert score <= 0.35, f"High title similarity ({score:.2f}) between '{title}' and '{ext}'"


def test_principles_registration_and_literature_review():
    """Verify principles extraction registration and Research OS literature review integration."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 4
    assert len(ALPHAALGO_301_400_PRINCIPLES) == 4

    ros = ResearchOS()
    # Review domain matching 'Market Microstructure'
    res_micro = ros.conduct_literature_review("Market Microstructure")
    assert res_micro["matched_principles_count"] >= 1
    assert "Hawkes" in res_micro["synthesized_trends"][0] or "Point" in res_micro["synthesized_trends"][0]

    # Review domain matching 'Active Inference'
    res_active = ros.conduct_literature_review("Active Inference")
    assert res_active["matched_principles_count"] >= 1


def test_code_rewrite_engine_hawkes_depth_check():
    """Verify CodeRewriteEngine AST validation with Hawkes recursive call depth checking."""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = CodeRewriteEngine(allowed_paths=[tmpdir], max_ast_call_depth=3)
        target_file = os.path.join(tmpdir, "strategy.py")

        with open(target_file, "w") as f:
            f.write("# Strategy file\ndef process(): return 1\n")

        # Non-recursive normal code should pass
        valid_code = "def compute(x):\n    a = x + 1\n    b = x * 2\n    return a + b\n"
        prop_valid = engine.propose_rewrite(target_file, "def process(): return 1\n", valid_code, "Add compute")
        assert engine.verify_proposal_ast(prop_valid) is True

        # Deeply recursive function exceeding max_ast_call_depth=3 should be vetoed
        recursive_code = (
            "def hawkes_recursion(n):\n"
            "    if n <= 0: return 0\n"
            "    return hawkes_recursion(n-1) + hawkes_recursion(n-2) + hawkes_recursion(n-3) + hawkes_recursion(n-4)\n"
        )
        prop_rec = engine.propose_rewrite(target_file, "def process(): return 1\n", recursive_code, "Deep recursion")
        assert engine.verify_proposal_ast(prop_rec) is False


def test_genetic_workflow_optimizer_boolean_handling_and_map_elites():
    """Verify GeneticWorkflowOptimizer boolean parameter mutation and MAP-Elites sorting."""
    base_params = {"learning_rate": 0.01, "enable_hedging": True, "max_depth": 5}
    optimizer = GeneticWorkflowOptimizer(population_size=5, mutation_rate=1.0)
    optimizer.initialize_population(base_template="Base prompt", base_params=base_params)

    # Confirm boolean param remains boolean or is flipped correctly
    for genome in optimizer.population:
        assert isinstance(genome.parameters["enable_hedging"], bool)

    # Evaluate generation and test population sorting
    def score_fn(g):
        return g.parameters.get("learning_rate", 0.0) * 10.0

    optimizer.evaluate_generation(score_fn)
    for i in range(len(optimizer.population) - 1):
        assert optimizer.population[i].fitness_score >= optimizer.population[i+1].fitness_score

    # Perform crossover and verify next gen population is sorted
    optimizer.perform_crossover_and_mutation()

    optimizer.evaluate_generation(score_fn)
    for i in range(len(optimizer.population) - 1):
        assert optimizer.population[i].fitness_score >= optimizer.population[i+1].fitness_score


def test_sft_preference_collector_clipped_margins_and_tie_breaking():
    """Verify SFTPreferenceCollector margin clipping and deterministic tie handling."""
    collector = SFTPreferenceCollector(discount_factor=0.9, max_margin_clip=5.0)

    step1 = TrajectoryStep(action="buy", predicted_expectation=1.0, actual_outcome=10.0, reward=10.0)
    step2 = TrajectoryStep(action="sell", predicted_expectation=1.0, actual_outcome=2.0, reward=2.0)

    # High advantage run A vs low advantage run B
    res = collector.compile_dpo_preference_pair(
        prompt="Execute trade",
        steps_run_a=[step1],
        steps_run_b=[step2]
    )

    assert "buy" in res["chosen"]
    assert "sell" in res["rejected"]
    assert res["margin"] <= 5.0  # Clipped from raw 9.0 to max_margin_clip 5.0
    assert res["raw_margin"] == 8.0

    # Equal advantage tie breaking
    res_tie = collector.compile_dpo_preference_pair(
        prompt="Execute trade",
        steps_run_a=[step1],
        steps_run_b=[step1]
    )
    assert res_tie["margin"] == 0.0
    assert res_tie["raw_margin"] == 0.0


def test_learnable_routing_gate_dispatcher():
    """Verify LearnableRoutingGateDispatcher EFE task routing and curiosity decay."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(
        agent_id="hft_agent",
        domain_specialty="Market Microstructure",
        cost_per_token=0.001,
        historical_success_rate=0.8,
        epistemic_curiosity=0.5
    )
    agent_b = SpecializedAgentProfile(
        agent_id="macro_agent",
        domain_specialty="Macro Economics",
        cost_per_token=0.005,
        historical_success_rate=0.4,
        epistemic_curiosity=0.2
    )

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    selected = dispatcher.route_task(task_complexity=100, domain="Market Microstructure")
    assert selected == "hft_agent"

    # Update routing metrics and verify epistemic curiosity decay
    initial_curiosity = agent_a.epistemic_curiosity
    dispatcher.update_routing_parameters(agent_id="hft_agent", success=True, cost_incurred=0.1)
    assert agent_a.epistemic_curiosity < initial_curiosity
    assert dispatcher.budget_spent == 0.1
