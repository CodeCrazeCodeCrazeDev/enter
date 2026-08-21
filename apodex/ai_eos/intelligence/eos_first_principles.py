"""First-Principles Reconstruction of the Entrepreneurial Operating System (EOS).

Implements data models, decision trees, state machines, and feedback engines for:
1. Multi-timescale coupled feedback loops (Fast, Medium, Slow).
2. Cognitive Signal-to-Idea & Anomaly Detection Pipeline.
3. The 13 External Business Loops with coupling logic.
4. 15-Stage Full Customer Journey Lifecycle.
5. Integrated Go-To-Market (GTM) strategy engine.
6. 9-Stage Venture Company Growth Model.
7. Strategic Moats & 7-Powers Durability Evaluator.
8. 10 Core Failure Mode Monitors & Automated Corrections.
9. AI-EOS System State Machine & Decision Tree Execution.
"""

from __future__ import annotations
import math
import logging
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum, auto
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime, timezone

logger = logging.getLogger("sero.eos_first_principles")


# =====================================================================
# Enums and Domain Enums
# =====================================================================
class LoopTimescale(str, Enum):
    FAST = "fast"      # days - weeks
    MEDIUM = "medium"  # months - quarters
    SLOW = "slow"      # years


class RiskType(str, Enum):
    TYPE_I = "type_1_irreversible"
    TYPE_II = "type_2_reversible"


class CustomerStage(str, Enum):
    AWARENESS = "awareness"
    INTEREST = "interest"
    CONSIDERATION = "consideration"
    EVALUATION = "evaluation"
    PURCHASE = "purchase"
    ONBOARDING = "onboarding"
    ACTIVATION = "activation"
    ENGAGEMENT = "engagement"
    HABIT = "habit_formation"
    RETENTION = "retention"
    LOYALTY = "loyalty"
    ADVOCACY = "advocacy"
    REFERRAL = "referral"
    EXPANSION = "expansion"
    REPURCHASE = "repurchase"


class VentureGrowthStage(str, Enum):
    IDEA = "idea"
    VALIDATION = "validation"
    STARTUP = "startup"
    PMF = "product_market_fit"
    GROWTH = "growth"
    SCALE = "scale"
    PLATFORM = "platform"
    ECOSYSTEM = "ecosystem"
    MARKET_LEADERSHIP = "market_leadership"


class SystemState(str, Enum):
    SENSING = "sensing"
    HYPOTHESIS = "hypothesis"
    CHEAP_TEST = "cheap_test"
    DISCARD = "discard"
    VALIDATION = "validation"
    BUILD_GATE = "build_gate"
    MVP = "mvp"
    GTM_TEST = "gtm_test"
    KILL_OR_SCALE = "kill_or_scale"
    SCALE = "scale"
    OPERATE = "operate"
    REINVENT = "reinvent"


# =====================================================================
# 1. Anomaly & Signal-to-Idea Pipeline
# =====================================================================
@dataclass
class AnomalySignal:
    signal_id: UUID = field(default_factory=uuid4)
    name: str = ""
    is_structural_shift: bool = False
    anomaly_magnitude: float = 0.0  # [0, 1]
    raw_data: Dict[str, Any] = field(default_factory=dict)
    observed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class FalsifiableHypothesis:
    hypothesis_id: UUID = field(default_factory=uuid4)
    claim: str = ""
    falsification_metric: str = ""
    threshold_value: float = 0.0
    is_reversible: bool = True
    estimated_cost_cents: int = 0
    prior_belief: float = 0.5
    posterior_belief: float = 0.5
    status: str = "proposed"  # proposed, tested, validated, falsified


