"""Unit and integration tests for AlphaAlgo Research OS.

Verifies statistical calculations, multiple-testing adjustments, registries,
immutability rules, and end-to-end pipeline execution.
"""
from __future__ import annotations

import math
from datetime import datetime
import pytest
from apodex.research_os import (
    Hypothesis,
    Dataset,
    Feature,
    Experiment,
    Model,
    HypothesisRegistry,
    DatasetRegistry,
    FeatureRegistry,
    ExperimentRegistry,
    ModelRegistry,
    adjust_p_values,
    calculate_dsr,
    walk_forward_split,
    block_bootstrap,
    capture_environment_fingerprint,
    verify_reproducibility,
    StatisticalValidator,
    GovernanceGateway,
    ResearchPipelineOrchestrator,
)


def test_multiple_testing_adjustments() -> None:
    """Verify Bonferroni, Holm-Bonferroni, and BH corrections."""
    p_values = [0.005, 0.01, 0.03, 0.05, 0.12]

    # Bonferroni: p * N, capped at 1.0
    bonf = adjust_p_values(p_values, "BONFERRONI")
    assert bonf[0] == pytest.approx(0.005 * 5)
    assert bonf[4] == pytest.approx(0.12 * 5)

    # Holm-Bonferroni
    holm = adjust_p_values(p_values, "HOLM")
    assert holm[0] == pytest.approx(0.005 * 5)  # lowest sorted compared to alpha / (5 - 0)
    assert holm[4] == pytest.approx(0.12 * 1)  # highest compared to alpha / 1

    # Benjamini-Hochberg (BH)
    bh = adjust_p_values(p_values, "BH")
    assert all(bh[i] >= p_values[i] for i in range(len(p_values)))
    assert bh[4] == pytest.approx(0.12)


def test_walk_forward_splits() -> None:
    """Verify correct segment bounds generation for walk-forward splits."""
    splits = walk_forward_split(total_length=100, train_size=50, test_size=10, step_size=10, rolling=True)
    assert len(splits) == 5
    # First split: train on 0-50, test on 50-60
    assert splits[0] == ((0, 50), (50, 60))
    # Second split (rolling): train on 10-60, test on 60-70
    assert splits[1] == ((10, 60), (60, 70))


def test_deflated_sharpe_ratio() -> None:
    """Verify that increased trials number properly deflates (lowers) DSR."""
    # Compute DSR for 1 trial vs 100 trials given the same Sharpe and observation size
    dsr_10 = calculate_dsr(sharpe=2.0, trials=10, returns_length=252, trials_variance=0.1)
    dsr_100 = calculate_dsr(sharpe=2.0, trials=100, returns_length=252, trials_variance=0.1)

    # Higher trials number must increase the hurdle (SR_0), therefore lowering the DSR
    assert dsr_10 > dsr_100


def test_block_bootstrapping() -> None:
    """Verify block bootstrap returns stable resampled returns."""
    returns = [0.001, 0.002, -0.001, 0.003, -0.002, 0.001, 0.002, 0.004, -0.001, 0.002] * 10
    boot = block_bootstrap(returns, block_size=5, num_samples=50, seed=42)
    assert len(boot) == 50
    assert all(isinstance(val, float) for val in boot)


def test_registries_immutability() -> None:
    """Verify registries prevent duplicate IDs and overwrites."""
    hyp_reg = HypothesisRegistry()
    h = Hypothesis(
        hypothesis_id="H_01",
        research_question_id="Q_01",
        title="Momentum",
        description="Exploits price trends",
        economic_rationale="BEHAVIORAL",
        null_hypothesis="Returns are zero",
        target_variable="1_day_forward_ret",
    )

    hyp_reg.register_hypothesis(h)
    assert hyp_reg.get_hypothesis("H_01") is not None

    # Re-registering must raise a ValueError
    with pytest.raises(ValueError, match="already exists"):
        hyp_reg.register_hypothesis(h)


def test_experiment_config_hashing() -> None:
    """Verify that configuration changes alter the SHA-256 hash."""
    exp1 = Experiment(
        experiment_id="exp_1",
        hypothesis_id="H_01",
        dataset_id="ds_1",
        feature_ids=["f_1", "f_2"],
        hyperparameters={"learning_rate": 0.01},
        reproducibility_package={"seed": 42},
    )

    exp2 = Experiment(
        experiment_id="exp_2",
        hypothesis_id="H_01",
        dataset_id="ds_1",
        feature_ids=["f_1", "f_2"],
        hyperparameters={"learning_rate": 0.05},  # config change
        reproducibility_package={"seed": 42},
    )

    hash1 = exp1.calculate_config_hash()
    hash2 = exp2.calculate_config_hash()
    assert hash1 != hash2


