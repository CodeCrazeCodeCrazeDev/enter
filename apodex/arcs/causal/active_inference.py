from __future__ import annotations
import math
import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger("arcs.causal.active_inference")


class ActiveInferenceEngine:
    """Layer 14 Active Inference Engine.

    Implements a formal framework where decisions minimize Variational Free Energy
    and reduce epistemic uncertainty about the market, rather than simply maximizing
    short-term correlational rewards.
    """

    def __init__(self, initial_beliefs: Optional[Dict[str, float]] = None) -> None:
        # Beliefs represent the agent's estimated probability distributions over states
        self.beliefs = initial_beliefs or {
            "customer_demand_is_high": 0.5,
            "competitor_will_retaliate": 0.5,
            "market_channels_are_receptive": 0.5
        }
        self.free_energy_history: List[float] = []

    def observe(self, observation_key: str, actual_value: float) -> float:
        """Observe an outcome, update variational free energy, and adjust internal beliefs."""
        predicted_belief = self.beliefs.get(observation_key, 0.5)

        # Variational Free Energy estimation: F = Complexity - Accuracy
        # Let's model this as the Kullback-Leibler (KL) divergence or squared prediction error
        # of the generative model prediction vs actual observed reality.
        prediction_error = actual_value - predicted_belief
        free_energy = (prediction_error ** 2)

        self.free_energy_history.append(free_energy)

        # Active Inference Update Loop: Update beliefs in direction of prediction error to reduce Free Energy
        # Belief(t+1) = Belief(t) + learning_rate * prediction_error
        learning_rate = 0.15
        updated_belief = predicted_belief + learning_rate * prediction_error
        self.beliefs[observation_key] = max(0.01, min(0.99, updated_belief))

        logger.info(
            f"[Active Inference] Observed {observation_key} = {actual_value:.2f} (Prediction: {predicted_belief:.2f}). "
            f"Free Energy: {free_energy:.4f}, Updated Belief: {self.beliefs[observation_key]:.2f}"
        )
        return free_energy

    def select_action_to_minimize_uncertainty(
        self,
        options: Dict[str, Dict[str, Any]]
    ) -> Tuple[str, Dict[str, Any]]:
        """Select an action or plan that minimizes Expected Free Energy (preferring epistemic exploration).

        Expected Free Energy (G) = Epistemic Value (uncertainty reduction) + Pragmatic Value (utility).
        """
        best_option_key = ""
        min_expected_free_energy = float("inf")
        selected_option = {}

        for key, opt in options.items():
            # Epistemic value: how much uncertainty does this reduce? (represented by variance or ignorance)
            epistemic_value = opt.get("epistemic_value", 0.5) # higher reduces uncertainty more
            # Pragmatic value: expected business outcome / reward
            pragmatic_value = opt.get("expected_roi", 0.0)

            # Expected Free Energy: G = Complexity (or Pragmatic cost/negative reward) - Epistemic Value
            # High pragmatic reward and high epistemic uncertainty-reduction minimize G
            expected_free_energy = -1.0 * pragmatic_value - 2.0 * epistemic_value

            if expected_free_energy < min_expected_free_energy:
                min_expected_free_energy = expected_free_energy
                best_option_key = key
                selected_option = opt

        logger.info(f"[Active Inference] Selected action '{best_option_key}' with Expected Free Energy: {min_expected_free_energy:.4f}")
        return best_option_key, selected_option
