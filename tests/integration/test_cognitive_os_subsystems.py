import pytest
import asyncio
from apodex.ai_eos.research.research_os import ResearchOS, Hypothesis
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.skills.models import CostTier
from apodex.skills.registry import SkillRegistry
from apodex.skills.runner import SkillRunner
from apodex.skills.implementation import register_all_custom_executors
from apodex.world_model.world_model import WorldModel, CausalNode


def test_layer1_research_os_flow():
    """Verify Layer 1: Research OS literature discovery and hypothesis evaluation."""
    ros = ResearchOS()
    literature = ros.conduct_literature_review("active inference portfolio optimization")
    assert literature is not None
    assert "synthesized_trends" in literature
    assert literature["reviewed_citations_count"] > 0

    hyp = ros.register_hypothesis(
        title="Active Inference Drawdown Reduction",
        description="Active inference reduces portfolio drawdowns during regime shifts",
        null_hypothesis="Active inference shows no drawdown reduction over static rebalancing",
        target_metric="max_drawdown_pct",
        significance_alpha=0.05
    )
    assert hyp is not None
    exp = ros.design_experiment(hypothesis_id=hyp.hypothesis_id)
    assert exp is not None


def test_layer2_aean_hivemind_flow():
    """Verify Layer 2: AEAN HiveMind swarm arbitration and token budgeting."""
    hive = HiveMind(token_budget=50000)
    assert hive.token_budget == 50000

    bids = [
        TaskBid(task="quant_allocation", priority=0.85, expected_value=100.0, token_cost=500),
        TaskBid(task="risk_hedging", priority=0.90, expected_value=150.0, token_cost=600)
    ]
    grants = hive.arbitrate(bids)
    assert grants is not None
    assert len(grants) > 0


@pytest.mark.asyncio
async def test_layer3_eios_kernel_flow():
    """Verify Layer 3: EIOS Kernel DAG compilation and execution."""
    kernel = EIOSKernel()
    dag = ExecutionDAG()
    node1 = ExecutionNode(
        node_id="step1",
        name="sense_market",
        action_type="sense",
        payload={"sector": "fintech"}
    )
    node2 = ExecutionNode(
        node_id="step2",
        name="allocate_capital",
        action_type="allocate",
        payload={"amount_usd": 10000},
        depends_on=["step1"]
    )
    dag.add_node(node1)
    dag.add_node(node2)

    success = await kernel.execute_dag(dag)
    assert success is True


def test_layer4_apodex_execution_flow():
    """Verify Layer 4: APODEX Skill Execution and World Model state updates."""
    registry = SkillRegistry()
    assert len(registry.list_skills()) >= 60

    runner = SkillRunner()
    register_all_custom_executors(runner)

    skill = registry.get_skill("opportunity_evaluation_frameworks")
    assert skill is not None

    exec_res = runner.execute_skill(
        skill=skill,
        tenant_id="tenant_01",
        venture_id="venture_01",
        input_payload={"niche_name": "SaaS Document Search"},
        tier=CostTier.CHEAP
    )
    assert exec_res is not None
    assert "status" in exec_res or "output_payload" in exec_res

    wm = WorldModel()
    c_node = CausalNode(node_id="n1", label="MarketTrend", node_type="state", value={"trend": "bullish"})
    wm.add_node(c_node)
    assert "n1" in wm.nodes


@pytest.mark.asyncio
async def test_end_to_end_cognitive_os_subsystems_cycle():
    """Verify full end-to-end 4-layer Cognitive OS cycle across Research OS, AEAN, EIOS, and APODEX."""
    # 1. Layer 1 Discovery
    ros = ResearchOS()
    lit = ros.conduct_literature_review("causal inference active learning")
    trend = lit["synthesized_trends"][0] if lit.get("synthesized_trends") else "Active Inference"

    # 2. Layer 2 Cognitive Arbitration
    hive = HiveMind()
    bids = [
        TaskBid(task=f"apply_{trend}", priority=0.92, expected_value=200.0, token_cost=800)
    ]
    grants = hive.arbitrate(bids)
    assert len(grants) > 0

    # 3. Layer 3 Orchestration Execution DAG
    kernel = EIOSKernel()
    dag = ExecutionDAG()
    dag.add_node(ExecutionNode(
        node_id="e2e_node",
        name="execute_orchestration",
        action_type="orchestrate",
        payload={"grant": grants[0].task}
    ))
    dag_success = await kernel.execute_dag(dag)
    assert dag_success is True

    # 4. Layer 4 APODEX Skill Execution
    registry = SkillRegistry()
    runner = SkillRunner()
    register_all_custom_executors(runner)

    skill = registry.get_skill("business_model_design")
    exec_res = runner.execute_skill(
        skill=skill,
        tenant_id="e2e_tenant",
        venture_id="e2e_venture",
        input_payload={"available_surplus_cents": 500000},
        tier=CostTier.CHEAP
    )
    assert exec_res is not None