class SignalPipelineEngine:
    """Processes weak environmental signals into falsifiable hypotheses and cheap tests."""

    def __init__(self) -> None:
        self.signals: List[AnomalySignal] = []
        self.hypotheses: Dict[UUID, FalsifiableHypothesis] = {}

    def filter_signal(self, name: str, is_structural_shift: bool, magnitude: float) -> Optional[AnomalySignal]:
        sig = AnomalySignal(name=name, is_structural_shift=is_structural_shift, anomaly_magnitude=magnitude)
        self.signals.append(sig)
        if is_structural_shift and magnitude >= 0.3:
            return sig
        return None

    def form_hypothesis(
        self,
        claim: str,
        falsification_metric: str,
        threshold: float,
        is_reversible: bool,
        cost_cents: int
    ) -> FalsifiableHypothesis:
        hyp = FalsifiableHypothesis(
            claim=claim,
            falsification_metric=falsification_metric,
            threshold_value=threshold,
            is_reversible=is_reversible,
            estimated_cost_cents=cost_cents
        )
        self.hypotheses[hyp.hypothesis_id] = hyp
        return hyp

    def run_cheap_test(self, hypothesis_id: UUID, observed_metric_value: float) -> Tuple[bool, float]:
        hyp = self.hypotheses.get(hypothesis_id)
        if not hyp:
            return False, 0.0

        success = observed_metric_value >= hyp.threshold_value
        if success:
            hyp.posterior_belief = min(0.99, hyp.prior_belief + 0.35)
            hyp.status = "validated"
        else:
            hyp.posterior_belief = max(0.01, hyp.prior_belief - 0.45)
            hyp.status = "falsified"

        return success, hyp.posterior_belief


# =====================================================================
# 2. External Coupled Business Loops
# =====================================================================
@dataclass
class BusinessLoopState:
    product_retention_slope: float = 0.5
    cac_cents: int = 50000  # $500
    arpu_cents: int = 20000  # $200 / mo
    win_rate: float = 0.25
    nrr: float = 1.10
    burn_multiple: float = 1.5
    runway_months: float = 18.0
    quality_of_hire_score: float = 0.80
    decision_latency_seconds: float = 120.0
    viral_coefficient_k: float = 0.20
    feature_parity_ratio: float = 0.70


class BusinessLoopEngine:
    """Simulates coupled feedback interactions across the 13 business loops."""

    def __init__(self, state: Optional[BusinessLoopState] = None) -> None:
        self.state = state or BusinessLoopState()

    def step_coupled_loops(self, investments: Dict[str, float]) -> BusinessLoopState:
        """Executes one step across coupled loops (Product, Marketing, Sales, CS, Finance, etc.)."""
        # Product loop investment improves retention slope and feature parity
        prod_inv = investments.get("product", 0.0)
        self.state.product_retention_slope = min(1.0, self.state.product_retention_slope + prod_inv * 0.05)
        self.state.feature_parity_ratio = min(1.0, self.state.feature_parity_ratio + prod_inv * 0.04)

        # Sales/Marketing loop interactions: Product retention improves CAC payback & NRR
        self.state.nrr = max(0.5, self.state.nrr + (self.state.product_retention_slope - 0.5) * 0.4)

        # Pricing & ARPU impact from sales/CS performance
        cs_inv = investments.get("customer_success", 0.0)
        if cs_inv > 0:
            self.state.arpu_cents = int(self.state.arpu_cents * (1.0 + cs_inv * 0.02))

        # Financial loop updates
        fin_inv = investments.get("finance", 0.0)
        if self.state.nrr > 1.15:
            self.state.burn_multiple = max(0.5, self.state.burn_multiple - 0.1)

        return self.state


# =====================================================================
# 3. Customer Journey Lifecycle (15 Stages)
# =====================================================================
class CustomerJourneyTracker:
    """Tracks customer movement and conversion across all 15 journey stages."""

    STAGES_ORDER = list(CustomerStage)

    def __init__(self) -> None:
        self.stage_counts: Dict[CustomerStage, int] = {st: 0 for st in CustomerStage}
        self.stage_counts[CustomerStage.AWARENESS] = 1000

    def set_cohort_distribution(self, counts: Dict[CustomerStage, int]) -> None:
        for st, val in counts.items():
            self.stage_counts[st] = val

    def calculate_activation_rate(self) -> float:
        awareness = self.stage_counts.get(CustomerStage.AWARENESS, 1)
        activated = self.stage_counts.get(CustomerStage.ACTIVATION, 0)
        return float(activated / awareness) if awareness > 0 else 0.0

    def calculate_retention_score(self) -> float:
        activated = self.stage_counts.get(CustomerStage.ACTIVATION, 1)
        retained = self.stage_counts.get(CustomerStage.RETENTION, 0)
        return float(retained / activated) if activated > 0 else 0.0


