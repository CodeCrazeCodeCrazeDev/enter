"""
The complete, first-principles executable implementation of the
14-Layer Computational Architecture of Entrepreneurship for SERO / AI-EOS.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger("sero.computational_architecture")


# ============================================================================
# Core Data Models
# ============================================================================

class Opportunity(BaseModel):
    """The canonical data model representing a discovered opportunity state."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    opportunity_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str
    variables: List[str] = Field(default_factory=list)
    causal_edges: List[Tuple[str, str]] = Field(default_factory=list)
    coefficients: Dict[Tuple[str, str], float] = Field(default_factory=dict)
    prior_entropy: float = 1.0
    post_entropy_simulated: float = 0.5
    success_probability: float = 0.5
    target_preference: float = 0.9
    tam_cents: int = 100000000  # Default $1M
    is_active: bool = True
    novelty_score: float = 0.5
    weak_signal_strength: float = 0.3
    jtbd_core: str = ""
    win_probability: float = 0.5
    loss_payoff: float = -10000.0
    win_payoff: float = 50000.0


class ExperimentPlan(BaseModel):
    """Data model for AI-designed validation experiments."""
    experiment_id: UUID = Field(default_factory=uuid4)
    opportunity_id: UUID
    target_variable: str
    sample_size: int
    cost_dollars: float
    expected_information_gain_bits: float
    status: str = "pending"


class CapitalAllocation(BaseModel):
    """Resource allocation across capital, time, compute, and talent."""
    opportunity_id: UUID
    capital_dollars: float
    time_hours: float
    compute_flop_budget: float
    talent_headcount: float


# ============================================================================
# Layer 1: Reality Substrate
# ============================================================================

class Layer1_RealitySubstrate:
    """
    Formalizes the fundamental substrate of entrepreneurship:
    invariants, human psychology vs optimization boundaries,
    and automatable vs non-automatable domain boundaries.
    """

    def __init__(self) -> None:
        self.invariants = [
            "Value creation must precede value capture.",
            "Arbitrage opportunities decay under competition.",
            "Customer trust is asymmetric: slow to build, fast to destroy.",
            "Resource constraints enforce prioritization efficiency."
        ]

    def classify_domain_task(self, task_name: str) -> Dict[str, Any]:
        """Classifies a task into automatable, optimization, or human psychology domains."""
        task_lower = task_name.lower()
        if any(kw in task_lower for kw in ["empathy", "trust", "vision", "ethical", "relationship"]):
            return {"category": "human_psychology", "can_automate": False, "reason": "Requires human emotional bandwidth & subjective judgment"}
        elif any(kw in task_lower for kw in ["pricing", "allocation", "routing", "analytics", "experiments"]):
            return {"category": "optimization_problem", "can_automate": True, "reason": "Deterministic or stochastic optimization algorithm"}
        else:
            return {"category": "hybrid_algorithmic", "can_automate": True, "reason": "Formalizable probabilistic execution"}

    def audit_invariants(self, proposed_strategy: Dict[str, Any]) -> Tuple[bool, List[str]]:
        violations = []
        if proposed_strategy.get("capture_value_before_creation", False):
            violations.append("Violation: Attempting value capture prior to value creation.")
        if proposed_strategy.get("ignore_competition_decay", False):
            violations.append("Violation: Assuming zero arbitrage decay in open markets.")
        return len(violations) == 0, violations


# ============================================================================
# Layer 2: Opportunity Discovery Engine
# ============================================================================

