# -*- coding: utf-8 -*-
"""
test_unified_cognitive_architecture_spec.py: End-to-end test suite validating
the 4-layer unified cognitive operating system specification across Layer 1 (Research OS),
Layer 2 (EIOS Kernel & EOS Engine), Layer 3 (AEAN HiveMind), and Layer 4 (APODEX WorldModel).
"""

import pytest
from unittest.mock import MagicMock
from apodex.ai_eos.research.integration import (
    ResearchToSystemBridge,
    CodeRewriteEngine,
    RewriteProposal,
    register_100_paper_alphaalgo_principles,
    register_200_paper_corpus_principles,
    register_301_400_paper_corpus_principles,
    register_401_500_paper_corpus_principles,
    register_501_600_paper_corpus_principles,
)
from apodex.ai_eos.intelligence import (
    EOSEngine,
    EntrepreneurialIntelligenceOrchestrator,
    AdvancedCausalEngine,
    ActiveInferencePlanner,
    Opportunity,
)


def test_research_to_system_bridge_active_inference_cycle():
    """Validates atomic cross-layer active inference state handoffs from Layer 1 down to Layer 4."""
    mock_ros = MagicMock()
    mock_ros.export_hypothesis_for_execution.return_value = {
        "hypothesis_id": "HYP-SPEC-2026",
        "statement": "Active Inference minimizes EFE over multi-agent task DAGs.",
        "confidence": 0.96,
        "status": "validated",
    }

    mock_eios = MagicMock()
    mock_eios.sense_opportunity_anomalies.return_value = {"anomaly_detected": False}

    mock_eos = MagicMock()

    mock_hive_mind = MagicMock()
    mock_hive_mind.bid_for_task.return_value = "Agent-Coder-01"

    mock_world_model = MagicMock()
    mock_world_model.update_belief.return_value = 0.99

    bridge = ResearchToSystemBridge(
        research_os=mock_ros,
        eios_kernel=mock_eios,
        eos_engine=mock_eos,
        hive_mind=mock_hive_mind,
        world_model=mock_world_model,
    )

    result = bridge.execute_cross_layer_active_inference_cycle("HYP-SPEC-2026")

    assert result["hypothesis_id"] == "HYP-SPEC-2026"
    assert result["layer1_status"] == "validated"
    assert result["layer3_winning_agent"] == "Agent-Coder-01"
    assert result["layer4_causal_node"] == "NODE-HYP-HYP-SPEC-2026"
    assert result["layer4_updated_belief"] == 0.99

    mock_ros.export_hypothesis_for_execution.assert_called_once_with("HYP-SPEC-2026")
    mock_eios.register_research_hypothesis.assert_called_once()
    mock_eos.ingest_validated_research.assert_called_once()
    mock_hive_mind.register_research_insight.assert_called_once()
    mock_world_model.create_node.assert_called_once()
    mock_world_model.update_belief.assert_called_once()


def test_hawkes_ast_recursion_depth_verification():
    """Validates that Hawkes point process limits on function recursion depth veto unsafe rewrites."""
    engine = CodeRewriteEngine(allowed_paths=["/tmp"])

    safe_snippet = """
def safe_calc(n):
    if n <= 1:
        return 1
    return safe_calc(n - 1)
"""
    proposal_safe = RewriteProposal(
        target_filepath="/tmp/safe.py",
        original_snippet="",
        proposed_snippet=safe_snippet,
        rationale="Safe single recursive call",
    )
    assert engine.verify_proposal_ast(proposal_safe) is True

    unsafe_snippet = """
def unsafe_calc(n):
    if n <= 1:
        return 1
    return unsafe_calc(n-1) + unsafe_calc(n-2) + unsafe_calc(n-3) + unsafe_calc(n-4)
"""
    proposal_unsafe = RewriteProposal(
        target_filepath="/tmp/unsafe.py",
        original_snippet="",
        proposed_snippet=unsafe_snippet,
        rationale="Unsafe excessive recursive calls",
    )
    assert engine.verify_proposal_ast(proposal_unsafe) is False


def test_principle_registration_registers():
    """Verifies principle registration functions for papers 1-600."""
    p100 = register_100_paper_alphaalgo_principles()
    p200 = register_200_paper_corpus_principles()
    p300 = register_301_400_paper_corpus_principles()
    p400 = register_401_500_paper_corpus_principles()
    p500 = register_501_600_paper_corpus_principles()

    assert len(p100) > 0
    assert len(p200) > 0
    assert len(p300) > 0
    assert len(p400) > 0
    assert len(p500) > 0


def test_computational_architecture_orchestration():
    """Validates the 14-layer computational architecture orchestrator."""
    causal_engine = AdvancedCausalEngine()
    planner = ActiveInferencePlanner(curiosity_weight=1.2)
    orchestrator = EntrepreneurialIntelligenceOrchestrator(
        causal_engine=causal_engine, planner=planner
    )

    opp = orchestrator.ingest_signal(
        {
            "title": "Autonomous AI Engineering Platform",
            "domain": "software_engineering",
            "variables": ["code_quality", "developer_velocity"],
            "causal_edges": [("code_quality", "developer_velocity")],
            "coefficients": {"code_quality->developer_velocity": 0.85},
            "prior_entropy": 1.2,
            "post_entropy_simulated": 0.3,
            "success_probability": 0.88,
        }
    )

    result = orchestrator.execute_orchestrated_pipeline()
    assert result["status"] == "executed"
    assert result["selected_opportunity"] == "Autonomous AI Engineering Platform"
    assert "propagated_state" in result
