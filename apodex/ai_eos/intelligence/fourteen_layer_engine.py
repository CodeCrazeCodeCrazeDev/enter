"""
Fourteen-Layer Computational Architecture Engine.

Provides continuous executable Python implementations for each layer of the
14-Layer Computational Architecture of Entrepreneurship:
1. Reality Substrate
2. Opportunity Discovery Engine
3. Problem Discovery Engine
4. Decision-Making Engine (Active Inference / EFE)
5. Opportunity Evaluation Engine
6. Product Creation Engine (JTBD & Minimum Viable Complexity)
7. Customer Psychology & Behavioral Engine
8. Marketing & System Dynamics Engine
9. Sales Engine & State Machine
10. Growth & Compounding Engine
11. Competitive Moat & Survival Engine
12. Organizational Design & Scaling Engine
13. Meta-Learning & System Evolution Engine
14. AI Entrepreneurship Unified Orchestrator Engine
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.fourteen_layer_engine")


# =====================================================================
# Layer 1: Reality Substrate
# =====================================================================
class ArbitrageOpportunity(BaseModel):
    opportunity_id: UUID = Field(default_factory=uuid4)
    domain: str
    current_utility: float
    expected_future_value: float
    risk_variance: float = 0.1

    def calculate_free_energy_delta(self) -> float:
        """Thermodynamic value arbitrage: dF = E[V] - U."""
        return max(0.0, self.expected_future_value - self.current_utility)


class RealitySubstrateEngine:
    """Layer 1: Evaluates fundamental thermodynamic free energy & value arbitrage."""

    def evaluate_arbitrage(self, current_utility: float, expected_future_value: float) -> Dict[str, float]:
        delta_f = max(0.0, expected_future_value - current_utility)
        return {
            "free_energy_delta": delta_f,
            "arbitrage_ratio": expected_future_value / max(1e-5, current_utility)
        }


# =====================================================================
# Layer 2: Opportunity Discovery Engine
# =====================================================================
class OpportunityDiscoveryEngine:
    """Layer 2: Continuous state-space search, weak signal detection, and tensor graph synthesis."""

    def detect_weak_signal_anomaly(self, observed_stream: List[float], baseline_mean: float, baseline_std: float) -> float:
        if baseline_std <= 0:
            return 0.0
        latest = observed_stream[-1] if observed_stream else baseline_mean
        z_score = abs(latest - baseline_mean) / baseline_std
        return float(z_score)

    def synthesize_cross_domain_knowledge(self, domain_a_nodes: List[str], domain_b_nodes: List[str]) -> List[Tuple[str, str]]:
        """Cartesian tensor graph product generating hybrid domain opportunities."""
        fused = []
        for a in domain_a_nodes:
            for b in domain_b_nodes:
                fused.append((a, b))
        return fused


# =====================================================================
# Layer 3: Problem Discovery Engine
# =====================================================================
class ProblemDiscoveryEngine:
    """Layer 3: Structural Causal Model decomposition & symptom vs. root cause isolation."""

    def decompose_problem(
        self,
        symptoms: List[str],
        causal_graph: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """Identifies root bottlenecks by finding nodes with highest out-degree in causal graph."""
        out_degrees: Dict[str, int] = {}
        for parent, children in causal_graph.items():
            out_degrees[parent] = len(children)

        root_cause = max(out_degrees.items(), key=lambda x: x[1])[0] if out_degrees else (symptoms[0] if symptoms else "unknown")

        return {
            "root_bottleneck": root_cause,
            "symptoms_count": len(symptoms),
            "is_first_order": root_cause in symptoms or out_degrees.get(root_cause, 0) > 1
        }


# =====================================================================
# Layer 4: Decision-Making Engine under Uncertainty
# =====================================================================
class ActiveInferenceDecisionEngine:
    """Layer 4: Active Inference Expected Free Energy (EFE) policy selection."""

    def compute_efe(
        self,
        p_success: float,
        p_target_preference: float,
        prior_entropy: float,
        simulated_entropy: float,
        curiosity_weight: float = 1.0
    ) -> float:
        eps = 1e-10
        p_s = max(eps, min(1.0 - eps, p_success))
        p_t = max(eps, min(1.0 - eps, p_target_preference))

        pragmatic_val = math.log(p_s) - math.log(p_t)
        epistemic_val = max(0.0, prior_entropy - simulated_entropy)

        efe = -pragmatic_val - (curiosity_weight * epistemic_val)
        return float(efe)


# =====================================================================
# Layer 5: Opportunity Evaluation Engine
# =====================================================================
class OpportunityEvaluationEngine:
    """Layer 5: Multi-variable risk-adjusted opportunity quality & hazard evaluation."""

    def evaluate_opportunity_quality(
        self,
        tam_cents: int,
        p_success: float,
        hazard_risk: float,
        capex_cents: int,
        risk_penalty_lambda: float = 1.5
    ) -> Dict[str, Any]:
        expected_gross = tam_cents * p_success
        risk_discount = math.exp(-risk_penalty_lambda * hazard_risk)
        net_quality_score = (expected_gross * risk_discount) - capex_cents

        return {
            "expected_gross_cents": expected_gross,
            "risk_discount_factor": risk_discount,
            "net_quality_score": net_quality_score,
            "is_viable": net_quality_score > 0
        }


# =====================================================================
# Layer 6: Product Creation Engine
# =====================================================================
class ProductCreationEngine:
    """Layer 6: Minimum Viable Complexity & Core Job-To-Be-Done (JTBD) optimization."""

    def optimize_minimum_viable_complexity(
        self,
        candidate_features: List[Dict[str, Any]],
        target_satisfaction_threshold: float = 0.8
    ) -> List[Dict[str, Any]]:
        """Sorts features by satisfaction impact / complexity cost ratio and selects minimal set."""
        scored = []
        for f in candidate_features:
            impact = f.get("satisfaction_impact", 0.1)
            complexity = max(1.0, f.get("complexity_cost", 1.0))
            scored.append((f, impact / complexity))

        scored.sort(key=lambda x: x[1], reverse=True)

        selected = []
        accumulated_sat = 0.0
        for feat, ratio in scored:
            selected.append(feat)
            accumulated_sat += feat.get("satisfaction_impact", 0.1)
            if accumulated_sat >= target_satisfaction_threshold:
                break

        return selected


# =====================================================================
# Layer 7: Customer Psychology & Behavioral Engine
# =====================================================================
class CustomerPsychologyEngine:
    """Layer 7: Switching utility, trust accumulation, and retention dynamics."""

    def calculate_switching_utility(
        self,
        v_new: float,
        v_old: float,
        cognitive_friction: float,
        financial_cost: float,
        perceived_risk: float
    ) -> Dict[str, Any]:
        total_friction = cognitive_friction + financial_cost + perceived_risk
        net_switching_utility = (v_new - v_old) - total_friction
        return {
            "net_switching_utility": net_switching_utility,
            "will_switch": net_switching_utility > 0.0
        }

    def update_trust_score(self, current_trust: float, promised_value: float, actual_value: float, learning_rate: float = 0.2) -> float:
        delta = actual_value - promised_value
        updated = current_trust + learning_rate * delta
        return max(0.0, min(1.0, updated))


# =====================================================================
# Layer 8: Marketing & System Dynamics Engine
# =====================================================================
class MarketingSystemDynamicsEngine:
    """Layer 8: Attention spread, viral coefficient mechanics, and channel attribution."""

    def simulate_viral_growth(self, initial_users: int, invite_rate: float, conversion_rate: float, cycles: int = 5) -> Dict[str, Any]:
        viral_k = invite_rate * conversion_rate
        users = initial_users
        trajectory = [users]

        for _ in range(cycles):
            new_users = int(users * viral_k)
            users += new_users
            trajectory.append(users)

        return {
            "viral_coefficient_k": viral_k,
            "final_user_count": users,
            "growth_trajectory": trajectory,
            "is_supercritical": viral_k > 1.0
        }


# =====================================================================
# Layer 9: Sales Engine & State Machine
# =====================================================================
class SalesEngineStateMachine:
    """Layer 9: Probabilistic sales pipeline transitions and objection resolution."""

    def compute_buying_urgency(self, cost_of_inaction_cents: int, time_to_value_days: float) -> float:
        ttv_days = max(1.0, time_to_value_days)
        return float(cost_of_inaction_cents / ttv_days)

    def handle_objection(self, objection_category: str, confidence_score: float) -> Dict[str, Any]:
        resolved = confidence_score >= 0.7
        return {
            "category": objection_category,
            "resolved": resolved,
            "recommended_action": "proceed_to_closing" if resolved else "provide_case_study"
        }


# =====================================================================
# Layer 10: Growth & Compounding Engine
# =====================================================================
class GrowthCompoundingEngine:
    """Layer 10: Network effects modeling (Metcalfe), platform expansion, and NRR prediction."""

    def calculate_metcalfe_network_value(self, active_nodes: int, value_per_connection_cents: int = 100) -> int:
        if active_nodes <= 1:
            return 0
        connections = (active_nodes * (active_nodes - 1)) // 2
        return connections * value_per_connection_cents

    def evaluate_growth_health(self, nrr_percent: float, ltv_to_cac: float, payback_months: float) -> Dict[str, Any]:
        healthy = (nrr_percent >= 120.0) and (ltv_to_cac >= 3.0) and (payback_months <= 12.0)
        return {
            "nrr_percent": nrr_percent,
            "ltv_to_cac": ltv_to_cac,
            "payback_months": payback_months,
            "is_compounding_healthy": healthy
        }


# =====================================================================
# Layer 11: Competitive Moat & Survival Engine
# =====================================================================
class CompetitiveMoatEngine:
    """Layer 11: Moat durability index calculation & game-theoretic pivot triggers."""

    def compute_moat_durability_index(
        self,
        network_density: float,
        switching_cost_ratio: float,
        cost_advantage_ratio: float,
        brand_trust: float
    ) -> float:
        w1, w2, w3, w4 = 0.3, 0.3, 0.2, 0.2
        score = (
            w1 * min(1.0, network_density) +
            w2 * min(1.0, switching_cost_ratio) +
            w3 * min(1.0, cost_advantage_ratio) +
            w4 * min(1.0, brand_trust)
        )
        return float(score)


# =====================================================================
# Layer 12: Organizational Design & Scaling Engine
# =====================================================================
class OrganizationalDesignEngine:
    """Layer 12: Capacity constraints, hiring triggers, and delegation topology."""

    def evaluate_hiring_need(self, capacity_utilization: float, threshold: float = 0.85) -> Dict[str, Any]:
        needs_hiring = capacity_utilization >= threshold
        return {
            "capacity_utilization": capacity_utilization,
            "needs_hiring": needs_hiring,
            "recommended_action": "scale_agent_nodes" if needs_hiring else "maintain_capacity"
        }


# =====================================================================
# Layer 13: Meta-Learning & System Evolution Engine
# =====================================================================
class MetaLearningEngine:
    """Layer 13: Mental model updates, decision quality scoring, and failure conversion."""

    def calculate_decision_quality(
        self,
        expected_utility: float,
        predicted_dist: List[float],
        observed_dist: List[float]
    ) -> float:
        # Compute discrete KL divergence
        kl_div = 0.0
        for p, q in zip(predicted_dist, observed_dist):
            p_c = max(1e-5, min(1.0, p))
            q_c = max(1e-5, min(1.0, q))
            kl_div += p_c * math.log(p_c / q_c)

        # High decision quality = high expected utility + low prediction error (low KL divergence)
        quality = expected_utility / (1.0 + kl_div)
        return float(quality)


# =====================================================================
# Layer 14: Autonomous AI Entrepreneurship Master Orchestrator
# =====================================================================
class FourteenLayerEntrepreneurialEngine:
    """
    Unified master orchestrator coupling all 14 computational layers into an autonomous,
    closed-loop AI Entrepreneurial Operating System.
    """

    def __init__(self) -> None:
        self.reality = RealitySubstrateEngine()
        self.opportunity_discovery = OpportunityDiscoveryEngine()
        self.problem_discovery = ProblemDiscoveryEngine()
        self.decision_engine = ActiveInferenceDecisionEngine()
        self.opportunity_eval = OpportunityEvaluationEngine()
        self.product_engine = ProductCreationEngine()
        self.customer_engine = CustomerPsychologyEngine()
        self.marketing_engine = MarketingSystemDynamicsEngine()
        self.sales_engine = SalesEngineStateMachine()
        self.growth_engine = GrowthCompoundingEngine()
        self.moat_engine = CompetitiveMoatEngine()
        self.org_engine = OrganizationalDesignEngine()
        self.meta_engine = MetaLearningEngine()

    def run_full_14_layer_pipeline(
        self,
        domain_a: List[str],
        domain_b: List[str],
        current_utility: float,
        expected_future_value: float,
        tam_cents: int,
        capex_cents: int
    ) -> Dict[str, Any]:
        """Runs an end-to-end multi-layer entrepreneurial sensing, evaluation, and execution cycle."""
        # Layer 1: Reality Substrate
        reality_res = self.reality.evaluate_arbitrage(current_utility, expected_future_value)

        # Layer 2: Opportunity Discovery
        cross_pairs = self.opportunity_discovery.synthesize_cross_domain_knowledge(domain_a, domain_b)
        selected_pair = cross_pairs[0] if cross_pairs else ("domain_a", "domain_b")

        # Layer 3: Problem Discovery
        problem_res = self.problem_discovery.decompose_problem(
            symptoms=["high_cac", "slow_onboarding"],
            causal_graph={"root_product_friction": ["high_cac", "slow_onboarding"]}
        )

        # Layer 4: Decision Making (Active Inference EFE)
        efe = self.decision_engine.compute_efe(
            p_success=0.6,
            p_target_preference=0.9,
            prior_entropy=1.5,
            simulated_entropy=0.4
        )

        # Layer 5: Opportunity Evaluation
        opp_eval = self.opportunity_eval.evaluate_opportunity_quality(
            tam_cents=tam_cents,
            p_success=0.6,
            hazard_risk=0.2,
            capex_cents=capex_cents
        )

        # Layer 6: Product Creation
        product_res = self.product_engine.optimize_minimum_viable_complexity([
            {"feature": "core_workflow", "satisfaction_impact": 0.6, "complexity_cost": 2.0},
            {"feature": "advanced_telemetry", "satisfaction_impact": 0.3, "complexity_cost": 5.0}
        ])

        # Layer 7: Customer Psychology
        switch_res = self.customer_engine.calculate_switching_utility(
            v_new=10.0, v_old=4.0, cognitive_friction=1.0, financial_cost=1.0, perceived_risk=1.0
        )

        # Layer 8: Marketing Dynamics
        viral_res = self.marketing_engine.simulate_viral_growth(initial_users=100, invite_rate=1.5, conversion_rate=0.8)

        # Layer 9: Sales
        urgency = self.sales_engine.compute_buying_urgency(cost_of_inaction_cents=50000_00, time_to_value_days=14.0)

        # Layer 10: Growth
        metcalfe_val = self.growth_engine.calculate_metcalfe_network_value(active_nodes=100)
        growth_health = self.growth_engine.evaluate_growth_health(nrr_percent=130.0, ltv_to_cac=4.2, payback_months=6.0)

        # Layer 11: Competitive Moat
        moat_score = self.moat_engine.compute_moat_durability_index(
            network_density=0.8, switching_cost_ratio=0.7, cost_advantage_ratio=0.5, brand_trust=0.9
        )

        # Layer 12: Org Design
        org_res = self.org_engine.evaluate_hiring_need(capacity_utilization=0.88)

        # Layer 13: Meta-Learning
        decision_qual = self.meta_engine.calculate_decision_quality(
            expected_utility=8.5, predicted_dist=[0.6, 0.4], observed_dist=[0.65, 0.35]
        )

        return {
            "status": "executed",
            "layer1_arbitrage": reality_res,
            "layer2_selected_pair": selected_pair,
            "layer3_problem_root": problem_res,
            "layer4_efe_score": efe,
            "layer5_opportunity_evaluation": opp_eval,
            "layer6_selected_features": product_res,
            "layer7_switching_utility": switch_res,
            "layer8_viral_growth": viral_res,
            "layer9_urgency_score": urgency,
            "layer10_network_value": metcalfe_val,
            "layer10_growth_health": growth_health,
            "layer11_moat_score": moat_score,
            "layer12_org_hiring": org_res,
            "layer13_decision_quality": decision_qual
        }
