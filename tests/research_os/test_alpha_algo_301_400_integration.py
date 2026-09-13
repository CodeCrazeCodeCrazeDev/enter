# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite for 100-paper research corpus (IDs 301-400),
extracted transferable principles, literature review querying, Hawkes stability, MAP-Elites QD migration,
trajectory edit-distance DPO penalties, causal do-calculus routing, and statistical validation edge cases.
"""

from __future__ import annotations
import os
import yaml
import pytest
import time
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
from apodex.research_os.statistical_validation import (
    adjust_p_values,
    standard_normal_cdf,
    standard_normal_ppf,
    calculate_dsr
)


def test_paper_corpus_301_400_zero_overlap() -> None:
    """Verify papers 301-400 exist in YAML database and have zero title/DOI overlap against papers 1-300."""
    yaml_301_400 = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    assert os.path.exists(yaml_301_400), f"File {yaml_301_400} missing"

    with open(yaml_301_400, "r", encoding="utf-8") as f:
        db_301 = yaml.safe_load(f)

    papers_301 = db_301.get("papers", [])
    assert len(papers_301) == 100, f"Expected 100 papers, got {len(papers_301)}"

    # Check ID range
    ids_301 = [p["id"] for p in papers_301]
    assert min(ids_301) == 301
    assert max(ids_301) == 400

    # Load existing titles and DOIs from papers 1-300
    existing_titles = []
    existing_dois = set()
    for fpath in ["docs/research/papers/AI_EOS_RESEARCH_DB.yaml", "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"]:
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                db_prev = yaml.safe_load(f)
            for p in db_prev.get("papers", []):
                existing_titles.append(p["metadata"]["title"].lower())
                if "doi" in p["metadata"]:
                    existing_dois.add(p["metadata"]["doi"].lower())

    # Verify zero Jaccard overlap and zero DOI duplication
    for p in papers_301:
        title = p["metadata"]["title"].lower()
        doi = p["metadata"]["doi"].lower()

        assert doi not in existing_dois, f"Duplicate DOI found: {doi}"

        p_tokens = set(title.split())
        for prev in existing_titles:
            prev_tokens = set(prev.split())
            if not p_tokens or not prev_tokens:
                continue
            intersection = p_tokens.intersection(prev_tokens)
            union = p_tokens.union(prev_tokens)
            score = len(intersection) / len(union)
            assert score <= 0.35, f"High title similarity ({score:.2f}) between '{title}' and '{prev}'"


def test_principles_registration_and_literature_review() -> None:
    """Verify principles registration and dynamic literature review querying."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 5
    assert "P301_320_HAWKES_MUTATION_STABILITY" in principles
    assert "P321_340_CAUSAL_DO_CALCULUS_ROUTING" in principles
    assert "P341_360_TRAJECTORY_EDIT_DISTANCE_DPO" in principles
    assert "P361_380_ISLAND_MAP_ELITES_MIGRATION" in principles
    assert "P381_400_SELF_REFERENTIAL_AST_SANDBOXING" in principles

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")
    assert review["reviewed_citations_count"] == 400
    assert len(review["active_principles"]) > 0


def test_hawkes_code_rewrite_engine_stability() -> None:
    """Verify non-Gaussian Hawkes process intensity capping in CodeRewriteEngine."""
    engine = CodeRewriteEngine(
        allowed_paths=["/tmp"],
        hawkes_baseline=0.2,
        hawkes_alpha=0.5,
        hawkes_beta=1.0,
        max_intensity_threshold=0.8
    )

    # First rewrite proposal under low intensity passes
    assert engine.check_hawkes_stability() is True

    # Simulate burst of mutation timestamps
    t_now = time.time()
    for _ in range(5):
        engine.mutation_timestamps.append(t_now - 0.1)

    # Verify Hawkes intensity calculation (exercising math.exp)
    calculated_intensity = engine.calculate_hawkes_intensity(current_time=t_now)
    assert calculated_intensity > 0.2

    # High intensity triggers Hawkes stability veto
    assert engine.check_hawkes_stability() is False
    with pytest.raises(RuntimeError, match="Hawkes Self-Excitation Veto"):
        engine.propose_rewrite(
            filepath="/tmp/test_file.py",
            original_snippet="x = 1",
            proposed_snippet="x = 2",
            rationale="Hawkes burst test"
        )


