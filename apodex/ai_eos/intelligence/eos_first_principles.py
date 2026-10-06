"""First-Principles Executable Engine for the Entrepreneurial Operating System (EOS).

Implements the 11-section architecture of how elite founders sense, build,
and compound enduring companies across fast, medium, and slow feedback loops.
"""

from __future__ import annotations
import math
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Set
from datetime import datetime, timezone

logger = logging.getLogger("apodex.ai_eos.eos_first_principles")


# =====================================================================
# 0 & 1. Master Loop Engine
# =====================================================================

class MasterLoopNode(str, Enum):
    A_ENVIRONMENTAL_SENSING = "A_Environmental_Sensing"
    B_SIGNAL_COLLECTION = "B_Signal_Collection"
    C_PATTERN_RECOGNITION = "C_Pattern_Recognition"
    D_OPPORTUNITY_DISCOVERY = "D_Opportunity_Discovery"
    E_ROOT_CAUSE_ANALYSIS = "E_Root_Cause_Analysis"
    F_CUSTOMER_VALIDATION = "F_Customer_Validation"
    G_BUSINESS_MODEL_DESIGN = "G_Business_Model_Design"
    H_MVP_EXPERIMENTATION = "H_MVP_Experimentation"
    I_PRODUCT_DEVELOPMENT = "I_Product_Development"
    J_GTM_SYSTEM = "J_GTM_System"
    K_CUSTOMER_ACQUISITION = "K_Customer_Acquisition"
    L_ONBOARDING_RETENTION = "L_Onboarding_Retention"
    M_UNIT_ECONOMICS = "M_Unit_Economics"
    N_OPERATIONS_SCALING = "N_Operations_Scaling"
    O_MOAT_CONSTRUCTION = "O_Moat_Construction"
    P_SCALING_EXPANSION = "P_Scaling_Expansion"
    Q_PLATFORM_ECOSYSTEM = "Q_Platform_Ecosystem"
    R_MARKET_LEADERSHIP = "R_Market_Leadership"
    S_CONTINUOUS_REINVENTION = "S_Continuous_Reinvention"


@dataclass
class MasterLoopExecutionState:
    current_node: MasterLoopNode = MasterLoopNode.A_ENVIRONMENTAL_SENSING
    fast_loop_velocity_days: float = 7.0
    medium_loop_velocity_months: float = 3.0
    slow_loop_velocity_years: float = 2.0
    kill_signals_triggered: List[Dict[str, str]] = field(default_factory=list)
    node_history: List[MasterLoopNode] = field(default_factory=list)


