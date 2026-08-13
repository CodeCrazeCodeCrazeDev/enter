"""Entrepreneurial Operating System (EOS) First-Principles Reconstruction.

A robust Python framework implementing the nested coupled feedback loops,
cognitive decision-making pipelines, business loop coupling, customer journey stages,
GTM systems, growth stages, strategic trackers, and failure-mode monitors
that characterize how elite founders build and compound enduring companies.
"""

from __future__ import annotations
import logging
import math
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger("ai_eos.eos_first_principles")


# =====================================================================
# 1. THE MASTER LOOP (Top-Level Architecture)
# =====================================================================

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
    ACTIVATION_RETENTION = "L"
    REVENUE_OPTIMIZATION = "M"
    OPERATIONS_SCALING = "N"
    MOAT_CONSTRUCTION = "O"
    SCALING_EXPANSION = "P"
    PLATFORM_FORMATION = "Q"
    MARKET_LEADERSHIP = "R"
    CONTINUOUS_REINVENTION = "S"


class MasterLoop(BaseModel):
    """Manages state and re-entrant transitions in the core EOS Master Loop."""
    current_node: MasterLoopNode = MasterLoopNode.ENVIRONMENTAL_SENSING
    history: List[MasterLoopNode] = Field(default_factory=list)
    is_halted: bool = False

    def transition_to(self, next_node: MasterLoopNode, reason: str = "") -> MasterLoopNode:
        """Transitions to the next node, recording the trajectory in history."""
        logger.info(f"MasterLoop: Transitioning from {self.current_node.name} -> {next_node.name}. Reason: {reason}")
        self.history.append(self.current_node)
        self.current_node = next_node
        return self.current_node

    def process_signal(self, signal_type: str, signal_value: float) -> MasterLoopNode:
        """Processes key environmental feedback signals to trigger transitions or re-entry paths.

        Handles:
        - F (Validation) -> D (Opportunity Discovery) [kill signal]
        - H (MVP) -> D (Opportunity Discovery) [kill signal]
        - K (Acquisition) -> J (GTM System) [weak GTM signal]
        - M (Revenue) -> G (Business Model Design) [bad economics signal]
        - S (Reinvention) -> A (Environmental Sensing) [reinvention loop]
        """
        # Node F: Customer Validation
        if self.current_node == MasterLoopNode.CUSTOMER_VALIDATION:
            if signal_type == "kill_signal" and signal_value > 0.5:
                return self.transition_to(MasterLoopNode.OPPORTUNITY_DISCOVERY, "Falsified customer validation -> Kill Signal")
            else:
                return self.transition_to(MasterLoopNode.BUSINESS_MODEL_DESIGN, "Validated customer demand")

        # Node H: MVP Experimentation
        elif self.current_node == MasterLoopNode.MVP_EXPERIMENTATION:
            if signal_type == "kill_signal" and signal_value > 0.5:
                return self.transition_to(MasterLoopNode.OPPORTUNITY_DISCOVERY, "Falsified MVP experiment -> Kill Signal")
            else:
                return self.transition_to(MasterLoopNode.PRODUCT_DEVELOPMENT, "Validated MVP performance")

        # Node K: Customer Acquisition
        elif self.current_node == MasterLoopNode.CUSTOMER_ACQUISITION:
            if signal_type == "weak_gtm" and signal_value < 0.3:
                return self.transition_to(MasterLoopNode.GTM_SYSTEM, "Weak GTM feedback -> Re-evaluating channel choices")
            else:
                return self.transition_to(MasterLoopNode.ACTIVATION_RETENTION, "Healthy customer acquisition")

        # Node M: Revenue & Unit Economics Optimization
        elif self.current_node == MasterLoopNode.REVENUE_OPTIMIZATION:
            if signal_type == "bad_economics" and signal_value > 0.6:
                return self.transition_to(MasterLoopNode.BUSINESS_MODEL_DESIGN, "Negative unit economics -> Re-designing value proposition")
            else:
                return self.transition_to(MasterLoopNode.OPERATIONS_SCALING, "Optimized unit economics")

        # Node S: Continuous Reinvention
        elif self.current_node == MasterLoopNode.CONTINUOUS_REINVENTION:
            return self.transition_to(MasterLoopNode.ENVIRONMENTAL_SENSING, "Re-entering Sensing loop for parallel continuous reinvention")

        # Standard sequential transitions
        nodes_list = list(MasterLoopNode)
        current_idx = nodes_list.index(self.current_node)
        next_idx = (current_idx + 1) % len(nodes_list)
        return self.transition_to(nodes_list[next_idx], "Default sequential path")