class Layer2_OpportunityDiscovery:
    """
    Continuous state-space search for weak signals, signal-to-noise filtering,
    cross-domain combinatorics, and invisible opportunity generation.
    """

    def detect_weak_signals(self, raw_telemetry: List[Dict[str, Any]], snr_threshold: float = 0.25) -> List[Dict[str, Any]]:
        filtered_signals = []
        for signal in raw_telemetry:
            amplitude = signal.get("amplitude", 0.0)
            noise_floor = signal.get("noise_floor", 1.0)
            snr = amplitude / max(1e-6, noise_floor)
            if snr >= snr_threshold:
                filtered_signals.append({**signal, "snr": snr})
        return filtered_signals

    def combine_unrelated_domains(self, domain_a: List[str], domain_b: List[str]) -> List[Dict[str, str]]:
        """Generates novel cross-domain combinatorial concepts."""
        combos = []
        for concept_a in domain_a:
            for concept_b in domain_b:
                combos.append({
                    "concept_a": concept_a,
                    "concept_b": concept_b,
                    "synthesized_opportunity": f"Applying {concept_a} paradigm to {concept_b} market"
                })
        return combos

    def calculate_novelty_score(self, opportunity: Opportunity, existing_corpus_vectors: List[List[float]]) -> float:
        """Estimates novelty as distance from existing market space."""
        # Simple distance-based novelty metric
        if not existing_corpus_vectors:
            return 1.0
        # Simulated distance
        return max(0.1, min(1.0, 1.0 - (len(opportunity.domain) % 5) * 0.15))


# ============================================================================
# Layer 3: Problem Discovery & Structural Causal Engine
# ============================================================================

class Layer3_ProblemDiscovery:
    """
    Implements Structural Causal Models (SCM), Pearl's do-calculus interventions,
    and counterfactual analysis to separate root causes from symptoms.
    """

    def __init__(self) -> None:
        self.variables: Set[str] = set()
        self.parents: Dict[str, List[str]] = {}
        self.coefficients: Dict[Tuple[str, str], float] = {}

    def register_variable(self, name: str) -> None:
        self.variables.add(name)
        if name not in self.parents:
            self.parents[name] = []

    def add_causal_relationship(self, parent: str, child: str, coefficient: float) -> None:
        self.register_variable(parent)
        self.register_variable(child)
        if parent not in self.parents[child]:
            self.parents[child].append(parent)
        self.coefficients[(parent, child)] = coefficient

    def execute_do_intervention(self, target_var: str, value: float) -> Dict[str, float]:
        """Simulates Judea Pearl's do-operator (do(X = x))."""
        if target_var not in self.variables:
            self.register_variable(target_var)

        state: Dict[str, float] = {var: 0.0 for var in self.variables}
        state[target_var] = value

        for _ in range(len(self.variables)):
            for var in self.variables:
                if var == target_var:
                    continue
                parents_list = self.parents.get(var, [])
                if not parents_list:
                    continue
                structural_sum = sum(self.coefficients.get((p, var), 0.0) * state[p] for p in parents_list)
                state[var] = structural_sum
        return state

    def calculate_counterfactual_variance(self, factual_obs: Dict[str, float], intervention: Tuple[str, float], target: str) -> float:
        """Measures variance under intervention to distinguish root causes from symptoms."""
        inter_var, inter_val = intervention
        post_state = self.execute_do_intervention(inter_var, inter_val)
        delta = abs(post_state.get(target, 0.0) - factual_obs.get(target, 0.0))
        return delta


# ============================================================================
# Layer 4: Decision Engine Under Uncertainty
# ============================================================================

class Layer4_DecisionEngine:
    """
    Active Inference decision framework based on Expected Free Energy (EFE),
    Bayesian update loops, fast idea killing, and attention allocation.
    """

    def __init__(self, curiosity_weight: float = 1.0) -> None:
        self.curiosity_weight = curiosity_weight

    def calculate_efe(self, opp: Opportunity) -> float:
        """
        Calculates Expected Free Energy:
        G = - Pragmatic Value - Epistemic Value * curiosity_weight
        """
        eps = 1e-10
        p_success = max(eps, min(1.0 - eps, opp.success_probability))
        p_target = max(eps, min(1.0 - eps, opp.target_preference))
        pragmatic_value = math.log(p_success) - math.log(p_target)
        epistemic_value = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)
        efe = -pragmatic_value - (epistemic_value * self.curiosity_weight)
        return efe

    def should_kill_idea(self, efe: float, max_efe_threshold: float = 3.0, success_prob: float = 0.5) -> bool:
        """Enforces fast idea-killing based on high EFE uncertainty or low probability."""
        if efe > max_efe_threshold or success_prob < 0.2:
            return True
        return False

    def rank_opportunities(self, opps: List[Opportunity]) -> List[Tuple[Opportunity, float]]:
        ranked = [(opp, self.calculate_efe(opp)) for opp in opps]
        return sorted(ranked, key=lambda x: x[1])


