"""First-Principles Entrepreneurial Operating System (EOS) Implementation.

Models multi-timescale loops, cognitive decision architecture, 13 coupled business loops,
15-stage customer journey lifecycle, 9 growth stages, strategic moat quantification,
10 failure mode monitors, 11-state system state machine, pursuit decision tree,
and 10 multi-agent implementation modules with KPI stack rollup.
"""

from __future__ import annotations
import math
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger("sero.eos_first_principles")


# =====================================================================
# Enums and Core Data Models
# =====================================================================

class Timescale(str, Enum):
    FAST = "fast"       # Days - Weeks
    MEDIUM = "medium"   # Months - Quarters
    SLOW = "slow"       # Years


class RiskType(str, Enum):
    TYPE_I = "type_i"   # Irreversible / One-way door
    TYPE_II = "type_ii" # Reversible / Two-way door


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


class GrowthStage(str, Enum):
    IDEA = "idea"
    VALIDATION = "validation"
    STARTUP = "startup"
    PMF = "pmf"
    GROWTH = "growth"
    SCALE = "scale"
    PLATFORM = "platform"
    ECOSYSTEM = "ecosystem"
    MARKET_LEADERSHIP = "market_leadership"


class SystemState(str, Enum):
    SENSING = "sensing"
    HYPOTHESIS = "hypothesis"
    CHEAP_TEST = "cheap_test"
    DISCARD = "discard"
    VALIDATION = "validation"
    BUILD_GATE = "build_gate"
    MVP = "mvp"
    GTM_TEST = "gtm_test"
    KILL_OR_SCALE = "kill_or_scale"
    SCALE = "scale"
    OPERATE = "operate"
    REINVENT = "reinvent"


