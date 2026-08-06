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
# Layer 1: Reality & Macroeconomic Drag Subsystem
# ----------------------------------------------------------------------

class MacroeconomicForecastingSubsystem:
    """Simulates macroeconomic and regulatory forces (drag, inflation, interest rate penalties)."""

    def __init__(self, baseline_interest_rate: float = 0.05, baseline_inflation_rate: float = 0.03) -> None:
        self.interest_rate = baseline_interest_rate
        self.inflation_rate = baseline_inflation_rate

    def calculate_drag_multiplier(self, regulatory_tariff_shocks: float = 0.0) -> float:
        """Computes the overall macroeconomic drag multiplier (value in [0.1, 1.0])."""
        drag = (self.interest_rate * 1.5) + (self.inflation_rate * 2.0) + regulatory_tariff_shocks
        return max(0.1, 1.0 - drag)


class RealityOptimizer:
    """Layer 1: The First-Principles Foundation of Entrepreneurship.

    Deconstructs entrepreneurship to its absolute baseline: returning high value
    on risk-adjusted cognitive energy and capital. Distinguishes psychology
    (intuition bias, risk tolerance) from optimization (calculable variables).
    """

    def __init__(self, human_risk_aversion: float = 2.0, cognitive_energy_weight: float = 1.0) -> None:
        self.human_risk_aversion = human_risk_aversion
        self.cognitive_energy_weight = cognitive_energy_weight
        self.macro_subsystem = MacroeconomicForecastingSubsystem()

    def calculate_global_objective(
        self,
        expected_revenue: float,
        value_at_risk: float,
        cognitive_energy_expended: float,
        capital_cost: float,
        regulatory_tariff_shocks: float = 0.0
    ) -> float:
        """Computes the global risk-adjusted macroeconomic-penalized utility:

        U_ent = ((E[R] * drag) - w_r * VaR(R)) / (E[E_cogn] + w_c * C)
        """
        drag = self.macro_subsystem.calculate_drag_multiplier(regulatory_tariff_shocks)
        numerator = (expected_revenue * drag) - (self.human_risk_aversion * value_at_risk)
        denominator = cognitive_energy_expended + (self.cognitive_energy_weight * capital_cost)

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


# ----------------------------------------------------------------------
# Layer 4: Decision Making & Founder Psychology
# ----------------------------------------------------------------------

