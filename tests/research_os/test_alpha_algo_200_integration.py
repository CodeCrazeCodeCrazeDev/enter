# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Unit and integration tests for the 200-paper research corpus
(IDs 301-500) zero-overlap verification, principle registration, ResearchOS multi-field literature review,
AEAN HiveMind bidding, EOS Engine opportunity scoring, and EIOS Kernel active inference sensing.
"""

import os
import yaml
import pytest
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
    ResearchToSystemBridge,
    ALPHAALGO_200_PRINCIPLES
)
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.world_model.world_model import WorldModel


def test_200_paper_corpus_zero_overlap():
    """Verify 200 new papers (IDs 301-500) exist and have zero title/DOI overlap against baseline databases."""
    yaml_200_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(yaml_200_path), f"File {yaml_200_path} must exist."

    with open(yaml_200_path, "r", encoding="utf-8") as f:
        db_200 = yaml.safe_load(f)

    papers_200 = db_200.get("papers", [])
    assert len(papers_200) == 200, f"Expected 200 papers, found {len(papers_200)}"
    assert papers_200[0]["id"] == 301
    assert papers_200[-1]["id"] == 500

    # Load baseline titles
    baseline_titles = set()
    baseline_dois = set()

    for path in ["docs/research/papers/AI_EOS_RESEARCH_DB.yaml", "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            p_list = data if isinstance(data, list) else data.get("papers", [])
            for p in p_list:
                meta = p.get("metadata", {})
                if "title" in meta:
                    baseline_titles.add(meta["title"].lower())
                if "doi" in meta:
                    baseline_dois.add(meta["doi"].lower())

    # Check that none of the 200 paper titles or DOIs are in baseline
    for p in papers_200:
        meta = p.get("metadata", {})
        title_lower = meta.get("title", "").lower()
        doi_lower = meta.get("doi", "").lower()

        assert title_lower not in baseline_titles, f"Duplicate title found: {title_lower}"
        assert doi_lower not in baseline_dois, f"Duplicate DOI found: {doi_lower}"


def test_principle_registration_and_literature_review():
    """Verify principles from the 200-paper corpus register into ResearchOS and support multi-field literature reviews."""
    ros = ResearchOS()
    principles = register_200_paper_corpus_principles(ros)

    assert len(principles) >= 8
    assert hasattr(ros, "registered_corpus_principles")
    assert len(ros.registered_corpus_principles) >= 8

    # Query multi-field literature review for AEAN
    review_aean = ros.conduct_literature_review("AEAN")
    assert review_aean["reviewed_citations_count"] > 0
    assert len(review_aean["matched_principles"]) > 0

    # Query multi-field literature review for Active Inference
    review_eios = ros.conduct_literature_review("active inference")
    assert review_eios["reviewed_citations_count"] > 0


def test_aean_hive_mind_enhancements():
    """Verify AEAN HiveMind sycophancy mitigation and research insight bidding."""
    hm = HiveMind(token_budget=50)

    # Register research insight bid
    grant = hm.register_research_insight("execute_active_inference", priority=0.9, expected_value=0.8, token_cost=15)
    assert grant.granted is True
    assert grant.task == "execute_active_inference"

    # Test sycophancy penalty on duplicate score bids
    bids = [
        TaskBid(task="task_a", priority=0.8, expected_value=0.5, token_cost=10),
        TaskBid(task="task_b", priority=0.8, expected_value=0.5, token_cost=10),  # Duplicate score -> sycophancy penalty
        TaskBid(task="task_c", priority=0.85, expected_value=0.5, token_cost=10)
    ]
    grants = hm.arbitrate(bids)
    assert len(grants) == 3
    # task_c should clear first as it lacks duplicate sycophancy penalty
    assert grants[0].task == "task_c"


def test_eos_engine_active_inference_evaluation():
    """Verify EOS Engine opportunity EFE evaluation and research ingestion."""
    eos = EOSEngine()

    # Research ingestion
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Market Risk Reduction",
        description="Active inference minimizes venture runway risk.",
        null_hypothesis="Active inference has no effect on runway.",
        target_metric="runway_months"
    )

    eos.ingest_validated_research(hyp)
    assert len(eos.active_hypotheses) == 1

    # Opportunity EFE calculation
    efe_score = eos.evaluate_opportunity_efe(hyp)
    assert isinstance(efe_score, float)
    assert efe_score > 0.0


def test_eios_kernel_active_sensing():
    """Verify EIOS Kernel hypothesis registration and EFE anomaly sensing."""
    kernel = EIOSKernel()

    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Hawkes Anomaly Detection",
        description="Self-exciting point processes detect kernel execution faults.",
        null_hypothesis="Point processes do not detect kernel faults.",
        target_metric="fault_rate"
    )

    node_id = kernel.register_research_hypothesis(hyp)
    assert node_id.startswith("node_hyp_")

    anomaly_report = kernel.sense_opportunity_anomalies()
    assert "efe_anomaly_score" in anomaly_report
    assert anomaly_report["total_nodes"] == 1
    assert anomaly_report["pending_nodes"] == 1


def test_research_to_system_bridge_cross_layer_handoff():
    """Verify end-to-end cross-layer active inference state handoff via ResearchToSystemBridge."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive_mind = HiveMind(token_budget=100)
    world_model = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive_mind,
        world_model=world_model
    )

    hyp = ros.register_hypothesis(
        title="Unified Cross-Layer Cognitive Integration",
        description="Cross-layer state handoff unifies ResearchOS, EIOS, EOS, AEAN, and WorldModel.",
        null_hypothesis="Cross-layer state handoff does not improve system unity.",
        target_metric="integration_score"
    )

    results = bridge.hand_off_hypothesis(hyp.hypothesis_id)
    assert results["hypothesis_id"] == str(hyp.hypothesis_id)
    assert "eios_kernel" in results["handoffs"]
    assert "eos_engine" in results["handoffs"]
    assert "aean_hive_mind" in results["handoffs"]
    assert "world_model" in results["handoffs"]

    # Verify state in downstream subsystems
    assert len(eos.active_hypotheses) == 1
    assert len(world_model.beliefs) == 1
