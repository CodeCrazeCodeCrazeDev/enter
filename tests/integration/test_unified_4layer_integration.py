"""End-to-End Cross-Layer Integration Test Suite for the Unified Cognitive Operating System.

Validates joint multi-paradigm state transitions across:
- Layer 1 (Research OS: Hypothesis registration, walk-forward simulation, DSR validation, research bridge state)
- Layer 2 (EIOS Kernel & EOS Engine: Active Inference sensing, opportunity DAG, coupled business loops, capital allocation)
- Layer 3 (AEAN HiveMind & Routing Gates: EFE learnable routing, token bidding, agent task dispatching, advantage preference collection)
- Layer 4 (APODEX WorldModel & Execution: Domain entities, causal graphs, recursive Bayesian belief updates, and execution feedback loops)
"""

from __future__ import annotations

import math
import pytest
from uuid import uuid4
from datetime import datetime, timezone

from apodex.research_os.models import Hypothesis as ROSHypothesis, ValidationReport
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import (
    ResearchToSystemBridge,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    SFTPreferenceCollector,
    TrajectoryStep,
)
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionNode, ExecutionDAG
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.ai_eos.domain.models import VentureCell, Evidence, ExecutionStatus
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel, CausalNode, RelationEdge
from apodex.world_model.domain.entities import Entity
from apodex.world_model.domain.beliefs import Belief


@pytest.mark.asyncio
async def test_layer1_to_layer2_hypothesis_handshake_and_active_inference():
    """Test Layer 1 Research OS hypothesis validation and handshake to Layer 2 EIOS Kernel."""
    ros = ResearchOS()
    bridge = ResearchToSystemBridge()

    # 1. Layer 1: Register scientific hypothesis
    hyp = ros.register_hypothesis(
        title="Microstructure Order Flow Imbalance Signal",
        description="Predictive edge derived from order book pressure imbalances.",
        null_hypothesis="Order book imbalance mean returns <= 0",
        target_metric="SharpeRatio",
        significance_alpha=0.05,
    )
    assert hyp.title == "Microstructure Order Flow Imbalance Signal"

    # 2. Execute experiment simulation
    exp = ros.create_experiment(hypothesis_id=hyp.hypothesis_id, seed=123)
    completed_exp = ros.execute_experiment_simulation(experiment_id=exp.experiment_id, ground_truth_yield=1.8)

    assert completed_exp.status == ExecutionStatus.COMPLETED
    assert completed_exp.deflated_sharpe_ratio > 0

    # 3. Handshake from Research OS to System Bridge
    handshake = bridge.handshake_hypothesis_to_execution(
        hypothesis_id=str(hyp.hypothesis_id),
        title=hyp.title,
        deflated_sharpe_ratio=completed_exp.deflated_sharpe_ratio,
        p_value=completed_exp.p_value,
        economic_rationale="MICROSTRUCTURE_IMBALANCE",
    )

    assert handshake["hypothesis_id"] == str(hyp.hypothesis_id)
    assert "handshake_status" in handshake

    # 4. Serialize bridge state
    serialized = bridge.serialize_bridge_state()
    assert serialized["total_handshakes"] == 1
    assert "promoted_count" in serialized


@pytest.mark.asyncio
async def test_layer2_eios_kernel_and_eos_engine_cycle():
    """Test Layer 2 EIOS Kernel DAG execution and EOS Engine capital allocation sensing cycle."""
    # 1. Initialize EIOS Kernel & compile DAG
    kernel = EIOSKernel()
    dag = ExecutionDAG()

    node1 = ExecutionNode(name="Conjoint Market Research", action_type="research_only")
    node2 = ExecutionNode(name="Feasibility Financial Model", action_type="research_only", depends_on=[node1.node_id])
    dag.add_node(node1)
    dag.add_node(node2)

    success = await kernel.execute_dag(dag)
    assert success is True
    assert node1.status == "COMPLETED"
    assert node2.status == "COMPLETED"

    # 2. Initialize EOS Engine
    eos = EOSEngine()
    v1 = VentureCell(cell_id=uuid4(), name="AI_Doc_Parser", namespace="ns_doc_parser", expected_free_energy=2.5, risk=0.2)
    v2 = VentureCell(cell_id=uuid4(), name="Market_Intelligence_Api", namespace="ns_market_api", expected_free_energy=1.8, risk=0.4)

    cycle_out = eos.run_continuous_sensing_cycle(cells=[v1, v2], total_budget_cents=100000)
    assert "allocated_budgets" in cycle_out
    assert len(cycle_out["allocated_budgets"]) == 2
    assert cycle_out["venture_portfolio_cents"] > 0