class MasterLoopEngine:
    """Orchestrates the 19-node Master Loop with re-entrant loops and kill signals."""

    def __init__(self) -> None:
        self.state = MasterLoopExecutionState()
        self.node_transitions: Dict[MasterLoopNode, MasterLoopNode] = {
            MasterLoopNode.A_ENVIRONMENTAL_SENSING: MasterLoopNode.B_SIGNAL_COLLECTION,
            MasterLoopNode.B_SIGNAL_COLLECTION: MasterLoopNode.C_PATTERN_RECOGNITION,
            MasterLoopNode.C_PATTERN_RECOGNITION: MasterLoopNode.D_OPPORTUNITY_DISCOVERY,
            MasterLoopNode.D_OPPORTUNITY_DISCOVERY: MasterLoopNode.E_ROOT_CAUSE_ANALYSIS,
            MasterLoopNode.E_ROOT_CAUSE_ANALYSIS: MasterLoopNode.F_CUSTOMER_VALIDATION,
            MasterLoopNode.F_CUSTOMER_VALIDATION: MasterLoopNode.G_BUSINESS_MODEL_DESIGN,
            MasterLoopNode.G_BUSINESS_MODEL_DESIGN: MasterLoopNode.H_MVP_EXPERIMENTATION,
            MasterLoopNode.H_MVP_EXPERIMENTATION: MasterLoopNode.I_PRODUCT_DEVELOPMENT,
            MasterLoopNode.I_PRODUCT_DEVELOPMENT: MasterLoopNode.J_GTM_SYSTEM,
            MasterLoopNode.J_GTM_SYSTEM: MasterLoopNode.K_CUSTOMER_ACQUISITION,
            MasterLoopNode.K_CUSTOMER_ACQUISITION: MasterLoopNode.L_ONBOARDING_RETENTION,
            MasterLoopNode.L_ONBOARDING_RETENTION: MasterLoopNode.M_UNIT_ECONOMICS,
            MasterLoopNode.M_UNIT_ECONOMICS: MasterLoopNode.N_OPERATIONS_SCALING,
            MasterLoopNode.N_OPERATIONS_SCALING: MasterLoopNode.O_MOAT_CONSTRUCTION,
            MasterLoopNode.O_MOAT_CONSTRUCTION: MasterLoopNode.P_SCALING_EXPANSION,
            MasterLoopNode.P_SCALING_EXPANSION: MasterLoopNode.Q_PLATFORM_ECOSYSTEM,
            MasterLoopNode.Q_PLATFORM_ECOSYSTEM: MasterLoopNode.R_MARKET_LEADERSHIP,
            MasterLoopNode.R_MARKET_LEADERSHIP: MasterLoopNode.S_CONTINUOUS_REINVENTION,
            MasterLoopNode.S_CONTINUOUS_REINVENTION: MasterLoopNode.A_ENVIRONMENTAL_SENSING,
        }

    def advance(self, signal: Optional[Dict[str, Any]] = None) -> MasterLoopNode:
        """Advance state machine or execute kill signal re-entrancy."""
        signal = signal or {}
        curr = self.state.current_node
        self.state.node_history.append(curr)

        # Check Kill Signals
        if curr == MasterLoopNode.F_CUSTOMER_VALIDATION and signal.get("falsified"):
            self.state.kill_signals_triggered.append({"from": "F", "to": "D", "reason": signal.get("reason", "Validation failed")})
            self.state.current_node = MasterLoopNode.D_OPPORTUNITY_DISCOVERY
            return self.state.current_node

        if curr == MasterLoopNode.H_MVP_EXPERIMENTATION and signal.get("falsified"):
            self.state.kill_signals_triggered.append({"from": "H", "to": "D", "reason": signal.get("reason", "MVP failed")})
            self.state.current_node = MasterLoopNode.D_OPPORTUNITY_DISCOVERY
            return self.state.current_node

        if curr == MasterLoopNode.K_CUSTOMER_ACQUISITION and signal.get("weak_gtm"):
            self.state.kill_signals_triggered.append({"from": "K", "to": "J", "reason": signal.get("reason", "Weak GTM conversion")})
            self.state.current_node = MasterLoopNode.J_GTM_SYSTEM
            return self.state.current_node

        if curr == MasterLoopNode.M_UNIT_ECONOMICS and signal.get("bad_economics"):
            self.state.kill_signals_triggered.append({"from": "M", "to": "G", "reason": signal.get("reason", "Unviable unit economics")})
            self.state.current_node = MasterLoopNode.G_BUSINESS_MODEL_DESIGN
            return self.state.current_node

        self.state.current_node = self.node_transitions[curr]
        return self.state.current_node


# =====================================================================
# 2. Internal Cognitive Loops
# =====================================================================

class DecisionRiskType(str, Enum):
    TYPE_I_IRREVERSIBLE = "Type_I_Irreversible_One_Way_Door"
    TYPE_II_REVERSIBLE = "Type_II_Reversible_Two_Way_Door"


@dataclass
class AnomalySignal:
    signal_id: str
    description: str
    is_structural_shift: bool
    observed_value: float
    expected_value: float
    confidence: float = 0.5


@dataclass
class FounderHypothesis:
    hypothesis_id: str
    claim: str
    kill_criteria: str
    prior_belief: float = 0.5
    posterior_belief: float = 0.5
    risk_type: DecisionRiskType = DecisionRiskType.TYPE_II_REVERSIBLE
    test_cost: float = 1000.0


