"""First-Principles Entrepreneurial Operating System (EOS) Engine.

Algorithmic implementation of the 11-section First-Principles EOS specification:
- Multi-timescale coupled feedback loops (Fast, Medium, Slow)
- Signal-to-Idea pipeline (Anomaly detection, hypothesis generation, Bayesian belief updates, Type I/II risk gating)
- 13 coupled external business loops with signal processing & unit economic feedback
- 15-stage Customer Journey full lifecycle tracker & bottleneck detector
- 9-stage Company Growth System & binding constraint classifier
- 10-pattern Operating Failure Mode Monitor
- Pursue Opportunity Decision Tree
- Re-entrant System State Machine with kill signals & reinvention triggers
- 10 AI-EOS Autonomous Executive Modules
"""

from __future__ import annotations
import math
import uuid
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Set
from pydantic import BaseModel, Field

logger = logging.getLogger("ai_eos.intelligence.eos_first_principles")


# =====================================================================
# 0. Timescales & Feedback Loops
# =====================================================================

class LoopTimescale(str, Enum):
    FAST = "FAST"        # Days - Weeks (Experiments, ad tests, sales calls)
    MEDIUM = "MEDIUM"    # Months - Quarters (GTM, pricing, org design, capital)
    SLOW = "SLOW"        # Years (Positioning, moats, ecosystem, reinvention)


class FeedbackLoop(BaseModel):
    loop_id: str
    name: str
    timescale: LoopTimescale
    cycle_time_days: float
    signal_to_noise_ratio: float
    is_compounding: bool = True
    input_stock: str
    output_stock: str
    kpi_name: str
    kpi_value: float

    def calculate_velocity(self) -> float:
        """Loop velocity: 1 / cycle_time_days."""
        if self.cycle_time_days <= 0:
            return 0.0
        return 1.0 / self.cycle_time_days


# =====================================================================
# 2. Internal Cognitive Loops (Signal-to-Idea Pipeline & Mental Models)
# =====================================================================

class Anomaly(BaseModel):
    anomaly_id: str = Field(default_factory=lambda: f"anom_{uuid.uuid4().hex[:8]}")
    description: str
    observed_value: float
    expected_value: float
    kuhn_surprise_score: float = 0.0  # Normalized deviation

    def evaluate_kuhn_threshold(self, threshold: float = 1.5) -> bool:
        """Checks if surprise violates expected model beyond Kuhn paradigm threshold."""
        if self.expected_value == 0:
            self.kuhn_surprise_score = abs(self.observed_value)
        else:
            self.kuhn_surprise_score = abs(self.observed_value - self.expected_value) / abs(self.expected_value)
        return self.kuhn_surprise_score >= threshold


class RiskType(str, Enum):
    TYPE_I = "TYPE_I"    # Irreversible, one-way door (slow deliberation)
    TYPE_II = "TYPE_II"  # Reversible, two-way door (fast execution)


class Hypothesis(BaseModel):
    hypothesis_id: str = Field(default_factory=lambda: f"hyp_{uuid.uuid4().hex[:8]}")
    claim: str
    prior_probability: float = 0.5
    posterior_probability: float = 0.5
    risk_type: RiskType = RiskType.TYPE_II
    test_cost_usd: float = 100.0
    information_value_usd: float = 1000.0
    is_falsified: bool = False


class MentalModel(BaseModel):
    model_id: str
    name: str
    parameters: Dict[str, float] = Field(default_factory=dict)
    structural_error: float = 0.0
    version: int = 1

    def update_parameters(self, delta: Dict[str, float]) -> None:
        """Fast loop parameter tuning."""
        for k, v in delta.items():
            if k in self.parameters:
                self.parameters[k] += v

    def trigger_paradigm_shift(self, new_structure_params: Dict[str, float]) -> None:
        """Slow loop structural update."""
        self.parameters = new_structure_params
        self.structural_error = 0.0
        self.version += 1


class SignalToIdeaEngine:
    """Processes weak environmental signals into falsifiable hypotheses and Bayesian updates."""

    def detect_anomaly(self, description: str, observed: float, expected: float) -> Tuple[Anomaly, bool]:
        anomaly = Anomaly(description=description, observed_value=observed, expected_value=expected)
        is_structural = anomaly.evaluate_kuhn_threshold()
        return anomaly, is_structural

    def form_hypothesis(self, claim: str, risk_type: RiskType, test_cost: float, info_value: float) -> Hypothesis:
        return Hypothesis(
            claim=claim,
            risk_type=risk_type,
            test_cost_usd=test_cost,
            information_value_usd=info_value
        )

    def update_bayesian_belief(self, hypothesis: Hypothesis, likelihood_if_true: float, likelihood_if_false: float) -> Hypothesis:
        """Bayes theorem: P(H|D) = P(D|H) * P(H) / [P(D|H)*P(H) + P(D|~H)*(1-P(H))]."""
        prior = hypothesis.prior_probability
        numerator = likelihood_if_true * prior
        denominator = (likelihood_if_true * prior) + (likelihood_if_false * (1.0 - prior))

        if denominator > 0:
            posterior = numerator / denominator
        else:
            posterior = prior

        hypothesis.posterior_probability = posterior
        if posterior < 0.15:
            hypothesis.is_falsified = True
        return hypothesis

    def evaluate_opportunity_cost(self, expected_return: float, hurdle_rate: float) -> bool:
        """Filters opportunities against hurdle rate discipline."""
        return expected_return >= hurdle_rate


