"""Entrepreneurial Operating System (EOS) First-Principles Engine.

Implements all 10 core AI modules and the master orchestrator from Section 10
of the Entrepreneurial Operating System Specification:
1. SensingAgent (Anomaly detection via Bayesian surprise)
2. HypothesisEngineFirstPrinciples (Forced falsifiable hypothesis generation & kill criteria)
3. ValidationAgent (Cheap test simulation & economic viability scoring)
4. GTMSimulator (Channel fit & cohort unit economics trajectory)
5. GrowthStageClassifier (9-stage evolution classifier & constraint/risk detection)
6. MoatAnalyzerFirstPrinciples (Composite moat durability scoring across 7 powers)
7. FailureModeMonitor (Operating metric pattern-matching vs failure modes)
8. CapitalAllocator (Opportunity-cost expected value ranking & allocation)
9. ReinventionTrigger (Self-disruption & model pivot triggers)
10. GovernanceSafetyLayer (Type I / Type II decision governance & kill enforcement)
11. EOSEngineFirstPrinciples (Integrated master state machine orchestrator)
"""

from __future__ import annotations
import math
import logging
from typing import Any, Dict, List, Optional, Tuple, Set
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.eos_first_principles")


# =====================================================================
# State Machine & Domain Enums
# =====================================================================
class EOSState(str, Enum):
    SENSING = "Sensing"
    HYPOTHESIS = "Hypothesis"
    CHEAP_TEST = "CheapTest"
    DISCARD = "Discard"
    VALIDATION = "Validation"
    BUILD_GATE = "BuildGate"
    MVP = "MVP"
    GTM_TEST = "GTMTest"
    KILL_OR_SCALE = "KillOrScale"
    SCALE = "Scale"
    OPERATE = "Operate"
    REINVENT = "Reinvent"


