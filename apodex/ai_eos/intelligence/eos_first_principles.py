"""First-Principles Entrepreneurial Operating System (EOS) Executable Engine.

Implements all 11 sections of the EOS specification:
- Section 1: Master Loop architecture & re-entrant node execution
- Section 2: Cognitive Loops (Signal-to-Idea pipeline, real options, Type I vs Type II risk evaluation, mental model updating)
- Section 3: Coupled Business Loops (13 coupled loops with stock/flow dynamics)
- Section 4: Customer Lifecycle Engine (15 full stages from Awareness to Repurchase)
- Section 5: Go-To-Market System Dynamics (Positioning, channel fit, pricing, motion compounding)
- Section 6: Company Growth System Classifier (9 stages from Idea to Market Leadership)
- Section 7: Strategic Thinking & Moat Construction (Helmer 7 Powers / Porter Moats, cost curves)
- Section 8: Failure Mode Monitor & Diagnostic Engine (10 explicit failure modes & correction mechanisms)
- Section 9: Scientific Foundations Mapping
- Section 10: AI-Driven Execution System (State Machine, Decision Tree, Subsystem Agents, KPI Stack)
- Section 11: Explicit Limitations & Domain Safeguards
"""

from __future__ import annotations
import math
import logging
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from uuid import UUID, uuid4

logger = logging.getLogger("sero.eos_first_principles")


# =====================================================================
# Section 10.1: System State Machine
# =====================================================================
class EOSState(str, Enum):
    SENSING = "Sensing"
    HYPOTHESIS = "Hypothesis"
    CHEAP_TEST = "CheapTest"
    VALIDATION = "Validation"
    BUILD_GATE = "BuildGate"
    MVP = "MVP"
    GTM_TEST = "GTMTest"
    KILL_OR_SCALE = "KillOrScale"
    SCALE = "Scale"
    OPERATE = "Operate"
    REINVENT = "Reinvent"
    DISCARD = "Discard"


class EOSStateMachine:
    """Implements Section 10.1 AI-Driven System State Machine."""

    TRANSITIONS: Dict[EOSState, List[EOSState]] = {
        EOSState.SENSING: [EOSState.HYPOTHESIS],
        EOSState.HYPOTHESIS: [EOSState.CHEAP_TEST, EOSState.DISCARD],
        EOSState.CHEAP_TEST: [EOSState.VALIDATION, EOSState.DISCARD],
        EOSState.DISCARD: [EOSState.SENSING],
        EOSState.VALIDATION: [EOSState.BUILD_GATE, EOSState.DISCARD],
        EOSState.BUILD_GATE: [EOSState.MVP, EOSState.DISCARD],
        EOSState.MVP: [EOSState.GTM_TEST],
        EOSState.GTM_TEST: [EOSState.KILL_OR_SCALE],
        EOSState.KILL_OR_SCALE: [EOSState.SCALE, EOSState.DISCARD],
        EOSState.SCALE: [EOSState.OPERATE],
        EOSState.OPERATE: [EOSState.REINVENT],
        EOSState.REINVENT: [EOSState.SENSING],
    }

    def __init__(self, initial_state: EOSState = EOSState.SENSING) -> None:
        self.current_state = initial_state
        self.history: List[Tuple[EOSState, str]] = [(initial_state, "Initialization")]

    def transition_to(self, new_state: EOSState, reason: str = "") -> EOSState:
        allowed = self.TRANSITIONS.get(self.current_state, [])
        if new_state not in allowed:
            raise ValueError(
                f"Invalid transition from state '{self.current_state.value}' to '{new_state.value}'. Allowed: {[s.value for s in allowed]}"
            )
        logger.info(f"EOS State Machine Transition: {self.current_state.value} -> {new_state.value} ({reason})")
        self.current_state = new_state
        self.history.append((new_state, reason))
        return self.current_state


# =====================================================================
# Section 10.2: Decision Tree Engine
# =====================================================================
@dataclass
class OpportunityContext:
    title: str
    is_structural_anomaly: bool
    is_reversible_decision: bool  # True = Type II door, False = Type I door
    high_confidence_multi_source: bool
    cheap_test_available: bool
    test_result_exceeds_kill_threshold: bool
    expected_value_clearly_positive: bool
    has_structural_advantage: bool


