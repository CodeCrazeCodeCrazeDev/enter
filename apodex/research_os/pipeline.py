"""Foundational orchestrator, validator, and governance gateway for AlphaAlgo Research OS.

Coordinates the non-bypassable research pipeline stages and enforces rigorous gates.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple
from .interfaces import IStatisticalValidator, IGovernanceGateway
from .models import (
    Experiment,
    ValidationReport,
    DecisionRecord,
    Model,
    compute_config_hash,
)
from .statistical_validation import adjust_p_values, calculate_dsr, block_bootstrap

logger = logging.getLogger("research_os.pipeline")


class StatisticalValidator(IStatisticalValidator):
    """Significance and multiple-testing correction evaluator."""

    def __init__(self, correction_method: str = "HOLM") -> None:
        self.correction_method = correction_method

    def validate_experiment(self, experiment: Experiment, all_trials: List[Experiment]) -> ValidationReport:
        if experiment.status != "COMPLETED":
            raise ValueError(f"Cannot validate experiment with status '{experiment.status}'.")

        returns = experiment.returns_time_series
        if not returns:
            raise ValueError("Experiment contains no returns time series.")

        # Compute raw metrics
        raw_sharpe = experiment.metrics.get("sharpe", 0.0)

        # Calculate raw p-value under the null (approximate from normal distribution of returns)
        # Standard t-statistic-like p-value for mean return > 0
        n_obs = len(returns)
        mean_ret = sum(returns) / n_obs
        var_ret = sum((r - mean_ret) ** 2 for r in returns) / (n_obs - 1) if n_obs > 1 else 1e-12
        std_ret = math_std = (var_ret ** 0.5) or 1e-12

        t_stat = (mean_ret / std_ret) * (n_obs ** 0.5) if std_ret > 0 else 0.0
        # Single-sided p-value
        raw_p = 1.0 - 0.5 * (1.0 + (t_stat / (2.0 ** 0.5)))  # normal approximation
        raw_p = max(1e-15, min(1.0 - 1e-15, raw_p))

        # Perform multiple testing correction across all completed trials
        trials_count = max(len(all_trials), 1)
        trial_p_values = []
        for trial in all_trials:
            trial_returns = trial.returns_time_series
            if trial_returns:
                t_len = len(trial_returns)
                t_mean = sum(trial_returns) / t_len
                if t_len > 1:
                    t_std = (sum((tr - t_mean) ** 2 for tr in trial_returns) / (t_len - 1)) ** 0.5 or 1e-12
                else:
                    t_std = 1e-12
                t_stat_trial = (t_mean / t_std) * (t_len ** 0.5)
                tp = 1.0 - 0.5 * (1.0 + (t_stat_trial / (2.0 ** 0.5)))
                trial_p_values.append(max(1e-15, min(1.0, tp)))
            else:
                trial_p_values.append(0.5)

        # Holm-Bonferroni or other corrections
        adjusted_p_values = adjust_p_values(trial_p_values, self.correction_method)
        # Find index of this experiment in all_trials to locate its adjusted p-value
        try:
            exp_idx = next(i for i, t in enumerate(all_trials) if t.experiment_id == experiment.experiment_id)
            adjusted_p = adjusted_p_values[exp_idx]
        except StopIteration:
            # If not found, run adjustment on its individual p-value
            adjusted_p = adjust_p_values([raw_p], self.correction_method)[0]

        # Calculate Deflated Sharpe Ratio (DSR)
        # Compute skewness, kurtosis, and trials variance of Sharpe Ratios
        all_sharpes = [t.metrics.get("sharpe", 0.0) for t in all_trials if t.status == "COMPLETED"]
        if not all_sharpes:
            all_sharpes = [raw_sharpe]
        trials_var = float(sum((s - (sum(all_sharpes)/len(all_sharpes)))**2 for s in all_sharpes)/len(all_sharpes)) if len(all_sharpes) > 1 else 0.1
        if trials_var < 1e-8:
            trials_var = 0.1

        # Calculate skewness & kurtosis of returns
        mean_r = sum(returns) / n_obs
        if n_obs > 1:
            std_r = (sum((r - mean_r)**2 for r in returns) / (n_obs - 1))**0.5 or 1e-12
            skew = sum((r - mean_r)**3 for r in returns) / (n_obs * (std_r**3)) if n_obs > 2 else 0.0
            kurt = sum((r - mean_r)**4 for r in returns) / (n_obs * (std_r**4)) if n_obs > 3 else 3.0
        else:
            std_r = 1e-12
            skew = 0.0
            kurt = 3.0

        dsr = calculate_dsr(
            sharpe=raw_sharpe,
            trials=trials_count,
            returns_length=n_obs,
            skewness=skew,
            kurtosis=kurt,
            trials_variance=trials_var,
        )

        # Block Bootstrapping
        boot_sharpes = block_bootstrap(returns, block_size=10, num_samples=200)
        boot_sharpes.sort()
        quantile_5 = boot_sharpes[int(len(boot_sharpes) * 0.05)]

        # Determine overall statistical significance
        # Must satisfy DSR >= 0.95 and adjusted p_value <= 0.05
        is_significant = (dsr >= 0.95) and (adjusted_p <= 0.05) and (quantile_5 > 0)

        # Compute mock Probability of Backtest Overfitting (PBO)
        # A mock implementation for metadata tracking
        pbo = 0.05 if is_significant else 0.45

        return ValidationReport(
            validation_id=f"val_{experiment.experiment_id}",
            experiment_id=experiment.experiment_id,
            raw_sharpe_ratio=raw_sharpe,
            deflated_sharpe_ratio=dsr,
            p_value=raw_p,
            adjusted_p_value=adjusted_p,
            correction_method=self.correction_method,
            probability_of_backtest_overfitting=pbo,
            bootstrap_sharpe_quantile_5=quantile_5,
            is_statistically_significant=is_significant,
        )


class GovernanceGateway(IGovernanceGateway):
    """Non-bypassable promotion gate and immutable cryptographic ledger tracker."""

    def __init__(self, initial_audit_hash: str = "GENESIS_AUDIT_LEDGER") -> None:
        self.last_audit_hash = initial_audit_hash

    def evaluate_promotion(
        self,
        experiment: Experiment,
        report: ValidationReport,
        reviewers: List[str],
        approvals: Dict[str, bool],
    ) -> DecisionRecord:
        # Evaluate consensus (approvals count)
        total_voters = len(reviewers)
        positive_votes = sum(1 for reviewer in reviewers if approvals.get(reviewer, False))

        # Gates checks
        rationales = []
        if not report.is_statistically_significant:
            rationales.append("Failed Gate 1: Experiment is not statistically significant (DSR or p-value).")
        if report.deflated_sharpe_ratio < 0.95:
            rationales.append(f"Failed Gate 1: Deflated Sharpe Ratio ({report.deflated_sharpe_ratio:.4f}) is below the 0.95 threshold.")
        if report.bootstrap_sharpe_quantile_5 <= 0:
            rationales.append(f"Failed Gate 2: Bootstrap 5th percentile Sharpe ({report.bootstrap_sharpe_quantile_5:.4f}) is <= 0.")
        if total_voters == 0 or (positive_votes / total_voters) < 0.5:
            rationales.append("Failed Gate 4: Under 50% approval from the peer-review panel.")

        # Determine decision status
        status = "APPROVED" if len(rationales) == 0 else "REJECTED"

        # Construct decision record
        decision = DecisionRecord(
            decision_id=f"dec_{experiment.experiment_id}",
            experiment_id=experiment.experiment_id,
            reviewers=reviewers,
            approvals=approvals,
            status=status,
            metrics_summary={
                "raw_sharpe": report.raw_sharpe_ratio,
                "dsr": report.deflated_sharpe_ratio,
                "bootstrap_quantile_5": report.bootstrap_sharpe_quantile_5,
                "pbo": report.probability_of_backtest_overfitting,
            },
            rejection_rationales=rationales,
            previous_log_hash=self.last_audit_hash,
        )

        # Compute immutable hash signature and update state
        decision.entry_hash = decision.calculate_entry_hash()
        self.last_audit_hash = decision.entry_hash

        return decision


class ResearchPipelineOrchestrator:
    """The central coordinator that executes the research pipeline in a deterministic sequence."""

    def __init__(
        self,
        hypotheses: IHypothesisRegistry,
        datasets: IDatasetRegistry,
        features: IFeatureRegistry,
        experiments: IExperimentRegistry,
        models: IModelRegistry,
        validator: IStatisticalValidator,
        gateway: IGovernanceGateway,
    ) -> None:
        self.hypotheses = hypotheses
        self.datasets = datasets
        self.features = features
        self.experiments = experiments
        self.models = models
        self.validator = validator
        self.gateway = gateway

    def execute_pipeline(
        self,
        hypothesis_id: str,
        dataset_id: str,
        feature_ids: List[str],
        hyperparameters: Dict[str, Any],
        trial_runner_fn: Any,  # Simulation/Backtest function to call
        reviewers: List[str],
        approvals: Dict[str, bool],
    ) -> Tuple[Experiment, Optional[ValidationReport], Optional[DecisionRecord], Optional[Model]]:
        """Coordinates and executes the entire research pipeline."""
        # Check pre-registrations
        hypothesis = self.hypotheses.get_hypothesis(hypothesis_id)
        if not hypothesis:
            raise ValueError(f"Hypothesis '{hypothesis_id}' is not pre-registered. No bypass allowed.")

        dataset = self.datasets.get_dataset(dataset_id)
        if not dataset:
            raise ValueError(f"Dataset snapshot '{dataset_id}' is not registered. No bypass allowed.")

        for fid in feature_ids:
            if not self.features.get_feature(fid):
                raise ValueError(f"Feature '{fid}' is not registered. No bypass allowed.")

        # 1. Deterministic Caching lookup
        # Construct tentative experiment object to calculate its unique config hash
        temp_exp = Experiment(
            experiment_id="temp",
            hypothesis_id=hypothesis_id,
            dataset_id=dataset_id,
            feature_ids=feature_ids,
            hyperparameters=hyperparameters,
        )
        config_hash = temp_exp.calculate_config_hash()

        cached_exp = self.experiments.get_experiment_by_hash(config_hash)
        if cached_exp:
            logger.info(f"Configuration match found in Experiment Registry. Reusing cached result {cached_exp.experiment_id}.")
            experiment = cached_exp
        else:
            # 2. Ingest and run backtest in deterministic sandbox
            experiment = Experiment(
                experiment_id=f"exp_{config_hash[:16]}",
                hypothesis_id=hypothesis_id,
                dataset_id=dataset_id,
                feature_ids=feature_ids,
                hyperparameters=hyperparameters,
                config_hash=config_hash,
                status="RUNNING",
            )

            try:
                # Call sandboxed backtester/simulator
                returns, metrics = trial_runner_fn(dataset, feature_ids, hyperparameters)
                experiment.returns_time_series = returns
                experiment.metrics = metrics
                experiment.status = "COMPLETED"
            except Exception as e:
                experiment.status = "FAILED"
                experiment.error_log = str(e)
                self.experiments.register_experiment(experiment)
                return experiment, None, None, None

            # Save completed trial to registry
            self.experiments.register_experiment(experiment)

        # 3. Statistical Validation
        # Get all completed trials in registry to adjust for multiple testing
        all_trials = [
            e for e in self.experiments._store.values() if e.status == "COMPLETED"
        ] if hasattr(self.experiments, "_store") else [experiment]

        report = self.validator.validate_experiment(experiment, all_trials)

        # 4. Peer Review and Governance Gate
        decision = self.gateway.evaluate_promotion(experiment, report, reviewers, approvals)

        # 5. Model Promotion
        model = None
        if decision.status == "APPROVED":
            model = Model(
                model_id=f"mod_{experiment.experiment_id}",
                experiment_id=experiment.experiment_id,
                decision_record_id=decision.decision_id,
                version="1.0.0",
                capacity_limit_usd=1000000.0,
                correlation_to_portfolio=0.15,
            )
            self.models.register_model(model)

        return experiment, report, decision, model
