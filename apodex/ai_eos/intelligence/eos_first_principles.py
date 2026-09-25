"""Entrepreneurial Operating System (EOS) First-Principles Executable Engine.

An executable implementation of the 11-section EOS architecture:
A First-Principles Reconstruction of How Elite Founders Sense, Build, and Compound Enduring Companies.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import math
import logging
from typing import Any, Dict, List, Optional, Tuple, Set
from datetime import datetime, timezone

logger = logging.getLogger("apodex.ai_eos.eos_first_principles")


# =====================================================================
# 0 & 1. Master Loop & Multi-Timescale Feedback Loops
# =====================================================================
class LoopTimescale(str, Enum):
    FAST = "fast"       # days–weeks: product experiments, sales calls, ad tests, hiring interviews
    MEDIUM = "medium"   # months–quarters: GTM iteration, pricing changes, org design, capital deployment
    SLOW = "slow"       # years: strategic positioning, moat construction, market category creation, reinvention


@dataclass
class FeedbackLoop:
    loop_id: str
    name: str
    timescale: LoopTimescale
    cycle_time_days: float
    signal_fidelity: float  # [0, 1]
    is_compounding: bool = True
    iteration_count: int = 0

    def execute_cycle(self, feedback_quality: float) -> float:
        self.iteration_count += 1
        # Loop velocity and signal fidelity update
        self.signal_fidelity = max(0.0, min(1.0, 0.7 * self.signal_fidelity + 0.3 * feedback_quality))
        if self.signal_fidelity < 0.3:
            self.is_compounding = False
        return self.signal_fidelity


class MasterLoopNode(str, Enum):
    SENSING = "A_EnvironmentalSensing"
    SIGNAL_COLLECTION = "B_SignalCollection"
    PATTERN_RECOGNITION = "C_PatternRecognition"
    OPPORTUNITY_DISCOVERY = "D_OpportunityDiscovery"
    ROOT_CAUSE_ANALYSIS = "E_OpportunityEvaluation"
    VALIDATION = "F_CustomerMarketValidation"
    BUSINESS_MODEL = "G_BusinessModelDesign"
    MVP_EXPERIMENTATION = "H_MVPDesignExperimentation"
    PRODUCT_DEV = "I_ProductDevelopment"
    GTM_SYSTEM = "J_GoToMarketSystem"
    CUSTOMER_ACQUISITION = "K_CustomerAcquisition"
    RETENTION_ACTIVATION = "L_OnboardingActivationRetention"
    UNIT_ECONOMICS = "M_RevenueUnitEconomicsOptimization"
    ORG_SCALING = "N_OperationsOrgScaling"
    MOAT_CONSTRUCTION = "O_CompetitiveStrategyMoatConstruction"
    SCALING_EXPANSION = "P_ScalingExpansion"
    PLATFORM_FORMATION = "Q_PlatformEcosystemFormation"
    MARKET_LEADERSHIP = "R_MarketLeadership"
    REINVENTION = "S_ContinuousReinvention"


class MasterLoopOrchestrator:
    """Manages the re-entrant master loop and signal kill pathways."""

    def __init__(self) -> None:
        self.current_node: MasterLoopNode = MasterLoopNode.SENSING
        self.node_history: List[MasterLoopNode] = [MasterLoopNode.SENSING]
        self.kill_signals_triggered: List[Dict[str, Any]] = []

    def transition(self, next_node: MasterLoopNode, kill_signal: Optional[str] = None) -> MasterLoopNode:
        if kill_signal:
            self.kill_signals_triggered.append({
                "from_node": self.current_node,
                "kill_signal": kill_signal,
                "timestamp": datetime.now(timezone.utc)
            })
            # Re-entrant routing based on kill signals (§1)
            if kill_signal == "customer_validation_failed":
                next_node = MasterLoopNode.OPPORTUNITY_DISCOVERY
            elif kill_signal == "mvp_failed":
                next_node = MasterLoopNode.OPPORTUNITY_DISCOVERY
            elif kill_signal == "weak_gtm":
                next_node = MasterLoopNode.GTM_SYSTEM
            elif kill_signal == "bad_economics":
                next_node = MasterLoopNode.BUSINESS_MODEL

        self.current_node = next_node
        self.node_history.append(next_node)
        return self.current_node


# =====================================================================
# 2. Internal Cognitive Loops & Signal-to-Idea Pipeline
# =====================================================================
class RiskType(str, Enum):
    TYPE_I = "Type_I_Irreversible"   # One-way door: high scrutiny, slow deliberation
    TYPE_II = "Type_II_Reversible"   # Two-way door: fast, cheap execution


@dataclass
class Anomaly:
    anomaly_id: str
    description: str
    observed_value: float
    expected_value: float
    surprise_score: float  # Kullback-Leibler divergence / Bayesian surprise score
    is_structural_shift: bool


@dataclass
class FalsifiableHypothesis:
    hypothesis_id: str
    claim: str
    falsification_condition: str
    pre_committed_kill_threshold: float
    prior_belief: float  # [0, 1]
    posterior_belief: float  # [0, 1]
    risk_type: RiskType
    cheap_test_cost_usd: float
    is_active: bool = True
    is_falsified: bool = False


class CognitiveDecisionEngine:
    """Implements Kuhn paradigm shift anomaly detection and real options experimentation."""

    def __init__(self) -> None:
        self.anomalies: List[Anomaly] = []
        self.hypotheses: Dict[str, FalsifiableHypothesis] = {}

    def detect_anomaly(self, description: str, observed: float, expected: float, baseline_variance: float = 1.0) -> Anomaly:
        # Surprise score measured via normalized deviation
        diff = abs(observed - expected)
        surprise = diff / (baseline_variance + 1e-6)
        is_structural = surprise > 2.0  # > 2 sigma anomaly

        anomaly = Anomaly(
            anomaly_id=f"anom_{len(self.anomalies) + 1}",
            description=description,
            observed_value=observed,
            expected_value=expected,
            surprise_score=surprise,
            is_structural_shift=is_structural
        )
        self.anomalies.append(anomaly)
        return anomaly

    def form_hypothesis(
        self,
        claim: str,
        falsification_condition: str,
        kill_threshold: float,
        prior_belief: float,
        risk_type: RiskType,
        cheap_test_cost_usd: float
    ) -> FalsifiableHypothesis:
        hyp_id = f"hyp_{len(self.hypotheses) + 1}"
        hyp = FalsifiableHypothesis(
            hypothesis_id=hyp_id,
            claim=claim,
            falsification_condition=falsification_condition,
            pre_committed_kill_threshold=kill_threshold,
            prior_belief=prior_belief,
            posterior_belief=prior_belief,
            risk_type=risk_type,
            cheap_test_cost_usd=cheap_test_cost_usd
        )
        self.hypotheses[hyp_id] = hyp
        return hyp

    def update_belief_with_test_result(self, hypothesis_id: str, observed_metric: float) -> FalsifiableHypothesis:
        hyp = self.hypotheses[hypothesis_id]
        if observed_metric < hyp.pre_committed_kill_threshold:
            hyp.is_falsified = True
            hyp.is_active = False
            hyp.posterior_belief = 0.0
        else:
            # Bayesian update using likelihood scaling
            likelihood = min(1.0, observed_metric / (hyp.pre_committed_kill_threshold + 1e-6))
            num = likelihood * hyp.prior_belief
            den = num + (1.0 - likelihood) * (1.0 - hyp.prior_belief) + 1e-6
            hyp.posterior_belief = min(1.0, max(0.0, num / den))
        return hyp


@dataclass
class MentalModel:
    model_name: str
    structure_version: int
    parameters: Dict[str, float]
    falsification_history: List[str] = field(default_factory=list)
    is_ossified: bool = False

    def update_parameters(self, updates: Dict[str, float]) -> None:
        """Fast parameter tuning."""
        self.parameters.update(updates)

    def update_structure(self, new_version: int, structural_reason: str) -> None:
        """Rare, costly paradigm shift update."""
        self.structure_version = new_version
        self.falsification_history.append(structural_reason)
        self.is_ossified = False

    def check_ossification(self, consecutive_contradictions: int) -> bool:
        if consecutive_contradictions >= 3:
            self.is_ossified = True
        return self.is_ossified


# =====================================================================
# 3. External Business Loops Engine
# =====================================================================
class BusinessLoopType(str, Enum):
    PRODUCT = "Product"
    MARKETING = "Marketing"
    SALES = "Sales"
    CUSTOMER_SUCCESS = "CustomerSuccess"
    BRAND = "Brand"
    PRICING = "Pricing"
    REFERRAL = "Referral"
    DATA = "Data"
    FINANCIAL = "Financial"
    HIRING = "Hiring"
    CULTURE = "Culture"
    INNOVATION = "Innovation"
    COMPETITIVE_INTELLIGENCE = "CompetitiveIntelligence"


@dataclass
class ExternalBusinessLoopSpec:
    loop_type: BusinessLoopType
    inputs: List[str]
    outputs: List[str]
    feedback_signal: str
    core_kpis: List[str]
    dominant_failure_mode: str
    current_kpi_values: Dict[str, float] = field(default_factory=dict)


class ExternalBusinessLoopsEngine:
    """Manages 13 coupled business loops and stock-and-flow dynamics."""

    def __init__(self) -> None:
        self.loops: Dict[BusinessLoopType, ExternalBusinessLoopSpec] = self._initialize_specs()
        self.stocks: Dict[str, float] = {
            "cash_usd": 1_000_000.0,
            "talent_count": 10.0,
            "brand_trust": 0.5,
            "data_assets": 100.0,
            "active_customers": 500.0
        }

    def _initialize_specs(self) -> Dict[BusinessLoopType, ExternalBusinessLoopSpec]:
        return {
            BusinessLoopType.PRODUCT: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.PRODUCT,
                inputs=["User behavior", "Support tickets", "Usage data"],
                outputs=["Feature changes", "Roadmap"],
                feedback_signal="Activation/retention deltas",
                core_kpis=["Retention curve", "NPS", "Feature adoption"],
                dominant_failure_mode="Building for loudest customer instead of representative one"
            ),
            BusinessLoopType.MARKETING: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.MARKETING,
                inputs=["Positioning", "Market data"],
                outputs=["Awareness", "Demand"],
                feedback_signal="CAC, traffic quality, message resonance",
                core_kpis=["CAC", "Brand recall", "Conversion rate"],
                dominant_failure_mode="Message-market mismatch; scaling spend before message works"
            ),
            BusinessLoopType.SALES: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.SALES,
                inputs=["Qualified leads", "Product"],
                outputs=["Closed revenue", "Customer feedback"],
                feedback_signal="Win/loss reasons",
                core_kpis=["Win rate", "Sales cycle length", "ACV"],
                dominant_failure_mode="Selling to non-ICP to hit quota"
            ),
            BusinessLoopType.CUSTOMER_SUCCESS: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.CUSTOMER_SUCCESS,
                inputs=["Onboarding data", "Usage"],
                outputs=["Retention", "Expansion"],
                feedback_signal="Churn reasons, health scores",
                core_kpis=["NRR", "Churn rate", "Time-to-value"],
                dominant_failure_mode="Success != support; reactive-only CS"
            ),
            BusinessLoopType.BRAND: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.BRAND,
                inputs=["Product experience", "Comms"],
                outputs=["Trust", "Pricing power"],
                feedback_signal="Sentiment, unaided recall",
                core_kpis=["Share of voice", "Price elasticity"],
                dominant_failure_mode="Brand as decoration, not strategy"
            ),
            BusinessLoopType.PRICING: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.PRICING,
                inputs=["Value delivered", "WTP data"],
                outputs=["Revenue", "Positioning signal"],
                feedback_signal="Conversion by price point, expansion rate",
                core_kpis=["ARPU", "Price realization", "Elasticity"],
                dominant_failure_mode="Cost-plus pricing instead of value-based"
            ),
            BusinessLoopType.REFERRAL: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.REFERRAL,
                inputs=["Customer satisfaction", "Incentive design"],
                outputs=["New customer flow"],
                feedback_signal="Referral rate, K-factor",
                core_kpis=["Viral coefficient", "Referral CAC"],
                dominant_failure_mode="Incentivizing referral volume over referral quality"
            ),
            BusinessLoopType.DATA: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.DATA,
                inputs=["All loop outputs"],
                outputs=["Decisions"],
                feedback_signal="Model accuracy vs outcomes",
                core_kpis=["Data latency", "Decision cycle time"],
                dominant_failure_mode="Vanity metrics; dashboards no one acts on"
            ),
            BusinessLoopType.FINANCIAL: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.FINANCIAL,
                inputs=["Revenue", "Costs", "Capital"],
                outputs=["Runway", "Reinvestment capacity"],
                feedback_signal="Burn multiple, margin trend",
                core_kpis=["Gross margin", "Burn multiple", "Runway"],
                dominant_failure_mode="Growth at negative unit economics with no path to positive"
            ),
            BusinessLoopType.HIRING: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.HIRING,
                inputs=["Org needs", "Culture"],
                outputs=["Capability", "Capacity"],
                feedback_signal="90-day performance, regretted attrition",
                core_kpis=["Time-to-fill", "Quality of hire", "Retention"],
                dominant_failure_mode="Hiring for pedigree over role-fit; hiring ahead of proven need"
            ),
            BusinessLoopType.CULTURE: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.CULTURE,
                inputs=["Values-in-action", "Incentives"],
                outputs=["Behavior consistency at scale"],
                feedback_signal="Employee sentiment, decision speed",
                core_kpis=["eNPS", "Decision latency"],
                dominant_failure_mode="Values-as-poster (stated but not incentivized)"
            ),
            BusinessLoopType.INNOVATION: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.INNOVATION,
                inputs=["R&D", "Market signals", "Internal ideas"],
                outputs=["New products/features/lines"],
                feedback_signal="Time-to-market, cannibalization rate",
                core_kpis=["# experiments run", "Hit rate", "Time-to-signal"],
                dominant_failure_mode="Innovation theater — activity without shipped bets"
            ),
            BusinessLoopType.COMPETITIVE_INTELLIGENCE: ExternalBusinessLoopSpec(
                loop_type=BusinessLoopType.COMPETITIVE_INTELLIGENCE,
                inputs=["Market/competitor data"],
                outputs=["Strategic repositioning"],
                feedback_signal="Win/loss vs named competitors",
                core_kpis=["Relative share trend", "Feature parity gap"],
                dominant_failure_mode="Reacting to competitors instead of running own strategy"
            )
        }

    def simulate_coupled_step(self, arpu_usd: float, monthly_burn_usd: float, new_hires: int) -> Dict[str, float]:
        """Demonstrates coupling between Pricing, Financial, and Hiring loops."""
        # ARPU feeds Financial stock
        revenue_gain = self.stocks["active_customers"] * arpu_usd
        self.stocks["cash_usd"] += revenue_gain - monthly_burn_usd

        # Cash stock determines Hiring loop capacity
        if self.stocks["cash_usd"] > 100_000.0 and new_hires > 0:
            self.stocks["talent_count"] += new_hires

        return self.stocks.copy()


# =====================================================================
# 4. Customer Journey Full Lifecycle Engine
# =====================================================================
class LifecycleStage(str, Enum):
    AWARENESS = "1_Awareness"
    INTEREST = "2_Interest"
    CONSIDERATION = "3_Consideration"
    EVALUATION = "4_Evaluation"
    PURCHASE = "5_Purchase"
    ONBOARDING = "6_Onboarding"
    ACTIVATION = "7_Activation"
    ENGAGEMENT = "8_Engagement"
    HABIT_FORMATION = "9_HabitFormation"
    RETENTION = "10_Retention"
    LOYALTY = "11_Loyalty"
    ADVOCACY = "12_Advocacy"
    REFERRAL = "13_Referral"
    EXPANSION = "14_Expansion"
    REPURCHASE = "15_Repurchase"


@dataclass
class LifecycleStageMetrics:
    stage: LifecycleStage
    founder_objective: str
    customer_psychology: str
    key_metric: str
    conversion_rate: float
    common_mistake: str
    optimization_lever: str


class CustomerLifecycleEngine:
    """Tracks cohort progression across all 15 customer lifecycle stages."""

    def __init__(self) -> None:
        self.stages: List[LifecycleStage] = list(LifecycleStage)

    def analyze_cohort_conversion(self, initial_cohort_size: int, stage_conversions: Dict[LifecycleStage, float]) -> Dict[str, Any]:
        """Evaluates customer counts across all 15 stages and detects primary dropoff bottleneck."""
        counts = {}
        current_count = float(initial_cohort_size)
        bottleneck_stage = None
        max_dropoff = 0.0

        for stage in self.stages:
            rate = stage_conversions.get(stage, 1.0)
            dropoff = (1.0 - rate)
            if dropoff > max_dropoff:
                max_dropoff = dropoff
                bottleneck_stage = stage

            current_count *= rate
            counts[stage.value] = int(current_count)

        return {
            "stage_counts": counts,
            "final_retaining_customers": counts.get(LifecycleStage.REPURCHASE.value, 0),
            "primary_bottleneck_stage": bottleneck_stage.value if bottleneck_stage else None,
            "max_dropoff_rate": max_dropoff
        }


# =====================================================================
# 5. Go-to-Market (GTM) System Engine
# =====================================================================
class GTMMotion(str, Enum):
    PLG = "Product-Led Growth"
    SLG = "Sales-Led Growth"
    CLG = "Community-Led Growth"
    CONTENT = "Content-Led Growth"
    ENTERPRISE = "Enterprise Sales"


class GTMSystemEngine:
    """Integrates positioning, pricing, segmentation, and motion selection logic."""

    def evaluate_gtm_fit(self, complexity: str, price_point_annual_usd: float, network_effects: bool) -> Dict[str, Any]:
        """Determines channel and motion alignment based on buyer behavior (§5)."""
        recommended_motions = []

        if complexity == "low" and price_point_annual_usd < 5_000.0:
            recommended_motions.extend([GTMMotion.PLG, GTMMotion.CONTENT])
        elif complexity == "high" and price_point_annual_usd >= 50_000.0:
            recommended_motions.extend([GTMMotion.SLG, GTMMotion.ENTERPRISE])

        if network_effects:
            recommended_motions.append(GTMMotion.CLG)

        return {
            "complexity": complexity,
            "annual_price_usd": price_point_annual_usd,
            "recommended_motions": [m.value for m in recommended_motions],
            "compounding_strategy": "Land via PLG, expand via SLG" if (GTMMotion.PLG in recommended_motions and GTMMotion.SLG in recommended_motions) else "Direct Motion"
        }


# =====================================================================
# 6. Company Growth System State Machine
# =====================================================================
class CompanyStage(str, Enum):
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
class StageSpec:
    stage: CompanyStage
    primary_objective: str
    org_change: str
    decision_making_change: str
    capital_allocation: str
    key_risk: str
    core_metric: str
    binding_constraint: str


class CompanyGrowthStateMachine:
    """Manages venture evolution across 9 growth stages and checks for premature scaling."""

    def __init__(self) -> None:
        self.current_stage: CompanyStage = CompanyStage.IDEA

    def check_premature_scaling(self, retention_curve_flattens: bool, cac_payback_months: float, stage: CompanyStage) -> Tuple[bool, str]:
        """Detects premature scaling (e.g. scaling before PMF retention flattens or CAC payback breaks)."""
        if stage in [CompanyStage.GROWTH, CompanyStage.SCALE] and not retention_curve_flattens:
            return True, "PREMATURE SCALING WARNING: Attempting to scale before retention curve flattens!"
        if stage == CompanyStage.GROWTH and cac_payback_months > 18.0:
            return True, f"PREMATURE SCALING WARNING: Scaling broken funnel with CAC payback of {cac_payback_months} months."
        return False, "Unit economics and retention support stage transition."

    def transition_stage(self, target_stage: CompanyStage, retention_flattens: bool, cac_payback: float) -> CompanyStage:
        is_premature, msg = self.check_premature_scaling(retention_flattens, cac_payback, target_stage)
        if is_premature:
            logger.warning(msg)
            return self.current_stage
        self.current_stage = target_stage
        return self.current_stage


# =====================================================================
# 7. Strategic Thinking & Capital Allocation Engine
# =====================================================================
class MoatType(str, Enum):
    NETWORK_EFFECTS = "Network Effects"
    SWITCHING_COSTS = "Switching Costs"
    ECONOMIES_OF_SCALE = "Economies of Scale"
    BRAND = "Brand"
    REGULATORY_IP = "Regulatory/IP"
    COUNTER_POSITIONING = "Counter-Positioning"


@dataclass
class StrategicInitiative:
    initiative_id: str
    name: str
    expected_return_usd: float
    required_capital_usd: float
    confidence_score: float  # [0, 1]

    @property
    def expected_roi_ratio(self) -> float:
        if self.required_capital_usd <= 0:
            return 0.0
        return (self.expected_return_usd * self.confidence_score) / self.required_capital_usd


class StrategicCapitalAllocator:
    """Ranks initiatives on Mauboussin common expected-return basis with opportunity cost discipline."""

    def rank_initiatives(self, initiatives: List[StrategicInitiative], budget_usd: float) -> Dict[str, Any]:
        ranked = sorted(initiatives, key=lambda i: i.expected_roi_ratio, reverse=True)
        funded = []
        remaining_budget = budget_usd

        for init in ranked:
            if init.required_capital_usd <= remaining_budget:
                funded.append(init)
                remaining_budget -= init.required_capital_usd

        return {
            "funded_initiatives": [f.name for f in funded],
            "unfunded_initiatives": [i.name for i in ranked if i not in funded],
            "capital_allocated_usd": budget_usd - remaining_budget,
            "remaining_capital_usd": remaining_budget
        }


# =====================================================================
# 8. Failure Mode Monitor
# =====================================================================
@dataclass
class FailureModePattern:
    name: str
    root_cause: str
    detection_signal: str
    correction_mechanism: str


class FailureModeMonitor:
    """Monitors venture health against all 10 failure modes (§8)."""

    def __init__(self) -> None:
        self.patterns: List[FailureModePattern] = [
            FailureModePattern("Solving the wrong problem", "Skipped root-cause analysis; solved a symptom", "Low engagement despite positive survey feedback", "Return to root-cause 5-Whys / JTBD interviews"),
            FailureModePattern("Building before validating", "Founder conviction substituted for evidence", "High build velocity, flat demand signal", "Enforce a validation gate before build resourcing"),
            FailureModePattern("Weak positioning", "No clear 'instead of X, use us because Y'", "High CAC, long sales cycles", "Rebuild positioning around real alternative"),
            FailureModePattern("Poor pricing", "Cost-plus instead of value-based pricing", "High conversion at low price, poor margin", "Re-anchor price to quantified customer value"),
            FailureModePattern("Distribution failure", "Great product, no repeatable channel", "High NPS, flat growth", "Systematically test channels against ICP behavior"),
            FailureModePattern("Lack of product-market fit", "Premature scaling of an unproven loop", "Retention curve never flattens", "Stop scaling; return to cohort-level retention work"),
            FailureModePattern("Organizational bottlenecks", "Decision rights not delegated", "Rising decision latency", "Push decision rights down with clear frameworks"),
            FailureModePattern("Founder bias", "Overconfidence, confirmation bias, sunk cost", "Ignoring disconfirming data", "Pre-committed kill criteria set before launch"),
            FailureModePattern("Scaling prematurely", "Confusing early demand spike with durable PMF", "CAC rising faster than LTV", "Re-test unit economics at each order-of-magnitude"),
            FailureModePattern("Capital misallocation", "No opportunity-cost discipline in budgeting", "Multiple underperforming bets funded", "Rank all initiatives on common expected-return basis")
        ]

    def audit_metrics(
        self,
        retention_flattens: bool,
        cac_to_ltv_ratio: float,
        decision_latency_days: float,
        build_vs_demand_ratio: float
    ) -> List[Dict[str, str]]:
        alerts = []
        if not retention_flattens:
            p = self.patterns[5]
            alerts.append({"failure_mode": p.name, "signal": p.detection_signal, "correction": p.correction_mechanism})
        if cac_to_ltv_ratio > 0.5:
            p = self.patterns[8]
            alerts.append({"failure_mode": p.name, "signal": p.detection_signal, "correction": p.correction_mechanism})
        if decision_latency_days > 14.0:
            p = self.patterns[6]
            alerts.append({"failure_mode": p.name, "signal": p.detection_signal, "correction": p.correction_mechanism})
        if build_vs_demand_ratio > 3.0:
            p = self.patterns[1]
            alerts.append({"failure_mode": p.name, "signal": p.detection_signal, "correction": p.correction_mechanism})

        return alerts


# =====================================================================
# 10. AI System State Machine & Decision Tree
# =====================================================================
class AISystemState(str, Enum):
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


class EOSOpportunityDecisionTree:
    """Executes the 10.2 Decision Tree: 'Should We Pursue This Opportunity?'"""

    def evaluate(
        self,
        is_structural_anomaly: bool,
        is_reversible_decision: bool,
        high_confidence_multi_source_signal: bool,
        cheap_test_available: bool,
        test_result_exceeds_kill_threshold: bool,
        expected_value_positive: bool,
        structural_advantage_possible: bool
    ) -> Dict[str, Any]:
        """Evaluates logical flow Q1 through Q5."""
        if not is_structural_anomaly:
            return {"pursue": False, "reason": "Discarded at Q1: Noise, not structural anomaly"}

        if not is_reversible_decision:
            if not high_confidence_multi_source_signal:
                return {"pursue": False, "reason": "Discarded at Q2a: High stakes decision without multi-source high-confidence signal"}

        if cheap_test_available:
            if not test_result_exceeds_kill_threshold:
                return {"pursue": False, "reason": "Discarded at Q4: Test result failed pre-committed kill threshold"}
        else:
            if not expected_value_positive:
                return {"pursue": False, "reason": "Discarded at Q4b: Expected value not clearly positive"}

        if not structural_advantage_possible:
            return {"pursue": False, "reason": "Discarded at Q5: No structural competitive advantage"}

        return {"pursue": True, "reason": "Commit resources: Passed all decision tree filters"}


class EntrepreneurialOperatingSystemFirstPrinciples:
    """Unified Orchestrator implementing the full 11-section EOS architecture."""

    def __init__(self) -> None:
        self.master_loop = MasterLoopOrchestrator()
        self.cognitive_engine = CognitiveDecisionEngine()
        self.business_loops_engine = ExternalBusinessLoopsEngine()
        self.lifecycle_engine = CustomerLifecycleEngine()
        self.gtm_engine = GTMSystemEngine()
        self.growth_state_machine = CompanyGrowthStateMachine()
        self.capital_allocator = StrategicCapitalAllocator()
        self.failure_monitor = FailureModeMonitor()
        self.decision_tree = EOSOpportunityDecisionTree()
        self.current_ai_state: AISystemState = AISystemState.SENSING

    def process_opportunity(
        self,
        description: str,
        observed_metric: float,
        expected_metric: float,
        cheap_test_cost_usd: float,
        test_result: float,
        kill_threshold: float,
        structural_advantage: bool
    ) -> Dict[str, Any]:
        # 1. Sensing & Anomaly Detection
        anomaly = self.cognitive_engine.detect_anomaly(description, observed_metric, expected_metric)
        self.current_ai_state = AISystemState.HYPOTHESIS

        # 2. Decision Tree Evaluation
        decision = self.decision_tree.evaluate(
            is_structural_anomaly=anomaly.is_structural_shift,
            is_reversible_decision=True,
            high_confidence_multi_source_signal=True,
            cheap_test_available=True,
            test_result_exceeds_kill_threshold=(test_result >= kill_threshold),
            expected_value_positive=True,
            structural_advantage_possible=structural_advantage
        )

        if not decision["pursue"]:
            self.current_ai_state = AISystemState.DISCARD
            return {
                "ai_state": self.current_ai_state.value,
                "anomaly": anomaly,
                "decision": decision
            }

        self.current_ai_state = AISystemState.SCALE
        return {
            "ai_state": self.current_ai_state.value,
            "anomaly": anomaly,
            "decision": decision
        }
