"""Entrepreneurial Operating System (EOS) First-Principles Engine.

Implements executable Python models covering all 11 core sections of the
Entrepreneurial Operating System specification.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


# =====================================================================
# 0. Framing & Timescales
# =====================================================================

class LoopTimescale(str, Enum):
    FAST = "fast"      # days - weeks (experiments, sales calls, ad tests, hiring interviews)
    MEDIUM = "medium"  # months - quarters (GTM iteration, pricing changes, org design, capital deployment)
    SLOW = "slow"      # years (strategic positioning, moat construction, market category creation, reinvention)


class CoupledFeedbackLoop(BaseModel):
    loop_id: str
    name: str
    timescale: LoopTimescale
    velocity_days: float
    signal_fidelity: float
    is_compounding: bool = True
    active: bool = True

    def evaluate_compounding(self, retention_delta: float, unit_economics_ratio: float) -> bool:
        """Kills or flags loops that are not compounding value."""
        self.is_compounding = retention_delta > 0 and unit_economics_ratio >= 1.0
        return self.is_compounding


# =====================================================================
# 1. Master Loop Architecture & Re-Entrant State Machine
# =====================================================================

class MasterLoopNode(str, Enum):
    A_ENVIRONMENTAL_SENSING = "Environmental Sensing"
    B_SIGNAL_COLLECTION = "Signal Collection & Knowledge Acquisition"
    C_PATTERN_RECOGNITION = "Pattern Recognition / Mental Model Formation"
    D_OPPORTUNITY_DISCOVERY = "Opportunity & Problem Discovery"
    E_ROOT_CAUSE_ANALYSIS = "Opportunity Evaluation & Root Cause Analysis"
    F_MARKET_VALIDATION = "Customer & Market Validation"
    G_BUSINESS_MODEL_DESIGN = "Business Model & Value Proposition Design"
    H_MVP_EXPERIMENTATION = "MVP Design & Experimentation"
    I_PRODUCT_DEVELOPMENT = "Product Development"
    J_GTM_SYSTEM = "Go-to-Market System"
    K_CUSTOMER_ACQUISITION = "Customer Acquisition"
    L_ONBOARDING_RETENTION = "Onboarding, Activation, Retention"
    M_UNIT_ECONOMICS = "Revenue & Unit Economics Optimization"
    N_ORG_SCALING = "Operations & Org Scaling"
    O_MOAT_CONSTRUCTION = "Competitive Strategy & Moat Construction"
    P_SCALING_EXPANSION = "Scaling & Expansion"
    Q_PLATFORM_ECOSYSTEM = "Platform / Ecosystem Formation"
    R_MARKET_LEADERSHIP = "Market Leadership"
    S_CONTINUOUS_REINVENTION = "Continuous Reinvention"


class MasterLoopOrchestrator:
    """Manages top-level re-entrant Master Loop traversal and kill signal routing."""

    def __init__(self) -> None:
        self.current_node: MasterLoopNode = MasterLoopNode.A_ENVIRONMENTAL_SENSING
        self.execution_history: List[Tuple[MasterLoopNode, datetime]] = []

    def transition_to(self, target_node: MasterLoopNode) -> MasterLoopNode:
        self.current_node = target_node
        self.execution_history.append((target_node, datetime.now()))
        return self.current_node

    def evaluate_kill_and_feedback_signals(self, signal_type: str, metric_value: float) -> MasterLoopNode:
        """Routes kill signals back to re-entrant upstream nodes per Section 1 Master Loop diagram."""
        if signal_type == "validation_kill" and metric_value < 0.3:
            return self.transition_to(MasterLoopNode.D_OPPORTUNITY_DISCOVERY)
        elif signal_type == "mvp_kill" and metric_value < 0.2:
            return self.transition_to(MasterLoopNode.D_OPPORTUNITY_DISCOVERY)
        elif signal_type == "weak_gtm" and metric_value < 1.0:
            return self.transition_to(MasterLoopNode.J_GTM_SYSTEM)
        elif signal_type == "bad_economics" and metric_value < 1.0:
            return self.transition_to(MasterLoopNode.G_BUSINESS_MODEL_DESIGN)

        # Default continuous forward loop
        nodes = list(MasterLoopNode)
        current_idx = nodes.index(self.current_node)
        next_idx = (current_idx + 1) % len(nodes)
        return self.transition_to(nodes[next_idx])


# =====================================================================
# 2. Internal Cognitive Loops & Risk Evaluation
# =====================================================================

class RiskType(str, Enum):
    TYPE_I = "Type I (Irreversible / One-Way Door)"
    TYPE_II = "Type II (Reversible / Two-Way Door)"


class CognitiveSignalToIdeaPipeline(BaseModel):
    signal_id: str = Field(default_factory=lambda: str(uuid4()))
    raw_signal: str
    is_structural_anomaly: bool
    falsifiable_claim: Optional[str] = None
    test_cost_usd: float = 0.0
    belief_confidence: float = 0.5
    status: str = "pending"  # pending, tested, falsified, strengthened

    def evaluate_anomaly(self, is_structural: bool) -> bool:
        self.is_structural_anomaly = is_structural
        if not is_structural:
            self.status = "discarded"
        return self.is_structural_anomaly

    def form_hypothesis(self, claim: str) -> str:
        if not self.is_structural_anomaly:
            raise ValueError("Cannot form hypothesis on non-structural noise signal.")
        self.falsifiable_claim = claim
        return self.falsifiable_claim

    def run_cheap_test(self, test_cost_usd: float, observed_outcome_positive: bool, effect_size: float) -> str:
        self.test_cost_usd = test_cost_usd
        if observed_outcome_positive and effect_size > 0.1:
            self.belief_confidence = min(0.99, self.belief_confidence + 0.3)
            self.status = "strengthened"
        else:
            self.belief_confidence = max(0.01, self.belief_confidence - 0.4)
            self.status = "falsified"
        return self.status

    @staticmethod
    def classify_risk(is_reversible: bool) -> RiskType:
        return RiskType.TYPE_II if is_reversible else RiskType.TYPE_I


class MentalModel(BaseModel):
    model_id: str
    name: str
    parameters: Dict[str, float]
    structural_assumptions: List[str]
    ossified: bool = False

    def update_parameters(self, metric_deltas: Dict[str, float]) -> None:
        """Fast parameter tuning."""
        for k, delta in metric_deltas.items():
            if k in self.parameters:
                self.parameters[k] += delta

    def update_structure(self, new_assumptions: List[str]) -> None:
        """Costly structural paradigm shift."""
        self.structural_assumptions = new_assumptions
        self.ossified = False

    def detect_ossification(self, contradiction_count: int) -> bool:
        """Flags mental model ossification when structural updates are ignored despite repeated contradictions."""
        if contradiction_count >= 3:
            self.ossified = True
        return self.ossified


# =====================================================================
# 3. External Business Loops & Systems Coupling
# =====================================================================

class BusinessLoopType(str, Enum):
    PRODUCT = "Product"
    MARKETING = "Marketing"
    SALES = "Sales"
    CUSTOMER_SUCCESS = "Customer Success"
    BRAND = "Brand"
    PRICING = "Pricing"
    REFERRAL = "Referral"
    DATA = "Data"
    FINANCIAL = "Financial"
    HIRING = "Hiring"
    CULTURE = "Culture"
    INNOVATION = "Innovation"
    COMPETITIVE_INTELLIGENCE = "Competitive Intelligence"


class BusinessLoopState(BaseModel):
    loop_type: BusinessLoopType
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    feedback_signal: Dict[str, Any]
    core_kpi: float
    failure_mode_detected: bool = False

    def evaluate_health(self, kpi_threshold: float) -> bool:
        self.failure_mode_detected = self.core_kpi < kpi_threshold
        return not self.failure_mode_detected


class CoupledBusinessSystemEngine:
    """Couples 13 external business loops as stocks and flows."""

    def __init__(self) -> None:
        self.loops: Dict[BusinessLoopType, BusinessLoopState] = {}
        self.stocks: Dict[str, float] = {
            "cash_usd": 1000000.0,
            "talent_count": 10.0,
            "trust_index": 0.8,
            "data_records": 50000.0
        }

    def register_loop(self, loop_type: BusinessLoopType, state: BusinessLoopState) -> None:
        self.loops[loop_type] = state

    def simulate_coupled_step(self, arpu_usd: float, cac_usd: float, churn_rate: float) -> Dict[str, float]:
        """Simulates coupled feedback: Pricing output (ARPU) -> Financial stock -> Hiring budget -> Product velocity."""
        mrr = (self.stocks["data_records"] * 0.05) * arpu_usd
        burn_rate = self.stocks["talent_count"] * 10000.0
        net_cash_flow = mrr - burn_rate

        self.stocks["cash_usd"] += net_cash_flow

        # Hiring leverage point
        if self.stocks["cash_usd"] > 1500000.0:
            self.stocks["talent_count"] += 2.0

        return {
            "mrr": mrr,
            "net_cash_flow": net_cash_flow,
            "cash_usd": self.stocks["cash_usd"],
            "talent_count": self.stocks["talent_count"]
        }


# =====================================================================
# 4. Customer Journey Lifecycle (15-Stage Engine)
# =====================================================================

class CustomerJourneyStage(str, Enum):
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


class CustomerCohort(BaseModel):
    cohort_id: str
    stage: CustomerJourneyStage = CustomerJourneyStage.AWARENESS
    size: int
    active_count: int
    conversion_rate: float = 1.0
    time_to_first_value_hours: float = 24.0
    k_factor: float = 0.0
    nrr_percent: float = 100.0

    def advance_stage(self, next_stage: CustomerJourneyStage, stage_conversion_rate: float) -> CustomerJourneyStage:
        self.stage = next_stage
        self.conversion_rate = stage_conversion_rate
        self.active_count = int(self.active_count * stage_conversion_rate)
        return self.stage

    def evaluate_aha_activation(self, time_to_value_hours: float) -> bool:
        self.time_to_first_value_hours = time_to_value_hours
        return self.time_to_first_value_hours <= 1.0

    def compute_viral_k_factor(self, invites_per_user: float, invite_conversion_rate: float) -> float:
        self.k_factor = invites_per_user * invite_conversion_rate
        return self.k_factor


# =====================================================================
# 5. Go-to-Market Integrated System Dynamics
# =====================================================================

class PositioningStrategy(BaseModel):
    category_name: str
    target_segment: str
    comparison_axis: str
    value_proposition: str


class PricingMotion(str, Enum):
    SELF_SERVE_PLG = "PLG / Self-Serve"
    SALES_LED_ENTERPRISE = "Sales-Led Enterprise"
    COMMUNITY_LED = "Community-Led"


class GTMIntegratedSystem(BaseModel):
    positioning: PositioningStrategy
    pricing_motion: PricingMotion
    acv_usd: float
    cac_usd: float
    sales_cycle_days: int

    def validate_channel_fit(self) -> bool:
        """Ensures channel choice follows buyer behavior & pricing economics."""
        if self.pricing_motion == PricingMotion.SELF_SERVE_PLG and self.acv_usd > 5000.0:
            return False
        if self.pricing_motion == PricingMotion.SALES_LED_ENTERPRISE and self.acv_usd < 10000.0:
            return False
        return True

    def calculate_payback_period_months(self, gross_margin_percent: float) -> float:
        if self.acv_usd <= 0 or gross_margin_percent <= 0:
            return 999.0
        monthly_gross_profit = (self.acv_usd / 12.0) * (gross_margin_percent / 100.0)
        return float(self.cac_usd / monthly_gross_profit)


# =====================================================================
# 6. Company Growth System (9-Stage Model)
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


class CompanyGrowthTracker(BaseModel):
    stage: GrowthStage = GrowthStage.IDEA
    paying_customers: int = 0
    retention_curve_flattened: bool = False
    rule_of_40_score: float = 0.0
    nrr_percent: float = 100.0
    premature_scaling_risk: bool = False

    def evaluate_stage_transition(self) -> GrowthStage:
        if self.stage == GrowthStage.IDEA and self.paying_customers >= 5:
            self.stage = GrowthStage.VALIDATION
        elif self.stage == GrowthStage.VALIDATION and self.paying_customers >= 20:
            self.stage = GrowthStage.STARTUP
        elif self.stage == GrowthStage.STARTUP and self.retention_curve_flattened:
            self.stage = GrowthStage.PMF
        elif self.stage == GrowthStage.PMF and self.nrr_percent >= 110.0:
            self.stage = GrowthStage.GROWTH
        elif self.stage == GrowthStage.GROWTH and self.rule_of_40_score >= 40.0:
            self.stage = GrowthStage.SCALE
        return self.stage

    def detect_premature_scaling(self, cac_payback_months: float) -> bool:
        """Flags premature scaling if scaling spend before PMF / retention flattening."""
        if not self.retention_curve_flattened and self.stage in [GrowthStage.GROWTH, GrowthStage.SCALE]:
            self.premature_scaling_risk = True
        elif cac_payback_months > 18.0 and self.stage in [GrowthStage.GROWTH, GrowthStage.SCALE]:
            self.premature_scaling_risk = True
        else:
            self.premature_scaling_risk = False
        return self.premature_scaling_risk


# =====================================================================
# 7. Strategic Thinking, Cost Curves & Moat Construction
# =====================================================================

class MoatType(str, Enum):
    NETWORK_EFFECTS = "Network Effects"
    SWITCHING_COSTS = "Switching Costs"
    ECONOMIES_OF_SCALE = "Economies of Scale"
    BRAND_TRUST = "Brand Trust"
    REGULATORY_IP = "Regulatory / IP"
    COUNTER_POSITIONING = "Counter-Positioning"


class MoatEvaluator(BaseModel):
    moat_type: MoatType
    network_density: float = 0.0         # [0, 1]
    switching_cost_usd: float = 0.0
    relative_cost_advantage_pct: float = 0.0
    brand_trust_score: float = 0.0       # [0, 1]

    def compute_durability_score(self) -> float:
        """Calculates normalized Moat Durability Score [0, 1]."""
        score_network = min(1.0, self.network_density)
        score_switching = min(1.0, self.switching_cost_usd / 10000.0)
        score_cost = min(1.0, self.relative_cost_advantage_pct / 100.0)
        score_brand = min(1.0, self.brand_trust_score)

        return float(0.3 * score_network + 0.3 * score_switching + 0.2 * score_cost + 0.2 * score_brand)


class CostCurveAnalysis(BaseModel):
    technology_domain: str
    cost_per_unit_historical: List[Tuple[int, float]]  # [(year, cost)]
    viability_threshold_cost: float

    def predict_viability_year(self) -> Optional[int]:
        """Predicts the crossover year when a cost curve crosses economic viability threshold."""
        if not self.cost_per_unit_historical or len(self.cost_per_unit_historical) < 2:
            return None

        # Linear projection on log-cost
        (y1, c1), (y2, c2) = self.cost_per_unit_historical[-2:]
        if c1 <= 0 or c2 <= 0 or c1 == c2:
            return None

        annual_rate = (c2 - c1) / (y2 - y1)
        if annual_rate >= 0:
            return None  # Cost is not decreasing

        years_needed = (self.viability_threshold_cost - c2) / annual_rate
        return int(y2 + max(0.0, years_needed))


class CapitalOpportunityCostAllocator:
    """Ranks all active internal projects on a common expected-return basis."""

    @staticmethod
    def rank_initiatives(initiatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for init in initiatives:
            ev = init.get("expected_value_usd", 0.0)
            prob = init.get("success_probability", 0.5)
            cost = max(1.0, init.get("capital_required_usd", 1.0))
            init["roi_score"] = (ev * prob) / cost

        return sorted(initiatives, key=lambda x: x["roi_score"], reverse=True)


# =====================================================================
# 8. Failure Mode Analysis & Diagnostic Warnings
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
    SCALING_PREMATURELY = "Scaling prematurely"
    CAPITAL_MISALLOCATION = "Capital misallocation"


class FailureModeDiagnostics:
    """Pattern matches operating metrics against the failure-mode diagnostic table."""

    @staticmethod
    def audit_operating_metrics(metrics: Dict[str, float]) -> List[Tuple[FailureMode, str, str]]:
        warnings = []
        if metrics.get("engagement_rate", 1.0) < 0.10 and metrics.get("survey_satisfaction", 0.0) > 0.8:
            warnings.append((
                FailureMode.SOLVING_WRONG_PROBLEM,
                "Low engagement despite positive survey feedback",
                "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)"
            ))

        if metrics.get("build_velocity_features", 0) > 10 and metrics.get("demand_signal_ctr", 0.0) < 0.01:
            warnings.append((
                FailureMode.BUILDING_BEFORE_VALIDATING,
                "High build velocity with flat demand signal",
                "Enforce a validation gate before build resourcing"
            ))

        if metrics.get("retention_curve_slope", -1.0) < -0.5:
            warnings.append((
                FailureMode.LACK_OF_PMF,
                "Retention curve never flattens",
                "Stop scaling; return to cohort-level retention work"
            ))

        if metrics.get("decision_latency_days", 0.0) > 14.0:
            warnings.append((
                FailureMode.ORGANIZATIONAL_BOTTLENECK,
                "Rising decision latency / founder single point of failure",
                "Push decision rights down with clear frameworks"
            ))

        return warnings


# =====================================================================
# 9. Scientific Foundations Framework Map
# =====================================================================

class DomainFoundation(BaseModel):
    domain: str
    core_concepts: List[str]
    key_sources: List[str]


def get_scientific_foundations() -> List[DomainFoundation]:
    return [
        DomainFoundation(
            domain="Economics",
            core_concepts=["Opportunity cost", "Cost curves", "Market structure"],
            key_sources=["Schumpeter (creative destruction)", "Christensen (disruption theory)"]
        ),
        DomainFoundation(
            domain="Systems Thinking",
            core_concepts=["Stocks/flows", "Feedback loops", "Leverage points"],
            key_sources=["Donella Meadows (Thinking in Systems)"]
        ),
        DomainFoundation(
            domain="Decision Theory",
            core_concepts=["Reversible vs. irreversible decisions", "Real options"],
            key_sources=["McGrath (Discovery-Driven Planning)", "Real options literature"]
        ),
        DomainFoundation(
            domain="Behavioral Economics",
            core_concepts=["Loss aversion", "Anchoring", "Sunk cost"],
            key_sources=["Kahneman & Tversky (Prospect Theory)"]
        ),
        DomainFoundation(
            domain="Cognitive Psychology",
            core_concepts=["Anomaly detection", "Mental model updating"],
            key_sources=["Kuhn (paradigm shifts)", "Bayesian belief updating literature"]
        )
    ]


# =====================================================================
# 10. Integrated AI-EOS Decision Tree & Subsystem Engine
# =====================================================================

class DecisionTreeResult(str, Enum):
    DISCARD = "Discard"
    RUN_CHEAP_TEST = "Run cheap test"
    COMMIT_RESOURCES = "Commit resources"


class OpportunityDecisionTree:
    """Implements Section 10.2 Decision Tree: Should We Pursue This Opportunity?"""

    @staticmethod
    def evaluate_opportunity(
        is_structural_anomaly: bool,
        is_reversible: bool,
        high_confidence_multi_source: bool,
        cheap_test_available: bool,
        test_result_exceeds_kill_threshold: bool,
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> DecisionTreeResult:
        if not is_structural_anomaly:
            return DecisionTreeResult.DISCARD

        if not is_reversible:
            if not high_confidence_multi_source:
                return DecisionTreeResult.DISCARD

        if cheap_test_available:
            if not test_result_exceeds_kill_threshold:
                return DecisionTreeResult.DISCARD
        else:
            if not expected_value_positive:
                return DecisionTreeResult.DISCARD

        if not has_structural_advantage:
            return DecisionTreeResult.DISCARD

        return DecisionTreeResult.COMMIT_RESOURCES


class AIEOSSubsystemState(BaseModel):
    sensing_lead_time_days: float = 3.0
    cost_per_validated_learning_usd: float = 150.0
    activation_rate_pct: float = 45.0
    cac_payback_months: float = 8.0
    burn_multiple: float = 1.2
    decision_latency_days: float = 2.0
    moat_durability_score: float = 0.75
    loop_closure_time_days: float = 5.0


class FullAIEOSSystemOrchestrator:
    """Master orchestrator executing the 10-module AI-EOS architecture."""

    def __init__(self) -> None:
        self.master_loop = MasterLoopOrchestrator()
        self.coupled_business_engine = CoupledBusinessSystemEngine()
        self.growth_tracker = CompanyGrowthTracker()
        self.kpi_stack = AIEOSSubsystemState()

    def run_full_execution_cycle(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Runs an integrated cycle across sensing, validation, GTM, and failure diagnostics."""
        # 1. Diagnostic audit
        warnings = FailureModeDiagnostics.audit_operating_metrics(metrics)

        # 2. Growth stage evaluation
        current_stage = self.growth_tracker.evaluate_stage_transition()
        premature_risk = self.growth_tracker.detect_premature_scaling(self.kpi_stack.cac_payback_months)

        # 3. Traversal step
        next_node = self.master_loop.evaluate_kill_and_feedback_signals(
            signal_type="weak_gtm" if self.kpi_stack.cac_payback_months > 18 else "none",
            metric_value=metrics.get("gtm_quality", 1.5)
        )

        return {
            "current_stage": current_stage,
            "premature_scaling_risk": premature_risk,
            "master_loop_node": next_node,
            "failure_warnings": warnings,
            "kpi_stack": self.kpi_stack
        }
