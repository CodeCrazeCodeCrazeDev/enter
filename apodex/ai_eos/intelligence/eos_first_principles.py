"""
The Entrepreneurial Operating System (EOS) - First-Principles Engine.

A executable Python implementation of how elite founders sense, build,
and compound enduring companies, as specified in ENTREPRENEURIAL_OPERATING_SYSTEM_SPEC.md.
"""

from __future__ import annotations
import math
import logging
from enum import Enum, auto
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger("ai_eos.eos_first_principles")


# =====================================================================
# 0. Timescale Loops
# =====================================================================
class LoopTimescale(str, Enum):
    FAST = "fast"        # Days - weeks (experiments, sales calls, ad tests)
    MEDIUM = "medium"    # Months - quarters (GTM iteration, pricing, org design)
    SLOW = "slow"        # Years (positioning, moat construction, reinvention)


@dataclass
class FeedbackLoopMetrics:
    timescale: LoopTimescale
    cycle_time_days: float
    signal_fidelity: float  # [0.0, 1.0]
    compounding_rate: float
    kill_discipline_score: float  # [0.0, 1.0]


# =====================================================================
# 1. Decision Theory & Risk Classification (§2.1)
# =====================================================================
class DecisionRiskType(str, Enum):
    TYPE_I = "type_i"   # Irreversible ("One-way door"), slow high-scrutiny deliberation
    TYPE_II = "type_ii" # Reversible ("Two-way door"), fast cheap execution


@dataclass
class WeakSignal:
    signal_id: str
    description: str
    source: str
    observed_value: float
    expected_value: float
    is_structural_anomaly: bool = False
    anomaly_score: float = 0.0


@dataclass
class FalsifiableHypothesis:
    hypothesis_id: UUID = field(default_factory=uuid4)
    claim: str = ""
    enabling_condition: str = ""
    cheap_test_description: str = ""
    test_cost_cents: int = 0
    kill_threshold_metric: str = ""
    kill_threshold_value: float = 0.0
    prior_belief: float = 0.5
    posterior_belief: float = 0.5
    status: str = "proposed"  # proposed, testing, validated, falsified, killed


class SignalToHypothesisPipeline:
    """Filters weak signals, detects structural anomalies, and generates forced hypotheses."""

    def filter_signal(self, signal: WeakSignal, threshold: float = 0.3) -> bool:
        """Determines if signal is a symptom of a structural shift vs background noise."""
        delta = abs(signal.observed_value - signal.expected_value)
        signal.anomaly_score = min(1.0, delta / max(1e-6, abs(signal.expected_value)))
        signal.is_structural_anomaly = signal.anomaly_score >= threshold
        return signal.is_structural_anomaly

    def categorize_risk(self, decision_name: str, capital_impact_cents: int, regulatory_or_safety: bool) -> DecisionRiskType:
        """Bezos 'One-way vs Two-way door' heuristic."""
        if regulatory_or_safety or capital_impact_cents >= 1000000_00:  # >= $1M
            return DecisionRiskType.TYPE_I
        return DecisionRiskType.TYPE_II

    def create_forced_hypothesis(
        self,
        signal: WeakSignal,
        enabling_condition: str,
        test_cost_cents: int,
        kill_metric: str,
        kill_value: float
    ) -> FalsifiableHypothesis:
        """Converts structural anomaly into falsifiable hypothesis with pre-committed kill criteria."""
        return FalsifiableHypothesis(
            claim=f"Structural anomaly in {signal.description} indicates market viability under condition: {enabling_condition}",
            enabling_condition=enabling_condition,
            cheap_test_description=f"Cheap test for {signal.signal_id}",
            test_cost_cents=test_cost_cents,
            kill_threshold_metric=kill_metric,
            kill_threshold_value=kill_value,
            prior_belief=0.5
        )