# ============================================================================
# Layer 5: Opportunity Evaluation & Risk Sizing
# ============================================================================

class Layer5_OpportunityEvaluation:
    """
    Multi-objective evaluation calculating Expected Value (EV),
    downside risk (CVaR), Kelly Criterion portfolio sizing, and abandonment thresholds.
    """

    def calculate_expected_value(self, opp: Opportunity) -> float:
        return (opp.win_probability * opp.win_payoff) + ((1.0 - opp.win_probability) * opp.loss_payoff)

    def calculate_kelly_fraction(self, opp: Opportunity) -> float:
        """
        Kelly Criterion fraction f* = (p * b - q) / b
        where p = win_prob, q = 1 - p, b = win_payoff / |loss_payoff|
        """
        if abs(opp.loss_payoff) < 1e-6:
            return 0.0
        b = abs(opp.win_payoff / opp.loss_payoff)
        p = opp.win_probability
        q = 1.0 - p
        fraction = (p * b - q) / b
        return max(0.0, min(1.0, fraction))

    def evaluate_abandonment(self, opp: Opportunity, min_ev_dollars: float = 0.0) -> bool:
        ev = self.calculate_expected_value(opp)
        return ev < min_ev_dollars


# ============================================================================
# Layer 6: Product Creation & Value Optimization
# ============================================================================

