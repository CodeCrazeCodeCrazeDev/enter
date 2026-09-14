"""First-Principles Entrepreneurial Operating System (EOS) Module.

Provides mathematical and state-machine models for:
- Multi-timescale loops (Fast, Medium, Slow)
- 11-State System Lifecycle State Machine
- 5-Node Opportunity Decision Tree
- 13 Coupled External Business Loops
- 15-Stage Customer Journey Lifecycle
- 9-Stage Venture Growth Matrix & Classifier
- 10 Operating Failure Mode Monitors & Automated Corrections
- 7 Powers / Moat Durability Analysis
- First-Principles EOS Orchestrator Engine
"""

from __future__ import annotations
import math
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger("sero.eos_first_principles")


# =====================================================================
# Enums and Core Data Models
# =====================================================================

class SystemState(str, Enum):
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


class CustomerStage(str, Enum):
    AWARENESS = "Awareness"
    INTEREST = "Interest"
    CONSIDERATION = "Consideration"
    EVALUATION = "Evaluation"
    PURCHASE = "Purchase"
    ONBOARDING = "Onboarding"
    ACTIVATION = "Activation"
    ENGAGEMENT = "Engagement"
    HABIT_FORMATION = "Habit Formation"
    RETENTION = "Retention"
    LOYALTY = "Loyalty"
    ADVOCACY = "Advocacy"
    REFERRAL = "Referral"
    EXPANSION = "Expansion"
    REPURCHASE = "Repurchase"


