# -*- coding: utf-8 -*-
"""
test_200_paper_integration.py: Verification and integration test suite covering
the 200-paper corpus (IDs 301-500) and cross-layer integration across Research OS,
EIOS Kernel, EOS Engine, AEAN HiveMind, and Research Integration components.
"""

from __future__ import annotations
import os
import yaml
import pytest
from uuid import UUID

from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
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
from apodex.aean.coordination.hive_mind import HiveMind


def test_complete_500_paper_corpus_zero_overlap() -> None:
    """Verifies that all 500 papers across all corpus files have 100% unique titles and identifiers."""
    db1_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    db2_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    db3_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"

    assert os.path.exists(db1_path), f"File {db1_path} missing"
    assert os.path.exists(db2_path), f"File {db2_path} missing"
    assert os.path.exists(db3_path), f"File {db3_path} missing"

    with open(db1_path, "r", encoding="utf-8") as f:
        db1 = yaml.safe_load(f)
    with open(db2_path, "r", encoding="utf-8") as f:
        db2 = yaml.safe_load(f)
    with open(db3_path, "r", encoding="utf-8") as f:
        db3 = yaml.safe_load(f)

    papers1 = db1.get("papers", [])
    papers2 = db2.get("papers", [])
    papers3 = db3.get("papers", [])

    assert len(papers1) == 200, f"Expected 200 papers in DB1, got {len(papers1)}"
    assert len(papers2) == 100, f"Expected 100 papers in DB2, got {len(papers2)}"
    assert len(papers3) == 200, f"Expected 200 papers in DB3, got {len(papers3)}"

    all_papers = papers1 + papers2 + papers3
    assert len(all_papers) == 500

    # Unique IDs check
    paper_ids = [p["id"] for p in all_papers]
    assert len(set(paper_ids)) == 500

    # Unique Titles check
    titles = [p["metadata"]["title"].lower() for p in all_papers]
    assert len(set(titles)) == 500, f"Found duplicate titles among {len(titles)} papers"

    # DOIs for papers 201-500 check
    new_dois = [p["metadata"]["doi"] for p in (papers2 + papers3)]
    assert len(set(new_dois)) == 300, f"Found duplicate DOIs among 300 new papers"


def test_200_paper_corpus_principle_registration() -> None:
    """Verifies registration of the extracted principles from papers 301-500."""
    principles = register_200_paper_corpus_principles()

    assert "hawkes_non_gaussian_stability" in principles
    assert "active_inference_efe_causal_routing" in principles
    assert "dpo_trajectory_distance_penalization" in principles
    assert "game_theoretic_token_bidding" in principles
    assert "island_map_elites_migration_gates" in principles

    assert principles["hawkes_non_gaussian_stability"]["target_subsystem"] == "EIOSKernel"
    assert principles["active_inference_efe_causal_routing"]["target_subsystem"] == "ResearchOS"


def test_research_os_literature_review_and_cross_subsystem_handoff() -> None:
    """Verifies ResearchOS literature review synthesis and cross-subsystem state handoffs."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()

    review = ros.conduct_literature_review("Active Inference")
    assert review["total_corpus_papers_indexed"] == 500
    assert len(review["synthesized_trends"]) == 5

    hyp = ros.register_hypothesis(
        title="Hawkes Anomaly Sensing Validation",
        description="Self-exciting intensity shifts predict book imbalance anomalies.",
        null_hypothesis="Hawkes intensity does not predict anomalies.",
        target_metric="book_imbalance_accuracy"
    )

    success_kernel = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, kernel_instance=kernel)
    assert success_kernel is True
    assert len(kernel.registered_hypotheses) == 1

    anomalies = kernel.sense_opportunity_anomalies([{"timestamp": 1.0}, {"timestamp": 1.2}])
    assert "hawkes_intensity" in anomalies
    assert "expected_free_energy" in anomalies

    success_eos = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos_instance=eos)
    assert success_eos is True
    assert len(eos.active_hypotheses) == 1


def test_aean_hivemind_research_token_bidding() -> None:
    """Verifies AEAN HiveMind research insight token registration and bidding."""
    hive = HiveMind(token_budget=50)

    bid1 = hive.register_research_insight(task="Sense Order Book Anomaly", priority=0.9, expected_value=0.8, token_cost=20)
    bid2 = hive.register_research_insight(task="Execute Multi-Agent Funnel", priority=0.5, expected_value=0.4, token_cost=20)

    grants = hive.arbitrate([bid1, bid2])
    assert len(grants) == 2
    assert grants[0].task == "Sense Order Book Anomaly"
    assert grants[0].granted is True


def test_sft_preference_collector_edit_distance_penalty() -> None:
    """Verifies that SFTPreferenceCollector applies Levenshtein edit trajectory distance penalties."""
    collector = SFTPreferenceCollector(discount_factor=0.9, edit_distance_penalty_weight=0.1)

    steps_a = [
        TrajectoryStep(action="query", predicted_expectation=0.5, actual_outcome=0.8, reward=0.8),
        TrajectoryStep(action="verify", predicted_expectation=0.8, actual_outcome=0.9, reward=0.9)
    ]
    steps_b = [
        TrajectoryStep(action="query", predicted_expectation=0.5, actual_outcome=0.3, reward=0.3),
        TrajectoryStep(action="fallback", predicted_expectation=0.3, actual_outcome=0.4, reward=0.4)
    ]

    dpo_pair = collector.compile_dpo_preference_pair("Run task", steps_a, steps_b)

    assert "edit_distance_penalty" in dpo_pair
    assert dpo_pair["edit_distance_penalty"] > 0.0
    assert dpo_pair["margin"] > 0.0
