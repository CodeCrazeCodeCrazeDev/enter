from __future__ import annotations
import pytest
from apodex.harness.feature_tests import FeatureTestRunner
from apodex.world_model.orchestration.self_improvement_coordinator import SelfImprovementFlywheelCoordinator
from apodex.world_model.config import WorldModelCreatorConfig
from apodex.world_model.dependency_injection import DependencyContainer
from apodex.harness.schemas.protocol_spec import ProtocolSpec
from apodex.protocols.loader import ProtocolLoader

@pytest.mark.asyncio
async def test_step_level_credit_and_no_progress_halt():
    # Setup simulated scenario where no progress is detected (no new anchors hit)
    runner = FeatureTestRunner()

    # Custom protocol with highly sensitive progress-rate and short K limit
    yaml_str = """
protocol_id: strict_test_protocol
name: Strict Test Protocol
k_steps: 3
downshift_after_steps_without_progress: 1
halt_after_steps_without_progress: 2
progress_rate_threshold: 0.8
steps:
  - step_id: security_scan
    skill_name: run_fast_security_scan
    anchors_to_hit: [] # Hit no new anchors
  - step_id: triage
    skill_name: find_related_files_and_tests
    anchors_to_hit: [] # Hit no new anchors
  - step_id: patch
    skill_name: generate_code_patch
    anchors_to_hit: [] # Hit no new anchors
"""
    spec = ProtocolLoader.load_from_yaml(yaml_str)

    # Overwrite protocol file locally so coordinator loads it
    import os
    os.makedirs("apodex/harness/schemas/", exist_ok=True)
    with open("apodex/harness/schemas/code_improvement_protocol.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_str)

    try:
        coord = await runner.run_scenario(tenant_id="strict_tenant", tier="EXPENSIVE", max_budget=10.0)

        # Verify downshift event was triggered
        downshift_events = [log for log in coord.execution_log if log.get("event") == "anchor_progress_downshift"]
        assert len(downshift_events) > 0
        assert downshift_events[0]["new_tier"] == "CHEAP"

        # Verify budget halt due to lack of progress was triggered
        halt_events = [log for log in coord.execution_log if log.get("status") == "BUDGET_HALTED" or log.get("event") == "budget_halt"]
        assert len(halt_events) > 0
    finally:
        # Revert changes to schema file
        if os.path.exists("apodex/harness/schemas/code_improvement_protocol.yaml"):
            os.remove("apodex/harness/schemas/code_improvement_protocol.yaml")
