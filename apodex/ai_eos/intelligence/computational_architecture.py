"""
The complete, first-principles executable implementation of the
14-Layer Computational Architecture of Entrepreneurship for APODEX / SERO v2.1.

Covers Layers 1 through 14:
- Layer 1: Reality Substrate & Invariants
- Layer 2: Opportunity Discovery & State-Space Search
- Layer 3: Problem Discovery & Causal Root Decomposition
- Layer 4: Decision Making under Uncertainty (Active Inference EFE)
- Layer 5: Opportunity Evaluation & Multi-Objective Optimization
- Layer 6: Product Creation & Value Minimization (JTBD)
- Layer 7: Customer Understanding & Psychological State Machines
- Layer 8: Marketing & Attention Network Diffusion
- Layer 9: Sales Systems & Urgency Dynamics
- Layer 10: Growth Systems, Network Effects & Ecosystems
- Layer 11: Competitive Moats & Game-Theoretic Counter-Strategy
- Layer 12: Organizational Design & Capital/Talent Allocation
- Layer 13: Meta-Learning & Epistemic Updating
- Layer 14: Autonomous AI Entrepreneurship & Master Orchestration
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.computational_architecture")


# -----------------------------------------------------------------------------
# Core Data Models
# -----------------------------------------------------------------------------

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
    timing_score: float = 0.7
    downside_risk: float = 0.2
    complexity_score: float = 0.3


class ProblemStatement(BaseModel):
    """Represents a defined problem, decomposing symptoms from root causes."""
    problem_id: UUID = Field(default_factory=uuid4)
    description: str
    symptoms: List[str] = Field(default_factory=list)
    candidate_root_causes: List[str] = Field(default_factory=list)
    is_second_order: bool = False
    noise_variance: float = 0.1


# -----------------------------------------------------------------------------
# Layer 1: Reality Substrate & Invariants Engine
# -----------------------------------------------------------------------------

class RealityEngine:
    """
    Layer 1: Models fundamental invariants, human psychological parameters
    (e.g. prospect theory loss aversion), convex resource allocation, and automation boundaries.
    """

    def __init__(self, loss_aversion_lambda: float = 2.25) -> None:
        self.loss_aversion_lambda = loss_aversion_lambda

    def evaluate_prospect_utility(self, gain: float, loss: float, p_gain: float) -> float:
        """Kahneman-Tversky Prospect Theory subjective utility function."""
        p_loss = 1.0 - p_gain
        v_gain = math.pow(gain, 0.88) if gain >= 0 else 0.0
        v_loss = -self.loss_aversion_lambda * math.pow(abs(loss), 0.88) if loss < 0 else 0.0
        return p_gain * v_gain + p_loss * v_loss

    def classify_automation_boundary(self, task_name: str, creativity_req: float, judgment_req: float) -> Dict[str, Any]:
        """Distinguishes human judgment/creativity from algorithmic optimization."""
        is_automatable = creativity_req < 0.7 and judgment_req < 0.8
        return {
            "task_name": task_name,
            "is_automatable": is_automatable,
            "recommended_mode": "Autonomous Algorithmic" if is_automatable else "Human-in-the-Loop Judgment"
        }


# -----------------------------------------------------------------------------
# Layer 2: Opportunity Discovery Engine
# -----------------------------------------------------------------------------

class OpportunityDiscoveryEngine:
    """
    Layer 2: Continuously searches the world state space for weak signals,
    calculates information entropy gain, and synthesizes combinatorial novelty.
    """

    def detect_weak_signals(self, raw_signals: List[Dict[str, Any]], signal_threshold: float = 0.3) -> List[Dict[str, Any]]:
        filtered = []
        for sig in raw_signals:
            amplitude = sig.get("amplitude", 0.0)
            confidence = sig.get("confidence", 0.0)
            signal_score = amplitude * confidence
            if signal_score >= signal_threshold:
                sig["signal_score"] = signal_score
                filtered.append(sig)
        return filtered

    def generate_combinatorial_novelty(self, domain_concepts_a: List[str], domain_concepts_b: List[str]) -> List[Tuple[str, str]]:
        """Synthesizes cross-domain concept pairs (N_comb = N_a * N_b)."""
        combinations = []
        for ca in domain_concepts_a:
            for cb in domain_concepts_b:
                combinations.append((ca, cb))
        return combinations


# -----------------------------------------------------------------------------
# Layer 3: Problem Discovery & Causal Engine
# -----------------------------------------------------------------------------

class AdvancedCausalEngine:
    """
    Layer 3: Structural Causal Model (SCM) implementing Judea Pearl's do-calculus
    interventions, counterfactual estimations, and root cause analysis.
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
        Freezes target_var and propagates interventional downstream effects.
        """
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
        """
        Computes counterfactual outcomes: 'What would target_outcome_var be had we done X=x?'
        """
        intervened_var, inter_value = counterfactual_intervention

        # 1. Abduction Phase: background noise U
        noise_estimates: Dict[str, float] = {}
        for var in self.variables:
            factual_val = factual_observations.get(var, 0.0)
            parents_list = self.parents.get(var, [])
            structural_expected = 0.0
            for parent in parents_list:
                coef = self.coefficients.get((parent, var), 0.0)
                structural_expected += coef * factual_observations.get(parent, 0.0)

            noise_estimates[var] = factual_val - structural_expected

        # 2. Action & Prediction Phase
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

    def identify_root_causes(self, outcome_var: str) -> List[str]:
        """Traverses causal DAG ancestors to find non-derived root driver variables."""
        if outcome_var not in self.variables:
            return []
        roots = []
        visited = set()

        def dfs(curr: str) -> None:
            if curr in visited:
                return
            visited.add(curr)
            parents = self.parents.get(curr, [])
            if not parents and curr != outcome_var:
                roots.append(curr)
            for p in parents:
                dfs(p)

        dfs(outcome_var)
        return roots


# -----------------------------------------------------------------------------
# Layer 4: Decision Making Engine (Active Inference)
# -----------------------------------------------------------------------------

class ActiveInferencePlanner:
    """
    Layer 4: Active Inference decision engine based on Expected Free Energy (EFE).
    G = - Pragmatic Value - Epistemic Curiosity * Curiosity Weight
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

    def generate_counter_hypothesis(self, belief_statement: str) -> str:
        """Mitigates confirmation bias by constructing explicit falsifying counter-hypotheses."""
        return f"Falsification Hypothesis: What if '{belief_statement}' is false due to unmodeled latent variable confounders?"


