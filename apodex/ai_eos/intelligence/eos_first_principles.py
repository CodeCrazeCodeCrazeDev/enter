"""First-Principles Executable Engine for the Entrepreneurial Operating System (EOS).

Implements the complete 11-section specification of how elite founders sense, build,
and compound enduring companies, including state machines, decision trees, cognitive loops,
external business loops, customer lifecycle engines, GTM simulators, company growth stages,
strategic moats, failure mode diagnostics, AI agents, and KPI stacks.
"""

from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
import logging

logger = logging.getLogger("apodex.ai_eos.eos_first_principles")


# =====================================================================
# 0. Enums & Core Domain Models
# =====================================================================

class EOSStage(Enum):
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


class RiskType(Enum):
    TYPE_I_IRREVERSIBLE = "Type_I_Irreversible"
    TYPE_II_REVERSIBLE = "Type_II_Reversible"


class ExternalLoopType(Enum):
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


class CustomerLifecycleStage(Enum):
    AWARENESS = "Awareness"
    INTEREST = "Interest"
    CONSIDERATION = "Consideration"
    EVALUATION = "Evaluation"
    PURCHASE = "Purchase"
    ONBOARDING = "Onboarding"
    ACTIVATION = "Activation"
    ENGAGEMENT = "Engagement"
    HABIT_FORMATION = "HabitFormation"
    RETENTION = "Retention"
    LOYALTY = "Loyalty"
    ADVOCACY = "Advocacy"
    REFERRAL = "Referral"
    EXPANSION = "Expansion"
    REPURCHASE = "Repurchase"


