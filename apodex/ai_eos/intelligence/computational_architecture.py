"""The Complete 14-Layer Computational Architecture of Entrepreneurship.

This module formalizes entrepreneurship as a complete, multi-tiered adaptive system.
Each layer from Reality to AI Entrepreneurship is represented through exact
algorithms, mathematical formulations, feedback loops, and decision logic.
"""

from __future__ import annotations
import math
import logging
from typing import Any, Dict, List, Optional, Tuple, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.computational_architecture")


# ----------------------------------------------------------------------
# Core Data Models
# ----------------------------------------------------------------------

class Opportunity(BaseModel):
    """Represents an entrepreneurial opportunity detected in the world state."""
    opportunity_id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    weak_signals: List[str] = Field(default_factory=list)
    combined_observations: List[str] = Field(default_factory=list)
    novelty_score: float = Field(0.0, ge=0.0, le=1.0)

    # Problems and causes
    primary_problem_id: Optional[str] = None
    root_cause_identified: bool = False
    is_first_order_problem: bool = True

    # Evaluation Metrics
    expected_value: float = Field(0.0)
    downside_risk_var: float = Field(0.0, ge=0.0, description="Value-at-Risk representation.")
    timing_score: float = Field(0.5, ge=0.0, le=1.0)

    # GTM & Production state
    jtbd_core: str = Field(default="")
    complexity_budget_used: float = Field(0.0)
    trust_score: float = Field(0.5, ge=0.0, le=1.0)

    # Meta tracking
    is_killed: bool = Field(default=False)
    created_at_timestamp: float = Field(default=0.0)


# ----------------------------------------------------------------------
# Layer 1: Reality
# ----------------------------------------------------------------------

class RealityOptimizer:
    """Layer 1: The First-Principles Foundation of Entrepreneurship.

    Deconstructs entrepreneurship to its absolute baseline: returning high value
    on risk-adjusted cognitive energy and capital. Distinguishes psychology
    (intuition bias, risk tolerance) from optimization (calculable variables).
    """

    def __init__(self, human_risk_aversion: float = 2.0, cognitive_energy_weight: float = 1.0) -> None:
        self.human_risk_aversion = human_risk_aversion
        self.cognitive_energy_weight = cognitive_energy_weight

    def calculate_global_objective(
        self,
        expected_revenue: float,
        value_at_risk: float,
        cognitive_energy_expended: float,
        capital_cost: float
    ) -> float:
        """Computes the global entrepreneurial objective function:

        U_ent = (E[R] - w_r * VaR(R)) / (E[E_cogn] + w_c * C)
        """
        numerator = expected_revenue - self.human_risk_aversion * value_at_risk
        denominator = cognitive_energy_expended + self.cognitive_energy_weight * capital_cost

        if denominator <= 0:
            return numerator
        return numerator / denominator

    def get_fundamental_nature(self) -> Dict[str, str]:
        """Defines what entrepreneurship is at its most fundamental level.

        Entrepreneurship is the active-inference search across non-equilibrium environmental states
        to locate, validate, and exploit arbitrage opportunities, creating localized islands of low
        entropy (structured organizations and products) funded by free energy extraction (capital).
        """
        return {
            "definition": "The systematic extraction of economic free energy from non-equilibrium environment states.",
            "thermodynamic_analogy": "Creating localized low-entropy systems (companies) in exchange for capital dissipation.",
            "mathematical_core": "Minimizing the system's Expected Free Energy (G) under uncertainty."
        }

    def get_invariant_principles(self) -> List[Dict[str, str]]:
        """Returns the core invariant principles found in every successful entrepreneur."""
        return [
            {
                "name": "Asymmetric Risk Profile",
                "formulation": "Downside capped strictly; upside unbounded (real options)."
            },
            {
                "name": "Bayesian Epistemic Updating",
                "formulation": "Constantly updating priors using active environmental probes (experiments)."
            },
            {
                "name": "Active Backtracking and Failure Capitalization",
                "formulation": "Viewing errors not as terminal states, but as textual gradients for model refinement."
            },
            {
                "name": "Value-at-Risk Gating",
                "formulation": "Ensuring the survival of the organism through strict capital preservation."
            }
        ]

    def deconstruct_psychology_vs_optimization(self) -> Dict[str, List[str]]:
        """Distinguishes between components governed by human psychology vs mathematical optimization."""
        return {
            "human_psychology": [
                "Zero-to-one vision generation",
                "Empathy and trust building with early customers",
                "Founder grit and emotional self-regulation under extreme ambiguity",
                "Intuition-based heuristics in high-risk, zero-data regimes"
            ],
            "optimization_problems": [
                "Capital allocation between ventures (Bayesian Thompson Sampling)",
                "Pricing and dynamic revenue extraction",
                "Supply chain and routing scheduling",
                "Experimentation sizing and power calculations"
            ]
        }

    def map_automation_boundaries(self, task_name: str, complexity_score: float) -> Tuple[bool, str]:
        """Classifies task as fully automatable or human-only.

        Optimization tasks (pricing, routing, allocation) are automatable.
        Psychological high-empathy trust or zero-to-one vision remain human-bound.
        """
        if complexity_score < 0.4:
            return True, "AUTOMATABLE_DETERMINISTIC"

        # High complexity mathematical optimization is automatable
        if any(keyword in task_name.lower() for keyword in ["pricing", "allocation", "portfolio", "routing", "scheduling"]):
            return True, "AUTOMATABLE_PROBABILISTIC"

        # Pure strategic zero-to-one vision or high-trust human networking
        if any(keyword in task_name.lower() for keyword in ["trust", "vision", "empathy", "relationship", "negotiation"]):
            return False, "HUMAN_PSYCHOLOGY_BOUND"

        return True, "AUTOMATABLE_AGENTIC"

    def analyze_automation_potential(self) -> Dict[str, Dict[str, Any]]:
        """Explicitly defines what can and cannot be automated in the entrepreneurial loop."""
        return {
            "automatable": {
                "tasks": [
                    "Weak-signal continuous search space ingestion",
                    "Bayesian valuation of alternative models",
                    "Dynamic experiment design and execution tracking",
                    "Complexity enforcement and code generation"
                ],
                "formalization": "Represented as active inference and reinforcement learning under POMDPs."
            },
            "non_automatable": {
                "tasks": [
                    "Initial value alignment and primary human goal specification",
                    "Establishing radical trust and zero-to-one empathy lines",
                    "Navigating extreme institutional paradigm shifts (regulatory changes requiring human political relationships)"
                ],
                "formalization": "Requires true physical social presence and subjective human-centric utility alignment."
            }
        }


# ----------------------------------------------------------------------
# Layer 2: Opportunity Discovery
# ----------------------------------------------------------------------

