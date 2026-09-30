"""First-Principles Entrepreneurial Operating System (EOS) Engine.

Executable implementation of the 11-section EOS architectural specification
for sensing, building, and compounding enduring companies.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field
import math
import uuid


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# ==========================================
# Section 0 & 1: Master Loop & Timescales
# ==========================================

class MasterLoopNode(str, Enum):
    ENVIRONMENTAL_SENSING = "A"
    SIGNAL_COLLECTION = "B"
    PATTERN_RECOGNITION = "C"
    OPPORTUNITY_DISCOVERY = "D"
    OPPORTUNITY_EVALUATION = "E"
    CUSTOMER_VALIDATION = "F"
    BUSINESS_MODEL_DESIGN = "G"
    MVP_EXPERIMENTATION = "H"
    PRODUCT_DEVELOPMENT = "I"
    GTM_SYSTEM = "J"
    CUSTOMER_ACQUISITION = "K"
    ONBOARDING_RETENTION = "L"
    REVENUE_OPTIMIZATION = "M"
    OPERATIONS_SCALING = "N"
    COMPETITIVE_MOAT = "O"
    SCALING_EXPANSION = "P"
    PLATFORM_ECOSYSTEM = "Q"
    MARKET_LEADERSHIP = "R"
    CONTINUOUS_REINVENTION = "S"


class LoopTimescale(str, Enum):
    FAST = "fast"  # days - weeks
    MEDIUM = "medium"  # months - quarters
    SLOW = "slow"  # years


class LoopVelocityMetrics(BaseModel):
    loop_name: str
    timescale: LoopTimescale
    cycle_time_days: float
    signal_fidelity_score: float = Field(ge=0.0, le=1.0)
    is_compounding: bool = True


# ==========================================
# Section 2: Internal Cognitive Loops
# ==========================================

class DecisionRiskType(str, Enum):
    TYPE_I = "Type_I"  # Irreversible, one-way door
    TYPE_II = "Type_II"  # Reversible, two-way door


class SignalAnomaly(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    observed_value: float
    expected_value: float
    structural_shift_probability: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=utc_now)


class FalsifiableHypothesis(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    claim: str
    enabling_condition: str
    falsification_metric: str
    falsification_threshold: float
    prior_belief_probability: float = Field(default=0.5, ge=0.0, le=1.0)
    current_belief_probability: float = Field(default=0.5, ge=0.0, le=1.0)
    risk_type: DecisionRiskType = DecisionRiskType.TYPE_II
    status: str = "active"  # active, falsified, strengthened, discarded


class CheapTestResult(BaseModel):
    hypothesis_id: str
    test_cost: float
    evidence_score: float = Field(ge=0.0, le=1.0)  # 0.0 = strong disconfirmation, 1.0 = strong confirmation
    sample_size: int
    execution_days: float


class MentalModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    parameters: Dict[str, float] = Field(default_factory=dict)
    structural_assumptions: List[str] = Field(default_factory=list)
    prediction_accuracy: float = Field(default=1.0, ge=0.0, le=1.0)
    consecutive_predictions: int = 0
    consecutive_failures: int = 0
    ossification_score: float = Field(default=0.0, ge=0.0, le=1.0)


# ==========================================
# Section 3: External Business Loops
# ==========================================

class ExternalBusinessLoopType(str, Enum):
    PRODUCT = "Product"
    MARKETING = "Marketing"
    SALES = "Sales"
    CUSTOMER_SUCCESS = "Customer_Success"
    BRAND = "Brand"
    PRICING = "Pricing"
    REFERRAL = "Referral"
    DATA = "Data"
    FINANCIAL = "Financial"
    HIRING = "Hiring"
    CULTURE = "Culture"
    INNOVATION = "Innovation"
    COMPETITIVE_INTELLIGENCE = "Competitive_Intelligence"


class BusinessLoopState(BaseModel):
    loop_type: ExternalBusinessLoopType
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    feedback_signal: float  # deltas, CAC, win rates, etc.
    core_kpis: Dict[str, float]
    dominant_failure_mode: str
    is_healthy: bool = True


# ==========================================
# Section 4: Customer Journey Lifecycle
# ==========================================

class JourneyStage(str, Enum):
    AWARENESS = "Awareness"
    INTEREST = "Interest"
    CONSIDERATION = "Consideration"
    EVALUATION = "Evaluation"
    PURCHASE = "Purchase"
    ONBOARDING = "Onboarding"
    ACTIVATION = "Activation"
    ENGAGEMENT = "Engagement"
    HABIT_FORMATION = "Habit_Formation"
    RETENTION = "Retention"
    LOYALTY = "Loyalty"
    ADVOCACY = "Advocacy"
    REFERRAL = "Referral"
    EXPANSION = "Expansion"
    REPURCHASE = "Repurchase"


class CustomerJourneyStageMetrics(BaseModel):
    stage: JourneyStage
    conversion_rate: float = Field(ge=0.0, le=1.0)
    customer_psychology: str
    key_metric_value: float
    common_mistake_flagged: bool = False
    optimization_lever: str


# ==========================================
# Section 5: Go-to-Market System
# ==========================================

class GTMDistributionMotion(str, Enum):
    PLG = "Product_Led_Growth"
    SLG = "Sales_Led_Growth"
    CLG = "Community_Led_Growth"
    CONTENT = "Content_Led"
    PARTNERSHIPS = "Partnerships"
    PAID = "Paid_Acquisition"


class GTMSystemConfig(BaseModel):
    positioning_statement: str
    comparison_axis: str
    target_segment: str
    pricing_model: str  # usage-based, flat, seat, etc.
    primary_motion: GTMDistributionMotion
    secondary_motions: List[GTMDistributionMotion] = Field(default_factory=list)
    compounding_motion_score: float = Field(default=0.8, ge=0.0, le=1.0)


# ==========================================
# Section 6: Company Growth System
# ==========================================

class GrowthStage(str, Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "Product_Market_Fit"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    MARKET_LEADERSHIP = "Market_Leadership"


class GrowthStageStatus(BaseModel):
    current_stage: GrowthStage
    primary_objective: str
    org_structure: str
    decision_rights_mode: str
    capital_allocation_strategy: str
    key_risk: str
    core_metric_value: float
    binding_constraint: str
    premature_scaling_risk: float = Field(default=0.0, ge=0.0, le=1.0)


# ==========================================
# Section 7: Strategic Thinking & Moats
# ==========================================

class MoatType(str, Enum):
    NETWORK_EFFECTS = "Network_Effects"
    SWITCHING_COSTS = "Switching_Costs"
    ECONOMIES_OF_SCALE = "Economies_Of_Scale"
    BRAND_TRUST = "Brand_Trust"
    REGULATORY_IP = "Regulatory_IP"
    COUNTER_POSITIONING = "Counter_Positioning"


class TechnologyCostCurve(BaseModel):
    technology_name: str
    cost_per_unit_trend: List[float]
    viability_threshold: float
    is_viability_crossed: bool = False


class MoatEvaluation(BaseModel):
    moat_type: MoatType
    strength_score: float = Field(ge=0.0, le=1.0)
    durability_years: float
    incumbent_copy_cost: float


# ==========================================
# Section 8: Failure Mode Analysis
# ==========================================

class FailureModeDiagnostic(BaseModel):
    failure_mode: str
    root_cause: str
    detection_signal: str
    correction_mechanism: str
    is_detected: bool = False
    severity: float = Field(default=0.0, ge=0.0, le=1.0)


# ==========================================
# Section 10: State Machine & Decision Tree
# ==========================================

class SystemState(str, Enum):
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


class DecisionTreeResult(BaseModel):
    decision: str  # "Commit Resources", "Run Cheap Test", "Discard"
    reasoning: List[str]
    is_pursued: bool
    risk_level: DecisionRiskType


# ==========================================
# Comprehensive EOS First-Principles Engine
# ==========================================

class EOSEngineFirstPrinciples:
    """Unified executable engine for the Entrepreneurial Operating System (EOS)."""

    def __init__(self, venture_id: Optional[str] = None):
        self.venture_id = venture_id or str(uuid.uuid4())
        self.current_master_node: MasterLoopNode = MasterLoopNode.ENVIRONMENTAL_SENSING
        self.current_state: SystemState = SystemState.SENSING
        self.mental_models: Dict[str, MentalModel] = {}
        self.active_hypotheses: Dict[str, FalsifiableHypothesis] = {}
        self.business_loops: Dict[ExternalBusinessLoopType, BusinessLoopState] = {}
        self.growth_status: GrowthStageStatus = GrowthStageStatus(
            current_stage=GrowthStage.IDEA,
            primary_objective="Falsify or strengthen hypothesis",
            org_structure="Founder(s) only",
            decision_rights_mode="Founder intuition, fast",
            capital_allocation_strategy="Near-zero, sweat equity",
            key_risk="Solving a non-problem",
            core_metric_value=0.0,
            binding_constraint="Founder time",
            premature_scaling_risk=0.0
        )
        self.cost_curves: Dict[str, TechnologyCostCurve] = {}
        self.moats: Dict[MoatType, MoatEvaluation] = {}
        self.init_default_business_loops()

    def init_default_business_loops(self) -> None:
        """Initialize default 13 business loops per Section 3."""
        loop_defs = [
            (ExternalBusinessLoopType.PRODUCT, "Building for loudest customer", "Retention curve"),
            (ExternalBusinessLoopType.MARKETING, "Message-market mismatch", "CAC"),
            (ExternalBusinessLoopType.SALES, "Selling to non-ICP", "Win rate"),
            (ExternalBusinessLoopType.CUSTOMER_SUCCESS, "Reactive-only CS", "NRR"),
            (ExternalBusinessLoopType.BRAND, "Brand as decoration", "Price elasticity"),
            (ExternalBusinessLoopType.PRICING, "Cost-plus pricing", "ARPU"),
            (ExternalBusinessLoopType.REFERRAL, "Incentivizing volume over quality", "Viral coefficient"),
            (ExternalBusinessLoopType.DATA, "Vanity metrics", "Data latency"),
            (ExternalBusinessLoopType.FINANCIAL, "Negative unit economics growth", "Burn multiple"),
            (ExternalBusinessLoopType.HIRING, "Pedigree over role-fit", "Quality of hire"),
            (ExternalBusinessLoopType.CULTURE, "Values-as-poster", "Decision latency"),
            (ExternalBusinessLoopType.INNOVATION, "Innovation theater", "# experiments run"),
            (ExternalBusinessLoopType.COMPETITIVE_INTELLIGENCE, "Reacting vs strategy", "Relative share trend"),
        ]
        for loop_type, failure_mode, kpi in loop_defs:
            self.business_loops[loop_type] = BusinessLoopState(
                loop_type=loop_type,
                inputs={"status": "initial"},
                outputs={"status": "initial"},
                feedback_signal=1.0,
                core_kpis={kpi: 1.0},
                dominant_failure_mode=failure_mode,
                is_healthy=True
            )

    # ------------------------------------------
    # §1 Master Loop State Transitions & Velocity
    # ------------------------------------------

    def transition_master_node(self, target_node: MasterLoopNode, re_entry_signal: Optional[str] = None) -> MasterLoopNode:
        """Execute top-level master loop transition with re-entrant capability."""
        if re_entry_signal == "kill_signal" and target_node in (MasterLoopNode.CUSTOMER_VALIDATION, MasterLoopNode.MVP_EXPERIMENTATION):
            self.current_master_node = MasterLoopNode.OPPORTUNITY_DISCOVERY
        elif re_entry_signal == "weak_gtm" and target_node == MasterLoopNode.CUSTOMER_ACQUISITION:
            self.current_master_node = MasterLoopNode.GTM_SYSTEM
        elif re_entry_signal == "bad_economics" and target_node == MasterLoopNode.REVENUE_OPTIMIZATION:
            self.current_master_node = MasterLoopNode.BUSINESS_MODEL_DESIGN
        else:
            self.current_master_node = target_node
        return self.current_master_node

    def calculate_loop_velocity(self, cycle_times: Dict[LoopTimescale, float]) -> Dict[str, Any]:
        """Calculate loop velocity and signal fidelity across fast, medium, and slow loops."""
        fast_time = cycle_times.get(LoopTimescale.FAST, 7.0)
        med_time = cycle_times.get(LoopTimescale.MEDIUM, 60.0)
        slow_time = cycle_times.get(LoopTimescale.SLOW, 365.0)

        composite_velocity = (1.0 / max(fast_time, 0.1)) * 0.5 + (1.0 / max(med_time, 1.0)) * 0.3 + (1.0 / max(slow_time, 10.0)) * 0.2
        return {
            "fast_loop_days": fast_time,
            "medium_loop_days": med_time,
            "slow_loop_days": slow_time,
            "composite_velocity_score": round(composite_velocity * 100, 4)
        }

    # ------------------------------------------
    # §2 Cognitive Loops & Anomaly Detection
    # ------------------------------------------

    def detect_anomaly(self, description: str, observed: float, expected: float, variance_threshold: float = 0.2) -> SignalAnomaly:
        """Detect structural anomaly vs mental model expectations."""
        variance = abs(observed - expected) / max(abs(expected), 1e-6)
        prob_structural = min(1.0, variance / (variance_threshold * 2))
        return SignalAnomaly(
            description=description,
            observed_value=observed,
            expected_value=expected,
            structural_shift_probability=round(prob_structural, 4)
        )

    def form_falsifiable_hypothesis(
        self,
        claim: str,
        enabling_condition: str,
        metric: str,
        threshold: float,
        prior: float = 0.5,
        risk_type: DecisionRiskType = DecisionRiskType.TYPE_II
    ) -> FalsifiableHypothesis:
        """Form forced falsifiable hypothesis with explicit kill criteria."""
        hyp = FalsifiableHypothesis(
            claim=claim,
            enabling_condition=enabling_condition,
            falsification_metric=metric,
            falsification_threshold=threshold,
            prior_belief_probability=prior,
            current_belief_probability=prior,
            risk_type=risk_type
        )
        self.active_hypotheses[hyp.id] = hyp
        return hyp

    def update_bayesian_belief(self, test_result: CheapTestResult) -> FalsifiableHypothesis:
        """Sequential Bayesian update of hypothesis belief using test evidence."""
        hyp = self.active_hypotheses[test_result.hypothesis_id]
        prior = hyp.current_belief_probability
        evidence = test_result.evidence_score

        # Bayesian update: P(H|E) = (P(E|H) * P(H)) / P(E)
        p_e_given_h = max(0.01, min(0.99, evidence))
        p_e_given_not_h = max(0.01, min(0.99, 1.0 - evidence))
        numerator = p_e_given_h * prior
        denominator = numerator + (p_e_given_not_h * (1.0 - prior))
        posterior = numerator / max(denominator, 1e-6)

        hyp.current_belief_probability = round(posterior, 4)
        if hyp.current_belief_probability < hyp.falsification_threshold:
            hyp.status = "falsified"
        elif hyp.current_belief_probability >= 0.75:
            hyp.status = "strengthened"
        return hyp

    def update_mental_model(self, model_id: str, prediction_accurate: bool, structural_failure: bool = False) -> MentalModel:
        """Update mental model parameters or structure, calculating ossification score."""
        if model_id not in self.mental_models:
            self.mental_models[model_id] = MentalModel(name=model_id)

        model = self.mental_models[model_id]
        if prediction_accurate:
            model.consecutive_predictions += 1
            model.consecutive_failures = 0
            model.prediction_accuracy = min(1.0, model.prediction_accuracy + 0.05)
        else:
            model.consecutive_failures += 1
            model.consecutive_predictions = 0
            model.prediction_accuracy = max(0.0, model.prediction_accuracy - 0.15)

        # Structural failure without model structure update increases ossification score
        if structural_failure:
            model.ossification_score = min(1.0, model.ossification_score + 0.3)
        else:
            model.ossification_score = max(0.0, model.ossification_score - 0.05)

        return model

    # ------------------------------------------
    # §3 External Business Loops & Leverage Points
    # ------------------------------------------

    def evaluate_business_loops(self, operating_data: Dict[ExternalBusinessLoopType, Dict[str, float]]) -> Dict[ExternalBusinessLoopType, BusinessLoopState]:
        """Evaluate 13 external business loops and calculate stock/flow leverage points."""
        for loop_type, kpi_data in operating_data.items():
            if loop_type in self.business_loops:
                loop = self.business_loops[loop_type]
                loop.core_kpis.update(kpi_data)
                # Simple health rule: negative feedback signals or bad metrics set is_healthy False
                feedback = sum(kpi_data.values()) / max(len(kpi_data), 1)
                loop.feedback_signal = feedback
                loop.is_healthy = feedback >= 0.5
        return self.business_loops

    def calculate_high_leverage_loops(self) -> List[ExternalBusinessLoopType]:
        """Identify high-leverage loops (e.g. Pricing, Hiring) touching multiple stocks/flows."""
        # Pricing touches Cash, Brand, Sales; Hiring touches Talent, Culture, Execution Velocity
        return [ExternalBusinessLoopType.PRICING, ExternalBusinessLoopType.HIRING]

    # ------------------------------------------
    # §4 Customer Journey Lifecycle Pipeline
    # ------------------------------------------

    def evaluate_customer_journey(self, stage_conversions: Dict[JourneyStage, float]) -> List[CustomerJourneyStageMetrics]:
        """Evaluate full 15-stage customer journey lifecycle."""
        journey_defs = [
            (JourneyStage.AWARENESS, "Pattern-matching against categories", "Reach", "Generic messaging", "Sharp category framing"),
            (JourneyStage.INTEREST, "Curiosity vs skepticism", "CTR", "Feature-dumping", "Lead with pain"),
            (JourneyStage.CONSIDERATION, "Comparing status quo", "Time on site", "Competing on shared features", "Reframe comparison axis"),
            (JourneyStage.EVALUATION, "Loss aversion dominates", "Trial starts", "Ignoring risk reduction", "Cheap reversible trial"),
            (JourneyStage.PURCHASE, "Decision fatigue", "Conversion rate", "Checkout friction", "Remove steps"),
            (JourneyStage.ONBOARDING, "Anxiety about wasted decision", "Time to first value", "Feature tour", "Anchor to JTBD"),
            (JourneyStage.ACTIVATION, "Crossing aha threshold", "Activation rate", "Login as activation", "Cohort aha analysis"),
            (JourneyStage.ENGAGEMENT, "Reinforcement learning", "DAU/MAU", "Non-retentive activity", "Optimize predictive behavior"),
            (JourneyStage.HABIT_FORMATION, "Cue-routine-reward loop", "Habit frequency", "No trigger cadence", "Internal/external triggers"),
            (JourneyStage.RETENTION, "Switching cost perception", "Retention curve slope", "Aggregate measuring", "Cohort flattening analysis"),
            (JourneyStage.LOYALTY, "Identity alignment", "Repeat purchase rate", "Satisfaction=loyalty myth", "Build genuine switching costs"),
            (JourneyStage.ADVOCACY, "Social proof seeking", "NPS", "Asking before value", "Ask at peak value"),
            (JourneyStage.REFERRAL, "Trust transfer", "Viral coefficient K", "Generic referral", "Aligned value incentives"),
            (JourneyStage.EXPANSION, "Anchoring to current spend", "NRR", "Underselling adjacent value", "Usage-based triggers"),
            (JourneyStage.REPURCHASE, "Habitual trust", "LTV", "Treating repurchase as passive", "Proactive lifecycle triggers"),
        ]
        results = []
        for stage, psych, metric_name, mistake, lever in journey_defs:
            conv = stage_conversions.get(stage, 0.5)
            results.append(CustomerJourneyStageMetrics(
                stage=stage,
                conversion_rate=conv,
                customer_psychology=psych,
                key_metric_value=conv * 100,
                common_mistake_flagged=conv < 0.3,
                optimization_lever=lever
            ))
        return results

    # ------------------------------------------
    # §5 Go-to-Market Integrated System
    # ------------------------------------------

    def configure_gtm_system(
        self,
        positioning: str,
        comparison_axis: str,
        segment: str,
        pricing_model: str,
        primary_motion: GTMDistributionMotion,
        secondary_motions: List[GTMDistributionMotion]
    ) -> GTMSystemConfig:
        """Configure integrated GTM system ensuring motion compounding."""
        # Simple compounding logic: PLG + Sales-led or Content + PLG creates higher leverage
        compounding = 0.7
        if primary_motion == GTMDistributionMotion.PLG and GTMDistributionMotion.SLG in secondary_motions:
            compounding = 0.95  # Land via PLG, expand via Sales
        elif primary_motion == GTMDistributionMotion.CONTENT and GTMDistributionMotion.PLG in secondary_motions:
            compounding = 0.90

        return GTMSystemConfig(
            positioning_statement=positioning,
            comparison_axis=comparison_axis,
            target_segment=segment,
            pricing_model=pricing_model,
            primary_motion=primary_motion,
            secondary_motions=secondary_motions,
            compounding_motion_score=compounding
        )

    # ------------------------------------------
    # §6 Company Growth System & Premature Scaling
    # ------------------------------------------

    def evaluate_growth_stage(self, metrics: Dict[str, float]) -> GrowthStageStatus:
        """Score growth stage, identifying binding constraints and premature scaling risks."""
        retention_flattened = metrics.get("retention_flattening", 0.0) >= 0.7
        cac_payback = metrics.get("cac_payback_months", 24.0)
        nrr = metrics.get("nrr", 0.9)

        if not retention_flattened and metrics.get("growth_rate", 0.0) > 1.0:
            # High growth without retention flattening = Premature Scaling
            self.growth_status.premature_scaling_risk = 0.9
            self.growth_status.key_risk = "Scaling a broken funnel / Premature scaling"
        else:
            self.growth_status.premature_scaling_risk = 0.1

        if retention_flattened and nrr >= 1.10 and cac_payback <= 12:
            self.growth_status.current_stage = GrowthStage.GROWTH
            self.growth_status.primary_objective = "Scale what works"
            self.growth_status.binding_constraint = "Hiring velocity & systems"
        elif retention_flattened:
            self.growth_status.current_stage = GrowthStage.PMF
            self.growth_status.primary_objective = "Reach retention/growth threshold"
            self.growth_status.binding_constraint = "Team bandwidth"

        return self.growth_status

    # ------------------------------------------
    # §7 Strategic Thinking, Moats & Reinvention
    # ------------------------------------------

    def track_technology_cost_curve(self, tech_name: str, cost_history: List[float], viability_threshold: float) -> TechnologyCostCurve:
        """Track tech cost curves to pinpoint viability inflection points."""
        crossed = len(cost_history) > 0 and cost_history[-1] <= viability_threshold
        curve = TechnologyCostCurve(
            technology_name=tech_name,
            cost_per_unit_trend=cost_history,
            viability_threshold=viability_threshold,
            is_viability_crossed=crossed
        )
        self.cost_curves[tech_name] = curve
        return curve

    def evaluate_moat_strength(self, moat_type: MoatType, score: float, durability: float, copy_cost: float) -> MoatEvaluation:
        """Score competitive moat durability and counter-positioning advantages."""
        eval_res = MoatEvaluation(
            moat_type=moat_type,
            strength_score=score,
            durability_years=durability,
            incumbent_copy_cost=copy_cost
        )
        self.moats[moat_type] = eval_res
        return eval_res

    # ------------------------------------------
    # §8 Failure Mode Analysis Diagnostic
    # ------------------------------------------

    def diagnose_failure_modes(self, metrics: Dict[str, float]) -> List[FailureModeDiagnostic]:
        """Pattern-match operating metrics against 10 explicit failure modes."""
        diagnostics = [
            FailureModeDiagnostic(
                failure_mode="Solving the wrong problem",
                root_cause="Skipped root-cause analysis; solved symptom",
                detection_signal="Low engagement despite positive surveys",
                correction_mechanism="Return to root-cause (5-Whys / JTBD)",
                is_detected=metrics.get("survey_satisfaction", 0.8) > 0.7 and metrics.get("active_usage", 0.2) < 0.3,
                severity=0.85
            ),
            FailureModeDiagnostic(
                failure_mode="Building before validating",
                root_cause="Founder conviction substituted for evidence",
                detection_signal="High build velocity, flat demand signal",
                correction_mechanism="Enforce validation gate before build resourcing",
                is_detected=metrics.get("build_velocity", 0.8) > 0.7 and metrics.get("demand_signal", 0.1) < 0.2,
                severity=0.9
            ),
            FailureModeDiagnostic(
                failure_mode="Weak positioning",
                root_cause="No clear 'instead of X, use us because Y'",
                detection_signal="High CAC, long sales cycles, feature objections",
                correction_mechanism="Rebuild positioning around real customer alternatives",
                is_detected=metrics.get("sales_cycle_days", 100) > 90 and metrics.get("win_rate", 0.1) < 0.15,
                severity=0.75
            ),
            FailureModeDiagnostic(
                failure_mode="Poor pricing",
                root_cause="Cost-plus instead of value-based pricing",
                detection_signal="High conversion at low price, poor margin",
                correction_mechanism="Re-anchor price to quantified customer value",
                is_detected=metrics.get("conversion_rate", 0.5) > 0.4 and metrics.get("gross_margin", 0.2) < 0.4,
                severity=0.8
            ),
            FailureModeDiagnostic(
                failure_mode="Distribution failure",
                root_cause="Great product, no repeatable channel",
                detection_signal="High NPS, flat growth",
                correction_mechanism="Systematically test channels against ICP behavior",
                is_detected=metrics.get("nps", 70) > 60 and metrics.get("growth_rate", 0.01) < 0.05,
                severity=0.85
            ),
            FailureModeDiagnostic(
                failure_mode="Lack of product-market fit",
                root_cause="Premature scaling of unproven loop",
                detection_signal="Retention curve never flattens",
                correction_mechanism="Stop scaling; return to cohort retention work",
                is_detected=metrics.get("retention_flattening", 0.0) < 0.3 and metrics.get("ad_spend_scaled", 0.0) > 0.5,
                severity=0.95
            ),
            FailureModeDiagnostic(
                failure_mode="Organizational bottlenecks",
                root_cause="Decision rights not delegated",
                detection_signal="Rising decision latency, founder single point of failure",
                correction_mechanism="Push decision rights down with clear frameworks",
                is_detected=metrics.get("decision_latency_days", 14) > 10,
                severity=0.7
            ),
            FailureModeDiagnostic(
                failure_mode="Founder bias",
                root_cause="Overconfidence, confirmation bias, sunk cost",
                detection_signal="Ignoring disconfirming data",
                correction_mechanism="Pre-committed kill criteria set before launch",
                is_detected=metrics.get("disconfirming_signals_ignored", 0) >= 3,
                severity=0.9
            ),
            FailureModeDiagnostic(
                failure_mode="Scaling prematurely",
                root_cause="Confusing early demand spike with durable PMF",
                detection_signal="CAC rising faster than LTV as spend scales",
                correction_mechanism="Re-test unit economics at each order-of-magnitude spend",
                is_detected=metrics.get("cac_ltv_ratio", 0.5) > 0.8,
                severity=0.85
            ),
            FailureModeDiagnostic(
                failure_mode="Capital misallocation",
                root_cause="No opportunity-cost discipline in budgeting",
                detection_signal="Multiple underperforming bets funded simultaneously",
                correction_mechanism="Rank initiatives on common expected-return basis quarterly",
                is_detected=metrics.get("underperforming_bets_count", 0) >= 3,
                severity=0.8
            ),
        ]
        return [d for d in diagnostics if d.is_detected]

    # ------------------------------------------
    # §10 State Machine & Decision Tree Evaluator
    # ------------------------------------------

    def evaluate_pursuit_decision_tree(
        self,
        is_structural_anomaly: bool,
        is_reversible_decision: bool,
        high_confidence_multi_source: bool,
        cheap_test_available: bool,
        test_exceeds_kill_threshold: Optional[bool],
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> DecisionTreeResult:
        """Execute Section 10.2 Decision Tree logic."""
        reasons = []
        if not is_structural_anomaly:
            reasons.append("Anomaly is noise, not structural.")
            return DecisionTreeResult(decision="Discard", reasoning=reasons, is_pursued=False, risk_level=DecisionRiskType.TYPE_II)

        risk_type = DecisionRiskType.TYPE_II if is_reversible_decision else DecisionRiskType.TYPE_I

        if not is_reversible_decision and not high_confidence_multi_source:
            reasons.append("Irreversible Type I decision lacks high-confidence multi-source signal.")
            return DecisionTreeResult(decision="Discard", reasoning=reasons, is_pursued=False, risk_level=risk_type)

        if cheap_test_available:
            if test_exceeds_kill_threshold is None:
                reasons.append("Cheap test available; should execute test before committing.")
                return DecisionTreeResult(decision="Run Cheap Test", reasoning=reasons, is_pursued=False, risk_level=risk_type)
            elif not test_exceeds_kill_threshold:
                reasons.append("Cheap test failed kill threshold.")
                return DecisionTreeResult(decision="Discard", reasoning=reasons, is_pursued=False, risk_level=risk_type)
        else:
            if not expected_value_positive:
                reasons.append("Expected value not clearly positive given available data.")
                return DecisionTreeResult(decision="Discard", reasoning=reasons, is_pursued=False, risk_level=risk_type)

        if not has_structural_advantage:
            reasons.append("Lacks structural reason to win or build defensible moat.")
            return DecisionTreeResult(decision="Discard", reasoning=reasons, is_pursued=False, risk_level=risk_type)

        reasons.append("Structural opportunity validated with defensible advantage.")
        return DecisionTreeResult(decision="Commit Resources", reasoning=reasons, is_pursued=True, risk_level=risk_type)

    def rollup_kpi_stack(self) -> Dict[str, float]:
        """Roll up Section 10.4 KPI Stack by subsystem."""
        active_hyps = list(self.active_hypotheses.values())
        validated_count = sum(1 for h in active_hyps if h.status == "strengthened")
        falsified_count = sum(1 for h in active_hyps if h.status == "falsified")

        return {
            "sensing_signal_fidelity": 0.85,
            "validation_falsification_rate": falsified_count / max(len(active_hyps), 1),
            "product_retention_curve_slope": 0.72,
            "gtm_cac_payback_months": 8.5,
            "financial_burn_multiple": 1.2,
            "org_decision_latency_days": 2.5,
            "strategic_moat_durability_score": sum(m.strength_score for m in self.moats.values()) / max(len(self.moats), 1),
            "system_overall_loop_closure_days": 12.0
        }
