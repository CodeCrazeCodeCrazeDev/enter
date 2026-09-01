"""Unified 4-Layer Active Inference integration test suite validating Layer 1 Research OS, Layer 2 EIOS Kernel & EOS Engine, Layer 3 AEAN HiveMind, and Layer 4 APODEX WorldModel."""

from __future__ import annotations
import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


@pytest.mark.asyncio
async def test_unified_4layer_end_to_end_flow():
    # 1. Layer 1 Research OS
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Predictive Funnel Optimization",
        description="Conversion increases with personalized LLM agents",
        null_hypothesis="conversion <= 0.02",
        target_metric="conversion_rate"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=42)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.0)

    # 2. Layer 2 EIOS Kernel & EOS Engine
    kernel = EIOSKernel()
    eos = EOSEngine()
    compiler = EntrepreneurialCompiler()

    dag = compiler.compile_goal_to_dag(goal="Deploy Personalized Agents", target_budget_usd=10000)
    exec_success = await kernel.execute_dag(dag)
    assert exec_success is True

    # 3. Layer 3 AEAN HiveMind
    hive_mind = HiveMind(token_budget=100)

    # 4. Layer 4 APODEX WorldModel
    world_model = WorldModel()

    # 5. Bridge Handoff Execution
    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive_mind,
        world_model=world_model
    )

    handoff_summary = bridge.execute_cross_layer_handoff(hyp)
    assert handoff_summary["status"] == "complete"

    # Sense anomalies over registered hypotheses in EIOS Kernel
    anomalies_report = kernel.sense_opportunity_anomalies()
    assert anomalies_report["anomalies_count"] == 1
    assert anomalies_report["anomalies"][0]["title"] == "Predictive Funnel Optimization"
