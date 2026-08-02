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


class ProblemDefinition(BaseModel):
    """Answers: How do they define a problem?

    Formalizes the structural, psychological, and economic components of a problem definition.
    """
    problem_id: UUID = Field(default_factory=uuid4)
    stated_symptom: str
    real_underlying_pain: str
    affected_user_segment: str
    economic_cost_of_inaction: float = Field(0.0)
    frequency_per_week: float = Field(0.0)
    severity_index: float = Field(0.5, ge=0.0, le=1.0)


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

    def map_automation_boundaries(self, task_name: str, complexity_score: float) -> Tuple[bool, str]:
        """Classifies task as fully automatable or human-only.

        Optimization tasks (pricing, routing, allocation) are automatable.
        Psychological high-empathy trust or zero-to-one vision remain human-bound.
        """
        if complexity_score < 0.4:
            return True, "AUTOMATABLE_DETERMINISTIC"

        # High complexity mathematical optimization is automatable
        if "pricing" in task_name.lower() or "allocation" in task_name.lower() or "portfolio" in task_name.lower():
            return True, "AUTOMATABLE_PROBABILISTIC"

        # Pure strategic zero-to-one vision or high-trust human networking
        if "trust" in task_name.lower() or "vision" in task_name.lower() or "empathy" in task_name.lower():
            return False, "HUMAN_PSYCHOLOGY_BOUND"

        return True, "AUTOMATABLE_AGENTIC"

    def get_invariant_principles(self) -> Dict[str, str]:
        """Answers: What invariant principles exist across every successful entrepreneur?

        Returns the mapped absolute baseline invariants of entrepreneurship.
        """
        return {
            "first_principles_thinking": "Reasoning from fundamental axioms rather than analogy.",
            "asymmetric_risk_return": "Searching for setups with finite downside and infinite/uncapped upside.",
            "epistemic_agility": "Rapidly updating beliefs in response to objective friction or market feedback.",
            "objection_liquidation": "Reframing structural and economic objections into collaborative alignments."
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
            # A signal is filtered out if amplitude is below our threshold
            if amplitude >= self.filter_threshold:
                valid_signals.append(signal_id)
        return valid_signals

    def synthesize_combinatorial_opportunity(
        self,
        signal_a: str,
        signal_b: str,
        world_context: Dict[str, Any]
    ) -> Opportunity:
        """Combines unrelated observations and weak signals to generate a novel opportunity."""
        name = f"Synthesis: {signal_a} + {signal_b}"
        desc = f"Synthesized opportunity from weak signals under context {world_context.get('market_trend', 'general')}"

        # Calculate novelty score as a function of the semantic distance between the signals
        # In a real system, this would use embedding distance; here we model it algebraically.
        dist = abs(len(signal_a) - len(signal_b)) / max(1, len(signal_a) + len(signal_b))
        novelty = min(0.99, max(0.1, dist * 2.0))

        return Opportunity(
            name=name,
            description=desc,
            weak_signals=[signal_a, signal_b],
            combined_observations=[signal_a, signal_b],
            novelty_score=novelty
        )

    def search_state_space(self, signals_database: Dict[str, float], world_context: Dict[str, Any]) -> List[Opportunity]:
        """Answers: How does an entrepreneur continuously search the world's state space?

        Performs a combinatorial state-space search to generate candidate Opportunities.
        """
        valid_signals = self.filter_weak_signals(signals_database)
        opportunities = []
        for i in range(len(valid_signals)):
            for j in range(i + 1, len(valid_signals)):
                opp = self.synthesize_combinatorial_opportunity(valid_signals[i], valid_signals[j], world_context)
                opportunities.append(opp)
        return opportunities

    def detect_weak_signals(self, signals: Dict[str, float], gain: float = 1.2) -> Dict[str, float]:
        """Answers: How are weak signals detected?

        Applies a non-linear gain multiplier to enhance low-amplitude signals.
        """
        boosted_signals = {}
        for k, v in signals.items():
            if v < self.filter_threshold:
                # Amplify weak signals close to the threshold using active signal gain
                boosted_signals[k] = min(1.0, v * gain)
            else:
                boosted_signals[k] = v
        return boosted_signals

    def evaluate_trend_relevance(self, signal_name: str, macro_trends: List[str]) -> float:
        """Answers: How do entrepreneurs know which trend matters?

        Computes semantic overlapping relevance of a signal against established macro trends.
        """
        if not macro_trends:
            return 0.0
        score = 0.0
        for trend in macro_trends:
            # Overlap coefficient or length matching as a deterministic heuristic
            shared_chars = len(set(signal_name.lower()) & set(trend.lower()))
            score += shared_chars / max(1, len(trend))
        return min(1.0, score / len(macro_trends))

    def predict_emerging_market(self, utility_trends: List[float], momentum_threshold: float = 0.1) -> bool:
        """Answers: How do they predict emerging markets before competitors?

        Analyzes consecutive acceleration/momentum in utility metrics to flag emerging markets.
        """
        if len(utility_trends) < 3:
            return False
        deltas = [utility_trends[i] - utility_trends[i-1] for i in range(1, len(utility_trends))]
        # Check if the rate of growth is accelerating
        acceleration = deltas[-1] - deltas[-2]
        return acceleration > momentum_threshold

    def is_invisible_opportunity(self, opportunity: Opportunity, competitor_focus_areas: Set[str]) -> bool:
        """Answers: What makes an opportunity invisible to everyone else?

        Flags an opportunity as invisible if its weak signals do not overlap with competitor focus.
        """
        for sig in opportunity.weak_signals:
            if any(focus in sig.lower() for focus in competitor_focus_areas):
                return False
        return opportunity.novelty_score > 0.6


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

    def classify_problem_order(self, problem_dependencies: Dict[str, List[str]], problem_id: str) -> bool:
        """Classifies if a problem is First-Order (no upstream dependencies) or Second-Order."""
        deps = problem_dependencies.get(problem_id, [])
        return len(deps) == 0

    def evaluate_root_cause_do(
        self,
        symptom_prob: float,
        confounder_prob: float,
        symptom_given_intervention_prob: float
    ) -> Tuple[bool, float]:
        """Uses the backdoor criterion mathematical structure to distinguish root cause from correlation.

        P(Symptom | do(Cause)) vs P(Symptom | Cause)
        """
        # If the post-interventional effect is significant, it indicates a strong causal root relationship
        causal_strength = symptom_given_intervention_prob - (symptom_prob * confounder_prob)
        is_root_cause = causal_strength > 0.25
        return is_root_cause, causal_strength

    def detect_stated_vs_real_problem(self, prob_def: ProblemDefinition) -> Tuple[bool, str]:
        """Answers: How do they know the stated problem isn't the real problem?

        Analyzes discrepancy and psychological mismatch between stated symptoms and underlying pain.
        """
        is_mismatch = prob_def.stated_symptom.lower().strip() != prob_def.real_underlying_pain.lower().strip()
        verdict = "MISMATCH_DETECTED" if is_mismatch else "SYMPTOM_ALIGNMENT"
        return is_mismatch, verdict

    def decompose_problem(self, problem_id: str, causal_graph: Dict[str, List[str]]) -> List[str]:
        """Answers: How do they decompose problems?

        Performs a topological or dependency BFS traversal to extract all sub-problems or root nodes.
        """
        visited = []
        queue = [problem_id]
        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.append(current)
                deps = causal_graph.get(current, [])
                for dep in deps:
                    if dep not in visited:
                        queue.append(dep)
        return visited

    def should_ignore_problem(self, prob_def: ProblemDefinition, min_cost_threshold: float = 1000.0) -> bool:
        """Answers: When should they ignore a problem entirely?

        Decides if a problem lacks sufficient economic density or severity to prioritize.
        """
        expected_annual_cost = prob_def.economic_cost_of_inaction * prob_def.frequency_per_week * 52.0
        return expected_annual_cost < min_cost_threshold or prob_def.severity_index < 0.2


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
        # Adjust positive evidence down, negative evidence up
        adjusted_pos = positive_evidence / bias_factor
        adjusted_neg = negative_evidence * bias_factor

        alpha_post = alpha_prior + adjusted_pos
        beta_post = beta_prior + adjusted_neg
        return alpha_post, beta_post

    def should_kill_idea(self, alpha: float, beta: float, total_trials: int) -> bool:
        """Triggers a fast-kill protocol if the expected value falls below thresholds."""
        if total_trials < 5:
            return False  # Give it some initial runway to learn

        expected_success_rate = alpha / (alpha + beta)
        return expected_success_rate < self.min_confidence_threshold

    def make_decision_under_uncertainty(self, options_ev: Dict[str, float], risk_variance: Dict[str, float], risk_aversion: float = 2.0) -> str:
        """Answers: How do elite founders make decisions under uncertainty?

        Applies Mean-Variance utility analysis under Prospect-style risk aversion to select the best option.
        """
        best_option = None
        max_utility = -float("inf")
        for opt, ev in options_ev.items():
            var = risk_variance.get(opt, 0.0)
            utility = ev - risk_aversion * var
            if utility > max_utility:
                max_utility = utility
                best_option = opt
        return best_option or ""

    def determine_information_seeking_priority(self, uncertainty_scores: Dict[str, float], cost_to_acquire: Dict[str, float]) -> List[str]:
        """Answers: What information do they seek first?

        Ranks information seeking based on high variance (uncertainty) per cost unit (Value of Information approximation).
        """
        priority = []
        for key, uncertainty in uncertainty_scores.items():
            cost = cost_to_acquire.get(key, 1.0)
            voi_heuristic = uncertainty / max(0.1, cost)
            priority.append((key, voi_heuristic))
        priority.sort(key=lambda x: x[1], reverse=True)
        return [p[0] for p in priority]

    def should_rely_on_intuition(self, domain_experience_years: float, domain_volatility_index: float) -> bool:
        """Answers: When do they trust intuition?

        Intuition is highly reliable ONLY in high-experience, low-to-medium chaotic environments.
        """
        return domain_experience_years >= 5.0 and domain_volatility_index < 0.7

    def should_rely_on_data(self, sample_size: int, p_value: float) -> bool:
        """Answers: When do they rely on data?

        Data should override intuition only if there is sufficient density and statistical significance.
        """
        return sample_size >= 30 and p_value <= 0.05

    def allocate_cognitive_attention(self, priority_tasks: Dict[str, float]) -> Dict[str, float]:
        """Answers: How do they allocate attention?

        Uses a Softmax function to distribute cognitive resources and attention non-linearly.
        """
        if not priority_tasks:
            return {}
        # Simple Softmax over priority values
        max_val = max(priority_tasks.values())
        exp_vals = {k: math.exp(v - max_val) for k, v in priority_tasks.items()}
        sum_exp = sum(exp_vals.values())
        return {k: round(v / sum_exp, 4) for k, v in exp_vals.items()}


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

    def calculate_expected_value(self, market_size: float, success_probability: float, launch_cost: float) -> float:
        """EV = (P_success * Market_Size) - Launch_Cost"""
        return (success_probability * market_size) - launch_cost

    def estimate_value_at_risk(self, expected_value: float, volatility: float) -> float:
        """Calculates Value at Risk (VaR) assuming normal return distribution.

        VaR = - (EV + Z * Volatility)
        """
        # Standard Z-score for 95% confidence is ~1.645
        z_score = 1.645 if self.confidence_alpha == 0.95 else 2.33
        var = - (expected_value - z_score * volatility)
        return max(0.0, var)

    def evaluate_timing_score(self, current_time: float, window_start: float, window_end: float) -> float:
        """Computes current market timing fitness score based on window intersection.

        Returns a score in [0, 1] representing market readiness.
        """
        if current_time < window_start:
            # Too early (emerging tech)
            return max(0.0, 1.0 - (window_start - current_time) / 10.0)
        elif current_time > window_end:
            # Too late (saturated market)
            return max(0.0, 1.0 - (current_time - window_end) / 5.0)
        else:
            # Optimal timing window
            return 1.0

    def evaluate_opportunity_quality_metrics(self, opp: Opportunity, margin: float, cap_efficiency: float) -> Dict[str, float]:
        """Answers: Which variables determine opportunity quality?

        Computes core operational and investment efficiency variables.
        """
        quality = (opp.expected_value * opp.timing_score * margin * cap_efficiency) / max(1.0, opp.downside_risk_var)
        return {
            "quality_index": quality,
            "margin": margin,
            "capital_efficiency": cap_efficiency,
            "downside_risk_ratio": opp.downside_risk_var / max(1.0, opp.expected_value)
        }

    def compare_opportunities(self, opp_a: Opportunity, opp_b: Opportunity) -> Opportunity:
        """Answers: How do they compare two opportunities?

        Compares opportunities based on expected value / Value-at-Risk ratio.
        """
        ratio_a = opp_a.expected_value / max(1.0, opp_a.downside_risk_var)
        ratio_b = opp_b.expected_value / max(1.0, opp_b.downside_risk_var)
        return opp_a if ratio_a >= ratio_b else opp_b

    def should_abandon_for_alternative(self, current_opp: Opportunity, alt_opp: Opportunity, transition_cost: float) -> bool:
        """Answers: When do they abandon one opportunity for another?

        Implements transition-cost gated decision boundary to abandon or persist.
        """
        current_net_ev = current_opp.expected_value - current_opp.downside_risk_var
        alt_net_ev = alt_opp.expected_value - alt_opp.downside_risk_var - transition_cost
        return alt_net_ev > current_net_ev


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
        # Alignment is average matching score across features
        return sum(feature_jtbd_vectors.values()) / len(feature_jtbd_vectors)

    def determine_excluded_features(self, all_features: Dict[str, float], importance_threshold: float = 0.4) -> List[str]:
        """Answers: How do they determine what not to build?

        Trims any feature with impact below a given threshold to maintain focus and minimize complexity.
        """
        return [f for f, importance in all_features.items() if importance < importance_threshold]

    def evaluate_feature_value_creation(self, feature_complexity: float, customer_willingness_to_pay: float) -> float:
        """Answers: How do they know which feature creates value?

        Value creation coefficient = (Willingness to Pay) / (Complexity cost ^ 1.5).
        """
        return customer_willingness_to_pay / max(0.1, math.pow(feature_complexity, 1.5))

    def discover_core_jtbd(self, user_frustrations_ranking: Dict[str, float]) -> str:
        """Answers: How do they discover the core job-to-be-done?

        Extracts the highest-ranked frustration to uncover the primary user job to be done.
        """
        if not user_frustrations_ranking:
            return "general_efficiency"
        return max(user_frustrations_ranking, key=user_frustrations_ranking.get)

    def optimize_for_learning_rate(self, current_learning_rate: float, deployment_cadence_days: float) -> float:
        """Answers: How do they optimize for learning rather than features?

        Adjusts feedback learning speed based on faster iteration cycles.
        """
        return current_learning_rate / max(1.0, deployment_cadence_days)


# ----------------------------------------------------------------------
# Layer 7: Customer Understanding
# ----------------------------------------------------------------------

class CustomerPsychologyModel(BaseModel):
    """Answers: How do entrepreneurs model customer psychology?

    Captures core variables of customer decision matrices and psychographic traits.
    """
    customer_id: UUID = Field(default_factory=uuid4)
    price_sensitivity: float = Field(0.5, ge=0.0, le=1.0)
    risk_aversion: float = Field(0.5, ge=0.0, le=1.0)
    inertia_strength: float = Field(0.5, ge=0.0, le=1.0)
    social_influence_susceptibility: float = Field(0.5, ge=0.0, le=1.0)


class CustomerUnderstandingEngine:
    """Layer 7: Psychological modeling of customer switching dynamics and trust building."""

    def __init__(self) -> None:
        pass

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

    def build_customer_trust(self, delivery_accuracy_rate: float, communication_transparency: float) -> float:
        """Answers: How do they build trust?

        Aggregates operational reliability and transparency into a unified trust metric.
        """
        return (delivery_accuracy_rate * 0.7) + (communication_transparency * 0.3)

    def analyze_buying_motives(self, pain_severity: float, return_on_investment: float) -> Dict[str, float]:
        """Answers: Why do customers buy?

        Weighs logical (ROI) and emotional/pain buying motives.
        """
        total = pain_severity + return_on_investment
        if total <= 0:
            return {"logical_motive": 0.5, "emotional_motive": 0.5}
        return {
            "logical_motive": return_on_investment / total,
            "emotional_motive": pain_severity / total
        }

    def analyze_churn_drivers(self, support_sla_breach_count: int, price_increase_ratio: float) -> float:
        """Answers: Why do customers leave?

        Computes risk score of churn based on service breaches and pricing shocks.
        """
        return min(1.0, (support_sla_breach_count * 0.1) + (price_increase_ratio * 0.5))

    def calculate_loyalty_index(self, repeat_purchase_count: int, net_promoter_score: float) -> float:
        """Answers: What creates loyalty?

        Loyalty index calculated from behavioral (purchases) and attitudinal (NPS) loyalty metrics.
        """
        normalized_purchases = min(1.0, repeat_purchase_count / 10.0)
        normalized_nps = max(0.0, net_promoter_score / 10.0)
        return (normalized_purchases * 0.5) + (normalized_nps * 0.5)

    def is_evangelist_candidate(self, loyalty_index: float, referral_rate_per_month: int) -> bool:
        """Answers: What creates evangelists?

        Identifies if high-loyalty users are proactively driving growth through peer networks.
        """
        return loyalty_index > 0.8 and referral_rate_per_month >= 2


# ----------------------------------------------------------------------
# Layer 8: Marketing
# ----------------------------------------------------------------------

class MarketingEngine:
    """Layer 8: Market formation, attention propagation, and channel attribution."""

    def __init__(self) -> None:
        pass

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
            # Attention propagation differential: d(Aware)/dt = k * Aware * (1 - Aware) * exposure_rate
            growth = viral_factor_k * current_aware * (1.0 - min(1.0, current_aware)) * exposure_rate
            current_aware += growth
            current_aware = min(1.0, max(0.0, current_aware))
            attention_curve.append(current_aware)

        return attention_curve

    def simulate_market_formation(self, demand_elasticity: float, supplier_density: float) -> float:
        """Answers: How do markets form?

        Calculates equilibrium velocity score of a forming market based on supply-demand density.
        """
        return max(0.0, 1.0 - (demand_elasticity * 0.4) - (supplier_density * 0.2))

    def evaluate_virality_factors(self, sharing_coefficient: float, retention_rate: float) -> float:
        """Answers: Why do ideas go viral?

        Evaluates the ultimate reproduction number (R0) of viral marketing ideas.
        """
        return sharing_coefficient * retention_rate

    def measure_brand_emergence(self, awareness: float, brand_sentiment: float) -> float:
        """Answers: How does brand emerge?

        Brand equity metric calculated as intersection of market reach and qualitative sentiment.
        """
        return awareness * brand_sentiment

    def compute_brand_authority(self, content_citations: int, domain_expertise_score: float) -> float:
        """Answers: What creates authority?

        Measures structural brand authority based on peer validation and verifiable domain expertise.
        """
        return min(1.0, (content_citations * 0.05) + (domain_expertise_score * 0.5))

    def calculate_positioning_perception_shift(self, baseline_perception: float, narrative_strength: float) -> float:
        """Answers: How does positioning influence perception?

        Models non-linear shift in audience perception as a function of narrative resonance.
        """
        delta = narrative_strength * (1.0 - baseline_perception)
        return min(1.0, baseline_perception + delta)

    def model_multi_channel_interaction(self, organic_leads: float, paid_ads_spend: float, synergy_factor: float = 0.2) -> float:
        """Answers: How do different acquisition channels interact?

        Quantifies the cross-channel attribution and synergy multiplier of simultaneous organic and paid campaigns.
        """
        base = organic_leads + (paid_ads_spend * 0.1)
        return base * (1.0 + synergy_factor)


# ----------------------------------------------------------------------
# Layer 9: Sales
# ----------------------------------------------------------------------

class SalesEngine:
    """Layer 9: Sales psychology and dynamic buying-urgency management."""

    def __init__(self) -> None:
        pass

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

    def simulate_sales_psychology_transition(self, cognitive_load: float, trust_index: float, perceived_value: float) -> float:
        """Answers: What actually happens psychologically during a sale?

        Switching probability / closing likelihood based on trust and value overcoming friction cognitive load.
        """
        net_force = perceived_value + trust_index - cognitive_load
        try:
            return 1.0 / (1.0 + math.exp(-net_force))
        except OverflowError:
            return 1.0 if net_force > 0 else 0.0

    def generate_sales_objections(self, customer_psychology: CustomerPsychologyModel) -> List[str]:
        """Answers: What creates objections?

        Derives logical and emotional buyer objections dynamically from customer psychographic profiles.
        """
        objections = []
        if customer_psychology.price_sensitivity > 0.7:
            objections.append("pricing_objection")
        if customer_psychology.risk_aversion > 0.7:
            objections.append("risk_objection")
        if customer_psychology.inertia_strength > 0.7:
            objections.append("switching_inertia_objection")
        return objections

    def should_automate_sales(self, annual_contract_value: float, deal_complexity_score: float) -> bool:
        """Answers: When should selling be automated?

        Determines if low contract value and low deal complexity warrant transactional self-serve automation.
        """
        return annual_contract_value < 5000.0 and deal_complexity_score < 0.3

    def is_enterprise_sales_necessary(self, annual_contract_value: float, stakeholder_count: int) -> bool:
        """Answers: When is enterprise sales necessary?

        Enterprise sales is required for high contract values with multiple decision makers/stakeholders.
        """
        return annual_contract_value >= 50000.0 or stakeholder_count >= 5

    def design_repeatable_sales_funnel(self, lead_count: int, conversion_rates: List[float]) -> Dict[str, float]:
        """Answers: How do founders design repeatable sales systems?

        Models volume progression and dropout rates step-by-step through the multi-stage sales funnel.
        """
        stages = ["lead_in", "qualified", "demo_completed", "proposal_sent", "closed_won"]
        funnel_flow = {"lead_in": float(lead_count)}
        current_volume = float(lead_count)

        for idx, rate in enumerate(conversion_rates):
            if idx + 1 < len(stages):
                current_volume *= rate
                funnel_flow[stages[idx + 1]] = round(current_volume, 2)
        return funnel_flow


# ----------------------------------------------------------------------
# Layer 10: Growth
# ----------------------------------------------------------------------

class GrowthEngine:
    """Layer 10: Compounding growth mechanics, platform shifts, and network dynamics."""

    def __init__(self) -> None:
        pass

    def calculate_network_effects_utility(self, active_users: int, coefficient: float) -> float:
        """Metcalfe's Law expansion utility score:

        Utility = c * N^2
        """
        return coefficient * (active_users ** 2)

    def evaluate_intentional_slowdown_trigger(self, churn_rate: float, support_sla_latency_hours: float) -> bool:
        """Flags that growth must decelerate intentionally to save product quality and prevent churn."""
        # Intentionally slow down if churn exceeds 10% or support latency exceeds 24 hours
        return churn_rate > 0.10 or support_sla_latency_hours > 24.0

    def detect_network_effects_emergence(self, active_users: int, total_nodes: int) -> bool:
        """Answers: How do network effects emerge?

        Checks if connected nodes pass the structural critical-mass utility threshold.
        """
        return active_users > 0.1 * total_nodes

    def evaluate_ecosystem_formation(self, partner_integrations_count: int, developer_api_calls: int) -> float:
        """Answers: How do ecosystems form?

        Computes gravity index of developer and partner interaction networks.
        """
        return (partner_integrations_count * 0.6) + (min(100000, developer_api_calls) / 100000.0 * 0.4)

    def evaluate_platform_transition(self, marginal_producer_cost: float, transaction_friction: float) -> bool:
        """Answers: How do platforms replace products?

        Platform shift is viable if supply enablement costs and transaction friction are low.
        """
        return marginal_producer_cost < 100.0 and transaction_friction < 0.2

    def predict_long_term_success_metrics(self, ltv_to_cac_ratio: float, net_revenue_retention: float) -> Dict[str, Any]:
        """Answers: What metrics predict long-term success?

        Assesses venture health variables against institutional venture investment benchmarks.
        """
        healthy = ltv_to_cac_ratio >= 3.0 and net_revenue_retention >= 1.1
        return {
            "is_scalable": healthy,
            "ltv_to_cac_ratio": ltv_to_cac_ratio,
            "net_revenue_retention": net_revenue_retention
        }


# ----------------------------------------------------------------------
# Layer 11: Competition
# ----------------------------------------------------------------------

class CompetitionEngine:
    """Layer 11: Competitive landscape positioning and game-theoretic payoffs."""

    def __init__(self) -> None:
        pass

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

                # Check player A best response
                a_is_best = True
                for alt_sa in player_a_strategies:
                    if payoff_matrix[(alt_sa, sb)][0] > current_payoff_a:
                        a_is_best = False
                        break

                # Check player B best response
                b_is_best = True
                for alt_sb in player_b_strategies:
                    if payoff_matrix[(sa, alt_sb)][1] > current_payoff_b:
                        b_is_best = False
                        break

                if a_is_best and b_is_best:
                    equilibria.append((sa, sb))

        return equilibria

    def anticipate_competitor_moves(self, competitor_strategy: str) -> str:
        """Answers: How do entrepreneurs anticipate competitors?

        Predicts optimal counter-strategy using a game-theoretic strategy matching heuristic.
        """
        strategy_map = {
            "low_price": "value_differentiation",
            "aggressive_marketing": "product_led_growth",
            "fast_feature_copying": "ecosystem_and_switching_costs"
        }
        return strategy_map.get(competitor_strategy, "first_principles_innovation")

    def evaluate_barrier_to_imitation(self, intellectual_property_score: float, unique_data_score: float) -> float:
        """Answers: How do they remain difficult to copy?

        Barrier score calculated on a [0, 1] scale.
        """
        return (intellectual_property_score * 0.5) + (unique_data_score * 0.5)

    def evaluate_pivot_triggers(self, customer_acquisition_cost: float, customer_lifetime_value: float, runway_months: float) -> bool:
        """Answers: How do they know when to pivot?

        Pivot is triggered if unit economics are structurally broken or runway is dangerously depleted.
        """
        return customer_acquisition_cost > customer_lifetime_value or runway_months < 3.0

    def simulate_disruption_survival(self, cash_reserves: float, monthly_burn: float, revenue_drop_ratio: float) -> bool:
        """Answers: How do they survive market disruptions?

        Verifies if cash reserves can withstand a sudden macro/disruptive revenue contraction.
        """
        adjusted_runway = cash_reserves / max(1.0, monthly_burn * (1.0 + revenue_drop_ratio))
        return adjusted_runway >= 6.0


# ----------------------------------------------------------------------
# Layer 12: Organizational Design
# ----------------------------------------------------------------------

class OrganizationalDesignEngine:
    """Layer 12: Constraint-based hiring thresholds and delegation structures."""

    def __init__(self) -> None:
        pass

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
            # Constraint is active; shadow price increases with marginal revenue gain of extra capacity
            return marginal_revenue * (current_utilization / capacity_limit)
        return 0.0  # Constraint inactive, shadow price is 0

    def determine_centralization_policy(self, decision_criticality: float, information_asymmetry: float) -> str:
        """Answers: What work should remain centralized?

        Decides centralized vs decentralized policy based on risk and local context.
        """
        if decision_criticality > 0.8:
            return "CENTRALIZED_EXECUTIVE_COMMAND"
        if information_asymmetry > 0.7:
            return "DECENTRALIZED_LOCAL_AUTONOMY"
        return "HYBRID_DELEGATED_POLICY"

    def determine_delegation_policy(self, team_capability: float, task_risk_level: float) -> str:
        """Answers: What should be delegated?

        Delegation decision algorithm based on skill trust and risk profile.
        """
        if team_capability > task_risk_level:
            return "FULL_DELEGATION"
        elif team_capability + 0.3 >= task_risk_level:
            return "SUPERVISED_DELEGATION"
        return "RETAIN_IN_CORE"

    def evolve_organizational_structure(self, headcount: int) -> str:
        """Answers: How does organizational structure evolve?

        Maps developmental milestones and organizational models by scale.
        """
        if headcount < 10:
            return "FLAT_COHESIVE_FOUNDING_TEAM"
        elif headcount < 50:
            return "FUNCTIONAL_DEPARTMENTS"
        return "MATRIX_OR_PRODUCT_DIVISIONS"

    def scale_decision_making_systems(self, standard_procedures_count: int, decentralized_groups_count: int) -> float:
        """Answers: How do decision-making systems scale?

        Throughput/Scale scalability ratio based on standard frameworks and local parallel autonomy groups.
        """
        return (standard_procedures_count * 1.5) + (decentralized_groups_count * 2.0)


# ----------------------------------------------------------------------
# Layer 13: Meta-Learning
# ----------------------------------------------------------------------

class MetaLearningEngine:
    """Layer 13: Cognitive mental model updates and textual backpropagation.

    Inspired by TextGrad, compiles failures into system instruction updates.
    """

    def __init__(self) -> None:
        self.mental_model_versions: Dict[str, int] = {}

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

        # Textual backpropagation update step
        updated_instructions = f"{current_system_instructions}\n[TextGrad Meta Update]: {'; '.join(feedback_gradients)}"
        return updated_instructions

    def evaluate_decision_quality(self, expected_outcome: float, actual_outcome: float, confidence_level: float) -> float:
        """Answers: How do they measure decision quality?

        Quality metric = 1 - abs(actual - expected) / expected * confidence.
        """
        if expected_outcome == 0:
            return 0.0
        error = abs(actual_outcome - expected_outcome) / expected_outcome
        return max(0.0, 1.0 - error * confidence_level)

    def train_intuition_feedback_loop(self, historic_intuition_accuracy: float, correction_feedback: float) -> float:
        """Answers: How do they build better intuition?

        Updates intuition success expectations in light of corrective real-world feedback.
        """
        learning_rate = 0.1
        return historic_intuition_accuracy + learning_rate * (correction_feedback - historic_intuition_accuracy)

    def calculate_competitive_learning_rate(self, experimental_velocity: float, cycle_time_days: float) -> float:
        """Answers: How do they learn faster than competitors?

        Measures structural learning cycle rate.
        """
        return experimental_velocity / max(1.0, cycle_time_days)

    def convert_failures_to_rules(self, failure_events: List[str]) -> List[str]:
        """Answers: How do they convert failures into reusable knowledge?

        Constructs generalized heuristic rules to avoid repeating observed failures.
        """
        rules = []
        for fail in failure_events:
            rules.append(f"PREVENT_RECURRENCE_OF_{fail.upper().replace(' ', '_')}")
        return rules


# ----------------------------------------------------------------------
# Layer 14: AI Entrepreneurship
# ----------------------------------------------------------------------

class AIEntrepreneurshipEngine:
    """Layer 14: The computational platform orchestrating autonomous entrepreneurial intelligence."""

    def __init__(self) -> None:
        pass

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

        # Simple priority-based allocation
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

    def rank_opportunities(self, opportunities: List[Opportunity]) -> List[Opportunity]:
        """Answers: How should an AI rank opportunities?

        Ranks opportunities based on risk-adjusted expected value.
        """
        return sorted(
            [opp for opp in opportunities if not opp.is_killed],
            key=lambda x: x.expected_value / max(1.0, x.downside_risk_var),
            reverse=True
        )

    def select_experimental_designs(self, uncertainty_dimensions: List[str]) -> List[str]:
        """Answers: How should an AI decide what experiments to run?

        Selects active learning experimental parameters to reduce targeted uncertainties.
        """
        experiments = []
        for dim in uncertainty_dimensions:
            experiments.append(f"RUN_ACTIVE_LEARNING_EXPERIMENT_ON_{dim.upper()}")
        return experiments

    def evaluate_entrepreneurial_performance(self, starting_assets: float, current_assets: float, alpha: float = 0.5) -> float:
        """Answers: How should an AI measure entrepreneurial performance?

        Performance metric based on log wealth return and capital growth rate.
        """
        if starting_assets <= 0:
            return 0.0
        return alpha * math.log(current_assets / starting_assets)


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

    def run_full_cognitive_cycle(
        self,
        raw_market_signals: Dict[str, float],
        available_capital: float,
        compute_hours: float
    ) -> Dict[str, Any]:
        """Runs an end-to-end multi-layer entrepreneurial lifecycle."""
        logger.info("Executing comprehensive 14-layer computational cycle...")

        # 1. Sense and Discover (Layer 2)
        filtered_signals = self.discovery_eng.filter_weak_signals(raw_market_signals)
        if len(filtered_signals) >= 2:
            opp = self.discovery_eng.synthesize_combinatorial_opportunity(
                filtered_signals[0], filtered_signals[1], {"market_trend": "active_inference_scale"}
            )
            self.registered_opportunities.append(opp)

        # If empty, create a default base opportunity
        if not self.registered_opportunities:
            self.registered_opportunities.append(
                Opportunity(name="Base Opportunity", description="Default initialized search candidate")
            )

        opp_to_test = self.registered_opportunities[-1]

        # 2. Problem Root-Cause Backdoor Analysis (Layer 3)
        # Classify and perform a do-calculus causal strength extraction
        opp_to_test.is_first_order_problem = self.problem_eng.classify_problem_order(
            {"prob_1": ["prob_0"]}, "prob_0"
        )
        is_root, causal_str = self.problem_eng.evaluate_root_cause_do(0.6, 0.4, 0.9)
        opp_to_test.root_cause_identified = is_root

        # 3. Decision-Making & Fast-Kill Gating (Layer 4)
        # Run confirmation-bias adjusted priors updating
        a, b = self.decision_eng.compute_confirmation_bias_adjusted_priors(10.0, 10.0, 3, 4)
        should_kill = self.decision_eng.should_kill_idea(a, b, 7)
        opp_to_test.is_killed = should_kill

        # 4. Evaluation Valuation (Layer 5)
        ev = self.evaluation_eng.calculate_expected_value(500000.0, 0.65, 50000.0)
        opp_to_test.expected_value = ev
        opp_to_test.downside_risk_var = self.evaluation_eng.estimate_value_at_risk(ev, 15000.0)
        opp_to_test.timing_score = self.evaluation_eng.evaluate_timing_score(2.5, 2.0, 5.0)

        # 5. Resource Allocation across live opportunities (Layer 14)
        allocations = self.ai_eng.allocate_capital_and_compute(
            self.registered_opportunities, available_capital, compute_hours
        )

        # 6. Meta-learning failure feedback loop (Layer 13)
        fail_logs = []
        if should_kill:
            fail_logs.append("Opportunity killed due to bad Bayesian confirmation updates.")
        if opp_to_test.downside_risk_var > 100000.0:
            fail_logs.append("Severe risk bottleneck found during valuation calculations.")

        self.system_instructions = self.meta_eng.run_textgrad_optimization(
            fail_logs, self.system_instructions
        )

        # Return state trace representing the complete 14-layer cycle
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
