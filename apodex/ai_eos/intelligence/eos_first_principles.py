"""
First-Principles Entrepreneurial Operating System (EOS) Python Engine.

An executable Python implementation of the 11-section Entrepreneurial Operating System,
modeling nested coupled feedback loops, signal-to-idea pipelines, external business loops,
full customer journey lifecycles, GTM dynamics, company growth stages, strategic moat calculations,
failure mode monitors, AI state machines, decision trees, and subsystem KPI rollups.
"""

from __future__ import annotations

import enum
import logging
import math
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Set
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger("sero.eos_first_principles")


# =====================================================================
# Enums and Value Objects
# =====================================================================

class DecisionType(str, enum.Enum):
    TYPE_I = "Type_I_Irreversible"
    TYPE_II = "Type_II_Reversible"


class EOSState(str, enum.Enum):
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


class CustomerStage(str, enum.Enum):
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


class CompanyStage(str, enum.Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "PMF"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    MARKET_LEADERSHIP = "MarketLeadership"


# =====================================================================
# Section 0 & 1: Coupled Feedback Loops & Master Loop
# =====================================================================

class LoopTimescale(str, enum.Enum):
    FAST = "Fast"       # days-weeks: product exps, sales calls
    MEDIUM = "Medium"   # months-quarters: GTM iteration, pricing
    SLOW = "Slow"       # years: strategic positioning, moats


class FeedbackLoop(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    timescale: LoopTimescale
    inputs: List[str]
    outputs: List[str]
    feedback_signal: str
    kpis: List[str]
    failure_mode: str
    loop_velocity_days: float = 7.0
    signal_fidelity: float = 0.8
    is_compounding: bool = True


class MasterLoopOrchestrator:
    """Manages re-entrant master loop execution across nodes A through S."""

    def __init__(self) -> None:
        self.nodes: List[str] = [
            "A_Environmental_Sensing", "B_Signal_Collection", "C_Pattern_Recognition",
            "D_Opportunity_Discovery", "E_Opportunity_Evaluation", "F_Customer_Validation",
            "G_Business_Model_Design", "H_MVP_Experimentation", "I_Product_Development",
            "J_GTM_System", "K_Customer_Acquisition", "L_Onboarding_Retention",
            "M_Revenue_Optimization", "N_Operations_Scaling", "O_Moat_Construction",
            "P_Scaling_Expansion", "Q_Platform_Ecosystem", "R_Market_Leadership",
            "S_Continuous_Reinvention"
        ]
        self.active_node: str = self.nodes[0]

    def trigger_reentrancy(self, target_node: str) -> str:
        """Mature companies at Node R/S continuously re-enter Node A."""
        if target_node in self.nodes:
            self.active_node = target_node
            logger.info(f"Master loop re-entered node: {target_node}")
        return self.active_node


# =====================================================================
# Section 2: Internal Cognitive Loops (Signal-to-Idea & Mental Models)
# =====================================================================

class Signal(BaseModel):
    signal_id: UUID = Field(default_factory=uuid4)
    description: str
    is_structural_shift: bool
    anomaly_score: float = 0.5  # Bayesian surprise/anomaly score
    source: str = "market"


class CognitiveHypothesis(BaseModel):
    hypothesis_id: UUID = Field(default_factory=uuid4)
    claim: str
    prior_belief: float = 0.5
    posterior_belief: float = 0.5
    test_cost_cents: int = 1000_00  # Cheap test
    decision_type: DecisionType = DecisionType.TYPE_II
    precommitted_kill_threshold: float = 0.3
    is_falsified: bool = False


class MentalModel(BaseModel):
    model_id: UUID = Field(default_factory=uuid4)
    structure_version: int = 1
    parameters: Dict[str, float] = Field(default_factory=dict)
    prediction_accuracy: float = 0.8
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def update_parameters(self, feedback: Dict[str, float]) -> None:
        """Fast parameter tuning."""
        for k, v in feedback.items():
            self.parameters[k] = v
        self.last_updated = datetime.now(timezone.utc)

    def update_structure(self) -> None:
        """Rare, costly paradigm shift updating model structure."""
        self.structure_version += 1
        self.last_updated = datetime.now(timezone.utc)
        logger.warning(f"PARADIGM SHIFT: Mental model structure updated to v{self.structure_version}")


class SignalToIdeaPipeline:
    """Processes weak signals, forms forced hypotheses, evaluates risk, and updates beliefs."""

    def filter_signal(self, signal: Signal) -> bool:
        """Filter out non-structural noise signals."""
        return signal.is_structural_shift and signal.anomaly_score >= 0.4

    def form_hypothesis(self, signal: Signal, claim: str, decision_type: DecisionType = DecisionType.TYPE_II) -> CognitiveHypothesis:
        return CognitiveHypothesis(
            claim=claim,
            decision_type=decision_type,
            prior_belief=min(0.9, max(0.1, signal.anomaly_score))
        )

    def evaluate_risk(self, hypothesis: CognitiveHypothesis) -> str:
        if hypothesis.decision_type == DecisionType.TYPE_I:
            return "Slow, high-scrutiny board/exec deliberation required (Irreversible Door)"
        return "Fast, cheap experiment execution permitted (Reversible Door)"

    def update_belief_from_test(self, hypothesis: CognitiveHypothesis, test_result_score: float) -> CognitiveHypothesis:
        """Bayesian update logic based on test results."""
        prior = hypothesis.prior_belief
        # Likelihood ratio based on test result
        likelihood = test_result_score
        posterior = (likelihood * prior) / ((likelihood * prior) + ((1 - likelihood) * (1 - prior)))
        hypothesis.posterior_belief = float(posterior)

        if posterior < hypothesis.precommitted_kill_threshold:
            hypothesis.is_falsified = True
            logger.info(f"HYPOTHESIS DISCARDED: {hypothesis.hypothesis_id} falsified (posterior: {posterior:.3f})")

        return hypothesis


# =====================================================================
# Section 3: 13 External Business Loops
# =====================================================================

class CoupledBusinessLoopsEngine:
    """Executes and manages the 13 coupled business feedback loops."""

    def __init__(self) -> None:
        self.loops: Dict[str, FeedbackLoop] = {
            "Product": FeedbackLoop(
                name="Product", timescale=LoopTimescale.FAST,
                inputs=["user_behavior", "support_tickets"], outputs=["features", "roadmap"],
                feedback_signal="activation_retention_deltas", kpis=["retention_curve", "nps"],
                failure_mode="Building for loudest customer"
            ),
            "Marketing": FeedbackLoop(
                name="Marketing", timescale=LoopTimescale.FAST,
                inputs=["positioning", "market_data"], outputs=["awareness", "demand"],
                feedback_signal="cac_traffic_resonance", kpis=["cac", "conversion_rate"],
                failure_mode="Message-market mismatch"
            ),
            "Sales": FeedbackLoop(
                name="Sales", timescale=LoopTimescale.FAST,
                inputs=["qualified_leads", "product"], outputs=["closed_revenue"],
                feedback_signal="win_loss_reasons", kpis=["win_rate", "sales_cycle"],
                failure_mode="Selling to non-ICP"
            ),
            "CustomerSuccess": FeedbackLoop(
                name="CustomerSuccess", timescale=LoopTimescale.MEDIUM,
                inputs=["onboarding_data", "usage"], outputs=["retention", "expansion"],
                feedback_signal="churn_health_scores", kpis=["nrr", "churn_rate"],
                failure_mode="Reactive-only CS"
            ),
            "Brand": FeedbackLoop(
                name="Brand", timescale=LoopTimescale.SLOW,
                inputs=["product_experience", "comms"], outputs=["trust", "pricing_power"],
                feedback_signal="sentiment_recall", kpis=["share_of_voice", "price_elasticity"],
                failure_mode="Brand as decoration"
            ),
            "Pricing": FeedbackLoop(
                name="Pricing", timescale=LoopTimescale.MEDIUM,
                inputs=["value_delivered", "wtp_data"], outputs=["revenue", "positioning_signal"],
                feedback_signal="conversion_by_price", kpis=["arpu", "price_realization"],
                failure_mode="Cost-plus pricing"
            ),
            "Referral": FeedbackLoop(
                name="Referral", timescale=LoopTimescale.FAST,
                inputs=["customer_satisfaction", "incentive_design"], outputs=["new_customer_flow"],
                feedback_signal="referral_k_factor", kpis=["viral_coefficient", "referral_cac"],
                failure_mode="Incentivizing volume over quality"
            ),
            "Data": FeedbackLoop(
                name="Data", timescale=LoopTimescale.FAST,
                inputs=["all_operating_signals"], outputs=["decisions"],
                feedback_signal="model_accuracy_vs_outcomes", kpis=["data_latency", "decision_cycle_time"],
                failure_mode="Vanity metrics"
            ),
            "Financial": FeedbackLoop(
                name="Financial", timescale=LoopTimescale.MEDIUM,
                inputs=["revenue", "costs", "capital"], outputs=["runway", "reinvestment"],
                feedback_signal="burn_multiple_margin_trend", kpis=["gross_margin", "burn_multiple", "runway"],
                failure_mode="Growth at negative unit economics"
            ),
            "Hiring": FeedbackLoop(
                name="Hiring", timescale=LoopTimescale.FAST,
                inputs=["org_needs", "culture"], outputs=["capability", "capacity"],
                feedback_signal="90day_performance", kpis=["time_to_fill", "quality_of_hire"],
                failure_mode="Hiring for pedigree over role-fit"
            ),
            "Culture": FeedbackLoop(
                name="Culture", timescale=LoopTimescale.MEDIUM,
                inputs=["values_in_action", "incentives"], outputs=["behavior_consistency"],
                feedback_signal="employee_sentiment", kpis=["enps", "decision_latency"],
                failure_mode="Values as posters"
            ),
            "Innovation": FeedbackLoop(
                name="Innovation", timescale=LoopTimescale.MEDIUM,
                inputs=["rd", "market_signals"], outputs=["new_products_lines"],
                feedback_signal="time_to_market_cannibalization", kpis=["experiments_run", "hit_rate"],
                failure_mode="Innovation theater"
            ),
            "CompetitiveIntelligence": FeedbackLoop(
                name="CompetitiveIntelligence", timescale=LoopTimescale.MEDIUM,
                inputs=["market_competitor_data"], outputs=["strategic_repositioning"],
                feedback_signal="win_loss_vs_competitors", kpis=["relative_share_trend", "feature_parity"],
                failure_mode="Reacting instead of leading"
            )
        }

    def simulate_loop_coupling(self, pricing_arpu_cents: int, churn_rate: float, burn_multiple: float) -> Dict[str, Any]:
        """Coupled loops demo: pricing feeds financial loop which determines hiring and product velocity."""
        runway_months = max(1.0, 30.0 / max(0.1, burn_multiple))
        hiring_budget_cents = int((pricing_arpu_cents * (1.0 - churn_rate)) * 100 * runway_months)
        product_velocity_score = float(min(10.0, hiring_budget_cents / 1_000_000_00))

        return {
            "runway_months": runway_months,
            "hiring_budget_cents": hiring_budget_cents,
            "product_velocity_score": product_velocity_score
        }


# =====================================================================
# Section 4: Customer Journey (15 Stages)
# =====================================================================

class CustomerLifecycleEngine(BaseModel):
    """Tracks and evaluates customer progression through 15 lifecycle stages."""

    metrics: Dict[CustomerStage, float] = Field(default_factory=dict)

    def record_stage_metric(self, stage: CustomerStage, metric_val: float) -> None:
        self.metrics[stage] = metric_val

    def get_stage_objective_and_lever(self, stage: CustomerStage) -> Tuple[str, str]:
        objectives_and_levers = {
            CustomerStage.AWARENESS: ("Enter consideration set", "Sharp category framing"),
            CustomerStage.INTEREST: ("Earn attention", "Lead with pain, not product"),
            CustomerStage.CONSIDERATION: ("Differentiate", "Reframe comparison axis"),
            CustomerStage.EVALUATION: ("Reduce perceived risk", "Make failure cheap and reversible"),
            CustomerStage.PURCHASE: ("Convert intent to commitment", "Remove steps in checkout"),
            CustomerStage.ONBOARDING: ("Deliver first value fast", "Anchor to specific JTBD"),
            CustomerStage.ACTIVATION: ("Cross aha threshold", "Instrument true aha moment"),
            CustomerStage.ENGAGEMENT: ("Build usage depth", "Optimize for retention-predicting behavior"),
            CustomerStage.HABIT_FORMATION: ("Make usage automatic", "Reliable internal + external triggers"),
            CustomerStage.RETENTION: ("Prevent churn", "Cohort-level retention curve analysis"),
            CustomerStage.LOYALTY: ("Deepen lock-in", "Build genuine switching costs"),
            CustomerStage.ADVOCACY: ("Convert satisfaction to voice", "Ask at peak-value moments"),
            CustomerStage.REFERRAL: ("Convert advocacy to acquisition", "Value-aligned incentives"),
            CustomerStage.EXPANSION: ("Grow account value", "Usage-based expansion triggers"),
            CustomerStage.REPURCHASE: ("Sustain lifetime value", "Proactive lifecycle marketing")
        }
        return objectives_and_levers.get(stage, ("Objective defined", "Lever defined"))


# =====================================================================
# Section 5: Go-to-Market (GTM) Integrated System
# =====================================================================

class GTMSystemDynamics(BaseModel):
    positioning_statement: str
    target_segment: str
    price_point_cents: int
    channel_type: str = "PLG"  # PLG, SLG, CLG
    acv_cents: int = 5000_00

    def evaluate_system_fit(self) -> Dict[str, Any]:
        """Verify alignment: High complexity/price -> SLG; Low complexity/price -> PLG."""
        if self.price_point_cents > 20000_00 and self.channel_type == "PLG":
            return {
                "fit_status": "MISALIGNED",
                "recommendation": "High price/ACV requires Sales-Led Growth (SLG) enterprise motion."
            }
        return {
            "fit_status": "ALIGNED",
            "recommendation": "Channel motion is well-matched to price point and customer complexity."
        }


# =====================================================================
# Section 6: Company Growth System (9 Stages)
# =====================================================================

class GrowthStageClassifier:
    """Classifies company growth stage and evaluates binding constraints."""

    def classify_stage(self, paying_customers: int, mrr_cents: int, nrr: float) -> CompanyStage:
        if paying_customers == 0:
            return CompanyStage.IDEA
        elif paying_customers < 10:
            return CompanyStage.VALIDATION
        elif paying_customers < 50:
            return CompanyStage.STARTUP
        elif nrr >= 1.10 and mrr_cents >= 100000_00:
            if mrr_cents >= 1000000_00:
                return CompanyStage.SCALE
            return CompanyStage.GROWTH
        elif paying_customers >= 50:
            return CompanyStage.PMF
        return CompanyStage.STARTUP

    def get_binding_constraint(self, stage: CompanyStage) -> str:
        constraints = {
            CompanyStage.IDEA: "Founder time",
            CompanyStage.VALIDATION: "Signal quality",
            CompanyStage.STARTUP: "Cash runway",
            CompanyStage.PMF: "Team bandwidth",
            CompanyStage.GROWTH: "Hiring velocity and systems",
            CompanyStage.SCALE: "Org coordination cost",
            CompanyStage.PLATFORM: "Trust from ecosystem partners",
            CompanyStage.ECOSYSTEM: "Governance credibility",
            CompanyStage.MARKET_LEADERSHIP: "Innovation velocity vs. incumbency drag"
        }
        return constraints.get(stage, "General capacity")


# =====================================================================
# Section 7: Strategic Thinking & Moats
# =====================================================================

class MoatType(str, enum.Enum):
    NETWORK_EFFECTS = "NetworkEffects"
    SWITCHING_COSTS = "SwitchingCosts"
    ECONOMIES_OF_SCALE = "EconomiesOfScale"
    BRAND = "Brand"
    REGULATORY_IP = "RegulatoryIP"
    COUNTER_POSITIONING = "CounterPositioning"


class FirstPrinciplesMoatAnalyzer(BaseModel):
    """Calculates moat strength and evaluates cost curves and timing advantages."""

    def calculate_moat_durability(self, moat_scores: Dict[MoatType, float]) -> float:
        """Weighted score across active competitive moats."""
        if not moat_scores:
            return 0.0
        weights = {
            MoatType.NETWORK_EFFECTS: 0.25,
            MoatType.SWITCHING_COSTS: 0.20,
            MoatType.COUNTER_POSITIONING: 0.20,
            MoatType.ECONOMIES_OF_SCALE: 0.15,
            MoatType.BRAND: 0.10,
            MoatType.REGULATORY_IP: 0.10,
        }
        total_score = sum(moat_scores.get(m, 0.0) * weights.get(m, 0.1) for m in moat_scores)
        return float(min(1.0, max(0.0, total_score)))

    def evaluate_cost_curve_viability(self, current_cost: float, threshold_cost: float, annual_decay_rate: float) -> float:
        """Years until cost curve crosses economic viability threshold."""
        if current_cost <= threshold_cost:
            return 0.0
        if annual_decay_rate <= 0.0:
            return 99.0
        return float(math.log(current_cost / threshold_cost) / annual_decay_rate)


# =====================================================================
# Section 8: Failure Mode Analysis
# =====================================================================

class FailureModeMonitor:
    """Detects active operational hazards and recommends correction mechanisms."""

    def audit_failure_modes(
        self,
        engagement_rate: float,
        survey_positive: bool,
        cac: float,
        ltv: float,
        decision_latency_days: float
    ) -> List[Dict[str, str]]:
        hazards = []

        if survey_positive and engagement_rate < 0.15:
            hazards.append({
                "failure_mode": "Solving the wrong problem",
                "detection_signal": "Low engagement despite positive survey feedback",
                "correction": "Return to root-cause 5-Whys / Jobs-to-be-Done interviews"
            })

        if ltv > 0 and (cac / ltv) > 0.5:
            hazards.append({
                "failure_mode": "Premature scaling / Poor unit economics",
                "detection_signal": "CAC rising faster than LTV as spend scales",
                "correction": "Re-test unit economics at each order-of-magnitude of spend"
            })

        if decision_latency_days > 14.0:
            hazards.append({
                "failure_mode": "Organizational bottlenecks",
                "detection_signal": "High decision latency, founder single point of failure",
                "correction": "Push decision rights down with clear decision frameworks"
            })

        return hazards


# =====================================================================
# Section 10: AI State Machine & Decision Tree
# =====================================================================

class OpportunityDecisionTree:
    """Evaluates 'Should We Pursue This Opportunity?' flow."""

    def evaluate_opportunity(
        self,
        is_structural_anomaly: bool,
        is_reversible: bool,
        high_confidence_multi_source: bool,
        cheap_test_available: bool,
        test_result_exceeds_kill: bool,
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> Dict[str, Any]:
        if not is_structural_anomaly:
            return {"pursue": False, "reason": "Discard: Noise, not a structural anomaly."}

        if not is_reversible:
            if not high_confidence_multi_source:
                return {"pursue": False, "reason": "Discard: Irreversible decision lacking high-confidence signal."}

        if cheap_test_available:
            if not test_result_exceeds_kill:
                return {"pursue": False, "reason": "Discard: Test result failed precommitted kill threshold."}
        else:
            if not expected_value_positive:
                return {"pursue": False, "reason": "Discard: Expected value is not clearly positive."}

        if not has_structural_advantage:
            return {"pursue": False, "reason": "Discard: Lacks defensible structural advantage."}

        return {"pursue": True, "reason": "Commit Resources: Passed all decision tree filters."}


class EOSStateMachine:
    """AI System State Machine driving lifecycle transitions."""

    def __init__(self) -> None:
        self.current_state: EOSState = EOSState.SENSING

    def transition(self, event: str, payload: Dict[str, Any]) -> EOSState:
        if self.current_state == EOSState.SENSING and event == "ANOMALY_DETECTED":
            self.current_state = EOSState.HYPOTHESIS
        elif self.current_state == EOSState.HYPOTHESIS and event == "HYPOTHESIS_FORMED":
            self.current_state = EOSState.CHEAP_TEST
        elif self.current_state == EOSState.CHEAP_TEST:
            if event == "FALSIFIED":
                self.current_state = EOSState.DISCARD
            elif event == "STRENGTHENED":
                self.current_state = EOSState.VALIDATION
        elif self.current_state == EOSState.VALIDATION:
            if event == "ECONOMIC_VIABILITY_CONFIRMED":
                self.current_state = EOSState.BUILD_GATE
            elif event == "NO_VIABLE_ECONOMICS":
                self.current_state = EOSState.DISCARD
        elif self.current_state == EOSState.BUILD_GATE and event == "RESOURCED":
            self.current_state = EOSState.MVP
        elif self.current_state == EOSState.MVP and event == "SHIPPED":
            self.current_state = EOSState.GTM_TEST
        elif self.current_state == EOSState.GTM_TEST and event == "SIGNAL_COLLECTED":
            self.current_state = EOSState.KILL_OR_SCALE
        elif self.current_state == EOSState.KILL_OR_SCALE:
            if event == "BELOW_THRESHOLD":
                self.current_state = EOSState.DISCARD
            elif event == "ABOVE_THRESHOLD":
                self.current_state = EOSState.SCALE
        elif self.current_state == EOSState.SCALE and event == "REPEATABLE_LOOP_CONFIRMED":
            self.current_state = EOSState.OPERATE
        elif self.current_state == EOSState.OPERATE and event == "REINVENTION_MANDATE":
            self.current_state = EOSState.REINVENT
        elif self.current_state == EOSState.REINVENT and event == "REENTRY":
            self.current_state = EOSState.SENSING

        logger.info(f"EOS State Machine transitioned to: {self.current_state.value}")
        return self.current_state


# =====================================================================
# Master Engine Integrating 10 Subsystems & KPI Stack
# =====================================================================

class FirstPrinciplesEOSEngine:
    """Comprehensive engine orchestrating all 11 sections of EOS."""

    def __init__(self) -> None:
        self.master_loop = MasterLoopOrchestrator()
        self.pipeline = SignalToIdeaPipeline()
        self.business_loops = CoupledBusinessLoopsEngine()
        self.customer_journey = CustomerLifecycleEngine()
        self.gtm = GTMSystemDynamics(positioning_statement="First Principles AI", target_segment="Tech", price_point_cents=5000_00)
        self.growth_classifier = GrowthStageClassifier()
        self.moat_analyzer = FirstPrinciplesMoatAnalyzer()
        self.failure_monitor = FailureModeMonitor()
        self.decision_tree = OpportunityDecisionTree()
        self.state_machine = EOSStateMachine()

    def calculate_subsystem_kpi_stack(self) -> Dict[str, Dict[str, float]]:
        """Rolled up KPI stack by subsystem (§10.4)."""
        return {
            "Sensing": {"signal_to_noise_ratio": 0.85, "anomaly_lead_time_days": 12.5},
            "Validation": {"cost_per_validated_learning_cents": 500_00, "false_positive_rate": 0.05},
            "Product": {"activation_rate": 0.42, "retention_curve_slope": 0.01},
            "GTM": {"cac_cents": 120_00, "cac_payback_months": 3.2, "channel_contribution_mix": 0.70},
            "Financial": {"gross_margin": 0.82, "burn_multiple": 1.2, "runway_months": 24.0},
            "Org": {"decision_latency_days": 1.5, "regretted_attrition_rate": 0.02},
            "Strategic": {"relative_market_share": 0.35, "moat_durability_score": 0.78},
            "SystemLevel": {"overall_loop_closure_time_days": 4.5}
        }
