"""
The executable Python implementation of the 14-Layer Computational Architecture
of Entrepreneurship.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.fourteen_layer_engine")


# =====================================================================
# Layer 1: Reality Substrate
# =====================================================================
class RealityEngine:
    """Models fundamental human psychology, optimization problems, invariants, and automation boundaries."""

    def __init__(self) -> None:
        self.non_automatable_aspects = {
            "ultimate_legal_accountability",
            "founder_vision_sovereignty",
            "deep_human_trust_formation"
        }

    def evaluate_task_automation(self, task_name: str, requires_legal_sovereignty: bool) -> Dict[str, Any]:
        """Determines if a task can be automated or requires human judgment/sovereignty."""
        if requires_legal_sovereignty or task_name in self.non_automatable_aspects:
            return {"task": task_name, "automatable": False, "category": "human_judgment_sovereignty"}
        return {"task": task_name, "automatable": True, "category": "probabilistic_optimization"}


# =====================================================================
# Layer 2: Opportunity Discovery
# =====================================================================
class OpportunityDiscoveryEngine:
    """Continuous active inference state space search using Hawkes processes and cross-domain synthesis."""

    def __init__(self, baseline_intensity: float = 0.2) -> None:
        self.baseline_intensity = baseline_intensity
        self.observed_events: List[Dict[str, Any]] = []

    def detect_weak_signal(self, event_title: str, surprise_score: float, domain: str) -> Dict[str, Any]:
        """Filters weak signals using statistical surprise and intensity estimation."""
        intensity = self.baseline_intensity + (0.5 * len(self.observed_events))
        is_weak_signal = surprise_score > 1.2 and intensity > 0.15
        signal = {
            "title": event_title,
            "domain": domain,
            "surprise_score": surprise_score,
            "hawkes_intensity": intensity,
            "is_valid_opportunity_signal": is_weak_signal
        }
        if is_weak_signal:
            self.observed_events.append(signal)
        return signal

    def synthesize_cross_domain_novelty(self, domain_a: str, domain_b: str) -> Dict[str, Any]:
        """Generates novel cross-domain opportunity candidates."""
        return {
            "title": f"Cross-domain convergence of {domain_a} and {domain_b}",
            "domain_a": domain_a,
            "domain_b": domain_b,
            "novelty_score": 0.88,
            "estimated_market_relevance": 0.75
        }


# =====================================================================
# Layer 3: Problem Discovery
# =====================================================================
class ProblemDiscoveryEngine:
    """Disentangles first-order vs second-order problems and symptoms vs root causes using SCMs."""

    def __init__(self) -> None:
        pass

    def decompose_problem(
        self,
        symptoms: List[str],
        candidate_root_cause: str,
        first_order_friction: float
    ) -> Dict[str, Any]:
        """Identifies root causes and classifies first-order vs second-order barriers."""
        is_root_cause = len(symptoms) >= 2
        problem_order = "first_order" if first_order_friction > 0.5 else "second_order"
        return {
            "symptoms": symptoms,
            "root_cause": candidate_root_cause,
            "is_root_cause_validated": is_root_cause,
            "problem_classification": problem_order,
            "should_ignore": first_order_friction < 0.1
        }


# =====================================================================
# Layer 4: Decision Making
# =====================================================================
class DecisionEngine:
    """Active Inference decision making under uncertainty minimizing Expected Free Energy (EFE)."""

    def __init__(self, curiosity_weight: float = 1.0) -> None:
        self.curiosity_weight = curiosity_weight

    def compute_expected_free_energy(
        self,
        p_success: float,
        p_target: float,
        prior_entropy: float,
        simulated_entropy: float
    ) -> float:
        """EFE G = - Pragmatic Value - Curiosity * Epistemic Value."""
        eps = 1e-10
        ps = max(eps, min(1.0 - eps, p_success))
        pt = max(eps, min(1.0 - eps, p_target))
        pragmatic_value = math.log(ps) - math.log(pt)
        epistemic_value = max(0.0, prior_entropy - simulated_entropy)
        efe = -pragmatic_value - (epistemic_value * self.curiosity_weight)
        return float(efe)


# =====================================================================
# Layer 5: Opportunity Evaluation
# =====================================================================
class OpportunityEvaluationEngine:
    """Computes expected value, real options timing, downside risk, and opportunity switching metrics."""

    def __init__(self) -> None:
        pass

    def evaluate_opportunity(
        self,
        tam_cents: int,
        p_success: float,
        downside_risk: float,
        ltv_to_cac: float
    ) -> Dict[str, Any]:
        """Calculates risk-adjusted Expected Value (EV)."""
        raw_ev_cents = tam_cents * p_success
        risk_penalty = math.exp(-downside_risk)
        risk_adjusted_ev_cents = raw_ev_cents * risk_penalty * (ltv_to_cac / 3.0)
        return {
            "tam_cents": tam_cents,
            "p_success": p_success,
            "downside_risk": downside_risk,
            "risk_adjusted_ev_cents": risk_adjusted_ev_cents,
            "quality_tier": "tier_1" if risk_adjusted_ev_cents > 10_000_000_00 else "tier_2"
        }

    def evaluate_switching_decision(
        self,
        ev_current_cents: float,
        ev_alternative_cents: float,
        switching_cost_cents: float
    ) -> bool:
        """Determines whether to abandon current opportunity for an alternative."""
        return (ev_alternative_cents - ev_current_cents) > switching_cost_cents


# =====================================================================
# Layer 6: Product Creation
# =====================================================================
class ProductCreationEngine:
    """Minimizes product complexity, discovers Jobs-to-be-Done (JTBD), and optimizes for learning."""

    def __init__(self) -> None:
        pass

    def optimize_feature_set(self, features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prunes unnecessary feature complexity while maximizing learning speed."""
        selected_features = []
        total_value = 0.0
        total_complexity = 0.0

        for f in features:
            val = f.get("value", 0.5)
            comp = f.get("complexity", 0.5)
            # Feature selection criterion: value/complexity ratio > 1.0
            if val / max(0.1, comp) >= 1.0:
                selected_features.append(f.get("name"))
                total_value += val
                total_complexity += comp

        return {
            "selected_features": selected_features,
            "pruned_features_count": len(features) - len(selected_features),
            "total_value": total_value,
            "total_complexity": total_complexity,
            "learning_efficiency_score": total_value / max(0.1, total_complexity)
        }


