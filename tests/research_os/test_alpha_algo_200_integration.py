# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite validating the 200-paper
corpus (IDs 301–500), principle registration, literature review querying, and cross-layer
state handoffs across Research OS, EIOS Kernel, EOS Engine, and AEAN Hive Mind.
"""

import os
import yaml
import pytest
from apodex.ai_eos.research.integration import (
    register_301_500_paper_corpus_principles,
    register_200_paper_corpus_principles,
    ResearchToSystemBridge,
    ALPHAALGO_301_500_PRINCIPLES
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid


def test_200_paper_corpus_uniqueness_and_integrity():
    """Verify 0 duplicate titles or DOIs across all 500 papers (1-200, 201-300, 301-500)."""
    db1_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    db2_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    db3_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"

    assert os.path.exists(db1_path), "AI_EOS_RESEARCH_DB.yaml missing"
    assert os.path.exists(db2_path), "ALPHA_ALGO_100_NEW_RESEARCH.yaml missing"
    assert os.path.exists(db3_path), "ALPHA_ALGO_200_NEW_RESEARCH.yaml missing"

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

    titles1 = {p["metadata"]["title"].strip().lower() for p in papers1}
    titles2 = {p["metadata"]["title"].strip().lower() for p in papers2}
    titles3 = {p["metadata"]["title"].strip().lower() for p in papers3}

    # Verify zero overlap between all sets
    assert len(titles1.intersection(titles2)) == 0, "Title overlap between DB1 and DB2!"
    assert len(titles1.intersection(titles3)) == 0, "Title overlap between DB1 and DB3!"
    assert len(titles2.intersection(titles3)) == 0, "Title overlap between DB2 and DB3!"

    # Verify DOIs in DB3
    dois3 = {str(p["metadata"]["doi"]).strip().lower() for p in papers3}
    assert len(dois3) == 200, f"Expected 200 unique DOIs in DB3, got {len(dois3)}"


def test_principle_registration_and_literature_review():
    """Verify registration of 200-paper principles and ResearchOS querying."""
    principles = register_301_500_paper_corpus_principles()
    alias_principles = register_200_paper_corpus_principles()

    assert len(principles) == 8
    assert principles == alias_principles
    assert principles == ALPHAALGO_301_500_PRINCIPLES

    ros = ResearchOS()
    review = ros.conduct_literature_review("AEAN")

    assert review["domain"] == "AEAN"
    assert review["reviewed_citations_count"] > 0
    assert len(review["synthesized_trends"]) > 0
    assert len(review["corpus_principles"]) > 0


def test_cross_subsystem_handoff_bridge():
    """Verify end-to-end handoff between ResearchOS -> EIOS Kernel -> EOS Engine -> AEAN HiveMind."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind(token_budget=100)

    bridge = ResearchToSystemBridge(research_os=ros, kernel=kernel, eos_engine=eos, hive_mind=hive)

    # 1. Register hypothesis in ResearchOS
    hyp = ros.register_hypothesis(
        title="Active Inference Multi-Agent Arbitrage",
        description="Active inference minimizes EFE in multi-agent compute bidding.",
        null_hypothesis="Active inference yields no improvement over random arbitration.",
        target_metric="roi",
        significance_alpha=0.05
    )

    # 2. Run simulation in ResearchOS to validate hypothesis
    exp = ros.create_experiment(hyp.hypothesis_id, seed=42)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert hyp.status in {"validated", "registered"}

    # 3. Export to EIOS Kernel
    export_res = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, kernel)
    assert export_res["exported"] is True
    assert len(kernel.registered_research_hypotheses) == 1

    # 4. Sense anomalies in EIOS Kernel
    anomalies = kernel.sense_opportunity_anomalies()
    assert isinstance(anomalies, list)

    # 5. Promote to EOS Engine
    eos_res = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    assert eos_res["ingested_id"] == str(hyp.hypothesis_id)
    assert hyp in eos.active_hypotheses

    # 6. Cross-layer Bridge handoff
    bridge_res = bridge.handoff_validated_hypothesis(hyp.hypothesis_id)
    assert bridge_res["hypothesis_id"] == str(hyp.hypothesis_id)
    assert bridge_res["hive_mind_bidding"] is not None