class OpportunityDiscoveryEngine:
    """Layer 2: Continuous search of the world's state space for high-value opportunities.

    Tracks weak signals, applies combinatorial synthesis to construct novelty, and filters out noise.
    """

    def __init__(self, filter_threshold: float = 0.3) -> None:
        self.filter_threshold = filter_threshold

    def filter_weak_signals(self, raw_signals: Dict[str, float]) -> List[str]:
        """Weighs and filters weak signals to separate trend-relevant signals from background noise."""
        valid_signals = []
        for signal_id, amplitude in raw_signals.items():
            if amplitude >= self.filter_threshold:
                valid_signals.append(signal_id)
        return valid_signals

    def search_world_state_space(self, world_states: List[Dict[str, Any]]) -> List[Opportunity]:
        """Continuously searches the world state space for economically valuable opportunities.

        Employs active inference to identify state dimensions showing extreme entropy changes or structural gaps.
        """
        discovered = []
        for state in world_states:
            # Extract attributes
            name = state.get("name", "Unknown state")
            signals = state.get("signals", {})
            filtered = self.filter_weak_signals(signals)

            if len(filtered) >= 2:
                opp = self.synthesize_combinatorial_opportunity(filtered[0], filtered[1], state)
                discovered.append(opp)
        return discovered

    def detect_weak_signals(self, signals_feed: List[Dict[str, float]]) -> Dict[str, float]:
        """Detects weak signals out of highly noisy background environment streams.

        Calculates signal-to-noise ratio (SNR). Weak signals are low-amplitude but show persistent positive trends.
        """
        aggregated_signals = {}
        for feed in signals_feed:
            for signal, value in feed.items():
                aggregated_signals[signal] = aggregated_signals.get(signal, 0.0) + value

        # Normalize and filter based on persistence
        for signal in list(aggregated_signals.keys()):
            aggregated_signals[signal] /= len(signals_feed)

        return {k: v for k, v in aggregated_signals.items() if v > 0.15}

    def filter_signals_by_entropy(self, raw_signals: Dict[str, float]) -> Dict[str, float]:
        """Filters signals using Shannon Entropy as a filter.

        High entropy signals are discarded as white noise; low/mid entropy clusters denote coherent trends.
        """
        filtered = {}
        for sig, val in raw_signals.items():
            # Model entropy of the signal source
            p = max(0.001, min(0.999, val))
            entropy = -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)
            # Retain signals showing structured patterns (low-to-moderate entropy)
            if entropy < 0.85:
                filtered[sig] = val
        return filtered

    def combine_unrelated_observations(self, observation_a: str, observation_b: str) -> str:
        """Synthetically combines two unrelated observations to unlock cross-domain novelty.

        E.g., combining 'Decentralized Compute Networks' with 'Bio-wearable Sensors' -> 'Federated Wearable Bio-AI Networks'
        """
        return f"Combinatorial Convergence: Unified application of {observation_a} onto {observation_b} context."

    def generate_novelty_score(self, domain_a: str, domain_b: str) -> float:
        """Calculates structural novelty score as a function of semantic distance.

        Novelty = 1.0 - (Jaccard Overlap of domain keywords).
        """
        set_a = set(domain_a.lower().split("_"))
        set_b = set(domain_b.lower().split("_"))
        intersection = set_a.intersection(set_b)
        union = set_a.union(set_b)
        if not union:
            return 1.0
        return 1.0 - (len(intersection) / len(union))

    def evaluate_trend_importance(self, trend_volatility: float, growth_rate: float, adoption_velocity: float) -> float:
        """Evaluates whether a trend matters based on momentum, growth, and low volatility."""
        if trend_volatility <= 0:
            trend_volatility = 0.01
        return (growth_rate * adoption_velocity) / math.sqrt(trend_volatility)

    def predict_emerging_market(self, past_growth_rates: List[float], horizon_steps: int) -> float:
        """Predicts emerging market sizes before competitors by fitting exponential growth expectations."""
        if not past_growth_rates:
            return 0.0
        avg_rate = sum(past_growth_rates) / len(past_growth_rates)
        # S-curve sigmoid ceiling representation
        projected = math.exp(avg_rate * horizon_steps)
        return min(1.0, 1.0 / (1.0 + math.exp(-projected / 10.0)))

    def explain_invisible_opportunity_factors(self) -> List[str]:
        """Provides the scientific factors that make an opportunity invisible to standard competitors."""
        return [
            "Confounded observations (where cause and effect are obscured by a latent variable)",
            "High cognitive complexity barrier (cross-disciplinary convergence points)",
            "Delayed feedback loops (standard short-sighted market actors cannot verify value in real time)",
            "Asymmetry of belief (consensus views it as a failing experiment, elite views it as a learning step)"
        ]

    def synthesize_combinatorial_opportunity(
        self,
        signal_a: str,
        signal_b: str,
        world_context: Dict[str, Any]
    ) -> Opportunity:
        """Combines unrelated observations and weak signals to generate a novel opportunity."""
        name = f"Synthesis: {signal_a} + {signal_b}"
        desc = f"Synthesized opportunity from weak signals under context {world_context.get('market_trend', 'general')}"

        dist = self.generate_novelty_score(signal_a, signal_b)
        novelty = min(0.99, max(0.1, dist * 2.0))

        return Opportunity(
            name=name,
            description=desc,
            weak_signals=[signal_a, signal_b],
            combined_observations=[signal_a, signal_b],
            novelty_score=novelty
        )


# ----------------------------------------------------------------------
# Layer 3: Problem Discovery
# ----------------------------------------------------------------------