# =====================================================================
# 2. Mental Model Evolution (§2.2)
# =====================================================================
class MentalModelTracker:
    """Tracks living, falsifiable mental models, parameter vs structural updates, and ossification."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.parameters: Dict[str, float] = {}
        self.structure_version: int = 1
        self.parameter_update_count: int = 0
        self.structural_update_count: int = 0
        self.consecutive_contradictions: int = 0

    def update_with_feedback(self, metric: str, predicted: float, actual: float, error_tolerance: float = 0.1) -> Dict[str, Any]:
        error = abs(actual - predicted) / max(1e-6, abs(predicted))
        if error <= error_tolerance:
            self.consecutive_contradictions = 0
            return {"action": "confirmed", "structure_version": self.structure_version}

        self.consecutive_contradictions += 1
        # If repeated contradictions occur, require structural update (paradigm shift)
        if self.consecutive_contradictions >= 3:
            self.structure_version += 1
            self.structural_update_count += 1
            self.consecutive_contradictions = 0
            logger.warning(f"MENTAL MODEL PARADIGM SHIFT: {self.model_name} updated to structure version {self.structure_version}")
            return {"action": "structural_shift", "structure_version": self.structure_version}

        # Otherwise, tune parameter (fast)
        self.parameters[metric] = actual
        self.parameter_update_count += 1
        return {"action": "parameter_tuned", "parameter": metric, "new_value": actual}

    def is_ossified(self) -> bool:
        """Model ossification occurs when structural updates remain 0 despite heavy parameter tuning."""
        return self.parameter_update_count > 10 and self.structural_update_count == 0


# =====================================================================
# 3. 13 Coupled External Business Loops (§3)
# =====================================================================
class BusinessLoopType(str, Enum):
    PRODUCT = "product"
    MARKETING = "marketing"
    SALES = "sales"
    CUSTOMER_SUCCESS = "customer_success"
    BRAND = "brand"
    PRICING = "pricing"
    REFERRAL = "referral"
    DATA = "data"
    FINANCIAL = "financial"
    HIRING = "hiring"
    CULTURE = "culture"
    INNOVATION = "innovation"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"


@dataclass
class BusinessLoopState:
    loop_type: BusinessLoopType
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    feedback_signal: float  # [-1.0, 1.0]
    kpis: Dict[str, float]
    failure_mode_flagged: Optional[str] = None


class BusinessLoopCoupler:
    """Manages execution and coupled interactions across all 13 external business loops."""

    def __init__(self) -> None:
        self.loops: Dict[BusinessLoopType, BusinessLoopState] = {}
        self._init_loops()

    def _init_loops(self) -> None:
        for loop_type in BusinessLoopType:
            self.loops[loop_type] = BusinessLoopState(
                loop_type=loop_type,
                inputs={},
                outputs={},
                feedback_signal=0.0,
                kpis={}
            )

    def evaluate_loop(self, loop_type: BusinessLoopType, inputs: Dict[str, Any]) -> BusinessLoopState:
        state = self.loops[loop_type]
        state.inputs = inputs

        if loop_type == BusinessLoopType.PRODUCT:
            # Retention curve, NPS
            retention = inputs.get("retention_curve_slope", 0.0)
            state.kpis = {"retention_slope": retention, "nps": inputs.get("nps", 50.0)}
            state.feedback_signal = 1.0 if retention >= 0.0 else -1.0
            if inputs.get("building_for_loudest_customer", False):
                state.failure_mode_flagged = "Building for loudest customer, not representative one"

        elif loop_type == BusinessLoopType.MARKETING:
            cac = inputs.get("cac_cents", 100_00)
            conversion = inputs.get("conversion_rate", 0.02)
            state.kpis = {"cac_cents": cac, "conversion_rate": conversion}
            state.feedback_signal = 1.0 if conversion >= 0.02 else -0.5

        elif loop_type == BusinessLoopType.SALES:
            win_rate = inputs.get("win_rate", 0.25)
            acv = inputs.get("acv_cents", 10000_00)
            state.kpis = {"win_rate": win_rate, "acv_cents": acv}
            state.feedback_signal = 1.0 if win_rate >= 0.20 else -1.0
            if inputs.get("selling_to_non_icp", False):
                state.failure_mode_flagged = "Selling to non-ICP to hit quota"

        elif loop_type == BusinessLoopType.CUSTOMER_SUCCESS:
            nrr = inputs.get("nrr", 1.10)
            churn = inputs.get("churn_rate", 0.02)
            state.kpis = {"nrr": nrr, "churn_rate": churn}
            state.feedback_signal = 1.0 if nrr >= 1.0 else -1.0

        elif loop_type == BusinessLoopType.PRICING:
            arpu = inputs.get("arpu_cents", 50_00)
            margin = inputs.get("price_realization_margin", 0.70)
            state.kpis = {"arpu_cents": arpu, "price_realization_margin": margin}
            state.feedback_signal = 1.0 if margin >= 0.50 else -0.5

        elif loop_type == BusinessLoopType.FINANCIAL:
            burn_multiple = inputs.get("burn_multiple", 1.5)
            runway = inputs.get("runway_months", 18.0)
            state.kpis = {"burn_multiple": burn_multiple, "runway_months": runway}
            state.feedback_signal = 1.0 if burn_multiple <= 2.0 and runway >= 12.0 else -1.0

        else:
            state.kpis = {"status_score": 0.8}
            state.feedback_signal = 0.5

        return state


# =====================================================================
# 4. Customer Journey Engine (§4)
# =====================================================================
class JourneyStage(str, Enum):
    AWARENESS = "awareness"
    INTEREST = "interest"
    CONSIDERATION = "consideration"
    EVALUATION = "evaluation"
    PURCHASE = "purchase"
    ONBOARDING = "onboarding"
    ACTIVATION = "activation"
    ENGAGEMENT = "engagement"
    HABIT_FORMATION = "habit_formation"
    RETENTION = "retention"
    LOYALTY = "loyalty"
    ADVOCACY = "advocacy"
    REFERRAL = "referral"
    EXPANSION = "expansion"
    REPURCHASE = "repurchase"


@dataclass
class JourneyStageSpec:
    stage: JourneyStage
    founder_objective: str
    customer_psychology: str
    key_metric: str
    common_mistake: str
    optimization_lever: str


class CustomerJourneyEngine:
    """Executes full 15-stage lifecycle cohort tracking and optimization."""

    STAGE_SPECS: Dict[JourneyStage, JourneyStageSpec] = {
        JourneyStage.AWARENESS: JourneyStageSpec(
            JourneyStage.AWARENESS, "Enter consideration set", "Pattern-matching against known categories",
            "Reach, unaided recall", "Generic category messaging", "Sharp category framing / naming a new category"
        ),
        JourneyStage.EVALUATION: JourneyStageSpec(
            JourneyStage.EVALUATION, "Reduce perceived risk", "Loss aversion dominates gain-seeking",
            "Trial starts, demo requests", "Ignoring risk-reduction", "Make failure cheap and reversible"
        ),
        JourneyStage.ACTIVATION: JourneyStageSpec(
            JourneyStage.ACTIVATION, "Cross the 'aha' threshold", "Forming initial habit loop",
            "Activation rate", "Defining activation as login", "Instrument true 'aha' moment via cohort analysis"
        ),
        JourneyStage.RETENTION: JourneyStageSpec(
            JourneyStage.RETENTION, "Prevent churn", "Switching cost perception, sunk value",
            "Retention curve, churn", "Measuring retention only in aggregate", "Cohort-level retention curve flattening"
        ),
        JourneyStage.EXPANSION: JourneyStageSpec(
            JourneyStage.EXPANSION, "Grow account value", "Anchoring to current spend",
            "Net revenue retention", "Under-selling adjacent value", "Usage-based expansion triggers"
        ),
    }

    def evaluate_cohort_funnel(self, stage_conversions: Dict[JourneyStage, float]) -> List[str]:
        """Identifies bottlenecks across the 15-stage customer journey."""
        bottlenecks = []
        for stage, rate in stage_conversions.items():
            if rate < 0.20:
                spec = self.STAGE_SPECS.get(stage)
                lever = spec.optimization_lever if spec else "Optimize conversion funnel"
                bottlenecks.append(f"Stage '{stage.value}' bottleneck (conversion: {rate:.1%}). Fix: {lever}")
        return bottlenecks


# =====================================================================
# 5. Go-To-Market (GTM) System Engine (§5)
# =====================================================================
class GTMMotion(str, Enum):
    PLG = "product_led_growth"
    SLG = "sales_led_growth"
    CLG = "community_led_growth"
    ENTERPRISE = "enterprise_sales"


class GTMSystemEngine:
    """Models upstream positioning, pricing signals, distribution channel selection, and motion alignment."""

    def determine_channel_motion(self, acv_cents: int, product_complexity: float) -> GTMMotion:
        """Enforces channel fit following buyer behavior rather than founder preference."""
        if acv_cents < 500_00 and product_complexity < 0.3:  # < $500
            return GTMMotion.PLG
        elif acv_cents >= 50000_00 or product_complexity >= 0.7:  # >= $50k
            return GTMMotion.ENTERPRISE
        elif product_complexity < 0.5:
            return GTMMotion.CLG
        else:
            return GTMMotion.SLG


# =====================================================================
# 6. Company Growth System Classifier (§6)
# =====================================================================
class CompanyGrowthStage(str, Enum):
    IDEA = "idea"
    VALIDATION = "validation"
    STARTUP = "startup"
    PMF = "pmf"
    GROWTH = "growth"
    SCALE = "scale"
    PLATFORM = "platform"
    ECOSYSTEM = "ecosystem"
    MARKET_LEADERSHIP = "market_leadership"


class GrowthStageClassifier:
    """Continuously scores venture metrics against the 9-stage model to flag premature scaling."""

    def classify_stage(
        self,
        paying_customers: int,
        retention_curve_flattened: bool,
        mrr_cents: int,
        ecosystem_gmv_cents: int
    ) -> Dict[str, Any]:
        if paying_customers == 0:
            stage = CompanyGrowthStage.IDEA
            constraint = "Founder time"
        elif paying_customers < 10 and not retention_curve_flattened:
            stage = CompanyGrowthStage.VALIDATION
            constraint = "Signal quality"
        elif paying_customers >= 10 and not retention_curve_flattened:
            stage = CompanyGrowthStage.STARTUP
            constraint = "Cash runway"
        elif retention_curve_flattened and mrr_cents < 100000_00:
            stage = CompanyGrowthStage.PMF
            constraint = "Team bandwidth"
        elif retention_curve_flattened and mrr_cents >= 100000_00 and mrr_cents < 1000000_00:
            stage = CompanyGrowthStage.GROWTH
            constraint = "Hiring velocity & systems"
        elif mrr_cents >= 1000000_00 and ecosystem_gmv_cents == 0:
            stage = CompanyGrowthStage.SCALE
            constraint = "Org coordination cost"
        elif ecosystem_gmv_cents > 0 and ecosystem_gmv_cents < 10000000_00:
            stage = CompanyGrowthStage.PLATFORM
            constraint = "Trust from ecosystem partners"
        elif ecosystem_gmv_cents >= 10000000_00:
            stage = CompanyGrowthStage.MARKET_LEADERSHIP
            constraint = "Innovation velocity vs incumbency drag"
        else:
            stage = CompanyGrowthStage.GROWTH
            constraint = "Hiring velocity"

        return {
            "stage": stage,
            "binding_constraint": constraint,
            "retention_curve_flattened": retention_curve_flattened
        }

    def detect_premature_scaling(self, current_stage: CompanyGrowthStage, marketing_spend_cents: int, retention_flattened: bool) -> bool:
        """Flags premature scaling if aggressive spend occurs before PMF retention curve flattening."""
        if not retention_flattened and marketing_spend_cents > 50000_00:  # > $50k spend without PMF
            logger.error("PREMATURE SCALING DETECTED: Marketing spend exceeds $50k before retention curve flattening!")
            return True
        return False


# =====================================================================
# 7. Strategic Thinking & Moats (§7)
# =====================================================================
class MoatType(str, Enum):
    NETWORK_EFFECTS = "network_effects"
    SWITCHING_COSTS = "switching_costs"
    ECONOMIES_OF_SCALE = "economies_of_scale"
    BRAND = "brand"
    REGULATORY_IP = "regulatory_ip"
    COUNTER_POSITIONING = "counter_positioning"


class StrategicThinkingEngine:
    """Evaluates Hamilton Helmer's 7 Powers, cost curve predictions, and platform shifts."""

    def calculate_moat_score(self, active_moats: Dict[MoatType, float]) -> float:
        """Calculates consolidated Moat Durability Score [0.0, 1.0]."""
        if not active_moats:
            return 0.0
        weights = {
            MoatType.NETWORK_EFFECTS: 0.25,
            MoatType.SWITCHING_COSTS: 0.20,
            MoatType.COUNTER_POSITIONING: 0.20,
            MoatType.ECONOMIES_OF_SCALE: 0.15,
            MoatType.BRAND: 0.10,
            MoatType.REGULATORY_IP: 0.10,
        }
        score = sum(active_moats.get(m, 0.0) * weights.get(m, 0.10) for m in active_moats)
        return min(1.0, score)

    def is_cost_curve_viable(self, unit_cost_cents: int, willingness_to_pay_cents: int) -> bool:
        """Checks if unit cost curve crossed viability threshold."""
        return unit_cost_cents < willingness_to_pay_cents


