from __future__ import annotations
import pytest
from apodex.cognition.controller import CognitiveBenchmarkSuite


def test_expected_free_energy_capital_allocation():
    # Prior and posterior distributions for strategic marketing GTM options
    p_prior = [0.4, 0.4, 0.2]
    q_posterior = [0.1, 0.8, 0.1]

    kl_div = CognitiveBenchmarkSuite.run_expected_free_energy_evaluation(p_prior, q_posterior)

    # Assert KL-divergence calibrates perfectly and is positive
    assert kl_div > 0.0
    # Expected analytical value: 0.1*log(0.1/0.4) + 0.8*log(0.8/0.4) + 0.1*log(0.1/0.2)
    # 0.1*(-1.386) + 0.8*(0.693) + 0.1*(-0.693) = -0.1386 + 0.5544 - 0.0693 = 0.3465
    assert abs(kl_div - 0.3465) < 0.05


def test_causal_do_calculus_intervention():
    # Base projected cost is 10,000 cents. Causal counterfactual do(intervention) raises it to 15,000 cents.
    # Causal path correlation coefficient is 0.65.
    counterfactual_cost = CognitiveBenchmarkSuite.run_causal_counterfactual_intervention(
        base_val=10000.0,
        intervention_val=15000.0,
        correlation_coeff=0.65
    )

    assert counterfactual_cost == 13250.0


def test_ebbinghaus_memory_decay_utilization():
    # Initial memory card utility is 100.0. Half-life is 10 days. Elapsed is 10 days.
    retention = CognitiveBenchmarkSuite.run_ebbinghaus_decay_retention(
        initial_utility=100.0,
        elapsed_days=10.0,
        half_life_days=10.0
    )

    # After exactly one half-life, utility must be exactly 50%
    assert abs(retention - 50.0) < 0.01


def test_swarm_debate_sycophancy_mitigation():
    # Swarm consensus votes: 4 affirmative, 1 negative. Compliance bias offset of 0.20.
    votes = ["AFFIRMATIVE", "AFFIRMATIVE", "AFFIRMATIVE", "AFFIRMATIVE", "NEGATIVE"]

    calibrated_consensus = CognitiveBenchmarkSuite.run_multi_mind_sycophancy_mitigation(
        consensus_votes=votes,
        base_bias=0.20
    )

    # Expected: (4/5) - 0.20 = 0.80 - 0.20 = 0.60
    assert abs(calibrated_consensus - 0.60) < 0.01