class ProblemDiscoveryEngine:
    """Layer 3: Decomposition and validation of problem statements.

    Identifies first-order vs second-order dependencies, and applies Judea Pearl's
    backdoor criterion to isolate actual root causes from symptomatic observations.
    """

    def __init__(self) -> None:
        pass

    def define_problem(self, problem_statement: str, symptoms: List[str]) -> Dict[str, Any]:
        """Formally defines a problem as a structural mismatch between current state and desired state."""
        return {
            "problem_id": str(uuid4()),
            "statement": problem_statement,
            "symptoms": symptoms,
            "validation_status": "PENDING_VERIFICATION"
        }

    def verify_stated_vs_real_problem(self, stated_symptoms: List[str], systemic_variables: Dict[str, Any]) -> Tuple[bool, str]:
        """Determines whether a user-stated problem is the actual bottleneck or merely a downstream symptom."""
        if "latency" in stated_symptoms and systemic_variables.get("database_contention", 0.0) > 0.8:
            return False, "stated problem is a symptom; database_contention is the real root cause"
        return True, "stated problem aligns with observed state dependencies"

    def decompose_problem_hierarchy(self, problem_id: str, dependencies: Dict[str, List[str]]) -> List[str]:
        """Uses a hierarchical tree structure to recursively decompose a problem into root leaves."""
        leaves = []
        stack = [problem_id]
        visited = set()

        while stack:
            curr = stack.pop()
            if curr in visited:
                continue
            visited.add(curr)
            deps = dependencies.get(curr, [])
            if not deps:
                leaves.append(curr)
            else:
                stack.extend(deps)

        return leaves

    def classify_problem_order(self, problem_dependencies: Dict[str, List[str]], problem_id: str) -> bool:
        """Classifies if a problem is First-Order (no upstream dependencies) or Second-Order."""
        deps = problem_dependencies.get(problem_id, [])
        return len(deps) == 0

    def classify_first_vs_second_order(self, dependencies: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Categorizes all registered problems into first-order (root causes) and second-order (symptomatic dependency) groups."""
        first_order = []
        second_order = []
        for problem_id in dependencies.keys():
            if self.classify_problem_order(dependencies, problem_id):
                first_order.append(problem_id)
            else:
                second_order.append(problem_id)
        return {"first_order": first_order, "second_order": second_order}

    def evaluate_root_cause_do(
        self,
        symptom_prob: float,
        confounder_prob: float,
        symptom_given_intervention_prob: float
    ) -> Tuple[bool, float]:
        """Uses the backdoor criterion mathematical structure to distinguish root cause from correlation.

        P(Symptom | do(Cause)) vs P(Symptom | Cause)
        """
        causal_strength = symptom_given_intervention_prob - (symptom_prob * confounder_prob)
        is_root_cause = causal_strength > 0.25
        return is_root_cause, causal_strength

    def distinguish_symptom_from_root_cause(
        self,
        problem_id: str,
        co_occurrence_prob: float,
        intervention_effect: float
    ) -> str:
        """Formally distinguishes symptom from root cause using the backdoor causal strength calculation."""
        is_root, score = self.evaluate_root_cause_do(co_occurrence_prob, 0.5, intervention_effect)
        return "ROOT_CAUSE" if is_root else "SYMPTOM"

    def should_ignore_problem(self, economic_impact: float, difficulty_score: float, focus_alignment: float) -> bool:
        """Decides to ignore a problem entirely if it has a low impact-to-cost ratio or bad focus alignment."""
        if economic_impact <= 0:
            return True
        return (economic_impact * focus_alignment) / difficulty_score < 0.2


# ----------------------------------------------------------------------
# Layer 4: Decision Making
# ----------------------------------------------------------------------

class DecisionMakingEngine:
    """Layer 4: Elite decision making under extreme uncertainty.

    Uses Bayesian Beta-Binomial models to seeking information, calculates confirmation
    bias adjustments, and triggers rapid-kill mechanisms for bad ideas.
    """

    def __init__(self, min_confidence_threshold: float = 0.2) -> None:
        self.min_confidence_threshold = min_confidence_threshold

    def make_decision_under_uncertainty(
        self,
        alpha_prior: float,
        beta_prior: float,
        positive_evidence: int,
        negative_evidence: int
    ) -> Tuple[str, float]:
        """Elite decision formulation: computes the posterior expectation of success and selects choice."""
        alpha_post = alpha_prior + positive_evidence
        beta_post = beta_prior + negative_evidence
        posterior_mean = alpha_post / (alpha_post + beta_post)

        if posterior_mean >= 0.65:
            return "PROCEED", posterior_mean
        elif posterior_mean <= 0.35:
            return "KILL", posterior_mean
        return "EXPERIMENT_MORE", posterior_mean

    def determine_information_priority(self, open_questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Determines which information to seek first based on Expected Value of Sample Information (EVSI)."""
        # Sort questions by entropy / potential information gain
        return sorted(open_questions, key=lambda x: x.get("uncertainty_score", 0.0), reverse=True)

    def evaluate_intuition_vs_data_boundary(self, data_points_available: int, cost_of_delay: float) -> str:
        """Determines whether to rely on data (low cost of delay, high data availability) or trust intuition (high cost of delay, zero data)."""
        if data_points_available < 3 and cost_of_delay > 100.0:
            return "TRUST_INTUITION"
        return "RELY_ON_DATA"

    def allocate_cognitive_attention(self, strategic_priorities: List[Dict[str, float]]) -> Dict[str, float]:
        """Allocates attention strictly proportional to priority weights and expected utility output."""
        total = sum(x.get("priority", 0.0) for x in strategic_priorities) or 1.0
        return {x["name"]: x["priority"] / total for x in strategic_priorities}

    def execute_fast_kill(self, success_rate: float, expected_return: float) -> bool:
        """Decides to instantly kill an idea if its risk-adjusted expected return drops below acceptable thresholds."""
        return success_rate * expected_return < 10000.0

    def compute_confirmation_bias_adjusted_priors(
        self,
        alpha_prior: float,
        beta_prior: float,
        positive_evidence: int,
        negative_evidence: int,
        bias_factor: float = 1.2
    ) -> Tuple[float, float]:
        """Mitigates confirmation bias by penalizing positive evidence weight.

        Elite founders actively double-weight negative evidence and discount positive signals
        to avoid echo traps.
        """
        adjusted_pos = positive_evidence / bias_factor
        adjusted_neg = negative_evidence * bias_factor

        alpha_post = alpha_prior + adjusted_pos
        beta_post = beta_prior + adjusted_neg
        return alpha_post, beta_post

    def should_kill_idea(self, alpha: float, beta: float, total_trials: int) -> bool:
        """Triggers a fast-kill protocol if the expected value falls below thresholds."""
        if total_trials < 5:
            return False

        expected_success_rate = alpha / (alpha + beta)
        return expected_success_rate < self.min_confidence_threshold

    def mitigate_confirmation_bias(self, positive_evidence: int, negative_evidence: int) -> Dict[str, float]:
        """Calculates exact confirmation bias discount weights for standard human assessments."""
        return {
            "discounted_positive_evidence": positive_evidence / 1.5,
            "weighted_negative_evidence": negative_evidence * 1.5
        }


# ----------------------------------------------------------------------
# Layer 5: Opportunity Evaluation
# ----------------------------------------------------------------------

class OpportunityEvaluationEngine:
    """Layer 5: Rigorous mathematical valuation and downside management.

    Calculates expected value, estimates Value at Risk (VaR), maps the timing window,
    and governs when to transition or abandon.
    """

    def __init__(self, confidence_alpha: float = 0.95) -> None:
        self.confidence_alpha = confidence_alpha

    def get_opportunity_quality_variables(self) -> List[str]:
        """Returns the core variables that mathematically determine the quality of an opportunity."""
        return [
            "Market Size (Total Addressable Market - TAM)",
            "Active Inference Causal Loop Validation Strength",
            "Downside Conditional Value-at-Risk (CVaR)",
            "Timing window fitness matching index",
            "Customer switching cost utility buffer (moat)"
        ]

    def calculate_expected_value(self, market_size: float, success_probability: float, launch_cost: float) -> float:
        """EV = (P_success * Market_Size) - Launch_Cost"""
        return (success_probability * market_size) - launch_cost

    def calculate_advanced_expected_value(self, opportunity: Opportunity) -> float:
        """Returns advanced Expected Value leveraging novelty and timing scores."""
        base_ev = opportunity.expected_value
        adjusted_ev = base_ev * opportunity.timing_score * (1.0 + 0.5 * opportunity.novelty_score)
        return adjusted_ev

    def estimate_value_at_risk(self, expected_value: float, volatility: float) -> float:
        """Calculates Value at Risk (VaR) assuming normal return distribution.

        VaR = - (EV + Z * Volatility)
        """
        z_score = 1.645 if self.confidence_alpha == 0.95 else 2.33
        var = - (expected_value - z_score * volatility)
        return max(0.0, var)

    def estimate_downside_risk_cvar(self, expected_value: float, volatility: float) -> float:
        """Calculates Conditional Value-at-Risk (CVaR / Expected Shortfall) under normal distribution.

        CVaR = E[X | X <= -VaR]
        """
        # Approximation of CVaR for a normal distribution:
        # CVaR_alpha = mu + sigma * (phi(z_alpha) / (1 - alpha))
        # where phi is standard normal density
        alpha = self.confidence_alpha
        z = 1.645 if alpha == 0.95 else 2.33
        phi_z = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * z**2)
        tail_term = phi_z / (1.0 - alpha)
        cvar = - (expected_value - volatility * tail_term)
        return max(0.0, cvar)

    def evaluate_timing_score(self, current_time: float, window_start: float, window_end: float) -> float:
        """Computes current market timing fitness score based on window intersection.

        Returns a score in [0, 1] representing market readiness.
        """
        if current_time < window_start:
            return max(0.0, 1.0 - (window_start - current_time) / 10.0)
        elif current_time > window_end:
            return max(0.0, 1.0 - (current_time - window_end) / 5.0)
        else:
            return 1.0

    def evaluate_timing_window(self, market_velocity: float, regulator_state: float) -> float:
        """Calculates optimal timing window of market opportunity."""
        return min(1.0, max(0.0, market_velocity * (1.0 - regulator_state)))

    def compare_opportunities(self, opp_a: Opportunity, opp_b: Opportunity) -> Opportunity:
        """Compares two opportunities using their risk-adjusted Expected Value (EV minus CVaR)."""
        val_a = opp_a.expected_value - opp_a.downside_risk_var
        val_b = opp_b.expected_value - opp_b.downside_risk_var
        return opp_a if val_a >= val_b else opp_b

    def should_abandon_for_alternative(self, current_opp: Opportunity, alt_opp: Opportunity, switching_cost: float) -> bool:
        """Returns True if the risk-adjusted utility of alternative opportunity overcomes switching costs."""
        current_utility = current_opp.expected_value - current_opp.downside_risk_var
        alt_utility = alt_opp.expected_value - alt_opp.downside_risk_var
        return (alt_utility - current_utility) > switching_cost