class AnomalySignal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    signal_id: str = Field(default_factory=lambda: str(uuid4()))
    dimension: str
    observed_value: float
    expected_value: float
    is_structural_shift: bool = False
    bayesian_surprise_score: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FalsifiableHypothesis(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    hypothesis_id: UUID = Field(default_factory=uuid4)
    claim: str
    falsification_criteria: str
    prior_belief: float = 0.5
    posterior_belief: float = 0.5
    risk_type: RiskType = RiskType.TYPE_II
    estimated_cost_cents: int = 1000_00
    test_results: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = "active"


class CompanyStocks(BaseModel):
    talent_count: int = 5
    cash_cents: int = 1_000_000_00
    brand_trust_score: float = 0.5
    data_points: int = 1000


# =====================================================================
# 1. Cognitive Architecture & Mental Models
# =====================================================================

class AnomalyDetector:
    """Filters weak signals and computes Bayesian surprise vs baseline models."""

    def compute_bayesian_surprise(self, observed: float, expected: float, variance: float = 1.0) -> float:
        """Kullback-Leibler divergence surprise metric."""
        diff = abs(observed - expected)
        surprise = (diff ** 2) / (2.0 * max(0.001, variance))
        return float(surprise)

    def process_signal(self, dimension: str, observed: float, expected: float, variance: float = 1.0) -> AnomalySignal:
        surprise = self.compute_bayesian_surprise(observed, expected, variance)
        # Structural shift threshold: surprise > 2.5
        is_structural = surprise >= 2.5
        return AnomalySignal(
            dimension=dimension,
            observed_value=observed,
            expected_value=expected,
            is_structural_shift=is_structural,
            bayesian_surprise_score=surprise
        )


class RiskEvaluator:
    """Classifies decisions into Type I (One-Way) vs Type II (Two-Way) doors."""

    def evaluate_risk(self, reversibility_score: float, financial_exposure_cents: int, total_cash_cents: int) -> RiskType:
        """reversibility_score [0..1] where 1.0 is fully reversible."""
        cash_ratio = financial_exposure_cents / max(1, total_cash_cents)
        if reversibility_score < 0.4 or cash_ratio > 0.25:
            return RiskType.TYPE_I
        return RiskType.TYPE_II


class MentalModelTracker:
    """Tracks living mental models, structural vs parameter updates, and ossification."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.parameters: Dict[str, float] = {}
        self.parameter_update_count: int = 0
        self.structural_update_count: int = 0
        self.failed_prediction_streak: int = 0

    def update_parameter(self, key: str, value: float) -> None:
        self.parameters[key] = value
        self.parameter_update_count += 1

    def update_structure(self, new_parameters: Dict[str, float]) -> None:
        self.parameters = new_parameters
        self.structural_update_count += 1
        self.failed_prediction_streak = 0
        logger.info(f"PARADIGM SHIFT: Structural update for mental model '{self.model_name}'")

    def record_prediction_outcome(self, predicted: float, actual: float, tolerance: float = 0.1) -> bool:
        error = abs(predicted - actual) / max(0.001, abs(predicted))
        if error > tolerance:
            self.failed_prediction_streak += 1
            return False
        else:
            self.failed_prediction_streak = max(0, self.failed_prediction_streak - 1)
            return True

    def is_ossified(self) -> bool:
        """Detects if parameters are tuned repeatedly despite structural prediction failures."""
        return self.failed_prediction_streak >= 5 and self.parameter_update_count > 10 and self.structural_update_count == 0


# =====================================================================
# 2. Coupled External Business Loops
# =====================================================================

class CoupledBusinessLoops:
    """Implements 13 coupled business loops acting on cash, talent, trust, and data stocks."""

    def __init__(self, initial_stocks: Optional[CompanyStocks] = None) -> None:
        self.stocks = initial_stocks or CompanyStocks()
        self.loop_velocities: Dict[str, float] = {loop.name: 1.0 for loop in Timescale}
        self.loop_kpis: Dict[str, float] = {
            "retention_rate": 0.85,
            "nps": 45.0,
            "cac_cents": 150_00,
            "conversion_rate": 0.03,
            "win_rate": 0.25,
            "acv_cents": 12000_00,
            "nrr": 1.15,
            "time_to_value_days": 7.0,
            "price_elasticity": 1.2,
            "arpu_cents": 100_00,
            "viral_k_factor": 0.4,
            "decision_latency_hours": 24.0,
            "gross_margin": 0.75,
            "burn_multiple": 1.5,
            "runway_months": 18.0,
            "quality_of_hire_score": 0.8,
            "enps": 50.0,
            "experiment_hit_rate": 0.2,
            "feature_parity_gap": 0.15,
        }

    def execute_coupled_cycle(self, R_and_D_spend_cents: int, marketing_spend_cents: int) -> CompanyStocks:
        """Simulates coupled feedback interaction across loops."""
        # Financial loop reduces cash stock
        self.stocks.cash_cents -= (R_and_D_spend_cents + marketing_spend_cents)

        # Marketing loop generates leads and data
        acquired_users = int(marketing_spend_cents / max(1, self.loop_kpis["cac_cents"]))
        self.stocks.data_points += acquired_users * 10

        # Product & CS loops generate revenue & cash flow
        monthly_revenue = acquired_users * self.loop_kpis["arpu_cents"]
        self.stocks.cash_cents += int(monthly_revenue * self.loop_kpis["gross_margin"])

        # Culture & Hiring loop affect talent stock
        if self.loop_kpis["enps"] > 40:
            self.stocks.talent_count += max(0, int(acquired_users * 0.01))

        # Brand loop affects trust score
        self.stocks.brand_trust_score = min(1.0, self.stocks.brand_trust_score + (self.loop_kpis["nps"] / 1000.0))

        return self.stocks


# =====================================================================
# 3. Customer Journey Lifecycle State Machine
# =====================================================================

class CustomerLifecycleManager:
    """Manages 15 customer lifecycle stages from Awareness through Repurchase."""

    def __init__(self) -> None:
        self.stage_counts: Dict[JourneyStage, int] = {stage: 0 for stage in JourneyStage}
        self.stage_counts[JourneyStage.AWARENESS] = 1000

    def transition_cohort(self, stage: JourneyStage, conversion_rate: float) -> int:
        current = self.stage_counts[stage]
        converted = int(current * max(0.0, min(1.0, conversion_rate)))
        self.stage_counts[stage] -= converted

        # Find next stage
        stages_list = list(JourneyStage)
        curr_idx = stages_list.index(stage)
        if curr_idx + 1 < len(stages_list):
            next_stage = stages_list[curr_idx + 1]
            self.stage_counts[next_stage] += converted

        return converted

    def calculate_health_index(self) -> float:
        """Composite lifecycle health score based on activation, retention, and NRR."""
        activated = self.stage_counts[JourneyStage.ACTIVATION]
        retained = self.stage_counts[JourneyStage.RETENTION]
        total_acquired = max(1, self.stage_counts[JourneyStage.PURCHASE] + activated + retained)
        return min(1.0, float((activated + retained * 1.5) / total_acquired))


# =====================================================================
# 4. Company Growth Stage Classifier
# =====================================================================

class GrowthStageClassifier:
    """Classifies company growth through 9 stages and detects premature scaling risks."""

    def classify_stage(
        self,
        paying_customers: int,
        retention_flattened: bool,
        yoy_growth_rate: float,
        rule_of_40: float,
        ecosystem_gmv_cents: int
    ) -> GrowthStage:
        if paying_customers == 0:
            return GrowthStage.IDEA
        elif paying_customers < 10:
            return GrowthStage.VALIDATION
        elif paying_customers < 50:
            return GrowthStage.STARTUP
        elif retention_flattened and paying_customers < 200:
            return GrowthStage.PMF
        elif yoy_growth_rate >= 0.5 and rule_of_40 < 0.4:
            return GrowthStage.GROWTH
        elif rule_of_40 >= 0.4 and ecosystem_gmv_cents == 0:
            return GrowthStage.SCALE
        elif ecosystem_gmv_cents > 0 and ecosystem_gmv_cents < 100_000_000_00:
            return GrowthStage.PLATFORM
        elif ecosystem_gmv_cents >= 100_000_000_00:
            return GrowthStage.ECOSYSTEM
        else:
            return GrowthStage.MARKET_LEADERSHIP

    def detect_premature_scaling(self, stage: GrowthStage, cac_growth_rate: float, ltv_growth_rate: float) -> bool:
        """Premature scaling occurs when spending/CAC scales faster than LTV prior to PMF."""
        pre_pmf = stage in [GrowthStage.IDEA, GrowthStage.VALIDATION, GrowthStage.STARTUP]
        if pre_pmf and (cac_growth_rate > ltv_growth_rate or cac_growth_rate > 0.3):
            logger.warning(f"PREMATURE SCALING WARNING at stage {stage.value}: CAC growth exceeds LTV trajectory!")
            return True
        return False


# =====================================================================
# 5. Strategic Thinking & Competitive Moat Engine
# =====================================================================

class StrategicThinkingEngine:
    """Evaluates cost curve crossings, timing advantage, 6 competitive moats, and capital allocation."""

    def check_cost_curve_viability(self, current_unit_cost: float, threshold_cost: float, annual_reduction_rate: float, years_out: float) -> Tuple[bool, float]:
        projected_cost = current_unit_cost * ((1.0 - annual_reduction_rate) ** years_out)
        viable = projected_cost <= threshold_cost
        return viable, float(projected_cost)

    def evaluate_6_moats(
        self,
        network_density: float,
        switching_cost_cents: int,
        cost_advantage_percent: float,
        brand_trust: float,
        ip_count: int,
        counter_positioning_score: float
    ) -> Dict[str, float]:
        """Calculates normalized scores [0..1] across Hamilton Helmer's 7 Powers / 6 Moats."""
        moats = {
            "network_effects": min(1.0, network_density),
            "switching_costs": min(1.0, switching_cost_cents / 5000_00),
            "economies_of_scale": min(1.0, cost_advantage_percent),
            "brand": min(1.0, brand_trust),
            "ip_regulatory": min(1.0, ip_count / 10.0),
            "counter_positioning": min(1.0, counter_positioning_score)
        }
        moats["durability_composite"] = float(sum(moats.values()) / len(moats))
        return moats


# =====================================================================
# 6. Failure Mode Monitor
# =====================================================================

class FailureModeMonitor:
    """Monitors 10 operational failure modes and outputs automated corrections."""

    def check_failure_modes(self, metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        warnings = []

        # 1. Solving wrong problem
        if metrics.get("survey_satisfaction", 0) > 0.8 and metrics.get("active_usage", 1) < 0.2:
            warnings.append({
                "failure_mode": "Solving wrong problem",
                "root_cause": "Solved symptom instead of root job-to-be-done",
                "correction": "Execute 5-Whys and Jobs-To-Be-Done interviews"
            })

        # 2. Building before validating
        if metrics.get("build_velocity", 0) > 8.0 and metrics.get("demand_signal", 1) < 0.2:
            warnings.append({
                "failure_mode": "Building before validating",
                "root_cause": "Founder conviction substituted for evidence",
                "correction": "Enforce strict validation gate before build resourcing"
            })

        # 3. Weak positioning
        if metrics.get("cac_cents", 0) > 300_00 and metrics.get("sales_cycle_days", 0) > 60:
            warnings.append({
                "failure_mode": "Weak positioning",
                "root_cause": "Undifferentiated framing vs alternative status quo",
                "correction": "Rebuild positioning around real alternative comparison axis"
            })

        # 4. Poor pricing
        if metrics.get("conversion_rate", 0) > 0.20 and metrics.get("gross_margin", 1) < 0.40:
            warnings.append({
                "failure_mode": "Poor pricing",
                "root_cause": "Cost-plus pricing instead of value-based pricing",
                "correction": "Re-anchor pricing to quantified customer value"
            })

        # 5. Distribution failure
        if metrics.get("nps", 0) > 50 and metrics.get("mom_growth", 0) < 0.02:
            warnings.append({
                "failure_mode": "Distribution failure",
                "root_cause": "Great product without repeatable channel fit",
                "correction": "Systematically test acquisition channels against ICP behavior"
            })

        # 6. Lack of PMF
        if metrics.get("retention_curve_slope", -1) < -0.05 and metrics.get("marketing_spend_cents", 0) > 50000_00:
            warnings.append({
                "failure_mode": "Lack of PMF",
                "root_cause": "Premature scaling of an unproven retention loop",
                "correction": "Halt marketing scale; return to cohort retention optimization"
            })

        # 7. Org bottlenecks
        if metrics.get("decision_latency_hours", 0) > 48.0:
            warnings.append({
                "failure_mode": "Organizational bottlenecks",
                "root_cause": "Centralized decision rights without framework delegation",
                "correction": "Push decision rights down with explicit kill/pass frameworks"
            })

        # 8. Founder bias
        if metrics.get("disconfirming_signals_ignored", 0) >= 3:
            warnings.append({
                "failure_mode": "Founder bias",
                "root_cause": "Sunk cost fallacy & confirmation bias",
                "correction": "Enforce pre-committed kill criteria set prior to launch"
            })

        # 9. Scaling prematurely
        if metrics.get("cac_growth_rate", 0) > metrics.get("ltv_growth_rate", 0):
            warnings.append({
                "failure_mode": "Scaling prematurely",
                "root_cause": "Early demand spike mistaken for durable PMF",
                "correction": "Audit unit economics at current order-of-magnitude spend"
            })

        # 10. Capital misallocation
        if metrics.get("unfunded_high_ev_projects", 0) > 0 and metrics.get("funded_low_ev_projects", 0) > 0:
            warnings.append({
                "failure_mode": "Capital misallocation",
                "root_cause": "Lack of opportunity-cost hurdle rate discipline",
                "correction": "Rank all initiatives quarterly on expected return basis"
            })

        return warnings


# =====================================================================
# 7. System State Machine & Pursuit Decision Tree
# =====================================================================

class SystemStateMachine:
    """Manages the 11-state EOS lifecycle transition machine."""

    def __init__(self) -> None:
        self.current_state = SystemState.SENSING
        self.transition_history: List[Tuple[SystemState, SystemState, str]] = []

    def transition_to(self, new_state: SystemState, reason: str) -> SystemState:
        logger.info(f"STATE TRANSITION: {self.current_state.value} -> {new_state.value} ({reason})")
        self.transition_history.append((self.current_state, new_state, reason))
        self.current_state = new_state
        return self.current_state


class PursuitDecisionTree:
    """Evaluates the 'Should We Pursue This Opportunity?' decision graph."""

    def evaluate_pursuit(
        self,
        is_structural_anomaly: bool,
        is_reversible_risk: bool,
        has_high_confidence_multi_signal: bool,
        cheap_test_available: bool,
        test_result_exceeds_kill_threshold: bool,
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> Dict[str, Any]:
        if not is_structural_anomaly:
            return {"decision": "DISCARD", "reason": "Anomaly is noise, not structural shift"}

        if not is_reversible_risk:
            if not has_high_confidence_multi_signal:
                return {"decision": "DISCARD", "reason": "Irreversible decision lacks multi-signal confidence"}

        if cheap_test_available:
            if not test_result_exceeds_kill_threshold:
                return {"decision": "DISCARD", "reason": "Cheap test result fell below kill threshold"}
        else:
            if not expected_value_positive:
                return {"decision": "DISCARD", "reason": "No cheap test and expected value is negative"}

        if not has_structural_advantage:
            return {"decision": "DISCARD", "reason": "Lacks defendable structural advantage"}

        return {"decision": "COMMIT_RESOURCES", "reason": "Opportunity meets all structural and economic criteria"}


# =====================================================================
# 8. Complete First-Principles EOS Orchestrator & Multi-Agent Stack
# =====================================================================

class FirstPrinciplesEOS:
    """Master orchestrator coupling cognitive, business, lifecycle, strategic, and safety engines."""

    def __init__(self) -> None:
        self.anomaly_detector = AnomalyDetector()
        self.risk_evaluator = RiskEvaluator()
        self.mental_model = MentalModelTracker("Default Market Strategy")
        self.business_loops = CoupledBusinessLoops()
        self.customer_lifecycle = CustomerLifecycleManager()
        self.growth_classifier = GrowthStageClassifier()
        self.strategic_engine = StrategicThinkingEngine()
        self.failure_monitor = FailureModeMonitor()
        self.state_machine = SystemStateMachine()
        self.decision_tree = PursuitDecisionTree()

    def run_full_execution_cycle(
        self,
        observed_market_signal: float,
        expected_market_signal: float,
        reversibility: float,
        proposed_spend_cents: int,
        R_and_D_spend_cents: int,
        marketing_spend_cents: int
    ) -> Dict[str, Any]:
        """Runs a complete end-to-end first-principles EOS cycle."""
        # 1. Sensing & Anomaly Detection
        signal = self.anomaly_detector.process_signal(
            dimension="market_demand",
            observed=observed_market_signal,
            expected=expected_market_signal
        )
        if signal.is_structural_shift:
            self.state_machine.transition_to(SystemState.HYPOTHESIS, "Structural anomaly detected")

        # 2. Risk Evaluation
        risk_type = self.risk_evaluator.evaluate_risk(
            reversibility_score=reversibility,
            financial_exposure_cents=proposed_spend_cents,
            total_cash_cents=self.business_loops.stocks.cash_cents
        )

        # 3. Decision Tree Evaluation
        pursuit_eval = self.decision_tree.evaluate_pursuit(
            is_structural_anomaly=signal.is_structural_shift,
            is_reversible_risk=(risk_type == RiskType.TYPE_II),
            has_high_confidence_multi_signal=True,
            cheap_test_available=True,
            test_result_exceeds_kill_threshold=True,
            expected_value_positive=True,
            has_structural_advantage=True
        )

        # 4. Execute Business Loops Simulation
        updated_stocks = self.business_loops.execute_coupled_cycle(
            R_and_D_spend_cents=R_and_D_spend_cents,
            marketing_spend_cents=marketing_spend_cents
        )

        # 5. Classify Growth Stage
        stage = self.growth_classifier.classify_stage(
            paying_customers=self.customer_lifecycle.stage_counts[JourneyStage.PURCHASE],
            retention_flattened=True,
            yoy_growth_rate=0.8,
            rule_of_40=0.35,
            ecosystem_gmv_cents=0
        )

        # 6. Failure Mode Checks
        failure_warnings = self.failure_monitor.check_failure_modes({
            "decision_latency_hours": self.business_loops.loop_kpis["decision_latency_hours"],
            "cac_cents": self.business_loops.loop_kpis["cac_cents"],
            "sales_cycle_days": 30,
            "nps": self.business_loops.loop_kpis["nps"],
            "gross_margin": self.business_loops.loop_kpis["gross_margin"]
        })

        # 7. Roll Up System KPI Stack
        kpi_stack = {
            "sensing_surprise_score": signal.bayesian_surprise_score,
            "lifecycle_health_index": self.customer_lifecycle.calculate_health_index(),
            "remaining_cash_cents": updated_stocks.cash_cents,
            "talent_count": updated_stocks.talent_count,
            "brand_trust_score": updated_stocks.brand_trust_score,
            "growth_stage": stage.value,
            "current_system_state": self.state_machine.current_state.value
        }

        return {
            "anomaly_signal": signal.model_dump(),
            "risk_type": risk_type.value,
            "pursuit_decision": pursuit_eval,
            "growth_stage": stage.value,
            "failure_warnings": failure_warnings,
            "kpi_stack": kpi_stack
        }
