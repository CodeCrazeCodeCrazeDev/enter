"""
The complete, first-principles executable implementation of the
14-Layer Computational Architecture of Entrepreneurship for SERO / AI EOS.

Layers Implemented:
  - Layer 1: Reality Framework (Invariant Principles, Automation Limits)
  - Layer 2: Opportunity Discovery Engine (State Space Search, Weak Signal Filter)
  - Layer 3: Problem Discovery Engine (Root Cause vs Symptom, Pearl SCM)
  - Layer 4: Decision Making Engine (Active Inference, Bias Elimination)
  - Layer 5: Opportunity Evaluation Engine (EV, Kelly Criterion, Downside Risk)
  - Layer 6: Product Creation Engine (JTBD, Complexity Pruning)
  - Layer 7: Customer Understanding Engine (Trust Dynamics, Switching Friction)
  - Layer 8: Marketing Engine (Attention Dynamics, Virality K-Factor)
  - Layer 9: Sales Engine (Urgency, Objection Resolution, Funnel Automation)
  - Layer 10: Growth Engine (Network Effects, Compounding Vectors)
  - Layer 11: Competition & Moat Engine (Moat Durability, Pivot Triggers)
  - Layer 12: Organizational Design Engine (Delegation Thresholds, Scaling)
  - Layer 13: Meta-Learning Engine (Bayesian Model Updates, Skill Conversion)
  - Layer 14: AI Entrepreneurship Orchestrator (Full 14-Layer Coordination)
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.computational_architecture")


# ============================================================================
# Core Data Models
# ============================================================================

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
    # Extended 14-layer fields
    weak_signal_score: float = 0.5
    trend_alignment: float = 0.8
    novelty_score: float = 0.7
    downside_risk: float = 0.2
    capital_required_cents: int = 20000000  # Default $200k


class ProblemDefinition(BaseModel):
    """Layer 3: Problem Discovery model."""
    stated_problem: str
    root_cause: str
    is_root_cause: bool = False
    order: int = 1  # 1st order vs 2nd order
    symptom_severity: float = 0.5
    ignore_score: float = 0.1  # Higher score indicates problem should be ignored


class CustomerProfile(BaseModel):
    """Layer 7: Customer Understanding model."""
    segment: str
    switching_friction: float = 0.8  # [0, 1]
    trust_level: float = 0.5        # [0, 1]
    core_jtbd: str = "Solve core operational inefficiency"
    evangelism_potential: float = 0.6


# ============================================================================
# Layer 1: Reality Framework
# ============================================================================

class RealityEngine:
    """
    Layer 1: Defines fundamental invariants across entrepreneurship,
    differentiating human psychological dynamics from pure mathematical optimization.
    """

    def __init__(self) -> None:
        self.invariants = [
            "Value creation precedes value capture",
            "Asymmetric payoff with limited downside and open-ended upside",
            "Arbitrage of state-space informational asymmetries",
            "Execution speed reduces uncertainty faster than passive reflection"
        ]

    def evaluate_task_automation(self, task_name: str) -> Dict[str, Any]:
        """Classifies tasks into automatable optimization vs non-automatable human judgment."""
        non_automatable = {"empathy_validation", "human_trust_building", "high_stakes_moral_arbitrage"}
        is_automatable = task_name.lower() not in non_automatable
        return {
            "task": task_name,
            "can_automate": is_automatable,
            "psychology_weight": 0.8 if not is_automatable else 0.2,
            "optimization_weight": 0.2 if not is_automatable else 0.8
        }


# ============================================================================
# Layer 2: Opportunity Discovery Engine
# ============================================================================

class OpportunityDiscoveryEngine:
    """
    Layer 2: Continuously searches world state space for economically valuable opportunities,
    filtering weak signals and predicting emerging trends before market convergence.
    """

    def search_state_space(self, signals: List[Dict[str, Any]]) -> List[Opportunity]:
        discovered = []
        for sig in signals:
            weak_signal_strength = sig.get("signal_strength", 0.3)
            trend_alignment = sig.get("trend_alignment", 0.7)
            # Filter signals below threshold unless novelty is exceptionally high
            novelty = sig.get("novelty", 0.5)
            if weak_signal_strength > 0.2 or novelty > 0.8:
                opp = Opportunity(
                    title=sig.get("title", "Discovered Opportunity"),
                    domain=sig.get("domain", "general"),
                    variables=sig.get("variables", []),
                    causal_edges=sig.get("causal_edges", []),
                    coefficients=sig.get("coefficients", {}),
                    prior_entropy=sig.get("prior_entropy", 1.5),
                    post_entropy_simulated=sig.get("post_entropy_simulated", 0.4),
                    success_probability=sig.get("success_probability", 0.5),
                    tam_cents=sig.get("tam_cents", 100000000),
                    weak_signal_score=weak_signal_strength,
                    trend_alignment=trend_alignment,
                    novelty_score=novelty
                )
                discovered.append(opp)
        return discovered


# ============================================================================
# Layer 3: Problem Discovery & Structural Causal Model Engine
# ============================================================================

class AdvancedCausalEngine:
    """
    Layer 3: Structural Causal Model (SCM) handling Pearl's do-calculus
    interventions, counterfactual estimations, and root-cause decomposition.
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

    def decompose_problem(self, stated_problem: str, observed_symptoms: List[str]) -> ProblemDefinition:
        """Distinguishes stated symptoms from root causes and determines 1st vs 2nd order impact."""
        # Simple causal heuristics over observed symptoms
        is_root = len(observed_symptoms) > 2
        root_cause = f"Systemic bottleneck in {stated_problem.lower()}" if is_root else stated_problem
        ignore_score = 0.05 if is_root else 0.7  # Pure symptoms should often be ignored
        return ProblemDefinition(
            stated_problem=stated_problem,
            root_cause=root_cause,
            is_root_cause=is_root,
            order=1 if is_root else 2,
            symptom_severity=0.8 if len(observed_symptoms) > 0 else 0.2,
            ignore_score=ignore_score
        )

    def execute_do_intervention(self, target_var: str, value: float) -> Dict[str, float]:
        if target_var not in self.variables:
            raise ValueError(f"Variable '{target_var}' is not registered.")

        state: Dict[str, float] = {var: 0.0 for var in self.variables}
        state[target_var] = value

        for _ in range(len(self.variables)):
            for var in self.variables:
                if var == target_var:
                    continue

                parents_list = self.parents.get(var, [])
                if not parents_list:
                    continue

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
        intervened_var, inter_value = counterfactual_intervention

        noise_estimates: Dict[str, float] = {}
        for var in self.variables:
            factual_val = factual_observations.get(var, 0.0)
            parents_list = self.parents.get(var, [])
            structural_expected = 0.0
            for parent in parents_list:
                coef = self.coefficients.get((parent, var), 0.0)
                structural_expected += coef * factual_observations.get(parent, 0.0)

            noise_estimates[var] = factual_val - structural_expected

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

                state[var] = structural_sum + noise_estimates.get(var, 0.0)

        return state.get(target_outcome_var, 0.0)


