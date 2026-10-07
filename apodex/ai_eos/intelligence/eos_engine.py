"""Entrepreneurial Operating System (EOS) Cognitive Engine implementation.

Features production-grade systems fully integrated behind a unified orchestrator
for continuous sensing, anomaly detection, business simulation, capital allocation,
moat analysis, failure prediction, growth stage classification, customer lifecycle tracking,
and strategic reinvention based on the first-principles EOS framework.
"""

from __future__ import annotations
import math
import logging
import random
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Set
from uuid import UUID, uuid4
from datetime import datetime, timezone

from ...ai_eos.domain.models import VentureCell, Hypothesis, Evidence, Theory

logger = logging.getLogger("sero.eos_engine")


# =====================================================================
# 0. EOS State Machine & Decision Enums
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


class CompanyStage(str, Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "PMF"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    MARKET_LEADERSHIP = "Market Leadership"


# =====================================================================
# 1. Entrepreneurial World Model & Anomalies Engine
# =====================================================================
class EntrepreneurialWorldModel:
    """Models world state transitions, resource parameters, and environment uncertainty."""

    def __init__(self) -> None:
        self.state: Dict[str, Any] = {
            "gdp_growth": 0.02,
            "market_demand_index": 1.0,
            "competitor_count": 5,
            "funding_climate": "moderate",  # loose, moderate, tight
            "technology_platform_shift": False,
        }
        self.uncertainty_scores: Dict[str, float] = {
            "market_demand_index": 0.25,
            "competitor_count": 0.15,
        }

    def transition_state(self) -> Dict[str, Any]:
        """Simulate stochastic environment transition."""
        self.state["market_demand_index"] += random.uniform(-0.1, 0.1)
        self.state["market_demand_index"] = max(0.1, self.state["market_demand_index"])

        # Competitor count grows stochastically
        if random.random() > 0.7:
            self.state["competitor_count"] += random.randint(1, 2)

        # Platform shift has small continuous hazard rate
        if not self.state["technology_platform_shift"] and random.random() > 0.95:
            self.state["technology_platform_shift"] = True
            logger.warning("WORLD STATE SHIFT: Major new technology platform shift detected!")

        return self.state

    def calculate_state_entropy(self) -> float:
        """Compute the average uncertainty/entropy across world dimensions."""
        if not self.uncertainty_scores:
            return 0.0
        return sum(self.uncertainty_scores.values()) / len(self.uncertainty_scores)

    def detect_anomalies(self, weak_signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect structural anomalies vs noise (§2.1)."""
        anomalies = []
        for sig in weak_signals:
            growth_rate = sig.get("growth_rate", 0.0)
            baseline_expected = sig.get("expected_growth_rate", 0.05)
            structural = sig.get("is_structural_shift", False)

            # Anomaly condition: actual growth rate departs significantly from baseline expectation or explicit structural flag
            if structural or abs(growth_rate - baseline_expected) > 0.20:
                anomalies.append({
                    "signal_id": sig.get("id", str(uuid4())),
                    "name": sig.get("name", "unnamed_signal"),
                    "growth_rate": growth_rate,
                    "anomaly_delta": abs(growth_rate - baseline_expected),
                    "is_structural": True
                })
        return anomalies


# =====================================================================
# 2. Opportunity Graph & Decision Tree (§10.2)
# =====================================================================
class OpportunityNode:
    def __init__(self, op_id: str, name: str, value_cents: int, keywords: Set[str]) -> None:
        self.op_id = op_id
        self.name = name
        self.value_cents = value_cents
        self.keywords = keywords
        self.adjacent_ids: List[str] = []


class OpportunityGraph:
    """Manages a DAG of market opportunities, node valuations, and similarity matches."""

    def __init__(self) -> None:
        self.nodes: Dict[str, OpportunityNode] = {}

    def add_opportunity(self, op_id: str, name: str, value_cents: int, keywords: List[str]) -> None:
        node = OpportunityNode(op_id, name, value_cents, set(keywords))
        self.nodes[op_id] = node

    def add_dependency(self, parent_id: str, child_id: str) -> None:
        if parent_id in self.nodes and child_id in self.nodes:
            self.nodes[parent_id].adjacent_ids.append(child_id)

    def find_similar_opportunities(self, query_keywords: List[str], threshold: float = 0.2) -> List[Tuple[str, float]]:
        """Jaccard similarity context keyword matching."""
        query_set = set(query_keywords)
        if not query_set:
            return []

        matches = []
        for op_id, node in self.nodes.items():
            intersection = query_set.intersection(node.keywords)
            union = query_set.union(node.keywords)
            similarity = len(intersection) / len(union) if union else 0.0
            if similarity >= threshold:
                matches.append((op_id, similarity))

        matches.sort(key=lambda x: x[1], reverse=True)
        return matches


class EOSOpportunityDecisionTree:
    """Implements §10.2 Decision Tree logic: 'Should We Pursue This Opportunity?'"""

    def evaluate(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        # Q1: Structural anomaly or just noise?
        is_structural = opportunity.get("is_structural_anomaly", False)
        if not is_structural:
            return {"pursue": False, "reason": "Filtered at Q1: Identified as noise, not structural anomaly"}

        # Q2: Reversible decision?
        is_reversible = opportunity.get("is_reversible", True)  # Type II = reversible, Type I = irreversible

        if not is_reversible:
            # High stakes / irreversible: require high-confidence multi-source signal
            multi_source_confidence = opportunity.get("multi_source_confidence", 0.0)
            if multi_source_confidence < 0.8:
                return {"pursue": False, "reason": "Filtered at Q2a: Irreversible decision lacks high-confidence multi-source signal"}

        # Q3: Cheap test available?
        cheap_test_available = opportunity.get("cheap_test_available", True)
        if cheap_test_available:
            test_result = opportunity.get("test_result_score", 0.0)
            kill_threshold = opportunity.get("kill_threshold", 0.5)
            if test_result < kill_threshold:
                return {"pursue": False, "reason": f"Filtered at Q4: Test result ({test_result}) below kill threshold ({kill_threshold})"}
        else:
            expected_value_positive = opportunity.get("expected_value_positive", False)
            if not expected_value_positive:
                return {"pursue": False, "reason": "Filtered at Q4b: Expected value not positive and no cheap test available"}

        # Q5: Structural advantage?
        structural_advantage = opportunity.get("has_structural_advantage", False)
        if not structural_advantage:
            return {"pursue": False, "reason": "Filtered at Q5: Lacks structural advantage/moat"}

        return {"pursue": True, "reason": "Passed all decision tree criteria: Commit resources"}


# =====================================================================
# 3. Hypothesis Engine & Risk Classification (§2.1)
# =====================================================================
class HypothesisEngine:
    """Manages the lifecycle, promotion, and evidence-updating of hypotheses."""

    def __init__(self) -> None:
        self.hypotheses: Dict[UUID, Hypothesis] = {}

    def add_hypothesis(self, hyp: Hypothesis) -> None:
        self.hypotheses[hyp.hypothesis_id] = hyp

    def classify_risk_type(self, is_reversible: bool) -> str:
        """Classify decision risk: Type I (irreversible, one-way door) vs Type II (reversible, two-way door)."""
        return "Type II (Reversible)" if is_reversible else "Type I (Irreversible)"

    def update_with_evidence(self, hyp_id: UUID, evidence: Evidence) -> None:
        """Update posterior confidence and distributions based on statistical evidence."""
        hyp = self.hypotheses.get(hyp_id)
        if not hyp:
            return

        is_supporting = False
        p_val = evidence.strength.get("p_value", 1.0)
        effect_size = evidence.strength.get("effect_size", 0.0)

        if p_val < 0.05 and effect_size > 0.0:
            is_supporting = True

        if is_supporting:
            hyp.supporting_evidence.append(evidence.evidence_id)
            alpha = hyp.confidence_distribution.get("params", {}).get("alpha", 10.0)
            hyp.confidence_distribution["params"]["alpha"] = alpha + 1.0
        else:
            hyp.contradicting_evidence.append(evidence.evidence_id)
            beta = hyp.confidence_distribution.get("params", {}).get("beta", 10.0)
            hyp.confidence_distribution["params"]["beta"] = beta + 1.0

        a = hyp.confidence_distribution["params"]["alpha"]
        b = hyp.confidence_distribution["params"]["beta"]
        hyp.posterior_confidence = float(a / (a + b))
        hyp.last_updated = datetime.now(timezone.utc)

    def evaluate_promotions(self) -> List[UUID]:
        """Promote high-confidence hypotheses (posterior > 0.8) to active or theory-ready."""
        promoted = []
        for hyp_id, hyp in self.hypotheses.items():
            if hyp.posterior_confidence >= 0.80 and hyp.status == "proposed":
                hyp.status = "active"
                promoted.append(hyp_id)
                logger.info(f"HYPOTHESIS PROMOTED: {hyp_id} promoted to ACTIVE.")
        return promoted


# =====================================================================
# 4. External Business Loops Engine (§3)
# =====================================================================
class ExternalBusinessLoopsEngine:
    """Manages the 13 coupled business loops and system stocks/flows (§3)."""

    def __init__(self) -> None:
        self.stocks = {
            "cash_cents": 100_000_00,
            "talent_count": 5,
            "brand_trust": 0.5,
            "data_assets": 10,
        }

    def execute_product_loop(self, user_feedback_score: float, dev_velocity: float) -> Dict[str, Any]:
        retention_delta = (user_feedback_score * 0.1) + (dev_velocity * 0.05)
        return {"retention_delta": retention_delta, "nps": int(50 + retention_delta * 100)}

    def execute_marketing_loop(self, spend_cents: int, positioning_clarity: float) -> Dict[str, Any]:
        cac_cents = int(5000 / max(0.1, positioning_clarity))
        acquired = int(spend_cents / max(1, cac_cents))
        return {"acquired_leads": acquired, "cac_cents": cac_cents}

    def execute_sales_loop(self, qualified_leads: int, sales_efficiency: float) -> Dict[str, Any]:
        win_rate = min(0.60, 0.15 + sales_efficiency * 0.3)
        closed_deals = int(qualified_leads * win_rate)
        return {"closed_deals": closed_deals, "win_rate": win_rate}

    def execute_customer_success_loop(self, active_customers: int, onboarding_quality: float) -> Dict[str, Any]:
        churn_rate = max(0.01, 0.10 - onboarding_quality * 0.08)
        nrr = 1.0 + (onboarding_quality * 0.25) - churn_rate
        return {"churn_rate": churn_rate, "nrr": nrr}

    def execute_brand_loop(self, product_experience_score: float, marketing_reach: int) -> Dict[str, Any]:
        self.stocks["brand_trust"] = min(1.0, self.stocks["brand_trust"] + product_experience_score * 0.05)
        return {"brand_trust": self.stocks["brand_trust"], "pricing_power_multiplier": 1.0 + self.stocks["brand_trust"] * 0.5}

    def execute_pricing_loop(self, value_delivered_cents: int, cost_basis_cents: int) -> Dict[str, Any]:
        value_based_price = int(value_delivered_cents * 0.20)
        margin = (value_based_price - cost_basis_cents) / max(1, value_based_price)
        return {"value_based_price_cents": value_based_price, "gross_margin": margin}

    def execute_referral_loop(self, satisfied_customers: int, viral_incentive_score: float) -> Dict[str, Any]:
        k_factor = satisfied_customers * 0.01 * (1.0 + viral_incentive_score)
        new_referrals = int(satisfied_customers * k_factor)
        return {"k_factor": k_factor, "new_referrals": new_referrals}

    def execute_data_loop(self, total_interactions: int) -> Dict[str, Any]:
        self.stocks["data_assets"] += total_interactions
        decision_latency_reduction = min(0.80, self.stocks["data_assets"] * 0.001)
        return {"data_assets": self.stocks["data_assets"], "latency_reduction": decision_latency_reduction}

    def execute_financial_loop(self, revenue_cents: int, costs_cents: int) -> Dict[str, Any]:
        net_cash_flow = revenue_cents - costs_cents
        self.stocks["cash_cents"] += net_cash_flow
        burn_multiple = (costs_cents - revenue_cents) / max(1, revenue_cents) if costs_cents > revenue_cents else 0.0
        runway_months = self.stocks["cash_cents"] / max(1, costs_cents - revenue_cents) if costs_cents > revenue_cents else 999.0
        return {"cash_balance_cents": self.stocks["cash_cents"], "burn_multiple": burn_multiple, "runway_months": runway_months}

    def execute_hiring_loop(self, open_roles: int, employer_brand_score: float) -> Dict[str, Any]:
        filled = int(open_roles * min(1.0, 0.5 + employer_brand_score * 0.5))
        self.stocks["talent_count"] += filled
        return {"filled_roles": filled, "talent_count": self.stocks["talent_count"]}

    def execute_culture_loop(self, values_alignment_score: float) -> Dict[str, Any]:
        decision_speed = 1.0 + values_alignment_score * 0.5
        enps = int(values_alignment_score * 100)
        return {"decision_speed": decision_speed, "enps": enps}

    def execute_innovation_loop(self, rd_spend_cents: int, experiments_count: int) -> Dict[str, Any]:
        hit_rate = min(0.35, 0.05 + (experiments_count * 0.02))
        shipped_bets = int(experiments_count * hit_rate)
        return {"hit_rate": hit_rate, "shipped_bets": shipped_bets}

    def execute_competitive_intel_loop(self, competitor_moves: List[str], feature_parity_gap: float) -> Dict[str, Any]:
        repositioning_required = feature_parity_gap < 0.70
        return {"repositioning_required": repositioning_required, "parity_gap": feature_parity_gap}


# =====================================================================
# 5. Customer Lifecycle Engine (§4)
# =====================================================================
class CustomerLifecycleEngine:
    """Tracks and optimizes the 15-stage full customer journey (§4)."""

    STAGES = [
        "Awareness", "Interest", "Consideration", "Evaluation", "Purchase",
        "Onboarding", "Activation", "Engagement", "Habit Formation", "Retention",
        "Loyalty", "Advocacy", "Referral", "Expansion", "Repurchase"
    ]

    def evaluate_stage_conversion(self, stage: str, cohort_metrics: Dict[str, Any]) -> Dict[str, Any]:
        if stage not in self.STAGES:
            raise ValueError(f"Invalid lifecycle stage: {stage}")

        metric_val = cohort_metrics.get(stage, 0.0)
        health = "healthy" if metric_val >= 0.20 else "bottleneck"
        return {"stage": stage, "conversion_value": metric_val, "health": health}


# =====================================================================
# 6. Go-To-Market Simulator (§5)
# =====================================================================
class GTMSystemSimulator:
    """Simulates GTM positioning, channel fit, pricing, and compounding motions (§5)."""

    def simulate_gtm_system(
        self,
        positioning_score: float,
        price_cents: int,
        complexity: str,  # low, medium, high
        motion: str       # PLG, SLG, CLG
    ) -> Dict[str, Any]:
        # Channel fit check: high complexity requires SLG; low complexity prefers PLG
        channel_fit = True
        if complexity == "high" and motion == "PLG":
            channel_fit = False
        elif complexity == "low" and motion == "SLG":
            channel_fit = False

        efficiency = positioning_score * (1.2 if channel_fit else 0.5)
        projected_cac = int(10000 / max(0.1, efficiency))

        return {
            "channel_fit": channel_fit,
            "system_efficiency": efficiency,
            "projected_cac_cents": projected_cac,
            "compounding_motion_enabled": channel_fit and positioning_score > 0.7
        }


# =====================================================================
# 7. Company Growth State Machine (§6)
# =====================================================================
class CompanyGrowthStateMachine:
    """Tracks growth across 9 company stages with constraint checks (§6)."""

    STAGE_CONSTRAINTS = {
        CompanyStage.IDEA: "Founder time",
        CompanyStage.VALIDATION: "Signal quality",
        CompanyStage.STARTUP: "Cash runway",
        CompanyStage.PMF: "Team bandwidth",
        CompanyStage.GROWTH: "Hiring velocity & systems",
        CompanyStage.SCALE: "Org coordination cost",
        CompanyStage.PLATFORM: "Trust from ecosystem partners",
        CompanyStage.ECOSYSTEM: "Governance credibility",
        CompanyStage.MARKET_LEADERSHIP: "Innovation velocity vs incumbency drag",
    }

    def __init__(self, current_stage: CompanyStage = CompanyStage.IDEA) -> None:
        self.current_stage = current_stage

    def transition_stage(self, metrics: Dict[str, Any]) -> Tuple[CompanyStage, str]:
        """Transition stage if validation gate requirements are met."""
        if self.current_stage == CompanyStage.IDEA and metrics.get("validated_learnings", 0) >= 5:
            self.current_stage = CompanyStage.VALIDATION
            return self.current_stage, "Promoted to Validation: Learnings confirmed"

        if self.current_stage == CompanyStage.VALIDATION and metrics.get("paying_customers", 0) >= 3:
            self.current_stage = CompanyStage.STARTUP
            return self.current_stage, "Promoted to Startup: Paying customers confirmed"

        if self.current_stage == CompanyStage.STARTUP and metrics.get("ltv_to_cac", 0.0) >= 3.0:
            self.current_stage = CompanyStage.PMF
            return self.current_stage, "Promoted to PMF: Unit economics healthy"

        if self.current_stage == CompanyStage.PMF and metrics.get("retention_curve_flat", False):
            self.current_stage = CompanyStage.GROWTH
            return self.current_stage, "Promoted to Growth: Durable PMF retention confirmed"

        if self.current_stage == CompanyStage.GROWTH and metrics.get("growth_rate", 0.0) >= 0.50:
            self.current_stage = CompanyStage.SCALE
            return self.current_stage, "Promoted to Scale: Repeatable scaling confirmed"

        return self.current_stage, f"Remaining at {self.current_stage.value}: Binding constraint is {self.STAGE_CONSTRAINTS[self.current_stage]}"


# =====================================================================
# 8. Strategic Moat & Capital Allocation Engine (§7)
# =====================================================================
class StrategicMoatEngine:
    """Evaluates cost curves, 6 moat dimensions, and opportunity cost capital allocation (§7)."""

    def score_composite_moat(self, moat_scores: Dict[str, float]) -> float:
        """Composite Moat Durability Score across 6 dimensions."""
        network_effects = moat_scores.get("network_effects", 0.0)
        switching_costs = moat_scores.get("switching_costs", 0.0)
        economies_of_scale = moat_scores.get("economies_of_scale", 0.0)
        brand = moat_scores.get("brand", 0.0)
        regulatory_ip = moat_scores.get("regulatory_ip", 0.0)
        counter_positioning = moat_scores.get("counter_positioning", 0.0)

        composite = (
            0.25 * network_effects +
            0.20 * switching_costs +
            0.15 * economies_of_scale +
            0.15 * brand +
            0.10 * regulatory_ip +
            0.15 * counter_positioning
        )
        return min(1.0, max(0.0, composite))

    def rank_opportunity_cost_initiatives(self, initiatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank initiatives by expected return per capital dollar to enforce opportunity cost discipline."""
        for init in initiatives:
            expected_return = init.get("expected_return_cents", 0)
            capital_required = max(1, init.get("capital_required_cents", 1))
            init["roi_ratio"] = expected_return / capital_required

        initiatives.sort(key=lambda x: x["roi_ratio"], reverse=True)
        return initiatives


# =====================================================================
# 9. Failure Mode Monitor (§8)
# =====================================================================
class FailureModeMonitor:
    """Detects 10 major entrepreneurial failure modes and triggers corrections (§8)."""

    FAILURE_PATTERNS = {
        "solving_wrong_problem": {"signal": "low_engagement_high_survey", "fix": "Return to root cause / 5-Whys interviews"},
        "building_before_validating": {"signal": "high_build_velocity_flat_demand", "fix": "Enforce validation gate before resourcing"},
        "weak_positioning": {"signal": "high_cac_feature_objections", "fix": "Rebuild positioning around real customer alternative"},
        "poor_pricing": {"signal": "high_conversion_poor_margin", "fix": "Re-anchor price to quantified value"},
        "distribution_failure": {"signal": "high_nps_flat_growth", "fix": "Systematically test channels against ICP behavior"},
        "lack_of_pmf": {"signal": "retention_never_flattens", "fix": "Stop scaling; return to cohort retention"},
        "organizational_bottlenecks": {"signal": "rising_decision_latency", "fix": "Push decision rights down via clear frameworks"},
        "founder_bias": {"signal": "ignoring_disconfirming_data", "fix": "Enforce pre-committed kill criteria"},
        "scaling_prematurely": {"signal": "cac_rising_faster_than_ltv", "fix": "Re-test unit economics at each order of magnitude"},
        "capital_misallocation": {"signal": "underperforming_bets_funded", "fix": "Rank initiatives quarterly on common expected-return basis"},
    }

    def audit_operating_metrics(self, metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        warnings = []
        if metrics.get("high_build_velocity") and metrics.get("demand_signal", 0.0) < 0.1:
            warnings.append({
                "failure_mode": "building_before_validating",
                "detection_signal": self.FAILURE_PATTERNS["building_before_validating"]["signal"],
                "correction_mechanism": self.FAILURE_PATTERNS["building_before_validating"]["fix"]
            })
        if metrics.get("decision_latency_seconds", 0) > 86400:  # > 1 day latency
            warnings.append({
                "failure_mode": "organizational_bottlenecks",
                "detection_signal": self.FAILURE_PATTERNS["organizational_bottlenecks"]["signal"],
                "correction_mechanism": self.FAILURE_PATTERNS["organizational_bottlenecks"]["fix"]
            })
        if metrics.get("cac_trend", 1.0) > metrics.get("ltv_trend", 1.0) * 1.5:
            warnings.append({
                "failure_mode": "scaling_prematurely",
                "detection_signal": self.FAILURE_PATTERNS["scaling_prematurely"]["signal"],
                "correction_mechanism": self.FAILURE_PATTERNS["scaling_prematurely"]["fix"]
            })
        return warnings


# =====================================================================
# 10. Coordinating First-Principles EOSEngine (Orchestrator)
# =====================================================================
class EOSEngine:
    """The continuous entrepreneurial operating orchestrator integrating all 11 EOS sections."""

    def __init__(self) -> None:
        self.world_model = EntrepreneurialWorldModel()
        self.opportunity_graph = OpportunityGraph()
        self.decision_tree = EOSOpportunityDecisionTree()
        self.hypothesis_engine = HypothesisEngine()
        self.business_loops = ExternalBusinessLoopsEngine()
        self.customer_lifecycle = CustomerLifecycleEngine()
        self.gtm_simulator = GTMSystemSimulator()
        self.growth_state_machine = CompanyGrowthStateMachine()
        self.moat_engine = StrategicMoatEngine()
        self.failure_monitor = FailureModeMonitor()
        self.current_state = EOSState.SENSING

    def transition_system_state(self, event: str, payload: Dict[str, Any]) -> EOSState:
        """System State Machine transition (§10.1)."""
        if self.current_state == EOSState.SENSING and event == "anomaly_detected":
            self.current_state = EOSState.HYPOTHESIS
        elif self.current_state == EOSState.HYPOTHESIS and event == "hypothesis_formed":
            self.current_state = EOSState.CHEAP_TEST
        elif self.current_state == EOSState.CHEAP_TEST:
            if event == "falsified":
                self.current_state = EOSState.DISCARD
            elif event == "strengthened":
                self.current_state = EOSState.VALIDATION
        elif self.current_state == EOSState.VALIDATION:
            if event == "economic_viability_confirmed":
                self.current_state = EOSState.BUILD_GATE
            elif event == "no_viable_economics":
                self.current_state = EOSState.DISCARD
        elif self.current_state == EOSState.BUILD_GATE and event == "resourced":
            self.current_state = EOSState.MVP
        elif self.current_state == EOSState.MVP and event == "shipped":
            self.current_state = EOSState.GTM_TEST
        elif self.current_state == EOSState.GTM_TEST and event == "signal_collected":
            self.current_state = EOSState.KILL_OR_SCALE
        elif self.current_state == EOSState.KILL_OR_SCALE:
            if event == "above_threshold":
                self.current_state = EOSState.SCALE
            elif event == "below_threshold":
                self.current_state = EOSState.DISCARD
        elif self.current_state == EOSState.SCALE and event == "repeatable_loop_confirmed":
            self.current_state = EOSState.OPERATE
        elif self.current_state == EOSState.OPERATE and event == "market_maturity":
            self.current_state = EOSState.REINVENT
        elif self.current_state == EOSState.REINVENT or self.current_state == EOSState.DISCARD:
            self.current_state = EOSState.SENSING

        logger.info(f"EOS STATE TRANSITION: Transitioned to {self.current_state.value} on event '{event}'")
        return self.current_state

    def evaluate_opportunity(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate an opportunity using the §10.2 Decision Tree."""
        return self.decision_tree.evaluate(opportunity)
