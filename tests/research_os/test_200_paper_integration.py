# -*- coding: utf-8 -*-
"""
test_200_paper_integration.py: Integration test suite verifying 200-paper corpus integrity,
principle registration, ResearchOS literature review querying, and cross-layer state handoffs
across ResearchOS, EIOS Kernel, EOS Engine, and AEAN HiveMind.
"""

import pytest
import yaml
from uuid import uuid4

from apodex.ai_eos.research.integration import register_200_paper_corpus_principles
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.aean.coordination.hive_mind import HiveMind


def test_200_paper_corpus_integrity():
    """Verify that AI_EOS_RESEARCH_DB.yaml contains exactly 200 unique papers with no duplicates."""
    with open("docs/research/papers/AI_EOS_RESEARCH_DB.yaml", "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    papers = db.get("papers", [])
    assert len(papers) == 200, f"Expected 200 papers, found {len(papers)}"

    titles = set()
    for p in papers:
        title = p["metadata"]["title"].strip().lower()
        assert title not in titles, f"Duplicate paper title detected: {title}"
        titles.add(title)


def test_registered_principles_and_literature_review():
    """Verify registration of 200-paper corpus principles and dynamic ResearchOS querying."""
    principles = register_200_paper_corpus_principles()
    assert "multi_agent_systems" in principles
    assert "active_inference" in principles

    ros = ResearchOS()
    review = ros.conduct_literature_review("multi_agent_systems")
    assert review["domain"] == "multi_agent_systems"
    assert len(review["matching_principles"]) > 0
    assert any("Awesome-Agent-Papers" in trend for trend in review["synthesized_trends"])


def test_cross_layer_state_handoffs():
    """Verify active inference state handoffs across ResearchOS -> EIOS Kernel -> EOS Engine -> AEAN HiveMind."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind(token_budget=50)

    # 1. Register and validate hypothesis in Research OS
    hyp = ros.register_hypothesis(
        title="Active Inference Swarm Arbitration",
        description="Active inference EFE scoring improves multi-agent task arbitration efficiency.",
        null_hypothesis="No efficiency gain",
        target_metric="task_throughput"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    # Simulate experiment yielding statistically significant results
    validated_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)
    assert hyp.status == "validated"

    # 2. Export validated hypothesis to EIOS Kernel for sensing
    exported_kernel = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, kernel)
    assert exported_kernel is True
    assert len(kernel.research_hypotheses) == 1
    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) == 1
    assert anomalies[0]["opportunity_flag"] is True

    # 3. Promote validated hypothesis to EOS Engine strategy
    promoted_eos = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    assert promoted_eos is True
    assert len(eos.active_hypotheses) >= 1

    # 4. Register scientific insight into AEAN HiveMind for token bidding
    bid = hive.register_research_insight("Active Inference Swarm Arbitration", priority=0.9, expected_value=0.8, token_cost=15)
    grants = hive.arbitrate([bid])
    assert len(grants) == 1
    assert grants[0].granted is True