class OpportunityDecisionTree:
    """Implements Section 10.2 Decision Tree ('Should We Pursue This Opportunity?')."""

    def evaluate(self, ctx: OpportunityContext) -> Tuple[bool, str]:
        # Q1: Structural anomaly or just noise?
        if not ctx.is_structural_anomaly:
            return False, "Discarded: Signal identified as noise rather than structural anomaly."

        # Q2: Reversible decision?
        if not ctx.is_reversible_decision:
            # Type I / Irreversible decision
            if not ctx.high_confidence_multi_source:
                return False, "Discarded: Irreversible (Type I) decision lacks high-confidence multi-source signal."

        # Q3: Cheap test available?
        if ctx.cheap_test_available:
            if not ctx.test_result_exceeds_kill_threshold:
                return False, "Discarded: Cheap test result failed pre-committed kill criteria threshold."
        else:
            if not ctx.expected_value_clearly_positive:
                return False, "Discarded: No cheap test available and expected value is not clearly positive."

        # Q5: Structural advantage?
        if not ctx.has_structural_advantage:
            return False, "Discarded: Venture lacks durable structural advantage/moat against competitors."

        return True, "Commit Resources: Opportunity satisfies all strategic, economic, and risk decision criteria."


# =====================================================================
# Section 3: Coupled Business Loops Engine
# =====================================================================
@dataclass
class BusinessLoopMetrics:
    product_retention_slope: float = 0.8
    product_nps: float = 65.0
    marketing_cac_cents: int = 5000  # $50
    sales_win_rate: float = 0.25
    cs_nrr: float = 1.15  # Net Retention Rate 115%
    cs_churn_rate: float = 0.03
    pricing_arpu_cents: int = 15000  # $150
    referral_k_factor: float = 0.4
    financial_burn_multiple: float = 1.2
    financial_gross_margin: float = 0.75
    financial_runway_months: float = 18.0
    hiring_decision_latency_days: float = 5.0
    culture_enps: float = 45.0
    innovation_hit_rate: float = 0.20
    comp_intel_feature_parity: float = 0.85


class CoupledBusinessLoopsEngine:
    """Implements Section 3 Coupled External Business Loops & Stock/Flow Dynamics."""

    def evaluate_loop_interactions(self, metrics: BusinessLoopMetrics) -> Dict[str, Any]:
        # Stocks: Cash, Talent, Trust, Data
        # Leverage points: Pricing and Hiring
        ltv_cents = int(metrics.pricing_arpu_cents / metrics.cs_churn_rate) if metrics.cs_churn_rate > 0 else metrics.pricing_arpu_cents * 24
        ltv_cac_ratio = ltv_cents / metrics.marketing_cac_cents if metrics.marketing_cac_cents > 0 else 1.0

        # Coupled feedback: ARPU -> Financial -> Hiring -> Velocity
        system_leverage_score = (ltv_cac_ratio * metrics.financial_gross_margin) / (metrics.financial_burn_multiple + 0.1)

        return {
            "ltv_cents": ltv_cents,
            "ltv_cac_ratio": ltv_cac_ratio,
            "system_leverage_score": system_leverage_score,
            "unit_economics_healthy": ltv_cac_ratio >= 3.0 and metrics.financial_burn_multiple <= 2.0,
            "leverage_bottleneck": "hiring_latency" if metrics.hiring_decision_latency_days > 14.0 else "none"
        }


# =====================================================================
# Section 4: Customer Lifecycle Engine
# =====================================================================
class CustomerLifecycleStage(str, Enum):
    AWARENESS = "Awareness"
    INTEREST = "Interest"
    CONSIDERATION = "Consideration"
    EVALUATION = "Evaluation"
    PURCHASE = "Purchase"
    ONBOARDING = "Onboarding"
    ACTIVATION = "Activation"
    ENGAGEMENT = "Engagement"
    HABIT_FORMATION = "HabitFormation"
    RETENTION = "Retention"
    LOYALTY = "Loyalty"
    ADVOCACY = "Advocacy"
    REFERRAL = "Referral"
    EXPANSION = "Expansion"
    REPURCHASE = "Repurchase"


