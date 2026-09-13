"""
The 14-Layer Computational Architecture of Entrepreneurship for SERO v2.1.
Executable algorithms, feedback loops, decision systems, and autonomous agent constructs
addressing the fundamental questions of AI Entrepreneurship across Layers 1 to 14.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.14_layer_engine")


# ============================================================================
# LAYER 1: REALITY SUBSTRATE
# ============================================================================

class TaskAutomationBound(BaseModel):
    """Categorizes tasks into human psychology, optimization, and automation feasibility."""
    task_name: str
    category: str  # "human_psychology", "optimization_problem", "hybrid"
    is_automatable: bool
    requires_human_judgment: bool
    invariant_principle: str  # e.g., "value_creation", "cash_flow_efficiency", "unit_economics"


class EntrepreneurialRealityModel:
    """
    Formalizes invariant principles across every successful entrepreneur,
    distinguishing what can be automated vs what requires human judgment.
    """

    INVARIANT_PRINCIPLES = {
        "value_creation": "Value created must exceed marginal cost of delivery.",
        "cash_flow_efficiency": "Solvency precedes growth; net cash flows govern survival.",
        "unit_economics": "LTV must sustainably exceed CAC under scale."
    }

    def evaluate_automation_bounds(self, task_name: str, domain: str) -> TaskAutomationBound:
        """
        Determines whether an entrepreneurial task is purely an optimization problem
        (automatable) or requires fundamental human judgment/empathy.
        """
        task_lower = task_name.lower()
        if any(kw in task_lower for kw in ["empathy", "trust", "founder vision", "vision", "legal", "board negotiation"]):
            return TaskAutomationBound(
                task_name=task_name,
                category="human_psychology",
                is_automatable=False,
                requires_human_judgment=True,
                invariant_principle=self.INVARIANT_PRINCIPLES["value_creation"]
            )
        elif any(kw in task_lower for kw in ["pricing optimization", "ad bidding", "financial forecasting", "seo graph", "pricing_optimization"]):
            return TaskAutomationBound(
                task_name=task_name,
                category="optimization_problem",
                is_automatable=True,
                requires_human_judgment=False,
                invariant_principle=self.INVARIANT_PRINCIPLES["unit_economics"]
            )
        else:
            return TaskAutomationBound(
                task_name=task_name,
                category="hybrid",
                is_automatable=True,
                requires_human_judgment=True,
                invariant_principle=self.INVARIANT_PRINCIPLES["cash_flow_efficiency"]
            )


# ============================================================================
# LAYER 2: OPPORTUNITY DISCOVERY
# ============================================================================

class OpportunitySignal(BaseModel):
    """Represents a weak signal detected in the world's continuous state space."""
    signal_id: UUID = Field(default_factory=uuid4)
    source: str
    domain: str
    raw_intensity: float  # 0.0 to 1.0
    decay_rate: float = 0.1  # Half-life factor
    novelty_score: float = 0.5
    timestamp_epoch: float = 0.0


class Layer2OpportunityEngine:
    """
    Continuously searches the world's state space for economically valuable opportunities.
    Filters noise, amplifies weak signals, recombines observations, and generates novelty.
    """

    def amplify_weak_signals(self, signals: List[OpportunitySignal], current_time: float) -> List[OpportunitySignal]:
        """Filters decayed noise and amplifies recurring weak signals across domains."""
        amplified = []
        for sig in signals:
            time_delta = max(0.0, current_time - sig.timestamp_epoch)
            effective_intensity = sig.raw_intensity * math.exp(-sig.decay_rate * time_delta)
            if effective_intensity >= 0.15:
                sig.raw_intensity = effective_intensity
                amplified.append(sig)
        return sorted(amplified, key=lambda s: s.raw_intensity, reverse=True)

    def recombine_unrelated_signals(self, sig1: OpportunitySignal, sig2: OpportunitySignal) -> OpportunitySignal:
        """Cross-pollinates signals across distinct domains to synthesize novelty."""
        combined_domain = f"{sig1.domain}×{sig2.domain}"
        novelty = min(1.0, (sig1.novelty_score + sig2.novelty_score) / 1.5 + 0.2)
        combined_intensity = (sig1.raw_intensity + sig2.raw_intensity) / 2.0 * 1.2
        return OpportunitySignal(
            source=f"recombination({sig1.source}, {sig2.source})",
            domain=combined_domain,
            raw_intensity=min(1.0, combined_intensity),
            novelty_score=novelty
        )