def test_layer3_aean_hivemind_and_learnable_routing_gate():
    """Test Layer 3 AEAN HiveMind bidding registry and learnable routing gate task dispatching."""
    # 1. Initialize HiveMind and submit bids
    hive = HiveMind(token_budget=100)
    bids = [
        TaskBid(task="demand_sensing", priority=0.9, expected_value=1.5, token_cost=30),
        TaskBid(task="narrative_engineering", priority=0.7, expected_value=1.0, token_cost=20),
    ]
    grants = hive.arbitrate(bids)
    assert len(grants) == 2
    assert grants[0].granted is True

    # 2. Initialize Learnable Routing Gate
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=100.0)
    dispatcher.register_subagent(
        SpecializedAgentProfile(
            agent_id="agent_ade",
            domain_specialty="demand_sensing",
            cost_per_token=0.001,
            historical_success_rate=0.85,
            epistemic_curiosity=0.6,
        )
    )
    dispatcher.register_subagent(
        SpecializedAgentProfile(
            agent_id="agent_are",
            domain_specialty="revenue_engine",
            cost_per_token=0.002,
            historical_success_rate=0.90,
            epistemic_curiosity=0.4,
        )
    )

    selected_agent = dispatcher.route_task(task_complexity=100.0, domain="demand_sensing")
    assert selected_agent == "agent_ade"

    # Update routing gate parameters
    dispatcher.update_routing_parameters(agent_id="agent_ade", success=True, cost_incurred=0.10)
    assert dispatcher.agents["agent_ade"].historical_success_rate > 0.80


def test_layer4_apodex_worldmodel_and_trajectory_preference():
    """Test Layer 4 APODEX WorldModel entity, causal graph, belief updating, and preference collection."""
    # 1. Initialize APODEX WorldModel
    wm = WorldModel()

    # Add causal nodes and relation edge
    c1 = CausalNode(node_id="demand_signal", node_type="SIGNAL", properties={"name": "High Pain Point Signal"})
    c2 = CausalNode(node_id="conversion_uplift", node_type="METRIC", properties={"name": "Conversion Lift"})
    wm.add_node(c1)
    wm.add_node(c2)

    edge = RelationEdge(source_id="demand_signal", target_id="conversion_uplift", relation_type="CAUSES", weight=0.85)
    wm.add_relation(edge)

    assert len(wm.nodes) == 2
    assert len(wm.edges) == 1

    # 2. Update recursive Bayesian belief over domain entity
    entity = Entity(name="SaaS Venture Alpha", entity_type="ORGANIZATION")
    belief = Belief(target_id=entity.entity_id, probability=0.80)
    belief.update_confidence(likelihood=0.90, prior_probability=0.80)
    assert belief.probability > 0.80

    # 3. Collect SFT/DPO trajectory preferences for self-referential evolution
    collector = SFTPreferenceCollector(discount_factor=0.95)
    run_a = [
        TrajectoryStep(action="sense_demand", predicted_expectation=0.5, actual_outcome=0.8, reward=0.8),
        TrajectoryStep(action="deploy_capital", predicted_expectation=0.7, actual_outcome=0.9, reward=0.9),
    ]
    run_b = [
        TrajectoryStep(action="sense_demand", predicted_expectation=0.5, actual_outcome=0.4, reward=0.4),
        TrajectoryStep(action="deploy_capital", predicted_expectation=0.7, actual_outcome=0.3, reward=0.3),
    ]

    pref_pair = collector.compile_dpo_preference_pair(
        prompt="Execute market expansion cycle",
        steps_run_a=run_a,
        steps_run_b=run_b,
    )
    assert "chosen" in pref_pair
    assert "rejected" in pref_pair
    assert pref_pair["margin"] > 0.0


def test_unified_4layer_end_to_end_workflow():
    """Validates the full joint 4-layer lifecycle execution chain in sequence."""
    # Layer 1: Research OS Pre-registers and validates hypothesis
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Predictive Demand Sensing Model",
        description="Active inference model over customer search volume.",
        null_hypothesis="Search volume uplift <= 0",
        target_metric="ConversionLift",
    )
    exp = ros.create_experiment(hypothesis_id=hyp.hypothesis_id, seed=42)
    completed_exp = ros.execute_experiment_simulation(experiment_id=exp.experiment_id, ground_truth_yield=2.0)

    # Layer 2: Bridge promotion to EOS Engine
    bridge = ResearchToSystemBridge()
    handshake = bridge.handshake_hypothesis_to_execution(
        hypothesis_id=str(hyp.hypothesis_id),
        title=hyp.title,
        deflated_sharpe_ratio=completed_exp.deflated_sharpe_ratio,
        p_value=completed_exp.p_value,
        economic_rationale="ACTIVE_INFERENCE_DEMAND",
    )

    eos = EOSEngine()
    v1 = VentureCell(
        cell_id=uuid4(),
        name=hyp.title,
        namespace="ns_predictive_demand",
        expected_free_energy=handshake["deflated_sharpe_ratio"],
        risk=0.1,
    )
    sensing_out = eos.run_continuous_sensing_cycle(cells=[v1], total_budget_cents=50000)

    # Layer 3: AEAN HiveMind bidding & Routing
    hive = HiveMind(token_budget=50)
    grants = hive.arbitrate([TaskBid(task="predictive_demand", priority=0.8, expected_value=1.2, token_cost=20)])

    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=50.0)
    dispatcher.register_subagent(
        SpecializedAgentProfile(agent_id="agent_ade", domain_specialty="demand_sensing", cost_per_token=0.001)
    )
    chosen_agent = dispatcher.route_task(task_complexity=10.0, domain="demand_sensing")

    # Layer 4: WorldModel belief update & Trajectory preference record
    wm = WorldModel()
    cnode = CausalNode(node_id=chosen_agent, node_type="AGENT", properties={"name": hyp.title})
    wm.add_node(cnode)

    assert completed_exp.status == ExecutionStatus.COMPLETED
    assert handshake["hypothesis_id"] == str(hyp.hypothesis_id)
    assert len(sensing_out["allocated_budgets"]) == 1
    assert len(wm.nodes) == 1
    assert len(grants) == 1
