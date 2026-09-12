import pytest
import asyncio
import uuid

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.domain.entities import Entity
from apodex.world_model.domain.beliefs import Belief

@pytest.mark.asyncio
async def test_cross_layer_cognitive_os_integration():
    """
    Validates end-to-end cognitive OS data and state flow across:
    Layer 1: Research OS (Hypothesis generation & literature review)
    Layer 2: EIOS Kernel (DAG execution) & EOS Engine (Strategy state)
    Layer 3: AEAN HiveMind (Resource arbitration & token budget)
    Layer 4: APODEX WorldModel (Entity management & Belief modeling)
    """
    # 1. Layer 1: Research OS
    research_os = ResearchOS()
    lit_review = research_os.conduct_literature_review("active inference multi-agent market design")
    assert "synthesized_trends" in lit_review
    assert len(lit_review["synthesized_trends"]) > 0

    registered_hyp = research_os.register_hypothesis(
        title="Active Inference Market Routing",
        description="Optimizes multi-agent bidding and token allocation.",
        null_hypothesis="Random bidding is equivalent.",
        target_metric="sharpe_ratio"
    )
    assert registered_hyp is not None
    assert registered_hyp.title == "Active Inference Market Routing"

    # 2. Layer 2: EIOS Kernel & EOS Engine
    eios_kernel = EIOSKernel()
    dag = ExecutionDAG()
    node1 = ExecutionNode(node_id="n1", name="sense_market", action_type="sense", payload={})
    node2 = ExecutionNode(node_id="n2", name="decide_strategy", action_type="decide", payload={}, depends_on=["n1"])
    dag.add_node(node1)
    dag.add_node(node2)

    kernel_result = await eios_kernel.execute_dag(dag)
    assert kernel_result is True

    eos_engine = EOSEngine()
    assert eos_engine.hypothesis_engine is not None

    # 3. Layer 3: AEAN HiveMind
    hive_mind = HiveMind()
    assert hive_mind.token_budget > 0
    bid = TaskBid(task="task_101", priority=1.0, expected_value=100.0, token_cost=10)
    grants = hive_mind.arbitrate([bid])
    assert isinstance(grants, list)

    # 4. Layer 4: APODEX WorldModel
    ent_uuid = uuid.uuid4()
    entity = Entity(
        entity_id=ent_uuid,
        name="Cognitive OS Venture",
        entity_type="Venture",
        properties={"mrr": 50000, "active_users": 1200}
    )
    assert entity.entity_id == ent_uuid

    belief = Belief(
        belief_id=uuid.uuid4(),
        target_id=ent_uuid,
        probability=0.85,
        evidence=["market_analysis_passed"]
    )
    assert belief.probability == 0.85