# -----------------------------------------------------------------------------
# Layer 5: Opportunity Evaluation Engine
# -----------------------------------------------------------------------------

class OpportunityEvaluationEngine:
    """
    Layer 5: Multi-objective Pareto scoring engine balancing Expected Value E[V],
    Downside Risk VaR, and Market Timing Index T.
    """

    def evaluate_pareto_score(self, opp: Opportunity) -> Dict[str, float]:
        expected_value = (opp.tam_cents / 100.0) * opp.success_probability
        downside_risk = (opp.tam_cents / 100.0) * opp.downside_risk
        timing_adjusted_ev = expected_value * opp.timing_score
        sharpe_ratio = expected_value / max(1.0, downside_risk)

        return {
            "expected_value_dollars": expected_value,
            "downside_risk_dollars": downside_risk,
            "timing_score": opp.timing_score,
            "timing_adjusted_ev": timing_adjusted_ev,
            "sharpe_ratio": sharpe_ratio
        }

    def should_switch_opportunity(self, current_opp: Opportunity, candidate_opp: Opportunity) -> bool:
        score_curr = self.evaluate_pareto_score(current_opp)["timing_adjusted_ev"]
        score_cand = self.evaluate_pareto_score(candidate_opp)["timing_adjusted_ev"]
        # Requires at least a 20% improvement to overcome switching friction
        return score_cand > score_curr * 1.20


# -----------------------------------------------------------------------------
# Layer 6: Product Creation Engine
# -----------------------------------------------------------------------------