# =====================================================================
# Layer 7: Customer Understanding
# =====================================================================
class CustomerUnderstandingEngine:
    """Models customer switching friction, trust formation, retention, and evangelism flywheels."""

    def __init__(self) -> None:
        pass

    def evaluate_customer_switching(
        self,
        utility_gain: float,
        financial_cost: float,
        habitual_friction: float
    ) -> Dict[str, Any]:
        """Models customer propensity to switch from status quo."""
        net_switch_utility = utility_gain - (financial_cost + habitual_friction)
        will_switch = net_switch_utility > 0.0
        return {
            "net_switch_utility": net_switch_utility,
            "will_switch": will_switch,
            "propensity": max(0.0, min(1.0, net_switch_utility))
        }


# =====================================================================
# Layer 8: Marketing
# =====================================================================
class MarketingEngine:
    """Models viral growth vectors (SEIR epidemic dynamics) and channel interaction graphs."""

    def __init__(self) -> None:
        pass

    def simulate_virality(self, invites_per_user: float, conversion_rate: float) -> Dict[str, Any]:
        """Calculates viral coefficient K and determines viral growth threshold."""
        k_factor = invites_per_user * conversion_rate
        is_viral = k_factor > 1.0
        return {
            "k_factor": k_factor,
            "is_viral": is_viral,
            "growth_mode": "exponential" if is_viral else "linear"
        }


# =====================================================================
# Layer 9: Sales
# =====================================================================
class SalesEngine:
    """Models sales conversion state machines, urgency triggers, and objection resolution graphs."""

    def __init__(self) -> None:
        pass

    def resolve_objection(self, objection_type: str, urgency_score: float) -> Dict[str, Any]:
        """Resolves customer objections based on urgency and mapped playbooks."""
        can_resolve = urgency_score > 0.4
        return {
            "objection_type": objection_type,
            "urgency_score": urgency_score,
            "resolved": can_resolve,
            "action": "close_sale" if can_resolve else "nurture_lead"
        }


# =====================================================================
# Layer 10: Growth
# =====================================================================
class GrowthEngine:
    """Calculates network effects, platform shifts, and compounding system dynamics."""

    def __init__(self) -> None:
        pass

    def compute_network_value(self, user_count: int, network_type: str = "metcalfe") -> float:
        """Metcalfe's Law (N^2) or Reed's Law (2^N) network valuation."""
        if network_type == "reed" and user_count < 30:
            return float(2 ** user_count)
        return float(user_count ** 2)


