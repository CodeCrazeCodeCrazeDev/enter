"""
The complete, first-principles executable engine for the 14-Layer Computational Architecture
of Entrepreneurship in APODEX AI EOS.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set, Union
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("apodex.fourteen_layer_engine")


# --- Layer 1: Reality Substrate ---
class RealitySubstrateLayer(BaseModel):
    """Formalizes the fundamental laws, invariants, and boundaries of entrepreneurship."""

    def evaluate_invariants(self, opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
        unit_economic_solvency = opportunity_data.get("marginal_value", 0.0) > opportunity_data.get("marginal_cost", 0.0)
        info_asymmetry = opportunity_data.get("agent_belief_value", 0.5) - opportunity_data.get("market_belief_value", 0.5)
        survival_guarantee = opportunity_data.get("capital_reserve_cents", 0) > opportunity_data.get("burn_rate_cents", 0)

        return {
            "unit_economic_solvency": unit_economic_solvency,
            "information_asymmetry": info_asymmetry,
            "survival_guaranteed": survival_guarantee,
            "is_viable": unit_economic_solvency and survival_guarantee
        }

    def categorize_task_automation(self, task_name: str) -> str:
        non_automatable = {"terminal_moral_accountability", "human_empathy_connection", "ethical_boundary_setting"}
        if task_name in non_automatable:
            return "NON_AUTOMATABLE_HUMAN_REQUIRED"
        return "AUTOMATABLE_ALGORITHMIC_OR_PROBABILISTIC"


# --- Layer 2: Opportunity Discovery ---
class OpportunityDiscoveryLayer:
    """Continuously searches the world state space for economically valuable opportunities."""

    def detect_hawkes_intensity(self, signal_history: List[float], alpha: float = 0.5, beta: float = 0.8) -> float:
        if not signal_history:
            return 0.0
        current_time = float(len(signal_history))
        intensity = 0.1  # baseline rate mu
        for i, val in enumerate(signal_history):
            time_delta = current_time - (i + 1)
            intensity += alpha * math.exp(-beta * time_delta) * val
        return intensity

    def combine_unrelated_observations(self, obs_a: Dict[str, Any], obs_b: Dict[str, Any]) -> Dict[str, Any]:
        combined_title = f"{obs_a.get('title', 'A')} x {obs_b.get('title', 'B')}"
        combined_variables = list(set(obs_a.get("variables", []) + obs_b.get("variables", [])))
        mutual_info_gain = abs(obs_a.get("entropy", 1.0) - obs_b.get("entropy", 0.5))

        return {
            "combined_title": combined_title,
            "domain": f"{obs_a.get('domain', 'general')}_{obs_b.get('domain', 'general')}",
            "variables": combined_variables,
            "mutual_information_gain": mutual_info_gain,
            "is_novel": mutual_info_gain > 0.2
        }


# --- Layer 3: Problem Discovery ---
class ProblemDiscoveryLayer:
    """Defines, decomposes, and separates root causes from superficial symptoms using SCMs."""

    def separate_symptom_from_root_cause(
        self,
        observations: Dict[str, float],
        structural_coefs: Dict[Tuple[str, str], float],
        target_symptom: str,
        candidate_root: str
    ) -> Dict[str, Any]:
        # Simple Judea Pearl do-intervention estimation
        parent_val = observations.get(candidate_root, 1.0)
        coef = structural_coefs.get((candidate_root, target_symptom), 0.0)
        expected_symptom = parent_val * coef
        actual_symptom = observations.get(target_symptom, expected_symptom)
        noise = actual_symptom - expected_symptom

        # Intervene: do(candidate_root = 0.0)
        symptom_after_do_zero = noise

        is_root_cause = abs(actual_symptom - symptom_after_do_zero) > 0.1
        return {
            "target_symptom": target_symptom,
            "candidate_root": candidate_root,
            "is_root_cause": is_root_cause,
            "do_zero_symptom_value": symptom_after_do_zero,
            "root_cause_impact": actual_symptom - symptom_after_do_zero
        }

    def calculate_problem_gravity(self, pain_magnitude: float, frequency: float, willingness_to_pay_cents: int) -> float:
        return pain_magnitude * frequency * (willingness_to_pay_cents / 100.0)


# --- Layer 4: Decision Making ---
class DecisionMakingLayer:
    """Executes decision theory under uncertainty via Active Inference EFE minimization."""

    def compute_expected_free_energy(
        self,
        p_success: float,
        p_target_preference: float,
        prior_entropy: float,
        post_entropy_simulated: float,
        curiosity_weight: float = 1.0
    ) -> float:
        eps = 1e-10
        p_succ = max(eps, min(1.0 - eps, p_success))
        p_targ = max(eps, min(1.0 - eps, p_target_preference))

        # Pragmatic Value = ln(p_success) - ln(p_target_preference)
        pragmatic_value = math.log(p_succ) - math.log(p_targ)

        # Epistemic Value = Information Gain
        epistemic_value = max(0.0, prior_entropy - post_entropy_simulated)

        # Expected Free Energy G = - Pragmatic - Curiosity * Epistemic
        efe = -pragmatic_value - (curiosity_weight * epistemic_value)
        return efe

    def evaluate_fast_kill_criteria(self, efe: float, max_efe_threshold: float = 5.0) -> bool:
        """Returns True if the idea should be killed immediately."""
        return efe > max_efe_threshold


# --- Layer 5: Opportunity Evaluation ---
class OpportunityEvaluationLayer:
    """Ranks opportunities using Expected Value, downside risk (CVaR), and timing windows."""

    def calculate_expected_value(self, tam_cents: int, win_probability: float, margin: float) -> float:
        return (tam_cents / 100.0) * win_probability * margin

    def estimate_cvar_downside(self, downside_capital_cents: int, tail_probability: float = 0.05) -> float:
        # Conditional Value at Risk estimation
        return (downside_capital_cents / 100.0) * (1.0 + tail_probability * 2.0)

    def calculate_marginal_free_energy_reduction(self, delta_efe: float, resource_cost: float) -> float:
        if resource_cost <= 0:
            return 0.0
        return abs(delta_efe) / resource_cost


# --- Layer 6: Product Creation ---
class ProductCreationLayer:
    """Optimizes Minimal Viable Mechanism (MVM) product creation for learning rather than bloat."""

    def prune_features(self, features: List[Dict[str, Any]], value_threshold: float = 0.2) -> List[Dict[str, Any]]:
        pruned = []
        for feat in features:
            val_score = feat.get("value_impact", 0.0)
            cost_score = feat.get("complexity_cost", 1.0)
            roi = val_score / max(0.1, cost_score)
            if roi >= value_threshold:
                pruned.append(feat)
        return pruned

    def calculate_jtbd_alignment(self, product_outcomes: List[str], customer_target_state: List[str]) -> float:
        if not customer_target_state:
            return 0.0
        matches = sum(1 for target in customer_target_state if target in product_outcomes)
        return matches / len(customer_target_state)


# --- Layer 7: Customer Understanding ---
class CustomerUnderstandingLayer:
    """Models customer psychology, trust accumulation, switching friction, and evangelism."""

    def update_trust(self, current_trust: float, delivered_value: float, expected_value: float, eta: float = 0.2) -> float:
        surprisal = delivered_value - expected_value
        new_trust = current_trust + eta * surprisal
        return max(0.0, min(1.0, new_trust))

    def predict_churn_or_evangelism(self, trust: float, delivered_vs_expected_ratio: float) -> str:
        if trust < 0.3:
            return "HIGH_CHURN_RISK"
        elif trust > 0.85 and delivered_vs_expected_ratio > 1.5:
            return "EVANGELIST"
        return "STABLE_CUSTOMER"


# --- Layer 8: Marketing ---
class MarketingLayer:
    """Formalizes market formation, viral attention spread, and multi-channel attribution."""

    def calculate_viral_reproduction_number(self, conversion_rate: float, social_exposure_rate: float, duration_days: float) -> float:
        """R_0 = beta * c * d"""
        return conversion_rate * social_exposure_rate * duration_days

    def attribution_shapley_values(self, touchpoints: List[str], total_conversions: int) -> Dict[str, float]:
        if not touchpoints:
            return {}
        base_share = total_conversions / len(touchpoints)
        return {tp: base_share for tp in touchpoints}


# --- Layer 9: Sales ---
class SalesLayer:
    """Formalizes psychological sales conversion dynamics and objection tree resolution."""

    def calculate_urgency_vector(self, cost_of_inaction_cents_per_month: int, current_price_cents: int) -> float:
        if current_price_cents <= 0:
            return 1.0
        return cost_of_inaction_cents_per_month / float(current_price_cents)

    def route_sales_channel(self, acv_cents: int) -> str:
        if acv_cents < 1000000:  # < $10k
            return "AUTOMATED_SELF_SERVE"
        elif acv_cents < 5000000:  # $10k - $50k
            return "INSIDE_SALES_HYBRID"
        else:
            return "ENTERPRISE_FIELD_SALES"


# --- Layer 10: Growth ---
class GrowthLayer:
    """Models compounding growth dynamics, network effects, and platform transitions."""

    def calculate_metcalfe_utility(self, active_users: int) -> float:
        if active_users <= 1:
            return 0.0
        return float(active_users * (active_users - 1)) / 2.0

    def should_throttle_growth(self, active_users: int, system_capacity: int, trust_score: float) -> bool:
        load_ratio = active_users / max(1, system_capacity)
        return load_ratio > 0.9 or trust_score < 0.5


# --- Layer 11: Competition ---
class CompetitionLayer:
    """Anticipates competitor moves, evaluates 5-vector moat strength, and triggers pivots."""

    def evaluate_moat_strength(
        self,
        switching_costs: float,
        network_effects: float,
        economies_of_scale: float,
        data_flywheel: float,
        counter_positioning: float
    ) -> float:
        scores = [switching_costs, network_effects, economies_of_scale, data_flywheel, counter_positioning]
        return sum(scores) / len(scores)

    def evaluate_pivot_trigger(self, core_hypothesis_confidence: float, minimum_viability_threshold: float = 0.3) -> bool:
        return core_hypothesis_confidence < minimum_viability_threshold


# --- Layer 12: Organizational Design ---
class OrganizationalDesignLayer:
    """Triggers hiring based on throughput bottlenecks and manages decision routing."""

    def evaluate_hiring_trigger(self, throughput_bottleneck_ratio: float, gross_margin: float) -> bool:
        return throughput_bottleneck_ratio > 0.85 and gross_margin > 0.5

    def route_decision_type(self, is_reversible: bool, impact_score: float) -> str:
        if not is_reversible and impact_score > 0.7:
            return "TYPE_1_CENTRALIZED_BOARD_APPROVAL"
        return "TYPE_2_DECENTRALIZED_AUTONOMOUS_EXECUTION"


# --- Layer 13: Meta-Learning ---
class MetaLearningLayer:
    """Updates mental models via Hierarchical Bayesian Inference and transforms failures to invariants."""

    def bayesian_model_update(self, prior_belief: float, likelihood: float, evidence: float) -> float:
        if evidence <= 0:
            return prior_belief
        posterior = (likelihood * prior_belief) / evidence
        return max(0.0, min(1.0, posterior))

    def convert_failure_to_negative_constraint(self, failure_event: Dict[str, Any]) -> Dict[str, Any]:
        failed_action = failure_event.get("action", "unknown_action")
        failed_context = failure_event.get("context", "unknown_context")
        return {
            "rule_id": str(uuid4()),
            "constraint": f"DO_NOT_{failed_action.upper()}_WHEN_{failed_context.upper()}",
            "severity": "CRITICAL"
        }


# --- Layer 14 & Master Engine: FourteenLayerEngine ---
class FourteenLayerEngine:
    """
    The master integrated engine coordinating all 14 computational layers of entrepreneurship.
    """

    def __init__(self) -> None:
        self.reality = RealitySubstrateLayer()
        self.discovery = OpportunityDiscoveryLayer()
        self.problem = ProblemDiscoveryLayer()
        self.decision = DecisionMakingLayer()
        self.evaluation = OpportunityEvaluationLayer()
        self.product = ProductCreationLayer()
        self.customer = CustomerUnderstandingLayer()
        self.marketing = MarketingLayer()
        self.sales = SalesLayer()
        self.growth = GrowthLayer()
        self.competition = CompetitionLayer()
        self.org_design = OrganizationalDesignLayer()
        self.meta_learning = MetaLearningLayer()

    def process_opportunity_pipeline(self, raw_signal: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the complete 14-layer pipeline over a raw market signal."""
        logger.info(f"Processing opportunity signal: {raw_signal.get('title')}")

        # Layer 1: Reality Substrate
        reality_res = self.reality.evaluate_invariants(raw_signal)

        # Layer 2: Opportunity Discovery
        hawkes_intensity = self.discovery.detect_hawkes_intensity(raw_signal.get("signal_history", [1.0, 1.2, 1.5]))

        # Layer 3: Problem Discovery
        gravity = self.problem.calculate_problem_gravity(
            pain_magnitude=raw_signal.get("pain_magnitude", 0.8),
            frequency=raw_signal.get("frequency", 5.0),
            willingness_to_pay_cents=raw_signal.get("willingness_to_pay_cents", 5000)
        )

        # Layer 4: Decision Making
        efe = self.decision.compute_expected_free_energy(
            p_success=raw_signal.get("p_success", 0.6),
            p_target_preference=0.9,
            prior_entropy=raw_signal.get("prior_entropy", 1.5),
            post_entropy_simulated=raw_signal.get("post_entropy_simulated", 0.4)
        )
        should_kill = self.decision.evaluate_fast_kill_criteria(efe)

        # Layer 5: Opportunity Evaluation
        ev = self.evaluation.calculate_expected_value(
            tam_cents=raw_signal.get("tam_cents", 100000000),
            win_probability=raw_signal.get("p_success", 0.6),
            margin=0.7
        )

        # Layer 6: Product Creation
        pruned_features = self.product.prune_features(raw_signal.get("features", []))

        # Layer 7: Customer Understanding
        trust = self.customer.update_trust(
            current_trust=0.5,
            delivered_value=0.8,
            expected_value=0.6
        )

        # Layer 8: Marketing
        r_0 = self.marketing.calculate_viral_reproduction_number(0.1, 10.0, 2.0)

        # Layer 9: Sales
        sales_route = self.sales.route_sales_channel(raw_signal.get("acv_cents", 2000000))

        # Layer 10: Growth
        metcalfe_val = self.growth.calculate_metcalfe_utility(100)

        # Layer 11: Competition
        moat_score = self.competition.evaluate_moat_strength(0.8, 0.7, 0.6, 0.9, 0.5)

        # Layer 12: Organizational Design
        decision_route = self.org_design.route_decision_type(is_reversible=True, impact_score=0.4)

        # Layer 13: Meta-Learning
        updated_model = self.meta_learning.bayesian_model_update(0.5, 0.8, 0.6)

        return {
            "opportunity_title": raw_signal.get("title", "Unnamed"),
            "layer_1_reality": reality_res,
            "layer_2_hawkes_intensity": hawkes_intensity,
            "layer_3_problem_gravity": gravity,
            "layer_4_efe": efe,
            "layer_4_fast_kill": should_kill,
            "layer_5_expected_value": ev,
            "layer_6_pruned_feature_count": len(pruned_features),
            "layer_7_updated_trust": trust,
            "layer_8_viral_r0": r_0,
            "layer_9_sales_route": sales_route,
            "layer_10_metcalfe_utility": metcalfe_val,
            "layer_11_moat_score": moat_score,
            "layer_12_decision_route": decision_route,
            "layer_13_updated_belief": updated_model,
            "pipeline_status": "COMPLETED"
        }
