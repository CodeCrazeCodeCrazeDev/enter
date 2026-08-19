"""
First-Principles Entrepreneurial Operating System (EOS) Cognitive Engine.

This module operationalizes the first-principles reconstruction of EOS,
modeling fast, medium, and slow feedback loops, signal-to-idea filtering,
13 coupled operational business loops, 15-stage customer journey lifecycle,
9-stage company growth classification, opportunity decision tree evaluation,
and operational failure mode monitoring.
"""

import math
from typing import Dict, List, Any, Optional, Tuple, Set
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


# ==========================================
# 0. Timescales & Loop Management
# ==========================================

class Timescale(str, Enum):
    FAST = "FAST"      # Days to weeks: micro-experiments, ad tests, sales calls
    MEDIUM = "MEDIUM"  # Months to quarters: GTM iteration, pricing, org design
    SLOW = "SLOW"      # Years: positioning, moats, category creation, reinvention


class FeedbackLoop(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    timescale: Timescale
    input_signals: List[str]
    output_artifacts: List[str]
    velocity_days: float
    signal_fidelity: float = Field(ge=0.0, le=1.0, default=0.8)
    compounding_yield: float = Field(default=1.0)
    is_active: bool = True
    iterations_completed: int = 0

    def execute_iteration(self, signal_quality: float) -> Dict[str, Any]:
        """Runs a loop iteration, updating metrics and compounding yield."""
        self.iterations_completed += 1
        effective_gain = signal_quality * self.signal_fidelity
        self.compounding_yield *= (1.0 + 0.05 * effective_gain)
        return {
            "loop": self.name,
            "timescale": self.timescale.value,
            "iterations": self.iterations_completed,
            "compounding_yield": self.compounding_yield,
            "effective_gain": effective_gain,
        }


class TimescaleLoopManager(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    loops: Dict[str, FeedbackLoop] = Field(default_factory=dict)

    def register_loop(self, loop: FeedbackLoop) -> None:
        self.loops[loop.name] = loop

    def get_loops_by_timescale(self, timescale: Timescale) -> List[FeedbackLoop]:
        return [l for l in self.loops.values() if l.timescale == timescale]

    def step_all(self, global_signals: Dict[str, float]) -> Dict[str, Any]:
        results = {}
        for name, loop in self.loops.items():
            if loop.is_active:
                quality = global_signals.get(name, 0.7)
                results[name] = loop.execute_iteration(quality)
        return results


# ==========================================
# 1. Cognitive Signal-to-Idea Pipeline
# ==========================================

class RiskType(str, Enum):
    TYPE_I = "TYPE_I"   # Irreversible / One-way door
    TYPE_II = "TYPE_II" # Reversible / Two-way door


class SignalRecord(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    signal_id: str
    description: str
    is_structural_anomaly: bool
    observed_magnitude: float
    baseline_expectation: float
    source: str


class FalsifiableHypothesis(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    hypothesis_id: str
    claim: str
    falsification_metric: str
    kill_threshold: float
    prior_confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    current_confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    status: str = "PROPOSED" # PROPOSED, TESTING, CONFIRMED, FALSIFIED


class SignalToIdeaPipeline(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    min_anomaly_threshold: float = 0.2

    def evaluate_signal(self, signal: SignalRecord) -> Optional[FalsifiableHypothesis]:
        """Filters weak signals. If structural anomaly exceeds threshold, forms falsifiable hypothesis."""
        anomaly_delta = abs(signal.observed_magnitude - signal.baseline_expectation)
        if not signal.is_structural_anomaly or anomaly_delta < self.min_anomaly_threshold:
            return None

        hypothesis_claim = f"Structural shift in {signal.source}: {signal.description}"
        return FalsifiableHypothesis(
            hypothesis_id=f"HYP_{signal.signal_id}",
            claim=hypothesis_claim,
            falsification_metric=f"metric_delta_{signal.source}",
            kill_threshold=self.min_anomaly_threshold * 0.5,
            prior_confidence=min(0.9, 0.3 + anomaly_delta * 0.5),
            current_confidence=min(0.9, 0.3 + anomaly_delta * 0.5),
        )

    def classify_risk(self, decision_context: Dict[str, Any]) -> RiskType:
        """Classifies decision as Type I (irreversible) or Type II (reversible)."""
        capital_commitment = decision_context.get("capital_cents", 0)
        reversibility_score = decision_context.get("reversibility_score", 1.0) # 1.0 = fully reversible
        has_regulatory_lockin = decision_context.get("regulatory_lockin", False)

        if capital_commitment > 500_000_00 or reversibility_score < 0.3 or has_regulatory_lockin:
            return RiskType.TYPE_I
        return RiskType.TYPE_II

    def run_real_option_test(
        self,
        hypothesis: FalsifiableHypothesis,
        test_cost_cents: int,
        observed_metric_value: float,
    ) -> Tuple[FalsifiableHypothesis, bool]:
        """Runs a cheap option test to update belief and determine if kill threshold is breached."""
        is_falsified = observed_metric_value < hypothesis.kill_threshold
        if is_falsified:
            hypothesis.status = "FALSIFIED"
            hypothesis.current_confidence = max(0.0, hypothesis.current_confidence - 0.4)
            return hypothesis, False
        else:
            hypothesis.status = "CONFIRMED"
            hypothesis.current_confidence = min(1.0, hypothesis.current_confidence + 0.3)
            return hypothesis, True


# ==========================================
# 2. External 13 Operational Loops
# ==========================================

class OperationalLoopType(str, Enum):
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


class OperationalLoopState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    loop_type: OperationalLoopType
    primary_kpi_name: str
    primary_kpi_value: float
    target_kpi_value: float
    health_score: float = Field(ge=0.0, le=1.0, default=0.8)
    dominant_failure_risk: str


class OperationalLoopSuite(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    loops: Dict[OperationalLoopType, OperationalLoopState] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.loops:
            self._initialize_default_loops()

    def _initialize_default_loops(self) -> None:
        defaults = [
            (OperationalLoopType.PRODUCT, "retention_rate", 0.40, 0.60, "Building for vocal non-ICP outliers"),
            (OperationalLoopType.MARKETING, "cac_dollars", 250.0, 150.0, "Scaling spend before message resonance"),
            (OperationalLoopType.SALES, "win_rate", 0.22, 0.35, "Selling to non-ICP to hit quota"),
            (OperationalLoopType.CUSTOMER_SUCCESS, "nrr", 1.05, 1.30, "Reactive support queue instead of proactive outcome"),
            (OperationalLoopType.BRAND, "price_elasticity", 0.80, 1.50, "Brand as decoration instead of strategic trust"),
            (OperationalLoopType.PRICING, "arpu_dollars", 120.0, 300.0, "Cost-plus pricing instead of value-based"),
            (OperationalLoopType.REFERRAL, "viral_k_factor", 0.15, 0.80, "Incentivizing referral volume over ICP quality"),
            (OperationalLoopType.DATA, "decision_latency_hours", 48.0, 4.0, "Vanity dashboard metrics without actions"),
            (OperationalLoopType.FINANCIAL, "burn_multiple", 2.2, 1.2, "Growth at negative unit economics"),
            (OperationalLoopType.HIRING, "quality_of_hire_score", 0.70, 0.90, "Hiring for pedigree over role capability fit"),
            (OperationalLoopType.CULTURE, "decision_speed_index", 0.65, 0.90, "Stated values contradicted by incentive structures"),
            (OperationalLoopType.INNOVATION, "shipped_experiments_count", 3.0, 10.0, "Innovation theater without shipped bets"),
            (OperationalLoopType.COMPETITIVE_INTELLIGENCE, "feature_parity_gap", 0.30, 0.05, "Obsessive reactivity instead of own strategy"),
        ]
        for loop_type, kpi_name, current_val, target_val, failure_risk in defaults:
            self.loops[loop_type] = OperationalLoopState(
                loop_type=loop_type,
                primary_kpi_name=kpi_name,
                primary_kpi_value=current_val,
                target_kpi_value=target_val,
                dominant_failure_risk=failure_risk,
            )

    def evaluate_coupling_impact(self) -> Dict[str, Any]:
        """Calculates system coupling effects (e.g. ARPU -> Financial -> Hiring -> Product)."""
        arpu = self.loops[OperationalLoopType.PRICING].primary_kpi_value
        cac = self.loops[OperationalLoopType.MARKETING].primary_kpi_value
        burn_multiple = self.loops[OperationalLoopType.FINANCIAL].primary_kpi_value

        ltv_cac_ratio = (arpu * 24.0) / max(1.0, cac) # 24 mo LTV proxy
        overall_health = sum(l.health_score for l in self.loops.values()) / len(self.loops)

        return {
            "ltv_cac_ratio": ltv_cac_ratio,
            "burn_multiple": burn_multiple,
            "overall_system_health": overall_health,
            "coupling_status": "HEALTHY" if ltv_cac_ratio >= 3.0 and burn_multiple <= 1.5 else "CONSTRAINED",
        }


# ==========================================
# 3. Customer Journey Lifecycle State Machine
# ==========================================

class JourneyStage(str, Enum):
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


class CustomerCohort(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cohort_id: str
    size: int
    current_stage: JourneyStage
    stage_conversion_rates: Dict[JourneyStage, float] = Field(default_factory=dict)
    ttfv_days: float = Field(default=7.0) # Time to first value
    retention_curve_slope: float = Field(default=-0.05)


class CustomerJourneyTracker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cohorts: Dict[str, CustomerCohort] = Field(default_factory=dict)

    def register_cohort(self, cohort: CustomerCohort) -> None:
        self.cohorts[cohort.cohort_id] = cohort

    def advance_cohort(self, cohort_id: str, next_stage: JourneyStage, conversion_rate: float) -> Optional[CustomerCohort]:
        cohort = self.cohorts.get(cohort_id)
        if not cohort:
            return None
        cohort.current_stage = next_stage
        cohort.stage_conversion_rates[next_stage] = conversion_rate
        cohort.size = int(cohort.size * conversion_rate)
        return cohort

    def analyze_retention_flattening(self, cohort_id: str) -> bool:
        """Determines if retention curve has flattened (indicating true Product-Market Fit)."""
        cohort = self.cohorts.get(cohort_id)
        if not cohort:
            return False
        return abs(cohort.retention_curve_slope) < 0.01


# ==========================================
# 4. Company Growth Stage Classifier
# ==========================================

class CompanyGrowthStage(str, Enum):
    IDEA = "IDEA"
    VALIDATION = "VALIDATION"
    STARTUP = "STARTUP"
    PMF = "PMF"
    GROWTH = "GROWTH"
    SCALE = "SCALE"
    PLATFORM = "PLATFORM"
    ECOSYSTEM = "ECOSYSTEM"
    MARKET_LEADERSHIP = "MARKET_LEADERSHIP"


class GrowthStageProfile(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    stage: CompanyGrowthStage
    primary_objective: str
    core_metric: str
    binding_constraint: str


class CompanyGrowthClassifier(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def classify_stage(self, metrics: Dict[str, Any]) -> GrowthStageProfile:
        paying_customers = metrics.get("paying_customers", 0)
        retention_flattened = metrics.get("retention_flattened", False)
        arr_dollars = metrics.get("arr_dollars", 0.0)
        third_party_devs = metrics.get("third_party_devs", 0)

        if third_party_devs > 1000 and arr_dollars >= 50_000_000:
            return GrowthStageProfile(
                stage=CompanyGrowthStage.MARKET_LEADERSHIP,
                primary_objective="Defend and extend category leadership",
                core_metric="Category market share & moat durability",
                binding_constraint="Innovation velocity vs incumbency drag",
            )
        elif third_party_devs > 100:
            return GrowthStageProfile(
                stage=CompanyGrowthStage.ECOSYSTEM,
                primary_objective="Orchestrate multi-sided network",
                core_metric="Ecosystem GMV & network density",
                binding_constraint="Governance credibility",
            )
        elif arr_dollars >= 20_000_000:
            return GrowthStageProfile(
                stage=CompanyGrowthStage.SCALE,
                primary_objective="Institutionalize repeatability",
                core_metric="Rule of 40 & NRR",
                binding_constraint="Org coordination cost",
            )
        elif arr_dollars >= 2_000_000:
            return GrowthStageProfile(
                stage=CompanyGrowthStage.GROWTH,
                primary_objective="Scale what works",
                core_metric="ARR Growth rate & CAC payback",
                binding_constraint="Hiring velocity & operational systems",
            )
        elif retention_flattened:
            return GrowthStageProfile(
                stage=CompanyGrowthStage.PMF,
                primary_objective="Reach retention and growth threshold",
                core_metric="Retention curve slope",
                binding_constraint="Team bandwidth",
            )
        elif paying_customers >= 10:
            return GrowthStageProfile(
                stage=CompanyGrowthStage.STARTUP,
                primary_objective="Build repeatable customer acquisition channel",
                core_metric="LTV:CAC ratio",
                binding_constraint="Cash runway",
            )
        elif paying_customers > 0:
            return GrowthStageProfile(
                stage=CompanyGrowthStage.VALIDATION,
                primary_objective="Prove willingness to pay",
                core_metric="Paying customers / LOIs",
                binding_constraint="Signal quality",
            )
        else:
            return GrowthStageProfile(
                stage=CompanyGrowthStage.IDEA,
                primary_objective="Falsify or strengthen hypothesis",
                core_metric="# of validated learnings",
                binding_constraint="Founder attention",
            )


# ==========================================
# 5. Opportunity Pursuit Decision Tree
# ==========================================

class DecisionOutcome(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    action: str  # COMMIT, DISCARD, RUN_CHEAP_TEST
    rationale: str
    risk_type: Optional[RiskType] = None


class OpportunityPursuitDecisionTree(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def evaluate(self, opportunity: Dict[str, Any]) -> DecisionOutcome:
        is_structural = opportunity.get("is_structural_anomaly", False)
        if not is_structural:
            return DecisionOutcome(
                action="DISCARD",
                rationale="Signal is noise or local fluctuation, not a structural shift.",
            )

        is_reversible = opportunity.get("is_reversible", True)
        if not is_reversible:
            high_confidence = opportunity.get("multi_source_confidence", False)
            if not high_confidence:
                return DecisionOutcome(
                    action="DISCARD",
                    rationale="Irreversible decision (Type I risk) lacks multi-source high-confidence validation.",
                    risk_type=RiskType.TYPE_I,
                )

        cheap_test_available = opportunity.get("cheap_test_available", True)
        if cheap_test_available:
            test_passed = opportunity.get("cheap_test_passed")
            if test_passed is None:
                return DecisionOutcome(
                    action="RUN_CHEAP_TEST",
                    rationale="Run cheap real-option experiment before committing capital.",
                    risk_type=RiskType.TYPE_II if is_reversible else RiskType.TYPE_I,
                )
            elif not test_passed:
                return DecisionOutcome(
                    action="DISCARD",
                    rationale="Cheap option test breached pre-committed kill threshold.",
                    risk_type=RiskType.TYPE_II if is_reversible else RiskType.TYPE_I,
                )

        has_structural_advantage = opportunity.get("has_structural_advantage", False)
        if not has_structural_advantage:
            return DecisionOutcome(
                action="DISCARD",
                rationale="Lacks defensible structural advantage or competitive moat.",
            )

        return DecisionOutcome(
            action="COMMIT",
            rationale="Opportunity validated: structural anomaly, risk mitigated, test passed, advantage present.",
            risk_type=RiskType.TYPE_II if is_reversible else RiskType.TYPE_I,
        )


# ==========================================
# 6. Operational Failure Mode Monitor
# ==========================================

class FailureWarning(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    failure_mode: str
    root_cause: str
    detection_signal: str
    corrective_action: str
    severity: str # LOW, MEDIUM, HIGH, CRITICAL


class FailureModeMonitor(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def audit_metrics(self, company_state: Dict[str, Any]) -> List[FailureWarning]:
        warnings = []

        # 1. Solving wrong problem
        if company_state.get("survey_nps", 0) > 80 and company_state.get("daily_active_ratio", 1.0) < 0.05:
            warnings.append(FailureWarning(
                failure_mode="Solving wrong problem",
                root_cause="Skipped root-cause analysis; solved a symptom",
                detection_signal="High NPS survey scores accompanied by low active retention",
                corrective_action="Return to Jobs-To-Be-Done interviews and root cause analysis",
                severity="HIGH",
            ))

        # 2. Building before validating
        if company_state.get("build_velocity_tickets", 0) > 50 and company_state.get("demand_conversion_rate", 1.0) < 0.01:
            warnings.append(FailureWarning(
                failure_mode="Building before validating",
                root_cause="Founder conviction substituted for market evidence",
                detection_signal="High feature velocity with flat user demand signal",
                corrective_action="Enforce strict validation gate before allocating build resources",
                severity="CRITICAL",
            ))

        # 3. Premature scaling
        cac_growth = company_state.get("cac_growth_rate", 0.0)
        ltv_growth = company_state.get("ltv_growth_rate", 0.0)
        if cac_growth > 0.5 and ltv_growth < 0.1:
            warnings.append(FailureWarning(
                failure_mode="Scaling prematurely",
                root_cause="Confusing early demand spike with durable Product-Market Fit",
                detection_signal="CAC rising faster than LTV as marketing spend scales",
                corrective_action="Re-test unit economics at current order-of-magnitude spend",
                severity="CRITICAL",
            ))

        # 4. Capital misallocation
        active_unvalidated_bets = company_state.get("active_unvalidated_bets", 0)
        if active_unvalidated_bets >= 5:
            warnings.append(FailureWarning(
                failure_mode="Capital misallocation",
                root_cause="Lack of opportunity-cost discipline in budgeting",
                detection_signal="Multiple underperforming bets funded simultaneously",
                corrective_action="Rank all active initiatives on expected return basis quarterly",
                severity="HIGH",
            ))

        return warnings
