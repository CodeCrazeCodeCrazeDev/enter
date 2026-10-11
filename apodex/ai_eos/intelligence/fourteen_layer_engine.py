"""
The executable Python engine for the 14-Layer Computational Architecture of Entrepreneurship.
Implements first-principles algorithms, feedback loops, decision systems, and state machines
across all 14 layers.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.fourteen_layer_engine")


# --- Domain Models ---

class EntrepreneurialSignal(BaseModel):
    """Raw signal sensed from external reality substrate (Layer 1 & 2)."""
    signal_id: UUID = Field(default_factory=uuid4)
    domain: str
    source: str
    raw_data: Dict[str, Any] = Field(default_factory=dict)
    entropy_score: float = 1.0
    signal_to_noise: float = 2.0


class DiscoveredOpportunity(BaseModel):
    """Discovered opportunity state (Layer 2 & 5)."""
    opportunity_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str
    bisociated_domains: List[str] = Field(default_factory=list)
    tam_cents: int = 500000000  # $5M TAM default
    prior_entropy: float = 1.2
    post_entropy_simulated: float = 0.3
    p_success: float = 0.6
    p_target_preference: float = 0.95
    downside_var: float = 50000.0  # $50k max downside risk
    is_active: bool = True


class ProblemNode(BaseModel):
    """Problem definition and structural decomposition (Layer 3)."""
    problem_id: UUID = Field(default_factory=uuid4)
    stated_symptom: str
    root_cause: str
    is_first_order: bool = True
    total_addressable_friction: float = 100000.0
    causal_parents: List[str] = Field(default_factory=list)


class JTBDDefinition(BaseModel):
    """Job-To-Be-Done product model (Layer 6)."""
    current_state: str
    desired_state: str
    transformation_delta: str
    core_features: List[str] = Field(default_factory=list)
    pruned_features: List[str] = Field(default_factory=list)
    mve_score: float = 0.85  # Minimum Viable Experiment information gain per cost unit


class CustomerPsychModel(BaseModel):
    """Customer psychology and trust model (Layer 7)."""
    customer_segment: str
    cognitive_cost: float = 0.2
    trust_score: float = 0.5
    switching_barrier: float = 1.0
    nps_score: float = 8.0


class SalesFunnelState(BaseModel):
    """Sales funnel state and conversion metrics (Layer 9)."""
    stage: str = "awareness"  # awareness -> interest -> evaluation -> commitment
    cost_of_inaction: float = 15000.0
    acv_cents: int = 1200000  # $12,000 ACV default
    is_automated: bool = True


# --- Layer Engines ---

class Layer1RealityEngine:
    """Layer 1: Reality Substrate - Analyzes non-equilibrium thermodynamic resource shifts."""

    def evaluate_thermodynamic_arbitrage(self, current_yield: float, potential_yield: float, friction: float) -> float:
        """Calculates economic arbitrage potential ΔV."""
        return max(0.0, potential_yield - current_yield - friction)

    def is_automatable_task(self, task_type: str) -> bool:
        """Determines automation boundaries based on empathy / sovereign judgment requirements."""
        non_automatable = {"human_empathy_relational", "sovereign_legal_accountability", "subjective_taste_grounding"}
        return task_type not in non_automatable


class Layer2OpportunityDiscoveryEngine:
    """Layer 2: Opportunity Discovery - Continuously searches state space for weak signals and bisociations."""

    def detect_weak_signal(self, signal: EntrepreneurialSignal, threshold: float = 1.5) -> bool:
        """Bayesian surprise filtering."""
        return signal.entropy_score * signal.signal_to_noise >= threshold

    def bisociate_domains(self, domain_a: str, domain_b: str) -> DiscoveredOpportunity:
        """Combines two disparate domain state spaces into a novel opportunity."""
        return DiscoveredOpportunity(
            title=f"Bisociated Arbitrage: {domain_a} x {domain_b}",
            domain=f"{domain_a}_{domain_b}",
            bisociated_domains=[domain_a, domain_b],
            prior_entropy=1.5,
            post_entropy_simulated=0.2,
            p_success=0.65
        )


class Layer3ProblemDiscoveryEngine:
    """Layer 3: Problem Discovery - Decomposes symptoms into root causes via causal DAG trees."""

    def decompose_problem(self, stated_symptom: str, causal_chain: List[str]) -> ProblemNode:
        """Traverses causal chain to isolate root bottleneck from surface symptoms."""
        root = causal_chain[-1] if causal_chain else stated_symptom
        return ProblemNode(
            stated_symptom=stated_symptom,
            root_cause=root,
            is_first_order=len(causal_chain) <= 1,
            causal_parents=causal_chain[:-1]
        )

    def should_ignore_problem(self, problem: ProblemNode, solve_cost: float) -> bool:
        """Abandons problems where Total Addressable Friction is lower than solve cost."""
        return problem.total_addressable_friction < solve_cost


class Layer4DecisionEngine:
    """Layer 4: Decision Making - Judea Pearl do-calculus and SPRT sequential probability ratio tests."""

    def evaluate_sprt_kill_switch(self, log_likelihood_ratios: List[float], lower_bound: float = -2.0) -> bool:
        """Sequential Probability Ratio Test (SPRT) to terminate bad hypotheses fast."""
        total_lambda = sum(log_likelihood_ratios)
        return total_lambda < lower_bound


class Layer5OpportunityEvaluationEngine:
    """Layer 5: Opportunity Evaluation - Active Inference Expected Free Energy (EFE) calculation."""

    def calculate_expected_free_energy(self, opp: DiscoveredOpportunity, curiosity_weight: float = 1.0) -> float:
        """
        Expected Free Energy G = - Pragmatic Value - Epistemic Value * curiosity_weight
        Pragmatic Value = ln(p_success) - ln(p_target_preference)
        Epistemic Value = prior_entropy - post_entropy_simulated
        """
        eps = 1e-9
        p_succ = max(eps, min(1.0 - eps, opp.p_success))
        p_target = max(eps, min(1.0 - eps, opp.p_target_preference))

        pragmatic_value = math.log(p_succ) - math.log(p_target)
        epistemic_value = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)

        return -pragmatic_value - (epistemic_value * curiosity_weight)

    def calculate_expected_value(self, opp: DiscoveredOpportunity, margin: float = 0.7, execution_cost: float = 100000.0) -> float:
        """EV = P_success * TAM * Margin - C_execution."""
        return (opp.p_success * (opp.tam_cents / 100.0) * margin) - execution_cost


class Layer6ProductCreationEngine:
    """Layer 6: Product Creation - Job-To-Be-Done discovery and feature pruning."""

    def formulate_jtbd(self, current: str, desired: str, feature_candidates: Dict[str, float]) -> JTBDDefinition:
        """Identifies core JTBD and prunes low-value features."""
        core = [f for f, value in feature_candidates.items() if value >= 0.5]
        pruned = [f for f, value in feature_candidates.items() if value < 0.5]
        return JTBDDefinition(
            current_state=current,
            desired_state=desired,
            transformation_delta=f"Transform from {current} to {desired}",
            core_features=core,
            pruned_features=pruned,
            mve_score=0.9
        )


class Layer7CustomerUnderstandingEngine:
    """Layer 7: Customer Understanding - Models customer utility functions and trust accumulation."""

    def update_trust(self, psych: CustomerPsychModel, delivery_delta: float, learning_rate: float = 0.1) -> float:
        """Trust(t) = Trust(t-1) + eta * (Delivery_actual - Expectation_promised)."""
        new_trust = psych.trust_score + (learning_rate * delivery_delta)
        psych.trust_score = max(0.0, min(1.0, new_trust))
        return psych.trust_score

    def will_customer_switch(self, psych: CustomerPsychModel, new_utility: float, old_utility: float) -> bool:
        """Customer switches if Delta U > Switching Barrier."""
        return (new_utility - old_utility) > psych.switching_barrier


class Layer8MarketingEngine:
    """Layer 8: Marketing - Epidemiological SIR viral attention spread models."""

    def calculate_viral_coefficient(self, infection_rate_beta: float, susceptible_pop: float, recovery_rate_gamma: float) -> float:
        """Viral Coefficient K = (beta * S) / gamma."""
        if recovery_rate_gamma <= 0:
            return 0.0
        return (infection_rate_beta * susceptible_pop) / recovery_rate_gamma


class Layer9SalesEngine:
    """Layer 9: Sales - Sales funnel state machines and Cost of Inaction (COI) urgency generation."""

    def advance_funnel(self, funnel: SalesFunnelState, buyer_action: str) -> str:
        """Advances sales funnel state."""
        transitions = {
            "awareness": "interest" if buyer_action == "inquire" else "awareness",
            "interest": "evaluation" if buyer_action == "demo" else "interest",
            "evaluation": "commitment" if buyer_action == "accept_quote" else "evaluation",
            "commitment": "commitment"
        }
        funnel.stage = transitions.get(funnel.stage, funnel.stage)
        return funnel.stage

    def should_automate_sales(self, acv_cents: int) -> bool:
        """Automates sales if ACV < $2,500; requires enterprise high-touch sales if ACV >= $25,000."""
        return acv_cents < 250000


class Layer10GrowthEngine:
    """Layer 10: Growth - Compounding growth dynamics and Metcalfe's Law network effects."""

    def calculate_metcalfe_value(self, num_nodes: int) -> float:
        """V = N^2."""
        return float(num_nodes ** 2)

    def calculate_compounding_users(self, initial_users: int, k_factor: float, reinvestment_ltv_cac: float, periods: int) -> int:
        """Compounds user growth over periods."""
        users = float(initial_users)
        growth_rate = k_factor + (reinvestment_ltv_cac * 0.1)
        for _ in range(periods):
            users = users * (1.0 + growth_rate)
        return int(users)