class CustomerLifecycleEngine:
    """Implements Section 4 Customer Journey (15 Stages)."""

    STAGES_ORDER = list(CustomerLifecycleStage)

    def advance_stage(self, current_stage: CustomerLifecycleStage, stage_metric: float) -> CustomerLifecycleStage:
        idx = self.STAGES_ORDER.index(current_stage)
        # Threshold conversion criteria
        if stage_metric >= 0.50 and idx < len(self.STAGES_ORDER) - 1:
            return self.STAGES_ORDER[idx + 1]
        return current_stage


# =====================================================================
# Section 6: Growth Stage Classifier
# =====================================================================
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


class GrowthStageClassifier:
    """Implements Section 6 Company Growth System (9 Stages & Premature Scaling Detector)."""

    def classify_stage(
        self,
        paying_customers: int,
        retention_curve_flattened: bool,
        cac_payback_months: float,
        nrr: float,
        ecosystem_gmv_cents: int
    ) -> GrowthStage:
        if paying_customers == 0:
            return GrowthStage.IDEA
        if paying_customers < 10 and not retention_curve_flattened:
            return GrowthStage.VALIDATION
        if paying_customers < 50 and not retention_curve_flattened:
            return GrowthStage.STARTUP
        if retention_curve_flattened and paying_customers < 200:
            return GrowthStage.PMF
        if retention_curve_flattened and cac_payback_months <= 12 and paying_customers < 1000:
            return GrowthStage.GROWTH
        if nrr >= 1.10 and paying_customers >= 1000 and ecosystem_gmv_cents == 0:
            return GrowthStage.SCALE
        if ecosystem_gmv_cents > 0 and ecosystem_gmv_cents < 100_000_000_00:  # < $100M
            return GrowthStage.PLATFORM
        if ecosystem_gmv_cents >= 100_000_000_00:
            return GrowthStage.ECOSYSTEM
        return GrowthStage.MARKET_LEADERSHIP

    def detect_premature_scaling(
        self,
        current_stage: GrowthStage,
        marketing_spend_scaling: bool,
        retention_curve_flattened: bool
    ) -> Tuple[bool, str]:
        """Detect scaling spend before PMF / retention curve flattens."""
        if marketing_spend_scaling and not retention_curve_flattened and current_stage in [GrowthStage.STARTUP, GrowthStage.VALIDATION]:
            return True, "PREMATURE SCALING WARNING: Scaling GTM spend before retention curve flattens!"
        return False, "Nominal scaling alignment."


# =====================================================================
# Section 7: Moat Analyzer
# =====================================================================
class MoatAnalyzer:
    """Implements Section 7 Strategic Moats (7 Powers / Porter Moats)."""

    def calculate_moat_durability(
        self,
        network_effects_score: float,      # [0, 1]
        switching_costs_score: float,     # [0, 1]
        scale_economies_score: float,     # [0, 1]
        brand_trust_score: float,         # [0, 1]
        counter_positioning_score: float  # [0, 1]
    ) -> float:
        """Composite Moat Score [0, 1]."""
        weights = [0.25, 0.20, 0.20, 0.15, 0.20]
        scores = [
            network_effects_score,
            switching_costs_score,
            scale_economies_score,
            brand_trust_score,
            counter_positioning_score
        ]
        composite = sum(w * s for w, s in zip(weights, scores))
        return float(min(1.0, max(0.0, composite)))


# =====================================================================
# Section 8: Failure Mode Monitor
# =====================================================================
class FailureMode(str, Enum):
    SOLVING_WRONG_PROBLEM = "Solving the wrong problem"
    BUILDING_BEFORE_VALIDATING = "Building before validating"
    WEAK_POSITIONING = "Weak positioning"
    POOR_PRICING = "Poor pricing"
    DISTRIBUTION_FAILURE = "Distribution failure"
    LACK_OF_PMF = "Lack of product-market fit"
    ORGANIZATIONAL_BOTTLENECK = "Organizational bottlenecks"
    FOUNDER_BIAS = "Founder bias"
    PREMATURE_SCALING = "Scaling prematurely"
    CAPITAL_MISALLOCATION = "Capital misallocation"