# =====================================================================
# 2. INTERNAL COGNITIVE LOOPS
# =====================================================================

class WeakSignal(BaseModel):
    """Represents a low-amplitude environmental or customer anomaly."""
    signal_id: str
    description: str
    amplitude: float  # 0.0 to 1.0
    is_structural_shift_symptom: bool = False


class SignalFilter(BaseModel):
    """Filters weak signals and produces falsifiable, structured hypotheses."""
    anomaly_threshold: float = 0.4

    def process_signal(self, signal: WeakSignal) -> Optional[Hypothesis]:
        """Filters a signal. If it exceeds the threshold and represents a structural shift, forms a Hypothesis."""
        if signal.amplitude >= self.anomaly_threshold and signal.is_structural_shift_symptom:
            logger.info(f"SignalFilter: Promoted weak signal '{signal.signal_id}' to a formal Hypothesis.")
            return Hypothesis(
                hypothesis_id=f"hyp_{signal.signal_id}",
                statement=f"Structural Shift Hypothesis derived from: {signal.description}",
                kill_criteria={"max_cost_cents": 1000_00, "min_metric_threshold": 0.15},
                confidence=0.5
            )
        logger.info(f"SignalFilter: Discarded weak signal '{signal.signal_id}' as noise.")
        return None


class Hypothesis(BaseModel):
    """A falsifiable claim with pre-committed kill criteria."""
    hypothesis_id: str
    statement: str
    kill_criteria: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.5


class CheapTest(BaseModel):
    """A sequential, cheap-to-expensive experiment that purchases information before capital is committed."""
    test_id: str
    hypothesis_id: str
    cost_cents: int
    target_metric_observed: float = 0.0

    def execute(self, external_metric_outcome: float) -> Tuple[bool, float]:
        """Executes the test, evaluating against the observed outcome.

        Returns (is_falsified, information_gain).
        """
        self.target_metric_observed = external_metric_outcome
        # Simulated information gain calculation (entropy reduction heuristic)
        info_gain = -0.5 * math.log2(max(0.01, min(0.99, self.target_metric_observed)))
        is_falsified = external_metric_outcome < 0.10  # Arbitrary low outcome falsifies
        return is_falsified, info_gain


class BeliefState(BaseModel):
    """Represents Bayesian conjugate belief distributions (Beta Distribution Parameters)."""
    alpha: float = 10.0
    beta: float = 10.0

    @property
    def expected_probability(self) -> float:
        return self.alpha / (self.alpha + self.beta)

    @property
    def variance(self) -> float:
        return (self.alpha * self.beta) / (((self.alpha + self.beta) ** 2) * (self.alpha + self.beta + 1))


class BeliefUpdater(BaseModel):
    """Sequential Bayesian update mechanism for updating beliefs based on experimental outcomes."""

    def update(self, current_belief: BeliefState, success: bool) -> BeliefState:
        """Applies a conjugate update based on binary success/failure."""
        new_alpha = current_belief.alpha + (1.0 if success else 0.0)
        new_beta = current_belief.beta + (0.0 if success else 1.0)
        logger.info(f"BeliefUpdater: Updated belief from α={current_belief.alpha}, β={current_belief.beta} -> α={new_alpha}, β={new_beta}")
        return BeliefState(alpha=new_alpha, beta=new_beta)


