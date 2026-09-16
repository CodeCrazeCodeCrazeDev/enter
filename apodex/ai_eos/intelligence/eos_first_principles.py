"""Entrepreneurial Operating System (EOS) - First-Principles Engine.

Executable implementation of the 11-section EOS architecture detailing how elite founders
sense, build, and compound enduring companies.
"""

from __future__ import annotations

import math
import logging
from typing import Dict, Any, List, Optional, Tuple, Set
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger("sero.eos_first_principles")


# =====================================================================
# Section 1. Master Loop Engine
# =====================================================================

class MasterNode(str, Enum):
    ENVIRONMENTAL_SENSING = "A"
    SIGNAL_COLLECTION = "B"
    PATTERN_RECOGNITION = "C"
    OPPORTUNITY_DISCOVERY = "D"
    ROOT_CAUSE_ANALYSIS = "E"
    CUSTOMER_VALIDATION = "F"
    BUSINESS_MODEL_DESIGN = "G"
    MVP_EXPERIMENTATION = "H"
    PRODUCT_DEVELOPMENT = "I"
    GTM_SYSTEM = "J"
    CUSTOMER_ACQUISITION = "K"
    ONBOARDING_RETENTION = "L"
    REVENUE_OPTIMIZATION = "M"
    OPERATIONS_SCALING = "N"
    MOAT_CONSTRUCTION = "O"
    SCALING_EXPANSION = "P"
    PLATFORM_ECOSYSTEM = "Q"
    MARKET_LEADERSHIP = "R"
    CONTINUOUS_REINVENTION = "S"