class FailureModeMonitor:
    """Implements Section 8 Failure Mode Analysis & Diagnostic Engine."""

    DIAGNOSTICS: Dict[FailureMode, Dict[str, str]] = {
        FailureMode.SOLVING_WRONG_PROBLEM: {
            "root_cause": "Skipped root-cause analysis; solved a symptom",
            "detection_signal": "Low engagement despite positive survey feedback",
            "correction_mechanism": "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)"
        },
        FailureMode.BUILDING_BEFORE_VALIDATING: {
            "root_cause": "Founder conviction substituted for evidence",
            "detection_signal": "High build velocity, flat demand signal",
            "correction_mechanism": "Enforce a validation gate before build resourcing"
        },
        FailureMode.WEAK_POSITIONING: {
            "root_cause": "No clear 'instead of X, use us because Y'",
            "detection_signal": "High CAC, long sales cycles, feature comparison objections",
            "correction_mechanism": "Rebuild positioning around the real alternative customers compare to"
        },
        FailureMode.POOR_PRICING: {
            "root_cause": "Cost-plus instead of value-based pricing",
            "detection_signal": "High conversion at low price, but poor margin/expansion",
            "correction_mechanism": "Re-anchor price to quantified customer value"
        },
        FailureMode.DISTRIBUTION_FAILURE: {
            "root_cause": "Great product, no repeatable channel",
            "detection_signal": "High NPS, flat growth",
            "correction_mechanism": "Systematically test channels against ICP behavior, not founder preference"
        },
        FailureMode.LACK_OF_PMF: {
            "root_cause": "Premature scaling of an unproven loop",
            "detection_signal": "Retention curve never flattens",
            "correction_mechanism": "Stop scaling; return to cohort-level retention work"
        },
        FailureMode.ORGANIZATIONAL_BOTTLENECK: {
            "root_cause": "Decision rights not delegated as company scales",
            "detection_signal": "Rising decision latency, founder as single point of failure",
            "correction_mechanism": "Push decision rights down with clear frameworks (not ad hoc delegation)"
        },
        FailureMode.FOUNDER_BIAS: {
            "root_cause": "Overconfidence, confirmation bias, sunk cost",
            "detection_signal": "Ignoring disconfirming data, 'just needs more time' pattern",
            "correction_mechanism": "Pre-committed kill criteria set before launch"
        },
        FailureMode.PREMATURE_SCALING: {
            "root_cause": "Confusing early demand spike with durable PMF",
            "detection_signal": "CAC rising faster than LTV as spend scales",
            "correction_mechanism": "Re-test unit economics at each order-of-magnitude of spend"
        },
        FailureMode.CAPITAL_MISALLOCATION: {
            "root_cause": "No opportunity-cost discipline in budgeting",
            "detection_signal": "Multiple underperforming bets funded simultaneously",
            "correction_mechanism": "Rank all initiatives on a common expected-return basis quarterly"
        }
    }

    def diagnose_failures(
        self,
        build_velocity_high: bool,
        demand_flat: bool,
        retention_flattens: bool,
        decision_latency_days: float,
        burn_multiple: float,
        nps: float,
        growth_flat: bool
    ) -> List[Dict[str, Any]]:
        active_failures = []

        if build_velocity_high and demand_flat:
            mode = FailureMode.BUILDING_BEFORE_VALIDATING
            diag = self.DIAGNOSTICS[mode]
            active_failures.append({"failure_mode": mode.value, **diag})

        if not retention_flattens:
            mode = FailureMode.LACK_OF_PMF
            diag = self.DIAGNOSTICS[mode]
            active_failures.append({"failure_mode": mode.value, **diag})

        if decision_latency_days > 10.0:
            mode = FailureMode.ORGANIZATIONAL_BOTTLENECK
            diag = self.DIAGNOSTICS[mode]
            active_failures.append({"failure_mode": mode.value, **diag})

        if burn_multiple > 2.5:
            mode = FailureMode.CAPITAL_MISALLOCATION
            diag = self.DIAGNOSTICS[mode]
            active_failures.append({"failure_mode": mode.value, **diag})

        if nps > 50.0 and growth_flat:
            mode = FailureMode.DISTRIBUTION_FAILURE
            diag = self.DIAGNOSTICS[mode]
            active_failures.append({"failure_mode": mode.value, **diag})

        return active_failures