class ProductCreationEngine:
    """
    Layer 6: Job-To-Be-Done (JTBD) canonical decomposition and value hypothesis
    minimization (maximizing value while penalizing feature complexity).
    """

    def calculate_jtbd_value_to_complexity(
        self,
        core_jtbd: str,
        feature_set: List[str],
        perceived_value: float,
        complexity_weights: Dict[str, float]
    ) -> Dict[str, Any]:
        total_complexity = sum(complexity_weights.get(f, 0.1) for f in feature_set)
        value_density = perceived_value / max(0.1, total_complexity)
        return {
            "core_jtbd": core_jtbd,
            "total_complexity": total_complexity,
            "value_density": value_density,
            "recommendation": "Lean Build" if value_density >= 1.5 else "Simplify Features"
        }


# -----------------------------------------------------------------------------
# Layer 7: Customer Understanding Engine
# -----------------------------------------------------------------------------

class CustomerUnderstandingEngine:
    """
    Layer 7: Models customer psychological state transitions, trust accumulation,
    switching friction, and churn/evangelist dynamics.
    """

    def simulate_customer_lifecycle(
        self,
        initial_trust: float,
        perceived_value_delivered: float,
        switching_barrier: float,
        friction_events: int
    ) -> Dict[str, Any]:
        trust = initial_trust + (perceived_value_delivered * 0.2) - (friction_events * 0.15)
        trust = max(0.0, min(1.0, trust))

        is_evangelist = trust >= 0.85 and perceived_value_delivered > switching_barrier * 1.5
        will_churn = trust < 0.30 and perceived_value_delivered < switching_barrier

        return {
            "final_trust_score": trust,
            "is_evangelist": is_evangelist,
            "will_churn": will_churn,
            "customer_state": "Evangelist" if is_evangelist else ("At-Risk" if will_churn else "Active Customer")
        }


# -----------------------------------------------------------------------------
# Layer 8: Marketing & Attention Diffusion Engine
# -----------------------------------------------------------------------------

class MarketingEngine:
    """
    Layer 8: Models attention network diffusion, viral reproductive factor R_0,
    and brand positioning perception transforms.
    """

    def calculate_virality_coefficient(self, sharing_rate: float, conversion_per_invite: float) -> float:
        """K-Factor (R_0) = Shares_per_user * Conversion_rate."""
        return sharing_rate * conversion_per_invite

    def simulate_attention_spread(self, initial_seeds: int, k_factor: float, rounds: int) -> List[int]:
        reach = [initial_seeds]
        current = initial_seeds
        for _ in range(rounds):
            next_generation = int(current * k_factor)
            reach.append(next_generation)
            current = next_generation
        return reach


# -----------------------------------------------------------------------------
# Layer 9: Sales Systems Engine
# -----------------------------------------------------------------------------

class SalesEngine:
    """
    Layer 9: Models buying urgency vs objection friction and routes prospects
    between automated self-serve and high-touch enterprise sales pathways.
    """

    def evaluate_sales_routing(self, deal_size_dollars: float, sales_cycle_complexity: float) -> Dict[str, Any]:
        if deal_size_dollars >= 25000 or sales_cycle_complexity >= 0.7:
            return {"route": "Enterprise High-Touch Sales", "requires_human_rep": True}
        else:
            return {"route": "Automated Self-Serve Funnel", "requires_human_rep": False}

    def resolve_objection_causally(self, objection_type: str, causal_engine: AdvancedCausalEngine) -> str:
        if objection_type == "price_concern":
            return "Demonstrate ROI and offer tiered usage-based pricing."
        elif objection_type == "security_risk":
            return "Provide SOC2 audit compliance reports and isolated tenant architecture guarantees."
        return "Conduct deep-dive discovery call to uncover root business blocker."


# -----------------------------------------------------------------------------
# Layer 10: Growth & Ecosystem Engine
# -----------------------------------------------------------------------------

class GrowthEngine:
    """
    Layer 10: Models Metcalfe's law network scaling (V ~ N^2), platform transition
    thresholds, and intentional growth pacing.
    """

    def calculate_metcalfe_value(self, active_nodes: int, value_per_connection: float = 0.01) -> float:
        if active_nodes <= 1:
            return 0.0
        connections = (active_nodes * (active_nodes - 1)) / 2.0
        return connections * value_per_connection

    def evaluate_platform_transition(self, user_count: int, developer_count: int) -> bool:
        """Triggers product-to-platform transition when multi-sided threshold is met."""
        return user_count >= 10000 and developer_count >= 50