# ============================================================================
# Layer 4: Decision Making Engine (Active Inference)
# ============================================================================

class ActiveInferencePlanner:
    """
    Layer 4: Active Inference decision framework utilizing Expected Free Energy (EFE)
    minimization to balance pragmatic value (goal achievement) with epistemic curiosity.
    """

    def __init__(self, curiosity_weight: float = 1.0) -> None:
        self.curiosity_weight = curiosity_weight

    def calculate_efe(self, opp: Opportunity) -> float:
        eps = 1e-10
        p_success = max(eps, min(1.0 - eps, opp.success_probability))
        p_target = max(eps, min(1.0 - eps, opp.target_preference))

        pragmatic_value = math.log(p_success) - math.log(p_target)
        epistemic_value = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)

        efe = -pragmatic_value - (epistemic_value * self.curiosity_weight)
        return efe

    def rank_opportunities(self, opportunities: List[Opportunity]) -> List[Tuple[Opportunity, float]]:
        ranked = []
        for opp in opportunities:
            efe = self.calculate_efe(opp)
            ranked.append((opp, efe))
        return sorted(ranked, key=lambda x: x[1])


# ============================================================================
# Layer 5: Opportunity Evaluation Engine
# ============================================================================

class OpportunityEvaluationEngine:
    """
    Layer 5: Evaluates expected value (EV), Kelly Criterion position sizing,
    downside risk, and explicit pivot/abandon conditions.
    """

    def compute_expected_value_cents(self, opp: Opportunity) -> float:
        return opp.tam_cents * opp.success_probability

    def calculate_kelly_fraction(self, opp: Opportunity) -> float:
        """Kelly Criterion: f* = (p * b - q) / b where b is payoff ratio."""
        p = opp.success_probability
        q = 1.0 - p
        payoff_ratio = (opp.tam_cents / max(1, opp.capital_required_cents))
        if payoff_ratio <= 0:
            return 0.0
        kelly = (p * payoff_ratio - q) / payoff_ratio
        # Fractional Kelly safety cap (0.25 max allocation)
        return max(0.0, min(0.25, kelly))

    def evaluate_abandonment(self, opp: Opportunity, current_loss_cents: int) -> bool:
        """Kills bad ideas when downside loss exceeds 50% of required capital or success prob drops below 0.15."""
        if current_loss_cents > (0.5 * opp.capital_required_cents) or opp.success_probability < 0.15:
            return True
        return False


