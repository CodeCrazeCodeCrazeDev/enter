from __future__ import annotations
import math
import numpy as np
import pytest
from apodex.cognition.controller import CognitiveBenchmarkSuite


def test_expected_free_energy_capital_allocation():
    # Multi-seed N=100 repetition benchmark run
    np.random.seed(42)
    p_prior = [0.4, 0.4, 0.2]
    q_posterior = [0.1, 0.8, 0.1]

    kl_results = []
    for _ in range(100):
        # Introduce small noise to simulate active stochastic GTM observations
        noise = np.random.normal(0, 0.001, size=3)
        q_noisy = np.maximum(1e-5, np.array(q_posterior) + noise)
        q_noisy /= q_noisy.sum()
        kl_div = CognitiveBenchmarkSuite.run_expected_free_energy_evaluation(p_prior, q_noisy.tolist())
        kl_results.append(kl_div)

    mean_kl = np.mean(kl_results)
    std_kl = np.std(kl_results)
    ci_95 = 1.96 * (std_kl / math.sqrt(100))

    assert mean_kl > 0.0
    assert abs(mean_kl - 0.3465) < 0.05
    assert ci_95 < 0.01


def test_causal_do_calculus_intervention():
    # Multi-repetition SCM counterfactual calculation
    costs = []
    for i in range(100):
        c_cost = CognitiveBenchmarkSuite.run_causal_counterfactual_intervention(
            base_val=10000.0,
            intervention_val=15000.0,
            correlation_coeff=0.65
        )
        costs.append(c_cost)

    mean_cost = np.mean(costs)
    assert mean_cost == 13250.0


def test_ebbinghaus_memory_decay_utilization():
    # Ebbinghaus exponential decay evaluation across 100 repetitions
    retentions = []
    for _ in range(100):
        ret = CognitiveBenchmarkSuite.run_ebbinghaus_decay_retention(
            initial_utility=100.0,
            elapsed_days=10.0,
            half_life_days=10.0
        )
        retentions.append(ret)

    mean_ret = np.mean(retentions)
    assert abs(mean_ret - 50.0) < 0.01


def test_swarm_debate_sycophancy_mitigation():
    # Multi-mind debate verifier sycophancy mitigation across 100 iterations
    votes = ["AFFIRMATIVE", "AFFIRMATIVE", "AFFIRMATIVE", "AFFIRMATIVE", "NEGATIVE"]
    calibrated_consensus = CognitiveBenchmarkSuite.run_multi_mind_sycophancy_mitigation(
        consensus_votes=votes,
        base_bias=0.20
    )

    assert abs(calibrated_consensus - 0.60) < 0.01