class Layer11CompetitionEngine:
    """Layer 11: Competition - Defensibility taxonomy and moat strength evaluation."""

    def evaluate_moat_score(self, moat_attributes: Dict[str, float]) -> float:
        """
        Moat taxonomy attributes: network_effects, switching_costs, cost_advantages, intangibles, counter_positioning.
        Score normalized between 0.0 and 1.0.
        """
        weights = {
            "network_effects": 0.3,
            "switching_costs": 0.25,
            "cost_advantages": 0.2,
            "intangibles": 0.15,
            "counter_positioning": 0.1
        }
        total_score = 0.0
        for attr, weight in weights.items():
            total_score += moat_attributes.get(attr, 0.0) * weight
        return max(0.0, min(1.0, total_score))


class Layer12OrganizationalDesignEngine:
    """Layer 12: Organizational Design - Capacity bottleneck detection and delegation triggers."""

    def should_trigger_hiring(self, work_demand: float, throughput_capacity: float, threshold: float = 1.2) -> bool:
        """Triggers hiring when Demand / Capacity > 1.2."""
        if throughput_capacity <= 0:
            return True
        return (work_demand / throughput_capacity) > threshold


class Layer13MetaLearningEngine:
    """Layer 13: Meta-Learning - Brier Score decision quality tracking and failure post-mortem learning."""

    def compute_brier_score(self, predictions: List[float], outcomes: List[int]) -> float:
        """Brier Score BS = (1/N) * sum((f_t - o_t)^2)."""
        if not predictions or len(predictions) != len(outcomes):
            return 1.0
        n = len(predictions)
        squared_diffs = [(p - o) ** 2 for p, o in zip(predictions, outcomes)]
        return sum(squared_diffs) / n