class CognitiveLoopsEngine:
    """Implements Signal-to-Idea Pipeline and Mental Model Evolution."""

    def __init__(self) -> None:
        self.active_hypotheses: List[FounderHypothesis] = []
        self.mental_model_structure: Dict[str, Any] = {
            "version": 1,
            "core_axioms": ["Demand is driven by workflow bottleneck"],
            "parameters": {"market_growth": 0.15, "elasticity": -1.2},
        }
        self.ossification_risk_score: float = 0.0
        self.consecutive_parameter_only_updates: int = 0

    def evaluate_signal(self, signal: AnomalySignal) -> Optional[FounderHypothesis]:
        """Signal-to-Idea Pipeline filter."""
        if not signal.is_structural_shift:
            logger.info("Discarding signal %s as noise.", signal.signal_id)
            return None

        # Forced hypothesis generation
        risk = DecisionRiskType.TYPE_I_IRREVERSIBLE if signal.observed_value > 10.0 else DecisionRiskType.TYPE_II_REVERSIBLE
        hyp = FounderHypothesis(
            hypothesis_id=f"hyp_{signal.signal_id}",
            claim=f"Structural anomaly in {signal.description} indicates market viability",
            kill_criteria="Cheap test conversion rate < 5%",
            prior_belief=signal.confidence,
            posterior_belief=signal.confidence,
            risk_type=risk,
            test_cost=500.0 if risk == DecisionRiskType.TYPE_II_REVERSIBLE else 10000.0,
        )
        self.active_hypotheses.append(hyp)
        return hyp

    def run_cheap_test(self, hypothesis_id: str, test_data: Dict[str, Any]) -> float:
        """Run cheap experiment and execute Bayesian belief update."""
        hyp = next((h for h in self.active_hypotheses if h.hypothesis_id == hypothesis_id), None)
        if not hyp:
            raise ValueError(f"Hypothesis {hypothesis_id} not found.")

        success = test_data.get("success", False)
        likelihood_if_true = test_data.get("likelihood_true", 0.8)
        likelihood_if_false = test_data.get("likelihood_false", 0.2)

        prior = hyp.posterior_belief
        if success:
            numerator = likelihood_if_true * prior
            denominator = numerator + (likelihood_if_false * (1.0 - prior))
        else:
            numerator = (1.0 - likelihood_if_true) * prior
            denominator = numerator + ((1.0 - likelihood_if_false) * (1.0 - prior))

        hyp.posterior_belief = numerator / max(denominator, 1e-9)
        self._update_mental_model(hypothesis_success=success, structural_change=(hyp.posterior_belief > 0.85))
        return hyp.posterior_belief

    def _update_mental_model(self, hypothesis_success: bool, structural_change: bool) -> None:
        """Evolve mental model structure vs parameter tuning."""
        if structural_change:
            self.mental_model_structure["version"] += 1
            self.mental_model_structure["core_axioms"].append(f"Axiom_v{self.mental_model_structure['version']}")
            self.consecutive_parameter_only_updates = 0
            self.ossification_risk_score = max(0.0, self.ossification_risk_score - 0.3)
        else:
            self.consecutive_parameter_only_updates += 1
            if self.consecutive_parameter_only_updates > 5:
                self.ossification_risk_score = min(1.0, self.ossification_risk_score + 0.2)


# =====================================================================
# 3. External Business Loops Engine
# =====================================================================

@dataclass
class BusinessLoopState:
    loop_name: str
    inputs: List[str]
    outputs: List[str]
    feedback_signal: str
    kpis: Dict[str, float]
    failure_mode: str


