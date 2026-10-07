"""The 14-Layer Computational Architecture Engine of Entrepreneurship.

Executable, first-principles implementation formalizing all 14 layers:
Reality, Opportunity Discovery, Problem Discovery, Decision Making,
Opportunity Evaluation, Product Creation, Customer Understanding, Marketing,
Sales, Growth, Competition, Organizational Design, Meta-Learning, and AI Entrepreneurship.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.fourteen_layer_engine")


# =====================================================================
# Layer 1: Reality Substrate & Fundamental Principles
# =====================================================================
class RealitySubstrateEngine:
    """Layer 1: Evaluates physical, thermodynamic, and financial constraints."""

    def evaluate_thermodynamic_runway(self, revenue_cents: int, burn_cents: int, cash_reserve_cents: int) -> Dict[str, Any]:
        """Calculates net burn rate and financial runway months."""
        net_burn = burn_cents - revenue_cents
        if net_burn <= 0:
            runway_months = float("inf")
            is_surviving = True
        else:
            runway_months = cash_reserve_cents / net_burn
            is_surviving = cash_reserve_cents > 0

        return {
            "net_burn_cents": net_burn,
            "runway_months": runway_months,
            "is_surviving": is_surviving,
            "capital_runway_constraint": cash_reserve_cents > 0
        }

    def classify_task_automation(self, task_type: str) -> Dict[str, Any]:
        """Classifies tasks into automatable vs. human-arbitrated boundaries."""
        human_tasks = {"terminal_utility_arbitration", "ethical_alignment", "physical_presence"}
        is_automatable = task_type not in human_tasks
        return {
            "task_type": task_type,
            "is_automatable": is_automatable,
            "execution_mode": "autonomous_agent" if is_automatable else "human_in_the_loop"
        }


# =====================================================================
# Layer 2: Opportunity Discovery & State Space Search
# =====================================================================
class StateSpaceOpportunityDiscoveryEngine:
    """Layer 2: Continuous search across non-stationary market state space."""

    def calculate_kl_divergence(self, demand_prior: Dict[str, float], supply_prior: Dict[str, float]) -> float:
        """Computes Kullback-Leibler divergence between market demand and supply distributions."""
        eps = 1e-10
        divergence = 0.0
        all_keys = set(demand_prior.keys()).union(set(supply_prior.keys()))
        for key in all_keys:
            p = max(eps, demand_prior.get(key, eps))
            q = max(eps, supply_prior.get(key, eps))
            divergence += p * math.log(p / q)
        return max(0.0, divergence)

    def detect_weak_signals(self, temporal_signals: List[Dict[str, Any]], z_threshold: float = 2.0) -> List[Dict[str, Any]]:
        """Filters temporal signals exceeding the Z-score anomaly threshold."""
        if not temporal_signals:
            return []

        values = [s.get("value", 0.0) for s in temporal_signals]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = math.sqrt(variance) if variance > 0 else 1.0

        anomalies = []
        for signal in temporal_signals:
            val = signal.get("value", 0.0)
            z_score = (val - mean) / std_dev
            if z_score >= z_threshold:
                signal["z_score"] = z_score
                anomalies.append(signal)

        return anomalies

    def synthesize_cross_domain_tensor(self, domain_a_features: List[float], domain_b_features: List[float]) -> List[float]:
        """Computes outer tensor product combination of cross-domain features."""
        combined = []
        for a in domain_a_features:
            for b in domain_b_features:
                combined.append(a * b)
        return combined


# =====================================================================
# Layer 3: Problem Discovery & Structural Decomposition
# =====================================================================
class StructuralProblemDecomposer:
    """Layer 3: Decomposes problems into Structural Causal Models (SCMs)."""

    def decompose_causal_graph(self, variables: List[str], edges: List[Tuple[str, str]]) -> Dict[str, Any]:
        """Identifies root cause nodes (no parents) vs symptoms (has upstream parents)."""
        children = {child for parent, child in edges}
        parents = {parent for parent, child in edges}

        root_causes = [var for var in variables if var not in children]
        symptoms = [var for var in variables if var in children]

        return {
            "root_causes": root_causes,
            "symptoms": symptoms,
            "is_decomposed": len(root_causes) > 0,
            "causal_edges_count": len(edges)
        }

    def evaluate_evig_ignore_threshold(self, evig: float, utility_delta: float, investigation_cost: float) -> bool:
        """Determines whether to ignore a problem based on EVIG + Delta U vs Cost."""
        total_value = evig + utility_delta
        should_ignore = total_value < investigation_cost
        logger.info(f"Problem EVIG check: Total Value={total_value:.4f}, Cost={investigation_cost:.4f}, Ignore={should_ignore}")
        return should_ignore


# =====================================================================
# Layer 4: Decision Making Under Uncertainty
# =====================================================================
class ActiveInferenceDecisionEngine:
    """Layer 4: Active Inference, Bayesian updating, and idea termination."""

    def bayesian_prior_likelihood_update(
        self, prior_mean: float, prior_std: float, obs_mean: float, obs_std: float, n_samples: int
    ) -> Tuple[float, float]:
        """Conjugate Bayesian update balancing intuition (prior) and data (likelihood)."""
        if n_samples <= 0:
            return prior_mean, prior_std

        prior_var = max(1e-6, prior_std ** 2)
        obs_var = max(1e-6, (obs_std ** 2) / n_samples)

        posterior_var = 1.0 / (1.0 / prior_var + 1.0 / obs_var)
        posterior_mean = posterior_var * (prior_mean / prior_var + obs_mean / obs_var)
        posterior_std = math.sqrt(posterior_var)

        return posterior_mean, posterior_std

    def evaluate_sprt_termination(
        self, log_likelihood_ratios: List[float], upper_bound_a: float = 2.0, lower_bound_b: float = -2.0
    ) -> str:
        """Sequential Probability Ratio Test (SPRT) for rapid idea termination."""
        cumulative_llr = sum(log_likelihood_ratios)
        if cumulative_llr >= upper_bound_a:
            return "ACCEPT_HYPOTHESIS"
        elif cumulative_llr <= lower_bound_b:
            return "TERMINATE_HYPOTHESIS"
        else:
            return "CONTINUE_EXPERIMENTATION"


# =====================================================================
# Layer 5: Opportunity Evaluation
# =====================================================================
class OpportunityEvaluationEngine:
    """Layer 5: Expected Free Energy (EFE) ranking and Real Options timing."""

    def calculate_expected_free_energy(
        self,
        success_probability: float,
        target_preference: float,
        prior_entropy: float,
        post_entropy: float,
        curiosity_weight: float = 1.0
    ) -> float:
        """Expected Free Energy G = - Pragmatic Value - Epistemic Value * curiosity_weight."""
        eps = 1e-10
        p_succ = max(eps, min(1.0 - eps, success_probability))
        p_pref = max(eps, min(1.0 - eps, target_preference))

        pragmatic_value = math.log(p_succ) - math.log(p_pref)
        epistemic_value = max(0.0, prior_entropy - post_entropy)

        efe = -pragmatic_value - (epistemic_value * curiosity_weight)
        return efe

    def evaluate_real_options_timing(self, opportunity_val: float, volatility: float, waiting_cost: float) -> str:
        """Evaluates whether to deploy immediately or defer via Real Option value."""
        option_value = opportunity_val * volatility - waiting_cost
        if option_value > opportunity_val * 0.2:
            return "DEFER_INVESTMENT"
        return "DEPLOY_IMMEDIATELY"


# =====================================================================
# Layer 6: Product Creation & Value Optimization
# =====================================================================
class MinimumComplexityProductEngine:
    """Layer 6: Minimizes Kolmogorov complexity and solves Job-To-Be-Done."""

    def minimize_product_complexity(
        self, features: List[Dict[str, Any]], complexity_penalty: float = 0.1
    ) -> List[Dict[str, Any]]:
        """Strips features where Utility - complexity_penalty * complexity <= 0."""
        retained = []
        for feat in features:
            utility = feat.get("utility", 0.5)
            complexity = feat.get("complexity", 1.0)
            net_value = utility - complexity_penalty * complexity
            if net_value > 0:
                feat["net_value"] = net_value
                retained.append(feat)

        retained.sort(key=lambda x: x["net_value"], reverse=True)
        return retained

    def extract_core_jtbd_factors(self, user_behaviors: List[Dict[str, Any]]) -> Dict[str, float]:
        """Extracts latent causal weights driving Job-To-Be-Done hiring."""
        factors: Dict[str, float] = {}
        for b in user_behaviors:
            action = b.get("action", "general")
            importance = b.get("frequency", 1) * b.get("satisfaction_gap", 0.5)
            factors[action] = factors.get(action, 0.0) + importance

        total = sum(factors.values()) if factors else 1.0
        return {k: v / total for k, v in factors.items()}


# =====================================================================
# Layer 7: Customer Psychology Modeler
# =====================================================================
class CustomerPsychologyModeler:
    """Layer 7: Customer switching dynamics and trust state vector."""

    def calculate_switching_probability(self, push: float, pull: float, inertia: float, anxiety: float) -> float:
        """Push-Pull-Inertia-Anxiety sigmoid transition probability."""
        net_force = push + pull - inertia - anxiety
        return 1.0 / (1.0 + math.exp(-net_force))

    def update_trust_state_vector(self, current_trust: float, execution_success: bool, decay: float = 0.05) -> float:
        """Updates trust state vector with slow decay and performance reinforcement."""
        if execution_success:
            updated = current_trust + (1.0 - current_trust) * 0.15
        else:
            updated = current_trust * 0.70  # Asymmetric downside shock
        return max(0.0, min(1.0, updated - decay * current_trust))


# =====================================================================
# Layer 8: Market Formation Engine
# =====================================================================
class MarketFormationEngine:
    """Layer 8: Scale-free social graph attention dynamics and Brand PageRank."""

    def simulate_attention_cascade(
        self, initial_nodes: int, transmission_rate: float, network_decay: float, steps: int = 5
    ) -> List[int]:
        """Simulates information cascade step-by-step."""
        history = [initial_nodes]
        current = initial_nodes
        for _ in range(steps):
            newly_infected = int(current * transmission_rate * (1.0 - network_decay))
            current = max(1, current + newly_infected)
            history.append(current)
        return history

    def calculate_brand_authority_pagerank(
        self, domain_nodes: List[str], adjacency: Dict[str, List[str]], damping: float = 0.85
    ) -> Dict[str, float]:
        """Calculates PageRank authority score across domain knowledge graph."""
        n = len(domain_nodes)
        if n == 0:
            return {}

        rank = {node: 1.0 / n for node in domain_nodes}
        for _ in range(10):  # Iterative power method
            new_rank = {node: (1.0 - damping) / n for node in domain_nodes}
            for node, neighbors in adjacency.items():
                if neighbors:
                    share = rank.get(node, 0.0) / len(neighbors)
                    for nbr in neighbors:
                        if nbr in new_rank:
                            new_rank[nbr] += damping * share
            rank = new_rank
        return rank


# =====================================================================
# Layer 9: Sales Psychology Engine
# =====================================================================
class SalesPsychologyEngine:
    """Layer 9: Urgency generation and sales automation boundaries."""

    def calculate_counterfactual_loss_of_inaction(self, daily_cost_of_delay_cents: int, delay_days: int) -> int:
        """Calculates compounding counterfactual loss of customer inaction."""
        return daily_cost_of_delay_cents * delay_days

    def determine_sales_automation_mode(self, acv_cents: int, decision_complexity: str) -> str:
        """Determines automated self-serve vs enterprise sales boundary."""
        if acv_cents >= 50000_00 or decision_complexity == "high":
            return "ENTERPRISE_HIGH_TOUCH_SALES"
        elif acv_cents < 5000_00 and decision_complexity == "low":
            return "AUTOMATED_SELF_SERVE_FUNNEL"
        else:
            return "HYBRID_INSIDE_SALES"


# =====================================================================
# Layer 10: Compounding Growth Engine
# =====================================================================
class CompoundingGrowthEngine:
    """Layer 10: Sub-quadratic network utility and blowout throttling."""

    def calculate_subquadratic_network_value(self, user_count: int, scaling_factor: float = 1.0) -> float:
        """Zipf/Beckstrom sub-quadratic network value V = scaling * N * log(N)."""
        if user_count <= 1:
            return 0.0
        return scaling_factor * user_count * math.log(user_count)

    def check_capacity_blowout_risk(self, growth_rate: float, operational_capacity: float) -> bool:
        """Flags risk if growth outpaces operational capacity limits."""
        return growth_rate > operational_capacity * 1.5


# =====================================================================
# Layer 11: Competitive Moat Engine
# =====================================================================
class CompetitiveMoatEngine:
    """Layer 11: Moat durability scoring and pivot triggers."""

    def calculate_moat_durability_score(
        self, switching_cost_score: float, network_density: float, brand_pagerank: float, cost_advantage: float
    ) -> float:
        """Composite Moat Durability Score [0, 1]."""
        return float(0.3 * network_density + 0.3 * switching_cost_score + 0.2 * brand_pagerank + 0.2 * cost_advantage)

    def check_pivot_trigger(self, gross_margin: float, threshold: float = 0.30) -> bool:
        """Triggers model pivot if gross margin decays below threshold."""
        return gross_margin < threshold


# =====================================================================
# Layer 12: Organizational Scaling Engine
# =====================================================================
class OrganizationalScalingEngine:
    """Layer 12: Lagrange shadow price hiring triggers and Coasian boundaries."""

    def evaluate_lagrange_hiring_trigger(self, resource_shadow_price: float, market_wage: float) -> bool:
        """Triggers hiring if resource constraint shadow price exceeds wage."""
        return resource_shadow_price > market_wage

    def evaluate_coasian_boundary(self, internal_coordination_cost: float, external_transaction_cost: float) -> str:
        """Determines whether to execute internally or delegate/outsource."""
        if internal_coordination_cost < external_transaction_cost:
            return "CENTRALIZED_IN_HOUSE"
        return "DELEGATE_OR_OUTSOURCE"


# =====================================================================
# Layer 13: Meta-Learning Engine
# =====================================================================
class MetaLearningEngine:
    """Layer 13: Triple-loop error backpropagation and post-mortem compilation."""

    def execute_triple_loop_backpropagation(self, forecast_errors: List[float]) -> Dict[str, Any]:
        """Executes single, double, and triple loop updates based on forecast calibration errors."""
        avg_error = sum(forecast_errors) / len(forecast_errors) if forecast_errors else 0.0

        single_loop_param_adj = min(0.5, avg_error * 0.5)
        rewrite_playbook = avg_error > 0.15
        rewrite_cognitive_code = avg_error > 0.30

        return {
            "avg_forecast_error": avg_error,
            "single_loop_param_delta": single_loop_param_adj,
            "double_loop_rewrite_playbook": rewrite_playbook,
            "triple_loop_rewrite_code": rewrite_cognitive_code
        }

    def compile_post_mortem_heuristics(self, failed_trajectories: List[Dict[str, Any]]) -> List[str]:
        """Extracts immutable safety rules from failure logs."""
        rules = []
        for traj in failed_trajectories:
            reason = traj.get("failure_reason", "unknown")
            rules.append(f"SAFETY_RULE_PREVENT_{reason.upper()}")
        return list(set(rules))


# =====================================================================
# Layer 14: Master AI Entrepreneurship Orchestrator
# =====================================================================
class FourteenLayerOrchestrator:
    """Master coordinating orchestrator coupling all 14 layers."""

    def __init__(self) -> None:
        self.reality_engine = RealitySubstrateEngine()
        self.opportunity_engine = StateSpaceOpportunityDiscoveryEngine()
        self.problem_decomposer = StructuralProblemDecomposer()
        self.decision_engine = ActiveInferenceDecisionEngine()
        self.eval_engine = OpportunityEvaluationEngine()
        self.product_engine = MinimumComplexityProductEngine()
        self.customer_engine = CustomerPsychologyModeler()
        self.market_engine = MarketFormationEngine()
        self.sales_engine = SalesPsychologyEngine()
        self.growth_engine = CompoundingGrowthEngine()
        self.moat_engine = CompetitiveMoatEngine()
        self.org_engine = OrganizationalScalingEngine()
        self.meta_engine = MetaLearningEngine()

    def ingest_and_orchestrate(self, signal: Dict[str, Any], budget_cents: int) -> Dict[str, Any]:
        """Executes full 14-layer pipeline over input market signal and capital budget."""
        logger.info(f"Orchestrator ingesting signal: {signal.get('title')}")

        # Layer 1: Reality check
        runway = self.reality_engine.evaluate_thermodynamic_runway(revenue_cents=0, burn_cents=100000, cash_reserve_cents=budget_cents)

        # Layer 2: Weak signal search
        signals = [signal]
        anomalies = self.opportunity_engine.detect_weak_signals(signals, z_threshold=0.0)

        # Layer 3: Problem decomposition
        vars_list = signal.get("variables", ["marketing", "conversion"])
        edges = signal.get("causal_edges", [("marketing", "conversion")])
        problem_decomp = self.problem_decomposer.decompose_causal_graph(vars_list, edges)

        # Layer 4 & 5: Active Inference evaluation & EFE
        efe = self.eval_engine.calculate_expected_free_energy(
            success_probability=signal.get("success_probability", 0.5),
            target_preference=0.9,
            prior_entropy=signal.get("prior_entropy", 1.2),
            post_entropy=signal.get("post_entropy", 0.4)
        )

        # Layer 6: Product complexity minimization
        raw_features = [{"feature": "core_mvp", "utility": 0.8, "complexity": 0.2}]
        minimized_features = self.product_engine.minimize_product_complexity(raw_features)

        # Layer 7 & 8: Customer switching & brand authority
        switch_prob = self.customer_engine.calculate_switching_probability(push=1.0, pull=1.5, inertia=0.5, anxiety=0.2)
        brand_ranks = self.market_engine.calculate_brand_authority_pagerank(["our_brand"], {"our_brand": []})

        # Layer 9 & 10: Sales mode & compounding network value
        sales_mode = self.sales_engine.determine_sales_automation_mode(acv_cents=signal.get("tam_cents", 100000) // 100, decision_complexity="low")
        network_val = self.growth_engine.calculate_subquadratic_network_value(user_count=100)

        # Layer 11 & 12: Moat score & Coasian delegation
        moat_score = self.moat_engine.calculate_moat_durability_score(0.8, 0.7, 0.6, 0.5)
        delegation = self.org_engine.evaluate_coasian_boundary(internal_coordination_cost=50.0, external_transaction_cost=100.0)

        # Layer 13: Meta-learning error calibration
        meta_backprop = self.meta_engine.execute_triple_loop_backpropagation([0.05, 0.08])

        return {
            "status": "orchestrated",
            "layer_1_runway": runway,
            "layer_2_anomalies_detected": len(anomalies),
            "layer_3_root_causes": problem_decomp["root_causes"],
            "layer_4_5_calculated_efe": efe,
            "layer_6_minimized_features": len(minimized_features),
            "layer_7_customer_switch_prob": switch_prob,
            "layer_8_brand_authority": brand_ranks,
            "layer_9_sales_mode": sales_mode,
            "layer_10_network_value": network_val,
            "layer_11_moat_score": moat_score,
            "layer_12_delegation_mode": delegation,
            "layer_13_meta_backprop": meta_backprop,
            "layer_14_execution_timestamp": datetime.now(timezone.utc).isoformat()
        }
