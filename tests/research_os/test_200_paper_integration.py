# -*- coding: utf-8 -*-
"""
test_200_paper_integration.py: Integration test suite validating the 200-paper corpus (IDs 301-500),
zero title/DOI overlap auditing, transferable engineering principles registration, Research OS synthesis,
AEAN algorithmic improvements, and EIOS Kernel / EOS Engine active inference handoffs.
"""

import os
import yaml
import pytest
from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
    get_registered_corpus_principles,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    TrajectoryStep,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine


def test_200_paper_corpus_zero_overlap_audit() -> None:
    """Verifies that the 200 new research papers (IDs 301-500) have 100% zero title and DOI overlap against papers 1-300."""
    yaml_200_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(yaml_200_path), f"File {yaml_200_path} must exist."

    with open(yaml_200_path, "r", encoding="utf-8") as f:
        data_200 = yaml.safe_load(f)

    papers_200 = data_200.get("papers", [])
    assert len(papers_200) == 200, f"Expected exactly 200 papers in new dataset, found {len(papers_200)}"
    assert papers_200[0]["id"] == 301
    assert papers_200[-1]["id"] == 500

    # Collect existing titles and DOIs from prior datasets (IDs 1-300)
    existing_titles = set()
    existing_dois = set()
    prior_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]
    for path in prior_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                db = yaml.safe_load(f)
            for p in db.get("papers", []):
                meta = p.get("metadata", {})
                t = meta.get("title", "").strip().lower()
                d = meta.get("doi", "").strip().lower()
                if t:
                    existing_titles.add(t)
                if d:
                    existing_dois.add(d)

    assert len(existing_titles) >= 300, f"Expected at least 300 existing titles, found {len(existing_titles)}"

    # Audit new papers
    for p in papers_200:
        meta = p.get("metadata", {})
        title = meta.get("title", "").strip().lower()
        doi = meta.get("doi", "").strip().lower()

        assert title not in existing_titles, f"Title collision detected for paper ID {p['id']}: '{title}'"
        assert doi not in existing_dois, f"DOI collision detected for paper ID {p['id']}: '{doi}'"


def test_principle_registration_and_literature_review() -> None:
    """Verifies registration of 200-paper principles and ResearchOS literature synthesis."""
    principles = register_200_paper_corpus_principles()
    assert len(principles) >= 5
    assert "non_gaussian_hawkes_bounds" in principles
    assert "causal_do_calculus_routing" in principles

    ros = ResearchOS()
    synthesis = ros.conduct_literature_review("Causal Inference")

    assert synthesis["reviewed_citations_count"] == 500
    assert len(synthesis["active_principles_found"]) >= 1
    assert "Causal Do-Calculus Interventions in Active Inference Routing" in synthesis["active_principles_found"]


def test_aean_algorithmic_enhancements() -> None:
    """Verifies AEAN algorithmic enhancements: Hawkes stability, Island migration, edit penalties, causal routing."""
    # 1. Hawkes process stability check
    engine = CodeRewriteEngine(allowed_paths=["/tmp"])
    assert engine.check_hawkes_stability(mutation_rate_hz=0.1) is True

    # 2. Island MAP-Elites cross-island migration
    island1 = GeneticWorkflowOptimizer(population_size=4, island_id="island_1")
    island2 = GeneticWorkflowOptimizer(population_size=4, island_id="island_2")
    island1.initialize_population("template", {"learning_rate": 0.01})
    island2.initialize_population("template", {"learning_rate": 0.02})

    # Force identical fitness to trigger low variance
    for g in island1.population:
        g.fitness_score = 0.85
    for g in island2.population:
        g.fitness_score = 0.50

    migrated = island1.migrate_genomes_between_islands(island2, fitness_variance_threshold=0.01)
    assert migrated == 1
    assert len(island2.population) == 4

    # 3. Trajectory edit distance penalties in SFT preference collection
    collector = SFTPreferenceCollector(edit_distance_penalty_lambda=0.05)
    steps_a = [
        TrajectoryStep(action="step_1", predicted_expectation=0.5, actual_outcome=0.8, reward=0.8),
        TrajectoryStep(action="step_2", predicted_expectation=0.6, actual_outcome=0.9, reward=0.9)
    ]
    steps_b = [
        TrajectoryStep(action="step_1", predicted_expectation=0.5, actual_outcome=0.4, reward=0.3),
        TrajectoryStep(action="step_2", predicted_expectation=0.4, actual_outcome=0.5, reward=0.4)
    ]
    advs_a = collector.compute_advantages(steps_a)
    advs_b = collector.compute_advantages(steps_b)
    assert sum(advs_a) > sum(advs_b)

    dpo = collector.compile_dpo_preference_pair("Prompt string", steps_a, steps_b)
    assert dpo["margin"] > 0.0

    # 4. Causal Do-Calculus EFE task routing
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=5.0)
    agent = SpecializedAgentProfile(
        agent_id="causal_agent",
        domain_specialty="Causal Inference",
        cost_per_token=0.002,
        historical_success_rate=0.88,
        epistemic_curiosity=0.60
    )
    dispatcher.register_subagent(agent)
    selected_agent = dispatcher.route_task(task_complexity=100, domain="Causal Inference", do_intervention_weight=0.25)
    assert selected_agent == "causal_agent"


def test_cross_subsystem_active_inference_handoffs() -> None:
    """Verifies active inference hypothesis export handoffs from Research OS to EIOS Kernel and EOS Engine."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()

    # 1. Register and validate hypothesis
    hyp = ros.register_hypothesis(
        title="Non-Gaussian Hawkes Process Stability Proof",
        description="Verifies heavy-tailed volatility jump stability bounds in mutation loops.",
        null_hypothesis="No stability difference.",
        target_metric="mutation_stability_index",
        significance_alpha=0.05
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.0)

    # 2. Export to EIOS Kernel for Active Inference EFE sensing
    exported_kernel = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, kernel)
    assert exported_kernel is True
    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) >= 1
    assert "Non-Gaussian Hawkes Process" in anomalies[0]["title"]

    # 3. Promote to EOS Engine for decision engine ingestion
    promoted_eos = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    assert promoted_eos is True
    assert len(eos.active_hypotheses) == 1
    assert eos.active_hypotheses[0].title == "Non-Gaussian Hawkes Process Stability Proof"
