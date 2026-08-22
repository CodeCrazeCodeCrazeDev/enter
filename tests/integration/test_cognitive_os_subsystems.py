"""End-to-end integration tests validating joint behavior across all 5 cognitive subsystems:
1. ResearchOS (Scientific Hypothesis & Validation)
2. EIOS Kernel (Active Inference, DAG Execution, Compilers)
3. EOS Engine (14-Layer Computational Architecture & Continuous Sensing)
4. AEAN (Autonomous Execution & Event Sourcing Lifecycle Engine)
5. APODEX (World Model & Causal Graph)
"""

from __future__ import annotations

import pytest
import asyncio
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler, HierarchicalActiveInference, RecursivePlanner
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, VentureCell
from apodex.aean.core import DecisionLifecycleManager, EventSourcingManager
from apodex.world_model.world_model import WorldModel, CausalNode, RelationEdge


def test_research_os_to_eios_bridge():
    """Test ResearchOS hypothesis registration, simulation, and bridge export to EIOS Kernel."""
    ros = ResearchOS()

    hyp = ros.register_hypothesis(
        title="Active Inference Pricing Optimization",
        description="Dynamic pricing reduces CAC and lowers Variational Free Energy",
        null_hypothesis="Pricing adjustments have no effect on CAC",
        target_metric="cac_reduction",
        significance_alpha=0.05
    )

    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert completed_exp.is_statistically_significant is True
    assert hyp.status == "validated"

    # Export payload for EIOS Kernel
    kernel_payload = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id)
    assert kernel_payload["source_subsystem"] == "ResearchOS"
    assert kernel_payload["hypothesis_id"] == str(hyp.hypothesis_id)
    assert "cac_reduction" in kernel_payload["recommended_action"]


def test_research_os_to_eos_promotion():
    """Test ResearchOS hypothesis promotion to EOS decision engine."""
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="AI-Driven Lead Generation",
        description="Autonomous agents increase outbound Conversion Rate by 40%",
        null_hypothesis="Conversion rates remain unchanged",
        target_metric="conversion_rate",
        significance_alpha=0.05
    )

    eos_proposal = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, commercial_value=0.95)
    assert eos_proposal["hypothesis_id"] == str(hyp.hypothesis_id)
    assert eos_proposal["commercial_score"] > 0.5
    assert eos_proposal["approved_for_eos_pipeline"] is True


@pytest.mark.asyncio
async def test_eios_kernel_and_compiler_workflow():
    """Test EIOS Compiler translating high-level business goals to DAG and Kernel executing it."""
    compiler = EntrepreneurialCompiler()
    kernel = EIOSKernel()

    dag = compiler.compile_goal_to_dag(goal="Scale Enterprise AI ARR to $10M", target_budget_usd=100000)
    assert len(dag.nodes) == 4

    success = await kernel.execute_dag(dag)
    assert success is True
    assert all(node.status == "COMPLETED" for node in dag.nodes.values())


def test_eos_engine_sensing_cycle():
    """Test EOS Engine continuous sensing cycle across multi-timescale loops."""
    eos = EOSEngine()
    cells = [VentureCell(name="Cell_01", namespace="ns_01")]
    result = eos.run_continuous_sensing_cycle(cells=cells, total_budget_cents=50000_00)

    assert "allocated_budgets" in result
    assert "world_state" in result


def test_aean_governance_and_proposal_cycle():
    """Test AEAN DecisionLifecycleManager proposing decisions and advancing state."""
    event_mgr = EventSourcingManager()
    dlm = DecisionLifecycleManager(event_manager=event_mgr)

    proposal = dlm.propose(
        decision="Deploy Zero-Touch Self-Healing Micro-VM",
        supporting_hypotheses=["hyp_01"],
        proposed_by="research_agent_01"
    )

    assert proposal.status == "proposed"
    assert proposal.decision == "Deploy Zero-Touch Self-Healing Micro-VM"

    # Advance state from proposed -> simulating -> approved
    proposal.status = "simulating"
    dlm.approve(proposal.id, approved_by="gov_chair")
    updated_prop = dlm.proposals[proposal.id]
    assert updated_prop.status == "approved"