def test_island_map_elites_genetic_optimizer() -> None:
    """Verify island MAP-Elites Quality-Diversity grid archive and migration in GeneticWorkflowOptimizer."""
    optimizer = GeneticWorkflowOptimizer(population_size=9, num_islands=3)
    optimizer.initialize_population(
        base_template="Analyze market data and evaluate trade signals.",
        base_params={"learning_rate": 0.01, "temperature": 0.5}
    )

    # Evaluate generation and check QD archive population
    optimizer.evaluate_generation(lambda genome: len(genome.prompt_template) * 0.05)
    assert len(optimizer.qd_archive) > 0

    # Perform crossover, mutation, and inter-island migration
    optimizer.perform_crossover_and_mutation()
    assert len(optimizer.population) == 9


def test_sft_preference_collector_edit_distance() -> None:
    """Verify trajectory edit-distance penalties in SFTPreferenceCollector DPO pair generation."""
    collector = SFTPreferenceCollector(discount_factor=0.95, edit_distance_weight=0.2)

    steps_a = [
        TrajectoryStep(action="query_market", predicted_expectation=0.8, actual_outcome=1.0, reward=1.0),
        TrajectoryStep(action="execute_order", predicted_expectation=0.9, actual_outcome=1.2, reward=1.0)
    ]
    steps_b = [
        TrajectoryStep(action="query_market", predicted_expectation=0.8, actual_outcome=0.5, reward=0.3),
        TrajectoryStep(action="wait", predicted_expectation=0.5, actual_outcome=0.2, reward=0.0)
    ]

    edit_dist = collector.calculate_trajectory_edit_distance(steps_a, steps_b)
    assert 0.0 <= edit_dist <= 1.0

    # Exercising compile_dpo_preference_pair which uses time_now()
    pair = collector.compile_dpo_preference_pair("Execute trade task", steps_a, steps_b)
    assert "trajectory_edit_distance" in pair
    assert pair["trajectory_edit_distance"] == edit_dist
    assert isinstance(pair["margin"], float)
    assert "timestamp_created" in pair
    assert len(pair["timestamp_created"]) > 0


def test_causal_do_calculus_routing_dispatcher() -> None:
    """Verify causal do-calculus Expected Free Energy routing in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=5.0)

    p1 = SpecializedAgentProfile(agent_id="fin_agent", domain_specialty="finance", cost_per_token=0.002, historical_success_rate=0.85)
    p2 = SpecializedAgentProfile(agent_id="code_agent", domain_specialty="coding", cost_per_token=0.001, historical_success_rate=0.70)

    dispatcher.register_subagent(p1)
    dispatcher.register_subagent(p2)

    selected = dispatcher.route_task(task_complexity=100.0, domain="finance")
    assert selected == "fin_agent"

    dispatcher.update_routing_parameters(selected, success=True, cost_incurred=0.20)
    assert dispatcher.budget_spent == pytest.approx(0.20)


def test_statistical_validation_edge_cases() -> None:
    """Verify edge case stability in p-value adjustments and Deflated Sharpe Ratio."""
    p_vals = [0.001, 0.05, 0.1, 0.5]

    bonf = adjust_p_values(p_vals, "BONFERRONI")
    assert bonf[0] == pytest.approx(0.004)
    assert bonf[3] == 1.0

    holm = adjust_p_values(p_vals, "HOLM")
    assert holm[0] == pytest.approx(0.004)

    bh = adjust_p_values(p_vals, "BH")
    assert bh[0] <= bh[1] <= bh[2] <= bh[3]

    dsr = calculate_dsr(sharpe=2.0, trials=100, returns_length=252)
    assert 0.0 <= dsr <= 1.0
