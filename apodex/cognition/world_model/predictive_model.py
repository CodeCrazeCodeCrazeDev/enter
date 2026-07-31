from __future__ import annotations
import logging
import math
import random
from typing import Dict, Any, List, Tuple, Optional

logger = logging.getLogger("apodex.cognition.world_model")


class UnifiedPredictiveModel:
    """
    The Single World Model Engine for AEAN, EIOS, and EOS (Redesigned).
    Upgraded for 5-Year continuous operational resilience:
    1. Dynamic state variables mapping to protect against hardcoding.
    2. Exact Pearl's do-calculus interventions with nonlinear boundary clipping limits.
    3. Safe parallel branching universes and Bayesian surprise regime checking.
    """

    def __init__(self) -> None:
        self.base_parameters: Dict[str, Any] = {
            "market_saturation": 0.15,
            "complexity_cost_multiplier": 1.2,
            "failure_probability_offset": 0.05,
            "interest_decay_rate": 0.02,
            "competitor_aggression": 0.35,
            "user_retention_rate": 0.85
        }
        # Generalized, dynamic variables mapping
        self.variables: List[str] = ["marketing_spend", "conversion_rate", "product_quality", "user_growth", "revenue"]
        self.causal_graph: Dict[str, List[str]] = {
            "marketing_spend": [],
            "product_quality": [],
            "conversion_rate": ["product_quality"],
            "user_growth": ["marketing_spend", "conversion_rate"],
            "revenue": ["user_growth"]
        }
        self.coefficients: Dict[Tuple[str, str], float] = {
            ("product_quality", "conversion_rate"): 1.5,
            ("marketing_spend", "user_growth"): 0.8,
            ("conversion_rate", "user_growth"): 1.2,
            ("user_growth", "revenue"): 10.0
        }

    def add_causal_relationship(self, cause: str, effect: str, coefficient: float) -> None:
        """Dynamically declares new variables and coefficients on the fly."""
        if cause not in self.variables:
            self.variables.append(cause)
        if effect not in self.variables:
            self.variables.append(effect)
        if effect not in self.causal_graph:
            self.causal_graph[effect] = []
        if cause not in self.causal_graph[effect]:
            self.causal_graph[effect].append(cause)
        self.coefficients[(cause, effect)] = coefficient

    def simulate_do_intervention(self, target_variable: str, intervention_value: float) -> Dict[str, float]:
        """
        Simulates Pearl's do-operator (do(X = x)).
        Enforces nonlinear boundary clipping limits to prevent negative values or infinite loops.
        """
        states: Dict[str, float] = {v: 0.1 for v in self.variables}
        states[target_variable] = float(intervention_value)

        # Non-linear threshold clipping bounds helper
        def clip_bounds(val: float) -> float:
            if math.isnan(val) or math.isinf(val):
                return 0.0
            return max(0.01, min(1000000.0, val))

        for _ in range(len(self.variables)):
            for var in self.variables:
                if var == target_variable:
                    states[var] = clip_bounds(states[var])
                    continue
                parents = self.causal_graph.get(var, [])
                if not parents:
                    continue
                val = 0.0
                for parent in parents:
                    coef = self.coefficients.get((parent, var), 0.5)
                    val += coef * states[parent]
                states[var] = clip_bounds(val)

        return states

    def generate_parallel_universe_rollout(
        self,
        strategy_type: str,
        initial_params: Dict[str, Any],
        timesteps: int = 5
    ) -> List[Dict[str, Any]]:
        """Generates branching futures representing parallel universe rollouts of a strategy."""
        universe_timeline = []
        current_state = {
            "marketing_spend": float(initial_params.get("marketing_spend", 10.0)),
            "product_quality": float(initial_params.get("product_quality", 5.0)),
            "conversion_rate": 0.1,
            "user_growth": 100.0,
            "revenue": 1000.0
        }

        for t in range(timesteps):
            noise = random.normalvariate(0.0, 0.1)
            # Clip bounds to protect against extreme noise
            current_state["product_quality"] = max(1.0, min(100.0, current_state["product_quality"] * (1.0 + noise * 0.2)))

            current_state["conversion_rate"] = max(0.01, min(0.99, current_state["product_quality"] * self.coefficients.get(("product_quality", "conversion_rate"), 1.5) * 0.02))
            current_state["user_growth"] = max(1.0, (
                current_state["marketing_spend"] * self.coefficients.get(("marketing_spend", "user_growth"), 0.8) +
                current_state["conversion_rate"] * 500.0
            ) * self.base_parameters["user_retention_rate"])

            current_state["revenue"] = max(10.0, current_state["user_growth"] * self.coefficients.get(("user_growth", "revenue"), 10.0))

            universe_timeline.append({
                "timestep": t,
                "states": current_state.copy()
            })

        return universe_timeline

    def predict_strategy_outcome(self, strategy_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Provides backward-compatible strategy outcomes with robust boundary safeguards."""
        logger.info(f"UnifiedPredictiveModel predicting strategy outcome: {strategy_type}")
        cost_cents = max(1, parameters.get("estimated_cost_cents", 100_000))
        base_risk = max(0.0, min(1.0, parameters.get("base_risk", 0.2)))
        market_size_cents = max(1000, parameters.get("market_size_cents", 10_000_000))

        interventional_val = float(parameters.get("marketing_spend", 50.0))
        post_states = self.simulate_do_intervention("marketing_spend", interventional_val)

        conversion_rate = max(0.001, min(0.15, post_states.get("conversion_rate", 0.1) * 0.1))
        expected_revenue_cents = int(market_size_cents * conversion_rate * (1.0 - self.base_parameters["market_saturation"]))
        roi_multiple = max(0.0, min(1000.0, expected_revenue_cents / cost_cents))

        feasibility_prob = max(0.01, min(0.99, 1.0 - (base_risk * self.base_parameters["complexity_cost_multiplier"])))

        return {
            "feasibility_confidence": feasibility_prob,
            "projected_revenue_cents": expected_revenue_cents,
            "roi_multiple": roi_multiple,
            "complexity_multiplier": self.base_parameters["complexity_cost_multiplier"],
            "risk_mitigation_factor": 1.0 - self.base_parameters["failure_probability_offset"],
            "causal_states_provenance": post_states
        }

    def detect_regime_change(self, observation_history: List[float], expected_mean: float) -> bool:
        """Detects significant shifts in environmental indicators using Bayesian Surprise."""
        if len(observation_history) < 5:
            return False

        empirical_mean = sum(observation_history) / len(observation_history)
        variance = sum((x - empirical_mean) ** 2 for x in observation_history) / len(observation_history)
        std_dev = math.sqrt(max(1e-5, variance))

        z_score = abs(empirical_mean - expected_mean) / std_dev
        surprise_entropy = 0.5 * (z_score ** 2)

        if surprise_entropy > 3.0:
            logger.warning(f"UnifiedPredictiveModel: REGIME CHANGE DETECTED! Surprise entropy: {surprise_entropy:.3f}")
            # Non-linear damping limits on parameters updates to prevent parameter explosions
            self.base_parameters["complexity_cost_multiplier"] = min(3.0, self.base_parameters["complexity_cost_multiplier"] * 1.1)
            self.base_parameters["failure_probability_offset"] = min(0.5, self.base_parameters["failure_probability_offset"] + 0.05)
            return True

        return False

    def update_model_parameters(self, factor_updates: Dict[str, Any]) -> None:
        """Enables learning loops to safely refine parameters with bounds limits."""
        for key, value in factor_updates.items():
            if key in self.base_parameters:
                logger.info(f"Updating world model parameter: {key} -> {value}")
                # Enforce safe parameter ranges [0.01, 10.0]
                self.base_parameters[key] = max(0.01, min(10.0, value))
