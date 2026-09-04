# -*- coding: utf-8 -*-
"""
test_unified_4layer_integration.py

Comprehensive end-to-end integration test suite for the Unified 4-Layer Cognitive Operating System:
- Layer 1: Research OS (Scientific literature & hypothesis validation)
- Layer 2: EIOS Kernel & EOS Engine (Active Inference sensing & strategic compilation)
- Layer 3: AEAN HiveMind (Multi-agent token bidding & swarm orchestration)
- Layer 4: APODEX WorldModel & SkillRegistry (Causal state updates & protocol execution)
"""

import pytest
from unittest.mock import MagicMock
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel
from apodex.skills.registry import SkillRegistry
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_unified_4layer_active_inference_handoff():
    """Validates explicit end-to-end active inference state handoffs across all 4 layers."""
    # 1. Initialize layer components
    research_os = ResearchOS()
    eios_kernel = EIOSKernel()
    eos_engine = EOSEngine()
    hive_mind = HiveMind()
    world_model = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=research_os,
        eios_kernel=eios_kernel,
        eos_engine=eos_engine,
        hive_mind=hive_mind,
        world_model=world_model
    )

    # 2. Execute active inference state handoff from Layer 1 hypothesis
    scientific_hypothesis = {
        "id": "HYP_ACTIVE_INFERENCE_2026",
        "title": "Non-Gaussian Hawkes Process Task Congestion Mitigation",
        "confidence": 0.94
    }

    log = bridge.execute_cross_layer_handoff(scientific_hypothesis)

    # 3. Assert state synchronization across all 4 layers
    assert log["layer1_research"] == "VALIDATED"
    assert log["layer2_eios_sensed"] is True
    assert log["layer3_aean_bidded"] is True
    assert log["layer4_apodex_updated"] is True

    # 4. Verify Layer 2 EIOS sensing over registered hypothesis
    anomalies = eios_kernel.sense_opportunity_anomalies({"volatility": 0.2, "market_demand": 0.85})
    assert len(anomalies) >= 1
    assert anomalies[0]["hypothesis_id"] == "HYP_ACTIVE_INFERENCE_2026"


def test_compiler_to_hivemind_execution_flow():
    """Validates translation from strategic compiler goal into executable DAG and HiveMind bidding."""
    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag("Autonomous SaaS Product Launch", target_budget_usd=10000)

    assert len(dag.nodes) == 4
    executable_nodes = dag.get_executable_nodes()
    assert len(executable_nodes) == 1
    assert executable_nodes[0].name == "Conjoint Market Research"

    # HiveMind bidding token arbitration
    hive_mind = HiveMind(token_budget=50)
    bids = [
        TaskBid(task=executable_nodes[0].name, priority=0.9, expected_value=1.5, token_cost=20),
        TaskBid(task="Background Maintenance", priority=0.2, expected_value=0.1, token_cost=40)
    ]

    grants = hive_mind.arbitrate(bids)
    assert len(grants) == 2
    assert grants[0].task == "Conjoint Market Research"
    assert grants[0].granted is True


def test_skill_registry_prepopulated_skills():
    """Validates that SkillRegistry contains pre-populated strategic/operational skills."""
    registry = SkillRegistry()
    skills = registry.list_skills()
    assert len(skills) >= 60

    # Test skill lookup capability
    skill = registry.get_skill("strategic_planning")
    assert skill is not None
