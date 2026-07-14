from __future__ import annotations
import pytest
from apodex.harness.feature_tests import FeatureTestRunner

@pytest.mark.asyncio
async def test_agentic_feature_test_harness_scenarios():
    runner = FeatureTestRunner()

    # 1. EXPENSIVE Run
    coord1 = await runner.run_scenario(tenant_id="tenant_A", tier="EXPENSIVE", max_budget=10.0)
    assert coord1.tenant_id == "tenant_A"
    assert len(coord1.world_model.pkc_traces) == 1

    # Verify that multi-tenant cache isolation doesn't leak cache records across tenants
    coord2 = await runner.run_scenario(tenant_id="tenant_B", tier="EXPENSIVE", max_budget=10.0)
    # Both runs executed completely without a cache-hit from tenant A, since they have separate tenants
    cache_hits_a = [log for log in coord1.execution_log if log.get("status") == "CACHE_HIT"]
    cache_hits_b = [log for log in coord2.execution_log if log.get("status") == "CACHE_HIT"]
    assert len(cache_hits_a) == 0
    assert len(cache_hits_b) == 0

    # 2. Budget ceiling halt scenario
    coord_halt = await runner.run_scenario(tenant_id="tenant_C", tier="EXPENSIVE", max_budget=0.01)
    # Finding a budget halt event in the execution logs
    halt_logs = [log for log in coord_halt.execution_log if log.get("event") == "budget_halt"]
    assert len(halt_logs) > 0
