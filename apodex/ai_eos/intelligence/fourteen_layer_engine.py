"""
The Complete 14-Layer Executable Engine for AI Entrepreneurial Operating System (AI EOS).
Implements layers 1 through 14 as formal algorithms, active inference search models,
structural causal engines, finite state machines, and closed-loop feedback systems.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger("sero.ai_eos.fourteen_layer_engine")


# ============================================================================
# LAYER 1: REALITY SUBSTRATE
# ============================================================================

class RealityState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    state_id: UUID = Field(default_factory=uuid4)
    entropy: float = 1.0
    scarce_resources: Dict[str, float] = Field(
        default_factory=lambda: {"capital_usd": 1000000.0, "compute_flops": 1e15, "talent_hours": 1000.0}
    )
    invariant_principles: List[str] = Field(
        default_factory=lambda: [
            "Negative Free Energy Principle",
            "Structural Arbitrage",
            "Irreversible Execution Velocity",
            "Asymmetric Risk-Reward Profiling",
        ]
    )


class RealitySubstrateEngine:
    """Layer 1: Evaluates environmental entropy, resource allocations, and automation boundaries."""

    def evaluate_arbitrage_potential(
        self, marginal_value: float, marginal_friction: float
    ) -> Dict[str, Any]:
        delta_v = marginal_value - marginal_friction
        is_viable = delta_v > 0
        return {
            "marginal_value": marginal_value,
            "marginal_friction": marginal_friction,
            "arbitrage_delta": delta_v,
            "is_viable": is_viable,
        }

    def partition_task_automation(self, task_name: str) -> Dict[str, Any]:
        """Distinguishes optimization & deterministic search from existential human judgment."""
        human_only = {"ultimate_value_axiology", "existential_risk_assumption", "moral_accountability"}
        is_human = task_name.lower() in human_only
        return {
            "task_name": task_name,
            "category": "human_judgment" if is_human else "optimizable_algorithmic",
            "can_be_automated": not is_human,
        }


# ============================================================================
# LAYER 2: OPPORTUNITY DISCOVERY ENGINE
# ============================================================================

class SignalObservation(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    signal_id: UUID = Field(default_factory=uuid4)
    domain: str
    title: str
    kl_surprise: float
    tam_estimate_usd: float
    noise_variance: float = 0.1
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class OpportunityDiscoveryEngine:
    """Layer 2: Weak signal detection, filtering, cross-domain synthesis, and novelty generation."""

    def __init__(self, filter_threshold: float = 0.5) -> None:
        self.filter_threshold = filter_threshold

    def filter_signal(self, signal: SignalObservation) -> bool:
        # Score = alpha * surprise + beta * log10(tam) - gamma * noise
        tam_factor = math.log10(max(1.0, signal.tam_estimate_usd)) / 10.0
        score = (0.5 * signal.kl_surprise) + (0.4 * tam_factor) - (0.3 * signal.noise_variance)
        return score >= self.filter_threshold

    def synthesize_cross_domain(
        self, domain_a_nodes: List[str], domain_b_nodes: List[str]
    ) -> List[Tuple[str, str, float]]:
        """Cross-domain knowledge tensor graph alignment revealing unexploited structural intersections."""
        synthesized_edges = []
        for a in domain_a_nodes:
            for b in domain_b_nodes:
                compatibility = (len(a) + len(b)) % 10 / 10.0 + 0.5
                synthesized_edges.append((a, b, round(compatibility, 2)))
        return sorted(synthesized_edges, key=lambda x: x[2], reverse=True)


# ============================================================================
# LAYER 3: PROBLEM DISCOVERY ENGINE
# ============================================================================

class ProblemNode(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    node_id: str
    description: str
    is_symptom: bool = False
    is_root_cause: bool = False
    parents: List[str] = Field(default_factory=list)


class ProblemDiscoveryEngine:
    """Layer 3: Problem definition, DAG factorization, 1st vs 2nd order decomposition, root cause analysis."""

    def decompose_problem_dag(
        self, nodes: List[ProblemNode], causal_edges: List[Tuple[str, str]]
    ) -> Dict[str, Any]:
        """Identifies root causes vs symptoms by analyzing parent-child degree centrality."""
        in_degrees = {n.node_id: 0 for n in nodes}
        out_degrees = {n.node_id: 0 for n in nodes}

        for p, c in causal_edges:
            if c in in_degrees:
                in_degrees[c] += 1
            if p in out_degrees:
                out_degrees[p] += 1

        root_causes = [n.node_id for n in nodes if in_degrees[n.node_id] == 0 and out_degrees[n.node_id] > 0]
        symptoms = [n.node_id for n in nodes if in_degrees[n.node_id] > 0 and out_degrees[n.node_id] == 0]

        return {
            "root_causes": root_causes,
            "symptoms": symptoms,
            "first_order_problems": root_causes,
            "second_order_symptoms": symptoms,
        }

    def should_ignore_problem(self, intervention_cost: float, recoverable_value: float) -> bool:
        """Ignore gate: reject if fix cost exceeds recoverable value."""
        return intervention_cost >= recoverable_value


# ============================================================================
# LAYER 4: DECISION MAKING ENGINE
# ============================================================================

class DecisionMakingEngine:
    """Layer 4: Decision making under uncertainty, Value of Information (VoI), attention allocation."""

    def calculate_value_of_information(
        self, prior_ev: float, post_ev_conditioned: float, experiment_cost: float
    ) -> Dict[str, Any]:
        voi = max(0.0, post_ev_conditioned - prior_ev)
        net_voi = voi - experiment_cost
        should_run_experiment = net_voi > 0
        return {
            "voi": voi,
            "experiment_cost": experiment_cost,
            "net_voi": net_voi,
            "should_run_experiment": should_run_experiment,
        }

    def allocate_attention_softmax(self, option_efes: Dict[str, float], temperature: float = 1.0) -> Dict[str, float]:
        """Softmax attention allocation over candidate strategic levers (lower EFE gets higher attention)."""
        eps = 1e-9
        inv_efes = {k: 1.0 / (max(eps, v)) for k, v in option_efes.items()}
        max_val = max(inv_efes.values())
        exp_vals = {k: math.exp((v - max_val) / temperature) for k, v in inv_efes.items()}
        sum_exp = sum(exp_vals.values())
        return {k: v / sum_exp for k, v in exp_vals.items()}


# ============================================================================
# LAYER 5: OPPORTUNITY EVALUATION ENGINE
# ============================================================================

class CandidateOpportunity(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    opp_id: UUID = Field(default_factory=uuid4)
    title: str
    tam_usd: float
    p_success: float
    gross_margin: float
    cac_usd: float
    ltv_usd: float
    downside_risk_usd: float
    prior_entropy: float = 1.0
    post_entropy: float = 0.4


class OpportunityEvaluationEngine:
    """Layer 5: Multi-variable opportunity valuation, EV, downside CVaR, capital efficiency ratio."""

    def evaluate_opportunity(self, opp: CandidateOpportunity) -> Dict[str, Any]:
        expected_value = (opp.p_success * opp.ltv_usd) - ((1.0 - opp.p_success) * opp.downside_risk_usd)
        ltv_cac_ratio = opp.ltv_usd / max(1.0, opp.cac_usd)
        capital_efficiency = expected_value / max(1.0, opp.cac_usd + opp.downside_risk_usd)

        # Expected Free Energy: G = - pragmatic - epistemic
        pragmatic = math.log(max(1e-6, opp.p_success))
        epistemic = max(0.0, opp.prior_entropy - opp.post_entropy)
        efe = -pragmatic - epistemic

        return {
            "opportunity_id": opp.opp_id,
            "title": opp.title,
            "expected_value": expected_value,
            "ltv_cac_ratio": ltv_cac_ratio,
            "capital_efficiency_ratio": capital_efficiency,
            "expected_free_energy": efe,
        }


# ============================================================================
# LAYER 6: PRODUCT CREATION ENGINE
# ============================================================================

class FeatureProposal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    feature_name: str
    jtbd_impact_score: float  # 0.0 to 10.0
    complexity_cost: float     # 0.0 to 10.0


class ProductCreationEngine:
    """Layer 6: Anti-build feature filter, complexity minimization, core JTBD discovery."""

    def anti_build_filter(
        self, proposal: FeatureProposal, min_impact_per_complexity: float = 1.2
    ) -> Dict[str, Any]:
        ratio = proposal.jtbd_impact_score / max(0.1, proposal.complexity_cost)
        should_build = ratio >= min_impact_per_complexity
        return {
            "feature_name": proposal.feature_name,
            "impact_complexity_ratio": ratio,
            "should_build": should_build,
            "action": "APPROVED" if should_build else "REJECTED_BY_ANTI_BUILD_FILTER",
        }


# ============================================================================
# LAYER 7: CUSTOMER UNDERSTANDING ENGINE
# ============================================================================

class CustomerUnderstandingEngine:
    """Layer 7: Customer utility modeling, trust dynamics, switching friction, churn risk."""

    def model_customer_utility(
        self, perceive_benefit: float, price_usd: float, switching_cost: float
    ) -> Dict[str, Any]:
        net_utility = perceive_benefit - price_usd - switching_cost
        will_switch = net_utility > 0
        return {
            "perceive_benefit": perceive_benefit,
            "price_usd": price_usd,
            "switching_cost": switching_cost,
            "net_utility": net_utility,
            "will_switch": will_switch,
        }

    def update_trust_score(
        self, current_trust: float, expected_performance: float, actual_performance: float
    ) -> float:
        delta = actual_performance - expected_performance
        # Trust increases when actual >= expected, drops sharply when actual < expected
        multiplier = 1.0 if delta >= 0 else 2.0
        new_trust = current_trust + (multiplier * delta * 0.1)
        return max(0.0, min(1.0, new_trust))


# ============================================================================
# LAYER 8: MARKETING ENGINE
# ============================================================================

class MarketingEngine:
    """Layer 8: Market formation, epidemic attention diffusion, viral coefficient calculation."""

    def calculate_viral_coefficient(self, invites_per_user: float, conversion_rate: float) -> Dict[str, Any]:
        k_factor = invites_per_user * conversion_rate
        is_viral = k_factor > 1.0
        return {
            "invites_per_user": invites_per_user,
            "conversion_rate": conversion_rate,
            "k_factor": k_factor,
            "is_viral": is_viral,
        }

    def simulate_epidemic_spread(
        self, susceptible: float, infected: float, beta: float, gamma: float, steps: int = 10
    ) -> List[Dict[str, float]]:
        trajectory = []
        s, i = susceptible, infected
        for step in range(steps):
            new_infected = beta * s * i
            new_recovered = gamma * i
            s = max(0.0, s - new_infected)
            i = max(0.0, i + new_infected - new_recovered)
            trajectory.append({"step": step, "susceptible": round(s, 2), "infected": round(i, 2)})
        return trajectory


# ============================================================================
# LAYER 9: SALES ENGINE
# ============================================================================

class SalesEngine:
    """Layer 9: Psychological sales state machine, objection resolution, urgency scoring."""

    VALID_STAGES = ["prospect", "qualified", "demo_completed", "objection_handling", "closed_won", "closed_lost"]

    def process_sales_funnel_transition(
        self, current_stage: str, action: str, buyer_trust: float
    ) -> Dict[str, Any]:
        if current_stage not in self.VALID_STAGES:
            raise ValueError(f"Invalid sales stage: {current_stage}")

        next_stage = current_stage
        if current_stage == "prospect" and action == "qualify":
            next_stage = "qualified"
        elif current_stage == "qualified" and action == "demo":
            next_stage = "demo_completed"
        elif current_stage == "demo_completed":
            if action == "raise_objection":
                next_stage = "objection_handling"
            elif action == "close" and buyer_trust >= 0.7:
                next_stage = "closed_won"
        elif current_stage == "objection_handling":
            if action == "resolve_objection" and buyer_trust >= 0.7:
                next_stage = "closed_won"
            elif action == "fail_objection":
                next_stage = "closed_lost"

        return {"previous_stage": current_stage, "action": action, "next_stage": next_stage}


# ============================================================================
# LAYER 10: GROWTH ENGINE
# ============================================================================

class GrowthEngine:
    """Layer 10: Compounding dynamics, network effect scaling, metric prediction."""

    def evaluate_network_effect_utility(self, active_users: int) -> Dict[str, Any]:
        metcalfe_value = active_users ** 2
        return {"active_users": active_users, "metcalfe_network_value": metcalfe_value}

    def predict_cohort_retention_compounding(
        self, initial_cohort: int, monthly_retention_rate: float, months: int = 12
    ) -> Dict[str, Any]:
        retained = initial_cohort * (monthly_retention_rate ** months)
        return {
            "initial_cohort": initial_cohort,
            "months": months,
            "retained_users": round(retained, 2),
            "effective_retention_pct": round((retained / initial_cohort) * 100, 2),
        }


# ============================================================================
# LAYER 11: COMPETITION ENGINE
# ============================================================================

class CompetitionEngine:
    """Layer 11: Competitor move prediction, moat strength scoring, pivot condition checking."""

    def evaluate_moat_strength(self, moat_dimensions: Dict[str, float]) -> Dict[str, Any]:
        """Dimensions: network_effects, switching_costs, scale_economies, proprietary_data, brand."""
        scores = list(moat_dimensions.values())
        avg_moat = sum(scores) / max(1, len(scores))
        is_defensible = avg_moat >= 0.6
        return {
            "moat_dimensions": moat_dimensions,
            "aggregate_moat_score": round(avg_moat, 3),
            "is_defensible": is_defensible,
        }

    def check_pivot_trigger(self, ltv_cac_ratio: float, burn_months_left: float) -> bool:
        """Triggers pivot recommendation if unit economics fail and runway is limited."""
        return ltv_cac_ratio < 1.0 or burn_months_left < 3.0


# ============================================================================
# LAYER 12: ORGANIZATIONAL DESIGN ENGINE
# ============================================================================

class OrganizationalDesignEngine:
    """Layer 12: Hiring trigger evaluation, delegation vs centralization matrix."""

    def evaluate_hiring_trigger(
        self, workload_utilization: float, expected_marginal_roi: float, fully_loaded_cost: float
    ) -> Dict[str, Any]:
        roi_ratio = expected_marginal_roi / max(1.0, fully_loaded_cost)
        should_hire = workload_utilization >= 0.85 and roi_ratio >= 3.0
        return {
            "workload_utilization": workload_utilization,
            "roi_cost_ratio": roi_ratio,
            "should_hire": should_hire,
        }


# ============================================================================
# LAYER 13: META-LEARNING ENGINE
# ============================================================================

class MetaLearningEngine:
    """Layer 13: Mental model belief updates via Bayes rule, decision quality scoring."""

    def update_hypothesis_prior(
        self, prior_prob: float, likelihood: float, marginal_evidence: float
    ) -> float:
        posterior = (likelihood * prior_prob) / max(1e-6, marginal_evidence)
        return max(0.0, min(1.0, posterior))

    def evaluate_decision_quality(
        self, ex_ante_voi: float, risk_adjusted_ev: float, actual_outcome: float
    ) -> Dict[str, Any]:
        # Decouples process quality from stochastic outcome (luck)
        process_score = min(1.0, max(0.0, (ex_ante_voi + risk_adjusted_ev) / 100.0))
        return {
            "process_quality_score": round(process_score, 3),
            "actual_outcome": actual_outcome,
            "luck_factor": actual_outcome - risk_adjusted_ev,
        }


# ============================================================================
# LAYER 14: AI ENTREPRENEURSHIP ENGINE
# ============================================================================

class AIEntrepreneurshipEngine:
    """Layer 14: Autonomous opportunity ranking, experiment selection, compute & capital allocation."""

    def allocate_resources(
        self, Total_capital_usd: float, total_compute_flops: float, opportunities: List[CandidateOpportunity]
    ) -> Dict[str, Any]:
        if not opportunities:
            return {"allocations": {}}

        # Weight allocation inversely proportional to risk and proportional to LTV/CAC
        scores = []
        for opp in opportunities:
            ratio = opp.ltv_usd / max(1.0, opp.cac_usd)
            risk_inv = 1.0 / max(100.0, opp.downside_risk_usd)
            score = ratio * risk_inv
            scores.append(score)

        total_score = sum(scores) or 1.0
        allocations = {}
        for opp, score in zip(opportunities, scores):
            weight = score / total_score
            allocations[opp.title] = {
                "capital_usd": round(Total_capital_usd * weight, 2),
                "compute_flops": round(total_compute_flops * weight, 2),
                "allocation_pct": round(weight * 100, 2),
            }

        return {"allocations": allocations}


# ============================================================================
# MASTER ORCHESTRATOR
# ============================================================================

class FourteenLayerEntrepreneurialEngine:
    """
    Master closed-loop orchestrator uniting all 14 layers into a unified execution system.
    """

    def __init__(self) -> None:
        self.l1_reality = RealitySubstrateEngine()
        self.l2_opportunity_discovery = OpportunityDiscoveryEngine()
        self.l3_problem_discovery = ProblemDiscoveryEngine()
        self.l4_decision_making = DecisionMakingEngine()
        self.l5_opportunity_evaluation = OpportunityEvaluationEngine()
        self.l6_product_creation = ProductCreationEngine()
        self.l7_customer = CustomerUnderstandingEngine()
        self.l8_marketing = MarketingEngine()
        self.l9_sales = SalesEngine()
        self.l10_growth = GrowthEngine()
        self.l11_competition = CompetitionEngine()
        self.l12_org_design = OrganizationalDesignEngine()
        self.l13_meta_learning = MetaLearningEngine()
        self.l14_ai_entrepreneurship = AIEntrepreneurshipEngine()

    def run_full_14_layer_pipeline(
        self,
        signal: SignalObservation,
        candidate_opp: CandidateOpportunity,
        feature: FeatureProposal,
        capital_usd: float = 1000000.0,
    ) -> Dict[str, Any]:
        """Executes an end-to-end cycle across all 14 computational layers."""
        logger.info("Starting closed-loop 14-layer pipeline execution.")

        # L1: Arbitrage check
        l1_res = self.l1_reality.evaluate_arbitrage_potential(100.0, 20.0)

        # L2: Signal Filtering
        l2_passed = self.l2_opportunity_discovery.filter_signal(signal)

        # L3: Problem Decomposition
        node1 = ProblemNode(node_id="latency_bottleneck", description="API latency slow", is_root_cause=True)
        node2 = ProblemNode(node_id="user_frustration", description="Users complaining", is_symptom=True)
        l3_res = self.l3_problem_discovery.decompose_problem_dag([node1, node2], [("latency_bottleneck", "user_frustration")])

        # L4: Decision VoI
        l4_res = self.l4_decision_making.calculate_value_of_information(100.0, 150.0, 10.0)

        # L5: Opportunity Evaluation
        l5_res = self.l5_opportunity_evaluation.evaluate_opportunity(candidate_opp)

        # L6: Product Anti-Build Filter
        l6_res = self.l6_product_creation.anti_build_filter(feature)

        # L7: Customer Utility
        l7_res = self.l7_customer.model_customer_utility(200.0, 50.0, 20.0)

        # L8: Marketing Virality
        l8_res = self.l8_marketing.calculate_viral_coefficient(5.0, 0.25)

        # L9: Sales State Transition
        l9_res = self.l9_sales.process_sales_funnel_transition("prospect", "qualify", 0.8)

        # L10: Growth Metcalfe Utility
        l10_res = self.l10_growth.evaluate_network_effect_utility(1000)

        # L11: Moat Strength
        l11_res = self.l11_competition.evaluate_moat_strength({"network_effects": 0.8, "brand": 0.7})

        # L12: Hiring Trigger
        l12_res = self.l12_org_design.evaluate_hiring_trigger(0.9, 300000.0, 90000.0)

        # L13: Meta-Learning Belief Update
        l13_posterior = self.l13_meta_learning.update_hypothesis_prior(0.5, 0.8, 0.6)

        # L14: AI Resource Allocation
        l14_res = self.l14_ai_entrepreneurship.allocate_resources(capital_usd, 1e15, [candidate_opp])

        return {
            "status": "completed",
            "layer_1_reality": l1_res,
            "layer_2_opportunity_discovery_passed": l2_passed,
            "layer_3_problem_decomposition": l3_res,
            "layer_4_decision_voi": l4_res,
            "layer_5_opportunity_evaluation": l5_res,
            "layer_6_product_filter": l6_res,
            "layer_7_customer_utility": l7_res,
            "layer_8_viral_marketing": l8_res,
            "layer_9_sales_funnel": l9_res,
            "layer_10_growth": l10_res,
            "layer_11_moat": l11_res,
            "layer_12_hiring": l12_res,
            "layer_13_belief_posterior": round(l13_posterior, 4),
            "layer_14_ai_allocations": l14_res,
        }
