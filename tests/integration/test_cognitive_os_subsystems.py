# -*- coding: utf-8 -*-
"""
test_cognitive_os_subsystems.py: Cross-subsystem integration test suite for
ResearchOS, EIOS Kernel, EOS Engine, and AEAN.
"""

import pytest
import asyncio
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.ai_eos.domain.models import VentureCell


def test_research_os_to_eios_and_eos_bridge_flow():
    """Verify that validated research in ResearchOS flows through the bridge into EIOS Kernel and EOS Engine."""
    research_os = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    bridge = ResearchToSystemBridge(research_os, kernel, eos)

    # 1. Register hypothesis in ResearchOS
    hyp = research_os.register_hypothesis(
        title="Active Inference Market Elasticity",
        description="Demand elasticity follows active inference EFE model",
        null_hypothesis="Demand is constant",
        target_metric="market_demand_index"
    )

    # 2. Mark hypothesis as validated
    hyp.status = "validated"

    # 3. Promote via bridge
    result = bridge.promote_validated_hypothesis(hyp.hypothesis_id)
    assert result["status"] == "PROMOTED_TO_SYSTEM"
    assert result["kernel_registration"] is True
    assert result["eos_promotion"] is True

    # 4. Check EIOS Kernel state
    assert str(hyp.hypothesis_id) in kernel.registered_research_hypotheses
    anomalies = kernel.sense_opportunity_anomalies({"market_demand_index": 2.1})
    assert len(anomalies) == 1
    assert anomalies[0]["hypothesis_id"] == str(hyp.hypothesis_id)

    # 5. Check EOS Engine state
    assert hyp.hypothesis_id in eos.active_hypotheses
    assert eos.active_hypotheses[hyp.hypothesis_id].title == "Active Inference Market Elasticity"


@pytest.mark.asyncio
async def test_end_to_end_subsystem_execution_cycle():
    """Verify combined execution across EntrepreneurialCompiler, EIOSKernel, and EOSEngine continuous sensing."""
    compiler = EntrepreneurialCompiler()
    kernel = EIOSKernel()
    eos = EOSEngine()

    # 1. Compile high level goal into DAG
    dag = compiler.compile_goal_to_dag(goal="Automate B2B SaaS Customer Acquisition", target_budget_usd=10000)
    assert len(dag.nodes) == 4

    # 2. Execute DAG using EIOS Kernel
    success = await kernel.execute_dag(dag)
    assert success is True

    # 3. Create Venture Cell and execute EOS Engine continuous sensing cycle
    cell = VentureCell(name="B2B SaaS Cell", namespace="b2b_saas")
    metrics = eos.run_continuous_sensing_cycle(cells=[cell], total_budget_cents=100000_00)

    assert "world_state" in metrics
    assert "allocated_budgets" in metrics
    assert cell.cell_id in metrics["allocated_budgets"]