# =====================================================================
# 8. Failure Mode Analysis (§8)
# =====================================================================
class FailureModeType(str, Enum):
    SOLVING_WRONG_PROBLEM = "solving_wrong_problem"
    BUILDING_BEFORE_VALIDATING = "building_before_validating"
    WEAK_POSITIONING = "weak_positioning"
    POOR_PRICING = "poor_pricing"
    DISTRIBUTION_FAILURE = "distribution_failure"
    LACK_OF_PMF = "lack_of_pmf"
    ORGANIZATIONAL_BOTTLENECK = "organizational_bottleneck"
    FOUNDER_BIAS = "founder_bias"
    SCALING_PREMATURELY = "scaling_prematurely"
    CAPITAL_MISALLOCATION = "capital_misallocation"


@dataclass
class FailureModeDiagnosis:
    failure_type: FailureModeType
    root_cause: str
    detection_signal: str
    correction_mechanism: str


class FailureModeDetector:
    """Pattern matches operating metrics against the failure-mode table and suggests corrections."""

    DIAGNOSES: Dict[FailureModeType, FailureModeDiagnosis] = {
        FailureModeType.SOLVING_WRONG_PROBLEM: FailureModeDiagnosis(
            FailureModeType.SOLVING_WRONG_PROBLEM, "Skipped root-cause analysis; solved a symptom",
            "Low engagement despite positive survey feedback", "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)"
        ),
        FailureModeType.BUILDING_BEFORE_VALIDATING: FailureModeDiagnosis(
            FailureModeType.BUILDING_BEFORE_VALIDATING, "Founder conviction substituted for evidence",
            "High build velocity, flat demand signal", "Enforce a validation gate before build resourcing"
        ),
        FailureModeType.LACK_OF_PMF: FailureModeDiagnosis(
            FailureModeType.LACK_OF_PMF, "Premature scaling of an unproven loop",
            "Retention curve never flattens", "Stop scaling; return to cohort-level retention work"
        ),
        FailureModeType.FOUNDER_BIAS: FailureModeDiagnosis(
            FailureModeType.FOUNDER_BIAS, "Overconfidence, confirmation bias, sunk cost",
            "Ignoring disconfirming data, 'just needs more time' pattern", "Pre-committed kill criteria set before launch"
        ),
        FailureModeType.SCALING_PREMATURELY: FailureModeDiagnosis(
            FailureModeType.SCALING_PREMATURELY, "Confusing early demand spike with durable PMF",
            "CAC rising faster than LTV as spend scales", "Re-test unit economics at each order-of-magnitude of spend"
        ),
    }

    def diagnose_metrics(
        self,
        build_velocity_high: bool,
        demand_signal_flat: bool,
        retention_flattens: bool,
        cac_rising_fast: bool
    ) -> List[FailureModeDiagnosis]:
        diagnoses = []
        if build_velocity_high and demand_signal_flat:
            diagnoses.append(self.DIAGNOSES[FailureModeType.BUILDING_BEFORE_VALIDATING])
        if not retention_flattens:
            diagnoses.append(self.DIAGNOSES[FailureModeType.LACK_OF_PMF])
        if cac_rising_fast and not retention_flattens:
            diagnoses.append(self.DIAGNOSES[FailureModeType.SCALING_PREMATURELY])
        return diagnoses


