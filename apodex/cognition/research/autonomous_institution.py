from __future__ import annotations
import math
import logging
import random
from typing import Dict, Any, List, Optional, Tuple
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("apodex.cognition.research")


class ResearchHypothesis(BaseModel):
    """Represents a scientific hypothesis to be evaluated."""
    hypothesis_id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    prior_probability: float = 0.5
    evidence_quality: float = 0.0


class BeliefState(BaseModel):
    """Represents the parameters of the conjugate Beta-Binomial model for a hypothesis."""
    alpha: float
    beta: float
    last_updated_timestamp: float


class ExpectedFreeEnergyPlanner:
    """
    Implements Karl Friston's Active Inference planning framework.
    Selects policies by minimizing Expected Free Energy (EFE), balancing
    Instrumental Value (pragmatic goal achievement) and Epistemic Value (information gain).
    """

    def __init__(self, curiosity_weight: float = 1.0) -> None:
        self.curiosity_weight = curiosity_weight

    def calculate_epistemic_value(self, prior_entropy: float, expected_posterior_entropy: float) -> float:
        """
        Epistemic Value is the Expected Information Gain, modeled as the expected
        reduction in uncertainty (entropy reduction) between prior and posterior states.
        """
        # KL-divergence / Information Gain bound
        return max(0.0, prior_entropy - expected_posterior_entropy)

    def calculate_instrumental_value(self, predicted_outcome_prob: float, target_preference: float) -> float:
        """
        Instrumental Value is the negative divergence between predicted outcomes and target preferences.
        """
        # Simplifies to maximizing log likelihood of satisfying preferences
        if predicted_outcome_prob <= 0.0:
            return -100.0
        return math.log(predicted_outcome_prob) - math.log(target_preference)

    def select_optimal_policy(
        self,
        candidate_policies: List[Dict[str, Any]]
    ) -> Tuple[Dict[str, Any], float]:
        """
        Selects the policy that minimizes Expected Free Energy (minimizing G implies maximizing utility):
        G = - Instrumental_Value - Epistemic_Value * curiosity_weight
        We choose the minimum G.
        """
        best_policy = None
        min_efe = float("inf")

        for policy in candidate_policies:
            # Extract attributes or simulate defaults
            prior_entropy = policy.get("prior_entropy", 1.0)
            post_entropy = policy.get("post_entropy", 0.5)
            predicted_prob = policy.get("predicted_prob", 0.8)
            target_pref = policy.get("target_pref", 0.9)

            epistemic = self.calculate_epistemic_value(prior_entropy, post_entropy)
            instrumental = self.calculate_instrumental_value(predicted_prob, target_pref)

            # EFE G = - Pragmatic - Curiosity * Epistemic
            # To minimize EFE, we maximize Pragmatic + Curiosity * Epistemic
            # Standard Active Inference formulation: G = -Instrumental - curiosity * Epistemic
            efe = -instrumental - (epistemic * self.curiosity_weight)

            policy["calculated_epistemic"] = epistemic
            policy["calculated_instrumental"] = instrumental
            policy["calculated_efe"] = efe

            if efe < min_efe:
                min_efe = efe
                best_policy = policy

        return best_policy or candidate_policies[0], min_efe


class StructuralCausalModel:
    """
    Represents structural causal models (SCMs) and Pearl's causal intervention calculus (do-calculus).
    Acts as a hybrid model: uses semantic identifiers for variables and computes treatment effects.
    """

    def __init__(self) -> None:
        self.variables: List[str] = []
        # causal parents: key is child, value is set of parents
        self.causal_graph: Dict[str, List[str]] = {}
        # linear coefficient relationships for structural equations
        self.coefficients: Dict[Tuple[str, str], float] = {}

    def add_variable(self, name: str) -> None:
        if name not in self.variables:
            self.variables.append(name)

    def add_causal_link(self, source: str, target: str, weight: float = 0.5) -> None:
        self.add_variable(source)
        self.add_variable(target)
        if target not in self.causal_graph:
            self.causal_graph[target] = []
        if source not in self.causal_graph[target]:
            self.causal_graph[target].append(source)
        self.coefficients[(source, target)] = weight

    def intervene_do(self, variable: str, value: float) -> Dict[str, float]:
        """
        Simulates Judea Pearl's do-operator (do(X = x)).
        Breaks the natural equations for the variable, settings its value to `value`,
        and propagates the effect down the causal graph.
        """
        values: Dict[str, float] = {v: 0.0 for v in self.variables}
        values[variable] = value

        # Topological sorting or simple propagation
        # Since we use directed relationships, we perform iterative updates to converge
        for _ in range(len(self.variables)):
            for child in self.variables:
                if child == variable:
                    continue  # do(X) keeps X locked
                parents = self.causal_graph.get(child, [])
                if not parents:
                    continue
                # Calculate value: sum of coefficient * parent_value
                child_val = 0.0
                for parent in parents:
                    coef = self.coefficients.get((parent, child), 0.0)
                    child_val += coef * values[parent]
                values[child] = child_val

        return values