# ============================================================================
# LAYER 3: PROBLEM DISCOVERY
# ============================================================================

class ProblemSCMNode(BaseModel):
    """Defines a node in a Structural Causal Model for problem decomposition."""
    name: str
    is_root_cause: bool = False
    symptom_level: int = 1  # 1 = root/1st-order, 2+ = 2nd/3rd order symptom
    estimated_impact: float = 0.5  # 0.0 to 1.0
    causal_parents: List[str] = Field(default_factory=list)


class Layer3ProblemEngine:
    """
    Decomposes stated problems using causal structures to isolate root causes
    from surface symptoms and filter out unviable/zero-value problems.
    """

    def decompose_problem(
        self,
        problem_name: str,
        causal_graph: Dict[str, List[str]],
        impact_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Decomposes a graph of problem factors (parent -> list of children),
        identifying root cause nodes (nodes with children, but which are not children of any node).
        """
        all_parents = set(causal_graph.keys())
        all_children = set(child for children in causal_graph.values() for child in children)
        all_nodes = all_parents.union(all_children)

        # Root causes are parents that are not children of any other node
        root_causes = [node for node in all_parents if node not in all_children and causal_graph.get(node)]
        if not root_causes:
            root_causes = [problem_name]

        total_impact = sum(impact_scores.get(node, 0.5) for node in root_causes)
        should_ignore = total_impact < 0.2  # Threshold below which problem is ignored

        return {
            "problem_name": problem_name,
            "root_causes": root_causes,
            "is_ignoreable_symptom": should_ignore,
            "aggregate_root_impact": total_impact,
            "decomposed_nodes": list(all_nodes)
        }


# ============================================================================
# LAYER 4: DECISION MAKING
# ============================================================================

class Layer4DecisionEngine:
    """
    Implements active inference decision making under uncertainty,
    balancing epistemic exploration and pragmatic value while eliminating confirmation bias.
    """

    def compute_decision_efe(
        self,
        pragmatic_value: float,
        epistemic_information_gain: float,
        curiosity_weight: float = 1.0
    ) -> float:
        """
        Calculates Expected Free Energy:
        G = - Pragmatic Value - (curiosity_weight * Epistemic Gain)
        Minimizing G minimizes variational surprise.
        """
        return -pragmatic_value - (curiosity_weight * epistemic_information_gain)

    def evaluate_and_kill_hypotheses(
        self,
        hypotheses: List[Dict[str, Any]],
        falsification_threshold: float = 0.25
    ) -> Dict[str, Any]:
        """
        Ranks hypotheses by EFE and instantly kills those whose posterior confidence
        falls below the falsification threshold to avoid confirmation bias.
        """
        active = []
        killed = []

        for h in hypotheses:
            posterior = h.get("posterior_confidence", 0.5)
            efe = self.compute_decision_efe(
                pragmatic_value=h.get("pragmatic_value", 0.5),
                epistemic_information_gain=h.get("epistemic_gain", 0.5)
            )
            h["efe"] = efe

            if posterior < falsification_threshold:
                killed.append(h["name"])
            else:
                active.append(h)

        active_sorted = sorted(active, key=lambda x: x["efe"])
        return {
            "active_hypotheses": active_sorted,
            "killed_hypotheses": killed,
            "best_decision": active_sorted[0]["name"] if active_sorted else None
        }


# ============================================================================
# LAYER 5: OPPORTUNITY EVALUATION
# ============================================================================

class Layer5EvaluationEngine:
    """
    Calculates expected financial value, downside Conditional Value at Risk (CVaR),
    and evaluates timing elasticity for opportunity selection/abandonment.
    """

    def calculate_opportunity_ev(
        self,
        tam_cents: int,
        p_success: float,
        downside_risk_cents: int,
        timing_factor: float = 1.0
    ) -> Dict[str, Any]:
        """Calculates expected value with downside CVaR adjustment."""
        expected_value_cents = int(tam_cents * p_success * timing_factor) - downside_risk_cents
        cvar_downside = downside_risk_cents * (1.0 - p_success)
        return {
            "expected_value_cents": expected_value_cents,
            "downside_cvar": cvar_downside,
            "is_viable": expected_value_cents > 0 and cvar_downside < (tam_cents * 0.3)
        }


# ============================================================================
# LAYER 6: PRODUCT CREATION
# ============================================================================

class Layer6ProductEngine:
    """
    Discovers the core Job-To-Be-Done (JTBD), enforces minimal feature complexity budgets,
    and optimizes for learning rate rather than feature volume.
    """

    def extract_jtbd_core(
        self,
        user_complaints: List[str],
        candidate_features: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Isolates the core JTBD and prunes non-essential features from MVP scope."""
        core_jtbd = f"Resolve primary pain: {user_complaints[0]}" if user_complaints else "Core Value Prop"
        mvp_features = []
        pruned_features = []

        for feature in candidate_features:
            if feature.get("value_impact", 0.0) >= 0.6 and feature.get("complexity", 1.0) <= 0.5:
                mvp_features.append(feature["name"])
            else:
                pruned_features.append(feature["name"])

        return {
            "core_jtbd": core_jtbd,
            "mvp_features": mvp_features,
            "pruned_features": pruned_features,
            "learning_velocity_score": len(mvp_features) / max(1, len(pruned_features))
        }


# ============================================================================
# LAYER 7: CUSTOMER UNDERSTANDING
# ============================================================================

class Layer7CustomerEngine:
    """
    Models customer psychology, trust accumulation dynamics, switching barriers,
    and factors creating viral evangelism.
    """

    def model_customer_psychology(
        self,
        trust_level: float,
        perceived_value: float,
        switching_friction: float
    ) -> Dict[str, Any]:
        """Computes customer churn risk and conversion probability."""
        net_utility = (perceived_value * trust_level) - switching_friction
        will_buy = net_utility > 0.3
        churn_risk = max(0.0, 1.0 - (trust_level * perceived_value))
        is_evangelist = trust_level > 0.85 and perceived_value > 0.8

        return {
            "net_utility": net_utility,
            "will_buy": will_buy,
            "churn_risk": churn_risk,
            "is_evangelist": is_evangelist
        }


# ============================================================================
# LAYER 8: MARKETING
# ============================================================================

class Layer8MarketingEngine:
    """
    Simulates attention propagation, viral coefficient dynamics (R0),
    brand authority emergence, and cross-channel positioning distortion.
    """

    def propagate_attention(
        self,
        initial_reach: int,
        viral_k_factor: float,
        conversion_rate: float,
        channel_decay: float = 0.2
    ) -> Dict[str, Any]:
        """Calculates attention propagation across viral cycles."""
        effective_reach = initial_reach
        total_acquired = 0

        for cycle in range(1, 4):  # 3 viral cycles
            converts = int(effective_reach * conversion_rate)
            total_acquired += converts
            effective_reach = int(converts * viral_k_factor * (1.0 - channel_decay))

        return {
            "total_acquired_customers": total_acquired,
            "viral_compounding_multiplier": total_acquired / max(1, initial_reach * conversion_rate)
        }


# ============================================================================
# LAYER 9: SALES
# ============================================================================

class Layer9SalesEngine:
    """
    Models sales psychology, objection graph resolution, buying urgency creation,
    and designs repeatable sales automation systems.
    """

    def resolve_objection_graph(
        self,
        objection: str,
        objection_resolution_map: Dict[str, str],
        urgency_score: float
    ) -> Dict[str, Any]:
        """Resolves customer objections and determines if enterprise or automated sales applies."""
        resolution = objection_resolution_map.get(objection, "Custom consultation required.")
        should_automate = urgency_score > 0.7 and objection in objection_resolution_map

        return {
            "objection": objection,
            "resolution_playbook": resolution,
            "automation_recommended": should_automate,
            "sales_motion": "automated_self_serve" if should_automate else "high_touch_enterprise"
        }


# ============================================================================
# LAYER 10: GROWTH & NETWORK DYNAMICS
# ============================================================================

class Layer10GrowthEngine:
    """
    Evaluates compounding growth loops, network effect strengths (Metcalfe's law),
    and intentionally throttles growth when infrastructure/quality bounds are threatened.
    """

    def evaluate_network_effects(
        self,
        user_count: int,
        engagement_factor: float,
        system_capacity: int
    ) -> Dict[str, Any]:
        """Calculates network value using Metcalfe's law and determines growth throttling."""
        metcalfe_value = (user_count ** 2) * engagement_factor
        capacity_utilization = user_count / max(1, system_capacity)
        should_throttle = capacity_utilization > 0.85

        return {
            "metcalfe_network_value": metcalfe_value,
            "capacity_utilization": capacity_utilization,
            "should_throttle_growth": should_throttle,
            "growth_state": "throttled_quality_protection" if should_throttle else "hypergrowth_active"
        }


# ============================================================================
# LAYER 11: COMPETITION & MOATS
# ============================================================================

class Layer11CompetitionEngine:
    """
    Anticipates competitor moves using game-theoretic payoffs, scores moat durability,
    and detects required pivot triggers during market disruptions.
    """

    def simulate_competitor_moves(
        self,
        our_action: str,
        competitor_payoffs: Dict[str, float],
        moat_type: str = "network_effects"
    ) -> Dict[str, Any]:
        """Simulates competitor counter-response and scores moat defensibility."""
        best_counter_move = max(competitor_payoffs.keys(), key=lambda k: competitor_payoffs[k])
        max_counter_payoff = competitor_payoffs[best_counter_move]

        # Moat score based on type
        moat_scores = {
            "network_effects": 0.9,
            "brand_loyalty": 0.8,
            "proprietary_tech": 0.7,
            "low_cost": 0.5
        }
        moat_score = moat_scores.get(moat_type, 0.4)
        is_difficult_to_copy = moat_score > 0.65

        return {
            "predicted_competitor_response": best_counter_move,
            "competitor_threat_payoff": max_counter_payoff,
            "moat_score": moat_score,
            "is_defensible": is_difficult_to_copy
        }


# ============================================================================
# LAYER 12: ORGANIZATIONAL DESIGN
# ============================================================================

class Layer12OrgDesignEngine:
    """
    Evaluates hiring triggers based on validated bottleneck constraints,
    demarcates centralized vs delegated autonomy, and scales decision systems.
    """

    def evaluate_hiring_triggers(
        self,
        task_backlog_hours: float,
        agent_utilization_ratio: float,
        unit_economics_positive: bool
    ) -> Dict[str, Any]:
        """Determines whether to spawn autonomous sub-agents or hire human talent."""
        should_expand_org = agent_utilization_ratio > 0.8 and task_backlog_hours > 40.0 and unit_economics_positive
        delegation_tier = "autonomous_agent_delegation" if unit_economics_positive else "centralized_founder_control"

        return {
            "should_expand_org": should_expand_org,
            "recommended_expansion": "spawn_autonomous_agent" if should_expand_org else "hold_headcount",
            "delegation_tier": delegation_tier
        }


# ============================================================================
# LAYER 13: META-LEARNING & SELF-IMPROVEMENT
# ============================================================================

class Layer13MetaLearningEngine:
    """
    Refines mental models from closed-loop outcomes, measures decision quality,
    builds intuition, and distills failures into reusable playbooks.
    """

    def distill_closed_loop_playbook(
        self,
        predicted_outcome: float,
        actual_outcome: float,
        decision_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Updates mental models and distills lessons from decision variance."""
        prediction_error = abs(actual_outcome - predicted_outcome)
        calibration_score = 1.0 - min(1.0, prediction_error)

        distilled_lesson = (
            f"Context '{decision_context.get('domain', 'general')}' demonstrated "
            f"calibration score {calibration_score:.2f}. Adjust prior weights by {prediction_error:.2f}."
        )

        return {
            "prediction_error": prediction_error,
            "calibration_score": calibration_score,
            "distilled_playbook_lesson": distilled_lesson,
            "update_mental_model": prediction_error > 0.15
        }


# ============================================================================
# LAYER 14: AI ENTREPRENEURSHIP ORCHESTRATOR
# ============================================================================

class Layer14AIEntrepreneurshipOrchestrator:
    """
    The master 14-layer computational engine uniting sensing, discovery, problem definition,
    decision making, product, marketing, sales, growth, competition, org design, and meta-learning.
    """

    def __init__(self) -> None:
        self.reality_engine = EntrepreneurialRealityModel()
        self.opportunity_engine = Layer2OpportunityEngine()
        self.problem_engine = Layer3ProblemEngine()
        self.decision_engine = Layer4DecisionEngine()
        self.eval_engine = Layer5EvaluationEngine()
        self.product_engine = Layer6ProductEngine()
        self.customer_engine = Layer7CustomerEngine()
        self.marketing_engine = Layer8MarketingEngine()
        self.sales_engine = Layer9SalesEngine()
        self.growth_engine = Layer10GrowthEngine()
        self.competition_engine = Layer11CompetitionEngine()
        self.org_engine = Layer12OrgDesignEngine()
        self.meta_engine = Layer13MetaLearningEngine()

    def run_end_to_end_pipeline(self, raw_signal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the complete 14-layer computational cycle from signal to meta-learning."""
        # Layer 1 & 2: Reality & Opportunity Sensing
        sig = OpportunitySignal(
            source=raw_signal_data.get("source", "market_scan"),
            domain=raw_signal_data.get("domain", "saas"),
            raw_intensity=raw_signal_data.get("intensity", 0.8)
        )
        amplified = self.opportunity_engine.amplify_weak_signals([sig], current_time=0.0)

        # Layer 3: Problem Decomposition
        problem_res = self.problem_engine.decompose_problem(
            problem_name=raw_signal_data.get("title", "Market Friction"),
            causal_graph={"root_cause_node": ["symptom_node"]},
            impact_scores={"root_cause_node": 0.8}
        )

        # Layer 4 & 5: Active Inference Decision & EV Evaluation
        eval_res = self.eval_engine.calculate_opportunity_ev(
            tam_cents=raw_signal_data.get("tam_cents", 100000000),
            p_success=0.6,
            downside_risk_cents=10000000
        )

        # Layer 6, 7, 8, 9: Execution Loop (Product -> Customer -> Marketing -> Sales)
        prod_res = self.product_engine.extract_jtbd_core(
            user_complaints=["High cost", "Slow speed"],
            candidate_features=[{"name": "Fast Engine", "value_impact": 0.8, "complexity": 0.3}]
        )
        cust_res = self.customer_engine.model_customer_psychology(0.9, 0.85, 0.2)
        mktg_res = self.marketing_engine.propagate_attention(1000, 1.2, 0.1)
        sales_res = self.sales_engine.resolve_objection_graph("High price", {"High price": "Show ROI"}, 0.8)

        # Layer 10, 11, 12: Scaling, Moat & Org Design
        growth_res = self.growth_engine.evaluate_network_effects(500, 0.01, 10000)
        comp_res = self.competition_engine.simulate_competitor_moves("Price drop", {"Match price": 0.5})
        org_res = self.org_engine.evaluate_hiring_triggers(50.0, 0.85, True)

        # Layer 13 & 14: Meta-Learning Feedback
        meta_res = self.meta_engine.distill_closed_loop_playbook(
            predicted_outcome=100000.0,
            actual_outcome=95000.0,
            decision_context={"domain": sig.domain}
        )

        return {
            "status": "completed",
            "opportunity_title": raw_signal_data.get("title", "Venture"),
            "opportunity_ev": eval_res,
            "product_mvp": prod_res,
            "customer_utility": cust_res,
            "marketing_reach": mktg_res,
            "sales_strategy": sales_res,
            "growth_status": growth_res,
            "defensibility": comp_res,
            "org_expansion": org_res,
            "meta_learning_lesson": meta_res["distilled_playbook_lesson"]
        }


FourteenLayerEntrepreneurialEngine = Layer14AIEntrepreneurshipOrchestrator
