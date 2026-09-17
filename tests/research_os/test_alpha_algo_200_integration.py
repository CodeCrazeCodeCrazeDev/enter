# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite for the 200-paper
AlphaAlgo research corpus (IDs 301-500), principle registration, literature review synthesis,
and runtime enhancements across ResearchOS, EIOSKernel, EOSEngine, and HiveMind.
"""

import os
import yaml
import pytest
from apodex.ai_eos.research.integration import register_301_500_paper_corpus_principles
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid


def test_200_paper_corpus_zero_overlap():
    """Verify 200 papers in ALPHA_ALGO_200_NEW_RESEARCH.yaml have zero title overlap with papers 1-300."""
    db1_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    db2_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    db3_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"

    assert os.path.exists(db3_path), f"{db3_path} does not exist."

    existing_titles = set()
    if os.path.exists(db1_path):
        with open(db1_path, "r", encoding="utf-8") as f:
            db1 = yaml.safe_load(f)
        for p in db1.get("papers", []):
            existing_titles.add(p["metadata"]["title"].lower())

    if os.path.exists(db2_path):
        with open(db2_path, "r", encoding="utf-8") as f:
            db2 = yaml.safe_load(f)
        for p in db2.get("papers", []):
            existing_titles.add(p["metadata"]["title"].lower())

    with open(db3_path, "r", encoding="utf-8") as f:
        db3 = yaml.safe_load(f)

    new_papers = db3.get("papers", [])
    assert len(new_papers) == 200, f"Expected 200 new papers, found {len(new_papers)}"

    # Audit IDs and titles
    paper_ids = [p["id"] for p in new_papers]
    assert min(paper_ids) == 301
    assert max(paper_ids) == 500

    for p in new_papers:
        title = p["metadata"]["title"].lower()

        # Check Jaccard similarity against existing 300 papers
        p_tokens = set(title.split())
        for ext in existing_titles:
            ext_tokens = set(ext.split())
            intersection = p_tokens.intersection(ext_tokens)
            union = p_tokens.union(ext_tokens)
            score = len(intersection) / len(union) if union else 0.0
            assert score <= 0.35, f"High similarity ({score:.2f}) found between new title '{title}' and existing '{ext}'"


def test_301_500_principles_registration():
    """Verify register_301_500_paper_corpus_principles returns 5 principle domains."""
    principles = register_301_500_paper_corpus_principles()
    assert len(principles) == 5
    assert "hawkes_order_flow_bounds" in principles
    assert "active_inference_efe_routing" in principles
    assert "advantage_weighted_dpo_alignment" in principles
    assert "sycophancy_robust_consensus" in principles
    assert "island_map_elites_evolution" in principles


def test_research_os_literature_review_synthesis():
    """Verify ResearchOS literature review queries registered 301-500 principles."""
    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")

    assert review["domain"] == "Active Inference"
    assert review["reviewed_citations_count"] == 200
    assert len(review["synthesized_trends"]) > 0
    assert any("Active Inference" in t for t in review["synthesized_trends"])


def test_cross_subsystem_active_inference_handoff():
    """Verify end-to-end handoff across ResearchOS, EIOSKernel, EOSEngine, and HiveMind."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind(token_budget=100)

    # 1. Register and run experiment on ResearchOS
    hyp = ros.register_hypothesis(
        title="Hawkes Self-Exciting Jump Arbitrage",
        description="Hawkes jump processes reduce order flow prediction error",
        null_hypothesis="Hawkes jump processes have no effect",
        target_metric="sharpe_ratio",
        significance_alpha=0.05
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    # Confirm hypothesis validated
    validated_hyp = ros.hypotheses.get(hyp.hypothesis_id)
    assert validated_hyp.status == "validated"

    # 2. Export validated hypothesis to EIOS Kernel & sense anomalies
    exported_data = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id)
    kernel.register_research_hypothesis(exported_data)
    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) == 1
    assert anomalies[0]["title"] == "Hawkes Self-Exciting Jump Arbitrage"

    # 3. Promote hypothesis to EOS Engine
    ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    assert len(eos.active_hypotheses) == 1
    assert eos.active_hypotheses[0].title == "Hawkes Self-Exciting Jump Arbitrage"

    # 4. Register research insight into HiveMind and arbitrate token bids
    hive.register_research_insight({
        "title": validated_hyp.title,
        "effect_size": exp.effect_size,
        "dsr": exp.deflated_sharpe_ratio
    })
    assert len(hive.research_insights) == 1

    bids = [
        TaskBid(task="Execute Hawkes Arbitrage Strategy", priority=0.9, expected_value=1.5, token_cost=30, epistemic_curiosity=0.8),
        TaskBid(task="Routine Maintenance", priority=0.2, expected_value=0.1, token_cost=10, epistemic_curiosity=0.1)
    ]
    grants = hive.arbitrate(bids)
    assert len(grants) == 2
    assert grants[0].task == "Execute Hawkes Arbitrage Strategy"
    assert grants[0].granted is True