# =====================================================================
# 9. System State Machine & Decision Tree (§10.1, §10.2)
# =====================================================================
class EOSState(str, Enum):
    SENSING = "sensing"
    HYPOTHESIS = "hypothesis"
    CHEAP_TEST = "cheap_test"
    VALIDATION = "validation"
    BUILD_GATE = "build_gate"
    MVP = "mvp"
    GTM_TEST = "gtm_test"
    KILL_OR_SCALE = "kill_or_scale"
    SCALE = "scale"
    OPERATE = "operate"
    REINVENT = "reinvent"
    DISCARD = "discard"


class EOSStateMachine:
    """State machine governing the venture execution loop with kill signal re-entrancy."""

    VALID_TRANSITIONS = {
        EOSState.SENSING: [EOSState.HYPOTHESIS],
        EOSState.HYPOTHESIS: [EOSState.CHEAP_TEST, EOSState.DISCARD],
        EOSState.CHEAP_TEST: [EOSState.VALIDATION, EOSState.DISCARD, EOSState.SENSING],
        EOSState.VALIDATION: [EOSState.BUILD_GATE, EOSState.DISCARD],
        EOSState.BUILD_GATE: [EOSState.MVP, EOSState.DISCARD],
        EOSState.MVP: [EOSState.GTM_TEST],
        EOSState.GTM_TEST: [EOSState.KILL_OR_SCALE],
        EOSState.KILL_OR_SCALE: [EOSState.SCALE, EOSState.DISCARD, EOSState.SENSING],
        EOSState.SCALE: [EOSState.OPERATE],
        EOSState.OPERATE: [EOSState.REINVENT],
        EOSState.REINVENT: [EOSState.SENSING],
        EOSState.DISCARD: [EOSState.SENSING],
    }

    def __init__(self) -> None:
        self.current_state = EOSState.SENSING

    def transition(self, next_state: EOSState) -> bool:
        if next_state in self.VALID_TRANSITIONS.get(self.current_state, []):
            logger.info(f"EOS STATE TRANSITION: {self.current_state.value} -> {next_state.value}")
            self.current_state = next_state
            return True
        logger.error(f"INVALID STATE TRANSITION: {self.current_state.value} -> {next_state.value}")
        return False


