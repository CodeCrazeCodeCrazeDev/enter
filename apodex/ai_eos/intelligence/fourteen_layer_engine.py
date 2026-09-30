"""
Executable Python engine implementation for the 14-Layer Computational Architecture
of Entrepreneurship (SERO v2.1).
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.fourteen_layer_engine")


class Layer1RealityEngine:
    """Layer 1: Reality Substrate - Thermodynamic and Conservation Bounds."""

    def evaluate_bounds(self, capital_in: float, capital_out: float, burn_rate_days: float) -> Dict[str, Any]:
        net_capital = capital_in - capital_out
        is_sustainable = net_capital >= 0.0
        runway_days = (capital_in / capital_out * burn_rate_days) if capital_out > 0 else float("inf")
        return {
            "net_capital": net_capital,
            "is_sustainable": is_sustainable,
            "runway_days": runway_days,
            "unautomatable_human_meaning_reserved": True,
        }


class Layer2OpportunityDiscoveryEngine:
    """Layer 2: Opportunity Discovery - State-Space Search & KL-Divergence."""

    def search_kl_divergence(self, demand_dist: List[float], supply_dist: List[float]) -> float:
        eps = 1e-10
        kl_div = 0.0
        for p, q in zip(demand_dist, supply_dist):
            p_clamped = max(eps, p)
            q_clamped = max(eps, q)
            kl_div += p_clamped * math.log(p_clamped / q_clamped)
        return kl_div

    def detect_weak_signals(self, event_stream: List[Dict[str, Any]], threshold: float = 1.5) -> List[Dict[str, Any]]:
        anomalies = []
        for event in event_stream:
            variance = event.get("variance", 0.0)
            frequency = event.get("frequency", 1.0)
            if variance / (frequency + 1e-5) > threshold:
                anomalies.append(event)
        return anomalies

    def combine_unrelated_domains(self, domain_a_vars: List[str], domain_b_vars: List[str]) -> List[str]:
        combined = []
        for v1 in domain_a_vars:
            for v2 in domain_b_vars:
                combined.append(f"{v1}_x_{v2}")
        return combined


class Layer3ProblemDiscoveryEngine:
    """Layer 3: Problem Discovery - SCM Decomposition & EVIG."""

    def decompose_causal_problem(self, causal_edges: List[Tuple[str, str]], target_node: str) -> Dict[str, Any]:
        parents = [p for p, c in causal_edges if c == target_node]
        root_causes = [p for p in parents if not any(c == p for _, c in causal_edges)]
        symptoms = [c for p, c in causal_edges if p == target_node]
        return {
            "target": target_node,
            "direct_parents": parents,
            "probable_root_causes": root_causes if root_causes else parents,
            "downstream_symptoms": symptoms,
        }

    def calculate_evig(self, prior_entropy: float, post_entropy: float, cost: float) -> Tuple[float, bool]:
        info_gain = max(0.0, prior_entropy - post_entropy)
        net_evig = info_gain - cost
        should_ignore = net_evig <= 0.0
        return net_evig, should_ignore


class Layer4DecisionMakingEngine:
    """Layer 4: Decision Making - Dual Bayesian Conjugate Updates & SPRT."""

    def bayesian_update(self, prior_mean: float, prior_prec: float, data_mean: float, data_prec: float) -> Tuple[float, float]:
        post_prec = prior_prec + data_prec
        post_mean = (prior_mean * prior_prec + data_mean * data_prec) / post_prec
        return post_mean, post_prec

    def sprt_idea_kill_check(self, log_likelihood_ratio: float, alpha: float = 0.05, beta: float = 0.20) -> str:
        lower_bound = math.log(beta / (1.0 - alpha))
        upper_bound = math.log((1.0 - beta) / alpha)
        if log_likelihood_ratio <= lower_bound:
            return "KILL"
        elif log_likelihood_ratio >= upper_bound:
            return "ACCEPT"
        return "CONTINUE_TESTING"


class Layer5OpportunityEvaluationEngine:
    """Layer 5: Opportunity Evaluation - Merton Jump-Diffusion & Real Options."""

    def calculate_jump_diffusion_ev(
        self, initial_val: float, drift: float, volatility: float, jump_prob: float, jump_size: float, time_horizon: float
    ) -> float:
        expected_drift = (drift - 0.5 * volatility**2) * time_horizon
        expected_jump = jump_prob * time_horizon * jump_size
        return initial_val * math.exp(expected_drift + expected_jump)


class Layer6ProductCreationEngine:
    """Layer 6: Product Creation - JTBD & Feature Pruning."""

    def prune_features_jtbd(self, features: List[Dict[str, Any]], min_utility_per_cost: float = 1.0) -> List[Dict[str, Any]]:
        pruned = []
        for feat in features:
            utility = feat.get("utility", 0.0)
            cost = feat.get("cost", 1.0)
            if (utility / max(0.01, cost)) >= min_utility_per_cost:
                pruned.append(feat)
        return pruned


class Layer7CustomerUnderstandingEngine:
    """Layer 7: Customer Understanding - Prospect Theory & Switching Friction."""

    def prospect_theory_utility(self, amount: float, alpha: float = 0.88, lambda_loss: float = 2.25) -> float:
        if amount >= 0:
            return amount**alpha
        else:
            return -lambda_loss * ((-amount)**alpha)

    def evaluate_switching_decision(self, utility_new: float, utility_old: float, switching_cost: float) -> bool:
        net_gain = utility_new - utility_old - switching_cost
        return net_gain > 0.0


class Layer8MarketingEngine:
    """Layer 8: Marketing - Viral Cascades & PageRank Brand Authority."""

    def calculate_viral_spread(self, conversion_rate: float, exposures_per_user: float) -> Tuple[float, bool]:
        k_factor = conversion_rate * exposures_per_user
        is_viral = k_factor > 1.0
        return k_factor, is_viral


class Layer9SalesEngine:
    """Layer 9: Sales - Risk Reduction & Enterprise Router."""

    def route_sales_model(self, acv_dollars: float) -> str:
        if acv_dollars < 5000:
            return "SELF_SERVICE_AUTOMATED"
        elif acv_dollars < 50000:
            return "INSIDE_SALES_HYBRID"
        else:
            return "HIGH_TOUCH_ENTERPRISE"


class Layer10GrowthEngine:
    """Layer 10: Growth - Sub-Quadratic Network Effects & Slowdown Checks."""

    def calculate_network_value(self, num_nodes: int) -> float:
        if num_nodes <= 1:
            return 0.0
        return num_nodes * math.log(num_nodes)

    def check_intentional_slowdown(self, current_load: float, system_capacity: float) -> bool:
        return current_load > system_capacity * 0.95


class Layer11CompetitionEngine:
    """Layer 11: Competition - Game Theory & Unit Economic Pivots."""

    def check_pivot_trigger(self, gross_margin: float, cost_of_capital: float) -> bool:
        return gross_margin < cost_of_capital


class Layer12OrgDesignEngine:
    """Layer 12: Organizational Design - Lagrange Multipliers & Coasian Bounds."""

    def evaluate_hiring_triggers(self, shadow_prices: Dict[str, float], market_wages: Dict[str, float]) -> List[str]:
        roles_to_hire = []
        for role, shadow_price in shadow_prices.items():
            wage = market_wages.get(role, float("inf"))
            if shadow_price > wage:
                roles_to_hire.append(role)
        return roles_to_hire

    def coase_delegation_boundary(self, internal_cost: float, market_cost: float) -> str:
        if internal_cost < market_cost:
            return "KEEP_IN_HOUSE"
        return "DELEGATE_OUTSOURCE"


class Layer13MetaLearningEngine:
    """Layer 13: Meta-Learning - Operational Error Backprop & Policy Compilation."""

    def backpropagate_error(
        self, weights: Dict[str, float], error: float, learning_rate: float = 0.01
    ) -> Dict[str, float]:
        updated = {}
        for k, v in weights.items():
            updated[k] = v - (learning_rate * error)
        return updated


class Layer14AIEntrepreneurshipEngine:
    """Layer 14: AI Entrepreneurship - Autonomous Active Inference Orchestration."""

    def __init__(self) -> None:
        self.l1 = Layer1RealityEngine()
        self.l2 = Layer2OpportunityDiscoveryEngine()
        self.l3 = Layer3ProblemDiscoveryEngine()
        self.l4 = Layer4DecisionMakingEngine()
        self.l5 = Layer5OpportunityEvaluationEngine()
        self.l6 = Layer6ProductCreationEngine()
        self.l7 = Layer7CustomerUnderstandingEngine()
        self.l8 = Layer8MarketingEngine()
        self.l9 = Layer9SalesEngine()
        self.l10 = Layer10GrowthEngine()
        self.l11 = Layer11CompetitionEngine()
        self.l12 = Layer12OrgDesignEngine()
        self.l13 = Layer13MetaLearningEngine()

    def run_full_14_layer_pipeline(self, pipeline_input: Dict[str, Any]) -> Dict[str, Any]:
        """Runs an end-to-end multi-layer evaluation over a target business concept."""
        # L1 Bounds
        l1_res = self.l1.evaluate_bounds(
            pipeline_input.get("capital_in", 100000),
            pipeline_input.get("capital_out", 20000),
            pipeline_input.get("burn_rate_days", 30),
        )

        # L2 Signal Discovery
        kl = self.l2.search_kl_divergence(
            pipeline_input.get("demand_dist", [0.7, 0.3]), pipeline_input.get("supply_dist", [0.2, 0.8])
        )

        # L3 Problem Root Cause
        l3_res = self.l3.decompose_causal_problem(
            pipeline_input.get("causal_edges", [("root_issue", "symptom_a")]), "symptom_a"
        )

        # L4 Decision
        kill_status = self.l4.sprt_idea_kill_check(pipeline_input.get("log_likelihood_ratio", 2.5))

        # L5 Evaluation
        ev = self.l5.calculate_jump_diffusion_ev(100000, 0.1, 0.2, 0.05, -0.3, 1.0)

        # L9 Sales Routing
        sales_model = self.l9.route_sales_model(pipeline_input.get("acv", 12000))

        # L10 Growth
        network_val = self.l10.calculate_network_value(pipeline_input.get("user_count", 100))

        # L12 Org Hiring
        hiring_roles = self.l12.evaluate_hiring_triggers({"eng": 150000}, {"eng": 120000})

        return {
            "status": "success",
            "l1_reality": l1_res,
            "l2_kl_divergence": kl,
            "l3_problem": l3_res,
            "l4_sprt_status": kill_status,
            "l5_jump_diffusion_ev": ev,
            "l9_sales_model": sales_model,
            "l10_network_value": network_val,
            "l12_hiring_roles": hiring_roles,
        }


class FourteenLayerEntrepreneurshipOrchestrator(Layer14AIEntrepreneurshipEngine):
    """Alias for Layer 14 master orchestrator."""

    pass
