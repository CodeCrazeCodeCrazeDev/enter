# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite for the 200 new research papers
(IDs 301-500) and cross-subsystem enhancements across ResearchOS, EIOS Kernel, EOS Engine, and AEAN HiveMind.
"""

import os
import yaml
import pytest
from uuid import uuid4

from apodex.ai_eos.research.integration import register_301_500_paper_corpus_principles, ALPHAALGO_301_500_PRINCIPLES
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid


def test_200_paper_corpus_integrity():
    """Verify papers 301-500 exist, have 200 records, and zero overlap with papers 1-300."""
    yaml_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(yaml_path), f"File {yaml_path} does not exist."

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    papers = data.get("papers", [])
    assert len(papers) == 200, f"Expected 200 papers in ALPHA_ALGO_200_NEW_RESEARCH.yaml, got {len(papers)}"

    # Check ID range 301-500
    paper_ids = [p["id"] for p in papers]
    assert paper_ids[0] == 301
    assert paper_ids[-1] == 500

    # Cross-verify zero title overlap with existing databases
    existing_titles = set()
    for ext_path in [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]:
        if os.path.exists(ext_path):
            with open(ext_path, "r", encoding="utf-8") as f:
                db_data = yaml.safe_load(f)
            for p in db_data.get("papers", []):
                existing_titles.add(p["metadata"]["title"].strip().lower())

    for p in papers:
        t = p["metadata"]["title"].strip().lower()
        assert t not in existing_titles, f"Duplicate paper title detected in corpus: '{t}'"


def test_principle_registration_301_500():
    """Verify principles extracted from papers 301-500 are registered correctly."""
    principles = register_301_500_paper_corpus_principles()
    assert len(principles) == 4
    assert principles == ALPHAALGO_301_500_PRINCIPLES
    for p in principles:
        assert "principle_id" in p
        assert "title" in p
        assert "target_subsystem" in p
        assert "description" in p


def test_research_os_literature_review_querying():
    """Verify ResearchOS queries principles 301-500 during conduct_literature_review."""
    ros = ResearchOS()
    review = ros.conduct_literature_review("EIOS Kernel")

    assert review["domain"] == "EIOS Kernel"
    assert review["reviewed_citations_count"] == 200
    assert "principles_queried" in review
    assert len(review["principles_queried"]) > 0


def test_cross_layer_state_handoff_integration():
    """Test full cross-layer state handoff: ResearchOS -> EIOS Kernel -> EOS Engine -> AEAN HiveMind."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind(token_budget=100)

    # 1. Register and validate hypothesis in Research OS
    hyp = ros.register_hypothesis(
        title="Active Inference Free Energy Minimization in Agent Swarms",
        description="Minimizing expected free energy improves task allocation under uncertainty.",
        null_hypothesis="Free energy minimization has no effect on task allocation.",
        target_metric="active_inference",
        significance_alpha=0.05
    )

    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert hyp.status == "validated"
    assert completed_exp.is_statistically_significant is True

    # 2. Export validated hypothesis to EIOS Kernel
    exported_kernel = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, kernel)
    assert exported_kernel is True
    assert len(kernel.research_hypotheses_registry) == 1

    anomalies = kernel.sense_opportunity_anomalies(epistemic_threshold=0.5)
    assert len(anomalies) == 1
    assert anomalies[0]["anomaly_type"] == "HIGH_EPISTEMIC_VALUE_OPPORTUNITY"

    # 3. Promote validated hypothesis to EOS Engine
    promoted_eos = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    assert promoted_eos is True
    assert len(eos.active_hypotheses) == 1

    # 4. Register research insight in AEAN HiveMind and arbitrate token bids
    bid = hive.register_research_insight({
        "hypothesis_id": str(hyp.hypothesis_id),
        "title": hyp.title,
        "domain": hyp.domain
    })

    grants = hive.arbitrate([bid])
    assert len(grants) == 1
    assert grants[0].granted is True
