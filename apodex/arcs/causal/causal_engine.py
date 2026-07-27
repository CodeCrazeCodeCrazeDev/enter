from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional

from apodex.arcs.world_graph import WorldGraph, EntityNode, RelationshipEdge

logger = logging.getLogger("arcs.causal")


class CausalIntelligenceEngine:
    """Phase 1 Causal Intelligence Engine.

    Implements structural causal graph representation over WorldGraph, Wright path
    propagation, lightweight treatment effect estimation, and counterfactual simulation.
    """

    def __init__(self, world_graph: Optional[WorldGraph] = None) -> None:
        self.world_graph = world_graph or WorldGraph()

    def register_causal_relation(
        self,
        cause_id: str,
        effect_id: str,
        coefficient: float,
        p_value: float = 0.05,
        confounders: Optional[List[str]] = None
    ) -> None:
        """Register a causal relationship between a cause and an effect node."""
        properties = {
            "coefficient": coefficient,
            "p_value": p_value,
            "confounders": confounders or []
        }

        # Ensure variable nodes exist
        if cause_id not in self.world_graph.nodes:
            self.world_graph.add_node(EntityNode(node_id=cause_id, node_type="causal_variable"))
        if effect_id not in self.world_graph.nodes:
            self.world_graph.add_node(EntityNode(node_id=effect_id, node_type="causal_variable"))

        edge = RelationshipEdge(
            source_id=cause_id,
            target_id=effect_id,
            relation_type="CAUSES",
            weight=abs(coefficient),  # Weight reflects absolute magnitude of impact
            properties=properties
        )
        self.world_graph.add_relation(edge)
        logger.info(f"Registered causal link: {cause_id} -> {effect_id} (coeff: {coefficient:.4f}, p-val: {p_value:.3f})")

    def estimate_treatment_effect(self, cause_id: str, effect_id: str) -> Dict[str, Any]:
        """Estimate the treatment effect of a cause on an effect.

        For Phase 1, uses Wright's Path Analysis rules (propagating coefficients
        along the shortest directed path) and handles potential direct/indirect effects.
        """
        path = self.world_graph.find_path(cause_id, effect_id)
        if not path:
            return {
                "treatment_effect": 0.0,
                "path_found": False,
                "confidence": 0.0,
                "method": "zero_effect_fallback"
            }

        # Calculate Wright's path coefficient (product of coefficients along the path)
        net_coefficient = 1.0
        confidence_product = 1.0

        for i in range(len(path) - 1):
            src, tgt = path[i], path[i+1]
            # Find the active CAUSES relation
            relations = self.world_graph.get_relations_from(src)
            causal_edge = None
            for r in relations:
                if r.target_id == tgt and r.relation_type == "CAUSES":
                    causal_edge = r
                    break

            if not causal_edge:
                return {
                    "treatment_effect": 0.0,
                    "path_found": False,
                    "confidence": 0.0,
                    "method": "broken_path"
                }

            coeff = causal_edge.properties.get("coefficient", 1.0)
            p_val = causal_edge.properties.get("p_value", 0.05)

            net_coefficient *= coeff
            # Simple heuristic confidence score: 1 - p_value
            confidence_product *= max(0.0, 1.0 - p_val)

        logger.info(f"Estimated treatment effect for {cause_id} -> {effect_id}: {net_coefficient:.4f} (Confidence: {confidence_product:.2%})")
        return {
            "treatment_effect": net_coefficient,
            "path_found": True,
            "path": path,
            "confidence": confidence_product,
            "method": "wright_path_analysis"
        }

    def run_counterfactual(
        self,
        intervention_id: str,
        intervention_value_change: float,
        outcome_id: str,
        baseline_value: float = 0.0
    ) -> float:
        """Simulate a counterfactual intervention.

        Answers: 'If we change variable X by value Y, what is the predicted counterfactual outcome of Z?'
        Outcome = baseline_value + (intervention_value_change * total_treatment_effect)
        """
        estimation = self.estimate_treatment_effect(intervention_id, outcome_id)
        treatment_effect = estimation["treatment_effect"]
        counterfactual_outcome = baseline_value + (intervention_value_change * treatment_effect)

        logger.info(
            f"Counterfactual Intervention: Change {intervention_id} by {intervention_value_change:+.2f} "
            f"-> Predicted outcome of {outcome_id}: {counterfactual_outcome:.4f} (baseline: {baseline_value:.2f})"
        )
        return counterfactual_outcome

    def bayesian_update_belief(self, prior_prob: float, likelihood_ratio: float) -> float:
        """Simple Bayesian update of belief probability given a likelihood ratio.

        Posterior Odds = Prior Odds * Likelihood Ratio
        """
        if prior_prob <= 0.0:
            return 0.0
        if prior_prob >= 1.0:
            return 1.0

        prior_odds = prior_prob / (1.0 - prior_prob)
        posterior_odds = prior_odds * likelihood_ratio
        posterior_prob = posterior_odds / (1.0 + posterior_odds)

        return max(0.0, min(1.0, posterior_prob))
