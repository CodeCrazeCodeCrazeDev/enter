# -*- coding: utf-8 -*-
"""
test_200_paper_integration.py: Cross-layer integration test suite verifying 200-paper research corpus.
Validates paper uniqueness, principle extraction, Research OS dynamic querying, and multi-subsystem state handoffs.
"""

import os
import yaml
import pytest
from apodex.ai_eos.research.integration import register_200_paper_corpus_principles
from apodex.ai_eos.research.research_os import ResearchOS


def test_200_paper_db_integrity_and_uniqueness():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    yaml_path = os.path.join(base_dir, "docs", "research", "papers", "AI_EOS_RESEARCH_DB.yaml")

    assert os.path.exists(yaml_path), f"Research DB missing at {yaml_path}"

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    papers = data.get("papers", [])
    assert len(papers) == 200, f"Expected 200 papers, found {len(papers)}"

    titles = set()
    ids = set()
    for p in papers:
        pid = p.get("id")
        title = p.get("metadata", {}).get("title")

        assert pid not in ids, f"Duplicate paper ID found: {pid}"
        assert title not in titles, f"Duplicate paper title found: {title}"

        ids.add(pid)
        titles.add(title)


def test_register_200_paper_corpus_principles():
    principles = register_200_paper_corpus_principles()
    assert len(principles) == 200, f"Expected 200 registered principles, got {len(principles)}"

    subsystems = {p["target_subsystem"] for p in principles}
    assert "AEAN" in subsystems
    assert "EOS" in subsystems
    assert "ResearchOS" in subsystems or "EIOS" in subsystems


def test_research_os_literature_review_querying():
    ros = ResearchOS()
    res = ros.conduct_literature_review("Multi-Agent Systems")

    assert res["domain"] == "Multi-Agent Systems"
    assert res["reviewed_citations_count"] > 0
    assert isinstance(res["synthesized_trends"], list)
    assert len(res["synthesized_trends"]) > 0


def test_cross_layer_hypothesis_handoff():
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Active Inference Swarm Scaling",
        description="Active inference reduces agent consensus latency.",
        null_hypothesis="Active inference has no effect on consensus latency.",
        target_metric="latency_ms"
    )

    exp = ros.create_experiment(hyp.hypothesis_id)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    updated_hyp = ros.hypotheses.get(hyp.hypothesis_id)
    assert updated_hyp.status in ["validated", "refuted"]