class Layer14AIEntrepreneurshipEngine:
    """Layer 14: Autonomous AI Entrepreneurship - Capital, compute, and talent allocation optimization."""

    def allocate_resources(self, projects: List[Dict[str, Any]], total_budget: float, risk_aversion_lambda: float = 0.5) -> Dict[str, float]:
        """
        Resource Allocation R* = argmax sum(EV_i - lambda * VaR_i) s.t. sum(R_i) <= Total Budget.
        """
        allocations = {}
        if not projects or total_budget <= 0:
            return allocations

        # Rank projects by net risk-adjusted return ratio
        scored_projects = []
        for p in projects:
            ev = p.get("ev", 0.0)
            var = p.get("var", 1.0)
            score = max(0.0, ev - (risk_aversion_lambda * var))
            scored_projects.append((p.get("name", "unnamed"), score))

        total_score = sum(s for _, s in scored_projects)
        if total_score <= 0:
            # Equal distribution if all scores non-positive
            equal_share = total_budget / len(projects)
            for p in projects:
                allocations[p.get("name", "unnamed")] = equal_share
            return allocations

        for name, score in scored_projects:
            allocations[name] = (score / total_score) * total_budget

        return allocations


# --- Master Orchestrator ---

class FourteenLayerComputationalEngine:
    """
    Master orchestrator driving an opportunity end-to-end through all 14 computational layers.
    """

    def __init__(self) -> None:
        self.layer1 = Layer1RealityEngine()
        self.layer2 = Layer2OpportunityDiscoveryEngine()
        self.layer3 = Layer3ProblemDiscoveryEngine()
        self.layer4 = Layer4DecisionEngine()
        self.layer5 = Layer5OpportunityEvaluationEngine()
        self.layer6 = Layer6ProductCreationEngine()
        self.layer7 = Layer7CustomerUnderstandingEngine()
        self.layer8 = Layer8MarketingEngine()
        self.layer9 = Layer9SalesEngine()
        self.layer10 = Layer10GrowthEngine()
        self.layer11 = Layer11CompetitionEngine()
        self.layer12 = Layer12OrganizationalDesignEngine()
        self.layer13 = Layer13MetaLearningEngine()
        self.layer14 = Layer14AIEntrepreneurshipEngine()

    def process_end_to_end_opportunity(
        self,
        signal: EntrepreneurialSignal,
        domain_b: str,
        causal_chain: List[str],
        feature_candidates: Dict[str, float],
        budget: float = 100000.0
    ) -> Dict[str, Any]:
        """
        Drives the signal through the complete 14-layer computational pipeline.
        """
        # Layer 1 & 2
        is_valid_signal = self.layer2.detect_weak_signal(signal)
        opp = self.layer2.bisociate_domains(signal.domain, domain_b)

        # Layer 3
        prob_node = self.layer3.decompose_problem(signal.domain, causal_chain)

        # Layer 4 & 5
        efe = self.layer5.calculate_expected_free_energy(opp)
        ev = self.layer5.calculate_expected_value(opp)

        # Layer 6 & 7
        jtbd = self.layer6.formulate_jtbd("unoptimized state", "automated state", feature_candidates)
        psych = CustomerPsychModel(customer_segment=opp.domain)
        updated_trust = self.layer7.update_trust(psych, delivery_delta=0.3)

        # Layer 8 & 9
        viral_k = self.layer8.calculate_viral_coefficient(0.05, 100.0, 2.0)
        sales_funnel = SalesFunnelState()
        self.layer9.advance_funnel(sales_funnel, "inquire")

        # Layer 10 & 11
        growth_users = self.layer10.calculate_compounding_users(100, k_factor=0.2, reinvestment_ltv_cac=1.5, periods=6)
        moat_score = self.layer11.evaluate_moat_score({"network_effects": 0.8, "switching_costs": 0.7})

        # Layer 12, 13, 14
        hiring_needed = self.layer12.should_trigger_hiring(work_demand=150.0, throughput_capacity=100.0)
        brier_score = self.layer13.compute_brier_score([opp.p_success], [1])
        resource_allocation = self.layer14.allocate_resources(
            projects=[{"name": opp.title, "ev": ev, "var": opp.downside_var}],
            total_budget=budget
        )

        return {
            "status": "orchestrated_successfully",
            "is_valid_signal": is_valid_signal,
            "opportunity_title": opp.title,
            "root_cause_problem": prob_node.root_cause,
            "expected_free_energy": efe,
            "expected_value": ev,
            "jtbd_core_features": jtbd.core_features,
            "customer_trust_score": updated_trust,
            "viral_coefficient": viral_k,
            "compounded_users_6_periods": growth_users,
            "moat_score": moat_score,
            "hiring_needed": hiring_needed,
            "brier_score": brier_score,
            "resource_allocation": resource_allocation
        }
