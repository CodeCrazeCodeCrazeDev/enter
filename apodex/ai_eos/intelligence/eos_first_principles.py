"""First-Principles Implementation of the Entrepreneurial Operating System (EOS).

Reconstructs how elite founders sense, build, and compound enduring companies,
providing structured Python models and logic for:
- Multi-timescale feedback loops (Fast, Medium, Slow)
- Signal-to-Idea Pipeline (Anomaly detection, Type I vs Type II risk, cheap tests, opportunity cost)
- Mental Model Evolution (Parameter vs structural updates, ossification metric)
- 13 Coupled External Business Loops & stock/flow network dynamics
- 15-Stage Customer Lifecycle Journey
- Integrated Go-to-Market (GTM) System & motion composition
- 9-Stage Company Growth Classifier & binding constraints
- Strategic Moat Durability Evaluator (6 moat types)
- 10 Failure Mode Detection & Correction Monitor
- 11-State System State Machine & Opportunity Decision Tree
- 10-Module AI Implementation Registry & Subsystem KPI Stack
"""

from __future__ import annotations
import math
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from datetime import datetime, UTC
from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger("ai_eos.eos_first_principles")


# =====================================================================
# 0. Framing & Timescale Loops
# =====================================================================
class Timescale(str, Enum):
    FAST = "days_weeks"
    MEDIUM = "months_quarters"
    SLOW = "years"