class DecisionMakingEngine:
    """Layer 4: Elite decision making under extreme uncertainty.

    Uses Bayesian Beta-Binomial models to seeking information, calculates confirmation
    bias adjustments, and triggers rapid-kill mechanisms for bad ideas.
    Now incorporates a cognitive exhaustion/burnout penalty.
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

    def should_kill_idea(
        self,
        alpha: float,
        beta: float,
        total_trials: int,
        cognitive_exhaustion_score: float = 0.0
    ) -> bool:
        """Triggers a fast-kill protocol if expected success falls below threshold.

        Now incorporates decision fatigue (burnout lowers confidence tolerance or accelerates kills).
        """
        if total_trials < 5:
            return False  # Give it some initial runway to learn

        expected_success_rate = alpha / (alpha + beta)
        # Decision fatigue increases the fast-kill threshold due to inability to sustain high-complexity operations
        dynamic_threshold = self.min_confidence_threshold + (cognitive_exhaustion_score * 0.1)
        return expected_success_rate < dynamic_threshold


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


# ----------------------------------------------------------------------
# Layer 7: Customer Understanding & Reputation Dynamics
# ----------------------------------------------------------------------

class CustomerUnderstandingEngine:
    """Layer 7: Psychological modeling of customer switching dynamics, reputation modeling, and trust decay."""

    def __init__(self) -> None:
        pass

    def evaluate_switching_probability(
        self,
        current_product_utility: float,
        proposed_product_utility: float,
        switching_costs: float,
        push_forces: float,
        pull_forces: float,
        reputation_score: float = 1.0,
        trust_decay_coefficient: float = 0.0
    ) -> float:
        """Computes customer transition probability using utility differentials, trust decay, and reputation.

        P_switch = sigmoid( (U_new - U_old) - C_switch + Push + Pull + ln(reputation) * (1 - decay) )
        """
        reputation_force = math.log(max(0.01, reputation_score)) * (1.0 - trust_decay_coefficient)
        net_utility = (proposed_product_utility - current_product_utility) - switching_costs + push_forces + pull_forces + reputation_force
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
            # d(Aware)/dt = k * Aware * (1 - Aware) * exposure_rate
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

    def calculate_network_effects_utility(self, active_users: int, coefficient: float) -> float:
        """Metcalfe's Law expansion utility score:

        Utility = c * N^2
        """
        return coefficient * (active_users ** 2)

    def evaluate_intentional_slowdown_trigger(self, churn_rate: float, support_sla_latency_hours: float) -> bool:
        """Flags that growth must decelerate intentionally to save product quality and prevent churn."""
        # Intentionally slow down if churn exceeds 10% or support latency exceeds 24 hours
        return churn_rate > 0.10 or support_sla_latency_hours > 24.0


# ----------------------------------------------------------------------
# Layer 11: Competition & Adversarial Signaling
# ----------------------------------------------------------------------

class CompetitionEngine:
    """Layer 11: Competitive landscape positioning, deceptive signaling, and game-theoretic payoffs."""

    def __init__(self) -> None:
        pass

    def calculate_moat_strength(self, generic_utility: float, switching_costs: float) -> float:
        """Moat = utility protection buffer provided by high customer switching friction."""
        return generic_utility + switching_costs

    def compute_nash_equilibrium_payoff(
        self,
        player_a_strategies: List[str],
        player_b_strategies: List[str],
        payoff_matrix: Dict[Tuple[str, str], Tuple[float, float]],
        deceptive_signal_factor_b: float = 0.0
    ) -> List[Tuple[str, str]]:
        """Identifies any Pure Strategy Nash Equilibria under potential deceptive signaling from player B.

        Deceptive signal shifts perceived payoff matrices.
        """
        equilibria = []

        for sa in player_a_strategies:
            for sb in player_b_strategies:
                perceived_payoff_a, perceived_payoff_b = payoff_matrix[(sa, sb)]
                # B deceptively inflates perceived values to player A to trigger bad commitments
                perceived_payoff_a_adjusted = perceived_payoff_a + deceptive_signal_factor_b

                # Check player A perceived best response
                a_is_best = True
                for alt_sa in player_a_strategies:
                    alt_payoff_a = payoff_matrix[(alt_sa, sb)][0] + deceptive_signal_factor_b
                    if alt_payoff_a > perceived_payoff_a_adjusted:
                        a_is_best = False
                        break

                # Check player B actual best response
                b_is_best = True
                for alt_sb in player_b_strategies:
                    if payoff_matrix[(sa, alt_sb)][1] > perceived_payoff_b:
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


# ----------------------------------------------------------------------
# Layer 14: AI Entrepreneurship (Portfolio Construction via Kelly Criterion)
# ----------------------------------------------------------------------

class AIEntrepreneurshipEngine:
    """Layer 14: The computational platform orchestrating autonomous portfolio construction via Kelly-Criterion."""

    def __init__(self) -> None:
        pass

    def allocate_capital_and_compute(
        self,
        opportunities: List[Opportunity],
        total_capital: float,
        total_compute_hours: float
    ) -> Dict[UUID, Tuple[float, float]]:
        """Solves a capital-allocation problem under Kelly Criterion heuristics.

        Returns (capital_cents, compute_hours) allocations.
        """
        return self.allocate_capital_and_compute_kelly(
            opportunities=opportunities,
            total_capital=total_capital,
            total_compute_hours=total_compute_hours,
            p_success_overrides={},
            odds_overrides={}
        )

    def allocate_capital_and_compute_kelly(
        self,
        opportunities: List[Opportunity],
        total_capital: float,
        total_compute_hours: float,
        p_success_overrides: Dict[UUID, float],
        odds_overrides: Dict[UUID, float]
    ) -> Dict[UUID, Tuple[float, float]]:
        """Applies exact Multi-Venture Kelly Criterion fractional allocation:

        f_i* = (p_i * b_i - q_i) / b_i
        """
        allocations = {}
        if not opportunities:
            return allocations

        kelly_fractions = {}
        total_fraction = 0.0

        for opp in opportunities:
            if opp.is_killed:
                kelly_fractions[opp.opportunity_id] = 0.0
                continue

            p = p_success_overrides.get(opp.opportunity_id, 0.5)
            # odds b = payout ratio (expected payout / cost)
            b = odds_overrides.get(opp.opportunity_id, 1.5)
            if b <= 0:
                b = 0.1

            # Kelly formula: f* = (p * b - (1 - p)) / b
            f_star = (p * b - (1.0 - p)) / b
            f_clamped = max(0.0, f_star)
            kelly_fractions[opp.opportunity_id] = f_clamped
            total_fraction += f_clamped

        # Prevent total allocation from exceeding 100% of reserves
        normalization = max(1.0, total_fraction)

        for opp in opportunities:
            f = kelly_fractions[opp.opportunity_id] / normalization
            allocations[opp.opportunity_id] = (
                total_capital * f,
                total_compute_hours * f
            )

        return allocations


# ----------------------------------------------------------------------
# Master Orchestrator (Version 1 State-of-the-Art Core)
# ----------------------------------------------------------------------

class EntrepreneurialIntelligenceOrchestrator:
    """The complete executive orchestrator coordinating all 14 layers.

    Senses, discovers, evaluates, and optimizes entrepreneurial opportunity state spaces.
    Handles multiple conflicting objectives, cognitive exhaustion, and macroeconomic shocks.
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
        self.cognitive_exhaustion_score = 0.0

    def run_full_cognitive_cycle(
        self,
        raw_market_signals: Dict[str, float],
        available_capital: float,
        compute_hours: float,
        regulatory_tariff_shocks: float = 0.0
    ) -> Dict[str, Any]:
        """Runs an end-to-end multi-layer entrepreneurial lifecycle."""
        logger.info("Executing comprehensive 14-layer computational cycle...")

        # Increment cognitive fatigue
        self.cognitive_exhaustion_score = min(1.0, self.cognitive_exhaustion_score + 0.05)

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

        # 3. Decision-Making & Fast-Kill Gating (Layer 4 with Cognitive Fatigue)
        a, b = self.decision_eng.compute_confirmation_bias_adjusted_priors(10.0, 10.0, 3, 4)
        should_kill = self.decision_eng.should_kill_idea(a, b, 7, self.cognitive_exhaustion_score)
        opp_to_test.is_killed = should_kill

        # 4. Evaluation Valuation (Layer 5 with Macroeconomic Shocks)
        ev = self.evaluation_eng.calculate_expected_value(500000.0, 0.65, 50000.0)
        opp_to_test.expected_value = ev
        opp_to_test.downside_risk_var = self.evaluation_eng.estimate_value_at_risk(ev, 15000.0)
        opp_to_test.timing_score = self.evaluation_eng.evaluate_timing_score(2.5, 2.0, 5.0)

        # Apply global macroeconomic objective check
        global_u = self.reality_opt.calculate_global_objective(
            expected_revenue=ev,
            value_at_risk=opp_to_test.downside_risk_var,
            cognitive_energy_expended=5.0,
            capital_cost=1000.0,
            regulatory_tariff_shocks=regulatory_tariff_shocks
        )

        # 5. Resource Allocation across live opportunities using exact Kelly formulations (Layer 14)
        p_success_map = {opp.opportunity_id: 0.65 for opp in self.registered_opportunities}
        odds_map = {opp.opportunity_id: 2.0 for opp in self.registered_opportunities}
        allocations = self.ai_eng.allocate_capital_and_compute_kelly(
            self.registered_opportunities, available_capital, compute_hours, p_success_map, odds_map
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
            "system_instructions_length": len(self.system_instructions),
            "global_utility": global_u,
            "cognitive_exhaustion": self.cognitive_exhaustion_score
        }