class ExternalBusinessLoopsEngine:
    """Manages 13 coupled feedback loops and stock/flow dynamics."""

    def __init__(self) -> None:
        self.stocks = {
            "cash": 1_000_000.0,
            "talent_count": 10.0,
            "trust_score": 0.8,
            "data_assets": 100.0,
        }
        self.loops: Dict[str, BusinessLoopState] = {
            "Product": BusinessLoopState("Product", ["User behavior", "Usage data"], ["Feature changes"], "Activation deltas", {"retention": 0.45, "nps": 55.0}, "Building for loudest customer"),
            "Marketing": BusinessLoopState("Marketing", ["Positioning", "Market data"], ["Awareness"], "CAC", {"cac": 150.0, "conversion": 0.03}, "Message-market mismatch"),
            "Sales": BusinessLoopState("Sales", ["Qualified leads"], ["Closed revenue"], "Win/loss reasons", {"win_rate": 0.25, "acv": 12000.0}, "Selling to non-ICP"),
            "CustomerSuccess": BusinessLoopState("CustomerSuccess", ["Onboarding data"], ["Retention"], "Churn reasons", {"nrr": 1.15, "churn_rate": 0.02}, "Reactive CS"),
            "Brand": BusinessLoopState("Brand", ["Product experience"], ["Trust"], "Sentiment", {"price_elasticity": -0.8}, "Brand as decoration"),
            "Pricing": BusinessLoopState("Pricing", ["Value delivered"], ["Revenue"], "Price conversion", {"arpu": 100.0}, "Cost-plus pricing"),
            "Referral": BusinessLoopState("Referral", ["Satisfaction"], ["New flow"], "Viral rate", {"viral_k": 0.4}, "Volume over quality"),
            "Data": BusinessLoopState("Data", ["Usage logs"], ["Decisions"], "Model accuracy", {"decision_cycle_hours": 24.0}, "Vanity metrics"),
            "Financial": BusinessLoopState("Financial", ["Revenue", "Costs"], ["Runway"], "Burn trend", {"gross_margin": 0.75, "burn_multiple": 1.2, "runway_months": 18.0}, "Negative unit economics"),
            "Hiring": BusinessLoopState("Hiring", ["Org needs"], ["Capacity"], "90-day performance", {"time_to_fill_days": 30.0}, "Pedigree over role-fit"),
            "Culture": BusinessLoopState("Culture", ["Values-in-action"], ["Consistency"], "Employee sentiment", {"enps": 60.0}, "Values-as-poster"),
            "Innovation": BusinessLoopState("Innovation", ["R&D", "Market signals"], ["New lines"], "Time-to-market", {"experiments_run": 12.0}, "Innovation theater"),
            "CompetitiveIntelligence": BusinessLoopState("CompetitiveIntelligence", ["Competitor data"], ["Repositioning"], "Win/loss", {"market_share": 0.12}, "Reacting instead of leading"),
        }

    def simulate_quarter(self) -> Dict[str, float]:
        """Execute coupled loop dynamics and update stocks."""
        # Coupling dynamics: Pricing ARPU -> Financial Revenue -> Hiring Budget -> Product Velocity
        arpu = self.loops["Pricing"].kpis["arpu"]
        win_rate = self.loops["Sales"].kpis["win_rate"]
        acv = self.loops["Sales"].kpis["acv"]

        quarterly_revenue = win_rate * acv * 10.0
        quarterly_burn = self.stocks["talent_count"] * 25000.0
        net_flow = quarterly_revenue - quarterly_burn

        self.stocks["cash"] += net_flow
        self.loops["Financial"].kpis["runway_months"] = max(0.0, self.stocks["cash"] / max(quarterly_burn / 3.0, 1.0))
        return self.stocks.copy()


# =====================================================================
# 4. Customer Journey Lifecycle Engine
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
    HABIT_FORMATION = "Habit_Formation"
    RETENTION = "Retention"
    LOYALTY = "Loyalty"
    ADVOCACY = "Advocacy"
    REFERRAL = "Referral"
    EXPANSION = "Expansion"
    REPURCHASE = "Repurchase"


@dataclass
class LifecycleStageConfig:
    stage: CustomerJourneyStage
    founder_objective: str
    customer_psychology: str
    key_metric: str
    common_mistake: str
    optimization_lever: str
    conversion_rate: float = 0.1


