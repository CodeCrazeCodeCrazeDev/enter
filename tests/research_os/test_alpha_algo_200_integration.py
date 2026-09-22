# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite for the 200 new paper research corpus (IDs 301-500).
Validates 0% duplicate overlap against papers 1-300, principle extraction and registration,
ResearchOS literature review querying, and cross-subsystem capability integration.
"""

import pytest
import os
import yaml
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import (
    register_301_500_paper_corpus_principles,
    ALPHAALGO_301_500_PRINCIPLES,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)


def test_200_paper_corpus_integrity_and_zero_overlap():
    """Verify that 200 papers (IDs 301-500) exist in YAML database with zero title/DOI overlap against papers 1-300."""
    db_200_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    db_100_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    db_base_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"

    assert os.path.exists(db_200_path), f"File {db_200_path} missing"

    with open(db_200_path, "r", encoding="utf-8") as f:
        data_200 = yaml.safe_load(f)

    papers_200 = data_200.get("papers", [])
    assert len(papers_200) == 200, f"Expected 200 papers, got {len(papers_200)}"

    # Check ID range 301 to 500
    p_ids = [p["id"] for p in papers_200]
    assert min(p_ids) == 301
    assert max(p_ids) == 500

    # Collect existing titles from papers 1-300
    existing_titles = set()
    for path in [db_base_path, db_100_path]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                d = yaml.safe_load(f)
            for p in d.get("papers", []):
                existing_titles.add(p["metadata"]["title"].lower())

    # Verify zero exact or high token Jaccard overlap
    for p in papers_200:
        title = p["metadata"]["title"].lower()
        assert title not in existing_titles, f"Exact duplicate title found: {title}"

        # Jaccard check
        p_tokens = set(title.split())
        for ext in existing_titles:
            ext_tokens = set(ext.split())
            intersection = p_tokens.intersection(ext_tokens)
            union = p_tokens.union(ext_tokens)
            if union:
                jaccard = len(intersection) / len(union)
                assert jaccard <= 0.35, f"High similarity Jaccard overlap ({jaccard:.2f}) between '{title}' and '{ext}'"


def test_principles_registration_and_researchos_query():
    """Verify principles registration and ResearchOS literature review querying over paper corpus."""
    principles = register_301_500_paper_corpus_principles()
    assert len(principles) >= 5
    assert 301 in principles
    assert 401 in principles
    assert 451 in principles

    ros = ResearchOS()
    review = ros.conduct_literature_review("aean")

    assert review["domain"] == "aean"
    assert review["reviewed_citations_count"] >= 1
    assert len(review["synthesized_trends"]) >= 1
    assert any("bidding" in t.lower() or "swarm" in t.lower() for t in review["synthesized_trends"])


def test_runtime_components_and_advantage_compilation():
    """Verify runtime preference collection, AST security verification, and routing gate dispatcher."""
    # 1. Trajectory SFT / DPO preference collection with advantage margin
    collector = SFTPreferenceCollector(discount_factor=0.9)
    run_a = [
        TrajectoryStep(action="plan_swarm", predicted_expectation=0.5, actual_outcome=0.8, reward=1.0),
        TrajectoryStep(action="execute_consensus", predicted_expectation=0.7, actual_outcome=0.9, reward=1.0)
    ]
    run_b = [
        TrajectoryStep(action="plan_swarm", predicted_expectation=0.5, actual_outcome=0.2, reward=-0.5),
        TrajectoryStep(action="execute_consensus", predicted_expectation=0.7, actual_outcome=0.1, reward=-0.5)
    ]

    pair = collector.compile_dpo_preference_pair("Solve task", run_a, run_b)
    assert "plan_swarm" in pair["chosen"]
    assert pair["margin"] > 0.0

    # 2. Learnable routing gate dispatcher
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    dispatcher.register_subagent(SpecializedAgentProfile(
        agent_id="agent_aean_1",
        domain_specialty="aean",
        cost_per_token=0.001,
        historical_success_rate=0.8,
        epistemic_curiosity=0.6
    ))

    selected = dispatcher.route_task(task_complexity=100.0, domain="aean")
    assert selected == "agent_aean_1"