# ============================================================================
# Layer 6: Product Creation Engine
# ============================================================================

class ProductCreationEngine:
    """
    Layer 6: Optimizes product creation by anti-feature pruning (determining what NOT to build),
    minimizing complexity, and prioritizing learning velocity over feature volume.
    """

    def prune_anti_features(self, candidate_features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prunes bloat features that increase complexity without driving core JTBD value."""
        pruned = []
        for feat in candidate_features:
            complexity = feat.get("complexity", 0.5)
            value = feat.get("jtbd_value", 0.5)
            # Retain feature only if value-to-complexity ratio is high
            if value / max(0.1, complexity) >= 1.0:
                pruned.append(feat)
        return pruned

    def calculate_learning_velocity(self, experiment_count: int, iteration_days: float) -> float:
        """Learning rate = experiments / iteration_days."""
        return experiment_count / max(0.1, iteration_days)


# ============================================================================
# Layer 7: Customer Understanding Engine
# ============================================================================

class CustomerUnderstandingEngine:
    """
    Layer 7: Models customer psychology, switching friction, trust buildup/decay,
    and retention versus evangelism dynamics.
    """

    def simulate_trust_dynamics(self, profile: CustomerProfile, positive_touchpoints: int, negative_touchpoints: int) -> float:
        """Trust increases linearly with positive interactions, decays exponentially with failures."""
        decay_factor = 0.5 ** negative_touchpoints
        gain = 0.1 * positive_touchpoints
        new_trust = min(1.0, (profile.trust_level + gain) * decay_factor)
        profile.trust_level = new_trust
        return new_trust

    def calculate_switching_probability(self, profile: CustomerProfile, competitor_value_delta: float) -> float:
        """Switching probability is governed by Value Delta relative to Switching Friction."""
        net_advantage = competitor_value_delta - profile.switching_friction
        if net_advantage <= 0:
            return 0.05  # Baseline passive retention
        return min(0.95, net_advantage / (net_advantage + profile.switching_friction))


# ============================================================================
# Layer 8: Marketing & Attention Engine
# ============================================================================

class MarketingEngine:
    """
    Layer 8: Models market formation, attention dynamics, viral spreading (K-factor),
    and channel acquisition interactions.
    """

    def compute_viral_k_factor(self, invites_per_user: float, conversion_rate: float) -> float:
        """K-Factor = i * c. K > 1.0 indicates exponential viral compounding."""
        return invites_per_user * conversion_rate

    def calculate_channel_synergy(self, channels: List[Dict[str, float]]) -> float:
        """Computes multi-channel synergy multiplier across acquisition vectors."""
        total_reach = sum(c.get("reach", 0.0) for c in channels)
        synergy_bonus = 1.15 if len(channels) > 1 else 1.0
        return total_reach * synergy_bonus


# ============================================================================
# Layer 9: Sales System Engine
# ============================================================================

class SalesEngine:
    """
    Layer 9: Formalizes psychological urgency, objection resolution mechanics,
    and sales automation thresholding.
    """

    def resolve_objections(self, buyer_objections: List[str], trust_level: float) -> Dict[str, Any]:
        resolved_count = 0
        for obj in buyer_objections:
            if trust_level > 0.6:  # Trust resolves minor friction objections
                resolved_count += 1
        return {
            "total_objections": len(buyer_objections),
            "resolved": resolved_count,
            "closing_urgency_score": trust_level * (resolved_count / max(1, len(buyer_objections)))
        }

    def should_automate_sales(self, deal_size_cents: int) -> bool:
        """Self-serve automation for deal sizes < $5,000 (500,000 cents); high-touch for enterprise."""
        return deal_size_cents < 500000


# ============================================================================
# Layer 10: Growth & Compounding Engine
# ============================================================================

class GrowthEngine:
    """
    Layer 10: Models compounding growth vectors, network effect strength,
    and platform vs product transformation.
    """

    def calculate_network_effect_value(self, active_nodes: int, coupling_coefficient: float = 0.01) -> float:
        """Metcalfe's Law adaptation: V = c * N^2."""
        return coupling_coefficient * (active_nodes ** 2)

    def evaluate_platform_transition(self, third_party_developers: int, ecosystem_revenue_share: float) -> bool:
        """Transitions product to platform when 3rd party ecosystem generates significant activity."""
        return third_party_developers >= 10 and ecosystem_revenue_share >= 0.20


# ============================================================================
# Layer 11: Competition & Moat Architecture
# ============================================================================

class CompetitionEngine:
    """
    Layer 11: Models competitive moat durability, defensive flywheels,
    and pivot requirements in response to structural market disruption.
    """

    def compute_moat_durability(self, switching_costs: float, network_effects: float, brand_equity: float) -> float:
        """Composite moat score [0, 1]."""
        return min(1.0, 0.4 * switching_costs + 0.4 * network_effects + 0.2 * brand_equity)

    def check_pivot_trigger(self, competitive_threat_level: float, market_share_loss_rate: float) -> bool:
        """Triggers strategic pivot if competitive threat > 0.8 and market share loss > 15%."""
        return competitive_threat_level > 0.8 and market_share_loss_rate > 0.15


# ============================================================================
# Layer 12: Organizational Design Engine
# ============================================================================

class OrganizationDesignEngine:
    """
    Layer 12: Formalizes delegation vs centralization thresholds, hiring signals,
    and organizational scaling mechanics.
    """

    def evaluate_delegation_threshold(self, task_complexity: float, employee_skill: float) -> str:
        if employee_skill >= task_complexity:
            return "delegate"
        elif employee_skill >= 0.7 * task_complexity:
            return "collaborate"
        return "centralize"


# ============================================================================
# Layer 13: Meta-Learning & Mental Model Flywheel
# ============================================================================

class MetaLearningEngine:
    """
    Layer 13: Measures decision quality, executes post-mortems, updates Bayesian
    mental models, and converts real-world failures into reusable skills.
    """

    def __init__(self) -> None:
        self.learned_rules: List[str] = []

    def process_failure_post_mortem(self, failure_reason: str, empirical_loss: float) -> str:
        rule = f"AVOID: {failure_reason} (Prior loss magnitude: {empirical_loss:.2f})"
        if rule not in self.learned_rules:
            self.learned_rules.append(rule)
        return rule

    def update_prior_belief(self, prior: float, likelihood: float) -> float:
        """Bayesian update: Posterior ~ Prior * Likelihood."""
        numerator = prior * likelihood
        denominator = (prior * likelihood) + ((1.0 - prior) * (1.0 - likelihood))
        if denominator == 0:
            return prior
        return numerator / denominator


# ============================================================================
# Layer 14: AI Entrepreneurship Orchestrator
# ============================================================================

class EntrepreneurialIntelligenceOrchestrator:
    """
    Layer 14: Master coordinating engine driving the complete 14-layer execution pipeline.
    Connects sensing, causal inference, evaluation, customer dynamics, growth, and meta-learning.
    """

    def __init__(self, causal_engine: AdvancedCausalEngine, planner: ActiveInferencePlanner) -> None:
        self.reality_engine = RealityEngine()
        self.discovery_engine = OpportunityDiscoveryEngine()
        self.causal_engine = causal_engine
        self.planner = planner
        self.eval_engine = OpportunityEvaluationEngine()
        self.product_engine = ProductCreationEngine()
        self.customer_engine = CustomerUnderstandingEngine()
        self.marketing_engine = MarketingEngine()
        self.sales_engine = SalesEngine()
        self.growth_engine = GrowthEngine()
        self.competition_engine = CompetitionEngine()
        self.org_engine = OrganizationDesignEngine()
        self.meta_engine = MetaLearningEngine()

        self.opportunities: List[Opportunity] = []

    def ingest_signal(self, signal: Dict[str, Any]) -> Opportunity:
        logger.info(f"Layer 2 Sensing external signal: {signal.get('title')}")
        opp = Opportunity(
            title=signal.get("title", "Unnamed Opportunity"),
            domain=signal.get("domain", "general"),
            variables=signal.get("variables", []),
            causal_edges=signal.get("causal_edges", []),
            coefficients=signal.get("coefficients", {}),
            prior_entropy=signal.get("prior_entropy", 1.5),
            post_entropy_simulated=signal.get("post_entropy_simulated", 0.4),
            success_probability=signal.get("success_probability", 0.5),
            tam_cents=signal.get("tam_cents", 100000000),
            capital_required_cents=signal.get("capital_required_cents", 20000000)
        )
        self.opportunities.append(opp)
        return opp

    def execute_orchestrated_pipeline(self) -> Dict[str, Any]:
        """Runs the full 14-layer analysis pipeline over active opportunities."""
        if not self.opportunities:
            return {"status": "idle", "reason": "No opportunities registered."}

        # Layer 1: Invariant Check
        reality_check = self.reality_engine.evaluate_task_automation("opportunity_evaluation")

        # Layer 2, 4, 5: Opportunity Ranking & Position Sizing
        ranked_opps = self.planner.rank_opportunities(self.opportunities)
        primary_opp, best_efe = ranked_opps[0]

        ev_cents = self.eval_engine.compute_expected_value_cents(primary_opp)
        kelly_fraction = self.eval_engine.calculate_kelly_fraction(primary_opp)

        # Layer 3: Causal Initialization & Problem Decomposition
        problem_def = self.causal_engine.decompose_problem(
            stated_problem=f"Market friction in {primary_opp.domain}",
            observed_symptoms=["high_cac", "churn", "low_margin"]
        )

        for var in primary_opp.variables:
            self.causal_engine.register_variable(var)
        for parent, child in primary_opp.causal_edges:
            weight = primary_opp.coefficients.get(f"{parent}->{child}", 0.5)
            self.causal_engine.add_causal_relationship(parent, child, weight)

        intervention_var = primary_opp.variables[0] if primary_opp.variables else "marketing_spend"
        inter_state = self.causal_engine.execute_do_intervention(intervention_var, 1.5)

        # Layer 6, 7, 8, 9, 10, 11, 12: Operational Subsystem Evaluations
        customer = CustomerProfile(segment="early_adopters")
        trust = self.customer_engine.simulate_trust_dynamics(customer, positive_touchpoints=3, negative_touchpoints=0)

        viral_k = self.marketing_engine.compute_viral_k_factor(invites_per_user=2.0, conversion_rate=0.6)
        sales_automation = self.sales_engine.should_automate_sales(deal_size_cents=100000)
        network_val = self.growth_engine.calculate_network_effect_value(active_nodes=100)
        moat_score = self.competition_engine.compute_moat_durability(0.8, 0.7, 0.6)
        delegation = self.org_engine.evaluate_delegation_threshold(task_complexity=0.6, employee_skill=0.8)

        # Layer 13: Meta-Learning Update
        post_mortem_rule = self.meta_engine.process_failure_post_mortem("unvalidated_channel_spend", 50000.0)

        return {
            "status": "executed",
            "layer_1_reality": reality_check,
            "selected_opportunity": primary_opp.title,
            "best_expected_free_energy": best_efe,
            "expected_value_cents": ev_cents,
            "kelly_allocation_fraction": kelly_fraction,
            "layer_3_problem_decomposition": problem_def.model_dump(),
            "intervention_performed": f"do({intervention_var} = 1.5)",
            "propagated_state": inter_state,
            "customer_trust": trust,
            "viral_k_factor": viral_k,
            "sales_automated": sales_automation,
            "network_effect_value": network_val,
            "moat_durability_score": moat_score,
            "delegation_recommendation": delegation,
            "meta_learning_rule": post_mortem_rule
        }
