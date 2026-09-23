"""
14-Layer Computational Engine for AI Entrepreneurship.
Implements the 14-layer first-principles computational decomposition of entrepreneurship.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger("sero.fourteen_layer_engine")


# --- Data Models ---

class SignalVector(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    signal_id: UUID = Field(default_factory=uuid4)
    source: str
    value: float
    historical_mean: float = 0.0
    historical_std: float = 1.0
    timestamp: float = 0.0


class ProblemNode(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    problem_id: UUID = Field(default_factory=uuid4)
    description: str
    is_symptom: bool = False
    causal_leverage: float = 0.5
    solution_cost: float = 1000.0
    addressable_friction: float = 5000.0


class OpportunityModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    opportunity_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str = "general"
    tam_usd: float = 1_000_000.0
    expected_value: float = 500_000.0
    downside_risk: float = 50_000.0
    prior_entropy: float = 1.5
    post_entropy_simulated: float = 0.4
    success_probability: float = 0.6
    target_preference: float = 0.95
    timing_index: float = 1.2
    active: bool = True


class FeatureCandidate(BaseModel):
    name: str
    utility_impact: float
    complexity_cost: float


class CustomerState(BaseModel):
    customer_id: UUID = Field(default_factory=uuid4)
    stage: str = "Unaware"  # Unaware, Problem-Aware, Evaluating, Active User, Evangelist, Churned
    trust_score: float = 0.5
    push_force: float = 0.0
    pull_force: float = 0.0
    anxiety_force: float = 0.0
    habit_force: float = 0.0
    switching_cost: float = 0.0


class DecisionRecord(BaseModel):
    decision_id: UUID = Field(default_factory=uuid4)
    predicted_probability: float
    ground_outcome: Optional[int] = None


# --- Layer Engines ---

class Layer1RealitySubstrateEngine:
    """Layer 1: Reality Substrate & Fundamental Invariants."""

    def evaluate_arbitrage_value(self, utility_captured: float, friction_cost: float, time_horizon: float, discount_rate: float = 0.05) -> float:
        if discount_rate <= 0:
            return (utility_captured - friction_cost) * time_horizon
        net_flow = utility_captured - friction_cost
        present_value = net_flow * ((1.0 - math.exp(-discount_rate * time_horizon)) / discount_rate)
        return max(0.0, present_value)

    def verify_positive_sum_exchange(self, buyer_utility: float, price: float, seller_cost: float) -> bool:
        buyer_surplus = buyer_utility - price
        seller_surplus = price - seller_cost
        return buyer_surplus > 0 and seller_surplus > 0


class Layer2OpportunityDiscoveryEngine:
    """Layer 2: Continuous State-Space Sensing & Weak Signal Fusion."""

    def compute_anomaly_index(self, signal: SignalVector) -> float:
        denom = signal.historical_std
        return abs(signal.value - signal.historical_mean) / denom if denom > 0 else 0.0

    def fuse_signals_and_generate_novelty(self, signal_a: SignalVector, signal_b: SignalVector) -> float:
        anomaly_a = self.compute_anomaly_index(signal_a)
        anomaly_b = self.compute_anomaly_index(signal_b)
        joint_tensor_magnitude = math.sqrt(anomaly_a**2 + anomaly_b**2)
        denom = abs(signal_a.value) + abs(signal_b.value)
        ratio = abs(signal_a.value - signal_b.value) / denom if denom > 0 else 0.0
        novelty_score = joint_tensor_magnitude * (1.0 + ratio)
        return novelty_score


class Layer3ProblemDiscoveryEngine:
    """Layer 3: Pearl Structural Causal Problem Decomposition."""

    def analyze_problem(self, problem: ProblemNode, causal_intervention_delta: float) -> Dict[str, Any]:
        is_real_root_cause = causal_intervention_delta > 0.3
        worth_solving = (problem.addressable_friction > problem.solution_cost) and (problem.causal_leverage > 0.2)
        return {
            "problem_id": problem.problem_id,
            "description": problem.description,
            "is_root_cause": is_real_root_cause,
            "worth_solving": worth_solving,
            "action": "Solve" if worth_solving and is_real_root_cause else "Ignore"
        }


class Layer4DecisionMakingEngine:
    """Layer 4: Decision Making under Uncertainty via Active Inference EFE."""

    def calculate_expected_free_energy(self, opp: OpportunityModel, curiosity_weight: float = 1.0) -> float:
        eps = 1e-9
        p_succ = max(eps, min(1.0 - eps, opp.success_probability))
        p_target = max(eps, min(1.0 - eps, opp.target_preference))

        pragmatic_value = math.log(p_succ) - math.log(p_target)
        epistemic_value = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)

        efe = -pragmatic_value - (curiosity_weight * epistemic_value)
        return efe

    def evaluate_kill_gate(self, opp: OpportunityModel, pmf_posterior_prob: float, kill_threshold: float = 0.2) -> bool:
        return pmf_posterior_prob < kill_threshold


class Layer5OpportunityEvaluationEngine:
    """Layer 5: Expected Value, Downside Risk, and Timing Index Evaluation."""

    def evaluate_opportunity(self, opp: OpportunityModel) -> Dict[str, Any]:
        net_ev = opp.expected_value - opp.downside_risk
        denom = opp.downside_risk if opp.downside_risk > 0 else 1e-6
        risk_return_ratio = opp.expected_value / denom
        timing_adjusted_ev = net_ev * opp.timing_index
        return {
            "opportunity_id": opp.opportunity_id,
            "net_ev": net_ev,
            "risk_return_ratio": risk_return_ratio,
            "timing_adjusted_ev": timing_adjusted_ev,
            "viable": timing_adjusted_ev > 0 and risk_return_ratio >= 2.0
        }

    def evaluate_opportunity_switch(self, current_efe_rate: float, candidate_efe_rate: float, switching_cost: float) -> bool:
        # Lower EFE rate is superior in Active Inference
        marginal_improvement = current_efe_rate - candidate_efe_rate
        return marginal_improvement > switching_cost


class Layer6ProductCreationEngine:
    """Layer 6: Jobs-to-be-Done (JTBD) & Complexity Minimization Engine."""

    def calculate_jtbd_utility(self, outcome_speed: float, reliability: float, cognitive_effort: float, friction: float) -> float:
        denom = cognitive_effort + friction
        return (outcome_speed * reliability) / denom if denom > 0 else 0.0

    def evaluate_feature_inclusion(self, feature: FeatureCandidate, threshold: float = 1.5) -> bool:
        denom = feature.complexity_cost if feature.complexity_cost > 0 else 1e-6
        roi = feature.utility_impact / denom
        return roi >= threshold


class Layer7CustomerUnderstandingEngine:
    """Layer 7: Customer Psychology & Trust Accumulation State Machine."""

    def evaluate_switching_trigger(self, customer: CustomerState) -> bool:
        driving_forces = customer.push_force + customer.pull_force
        restraining_forces = customer.anxiety_force + customer.habit_force + customer.switching_cost
        return driving_forces > restraining_forces

    def update_trust(self, current_trust: float, delivered_value: float, promised_value: float, gamma: float = 0.8) -> float:
        ratio = min(2.0, delivered_value / promised_value) if promised_value > 0 else 0.0
        updated_trust = (gamma * current_trust) + ((1.0 - gamma) * ratio)
        return max(0.0, min(1.0, updated_trust))


class Layer8MarketingEngine:
    """Layer 8: Virality Dynamics & Brand Authority Geometry."""

    def calculate_reproduction_number(self, transmission_rate: float, share_factor: float, recovery_rate: float) -> float:
        return (transmission_rate * share_factor) / recovery_rate if recovery_rate > 0 else 0.0

    def calculate_brand_authority(self, brand_vector: List[float], aspiration_vector: List[float], messaging_variance: float) -> float:
        dot_prod = sum(b * a for b, a in zip(brand_vector, aspiration_vector))
        norm_b = math.sqrt(sum(b**2 for b in brand_vector))
        norm_a = math.sqrt(sum(a**2 for a in aspiration_vector))
        cosine_sim = dot_prod / (norm_b * norm_a) if norm_b > 0 and norm_a > 0 else 0.0
        authority = cosine_sim / (messaging_variance + 1.0)
        return authority


class Layer9SalesEngine:
    """Layer 9: Sales Urgency & Objection Resolution State Machine."""

    def calculate_buying_urgency(self, cost_of_inaction: float, time_sensitivity: float, implementation_risk: float) -> float:
        denom = implementation_risk if implementation_risk > 0 else 1e-6
        return (cost_of_inaction * time_sensitivity) / denom

    def is_objection_resolved(self, initial_risk: float, proof_strength: float, tolerance: float = 0.3) -> bool:
        residual_risk = initial_risk * math.exp(-proof_strength)
        return residual_risk < tolerance


class Layer10GrowthEngine:
    """Layer 10: Platform Compounding & Intentional Slowdown Gate."""

    def project_compounding_users(self, current_users: int, virality_k: float, retention_k: float, churn_rate: float) -> int:
        growth_factor = 1.0 + virality_k + retention_k - churn_rate
        new_users = current_users * growth_factor
        return max(0, int(new_users))

    def evaluate_slowdown_gate(self, churn_derivative: float, nps_score: float, danger_threshold: float = 0.05, min_nps: float = 30.0) -> bool:
        return churn_derivative > danger_threshold or nps_score < min_nps


class Layer11CompetitionEngine:
    """Layer 11: Moat Strength & Counter-Positioning Game Engine."""

    def calculate_moat_strength(self, competitor_replication_cost: float, incumbent_operational_cost: float) -> float:
        denom = incumbent_operational_cost if incumbent_operational_cost > 0 else 1e-6
        return competitor_replication_cost / denom

    def evaluate_counter_positioning(self, incumbent_revenue_cannibalization: float, new_entrant_profit: float) -> bool:
        # Incumbent will hesitate to copy if cannibalization cost exceeds new entrant profit
        return incumbent_revenue_cannibalization > new_entrant_profit


class Layer12OrganizationalDesignEngine:
    """Layer 12: Capacity Sensing & Decision Rule Delegation Engine."""

    def evaluate_hiring_need(self, team_utilization: float, delay_cost: float, salary_cost: float) -> bool:
        return team_utilization > 0.85 and delay_cost > salary_cost

    def determine_decision_mode(self, operational_risk: float, local_context_specificity: float) -> str:
        if operational_risk > 0.7 or local_context_specificity < 0.3:
            return "Centralized"
        return "Delegated"


class Layer13MetaLearningEngine:
    """Layer 13: Brier Score Calibration & Mental Model Refinement Flywheel."""

    def calculate_brier_score(self, records: List[DecisionRecord]) -> float:
        if not records:
            return 0.0
        valid_records = [r for r in records if r.ground_outcome is not None]
        if not valid_records:
            return 0.0
        squared_errors = [(r.predicted_probability - r.ground_outcome) ** 2 for r in valid_records]
        return sum(squared_errors) / len(squared_errors)

    def update_confidence_prior(self, prior_confidence: float, brier_score: float, learning_rate: float = 0.1) -> float:
        # Perfect brier score is 0.0, worst is 1.0
        adjustment = (0.25 - brier_score) * learning_rate
        updated = prior_confidence + adjustment
        return max(0.05, min(0.95, updated))


class Layer14AIEntrepreneurshipOrchestrator:
    """Layer 14: Capital, Compute, and Talent Allocation Orchestrator."""

    def allocate_resources(self, capital_budget: float, compute_budget: float, opportunities: List[OpportunityModel]) -> Dict[str, Any]:
        if not opportunities:
            return {"allocations": [], "unallocated_capital": capital_budget, "unallocated_compute": compute_budget}

        # Active Inference ranking (lower EFE is better)
        decision_engine = Layer4DecisionMakingEngine()
        ranked = sorted(opportunities, key=lambda opp: decision_engine.calculate_expected_free_energy(opp))

        allocations = []
        remaining_cap = capital_budget
        remaining_comp = compute_budget

        for opp in ranked:
            if remaining_cap <= 0 or remaining_comp <= 0:
                break
            cap_allocated = min(remaining_cap, opp.expected_value * 0.1)
            comp_allocated = min(remaining_comp, 100.0)

            allocations.append({
                "opportunity_id": opp.opportunity_id,
                "title": opp.title,
                "capital_allocated": cap_allocated,
                "compute_allocated": comp_allocated
            })

            remaining_cap -= cap_allocated
            remaining_comp -= comp_allocated

        return {
            "allocations": allocations,
            "unallocated_capital": remaining_cap,
            "unallocated_compute": remaining_comp
        }


# --- Unified Master Engine ---

class FourteenLayerEntrepreneurialEngine:
    """Master Unified Engine coordinating all 14 computational layers."""

    def __init__(self) -> None:
        self.l1_reality = Layer1RealitySubstrateEngine()
        self.l2_discovery = Layer2OpportunityDiscoveryEngine()
        self.l3_problem = Layer3ProblemDiscoveryEngine()
        self.l4_decision = Layer4DecisionMakingEngine()
        self.l5_evaluation = Layer5OpportunityEvaluationEngine()
        self.l6_product = Layer6ProductCreationEngine()
        self.l7_customer = Layer7CustomerUnderstandingEngine()
        self.l8_marketing = Layer8MarketingEngine()
        self.l9_sales = Layer9SalesEngine()
        self.l10_growth = Layer10GrowthEngine()
        self.l11_competition = Layer11CompetitionEngine()
        self.l12_org = Layer12OrganizationalDesignEngine()
        self.l13_meta = Layer13MetaLearningEngine()
        self.l14_orchestrator = Layer14AIEntrepreneurshipOrchestrator()

        self.decisions_history: List[DecisionRecord] = []

    def execute_full_cycle(
        self,
        signals: List[SignalVector],
        problems: List[ProblemNode],
        opportunities: List[OpportunityModel],
        capital_budget: float = 100_000.0,
        compute_budget: float = 1_000.0
    ) -> Dict[str, Any]:
        """Executes a full 14-layer sensing, discovery, evaluation, product, growth, and meta-learning cycle."""

        # Layer 1 & 2: Sensing & Anomaly Fusion
        fused_signals = []
        if len(signals) >= 2:
            novelty = self.l2_discovery.fuse_signals_and_generate_novelty(signals[0], signals[1])
            fused_signals.append({"novelty_score": novelty})

        # Layer 3: Causal Problem Analysis
        problem_results = []
        for p in problems:
            res = self.l3_problem.analyze_problem(p, causal_intervention_delta=0.5)
            problem_results.append(res)

        # Layer 4 & 5: Active Inference Opportunity Ranking & Evaluation
        evaluated_opps = []
        for opp in opportunities:
            efe = self.l4_decision.calculate_expected_free_energy(opp)
            eval_res = self.l5_evaluation.evaluate_opportunity(opp)
            eval_res["efe"] = efe
            evaluated_opps.append(eval_res)

        # Layer 14: Resource Allocation Orchestration
        allocation_plan = self.l14_orchestrator.allocate_resources(capital_budget, compute_budget, opportunities)

        # Layer 13: Meta-Learning Feedback Update
        brier_score = self.l13_meta.calculate_brier_score(self.decisions_history)

        return {
            "status": "completed",
            "fused_signals": fused_signals,
            "problem_results": problem_results,
            "evaluated_opportunities": evaluated_opps,
            "resource_allocation_plan": allocation_plan,
            "meta_learning_brier_score": brier_score
        }
