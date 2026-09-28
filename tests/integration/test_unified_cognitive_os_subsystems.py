"""Integration test suite validating closed-loop interactions across:
- Research OS (Hypothesis registration & statistical validation)
- EIOS (Kernel execution DAGs & Active Inference)
- EOS (Engine continuous sensing & VentureCell allocation)
- AEAN (HiveMind Agent token bidding & arbitration)
- APODEX (WorldModel causal graph & relation traversal)
"""

import pytest
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.domain.models import ExecutionStatus, VentureCell
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel, CausalNode, RelationEdge


def test_research_os_hypothesis_validation_flow():
    """Verify Research OS hypothesis registration, experiment creation, and walk-forward simulation."""
    ros = ResearchOS()

    # 1. Register hypothesis
    hyp = ros.register_hypothesis(
        title="EFE Optimization",
        description="Optimizing active inference reduces Expected Free Energy in agent tasks",
        null_hypothesis="No significant reduction in EFE",
        target_metric="efe_reduction",
        significance_alpha=0.05,
    )
    assert hyp.hypothesis_id is not None
    assert hyp.status == "registered"

    # 2. Create sandbox experiment
    exp = ros.create_experiment(hypothesis_id=hyp.hypothesis_id, seed=123)
    assert exp.experiment_id is not None
    assert exp.status == ExecutionStatus.QUEUED

    # 3. Execute experiment simulation with high ground truth yield
    completed_exp = ros.execute_experiment_simulation(
        experiment_id=exp.experiment_id,
        ground_truth_yield=2.5,
    )

    assert completed_exp.status == ExecutionStatus.COMPLETED
    assert completed_exp.p_value is not None
    assert completed_exp.p_value < 0.05
    assert completed_exp.is_statistically_significant is True
    assert hyp.status == "validated"


@pytest.mark.asyncio
async def test_eios_kernel_and_eos_engine_execution():
    """Verify EIOS Kernel DAG execution and EOS Engine continuous sensing cycle."""
    kernel = EIOSKernel()
    eos = EOSEngine()

    # 1. EIOS Kernel DAG execution
    dag = ExecutionDAG()
    node = ExecutionNode(
        name="Market Sensing Task",
        action_type="sensing",
        payload={"domain": "ai_agents"},
    )
    dag.add_node(node)

    success = await kernel.execute_dag(dag)
    assert success is True
    assert node.status == "COMPLETED"

    # 2. EOS Engine continuous sensing & capital allocation cycle
    cell = VentureCell(
        cell_id=uuid4(),
        name="Cell Alpha",
        namespace="cell_alpha_ns",
        uncertainty=0.3,
        expected_free_energy=1.2,
        capital_allocation_score=0.8,
        risk=0.2,
    )

    cycle_results = eos.run_continuous_sensing_cycle(
        cells=[cell],
        total_budget_cents=1_000_000,
    )

    assert "world_state" in cycle_results
    assert "market_uncertainty" in cycle_results
    assert "allocated_budgets" in cycle_results
    assert cell.cell_id in cycle_results["allocated_budgets"]
    assert cycle_results["allocated_budgets"][cell.cell_id] > 0


def test_aean_hivemind_bidding_and_apodex_world_model():
    """Verify AEAN HiveMind agent token bidding arbitration and APODEX WorldModel causal graph tracing."""
    # 1. AEAN HiveMind token budget arbitration
    hive_mind = HiveMind(token_budget=100)

    bids = [
        TaskBid(task="market_research", priority=0.9, expected_value=0.8, token_cost=30),
        TaskBid(task="ad_campaign", priority=0.4, expected_value=0.3, token_cost=80),
    ]

    grants = hive_mind.arbitrate(bids)
    assert len(grants) == 2

    granted_map = hive_mind.granted_tasks(grants)
    assert granted_map["market_research"] is True
    assert granted_map["ad_campaign"] is False

    # 2. APODEX WorldModel causal graph and relation path traversal
    world_model = WorldModel()

    node1 = CausalNode(
        node_id="hyp_001",
        node_type="hypothesis",
        properties={"title": "EFE Reduction"},
    )
    node2 = CausalNode(
        node_id="act_001",
        node_type="action",
        properties={"title": "Execute Campaign"},
    )

    world_model.add_node(node1)
    world_model.add_node(node2)

    edge = RelationEdge(
        source_id="hyp_001",
        target_id="act_001",
        relation_type="triggers",
        weight=0.95,
    )
    world_model.add_relation(edge)

    path = world_model.find_path("hyp_001", "act_001")
    assert path is not None
    assert path == ["hyp_001", "act_001"]
