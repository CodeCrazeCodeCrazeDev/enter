"""First-Principles Entrepreneurial Operating System (EOS) Engine Implementation.

Models how elite founders sense, build, and compound enduring companies based on:
1. Multi-timescale feedback loops (Fast, Medium, Slow).
2. Master Loop re-entrant state machine (Nodes A-S with kill and reset signals).
3. Signal-to-Idea pipeline with structural anomaly filtering and Bayesian belief updating.
4. 13 coupled business loops (Product, Marketing, Sales, CS, Brand, Pricing, Referral,
   Data, Financial, Hiring, Culture, Innovation, Competitive Intel) as stocks and flows.
5. Full 15-stage customer journey lifecycle tracking and optimization.
6. 9-stage company growth classifier with binding constraints and key metrics.
7. Strategic thinking engine with technology cost curve modeling and moat durability scoring.
8. Failure mode monitor matrix with early detection signals and correction mechanisms.
9. Autonomous AI-EOS module orchestrator (§10.3 architecture).
"""

from __future__ import annotations
import math
import logging
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

logger = logging.getLogger("ai_eos.eos_first_principles")


# =====================================================================
# 0. Timescales & Enums
# =====================================================================
class Timescale(str, Enum):
    FAST = "fast"        # Days - Weeks
    MEDIUM = "medium"    # Months - Quarters
    SLOW = "slow"        # Years


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
    ONBOARDING_RETENTION = "L"
    UNIT_ECONOMICS_OPTIMIZATION = "M"
    OPERATIONS_ORG_SCALING = "N"
    MOAT_CONSTRUCTION = "O"
    SCALING_EXPANSION = "P"
    PLATFORM_ECOSYSTEM = "Q"
    MARKET_LEADERSHIP = "R"
    CONTINUOUS_REINVENTION = "S"


class CustomerJourneyStage(str, Enum):
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


# =====================================================================
# 1. Multi-Timescale Loop Engine
# =====================================================================
class FeedbackLoop(BaseModel):
    loop_id: str
    name: str
    timescale: Timescale
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    feedback_signal: float = 0.0
    core_kpi: float = 0.0
    velocity: float = 1.0  # Execution frequency multiplier
    active: bool = True


class MultiTimescaleLoopEngine:
    """Manages nested coupled feedback loops operating across fast, medium, and slow timescales."""

    def __init__(self) -> None:
        self.loops: Dict[str, FeedbackLoop] = {}

    def register_loop(self, loop: FeedbackLoop) -> None:
        self.loops[loop.loop_id] = loop

    def execute_timescale(self, timescale: Timescale) -> Dict[str, Any]:
        """Execute active loops belonging to a specific timescale and compute effective velocity."""
        executed = {}
        for loop_id, loop in self.loops.items():
            if loop.timescale == timescale and loop.active:
                # Loop compounding effect: output scales with velocity and feedback fidelity
                compounding_factor = loop.velocity * (1.0 + max(-0.5, loop.feedback_signal))
                executed[loop_id] = {
                    "name": loop.name,
                    "timescale": loop.timescale.value,
                    "compounding_factor": compounding_factor,
                    "kpi": loop.core_kpi,
                }
        return executed


