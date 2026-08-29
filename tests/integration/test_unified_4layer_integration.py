"""
Integration Test Suite for Unified 4-Layer Cognitive Operating System Architecture.

Verifies end-to-end non-cyclic cross-layer execution flow:
Layer 1 (Research OS) -> Layer 2 (EIOS Kernel & EOS Engine) -> Layer 3 (AEAN Planner/Swarm) -> Layer 4 (APODEX Skill Registry & World Model).
"""

import uuid
import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, VentureCell
from apodex.skills.registry import SkillRegistry
from apodex.world_model.world_model import WorldModel, CausalNode


@pytest.mark.asyncio
async def test_unified_4layer_cross_layer_flow():
    # 1. Layer 1: Research OS conducts literature review & registers hypothesis
    ros = ResearchOS()
    literature = ros.conduct_literature_review("active_inference")
    assert literature["reviewed_citations_count"] > 0
    assert len(literature["synthesized_trends"]) > 0

    registered_hypo = ros.register_hypothesis(
        title="Active Inference EFE Capital Allocation",
        description="Active inference EFE routing reduces capital allocation uncertainty by 30%",
        null_hypothesis="Active inference EFE routing has no effect on capital uncertainty",
        target_metric="uncertainty_reduction",
        significance_alpha=0.05
    )
    assert registered_hypo.title == "Active Inference EFE Capital Allocation"
    assert registered_hypo.target_metric == "uncertainty_reduction"

    # 2. Layer 2: EIOS Kernel & EOS Engine DAG compilation and continuous sensing cycle
    kernel = EIOSKernel()
    node = ExecutionNode(
        node_id="n1",
        name="sense_step",
        action_type="sense_active_inference",
        payload={"hypo_id": str(registered_hypo.hypothesis_id)}
    )
    dag = ExecutionDAG(id="dag_001", nodes={"n1": node})
    success = await kernel.execute_dag(dag)
    assert success is True

    eos = EOSEngine()
    cell = VentureCell(cell_id=uuid.uuid4(), name="Test Venture", namespace="fintech")
    sensing_result = eos.run_continuous_sensing_cycle(cells=[cell], total_budget_cents=10000)
    assert sensing_result is not None

    # 3. Layer 3: AEAN Cognitive Swarm / Skill resolution
    registry = SkillRegistry()
    skill = registry.get_skill("competitive_analysis")
    assert skill is not None

    # 4. Layer 4: APODEX Platform & World Model state update
    wm = WorldModel()
    causal_node = CausalNode(
        node_id="hypo_node_1",
        node_type="hypothesis",
        properties={"label": registered_hypo.description, "prior_probability": 0.85}
    )
    wm.add_node(causal_node)

    retrieved = wm.nodes.get("hypo_node_1")
    assert retrieved is not None
    assert retrieved.node_type == "hypothesis"
    assert retrieved.properties["label"] == registered_hypo.description
    assert retrieved.properties["prior_probability"] == 0.85
