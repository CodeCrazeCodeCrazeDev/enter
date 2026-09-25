# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Test suite covering the 200-paper research corpus
(IDs 301-500), principle registration, ResearchOS literature synthesis, subsystem
enhancements across AEAN, EOS, EIOS, and ResearchOS, and cross-layer state handoffs.
"""

from __future__ import annotations
import os
import yaml
import pytest
from typing import Dict, Any

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, OpportunityNode
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.ai_eos.research.integration import (
    register_500_paper_corpus_principles,
    register_200_paper_corpus_principles,
    ResearchToSystemBridge,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    TrajectoryStep,
    SpecializedAgentProfile
)


def test_500_paper_corpus_uniqueness_and_integrity() -> None:
    """Verifies that all 500 papers across DB1, DB2, and DB3 have 100% unique IDs, titles, and DOIs."""
    yaml_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    ]

    seen_ids = set()
    seen_titles = set()
    seen_dois = set()
    total_papers = 0

    for path in yaml_paths:
        assert os.path.exists(path), f"File {path} must exist."
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        papers = data.get("papers", [])
        total_papers += len(papers)

        for p in papers:
            paper_id = p.get("id")
            meta = p.get("metadata", {})
            title = meta.get("title", "").strip().lower()
            doi = meta.get("doi", "").strip().lower()

            assert paper_id not in seen_ids, f"Duplicate paper ID {paper_id} in {path}"
            seen_ids.add(paper_id)

            assert title, f"Paper ID {paper_id} missing title"
            assert title not in seen_titles, f"Duplicate title '{title}' for ID {paper_id}"
            seen_titles.add(title)

            if doi and doi != "n/a":
                assert doi not in seen_dois, f"Duplicate DOI '{doi}' for ID {paper_id}"
                seen_dois.add(doi)

    assert total_papers == 500, f"Expected 500 papers, found {total_papers}"


def test_principle_registration_and_literature_review() -> None:
    """Verifies principle registration and multi-field literature review searching in ResearchOS."""
    principles = register_500_paper_corpus_principles()
    assert len(principles) == 500

    alias_principles = register_200_paper_corpus_principles()
    assert len(alias_principles) == 500

    ros = ResearchOS()

    # Test literature review search by domain
    aean_review = ros.conduct_literature_review("AEAN")
    assert aean_review["total_corpus_papers"] == 500
    assert aean_review["reviewed_citations_count"] > 0
    assert len(aean_review["synthesized_trends"]) > 0

    eios_review = ros.conduct_literature_review("Executive Intelligence")
    assert eios_review["reviewed_citations_count"] > 0

    all_review = ros.conduct_literature_review("all")
    assert all_review["reviewed_citations_count"] == 500


def test_aean_hivemind_research_insight_bidding() -> None:
    """Verifies AEAN HiveMind research insight registration and token bidding."""
    hive_mind = HiveMind(token_budget=50)

    insight = {
        "title": "Monotonic Value Function Factorisation for Swarms",
        "priority": 0.90,
        "expected_value": 0.95,
        "token_cost": 20
    }

    bid = hive_mind.register_research_insight(insight)
    assert bid.priority == 0.90
    assert bid.expected_value == 0.95
    assert bid.score > 1.0

    grants = hive_mind.arbitrate([bid])
    assert len(grants) == 1
    assert grants[0].granted is True
    assert grants[0].tokens == 20


def test_eios_kernel_and_eos_engine_hypotheses_integration() -> None:
    """Verifies hypothesis active inference sensing in EIOS Kernel and hypothesis ingestion in EOSEngine."""
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Active Inference Anomaly Sensing in DAGs",
        description="Minimizes Expected Free Energy across DAG execution nodes.",
        null_hypothesis="No anomaly reduction",
        target_metric="EFE_reduction"
    )

    exp = ros.create_experiment(hyp.hypothesis_id)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.0)
    assert hyp.status in ["validated", "active"]

    kernel = EIOSKernel()
    ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, kernel)
    assert len(kernel.metrics_history) == 1
    assert kernel.metrics_history[0]["type"] == "research_hypothesis"

    eos = EOSEngine()
    ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    active_hyps = eos.active_hypotheses
    assert len(active_hyps) == 1
    assert active_hyps[0].title == "Active Inference Anomaly Sensing in DAGs"


def test_cross_layer_research_to_system_bridge() -> None:
    """Verifies ResearchToSystemBridge multi-layer state handoffs across Layer 1-4."""
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Cross-Layer Active Inference State Handoff",
        description="Validates state transitions across ResearchOS, EIOS, EOS, and AEAN.",
        null_hypothesis="No cross-layer synchronization",
        target_metric="state_handoff_fidelity"
    )
    exp = ros.create_experiment(hyp.hypothesis_id)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.0)

    kernel = EIOSKernel()
    eos = EOSEngine()
    hive_mind = HiveMind()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive_mind
    )

    handoff_res = bridge.execute_cross_layer_handoff(hyp.hypothesis_id)
    assert handoff_res["status"] == "validated"
    assert handoff_res["eios_registered"] is True
    assert handoff_res["eos_promoted"] is True
    assert handoff_res["hive_mind_bid_score"] > 0.0