# =====================================================================
# 2. Master Loop State Machine
# =====================================================================
class MasterLoopStateMachine:
    """Implements the 19-node Master Loop (Nodes A through S) with re-entrancy and kill signals."""

    def __init__(self) -> None:
        self.current_node: MasterLoopNode = MasterLoopNode.ENVIRONMENTAL_SENSING
        self.history: List[Tuple[MasterLoopNode, str]] = []

    def transition_to(self, next_node: MasterLoopNode, reason: str = "sequential") -> MasterLoopNode:
        self.history.append((self.current_node, reason))
        logger.info(f"Master Loop Transition: {self.current_node.value} -> {next_node.value} ({reason})")
        self.current_node = next_node
        return self.current_node

    def evaluate_reentrant_signal(self, node: MasterLoopNode, signal_data: Dict[str, Any]) -> MasterLoopNode:
        """Evaluate re-entrancy conditions and kill/reset signals."""
        if node == MasterLoopNode.CUSTOMER_VALIDATION and signal_data.get("falsified", False):
            # Kill signal from F -> return to Opportunity Discovery D
            return self.transition_to(MasterLoopNode.OPPORTUNITY_DISCOVERY, reason="customer_validation_kill_signal")

        if node == MasterLoopNode.MVP_EXPERIMENTATION and signal_data.get("kill_threshold_breached", False):
            # Kill signal from H -> return to Opportunity Discovery D
            return self.transition_to(MasterLoopNode.OPPORTUNITY_DISCOVERY, reason="mvp_kill_threshold_breached")

        if node == MasterLoopNode.CUSTOMER_ACQUISITION and signal_data.get("weak_gtm", False):
            # Weak GTM signal from K -> return to Go-to-Market System J
            return self.transition_to(MasterLoopNode.GTM_SYSTEM, reason="weak_gtm_signal")

        if node == MasterLoopNode.UNIT_ECONOMICS_OPTIMIZATION and signal_data.get("bad_economics", False):
            # Bad economics signal from M -> return to Business Model Design G
            return self.transition_to(MasterLoopNode.BUSINESS_MODEL_DESIGN, reason="bad_unit_economics_signal")

        # Default sequential progress
        return self.current_node


# =====================================================================
# 3. Signal-to-Idea Pipeline
# =====================================================================
class SignalHypothesisFilter:
    """Filters weak signals into falsifiable claims using anomaly detection and Bayesian updating."""

    def __init__(self, anomaly_threshold: float = 0.6) -> None:
        self.anomaly_threshold = anomaly_threshold

    def is_structural_anomaly(self, signal: Dict[str, Any]) -> bool:
        """Determines if a weak signal represents a structural shift vs background noise."""
        unexpectedness = signal.get("unexpectedness", 0.0)
        structural_alignment = signal.get("structural_alignment", 0.0)
        score = 0.6 * unexpectedness + 0.4 * structural_alignment
        return score >= self.anomaly_threshold

    def update_bayesian_belief(self, prior_confidence: float, likelihood_ratio: float) -> float:
        """Bayesian updating of hypothesis confidence given experimental evidence."""
        prior_odds = prior_confidence / (1.0 - prior_confidence + 1e-9)
        posterior_odds = prior_odds * likelihood_ratio
        posterior = posterior_odds / (1.0 + posterior_odds)
        return float(min(0.99, max(0.01, posterior)))

    def evaluate_risk_heuristic(self, decision_type: str, confidence: float) -> str:
        """Type I (irreversible) vs Type II (reversible) decision evaluation."""
        if decision_type == "type_i":
            # Reversible decision gate: requires high confidence >= 0.8
            return "proceed_deliberate" if confidence >= 0.8 else "defer_gather_evidence"
        else:
            # Type II reversible decision: execute fast cheaply
            return "proceed_fast_cheap"