class DecisionRiskType(str, Enum):
    TYPE_I = "TYPE_I"   # Irreversible, high stakes, slow deliberation
    TYPE_II = "TYPE_II" # Reversible, cheap, fast action


class RiskEvaluator(BaseModel):
    """Differentiates Type I (irreversible) from Type II (reversible) risks."""

    def evaluate(self, reversibility_score: float, financial_impact_cents: int) -> DecisionRiskType:
        """Determines risk type. Low reversibility (<0.3) or high cost (> $50k) implies Type I."""
        if reversibility_score < 0.3 or financial_impact_cents > 50000_00:
            return DecisionRiskType.TYPE_I
        return DecisionRiskType.TYPE_II


class OpportunityCostLens(BaseModel):
    """Governs project selection based on compounding potential and structural competitive advantages."""
    min_market_size_billions: float = 1.0
    requires_structural_advantage: bool = True

    def evaluate_project(self, project_name: str, expected_compounding: bool, has_advantage: bool, market_size_billions: float) -> bool:
        """Returns True if the project satisfies elite selection filters, preventing distraction."""
        if not expected_compounding:
            logger.info(f"OpportunityCostLens: Rejected '{project_name}' - does not compound.")
            return False
        if self.requires_structural_advantage and not has_advantage:
            logger.info(f"OpportunityCostLens: Rejected '{project_name}' - lacks structural advantage.")
            return False
        if market_size_billions < self.min_market_size_billions:
            logger.info(f"OpportunityCostLens: Rejected '{project_name}' - market size {market_size_billions}B < {self.min_market_size_billions}B.")
            return False
        logger.info(f"OpportunityCostLens: Passed '{project_name}' selection filter.")
        return True


class MentalModel(BaseModel):
    """A living, falsifiable theory model representing the system's core strategic thesis."""
    name: str
    parameters: Dict[str, float] = Field(default_factory=dict)
    structural_complexity: int = 1
    consecutive_failed_predictions: int = 0
    ossification_score: float = 0.0  # High score means stops updating structure

    def generate_prediction(self, inputs: Dict[str, float]) -> float:
        """Predicts an outcome based on linear-combination parameter heuristic."""
        pred = sum(inputs.get(k, 0.0) * val for k, val in self.parameters.items())
        return pred

    def update_model(self, error: float) -> None:
        """Updates parameters or performs a structural paradigm shift if error persists."""
        if abs(error) < 0.15:
            # Fast parameter tuning
            for k in self.parameters:
                self.parameters[k] += 0.05 * error
            self.consecutive_failed_predictions = 0
            logger.info(f"MentalModel '{self.name}': Parameter tuning updated values slightly.")
        else:
            self.consecutive_failed_predictions += 1
            # Check for structural paradigm shift threshold
            if self.consecutive_failed_predictions >= 3:
                if self.ossification_score < 0.8:
                    # Perform structural paradigm shift (e.g. increase complexity, shift model structure)
                    self.structural_complexity += 1
                    self.consecutive_failed_predictions = 0
                    logger.warning(f"MentalModel '{self.name}': PARADIGM SHIFT triggered. Complexity increased to {self.structural_complexity}.")
                else:
                    logger.error(f"MentalModel '{self.name}': MODEL OSSIFICATION detected! Failed to shift structure due to ossification.")


# =====================================================================
# 3. EXTERNAL BUSINESS LOOPS
# =====================================================================

class BusinessLoop(BaseModel):
    """An operational feedback loop in the company systems-thinking model."""
    name: str
    inputs: List[str] = Field(default_factory=list)
    outputs: List[str] = Field(default_factory=list)
    feedback_signal: str
    core_kpis: Dict[str, float] = Field(default_factory=dict)
    failure_mode: str


