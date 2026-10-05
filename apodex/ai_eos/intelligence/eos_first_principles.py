"""
First-Principles Entrepreneurial Operating System (EOS) Cognitive Engine

An executable implementation of how elite founders sense, build, and compound
enduring companies according to the 11-section EOS specification.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class DecisionType(str, Enum):
    TYPE_I = "TYPE_I"   # One-way door, irreversible, slow high-scrutiny deliberation
    TYPE_II = "TYPE_II" # Two-way door, reversible, fast cheap testing


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


class CustomerLifecycleStage(str, Enum):
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


class AnomalySignal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    signal_id: str
    source: str
    description: str
    is_structural: bool
    confidence: float = Field(ge=0.0, le=1.0)
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EOSHypothesis(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    hypothesis_id: str
    signal_id: str
    claim: str
    kill_threshold: float = Field(ge=0.0, le=1.0, description="Minimum metric performance required to keep bet alive")
    decision_type: DecisionType = DecisionType.TYPE_II
    belief_score: float = Field(default=0.5, ge=0.0, le=1.0)
    status: str = "active" # active, falsified, strengthened, scaled, discarded
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CheapTestResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    test_id: str
    hypothesis_id: str
    cost: float
    metric_measured: str
    metric_value: float
    passed_kill_threshold: bool
    belief_delta: float
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BusinessLoopState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    loop_type: BusinessLoopType
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    feedback_signal: str = ""
    kpi_values: Dict[str, float] = Field(default_factory=dict)
    failure_mode_detected: Optional[str] = None


class CustomerJourneyMetrics(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    stage: CustomerLifecycleStage
    conversion_rate: float
    dropoff_rate: float
    key_metric_value: float
    optimization_lever: str


class GTMSimulationConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    positioning: str
    pricing_model: str # e.g. usage_based, flat_rate, enterprise
    price_point: float
    primary_channel: str # PLG, SLG, Content, Community, Paid
    target_segment: str


class GTMSimulationResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    projected_cac: float
    projected_ltv: float
    projected_payback_months: float
    channel_fit_score: float = Field(ge=0.0, le=1.0)
    recommended_motion: str


class GrowthStageAssessment(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    current_stage: CompanyStage
    primary_objective: str
    org_structure: str
    decision_making_mode: str
    capital_allocation_strategy: str
    key_risk: str
    binding_constraint: str
    premature_scaling_risk: float = Field(ge=0.0, le=1.0)


class FailureModeAlert(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    failure_mode: str
    root_cause: str
    detection_signal: str
    correction_mechanism: str
    severity: float = Field(ge=0.0, le=1.0)


class DecisionTreeResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    pursue: bool
    rationale: str
    decision_path: List[str]


class EOSEngineFirstPrinciples:
    """
    Core engine encapsulating the 11-section Entrepreneurial Operating System.
    Orchestrates sensing, hypothesis creation, cheap testing, loop monitoring,
    customer lifecycle optimization, GTM modeling, growth stage assessment,
    and failure mode diagnostics.
    """

    def __init__(self):
        self.anomalies: Dict[str, AnomalySignal] = {}
        self.hypotheses: Dict[str, EOSHypothesis] = {}
        self.test_results: List[CheapTestResult] = []
        self.business_loops: Dict[BusinessLoopType, BusinessLoopState] = {}
        self._initialize_business_loops()

    def _initialize_business_loops(self):
        for loop_type in BusinessLoopType:
            self.business_loops[loop_type] = BusinessLoopState(
                loop_type=loop_type,
                feedback_signal="nominal",
                kpi_values={"health_score": 1.0}
            )

    # --- §1 & §2 Sensing & Internal Cognitive Loops ---
    def sense_anomaly(self, signal_id: str, source: str, description: str, is_structural: bool, confidence: float) -> AnomalySignal:
        signal = AnomalySignal(
            signal_id=signal_id,
            source=source,
            description=description,
            is_structural=is_structural,
            confidence=confidence
        )
        self.anomalies[signal_id] = signal
        return signal

    def form_hypothesis(self, hypothesis_id: str, signal_id: str, claim: str, kill_threshold: float, decision_type: DecisionType = DecisionType.TYPE_II) -> Optional[EOSHypothesis]:
        signal = self.anomalies.get(signal_id)
        if not signal:
            return None

        # Section 2.1 Filter: Is this a symptom of a structural shift?
        if not signal.is_structural:
            return None # Discard noise

        hyp = EOSHypothesis(
            hypothesis_id=hypothesis_id,
            signal_id=signal_id,
            claim=claim,
            kill_threshold=kill_threshold,
            decision_type=decision_type,
            belief_score=signal.confidence
        )
        self.hypotheses[hypothesis_id] = hyp
        return hyp

    def run_cheap_test(self, test_id: str, hypothesis_id: str, cost: float, metric_measured: str, metric_value: float) -> Optional[CheapTestResult]:
        hyp = self.hypotheses.get(hypothesis_id)
        if not hyp:
            return None

        passed = metric_value >= hyp.kill_threshold
        belief_delta = 0.2 if passed else -0.3

        # Bayesian belief updating
        hyp.belief_score = max(0.0, min(1.0, hyp.belief_score + belief_delta))
        if hyp.belief_score < 0.2 or not passed:
            hyp.status = "falsified"
        else:
            hyp.status = "strengthened"

        result = CheapTestResult(
            test_id=test_id,
            hypothesis_id=hypothesis_id,
            cost=cost,
            metric_measured=metric_measured,
            metric_value=metric_value,
            passed_kill_threshold=passed,
            belief_delta=belief_delta
        )
        self.test_results.append(result)
        return result

    # --- §3 External Business Loops ---
    def update_business_loop(self, loop_type: BusinessLoopType, inputs: Dict[str, Any], outputs: Dict[str, Any], kpis: Dict[str, float]) -> BusinessLoopState:
        state = self.business_loops.get(loop_type)
        if not state:
            state = BusinessLoopState(loop_type=loop_type)
            self.business_loops[loop_type] = state

        state.inputs.update(inputs)
        state.outputs.update(outputs)
        state.kpi_values.update(kpis)

        # Check specific failure modes
        if loop_type == BusinessLoopType.PRODUCT and kpis.get("retention_slope", 0) < 0:
            state.failure_mode_detected = "Solving the wrong problem / Building for loud customers"
        elif loop_type == BusinessLoopType.FINANCIAL and kpis.get("burn_multiple", 0) > 3.0:
            state.failure_mode_detected = "Scaling prematurely / Poor pricing"
        elif loop_type == BusinessLoopType.MARKETING and kpis.get("cac", 0) > kpis.get("ltv", 0) * 0.5:
            state.failure_mode_detected = "Weak positioning / Distribution failure"
        else:
            state.failure_mode_detected = None

        return state

    # --- §4 Customer Journey ---
    def analyze_customer_journey(self, stage: CustomerLifecycleStage, conversion_rate: float, dropoff_rate: float, key_metric: float) -> CustomerJourneyMetrics:
        levers = {
            CustomerLifecycleStage.AWARENESS: "Sharp category framing / naming new category",
            CustomerLifecycleStage.INTEREST: "Lead with pain, not product",
            CustomerLifecycleStage.CONSIDERATION: "Reframe comparison axis",
            CustomerLifecycleStage.EVALUATION: "Make failure cheap and reversible",
            CustomerLifecycleStage.PURCHASE: "Remove friction steps",
            CustomerLifecycleStage.ONBOARDING: "Anchor to customer specific job-to-be-done",
            CustomerLifecycleStage.ACTIVATION: "Instrument true 'aha' moment via cohort analysis",
            CustomerLifecycleStage.ENGAGEMENT: "Optimize behavior predicting retention",
            CustomerLifecycleStage.HABIT_FORMATION: "Build reliable internal + external triggers",
            CustomerLifecycleStage.RETENTION: "Cohort-level retention curve flattening analysis",
            CustomerLifecycleStage.LOYALTY: "Build genuine switching costs (data, workflow, community)",
            CustomerLifecycleStage.ADVOCACY: "Ask at peak-value moments",
            CustomerLifecycleStage.REFERRAL: "Incentive aligned with genuine value",
            CustomerLifecycleStage.EXPANSION: "Usage-based expansion triggers",
            CustomerLifecycleStage.REPURCHASE: "Proactive lifecycle marketing tied to usage signals",
        }
        return CustomerJourneyMetrics(
            stage=stage,
            conversion_rate=conversion_rate,
            dropoff_rate=dropoff_rate,
            key_metric_value=key_metric,
            optimization_lever=levers.get(stage, "General funnel optimization")
        )

    # --- §5 Go-to-Market System ---
    def simulate_gtm(self, config: GTMSimulationConfig) -> GTMSimulationResult:
        # System logic: price and positioning drive motion
        if config.price_point > 10000:
            recommended = "Sales-Led Growth (SLG)"
            cac = 5000.0
            ltv = config.price_point * 3.5
            fit = 0.9 if config.primary_channel in ["SLG", "Enterprise"] else 0.4
        elif config.pricing_model == "usage_based" or config.price_point < 500:
            recommended = "Product-Led Growth (PLG)"
            cac = 150.0
            ltv = config.price_point * 24.0
            fit = 0.95 if config.primary_channel in ["PLG", "Content", "Organic"] else 0.5
        else:
            recommended = "Hybrid Motion"
            cac = 1200.0
            ltv = config.price_point * 12.0
            fit = 0.75

        payback = (cac / (ltv / 36.0)) if ltv > 0 else 999.0
        return GTMSimulationResult(
            projected_cac=cac,
            projected_ltv=ltv,
            projected_payback_months=round(payback, 1),
            channel_fit_score=fit,
            recommended_motion=recommended
        )

    # --- §6 Company Growth System ---
    def assess_growth_stage(self, stage: CompanyStage, metrics: Dict[str, float]) -> GrowthStageAssessment:
        stage_map = {
            CompanyStage.IDEA: ("Falsify or strengthen hypothesis", "Founder(s) only", "Founder intuition, fast", "Near-zero, sweat equity", "Solving non-problem", "Founder time"),
            CompanyStage.VALIDATION: ("Prove willingness to pay", "First 1-3 hires", "Founder-centric", "Pre-seed/seed", "False positive validation", "Signal quality"),
            CompanyStage.STARTUP: ("Build repeatable acquisition", "Functional roles emerge", "Founder + small team", "Seed/Series A", "Premature scaling before PMF", "Cash runway"),
            CompanyStage.PMF: ("Reach retention/growth threshold", "First managers", "Data overriding intuition", "Growth capital", "Mistaking early traction for PMF", "Team bandwidth"),
            CompanyStage.GROWTH: ("Scale what works", "Middle management layer", "Process + data-driven", "Series B/C", "Scaling broken funnel", "Hiring velocity"),
            CompanyStage.SCALE: ("Institutionalize repeatability", "Departments & specialized functions", "Delegated, framework-driven", "Efficient growth capital", "Culture dilution, bureaucracy creep", "Org coordination cost"),
            CompanyStage.PLATFORM: ("Enable others to build on you", "Platform/ecosystem teams", "Governance structures, APIs-as-product", "Infrastructure investment", "Platform without ecosystem demand", "Ecosystem trust"),
            CompanyStage.ECOSYSTEM: ("Orchestrate multi-sided network", "Ecosystem management, BD at scale", "Distributed decision rights", "Strategic/M&A capital", "Ecosystem fragmentation", "Governance credibility"),
            CompanyStage.MARKET_LEADERSHIP: ("Defend and extend category", "Full corporate structure", "Board-level strategic governance", "Diversified, defensive + offensive", "Complacency, disruption from below", "Innovation velocity vs. incumbency drag"),
        }

        info = stage_map.get(stage, ("Scale business", "Org", "Mode", "Capital", "Risk", "Constraint"))

        # Calculate premature scaling risk
        premature_risk = 0.0
        if stage in [CompanyStage.STARTUP, CompanyStage.GROWTH]:
            retention_flattened = metrics.get("retention_flattened", 0.0)
            cac_ltv_ratio = metrics.get("cac_ltv_ratio", 0.5)
            if retention_flattened < 0.5 or cac_ltv_ratio > 0.33:
                premature_risk = 0.8

        return GrowthStageAssessment(
            current_stage=stage,
            primary_objective=info[0],
            org_structure=info[1],
            decision_making_mode=info[2],
            capital_allocation_strategy=info[3],
            key_risk=info[4],
            binding_constraint=info[5],
            premature_scaling_risk=premature_risk
        )

    # --- §8 Failure Mode Analysis ---
    def diagnose_failure_modes(self) -> List[FailureModeAlert]:
        alerts = []
        failure_table = [
            ("Solving the wrong problem", "Skipped root-cause analysis", "Low engagement despite positive surveys", "Return to root cause (5-Whys / JTBD)"),
            ("Building before validating", "Founder conviction substituted for evidence", "High build velocity, flat demand", "Enforce validation gate before build"),
            ("Weak positioning", "No clear 'instead of X, use us because Y'", "High CAC, long sales cycles", "Rebuild positioning around real customer alternatives"),
            ("Poor pricing", "Cost-plus instead of value-based", "High conversion at low price, poor margin", "Re-anchor price to quantified value"),
            ("Distribution failure", "Great product, no repeatable channel", "High NPS, flat growth", "Systematically test channels against ICP behavior"),
            ("Lack of product-market fit", "Premature scaling of unproven loop", "Retention curve never flattens", "Stop scaling; return to cohort-level retention work"),
            ("Organizational bottlenecks", "Decision rights not delegated as company scales", "Rising decision latency, founder SPOF", "Push decision rights down with clear frameworks"),
            ("Founder bias", "Overconfidence, confirmation bias, sunk cost", "Ignoring disconfirming data", "Pre-committed kill criteria set before launch"),
            ("Scaling prematurely", "Confusing early demand spike with durable PMF", "CAC rising faster than LTV", "Re-test unit economics at each order-of-magnitude"),
            ("Capital misallocation", "No opportunity-cost discipline in budgeting", "Multiple underperforming bets funded", "Rank all initiatives on common expected-return basis"),
        ]

        # Evaluate against active business loop states
        for loop_type, state in self.business_loops.items():
            if state.failure_mode_detected:
                for mode, root, sig, corr in failure_table:
                    # Match mode keywords against state's detected failure mode string
                    mode_words = [w.lower() for w in mode.split()]
                    det_lower = state.failure_mode_detected.lower()
                    if any(w in det_lower for w in mode_words if len(w) > 3):
                        alerts.append(FailureModeAlert(
                            failure_mode=mode,
                            root_cause=root,
                            detection_signal=sig,
                            correction_mechanism=corr,
                            severity=0.85
                        ))
        return alerts

    # --- §10.2 Decision Tree ---
    def evaluate_opportunity_decision_tree(
        self,
        is_structural_anomaly: bool,
        is_reversible_decision: bool,
        high_confidence_multi_source: bool,
        cheap_test_available: bool,
        test_result_exceeds_kill_threshold: Optional[bool],
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> DecisionTreeResult:
        path = []

        # Q1: Structural anomaly or just noise?
        path.append("Q1: Structural anomaly vs noise")
        if not is_structural_anomaly:
            return DecisionTreeResult(pursue=False, rationale="Discarded: Anomaly is noise, not structural shift.", decision_path=path)

        # Q2: Reversible decision?
        path.append("Q2: Reversible decision check")
        if not is_reversible_decision:
            path.append("Q2a: High-confidence multi-source signal check (Type I Decision)")
            if not high_confidence_multi_source:
                return DecisionTreeResult(pursue=False, rationale="Discarded: Irreversible (Type I) decision lacks multi-source high-confidence signal.", decision_path=path)
        else:
            path.append("Type II Decision (Reversible / Two-way door)")

        # Q3: Cheap test available?
        path.append("Q3: Cheap test availability check")
        if cheap_test_available:
            path.append("Q4: Run cheap test")
            if test_result_exceeds_kill_threshold is False:
                return DecisionTreeResult(pursue=False, rationale="Discarded: Cheap test failed to cross kill threshold.", decision_path=path)
        else:
            path.append("Q4b: Expected value check")
            if not expected_value_positive:
                return DecisionTreeResult(pursue=False, rationale="Discarded: Expected value is not positive.", decision_path=path)

        # Q5: Do we have or can we build a structural advantage?
        path.append("Q5: Structural advantage / Moat check")
        if not has_structural_advantage:
            return DecisionTreeResult(pursue=False, rationale="Discarded: Lacks structural competitive advantage or moat.", decision_path=path)

        path.append("GO: Commit resources")
        return DecisionTreeResult(
            pursue=True,
            rationale="Approved: Opportunity exhibits structural anomaly, passed validation tests, and builds structural advantage.",
            decision_path=path
        )

    # --- Cross-Layer Research OS Ingestion ---
    def ingest_validated_research(self, hypothesis_id: str, claim: str, kill_threshold: float = 0.6) -> EOSHypothesis:
        """
        Ingests validated research hypotheses directly from Layer 1 Research OS.
        """
        signal_id = f"research_sig_{hypothesis_id}"
        self.sense_anomaly(
            signal_id=signal_id,
            source="Layer1_ResearchOS",
            description=claim,
            is_structural=True,
            confidence=0.85
        )
        hyp = self.form_hypothesis(
            hypothesis_id=hypothesis_id,
            signal_id=signal_id,
            claim=claim,
            kill_threshold=kill_threshold,
            decision_type=DecisionType.TYPE_II
        )
        return hyp

    def get_active_hypotheses(self) -> List[EOSHypothesis]:
        return [h for h in self.hypotheses.values() if h.status in ["active", "strengthened"]]
