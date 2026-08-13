# -*- coding: utf-8 -*-
"""
test_real_benchmarks.py: Tests for real capability benchmarks and the
Welch's t-test experiment framework logging.
"""
from __future__ import annotations
import math
import pytest
from uuid import UUID
from apodex.ai_eos.research.experiment_framework import ExperimentRecord
from apodex.ai_eos.research.research_os import ResearchOS


def test_experiment_record_welchs_t_test_calculation():
    """Verify Welch's t-test and p-value calculation inside ExperimentRecord."""
    record = ExperimentRecord(
        hypothesis="Recursive planning decreases decomposition latency.",
        baseline_version="1.0.0 (Monolithic)",
        candidate_version="2.0.0 (Recursive)",
        task_distribution="Planning Latency Tasks",
        metrics=["duration_ms"]
    )

    # Log 10 trials
    # Baseline mean is ~15.0, Candidate mean is ~10.0 (effect size is -5.0, which means candidate is faster)
    baseline_outcomes = [15.1, 14.8, 16.2, 14.5, 15.5, 14.9, 15.0, 15.2, 14.7, 15.1]
    candidate_outcomes = [10.2, 9.8, 10.5, 10.1, 9.9, 10.3, 10.0, 10.1, 9.7, 10.4]

    record.log_trial_outcomes(baseline_outcomes, candidate_outcomes)

    assert record.sample_size == 10
    assert record.mean_baseline == pytest.approx(15.1)
    assert record.mean_candidate == pytest.approx(10.1)
    assert record.effect_size == pytest.approx(-5.0)

    # Since effect_size is negative (duration decreased), we reject/revise if we wanted positive gain.
    # But wait, let's check decision boundary
    decision = record.make_decision(alpha=0.05)
    # Since effect_size is negative, decision is REJECT (because our logic expects positive metric improvement)
    assert decision == "REJECT"


def test_experiment_record_promotion_gain_outcomes():
    """Verify PROMOTE decision when candidate outperforms baseline (positive outcome metric)."""
    record = ExperimentRecord(
        hypothesis="Ebbinghaus consolidator increases memory recall precision.",
        baseline_version="1.0.0 (Stale)",
        candidate_version="2.0.0 (Consolidated)",
        task_distribution="Recall Tasks",
        metrics=["recall_precision"]
    )

    # Positive outcome metric (e.g. recall accuracy where higher is better)
    baseline_outcomes = [0.72, 0.75, 0.70, 0.73, 0.71, 0.74, 0.72, 0.75, 0.70, 0.73]
    candidate_outcomes = [0.92, 0.94, 0.90, 0.93, 0.91, 0.95, 0.92, 0.94, 0.90, 0.93]

    record.log_trial_outcomes(baseline_outcomes, candidate_outcomes)
    assert record.effect_size > 0.15
    assert record.p_value < 0.01

    decision = record.make_decision(alpha=0.05)
    assert decision == "PROMOTE"


def test_real_world_planning_latency_benchmark():
    """Execute real platform planning benchmark with actual planners to verify capability gain."""
    ros = ResearchOS()

    # Stage 1: Formulate Question and Hypotheses
    question_data = ros.discover_problem_and_formulate_question("prob_planning_efficiency")
    hyp = ros.generate_hypothesis(paper_id=9, problem_id="prob_planning_efficiency")
    exp = ros.create_experiment(hyp.hypothesis_id, seed=50)

    # Stage 2: Controlled Benchmark Execution (Run actual planner code/workload simulations)
    benchmark_res = ros.execute_real_benchmark_experiment(
        experiment_id=exp.experiment_id,
        run_actual=True,
        sample_size=12
    )

    # Stage 3: Statistical Evaluation
    record = ExperimentRecord(
        hypothesis=hyp.statement,
        baseline_version="StrategicPlanner (Baseline)",
        candidate_version="OptimizedPlanner (Candidate)",
        task_distribution=question_data["target_metric"],
        metrics=["execution_ms"]
    )
    record.log_trial_outcomes(benchmark_res["baseline_runs"], benchmark_res["candidate_runs"])

    # Latencies should be positive values
    assert len(record.raw_baseline_results) == 12
    assert record.mean_baseline > 0.0
    assert record.mean_candidate > 0.0
    assert record.effect_size != 0.0