# =====================================================================
# 4. 13 Coupled Business Loops (Systems Thinking Stocks & Flows)
# =====================================================================
class BusinessLoopSet:
    """Simulates the 13 coupled business loops as an integrated system of stocks and flows."""

    def __init__(self) -> None:
        # Stocks
        self.stocks = {
            "cash_cents": 100_000_000,  # $1M starting capital
            "talent_capacity": 10.0,
            "brand_trust": 0.5,
            "customer_base": 100,
            "data_assets": 1.0,
            "product_capability": 1.0,
        }

    def simulate_step(
        self,
        cac_cents: int,
        arpu_cents: int,
        churn_rate: float,
        hiring_budget_cents: int,
        rd_investment_cents: int
    ) -> Dict[str, Any]:
        """Execute one step of coupled stocks and flows across pricing, financial, product, hiring loops."""
        # Financial & Customer Flows
        acquired = int((self.stocks["cash_cents"] * 0.2) / max(1, cac_cents))
        churned = int(self.stocks["customer_base"] * churn_rate)
        self.stocks["customer_base"] = max(0, self.stocks["customer_base"] + acquired - churned)

        mrr_cents = self.stocks["customer_base"] * arpu_cents
        expenses_cents = hiring_budget_cents + rd_investment_cents + (acquired * cac_cents)

        # Update cash stock
        self.stocks["cash_cents"] += (mrr_cents - expenses_cents)

        # Product capability stock grows with R&D flow
        self.stocks["product_capability"] += (rd_investment_cents / 100_000_000) * 0.1

        # Talent stock grows with hiring flow
        self.stocks["talent_capacity"] += (hiring_budget_cents / 100_000_000) * 2.0

        # Compute key leverage indicators
        burn_multiple = (expenses_cents - mrr_cents) / max(1, mrr_cents) if expenses_cents > mrr_cents else 0.0
        runway_months = (self.stocks["cash_cents"] / max(1, (expenses_cents - mrr_cents))) if expenses_cents > mrr_cents else 999.0

        ltv_cents = arpu_cents / max(1e-5, churn_rate)

        return {
            "mrr_cents": mrr_cents,
            "stocks": self.stocks.copy(),
            "burn_multiple": burn_multiple,
            "runway_months": runway_months,
            "unit_economics_healthy": ltv_cents >= (3.0 * cac_cents),
        }


# =====================================================================
# 5. Customer Journey Lifecycle (15 Stages)
# =====================================================================
class CustomerJourneyLifecycle:
    """Tracks and optimizes progression across all 15 stages of the full customer lifecycle."""

    def __init__(self) -> None:
        self.stage_conversion_rates: Dict[CustomerJourneyStage, float] = {
            CustomerJourneyStage.AWARENESS: 0.10,
            CustomerJourneyStage.INTEREST: 0.20,
            CustomerJourneyStage.CONSIDERATION: 0.30,
            CustomerJourneyStage.EVALUATION: 0.40,
            CustomerJourneyStage.PURCHASE: 0.15,
            CustomerJourneyStage.ONBOARDING: 0.70,
            CustomerJourneyStage.ACTIVATION: 0.60,
            CustomerJourneyStage.ENGAGEMENT: 0.50,
            CustomerJourneyStage.HABIT_FORMATION: 0.40,
            CustomerJourneyStage.RETENTION: 0.80,
            CustomerJourneyStage.LOYALTY: 0.50,
            CustomerJourneyStage.ADVOCACY: 0.30,
            CustomerJourneyStage.REFERRAL: 0.20,
            CustomerJourneyStage.EXPANSION: 0.25,
            CustomerJourneyStage.REPURCHASE: 0.85,
        }

    def compute_funnel_throughput(self, initial_awareness_count: int) -> Dict[str, Any]:
        """Compute cohort throughput across the 15-stage pipeline."""
        current_count = float(initial_awareness_count)
        funnel_counts = {}

        for stage in CustomerJourneyStage:
            conv = self.stage_conversion_rates[stage]
            current_count *= conv
            funnel_counts[stage.value] = int(current_count)

        viral_coefficient = (
            funnel_counts[CustomerJourneyStage.REFERRAL.value] *
            self.stage_conversion_rates[CustomerJourneyStage.PURCHASE]
        ) / max(1, initial_awareness_count)

        return {
            "funnel_counts": funnel_counts,
            "activated_customers": funnel_counts[CustomerJourneyStage.ACTIVATION.value],
            "retained_customers": funnel_counts[CustomerJourneyStage.RETENTION.value],
            "viral_coefficient_k": viral_coefficient,
        }