class CustomerLifecycleEngine:
    """Manages the 15-stage Customer Journey lifecycle."""

    def __init__(self) -> None:
        self.stages: Dict[CustomerJourneyStage, LifecycleStageConfig] = {
            CustomerJourneyStage.AWARENESS: LifecycleStageConfig(CustomerJourneyStage.AWARENESS, "Enter consideration set", "Pattern-matching", "Reach", "Generic messaging", "Sharp category framing", 0.20),
            CustomerJourneyStage.INTEREST: LifecycleStageConfig(CustomerJourneyStage.INTEREST, "Earn attention", "Curiosity vs skepticism", "CTR", "Feature-dumping", "Lead with pain", 0.15),
            CustomerJourneyStage.CONSIDERATION: LifecycleStageConfig(CustomerJourneyStage.CONSIDERATION, "Differentiate", "Comparing alternatives", "Time on site", "Competing on standard features", "Reframe comparison axis", 0.25),
            CustomerJourneyStage.EVALUATION: LifecycleStageConfig(CustomerJourneyStage.EVALUATION, "Reduce risk", "Loss aversion dominates", "Trial starts", "Ignoring risk-reduction", "Make failure cheap", 0.30),
            CustomerJourneyStage.PURCHASE: LifecycleStageConfig(CustomerJourneyStage.PURCHASE, "Convert intent", "Decision fatigue", "Conversion rate", "Checkout friction", "Remove steps", 0.40),
            CustomerJourneyStage.ONBOARDING: LifecycleStageConfig(CustomerJourneyStage.ONBOARDING, "Deliver fast value", "Anxiety", "Time-to-first-value", "Feature-tour", "Anchor to JTBD", 0.60),
            CustomerJourneyStage.ACTIVATION: LifecycleStageConfig(CustomerJourneyStage.ACTIVATION, "Cross aha threshold", "Initial habit loop", "Activation rate", "Defining activation as login", "Cohort aha analysis", 0.50),
            CustomerJourneyStage.ENGAGEMENT: LifecycleStageConfig(CustomerJourneyStage.ENGAGEMENT, "Build depth", "Reinforcement learning", "DAU/MAU", "Uncorrelated engagement", "Optimize for retention predictor", 0.70),
            CustomerJourneyStage.HABIT_FORMATION: LifecycleStageConfig(CustomerJourneyStage.HABIT_FORMATION, "Make usage automatic", "Cue-routine-reward", "Habit frequency", "No trigger cadence", "Build internal+external triggers", 0.65),
            CustomerJourneyStage.RETENTION: LifecycleStageConfig(CustomerJourneyStage.RETENTION, "Prevent churn", "Switching costs", "Retention curve", "Aggregate measuring", "Cohort flattening analysis", 0.80),
            CustomerJourneyStage.LOYALTY: LifecycleStageConfig(CustomerJourneyStage.LOYALTY, "Deepen lock-in", "Identity alignment", "Repeat purchase rate", "Assuming satisfaction=loyalty", "Build genuine switching costs", 0.75),
            CustomerJourneyStage.ADVOCACY: LifecycleStageConfig(CustomerJourneyStage.ADVOCACY, "Convert satisfaction to voice", "Social proof", "NPS", "Asking before value proven", "Ask at peak-value moments", 0.20),
            CustomerJourneyStage.REFERRAL: LifecycleStageConfig(CustomerJourneyStage.REFERRAL, "Convert advocacy to acquisition", "Trust transfer", "Viral coefficient K", "Generic referral programs", "Align incentive with value", 0.15),
            CustomerJourneyStage.EXPANSION: LifecycleStageConfig(CustomerJourneyStage.EXPANSION, "Grow account value", "Anchoring spend", "NRR", "Underselling adjacent value", "Usage-based triggers", 0.30),
            CustomerJourneyStage.REPURCHASE: LifecycleStageConfig(CustomerJourneyStage.REPURCHASE, "Sustain LTV", "Habitual trust", "Repurchase rate", "Treating repurchase as passive", "Proactive lifecycle marketing", 0.85),
        }

    def compute_funnel_efficiency(self, cohort_size: int = 10000) -> Dict[str, float]:
        """Compute end-to-end customer survival and lifecycle throughput."""
        current = float(cohort_size)
        results = {}
        for stage_enum in CustomerJourneyStage:
            cfg = self.stages[stage_enum]
            current *= cfg.conversion_rate
            results[cfg.stage.value] = current
        return results


# =====================================================================
# 5. Go-to-Market System Simulator
# =====================================================================

class GTMChannel(str, Enum):
    PLG = "Product-Led Growth"
    SLG = "Sales-Led Growth"
    CLG = "Community-Led Growth"
    ORGANIC = "Organic Growth"
    PAID = "Paid Acquisition"
    PARTNERSHIPS = "Partnerships"
    CONTENT = "Content Strategy"


class GTMSystemSimulator:
    """Models integrated GTM system dynamics (positioning, pricing, channels)."""

    def simulate_channel_fit(
        self,
        positioning_type: str,  # "Self-Serve" vs "Enterprise"
        price_point_acv: float,
        target_channel: GTMChannel,
    ) -> Dict[str, Any]:
        """Evaluate channel compatibility and system logic."""
        fit_score = 0.5
        reason = "Moderate fit"

        if price_point_acv < 5000 and target_channel in [GTMChannel.PLG, GTMChannel.ORGANIC, GTMChannel.CONTENT]:
            fit_score = 0.95
            reason = "High efficiency for low-complexity, self-serve buyer behavior."
        elif price_point_acv >= 50000 and target_channel in [GTMChannel.SLG]:
            fit_score = 0.90
            reason = "High ACV justifies enterprise sales-led motion."
        elif price_point_acv < 5000 and target_channel == GTMChannel.SLG:
            fit_score = 0.15
            reason = "Low ACV cannot sustain sales-led field sales CAC."

        return {
            "positioning": positioning_type,
            "acv": price_point_acv,
            "channel": target_channel.value,
            "fit_score": fit_score,
            "system_recommendation": reason,
        }


