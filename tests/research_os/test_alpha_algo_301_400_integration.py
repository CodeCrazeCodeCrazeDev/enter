# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite for papers 301-400,
verifying zero corpus overlap, principle registration, runtime component enhancements, and statistical flaw fixes.
"""

import pytest
import os
import glob
import yaml
import math
from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    ALPHAALGO_301_400_PRINCIPLES,
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.research_os.statistical_validation import standard_normal_ppf, calculate_dsr


def test_zero_corpus_overlap_across_all_400_papers():
    """Verifies 100% zero title and DOI overlap across papers 1-400."""
    all_titles = {}
    all_dois = {}

    db_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    ]

    total_papers = 0
    for p_path in db_paths:
        assert os.path.exists(p_path), f"Database file {p_path} missing!"
        with open(p_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        papers = data.get("papers", [])
        total_papers += len(papers)

        for p in papers:
            pid = p.get("id")
            meta = p.get("metadata", {})
            title = meta.get("title", "").strip().lower()
            doi = meta.get("doi", "").strip().lower()

            assert title not in all_titles, f"Duplicate title detected for Paper {pid}: '{title}'"
            all_titles[title] = pid

            if doi:
                assert doi not in all_dois, f"Duplicate DOI detected for Paper {pid}: '{doi}'"
                all_dois[doi] = pid

    assert total_papers == 400, f"Expected 400 total papers, got {total_papers}"


def test_principle_registration_301_400():
    """Verifies principles from papers 301-400 are registered correctly."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 5
    assert len(ALPHAALGO_301_400_PRINCIPLES) == 5
    p_ids = [p["id"] for p in principles]
    assert "P-301" in p_ids
    assert "P-321" in p_ids
    assert "P-341" in p_ids
    assert "P-361" in p_ids
    assert "P-381" in p_ids


def test_code_rewrite_hawkes_stability():
    """Verifies non-Gaussian Hawkes process intensity decay in CodeRewriteEngine (Paper 301)."""
    engine = CodeRewriteEngine(allowed_paths=["/tmp"])
    assert engine.hawkes_excitation_intensity == 0.0

    # Simulate rapid mutations to trigger Hawkes stability veto (6.0 * exp(-0.5) = 3.64 > 3.0)
    engine.hawkes_excitation_intensity = 6.0
    assert not engine.check_hawkes_stability()

    # Allow decay
    engine.hawkes_excitation_intensity = 1.0
    assert engine.check_hawkes_stability()


def test_genetic_workflow_island_migration():
    """Verifies island MAP-Elites migration gate control (Paper 381)."""
    optimizer = GeneticWorkflowOptimizer(population_size=5)
    optimizer.initialize_population("base template", {"param1": 1.0})

    # Add genomes to island_a
    from apodex.ai_eos.research.integration import ProgramGenome
    g_elite = ProgramGenome(prompt_template="elite prompt", parameters={"p": 1}, fitness_score=0.95)
    optimizer.islands["island_a"].append(g_elite)

    # Migrate to island_b
    optimizer.migrate_island_elites("island_a", "island_b")
    assert len(optimizer.islands["island_b"]) == 1
    assert optimizer.islands["island_b"][0].fitness_score == 0.95


def test_sft_preference_edit_distance_penalty():
    """Verifies trajectory edit path distance penalty in SFTPreferenceCollector (Paper 342)."""
    collector = SFTPreferenceCollector()
    steps_a = [
        TrajectoryStep(action="action_1", predicted_expectation=0.5, actual_outcome=0.8, reward=0.8),
        TrajectoryStep(action="action_2", predicted_expectation=0.5, actual_outcome=0.8, reward=0.8)
    ]
    steps_b = [
        TrajectoryStep(action="action_1", predicted_expectation=0.5, actual_outcome=0.8, reward=0.8),
        TrajectoryStep(action="action_3", predicted_expectation=0.5, actual_outcome=0.2, reward=0.2),
        TrajectoryStep(action="action_4", predicted_expectation=0.5, actual_outcome=0.2, reward=0.2)
    ]

    penalty = collector.compute_edit_distance_penalty(steps_a, steps_b)
    assert penalty > 0.0

    pair = collector.compile_dpo_preference_pair("test prompt", steps_a, steps_b)
    assert "chosen" in pair
    assert "rejected" in pair
    assert pair["margin"] > 0.0


def test_learnable_routing_causal_do_calculus():
    """Verifies causal do-calculus intervention EFE in LearnableRoutingGateDispatcher (Paper 321)."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    agent = SpecializedAgentProfile(agent_id="agent_1", domain_specialty="fintech", cost_per_token=0.001)

    score_do = dispatcher.compute_causal_do_calculus_efe(agent, task_complexity=100.0, domain="fintech", do_intervention=True)
    score_no_do = dispatcher.compute_causal_do_calculus_efe(agent, task_complexity=100.0, domain="fintech", do_intervention=False)

    # Pearl do(X) intervention adds bonus for domain match
    assert score_do > score_no_do


def test_statistical_validation_flaw_fixes():
    """Verifies probability clamping and zero-division protection in statistical_validation.py."""
    # Test boundary clamping at p=0 and p=1
    val_0 = standard_normal_ppf(0.0)
    val_1 = standard_normal_ppf(1.0)
    assert not math.isnan(val_0)
    assert not math.isnan(val_1)
    assert val_0 < 0
    assert val_1 > 0

    # Test DSR with 0 trial variance
    dsr_val = calculate_dsr(sharpe=1.5, trials=10, returns_length=252, trials_variance=0.0)
    assert not math.isnan(dsr_val)
    assert 0.0 <= dsr_val <= 1.0
