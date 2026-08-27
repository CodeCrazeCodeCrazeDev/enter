"""
Integration test suite verifying cross-layer cognitive flow across the 4-layer taxonomy:
- Layer 1: Research OS
- Layer 2: EIOS / EOS Kernel
- Layer 3: AEAN Brain
- Layer 4: APODEX 14-Layer Computational Engine Orchestrator
"""

import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.cognition.brain import CognitiveBrain
from apodex.ai_eos.intelligence.computational_architecture import (
    EntrepreneurialIntelligenceOrchestrator,
    AdvancedCausalEngine,
    ActiveInferencePlanner,
)

@pytest.mark.asyncio
async def test_full_cross_layer_cognitive_flow():
    # 1. Layer 1: Research OS conducts literature review & hypothesis formulation
    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference Expected Free Energy")
    assert review is not None
    assert "domain" in review

    hyp = ros.register_hypothesis(
        title="Active Inference Allocation Test",
        description="Active Inference minimizes epistemic uncertainty in market allocation.",
        null_hypothesis="Active Inference has no impact on allocation efficiency.",
        target_metric="allocation_yield"
    )
    assert hyp.hypothesis_id is not None

    # 2. Layer 2: EIOS Kernel registers hypothesis and manages execution DAG
    kernel = EIOSKernel()
    node = ExecutionNode(node_id="node_1", name="test_node", action_type="test_action", payload={"hyp_id": str(hyp.hypothesis_id)})
    dag = ExecutionDAG(
        id="dag_integration_01",
        nodes={"node_1": node}
    )
    dag_result = await kernel.execute_dag(dag)
    assert dag_result is True

    # 3. Layer 3: AEAN Cognitive Brain executes strategic cycle
    brain = CognitiveBrain(agent_id="integration_agent_01", domain="Autonomous System Orchestration")
    cycle_result = brain.run_strategic_cycle(goal_title="Optimize cross-layer resource allocation based on anomaly signals")
    assert cycle_result is not None
    assert isinstance(cycle_result, dict)

    # 4. Layer 4: APODEX 14-Layer Computational Engine processes end-to-end execution pipeline
    causal_engine = AdvancedCausalEngine()
    planner = ActiveInferencePlanner()
    orchestrator = EntrepreneurialIntelligenceOrchestrator(causal_engine, planner)

    signal_data = {
        "title": "Integration Scale Opportunity",
        "domain": "market_expansion",
        "variables": ["marketing_spend", "click_through_rate", "sales_revenue"],
        "causal_edges": [("marketing_spend", "click_through_rate"), ("click_through_rate", "sales_revenue")],
        "coefficients": {
            "marketing_spend->click_through_rate": 0.5,
            "click_through_rate->sales_revenue": 2.0
        },
        "prior_entropy": 1.8,
        "post_entropy_simulated": 0.5,
        "success_probability": 0.6,
        "tam_cents": 500000000
    }
    orchestrator.ingest_signal(signal_data)
    results = orchestrator.execute_orchestrated_pipeline()
    assert isinstance(results, dict)
    assert results.get("status") == "executed"