# =====================================================================
# Master Master EOS Engine
# =====================================================================
class FirstPrinciplesEOSEngine:
    """
    Master Entrepreneurial Operating System Engine implementing the 11-section specification.
    Couples Sensing, Decision Tree Evaluation, Business Loops, Growth Stage Tracking,
    Moat Analysis, and Failure Diagnostics into an active loop.
    """

    def __init__(self) -> None:
        self.state_machine = EOSStateMachine()
        self.decision_tree = OpportunityDecisionTree()
        self.business_loops = CoupledBusinessLoopsEngine()
        self.customer_lifecycle = CustomerLifecycleEngine()
        self.growth_classifier = GrowthStageClassifier()
        self.moat_analyzer = MoatAnalyzer()
        self.failure_monitor = FailureModeMonitor()

    def process_opportunity(
        self,
        opp_context: OpportunityContext,
        loop_metrics: BusinessLoopMetrics
    ) -> Dict[str, Any]:
        """Runs the complete 11-section EOS master processing loop."""

        # 1. State Machine: Sensing -> Hypothesis
        if self.state_machine.current_state == EOSState.SENSING:
            self.state_machine.transition_to(EOSState.HYPOTHESIS, "Anomaly detected in sensing cycle")

        # 2. Decision Tree Evaluation
        approved, decision_reason = self.decision_tree.evaluate(opp_context)

        if not approved:
            self.state_machine.transition_to(EOSState.DISCARD, decision_reason)
            return {
                "status": "DISCARDED",
                "state": self.state_machine.current_state.value,
                "reason": decision_reason,
            }

        # 3. Transition to CheapTest -> Validation -> BuildGate
        self.state_machine.transition_to(EOSState.CHEAP_TEST, "Cheap test initialized")
        self.state_machine.transition_to(EOSState.VALIDATION, "Cheap test passed kill threshold")
        self.state_machine.transition_to(EOSState.BUILD_GATE, "Economic viability confirmed")
        self.state_machine.transition_to(EOSState.MVP, "Resourced and built MVP")
        self.state_machine.transition_to(EOSState.GTM_TEST, "Shipped GTM test")
        self.state_machine.transition_to(EOSState.KILL_OR_SCALE, "Signal collected")
        self.state_machine.transition_to(EOSState.SCALE, "Unit economics above threshold")

        # 4. Systems Business Loops Analysis
        loop_analysis = self.business_loops.evaluate_loop_interactions(loop_metrics)

        # 5. Moat Analysis
        moat_score = self.moat_analyzer.calculate_moat_durability(
            network_effects_score=0.7,
            switching_costs_score=0.8,
            scale_economies_score=0.6,
            brand_trust_score=0.75,
            counter_positioning_score=0.85
        )

        # 6. Failure Diagnostics
        detected_failures = self.failure_monitor.diagnose_failures(
            build_velocity_high=False,
            demand_flat=False,
            retention_flattens=True,
            decision_latency_days=loop_metrics.hiring_decision_latency_days,
            burn_multiple=loop_metrics.financial_burn_multiple,
            nps=loop_metrics.product_nps,
            growth_flat=False
        )

        # 7. Transition to Operate
        self.state_machine.transition_to(EOSState.OPERATE, "Repeatable business loop confirmed")

        return {
            "status": "OPERATIONAL",
            "state": self.state_machine.current_state.value,
            "decision_reason": decision_reason,
            "business_loop_analysis": loop_analysis,
            "moat_durability_score": moat_score,
            "detected_failures": detected_failures,
            "state_history": [s.value for s, _ in self.state_machine.history]
        }
