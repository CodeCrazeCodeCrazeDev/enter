# -*- coding: utf-8 -*-
"""
test_cognitive_os_subsystems.py: End-to-end integration test suite validating
joint interactions across Research OS, EIOS Kernel, EOS Engine, AEAN Hive Mind,
and APODEX World Model.
"""

from __future__ import annotations
import pytest
import asyncio
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel
from apodex.world_model.domain.beliefs import Belief
from apodex.world_model.domain.entities import Entity
from apodex.skills.registry import SkillRegistry
from apodex.skills.models import BusinessSkill


# =====================================================================
# 1. Research OS Scientific Hypothesis & Experiment Lifecycle Test
# =====================================================================

def test_research_os_hypothesis_lifecycle():
    ros = ResearchOS()

    # 1. Register hypothesis
    hyp = ros.register_hypothesis(
        title="GRPO Optimization Yields 25% Latency Reduction",
        description="Applying Group Relative Policy Optimization reduces inference latency without accuracy loss.",
        null_hypothesis="H0: Mean latency reduction <= 0%",
        target_metric="latency_reduction_pct",
        significance_alpha=0.05
    )
    assert hyp.status == "registered"

    # 2. Design experiment
    design = ros.design_experiment(hyp.hypothesis_id)
    assert design["recommended_sample_size"] > 0
    assert design["statistical_power"] == 0.80

    # 3. Create and execute experiment simulation with positive ground truth yield
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert completed_exp.is_statistically_significant is True
    assert completed_exp.p_value < 0.05
    assert hyp.status == "validated"


# =====================================================================
# 2. EIOS Kernel & Active Inference DAG Execution Test
# =====================================================================

@pytest.mark.asyncio
async def test_eios_kernel_and_dag_execution():
    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag(
        goal="Scale autonomous AI product pipeline in SMB market",
        target_budget_usd=15000
    )
    assert len(dag.nodes) == 4

    kernel = EIOSKernel()
    success = await kernel.execute_dag(dag)
    assert success is True


# =====================================================================
# 3. EOS Decision Engine Research Ingestion Test
# =====================================================================

def test_eos_engine_research_ingestion():
    eos = EOSEngine()
    initial_count = len(eos.active_hypotheses) if hasattr(eos, "active_hypotheses") else 0

    research_payload = {
        "hypothesis_id": str(uuid4()),
        "title": "Usage-Based Pricing Increases Net Revenue Retention",
        "target_metric": "nrr_percentage",
        "status": "validated"
    }

    eos.ingest_validated_research(research_payload)
    if hasattr(eos, "active_hypotheses"):
        assert len(eos.active_hypotheses) == initial_count + 1


# =====================================================================
# 4. AEAN Hive Mind Token Bidding & Research Registration Test
# =====================================================================

def test_aean_hive_mind_coordination():
    hive = HiveMind()

    # Register research insight from Research OS
    hive.register_research_insight(
        topic="GRPO Latency Optimization",
        insight_summary="Validated 25% inference acceleration in sandbox benchmark.",
        confidence=0.95
    )
    assert "GRPO Latency Optimization" in hive.research_registry

    # Multi-agent task bidding
    bid1 = TaskBid(task="task_opt_1", priority=0.8, expected_value=0.5, token_cost=10)
    bid2 = TaskBid(task="task_opt_1", priority=0.9, expected_value=0.8, token_cost=10)

    hive.submit_bid(bid1)
    hive.submit_bid(bid2)

    winner = hive.resolve_auction("task_opt_1")
    assert winner is not None
    assert winner.priority in [0.8, 0.9]


# =====================================================================
# 5. APODEX World Model & Skill Execution Flywheel Test
# =====================================================================

def test_apodex_world_model_and_skills():
    wm = WorldModel()

    # Create entity and register causal node in World Model
    entity = Entity(
        name="Apodex Growth Unit",
        entity_type="ORGANIZATION",
        properties={"status": "scaling", "mrr_cents": 12000_00}
    )
    wm.add_causal_relation(source=entity.name, target="revenue_growth", effect_size=0.85)
    wm.update_bayesian_belief(belief_key="growth_trajectory", new_evidence_weight=0.9)

    assert "growth_trajectory" in wm.beliefs
    assert wm.beliefs["growth_trajectory"]["probability"] > 0.5

    # Skill Registry & Verification
    registry = SkillRegistry()
    skill_keys = registry.list_skills()
    assert len(skill_keys) >= 10


# =====================================================================
# 6. Joint End-to-End Cross-Layer ResearchToSystemBridge Test
# =====================================================================

def test_cross_layer_system_bridge():
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind()
    wm = WorldModel()

    # Create 4-layer bridge
    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive,
        world_model=wm
    )

    # 1. Layer 1: Register and validate hypothesis
    hyp = ros.register_hypothesis(
        title="Predictive Churn Interventions Reduce CAC",
        description="Autonomous customer risk scoring prevents monthly subscription churn.",
        null_hypothesis="H0: Churn reduction <= 0%",
        target_metric="churn_reduction"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=42)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.0)

    # 2. Bridge handoff across Layer 1 -> Layer 2 -> Layer 3 -> Layer 4
    record = bridge.bridge_validated_hypothesis(hyp.hypothesis_id)

    assert record["status"] == "validated"
    assert "Layer2_EIOS_Kernel" in record["layers_notified"]
    assert "Layer2_EOS_Engine" in record["layers_notified"]
    assert "Layer3_AEAN_HiveMind" in record["layers_notified"]
    assert "Layer4_APODEX_WorldModel" in record["layers_notified"]
    assert len(bridge.bridge_history) == 1