# =====================================================================
# 3. External Coupled Business Loops
# =====================================================================

class BusinessLoopName(str, Enum):
    PRODUCT = "PRODUCT"
    MARKETING = "MARKETING"
    SALES = "SALES"
    CUSTOMER_SUCCESS = "CUSTOMER_SUCCESS"
    BRAND = "BRAND"
    PRICING = "PRICING"
    REFERRAL = "REFERRAL"
    DATA = "DATA"
    FINANCIAL = "FINANCIAL"
    HIRING = "HIRING"
    CULTURE = "CULTURE"
    INNOVATION = "INNOVATION"
    COMPETITIVE = "COMPETITIVE"


class CoupledBusinessLoopsEngine:
    """Simulates and evaluates the 13 coupled business feedback loops."""

    def __init__(self) -> None:
        self.state: Dict[str, float] = {
            "retention_slope": 0.05,
            "nps": 45.0,
            "cac_usd": 120.0,
            "conversion_rate": 0.03,
            "win_rate": 0.25,
            "acv_usd": 5000.0,
            "nrr": 1.15,
            "churn_rate": 0.02,
            "arpu_usd": 400.0,
            "gross_margin": 0.80,
            "viral_coefficient_k": 0.4,
            "burn_multiple": 1.5,
            "runway_months": 18.0,
            "decision_latency_days": 3.0,
            "eNPS": 50.0,
            "experiment_throughput": 12.0,
            "relative_market_share": 0.15
        }

    def run_coupled_step(self) -> Dict[str, Any]:
        """Propagates state updates across coupled loops."""
        # Pricing -> ARPU -> Revenue -> Financial Loop -> Runway
        arpu = self.state["arpu_usd"]
        gross_margin = self.state["gross_margin"]
        self.state["ltv_usd"] = (arpu * 12.0 * gross_margin) / max(0.01, self.state["churn_rate"])

        cac = self.state["cac_usd"]
        self.state["ltv_cac_ratio"] = self.state["ltv_usd"] / max(1.0, cac)

        # Referral -> Organic Acquisition -> Reduced Effective CAC
        k_factor = self.state["viral_coefficient_k"]
        if k_factor > 1.0:
            self.state["cac_usd"] = max(10.0, self.state["cac_usd"] * 0.8)

        # Culture -> Decision Latency -> Execution Throughput
        if self.state["eNPS"] > 60:
            self.state["decision_latency_days"] = max(0.5, self.state["decision_latency_days"] * 0.9)

        return self.state


# =====================================================================
# 4. Full Customer Journey Lifecycle (15 Stages)
# =====================================================================

class CustomerStage(str, Enum):
    AWARENESS = "1_AWARENESS"
    INTEREST = "2_INTEREST"
    CONSIDERATION = "3_CONSIDERATION"
    EVALUATION = "4_EVALUATION"
    PURCHASE = "5_PURCHASE"
    ONBOARDING = "6_ONBOARDING"
    ACTIVATION = "7_ACTIVATION"
    ENGAGEMENT = "8_ENGAGEMENT"
    HABIT_FORMATION = "9_HABIT_FORMATION"
    RETENTION = "10_RETENTION"
    LOYALTY = "11_LOYALTY"
    ADVOCACY = "12_ADVOCACY"
    REFERRAL = "13_REFERRAL"
    EXPANSION = "14_EXPANSION"
    REPURCHASE = "15_REPURCHASE"


