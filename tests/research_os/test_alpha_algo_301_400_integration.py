# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite for the 100 new research papers (301-400)
and the AlphaAlgo research improvements.
"""
import os
import time
import pytest
import yaml
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.research_os.models import Experiment
from apodex.research_os.reproducibility import verify_reproducibility


def test_corpus_301_400_zero_overlap():
    """Verify that papers 301-400 have 100% zero title and DOI overlap with papers 1-300."""
    yaml_301 = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    assert os.path.exists(yaml_301), "ALPHA_ALGO_301_400_RESEARCH.yaml must exist."

    with open(yaml_301, "r", encoding="utf-8") as f:
        data301 = yaml.safe_load(f)

    papers301 = data301.get("papers", [])
    assert len(papers301) == 100, "Should contain exactly 100 papers."

    ids301 = {p["id"] for p in papers301}
    assert min(ids301) == 301 and max(ids301) == 400

    titles301 = {p["metadata"]["title"].strip().lower() for p in papers301}
    dois301 = {p["metadata"]["doi"].strip().lower() for p in papers301}

    # Check against previous DBs
    for prev_path in ["docs/research/papers/AI_EOS_RESEARCH_DB.yaml", "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"]:
        if os.path.exists(prev_path):
            with open(prev_path, "r", encoding="utf-8") as f:
                prev_data = yaml.safe_load(f)
            prev_papers = prev_data if isinstance(prev_data, list) else prev_data.get("papers", [])
            for p in prev_papers:
                meta = p.get("metadata", {}) if isinstance(p, dict) and "metadata" in p else p
                t = (meta.get("title") or p.get("title") or "").strip().lower()
                d = (meta.get("doi") or p.get("doi") or meta.get("arxiv_id") or p.get("arxiv_id") or "").strip().lower()
                pid = p.get("id")

                assert pid not in ids301, f"Duplicate ID {pid} detected!"
                assert t not in titles301, f"Duplicate Title '{t}' detected!"
                if d:
                    assert d not in dois301, f"Duplicate DOI '{d}' detected!"


def test_principles_registration_and_research_os():
    """Verify principles registration and ResearchOS literature review synthesis."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) >= 5

    ros = ResearchOS()
    review = ros.conduct_literature_review("Deep Active Inference")
    assert review["domain"] == "Deep Active Inference"
    assert "extracted_principles" in review
    assert len(review["extracted_principles"]) > 0


def test_code_rewrite_engine_hawkes_and_ast():
    """Verify CodeRewriteEngine AST security check and Hawkes self-exciting intensity rate limit."""
    engine = CodeRewriteEngine(allowed_paths=["."], hawkes_alpha=1.0, hawkes_beta=0.1)

    # Test AST security veto
    prop_bad = engine.propose_rewrite(
        filepath="apodex/test_tmp.py",
        original_snippet="a = 1",
        proposed_snippet="import os; os.system('rm -rf /')",
        rationale="dangerous"
    )
    assert engine.verify_proposal_ast(prop_bad) is False

    # Test Hawkes intensity surge
    engine.last_mutation_time = time.time()
    engine.current_intensity = 3.5  # simulate spike above threshold
    with pytest.raises(RuntimeError, match="Hawkes Instability Veto"):
        engine.propose_rewrite(
            filepath="apodex/test_tmp.py",
            original_snippet="a = 1",
            proposed_snippet="a = 2",
            rationale="valid"
        )


def test_genetic_workflow_optimizer_map_elites():
    """Verify GeneticWorkflowOptimizer island demes and MAP-Elites migration."""
    optimizer = GeneticWorkflowOptimizer(population_size=10, mutation_rate=0.2, num_islands=2)
    optimizer.initialize_population(
        base_template="Analyze query: {query}",
        base_params={"temperature": 0.7, "max_tokens": 100}
    )

    assert len(optimizer.islands) == 2
    assert len(optimizer.population) == 10

    # Evaluate fitness
    optimizer.evaluate_generation(lambda g: len(g.prompt_template) * 0.1)

    # Perform crossover & migration
    optimizer.perform_crossover_and_mutation()
    assert len(optimizer.population) == 10


def test_sft_preference_collector_edit_distance():
    """Verify SFTPreferenceCollector edit-distance calculation and DPO compiler."""
    collector = SFTPreferenceCollector(discount_factor=0.9, edit_distance_penalty=0.1)

    steps_a = [
        TrajectoryStep(action="SEARCH_KNOWLEDGE", predicted_expectation=0.5, actual_outcome=0.8, reward=1.0),
        TrajectoryStep(action="RUN_SIMULATION", predicted_expectation=0.6, actual_outcome=0.9, reward=1.2)
    ]

    steps_b = [
        TrajectoryStep(action="SEARCH_KNOWLEDGE", predicted_expectation=0.5, actual_outcome=0.3, reward=0.2),
        TrajectoryStep(action="FAIL_TASK", predicted_expectation=0.4, actual_outcome=0.1, reward=-0.5)
    ]

    dpo_pair = collector.compile_dpo_preference_pair(
        prompt="Execute hypothesis validation",
        steps_run_a=steps_a,
        steps_run_b=steps_b
    )

    assert "chosen" in dpo_pair
    assert "rejected" in dpo_pair
    assert dpo_pair["margin"] > 0
    assert dpo_pair["edit_distance"] == 1.0


def test_learnable_routing_gate_causal_intervention():
    """Verify LearnableRoutingGateDispatcher causal do-calculus intervention task routing."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=100.0)

    p1 = SpecializedAgentProfile(agent_id="curious_bot", domain_specialty="Research", cost_per_token=0.01, historical_success_rate=0.4, epistemic_curiosity=0.9)
    p2 = SpecializedAgentProfile(agent_id="pragmatic_bot", domain_specialty="Research", cost_per_token=0.01, historical_success_rate=0.9, epistemic_curiosity=0.2)

    dispatcher.register_subagent(p1)
    dispatcher.register_subagent(p2)

    # Standard routing favors pragmatic_bot
    route_std = dispatcher.route_task(task_complexity=1.0, domain="Research")
    assert route_std == "pragmatic_bot"

    # Causal do-calculus intervention forcing exploration favors curious_bot
    route_causal = dispatcher.route_task(task_complexity=1.0, domain="Research", do_intervention={"force_exploration": True})
    assert route_causal == "curious_bot"


def test_verify_reproducibility_type_safety():
    """Verify verify_reproducibility type safety on string metric inputs."""
    exp = Experiment(
        experiment_id=str(uuid4()),
        hypothesis_id="hyp1",
        dataset_id="ds1",
        returns_time_series=[0.01, 0.02, -0.01],
        metrics={"sharpe": "1.5"},
        status="COMPLETED"
    )

    replayed_returns = [0.01, 0.02, -0.01]
    replayed_metrics = {"sharpe": 1.5}

    assert verify_reproducibility(exp, replayed_returns, replayed_metrics) is True
