# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite for the 200-paper research corpus
(IDs 301-500), principle registration, ResearchOS literature review synthesis, and cross-layer state handoffs.
"""

import pytest
import os
import yaml
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_301_500_paper_corpus_principles,
    ALPHAALGO_301_500_PRINCIPLES
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind


def test_200_paper_corpus_zero_overlap():
    """Verifies that papers 301-500 have 100% zero title and DOI overlap against papers 1-300."""
    path_1_200 = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    path_201_300 = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    path_301_500 = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"

    assert os.path.exists(path_1_200)
    assert os.path.exists(path_201_300)
    assert os.path.exists(path_301_500)

    with open(path_1_200, "r", encoding="utf-8") as f:
        data1 = yaml.safe_load(f)
    with open(path_201_300, "r", encoding="utf-8") as f:
        data2 = yaml.safe_load(f)
    with open(path_301_500, "r", encoding="utf-8") as f:
        data3 = yaml.safe_load(f)

    existing_titles = set()
    existing_dois = set()

    papers1 = data1.get("papers", [])
    papers2 = data2.get("papers", [])
    papers3 = data3.get("papers", [])

    assert len(papers3) == 200

    for p in papers1 + papers2:
        meta = p.get("metadata", {})
        if "title" in meta:
            existing_titles.add(meta["title"].lower().strip())
        if "doi" in meta and meta["doi"]:
            existing_dois.add(meta["doi"].lower().strip())

    for p in papers3:
        meta = p.get("metadata", {})
        title = meta.get("title", "").lower().strip()
        doi = meta.get("doi", "").lower().strip()

        assert title not in existing_titles, f"Title overlap detected: '{title}'"
        if doi:
            assert doi not in existing_dois, f"DOI overlap detected: '{doi}'"


def test_principle_registration():
    """Verifies principle registration for papers 301-500."""
    principles = register_301_500_paper_corpus_principles()
    assert len(principles) == 5
    assert "active_inference_efe" in principles
    assert "sycophancy_proof_multi_agent_consensus" in principles
    assert "causal_do_calculus_attribution" in principles
    assert "trajectory_dpo_process_supervision" in principles
    assert "map_elites_island_workflow_mutation" in principles


def test_research_os_literature_review():
    """Verifies ResearchOS literature review querying incorporating 500-paper principles."""
    ros = ResearchOS()
    synthesis = ros.conduct_literature_review("Active Inference & Causal Reasoning")

    assert synthesis["domain"] == "Active Inference & Causal Reasoning"
    assert synthesis["reviewed_citations_count"] == 500
    assert synthesis["principles_registered"] == 5
    assert len(synthesis["synthesized_trends"]) >= 4


def test_cross_layer_state_handoffs():
    """Validates active inference state handoffs across ResearchOS, EIOS Kernel, EOS Engine, and AEAN HiveMind."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind()

    # 1. Register and validate hypothesis in Research OS
    hyp = ros.register_hypothesis(
        title="Expected Free Energy Active Sensing Bounds",
        description="Minimizes epistemic surprise in volatile regimes.",
        null_hypothesis="EFE active sensing provides zero statistical advantage.",
        target_metric="sharpe_ratio",
        significance_alpha=0.05
    )

    exp = ros.create_experiment(hyp.hypothesis_id, seed=1234)
    evaluated_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)
    assert hyp.status == "validated"

    # 2. Export validated hypothesis to EIOS Kernel
    kernel_exported = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, kernel)
    assert kernel_exported is True
    assert len(kernel.registered_hypotheses) == 1

    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) == 1
    assert anomalies[0]["hypothesis_title"] == "Expected Free Energy Active Sensing Bounds"

    # 3. Promote validated hypothesis to EOS Engine
    eos_promoted = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    assert eos_promoted is True
    assert len(eos.active_hypotheses) == 1

    # 4. Register research insight in AEAN HiveMind
    hive.register_research_insight("Active Inference", "EFE minimization improves sub-agent token allocation efficiency.")
    assert len(hive.research_insights) == 1
    assert hive.research_insights[0]["topic"] == "Active Inference"
