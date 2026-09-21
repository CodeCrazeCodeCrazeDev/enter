# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Verification and integration test suite covering
the 200-paper quantitative research corpus (IDs 301-500) and cross-layer cognitive OS integrations.
"""

from __future__ import annotations
import os
import yaml
import pytest
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_301_500_paper_corpus_principles,
    register_200_paper_corpus_principles,
    ALPHAALGO_301_500_PRINCIPLES,
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid


def test_200_paper_corpus_yaml_integrity_and_zero_overlap() -> None:
    """Verifies that docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml exists, contains 200 papers,
    and has 0 title/DOI overlap against papers 1-300."""
    yaml_200_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(yaml_200_path), f"File {yaml_200_path} does not exist!"

    with open(yaml_200_path, "r", encoding="utf-8") as f:
        data_200 = yaml.safe_load(f)

    papers_200 = data_200.get("papers", [])
    assert len(papers_200) == 200, f"Expected exactly 200 papers, found {len(papers_200)}"

    ids = [p["id"] for p in papers_200]
    assert min(ids) == 301 and max(ids) == 500

    # Load papers 1-300 to verify 0 duplicate overlap
    previous_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]

    prev_titles = set()
    prev_dois = set()

    for p_path in previous_paths:
        if os.path.exists(p_path):
            with open(p_path, "r", encoding="utf-8") as f:
                d = yaml.safe_load(f)
            for p in d.get("papers", []):
                meta = p.get("metadata", {})
                if "title" in meta:
                    prev_titles.add(meta["title"].lower().strip())
                if "doi" in meta:
                    prev_dois.add(meta["doi"].lower().strip())

    for p in papers_200:
        meta = p["metadata"]
        title_200 = meta["title"].lower().strip()
        doi_200 = meta["doi"].lower().strip()

        assert title_200 not in prev_titles, f"Duplicate title found in 200-paper corpus: '{meta['title']}'"
        assert doi_200 not in prev_dois, f"Duplicate DOI found in 200-paper corpus: '{meta['doi']}'"


def test_extracted_principles_registration_and_literature_review() -> None:
    """Verifies that 200-paper corpus principles are correctly registered and queryable in Research OS."""
    principles = register_301_500_paper_corpus_principles()
    assert len(principles) >= 5
    assert len(register_200_paper_corpus_principles()) == len(principles)

    ros = ResearchOS()
    lit_review = ros.conduct_literature_review("AEAN Multi-Agent")

    assert lit_review["domain"] == "AEAN Multi-Agent"
    assert lit_review["reviewed_citations_count"] > 0
    assert len(lit_review["extracted_principles"]) > 0


def test_cross_subsystem_runtime_integration() -> None:
    """Verifies end-to-end multi-layer state handoffs between Research OS, EIOS Kernel, EOS Engine, and AEAN HiveMind."""
    # 1. Research OS registers and validates a hypothesis
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Token-Weighted Bidding for Agent Swarms",
        description="Sub-agents with higher capability profiles yield higher EV.",
        null_hypothesis="Token bidding provides zero task improvement.",
        target_metric="task_throughput"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    exp_res = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    # 2. EIOS Kernel ingests validated research and performs active inference sensing
    kernel = EIOSKernel()
    kernel.register_research_hypothesis({
        "hypothesis_id": hyp.hypothesis_id,
        "title": hyp.title,
        "description": hyp.description
    })
    assert str(hyp.hypothesis_id) in kernel.research_hypotheses

    sensory_data = [
        {"pragmatic_cost": 0.2, "epistemic_uncertainty": 0.8},
        {"pragmatic_cost": 0.1, "epistemic_uncertainty": 0.2}
    ]
    anomalies = kernel.sense_opportunity_anomalies(sensory_data)
    assert len(anomalies) == 1  # 0.2 + 0.8 = 1.0 > 0.6

    # 3. EOS Engine ingests research hypothesis into opportunity graph
    eos = EOSEngine()
    eos_hyp = eos.ingest_validated_research({
        "title": hyp.title,
        "domain": hyp.domain,
        "description": hyp.description
    })
    assert len(eos.active_hypotheses) >= 1
    similar_ops = eos.opportunity_graph.find_similar_opportunities(["research_validated"])
    assert len(similar_ops) >= 1

    # 4. AEAN HiveMind registers research insight and arbitrates token bids
    hive_mind = HiveMind(token_budget=50)
    bid = hive_mind.register_research_insight({
        "title": hyp.title,
        "priority": 0.95,
        "expected_value": 1.5,
        "token_cost": 20
    })
    assert bid.priority == 0.95

    grants = hive_mind.arbitrate([bid])
    assert len(grants) == 1
    assert grants[0].granted is True
    assert grants[0].tokens == 20
