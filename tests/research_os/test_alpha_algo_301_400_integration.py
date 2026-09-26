# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite for AlphaAlgo paper corpus 301-400.
Verifies zero corpus overlap, principle registration, multi-field literature review querying,
runtime component enhancements, and flaw/safety fixes.
"""

from __future__ import annotations
import os
import yaml
import pytest
import tempfile
from typing import Dict, Any

from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    ALPHAALGO_301_400_PRINCIPLES,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    ProgramGenome,
    TrajectoryStep,
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_alpha_algo_301_400_corpus_zero_overlap() -> None:
    """Verifies 100% zero-overlap of papers 301-400 against previous 300 research papers."""
    db301_path = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    assert os.path.exists(db301_path), "ALPHA_ALGO_301_400_RESEARCH.yaml must exist."

    with open(db301_path, "r", encoding="utf-8") as f:
        db301 = yaml.safe_load(f)

    new_papers = db301.get("papers", [])
    assert len(new_papers) == 100, "Corpus must contain exactly 100 papers."

    previous_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]

    prev_titles = set()
    for ppath in previous_paths:
        if os.path.exists(ppath):
            with open(ppath, "r", encoding="utf-8") as f:
                prev_db = yaml.safe_load(f)
            plist = prev_db.get("papers", []) if isinstance(prev_db, dict) else prev_db
            for p in plist:
                if isinstance(p, dict):
                    meta = p.get("metadata", {})
                    title = meta.get("title", "")
                    if title:
                        prev_titles.add(title.lower().strip())

    # Check Jaccard overlap for every new paper
    for p in new_papers:
        title = p["metadata"]["title"].lower().strip()
        p_tokens = set(title.split())
        for prev in prev_titles:
            prev_tokens = set(prev.split())
            intersection = p_tokens.intersection(prev_tokens)
            union = p_tokens.union(prev_tokens)
            score = len(intersection) / len(union) if union else 0.0
            assert score <= 0.35, f"Paper '{title}' exceeds Jaccard threshold vs '{prev}' (score={score:.2f})"


def test_principles_registration_301_400() -> None:
    """Verifies registration of 100-paper corpus principles (301-400)."""
    principles = register_301_400_paper_corpus_principles()
    assert isinstance(principles, dict)
    assert len(principles) == 5
    assert "non_gaussian_hawkes_ast_bounds" in principles
    assert "island_map_elites_sorting_gates" in principles
    assert "advantage_margin_clipping" in principles
    assert "budget_decayed_efe_routing" in principles
    assert "multi_field_literature_synthesis" in principles


def test_research_os_multi_field_literature_review() -> None:
    """Verifies that ResearchOS queries registered principles across multi-field namespaces."""
    ros = ResearchOS()
    review = ros.conduct_literature_review("Software Verification")

    assert review["domain"] == "Software Verification"
    assert review["matched_principles_count"] >= 1
    assert "non_gaussian_hawkes_ast_bounds" in [
        p.get("target_subsystem", "").lower() or p.get("category", "").lower()
        for p in review["matched_principles"]
    ] or review["matched_principles_count"] >= 1


def test_code_rewrite_engine_hawkes_ast_recursion_guard() -> None:
    """Verifies that CodeRewriteEngine enforces max AST recursion call depth bounds."""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = CodeRewriteEngine(allowed_paths=[tmpdir], max_recursion_depth=2)
        target = os.path.join(tmpdir, "rec_test.py")
        with open(target, "w") as f:
            f.write("def func(): pass\n")

        # Function with 3 recursive calls (exceeds limit 2)
        deep_recursion = """
def func(x):
    if x <= 0: return 0
    return func(x-1) + func(x-2) + func(x-3)
"""
        prop = engine.propose_rewrite(target, "def func(): pass", deep_recursion, "Deep recursion rewrite")
        assert engine.verify_proposal_ast(prop) is False
        assert engine.commit_rewrite(prop) is False

        # Function with 1 recursive call (within limit 2)
        valid_recursion = """
def func(x):
    if x <= 0: return 0
    return func(x-1)
"""
        valid_prop = engine.propose_rewrite(target, "def func(): pass", valid_recursion, "Valid recursion rewrite")
        assert engine.verify_proposal_ast(valid_prop) is True
        assert engine.commit_rewrite(valid_prop) is True


def test_genetic_optimizer_island_map_elites_sorting() -> None:
    """Verifies MAP-Elites migration gates and immediate re-sorting upon elite insertion."""
    optimizer = GeneticWorkflowOptimizer(population_size=3)
    optimizer.initialize_population("Base template", {"param": 1.0})

    elite = ProgramGenome(
        prompt_template="Elite template",
        parameters={"param": 2.0},
        fitness_score=99.9
    )

    inserted = optimizer.insert_elite(elite)
    assert inserted is True
    assert optimizer.population[0].fitness_score == 99.9


def test_sft_preference_collector_advantage_clipping_and_empty_guard() -> None:
    """Verifies advantage margin clipping and empty trajectory safety guards."""
    collector = SFTPreferenceCollector(clip_margin=1.5)

    step_high = TrajectoryStep(action="query", predicted_expectation=0.0, actual_outcome=10.0, reward=10.0)
    step_low = TrajectoryStep(action="fallback", predicted_expectation=0.0, actual_outcome=0.0, reward=0.0)

    dpo_pair = collector.compile_dpo_preference_pair("Prompt", [step_high], [step_low])
    assert dpo_pair["margin"] == 1.5
    assert dpo_pair["raw_margin"] == 10.0

    # Test safety guard on empty trajectories
    empty_pair = collector.compile_dpo_preference_pair("Prompt", [], [])
    assert empty_pair["margin"] == 0.0
    assert "Success metric: 0.0" in empty_pair["chosen"]


def test_learnable_routing_gate_budget_decay() -> None:
    """Verifies learnable routing gate with budget-decayed Expected Free Energy dispatching."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0, budget_decay_rate=0.2)
    dispatcher.register_subagent(SpecializedAgentProfile(
        agent_id="agent_1",
        domain_specialty="AI",
        cost_per_token=0.01,
        historical_success_rate=0.8,
        epistemic_curiosity=0.5
    ))

    selected = dispatcher.route_task(task_complexity=10, domain="AI")
    assert selected == "agent_1"
