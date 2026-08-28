"""Integration test validating cross-layer handoffs across Layer 1 Research OS, Layer 2 EIOS Kernel & EOS Engine, Layer 3 AEAN, and Layer 4 APODEX."""

from __future__ import annotations
import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.ai_eos.domain.models import VentureCell


def test_unified_4layer_active_inference_handoff():
    # 1. Initialize Subsystems (Layers 1, 2, 3, 4)
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    bridge = ResearchToSystemBridge(research_os=ros, eios_kernel=kernel, eos_engine=eos)

    # 2. Layer 1: Register and Validate Research Hypothesis
    hyp = ros.register_hypothesis(
        title="Active Inference Expected Free Energy Routing",
        description="EFE minimization reduces task uncertainty by 40%",
        null_hypothesis="EFE routing has no effect",
        target_metric="uncertainty_reduction"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=42)
    val_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.0)
    assert val_exp.is_statistically_significant is True
    assert hyp.status == "validated"

    # 3. Layer 1 -> Layer 2 Active Inference Bridge Handoff
    payload = bridge.bridge_hypothesis_to_execution(hyp.hypothesis_id)
    assert payload["status"] == "validated"
    assert payload["title"] == "Active Inference Expected Free Energy Routing"

    # Verify Layer 2 Kernel received sensing hypothesis
    assert str(hyp.hypothesis_id) in kernel.research_hypotheses

    # Verify Layer 2 EOS Engine ingested active hypothesis
    assert len(eos.active_hypotheses) == 1
    assert eos.active_hypotheses[0]["title"] == "Active Inference Expected Free Energy Routing"

    # 4. Layer 2: Sense opportunity anomalies & execute continuous sensing cycle
    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) == 1
    assert anomalies[0]["hypothesis_id"] == str(hyp.hypothesis_id)

    cell = VentureCell(name="Autonomous Research Cell", namespace="res_cell_01", allocated_capital_cents=5000000)
    sensing_result = eos.run_continuous_sensing_cycle([cell], total_budget_cents=5000000)
    assert sensing_result["market_uncertainty"] >= 0.0

    # 5. Full End-to-End Cross-Layer Cycle Execution
    cycle_res = bridge.execute_cross_layer_cycle("Cognitive OS Active Inference")
    assert cycle_res["status"] == "success"
    assert cycle_res["is_significant"] is True
    assert len(cycle_res["kernel_anomalies"]) >= 1


@pytest.mark.asyncio
async def test_eios_kernel_dag_compilation_and_execution():
    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag("Deploy Autonomous Agentic Institution", target_budget_usd=10000)
    assert len(dag.nodes) == 4

    kernel = EIOSKernel()
    success = await kernel.execute_dag(dag)
    assert success is True