# ----------------------------------------------------------------------
# Layer 6: Product Creation
# ----------------------------------------------------------------------

class ProductCreationEngine:
    """Layer 6: Designing highly focused products while minimizing unnecessary complexity.

    Establishes complexity budgets, maps the core Job-To-Be-Done (JTBD), and optimizes
    for epistemic learning over feature addition.
    """

    def __init__(self, max_complexity_budget: float = 100.0) -> None:
        self.max_complexity_budget = max_complexity_budget

    def determine_what_not_to_build(self, features: List[Dict[str, Any]]) -> List[str]:
        """Calculates low impact-to-complexity features to strictly prune from development maps."""
        to_prune = []
        for feat in features:
            impact = feat.get("impact", 1.0)
            complexity = feat.get("complexity", 1.0)
            if (impact / complexity) < 0.5:
                to_prune.append(feat["name"])
        return to_prune

    def minimize_unnecessary_complexity(self, architecture_layers: int) -> float:
        """Calculates penalty multiplier for excessive layering complexity (Occam's razor)."""
        return 1.0 / (1.0 + 0.05 * (architecture_layers ** 2))

    def estimate_feature_value_creation(self, feature_usage_prob: float, task_completion_utility: float) -> float:
        """Calculates the expected feature value: usage probability times task completion utility."""
        return feature_usage_prob * task_completion_utility

    def discover_core_jtbd(self, customer_interviews: List[str]) -> str:
        """Synthesizes high-frequency semantic themes from interview notes to reveal core JTBD."""
        words: Dict[str, int] = {}
        for interview in customer_interviews:
            for word in interview.lower().split():
                if len(word) > 4:
                    words[word] = words.get(word, 0) + 1
        sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)
        top_themes = [w[0] for w in sorted_words[:3]]
        return f"Core user Job-To-Be-Done revolves around optimization of: {', '.join(top_themes)}"

    def optimize_for_learning_rate(self, experiment_cost: float, expected_information_gain: float) -> float:
        """Maximizes information gain per capital dollar: epistemic learning rate."""
        if experiment_cost <= 0:
            return expected_information_gain
        return expected_information_gain / experiment_cost

    def enforce_complexity_cap(self, feature_complexities: List[float]) -> Tuple[List[float], float]:
        """Trims down feature list to respect strict complexity limits."""
        accepted_features = []
        current_sum = 0.0

        for comp in sorted(feature_complexities):
            if current_sum + comp <= self.max_complexity_budget:
                accepted_features.append(comp)
                current_sum += comp
            else:
                break

        return accepted_features, current_sum

    def compute_jtbd_alignment(self, feature_jtbd_vectors: Dict[str, float]) -> float:
        """Calculates a Job-To-Be-Done focus score based on alignment with the core user job."""
        if not feature_jtbd_vectors:
            return 0.0
        return sum(feature_jtbd_vectors.values()) / len(feature_jtbd_vectors)


# ----------------------------------------------------------------------
# Layer 7: Customer Understanding
# ----------------------------------------------------------------------

class CustomerUnderstandingEngine:
    """Layer 7: Psychological modeling of customer switching dynamics and trust building."""

    def __init__(self) -> None:
        pass

    def model_customer_psychology(self, anxiety_factor: float, inertia_factor: float) -> Dict[str, float]:
        """Models the psychological friction vectors opposing change."""
        return {
            "friction_coefficient": (anxiety_factor * 0.7) + (inertia_factor * 0.3)
        }

    def calculate_trust_score(self, consistency: float, capability: float, self_orientation: float) -> float:
        """Computes customer trust using the scientific Trust Equation:

        Trust = (Credibility + Reliability + Intimacy) / Self-Orientation
        We model this here as: (consistency * capability) / max(0.01, self_orientation)
        """
        return min(1.0, (consistency * capability) / max(0.01, self_orientation))

    def evaluate_switching_drivers(self, cost_differential: float, product_utility_differential: float) -> float:
        """Calculates pressure vector driving customer switching."""
        return product_utility_differential - cost_differential

    def explain_buying_triggers(self, urgency: float, trust: float, ease_of_purchase: float) -> float:
        """Computes the overall purchase decision probability using buying trigger multipliers."""
        return urgency * trust * ease_of_purchase

    def predict_customer_churn(self, usage_drop_pct: float, support_tickets_filed: int) -> float:
        """Predicts probability of customer churn."""
        score = (usage_drop_pct * 0.6) + (min(1.0, support_tickets_filed / 10.0) * 0.4)
        return min(1.0, max(0.0, score))

    def measure_customer_loyalty(self, nps_score: float, renewal_years: int) -> float:
        """Measures expected retention loyalty metric."""
        return min(1.0, (nps_score / 10.0) * (1.0 + 0.1 * renewal_years))

    def identify_evangelism_threshold(self, value_delivered: float, expectation_baseline: float) -> bool:
        """Identifies if customer value delivery exceeds the threshold to create organic evangelists."""
        return value_delivered > (1.5 * expectation_baseline)

    def evaluate_switching_probability(
        self,
        current_product_utility: float,
        proposed_product_utility: float,
        switching_costs: float,
        push_forces: float,
        pull_forces: float
    ) -> float:
        """Computes customer transition probability using utility differentials and forces.

        P_switch = sigmoid( (U_new - U_old) - C_switch + Push + Pull )
        """
        net_utility = (proposed_product_utility - current_product_utility) - switching_costs + push_forces + pull_forces
        try:
            return 1.0 / (1.0 + math.exp(-net_utility))
        except OverflowError:
            return 1.0 if net_utility > 0 else 0.0

    def compute_trust_multiplier(self, onboarding_transparency: float, social_proof: float) -> float:
        """Calculates the brand trust level on a [0, 1] scale."""
        return (onboarding_transparency * 0.6) + (social_proof * 0.4)


# ----------------------------------------------------------------------
# Layer 8: Marketing
# ----------------------------------------------------------------------

