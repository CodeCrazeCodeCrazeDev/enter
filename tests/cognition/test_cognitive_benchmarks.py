# -*- coding: utf-8 -*-
"""
test_cognitive_benchmarks.py: Comprehensive unit and validation test suite
verifying the CognitiveBenchmarkSuite performance metrics.
"""
from __future__ import annotations
import pytest
from apodex.cognition.controller import CognitiveBenchmarkSuite


def test_cognitive_benchmark_suite_execution() -> None:
    """Verifies that CognitiveBenchmarkSuite accurately executes and computes all 6 substrates."""
    suite = CognitiveBenchmarkSuite()
    metrics = suite.run_all_benchmarks()

    # 1. Reasoning Substrate
    assert metrics["reasoning_multistep_accuracy"] > 0.80
    assert metrics["reasoning_contradiction_detection"] > 0.80
    assert metrics["reasoning_uncertainty_calibration"] > 0.80
    assert metrics["reasoning_hypothesis_quality"] > 0.80

    # 2. Planning Substrate
    assert metrics["planning_decomposition_quality"] > 0.80
    assert metrics["planning_validity"] > 0.80
    assert metrics["planning_replanning_success"] > 0.80
    assert metrics["planning_long_horizon_completion"] > 0.80

    # 3. Research Substrate
    assert metrics["research_retrieval_precision"] > 0.80
    assert metrics["research_retrieval_recall"] > 0.80
    assert metrics["research_claim_verification"] > 0.80
    assert metrics["research_experiment_design_quality"] > 0.80
    assert metrics["research_cycle_time_sec"] < 20.0

    # 4. Memory Substrate
    assert metrics["memory_retrieval_precision"] > 0.80
    assert metrics["memory_retrieval_recall"] > 0.80
    assert metrics["memory_temporal_consistency"] > 0.80
    assert metrics["memory_provenance_accuracy"] > 0.90
    assert metrics["memory_contamination_rate"] < 0.05

    # 5. Multi-Agent Substrate
    assert metrics["multi_agent_coordination_efficiency"] > 0.80
    assert metrics["multi_agent_redundant_work_rate"] < 0.10
    assert metrics["multi_agent_disagreement_resolution_rate"] > 0.80
    assert metrics["multi_agent_communication_overhead_tokens"] < 2000.0

    # 6. Self-Improvement Substrate
    assert metrics["self_improvement_weakness_detection"] > 0.80
    assert metrics["self_improvement_regression_detection"] > 0.80
    assert metrics["self_improvement_acceptance_accuracy"] > 0.80
    assert metrics["self_improvement_rollback_correctness"] > 0.90
    assert metrics["self_improvement_capability_growth"] > 0.10

    # 7. Engineering Performance Substrate
    assert metrics["engineering_test_reliability"] > 0.95
    assert metrics["engineering_fault_recovery_rate"] > 0.90
    assert metrics["engineering_latency_ms"] < 200.0
    assert metrics["engineering_memory_usage_mb"] < 500.0
    assert metrics["engineering_architectural_complexity_score"] < 50.0
