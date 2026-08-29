# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Unit and integration test suite validating
the 100 new research papers (IDs 301-400), extracted principles registration,
AlphaAlgo component enhancements, and flaw fixes.
"""

import os
import yaml
import pytest
from pydantic import BaseModel

from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    ProgramGenome,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.research_os.statistical_validation import standard_normal_ppf, calculate_dsr
from apodex.cognition.brain import CognitiveBrain


def test_301_400_corpus_zero_overlap():
    """Verify that all 100 new papers (IDs 301-400) have zero title overlap with existing papers 1-300."""
    yaml_path = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    assert os.path.exists(yaml_path), f"Corpus YAML file {yaml_path} does not exist!"

    with open(yaml_path, "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    papers = db.get("papers", [])
    assert len(papers) == 100, f"Expected 100 papers, got {len(papers)}"

    # Verify ID range 301-400
    p_ids = [p["id"] for p in papers]
    assert min(p_ids) == 301
    assert max(p_ids) == 400

    # Verify audit matrix zero duplicates
    audit_matrix = db.get("duplicate_detection_matrix", [])
    flagged = [row for row in audit_matrix if row.get("status") != "Approved"]
    assert len(flagged) == 0, f"Found {len(flagged)} flagged duplicate paper(s) in audit matrix!"


def test_principle_registration_and_research_os():
    """Verify registration and literature review querying of 301-400 principles."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) >= 4
    assert "non_gaussian_hawkes_volatility" in principles
    assert "variational_free_energy_causal_do_calculus" in principles

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")
    assert review["domain"] == "Active Inference"
    assert len(review["extracted_principles"]) >= 1
    assert "Causal Do-Calculus Interventions under Expected Free Energy" in review["extracted_principles"][0]["principle"]


def test_code_rewrite_engine_hawkes_check():
    """Verify CodeRewriteEngine non-Gaussian Hawkes stability check."""
    engine = CodeRewriteEngine(allowed_paths=["/tmp"])
    stable = engine.check_non_gaussian_hawkes_stability([0.1, 0.2, -0.1, 0.05])
    assert stable is True

    unstable = engine.check_non_gaussian_hawkes_stability([5.0, 10.0, 15.0, 20.0], alpha=2.0)
    assert unstable is False


def test_genetic_optimizer_island_migration():
    """Verify GeneticWorkflowOptimizer epistemic curiosity island migration gate."""
    optimizer = GeneticWorkflowOptimizer(population_size=5)
    optimizer.initialize_population(base_template="Analyze market data", base_params={"lr": 0.01})

    other_island = [
        ProgramGenome(prompt_template="Elite prompt", fitness_score=0.85),
        ProgramGenome(prompt_template="Low prompt", fitness_score=0.1)
    ]

    optimizer.execute_island_migration_gate(other_island, curiosity_threshold=0.3)
    # Confirm migrant was integrated
    templates = [g.prompt_template for g in optimizer.population]
    assert "Elite prompt" in templates


def test_sft_preference_collector_edit_path_distance():
    """Verify SFTPreferenceCollector DPO edit path trajectory penalties."""
    collector = SFTPreferenceCollector(discount_factor=0.95)

    steps_a = [
        TrajectoryStep(action="query_database", predicted_expectation=0.5, actual_outcome=0.8, reward=0.8),
        TrajectoryStep(action="execute_trade", predicted_expectation=0.8, actual_outcome=0.9, reward=0.9)
    ]
    steps_b = [
        TrajectoryStep(action="query_database", predicted_expectation=0.5, actual_outcome=0.4, reward=0.3),
        TrajectoryStep(action="cancel_order", predicted_expectation=0.4, actual_outcome=0.2, reward=0.1)
    ]

    pair = collector.compile_dpo_preference_pair("Optimize portfolio", steps_a, steps_b)
    assert pair["edit_path_distance"] == 1
    assert "margin" in pair
    assert pair["margin"] > 0.0


def test_learnable_routing_gate_causal_do():
    """Verify LearnableRoutingGateDispatcher causal do-calculus intervention routing."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(
        agent_id="agent_standard",
        domain_specialty="Market Microstructure",
        cost_per_token=0.01,
        historical_success_rate=0.8,
        epistemic_curiosity=0.2
    )
    agent_b = SpecializedAgentProfile(
        agent_id="agent_curious",
        domain_specialty="Active Inference",
        cost_per_token=0.01,
        historical_success_rate=0.4,
        epistemic_curiosity=0.9
    )

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    # Without do-intervention, agent_a dominates
    selected_standard = dispatcher.route_task(task_complexity=1.0, domain="Market Microstructure", do_intervention=False)
    assert selected_standard == "agent_standard"

    # With do-intervention on high curiosity domain, agent_b epistemic value is boosted
    selected_do = dispatcher.route_task(task_complexity=1.0, domain="Active Inference", do_intervention=True)
    assert selected_do == "agent_curious"


def test_standard_normal_ppf_boundary_clamping():
    """Verify safe probability boundary clamping in standard_normal_ppf."""
    # Should not raise ValueError on boundary probabilities
    val_zero = standard_normal_ppf(0.0)
    val_one = standard_normal_ppf(1.0)
    assert isinstance(val_zero, float)
    assert isinstance(val_one, float)
    assert val_zero < 0.0
    assert val_one > 0.0


def test_cognitive_brain_pydantic_v2():
    """Verify CognitiveBrain instantiation and cycle execution under Pydantic V2."""
    brain = CognitiveBrain()
    res = brain.run_strategic_cycle("Audit and optimize AlphaAlgo")
    assert res["goal"] == "Audit and optimize AlphaAlgo"
    assert res["plan_length"] == 4