class TimescaleLoop(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    loop_id: str
    name: str
    timescale: Timescale
    velocity_hz: float = 1.0  # Execution frequency relative to baseline
    active: bool = True
    compounding_rate: float = 0.05  # Rate of cumulative learning/yield per cycle


class MultiTimescaleLoopEngine(BaseModel):
    """Orchestrates fast, medium, and slow nested feedback loops."""

    loops: Dict[str, TimescaleLoop] = Field(default_factory=dict)

    def register_loop(self, loop: TimescaleLoop) -> None:
        self.loops[loop.loop_id] = loop

    def calculate_aggregate_loop_velocity(self) -> Dict[str, float]:
        velocities = {Timescale.FAST.value: 0.0, Timescale.MEDIUM.value: 0.0, Timescale.SLOW.value: 0.0}
        counts = {Timescale.FAST.value: 0, Timescale.MEDIUM.value: 0, Timescale.SLOW.value: 0}

        for loop in self.loops.values():
            if loop.active:
                ts = loop.timescale.value
                velocities[ts] += loop.velocity_hz
                counts[ts] += 1

        return {
            ts: (velocities[ts] / counts[ts] if counts[ts] > 0 else 0.0)
            for ts in velocities
        }

    def evaluate_kill_discipline(self, performance_threshold: float = 0.02) -> List[str]:
        """Identifies loops that are failing to compound and should be killed/refactored."""
        killed_loops = []
        for loop_id, loop in self.loops.items():
            if loop.active and loop.compounding_rate < performance_threshold:
                loop.active = False
                killed_loops.append(loop_id)
                logger.info(f"[MultiTimescaleLoopEngine] Killed non-compounding loop: {loop.name}")
        return killed_loops


# =====================================================================
# 2. Internal Cognitive Loops & Signal-to-Idea Pipeline
# =====================================================================
class RiskType(str, Enum):
    TYPE_1 = "TYPE_1_IRREVERSIBLE"  # One-way door: high scrutiny, slow deliberation
    TYPE_2 = "TYPE_2_REVERSIBLE"    # Two-way door: fast, cheap execution


class Signal(BaseModel):
    signal_id: str
    source: str
    content: str
    is_anomaly: bool = False
    structural_shift_probability: float = 0.0
    noise_level: float = 0.5


class DecisionRiskEvaluation(BaseModel):
    decision_name: str
    is_reversible: bool
    risk_type: RiskType
    required_confidence_threshold: float
    recommended_deliberation_speed: str


class SignalToIdeaPipeline(BaseModel):
    """Converts weak signals into falsifiable hypotheses and cheap real-option experiments."""

    symptomatic_filter_threshold: float = 0.6

    def filter_signal(self, signal: Signal) -> bool:
        """Determines if a weak signal is a symptom of a structural shift or just noise."""
        if not signal.is_anomaly:
            return False
        signal_score = signal.structural_shift_probability * (1.0 - signal.noise_level)
        return signal_score >= self.symptomatic_filter_threshold

    def evaluate_decision_risk(self, is_reversible: bool, stakes_usd: float) -> DecisionRiskEvaluation:
        """Classifies risk into Type I (irreversible) vs Type II (reversible) - Bezos's heuristic."""
        if not is_reversible or stakes_usd > 100_000:
            return DecisionRiskEvaluation(
                decision_name="High-Stakes / Irreversible Commitment",
                is_reversible=False,
                risk_type=RiskType.TYPE_1,
                required_confidence_threshold=0.85,
                recommended_deliberation_speed="SLOW_HIGH_SCRUTINY"
            )
        return DecisionRiskEvaluation(
            decision_name="Low-Stakes / Reversible Experiment",
            is_reversible=True,
            risk_type=RiskType.TYPE_2,
            required_confidence_threshold=0.40,
            recommended_deliberation_speed="FAST_CHEAP_TEST"
        )

    def evaluate_cheap_test(self, test_cost_usd: float, expected_information_gain: float) -> bool:
        """Real options approach: purchases information cheaply before committing major capital."""
        if test_cost_usd <= 0:
            return True
        roi = expected_information_gain / test_cost_usd
        return roi >= 0.01

    def calculate_opportunity_cost_score(
        self,
        expected_compounding_return: float,
        best_alternative_return: float,
        structural_win_reason: bool,
        market_size_5yr_usd: float
    ) -> float:
        """Scores opportunity pursuit via compounding, structural edge, and market scale."""
        if not structural_win_reason or market_size_5yr_usd < 10_000_000:
            return 0.0
        return max(0.0, expected_compounding_return - best_alternative_return)


# =====================================================================
# 2.2 Mental Model Evolution
# =====================================================================
class MentalModel(BaseModel):
    model_id: str
    name: str
    structure_version: int = 1
    parameters: Dict[str, float] = Field(default_factory=dict)
    prediction_history: List[Dict[str, Any]] = Field(default_factory=list)
    parameter_updates_count: int = 0
    structural_refactors_count: int = 0

    def generate_prediction(self, metric_name: str, input_value: float) -> float:
        weight = self.parameters.get(metric_name, 1.0)
        predicted = weight * input_value
        self.prediction_history.append({
            "metric": metric_name,
            "input": input_value,
            "predicted": predicted,
            "actual": None,
            "timestamp": datetime.now(UTC).isoformat()
        })
        return predicted

    def process_feedback(self, metric_name: str, actual_value: float) -> float:
        """Compares prediction with reality and calculates forecast error."""
        if not self.prediction_history:
            return 0.0
        latest = self.prediction_history[-1]
        if latest["metric"] == metric_name:
            latest["actual"] = actual_value
            error = abs(actual_value - latest["predicted"])
            return error
        return 0.0

    def update_model(self, metric_name: str, actual_value: float, learning_rate: float = 0.1) -> str:
        """Updates model parameters (fast) or structure (paradigm shift when error is persistent)."""
        error = self.process_feedback(metric_name, actual_value)
        current_param = self.parameters.get(metric_name, 1.0)

        # Large persistent error (>50%) triggers a structural refactor (paradigm shift)
        if error > 0.5 * actual_value and actual_value > 0:
            self.structure_version += 1
            self.structural_refactors_count += 1
            self.parameters[metric_name] = actual_value / max(0.01, self.prediction_history[-1]["input"])
            logger.warning(f"[MentalModel] Paradigm shift! Structural refactor to v{self.structure_version}")
            return "STRUCTURAL_REFACTOR"
        else:
            # Parameter tuning normalized by input value
            latest_pred = self.prediction_history[-1]["predicted"] if self.prediction_history else 0.0
            latest_input = self.prediction_history[-1]["input"] if self.prediction_history else 1.0
            param_delta = learning_rate * (actual_value - latest_pred) / max(0.01, latest_input)
            new_param = current_param + param_delta
            self.parameters[metric_name] = float(new_param)
            self.parameter_updates_count += 1
            return "PARAMETER_TUNING"

    @property
    def ossification_score(self) -> float:
        """Measures risk of model ossification (tuning parameters without updating structure)."""
        if self.structural_refactors_count == 0:
            return min(1.0, self.parameter_updates_count / 20.0)
        return float(self.parameter_updates_count / (self.structural_refactors_count * 50.0))


# =====================================================================
# 3. External Business Loops
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
    COMPETITIVE_INTELLIGENCE = "COMPETITIVE_INTELLIGENCE"


class BusinessLoop(BaseModel):
    name: BusinessLoopName
    inputs: List[str]
    outputs: List[str]
    feedback_signal: str
    core_kpis: List[str]
    failure_mode: str
    health_score: float = 1.0  # [0, 1]


class BusinessLoopNetwork(BaseModel):
    """Network of 13 coupled business loops operating over company stocks and flows."""

    loops: Dict[BusinessLoopName, BusinessLoop] = Field(default_factory=dict)
    stocks: Dict[str, float] = Field(default_factory=lambda: {
        "cash_usd": 1_000_000.0,
        "talent_headcount": 10.0,
        "trust_score": 0.8,
        "data_volume_gb": 100.0
    })

    def initialize_canonical_loops(self) -> None:
        """Initializes the 13 canonical business loops specified in Section 3."""
        canonical_specs = [
            (BusinessLoopName.PRODUCT, ["User behavior", "Support tickets"], ["Feature changes", "Roadmap"], "Activation/retention deltas", ["Retention curve", "NPS"], "Building for loudest customer"),
            (BusinessLoopName.MARKETING, ["Positioning", "Market data"], ["Awareness", "Demand"], "CAC, traffic quality", ["CAC", "Brand recall", "Conversion rate"], "Message-market mismatch"),
            (BusinessLoopName.SALES, ["Qualified leads", "Product"], ["Closed revenue", "Customer feedback"], "Win/loss reasons", ["Win rate", "Sales cycle length", "ACV"], "Selling to non-ICP"),
            (BusinessLoopName.CUSTOMER_SUCCESS, ["Onboarding data", "Usage"], ["Retention", "Expansion"], "Churn reasons", ["NRR", "Churn rate", "Time-to-value"], "Reactive CS"),
            (BusinessLoopName.BRAND, ["Product experience", "Comms"], ["Trust", "Pricing power"], "Sentiment, unaided recall", ["Share of voice", "Price elasticity"], "Brand as decoration"),
            (BusinessLoopName.PRICING, ["Value delivered", "WTP data"], ["Revenue", "Positioning signal"], "Conversion by price point", ["ARPU", "Price realization"], "Cost-plus pricing"),
            (BusinessLoopName.REFERRAL, ["Customer satisfaction", "Incentives"], ["New customer flow"], "Referral rate, K-factor", ["Viral coefficient", "Referral CAC"], "Incentivizing volume over quality"),
            (BusinessLoopName.DATA, ["All metrics"], ["Decisions"], "Model accuracy vs outcomes", ["Data latency", "Decision cycle time"], "Vanity metrics"),
            (BusinessLoopName.FINANCIAL, ["Revenue", "Costs", "Capital"], ["Runway", "Reinvestment capacity"], "Burn multiple, margin trend", ["Gross margin", "Burn multiple", "Runway"], "Growth at negative unit economics"),
            (BusinessLoopName.HIRING, ["Org needs", "Culture"], ["Capability", "Capacity"], "90-day performance", ["Time-to-fill", "Quality of hire", "Retention"], "Hiring for pedigree over role-fit"),
            (BusinessLoopName.CULTURE, ["Values-in-action", "Incentives"], ["Behavior consistency"], "Employee sentiment, decision speed", ["eNPS", "Decision latency"], "Values-as-poster"),
            (BusinessLoopName.INNOVATION, ["R&D", "Market signals"], ["New products/features"], "Time-to-market, cannibalization", ["# experiments run", "Hit rate"], "Innovation theater"),
            (BusinessLoopName.COMPETITIVE_INTELLIGENCE, ["Market/competitor data"], ["Strategic repositioning"], "Win/loss vs competitors", ["Relative share trend", "Feature parity gap"], "Reacting instead of leading")
        ]
        for name, inp, out, fb, kpis, fm in canonical_specs:
            self.loops[name] = BusinessLoop(
                name=name, inputs=inp, outputs=out, feedback_signal=fb, core_kpis=kpis, failure_mode=fm
            )

    def propagate_coupling_effects(self, arpu_delta: float, churn_delta: float) -> Dict[str, Any]:
        """Simulates coupling: Pricing output (ARPU) -> Financial -> Hiring -> Product velocity."""
        if BusinessLoopName.PRICING in self.loops:
            self.loops[BusinessLoopName.PRICING].health_score = max(0.1, min(1.0, 1.0 + arpu_delta))

        # Financial impact
        financial_health = max(0.1, min(1.0, 1.0 + 0.8 * arpu_delta - 1.2 * churn_delta))
        if BusinessLoopName.FINANCIAL in self.loops:
            self.loops[BusinessLoopName.FINANCIAL].health_score = financial_health

        # Hiring budget follows financial health
        hiring_health = 0.9 * financial_health
        if BusinessLoopName.HIRING in self.loops:
            self.loops[BusinessLoopName.HIRING].health_score = hiring_health

        # Product loop velocity follows hiring capacity
        product_health = 0.85 * hiring_health
        if BusinessLoopName.PRODUCT in self.loops:
            self.loops[BusinessLoopName.PRODUCT].health_score = product_health

        return {
            "financial_health": financial_health,
            "hiring_health": hiring_health,
            "product_health": product_health
        }


# =====================================================================
# 4. Customer Journey Lifecycle
# =====================================================================
class CustomerJourneyStage(str, Enum):
    AWARENESS = "AWARENESS"
    INTEREST = "INTEREST"
    CONSIDERATION = "CONSIDERATION"
    EVALUATION = "EVALUATION"
    PURCHASE = "PURCHASE"
    ONBOARDING = "ONBOARDING"
    ACTIVATION = "ACTIVATION"
    ENGAGEMENT = "ENGAGEMENT"
    HABIT_FORMATION = "HABIT_FORMATION"
    RETENTION = "RETENTION"
    LOYALTY = "LOYALTY"
    ADVOCACY = "ADVOCACY"
    REFERRAL = "REFERRAL"
    EXPANSION = "EXPANSION"
    REPURCHASE = "REPURCHASE"


class CustomerJourneyStageDetail(BaseModel):
    stage: CustomerJourneyStage
    founder_objective: str
    customer_psychology: str
    key_metric: str
    common_mistake: str
    optimization_lever: str


class CustomerJourneyEngine(BaseModel):
    """Manages the 15-stage customer lifecycle from Awareness to Repurchase."""

    stages: Dict[CustomerJourneyStage, CustomerJourneyStageDetail] = Field(default_factory=dict)

    def initialize_canonical_stages(self) -> None:
        canonical_specs = [
            (CustomerJourneyStage.AWARENESS, "Enter consideration set", "Pattern-matching against known categories", "Reach, unaided recall", "Generic category messaging", "Sharp category framing"),
            (CustomerJourneyStage.INTEREST, "Earn attention", "Curiosity vs skepticism", "CTR, engagement rate", "Feature-dumping", "Lead with pain"),
            (CustomerJourneyStage.CONSIDERATION, "Differentiate", "Comparing against status quo & alternatives", "Time-on-site, content depth", "Competing on features competitors have", "Reframe comparison axis"),
            (CustomerJourneyStage.EVALUATION, "Reduce perceived risk", "Loss aversion dominates gain-seeking", "Trial starts, demo requests", "Ignoring risk-reduction", "Make failure cheap & reversible"),
            (CustomerJourneyStage.PURCHASE, "Convert intent to commitment", "Decision fatigue, need for certainty", "Conversion rate", "Friction in checkout/contracting", "Remove friction steps"),
            (CustomerJourneyStage.ONBOARDING, "Deliver first value fast", "Anxiety about wasted decision", "Time-to-first-value", "Feature-tour instead of outcome-tour", "Anchor onboarding to JTBD"),
            (CustomerJourneyStage.ACTIVATION, "Cross 'aha' threshold", "Forming initial habit loop", "Activation rate", "Defining activation as login", "Instrument true 'aha' moment"),
            (CustomerJourneyStage.ENGAGEMENT, "Build usage depth", "Reinforcement learning (reward loop)", "DAU/MAU, session depth", "Engagement not correlating with retention", "Optimize behavior predicting retention"),
            (CustomerJourneyStage.HABIT_FORMATION, "Make usage automatic", "Cue-routine-reward loop (Hook Model)", "Habit strength / frequency", "No external trigger cadence", "Build reliable triggers"),
            (CustomerJourneyStage.RETENTION, "Prevent churn", "Switching cost perception, sunk value", "Retention curve, churn", "Measuring retention in aggregate only", "Cohort retention flattening point analysis"),
            (CustomerJourneyStage.LOYALTY, "Deepen emotional/economic lock-in", "Identity alignment with brand", "Repeat purchase rate", "Assuming satisfaction = loyalty", "Build genuine switching costs"),
            (CustomerJourneyStage.ADVOCACY, "Convert satisfaction to voice", "Social proof-seeking, reciprocity", "NPS, UGC volume", "Asking for advocacy before value proven", "Ask at peak-value moments"),
            (CustomerJourneyStage.REFERRAL, "Convert advocacy to acquisition", "Trust transfer peer to peer", "Viral coefficient (K)", "Generic referral programs", "Align incentive with genuine value"),
            (CustomerJourneyStage.EXPANSION, "Grow account value", "Anchoring to current spend", "Net revenue retention (NRR)", "Under-selling adjacent value", "Usage-based expansion triggers"),
            (CustomerJourneyStage.REPURCHASE, "Sustain lifetime value", "Habitual trust, low re-evaluation cost", "LTV, repurchase rate", "Treating repurchase as passive", "Proactive lifecycle marketing")
        ]
        for st, obj, psych, km, cm, ol in canonical_specs:
            self.stages[st] = CustomerJourneyStageDetail(
                stage=st, founder_objective=obj, customer_psychology=psych, key_metric=km, common_mistake=cm, optimization_lever=ol
            )

    def analyze_cohort_retention_flattening(self, cohort_retention_by_period: List[float]) -> Dict[str, Any]:
        """Analyzes retention curve slope to verify if cohort retention flattens (PMF indicator)."""
        if len(cohort_retention_by_period) < 3:
            return {"flattens": False, "flattening_period": None, "terminal_retention": 0.0}

        # Calculate deltas between consecutive periods
        deltas = [cohort_retention_by_period[i] - cohort_retention_by_period[i - 1] for i in range(1, len(cohort_retention_by_period))]

        # Check if recent deltas are near zero (slope flattening)
        recent_deltas = deltas[-2:]
        flattens = all(abs(d) < 0.02 for d in recent_deltas)
        terminal_retention = cohort_retention_by_period[-1]

        return {
            "flattens": flattens,
            "flattening_period": len(cohort_retention_by_period) - 1 if flattens else None,
            "terminal_retention": terminal_retention
        }


# =====================================================================
# 5. Go-to-Market System
# =====================================================================
class ChannelType(str, Enum):
    ORGANIC = "ORGANIC"
    PAID = "PAID"
    PARTNER = "PARTNER"
    CONTENT = "CONTENT"
    PLG = "PRODUCT_LED"
    SLG = "SALES_LED"
    CLG = "COMMUNITY_LED"
    ENTERPRISE = "ENTERPRISE_SALES"


class GTMSystem(BaseModel):
    """Integrated Go-To-Market system connecting positioning, pricing, segmentation, and channels."""

    category_positioning: str = "Category Leader"
    price_point_usd: float = 100.0

    def select_optimal_distribution_channels(
        self,
        product_complexity: str,  # LOW, MEDIUM, HIGH
        price_point_annual_usd: float,
        network_effects_present: bool
    ) -> List[ChannelType]:
        """Channel selection follows buyer behavior and product complexity."""
        channels = []
        if product_complexity == "LOW" and price_point_annual_usd < 1_000:
            channels.extend([ChannelType.PLG, ChannelType.CONTENT, ChannelType.ORGANIC])
        elif product_complexity == "HIGH" or price_point_annual_usd >= 50_000:
            channels.extend([ChannelType.SLG, ChannelType.ENTERPRISE])
            if price_point_annual_usd >= 100_000:
                channels.append(ChannelType.PARTNER)
        else:
            channels.extend([ChannelType.CONTENT, ChannelType.PAID, ChannelType.SLG])

        if network_effects_present:
            channels.append(ChannelType.CLG)

        return channels

    def evaluate_pricing_positioning_alignment(self, price_usd: float, segment_tier: str) -> bool:
        """Verifies pricing is a positioning signal and segmentation filter, not cost-plus."""
        if segment_tier == "ENTERPRISE" and price_usd < 10_000:
            logger.warning("[GTMSystem] Price too low for Enterprise positioning - undercutting value signal.")
            return False
        if segment_tier == "SELF_SERVE" and price_usd > 2_000:
            logger.warning("[GTMSystem] Price too high for Self-Serve self-checkout friction.")
            return False
        return True


# =====================================================================
# 6. Company Growth System
# =====================================================================
class GrowthStage(str, Enum):
    IDEA = "IDEA"
    VALIDATION = "VALIDATION"
    STARTUP = "STARTUP"
    PMF = "PRODUCT_MARKET_FIT"
    GROWTH = "GROWTH"
    SCALE = "SCALE"
    PLATFORM = "PLATFORM"
    ECOSYSTEM = "ECOSYSTEM"
    MARKET_LEADERSHIP = "MARKET_LEADERSHIP"


class GrowthStageDetail(BaseModel):
    stage: GrowthStage
    primary_objective: str
    org_change: str
    decision_making_change: str
    capital_allocation: str
    key_risk: str
    core_metric: str
    binding_constraint: str


class CompanyGrowthEngine(BaseModel):
    """Tracks progression across 9 growth stages and identifies stage binding constraints."""

    stage_details: Dict[GrowthStage, GrowthStageDetail] = Field(default_factory=dict)

    def initialize_canonical_stages(self) -> None:
        canonical = [
            (GrowthStage.IDEA, "Falsify or strengthen hypothesis", "Founder(s) only", "Founder intuition, fast", "Near-zero, sweat equity", "Solving a non-problem", "# validated learnings", "Founder time"),
            (GrowthStage.VALIDATION, "Prove willingness to pay", "First 1-3 hires", "Still founder-centric", "Pre-seed/seed capital", "False positive validation", "Paying customers / LOIs", "Signal quality"),
            (GrowthStage.STARTUP, "Build repeatable acquisition", "Functional roles emerge", "Founder + small team", "Seed/Series A", "Premature scaling before PMF", "CAC:LTV early signal", "Cash runway"),
            (GrowthStage.PMF, "Reach retention/growth threshold", "First managers", "Data starts overriding intuition", "Growth capital", "Mistaking early traction for PMF", "Retention curve flattening", "Team bandwidth"),
            (GrowthStage.GROWTH, "Scale what works", "Middle management layer", "Process + data-driven", "Series B/C", "Scaling broken funnel", "Growth rate, CAC payback", "Hiring velocity"),
            (GrowthStage.SCALE, "Institutionalize repeatability", "Departments, specialized functions", "Delegated, framework-driven", "Efficient growth capital", "Culture dilution, bureaucracy", "Rule of 40, NRR", "Org coordination cost"),
            (GrowthStage.PLATFORM, "Enable others to build on you", "Platform/ecosystem teams", "Governance structures, APIs", "Infrastructure investment", "Platform without ecosystem demand", "3rd-party developer activity", "Trust from partners"),
            (GrowthStage.ECOSYSTEM, "Orchestrate multi-sided network", "Ecosystem management, BD", "Distributed decision rights", "Strategic/M&A capital", "Ecosystem fragmentation", "Ecosystem GMV / network density", "Governance credibility"),
            (GrowthStage.MARKET_LEADERSHIP, "Defend and extend category", "Full corporate structure", "Board-level strategic governance", "Diversified capital", "Complacency, disruption", "Category share, moat durability", "Innovation velocity vs drag")
        ]
        for st, obj, org, dec, cap, rk, cm, bc in canonical:
            self.stage_details[st] = GrowthStageDetail(
                stage=st, primary_objective=obj, org_change=org, decision_making_change=dec, capital_allocation=cap, key_risk=rk, core_metric=cm, binding_constraint=bc
            )

    def classify_stage(self, paying_customers: int, nrr: float, retention_flattens: bool, annual_revenue_usd: float) -> GrowthStage:
        """Classifies venture stage to prevent premature scaling or under-investment."""
        if paying_customers == 0:
            return GrowthStage.IDEA if annual_revenue_usd == 0 else GrowthStage.VALIDATION
        if paying_customers < 10 or not retention_flattens:
            return GrowthStage.VALIDATION
        if annual_revenue_usd < 1_000_000:
            return GrowthStage.STARTUP if not retention_flattens else GrowthStage.PMF
        if annual_revenue_usd < 10_000_000:
            return GrowthStage.GROWTH
        if annual_revenue_usd < 50_000_000:
            return GrowthStage.SCALE
        if nrr > 1.20 and annual_revenue_usd >= 50_000_000:
            return GrowthStage.PLATFORM
        return GrowthStage.MARKET_LEADERSHIP


# =====================================================================
# 7. Strategic Moats & Moat Evaluator
# =====================================================================
class MoatType(str, Enum):
    NETWORK_EFFECTS = "NETWORK_EFFECTS"
    SWITCHING_COSTS = "SWITCHING_COSTS"
    SCALE_ECONOMIES = "SCALE_ECONOMIES"
    BRAND = "BRAND"
    REGULATORY_IP = "REGULATORY_IP"
    COUNTER_POSITIONING = "COUNTER_POSITIONING"


class MoatEvaluator(BaseModel):
    """Evaluates composite moat durability across 6 structural advantage dimensions."""

    def calculate_composite_moat_score(
        self,
        network_density: float,         # [0, 1]
        avg_switching_cost_usd: float,   # normalized at $10k
        brand_trust_score: float,       # [0, 1]
        cost_advantage_percent: float,  # [0, 1]
        ip_protection_score: float,     # [0, 1]
        counter_positioning_score: float# [0, 1]
    ) -> float:
        """Calculates normalized composite moat durability score [0, 1]."""
        s_net = min(1.0, max(0.0, network_density))
        s_sw = min(1.0, max(0.0, avg_switching_cost_usd / 10_000.0))
        s_br = min(1.0, max(0.0, brand_trust_score))
        s_ca = min(1.0, max(0.0, cost_advantage_percent))
        s_ip = min(1.0, max(0.0, ip_protection_score))
        s_cp = min(1.0, max(0.0, counter_positioning_score))

        composite = (0.25 * s_net + 0.20 * s_sw + 0.15 * s_ca + 0.15 * s_br + 0.10 * s_ip + 0.15 * s_cp)
        return float(round(composite, 4))


# =====================================================================
# 8. Failure Mode Analysis
# =====================================================================
class FailureMode(str, Enum):
    SOLVING_WRONG_PROBLEM = "SOLVING_WRONG_PROBLEM"
    BUILDING_BEFORE_VALIDATING = "BUILDING_BEFORE_VALIDATING"
    WEAK_POSITIONING = "WEAK_POSITIONING"
    POOR_PRICING = "POOR_PRICING"
    DISTRIBUTION_FAILURE = "DISTRIBUTION_FAILURE"
    LACK_OF_PMF = "LACK_OF_PMF"
    ORGANIZATIONAL_BOTTLENECKS = "ORGANIZATIONAL_BOTTLENECKS"
    FOUNDER_BIAS = "FOUNDER_BIAS"
    PREMATURE_SCALING = "PREMATURE_SCALING"
    CAPITAL_MISALLOCATION = "CAPITAL_MISALLOCATION"


class FailureModeDetail(BaseModel):
    mode: FailureMode
    root_cause: str
    detection_signal: str
    correction_mechanism: str


class FailureModeMonitor(BaseModel):
    """Pattern-matches operating metrics against canonical failure modes to raise early warnings."""

    canonical_failures: Dict[FailureMode, FailureModeDetail] = Field(default_factory=dict)

    def initialize_canonical_failures(self) -> None:
        specs = [
            (FailureMode.SOLVING_WRONG_PROBLEM, "Skipped root-cause analysis; solved symptom", "Low engagement despite positive survey feedback", "Return to root-cause (5-Whys / JTBD interviews)"),
            (FailureMode.BUILDING_BEFORE_VALIDATING, "Founder conviction substituted for evidence", "High build velocity, flat demand signal", "Enforce validation gate before build resourcing"),
            (FailureMode.WEAK_POSITIONING, "No clear 'instead of X, use us because Y'", "High CAC, long sales cycles, feature objections", "Rebuild positioning around real alternative"),
            (FailureMode.POOR_PRICING, "Cost-plus instead of value-based pricing", "High conversion at low price, poor margin", "Re-anchor price to quantified customer value"),
            (FailureMode.DISTRIBUTION_FAILURE, "Great product, no repeatable channel", "High NPS, flat growth", "Systematically test channels against ICP behavior"),
            (FailureMode.LACK_OF_PMF, "Premature scaling of unproven loop", "Retention curve never flattens", "Stop scaling; return to cohort retention work"),
            (FailureMode.ORGANIZATIONAL_BOTTLENECKS, "Decision rights not delegated", "Rising decision latency, founder bottleneck", "Push decision rights down with clear frameworks"),
            (FailureMode.FOUNDER_BIAS, "Overconfidence, confirmation bias, sunk cost", "Ignoring disconfirming data, 'needs time' pattern", "Pre-committed kill criteria set before launch"),
            (FailureMode.PREMATURE_SCALING, "Confusing early demand spike with PMF", "CAC rising faster than LTV as spend scales", "Re-test unit economics at order of magnitude spend"),
            (FailureMode.CAPITAL_MISALLOCATION, "No opportunity-cost discipline", "Multiple underperforming bets funded simultaneously", "Rank all initiatives on expected-return quarterly")
        ]
        for fm, rc, ds, cm in specs:
            self.canonical_failures[fm] = FailureModeDetail(mode=fm, root_cause=rc, detection_signal=ds, correction_mechanism=cm)

    def scan_for_failure_modes(
        self,
        retention_flattens: bool,
        cac_usd: float,
        ltv_usd: float,
        decision_latency_days: float,
        spending_growth_rate: float,
        user_growth_rate: float
    ) -> List[FailureModeDetail]:
        """Scans metrics and returns detected failure modes with corrective mechanisms."""
        detected = []
        if not self.canonical_failures:
            self.initialize_canonical_failures()

        if not retention_flattens and spending_growth_rate > 0.3:
            detected.append(self.canonical_failures[FailureMode.LACK_OF_PMF])
        if cac_usd > 0 and ltv_usd / cac_usd < 2.0 and spending_growth_rate > user_growth_rate:
            detected.append(self.canonical_failures[FailureMode.PREMATURE_SCALING])
        if decision_latency_days > 14.0:
            detected.append(self.canonical_failures[FailureMode.ORGANIZATIONAL_BOTTLENECKS])

        return detected


# =====================================================================
# 10. System State Machine & Opportunity Decision Tree
# =====================================================================
class EOSState(str, Enum):
    SENSING = "SENSING"
    HYPOTHESIS = "HYPOTHESIS"
    CHEAP_TEST = "CHEAP_TEST"
    DISCARD = "DISCARD"
    VALIDATION = "VALIDATION"
    BUILD_GATE = "BUILD_GATE"
    MVP = "MVP"
    GTM_TEST = "GTM_TEST"
    KILL_OR_SCALE = "KILL_OR_SCALE"
    SCALE = "SCALE"
    OPERATE = "OPERATE"
    REINVENT = "REINVENT"


class EOSStateMachine(BaseModel):
    """System state machine governing venture development lifecycle transitions."""

    current_state: EOSState = EOSState.SENSING
    state_history: List[Tuple[EOSState, str]] = Field(default_factory=list)

    def transition_to(self, new_state: EOSState, reason: str) -> None:
        self.state_history.append((self.current_state, reason))
        logger.info(f"[EOSStateMachine] Transition: {self.current_state.value} -> {new_state.value} ({reason})")
        self.current_state = new_state


class EOSDecisionTree(BaseModel):
    """Decision Tree — 'Should We Pursue This Opportunity?' (§10.2)."""

    def evaluate_opportunity(
        self,
        is_structural_anomaly: bool,
        is_reversible: bool,
        high_confidence_multi_source: bool,
        cheap_test_available: bool,
        test_result_exceeds_threshold: bool,
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> Tuple[bool, str]:
        """Evaluates opportunity pursuit logic returning (should_pursue, reasoning)."""
        if not is_structural_anomaly:
            return False, "DISCARD: Anomaly is noise, not a structural shift."

        if not is_reversible:
            if not high_confidence_multi_source:
                return False, "DISCARD: High-stakes irreversible decision lacking multi-source confidence."

        if cheap_test_available:
            if not test_result_exceeds_threshold:
                return False, "DISCARD: Cheap test result failed pre-committed kill threshold."
        else:
            if not expected_value_positive:
                return False, "DISCARD: Expected value is not clearly positive."

        if not has_structural_advantage:
            return False, "DISCARD: No defensible structural advantage can be built."

        return True, "COMMIT: Resource opportunity - passes structural, risk, test, and moat filters."


# =====================================================================
# 10.3 AI Implementation Module Registry & Subsystem KPI Stack
# =====================================================================
class AIEOSModuleRegistry(BaseModel):
    """Registry mapping 10 AI implementation agents/modules to system architecture."""

    registered_modules: Dict[str, str] = Field(default_factory=lambda: {
        "Sensing Agent": "Continuously ingests market/tech/data signals, flags anomalies vs baseline",
        "Hypothesis Engine": "Converts anomalies into falsifiable claims with pre-committed kill criteria",
        "Validation Agent": "Runs cheap tests (search demand, landing pages) & scores economic viability",
        "GTM Simulator": "Models channel fit against segment/pricing/positioning combinations",
        "Growth-Stage Classifier": "Continuously scores venture against Idea->Leadership stage model",
        "Moat Analyzer": "Tracks competitive data to score durability of advantage type",
        "Failure-Mode Monitor": "Pattern-matches operating metrics against failure-mode table",
        "Capital Allocator": "Ranks initiatives on common expected-return basis enforcing opportunity cost",
        "Reinvention Trigger": "Runs Sensing Agent internally forcing periodic self-disruption reviews",
        "Governance/Safety Layer": "Enforces kill criteria, prevents runaway capital, requires human sign-off on Type-I"
    })


class SubsystemKPIStack(BaseModel):
    """Rolled up KPI stack across all system modules (§10.4)."""

    sensing_signal_to_noise_ratio: float = 0.85
    sensing_anomaly_lead_time_days: float = 14.0
    validation_cost_per_learning_usd: float = 250.0
    validation_false_positive_rate: float = 0.05
    product_activation_rate: float = 0.45
    product_retention_curve_slope: float = 0.01  # Near 0 indicates flattening
    gtm_cac_usd: float = 120.0
    gtm_cac_payback_months: float = 6.0
    financial_gross_margin: float = 0.80
    financial_burn_multiple: float = 1.2
    financial_runway_months: float = 18.0
    org_decision_latency_days: float = 2.0
    org_regretted_attrition_rate: float = 0.02
    strategic_relative_market_share: float = 0.35
    strategic_moat_durability_score: float = 0.78
    overall_loop_closure_time_days: float = 5.0