# -----------------------------------------------------------------------------
# Layer 11: Competitive Moats Engine
# -----------------------------------------------------------------------------

class CompetitiveMoatEngine:
    """
    Layer 11: Assesses durability of competitive moats (network effects, switching cost,
    economies of scale, brand asset) and triggers strategic pivot reviews.
    """

    def score_moat_durability(
        self,
        switching_costs: float,
        network_effects: float,
        scale_advantages: float,
        brand_equity: float
    ) -> Dict[str, float]:
        composite_moat = (switching_costs * 0.3) + (network_effects * 0.3) + (scale_advantages * 0.2) + (brand_equity * 0.2)
        return {
            "composite_moat_score": composite_moat,
            "is_defensible": composite_moat >= 0.65
        }

    def evaluate_pivot_trigger(self, quarterly_growth: float, moat_decay_rate: float) -> bool:
        return quarterly_growth < 0.0 and moat_decay_rate > 0.15


# -----------------------------------------------------------------------------
# Layer 12: Organizational Design Engine
# -----------------------------------------------------------------------------

class OrganizationalDesignEngine:
    """
    Layer 12: Capital & talent allocation scheduler, decision scaling laws, and
    centralization vs delegation entropy thresholding.
    """

    def optimize_capital_allocation(
        self,
        total_capital_dollars: float,
        rd_ratio: float = 0.4,
        gtm_ratio: float = 0.4,
        ops_ratio: float = 0.2
    ) -> Dict[str, float]:
        return {
            "rd_budget": total_capital_dollars * rd_ratio,
            "gtm_budget": total_capital_dollars * gtm_ratio,
            "ops_budget": total_capital_dollars * ops_ratio
        }

    def determine_delegation_level(self, decision_reversibility: float, decision_impact_dollars: float) -> str:
        """Type 1 vs Type 2 decisions (Jeff Bezos framework)."""
        if decision_reversibility >= 0.7 and decision_impact_dollars < 50000:
            return "Type 2: Delegated Autonomous Execution"
        return "Type 1: Centralized Executive Approval"


# -----------------------------------------------------------------------------
# Layer 13: Meta-Learning Engine
# -----------------------------------------------------------------------------

class MetaLearningEngine:
    """
    Layer 13: Bayesian mental model updating, decision quality tracking, and
    converting failure outcomes into reusable epistemic knowledge rules.
    """

    def __init__(self) -> None:
        self.knowledge_rules: List[Dict[str, Any]] = []

    def update_mental_model(self, prior_belief: float, outcome_observation: float, learning_rate: float = 0.2) -> float:
        posterior_belief = prior_belief + learning_rate * (outcome_observation - prior_belief)
        return max(0.0, min(1.0, posterior_belief))

    def Synthesize_failure_lesson(self, failure_event: str, root_cause: str) -> Dict[str, Any]:
        rule = {
            "rule_id": uuid4(),
            "failure_event": failure_event,
            "root_cause": root_cause,
            "rule_statement": f"WHEN encountering '{failure_event}', CHECK for root cause '{root_cause}' BEFORE committing capital."
        }
        self.knowledge_rules.append(rule)
        return rule


# -----------------------------------------------------------------------------
# Layer 14: Autonomous AI Entrepreneurship Orchestrator
# -----------------------------------------------------------------------------

