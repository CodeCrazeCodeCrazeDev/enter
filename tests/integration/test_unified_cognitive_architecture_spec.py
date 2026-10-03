"""
Integration test suite verifying the Unified 4-Layer Cognitive Operating System Architecture.
Layer 1: Research OS (Research)
Layer 2: EIOS / EOS (Execution & Orchestration)
Layer 3: AEAN (Cognitive Intelligence & Multi-Agent Swarm)
Layer 4: APODEX (Decision & Execution Platform / World Model)
"""

import pytest
import asyncio
from uuid import uuid4
from apodex.ai_eos.research.research_os import ResearchOS, Hypothesis
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel, CausalNode
from apodex.ai_eos.research.integration import ResearchToSystemBridge


@pytest.mark.asyncio
async def test_unified_4layer_cognitive_architecture_spec_flow():
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
        world_model=world_model,
    )

    # 2. Layer 1: Research OS creates and validates hypothesis
    hyp = research_os.register_hypothesis(
        title="Active Inference Expected Free Energy Bounds",
        description="EFE minimization reduces task routing ambiguity.",
        null_hypothesis="EFE minimization does not alter task routing ambiguity.",
        target_metric="cost_variance",
        significance_alpha=0.05,
    )
    hyp.status = "validated"
    hyp_uuid = hyp.hypothesis_id
    assert research_os.hypotheses.get(hyp_uuid) is not None

    # 3. Handshake Layer 1 -> Layer 2 via Bridge
    bridge_state = bridge.handshake_and_sync()
    assert bridge_state["validated_hypotheses_count"] >= 1
    assert hyp_uuid in eios_kernel.research_hypotheses

    # 4. Layer 2: EIOS Kernel active inference sensing
    efe_vector = eios_kernel.sense_opportunity_anomalies(
        observation={"market_anomaly": True, "ambiguity": 0.15}
    )
    assert "efe_score" in efe_vector
    assert efe_vector["efe_score"] > 0.0

    # 5. Layer 2 -> Layer 3: Task publication to AEAN HiveMind
    insight_id = hive_mind.register_research_insight(
        title="Optimize Task Routing DAG",
        extracted_principle="Minimizing expected free energy reduces cost variance.",
        source_paper="Active Inference for Agentic Systems (2025)",
        confidence_score=0.92,
    )
    assert insight_id in hive_mind.insights

    # 6. Layer 3: Agent bidding and allocation
    bid_result = hive_mind.submit_agent_bid(
        insight_id=insight_id,
        agent_id="executive-agent-01",
        stake_tokens=150.0,
        strategy_proposal="Execute adaptive routing DAG optimization",
    )
    assert bid_result["status"] == "bid_accepted"

    # 7. Layer 3 -> Layer 4: World Model Causal Node creation & Bayesian Belief update
    node = CausalNode(
        node_id="node-spec-101",
        label="Active Inference Routing DAG",
        node_type="action",
        description="Active inference guided task node",
    )
    world_model.create_node(node)
    assert "node-spec-101" in world_model.nodes

    world_model.update_belief(
        hypothesis_id=str(hyp_uuid),
        evidence_signal=0.88,
        source_agent="executive-agent-01",
    )
    assert str(hyp_uuid) in world_model.beliefs
    assert world_model.beliefs[str(hyp_uuid)].probability > 0.5