class BusinessLoopCoupler(BaseModel):
    """Manages the 13 coupled operational loops and routes flow dynamics between them."""
    loops: Dict[str, BusinessLoop] = Field(default_factory=dict)
    stocks: Dict[str, float] = Field(default_factory=dict)  # cash, talent, trust, data

    def register_loop(self, loop: BusinessLoop) -> None:
        self.loops[loop.name] = loop

    def execute_tick(self) -> Dict[str, float]:
        """Simulates coupled feedback loops shifting stock values over time.

        Pricing (ARPU) -> Financial budget -> Hiring budget -> Product velocity.
        """
        logger.info("BusinessLoopCoupler: Simulating operational coupled loop tick.")

        arpu = self.loops.get("Pricing", BusinessLoop(name="Pricing", feedback_signal="", failure_mode="")).core_kpis.get("ARPU", 10.0)
        conversion = self.loops.get("Sales", BusinessLoop(name="Sales", feedback_signal="", failure_mode="")).core_kpis.get("conversion_rate", 0.05)
        leads = self.loops.get("Marketing", BusinessLoop(name="Marketing", feedback_signal="", failure_mode="")).core_kpis.get("traffic", 1000.0)

        # Inflow to cash stock based on Pricing & Sales loops
        revenue_inflow = leads * conversion * arpu
        self.stocks["cash"] = self.stocks.get("cash", 10000.0) + revenue_inflow

        # Financial loop allocates budget to hiring
        financial_health = self.loops.get("Financial", BusinessLoop(name="Financial", feedback_signal="", failure_mode=""))
        burn_multiple = financial_health.core_kpis.get("burn_multiple", 1.5)
        hiring_budget = max(0.0, self.stocks["cash"] * 0.3 / burn_multiple)

        # Hiring loop consumes hiring_budget to increase talent stock
        hiring_loop = self.loops.get("Hiring", BusinessLoop(name="Hiring", feedback_signal="", failure_mode=""))
        time_to_fill = hiring_loop.core_kpis.get("time_to_fill_days", 30.0)
        talent_gained = hiring_budget / (time_to_fill * 100.0)
        self.stocks["talent"] = self.stocks.get("talent", 5.0) + talent_gained

        # Talent stock drives Product loop velocity
        product_loop = self.loops.get("Product", BusinessLoop(name="Product", feedback_signal="", failure_mode=""))
        product_loop.core_kpis["velocity"] = self.stocks["talent"] * 2.0

        return self.stocks


# =====================================================================
# 4. CUSTOMER JOURNEY (Full Lifecycle)
# =====================================================================

class CustomerJourneyStageType(str, Enum):
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


class CustomerJourneyStage(BaseModel):
    """Models a single stage of the 15-stage customer lifecycle."""
    stage_type: CustomerJourneyStageType
    founder_objective: str
    customer_psychology: str
    key_metric_name: str
    metric_value: float = 0.0
    common_mistake: str
    optimization_lever: str


class CustomerJourney(BaseModel):
    """Coordinates customer progression and identifies optimization leverage points."""
    stages: Dict[CustomerJourneyStageType, CustomerJourneyStage] = Field(default_factory=dict)

    def transition_cohort(self, stage_from: CustomerJourneyStageType, stage_to: CustomerJourneyStageType, volume: float, efficiency: float) -> float:
        """Moves customer volume between lifecycle stages based on metric efficiency."""
        from_stage = self.stages.get(stage_from)
        to_stage = self.stages.get(stage_to)
        if not from_stage or not to_stage:
            return 0.0

        transitioned_volume = volume * efficiency
        to_stage.metric_value += transitioned_volume
        logger.info(f"CustomerJourney: Transitioned {transitioned_volume:.1f} users from {stage_from.value} -> {stage_to.value}")
        return transitioned_volume


# =====================================================================
# 5. GO-TO-MARKET SYSTEM (Integrated, Non-Functional)
# =====================================================================