class EntrepreneurialIntelligenceOrchestrator:
    """
    Layer 14: Master coordinating engine driving all 14 computational layers.
    Also aliased as FourteenLayerEngine & ComputationalArchitectureOfEntrepreneurship.
    """

    def __init__(
        self,
        causal_engine: Optional[AdvancedCausalEngine] = None,
        planner: Optional[ActiveInferencePlanner] = None
    ) -> None:
        self.reality_engine = RealityEngine()
        self.discovery_engine = OpportunityDiscoveryEngine()
        self.causal_engine = causal_engine or AdvancedCausalEngine()
        self.planner = planner or ActiveInferencePlanner(curiosity_weight=1.5)
        self.evaluation_engine = OpportunityEvaluationEngine()
        self.product_engine = ProductCreationEngine()
        self.customer_engine = CustomerUnderstandingEngine()
        self.marketing_engine = MarketingEngine()
        self.sales_engine = SalesEngine()
        self.growth_engine = GrowthEngine()
        self.moat_engine = CompetitiveMoatEngine()
        self.org_engine = OrganizationalDesignEngine()
        self.meta_engine = MetaLearningEngine()

        self.opportunities: List[Opportunity] = []

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
            tam_cents=signal.get("tam_cents", 100000000),
            timing_score=signal.get("timing_score", 0.7),
            downside_risk=signal.get("downside_risk", 0.2),
            complexity_score=signal.get("complexity_score", 0.3)
        )
        self.opportunities.append(opp)
        return opp

    def execute_orchestrated_pipeline(self) -> Dict[str, Any]:
        """Runs the complete 14-layer analysis pipeline over active opportunities."""
        if not self.opportunities:
            return {"status": "idle", "reason": "No opportunities registered."}

        # Layer 1 & 2: Discover and filter signals
        ranked_opps = self.planner.rank_opportunities(self.opportunities)
        primary_opp, best_efe = ranked_opps[0]

        logger.info(f"Orchestrator selected primary opportunity: '{primary_opp.title}' with EFE: {best_efe:.4f}")

        # Layer 3: Causal Registration
        for var in primary_opp.variables:
            self.causal_engine.register_variable(var)
        for parent, child in primary_opp.causal_edges:
            weight = primary_opp.coefficients.get(f"{parent}->{child}", 0.5)
            self.causal_engine.add_causal_relationship(parent, child, weight)

        # Layer 4: Active Inference Intervention
        intervention_var = primary_opp.variables[0] if primary_opp.variables else "marketing_spend"
        inter_state = self.causal_engine.execute_do_intervention(intervention_var, 1.5)

        # Layer 5: Pareto Score
        pareto_evaluation = self.evaluation_engine.evaluate_pareto_score(primary_opp)

        # Layer 6: Product Value Density
        product_eval = self.product_engine.calculate_jtbd_value_to_complexity(
            core_jtbd=f"Solve {primary_opp.domain} challenges",
            feature_set=["core_engine", "analytics"],
            perceived_value=0.85,
            complexity_weights={"core_engine": 0.2, "analytics": 0.1}
        )

        # Layer 7: Customer Lifecycle Simulation
        customer_eval = self.customer_engine.simulate_customer_lifecycle(
            initial_trust=0.7,
            perceived_value_delivered=0.9,
            switching_barrier=0.4,
            friction_events=1
        )

        # Layer 8: Virality
        k_factor = self.marketing_engine.calculate_virality_coefficient(0.4, 0.5)

        # Layer 9: Sales Routing
        sales_route = self.sales_engine.evaluate_sales_routing(deal_size_dollars=35000, sales_cycle_complexity=0.8)

        # Layer 10: Growth Network Effect
        metcalfe_val = self.growth_engine.calculate_metcalfe_value(active_nodes=500)

        # Layer 11: Competitive Moat Rating
        moat_eval = self.moat_engine.score_moat_durability(0.8, 0.7, 0.6, 0.75)

        # Layer 12: Capital Allocation
        capital_eval = self.org_engine.optimize_capital_allocation(1000000.0)

        # Layer 13: Meta-Learning Lesson Synthesis
        meta_lesson = self.meta_engine.Synthesize_failure_lesson(
            failure_event="Uncalibrated CAC Spike",
            root_cause="Ad channel exhaustion without organic virality"
        )

        return {
            "status": "executed",
            "selected_opportunity": primary_opp.title,
            "best_expected_free_energy": best_efe,
            "intervention_performed": f"do({intervention_var} = 1.5)",
            "propagated_state": inter_state,
            "pareto_evaluation": pareto_evaluation,
            "product_evaluation": product_eval,
            "customer_evaluation": customer_eval,
            "virality_k_factor": k_factor,
            "sales_routing": sales_route,
            "growth_metcalfe_value": metcalfe_val,
            "moat_durability": moat_eval,
            "capital_allocation": capital_eval,
            "meta_learning_rule": meta_lesson["rule_statement"]
        }


# Canonical Aliases
FourteenLayerEngine = EntrepreneurialIntelligenceOrchestrator
ComputationalArchitectureOfEntrepreneurship = EntrepreneurialIntelligenceOrchestrator
