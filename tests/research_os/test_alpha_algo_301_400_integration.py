# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py:
Comprehensive integration test suite verifying the 100 new research papers (IDs 301-400),
zero-overlap corpus integrity, principle registration, literature review querying,
and runtime enhancements in CodeRewriteEngine, GeneticWorkflowOptimizer, SFTPreferenceCollector,
and LearnableRoutingGateDispatcher.
"""

import pytest
import os
import yaml
import ast
from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    ALPHAALGO_301_400_PRINCIPLES,
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    ProgramGenome,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.cognition.brain import CognitiveBrain


def test_301_400_paper_corpus_zero_overlap():
    """Verifies that all 100 papers (IDs 301-400) have zero title and DOI overlap against papers 1-300."""
    corpus_file = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    assert os.path.exists(corpus_file), f"Corpus file {corpus_file} missing!"

    with open(corpus_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    papers = data.get("papers", [])
    assert len(papers) == 100, f"Expected 100 papers, found {len(papers)}"

    # Load existing titles and DOIs from papers 1-300
    existing_titles = set()
    existing_dois = set()
    for prev_file in [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]:
        if os.path.exists(prev_file):
            with open(prev_file, "r", encoding="utf-8") as pf:
                prev_data = yaml.safe_load(pf)
            prev_papers = prev_data.get("papers", []) if isinstance(prev_data, dict) else prev_data
            for p in prev_papers:
                meta = p.get("metadata", {})
                if meta.get("title"):
                    existing_titles.add(meta["title"].strip().lower())
                if meta.get("doi"):
                    existing_dois.add(meta["doi"].strip().lower())

    for p in papers:
        meta = p.get("metadata", {})
        title = meta.get("title", "").strip().lower()
        doi = meta.get("doi", "").strip().lower()

        assert title not in existing_titles, f"Duplicate title detected: '{title}'"
        assert doi not in existing_dois, f"Duplicate DOI detected: '{doi}'"


def test_principle_registration():
    """Verifies registration and export of extracted principles from papers 301-400."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 5
    assert len(ALPHAALGO_301_400_PRINCIPLES) == 5

    categories = {p["category"] for p in principles}
    assert "Market Microstructure" in categories
    assert "Active Inference" in categories
    assert "RL & Alignment" in categories
    assert "Multi-Agent Systems" in categories
    assert "Evolutionary Search" in categories


def test_code_rewrite_engine_hawkes_ast_recursion_limit(tmp_path):
    """Verifies that CodeRewriteEngine enforces per-function nested AST recursion depth boundaries."""
    engine = CodeRewriteEngine(allowed_paths=[str(tmp_path)], max_ast_recursion_depth=2)

    target_file = tmp_path / "sample.py"
    target_file.write_text("def fn(): pass\n")

    # Safe snippet (1 nested recursive call)
    safe_code = """
def recursive_fn(n):
    if n <= 0:
        return 0
    return recursive_fn(n - 1)
"""
    proposal_safe = engine.propose_rewrite(
        filepath=str(target_file),
        original_snippet="def fn(): pass",
        proposed_snippet=safe_code,
        rationale="Safe single recursion"
    )
    assert engine.verify_proposal_ast(proposal_safe) is True

    # Code with 3 nested recursive calls recursive_fn(recursive_fn(recursive_fn(n))) > max 2
    excessive_recursion_code = """
def recursive_fn(n):
    if n <= 0:
        return 0
    return recursive_fn(recursive_fn(recursive_fn(n - 1)))
"""
    proposal_excessive = engine.propose_rewrite(
        filepath=str(target_file),
        original_snippet="def fn(): pass",
        proposed_snippet=excessive_recursion_code,
        rationale="Excessive nested recursive calls"
    )
    assert engine.verify_proposal_ast(proposal_excessive) is False


def test_genetic_workflow_optimizer_island_map_elites():
    """Verifies island MAP-Elites migration gate and immediate population re-sorting."""
    optimizer = GeneticWorkflowOptimizer(population_size=6, mutation_rate=0.2, num_islands=3)
    optimizer.initialize_population(
        base_template="Base execution prompt",
        base_params={"lr": 0.01, "depth": 5}
    )

    def scoring_fn(genome: ProgramGenome) -> float:
        return float(len(genome.prompt_template))

    optimizer.evaluate_generation(scoring_fn)

    migrated_count = optimizer.migrate_elites_between_islands(migration_threshold=10.0)
    assert migrated_count >= 1

    scores = [g.fitness_score for g in optimizer.population]
    assert scores == sorted(scores, reverse=True)


def test_sft_preference_collector_clipped_advantage_margin():
    """Verifies trajectory DPO advantage calculation and margin clipping bounds."""
    collector = SFTPreferenceCollector(discount_factor=0.9, advantage_clip_threshold=3.0)

    steps_a = [
        TrajectoryStep(action="a1", predicted_expectation=1.0, actual_outcome=10.0, reward=5.0),
        TrajectoryStep(action="a2", predicted_expectation=1.0, actual_outcome=10.0, reward=10.0)
    ]
    steps_b = [
        TrajectoryStep(action="b1", predicted_expectation=5.0, actual_outcome=1.0, reward=0.0),
        TrajectoryStep(action="b2", predicted_expectation=5.0, actual_outcome=1.0, reward=0.0)
    ]

    dpo_pair = collector.compile_dpo_preference_pair(
        prompt="Execute task",
        steps_run_a=steps_a,
        steps_run_b=steps_b
    )

    assert "prompt" in dpo_pair
    assert dpo_pair["raw_margin"] > 3.0
    assert dpo_pair["margin"] == 3.0


def test_learnable_routing_gate_budget_decayed_efe():
    """Verifies budget-decayed Expected Free Energy task routing and curiosity reduction."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(
        agent_id="curious_agent",
        domain_specialty="research",
        cost_per_token=0.01,
        historical_success_rate=0.6,
        epistemic_curiosity=0.9
    )
    agent_b = SpecializedAgentProfile(
        agent_id="pragmatic_agent",
        domain_specialty="research",
        cost_per_token=0.01,
        historical_success_rate=0.95,
        epistemic_curiosity=0.1
    )

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    selected_1 = dispatcher.route_task(task_complexity=100, domain="research")
    assert selected_1 in ["curious_agent", "pragmatic_agent"]

    dispatcher.update_routing_parameters(agent_id="curious_agent", success=True, cost_incurred=9.5)

    selected_2 = dispatcher.route_task(task_complexity=10, domain="research")
    assert selected_2 == "pragmatic_agent"


def test_research_os_literature_review_multi_field_query():
    """Verifies Research OS literature review querying across all corpus principle fields."""
    ros = ResearchOS()

    res_subsystem = ros.conduct_literature_review("ResearchOS")
    assert res_subsystem["matched_principles_count"] >= 1

    res_dpo = ros.conduct_literature_review("DPO")
    assert res_dpo["matched_principles_count"] >= 1

    res_hawkes = ros.conduct_literature_review("Hawkes")
    assert res_hawkes["matched_principles_count"] >= 1


def test_cognitive_brain_strategic_cycle():
    """Verifies end-to-end CognitiveBrain strategic cycle execution."""
    brain = CognitiveBrain()
    res = brain.run_strategic_cycle("Optimize algorithmic execution pipelines")

    assert res["goal"] == "Optimize algorithmic execution pipelines"
    assert res["plan_length"] == 4
    assert res["consensus_score"] > 0.0
    assert "sim_results" in res