def test_apodex_world_model_causal_graph():
    """Test APODEX World Model registering causal nodes and relation edges."""
    wm = WorldModel()

    node_a = CausalNode(node_id="research_hypothesis", node_type="HypothesisNode", properties={"uncertainty": 0.1})
    node_b = CausalNode(node_id="eos_strategy", node_type="StrategyNode", properties={"uncertainty": 0.2})
    node_c = CausalNode(node_id="aean_execution", node_type="ExecutionNode", properties={"uncertainty": 0.15})

    wm.add_node(node_a)
    wm.add_node(node_b)
    wm.add_node(node_c)

    edge_1 = RelationEdge(source_id="research_hypothesis", target_id="eos_strategy", weight=0.9, relation_type="causal_driver")
    edge_2 = RelationEdge(source_id="eos_strategy", target_id="aean_execution", weight=0.85, relation_type="execution_dependency")

    wm.add_relation(edge_1)
    wm.add_relation(edge_2)

    assert len(wm.nodes) == 3


@pytest.mark.asyncio
async def test_full_cross_subsystem_joint_pipeline():
    """Test complete end-to-end cross-subsystem cognitive pipeline across all 5 layers."""
    # Step 1: ResearchOS discovers and validates a scientific hypothesis
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Self-Evolving Cognitive Prompting",
        description="Genetic prompt mutation reduces LLM token overhead by 35%",
        null_hypothesis="Mutation has no impact on token efficiency",
        target_metric="token_efficiency"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=99)
    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.0)
    assert completed_exp.is_statistically_significant is True

    # Step 2: Export from ResearchOS to EIOS Kernel & EOS Decision Engine
    kernel_payload = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id)
    eos_proposal = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, commercial_value=0.92)
    assert eos_proposal["approved_for_eos_pipeline"] is True

    # Step 3: EIOS Kernel compiles goal into DAG and executes
    compiler = EntrepreneurialCompiler()
    kernel = EIOSKernel()
    dag = compiler.compile_goal_to_dag(goal=kernel_payload["recommended_action"], target_budget_usd=50000)
    dag_success = await kernel.execute_dag(dag)
    assert dag_success is True

    # Step 4: EOS Engine continuous sensing cycle
    eos = EOSEngine()
    cells = [VentureCell(name="Venture_Alpha", namespace="ns_alpha")]
    sensing_res = eos.run_continuous_sensing_cycle(cells=cells, total_budget_cents=100000_00)
    assert "allocated_budgets" in sensing_res

    # Step 5: AEAN DecisionLifecycleManager proposes decision and approves
    event_mgr = EventSourcingManager()
    dlm = DecisionLifecycleManager(event_manager=event_mgr)
    prop = dlm.propose(
        decision=f"Deploy {hyp.title}",
        supporting_hypotheses=[str(hyp.hypothesis_id)],
        proposed_by="research_os_bridge"
    )
    prop.status = "simulating"
    dlm.approve(prop.id, approved_by="super_node")
    updated_prop = dlm.proposals[prop.id]
    assert updated_prop.status == "approved"

    # Step 6: APODEX World Model records the outcome and causal relationships
    wm = WorldModel()
    wm.add_node(CausalNode(node_id=str(hyp.hypothesis_id), node_type="HypothesisNode", properties={"title": hyp.title}))
    wm.add_node(CausalNode(node_id="aean_deployment", node_type="ExecutionNode", properties={"status": "APPROVED"}))
    wm.add_relation(RelationEdge(source_id=str(hyp.hypothesis_id), target_id="aean_deployment", weight=0.95, relation_type="provenance"))

    assert len(wm.nodes) == 2
