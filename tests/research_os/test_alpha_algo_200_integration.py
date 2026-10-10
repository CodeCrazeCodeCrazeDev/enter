# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite for the 200-paper quantitative research corpus
(IDs 301-500) and its cross-layer integration into AEAN, EOS, EIOS, Research OS, and APODEX WorldModel.
"""

import os
import yaml
import pytest
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
    ALPHAALGO_200_PRINCIPLES,
    ResearchToSystemBridge,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel


def test_200_paper_yaml_corpus_integrity_and_zero_overlap():
    """Validates 200-paper YAML database schema integrity and zero overlap against papers 1-300."""
    yaml_200_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(yaml_200_path), f"Corpus YAML file missing at {yaml_200_path}"

    with open(yaml_200_path, "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    papers = db.get("papers", [])
    assert len(papers) == 200, f"Expected exactly 200 papers, got {len(papers)}"

    # Verify ID range 301-500
    paper_ids = [p["id"] for p in papers]
    assert min(paper_ids) == 301 and max(paper_ids) == 500

    # Load previous paper databases to verify 100% zero overlap
    prev_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]
    prev_titles = set()
    prev_dois = set()

    for path in prev_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                prev_db = yaml.safe_load(f)
            for p in prev_db.get("papers", []):
                meta = p.get("metadata", {})
                if meta.get("title"):
                    prev_titles.add(meta["title"].lower().strip())
                if meta.get("doi"):
                    prev_dois.add(meta["doi"].lower().strip())

    for p in papers:
        meta = p["metadata"]
        title = meta["title"].lower().strip()
        doi = meta["doi"].lower().strip()

        assert title not in prev_titles, f"Duplicate title detected: '{meta['title']}'"
        assert doi not in prev_dois, f"Duplicate DOI detected: '{meta['doi']}'"


def test_200_paper_principles_registration():
    """Verifies principles registration and data structure of extracted transferable principles."""
    principles = register_200_paper_corpus_principles()
    assert len(principles) >= 10
    assert len(ALPHAALGO_200_PRINCIPLES) == len(principles)

    for p in principles:
        assert "principle_id" in p
        assert "paper_id" in p
        assert 301 <= p["paper_id"] <= 500
        assert "category" in p
        assert "target_subsystem" in p
        assert "extracted_principle" in p


def test_research_os_literature_review_queries_200_corpus():
    """Verifies that Research OS literature review queries the 200-paper principles corpus."""
    ros = ResearchOS()
    result = ros.conduct_literature_review("Multi-Agent Systems")

    assert result["domain"] == "Multi-Agent Systems"
    assert result["reviewed_citations_count"] >= 14
    assert len(result["extracted_principles"]) > 0
    assert any("AEAN HiveMind" in p["target_subsystem"] for p in result["extracted_principles"])


def test_research_to_system_bridge_cross_layer_handoff():
    """Verifies closed-loop active inference state handoffs across Research OS, EIOS, EOS, AEAN, and WorldModel."""
    ros = ResearchOS()
    eios = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind()
    wm = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=eios,
        eos_engine=eos,
        hive_mind=hive,
        world_model=wm
    )

    hyp = ros.register_hypothesis(
        title="Decentralized Task Bidding and Active Inference Sensing",
        description="Active inference EFE bidding balances pragmatic and epistemic rewards in swarms.",
        null_hypothesis="EFE bidding yields equivalent outcome to random task allocation.",
        target_metric="active_inference_efficiency",
        significance_alpha=0.05
    )

    # Simulate validation
    hyp.status = "validated"

    handoff_result = bridge.handoff_validated_hypothesis(hyp)

    assert handoff_result["title"] == "Decentralized Task Bidding and Active Inference Sensing"
    assert "EOSEngine" in handoff_result["subsystems_notified"]
    assert "EIOSKernel" in handoff_result["subsystems_notified"]
    assert "HiveMind" in handoff_result["subsystems_notified"]
    assert "WorldModel" in handoff_result["subsystems_notified"]
    assert len(bridge.handoff_history) == 1


def test_learnable_routing_gate_efe_dispatch():
    """Verifies Active Inference Expected Free Energy (EFE) task dispatch in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=100.0)

    agent_a = SpecializedAgentProfile(
        agent_id="agent_quant",
        domain_specialty="Quantitative Finance",
        cost_per_token=0.01,
        historical_success_rate=0.8,
        epistemic_curiosity=0.6
    )
    agent_b = SpecializedAgentProfile(
        agent_id="agent_swarms",
        domain_specialty="Multi-Agent Systems",
        cost_per_token=0.005,
        historical_success_rate=0.7,
        epistemic_curiosity=0.9
    )

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    selected = dispatcher.route_task(task_complexity=10.0, domain="Multi-Agent Systems")
    assert selected == "agent_swarms"

    # Update metrics
    dispatcher.update_routing_parameters(agent_id="agent_swarms", success=True, cost_incurred=0.05)
    assert dispatcher.agents["agent_swarms"].historical_success_rate > 0.7
