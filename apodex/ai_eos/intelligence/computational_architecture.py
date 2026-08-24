"""
The complete, first-principles executable implementation of the
Computational Architecture of Entrepreneurship for SERO v2.1.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.computational_architecture")


class Opportunity(BaseModel):
    """The canonical data model representing a discovered opportunity state."""
    opportunity_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str
    variables: List[str] = Field(default_factory=list)
    causal_edges: List[Tuple[str, str]] = Field(default_factory=list)
    coefficients: Dict[str, float] = Field(default_factory=dict)
    prior_entropy: float = 1.0
    post_entropy_simulated: float = 0.5
    success_probability: float = 0.5
    target_preference: float = 0.9
    tam_cents: int = 100000000  # Default $1M
    is_active: bool = True


class AdvancedCausalEngine:
    """
    Implements a robust Structural Causal Model (SCM) capable of handling
    Pearl's do-calculus interventions and counterfactual estimations.
    """

    def __init__(self) -> None:
        self.variables: Set[str] = set()
        self.parents: Dict[str, List[str]] = {}
        self.coefficients: Dict[Tuple[str, str], float] = {}
        self.baseline_noise: Dict[str, float] = {}

    def register_variable(self, name: str, noise_variance: float = 0.1) -> None:
        self.variables.add(name)
        self.baseline_noise[name] = noise_variance
        if name not in self.parents:
            self.parents[name] = []

    def add_causal_relationship(self, parent: str, child: str, coefficient: float) -> None:
        self.register_variable(parent)
        self.register_variable(child)
        if parent not in self.parents[child]:
            self.parents[child].append(parent)
        self.coefficients[(parent, child)] = coefficient

    def execute_do_intervention(self, target_var: str, value: float) -> Dict[str, float]:
        """
        Simulates Judea Pearl's do-operator (do(X = x)).
        Mutates the structural equations, freezing the target variable
        and propagating the interventional downstream effects.
        """
        if target_var not in self.variables:
            raise ValueError(f"Variable '{target_var}' is not registered.")

        state: Dict[str, float] = {var: 0.0 for var in self.variables}
        state[target_var] = value

        # Topological propagation loop (max iterations equal to variable count to ensure convergence)
        for _ in range(len(self.variables)):
            for var in self.variables:
                if var == target_var:
                    continue  # The intervened variable is locked

                parents_list = self.parents.get(var, [])
                if not parents_list:
                    continue

                # Propagate structural linear relationships
                structural_sum = 0.0
                for parent in parents_list:
                    coef = self.coefficients.get((parent, var), 0.0)
                    structural_sum += coef * state[parent]

                state[var] = structural_sum

        return state

    def estimate_counterfactual(
        self,
        factual_observations: Dict[str, float],
        counterfactual_intervention: Tuple[str, float],
        target_outcome_var: str
    ) -> float:
        """
        Computes counterfactual outcomes: 'What would the target outcome variable have been,
        had we performed the counterfactual intervention, given the factual observations?'
        """
        intervened_var, inter_value = counterfactual_intervention

        # 1. Abduction Phase: Estimate the background noise (U) for each variable
        noise_estimates: Dict[str, float] = {}
        for var in self.variables:
            factual_val = factual_observations.get(var, 0.0)
            parents_list = self.parents.get(var, [])
            structural_expected = 0.0
            for parent in parents_list:
                coef = self.coefficients.get((parent, var), 0.0)
                structural_expected += coef * factual_observations.get(parent, 0.0)

            # Noise U = Observed - Structural Expected
            noise_estimates[var] = factual_val - structural_expected

        # 2. Action & Prediction Phase: Execute intervention under the updated noise state
        state: Dict[str, float] = {var: 0.0 for var in self.variables}
        state[intervened_var] = inter_value

        for _ in range(len(self.variables)):
            for var in self.variables:
                if var == intervened_var:
                    continue

                parents_list = self.parents.get(var, [])
                structural_sum = 0.0
                for parent in parents_list:
                    coef = self.coefficients.get((parent, var), 0.0)
                    structural_sum += coef * state[parent]

                # Apply estimated noise baseline
                state[var] = structural_sum + noise_estimates.get(var, 0.0)

        return state.get(target_outcome_var, 0.0)


class ActiveInferencePlanner:
    """
    Implements the Active Inference decision framework based on Expected Free Energy (EFE).
    """

    def __init__(self, curiosity_weight: float = 1.0) -> None:
        self.curiosity_weight = curiosity_weight

    def calculate_efe(self, opp: Opportunity) -> float:
        """
        Expected Free Energy G = - Pragmatic Value - Epistemic Value * curiosity_weight
        Where:
          - Pragmatic Value = ln(p_success) - ln(p_target_preference)
          - Epistemic Value = prior_entropy - post_entropy_simulated (uncertainty reduction)
        """
        # Pragmatic Value
        eps = 1e-10
        p_success = max(eps, min(1.0 - eps, opp.success_probability))
        p_target = max(eps, min(1.0 - eps, opp.target_preference))

        pragmatic_value = math.log(p_success) - math.log(p_target)

        # Epistemic Value (Information Gain)
        epistemic_value = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)

        # G = - Pragmatic - Curiosity * Epistemic
        efe = -pragmatic_value - (epistemic_value * self.curiosity_weight)
        return efe

    def rank_opportunities(self, opportunities: List[Opportunity]) -> List[Tuple[Opportunity, float]]:
        ranked = []
        for opp in opportunities:
            efe = self.calculate_efe(opp)
            ranked.append((opp, efe))
        # Lower EFE is superior (minimizing variational surprise)
        return sorted(ranked, key=lambda x: x[1])


from apodex.ai_eos.intelligence.fourteen_layer_engine import FourteenLayerEngine


class EntrepreneurialIntelligenceOrchestrator:
    """
    The master coordinating engine that drives the complete 14-layer execution pipeline.
    """

    def __init__(self, causal_engine: AdvancedCausalEngine, planner: ActiveInferencePlanner) -> None:
        self.causal_engine = causal_engine
        self.planner = planner
        self.opportunities: List[Opportunity] = []
        self.fourteen_layer_engine = FourteenLayerEngine()

    def ingest_signal(self, signal: Dict[str, Any]) -> Opportunity:
        """Senses external changes and creates a candidate opportunity state."""
        logger.info(f"Sensing external signal: {signal.get('title')}")
        opp = Opportunity(
            title=signal.get("title", "Unnamed Opportunity"),
            domain=signal.get("domain", "general"),
            variables=signal.get("variables", []),
            causal_edges=signal.get("causal_edges", []),
            coefficients=signal.get("coefficients", {}),
            prior_entropy=signal.get("prior_entropy", 1.5),
            post_entropy_simulated=signal.get("post_entropy_simulated", 0.4),
            success_probability=signal.get("success_probability", 0.5),
            tam_cents=signal.get("tam_cents", 100000000)
        )
        self.opportunities.append(opp)
        return opp

    def execute_orchestrated_pipeline(self) -> Dict[str, Any]:
        """Runs the 14-layer analysis pipeline over active opportunities."""
        if not self.opportunities:
            return {"status": "idle", "reason": "No opportunities registered."}

        # 1. Opportunity Evaluation and Ranking (Layer 2, 5, 14)
        ranked_opps = self.planner.rank_opportunities(self.opportunities)
        primary_opp, best_efe = ranked_opps[0]

        logger.info(f"Orchestrator selected primary opportunity: '{primary_opp.title}' with EFE: {best_efe:.4f}")

        # 2. Structural Causal Initialization (Layer 3)
        for var in primary_opp.variables:
            self.causal_engine.register_variable(var)
        for parent, child in primary_opp.causal_edges:
            weight = primary_opp.coefficients.get(f"{parent}->{child}", 0.5)
            self.causal_engine.add_causal_relationship(parent, child, weight)

        # 3. Simulate Causal Intervention (Layer 3 & 4)
        # Attempting intervention on the primary driver variable (typically the first registered)
        intervention_var = primary_opp.variables[0] if primary_opp.variables else "marketing_spend"
        inter_state = self.causal_engine.execute_do_intervention(intervention_var, 1.5)

        # 4. Integrate 14-Layer Engine Pipeline Execution
        fourteen_layer_results = self.fourteen_layer_engine.execute_complete_14_layer_pipeline({
            "title": primary_opp.title,
            "domain": primary_opp.domain,
            "variables": primary_opp.variables,
            "tam_cents": primary_opp.tam_cents
        })

        return {
            "status": "executed",
            "selected_opportunity": primary_opp.title,
            "best_expected_free_energy": best_efe,
            "intervention_performed": f"do({intervention_var} = 1.5)",
            "propagated_state": inter_state,
            "fourteen_layer_results": fourteen_layer_results
        }