class EOSDecisionTree:
    """Evaluates 'Should We Pursue This Opportunity?' decision tree (§10.2)."""

    def evaluate_opportunity(
        self,
        is_structural_anomaly: bool,
        is_reversible_decision: bool,
        high_confidence_signal: bool,
        cheap_test_available: bool,
        test_result_exceeds_kill_threshold: bool,
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> Dict[str, Any]:
        # Q1: Structural anomaly or just noise?
        if not is_structural_anomaly:
            return {"decision": "discard", "reason": "Signal is noise, not structural anomaly"}

        # Q2: Reversible decision?
        if not is_reversible_decision:
            if not high_confidence_signal:
                return {"decision": "discard", "reason": "Irreversible decision with low confidence signal"}

        # Q3: Cheap test available?
        if cheap_test_available:
            if not test_result_exceeds_kill_threshold:
                return {"decision": "discard", "reason": "Cheap test result fell below kill threshold"}
        else:
            if not expected_value_positive:
                return {"decision": "discard", "reason": "No cheap test and expected value is not positive"}

        # Q5: Structural advantage?
        if not has_structural_advantage:
            return {"decision": "discard", "reason": "No structural advantage or win condition"}

        return {"decision": "pursue", "reason": "Meets all decision tree criteria"}


# =====================================================================
# 10. Master First-Principles EOS OS Engine (§10.3)
# =====================================================================
class FirstPrinciplesEOSEngine(BaseModel):
    """Integrated AI-Driven Operating System orchestrating all 10 modules and rolled-up KPI stack."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    pipeline: SignalToHypothesisPipeline = Field(default_factory=SignalToHypothesisPipeline)
    growth_classifier: GrowthStageClassifier = Field(default_factory=GrowthStageClassifier)
    gtm_engine: GTMSystemEngine = Field(default_factory=GTMSystemEngine)
    strategic_engine: StrategicThinkingEngine = Field(default_factory=StrategicThinkingEngine)
    failure_detector: FailureModeDetector = Field(default_factory=FailureModeDetector)
    state_machine: EOSStateMachine = Field(default_factory=EOSStateMachine)
    decision_tree: EOSDecisionTree = Field(default_factory=EOSDecisionTree)

    def execute_sensing_and_evaluation(
        self,
        signal: WeakSignal,
        enabling_condition: str,
        test_cost_cents: int,
        kill_metric: str,
        kill_value: float,
        acv_cents: int,
        product_complexity: float,
        active_moats: Dict[MoatType, float]
    ) -> Dict[str, Any]:
        """Runs integrated pipeline from Sensing -> Anomaly Filter -> Hypothesis -> Decision -> Moat."""
        self.state_machine.current_state = EOSState.SENSING
        # 1. Sensing & Filtering
        is_anomaly = self.pipeline.filter_signal(signal)
        if not is_anomaly:
            self.state_machine.transition(EOSState.HYPOTHESIS)
            self.state_machine.transition(EOSState.DISCARD)
            return {"status": "discarded", "reason": "Signal filtered out as noise"}

        # 2. Forced Hypothesis Generation
        hyp = self.pipeline.create_forced_hypothesis(signal, enabling_condition, test_cost_cents, kill_metric, kill_value)
        self.state_machine.transition(EOSState.HYPOTHESIS)

        # 3. Decision Tree Evaluation
        decision = self.decision_tree.evaluate_opportunity(
            is_structural_anomaly=is_anomaly,
            is_reversible_decision=True,
            high_confidence_signal=True,
            cheap_test_available=True,
            test_result_exceeds_kill_threshold=True,
            expected_value_positive=True,
            has_structural_advantage=True
        )

        if decision["decision"] == "pursue":
            self.state_machine.transition(EOSState.CHEAP_TEST)
            gtm_motion = self.gtm_engine.determine_channel_motion(acv_cents, product_complexity)
            moat_score = self.strategic_engine.calculate_moat_score(active_moats)
            return {
                "status": "pursuing",
                "hypothesis_claim": hyp.claim,
                "gtm_motion": gtm_motion,
                "moat_durability_score": moat_score,
                "current_state": self.state_machine.current_state.value
            }
        else:
            self.state_machine.transition(EOSState.DISCARD)
            return {"status": "discarded", "reason": decision["reason"]}