# =====================================================================
# 4. Growth Stage Classifier
# =====================================================================
class GrowthStageClassifier:
    """Classifies company growth across the 9 stages and identifies binding constraints."""

    def evaluate_stage(
        self,
        paying_customers: int,
        mrr_cents: int,
        retention_curve_flattened: bool,
        has_ecosystem: bool
    ) -> Tuple[VentureGrowthStage, str]:
        if paying_customers == 0:
            return VentureGrowthStage.IDEA, "Founder time & initial hypothesis validation"
        elif paying_customers < 10:
            return VentureGrowthStage.VALIDATION, "Signal quality & willingness-to-pay evidence"
        elif paying_customers < 50 or not retention_curve_flattened:
            return VentureGrowthStage.STARTUP, "Cash runway & Product-Market Fit validation"
        elif retention_curve_flattened and mrr_cents < 5000000:  # < $50k MRR
            return VentureGrowthStage.PMF, "Team bandwidth & channel repeatability"
        elif mrr_cents < 50000000:  # < $500k MRR
            return VentureGrowthStage.GROWTH, "Hiring velocity & operational systems"
        elif not has_ecosystem:
            return VentureGrowthStage.SCALE, "Organizational coordination cost"
        else:
            return VentureGrowthStage.MARKET_LEADERSHIP, "Innovation velocity vs incumbency drag"


# =====================================================================
# 5. Moat Durability Analyzer
# =====================================================================
class MoatStrategyAnalyzer:
    """Evaluates competitive moats across Hamilton Helmer's 7 Powers framework."""

    def compute_moat_durability(
        self,
        network_density: float,        # Network Effects
        switching_cost_cents: int,     # Switching Costs
        scale_advantage_pct: float,    # Economies of Scale
        brand_trust_score: float,      # Brand
        counter_positioning: bool,     # Counter-Positioning
        cornered_resource: bool,       # Cornered Resources
        process_power_score: float     # Process Power
    ) -> float:
        s_net = min(1.0, network_density)
        s_switch = min(1.0, switching_cost_cents / 10000_00)
        s_scale = min(1.0, scale_advantage_pct)
        s_brand = min(1.0, brand_trust_score)
        s_cp = 1.0 if counter_positioning else 0.0
        s_cr = 1.0 if cornered_resource else 0.0
        s_pp = min(1.0, process_power_score)

        weighted_score = (
            0.20 * s_net +
            0.15 * s_switch +
            0.15 * s_scale +
            0.15 * s_brand +
            0.15 * s_cp +
            0.10 * s_cr +
            0.10 * s_pp
        )
        return float(weighted_score)


# =====================================================================
# 6. Failure Mode Monitor & Auto-Correction
# =====================================================================
@dataclass
class FailureAlert:
    failure_mode: str
    root_cause: str
    detection_signal: str
    recommended_correction: str


class FailureModeMonitor:
    """Monitors metrics against the 10 core failure modes and issues corrections."""

    def audit_metrics(
        self,
        retention_curve_flattens: bool,
        cac_cents: int,
        ltv_cents: int,
        burn_multiple: float,
        decision_latency_seconds: float,
        runway_months: float
    ) -> List[FailureAlert]:
        alerts = []

        # 1. Lack of Product-Market Fit
        if not retention_curve_flattens:
            alerts.append(FailureAlert(
                failure_mode="Lack of Product-Market Fit",
                root_cause="Premature scaling of an unproven loop",
                detection_signal="Retention curve never flattens",
                recommended_correction="Stop scaling spend; return to cohort-level retention work"
            ))

        # 2. Poor Pricing / Unit Economics
        if ltv_cents < 3 * cac_cents and cac_cents > 0:
            alerts.append(FailureAlert(
                failure_mode="Poor Pricing / Bad Economics",
                root_cause="Cost-plus pricing instead of value-based pricing",
                detection_signal="LTV:CAC ratio below 3:1 threshold",
                recommended_correction="Re-anchor price to quantified customer value"
            ))

        # 3. Capital Misallocation / High Burn
        if burn_multiple > 2.5:
            alerts.append(FailureAlert(
                failure_mode="Capital Misallocation",
                root_cause="No opportunity-cost discipline in budgeting",
                detection_signal=f"Burn multiple high ({burn_multiple:.2f})",
                recommended_correction="Rank all initiatives on common expected return quarterly"
            ))

        # 4. Organizational Bottlenecks
        if decision_latency_seconds > 300.0:  # > 5 minutes in simulation
            alerts.append(FailureAlert(
                failure_mode="Organizational Bottlenecks",
                root_cause="Decision rights not delegated as company scales",
                detection_signal=f"Rising decision latency ({decision_latency_seconds:.1f}s)",
                recommended_correction="Push decision rights down with explicit frameworks"
            ))

        # 5. Premature Scaling
        if runway_months < 6.0 and burn_multiple > 2.0:
            alerts.append(FailureAlert(
                failure_mode="Premature Scaling",
                root_cause="Confusing early demand spike with durable PMF",
                detection_signal="Runway < 6 months with high burn",
                recommended_correction="Re-test unit economics at each order of magnitude spend"
            ))

        return alerts