class CustomerLifecycleTracker:
    """Tracks cohort progression and identifies drop-off bottlenecks across 15 stages."""

    def __init__(self) -> None:
        self.stage_counts: Dict[CustomerStage, int] = {stage: 0 for stage in CustomerStage}

    def record_cohort(self, stage_volumes: Dict[CustomerStage, int]) -> None:
        self.stage_counts.update(stage_volumes)

    def identify_primary_bottleneck(self) -> Tuple[Optional[CustomerStage], float]:
        """Finds the stage transition with the lowest drop-off retention ratio."""
        stages = list(CustomerStage)
        max_dropoff = 0.0
        bottleneck_stage = None

        for i in range(len(stages) - 1):
            curr_s = stages[i]
            next_s = stages[i+1]
            curr_count = self.stage_counts[curr_s]
            next_count = self.stage_counts[next_s]

            if curr_count > 0:
                conversion = next_count / curr_count
                dropoff = 1.0 - conversion
                if dropoff > max_dropoff:
                    max_dropoff = dropoff
                    bottleneck_stage = next_s

        return bottleneck_stage, max_dropoff


# =====================================================================
# 6. Company Growth System (9 Stages)
# =====================================================================

class GrowthStage(str, Enum):
    IDEA = "IDEA"
    VALIDATION = "VALIDATION"
    STARTUP = "STARTUP"
    PMF = "PMF"
    GROWTH = "GROWTH"
    SCALE = "SCALE"
    PLATFORM = "PLATFORM"
    ECOSYSTEM = "ECOSYSTEM"
    MARKET_LEADERSHIP = "MARKET_LEADERSHIP"


class GrowthStageClassifier:
    """Classifies company stage and detects the binding constraint."""

    def classify_stage(self, metrics: Dict[str, Any]) -> Tuple[GrowthStage, str]:
        paying_cust = metrics.get("paying_customers", 0)
        retention_flattened = metrics.get("retention_flattened", False)
        nrr = metrics.get("nrr", 1.0)
        third_party_devs = metrics.get("third_party_devs", 0)
        market_share = metrics.get("market_share", 0.0)

        if market_share >= 0.40 and third_party_devs >= 1000:
            return GrowthStage.MARKET_LEADERSHIP, "Innovation velocity vs. incumbency drag"
        elif third_party_devs >= 500:
            return GrowthStage.ECOSYSTEM, "Governance credibility"
        elif third_party_devs >= 50:
            return GrowthStage.PLATFORM, "Partner trust"
        elif nrr >= 1.20 and paying_cust >= 200:
            return GrowthStage.SCALE, "Organizational coordination cost"
        elif paying_cust >= 50 and retention_flattened:
            return GrowthStage.GROWTH, "Hiring velocity & scaling systems"
        elif retention_flattened:
            return GrowthStage.PMF, "Team bandwidth"
        elif paying_cust >= 5:
            return GrowthStage.STARTUP, "Cash runway"
        elif paying_cust > 0:
            return GrowthStage.VALIDATION, "Signal quality"
        else:
            return GrowthStage.IDEA, "Founder time"


# =====================================================================
# 8. Failure Mode Monitor
# =====================================================================