# =====================================================================
# 6. Company Growth Stage Classifier
# =====================================================================
class GrowthStageClassifier:
    """Classifies company growth stage across the 9-stage taxonomy and identifies binding constraints."""

    def classify_stage(
        self,
        has_validated_learnings: bool,
        paying_customers: int,
        retention_flattening: bool,
        growth_rate_mom: float,
        rule_of_40_score: float,
        has_ecosystem_api: bool,
        ecosystem_gmv_cents: int,
        category_share: float
    ) -> Dict[str, Any]:
        """Classify stage based on metrics and determine primary constraint."""
        if category_share >= 0.40:
            stage = CompanyGrowthStage.MARKET_LEADERSHIP
            constraint = "innovation_velocity_vs_incumbency_drag"
        elif ecosystem_gmv_cents > 10_000_000_00:
            stage = CompanyGrowthStage.ECOSYSTEM
            constraint = "governance_credibility"
        elif has_ecosystem_api:
            stage = CompanyGrowthStage.PLATFORM
            constraint = "ecosystem_trust"
        elif rule_of_40_score >= 0.40:
            stage = CompanyGrowthStage.SCALE
            constraint = "org_coordination_cost"
        elif growth_rate_mom >= 0.15:
            stage = CompanyGrowthStage.GROWTH
            constraint = "hiring_velocity_and_systems"
        elif retention_flattening:
            stage = CompanyGrowthStage.PMF
            constraint = "team_bandwidth"
        elif paying_customers >= 10:
            stage = CompanyGrowthStage.STARTUP
            constraint = "cash_runway"
        elif paying_customers > 0:
            stage = CompanyGrowthStage.VALIDATION
            constraint = "signal_quality"
        else:
            stage = CompanyGrowthStage.IDEA
            constraint = "founder_time"

        return {
            "stage": stage.value,
            "binding_constraint": constraint,
        }


# =====================================================================
# 7. Strategic Moat & Cost Curve Engine
# =====================================================================
class CompetitiveStrategyEngine:
    """Models technology cost curves and computes composite moat durability scores."""

    def compute_cost_curve_viability(
        self,
        c0_initial_cost: float,
        decay_rate_lambda: float,
        time_t: float,
        viability_threshold: float
    ) -> Tuple[float, bool]:
        r"""Compute future cost $C(t) = C_0 e^{-\lambda t}$ and check economic viability."""
        current_cost = c0_initial_cost * math.exp(-decay_rate_lambda * time_t)
        is_viable = current_cost <= viability_threshold
        return float(current_cost), is_viable

    def compute_moat_durability(
        self,
        network_density: float,
        switching_cost_score: float,
        brand_trust_score: float,
        cost_advantage_score: float
    ) -> float:
        r"""Composite Moat Durability Score $M \in [0, 1]$."""
        score = (
            0.30 * min(1.0, network_density) +
            0.25 * min(1.0, switching_cost_score) +
            0.20 * min(1.0, brand_trust_score) +
            0.25 * min(1.0, cost_advantage_score)
        )
        return float(min(1.0, max(0.0, score)))


