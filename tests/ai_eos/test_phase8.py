"""Unit tests for Phase 8 Validation Platform and Benchmarks."""

import pytest
from uuid import uuid4
from apodex.ai_eos.validation.platform import ValidationPlatform


def test_chaos_fault_injection():
    """Verify stochastic fault injection handles chaos monkey events gracefully."""
    vp = ValidationPlatform()

    # Stub call failing with 100% probability
    failed = vp.inject_fault("resolve_db", fail_probability=1.0)
    assert failed is True

    # Stub call passing with 0% failure probability
    passed = vp.inject_fault("resolve_db", fail_probability=0.0)
    assert passed is False


def test_regression_replay_determinism():
    """Verify that decision replay matches expected output precisely."""
    vp = ValidationPlatform()

    # Map inputs -> outputs
    trace_id_1 = uuid4()
    vp.log_regression_trace(
        trace_id=trace_id_1,
        decision_inputs={"allocated_capital": 50000},
        expected_output="APPROVED"
    )

    trace_id_2 = uuid4()
    vp.log_regression_trace(
        trace_id=trace_id_2,
        decision_inputs={"allocated_capital": 2000000},
        expected_output="REJECTED"
    )

    # Simple mock decision engine
    def mock_decision_engine(inputs: dict) -> str:
        if inputs["allocated_capital"] > 100000:
            return "REJECTED"
        return "APPROVED"

    result = vp.run_regression_replay(mock_decision_engine)
    assert result["total_runs"] == 2
    assert result["passed_runs"] == 2
    assert result["success_rate"] == 1.0


def test_architectural_conformance_scanner():
    """Verify that file scans correctly pass when import coupling boundaries are clean."""
    vp = ValidationPlatform()
    # Execute scan on our newly created clean package
    conforms = vp.verify_architectural_conformance()
    assert conforms is True