def test_end_to_end_pipeline_success() -> None:
    """Test successful pipeline flow through statistical and governance gates."""
    # Setup registries
    hyp_reg = HypothesisRegistry()
    ds_reg = DatasetRegistry()
    feat_reg = FeatureRegistry()
    exp_reg = ExperimentRegistry()
    mod_reg = ModelRegistry()

    # Pre-register objects
    h = Hypothesis(
        hypothesis_id="H_01",
        research_question_id="Q_01",
        title="Trend Following",
        description="Exploiting price persistence",
        economic_rationale="BEHAVIORAL",
        null_hypothesis="No trend exists",
        target_variable="forward_ret",
    )
    hyp_reg.register_hypothesis(h)

    ds = Dataset(
        dataset_id="DS_01",
        version="v1.0",
        raw_source="s3://data",
        ingestion_pipeline_hash="h123",
    )
    ds_reg.register_dataset(ds)

    f1 = Feature(
        feature_id="F_01",
        name="SMA_10",
        formula="mean(close, 10)",
        lineage_dataset_id="DS_01",
    )
    feat_reg.register_feature(f1)

    # Mock trial runner function returning significant returns
    # Daily returns leading to high Sharpe (e.g. 2.5)
    def mock_successful_trial(dataset, feature_ids, hyperparameters):
        daily_returns = [0.002, 0.003, -0.001, 0.004, 0.001, 0.002, 0.003] * 30  # 210 observations
        # Sharpe ratio is highly positive
        metrics = {"sharpe": 2.5, "max_drawdown": 0.05}
        return daily_returns, metrics

    # Instantiate validators and gateway
    validator = StatisticalValidator(correction_method="HOLM")
    gateway = GovernanceGateway()

    orchestrator = ResearchPipelineOrchestrator(
        hypotheses=hyp_reg,
        datasets=ds_reg,
        features=feat_reg,
        experiments=exp_reg,
        models=mod_reg,
        validator=validator,
        gateway=gateway,
    )

    reviewers = ["expert_human", "ai_critic"]
    approvals = {"expert_human": True, "ai_critic": True}

    # Execute
    exp, report, decision, model = orchestrator.execute_pipeline(
        hypothesis_id="H_01",
        dataset_id="DS_01",
        feature_ids=["F_01"],
        hyperparameters={"learning_rate": 0.01},
        trial_runner_fn=mock_successful_trial,
        reviewers=reviewers,
        approvals=approvals,
    )

    # Assertions
    assert exp.status == "COMPLETED"
    assert report is not None
    assert report.raw_sharpe_ratio == 2.5
    assert report.deflated_sharpe_ratio > 0.95
    assert report.is_statistically_significant is True
    assert decision.status == "APPROVED"
    assert model is not None
    assert mod_reg.get_model(model.model_id) is not None


def test_end_to_end_pipeline_rejection() -> None:
    """Test pipeline rejection on low-significance performance."""
    hyp_reg = HypothesisRegistry()
    ds_reg = DatasetRegistry()
    feat_reg = FeatureRegistry()
    exp_reg = ExperimentRegistry()
    mod_reg = ModelRegistry()

    h = Hypothesis(
        hypothesis_id="H_01",
        research_question_id="Q_01",
        title="Mean Reversion",
        description="Exploits temporary deviation",
        economic_rationale="MICROSTRUCTURE",
        null_hypothesis="No deviation",
        target_variable="forward_ret",
    )
    hyp_reg.register_hypothesis(h)

    ds = Dataset(
        dataset_id="DS_01",
        version="v1.0",
        raw_source="s3://data",
        ingestion_pipeline_hash="h123",
    )
    ds_reg.register_dataset(ds)

    f1 = Feature(
        feature_id="F_01",
        name="RSI_14",
        formula="rsi(close, 14)",
        lineage_dataset_id="DS_01",
    )
    feat_reg.register_feature(f1)

    # Mock trial runner returning flat/unprofitable returns
    def mock_failed_trial(dataset, feature_ids, hyperparameters):
        daily_returns = [0.0001, -0.0001, 0.0002, -0.0003] * 50
        metrics = {"sharpe": 0.1, "max_drawdown": 0.15}
        return daily_returns, metrics

    validator = StatisticalValidator(correction_method="HOLM")
    gateway = GovernanceGateway()

    orchestrator = ResearchPipelineOrchestrator(
        hypotheses=hyp_reg,
        datasets=ds_reg,
        features=feat_reg,
        experiments=exp_reg,
        models=mod_reg,
        validator=validator,
        gateway=gateway,
    )

    reviewers = ["expert_human", "ai_critic"]
    approvals = {"expert_human": True, "ai_critic": True}

    # Execute
    exp, report, decision, model = orchestrator.execute_pipeline(
        hypothesis_id="H_01",
        dataset_id="DS_01",
        feature_ids=["F_01"],
        hyperparameters={"learning_rate": 0.01},
        trial_runner_fn=mock_failed_trial,
        reviewers=reviewers,
        approvals=approvals,
    )

    # Assertions
    assert exp.status == "COMPLETED"
    assert report is not None
    assert report.is_statistically_significant is False
    assert decision.status == "REJECTED"
    assert len(decision.rejection_rationales) > 0
    assert model is None


def test_self_improvement_flywheel_advanced_policy() -> None:
    """Verify that SelfImprovementFlywheel generates advanced paper-derived policy rules."""
    from apodex.research_os.self_improvement import SelfImprovementFlywheel
    from apodex.research_os.storage import ResearchRepository
    from apodex.research_os.events import EventBus
    import uuid

    repo = ResearchRepository()
    bus = EventBus()
    flywheel = SelfImprovementFlywheel(repository=repo, event_bus=bus)

    # Log 2 failures for a stage called "data_ingestion"
    run_id = uuid.uuid4()
    flywheel.log_failure(run_id, "data_ingestion", "Out of memory error.")
    flywheel.log_failure(run_id, "data_ingestion", "JSON parsing failed.")

    # Evolve and assert policy rules match our new advanced principles
    policy = flywheel.analyze_bottlenecks_and_evolve()
    assert policy is not None
    assert "data_ingestion" in policy.policy_name.lower()

    rules = policy.rules
    assert len(rules) == 4
    assert any("verification confidence rate of >= 0.85" in r for r in rules)
    assert any("Execute 3x independent replicates" in r for r in rules)
    assert any("step-wise process verification" in r for r in rules)
    assert any("Multi-Mind Consensus" in r for r in rules)
