# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Verification and integration test suite covering
the 200-paper quantitative research corpus (IDs 301-500) and cross-layer integration
across Research OS, EIOS Kernel, EOS Engine, and AEAN HiveMind.
"""

from __future__ import annotations
import os
import yaml
import pytest
from typing import Dict, Any

from apodex.ai_eos.research.integration import (
    ALPHAALGO_200_PRINCIPLES,
    register_200_paper_corpus_principles,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    RewriteProposal,
    ProgramGenome,
    TrajectoryStep,
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, Hypothesis
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid


def test_200_paper_database_integrity_and_zero_overlap() -> None:
    """Verifies that the 200-paper YAML database is properly formatted and passes zero overlap audits."""
    yaml_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(yaml_path), f"File {yaml_path} does not exist."

    with open(yaml_path, "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    papers = db.get("papers", [])
    assert len(papers) == 200, f"Expected 200 papers, found {len(papers)}"

    ids = [p["id"] for p in papers]
    assert min(ids) == 301
    assert max(ids) == 500

    matrix = db.get("duplicate_detection_matrix", [])
    flagged = [row for row in matrix if row.get("status") == "FLAGGED DUPLICATE"]
    assert len(flagged) == 0, f"Programmatic audit found flagged duplicates: {flagged}"


def test_200_paper_principles_registration_and_literature_review() -> None:
    """Verifies that extracted principles from papers 301-500 are registered and queryable by ResearchOS."""
    principles = register_200_paper_corpus_principles()
    assert len(principles) == len(ALPHAALGO_200_PRINCIPLES)
    assert len(principles) >= 5

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")

    assert review["domain"] == "Active Inference"
    assert review["matching_principles_count"] >= 1
    assert any("Active Inference" in trend or "Inference" in trend for trend in review["synthesized_trends"])


def test_code_rewrite_ast_recursion_depth_verification() -> None:
    """Verifies that CodeRewriteEngine enforces AST recursion depth limits."""
    engine = CodeRewriteEngine(allowed_paths=[os.getcwd()], max_recursion_depth=2)

    # Valid rewrite proposal without excessive recursion
    valid_snippet = "def compute_val(n):\n    if n <= 1:\n        return 1\n    return compute_val(n - 1)\n"
    prop_valid = RewriteProposal(
        target_filepath=os.path.abspath("test_file.py"),
        original_snippet="pass",
        proposed_snippet=valid_snippet,
        rationale="Single recursive call"
    )
    assert engine.verify_proposal_ast(prop_valid) is True

    # Invalid rewrite proposal with excessive recursion calls (> 2)
    invalid_snippet = "def compute_val(n):\n    if n <= 1:\n        return 1\n    return compute_val(n - 1) + compute_val(n - 2) + compute_val(n - 3)\n"
    prop_invalid = RewriteProposal(
        target_filepath=os.path.abspath("test_file.py"),
        original_snippet="pass",
        proposed_snippet=invalid_snippet,
        rationale="Excessive recursive calls"
    )
    assert engine.verify_proposal_ast(prop_invalid) is False


def test_genetic_workflow_optimizer_elite_insertion() -> None:
    """Verifies island population re-sorting and elite insertion in GeneticWorkflowOptimizer."""
    optimizer = GeneticWorkflowOptimizer(population_size=5, mutation_rate=0.2)
    base_template = "Execute strategy workflow"
    optimizer.initialize_population(base_template, {"param": 1.0})

    elite_genome = ProgramGenome(
        prompt_template="Super elite prompt workflow",
        parameters={"param": 2.0},
        fitness_score=0.99
    )
    optimizer.insert_elite(elite_genome)

    assert len(optimizer.population) == 5
    assert optimizer.population[0].fitness_score == 0.99
    assert optimizer.population[0].prompt_template == "Super elite prompt workflow"


def test_sft_preference_collector_clipped_advantages() -> None:
    """Verifies that SFTPreferenceCollector enforces clipped advantage bounds."""
    collector = SFTPreferenceCollector(discount_factor=0.95, max_advantage_clip=2.0)

    steps = [
        TrajectoryStep(action="step1", predicted_expectation=0.0, actual_outcome=10.0, reward=10.0)
    ]
    advantages = collector.compute_advantages(steps)
    # Raw advantage = 10.0 - 0.0 = 10.0, clipped to max_advantage_clip = 2.0
    assert advantages[0] == 2.0


def test_cross_subsystem_200_paper_integrations() -> None:
    """Verifies joint multi-subsystem workflows across Research OS, EIOS Kernel, EOS Engine, and AEAN HiveMind."""
    ros = ResearchOS()
    eos = EOSEngine()
    kernel = EIOSKernel()
    hive = HiveMind()

    # 1. Research OS registers and validates a hypothesis
    hyp = ros.register_hypothesis(
        title="Multi-Agent Token Arbitrate Principle 341",
        description="Verify token bidding efficiency under active inference.",
        null_hypothesis="Token bidding yields no gain",
        target_metric="efficiency"
    )
    exp = ros.create_experiment(hyp.hypothesis_id)
    validated_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert validated_exp.is_statistically_significant is True
    assert hyp.status == "validated"

    # 2. EOS Engine ingests validated research hypothesis
    eos.ingest_validated_research(hyp)
    assert len(eos.active_hypotheses) == 1
    assert eos.active_hypotheses[0].title == "Multi-Agent Token Arbitrate Principle 341"

    # 3. EIOS Kernel registers research hypothesis and senses anomalies
    kernel.register_research_hypothesis(hyp.title, hyp.description, efe_priority=0.85)
    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) >= 1
    assert anomalies[0]["source_hypothesis"] == "Multi-Agent Token Arbitrate Principle 341"

    # 4. AEAN HiveMind registers research insight and arbitrates bids
    hive.register_research_insight("Multi-Agent Token Arbitrate Principle 341", priority_boost=0.3)
    bids = [
        TaskBid(task="task_research_action", priority=0.9, expected_value=0.8, token_cost=20),
        TaskBid(task="task_backup", priority=0.3, expected_value=0.2, token_cost=30)
    ]
    grants = hive.arbitrate(bids)
    assert grants[0].task == "task_research_action"
    assert grants[0].granted is True