class EbbinghausMemoryConsolidator:
    """
    Implements Bayesian posterior updates under a Beta-Binomial conjugate model,
    with an exponential decay function based on the Ebbinghaus Forgetting Curve.
    """

    def __init__(self, decay_rate: float = 0.01) -> None:
        self.decay_rate = decay_rate

    def consolidate_belief(
        self,
        current_belief: BeliefState,
        trials: int,
        successes: int,
        current_timestamp: float
    ) -> BeliefState:
        """
        Updates Beta(alpha, beta) parameters. Prior experiences decay exponentially over time
        to model forgetting of obsolete/unreinforced evidence.
        """
        delta_t = max(0.0, current_timestamp - current_belief.last_updated_timestamp)
        decay_factor = math.exp(-self.decay_rate * delta_t)

        # Decay prior parameters towards flat priors or zero-mean
        # In Beta-Binomial, decay brings alpha/beta closer to 1 (neutral) or just decays them.
        # We decay the historical evidence weight above the uniform prior baseline (alpha=1, beta=1)
        decayed_alpha_excess = (current_belief.alpha - 1.0) * decay_factor
        decayed_beta_excess = (current_belief.beta - 1.0) * decay_factor

        new_alpha = 1.0 + decayed_alpha_excess + successes
        new_beta = 1.0 + decayed_beta_excess + (trials - successes)

        return BeliefState(
            alpha=new_alpha,
            beta=new_beta,
            last_updated_timestamp=current_timestamp
        )


class ConsensAgentEngine:
    """
    Mitigates multi-agent sycophancy (CONSENSAGENT, VT 2024/2025) in multi-mind strategic consensus.
    Coordinates distinct agentic paradigms to debate and deliberate research hypotheses.
    """

    def __init__(self, paradigms: Optional[List[str]] = None) -> None:
        self.paradigms = paradigms or [
            "Bayesian",
            "Symbolic",
            "Causal",
            "Economic",
            "Game-Theoretic",
            "Mechanistic"
        ]

    def resolve_debate_consensus(
        self,
        hypothesis: ResearchHypothesis,
        individual_evaluations: Dict[str, float]
    ) -> Tuple[float, float]:
        """
        Collects paradigm evaluations, detects echo traps/sycophancy (by measuring low-variance clustering),
        dynamically re-weights conforming minds, and returns the unified strategic confidence level.
        """
        raw_vals = [individual_evaluations.get(p, 0.5) for p in self.paradigms]
        mean_val = sum(raw_vals) / len(raw_vals)

        # Measure variance of opinions
        variance = sum((v - mean_val) ** 2 for v in raw_vals) / len(raw_vals)
        std_dev = math.sqrt(variance)

        # Sycophancy mitigation: if variance is extremely low (std_dev < 0.05),
        # meaning minds are uncritically echoing each other, we inject a dissenting/adversarial critic weight
        # to depress over-confidence.
        sycophancy_correction = 1.0
        if std_dev < 0.05:
            logger.warning("CONSENSAGENT: Sycophancy/echo trap detected! Low cognitive diversity in debate.")
            # Penalize overall confidence to reflect echo-chamber risk
            sycophancy_correction = 0.8

        final_score = mean_val * sycophancy_correction
        return final_score, std_dev
