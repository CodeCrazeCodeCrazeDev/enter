"""Unit tests for Phase 2 Research Operating System statistical validation and registries."""

import pytest
from uuid import uuid4
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.domain.models import Hypothesis, Experiment, ExecutionStatus


def test_research_os_registries():
    """Verify hypothesis registration and experiment generation works correctly."""
    ros = ResearchOS()

    hyp = ros.register_hypothesis(
        title="Revenue Elasticity",
        description="Hypothesis that decreasing price by 10% increases volume by 25%.",
        null_hypothesis="H0: Volume increase <= 10%",
        target_metric="volume_increase"
    )

    assert hyp.title == "Revenue Elasticity"
    assert hyp.status == "registered"

    exp = ros.create_experiment(hyp.hypothesis_id, seed=101)
    assert exp.hypothesis_id == hyp.hypothesis_id
    assert exp.seed == 101
    assert len(exp.reproducibility_hash) == 64


def test_data_leakage_detection():
    """Verify data leakage checks correctly identify overlap."""
    ros = ResearchOS()

    train = ["key1", "key2", "key3"]
    test_clean = ["key4", "key5"]
    test_leaked = ["key3", "key6"]

    assert ros.detect_data_leakage(train, test_clean) is False
    assert ros.detect_data_leakage(train, test_leaked) is True


def test_statistical_validation_reproducible():
    """Verify that walk-forward statistical simulation yields reproducible results."""
    ros = ResearchOS()

    hyp = ros.register_hypothesis(
        title="Ad Placement CTR Boost",
        description="Placing banner on top increases CTR by 15%",
        null_hypothesis="H0: CTR increase <= 0%",
        target_metric="ctr_increase"
    )

    exp1 = ros.create_experiment(hyp.hypothesis_id, seed=42)
    exp2 = ros.create_experiment(hyp.hypothesis_id, seed=42)

    # Run simulation with high positive effect (ground truth = 2.5)
    outcome1 = ros.execute_experiment_simulation(exp1.experiment_id, ground_truth_yield=2.5)
    outcome2 = ros.execute_experiment_simulation(exp2.experiment_id, ground_truth_yield=2.5)

    # Check reproducibility (equal seeds and setups must match exactly)
    assert outcome1.p_value == outcome2.p_value
    assert outcome1.effect_size == outcome2.effect_size
    assert outcome1.deflated_sharpe_ratio == outcome2.deflated_sharpe_ratio
    assert outcome1.is_statistically_significant == outcome2.is_statistically_significant


def test_statistical_significance_filtering():
    """Verify significant signals are promoted and weak ones are refuted."""
    ros = ResearchOS()

    hyp_strong = ros.register_hypothesis(
        title="Strong Signal",
        description="High yield",
        null_hypothesis="H0 <= 0",
        target_metric="yield"
    )
    exp_strong = ros.create_experiment(hyp_strong.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(exp_strong.experiment_id, ground_truth_yield=5.0)

    # Reload and assert validated
    hyp_strong_res = ros.hypotheses.get(hyp_strong.hypothesis_id)
    assert hyp_strong_res.status == "validated"

    hyp_weak = ros.register_hypothesis(
        title="Weak Signal",
        description="Zero yield",
        null_hypothesis="H0 <= 0",
        target_metric="yield"
    )
    exp_weak = ros.create_experiment(hyp_weak.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(exp_weak.experiment_id, ground_truth_yield=-0.5)

    hyp_weak_res = ros.hypotheses.get(hyp_weak.hypothesis_id)
    assert hyp_weak_res.status == "refuted"
