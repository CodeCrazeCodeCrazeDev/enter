from __future__ import annotations
import pytest
from apodex.protocols.loader import ProtocolLoader
from apodex.harness.schemas.protocol_spec import ProtocolSpec

def test_protocol_serialization_and_loader():
    yaml_str = """
protocol_id: test_protocol
name: Test Protocol
k_steps: 10
downshift_after_steps_without_progress: 4
halt_after_steps_without_progress: 8
progress_rate_threshold: 0.5
steps:
  - step_id: step1
    skill_name: run_fast_security_scan
    anchors_to_hit:
      - ANCHOR_RAN_SECURITY_SCAN
  - step_id: step2
    skill_name: find_related_files_and_tests
    anchors_to_hit:
      - ANCHOR_FOUND_RELEVANT_FILES
"""
    spec = ProtocolLoader.load_from_yaml(yaml_str)
    assert spec.protocol_id == "test_protocol"
    assert spec.k_steps == 10
    assert len(spec.steps) == 2
    assert spec.steps[0].skill_name == "run_fast_security_scan"
    assert spec.steps[0].anchors_to_hit == ["ANCHOR_RAN_SECURITY_SCAN"]