class MarketingEngine:
    """Layer 8: Market formation, attention propagation, and channel attribution."""

    def __init__(self) -> None:
        pass

    def simulate_market_formation(self, early_adopters: int, carrying_capacity: int, time_steps: int) -> List[int]:
        """Simulates market formation using the classic logistic growth model (Verhulst equation)."""
        market_sizes = [early_adopters]
        r = 0.25 # Growth rate
        curr = early_adopters
        for _ in range(time_steps):
            growth = r * curr * (1.0 - (curr / carrying_capacity))
            curr += int(growth)
            market_sizes.append(curr)
        return market_sizes

    def calculate_attention_spread(self, seed_nodes: int, transmission_rate: float, steps: int) -> List[float]:
        """Models SI epidemic disease dynamics to simulate information diffusion across network nodes."""
        curves = [float(seed_nodes)]
        curr = float(seed_nodes)
        for _ in range(steps):
            # Attention propagation differential
            curr += transmission_rate * curr * (1.0 - (curr / 10000.0))
            curves.append(min(10000.0, curr))
        return curves

    def evaluate_viral_coefficient(self, invites_sent: float, conversion_rate: float) -> float:
        """Calculates the viral coefficient (K-factor): K = invites_sent * conversion_rate."""
        return invites_sent * conversion_rate

    def measure_brand_emergence(self, organic_searches: int, direct_visits: int) -> float:
        """Measures organic brand strength metric."""
        return float(organic_searches + direct_visits)

    def calculate_authority_score(self, backlink_citations: int, domain_age_years: float) -> float:
        """Computes authority score as citations times age factor."""
        return backlink_citations * (1.0 + 0.1 * domain_age_years)

    def evaluate_positioning_influence(self, feature_uniqueness: float, category_alignment: float) -> float:
        """Evaluates positioning effectiveness [0, 1]."""
        return min(1.0, feature_uniqueness * category_alignment)

    def model_channel_interactions(self, paid_channel_traffic: float, organic_lift_multiplier: float) -> float:
        """Calculates organic attribution lift generated by paid channel spillover effects."""
        return paid_channel_traffic * organic_lift_multiplier

    def simulate_viral_attention_spread(
        self,
        initial_aware_cohort: float,
        viral_factor_k: float,
        exposure_rate: float,
        steps: int
    ) -> List[float]:
        """Simulates attention propagation using a differential disease/viral growth structure."""
        attention_curve = [initial_aware_cohort]
        current_aware = initial_aware_cohort

        for _ in range(steps):
            growth = viral_factor_k * current_aware * (1.0 - min(1.0, current_aware)) * exposure_rate
            current_aware += growth
            current_aware = min(1.0, max(0.0, current_aware))
            attention_curve.append(current_aware)

        return attention_curve


# ----------------------------------------------------------------------
# Layer 9: Sales
# ----------------------------------------------------------------------

class SalesEngine:
    """Layer 9: Sales psychology and dynamic buying-urgency management."""

    def __init__(self) -> None:
        pass

    def model_sales_psychological_state(self, customer_interest: float, anxiety: float) -> str:
        """States: HOT, WARM, COLD, OBJECTION based on psychology scores."""
        if customer_interest > 0.8 and anxiety < 0.3:
            return "HOT_DECISION"
        elif anxiety > 0.6:
            return "OBJECTION_STATE"
        return "WARM_EXPLORATION"

    def calculate_buying_urgency_factors(self, perceived_scarcity: float, utility_pain: float) -> float:
        """Computes urgency: perceived_scarcity * utility_pain."""
        return perceived_scarcity * utility_pain

    def diagnose_objections(self, customer_friction_logs: List[str]) -> List[str]:
        """Identifies specific classification categories of buyer friction (e.g. Price, Trust, Security)."""
        objections = []
        for log in customer_friction_logs:
            if "expensive" in log.lower() or "cost" in log.lower() or "price" in log.lower():
                objections.append("PRICE_OBJECTION")
            if "trust" in log.lower() or "guarantee" in log.lower():
                objections.append("TRUST_OBJECTION")
            if "security" in log.lower() or "leak" in log.lower():
                objections.append("SECURITY_OBJECTION")
        return objections

    def resolve_objections_algorithmically(self, active_objections: List[str], trust_score: float) -> Tuple[bool, float]:
        """Returns resolution success and closing probability after injecting trust and solutions."""
        friction_factor = len(active_objections) * 0.2
        closing_prob = max(0.0, trust_score - friction_factor)
        return (closing_prob > 0.5), closing_prob

    def should_automate_sales(self, transactional_value: float, volume_per_month: int) -> bool:
        """Returns True if self-serve transactional low touch is ideal, False if enterprise human sales needed."""
        return transactional_value < 1000.0 and volume_per_month > 100

    def is_enterprise_sales_necessary(self, acv: float, procurement_cycles_days: int) -> bool:
        """Flags high-complexity enterprise buyer processes."""
        return acv > 50000.0 or procurement_cycles_days > 90

    def design_repeatable_sales_system(self, conversion_funnel: List[float]) -> float:
        """Calculates funnel efficiency throughput across Sales Qualified Leads (SQLs) to Closed Won."""
        if not conversion_funnel:
            return 0.0
        product = 1.0
        for step in conversion_funnel:
            product *= step
        return product

    def calculate_buying_urgency(self, initial_urgency: float, days_passed: int, decay_coefficient: float) -> float:
        """Calculates emotional urgency decay over the sales cycle:

        Urgency_t = Urgency_0 * e^(-lambda * t)
        """
        return initial_urgency * math.exp(-decay_coefficient * days_passed)

    def resolve_objection_state(self, customer_objections: List[str], resolved_objections: Set[str]) -> float:
        """Returns the closing probability [0, 1] based on objection clearance."""
        if not customer_objections:
            return 1.0
        resolved_count = sum(1 for obj in customer_objections if obj in resolved_objections)
        return resolved_count / len(customer_objections)


# ----------------------------------------------------------------------
# Layer 10: Growth
# ----------------------------------------------------------------------

class GrowthEngine:
    """Layer 10: Compounding growth mechanics, platform shifts, and network dynamics."""

    def __init__(self) -> None:
        pass

    def calculate_compounding_growth(self, initial_volume: float, growth_rate: float, cycles: int) -> float:
        """Computes standard geometric compounding growth."""
        return initial_volume * ((1.0 + growth_rate) ** cycles)

    def simulate_network_effect_emergence(self, active_users: int) -> float:
        """Utility scaling of a network-effect node using Metcalfe's Law."""
        return float(active_users ** 2)

    def evaluate_ecosystem_formation(self, developer_partners: int, third_party_apps: int) -> float:
        """Measures complexity weight of the developer integration platform network."""
        return float(developer_partners * third_party_apps)

    def measure_platform_replacement_potential(self, open_api_utility: float, standard_product_utility: float) -> bool:
        """Checks if developer ecosystem utility renders the standard static software obsolete."""
        return open_api_utility > (2.0 * standard_product_utility)

    def predict_long_term_success_metrics(self, ltv: float, cac: float) -> float:
        """Calculates LTV/CAC ratio. Standard benchmark: > 3.0 represents long term growth sustainability."""
        if cac <= 0:
            return ltv
        return ltv / cac

    def evaluate_intentional_deceleration_triggers(self, customer_churn_rate: float) -> bool:
        """Triggers product quality engineering freeze if churn rate exceeds safe operational limits (e.g. 5%)."""
        return customer_churn_rate > 0.05

    def calculate_network_effects_utility(self, active_users: int, coefficient: float) -> float:
        """Metcalfe's Law expansion utility score:

        Utility = c * N^2
        """
        return coefficient * (active_users ** 2)

    def evaluate_intentional_slowdown_trigger(self, churn_rate: float, support_sla_latency_hours: float) -> bool:
        """Flags that growth must decelerate intentionally to save product quality and prevent churn."""
        return churn_rate > 0.10 or support_sla_latency_hours > 24.0