# =====================================================================
# 8. Failure Mode Monitor
# =====================================================================
class FailureModeMonitor:
    """Monitors operating metrics against the failure matrix to generate early warnings."""

    def evaluate_operating_metrics(self, metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        """Evaluate metrics against key failure mode signatures."""
        warnings = []

        if metrics.get("engagement_rate", 1.0) < 0.10 and metrics.get("survey_satisfaction", 0.0) > 0.80:
            warnings.append({
                "failure_mode": "solving_wrong_problem",
                "root_cause": "skipped_root_cause_analysis",
                "correction": "return_to_5_whys_and_jtbd_interviews",
            })

        if metrics.get("cac_payback_months", 0.0) > 24.0 and metrics.get("growth_spend_scaling", False):
            warnings.append({
                "failure_mode": "premature_scaling",
                "root_cause": "confusing_early_spike_with_durable_pmf",
                "correction": "pause_scaling_and_retest_unit_economics",
            })

        if metrics.get("decision_latency_hours", 0.0) > 72.0:
            warnings.append({
                "failure_mode": "organizational_bottleneck",
                "root_cause": "centralized_decision_rights",
                "correction": "push_decision_rights_down_with_clear_frameworks",
            })

        if metrics.get("burn_multiple", 0.0) > 3.0 and metrics.get("runway_months", 12.0) < 6.0:
            warnings.append({
                "failure_mode": "capital_misallocation",
                "root_cause": "growth_at_negative_unit_economics",
                "correction": "enforce_opportunity_cost_budgeting_and_cut_burn",
            })

        return warnings


# =====================================================================
# 9. Autonomous AI-EOS Orchestrator
# =====================================================================
class FirstPrinciplesEOSEngine:
    """Autonomous AI-EOS orchestrator unifying all first-principles components."""

    def __init__(self) -> None:
        self.loop_engine = MultiTimescaleLoopEngine()
        self.state_machine = MasterLoopStateMachine()
        self.signal_filter = SignalHypothesisFilter()
        self.business_loops = BusinessLoopSet()
        self.customer_journey = CustomerJourneyLifecycle()
        self.growth_classifier = GrowthStageClassifier()
        self.strategy_engine = CompetitiveStrategyEngine()
        self.failure_monitor = FailureModeMonitor()

    def run_full_execution_cycle(
        self,
        signal_data: Dict[str, Any],
        business_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Runs a complete first-principles sensing, classification, simulation, and monitoring cycle."""
        # 1. Signal sensing & anomaly filtering
        is_anomaly = self.signal_filter.is_structural_anomaly(signal_data)

        # 2. State machine evaluation
        current_node = self.state_machine.evaluate_reentrant_signal(
            self.state_machine.current_node,
            signal_data
        )

        cac_cents = business_params.get("cac_cents", 500_00)
        arpu_cents = business_params.get("arpu_cents", 100_00)

        # 3. Business loop simulation
        sim_results = self.business_loops.simulate_step(
            cac_cents=cac_cents,
            arpu_cents=arpu_cents,
            churn_rate=business_params.get("churn_rate", 0.05),
            hiring_budget_cents=business_params.get("hiring_budget_cents", 100_000_00),
            rd_investment_cents=business_params.get("rd_investment_cents", 50_000_00)
        )

        # 4. Growth stage classification
        stage_info = self.growth_classifier.classify_stage(
            has_validated_learnings=True,
            paying_customers=business_params.get("paying_customers", 15),
            retention_flattening=business_params.get("retention_flattening", True),
            growth_rate_mom=business_params.get("growth_rate_mom", 0.10),
            rule_of_40_score=0.25,
            has_ecosystem_api=False,
            ecosystem_gmv_cents=0,
            category_share=0.05
        )

        # 5. Strategic moat scoring
        moat_score = self.strategy_engine.compute_moat_durability(
            network_density=business_params.get("network_density", 0.3),
            switching_cost_score=0.4,
            brand_trust_score=0.5,
            cost_advantage_score=0.2
        )

        cac_payback_months = cac_cents / max(1, arpu_cents)

        # 6. Failure monitoring
        failure_warnings = self.failure_monitor.evaluate_operating_metrics({
            "engagement_rate": business_params.get("engagement_rate", 0.5),
            "survey_satisfaction": 0.85,
            "cac_payback_months": cac_payback_months,
            "burn_multiple": sim_results["burn_multiple"],
            "runway_months": sim_results["runway_months"],
            "decision_latency_hours": business_params.get("decision_latency_hours", 12.0)
        })

        return {
            "is_structural_anomaly": is_anomaly,
            "master_loop_node": current_node.value,
            "simulation": sim_results,
            "growth_stage": stage_info,
            "moat_durability_score": moat_score,
            "failure_warnings": failure_warnings,
        }