class VentureGrowthStage(str, Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "PMF"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    MARKET_LEADERSHIP = "Market Leadership"


class FailureModeType(str, Enum):
    SOLVING_WRONG_PROBLEM = "Solving Wrong Problem"
    BUILDING_WITHOUT_VALIDATING = "Building Before Validating"
    WEAK_POSITIONING = "Weak Positioning"
    POOR_PRICING = "Poor Pricing"
    DISTRIBUTION_FAILURE = "Distribution Failure"
    LACK_OF_PMF = "Lack of Product-Market Fit"
    ORGANIZATIONAL_BOTTLENECK = "Organizational Bottlenecks"
    FOUNDER_BIAS = "Founder Bias"
    PREMATURE_SCALING = "Scaling Prematurely"
    CAPITAL_MISALLOCATION = "Capital Misallocation"


@dataclass
class AnomalySignal:
    signal_id: UUID = field(default_factory=uuid4)
    description: str = ""
    is_structural: bool = False
    confidence: float = 0.0
    detected_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class OpportunityCandidate:
    opportunity_id: UUID = field(default_factory=uuid4)
    name: str = ""
    is_structural_anomaly: bool = True
    is_reversible: bool = True
    multi_source_confidence: float = 0.5
    cheap_test_available: bool = True
    cheap_test_score: float = 0.0
    cheap_test_kill_threshold: float = 0.5
    expected_value_positive: bool = True
    has_structural_advantage: bool = False


@dataclass
class FailureAlert:
    failure_type: FailureModeType
    root_cause: str
    detection_signal: str
    recommended_correction: str
    severity: float  # [0.0, 1.0]


# =====================================================================
# 1. 11-State System State Machine
# =====================================================================

class EOSStateMachine:
    """Manages state transitions across the 11-state lifecycle of an EOS venture idea."""

    VALID_TRANSITIONS: Dict[SystemState, Set[SystemState]] = {
        SystemState.SENSING: {SystemState.HYPOTHESIS},
        SystemState.HYPOTHESIS: {SystemState.CHEAP_TEST, SystemState.DISCARD},
        SystemState.CHEAP_TEST: {SystemState.VALIDATION, SystemState.DISCARD},
        SystemState.VALIDATION: {SystemState.BUILD_GATE, SystemState.DISCARD},
        SystemState.BUILD_GATE: {SystemState.MVP, SystemState.DISCARD},
        SystemState.MVP: {SystemState.GTM_TEST},
        SystemState.GTM_TEST: {SystemState.KILL_OR_SCALE},
        SystemState.KILL_OR_SCALE: {SystemState.SCALE, SystemState.DISCARD},
        SystemState.SCALE: {SystemState.OPERATE},
        SystemState.OPERATE: {SystemState.REINVENT},
        SystemState.REINVENT: {SystemState.SENSING},
        SystemState.DISCARD: {SystemState.SENSING},
    }

    def __init__(self, initial_state: SystemState = SystemState.SENSING) -> None:
        self.current_state: SystemState = initial_state
        self.history: List[Tuple[SystemState, datetime]] = [(initial_state, datetime.utcnow())]

    def transition(self, next_state: SystemState) -> bool:
        allowed = self.VALID_TRANSITIONS.get(self.current_state, set())
        if next_state not in allowed:
            logger.warning(f"Invalid transition attempted: {self.current_state.value} -> {next_state.value}")
            return False
        self.current_state = next_state
        self.history.append((next_state, datetime.utcnow()))
        logger.info(f"EOS State Machine transitioned to: {next_state.value}")
        return True


# =====================================================================
# 2. Opportunity Decision Tree Evaluator
# =====================================================================

class OpportunityDecisionTree:
    """Evaluates whether an opportunity should be pursued based on the §10.2 Decision Tree."""

    def evaluate(self, candidate: OpportunityCandidate) -> Tuple[bool, str]:
        # Q1: Structural anomaly or noise?
        if not candidate.is_structural_anomaly:
            return False, "Discarded at Q1: Signal classified as noise, not structural anomaly."

        # Q2: Reversible decision? (Type I vs Type II)
        if not candidate.is_reversible:
            # Irreversible (Type I): Requires high-confidence multi-source signal
            if candidate.multi_source_confidence < 0.70:
                return False, "Discarded at Q2a: Irreversible decision lacking high-confidence multi-source signal (<0.70)."

        # Q3: Cheap test available?
        if candidate.cheap_test_available:
            if candidate.cheap_test_score <= candidate.cheap_test_kill_threshold:
                return False, f"Discarded at Q4: Cheap test score ({candidate.cheap_test_score:.2f}) failed kill threshold ({candidate.cheap_test_kill_threshold:.2f})."
        else:
            if not candidate.expected_value_positive:
                return False, "Discarded at Q4b: No cheap test available and Expected Value is not clearly positive."

        # Q5: Do we have or can we build a structural advantage?
        if not candidate.has_structural_advantage:
            return False, "Discarded at Q5: Lack of defensible structural advantage or moat."

        return True, "Approved: Opportunity satisfies all decision tree criteria; commit capital and resources."


# =====================================================================
# 3. 13 Coupled External Business Loops Engine
# =====================================================================

class CoupledBusinessLoopsEngine:
    """Simulates interactions across all 13 business loops and calculates systemic stock-and-flow propagation."""

    def __init__(self) -> None:
        self.loop_states: Dict[str, Dict[str, float]] = {
            "Product": {"activation": 0.30, "retention_30d": 0.25, "nps": 40.0},
            "Marketing": {"cac_cents": 15000, "conversion_rate": 0.03, "brand_recall": 0.15},
            "Sales": {"win_rate": 0.20, "sales_cycle_days": 60.0, "acv_cents": 500000},
            "Customer Success": {"nrr": 1.05, "churn_rate": 0.05, "ttv_days": 14.0},
            "Brand": {"share_of_voice": 0.10, "trust_score": 0.60},
            "Pricing": {"arpu_cents": 10000, "price_realization": 0.85},
            "Referral": {"viral_k_factor": 0.20, "referral_cac_cents": 3000},
            "Data": {"latency_sec": 120.0, "decision_cycle_hours": 24.0},
            "Financial": {"gross_margin": 0.75, "burn_multiple": 1.5, "runway_months": 18.0},
            "Hiring": {"time_to_fill_days": 45.0, "regretted_attrition": 0.05},
            "Culture": {"enps": 35.0, "decision_latency_hours": 12.0},
            "Innovation": {"experiment_velocity": 4.0, "hit_rate": 0.15},
            "Competitive Intel": {"feature_parity": 0.80, "relative_share": 0.12},
        }

    def step_simulation(self, product_quality_delta: float, marketing_spend_cents: int) -> Dict[str, Any]:
        """Propagate coupled loop dynamics across stocks and flows."""
        # Product quality improves activation & retention
        self.loop_states["Product"]["activation"] = min(0.95, self.loop_states["Product"]["activation"] + product_quality_delta * 0.1)
        self.loop_states["Product"]["retention_30d"] = min(0.90, self.loop_states["Product"]["retention_30d"] + product_quality_delta * 0.08)

        # Retention feeds Customer Success NRR & Referral viral K factor
        ret = self.loop_states["Product"]["retention_30d"]
        self.loop_states["Customer Success"]["nrr"] = 0.80 + ret * 0.80
        self.loop_states["Referral"]["viral_k_factor"] = max(0.05, ret * 0.60)

        # Marketing spend impacts CAC and Brand share of voice
        if marketing_spend_cents > 100000_00:
            self.loop_states["Marketing"]["cac_cents"] = int(self.loop_states["Marketing"]["cac_cents"] * 1.05)  # Diminishing returns
            self.loop_states["Brand"]["share_of_voice"] = min(0.80, self.loop_states["Brand"]["share_of_voice"] + 0.02)

        # Calculated LTV / CAC
        arpu = self.loop_states["Pricing"]["arpu_cents"]
        churn = max(0.01, self.loop_states["Customer Success"]["churn_rate"])
        ltv_cents = int(arpu / churn)
        cac = max(1, self.loop_states["Marketing"]["cac_cents"])
        ltv_to_cac = ltv_cents / cac

        return {
            "ltv_cents": ltv_cents,
            "ltv_to_cac": ltv_to_cac,
            "viral_k_factor": self.loop_states["Referral"]["viral_k_factor"],
            "nrr": self.loop_states["Customer Success"]["nrr"],
            "loop_states": self.loop_states,
        }


# =====================================================================
# 4. 15-Stage Customer Journey Engine
# =====================================================================

class CustomerLifecycleEngine:
    """Tracks conversion and friction across the 15 stages of the customer journey."""

    STAGE_ORDER: List[CustomerStage] = list(CustomerStage)

    def __init__(self) -> None:
        # Default cohort funnel stage counts
        self.funnel_counts: Dict[CustomerStage, int] = {
            stage: 1000 if i == 0 else 0 for i, stage in enumerate(self.STAGE_ORDER)
        }

    def simulate_funnel(self, conversion_rates: Optional[Dict[CustomerStage, float]] = None) -> Dict[CustomerStage, int]:
        """Simulate cohort progression through all 15 stages."""
        defaults = {
            CustomerStage.AWARENESS: 1.0,
            CustomerStage.INTEREST: 0.35,
            CustomerStage.CONSIDERATION: 0.50,
            CustomerStage.EVALUATION: 0.60,
            CustomerStage.PURCHASE: 0.40,
            CustomerStage.ONBOARDING: 0.85,
            CustomerStage.ACTIVATION: 0.70,
            CustomerStage.ENGAGEMENT: 0.80,
            CustomerStage.HABIT_FORMATION: 0.65,
            CustomerStage.RETENTION: 0.85,
            CustomerStage.LOYALTY: 0.60,
            CustomerStage.ADVOCACY: 0.40,
            CustomerStage.REFERRAL: 0.30,
            CustomerStage.EXPANSION: 0.25,
            CustomerStage.REPURCHASE: 0.75,
        }
        if conversion_rates:
            defaults.update(conversion_rates)

        current_cohort = 10000
        for stage in self.STAGE_ORDER:
            rate = defaults.get(stage, 0.50)
            current_cohort = int(current_cohort * rate)
            self.funnel_counts[stage] = current_cohort

        return self.funnel_counts

    def identify_bottleneck_stage(self) -> Tuple[CustomerStage, float]:
        """Find the stage with the lowest retention/conversion delta."""
        min_stage = CustomerStage.PURCHASE
        min_ratio = 1.0

        for i in range(1, len(self.STAGE_ORDER)):
            prev_stage = self.STAGE_ORDER[i - 1]
            curr_stage = self.STAGE_ORDER[i]
            prev_cnt = max(1, self.funnel_counts[prev_stage])
            curr_cnt = self.funnel_counts[curr_stage]
            ratio = curr_cnt / prev_cnt
            if ratio < min_ratio:
                min_ratio = ratio
                min_stage = curr_stage

        return min_stage, min_ratio


# =====================================================================
# 5. 9-Stage Growth Classifier
# =====================================================================

class GrowthStageClassifier:
    """Scores a venture against criteria across the 9 growth stages to prevent premature scaling."""

    def classify_stage(
        self,
        paying_customers: int,
        retention_curve_flattened: bool,
        yoy_growth_rate: float,
        rule_of_40: float,
        has_ecosystem_developers: bool
    ) -> VentureGrowthStage:
        if paying_customers == 0:
            return VentureGrowthStage.IDEA
        if paying_customers < 10 and not retention_curve_flattened:
            return VentureGrowthStage.VALIDATION
        if paying_customers >= 10 and not retention_curve_flattened:
            return VentureGrowthStage.STARTUP
        if has_ecosystem_developers:
            if yoy_growth_rate >= 1.0:
                return VentureGrowthStage.ECOSYSTEM
            return VentureGrowthStage.PLATFORM
        if rule_of_40 >= 0.30:
            return VentureGrowthStage.SCALE
        if yoy_growth_rate >= 0.50:
            return VentureGrowthStage.GROWTH
        if retention_curve_flattened:
            return VentureGrowthStage.PMF

        return VentureGrowthStage.MARKET_LEADERSHIP


# =====================================================================
# 6. Moat & Hamilton Helmer 7 Powers Analyzer
# =====================================================================

class MoatAnalyzer:
    """Quantifies structural competitive advantages across the 7 Powers."""

    def calculate_7powers_score(
        self,
        network_density: float,
        switching_cost_cents: int,
        cornered_resource_uniqueness: float,
        counter_positioning_delta: float,
        scale_cost_advantage: float,
        process_power_efficiency: float,
        brand_trust_score: float
    ) -> Dict[str, float]:
        scores = {
            "network_effects": min(1.0, network_density),
            "switching_costs": min(1.0, switching_cost_cents / 10000_00),
            "cornered_resource": min(1.0, cornered_resource_uniqueness),
            "counter_positioning": min(1.0, counter_positioning_delta),
            "scale_economies": min(1.0, scale_cost_advantage),
            "process_power": min(1.0, process_power_efficiency),
            "brand": min(1.0, brand_trust_score),
        }
        composite_moat_score = sum(scores.values()) / len(scores)
        scores["composite_moat_score"] = composite_moat_score
        return scores


# =====================================================================
# 7. Failure Mode Monitor
# =====================================================================

class FailureModeMonitor:
    """Pattern-matches operational telemetry against the 10 core failure modes."""

    def evaluate_telemetry(self, metrics: Dict[str, Any]) -> List[FailureAlert]:
        alerts: List[FailureAlert] = []

        # 1. Solving wrong problem
        if metrics.get("survey_satisfaction", 0.0) > 0.8 and metrics.get("retention_30d", 0.0) < 0.15:
            alerts.append(FailureAlert(
                failure_type=FailureModeType.SOLVING_WRONG_PROBLEM,
                root_cause="Skipped root-cause analysis; solved symptom instead of actual job-to-be-done.",
                detection_signal="High survey scores coexisting with zero usage retention.",
                recommended_correction="Return to 5-Whys and Jobs-to-be-Done customer interviews.",
                severity=0.85
            ))

        # 2. Building before validating
        if metrics.get("commit_velocity", 0) > 50 and metrics.get("active_users", 0) < 10:
            alerts.append(FailureAlert(
                failure_type=FailureModeType.BUILDING_WITHOUT_VALIDATING,
                root_cause="Founder conviction substituted for empirical validation.",
                detection_signal="High build/dev velocity with flat user demand signal.",
                recommended_correction="Impose mandatory pre-build validation gate.",
                severity=0.90
            ))

        # 3. Lack of Product-Market Fit
        if metrics.get("retention_curve_flattened") is False and metrics.get("monthly_ad_spend_cents", 0) > 50000_00:
            alerts.append(FailureAlert(
                failure_type=FailureModeType.LACK_OF_PMF,
                root_cause="Premature scaling of an unproven, leaking funnel.",
                detection_signal="Retention curve never flattens despite scaling acquisition spend.",
                recommended_correction="Freeze growth spend; return to cohort retention optimization.",
                severity=0.95
            ))

        # 4. Premature scaling
        cac = metrics.get("cac_cents", 1)
        ltv = metrics.get("ltv_cents", 0)
        if metrics.get("growth_rate", 0.0) > 0.50 and (ltv / max(1, cac)) < 2.0:
            alerts.append(FailureAlert(
                failure_type=FailureModeType.PREMATURE_SCALING,
                root_cause="Confusing early demand spike with durable PMF under negative unit economics.",
                detection_signal="CAC rising faster than LTV as acquisition scales.",
                recommended_correction="Re-test unit economics per order of magnitude of spend.",
                severity=0.90
            ))

        return alerts


# =====================================================================
# 8. First-Principles EOS Engine (Orchestrator)
# =====================================================================

class FirstPrinciplesEOSEngine:
    """Master Orchestrator integrating all state machine, decision tree, loop, and monitor components."""

    def __init__(self) -> None:
        self.state_machine = EOSStateMachine()
        self.decision_tree = OpportunityDecisionTree()
        self.coupled_loops = CoupledBusinessLoopsEngine()
        self.customer_lifecycle = CustomerLifecycleEngine()
        self.growth_classifier = GrowthStageClassifier()
        self.moat_analyzer = MoatAnalyzer()
        self.failure_monitor = FailureModeMonitor()

    def run_cycle(self, candidate: OpportunityCandidate, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one complete sensing, decision, simulation, and diagnostic cycle."""
        # Decision tree check
        approved, reason = self.decision_tree.evaluate(candidate)

        if approved and self.state_machine.current_state == SystemState.SENSING:
            self.state_machine.transition(SystemState.HYPOTHESIS)

        # Coupled loop propagation
        loop_results = self.coupled_loops.step_simulation(
            product_quality_delta=telemetry.get("product_quality_delta", 0.1),
            marketing_spend_cents=telemetry.get("marketing_spend_cents", 50000_00)
        )

        # Customer lifecycle simulation
        funnel = self.customer_lifecycle.simulate_funnel()
        bottleneck, ratio = self.customer_lifecycle.identify_bottleneck_stage()

        # Growth classification
        growth_stage = self.growth_classifier.classify_stage(
            paying_customers=telemetry.get("paying_customers", 15),
            retention_curve_flattened=telemetry.get("retention_curve_flattened", True),
            yoy_growth_rate=telemetry.get("yoy_growth_rate", 0.60),
            rule_of_40=telemetry.get("rule_of_40", 0.35),
            has_ecosystem_developers=telemetry.get("has_ecosystem_developers", False)
        )

        # Moat evaluation
        moat_scores = self.moat_analyzer.calculate_7powers_score(
            network_density=telemetry.get("network_density", 0.40),
            switching_cost_cents=telemetry.get("switching_cost_cents", 5000_00),
            cornered_resource_uniqueness=telemetry.get("cornered_resource_uniqueness", 0.70),
            counter_positioning_delta=telemetry.get("counter_positioning_delta", 0.80),
            scale_cost_advantage=telemetry.get("scale_cost_advantage", 0.30),
            process_power_efficiency=telemetry.get("process_power_efficiency", 0.50),
            brand_trust_score=telemetry.get("brand_trust_score", 0.65)
        )

        # Failure mode monitoring
        failure_alerts = self.failure_monitor.evaluate_telemetry(telemetry)

        return {
            "current_system_state": self.state_machine.current_state.value,
            "opportunity_approved": approved,
            "decision_reason": reason,
            "growth_stage": growth_stage.value,
            "funnel_bottleneck": bottleneck.value,
            "funnel_bottleneck_ratio": ratio,
            "composite_moat_score": moat_scores["composite_moat_score"],
            "failure_alerts_count": len(failure_alerts),
            "failure_alerts": failure_alerts,
            "coupled_loops": loop_results,
        }
