# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py

Comprehensive unit and integration test suite verifying:
- 200-paper corpus integrity (IDs 301-500) and zero title/DOI duplicate overlap against papers 1-300.
- Registration of 200-paper corpus principles via register_200_paper_corpus_principles().
- Research OS literature review multi-field querying across category, target_subsystem, description, and impl_module.
- Core subsystem runtime principle integrations across AEAN, EOS, EIOS, and Research OS.
"""

from __future__ import annotations
import os
import yaml
import pytest

from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
    CodeRewriteEngine,
    RewriteProposal,
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.ai_eos.domain.models import Hypothesis
from apodex.arcs.kernel.kernel import EIOSKernel


def test_200_paper_corpus_zero_duplicate_overlap() -> None:
    """Verify 200-paper corpus (IDs 301-500) has zero title or DOI duplicate overlap against papers 1-300."""
    new_yaml = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    existing_yamls = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
    ]

    assert os.path.exists(new_yaml), f"File {new_yaml} does not exist."

    existing_titles = set()
    existing_dois = set()

    for path in existing_yamls:
        if os.path.exists(path):
            with open(path) as f:
                data = yaml.safe_load(f)
                papers = data.get("papers") or data.get("research_papers") or []
                for p in papers:
                    meta = p.get("metadata", {})
                    t = meta.get("title") or p.get("paper_title")
                    d = meta.get("doi")
                    if t:
                        existing_titles.add(t.strip().lower())
                    if d:
                        existing_dois.add(d.strip().lower())

    with open(new_yaml) as f:
        new_data = yaml.safe_load(f)

    new_papers = new_data.get("papers", [])
    assert len(new_papers) == 200, f"Expected 200 papers, got {len(new_papers)}"
    assert new_papers[0]["id"] == 301
    assert new_papers[-1]["id"] == 500

    new_titles = set()
    new_dois = set()

    for p in new_papers:
        meta = p["metadata"]
        title = meta["title"].strip().lower()
        doi = meta["doi"].strip().lower()

        assert title not in existing_titles, f"Duplicate title against existing corpus: {meta['title']}"
        assert doi not in existing_dois, f"Duplicate DOI against existing corpus: {meta['doi']}"

        assert title not in new_titles, f"Duplicate title within 200-paper corpus: {meta['title']}"
        assert doi not in new_dois, f"Duplicate DOI within 200-paper corpus: {meta['doi']}"

        new_titles.add(title)
        new_dois.add(doi)


def test_register_200_paper_corpus_principles() -> None:
    """Verify principles registration from 200-paper corpus."""
    principles = register_200_paper_corpus_principles()
    assert isinstance(principles, list)
    assert len(principles) == 10

    required_fields = {"id", "category", "target_subsystem", "paper_title", "doi", "description", "extracted_principle", "impl_module"}
    for p in principles:
        assert required_fields.issubset(p.keys())


def test_research_os_literature_review_multi_field_query() -> None:
    """Verify ResearchOS literature review multi-field search."""
    ros = ResearchOS()

    # Query by Active Inference
    res1 = ros.conduct_literature_review("Active Inference")
    assert res1["matched_principles_count"] >= 1
    assert any("Active Inference" in p["category"] for p in res1["matched_principles"])

    # Query by subsystem EIOS
    res2 = ros.conduct_literature_review("EIOS")
    assert res2["matched_principles_count"] >= 1
    assert any(p["target_subsystem"] == "EIOS" for p in res2["matched_principles"])

    # Query all
    res_all = ros.conduct_literature_review("all")
    assert res_all["matched_principles_count"] == 10


def test_aean_hive_mind_token_deflator_and_insights() -> None:
    """Verify AEAN HiveMind arbitrates using token burn deflator and stores research insights."""
    hm = HiveMind(token_budget=100, token_burn_deflator=0.5)

    hm.register_research_insight({
        "source": "ResearchOS",
        "principle": "EFE Active Inference Task Routing"
    })
    assert len(hm.research_insights) == 1

    bids = [
        TaskBid(task="task_a", priority=0.9, expected_value=0.8, token_cost=40),
        TaskBid(task="task_b", priority=0.7, expected_value=0.6, token_cost=60),
    ]

    # With deflator = 0.5, effective costs are 20 and 30, total 50 <= budget 100
    grants = hm.arbitrate(bids)
    granted = hm.granted_tasks(grants)

    assert granted["task_a"] is True
    assert granted["task_b"] is True


def test_eos_engine_validated_research_ingestion() -> None:
    """Verify EOS Engine ingests validated research hypotheses and updates active hypotheses."""
    eos = EOSEngine()
    hyp = Hypothesis(statement="Strategic Moat Non-Linear Scaling", domain="EOS")

    eos.ingest_validated_research(hyp)
    active = eos.active_hypotheses

    assert len(active) == 1
    assert active[0].statement == "Strategic Moat Non-Linear Scaling"


def test_eios_kernel_hypothesis_sensing_and_hawkes_anomalies() -> None:
    """Verify EIOS Kernel hypothesis registration and Hawkes intensity anomaly sensing."""
    kernel = EIOSKernel()
    hyp = Hypothesis(statement="EFE Active Sensing Bounds", domain="EIOS")

    kernel.register_research_hypothesis(hyp)
    assert len(kernel.research_hypotheses) == 1

    # Hawkes process anomaly test on low vs high event streams
    low_events = [{"event": 1}, {"event": 2}]
    low_res = kernel.sense_opportunity_anomalies(low_events)
    assert low_res["is_anomaly"] is False

    high_events = [{"event": i} for i in range(15)]
    high_res = kernel.sense_opportunity_anomalies(high_events)
    assert high_res["is_anomaly"] is True
    assert high_res["anomaly_type"] == "HIGH_FREQUENCY_OPPORTUNITY_SPIKE"


def test_code_rewrite_engine_ast_recursion_limit() -> None:
    """Verify CodeRewriteEngine verifies valid ASTs and catches excessive function recursion depth."""
    engine = CodeRewriteEngine(allowed_paths=["."])

    # Valid rewrite
    p_valid = RewriteProposal(
        target_filepath="test_module.py",
        original_snippet="x = 0",
        proposed_snippet="def add_one(val):\n    return val + 1",
        rationale="Optimization"
    )
    assert engine.verify_proposal_ast(p_valid) is True

    # Invalid rewrite (excessive recursion > 5)
    p_invalid = RewriteProposal(
        target_filepath="test_module.py",
        original_snippet="x = 0",
        proposed_snippet="def recursive_fn(val):\n    return recursive_fn(val) + recursive_fn(val) + recursive_fn(val) + recursive_fn(val) + recursive_fn(val) + recursive_fn(val)",
        rationale="Recursive rewrite test"
    )
    assert engine.verify_proposal_ast(p_invalid) is False