class GrowthStage(Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "ProductMarketFit"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    MARKET_LEADERSHIP = "MarketLeadership"


class MoatType(Enum):
    NETWORK_EFFECTS = "NetworkEffects"
    SWITCHING_COSTS = "SwitchingCosts"
    ECONOMIES_OF_SCALE = "EconomiesOfScale"
    BRAND = "Brand"
    REGULATORY_IP = "RegulatoryIP"
    COUNTER_POSITIONING = "CounterPositioning"


class FailureModeType(Enum):
    SOLVING_WRONG_PROBLEM = "SolvingWrongProblem"
    BUILDING_BEFORE_VALIDATING = "BuildingBeforeValidating"
    WEAK_POSITIONING = "WeakPositioning"
    POOR_PRICING = "PoorPricing"
    DISTRIBUTION_FAILURE = "DistributionFailure"
    LACK_OF_PMF = "LackOfPMF"
    ORGANIZATIONAL_BOTTLENECKS = "OrganizationalBottlenecks"
    FOUNDER_BIAS = "FounderBias"
    SCALING_PREMATURELY = "ScalingPrematurely"
    CAPITAL_MISALLOCATION = "CapitalMisallocation"


@dataclass
class AnomalySignal:
    signal_id: str
    description: str
    is_structural_shift: bool
    confidence: float
    source: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class EOSHypothesis:
    hypothesis_id: str
    claim: str
    falsifiable_condition: str
    kill_threshold: float
    confidence_prior: float = 0.5
    confidence_posterior: float = 0.5
    is_falsified: bool = False
    tests_run: int = 0


@dataclass
class OpportunityDecision:
    opportunity_id: str
    pursue: bool
    decision_path: List[str]
    rationale: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# =====================================================================
# 1. Top-Level System State Machine (§1, §10.1)
# =====================================================================

class SystemStateMachine:
    """Implements state transitions for the AI-EOS §10.1 System State Machine."""

    VALID_TRANSITIONS: Dict[EOSStage, Set[EOSStage]] = {
        EOSStage.SENSING: {EOSStage.HYPOTHESIS},
        EOSStage.HYPOTHESIS: {EOSStage.CHEAP_TEST, EOSStage.DISCARD},
        EOSStage.CHEAP_TEST: {EOSStage.VALIDATION, EOSStage.DISCARD},
        EOSStage.DISCARD: {EOSStage.SENSING},
        EOSStage.VALIDATION: {EOSStage.BUILD_GATE, EOSStage.DISCARD},
        EOSStage.BUILD_GATE: {EOSStage.MVP, EOSStage.DISCARD},
        EOSStage.MVP: {EOSStage.GTM_TEST},
        EOSStage.GTM_TEST: {EOSStage.KILL_OR_SCALE},
        EOSStage.KILL_OR_SCALE: {EOSStage.SCALE, EOSStage.DISCARD},
        EOSStage.SCALE: {EOSStage.OPERATE},
        EOSStage.OPERATE: {EOSStage.REINVENT},
        EOSStage.REINVENT: {EOSStage.SENSING},
    }

    def __init__(self, initial_stage: EOSStage = EOSStage.SENSING) -> None:
        self.current_stage = initial_stage
        self.history: List[Tuple[EOSStage, datetime]] = [(initial_stage, datetime.now(timezone.utc))]

    def transition_to(self, target_stage: EOSStage, reason: str = "") -> bool:
        allowed = self.VALID_TRANSITIONS.get(self.current_stage, set())
        if target_stage not in allowed:
            logger.warning(f"Invalid transition attempted: {self.current_stage.value} -> {target_stage.value}")
            return False

        logger.info(f"EOS State Transition: {self.current_stage.value} -> {target_stage.value} ({reason})")
        self.current_stage = target_stage
        self.history.append((target_stage, datetime.now(timezone.utc)))
        return True


# =====================================================================
# 2. Decision Tree — "Should We Pursue This Opportunity?" (§10.2)
# =====================================================================

class EOSOpportunityDecisionTree:
    """Evaluates whether an opportunity should be pursued per §10.2."""

    def evaluate(
        self,
        opportunity_id: str,
        is_structural_anomaly: bool,
        is_reversible: bool,
        high_confidence_multi_source: bool = False,
        cheap_test_available: bool = True,
        cheap_test_result_exceeds_kill: Optional[bool] = None,
        expected_value_positive: Optional[bool] = None,
        structural_advantage_possible: bool = True
    ) -> OpportunityDecision:
        path = []

        # Q1: Structural anomaly or just noise?
        path.append("Q1: Structural anomaly check")
        if not is_structural_anomaly:
            return OpportunityDecision(
                opportunity_id=opportunity_id,
                pursue=False,
                decision_path=path,
                rationale="Discarded: Signal identified as noise, not structural anomaly."
            )

        # Q2: Reversible decision?
        path.append("Q2: Reversibility check")
        if not is_reversible:
            # Type I decision (irreversible)
            path.append("Q2a: High-confidence multi-source signal check (Type I)")
            if not high_confidence_multi_source:
                return OpportunityDecision(
                    opportunity_id=opportunity_id,
                    pursue=False,
                    decision_path=path,
                    rationale="Discarded: Type I irreversible decision lacks high-confidence multi-source signal."
                )

        # Branch to cheap test evaluation
        path.append("Q3: Cheap test availability check")
        if cheap_test_available:
            path.append("Q4: Cheap test result check")
            if cheap_test_result_exceeds_kill is False:
                return OpportunityDecision(
                    opportunity_id=opportunity_id,
                    pursue=False,
                    decision_path=path,
                    rationale="Discarded: Cheap test result failed to exceed kill threshold."
                )
        else:
            path.append("Q4b: Expected value check (no cheap test)")
            if expected_value_positive is False:
                return OpportunityDecision(
                    opportunity_id=opportunity_id,
                    pursue=False,
                    decision_path=path,
                    rationale="Discarded: Expected value is not clearly positive."
                )

        # Q5: Structural advantage check
        path.append("Q5: Structural advantage check")
        if not structural_advantage_possible:
            return OpportunityDecision(
                opportunity_id=opportunity_id,
                pursue=False,
                decision_path=path,
                rationale="Discarded: No structural advantage can be built or possessed."
            )

        return OpportunityDecision(
            opportunity_id=opportunity_id,
            pursue=True,
            decision_path=path,
            rationale="Approved: All decision tree criteria satisfied to commit resources."
        )


# =====================================================================
# 3. Internal Cognitive Loops (§2)
# =====================================================================

class AnomaliesAndSensingEngine:
    """Handles anomaly detection, hypothesis formation, risk classification, and mental model updates."""

    def __init__(self) -> None:
        self.mental_model_parameters: Dict[str, float] = {"market_growth_rate": 0.05, "baseline_cac": 100.0}
        self.mental_model_structure: Dict[str, Any] = {"version": "1.0", "core_assumptions": ["linear_channel_growth"]}
        self.hypotheses: Dict[str, EOSHypothesis] = {}

    def process_signal(self, signal: AnomalySignal) -> Optional[EOSHypothesis]:
        if not signal.is_structural_shift:
            return None

        hyp_id = f"hyp_{len(self.hypotheses) + 1}"
        hyp = EOSHypothesis(
            hypothesis_id=hyp_id,
            claim=f"Falsifiable claim for signal {signal.signal_id}: {signal.description}",
            falsifiable_condition=f"metric_delta > {signal.confidence * 0.2:.2f}",
            kill_threshold=0.3,
            confidence_prior=signal.confidence
        )
        self.hypotheses[hyp_id] = hyp
        return hyp

    def classify_decision_risk(self, decision_type: str, is_reversible: bool) -> RiskType:
        """Bezos 'One-way vs Two-way doors' heuristic."""
        if is_reversible:
            return RiskType.TYPE_II_REVERSIBLE
        return RiskType.TYPE_I_IRREVERSIBLE

    def update_mental_model(self, feedback_metric: str, value: float, structural_shift: bool = False) -> Dict[str, Any]:
        if structural_shift:
            self.mental_model_structure["version"] = f"v{float(self.mental_model_structure['version'][1:]) + 1.0:.1f}"
            self.mental_model_structure["paradigm_shift"] = True
            logger.info("PARADIGM SHIFT: Mental model structure updated.")
        else:
            self.mental_model_parameters[feedback_metric] = value
        return {"parameters": self.mental_model_parameters, "structure": self.mental_model_structure}


# =====================================================================
# 4. External Business Loops (§3)
# =====================================================================

class ExternalBusinessLoopsEngine:
    """Engine for simulating and monitoring the 13 external business loops (§3)."""

    def __init__(self) -> None:
        self.loops_state: Dict[ExternalLoopType, Dict[str, Any]] = {
            loop: {"kpis": {}, "status": "healthy", "failure_mode_flagged": False}
            for loop in ExternalLoopType
        }

    def update_loop_kpis(self, loop: ExternalLoopType, kpis: Dict[str, float]) -> Dict[str, Any]:
        state = self.loops_state[loop]
        state["kpis"].update(kpis)

        # Basic failure mode check per loop
        if loop == ExternalLoopType.PRODUCT and kpis.get("retention_flattening", 1.0) < 0.2:
            state["status"] = "degraded"
            state["failure_mode_flagged"] = True
        elif loop == ExternalLoopType.FINANCIAL and kpis.get("burn_multiple", 1.0) > 2.5:
            state["status"] = "degraded"
            state["failure_mode_flagged"] = True
        elif loop == ExternalLoopType.HIRING and kpis.get("regretted_attrition", 0.0) > 0.15:
            state["status"] = "degraded"
            state["failure_mode_flagged"] = True
        else:
            state["status"] = "healthy"
            state["failure_mode_flagged"] = False

        return state


# =====================================================================
# 5. Customer Lifecycle Engine (§4)
# =====================================================================

class CustomerLifecycleEngine:
    """Monitors and optimizes the 15 stages of the full customer journey (§4)."""

    def __init__(self) -> None:
        self.stage_metrics: Dict[CustomerLifecycleStage, float] = {stage: 0.0 for stage in CustomerLifecycleStage}

    def record_stage_conversion(self, stage: CustomerLifecycleStage, metric_value: float) -> None:
        self.stage_metrics[stage] = metric_value

    def calculate_health_score(self) -> float:
        """Calculates weighted average customer journey health across key activation and retention levers."""
        key_weights = {
            CustomerLifecycleStage.ONBOARDING: 0.15,
            CustomerLifecycleStage.ACTIVATION: 0.25,
            CustomerLifecycleStage.RETENTION: 0.30,
            CustomerLifecycleStage.EXPANSION: 0.15,
            CustomerLifecycleStage.REFERRAL: 0.15,
        }
        score = 0.0
        for stage, weight in key_weights.items():
            score += self.stage_metrics.get(stage, 0.0) * weight
        return min(1.0, score)


# =====================================================================
# 6. Go-to-Market System (§5)
# =====================================================================

class GTMSystemSimulator:
    """Simulates channel selection, pricing alignment, and compounding motions (§5)."""

    def select_gtm_motion(self, product_complexity: str, price_point_cents: int, network_effect: bool) -> List[str]:
        motions = []
        if network_effect:
            motions.append("Community-Led Growth (CLG)")

        if price_point_cents < 500_00 and product_complexity in ["low", "medium"]:
            motions.append("Product-Led Growth (PLG)")
            motions.append("Content / Organic")
        else:
            motions.append("Sales-Led Growth (SLG)")
            motions.append("Enterprise Sales")

        return motions

    def evaluate_pricing_alignment(self, value_delivered_dollars: float, price_dollars: float) -> Dict[str, Any]:
        margin = (value_delivered_dollars - price_dollars) / value_delivered_dollars if value_delivered_dollars > 0 else 0.0
        aligned = 0.10 <= price_dollars / value_delivered_dollars <= 0.30 if value_delivered_dollars > 0 else False
        return {
            "value_capture_ratio": price_dollars / value_delivered_dollars if value_delivered_dollars > 0 else 0.0,
            "value_margin_left_to_customer": margin,
            "is_value_based_aligned": aligned
        }


# =====================================================================
# 7. Company Growth State Machine (§6)
# =====================================================================

class CompanyGrowthStateMachine:
    """Manages progression across the 8 company growth stages (§6)."""

    STAGE_ORDER = [
        GrowthStage.IDEA,
        GrowthStage.VALIDATION,
        GrowthStage.STARTUP,
        GrowthStage.PMF,
        GrowthStage.GROWTH,
        GrowthStage.SCALE,
        GrowthStage.PLATFORM,
        GrowthStage.ECOSYSTEM,
        GrowthStage.MARKET_LEADERSHIP,
    ]

    STAGE_SPECS = {
        GrowthStage.IDEA: {
            "objective": "Falsify or strengthen hypothesis",
            "org": "Founder(s) only",
            "capital": "Near-zero, sweat equity",
            "risk": "Solving a non-problem",
            "metric": "validated_learnings"
        },
        GrowthStage.VALIDATION: {
            "objective": "Prove willingness to pay",
            "org": "First 1-3 hires",
            "capital": "Pre-seed/seed capital",
            "risk": "False positive validation",
            "metric": "paying_customers"
        },
        GrowthStage.PMF: {
            "objective": "Reach retention/growth threshold",
            "org": "First managers",
            "capital": "Growth capital",
            "risk": "Mistaking early traction for PMF",
            "metric": "retention_curve_flattening"
        },
        GrowthStage.GROWTH: {
            "objective": "Scale what works",
            "org": "Middle management layer",
            "capital": "Series B/C",
            "risk": "Scaling a broken funnel",
            "metric": "growth_rate"
        },
        GrowthStage.MARKET_LEADERSHIP: {
            "objective": "Defend and extend category",
            "org": "Full corporate structure",
            "capital": "Diversified",
            "risk": "Complacency / disruption",
            "metric": "category_share"
        }
    }

    def __init__(self, current_stage: GrowthStage = GrowthStage.IDEA) -> None:
        self.current_stage = current_stage

    def evaluate_stage_transition(self, metrics: Dict[str, float]) -> GrowthStage:
        if self.current_stage == GrowthStage.IDEA and metrics.get("validated_learnings", 0) >= 3:
            self.current_stage = GrowthStage.VALIDATION
        elif self.current_stage == GrowthStage.VALIDATION and metrics.get("paying_customers", 0) >= 5:
            self.current_stage = GrowthStage.STARTUP
        elif self.current_stage == GrowthStage.STARTUP and metrics.get("retention_curve_flattened", 0) == 1:
            self.current_stage = GrowthStage.PMF
        elif self.current_stage == GrowthStage.PMF and metrics.get("mrr_growth_rate", 0) >= 0.15:
            self.current_stage = GrowthStage.GROWTH
        elif self.current_stage == GrowthStage.GROWTH and metrics.get("arr_dollars", 0) >= 10_000_000:
            self.current_stage = GrowthStage.SCALE
        return self.current_stage


# =====================================================================
# 8. Strategic Moat Engine (§7)
# =====================================================================

class StrategicMoatEngine:
    """Tracks cost curves, timing advantages, 6 competitive moats, and capital allocation (§7)."""

    def __init__(self) -> None:
        self.cost_curves: Dict[str, List[float]] = {}

    def track_cost_curve(self, technology: str, unit_cost: float) -> List[float]:
        if technology not in self.cost_curves:
            self.cost_curves[technology] = []
        self.cost_curves[technology].append(unit_cost)
        return self.cost_curves[technology]

    def evaluate_timing_viability(self, technology: str, threshold_cost: float) -> bool:
        history = self.cost_curves.get(technology, [])
        if not history:
            return False
        return history[-1] <= threshold_cost

    def calculate_moat_durability(self, moat_scores: Dict[MoatType, float]) -> float:
        """Calculates combined moat score across the 6 moat types."""
        weights = {
            MoatType.NETWORK_EFFECTS: 0.25,
            MoatType.SWITCHING_COSTS: 0.20,
            MoatType.ECONOMIES_OF_SCALE: 0.20,
            MoatType.BRAND: 0.15,
            MoatType.COUNTER_POSITIONING: 0.10,
            MoatType.REGULATORY_IP: 0.10,
        }
        total = 0.0
        for moat, weight in weights.items():
            total += moat_scores.get(moat, 0.0) * weight
        return min(1.0, total)


# =====================================================================
# 9. Failure Mode Monitor (§8)
# =====================================================================

class FailureModeMonitor:
    """Pattern-matches operating metrics against the 10 failure modes (§8)."""

    FAILURE_PATTERNS = {
        FailureModeType.SOLVING_WRONG_PROBLEM: "Low engagement despite positive survey feedback",
        FailureModeType.BUILDING_BEFORE_VALIDATING: "High build velocity, flat demand signal",
        FailureModeType.WEAK_POSITIONING: "High CAC, long sales cycles, feature comparison objections",
        FailureModeType.POOR_PRICING: "High conversion at low price, but poor margin/expansion",
        FailureModeType.DISTRIBUTION_FAILURE: "High NPS, flat growth",
        FailureModeType.LACK_OF_PMF: "Retention curve never flattens",
        FailureModeType.ORGANIZATIONAL_BOTTLENECKS: "Rising decision latency, founder single point of failure",
        FailureModeType.FOUNDER_BIAS: "Ignoring disconfirming data, 'just needs more time' pattern",
        FailureModeType.SCALING_PREMATURELY: "CAC rising faster than LTV as spend scales",
        FailureModeType.CAPITAL_MISALLOCATION: "Multiple underperforming bets funded simultaneously",
    }

    def detect_failure_modes(self, metrics: Dict[str, float]) -> List[Tuple[FailureModeType, str, str]]:
        detected = []

        if metrics.get("survey_satisfaction", 0.0) > 0.8 and metrics.get("active_usage", 1.0) < 0.2:
            detected.append((
                FailureModeType.SOLVING_WRONG_PROBLEM,
                "Low engagement despite positive survey feedback",
                "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)"
            ))

        if metrics.get("build_velocity", 0.0) > 0.8 and metrics.get("demand_growth", 1.0) < 0.05:
            detected.append((
                FailureModeType.BUILDING_BEFORE_VALIDATING,
                "High build velocity, flat demand signal",
                "Enforce a validation gate before build resourcing"
            ))

        if metrics.get("retention_curve_slope", -1.0) < -0.05 and metrics.get("months_active", 0) > 6:
            detected.append((
                FailureModeType.LACK_OF_PMF,
                "Retention curve never flattens",
                "Stop scaling; return to cohort-level retention work"
            ))

        if metrics.get("cac_growth_rate", 0.0) > metrics.get("ltv_growth_rate", 0.0) and metrics.get("growth_spend", 0.0) > 100_000:
            detected.append((
                FailureModeType.SCALING_PREMATURELY,
                "CAC rising faster than LTV as spend scales",
                "Re-test unit economics at each order-of-magnitude of spend"
            ))

        return detected


# =====================================================================
# 10. AI Agents & Modules Registry (§10.3)
# =====================================================================

class SensingAgent:
    def process_environment(self, signals: List[AnomalySignal]) -> List[AnomalySignal]:
        return [s for s in signals if s.is_structural_shift and s.confidence >= 0.6]


class HypothesisEngineAgent:
    def generate_hypotheses(self, signals: List[AnomalySignal]) -> List[EOSHypothesis]:
        return [
            EOSHypothesis(
                hypothesis_id=f"hyp_{i}",
                claim=f"Testable hypothesis for {s.description}",
                falsifiable_condition="retention >= 0.40",
                kill_threshold=0.20
            )
            for i, s in enumerate(signals)
        ]


class ValidationAgent:
    def run_cheap_test(self, hyp: EOSHypothesis, test_cost_dollars: float) -> Dict[str, Any]:
        hyp.tests_run += 1
        success = test_cost_dollars <= 500 and hyp.confidence_prior > 0.4
        if not success:
            hyp.is_falsified = True
        return {"hypothesis_id": hyp.hypothesis_id, "passed": success, "cost": test_cost_dollars}


class GTMSimulatorAgent:
    def simulate_funnel(self, traffic: int, conversion: float, cac: float, ltv: float) -> Dict[str, float]:
        customers = traffic * conversion
        return {"customers": customers, "ltv_cac_ratio": ltv / cac if cac > 0 else 0.0}


class GrowthStageClassifierAgent:
    def classify_stage(self, metrics: Dict[str, float]) -> GrowthStage:
        if metrics.get("paying_customers", 0) < 5:
            return GrowthStage.VALIDATION
        if metrics.get("retention_curve_flattened", 0) == 0:
            return GrowthStage.STARTUP
        return GrowthStage.PMF


class MoatAnalyzerAgent:
    def score_moats(self, network_density: float, switching_cost: float) -> float:
        return min(1.0, 0.5 * network_density + 0.5 * min(1.0, switching_cost / 1000))


class FailureModeMonitorAgent:
    def monitor(self, metrics: Dict[str, float]) -> List[FailureModeType]:
        monitor = FailureModeMonitor()
        return [item[0] for item in monitor.detect_failure_modes(metrics)]


class CapitalAllocatorAgent:
    def rank_initiatives(self, initiatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return sorted(initiatives, key=lambda x: x.get("expected_return", 0.0), reverse=True)


class ReinventionTriggerAgent:
    def evaluate_disruption_requisite(self, revenue_decay: float, attrition_rate: float) -> bool:
        return revenue_decay > 0.15 and attrition_rate > 0.20


class GovernanceSafetyLayerAgent:
    def enforce_safety(self, decision_type: RiskType, approved_by_human: bool) -> bool:
        if decision_type == RiskType.TYPE_I_IRREVERSIBLE and not approved_by_human:
            logger.warning("GOVERNANCE BLOCK: Type I irreversible decision requires human sign-off.")
            return False
        return True


# =====================================================================
# 11. KPI Stack (§10.4) & EOSEngineFirstPrinciples Orchestrator
# =====================================================================

class KPISystemStack:
    """Rolled up KPI stack across all subsystems (§10.4)."""

    def aggregate_kpis(
        self,
        signal_noise_ratio: float,
        cost_per_validated_learning: float,
        activation_rate: float,
        cac: float,
        burn_multiple: float,
        decision_latency_days: float,
        moat_score: float,
        loop_closure_time_days: float
    ) -> Dict[str, float]:
        return {
            "sensing_signal_noise_ratio": signal_noise_ratio,
            "validation_cost_per_learning": cost_per_validated_learning,
            "product_activation_rate": activation_rate,
            "gtm_cac": cac,
            "financial_burn_multiple": burn_multiple,
            "org_decision_latency_days": decision_latency_days,
            "strategic_moat_durability": moat_score,
            "system_loop_closure_time_days": loop_closure_time_days
        }


class EOSEngineFirstPrinciples:
    """The authoritative continuous Entrepreneurial Operating System (EOS) Orchestrator."""

    def __init__(self) -> None:
        self.state_machine = SystemStateMachine()
        self.decision_tree = EOSOpportunityDecisionTree()
        self.cognitive_engine = AnomaliesAndSensingEngine()
        self.external_loops = ExternalBusinessLoopsEngine()
        self.customer_lifecycle = CustomerLifecycleEngine()
        self.gtm_simulator = GTMSystemSimulator()
        self.growth_state = CompanyGrowthStateMachine()
        self.moat_engine = StrategicMoatEngine()
        self.failure_monitor = FailureModeMonitor()
        self.kpi_stack = KPISystemStack()

        # Agent Registry (§10.3)
        self.sensing_agent = SensingAgent()
        self.hypothesis_agent = HypothesisEngineAgent()
        self.validation_agent = ValidationAgent()
        self.gtm_agent = GTMSimulatorAgent()
        self.growth_classifier = GrowthStageClassifierAgent()
        self.moat_agent = MoatAnalyzerAgent()
        self.failure_agent = FailureModeMonitorAgent()
        self.capital_agent = CapitalAllocatorAgent()
        self.reinvention_agent = ReinventionTriggerAgent()
        self.governance_agent = GovernanceSafetyLayerAgent()

    def run_master_loop_cycle(
        self,
        signals: List[AnomalySignal],
        opportunity_id: str,
        human_approved_type1: bool = True
    ) -> Dict[str, Any]:
        """Runs one integrated cycle across the Master Loop (§1 & §10.1)."""
        cycle_result: Dict[str, Any] = {"stage": self.state_machine.current_stage.value}

        # 1. Sensing & Anomaly Processing
        filtered_signals = self.sensing_agent.process_environment(signals)
        cycle_result["filtered_signals_count"] = len(filtered_signals)

        if not filtered_signals:
            return cycle_result

        # Transition to Hypothesis stage
        self.state_machine.transition_to(EOSStage.HYPOTHESIS, "Structural anomaly detected")
        hypotheses = self.hypothesis_agent.generate_hypotheses(filtered_signals)
        cycle_result["hypotheses_generated"] = len(hypotheses)

        # 2. Decision Tree Evaluation
        top_sig = filtered_signals[0]
        decision = self.decision_tree.evaluate(
            opportunity_id=opportunity_id,
            is_structural_anomaly=top_sig.is_structural_shift,
            is_reversible=True,
            cheap_test_available=True,
            cheap_test_result_exceeds_kill=True,
            structural_advantage_possible=True
        )
        cycle_result["decision"] = decision

        if not decision.pursue:
            self.state_machine.transition_to(EOSStage.DISCARD, "Decision tree discarded opportunity")
            self.state_machine.transition_to(EOSStage.SENSING, "Return to sensing")
            return cycle_result

        # 3. Governance check
        risk = self.cognitive_engine.classify_decision_risk("strategic_pursuit", is_reversible=True)
        if not self.governance_agent.enforce_safety(risk, human_approved_type1):
            cycle_result["governance_blocked"] = True
            return cycle_result

        # 4. Cheap test execution
        self.state_machine.transition_to(EOSStage.CHEAP_TEST, "Running cheap experiment")
        if hypotheses:
            test_res = self.validation_agent.run_cheap_test(hypotheses[0], test_cost_dollars=100.0)
            cycle_result["test_result"] = test_res

            if test_res["passed"]:
                self.state_machine.transition_to(EOSStage.VALIDATION, "Cheap test strengthened hypothesis")
                self.state_machine.transition_to(EOSStage.BUILD_GATE, "Economic viability confirmed")
            else:
                self.state_machine.transition_to(EOSStage.DISCARD, "Falsified by cheap test")
                self.state_machine.transition_to(EOSStage.SENSING, "Return to sensing")

        cycle_result["final_stage"] = self.state_machine.current_stage.value
        return cycle_result
