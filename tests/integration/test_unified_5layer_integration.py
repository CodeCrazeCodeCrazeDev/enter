"""Comprehensive 5-Layer Unified Cognitive System Integration Test Suite.
Validates end-to-end joint workflows and active inference state propagation across:
  1. Research OS (Hypothesis validation & literature synthesis)
  2. EIOS Kernel (DAG execution & anomaly sensing)
  3. EOS Engine (Capital allocation & hypothesis ingestion)
  4. AEAN HiveMind (Token bidding & agent resource arbitration)
  5. APODEX WorldModel & Cognitive Brain (Entity updating & Bayesian belief propagation)
"""

from __future__ import annotations

import pytest
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler, ExecutionDAG, ExecutionNode
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.ai_eos.domain.models import VentureCell
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.domain.entities import Entity
from apodex.world_model.domain.beliefs import Belief
from apodex.ai_eos.research.integration import ResearchToSystemBridge


@pytest.mark.asyncio
async def test_end_to_end_research_to_system_bridge_active_inference_cycle():
    # 1. Initialize Subsystems
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive_mind = HiveMind(token_budget=100)

    # 2. Register Hypothesis in Layer 1 Research OS
    hyp = ros.register_hypothesis(
        title="Autonomous Active Inference Monetization Strategy",
        description="Active inference EFE optimization increases Venture LTV:CAC by >30%",
        null_hypothesis="Active inference EFE optimization has no effect on Venture LTV:CAC",
        target_metric="LTV_CAC_Ratio",
        significance_alpha=0.05
    )

    # 3. Instantiate Bridge and Execute State Handoff
    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive_mind
    )

    res = bridge.process_and_propagate_hypothesis(hypothesis_id=hyp.hypothesis_id, ground_truth_yield=3.2)

    # 4. Verify Layer 1 Research OS outputs
    assert res["is_significant"] is True
    assert res["p_value"] < 0.05
    assert res["effect_size"] > 0

    # 5. Verify Layer 2 EIOS Kernel & EOS Engine state
    assert len(kernel.registered_research_hypotheses) == 1
    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) == 1
    assert anomalies[0]["anomaly_type"] == "HIGH_CONFIDENCE_RESEARCH_INSIGHT"

    assert len(eos.active_hypotheses) == 1
    eos_hyp = eos.active_hypotheses[0]
    assert eos_hyp.title == "Autonomous Active Inference Monetization Strategy"

    # 6. Verify Layer 3 AEAN HiveMind token bidding
    assert res["hive_mind_task_bid"] == "execute_insight_Autonomous Active Inference Monetization Strategy"

    # Arbitrate bids in HiveMind
    bids = [
        TaskBid(task=res["hive_mind_task_bid"], priority=0.95, expected_value=3.2, token_cost=20),
        TaskBid(task="routine_maintenance", priority=0.2, expected_value=0.5, token_cost=10)
    ]
    grants = hive_mind.arbitrate(bids)
    granted_map = hive_mind.granted_tasks(grants)
    assert granted_map[res["hive_mind_task_bid"]] is True

    # 7. Execute continuous sensing loop in EOS Engine
    cell1 = VentureCell(cell_id=uuid4(), namespace="ActiveInferenceCell", name="ActiveInferenceCell", capital_allocation_score=0.85)
    cycle_res = eos.run_continuous_sensing_cycle(cells=[cell1], total_budget_cents=100000_00)
    assert cycle_res["market_uncertainty"] >= 0.0
    assert cell1.allocated_capital_cents > 0

    # 8. Verify Layer 4 WorldModel Domain Entities and Belief Updates
    entity = Entity(name="Active Inference Strategy", entity_type="TECHNOLOGY")
    entity.update_property("validated_p_value", res["p_value"])
    assert entity.properties["validated_p_value"] == res["p_value"]

    belief = Belief(target_id=entity.entity_id, probability=0.5)
    belief.update_confidence(likelihood=0.9, prior_probability=0.5)
    assert belief.probability > 0.5


@pytest.mark.asyncio
async def test_eios_kernel_dag_execution_with_research_nodes():
    kernel = EIOSKernel()
    compiler = EntrepreneurialCompiler()

    dag = compiler.compile_goal_to_dag(
        goal="Scale Research OS and AEAN Autonomous Agents",
        target_budget_usd=50000
    )

    success = await kernel.execute_dag(dag)
    assert success is True
    assert all(node.status == "COMPLETED" for node in dag.nodes.values())