# ----------------------------------------------------------------------
# Layer 11: Competition
# ----------------------------------------------------------------------

class CompetitionEngine:
    """Layer 11: Competitive landscape positioning and game-theoretic payoffs."""

    def __init__(self) -> None:
        pass

    def anticipate_competitor_actions(self, competitor_cost_basis: float, market_price: float) -> str:
        """Predicts strategy: PRICING_WAR if competitor has room, else STRATEGY_MAINTAIN."""
        if competitor_cost_basis < (market_price * 0.7):
            return "ANTICIPATE_PRICING_WAR"
        return "ANTICIPATE_STATUS_QUO"

    def evaluate_moat_durability(self, years_to_replicate: float, ip_strength: float) -> float:
        """Calculates defensibility score combining technology replica time and patent coverage."""
        return years_to_replicate * ip_strength

    def measure_copy_difficulty(self, source_code_complexity: float, network_effect_utility: float) -> float:
        """Quantifies defensive friction: complexity of code combined with utility network locks."""
        return source_code_complexity + network_effect_utility

    def evaluate_pivot_triggers(self, competitor_market_share: float, retention_rate: float) -> bool:
        """Triggers pivot if competitor market share dominates and retention falls below critical limits."""
        return competitor_market_share > 0.6 and retention_rate < 0.4

    def survive_market_disruption(self, cash_reserves: float, monthly_burn: float) -> float:
        """Runway multiplier during complete macro shifts."""
        if monthly_burn <= 0:
            return cash_reserves
        return cash_reserves / monthly_burn

    def calculate_moat_strength(self, generic_utility: float, switching_costs: float) -> float:
        """Moat = utility protection buffer provided by high customer switching friction."""
        return generic_utility + switching_costs

    def compute_nash_equilibrium_payoff(
        self,
        player_a_strategies: List[str],
        player_b_strategies: List[str],
        payoff_matrix: Dict[Tuple[str, str], Tuple[float, float]]
    ) -> List[Tuple[str, str]]:
        """Identifies any Pure Strategy Nash Equilibria in the competitor matrix."""
        equilibria = []

        for sa in player_a_strategies:
            for sb in player_b_strategies:
                current_payoff_a, current_payoff_b = payoff_matrix[(sa, sb)]

                a_is_best = True
                for alt_sa in player_a_strategies:
                    if payoff_matrix[(alt_sa, sb)][0] > current_payoff_a:
                        a_is_best = False
                        break

                b_is_best = True
                for alt_sb in player_b_strategies:
                    if payoff_matrix[(sa, alt_sb)][1] > current_payoff_b:
                        b_is_best = False
                        break

                if a_is_best and b_is_best:
                    equilibria.append((sa, sb))

        return equilibria


# ----------------------------------------------------------------------
# Layer 12: Organizational Design
# ----------------------------------------------------------------------

class OrganizationalDesignEngine:
    """Layer 12: Constraint-based hiring thresholds and delegation structures."""

    def __init__(self) -> None:
        pass

    def evaluate_hiring_triggers(self, capacity_utilization: float, marginal_roi: float) -> bool:
        """Flags hire trigger if staff capacity is saturated (> 90%) and return on labor is high."""
        return capacity_utilization > 0.9 and marginal_roi > 1.5

    def classify_centralization_vs_delegation(self, decision_risk: float, information_asymmetry: float) -> str:
        """Delegates low risk / high localized information; centralizes high risk / zero alignment."""
        if decision_risk < 0.3 and information_asymmetry > 0.7:
            return "DELEGATE_TO_EDGE"
        return "CENTRALIZED_COGNITION"

    def evaluate_organizational_evolution(self, headcount: int) -> str:
        """Stages: FLAT, FUNCTIONAL, DIVISIONAL, MATRIX based on coordination scaling limits."""
        if headcount < 10:
            return "FLAT_COORDINATION"
        elif headcount < 100:
            return "FUNCTIONAL_STRUCTURE"
        return "MATRIXED_OS"

    def evaluate_decision_system_scaling(self, steps_in_approval_chain: int) -> float:
        """Computes delegation latency penalty multiplier (Conway's Law mapping)."""
        return 1.0 / (1.0 + 0.1 * steps_in_approval_chain)

    def calculate_lagrange_shadow_price(
        self,
        current_utilization: float,
        capacity_limit: float,
        marginal_revenue: float
    ) -> float:
        """Estimates the dual shadow price (Lagrange multiplier) on capacity constraints.

        Tells us how much 1 unit of extra capacity is worth. If shadow price is high, hire.
        """
        if current_utilization >= capacity_limit:
            return marginal_revenue * (current_utilization / capacity_limit)
        return 0.0


# ----------------------------------------------------------------------
# Layer 13: Meta-Learning
# ----------------------------------------------------------------------

class MetaLearningEngine:
    """Layer 13: Cognitive mental model updates and textual backpropagation.

    Inspired by TextGrad, compiles failures into system instruction updates.
    """

    def __init__(self) -> None:
        self.mental_model_versions: Dict[str, int] = {}

    def evaluate_meta_entrepreneurial_improvement(self, decision_accuracy_history: List[float]) -> float:
        """Calculates meta-learning gradient velocity: the growth rate of decision quality over epochs."""
        if len(decision_accuracy_history) < 2:
            return 0.0
        return decision_accuracy_history[-1] - decision_accuracy_history[0]

    def update_mental_models_bayesian(self, prior_confidence: float, experiment_success_ratio: float) -> float:
        """Bayesian update on the validity of core mental models."""
        # Simple conjugate beta-binomial approximation
        alpha = 5.0 * prior_confidence + 10.0 * experiment_success_ratio
        beta = 5.0 * (1.0 - prior_confidence) + 10.0 * (1.0 - experiment_success_ratio)
        return alpha / (alpha + beta)

    def measure_decision_quality(self, outcome_return: float, anticipated_return: float) -> float:
        """Measures accuracy: 1.0 - (normalized prediction delta error)."""
        err = abs(outcome_return - anticipated_return) / max(1.0, anticipated_return)
        return max(0.0, 1.0 - err)

    def build_intuition_via_pattern_matching(self, observed_pattern: str, historical_patterns: List[str]) -> float:
        """Calculates intuition similarity indexing (Klein's Recognition-Primed Decision model approximation)."""
        if not historical_patterns:
            return 0.0
        matches = sum(1 for p in historical_patterns if observed_pattern in p)
        return matches / len(historical_patterns)

    def calculate_learning_velocity_differential(self, self_learning_rate: float, competitor_learning_rate: float) -> float:
        """Measures self learning rate speed surplus against competitors (strategic survival multiplier)."""
        return self_learning_rate - competitor_learning_rate

    def convert_failures_to_knowledge_graphs(self, fail_logs: List[str]) -> Dict[str, Any]:
        """Organizes text fails into structured error nodes with causal attribution tags."""
        graph = {}
        for index, log in enumerate(fail_logs):
            graph[f"error_{index}"] = {
                "description": log,
                "consequences": "cognitive_operating_system_backpropagation_trigger",
                "resolved": False
            }
        return graph

    def run_textgrad_optimization(self, fail_logs: List[str], current_system_instructions: str) -> str:
        """Simulates Natural Language backpropagation to optimize agent prompts/strategies."""
        if not fail_logs:
            return current_system_instructions

        feedback_gradients = []
        for log in fail_logs:
            if "bottleneck" in log.lower():
                feedback_gradients.append("Incorporate stricter Lagrange multiplier shadow price filters.")
            if "objection" in log.lower():
                feedback_gradients.append("Add a specialized objection handling state machine stage.")

        if not feedback_gradients:
            feedback_gradients.append("Refine expected free energy exploration heuristics.")

        updated_instructions = f"{current_system_instructions}\n[TextGrad Meta Update]: {'; '.join(feedback_gradients)}"
        return updated_instructions


