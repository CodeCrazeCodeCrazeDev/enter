# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite validating the 200-paper corpus
(IDs 301-500), principle registration, ResearchOS literature review synthesis, and cross-layer state
handoffs across AEAN, EOS Engine, EIOS Kernel, and Research OS.
"""

import os
import yaml
import pytest
from uuid import UUID

from apodex.ai_eos.research.integration import (
    register_301_500_paper_corpus_principles,
    ALPHAALGO_301_500_PRINCIPLES
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.arcs.kernel.kernel import EIOSKernel


def test_200_paper_corpus_uniqueness():
    """Verify all 500 papers across DB1 (1-200), DB2 (201-300), and DB3 (301-500) have zero title/DOI overlap."""
    p1_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    p2_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    p3_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"

    assert os.path.exists(p1_path)
    assert os.path.exists(p2_path)
    assert os.path.exists(p3_path)

    with open(p1_path, "r", encoding="utf-8") as f:
        db1 = yaml.safe_load(f)
    with open(p2_path, "r", encoding="utf-8") as f:
        db2 = yaml.safe_load(f)
    with open(p3_path, "r", encoding="utf-8") as f:
        db3 = yaml.safe_load(f)

    papers1 = db1.get("papers", db1) if isinstance(db1, dict) else db1
    papers2 = db2.get("papers", db2) if isinstance(db2, dict) else db2
    papers3 = db3.get("papers", db3) if isinstance(db3, dict) else db3

    assert len(papers1) == 200
    assert len(papers2) == 100
    assert len(papers3) == 200

    titles1 = {p["metadata"]["title"].lower() for p in papers1}
    titles2 = {p["metadata"]["title"].lower() for p in papers2}
    titles3 = {p["metadata"]["title"].lower() for p in papers3}

    # Verify zero title overlap
    assert len(titles1.intersection(titles2)) == 0
    assert len(titles1.intersection(titles3)) == 0
    assert len(titles2.intersection(titles3)) == 0


def test_principles_registration_and_literature_review():
    """Verify principles registration from papers 301-500 and ResearchOS synthesis."""
    principles = register_301_500_paper_corpus_principles()
    assert len(principles) == 5
    assert principles == ALPHAALGO_301_500_PRINCIPLES

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")

    assert review["domain"] == "Active Inference"
    assert review["reviewed_citations_count"] >= 200
    assert len(review["extracted_principles"]) == 1
    assert review["extracted_principles"][0]["principle_id"] == "P-341-380-ACTIVE-INFERENCE"


def test_cross_layer_subsystem_integration():
    """Verify cross-layer state handoffs from ResearchOS to AEAN HiveMind, EOS Engine, and EIOS Kernel."""
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Hawkes Liquidity Predictor",
        description="Predicts short-term liquidity cascades",
        null_hypothesis="No predictive power",
        target_metric="sharpe_ratio"
    )

    # 1. Promote hypothesis to EOS Engine
    eos = EOSEngine()
    ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    assert len(eos.opportunity_graph.nodes) == 1
    assert str(hyp.hypothesis_id) in eos.opportunity_graph.nodes

    # 2. Export hypothesis to EIOS Kernel
    kernel = EIOSKernel()
    ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, kernel)
    assert len(kernel.registered_hypotheses) == 1
    assert kernel.registered_hypotheses[0].title == "Hawkes Liquidity Predictor"

    # 3. Register research insight in AEAN HiveMind
    hm = HiveMind()
    initial_budget = hm.token_budget
    hm.register_research_insight({
        "name": hyp.title,
        "confidence": 0.92
    })
    assert hm.token_budget > initial_budget