# =====================================================================
# 6. Company Growth System State Machine
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


@dataclass
class StageProfile:
    stage: GrowthStage
    primary_objective: str
    binding_constraint: str
    key_risk: str
    core_metric: str


class CompanyGrowthStateMachine:
    """Tracks company evolution through 9 growth stages."""

    def __init__(self) -> None:
        self.current_stage = GrowthStage.IDEA
        self.profiles: Dict[GrowthStage, StageProfile] = {
            GrowthStage.IDEA: StageProfile(GrowthStage.IDEA, "Falsify or strengthen hypothesis", "Founder time", "Solving non-problem", "# validated learnings"),
            GrowthStage.VALIDATION: StageProfile(GrowthStage.VALIDATION, "Prove willingness to pay", "Signal quality", "False positive validation", "Paying customers / LOIs"),
            GrowthStage.STARTUP: StageProfile(GrowthStage.STARTUP, "Build repeatable acquisition", "Cash runway", "Premature scaling before PMF", "CAC:LTV early signal"),
            GrowthStage.PMF: StageProfile(GrowthStage.PMF, "Reach retention threshold", "Team bandwidth", "Mistaking early traction for PMF", "Retention curve flattening"),
            GrowthStage.GROWTH: StageProfile(GrowthStage.GROWTH, "Scale what works", "Hiring velocity", "Scaling broken funnel", "Growth rate & CAC payback"),
            GrowthStage.SCALE: StageProfile(GrowthStage.SCALE, "Institutionalize repeatability", "Org coordination cost", "Bureaucracy creep", "Rule of 40 & NRR"),
            GrowthStage.PLATFORM: StageProfile(GrowthStage.PLATFORM, "Enable third-parties", "Trust from partners", "Platform without demand", "3rd-party developer activity"),
            GrowthStage.ECOSYSTEM: StageProfile(GrowthStage.ECOSYSTEM, "Orchestrate multi-sided network", "Governance credibility", "Ecosystem fragmentation", "Ecosystem GMV & density"),
            GrowthStage.MARKET_LEADERSHIP: StageProfile(GrowthStage.MARKET_LEADERSHIP, "Defend & extend category", "Innovation velocity", "Incumbency drag", "Category share & moat score"),
        }

    def evaluate_transition(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Check criteria for advancing to next growth stage."""
        curr = self.current_stage
        advanced = False

        if curr == GrowthStage.IDEA and metrics.get("validated_learnings", 0) >= 3:
            self.current_stage = GrowthStage.VALIDATION
            advanced = True
        elif curr == GrowthStage.VALIDATION and metrics.get("paying_customers", 0) >= 5:
            self.current_stage = GrowthStage.STARTUP
            advanced = True
        elif curr == GrowthStage.STARTUP and metrics.get("retention_flattened", False):
            self.current_stage = GrowthStage.PMF
            advanced = True
        elif curr == GrowthStage.PMF and metrics.get("nrr", 0.0) >= 1.10:
            self.current_stage = GrowthStage.GROWTH
            advanced = True

        return {
            "previous_stage": curr.value,
            "current_stage": self.current_stage.value,
            "advanced": advanced,
            "active_profile": self.profiles[self.current_stage],
        }


# =====================================================================
# 7. Strategic Thinking & Moat Engine
# =====================================================================

class MoatType(str, Enum):
    NETWORK_EFFECTS = "Network Effects"
    SWITCHING_COSTS = "Switching Costs"
    ECONOMIES_OF_SCALE = "Economies of Scale"
    BRAND = "Brand"
    REGULATORY_IP = "Regulatory / IP"
    COUNTER_POSITIONING = "Counter-Positioning"


class StrategicMoatEngine:
    """Evaluates competitive moats, cost curves, and timing advantage."""

    def evaluate_moat_durability(self, moat_type: MoatType, characteristics: Dict[str, Any]) -> float:
        """Score durability of moat (0.0 to 1.0)."""
        score = 0.5
        if moat_type == MoatType.COUNTER_POSITIONING and characteristics.get("incumbent_business_model_conflict", False):
            score = 0.92
        elif moat_type == MoatType.NETWORK_EFFECTS and characteristics.get("data_flywheel_active", False):
            score = 0.88
        elif moat_type == MoatType.SWITCHING_COSTS and characteristics.get("workflow_embedding_depth", 0) > 3:
            score = 0.85
        return score

    def evaluate_cost_curve_viability(self, current_unit_cost: float, annual_cost_decline_rate: float, threshold_cost: float) -> int:
        """Calculate years until cost curve crosses economic viability threshold."""
        if current_unit_cost <= threshold_cost:
            return 0
        if annual_cost_decline_rate <= 0.0:
            return 999

        years = math.ceil(math.log(threshold_cost / current_unit_cost) / math.log(1.0 - annual_cost_decline_rate))
        return max(0, years)


# =====================================================================
# 8. Failure Mode Monitor
# =====================================================================

@dataclass
class FailureModeDiagnostics:
    failure_mode: str
    root_cause: str
    detection_signal: str
    correction_mechanism: str
    triggered: bool = False


class FailureModeMonitor:
    """Pattern-matches operating metrics against the 10 core failure modes."""

    def __init__(self) -> None:
        self.catalog = [
            FailureModeDiagnostics("Solving the wrong problem", "Skipped root-cause analysis", "Low engagement despite survey feedback", "5-Whys / JTBD interviews"),
            FailureModeDiagnostics("Building before validating", "Conviction substituted for evidence", "High build velocity, flat demand", "Enforce validation gate"),
            FailureModeDiagnostics("Weak positioning", "No clear differentiation vs alternative", "High CAC, long sales cycle", "Rebuild positioning around real alternative"),
            FailureModeDiagnostics("Poor pricing", "Cost-plus pricing", "High conversion at low price, poor margin", "Re-anchor price to value"),
            FailureModeDiagnostics("Distribution failure", "No repeatable channel", "High NPS, flat growth", "Test channels against ICP behavior"),
            FailureModeDiagnostics("Lack of PMF", "Premature scaling of unproven loop", "Retention curve never flattens", "Stop scaling; fix cohort retention"),
            FailureModeDiagnostics("Organizational bottlenecks", "Decision rights not delegated", "Rising decision latency", "Push decision rights down"),
            FailureModeDiagnostics("Founder bias", "Overconfidence / sunk cost", "Ignoring disconfirming data", "Pre-committed kill criteria"),
            FailureModeDiagnostics("Scaling prematurely", "Confusing demand spike with PMF", "CAC rising faster than LTV", "Re-test unit economics"),
            FailureModeDiagnostics("Capital misallocation", "No opportunity-cost discipline", "Multiple underperforming bets funded", "Rank initiatives on expected-return"),
        ]

    def audit_metrics(self, metrics: Dict[str, Any]) -> List[FailureModeDiagnostics]:
        """Audit company metrics and trigger failure warnings."""
        warnings = []
        # Premature scaling check
        if metrics.get("cac_growth_rate", 0.0) > metrics.get("ltv_growth_rate", 0.0) and metrics.get("spend_scaling", False):
            d = next(f for f in self.catalog if f.failure_mode == "Scaling prematurely")
            d.triggered = True
            warnings.append(d)

        # Lack of PMF check
        if metrics.get("retention_curve_slope", -0.1) < -0.01 and metrics.get("marketing_spend", 0) > 100000:
            d = next(f for f in self.catalog if f.failure_mode == "Lack of PMF")
            d.triggered = True
            warnings.append(d)

        return warnings


# =====================================================================
# 10. Integrated AI Operating System (EOSEngineFirstPrinciples)
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


class EOSOpportunityDecisionTree:
    """Executes Section 10.2 Decision Tree: Should We Pursue This Opportunity?"""

    def evaluate(self, opportunity_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Run decision tree Q1 through Q5."""
        # Q1: Structural anomaly or just noise?
        if not opportunity_data.get("is_structural_anomaly", False):
            return False, "Discard: Anomaly is noise, not structural."

        # Q2: Reversible decision?
        is_reversible = opportunity_data.get("is_reversible_decision", True)
        if not is_reversible:
            if not opportunity_data.get("high_confidence_multi_source_signal", False):
                return False, "Discard: Irreversible decision lacks high-confidence multi-source signal."

        # Q3: Cheap test available?
        cheap_test = opportunity_data.get("cheap_test_available", True)
        if cheap_test:
            test_passed = opportunity_data.get("test_exceeds_kill_threshold", False)
            if not test_passed:
                return False, "Discard: Cheap test failed to cross pre-committed kill threshold."
        else:
            ev_positive = opportunity_data.get("expected_value_positive", False)
            if not ev_positive:
                return False, "Discard: Expected value is not clearly positive."

        # Q5: Structural advantage?
        if not opportunity_data.get("has_or_can_build_structural_advantage", False):
            return False, "Discard: No structural advantage attainable."

        return True, "Go: Commit resources to opportunity."


class EOSEngineFirstPrinciples:
    """Top-level orchestrator integrating the 11-section EOS architecture."""

    def __init__(self) -> None:
        self.system_state = SystemState.SENSING
        self.master_loop = MasterLoopEngine()
        self.cognitive_loops = CognitiveLoopsEngine()
        self.business_loops = ExternalBusinessLoopsEngine()
        self.customer_lifecycle = CustomerLifecycleEngine()
        self.gtm_simulator = GTMSystemSimulator()
        self.growth_state_machine = CompanyGrowthStateMachine()
        self.moat_engine = StrategicMoatEngine()
        self.failure_monitor = FailureModeMonitor()
        self.decision_tree = EOSOpportunityDecisionTree()

        # System KPI Stack (Section 10.4)
        self.kpi_stack = {
            "signal_to_noise_ratio": 3.5,
            "cost_per_validated_learning": 450.0,
            "activation_rate": 0.42,
            "cac": 120.0,
            "cac_payback_months": 7.5,
            "gross_margin": 0.78,
            "burn_multiple": 1.1,
            "decision_latency_hours": 12.0,
            "moat_durability_score": 0.85,
            "loop_closure_time_days": 4.2,
        }

    def execute_sensing_cycle(self, raw_signal: Dict[str, Any]) -> Dict[str, Any]:
        """Execute continuous sensing state machine flow."""
        self.system_state = SystemState.SENSING
        anomaly = AnomalySignal(
            signal_id=raw_signal.get("id", "sig_001"),
            description=raw_signal.get("description", "Market shift"),
            is_structural_shift=raw_signal.get("is_structural", True),
            observed_value=raw_signal.get("observed", 12.0),
            expected_value=raw_signal.get("expected", 2.0),
        )

        hyp = self.cognitive_loops.evaluate_signal(anomaly)
        if not hyp:
            self.system_state = SystemState.DISCARD
            return {"status": "DISCARD", "reason": "Noise signal"}

        self.system_state = SystemState.HYPOTHESIS

        # Decision tree evaluation
        opp_data = {
            "is_structural_anomaly": anomaly.is_structural_shift,
            "is_reversible_decision": hyp.risk_type == DecisionRiskType.TYPE_II_REVERSIBLE,
            "high_confidence_multi_source_signal": True,
            "cheap_test_available": True,
            "test_exceeds_kill_threshold": True,
            "has_or_can_build_structural_advantage": True,
        }
        go_decision, reason = self.decision_tree.evaluate(opp_data)

        if not go_decision:
            self.system_state = SystemState.DISCARD
            return {"status": "DISCARD", "reason": reason}

        self.system_state = SystemState.CHEAP_TEST
        belief = self.cognitive_loops.run_cheap_test(hyp.hypothesis_id, {"success": True, "likelihood_true": 0.85, "likelihood_false": 0.15})

        if belief >= 0.7:
            self.system_state = SystemState.VALIDATION
            self.system_state = SystemState.BUILD_GATE
            self.system_state = SystemState.MVP
            self.system_state = SystemState.GTM_TEST
            self.system_state = SystemState.SCALE
            self.system_state = SystemState.OPERATE

        return {
            "status": self.system_state.value,
            "hypothesis": hyp,
            "posterior_belief": belief,
            "master_loop_node": self.master_loop.state.current_node.value,
            "kpis": self.kpi_stack,
        }