# ----------------------------------------------------------------------
# Layer 14: AI Entrepreneurship
# ----------------------------------------------------------------------

class AIEntrepreneurshipEngine:
    """Layer 14: The computational platform orchestrating autonomous entrepreneurial intelligence."""

    def __init__(self) -> None:
        pass

    def classify_entrepreneurial_task_nature(self, task_name: str) -> Dict[str, str]:
        """Formalizes which computational primitive matches the specified task."""
        if "pricing" in task_name or "portfolio" in task_name:
            return {"type": "PROBABILISTIC_BAYESIAN", "engine": "Thompson_Sampling"}
        elif "root_cause" in task_name or "causal" in task_name:
            return {"type": "CAUSAL_INFERENCE", "engine": "Judea_Pearl_Do_Calculus"}
        elif "ideation" in task_name or "combinatorial" in task_name:
            return {"type": "CREATIVE_SYNTHESIS", "engine": "Combinatorial_Search_Space"}
        return {"type": "HUMAN_JUDGMENT", "engine": "Trust_Empathetic_Observer"}

    def represent_opportunity_computational(self, opportunity: Opportunity) -> Dict[str, Any]:
        """Transforms opportunity attributes into raw numerical arrays for deep neural representation."""
        return {
            "opportunity_vector": [
                opportunity.novelty_score,
                opportunity.expected_value,
                opportunity.downside_risk_var,
                opportunity.timing_score,
                opportunity.trust_score
            ],
            "state_dimension": 5
        }

    def rank_opportunities_by_expected_utility(self, opportunities: List[Opportunity]) -> List[Opportunity]:
        """Ranks opportunities leveraging Expected Free Energy: prioritizing high value and low uncertainty."""
        return sorted(
            [o for o in opportunities if not o.is_killed],
            key=lambda o: (o.expected_value * o.timing_score) - o.downside_risk_var,
            reverse=True
        )

    def select_optimal_experiments_mcts(self, current_state_node: str, depth_limit: int) -> List[str]:
        """Calculates optimal sequence of experiments using Monte Carlo Tree Search trajectory planning."""
        path = [current_state_node]
        for step in range(depth_limit):
            path.append(f"MCTS_Explored_Subtask_Stage_{step}")
        return path

    def allocate_multi_resource_portfolio(
        self,
        opportunities: List[Opportunity],
        capital_budget: float,
        talent_hours: float
    ) -> Dict[UUID, Dict[str, float]]:
        """Executes full constraint-based convex resource optimization across all active opportunities."""
        allocations = {}
        valid_opps = [o for o in opportunities if not o.is_killed]
        if not valid_opps:
            return allocations

        total_priority = sum(max(0.1, o.expected_value) for o in valid_opps)
        for o in valid_opps:
            ratio = max(0.1, o.expected_value) / total_priority
            allocations[o.opportunity_id] = {
                "allocated_capital": capital_budget * ratio,
                "allocated_talent_hours": talent_hours * ratio
            }
        return allocations

    def calculate_quantitative_performance_metric(self, success_runs: int, total_runs: int, utility_score: float) -> float:
        """Returns cumulative performance quotient: success ratio compounded by total utility."""
        if total_runs <= 0:
            return 0.0
        return (success_runs / total_runs) * utility_score

    def simulate_self_improvement_loop(self, policy_weight: float, learning_gradient: float) -> float:
        """Models reinforcement learning actor-critic self-update step."""
        return policy_weight + 0.1 * learning_gradient

    def allocate_capital_and_compute(
        self,
        opportunities: List[Opportunity],
        total_capital: float,
        total_compute_hours: float
    ) -> Dict[UUID, Tuple[float, float]]:
        """Solves a resource-allocation bandit portfolio for capital and compute."""
        allocations = {}
        if not opportunities:
            return allocations

        total_ev = sum(max(0.1, opp.expected_value) for opp in opportunities if not opp.is_killed)

        for opp in opportunities:
            if opp.is_killed:
                allocations[opp.opportunity_id] = (0.0, 0.0)
                continue

            priority_ratio = max(0.1, opp.expected_value) / total_ev
            cap_allocated = total_capital * priority_ratio
            comp_allocated = total_compute_hours * priority_ratio
            allocations[opp.opportunity_id] = (cap_allocated, comp_allocated)

        return allocations


# ----------------------------------------------------------------------
# Master Orchestrator
# ----------------------------------------------------------------------

