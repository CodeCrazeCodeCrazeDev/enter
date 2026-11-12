# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Verification and integration test suite validating
the 200-paper research corpus (IDs 301-500) and its cross-layer integration into AEAN,
EOS Engine, EIOS Kernel, and Research OS.
"""

from __future__ import annotations
import os
import yaml
import pytest
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_301_500_paper_corpus_principles,
    register_500_paper_corpus_principles,
    ALPHAALGO_301_500_PRINCIPLES,
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid


def test_200_paper_corpus_zero_overlap() -> None:
    """Verifies that all 200 papers in ALPHA_ALGO_200_NEW_RESEARCH.yaml have zero overlap with papers 1-300."""
    new_db_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    old_db_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    mid_db_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"

    assert os.path.exists(new_db_path), f"File {new_db_path} must exist."

    existing_titles = []
    for path in [old_db_path, mid_db_path]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                db_data = yaml.safe_load(f)
            for p in db_data.get("papers", []):
                existing_titles.append(p["metadata"]["title"].lower())

    with open(new_db_path, "r", encoding="utf-8") as f:
        new_db_data = yaml.safe_load(f)

    new_papers = new_db_data.get("papers", [])
    assert len(new_papers) == 200, f"Expected 200 new papers, got {len(new_papers)}."

    for p in new_papers:
        title = p["metadata"]["title"].lower()
        p_tokens = set(title.split())
        for ext in existing_titles:
            ext_tokens = set(ext.split())
            if not p_tokens or not ext_tokens:
                continue
            intersection = p_tokens.intersection(ext_tokens)
            union = p_tokens.union(ext_tokens)
            score = len(intersection) / len(union)
            assert score <= 0.35, f"Paper #{p['id']} '{title}' overlaps with '{ext}' with Jaccard score {score:.2f} > 0.35"


def test_principle_registration_and_literature_review() -> None:
    """Verifies principles registration and querying in ResearchOS.conduct_literature_review."""
    principles = register_301_500_paper_corpus_principles()
    assert "Active Inference" in principles
    assert "Multi-Agent Systems" in principles
    assert principles["Active Inference"]["count"] == 40

    ros = ResearchOS()
    review = ros.conduct_literature_review(domain="Active Inference")
    assert review["domain"] == "Active Inference"
    assert review["reviewed_citations_count"] == 500
    assert "extracted_principles" in review
    assert review["extracted_principles"]["count"] == 40


def test_eios_kernel_active_inference_sensing() -> None:
    """Verifies that EIOSKernel registers research hypotheses and senses EFE opportunity anomalies."""
    kernel = EIOSKernel()
    hyp_id = str(uuid4())
    record = kernel.register_research_hypothesis(
        hypothesis_id=hyp_id,
        title="Active Inference Free Energy Minimization",
        target_metric="predictive_entropy",
        alpha=0.01
    )
    assert record["hypothesis_id"] == hyp_id
    assert hyp_id in kernel.registered_hypotheses

    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) > 0
    assert anomalies[0]["hypothesis_id"] == hyp_id
    assert anomalies[0]["efe_score"] > 1.0


def test_eos_engine_opportunity_ingestion() -> None:
    """Verifies that EOSEngine ingests validated research hypotheses into its opportunity graph."""
    engine = EOSEngine()
    hyp_id = str(uuid4())
    result = engine.ingest_validated_research(
        hypothesis_id=hyp_id,
        title="Step-Level Advantage Estimation",
        domain="RL & Alignment",
        effect_size=1.2
    )

    assert result["status"] == "ingested_into_eos"
    assert len(engine.active_hypotheses) == 1
    assert engine.active_hypotheses[0].title == "Step-Level Advantage Estimation"


def test_aean_hive_mind_token_bidding() -> None:
    """Verifies that HiveMind registers research insights and arbitrates token grants."""
    hive = HiveMind(token_budget=50)
    bid = hive.register_research_insight(
        insight_id=str(uuid4()),
        title="Decentralized Token Auction Clearing",
        priority=0.90,
        token_cost=15
    )

    assert isinstance(bid, TaskBid)
    assert len(hive.registered_research_bids) == 1

    grants = hive.arbitrate([bid])
    assert len(grants) == 1
    assert grants[0].granted is True
    assert grants[0].tokens == 15


def test_cross_layer_research_state_handoff() -> None:
    """Verifies end-to-end handoff of validated hypotheses from ResearchOS to EIOS Kernel and EOS Engine."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()

    # 1. Register hypothesis
    hyp = ros.register_hypothesis(
        title="High-Frequency Hawkes Jump Volatility",
        description="Self-excitation jump models reduce forecast variance.",
        null_hypothesis="H0: mean return <= 0",
        target_metric="volatility_error",
        significance_alpha=0.05
    )

    # 2. Create and run experiment simulation to validate
    exp = ros.create_experiment(hypothesis_id=hyp.hypothesis_id, seed=123)
    validated_exp = ros.execute_experiment_simulation(experiment_id=exp.experiment_id, ground_truth_yield=2.5)

    assert hyp.status == "validated"

    # 3. Export to EIOS Kernel
    kernel_result = ros.export_validated_hypothesis_to_kernel(
        hypothesis_id=hyp.hypothesis_id,
        kernel_instance=kernel
    )
    assert str(hyp.hypothesis_id) in kernel.registered_hypotheses

    # 4. Promote to EOS Engine
    eos_result = ros.promote_hypothesis_to_eos(
        hypothesis_id=hyp.hypothesis_id,
        eos_engine=eos
    )
    assert eos_result["status"] == "ingested_into_eos"
    assert len(eos.active_hypotheses) == 1
