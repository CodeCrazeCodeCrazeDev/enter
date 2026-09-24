# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite for the 200-paper research corpus (301-500).
Validates 500-paper total corpus uniqueness, principle registration, literature review querying,
and active inference cross-subsystem integrations across AEAN, EOS, EIOS, and Research OS.
"""

import os
import pytest
import yaml
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_301_500_paper_corpus_principles,
    ALPHAALGO_301_500_PRINCIPLES,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    TrajectoryStep,
    RewriteProposal
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_200_paper_corpus_yaml_integrity_and_uniqueness():
    """Verify that ALPHA_ALGO_200_NEW_RESEARCH.yaml exists, contains 200 papers, and has 0 duplicates against 1-300."""
    yaml_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(yaml_path), "ALPHA_ALGO_200_NEW_RESEARCH.yaml must exist"

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    papers = data.get("papers", [])
    assert len(papers) == 200, f"Expected exactly 200 papers in 200-paper database, got {len(papers)}"

    # Check ID boundaries
    paper_ids = [p["id"] for p in papers]
    assert paper_ids[0] == 301 and paper_ids[-1] == 500, "Paper IDs must span strictly 301 to 500"

    # Cross-check titles and DOIs against existing DBs
    existing_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]
    existing_titles = set()
    existing_dois = set()

    for path in existing_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                d = yaml.safe_load(f)
                for p in d.get("papers", []):
                    existing_titles.add(p["metadata"]["title"].lower())
                    if p["metadata"].get("doi"):
                        existing_dois.add(p["metadata"]["doi"].strip().lower())

    for p in papers:
        title = p["metadata"]["title"].lower()
        doi = p["metadata"].get("doi", "").strip().lower()
        assert title not in existing_titles, f"Duplicate title found across corpus: '{title}'"
        if doi:
            assert doi not in existing_dois, f"Duplicate DOI found across corpus: '{doi}'"


def test_principle_registration_and_literature_review():
    """Verify registration of 200-paper principles and ResearchOS literature review integration."""
    principles = register_301_500_paper_corpus_principles()
    assert len(principles) == 200, "Should register 200 principles"

    ros = ResearchOS()
    # Test querying by target subsystem
    review_aean = ros.conduct_literature_review("AEAN")
    assert review_aean["reviewed_citations_count"] > 0
    assert len(review_aean["matching_principles"]) > 0

    review_eos = ros.conduct_literature_review("EOS")
    assert review_eos["reviewed_citations_count"] > 0

    review_eios = ros.conduct_literature_review("EIOS")
    assert review_eios["reviewed_citations_count"] > 0


def test_subsystem_integrations_and_runtime_components():
    """Verify runtime integration components derived from extracted principles."""
    # 1. AEAN Active Inference Shepherd Routing Gate
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    agent_a = SpecializedAgentProfile(agent_id="agent_aean_1", domain_specialty="AEAN", cost_per_token=0.001, historical_success_rate=0.8)
    agent_b = SpecializedAgentProfile(agent_id="agent_eos_2", domain_specialty="EOS", cost_per_token=0.002, historical_success_rate=0.6)
    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    routed = dispatcher.route_task(task_complexity=100.0, domain="AEAN")
    assert routed == "agent_aean_1"

    # 2. SFT/DPO Preference Collection (GRPO)
    collector = SFTPreferenceCollector(discount_factor=0.95)
    steps_a = [TrajectoryStep(action="action_1", predicted_expectation=0.5, actual_outcome=0.9, reward=0.8)]
    steps_b = [TrajectoryStep(action="action_2", predicted_expectation=0.5, actual_outcome=0.2, reward=0.2)]
    dpo_pair = collector.compile_dpo_preference_pair("Optimize AEAN Shepherd route", steps_a, steps_b)
    assert dpo_pair["margin"] > 0
    assert "action_1" in dpo_pair["chosen"]

    # 3. Code Rewrite AST Verification Safety Veto
    rewrite_engine = CodeRewriteEngine(allowed_paths=["./apodex"])
    proposal_safe = rewrite_engine.propose_rewrite("apodex/dummy.py", "a = 1", "a = 2", "Update constant")
    assert rewrite_engine.verify_proposal_ast(proposal_safe) is True

    proposal_unsafe = RewriteProposal(
        target_filepath=os.path.abspath("apodex/dummy.py"),
        original_snippet="a = 1",
        proposed_snippet="eval('import os')",
        rationale="Dangerous code"
    )
    assert rewrite_engine.verify_proposal_ast(proposal_unsafe) is False
