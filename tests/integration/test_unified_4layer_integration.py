"""
test_unified_4layer_integration.py: Unified end-to-end integration test suite.
Validates cross-layer interaction between Layer 1 Research OS, Layer 2 EIOS Kernel & EOS Engine,
Layer 3 AEAN HiveMind, and Layer 4 APODEX platform execution.
"""

import pytest
from uuid import uuid4
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.ai_eos.research.integration import ResearchToSystemBridge


@pytest.mark.asyncio
async def test_unified_4layer_research_to_execution_lifecycle():
    # 1. Layer 1: Research OS
    research_os = ResearchOS()
    hyp = research_os.register_hypothesis(
        title="Active Inference Market Arbitrage",
        description="EFE minimization reduces GTM cost volatility by >15%",
        null_hypothesis="No cost variance reduction",
        target_metric="gtm_cost_volatility",
        significance_alpha=0.05
    )

    exp = research_os.create_experiment(hyp.hypothesis_id, seed=42)
    completed_exp = research_os.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert completed_exp.is_statistically_significant is True
    assert hyp.status == "validated"

    # 2. Layer 2: EIOS Kernel & EOS Engine
    eios_kernel = EIOSKernel()
    eos_engine = EOSEngine()

    # 3. Layer 3: AEAN Multi-Agent HiveMind
    hive_mind = HiveMind()

    # Bridge setup
    bridge = ResearchToSystemBridge(
        research_os=research_os,
        eios_kernel=eios_kernel,
        eos_engine=eos_engine,
        hive_mind=hive_mind
    )

    # Execute handoff
    record = bridge.handoff_validated_hypothesis(hyp.hypothesis_id)

    assert record["status"] == "completed"
    assert record["layer1_research_os"] is True
    assert record["layer2_eios_kernel"] is True
    assert record["layer2_eos_engine"] is True
    assert record["layer3_aean_hivemind"] is True

    # Verify state updates across layers
    sensors = eios_kernel.sense_opportunity_anomalies()
    assert len(sensors) == 1
    assert sensors[0]["title"] == "Active Inference Market Arbitrage"

    assert hyp.hypothesis_id in eos_engine.active_hypotheses

    # Layer 4 Execution DAG simulation
    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag("Deploy EFE Arbitrage Campaign", target_budget_usd=10000)
    success = await eios_kernel.execute_dag(dag)

    assert success is True