class ChannelType(str, Enum):
    PLG = "Product-Led Growth"
    SLG = "Sales-Led Growth"
    CLG = "Community-Led Growth"


class GTMSystem(BaseModel):
    """Represents the GTM strategic alignment flow."""
    positioning_axes: List[str] = Field(default_factory=list)
    pricing_arpu_cents: int
    product_complexity: float  # 0.0 to 1.0 (self-serve vs enterprise)
    selected_channel: Optional[ChannelType] = None

    def select_optimal_distribution_channel(self) -> ChannelType:
        """Determines the correct GTM channel based on pricing and product complexity (Bezos/Collison style)."""
        # Low price, low complexity -> PLG
        if self.pricing_arpu_cents < 100_00 and self.product_complexity < 0.4:
            self.selected_channel = ChannelType.PLG
        # High price, high complexity -> SLG
        elif self.pricing_arpu_cents >= 1000_00 and self.product_complexity >= 0.6:
            self.selected_channel = ChannelType.SLG
        # Network effect / moderate price -> CLG
        else:
            self.selected_channel = ChannelType.CLG

        logger.info(f"GTMSystem: Selected distribution channel {self.selected_channel.value} based on ARPU and Complexity.")
        return self.selected_channel


# =====================================================================
# 6. COMPANY GROWTH SYSTEM
# =====================================================================