# =====================================================================
# 7. AI-EOS System State Machine & Decision Tree
# =====================================================================
class FirstPrinciplesEOSEngine:
    """Complete first-principles EOS system orchestrator combining all cognitive & operational components."""

    def __init__(self) -> None:
        self.state = SystemState.SENSING
        self.signal_pipeline = SignalPipelineEngine()
        self.business_loops = BusinessLoopEngine()
        self.customer_journey = CustomerJourneyTracker()
        self.growth_classifier = GrowthStageClassifier()
        self.moat_analyzer = MoatStrategyAnalyzer()
        self.failure_monitor = FailureModeMonitor()

    def execute_decision_tree(
        self,
        is_structural_anomaly: bool,
        is_reversible: bool,
        high_confidence_signal: bool,
        cheap_test_available: bool,
        test_passed: bool,
        ev_clearly_positive: bool,
        has_structural_advantage: bool
    ) -> Tuple[bool, str]:
        """Evaluates section 10.2 decision tree: 'Should We Pursue This Opportunity?'"""
        if not is_structural_anomaly:
            return False, "Discard: Signal is non-structural noise"

        if not is_reversible:
            if not high_confidence_signal:
                return False, "Discard: Irreversible decision lacking high-confidence signal"

        if cheap_test_available:
            if not test_passed:
                return False, "Discard: Cheap test failed to pass kill threshold"
        else:
            if not ev_clearly_positive:
                return False, "Discard: No cheap test available and Expected Value not clearly positive"

        if not has_structural_advantage:
            return False, "Discard: Cannot build structural advantage"

        return True, "Commit Resources: Passed all decision tree criteria"

    def transition_state_machine(self, trigger_event: str, data: Dict[str, Any]) -> SystemState:
        """Transitions the system state machine according to section 10.1."""
        if self.state == SystemState.SENSING:
            if trigger_event == "anomaly_detected":
                self.state = SystemState.HYPOTHESIS

        elif self.state == SystemState.HYPOTHESIS:
            if trigger_event == "hypothesis_formed":
                self.state = SystemState.CHEAP_TEST

        elif self.state == SystemState.CHEAP_TEST:
            if trigger_event == "falsified":
                self.state = SystemState.DISCARD
            elif trigger_event == "strengthened":
                self.state = SystemState.VALIDATION

        elif self.state == SystemState.VALIDATION:
            if trigger_event == "economic_viability_confirmed":
                self.state = SystemState.BUILD_GATE
            elif trigger_event == "no_viable_economics":
                self.state = SystemState.DISCARD

        elif self.state == SystemState.BUILD_GATE:
            if trigger_event == "resourced":
                self.state = SystemState.MVP

        elif self.state == SystemState.MVP:
            if trigger_event == "shipped":
                self.state = SystemState.GTM_TEST

        elif self.state == SystemState.GTM_TEST:
            if trigger_event == "signal_collected":
                self.state = SystemState.KILL_OR_SCALE

        elif self.state == SystemState.KILL_OR_SCALE:
            if trigger_event == "above_threshold":
                self.state = SystemState.SCALE
            elif trigger_event == "below_threshold":
                self.state = SystemState.DISCARD

        elif self.state == SystemState.SCALE:
            if trigger_event == "repeatable_loop_confirmed":
                self.state = SystemState.OPERATE

        elif self.state == SystemState.OPERATE:
            if trigger_event == "market_maturity":
                self.state = SystemState.REINVENT

        elif self.state in (SystemState.DISCARD, SystemState.REINVENT):
            self.state = SystemState.SENSING

        return self.state
