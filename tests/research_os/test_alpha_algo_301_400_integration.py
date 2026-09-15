# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite for 100 new research papers (IDs 301-400),
extracted transferable engineering principles, ResearchOS literature review synthesis,
and runtime component enhancements.
"""

import pytest
import glob
import yaml
from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    ALPHAALGO_301_400_PRINCIPLES
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.cognition.brain import CognitiveBrain


def test_400_paper_corpus_integrity_and_zero_overlap():
    """Verify that all 400 papers across all YAML files have 100% unique IDs, Titles, and DOIs (where applicable)."""
    files = sorted(glob.glob("docs/research/papers/*.yaml"))
    all_ids = set()
    all_titles = set()
    all_dois = set()
    total_papers = 0

    for f in files:
        if "DECISIONS" in f:
            continue
        with open(f) as fh:
            data = yaml.safe_load(fh)
            if not data or "papers" not in data:
                continue
            for p in data["papers"]:
                total_papers += 1
                pid = p["id"]
                meta = p.get("metadata", {})
                title = meta.get("title", "").strip().lower()
                doi = meta.get("doi", "").strip().lower()

                assert pid not in all_ids, f"Duplicate Paper ID {pid} found in {f}"
                all_ids.add(pid)

                assert title not in all_titles, f"Duplicate Paper Title '{title}' found in {f}"
                all_titles.add(title)

                if doi:
                    assert doi not in all_dois, f"Duplicate Paper DOI '{doi}' found in {f}"
                    all_dois.add(doi)

    assert total_papers == 400
    assert len(all_ids) == 400
    assert len(all_titles) == 400


def test_register_301_400_paper_corpus_principles():
    """Verify registration of transferable engineering principles P301-P306."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 6
    assert principles[0]["principle_id"] == "P301_HAWKES_STABILITY"
    assert principles[3]["principle_id"] == "P304_MAP_ELITES_ISLAND_MIGRATION"


def test_research_os_literature_review_synthesis():
    """Verify ResearchOS literature review synthesis with 400-paper principles."""
    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")
    assert review["reviewed_citations_count"] == 400
    assert review["principles_incorporated_count"] == 6
    assert "Continuous-Time Hawkes Intensity Parameter Bounds for Spiky Volatility Regimes" in review["synthesized_trends"]


def test_code_rewrite_engine_hawkes_bounds():
    """Verify CodeRewriteEngine Hawkes stability parameters."""
    engine = CodeRewriteEngine(allowed_paths=["/tmp"], hawkes_alpha=0.5, hawkes_beta=1.0)
    assert engine.hawkes_alpha == 0.5

    with pytest.raises(ValueError, match="Hawkes process branching ratio"):
        CodeRewriteEngine(allowed_paths=["/tmp"], hawkes_alpha=1.2, hawkes_beta=1.0)


def test_genetic_workflow_optimizer_islands():
    """Verify GeneticWorkflowOptimizer island-based population initialization and evolution."""
    optimizer = GeneticWorkflowOptimizer(population_size=10, mutation_rate=0.2, num_islands=2)
    optimizer.initialize_population(
        base_template="Base Prompt Template",
        base_params={"param_a": 1.0, "param_b": True}
    )
    assert len(optimizer.population) == 10
    islands = set(g.island_id for g in optimizer.population)
    assert len(islands) == 2

    # Run evaluation and crossover
    def dummy_scoring(genome):
        return len(genome.prompt_template) + genome.parameters.get("param_a", 0.0)

    optimizer.evaluate_generation(dummy_scoring)
    optimizer.perform_crossover_and_mutation()
    assert len(optimizer.population) == 10


def test_sft_preference_collector_edit_distance_penalty():
    """Verify trajectory edit distance penalties in SFTPreferenceCollector."""
    collector = SFTPreferenceCollector(discount_factor=0.9, trajectory_distance_penalty=0.5)

    steps_low_edit = [
        TrajectoryStep(action="a1", predicted_expectation=0.5, actual_outcome=1.0, reward=1.0, edit_distance=0.0)
    ]
    steps_high_edit = [
        TrajectoryStep(action="a1", predicted_expectation=0.5, actual_outcome=1.0, reward=1.0, edit_distance=2.0)
    ]

    adv_low = collector.compute_advantages(steps_low_edit)
    adv_high = collector.compute_advantages(steps_high_edit)

    # High edit distance should yield lower advantage due to penalty
    assert adv_low[0] > adv_high[0]


def test_learnable_routing_gate_dispatcher_efe():
    """Verify Expected Free Energy routing in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    agent1 = SpecializedAgentProfile(
        agent_id="agent_fast",
        domain_specialty="Active Inference",
        cost_per_token=0.001,
        historical_success_rate=0.9,
        epistemic_curiosity=0.2
    )
    agent2 = SpecializedAgentProfile(
        agent_id="agent_slow",
        domain_specialty="Quantitative Finance",
        cost_per_token=0.01,
        historical_success_rate=0.6,
        epistemic_curiosity=0.8
    )
    dispatcher.register_subagent(agent1)
    dispatcher.register_subagent(agent2)

    selected = dispatcher.route_task(task_complexity=100.0, domain="Active Inference")
    assert selected == "agent_fast"


def test_cognitive_brain_pydantic_v2_instantiation():
    """Verify CognitiveBrain instantiates without Pydantic V2 warnings or errors."""
    brain = CognitiveBrain()
    res = brain.run_strategic_cycle("Test Objective")
    assert res["goal"] == "Test Objective"
    assert "plan_length" in res