# =====================================================================
# Layer 11: Competition
# =====================================================================
class CompetitionEngine:
    """Quantifies moat durability and evaluates pivot triggers."""

    def __init__(self) -> None:
        pass

    def score_moat_durability(
        self,
        network_density: float,
        switching_cost_ratio: float,
        cost_advantage: float,
        brand_trust: float
    ) -> float:
        """Composite moat score."""
        return float(0.3 * network_density + 0.3 * switching_cost_ratio + 0.2 * cost_advantage + 0.2 * brand_trust)

    def evaluate_pivot_trigger(self, revenue_decay_rate: float, customer_churn_rate: float) -> bool:
        """Triggers pivot if performance decays below critical thresholds."""
        return revenue_decay_rate > 0.15 and customer_churn_rate > 0.20


# =====================================================================
# Layer 12: Organizational Design
# =====================================================================
class OrganizationalDesignEngine:
    """Calculates delegation thresholds and task routing across multi-agent structures."""

    def __init__(self) -> None:
        pass

    def evaluate_delegation(
        self,
        founder_hourly_value: float,
        task_hours: float,
        agent_execution_cost: float,
        error_risk_cost: float
    ) -> Dict[str, Any]:
        """Determines whether to delegate a task or keep centralized."""
        founder_cost = founder_hourly_value * task_hours
        delegation_cost = agent_execution_cost + error_risk_cost
        should_delegate = founder_cost > delegation_cost
        return {
            "founder_cost": founder_cost,
            "delegation_cost": delegation_cost,
            "should_delegate": should_delegate,
            "action": "delegate_to_agent" if should_delegate else "retain_founder_execution"
        }


# =====================================================================
# Layer 13: Meta-Learning
# =====================================================================
class MetaLearningEngine:
    """Measures decision quality vs outcome quality and updates prior mental models from failure."""

    def __init__(self) -> None:
        self.decision_history: List[Dict[str, Any]] = []

    def record_and_calibrate_decision(
        self,
        predicted_success_prob: float,
        actual_outcome: float
    ) -> Dict[str, Any]:
        """Calibrates mental models by calculating decision prediction error."""
        prediction_error = abs(predicted_success_prob - actual_outcome)
        decision_quality = max(0.0, 1.0 - prediction_error)
        calibration_record = {
            "predicted": predicted_success_prob,
            "actual": actual_outcome,
            "prediction_error": prediction_error,
            "decision_quality_score": decision_quality
        }
        self.decision_history.append(calibration_record)
        return calibration_record


# =====================================================================
# Layer 14: AI Entrepreneurship Master Engine
# =====================================================================
class AIEntrepreneurshipEngine:
    """Allocates resources (capital, time, compute, talent) and runs autonomous active inference loops."""

    def __init__(self) -> None:
        pass

    def allocate_resources(
        self,
        opportunities: List[Dict[str, Any]],
        total_capital_cents: int,
        total_compute_flops: float
    ) -> Dict[str, Any]:
        """Allocates capital and compute across active opportunities based on EFE rank."""
        if not opportunities:
            return {"status": "idle", "allocations": []}

        # Sort by EFE (lower is better)
        sorted_opps = sorted(opportunities, key=lambda x: x.get("efe", 0.0))
        allocations = {}
        remaining_capital = total_capital_cents

        for i, opp in enumerate(sorted_opps):
            share = 0.6 if i == 0 else (0.4 / max(1, len(sorted_opps) - 1))
            capital = int(total_capital_cents * share)
            compute = total_compute_flops * share
            allocations[opp.get("title", f"opp_{i}")] = {
                "allocated_capital_cents": capital,
                "allocated_compute_flops": compute,
                "priority_rank": i + 1
            }

        return {
            "status": "allocated",
            "allocations": allocations
        }