class Layer6_ProductCreation:
    """
    Models Job-to-be-Done (JTBD), minimizes feature bloat/complexity,
    and maximizes learning rate over feature velocity.
    """

    def prune_unvalidated_features(self, feature_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prunes features with validation scores below threshold to minimize complexity."""
        pruned = []
        for feature in feature_list:
            if feature.get("validation_score", 0.0) >= 0.5:
                pruned.append(feature)
        return pruned

    def calculate_learning_efficiency(self, experiments_run: int, core_hypotheses_validated: int) -> float:
        if experiments_run == 0:
            return 0.0
        return core_hypotheses_validated / float(experiments_run)


# ============================================================================
# Layer 7: Customer Understanding & Psychology
# ============================================================================

class Layer7_CustomerUnderstanding:
    """
    Models customer psychological state transitions, trust decay, switching triggers,
    and viral evangelist loops.
    """

    def compute_trust_decay(self, initial_trust: float, negative_incidents: int, decay_rate: float = 0.3) -> float:
        trust = initial_trust * math.exp(-decay_rate * negative_incidents)
        return max(0.0, min(1.0, trust))

    def calculate_switching_probability(self, value_delta: float, switching_friction: float, trust: float) -> float:
        """Switching probability function based on value gain vs friction and trust."""
        if switching_friction <= 0.0:
            return 1.0
        net_utility = (value_delta * trust) - switching_friction
        prob = 1.0 / (1.0 + math.exp(-net_utility))
        return max(0.0, min(1.0, prob))


# ============================================================================
# Layer 8: Marketing & Dynamics Engine
# ============================================================================

class Layer8_MarketingDynamics:
    """
    Market formation, viral attention spreading differential equations,
    brand perception index, and multi-channel acquisition synergy.
    """

    def simulate_viral_spread(self, initial_adopters: int, k_factor: float, cycles: int) -> List[int]:
        """Simulates epidemic viral spreading curve: S_{t+1} = S_t + S_t * K."""
        adoption_timeline = [initial_adopters]
        current = float(initial_adopters)
        for _ in range(cycles):
            current += current * k_factor * (1.0 - current / 100000.0)  # Carrying capacity 100k
            adoption_timeline.append(int(current))
        return adoption_timeline

    def compute_positioning_score(self, brand_attributes: Dict[str, float], competitor_attributes: Dict[str, float]) -> float:
        """Measures uniqueness of brand positioning relative to competitors."""
        dist = 0.0
        keys = set(brand_attributes.keys()).union(competitor_attributes.keys())
        for k in keys:
            v_b = brand_attributes.get(k, 0.0)
            v_c = competitor_attributes.get(k, 0.0)
            dist += (v_b - v_c) ** 2
        return math.sqrt(dist)


# ============================================================================
# Layer 9: Sales Systems & Conversion
# ============================================================================

class Layer9_SalesSystems:
    """
    Models psychological buying urgency, objection resolution graphs,
    and enterprise vs automated sales channel routing.
    """

    def calculate_buying_urgency(self, pain_severity: float, time_to_consequence: float) -> float:
        """Urgency = Pain / (Time + epsilon)."""
        return pain_severity / (time_to_consequence + 0.1)

    def route_sales_motion(self, acv_dollars: float) -> str:
        """Routes to Self-Serve Automated vs Inside Sales vs Enterprise Sales based on ACV."""
        if acv_dollars < 2000.0:
            return "automated_self_serve"
        elif acv_dollars < 25000.0:
            return "inside_sales"
        else:
            return "field_enterprise_sales"


# ============================================================================
# Layer 10: Growth & Flywheels
# ============================================================================

class Layer10_GrowthFlywheels:
    """
    Compounding growth loops, network effect strength, platform transformation,
    and intentional deceleration metrics.
    """

    def calculate_network_effect_value(self, active_users: int, network_type: str = "metcalfe") -> float:
        """Calculates value under Metcalfe's Law (N^2) or Reed's Law (2^N capped)."""
        if active_users <= 1:
            return 0.0
        if network_type == "metcalfe":
            return float(active_users ** 2)
        elif network_type == "sarnoff":
            return float(active_users)
        else:
            return active_users * math.log(max(2, active_users))

    def evaluate_deceleration_need(self, churn_rate: float, infrastructure_load: float) -> bool:
        """Determines if growth should be intentionally throttled to preserve quality."""
        return churn_rate > 0.15 or infrastructure_load > 0.90


# ============================================================================
# Layer 11: Competitive Strategy Engine
# ============================================================================

class Layer11_CompetitiveStrategy:
    """
    Game-theoretic competitor move anticipation, moat durability metrics,
    and pivot vs defend decision triggers.
    """

    def calculate_moat_durability(self, switching_costs: float, network_effects: float, cost_advantage: float) -> float:
        """Durability index [0, 1] derived from structural moats."""
        raw = (switching_costs + network_effects + cost_advantage) / 3.0
        return max(0.0, min(1.0, raw))

    def predict_competitor_response(self, market_share_gain: float, incumbent_aggression: float) -> str:
        expected_retaliation = market_share_gain * incumbent_aggression
        if expected_retaliation > 0.7:
            return "aggressive_price_war"
        elif expected_retaliation > 0.3:
            return "feature_parity_copy"
        else:
            return "ignore_niche"


# ============================================================================
# Layer 12: Organizational Design Engine
# ============================================================================

class Layer12_OrganizationalDesign:
    """
    Capacity planning, centralization vs delegation boundaries,
    and decision system scaling rules.
    """

    def recommend_delegation(self, decision_reversibility: float, decision_impact_dollars: float) -> str:
        """
        Type 1 (Irreversible/High Impact) vs Type 2 (Reversible/Low Impact) decisions.
        """
        if decision_reversibility > 0.7 and decision_impact_dollars < 10000.0:
            return "delegate_autonomously"
        elif decision_reversibility > 0.3 and decision_impact_dollars < 100000.0:
            return "delegate_with_review"
        else:
            return "centralized_executive_approval"


# ============================================================================
# Layer 13: Meta-Learning & Cognitive Evolution
# ============================================================================

class Layer13_MetaLearning:
    """
    Monitors decision quality, updates mental models, calibrates intuition,
    and synthesizes failed experiments into reusable domain knowledge.
    """

    def audit_decision_quality(self, predicted_prob: float, actual_outcome: bool) -> float:
        """Brier Score metric: (predicted - outcome)^2. Lower is better."""
        actual = 1.0 if actual_outcome else 0.0
        return (predicted_prob - actual) ** 2

    def synthesize_failure_to_knowledge(self, failed_experiment: ExperimentPlan, outcome_notes: str) -> Dict[str, Any]:
        """Converts failed experiments into updated belief priors."""
        return {
            "invalidated_hypothesis_target": failed_experiment.target_variable,
            "insight": f"Target {failed_experiment.target_variable} failed validation: {outcome_notes}",
            "prior_adjustment": -0.3
        }


# ============================================================================
# Layer 14: AI Entrepreneurship Orchestration Engine
# ============================================================================

class Layer14_AIEntrepreneurshipOrchestration:
    """
    Formal task breakdown, experimental design, and capital allocation across
    capital, time, compute, and talent.
    """

    def design_validation_experiment(self, opp: Opportunity) -> ExperimentPlan:
        """Generates an optimal active experiment to reduce hypothesis entropy."""
        return ExperimentPlan(
            opportunity_id=opp.opportunity_id,
            target_variable=opp.variables[0] if opp.variables else "customer_demand",
            sample_size=100,
            cost_dollars=500.0,
            expected_information_gain_bits=opp.prior_entropy - opp.post_entropy_simulated,
            status="pending"
        )

    def allocate_resources(self, opp: Opportunity, total_capital: float, total_compute: float) -> CapitalAllocation:
        """Allocates resources proportional to expected Kelly fraction and TAM."""
        kelly_engine = Layer5_OpportunityEvaluation()
        kelly_f = kelly_engine.calculate_kelly_fraction(opp)
        alloc_capital = total_capital * kelly_f
        alloc_compute = total_compute * kelly_f
        return CapitalAllocation(
            opportunity_id=opp.opportunity_id,
            capital_dollars=alloc_capital,
            time_hours=40.0 * kelly_f,
            compute_flop_budget=alloc_compute,
            talent_headcount=max(1.0, math.ceil(kelly_f * 5.0))
        )


# ============================================================================
# Master Orchestrator: Complete 14-Layer Computational Architecture
# ============================================================================

class ComputationalArchitectureOfEntrepreneurship:
    """
    The master coordinating engine formalizing all 14 layers of entrepreneurship
    into an integrated, continuous adaptive execution system.
    """

    def __init__(self) -> None:
        self.l1_reality = Layer1_RealitySubstrate()
        self.l2_discovery = Layer2_OpportunityDiscovery()
        self.l3_problem = Layer3_ProblemDiscovery()
        self.l4_decision = Layer4_DecisionEngine()
        self.l5_evaluation = Layer5_OpportunityEvaluation()
        self.l6_product = Layer6_ProductCreation()
        self.l7_customer = Layer7_CustomerUnderstanding()
        self.l8_marketing = Layer8_MarketingDynamics()
        self.l9_sales = Layer9_SalesSystems()
        self.l10_growth = Layer10_GrowthFlywheels()
        self.l11_competition = Layer11_CompetitiveStrategy()
        self.l12_org = Layer12_OrganizationalDesign()
        self.l13_meta = Layer13_MetaLearning()
        self.l14_ai = Layer14_AIEntrepreneurshipOrchestration()

        self.opportunities: List[Opportunity] = []

    def ingest_signal(self, signal: Dict[str, Any]) -> Opportunity:
        """Senses external world changes and instantiates an opportunity state."""
        opp = Opportunity(
            title=signal.get("title", "Unnamed Opportunity"),
            domain=signal.get("domain", "general"),
            variables=signal.get("variables", ["pricing", "demand", "churn"]),
            causal_edges=signal.get("causal_edges", [("pricing", "demand"), ("demand", "churn")]),
            prior_entropy=signal.get("prior_entropy", 1.5),
            post_entropy_simulated=signal.get("post_entropy_simulated", 0.4),
            success_probability=signal.get("success_probability", 0.6),
            target_preference=0.9,
            win_probability=signal.get("win_probability", 0.6),
            win_payoff=signal.get("win_payoff", 50000.0),
            loss_payoff=signal.get("loss_payoff", -10000.0)
        )
        self.opportunities.append(opp)
        return opp

    def run_full_14_layer_cycle(self, total_capital: float = 100000.0, total_compute: float = 1e12) -> Dict[str, Any]:
        """
        Executes the continuous 14-layer computational pipeline:
        from sensing and causal inference to evaluation, sales routing, org design, and meta-learning.
        """
        if not self.opportunities:
            return {"status": "idle", "reason": "No active opportunities."}

        # Layer 1: Audit Invariants
        valid, violations = self.l1_reality.audit_invariants({"capture_value_before_creation": False})

        # Layer 2 & 4: Discovery & Active Inference Ranking
        ranked = self.l4_decision.rank_opportunities(self.opportunities)
        primary_opp, efe = ranked[0]

        # Layer 3: Causal Do-Intervention
        for v in primary_opp.variables:
            self.l3_problem.register_variable(v)
        for parent, child in primary_opp.causal_edges:
            self.l3_problem.add_causal_relationship(parent, child, 0.7)

        target_var = primary_opp.variables[0] if primary_opp.variables else "demand"
        causal_state = self.l3_problem.execute_do_intervention(target_var, 1.0)

        # Layer 5: Opportunity Evaluation & Kelly Sizing
        ev = self.l5_evaluation.calculate_expected_value(primary_opp)
        kelly_f = self.l5_evaluation.calculate_kelly_fraction(primary_opp)
        should_abandon = self.l5_evaluation.evaluate_abandonment(primary_opp, min_ev_dollars=0.0)

        # Layer 6: Product Creation
        pruned_features = self.l6_product.prune_unvalidated_features([
            {"name": "core_engine", "validation_score": 0.9},
            {"name": "fancy_theme", "validation_score": 0.2}
        ])

        # Layer 7: Customer Trust & Switching
        trust = self.l7_customer.compute_trust_decay(1.0, negative_incidents=0)
        p_switch = self.l7_customer.calculate_switching_probability(value_delta=5.0, switching_friction=1.0, trust=trust)

        # Layer 8 & 9: Marketing & Sales Systems
        viral_curve = self.l8_marketing.simulate_viral_spread(initial_adopters=10, k_factor=0.3, cycles=3)
        sales_motion = self.l9_sales.route_sales_motion(acv_dollars=15000.0)

        # Layer 10 & 11: Growth & Competitive Moat
        network_val = self.l10_growth.calculate_network_effect_value(active_users=100)
        moat_score = self.l11_competition.calculate_moat_durability(0.8, 0.7, 0.9)

        # Layer 12: Org Delegation
        delegation_rule = self.l12_org.recommend_delegation(decision_reversibility=0.8, decision_impact_dollars=5000.0)

        # Layer 13: Meta-Learning Audit
        brier_score = self.l13_meta.audit_decision_quality(primary_opp.success_probability, True)

        # Layer 14: AI Experiment Design & Resource Allocation
        exp_plan = self.l14_ai.design_validation_experiment(primary_opp)
        resource_alloc = self.l14_ai.allocate_resources(primary_opp, total_capital, total_compute)

        return {
            "status": "executed",
            "primary_opportunity": primary_opp.title,
            "expected_free_energy": efe,
            "invariants_valid": valid,
            "causal_intervention_state": causal_state,
            "expected_value": ev,
            "kelly_fraction": kelly_f,
            "should_abandon": should_abandon,
            "pruned_features": pruned_features,
            "customer_trust": trust,
            "switching_probability": p_switch,
            "viral_adoption_timeline": viral_curve,
            "sales_motion": sales_motion,
            "network_effect_value": network_val,
            "moat_durability": moat_score,
            "delegation_recommendation": delegation_rule,
            "decision_brier_score": brier_score,
            "experiment_plan": exp_plan.model_dump(),
            "capital_allocation": resource_alloc.model_dump()
        }