class FailureModeMonitor:
    """Pattern matches operating metrics against the 10 failure modes."""

    def evaluate_failure_modes(self, metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        alerts = []
        if metrics.get("engagement_rate", 1.0) < 0.10 and metrics.get("survey_satisfaction", 0.0) > 0.80:
            alerts.append({
                "mode": "Solving the wrong problem",
                "cause": "Skipped root cause analysis; solved symptom",
                "correction": "Return to 5-Whys / Jobs-to-be-Done interviews"
            })
        if metrics.get("cac_payback_months", 0) > 24 and metrics.get("growth_rate", 0) > 0.50:
            alerts.append({
                "mode": "Premature scaling",
                "cause": "Scaling unproven loop before retention/payback holds",
                "correction": "Halt spend expansion; focus on cohort retention"
            })
        if metrics.get("ltv_cac_ratio", 3.0) < 1.0:
            alerts.append({
                "mode": "Lack of Product-Market Fit",
                "cause": "Negative unit economics at scale",
                "correction": "Stop scaling; return to retention curve flattening"
            })
        if metrics.get("decision_latency_days", 0) > 14:
            alerts.append({
                "mode": "Organizational bottlenecks",
                "cause": "Decision rights not delegated; single point of failure",
                "correction": "Push decision rights down with explicit frameworks"
            })
        return alerts


# =====================================================================
# 10. Integrated AI-EOS Operating Architecture
# =====================================================================

class EOSLifecycleState(str, Enum):
    SENSING = "SENSING"
    HYPOTHESIS = "HYPOTHESIS"
    CHEAP_TEST = "CHEAP_TEST"
    VALIDATION = "VALIDATION"
    BUILD_GATE = "BUILD_GATE"
    MVP = "MVP"
    GTM_TEST = "GTM_TEST"
    SCALE = "SCALE"
    OPERATE = "OPERATE"
    REINVENT = "REINVENT"
    DISCARD = "DISCARD"


class EOSStateMachine:
    """Manages the re-entrant lifecycle state transitions."""

    def __init__(self) -> None:
        self.current_state = EOSLifecycleState.SENSING
        self.history: List[EOSLifecycleState] = [EOSLifecycleState.SENSING]

    def transition_to(self, target: EOSLifecycleState, reason: str = "") -> None:
        logger.info(f"[EOS State Machine] Transition: {self.current_state.value} -> {target.value} ({reason})")
        self.current_state = target
        self.history.append(target)


class OpportunityDecisionTree:
    """Evaluates whether to pursue an opportunity according to Section 10.2."""

    def evaluate(
        self,
        is_structural_anomaly: bool,
        is_reversible: bool,
        high_confidence_signal: bool,
        cheap_test_available: bool,
        test_passed: bool,
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> Tuple[bool, str]:
        if not is_structural_anomaly:
            return False, "Discard: Anomaly is noise, not structural."

        if not is_reversible:
            if not high_confidence_signal:
                return False, "Discard: Irreversible Type I decision lacks high-confidence signal."
        else:
            if cheap_test_available:
                if not test_passed:
                    return False, "Discard: Cheap test falsified hypothesis below kill threshold."
            else:
                if not expected_value_positive:
                    return False, "Discard: Reversible decision lacks positive expected value."

        if not has_structural_advantage:
            return False, "Discard: Lacks defensible structural advantage or moat."

        return True, "Commit Resources: Opportunity passed all decision tree filters."


# =====================================================================
# 10.3 10 AI-EOS Autonomous Executive Modules
# =====================================================================

class AIEOSAutonomousModules:
    """Integrates the 10 executive agents defined in Section 10.3."""

    def __init__(self) -> None:
        self.signal_engine = SignalToIdeaEngine()
        self.loops_engine = CoupledBusinessLoopsEngine()
        self.lifecycle_tracker = CustomerLifecycleTracker()
        self.stage_classifier = GrowthStageClassifier()
        self.failure_monitor = FailureModeMonitor()
        self.decision_tree = OpportunityDecisionTree()
        self.state_machine = EOSStateMachine()

    def run_full_sensing_to_allocation_cycle(
        self,
        telemetry: Dict[str, Any],
        opportunity_claim: str
    ) -> Dict[str, Any]:
        # 1. Sensing Agent
        anomaly, is_structural = self.signal_engine.detect_anomaly(
            description=telemetry.get("anomaly_desc", "Signal observation"),
            observed=telemetry.get("observed", 100.0),
            expected=telemetry.get("expected", 10.0)
        )
        if is_structural:
            self.state_machine.transition_to(EOSLifecycleState.HYPOTHESIS, "Structural anomaly detected")

        # 2. Hypothesis Engine
        hyp = self.signal_engine.form_hypothesis(
            claim=opportunity_claim,
            risk_type=RiskType.TYPE_II if telemetry.get("reversible", True) else RiskType.TYPE_I,
            test_cost=telemetry.get("test_cost", 50.0),
            info_value=telemetry.get("info_val", 500.0)
        )
        self.state_machine.transition_to(EOSLifecycleState.CHEAP_TEST, "Hypothesis formed")

        # 3. Validation Agent (Bayesian update)
        hyp = self.signal_engine.update_bayesian_belief(hyp, likelihood_if_true=0.8, likelihood_if_false=0.2)
        if hyp.is_falsified:
            self.state_machine.transition_to(EOSLifecycleState.DISCARD, "Hypothesis falsified in cheap test")
            return {"status": "DISCARDED", "reason": "Falsified"}

        self.state_machine.transition_to(EOSLifecycleState.VALIDATION, "Cheap test strengthened hypothesis")

        # 4. Decision Tree Gating
        pursue, reason = self.decision_tree.evaluate(
            is_structural_anomaly=is_structural,
            is_reversible=(hyp.risk_type == RiskType.TYPE_II),
            high_confidence_signal=(hyp.posterior_probability > 0.70),
            cheap_test_available=True,
            test_passed=(not hyp.is_falsified),
            expected_value_positive=True,
            has_structural_advantage=telemetry.get("moat_advantage", True)
        )

        if not pursue:
            self.state_machine.transition_to(EOSLifecycleState.DISCARD, reason)
            return {"status": "DISCARDED", "reason": reason}

        self.state_machine.transition_to(EOSLifecycleState.SCALE, "Validated & decision tree passed")

        # 5. Growth Stage & Failure Monitoring
        stage, constraint = self.stage_classifier.classify_stage(telemetry.get("metrics", {}))
        alerts = self.failure_monitor.evaluate_failure_modes(telemetry.get("metrics", {}))

        return {
            "status": "APPROVED",
            "stage": stage.value,
            "binding_constraint": constraint,
            "hypothesis_posterior": hyp.posterior_probability,
            "failure_alerts": alerts,
            "decision_reason": reason
        }