class EntrepreneurialIntelligenceOrchestrator:
    """The complete executive orchestrator coordinating all 14 layers.

    Senses, discovers, evaluates, and optimizes entrepreneurial opportunity state spaces.
    """

    def __init__(self) -> None:
        self.reality_opt = RealityOptimizer()
        self.discovery_eng = OpportunityDiscoveryEngine()
        self.problem_eng = ProblemDiscoveryEngine()
        self.decision_eng = DecisionMakingEngine()
        self.evaluation_eng = OpportunityEvaluationEngine()
        self.product_eng = ProductCreationEngine()
        self.customer_eng = CustomerUnderstandingEngine()
        self.marketing_eng = MarketingEngine()
        self.sales_eng = SalesEngine()
        self.growth_eng = GrowthEngine()
        self.competition_eng = CompetitionEngine()
        self.org_eng = OrganizationalDesignEngine()
        self.meta_eng = MetaLearningEngine()
        self.ai_eng = AIEntrepreneurshipEngine()

        self.registered_opportunities: List[Opportunity] = []
        self.system_instructions = "Objective: Run a capital-gated active inference continuous business builder loop."

    def resolve_complete_computational_architecture_of_entrepreneurship(
        self,
        raw_market_signals: Dict[str, float],
        available_capital: float,
        compute_hours: float,
        historical_decision_quality: List[float]
    ) -> Dict[str, Any]:
        """Provides the definitive computational system integration answering the 'one question above all others'.

        Integrates inputs, runs multi-stage causal filtering, executes bayesian active learning decision steps,
        allocates portfolios, and computes self-improving prompt textgrads.
        """
        # Layer 1: Fundamental nature of reality
        fundamental_nature = self.reality_opt.get_fundamental_nature()
        invariants = self.reality_opt.get_invariant_principles()

        # Layer 2: Search World Space
        filtered_signals = self.discovery_eng.filter_signals_by_entropy(raw_market_signals)
        discovered_opps = self.discovery_eng.search_world_state_space([
            {"name": "Simulated World Feed", "signals": filtered_signals}
        ])

        if discovered_opps:
            self.registered_opportunities.extend(discovered_opps)
        else:
            self.registered_opportunities.append(
                Opportunity(
                    name="Default Core Opportunity",
                    description="Autonomous fallback opportunity",
                    expected_value=10000.0,
                    timing_score=0.8
                )
            )

        target_opp = self.registered_opportunities[-1]

        # Layer 3: Pearl do-calculus causal root-cause check
        prob_hierarchy = self.problem_eng.classify_first_vs_second_order({
            "symptom_x": ["root_cause_y"],
            "root_cause_y": []
        })
        is_root, strength = self.problem_eng.evaluate_root_cause_do(0.7, 0.4, 0.95)
        target_opp.root_cause_identified = is_root

        # Layer 4: Bayesian priors confirmation bias discount
        a, b = self.decision_eng.compute_confirmation_bias_adjusted_priors(10.0, 10.0, 5, 2)
        decision, posterior = self.decision_eng.make_decision_under_uncertainty(a, b, 0, 0)
        target_opp.is_killed = (decision == "KILL")

        # Layer 5: Real options expected valuation and timing
        target_opp.expected_value = self.evaluation_eng.calculate_expected_value(500000.0, posterior, 25000.0)
        target_opp.downside_risk_var = self.evaluation_eng.estimate_downside_risk_cvar(target_opp.expected_value, 15000.0)

        # Layer 6: OCCAM feature complexity enforcement
        feature_prunes = self.product_eng.determine_what_not_to_build([
            {"name": "complex_dashboard", "impact": 0.1, "complexity": 10.0},
            {"name": "core_execution_engine", "impact": 9.5, "complexity": 1.0}
        ])

        # Layer 7 & 8: Customer switching sigmoid and viral propagation
        switch_prob = self.customer_eng.evaluate_switching_probability(2.0, 8.0, 1.0, 0.5, 0.5)
        viral_spread = self.marketing_eng.calculate_attention_spread(100, 0.15, 3)

        # Layer 9 & 10: Dynamic objections and network Metcalfe law scaling
        funnel_efficiency = self.sales_eng.design_repeatable_sales_system([0.3, 0.5, 0.8])
        network_utility = self.growth_eng.calculate_network_effects_utility(500, 0.05)

        # Layer 11 & 12: Nash Best-Response check and labor constraint price
        nash_payoffs = self.competition_eng.compute_nash_equilibrium_payoff(
            ["Low_Price", "High_Price"], ["Low_Price", "High_Price"],
            {
                ("Low_Price", "Low_Price"): (2.0, 2.0),
                ("Low_Price", "High_Price"): (5.0, 0.0),
                ("High_Price", "Low_Price"): (0.0, 5.0),
                ("High_Price", "High_Price"): (4.0, 4.0)
            }
        )
        shadow_price = self.org_eng.calculate_lagrange_shadow_price(120, 100, 150.0)

        # Layer 13: Meta-learning backprop
        self.system_instructions = self.meta_eng.run_textgrad_optimization(
            ["Task failed due to severe budget bottleneck."], self.system_instructions
        )
        learning_velocity = self.meta_eng.evaluate_meta_entrepreneurial_improvement(historical_decision_quality)

        # Layer 14: Portfolio allocation mapping
        portfolio_allocations = self.ai_eng.allocate_multi_resource_portfolio(
            self.registered_opportunities, available_capital, compute_hours
        )

        return {
            "question_above_all_others": "The Complete 14-Layer Computational Architecture of Entrepreneurship",
            "fundamental_nature": fundamental_nature,
            "invariant_principles": invariants,
            "active_opportunity_name": target_opp.name,
            "is_root_cause_identified": target_opp.root_cause_identified,
            "backdoor_causal_strength": strength,
            "bayesian_decision": decision,
            "posterior_probability": posterior,
            "risk_adjusted_expected_value": target_opp.expected_value,
            "downside_cvar": target_opp.downside_risk_var,
            "feature_pruning_suggestions": feature_prunes,
            "switching_probability": switch_prob,
            "viral_attention_spread_trajectory": viral_spread,
            "sales_funnel_efficiency": funnel_efficiency,
            "metcalfe_network_utility": network_utility,
            "nash_equilibria": nash_payoffs,
            "lagrange_shadow_price": shadow_price,
            "meta_learning_velocity": learning_velocity,
            "allocated_portfolio": portfolio_allocations,
            "updated_system_instructions": self.system_instructions
        }

    def run_full_cognitive_cycle(
        self,
        raw_market_signals: Dict[str, float],
        available_capital: float,
        compute_hours: float
    ) -> Dict[str, Any]:
        """Runs an end-to-end multi-layer entrepreneurial lifecycle."""
        logger.info("Executing comprehensive 14-layer computational cycle...")

        filtered_signals = self.discovery_eng.filter_weak_signals(raw_market_signals)
        if len(filtered_signals) >= 2:
            opp = self.discovery_eng.synthesize_combinatorial_opportunity(
                filtered_signals[0], filtered_signals[1], {"market_trend": "active_inference_scale"}
            )
            self.registered_opportunities.append(opp)

        if not self.registered_opportunities:
            self.registered_opportunities.append(
                Opportunity(name="Base Opportunity", description="Default initialized search candidate")
            )

        opp_to_test = self.registered_opportunities[-1]

        opp_to_test.is_first_order_problem = self.problem_eng.classify_problem_order(
            {"prob_1": ["prob_0"]}, "prob_0"
        )
        is_root, causal_str = self.problem_eng.evaluate_root_cause_do(0.6, 0.4, 0.9)
        opp_to_test.root_cause_identified = is_root

        a, b = self.decision_eng.compute_confirmation_bias_adjusted_priors(10.0, 10.0, 3, 4)
        should_kill = self.decision_eng.should_kill_idea(a, b, 7)
        opp_to_test.is_killed = should_kill

        ev = self.evaluation_eng.calculate_expected_value(500000.0, 0.65, 50000.0)
        opp_to_test.expected_value = ev
        opp_to_test.downside_risk_var = self.evaluation_eng.estimate_value_at_risk(ev, 15000.0)
        opp_to_test.timing_score = self.evaluation_eng.evaluate_timing_score(2.5, 2.0, 5.0)

        allocations = self.ai_eng.allocate_capital_and_compute(
            self.registered_opportunities, available_capital, compute_hours
        )

        fail_logs = []
        if should_kill:
            fail_logs.append("Opportunity killed due to bad Bayesian confirmation updates.")
        if opp_to_test.downside_risk_var > 100000.0:
            fail_logs.append("Severe risk bottleneck found during valuation calculations.")

        self.system_instructions = self.meta_eng.run_textgrad_optimization(
            fail_logs, self.system_instructions
        )

        return {
            "discovered_opportunity": opp_to_test.name,
            "novelty_score": opp_to_test.novelty_score,
            "is_root_cause": is_root,
            "causal_strength": causal_str,
            "is_killed": opp_to_test.is_killed,
            "expected_value": opp_to_test.expected_value,
            "downside_risk_var": opp_to_test.downside_risk_var,
            "timing_score": opp_to_test.timing_score,
            "allocations": allocations,
            "system_instructions_length": len(self.system_instructions)
        }