class GrowthStageType(str, Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "Product-Market Fit"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    MARKET_LEADERSHIP = "Market Leadership"


class GrowthStage(BaseModel):
    """An era of organizational growth with constraints and key objectives."""
    stage_type: GrowthStageType
    primary_objective: str
    org_change: str
    decision_making_change: str
    capital_allocation: str
    key_risk: str
    core_metric: str
    binding_constraint: str


class CompanyGrowthTracker(BaseModel):
    """Tracks and scores organizational maturity across the 9 major growth stages."""
    current_stage: GrowthStageType = GrowthStageType.IDEA
    scores: Dict[str, float] = Field(default_factory=dict)

    def evaluate_transition(self) -> GrowthStageType:
        """Scores metrics and triggers growth-stage progression, checking against premature scaling."""
        if self.current_stage == GrowthStageType.IDEA:
            if self.scores.get("validated_learnings", 0.0) >= 5.0:
                self.current_stage = GrowthStageType.VALIDATION
        elif self.current_stage == GrowthStageType.VALIDATION:
            if self.scores.get("paying_customers", 0.0) >= 10.0:
                self.current_stage = GrowthStageType.STARTUP
        elif self.current_stage == GrowthStageType.STARTUP:
            if self.scores.get("retention_rate", 0.0) >= 0.40:
                self.current_stage = GrowthStageType.PMF
        elif self.current_stage == GrowthStageType.PMF:
            if self.scores.get("ltv_cac_ratio", 0.0) >= 3.0:
                self.current_stage = GrowthStageType.GROWTH
        elif self.current_stage == GrowthStageType.GROWTH:
            if self.scores.get("nrr_rate", 0.0) >= 1.15:
                self.current_stage = GrowthStageType.SCALE

        logger.info(f"CompanyGrowthTracker: Evaluated state. Current Stage is {self.current_stage.value}")
        return self.current_stage


# =====================================================================
# 7. STRATEGIC THINKING
# =====================================================================

class CostCurveTracker(BaseModel):
    """Tracks historical costs of enabling infrastructure to predict viability sweet spots."""
    technology_name: str
    historical_cost_per_unit: Dict[int, float] = Field(default_factory=dict)  # Year -> cost

    def predict_viability_year(self, target_economic_cost: float) -> int:
        """Extrapolates exponential cost decay to find the crossing point of economic viability."""
        if len(self.historical_cost_per_unit) < 2:
            return 2026 # Default baseline

        years = sorted(self.historical_cost_per_unit.keys())
        y1, y2 = years[0], years[-1]
        c1, c2 = self.historical_cost_per_unit[y1], self.historical_cost_per_unit[y2]

        if c1 <= c2 or c1 <= 0 or c2 <= 0:
            return 2026

        # log(c) = a * year + b
        a = (math.log(c2) - math.log(c1)) / (y2 - y1)
        b = math.log(c1) - a * y1

        # Target cost crossing: year = (log(target) - b) / a
        predicted_year = (math.log(target_economic_cost) - b) / a
        return int(math.ceil(predicted_year))


class MoatAuditor(BaseModel):
    """Tracks and scores the strength and durability of the 6 competitive moats."""
    moat_scores: Dict[str, float] = Field(
        default_factory=lambda: {
            "network_effects": 0.0,
            "switching_costs": 0.0,
            "scale_economies": 0.0,
            "brand_trust": 0.0,
            "regulatory_ip": 0.0,
            "counter_positioning": 0.0
        }
    )

    def calculate_total_moat_index(self) -> float:
        """Returns normalized mean moat value across Porter / Helmer axes."""
        return sum(self.moat_scores.values()) / 6.0


# =====================================================================
# 8. FAILURE MODE ANALYSIS
# =====================================================================

class FailureModeType(str, Enum):
    WRONG_PROBLEM = "Solving the wrong problem"
    BUILD_WITHOUT_VALIDATION = "Building before validating"
    WEAK_POSITIONING = "Weak positioning"
    POOR_PRICING = "Poor pricing"
    DISTRIBUTION_FAILURE = "Distribution failure"
    NO_PMF = "Lack of product-market fit"
    ORG_BOTTLENECK = "Organizational bottlenecks"
    FOUNDER_BIAS = "Founder bias"
    PREMATURE_SCALING = "Scaling prematurely"
    CAPITAL_MISALLOCATION = "Capital misallocation"


class FailureModeMonitor(BaseModel):
    """Continuously monitors metrics, raises warnings, and returns recovery scripts."""

    def analyze_failures(self, metrics: Dict[str, float]) -> List[Tuple[FailureModeType, str]]:
        """Scans metrics and identifies active organizational failure modes."""
        anomalies = []
        if metrics.get("engagement_rate", 1.0) < 0.10 and metrics.get("customer_satisfaction_score", 5.0) >= 4.0:
            anomalies.append((FailureModeType.WRONG_PROBLEM, "Return to root-cause JTBD interviews."))
        if metrics.get("build_velocity", 0.0) > 10.0 and metrics.get("conversions", 10.0) == 0.0:
            anomalies.append((FailureModeType.BUILD_WITHOUT_VALIDATION, "Enforce strict validation gate before build resourcing."))
        if metrics.get("cac_payback_months", 0.0) > 24.0:
            anomalies.append((FailureModeType.DISTRIBUTION_FAILURE, "Systematically test distribution channels against buyer behavior."))
        if metrics.get("burn_multiple", 0.0) > 3.0 and metrics.get("ltv_cac_ratio", 5.0) < 1.5:
            anomalies.append((FailureModeType.PREMATURE_SCALING, "Cut spending immediately; focus on cohort retention stabilization."))

        return anomalies


# =====================================================================
# 10. INTEGRATED AI-DRIVEN OPERATING SYSTEM ENGINE
# =====================================================================

class SensingAgent(BaseModel):
    """Anomalous pattern detection against the baseline model."""
    def detect_anomalies(self, data: List[float], baseline: float) -> bool:
        if not data:
            return False
        mean = sum(data) / len(data)
        return abs(mean - baseline) > (0.25 * baseline)


class HypothesisEngine(BaseModel):
    """Translates anomalies into falsifiable claims."""
    def generate_hypothesis(self, description: str) -> Hypothesis:
        return Hypothesis(
            hypothesis_id=f"hyp_{hash(description) % 10000}",
            statement=f"Falsifiable hypothesis for anomaly: {description}",
            kill_criteria={"max_budget_cents": 500_00},
            confidence=0.5
        )


class ValidationAgent(BaseModel):
    """Scores economic viability through low-cost checks."""
    def score_viability(self, test: CheapTest) -> float:
        # returns scoring index between 0.0 and 1.0
        return min(1.0, test.target_metric_observed / 0.5)


class GTMSimulator(BaseModel):
    """Predicts channel alignment score."""
    def evaluate_alignment(self, channel: ChannelType, conversion: float) -> float:
        if channel == ChannelType.PLG:
            return conversion * 1.5
        return conversion * 1.0


class CapitalAllocator(BaseModel):
    """Optimizes investment across competing experiments under opportunity cost."""
    def allocate(self, initiatives: List[Dict[str, Any]], total_budget_cents: int) -> Dict[str, int]:
        """Rank-orders and distributes capital based on expected return."""
        allocations = {}
        if not initiatives:
            return allocations

        # Sort initiatives by expected ROI descending
        sorted_in = sorted(initiatives, key=lambda x: x.get("expected_return", 0.0), reverse=True)
        remaining_budget = total_budget_cents

        for item in sorted_in:
            cost = item.get("required_cost_cents", 100_00)
            if remaining_budget >= cost:
                allocations[item["id"]] = cost
                remaining_budget -= cost
            else:
                allocations[item["id"]] = remaining_budget
                remaining_budget = 0
                break

        return allocations


class GovernanceSafetyLayer(BaseModel):
    """Guarantees safety-critical parameters and enforces kill-criteria gates."""
    min_runway_months: float = 6.0

    def audit_execution(self, runway_months: float, is_type_i: bool, is_approved_by_human: bool) -> bool:
        """Returns True if execution passes security audits."""
        if runway_months < self.min_runway_months:
            logger.error("GovernanceSafetyLayer: BLOCKING execution due to low runway.")
            return False
        if is_type_i and not is_approved_by_human:
            logger.error("GovernanceSafetyLayer: BLOCKING execution. Type I decisions require human sign-off.")
            return False
        return True


class IntegratedEOSEngine(BaseModel):
    """Authoritative, unified manager for the first-principles EOS runtime."""
    master_loop: MasterLoop = Field(default_factory=MasterLoop)
    belief_state: BeliefState = Field(default_factory=BeliefState)
    growth_tracker: CompanyGrowthTracker = Field(default_factory=CompanyGrowthTracker)
    moat_auditor: MoatAuditor = Field(default_factory=MoatAuditor)
    failure_monitor: FailureModeMonitor = Field(default_factory=FailureModeMonitor)
    safety_layer: GovernanceSafetyLayer = Field(default_factory=GovernanceSafetyLayer)

    # Agents
    sensing_agent: SensingAgent = Field(default_factory=SensingAgent)
    hypothesis_engine: HypothesisEngine = Field(default_factory=HypothesisEngine)
    validation_agent: ValidationAgent = Field(default_factory=ValidationAgent)
    gtm_simulator: GTMSimulator = Field(default_factory=GTMSimulator)
    capital_allocator: CapitalAllocator = Field(default_factory=CapitalAllocator)

    def run_strategic_audit(self, context_metrics: Dict[str, float]) -> List[str]:
        """Runs the failure monitor, checks growth state, and triggers self-disruption if required."""
        alerts = []
        failures = self.failure_monitor.analyze_failures(context_metrics)
        for fail_type, correction in failures:
            msg = f"WARNING: Active Failure Mode [{fail_type.value}] detected. Correction: {correction}"
            alerts.append(msg)
            logger.warning(msg)

        # Check self-disruption/reinvention triggers
        if self.growth_tracker.current_stage == GrowthStageType.MARKET_LEADERSHIP:
            alerts.append("TRIGGER: Continuous Reinvention activated for Market Leadership defense.")
            self.master_loop.transition_to(MasterLoopNode.CONTINUOUS_REINVENTION, "Leadership reinvention trigger")

        return alerts
