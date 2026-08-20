"""
The Entrepreneurial Operating System (EOS): Executable First-Principles Reconstruction.

Operationalizes the First-Principles Reconstruction of How Elite Founders Sense,
Build, and Compound Enduring Companies.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


# =====================================================================
# 0 & 1. Timescales & Master Loop Primitives
# =====================================================================

class Timescale(str, Enum):
    FAST = "fast"      # days - weeks (experiments, sales calls, ad tests, hiring)
    MEDIUM = "medium"  # months - quarters (GTM iteration, pricing, org design, capital deployment)
    SLOW = "slow"      # years (positioning, moats, category creation, reinvention)


class RiskType(str, Enum):
    TYPE_I = "type_1"  # Irreversible, one-way door (high scrutiny)
    TYPE_II = "type_2" # Reversible, two-way door (fast, cheap test)


# =====================================================================
# 2. Internal Cognitive Loops
# =====================================================================

class Anomaly(BaseModel):
    id: str
    description: str
    is_structural_shift: bool
    observed_signal_strength: float = Field(ge=0.0, le=1.0)
    source: str


class Hypothesis(BaseModel):
    id: str
    anomaly_id: str
    claim: str
    falsifiable_condition: str
    kill_threshold_metric: str
    kill_threshold_value: float
    estimated_cost: float
    risk_type: RiskType
    is_falsified: Optional[bool] = None


class MentalModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    version: str = "1.0.0"
    parameters: Dict[str, float] = Field(default_factory=dict)
    structural_assumptions: List[str] = Field(default_factory=list)
    prediction_history: List[Dict[str, Any]] = Field(default_factory=list)

    def predict(self, input_signal: str) -> float:
        return self.parameters.get(input_signal, 0.5)

    def update_parameters(self, key: str, value: float) -> None:
        self.parameters[key] = value

    def update_structure(self, new_assumption: str) -> None:
        if new_assumption not in self.structural_assumptions:
            self.structural_assumptions.append(new_assumption)


class SignalPipeline(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    mental_model: MentalModel
    anomalies: List[Anomaly] = Field(default_factory=list)
    hypotheses: List[Hypothesis] = Field(default_factory=list)

    def filter_anomaly(self, anomaly: Anomaly) -> bool:
        """Structural shift filter (§2.1)."""
        self.anomalies.append(anomaly)
        return anomaly.is_structural_shift

    def form_hypothesis(
        self,
        anomaly_id: str,
        claim: str,
        falsifiable_condition: str,
        kill_threshold_metric: str,
        kill_threshold_value: float,
        estimated_cost: float,
        risk_type: RiskType
    ) -> Hypothesis:
        hyp = Hypothesis(
            id=f"hyp_{len(self.hypotheses)+1}",
            anomaly_id=anomaly_id,
            claim=claim,
            falsifiable_condition=falsifiable_condition,
            kill_threshold_metric=kill_threshold_metric,
            kill_threshold_value=kill_threshold_value,
            estimated_cost=estimated_cost,
            risk_type=risk_type,
        )
        self.hypotheses.append(hyp)
        return hyp

    def evaluate_test_result(self, hypothesis_id: str, measured_value: float) -> bool:
        """Returns True if hypothesis is strengthened, False if falsified."""
        for hyp in self.hypotheses:
            if hyp.id == hypothesis_id:
                if measured_value < hyp.kill_threshold_value:
                    hyp.is_falsified = True
                    return False
                else:
                    hyp.is_falsified = False
                    return True
        raise ValueError(f"Hypothesis {hypothesis_id} not found")


# =====================================================================
# 3. External Business Loops (13 Coupled Loops)
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


class BusinessLoop(BaseModel):
    name: BusinessLoopName
    inputs: List[str]
    outputs: List[str]
    feedback_signal: str
    core_kpis: List[str]
    dominant_failure_mode: str
    timescale: Timescale
    kpi_values: Dict[str, float] = Field(default_factory=dict)


class BusinessLoopRegistry(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    loops: Dict[BusinessLoopName, BusinessLoop] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.loops:
            self._initialize_canonical_loops()

    def _initialize_canonical_loops(self) -> None:
        canonical_defs = [
            (BusinessLoopName.PRODUCT, ["User behavior", "support tickets", "usage data"], ["Feature changes", "roadmap"], "Activation/retention deltas", ["Retention curve", "NPS", "feature adoption"], "Building for the loudest customer, not the representative one", Timescale.FAST),
            (BusinessLoopName.MARKETING, ["Positioning", "market data"], ["Awareness", "demand"], "CAC, traffic quality, message resonance", ["CAC", "brand recall", "conversion rate"], "Message-market mismatch; scaling spend before message works", Timescale.FAST),
            (BusinessLoopName.SALES, ["Qualified leads", "product"], ["Closed revenue", "customer feedback"], "Win/loss reasons", ["Win rate", "sales cycle length", "ACV"], "Selling to non-ICP to hit quota", Timescale.FAST),
            (BusinessLoopName.CUSTOMER_SUCCESS, ["Onboarding data", "usage"], ["Retention", "expansion"], "Churn reasons, health scores", ["NRR", "churn rate", "time-to-value"], "Success != support; reactive-only CS", Timescale.MEDIUM),
            (BusinessLoopName.BRAND, ["Product experience", "comms"], ["Trust", "pricing power"], "Sentiment, unaided recall", ["Share of voice", "price elasticity"], "Brand as decoration, not strategy", Timescale.SLOW),
            (BusinessLoopName.PRICING, ["Value delivered", "WTP data"], ["Revenue", "positioning signal"], "Conversion by price point, expansion rate", ["ARPU", "price realization", "elasticity"], "Cost-plus pricing instead of value-based", Timescale.MEDIUM),
            (BusinessLoopName.REFERRAL, ["Customer satisfaction", "incentive design"], ["New customer flow"], "Referral rate, K-factor", ["Viral coefficient", "referral CAC"], "Incentivizing referral volume over referral quality", Timescale.FAST),
            (BusinessLoopName.DATA, ["All loops data"], ["Decisions"], "Model accuracy vs. outcomes", ["Data latency", "decision cycle time"], "Vanity metrics; dashboards no one acts on", Timescale.FAST),
            (BusinessLoopName.FINANCIAL, ["Revenue", "costs", "capital"], ["Runway", "reinvestment capacity"], "Burn multiple, margin trend", ["Gross margin", "burn multiple", "runway"], "Growth at negative unit economics with no path to positive", Timescale.MEDIUM),
            (BusinessLoopName.HIRING, ["Org needs", "culture"], ["Capability", "capacity"], "90-day performance, regretted attrition", ["Time-to-fill", "quality of hire", "retention"], "Hiring for pedigree over role-fit; hiring ahead of proven need", Timescale.MEDIUM),
            (BusinessLoopName.CULTURE, ["Values-in-action", "incentives"], ["Behavior consistency at scale"], "Employee sentiment, decision speed", ["eNPS", "decision latency"], "Values-as-poster (stated but not incentivized)", Timescale.SLOW),
            (BusinessLoopName.INNOVATION, ["R&D", "market signals", "internal ideas"], ["New products/features/lines"], "Time-to-market, cannibalization rate", ["# experiments run", "hit rate", "time-to-signal"], "Innovation theater — activity without shipped bets", Timescale.MEDIUM),
            (BusinessLoopName.COMPETITIVE_INTELLIGENCE, ["Market/competitor data"], ["Strategic repositioning"], "Win/loss vs. named competitors", ["Relative share trend", "feature parity gap"], "Reacting to competitors instead of running own strategy", Timescale.MEDIUM),
        ]
        for name, inputs, outputs, feedback, kpis, fail_mode, timescale in canonical_defs:
            self.loops[name] = BusinessLoop(
                name=name,
                inputs=inputs,
                outputs=outputs,
                feedback_signal=feedback,
                core_kpis=kpis,
                dominant_failure_mode=fail_mode,
                timescale=timescale,
                kpi_values={k: 0.0 for k in kpis}
            )

    def get_loop(self, name: BusinessLoopName) -> BusinessLoop:
        return self.loops[name]

    def update_loop_kpi(self, name: BusinessLoopName, kpi: str, value: float) -> None:
        if name in self.loops:
            self.loops[name].kpi_values[kpi] = value


# =====================================================================
# 4. Customer Journey (15-Stage Lifecycle)
# =====================================================================

class CustomerJourneyStageName(str, Enum):
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


class CustomerJourneyStageData(BaseModel):
    stage: CustomerJourneyStageName
    founder_objective: str
    customer_psychology: str
    key_metric_name: str
    common_mistake: str
    optimization_lever: str
    current_metric_value: float = 0.0


class CustomerLifecycle(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    stages: Dict[CustomerJourneyStageName, CustomerJourneyStageData] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.stages:
            self._initialize_stages()

    def _initialize_stages(self) -> None:
        defs = [
            (CustomerJourneyStageName.AWARENESS, "Enter consideration set", "Pattern-matching against known categories", "Reach / unaided recall", "Generic category messaging", "Sharp category framing / naming a new category"),
            (CustomerJourneyStageName.INTEREST, "Earn attention", "Curiosity vs. skepticism", "CTR / engagement rate", "Feature-dumping", "Lead with the pain, not the product"),
            (CustomerJourneyStageName.CONSIDERATION, "Differentiate", "Comparing against status quo & alternatives", "Time-on-site / content depth", "Competing on features competitors also have", "Reframe the comparison axis"),
            (CustomerJourneyStageName.EVALUATION, "Reduce perceived risk", "Loss aversion dominates gain-seeking", "Trial starts / demo requests", "Ignoring risk-reduction", "Make failure cheap and reversible"),
            (CustomerJourneyStageName.PURCHASE, "Convert intent to commitment", "Decision fatigue, need for certainty", "Conversion rate", "Friction in checkout/contracting", "Remove steps, not add persuasion"),
            (CustomerJourneyStageName.ONBOARDING, "Deliver first value fast", "Anxiety about wasted decision", "Time-to-first-value", "Feature-tour instead of outcome-tour", "Anchor onboarding to specific job-to-be-done"),
            (CustomerJourneyStageName.ACTIVATION, "Cross the 'aha' threshold", "Forming initial habit loop", "Activation rate", "Defining activation as login, not value", "Instrument the true 'aha' moment via cohort analysis"),
            (CustomerJourneyStageName.ENGAGEMENT, "Build usage depth", "Reinforcement learning (reward loop)", "DAU/MAU / session depth", "Engagement metrics not correlated with retention", "Optimize for behavior predicting retention"),
            (CustomerJourneyStageName.HABIT_FORMATION, "Make usage automatic", "Cue-routine-reward loop", "Habit strength / frequency", "No external trigger cadence", "Build reliable internal + external triggers"),
            (CustomerJourneyStageName.RETENTION, "Prevent churn", "Switching cost perception, sunk value", "Retention curve / churn", "Measuring aggregate instead of cohort retention", "Cohort-level retention curves, flattening analysis"),
            (CustomerJourneyStageName.LOYALTY, "Deepen emotional/economic lock-in", "Identity alignment with brand", "Repeat purchase rate", "Assuming satisfaction = loyalty", "Build genuine switching costs"),
            (CustomerJourneyStageName.ADVOCACY, "Convert satisfaction to voice", "Social proof-seeking, reciprocity", "NPS / UGC volume", "Asking before value is proven", "Ask at peak-value moments"),
            (CustomerJourneyStageName.REFERRAL, "Convert advocacy to acquisition", "Trust transfer from peer to peer", "Viral coefficient (K)", "Generic referral programs", "Incentive aligned with genuine value"),
            (CustomerJourneyStageName.EXPANSION, "Grow account value", "Anchoring to current spend", "Net revenue retention (NRR)", "Under-selling adjacent value", "Usage-based expansion triggers"),
            (CustomerJourneyStageName.REPURCHASE, "Sustain lifetime value", "Habitual trust, low re-evaluation cost", "LTV / repurchase rate", "Treating repurchase as passive", "Proactive lifecycle marketing tied to usage signals"),
        ]
        for stage, obj, psych, metric, mistake, lever in defs:
            self.stages[stage] = CustomerJourneyStageData(
                stage=stage,
                founder_objective=obj,
                customer_psychology=psych,
                key_metric_name=metric,
                common_mistake=mistake,
                optimization_lever=lever,
            )

    def set_metric(self, stage: CustomerJourneyStageName, val: float) -> None:
        if stage in self.stages:
            self.stages[stage].current_metric_value = val


# =====================================================================
# 5. Go-to-Market System
# =====================================================================

class ChannelType(str, Enum):
    PLG = "Product-Led Growth"
    SLG = "Sales-Led Growth"
    CLG = "Community-Led Growth"
    CONTENT = "Content Strategy"
    PAID = "Paid Acquisition"
    ORGANIC = "Organic Growth"
    PARTNER = "Partnerships"


class GTMSystem(BaseModel):
    positioning: str
    messaging: str
    target_segment: str
    price_point: float
    complexity_score: float = Field(ge=0.0, le=1.0) # 0 = low complexity, 1 = high enterprise

    def recommend_primary_channel(self) -> ChannelType:
        if self.complexity_score > 0.7 or self.price_point >= 50000:
            return ChannelType.SLG
        elif self.complexity_score < 0.3 and self.price_point < 1000:
            return ChannelType.PLG
        else:
            return ChannelType.CONTENT


# =====================================================================
# 6. Company Growth System (9 Stages)
# =====================================================================

class GrowthStageEnum(str, Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "Product-Market Fit"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    LEADERSHIP = "Market Leadership"


class CompanyGrowthStage(BaseModel):
    stage: GrowthStageEnum
    primary_objective: str
    org_structure: str
    decision_making_style: str
    capital_allocation: str
    key_risk: str
    core_metric: str
    binding_constraint: str


class GrowthClassifier(BaseModel):
    @staticmethod
    def classify_stage(
        paying_customers: int,
        retention_curve_flattened: bool,
        annual_growth_rate: float,
        third_party_developers: int,
        market_share: float
    ) -> GrowthStageEnum:
        if market_share >= 0.4:
            return GrowthStageEnum.LEADERSHIP
        if third_party_developers >= 500:
            return GrowthStageEnum.ECOSYSTEM
        if third_party_developers >= 50:
            return GrowthStageEnum.PLATFORM
        if annual_growth_rate >= 1.0 and retention_curve_flattened:
            return GrowthStageEnum.GROWTH
        if retention_curve_flattened:
            return GrowthStageEnum.PMF
        if paying_customers >= 10:
            return GrowthStageEnum.STARTUP
        if paying_customers > 0:
            return GrowthStageEnum.VALIDATION
        return GrowthStageEnum.IDEA


# =====================================================================
# 7. Strategic Thinking & Competitive Moats
# =====================================================================

class MoatType(str, Enum):
    NETWORK_EFFECTS = "Network Effects"
    SWITCHING_COSTS = "Switching Costs"
    ECONOMIES_OF_SCALE = "Economies of Scale"
    BRAND = "Brand"
    REGULATORY_IP = "Regulatory / IP"
    COUNTER_POSITIONING = "Counter-Positioning"


class StrategicMoatAnalyzer(BaseModel):
    active_moats: Dict[MoatType, float] = Field(default_factory=dict) # 0.0 to 1.0 score

    def evaluate_durability(self) -> float:
        if not self.active_moats:
            return 0.0
        return sum(self.active_moats.values()) / len(self.active_moats)


# =====================================================================
# 8. Failure Mode Analysis (10 Failure Modes)
# =====================================================================

class FailureModeEnum(str, Enum):
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


class FailureModeAlert(BaseModel):
    failure_mode: FailureModeEnum
    root_cause: str
    detection_signal: str
    correction_mechanism: str
    severity: float = Field(ge=0.0, le=1.0)


class FailureModeMonitor(BaseModel):
    alerts: List[FailureModeAlert] = Field(default_factory=list)

    def scan_metrics(
        self,
        survey_vs_usage_gap: float = 0.0,
        build_velocity_high_demand_flat: bool = False,
        cac_payback_months: float = 12.0,
        retention_flattened: bool = True,
        decision_latency_days: float = 1.0,
        spend_scaled_before_pmf: bool = False
    ) -> List[FailureModeAlert]:
        detected = []
        if survey_vs_usage_gap > 0.5:
            detected.append(FailureModeAlert(
                failure_mode=FailureModeEnum.SOLVING_WRONG_PROBLEM,
                root_cause="Skipped root-cause analysis; solved a symptom",
                detection_signal="Low engagement despite positive survey feedback",
                correction_mechanism="Return to root-cause (5-Whys / Jobs-to-be-Done interviews)",
                severity=0.8
            ))
        if build_velocity_high_demand_flat:
            detected.append(FailureModeAlert(
                failure_mode=FailureModeEnum.BUILDING_BEFORE_VALIDATING,
                root_cause="Founder conviction substituted for evidence",
                detection_signal="High build velocity, flat demand signal",
                correction_mechanism="Enforce a validation gate before build resourcing",
                severity=0.9
            ))
        if spend_scaled_before_pmf or (not retention_flattened and cac_payback_months > 24):
            detected.append(FailureModeAlert(
                failure_mode=FailureModeEnum.SCALING_PREMATURELY,
                root_cause="Confusing early demand spike with durable PMF",
                detection_signal="CAC rising faster than LTV as spend scales",
                correction_mechanism="Re-test unit economics at each order-of-magnitude of spend",
                severity=0.95
            ))
        if decision_latency_days > 14:
            detected.append(FailureModeAlert(
                failure_mode=FailureModeEnum.ORGANIZATIONAL_BOTTLENECK,
                root_cause="Decision rights not delegated as company scales",
                detection_signal="Rising decision latency, founder as single point of failure",
                correction_mechanism="Push decision rights down with clear frameworks",
                severity=0.7
            ))
        self.alerts = detected
        return detected


# =====================================================================
# 10. Integrated AI-Driven System State Machine & Decision Tree
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
    current_state: EOSState = EOSState.SENSING
    state_history: List[EOSState] = Field(default_factory=lambda: [EOSState.SENSING])

    def transition_to(self, target_state: EOSState) -> EOSState:
        self.current_state = target_state
        self.state_history.append(target_state)
        return target_state


class OpportunityDecisionTree(BaseModel):
    """
    Implements §10.2 Decision Tree: "Should We Pursue This Opportunity?"
    """
    @staticmethod
    def evaluate(
        is_structural_anomaly: bool,
        is_reversible_decision: bool,
        has_high_confidence_multi_source_signal: bool,
        cheap_test_available: bool,
        cheap_test_exceeds_kill_threshold: bool,
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> Tuple[bool, str]:
        # Q1: Structural anomaly or noise?
        if not is_structural_anomaly:
            return False, "Discard: Signal is noise, not a structural anomaly."

        # Q2: Reversible decision?
        if not is_reversible_decision:
            # Q2a: High confidence signal from multiple sources?
            if not has_high_confidence_multi_source_signal:
                return False, "Discard: Irreversible decision lacking high-confidence multi-source signal."

        # Q3: Cheap test available?
        if cheap_test_available:
            if not cheap_test_exceeds_kill_threshold:
                return False, "Discard: Cheap test result failed pre-committed kill threshold."
        else:
            if not expected_value_positive:
                return False, "Discard: No cheap test available and expected value is not positive."

        # Q5: Structural advantage?
        if not has_structural_advantage:
            return False, "Discard: No clear structural advantage or moats."

        return True, "Commit resources: Opportunity passes all first-principles decision gates."


# =====================================================================
# 10.3 AI Modules Architecture
# =====================================================================

class SensingAgent(BaseModel):
    signal_pipeline: SignalPipeline

    def scan_environment(self, anomalies: List[Anomaly]) -> List[Anomaly]:
        structural = []
        for a in anomalies:
            if self.signal_pipeline.filter_anomaly(a):
                structural.append(a)
        return structural


class HypothesisEngine(BaseModel):
    signal_pipeline: SignalPipeline

    def convert_anomaly_to_hypothesis(
        self,
        anomaly: Anomaly,
        claim: str,
        falsifiable_condition: str,
        kill_threshold_metric: str,
        kill_threshold_value: float,
        estimated_cost: float,
        risk_type: RiskType
    ) -> Hypothesis:
        return self.signal_pipeline.form_hypothesis(
            anomaly_id=anomaly.id,
            claim=claim,
            falsifiable_condition=falsifiable_condition,
            kill_threshold_metric=kill_threshold_metric,
            kill_threshold_value=kill_threshold_value,
            estimated_cost=estimated_cost,
            risk_type=risk_type,
        )


class ValidationAgent(BaseModel):
    signal_pipeline: SignalPipeline

    def run_cheap_test(self, hypothesis_id: str, metric_result: float) -> bool:
        return self.signal_pipeline.evaluate_test_result(hypothesis_id, metric_result)


class GTMSimulator(BaseModel):
    def simulate_gtm(self, gtm: GTMSystem) -> Dict[str, Any]:
        recommended_channel = gtm.recommend_primary_channel()
        estimated_cac = 100.0 if recommended_channel == ChannelType.PLG else 5000.0
        return {
            "channel": recommended_channel,
            "estimated_cac": estimated_cac,
            "channel_fit_score": 0.85 if recommended_channel == ChannelType.PLG and gtm.price_point < 1000 else 0.65
        }


class GrowthStageClassifier(BaseModel):
    def evaluate_venture(
        self,
        paying_customers: int,
        retention_curve_flattened: bool,
        annual_growth_rate: float,
        third_party_developers: int,
        market_share: float
    ) -> GrowthStageEnum:
        return GrowthClassifier.classify_stage(
            paying_customers,
            retention_curve_flattened,
            annual_growth_rate,
            third_party_developers,
            market_share
        )


class MoatAnalyzer(BaseModel):
    analyzer: StrategicMoatAnalyzer = Field(default_factory=StrategicMoatAnalyzer)

    def evaluate(self) -> float:
        return self.analyzer.evaluate_durability()


class FailureModeMonitorAgent(BaseModel):
    monitor: FailureModeMonitor = Field(default_factory=FailureModeMonitor)

    def scan(self, **kwargs: Any) -> List[FailureModeAlert]:
        return self.monitor.scan_metrics(**kwargs)


class CapitalAllocator(BaseModel):
    def rank_initiatives(self, initiatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ranks initiatives by expected return and capital efficiency."""
        return sorted(initiatives, key=lambda x: x.get("expected_return", 0.0) / max(x.get("cost", 1.0), 1.0), reverse=True)


class ReinventionTrigger(BaseModel):
    def evaluate_self_disruption(self, market_share: float, innovation_velocity: float) -> bool:
        """Triggers reinvention if market leadership is high but innovation velocity drops."""
        return market_share > 0.4 and innovation_velocity < 0.3


class GovernanceSafetyLayer(BaseModel):
    def require_approval(self, risk_type: RiskType, budget: float) -> bool:
        """Enforces human sign-off on Type-I decisions or large budgets."""
        if risk_type == RiskType.TYPE_I or budget >= 100000.0:
            return True # Requires approval
        return False # Auto-approved


# =====================================================================
# 10.4 KPI Stack
# =====================================================================

class KPIStack(BaseModel):
    signal_to_noise_ratio: float = 0.0
    cost_per_validated_learning: float = 0.0
    activation_rate: float = 0.0
    retention_curve_slope: float = 0.0
    cac: float = 0.0
    cac_payback_months: float = 0.0
    gross_margin: float = 0.0
    burn_multiple: float = 0.0
    runway_months: float = 0.0
    decision_latency_days: float = 0.0
    moat_durability_score: float = 0.0
    overall_loop_closure_time_days: float = 0.0
