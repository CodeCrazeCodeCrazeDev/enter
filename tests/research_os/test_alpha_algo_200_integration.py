# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Comprehensive integration test suite for the
200-paper quantitative research corpus (IDs 301-500) and runtime enhancements
across AEAN, EOS, EIOS, and Research OS.
"""

import os
import pytest
import yaml
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
    CodeRewriteEngine,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.ai_eos.intelligence.eos_engine import EOSEngine


def test_200_paper_corpus_yaml_integrity_and_zero_overlap():
    """Verify that the 200-paper YAML database exists, contains 200 papers, and has zero overlap."""
    yaml_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(yaml_path), f"YAML file {yaml_path} does not exist."

    with open(yaml_path, "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    papers = db.get("papers", [])
    assert len(papers) == 200, f"Expected 200 papers, found {len(papers)}"

    ids = [p["id"] for p in papers]
    assert min(ids) == 301 and max(ids) == 500, f"Expected paper IDs 301..500, got {min(ids)}..{max(ids)}"

    # Audit zero overlap against existing papers (IDs 1..300)
    existing_titles = []
    existing_dois = set()
    for old_path in ["docs/research/papers/AI_EOS_RESEARCH_DB.yaml", "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"]:
        if os.path.exists(old_path):
            with open(old_path, "r", encoding="utf-8") as f:
                old_db = yaml.safe_load(f)
            old_papers = old_db.get("papers", []) if isinstance(old_db, dict) else old_db
            for op in old_papers:
                meta = op.get("metadata", {})
                if meta.get("title"):
                    existing_titles.append(meta["title"].lower())
                if meta.get("doi"):
                    existing_dois.add(meta["doi"].lower())

    for p in papers:
        title = p["metadata"]["title"].lower()
        doi = p["metadata"]["doi"].lower()

        # Check DOI overlap
        assert doi not in existing_dois, f"DOI overlap detected for paper #{p['id']}: {doi}"

        # Check title similarity overlap
        p_tokens = set(title.split())
        for ext in existing_titles:
            ext_tokens = set(ext.split())
            score = len(p_tokens.intersection(ext_tokens)) / len(p_tokens.union(ext_tokens))
            assert score <= 0.35, f"Title overlap detected for paper #{p['id']} '{title}' matched '{ext}' score {score:.2f}"


def test_principle_registration_and_literature_review():
    """Verify registration of 200-paper corpus principles and literature review querying."""
    principles = register_200_paper_corpus_principles()
    assert len(principles) == 200, f"Expected 200 registered principles, got {len(principles)}"

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")

    assert review["domain"] == "Active Inference"
    assert review["reviewed_citations_count"] > 0
    assert "target_subsystems_impacted" in review
    assert len(review["synthesized_trends"]) >= 2


def test_eios_kernel_active_inference_sensing():
    """Verify EIOS Kernel active inference sensing and hypothesis registration."""
    kernel = EIOSKernel()
    kernel.register_research_hypothesis(hypothesis_id="hyp_301", title="Variational EFE Sensing")

    anomaly = kernel.sense_opportunity_anomalies(domain="EIOS Sensing", expected_free_energy=0.85)
    assert anomaly["status"] == "ANOMALY_TRIGGERED"
    assert anomaly["action_required"] is True

    nominal = kernel.sense_opportunity_anomalies(domain="EIOS Sensing", expected_free_energy=0.2)
    assert nominal["status"] == "NOMINAL"
    assert nominal["action_required"] is False


def test_aean_hivemind_token_bidding_for_research():
    """Verify AEAN HiveMind token bidding for research insights."""
    hive = HiveMind(token_budget=100)

    bid1 = hive.register_research_insight(task="EFE Active Sensing", priority=0.9, expected_value=1.2, token_cost=30)
    bid2 = hive.register_research_insight(task="Sycophancy-Proof Consensus", priority=0.7, expected_value=0.8, token_cost=40)

    grants = hive.arbitrate([bid1, bid2])
    assert len(grants) == 2
    assert grants[0].granted is True
    assert grants[1].granted is True


def test_eos_engine_research_ingestion():
    """Verify EOS Engine research hypothesis ingestion into opportunity graph."""
    engine = EOSEngine()
    hyp_id = uuid4()

    opp_id = engine.ingest_validated_research(
        hypothesis_id=hyp_id,
        title="Active Free Energy Strategy",
        domain="Active Inference",
        expected_yield=2.5
    )

    assert opp_id is not None
    assert len(engine.active_hypotheses) > 0


def test_code_rewrite_engine_security_verification(tmp_path):
    """Verify CodeRewriteEngine AST verification and dry run simulation."""
    test_file = tmp_path / "sample.py"
    test_file.write_text("def hello():\n    return 'world'\n", encoding="utf-8")

    engine = CodeRewriteEngine(allowed_paths=[str(tmp_path)])

    proposal = engine.propose_rewrite(
        filepath=str(test_file),
        original_snippet="return 'world'",
        proposed_snippet="return 'hello world'",
        rationale="Update greeting"
    )

    assert engine.verify_proposal_ast(proposal) is True
    assert engine.dry_run_simulation(proposal) is True
    assert engine.commit_rewrite(proposal) is True

    # Dangerous code test
    bad_proposal = engine.propose_rewrite(
        filepath=str(test_file),
        original_snippet="return 'hello world'",
        proposed_snippet="eval('import os')",
        rationale="Dangerous eval"
    )
    assert engine.verify_proposal_ast(bad_proposal) is False


def test_learnable_routing_gate_dispatcher():
    """Verify LearnableRoutingGateDispatcher active inference EFE routing."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(
        agent_id="agent_a",
        domain_specialty="Active Inference",
        cost_per_token=0.001,
        historical_success_rate=0.8,
        epistemic_curiosity=0.7
    )
    dispatcher.register_subagent(agent_a)

    routed_agent = dispatcher.route_task(task_complexity=100.0, domain="Active Inference")
    assert routed_agent == "agent_a"