class MasterLoopEngine(BaseModel):
    """Top-level re-entrant master loop with kill signals and reinvention processes."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    current_node: MasterNode = MasterNode.ENVIRONMENTAL_SENSING
    loop_velocity_days: float = 14.0
    signal_fidelity_score: float = 0.85
    execution_history: List[Dict[str, Any]] = Field(default_factory=list)

    def transition(self, target_node: MasterNode, reason: str, kill_signal: bool = False) -> MasterNode:
        record = {
            "from_node": self.current_node.value,
            "to_node": target_node.value,
            "reason": reason,
            "kill_signal": kill_signal,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.execution_history.append(record)
        self.current_node = target_node
        logger.info(f"MasterLoop transition: {record['from_node']} -> {target_node.value} ({reason})")
        return self.current_node

    def evaluate_kill_signals(
        self,
        validation_passed: bool,
        mvp_passed: bool,
        gtm_viable: bool,
        economics_viable: bool
    ) -> Optional[MasterNode]:
        """Processes re-entrant kill and feedback loops from §1 diagram."""
        if not validation_passed:
            # F -. kill signal .-> D
            return self.transition(MasterNode.OPPORTUNITY_DISCOVERY, "Validation kill signal triggered", kill_signal=True)
        if not mvp_passed:
            # H -. kill signal .-> D
            return self.transition(MasterNode.OPPORTUNITY_DISCOVERY, "MVP experiment kill signal triggered", kill_signal=True)
        if not gtm_viable:
            # K -. weak GTM .-> J
            return self.transition(MasterNode.GTM_SYSTEM, "Weak GTM feedback loop triggered")
        if not economics_viable:
            # M -. bad economics .-> G
            return self.transition(MasterNode.BUSINESS_MODEL_DESIGN, "Bad economics feedback loop triggered")
        return None


# =====================================================================
# Section 2. Internal Cognitive Loops
# =====================================================================

class DecisionRiskType(str, Enum):
    TYPE_I = "irreversible_one_way_door"
    TYPE_II = "reversible_two_way_door"


class HypothesisClaim(BaseModel):
    claim_id: UUID = Field(default_factory=uuid4)
    statement: str
    falsifiable_criteria: str
    is_falsified: bool = False
    prior_belief: float = 0.5
    posterior_belief: float = 0.5
    test_cost_cents: int = 100_00
    risk_type: DecisionRiskType = DecisionRiskType.TYPE_II


class SignalToIdeaPipeline(BaseModel):
    """Processes weak signals into falsifiable hypotheses and runs cheap tests."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    anomalies_detected: List[Dict[str, Any]] = Field(default_factory=list)
    hypotheses: List[HypothesisClaim] = Field(default_factory=list)

    def detect_anomaly(self, signal_name: str, observed_value: float, expected_value: float, threshold: float = 0.2) -> bool:
        """Detects Kuhn/Bayesian surprise anomaly where observed deviates from mental model expected."""
        deviation = abs(observed_value - expected_value) / max(1e-6, abs(expected_value))
        is_anomaly = deviation >= threshold
        if is_anomaly:
            self.anomalies_detected.append({
                "signal": signal_name,
                "observed": observed_value,
                "expected": expected_value,
                "deviation": deviation,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        return is_anomaly

    def form_forced_hypothesis(
        self,
        statement: str,
        falsifiable_criteria: str,
        prior_belief: float = 0.5,
        risk_type: DecisionRiskType = DecisionRiskType.TYPE_II,
        test_cost_cents: int = 100_00
    ) -> HypothesisClaim:
        hyp = HypothesisClaim(
            statement=statement,
            falsifiable_criteria=falsifiable_criteria,
            prior_belief=prior_belief,
            posterior_belief=prior_belief,
            risk_type=risk_type,
            test_cost_cents=test_cost_cents
        )
        self.hypotheses.append(hyp)
        return hyp

    def run_cheap_test(self, hyp: HypothesisClaim, test_result_success: bool, likelihood_ratio: float = 2.5) -> float:
        """Sequential Bayesian update after cheap experiment execution."""
        prior = hyp.prior_belief
        if test_result_success:
            # Posterior = (Prior * LR) / (Prior * LR + (1 - Prior))
            posterior = (prior * likelihood_ratio) / (prior * likelihood_ratio + (1.0 - prior))
        else:
            posterior = (prior / likelihood_ratio) / ((prior / likelihood_ratio) + (1.0 - prior))

        hyp.posterior_belief = posterior
        if posterior < 0.15:
            hyp.is_falsified = True
        return posterior

    def filter_opportunity_cost(
        self,
        is_compounding: bool,
        has_structural_advantage: bool,
        tam_5_to_10_yr_cents: int,
        min_tam_cents: int = 50_000_000_00
    ) -> bool:
        """Filter governing what NOT to pursue based on compounding, moat, and TAM."""
        return is_compounding and has_structural_advantage and (tam_5_to_10_yr_cents >= min_tam_cents)


class MentalModelEngine(BaseModel):
    """Manages living mental models and detects model ossification."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    parameters: Dict[str, float] = Field(default_factory=dict)
    structural_assumptions: List[str] = Field(default_factory=list)
    contradiction_count: int = 0
    is_ossified: bool = False

    def update_parameters(self, updates: Dict[str, float]) -> None:
        self.parameters.update(updates)

    def record_market_contradiction(self, description: str) -> bool:
        self.contradiction_count += 1
        # Model ossification occurs when structural model is not updated despite repeated contradictions
        if self.contradiction_count >= 5:
            self.is_ossified = True
        return self.is_ossified

    def execute_paradigm_shift(self, new_structural_assumptions: List[str]) -> None:
        """Costly structural update resetting model parameters and resolving ossification."""
        self.structural_assumptions = new_structural_assumptions
        self.contradiction_count = 0
        self.is_ossified = False
        logger.info("PARADIGM SHIFT: Structural mental model reset successfully.")


# =====================================================================
# Section 3. External Business Loops
# =====================================================================

class BusinessLoopName(str, Enum):
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


class BusinessLoopSpec(BaseModel):
    name: BusinessLoopName
    inputs: List[str]
    outputs: List[str]
    feedback_signal: str
    core_kpis: List[str]
    failure_mode: str
    health_score: float = 1.0


class CoupledBusinessLoopsEngine(BaseModel):
    """Executes and models the 12 coupled external business loops and stock-and-flow dynamics."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    loops: Dict[BusinessLoopName, BusinessLoopSpec] = Field(default_factory=dict)
    stocks: Dict[str, float] = Field(default_factory=lambda: {
        "cash_cents": 1000000_00,
        "talent_headcount": 10.0,
        "brand_trust": 0.8,
        "data_assets": 0.7
    })

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if not self.loops:
            self._init_default_loops()

    def _init_default_loops(self) -> None:
        specs = [
            (BusinessLoopName.PRODUCT, ["User behavior", "Support tickets"], ["Feature changes"], "Activation deltas", ["Retention", "NPS"], "Building for loudest customer"),
            (BusinessLoopName.MARKETING, ["Positioning", "Market data"], ["Awareness", "Demand"], "CAC resonance", ["CAC", "Conversion"], "Message-market mismatch"),
            (BusinessLoopName.SALES, ["Qualified leads"], ["Closed revenue"], "Win/loss reasons", ["Win rate", "ACV"], "Selling to non-ICP"),
            (BusinessLoopName.CUSTOMER_SUCCESS, ["Onboarding data"], ["Retention", "Expansion"], "Churn reasons", ["NRR", "Time-to-value"], "Reactive support only"),
            (BusinessLoopName.BRAND, ["Product experience"], ["Trust", "Pricing power"], "Sentiment", ["Share of voice"], "Brand as decoration"),
            (BusinessLoopName.PRICING, ["Value delivered"], ["Revenue signal"], "Conversion by price", ["ARPU", "Realization"], "Cost-plus pricing"),
            (BusinessLoopName.REFERRAL, ["Customer satisfaction"], ["New flow"], "K-factor", ["Viral coefficient"], "Volume over quality"),
            (BusinessLoopName.DATA, ["Usage metrics"], ["Decisions"], "Model accuracy", ["Decision cycle time"], "Vanity metrics"),
            (BusinessLoopName.FINANCIAL, ["Revenue", "Capital"], ["Runway"], "Burn trend", ["Gross margin", "Burn multiple"], "Growth at negative unit economics"),
            (BusinessLoopName.HIRING, ["Org needs"], ["Capability"], "90-day performance", ["Time-to-fill"], "Pedigree over fit"),
            (BusinessLoopName.CULTURE, ["Values-in-action"], ["Consistency"], "Employee sentiment", ["eNPS"], "Values as poster"),
            (BusinessLoopName.INNOVATION, ["R&D", "Ideas"], ["New products"], "Time-to-market", ["Hit rate"], "Innovation theater"),
            (BusinessLoopName.COMPETITIVE_INTELLIGENCE, ["Market data"], ["Repositioning"], "Win/loss vs comps", ["Share trend"], "Reacting vs strategy"),
        ]
        for name, inp, out, sig, kpis, fail in specs:
            self.loops[name] = BusinessLoopSpec(
                name=name, inputs=inp, outputs=out, feedback_signal=sig, core_kpis=kpis, failure_mode=fail
            )

    def simulate_loop_coupling(self, arpu_cents: int, churn_rate: float, burn_multiple: float) -> Dict[str, float]:
        """Coupled simulation where pricing loop output (ARPU) feeds financial & hiring stocks."""
        # 1. Financial stock update from ARPU & burn
        mrr_cents = arpu_cents * 100
        net_flow_cents = mrr_cents - (mrr_cents * burn_multiple)
        self.stocks["cash_cents"] += net_flow_cents

        # 2. Hiring capacity update from cash stock
        if self.stocks["cash_cents"] > 500000_00:
            self.stocks["talent_headcount"] += 0.5
        elif self.stocks["cash_cents"] < 100000_00:
            self.stocks["talent_headcount"] = max(1.0, self.stocks["talent_headcount"] - 0.5)

        # 3. Product loop health update from churn rate
        product_health = max(0.0, 1.0 - (churn_rate * 5.0))
        self.loops[BusinessLoopName.PRODUCT].health_score = product_health

        return self.stocks


# =====================================================================
# Section 4. Customer Journey Engine
# =====================================================================

class CustomerStageName(str, Enum):
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


class CustomerStageSpec(BaseModel):
    stage: CustomerStageName
    founder_objective: str
    customer_psychology: str
    key_metric: str
    common_mistake: str
    optimization_lever: str
    conversion_rate: float = 0.5


class CustomerLifecycleEngine(BaseModel):
    """Models the complete 15-stage customer journey lifecycle."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    stages: Dict[CustomerStageName, CustomerStageSpec] = Field(default_factory=dict)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if not self.stages:
            self._init_stages()

    def _init_stages(self) -> None:
        journey_data = [
            (CustomerStageName.AWARENESS, "Enter consideration set", "Pattern-matching", "Reach", "Generic messaging", "Sharp framing"),
            (CustomerStageName.INTEREST, "Earn attention", "Curiosity vs skepticism", "CTR", "Feature dumping", "Lead with pain"),
            (CustomerStageName.CONSIDERATION, "Differentiate", "Comparing status quo", "Time-on-site", "Competing on shared features", "Reframe comparison"),
            (CustomerStageName.EVALUATION, "Reduce perceived risk", "Loss aversion dominates", "Trial starts", "Ignoring risk reduction", "Make failure cheap"),
            (CustomerStageName.PURCHASE, "Convert intent", "Decision fatigue", "Conversion rate", "Checkout friction", "Remove friction steps"),
            (CustomerStageName.ONBOARDING, "Deliver value fast", "Anxiety on wasted choice", "Time-to-first-value", "Feature tour", "Job-to-be-done onboarding"),
            (CustomerStageName.ACTIVATION, "Cross aha threshold", "Forming initial habit", "Activation rate", "Defining as login", "Cohort aha moment"),
            (CustomerStageName.ENGAGEMENT, "Build usage depth", "Reinforcement learning", "DAU/MAU", "Uncorrelated engagement", "Optimize retention behavior"),
            (CustomerStageName.HABIT_FORMATION, "Automatic usage", "Cue-routine-reward", "Habit frequency", "No trigger cadence", "Reliable triggers"),
            (CustomerStageName.RETENTION, "Prevent churn", "Switching cost perception", "Retention curve", "Aggregate-only retention", "Cohort flattening analysis"),
            (CustomerStageName.LOYALTY, "Deepen lock-in", "Identity alignment", "Repeat rate", "Assuming satisfaction = loyalty", "Genuine switching costs"),
            (CustomerStageName.ADVOCACY, "Convert satisfaction to voice", "Social proof", "NPS", "Asking before value proven", "Ask at peak value"),
            (CustomerStageName.REFERRAL, "Convert advocacy to acquisition", "Peer trust transfer", "K-factor", "Generic incentives", "Aligned value incentives"),
            (CustomerStageName.EXPANSION, "Grow account value", "Anchoring spend", "NRR", "Underselling adjacent value", "Usage expansion triggers"),
            (CustomerStageName.REPURCHASE, "Sustain LTV", "Habitual trust", "LTV", "Treating as passive", "Proactive lifecycle marketing")
        ]
        for stg, obj, psych, met, err, lev in journey_data:
            self.stages[stg] = CustomerStageSpec(
                stage=stg, founder_objective=obj, customer_psychology=psych, key_metric=met, common_mistake=err, optimization_lever=lev
            )

    def compute_funnel_throughput(self, initial_cohort_size: int = 10000) -> Dict[str, Any]:
        """Calculates cohort decay across all 15 customer journey stages."""
        current_count = initial_cohort_size
        funnel = {}
        for stage_name, spec in self.stages.items():
            current_count = int(current_count * spec.conversion_rate)
            funnel[stage_name.value] = current_count
        return {
            "initial_cohort": initial_cohort_size,
            "stage_counts": funnel,
            "overall_conversion": funnel[CustomerStageName.REPURCHASE.value] / max(1, initial_cohort_size)
        }


# =====================================================================
# Section 5. Go-to-Market System Engine
# =====================================================================

class MotionType(str, Enum):
    PLG = "product_led_growth"
    SLG = "sales_led_growth"
    CLG = "community_led_growth"


class GTMSystemEngine(BaseModel):
    """Integrated GTM System linking positioning, pricing, segmentation, and distribution channels."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    positioning_category: str = "Developer Tool"
    target_segment: str = "SMB"
    primary_motion: MotionType = MotionType.PLG
    pricing_model: str = "Usage-Based"

    def determine_channel_fit(self, complexity_score: float, price_acv_cents: int) -> MotionType:
        """Determines channel fit based on product complexity and ACV price point."""
        if price_acv_cents > 50000_00 or complexity_score > 0.7:
            self.primary_motion = MotionType.SLG
        elif complexity_score < 0.3 and price_acv_cents < 5000_00:
            self.primary_motion = MotionType.PLG
        else:
            self.primary_motion = MotionType.CLG
        return self.primary_motion


# =====================================================================
# Section 6. Company Growth System
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


class GrowthStageClassifier(BaseModel):
    """Classifies venture growth stage and enforces stage-appropriate constraints."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    current_stage: GrowthStage = GrowthStage.IDEA

    def classify_stage(
        self,
        paying_customers: int,
        mrr_cents: int,
        retention_curve_flattened: bool,
        rule_of_40: float,
        has_ecosystem_developers: bool
    ) -> GrowthStage:
        if has_ecosystem_developers and mrr_cents > 10000000_00:
            self.current_stage = GrowthStage.MARKET_LEADERSHIP
        elif mrr_cents > 5000000_00 and rule_of_40 > 0.40:
            self.current_stage = GrowthStage.SCALE
        elif mrr_cents > 1000000_00 and retention_curve_flattened:
            self.current_stage = GrowthStage.GROWTH
        elif retention_curve_flattened and paying_customers > 20:
            self.current_stage = GrowthStage.PMF
        elif paying_customers > 0:
            self.current_stage = GrowthStage.STARTUP
        elif paying_customers == 0 and mrr_cents == 0:
            self.current_stage = GrowthStage.IDEA
        return self.current_stage


# =====================================================================
# Section 7. Strategic Thinking & Moats
# =====================================================================

class StrategicMoatEngine(BaseModel):
    """Quantifies 6 competitive moat scores, cost curves, and counter-positioning."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    network_effects_score: float = 0.5
    switching_costs_score: float = 0.5
    economies_of_scale_score: float = 0.5
    brand_trust_score: float = 0.5
    ip_regulatory_score: float = 0.5
    counter_positioning_score: float = 0.5

    def compute_composite_moat_durability(self) -> float:
        scores = [
            self.network_effects_score,
            self.switching_costs_score,
            self.economies_of_scale_score,
            self.brand_trust_score,
            self.ip_regulatory_score,
            self.counter_positioning_score
        ]
        return float(sum(scores) / len(scores))


# =====================================================================
# Section 8. Failure Mode Analysis
# =====================================================================

class FailureModeName(str, Enum):
    WRONG_PROBLEM = "Solving the wrong problem"
    BUILD_BEFORE_VALIDATE = "Building before validating"
    WEAK_POSITIONING = "Weak positioning"
    POOR_PRICING = "Poor pricing"
    DISTRIBUTION_FAILURE = "Distribution failure"
    LACK_OF_PMF = "Lack of product-market fit"
    ORG_BOTTLENECKS = "Organizational bottlenecks"
    FOUNDER_BIAS = "Founder bias"
    PREMATURE_SCALING = "Scaling prematurely"
    CAPITAL_MISALLOCATION = "Capital misallocation"


class FailureModeMonitor(BaseModel):
    """Pattern-matches operating metrics to raise early warning signals and corrections."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    active_warnings: List[Dict[str, str]] = Field(default_factory=list)

    def evaluate_diagnostics(
        self,
        survey_vs_engagement_gap: float,
        build_velocity_vs_demand_gap: float,
        retention_flattened: bool,
        cac_growth_vs_ltv_growth: float,
        decision_latency_sec: float
    ) -> List[Dict[str, str]]:
        self.active_warnings.clear()

        if survey_vs_engagement_gap > 0.4:
            self.active_warnings.append({
                "failure_mode": FailureModeName.WRONG_PROBLEM.value,
                "signal": "Low engagement despite positive survey feedback",
                "correction": "Return to root cause JTBD interviews"
            })
        if build_velocity_vs_demand_gap > 0.5:
            self.active_warnings.append({
                "failure_mode": FailureModeName.BUILD_BEFORE_VALIDATE.value,
                "signal": "High build velocity with flat demand signal",
                "correction": "Enforce validation gate before build resourcing"
            })
        if not retention_flattened:
            self.active_warnings.append({
                "failure_mode": FailureModeName.LACK_OF_PMF.value,
                "signal": "Retention curve never flattens",
                "correction": "Stop scaling; return to cohort-level retention work"
            })
        if cac_growth_vs_ltv_growth > 1.5:
            self.active_warnings.append({
                "failure_mode": FailureModeName.PREMATURE_SCALING.value,
                "signal": "CAC rising faster than LTV as spend scales",
                "correction": "Re-test unit economics at each order of magnitude"
            })
        if decision_latency_sec > 86400.0:  # > 24 hours
            self.active_warnings.append({
                "failure_mode": FailureModeName.ORG_BOTTLENECKS.value,
                "signal": "Rising decision latency",
                "correction": "Push decision rights down with clear frameworks"
            })

        return self.active_warnings


# =====================================================================
# Section 9. Scientific Foundations Registry
# =====================================================================

class ScientificFoundationsRegistry(BaseModel):
    """Maps core concepts and key academic sources across 12 scientific domains."""

    domains: Dict[str, Dict[str, str]] = Field(default_factory=lambda: {
        "Economics": {"concepts": "Opportunity cost, cost curves", "sources": "Schumpeter, Christensen"},
        "Strategy": {"concepts": "Moats, positioning, counter-positioning", "sources": "Porter, Helmer"},
        "Systems Thinking": {"concepts": "Stocks/flows, feedback loops", "sources": "Donella Meadows"},
        "Decision Theory": {"concepts": "Reversible vs irreversible, real options", "sources": "McGrath"},
        "Game Theory": {"concepts": "Competitive response, signaling", "sources": "Schelling"},
        "Behavioral Economics": {"concepts": "Loss aversion, sunk cost", "sources": "Kahneman & Tversky"},
        "Cognitive Psychology": {"concepts": "Anomaly detection, mental model updating", "sources": "Kuhn, Bayesian surprise"},
        "Organizational Theory": {"concepts": "Decision-rights delegation", "sources": "Chandler"},
        "Marketing Science": {"concepts": "Positioning, category design", "sources": "Ries & Trout, Aaker"},
        "Innovation Research": {"concepts": "Disruption, platform shifts", "sources": "Christensen, Bower"},
        "Operations Research": {"concepts": "Throughput, bottleneck theory", "sources": "Goldratt"},
        "Complexity Science": {"concepts": "Emergence, adaptive systems", "sources": "Holland, Beinhocker"}
    })


# =====================================================================
# Section 10. AI-Driven State Machine & Decision Tree
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


class EOSStateMachine(BaseModel):
    """System State Machine implementing §10.1 transitions."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    current_state: EOSState = EOSState.SENSING
    transition_log: List[Dict[str, str]] = Field(default_factory=list)

    def transition_to(self, new_state: EOSState, trigger_event: str) -> EOSState:
        prev = self.current_state
        self.current_state = new_state
        self.transition_log.append({
            "from": prev.value,
            "to": new_state.value,
            "event": trigger_event,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        logger.info(f"EOSStateMachine state transition: {prev.value} -> {new_state.value} via '{trigger_event}'")
        return self.current_state


class OpportunityDecisionTree(BaseModel):
    """Sequential Decision Tree implementing §10.2 ('Should We Pursue This Opportunity?')."""

    def evaluate_opportunity(
        self,
        is_structural_anomaly: bool,
        is_reversible_decision: bool,
        has_high_confidence_multi_source: bool,
        cheap_test_available: bool,
        test_exceeds_kill_threshold: bool,
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> Tuple[bool, str]:
        """Runs decision tree and returns (pursue_boolean, resolution_path_description)."""
        # Q1: Structural anomaly or just noise?
        if not is_structural_anomaly:
            return (False, "Discard: Noise signal, not a structural anomaly")

        # Q2: Reversible decision?
        if not is_reversible_decision:
            # Q2a: High-confidence signal from multiple sources?
            if not has_high_confidence_multi_source:
                return (False, "Discard: Irreversible decision without high-confidence multi-source signal")

        # Q3: Cheap test available?
        if cheap_test_available:
            if not test_exceeds_kill_threshold:
                return (False, "Discard: Cheap test result failed kill threshold")
        else:
            if not expected_value_positive:
                return (False, "Discard: No cheap test and expected value not positive")

        # Q5: Do we have or can we build a structural advantage?
        if not has_structural_advantage:
            return (False, "Discard: Lack of structural competitive advantage")

        return (True, "Pursue: All decision tree criteria passed successfully - Commit resources")


# =====================================================================
# Master Orchestrator: FirstPrinciplesEOSEngine
# =====================================================================

class FirstPrinciplesEOSEngine(BaseModel):
    """Unified master engine orchestrating all 11 sections of the Entrepreneurial Operating System."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    master_loop: MasterLoopEngine = Field(default_factory=MasterLoopEngine)
    signal_pipeline: SignalToIdeaPipeline = Field(default_factory=SignalToIdeaPipeline)
    mental_model: MentalModelEngine = Field(default_factory=MentalModelEngine)
    business_loops: CoupledBusinessLoopsEngine = Field(default_factory=CoupledBusinessLoopsEngine)
    customer_lifecycle: CustomerLifecycleEngine = Field(default_factory=CustomerLifecycleEngine)
    gtm_system: GTMSystemEngine = Field(default_factory=GTMSystemEngine)
    growth_classifier: GrowthStageClassifier = Field(default_factory=GrowthStageClassifier)
    moat_engine: StrategicMoatEngine = Field(default_factory=StrategicMoatEngine)
    failure_monitor: FailureModeMonitor = Field(default_factory=FailureModeMonitor)
    foundations_registry: ScientificFoundationsRegistry = Field(default_factory=ScientificFoundationsRegistry)
    state_machine: EOSStateMachine = Field(default_factory=EOSStateMachine)
    decision_tree: OpportunityDecisionTree = Field(default_factory=OpportunityDecisionTree)

    def process_opportunity_signal(
        self,
        signal_name: str,
        observed_val: float,
        expected_val: float,
        is_reversible: bool = True,
        has_structural_advantage: bool = True
    ) -> Dict[str, Any]:
        """Runs complete end-to-end processing of an incoming market signal through state machine & decision tree."""
        # 1. Anomaly detection in signal pipeline
        is_anomaly = self.signal_pipeline.detect_anomaly(signal_name, observed_val, expected_val)

        if not is_anomaly:
            return {"action": "discard", "reason": "No structural anomaly detected", "state": self.state_machine.current_state.value}

        self.state_machine.transition_to(EOSState.HYPOTHESIS, "Anomaly detected")

        # 2. Form forced hypothesis
        hyp = self.signal_pipeline.form_forced_hypothesis(
            statement=f"Structural shift detected in {signal_name}",
            falsifiable_criteria="Metric increases by >=20% in 30 days",
            risk_type=DecisionRiskType.TYPE_II if is_reversible else DecisionRiskType.TYPE_I
        )

        self.state_machine.transition_to(EOSState.CHEAP_TEST, "Hypothesis formed")

        # 3. Evaluate cheap test
        post_belief = self.signal_pipeline.run_cheap_test(hyp, test_result_success=True)

        if hyp.is_falsified:
            self.state_machine.transition_to(EOSState.DISCARD, "Cheap test falsified hypothesis")
            return {"action": "discard", "reason": "Falsified in cheap test", "posterior_belief": post_belief}

        self.state_machine.transition_to(EOSState.VALIDATION, "Cheap test strengthened belief")

        # 4. Evaluate Decision Tree
        pursue, decision_reason = self.decision_tree.evaluate_opportunity(
            is_structural_anomaly=True,
            is_reversible_decision=is_reversible,
            has_high_confidence_multi_source=True,
            cheap_test_available=True,
            test_exceeds_kill_threshold=True,
            expected_value_positive=True,
            has_structural_advantage=has_structural_advantage
        )

        if pursue:
            self.state_machine.transition_to(EOSState.BUILD_GATE, "Economic viability confirmed")
            self.state_machine.transition_to(EOSState.MVP, "Resources committed")
            self.state_machine.transition_to(EOSState.GTM_TEST, "MVP shipped")
            self.state_machine.transition_to(EOSState.KILL_OR_SCALE, "GTM signal collected")
            self.state_machine.transition_to(EOSState.SCALE, "Scale threshold exceeded")
            self.state_machine.transition_to(EOSState.OPERATE, "Repeatable loop confirmed")

        return {
            "action": "pursue" if pursue else "discard",
            "decision_reason": decision_reason,
            "posterior_belief": post_belief,
            "final_state": self.state_machine.current_state.value
        }

    def compute_kpi_stack(self) -> Dict[str, float]:
        """Rolls up system KPIs across Sensing, Validation, Product, GTM, Financial, Org, and Strategy."""
        moat_durability = self.moat_engine.compute_composite_moat_durability()
        stocks = self.business_loops.stocks
        cash = stocks.get("cash_cents", 0.0) / 100.0

        return {
            "sensing_signal_fidelity": self.master_loop.signal_fidelity_score,
            "loop_velocity_days": self.master_loop.loop_velocity_days,
            "product_loop_health": self.business_loops.loops[BusinessLoopName.PRODUCT].health_score,
            "financial_cash_balance": cash,
            "moat_durability_score": moat_durability,
            "failure_warnings_count": float(len(self.failure_monitor.active_warnings))
        }