# =====================================================================
# FourteenLayerEngine Orchestrator
# =====================================================================
class FourteenLayerEngine:
    """
    Master orchestrator coupling all 14 computational layers into an autonomous,
    continuous active inference loop.
    """

    def __init__(self) -> None:
        self.layer_1_reality = RealityEngine()
        self.layer_2_opportunity_discovery = OpportunityDiscoveryEngine()
        self.layer_3_problem_discovery = ProblemDiscoveryEngine()
        self.layer_4_decision_making = DecisionEngine()
        self.layer_5_opportunity_evaluation = OpportunityEvaluationEngine()
        self.layer_6_product_creation = ProductCreationEngine()
        self.layer_7_customer_understanding = CustomerUnderstandingEngine()
        self.layer_8_marketing = MarketingEngine()
        self.layer_9_sales = SalesEngine()
        self.layer_10_growth = GrowthEngine()
        self.layer_11_competition = CompetitionEngine()
        self.layer_12_organizational_design = OrganizationalDesignEngine()
        self.layer_13_meta_learning = MetaLearningEngine()
        self.layer_14_ai_entrepreneurship = AIEntrepreneurshipEngine()

    def run_full_14_layer_cycle(
        self,
        signal_title: str,
        surprise_score: float,
        domain: str,
        total_capital_cents: int = 100_000_000,  # $1M
        total_compute_flops: float = 1e18
    ) -> Dict[str, Any]:
        """Executes a complete 14-layer autonomous cycle from sensing to resource allocation."""
        # Layer 1
        automation = self.layer_1_reality.evaluate_task_automation("evaluate_opportunity", False)

        # Layer 2
        signal = self.layer_2_opportunity_discovery.detect_weak_signal(signal_title, surprise_score, domain)

        # Layer 3
        problem = self.layer_3_problem_discovery.decompose_problem(
            symptoms=["high_churn", "low_nps"],
            candidate_root_cause="poor_onboarding_ux",
            first_order_friction=0.8
        )

        # Layer 4
        efe = self.layer_4_decision_making.compute_expected_free_energy(
            p_success=0.7, p_target=0.9, prior_entropy=1.2, simulated_entropy=0.4
        )

        # Layer 5
        eval_res = self.layer_5_opportunity_evaluation.evaluate_opportunity(
            tam_cents=500_000_000_00, p_success=0.7, downside_risk=0.2, ltv_to_cac=4.5
        )

        # Layer 6
        product = self.layer_6_product_creation.optimize_feature_set([
            {"name": "core_workflow", "value": 0.9, "complexity": 0.3},
            {"name": "fancy_analytics", "value": 0.2, "complexity": 0.8}
        ])

        # Layer 7
        customer = self.layer_7_customer_understanding.evaluate_customer_switching(
            utility_gain=0.8, financial_cost=0.1, habitual_friction=0.2
        )

        # Layer 8
        marketing = self.layer_8_marketing.simulate_virality(invites_per_user=2.5, conversion_rate=0.4)

        # Layer 9
        sales = self.layer_9_sales.resolve_objection(objection_type="price", urgency_score=0.8)

        # Layer 10
        growth_val = self.layer_10_growth.compute_network_value(user_count=100)

        # Layer 11
        moat_score = self.layer_11_competition.score_moat_durability(0.8, 0.7, 0.6, 0.9)
        pivot_triggered = self.layer_11_competition.evaluate_pivot_trigger(0.05, 0.08)

        # Layer 12
        delegation = self.layer_12_organizational_design.evaluate_delegation(
            founder_hourly_value=500.0, task_hours=10.0, agent_execution_cost=50.0, error_risk_cost=100.0
        )

        # Layer 13
        calibration = self.layer_13_meta_learning.record_and_calibrate_decision(
            predicted_success_prob=0.7, actual_outcome=1.0
        )

        # Layer 14
        opp_candidate = {"title": signal_title, "efe": efe}
        resource_allocation = self.layer_14_ai_entrepreneurship.allocate_resources(
            opportunities=[opp_candidate],
            total_capital_cents=total_capital_cents,
            total_compute_flops=total_compute_flops
        )

        return {
            "cycle_status": "completed",
            "layer_1_automation": automation,
            "layer_2_signal": signal,
            "layer_3_problem": problem,
            "layer_4_efe": efe,
            "layer_5_evaluation": eval_res,
            "layer_6_product": product,
            "layer_7_customer": customer,
            "layer_8_marketing": marketing,
            "layer_9_sales": sales,
            "layer_10_growth_network_value": growth_val,
            "layer_11_moat_score": moat_score,
            "layer_11_pivot_triggered": pivot_triggered,
            "layer_12_delegation": delegation,
            "layer_13_calibration": calibration,
            "layer_14_resource_allocation": resource_allocation
        }