class GrowthStage(str, Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "Product-Market Fit"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    MARKET_LEADERSHIP = "Market Leadership"


class DecisionType(str, Enum):
    TYPE_I = "Type I (Irreversible / High Stakes)"
    TYPE_II = "Type II (Reversible / Low Stakes)"


# =====================================================================
# Domain Data Models
# =====================================================================
class OpportunitySignal(BaseModel):
    signal_id: UUID = Field(default_factory=uuid4)
    source: str
    metric_name: str
    observed_value: float
    baseline_expected_value: float
    variance: float = 0.1
    is_structural_shift: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class FalsifiableHypothesis(BaseModel):
    hypothesis_id: UUID = Field(default_factory=uuid4)
    title: str
    falsifiable_claim: str
    prior_confidence: float = 0.5
    posterior_confidence: float = 0.5
    kill_threshold_confidence: float = 0.3
    promotion_threshold_confidence: float = 0.8
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    status: str = "PROPOSED"  # PROPOSED, TESTING, CONFIRMED, FALSIFIED


class ExperimentResult(BaseModel):
    experiment_id: UUID = Field(default_factory=uuid4)
    hypothesis_id: UUID
    cost_cents: int
    p_value: float
    effect_size: float
    sample_size: int
    success: bool
    summary: str


class VentureCohortMetrics(BaseModel):
    traffic: int
    conversion_rate: float
    arpu_cents: int
    cac_cents: int
    churn_rate: float
    payback_months_max_threshold: float = 12.0
    min_ltv_cac_ratio: float = 3.0


class Initiative(BaseModel):
    initiative_id: UUID = Field(default_factory=uuid4)
    name: str
    stage: GrowthStage = GrowthStage.IDEA
    expected_return_cents: int
    required_budget_cents: int
    risk_factor: float  # 0.0 to 1.0
    strategic_alignment: float  # 0.0 to 1.0
    allocated_budget_cents: int = 0


# =====================================================================
# 1. Sensing Agent
# =====================================================================
class SensingAgent:
    """Continuously ingests market/tech signals and flags anomalies via Bayesian surprise."""

    def __init__(self, surprise_threshold: float = 2.0) -> None:
        self.surprise_threshold = surprise_threshold

    def evaluate_signal(self, signal: OpportunitySignal) -> Dict[str, Any]:
        """Compute Bayesian surprise (Kullback-Leibler divergence proxy) for a signal."""
        diff = abs(signal.observed_value - signal.baseline_expected_value)
        surprise_score = (diff ** 2) / (2 * max(0.0001, signal.variance))

        is_anomaly = surprise_score >= self.surprise_threshold
        signal.is_structural_shift = is_anomaly

        return {
            "signal_id": signal.signal_id,
            "metric": signal.metric_name,
            "surprise_score": surprise_score,
            "is_anomaly": is_anomaly,
            "recommendation": "FORM_HYPOTHESIS" if is_anomaly else "IGNORE_NOISE"
        }


# =====================================================================
# 2. Hypothesis Engine (First-Principles)
# =====================================================================
class HypothesisEngineFirstPrinciples:
    """Converts anomalies into falsifiable claims with pre-committed kill criteria."""

    def __init__(self) -> None:
        self.hypotheses: Dict[UUID, FalsifiableHypothesis] = {}

    def generate_hypothesis(self, title: str, claim: str, prior: float = 0.5) -> FalsifiableHypothesis:
        hyp = FalsifiableHypothesis(
            title=title,
            falsifiable_claim=claim,
            prior_confidence=prior,
            posterior_confidence=prior
        )
        self.hypotheses[hyp.hypothesis_id] = hyp
        return hyp

    def update_hypothesis(self, hypothesis_id: UUID, exp_result: ExperimentResult) -> FalsifiableHypothesis:
        hyp = self.hypotheses.get(hypothesis_id)
        if not hyp:
            raise ValueError(f"Hypothesis {hypothesis_id} not found")

        if exp_result.p_value < 0.05 and exp_result.effect_size > 0.0:
            hyp.supporting_evidence.append(exp_result.summary)
            # Bayesian update approximation
            hyp.posterior_confidence = min(0.99, hyp.posterior_confidence + 0.35 * exp_result.effect_size)
        else:
            hyp.contradicting_evidence.append(exp_result.summary)
            hyp.posterior_confidence = max(0.01, hyp.posterior_confidence - 0.30)

        # Check thresholds
        if hyp.posterior_confidence <= hyp.kill_threshold_confidence:
            hyp.status = "FALSIFIED"
        elif hyp.posterior_confidence >= hyp.promotion_threshold_confidence:
            hyp.status = "CONFIRMED"
        else:
            hyp.status = "TESTING"

        return hyp


# =====================================================================
# 3. Validation Agent
# =====================================================================
class ValidationAgent:
    """Runs cheap tests and scores economic viability of opportunity hypotheses."""

    def __init__(self) -> None:
        pass

    def evaluate_economic_viability(
        self,
        hypothesis: FalsifiableHypothesis,
        estimated_tam_cents: int,
        target_margin: float,
        test_cost_cents: int
    ) -> Dict[str, Any]:
        """Calculates expected return and determines if economic gate is cleared."""
        expected_value_cents = int(estimated_tam_cents * target_margin * hypothesis.posterior_confidence)
        roi_ratio = expected_value_cents / max(1, test_cost_cents)

        cleared_gate = hypothesis.status == "CONFIRMED" and roi_ratio >= 5.0 and expected_value_cents > 1000000_00

        return {
            "hypothesis_id": hypothesis.hypothesis_id,
            "posterior_confidence": hypothesis.posterior_confidence,
            "expected_value_cents": expected_value_cents,
            "test_roi_ratio": roi_ratio,
            "cleared_build_gate": cleared_gate
        }


# =====================================================================
# 4. GTM Simulator
# =====================================================================
class GTMSimulator:
    """Models channel fit, unit economics, payback period, and cohort trajectories."""

    def __init__(self) -> None:
        pass

    def simulate_cohort(self, metrics: VentureCohortMetrics) -> Dict[str, Any]:
        acquired_customers = int(metrics.traffic * metrics.conversion_rate)
        total_cac_cents = acquired_customers * metrics.cac_cents
        mrr_cents = acquired_customers * metrics.arpu_cents

        ltv_cents = int(metrics.arpu_cents / metrics.churn_rate) if metrics.churn_rate > 0 else metrics.arpu_cents * 12
        ltv_cac_ratio = ltv_cents / max(1, metrics.cac_cents)
        payback_months = metrics.cac_cents / max(1, metrics.arpu_cents)

        is_scalable = (
            ltv_cac_ratio >= metrics.min_ltv_cac_ratio and
            payback_months <= metrics.payback_months_max_threshold
        )

        return {
            "acquired_customers": acquired_customers,
            "total_cac_cents": total_cac_cents,
            "mrr_cents": mrr_cents,
            "ltv_cents": ltv_cents,
            "ltv_cac_ratio": round(ltv_cac_ratio, 2),
            "payback_months": round(payback_months, 2),
            "is_scalable": is_scalable
        }


# =====================================================================
# 5. Growth Stage Classifier
# =====================================================================
class GrowthStageClassifier:
    """Classifies company growth stage and identifies binding constraints & risks."""

    def __init__(self) -> None:
        pass

    def classify_stage(
        self,
        validated_learnings_count: int,
        paying_customers: int,
        retention_curve_flattened: bool,
        growth_rate_mom: float,
        ecosystem_gmv_cents: int
    ) -> Dict[str, Any]:
        """Classifies venture into one of 9 stages with binding constraint diagnosis."""
        if ecosystem_gmv_cents > 100_000_000_00:
            stage = GrowthStage.ECOSYSTEM
            constraint = "Governance Credibility & Network Fragmentation"
        elif growth_rate_mom > 0.20 and retention_curve_flattened and paying_customers > 1000:
            stage = GrowthStage.GROWTH
            constraint = "Hiring Velocity & System Scaling"
        elif retention_curve_flattened and paying_customers > 100:
            stage = GrowthStage.PMF
            constraint = "Team Bandwidth & Process Execution"
        elif paying_customers > 10:
            stage = GrowthStage.STARTUP
            constraint = "Cash Runway & Channel Repeatability"
        elif paying_customers > 0 or validated_learnings_count > 5:
            stage = GrowthStage.VALIDATION
            constraint = "Signal Quality & Willingness to Pay"
        else:
            stage = GrowthStage.IDEA
            constraint = "Founder Time & Hypothesis Falsification"

        return {
            "growth_stage": stage.value,
            "binding_constraint": constraint,
            "premature_scaling_risk": stage == GrowthStage.GROWTH and not retention_curve_flattened
        }


# =====================================================================
# 6. Moat Analyzer (First-Principles)
# =====================================================================
class MoatAnalyzerFirstPrinciples:
    """Quantifies structural competitive advantages across Helmer's 7 Powers & Porter."""

    def score_moat(
        self,
        network_density: float,          # 0.0 to 1.0
        switching_cost_score: float,     # 0.0 to 1.0
        scale_economies_score: float,    # 0.0 to 1.0
        brand_trust_score: float,        # 0.0 to 1.0
        counter_positioning: bool,       # True/False
        cornered_resource: bool          # True/False
    ) -> Dict[str, Any]:
        score = (
            0.25 * network_density +
            0.20 * switching_cost_score +
            0.20 * scale_economies_score +
            0.15 * brand_trust_score +
            (0.10 if counter_positioning else 0.0) +
            (0.10 if cornered_resource else 0.0)
        )
        durability_score = round(min(1.0, max(0.0, score)), 2)

        return {
            "moat_durability_score": durability_score,
            "is_defensible": durability_score >= 0.60,
            "primary_advantage": "Network Effects" if network_density > 0.6 else "Switching Costs/Scale"
        }


# =====================================================================
# 7. Failure Mode Monitor
# =====================================================================
class FailureModeMonitor:
    """Pattern-matches operating metrics against failure mode table and raises alerts."""

    def __init__(self) -> None:
        pass

    def evaluate_health(
        self,
        burn_multiple: float,
        retention_curve_flattened: bool,
        decision_latency_days: float,
        cac_payback_months: float
    ) -> List[Dict[str, str]]:
        alerts = []

        if burn_multiple > 2.5:
            alerts.append({
                "failure_mode": "Capital Misallocation / High Burn",
                "root_cause": "Scaling spend ahead of unit economic stability",
                "correction": "Rank all initiatives on expected return and trim non-performing bets"
            })

        if not retention_curve_flattened and cac_payback_months > 18.0:
            alerts.append({
                "failure_mode": "Lack of Product-Market Fit / Premature Scaling",
                "root_cause": "Confusing early demand spike with durable PMF",
                "correction": "Stop scaling acquisition spend; return to cohort retention optimization"
            })

        if decision_latency_days > 14.0:
            alerts.append({
                "failure_mode": "Organizational Bottleneck",
                "root_cause": "Founder as single point of failure / central decision rights",
                "correction": "Delegate decision rights with clear framework rules"
            })

        return alerts


# =====================================================================
# 8. Capital Allocator
# =====================================================================
class CapitalAllocator:
    """Ranks initiatives on common expected-return basis & enforces opportunity-cost discipline."""

    def __init__(self) -> None:
        pass

    def allocate_capital(
        self,
        initiatives: List[Initiative],
        total_available_budget_cents: int
    ) -> Dict[str, Any]:
        if not initiatives:
            return {"allocations": {}, "unallocated_cents": total_available_budget_cents}

        # Calculate Expected Value net of risk for each initiative
        scored = []
        for init in initiatives:
            # Expected value = expected_return * strategic_alignment * (1 - risk)
            ev = init.expected_return_cents * init.strategic_alignment * (1.0 - init.risk_factor)
            roi = ev / max(1, init.required_budget_cents)
            scored.append((roi, init))

        # Rank by ROI descending (Opportunity cost ranking)
        scored.sort(key=lambda x: x[0], reverse=True)

        remaining = total_available_budget_cents
        allocations = {}

        for roi, init in scored:
            if roi <= 1.0:
                # Do not fund initiatives with ROI <= 1.0
                continue
            if remaining >= init.required_budget_cents:
                init.allocated_budget_cents = init.required_budget_cents
                remaining -= init.required_budget_cents
            else:
                init.allocated_budget_cents = remaining
                remaining = 0
            allocations[str(init.initiative_id)] = {
                "name": init.name,
                "allocated_cents": init.allocated_budget_cents,
                "roi": round(roi, 2)
            }

        return {
            "allocations": allocations,
            "unallocated_cents": remaining,
            "funded_count": len(allocations)
        }


# =====================================================================
# 9. Reinvention Trigger
# =====================================================================
class ReinventionTrigger:
    """Forces periodic self-disruption and model pivot reviews on market decay signals."""

    def evaluate_reinvention_need(
        self,
        revenue_decay_rate_mom: float,
        churn_rate: float,
        competitor_feature_disruption: bool
    ) -> Dict[str, Any]:
        should_reinvent = (
            (revenue_decay_rate_mom > 0.10 and churn_rate > 0.15) or
            competitor_feature_disruption
        )

        return {
            "should_reinvent": should_reinvent,
            "trigger_reason": "Structural metric decay / market disruption" if should_reinvent else "Nominal trajectory",
            "action": "TRIGGER_PARALLEL_SENSING" if should_reinvent else "CONTINUE_OPERATE"
        }


# =====================================================================
# 10. Governance & Safety Layer
# =====================================================================
class GovernanceSafetyLayer:
    """Enforces kill criteria, prevents runaway capital, and gates Type I decisions."""

    def evaluate_decision(
        self,
        decision_name: str,
        decision_type: DecisionType,
        is_reversible: bool,
        capital_at_risk_cents: int,
        human_approved: bool = False
    ) -> Dict[str, Any]:
        if decision_type == DecisionType.TYPE_I or not is_reversible or capital_at_risk_cents > 100_000_000_00:
            # Type I decision requires explicit human sign-off
            allowed = human_approved
            reason = "Type I decision requires explicit human sign-off" if not human_approved else "Human approved"
        else:
            # Type II decision: fast, autonomous execution
            allowed = True
            reason = "Type II reversible decision approved for fast autonomous execution"

        return {
            "decision": decision_name,
            "type": decision_type.value,
            "allowed": allowed,
            "reason": reason
        }


# =====================================================================
# 11. EOSEngineFirstPrinciples Orchestrator
# =====================================================================
class EOSEngineFirstPrinciples:
    """Master Orchestrator connecting all 10 AI-EOS modules into a continuous loop."""

    def __init__(self) -> None:
        self.current_state: EOSState = EOSState.SENSING
        self.sensing_agent = SensingAgent()
        self.hypothesis_engine = HypothesisEngineFirstPrinciples()
        self.validation_agent = ValidationAgent()
        self.gtm_simulator = GTMSimulator()
        self.growth_classifier = GrowthStageClassifier()
        self.moat_analyzer = MoatAnalyzerFirstPrinciples()
        self.failure_monitor = FailureModeMonitor()
        self.capital_allocator = CapitalAllocator()
        self.reinvention_trigger = ReinventionTrigger()
        self.governance = GovernanceSafetyLayer()

        self.active_hypotheses: List[FalsifiableHypothesis] = []
        self.state_history: List[Dict[str, Any]] = []

    def transition_to(self, new_state: EOSState, reason: str = "") -> None:
        logger.info(f"EOS STATE TRANSITION: {self.current_state.value} -> {new_state.value} ({reason})")
        self.state_history.append({
            "from_state": self.current_state.value,
            "to_state": new_state.value,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc)
        })
        self.current_state = new_state

    def run_master_cycle(
        self,
        signals: List[OpportunitySignal],
        available_capital_cents: int,
        human_governance_approved: bool = False
    ) -> Dict[str, Any]:
        """Runs a complete end-to-end master loop iteration."""
        results: Dict[str, Any] = {"initial_state": self.current_state.value}

        # 1. Sensing & Anomaly Detection
        self.transition_to(EOSState.SENSING, "Processing signals")
        anomalies = []
        for sig in signals:
            eval_res = self.sensing_agent.evaluate_signal(sig)
            if eval_res["is_anomaly"]:
                anomalies.append(sig)

        results["anomalies_detected"] = len(anomalies)

        if not anomalies:
            self.transition_to(EOSState.SENSING, "No structural anomalies detected")
            results["final_state"] = self.current_state.value
            return results

        # 2. Hypothesis Generation
        self.transition_to(EOSState.HYPOTHESIS, "Anomalies detected")
        created_hypotheses = []
        for anom in anomalies:
            hyp = self.hypothesis_engine.generate_hypothesis(
                title=f"Structural shift in {anom.metric_name}",
                claim=f"Observed value {anom.observed_value} vs baseline {anom.baseline_expected_value} indicates market opportunity",
                prior=0.5
            )
            created_hypotheses.append(hyp)

        results["hypotheses_created"] = len(created_hypotheses)

        # 3. Cheap Testing & Validation
        self.transition_to(EOSState.CHEAP_TEST, "Running validation experiments")
        validated_hypotheses = []
        for hyp in created_hypotheses:
            exp = ExperimentResult(
                hypothesis_id=hyp.hypothesis_id,
                cost_cents=500_00,  # $500 cheap experiment
                p_value=0.01,
                effect_size=1.0,
                sample_size=200,
                success=True,
                summary="Strong user conversion signal in cheap test"
            )
            updated_hyp = self.hypothesis_engine.update_hypothesis(hyp.hypothesis_id, exp)
            if updated_hyp.status == "CONFIRMED":
                validated_hypotheses.append(updated_hyp)

        results["validated_hypotheses_count"] = len(validated_hypotheses)

        if not validated_hypotheses:
            self.transition_to(EOSState.DISCARD, "All hypotheses falsified")
            results["final_state"] = self.current_state.value
            return results

        # 4. Build Gate & Governance
        self.transition_to(EOSState.BUILD_GATE, "Checking economic viability & governance")
        top_hyp = validated_hypotheses[0]
        viability = self.validation_agent.evaluate_economic_viability(
            hypothesis=top_hyp,
            estimated_tam_cents=50000000_00, # $50M TAM
            target_margin=0.70,
            test_cost_cents=500_00
        )

        gov_check = self.governance.evaluate_decision(
            decision_name=f"Commit build resources for {top_hyp.title}",
            decision_type=DecisionType.TYPE_II, # Reversible MVP bet
            is_reversible=True,
            capital_at_risk_cents=5000_00,
            human_approved=human_governance_approved
        )

        results["viability"] = viability
        results["governance"] = gov_check

        if viability["cleared_build_gate"] and gov_check["allowed"]:
            self.transition_to(EOSState.MVP, "Build gate cleared")
            self.transition_to(EOSState.GTM_TEST, "MVP shipped")

            # Simulate GTM cohort
            gtm_res = self.gtm_simulator.simulate_cohort(
                VentureCohortMetrics(
                    traffic=10000,
                    conversion_rate=0.05,
                    arpu_cents=100_00,
                    cac_cents=150_00,
                    churn_rate=0.03
                )
            )
            results["gtm_simulation"] = gtm_res

            if gtm_res["is_scalable"]:
                self.transition_to(EOSState.SCALE, "Repeatable unit economics confirmed")
                self.transition_to(EOSState.OPERATE, "Operate scaling loop")
            else:
                self.transition_to(EOSState.KILL_OR_SCALE, "Economics below threshold")
        else:
            self.transition_to(EOSState.DISCARD, "Build gate or governance failed")

        results["final_state"] = self.current_state.value
        return results
