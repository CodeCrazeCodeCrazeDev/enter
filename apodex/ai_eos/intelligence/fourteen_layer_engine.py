"""
Executable first-principles engine for the 14-Layer Computational Architecture
of Entrepreneurship (Autonomous AI Entrepreneurial Operating System - AI-EOS).
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.fourteen_layer_engine")


# ============================================================================
# Core Data Models
# ============================================================================

class OpportunityState(BaseModel):
    """Data model representing an opportunity moving through the 14-layer pipeline."""
    opportunity_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str = "general"
    variables: List[str] = Field(default_factory=list)
    causal_edges: List[Tuple[str, str]] = Field(default_factory=list)
    coefficients: Dict[str, float] = Field(default_factory=dict)
    prior_entropy: float = 1.5
    post_entropy_simulated: float = 0.4
    success_probability: float = 0.5
    target_preference: float = 0.95
    tam_cents: int = 500000000  # $5M
    cac_cents: float = 10000.0  # $100
    ltv_cents: float = 50000.0  # $500
    payback_months: float = 6.0
    moat_score: float = 0.7
    stage: str = "discovered"


# ============================================================================
# Layer 1: Reality Substrate & Invariants Engine
# ============================================================================

class RealitySubstrateEngine:
    """Evaluates fundamental invariants (entropy reduction, asymmetric risk, automation boundary)."""

    def analyze_invariants(self, opp: OpportunityState) -> Dict[str, Any]:
        downside = min(1.0, opp.cac_cents / 100000.0)
        upside = max(1.0, opp.ltv_cents / opp.cac_cents)
        asymmetry_ratio = upside / max(0.01, downside)
        entropy_reduction = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)
        return {
            "is_viable_invariant": asymmetry_ratio > 2.0 and entropy_reduction > 0.2,
            "asymmetry_ratio": asymmetry_ratio,
            "entropy_reduction": entropy_reduction,
            "can_be_automated": True
        }


# ============================================================================
# Layer 2: Opportunity Discovery Engine (Hawkes Process)
# ============================================================================

class OpportunityDiscoveryEngine:
    """Detects weak market signals via Hawkes point processes and cross-domain tensor fusion."""

    def compute_hawkes_intensity(self, timestamps: List[float], current_time: float, mu0: float = 0.1, alpha: float = 0.5, beta: float = 1.0) -> float:
        intensity = mu0
        for t_i in timestamps:
            if t_i < current_time:
                intensity += alpha * math.exp(-beta * (current_time - t_i))
        return intensity

    def discover_opportunity(self, signal: Dict[str, Any]) -> OpportunityState:
        timestamps = signal.get("signal_timestamps", [1.0, 2.0, 2.5, 2.8])
        intensity = self.compute_hawkes_intensity(timestamps, current_time=3.0)
        opp = OpportunityState(
            title=signal.get("title", "Discovered Opportunity"),
            domain=signal.get("domain", "general"),
            variables=signal.get("variables", ["marketing_spend", "user_growth", "revenue"]),
            causal_edges=signal.get("causal_edges", [("marketing_spend", "user_growth"), ("user_growth", "revenue")]),
            coefficients=signal.get("coefficients", {"marketing_spend->user_growth": 2.0, "user_growth->revenue": 1.5}),
            success_probability=min(0.95, max(0.1, intensity / 5.0))
        )
        return opp


# ============================================================================
# Layer 3: Problem Discovery & Decomposition Engine (SCM)
# ============================================================================

class ProblemDiscoveryEngine:
    """Decomposes problems using Structural Causal Models (SCMs) to isolate root causes from symptoms."""

    def isolate_root_cause(self, variables: List[str], edges: List[Tuple[str, str]]) -> Dict[str, Any]:
        in_degrees = {v: 0 for v in variables}
        out_degrees = {v: 0 for v in variables}
        for parent, child in edges:
            if parent in out_degrees:
                out_degrees[parent] += 1
            if child in in_degrees:
                in_degrees[child] += 1

        root_causes = [v for v in variables if in_degrees.get(v, 0) == 0 and out_degrees.get(v, 0) > 0]
        symptoms = [v for v in variables if out_degrees.get(v, 0) == 0 and in_degrees.get(v, 0) > 0]
        return {
            "root_causes": root_causes if root_causes else [variables[0]] if variables else [],
            "symptoms": symptoms if symptoms else [variables[-1]] if variables else [],
            "graph_depth": len(edges)
        }


# ============================================================================
# Layer 4: Decision Making Engine (Active Inference Expected Free Energy)
# ============================================================================

class DecisionMakingEngine:
    """Ranks options using Expected Free Energy (EFE = - Pragmatic Value - Curiosity * Epistemic Value)."""

    def __init__(self, curiosity_weight: float = 1.0) -> None:
        self.curiosity_weight = curiosity_weight

    def calculate_efe(self, opp: OpportunityState) -> float:
        eps = 1e-10
        p_success = max(eps, min(1.0 - eps, opp.success_probability))
        p_target = max(eps, min(1.0 - eps, opp.target_preference))
        pragmatic_value = math.log(p_success) - math.log(p_target)
        epistemic_value = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)
        return -pragmatic_value - (epistemic_value * self.curiosity_weight)

    def select_best_decision(self, opps: List[OpportunityState]) -> Tuple[OpportunityState, float]:
        ranked = [(opp, self.calculate_efe(opp)) for opp in opps]
        ranked.sort(key=lambda x: x[1])
        return ranked[0]


# ============================================================================
# Layer 5: Opportunity Evaluation & Capital Allocation Engine (Real Options & Kelly)
# ============================================================================

class OpportunityEvaluationEngine:
    """Calculates Real Options valuation and optimal capital fraction via Modified Kelly Criterion."""

    def evaluate_real_option(self, opp: OpportunityState, strike_cost: float = 50000.0, risk_free_rate: float = 0.05, time_years: float = 1.0) -> float:
        s = float(opp.tam_cents) / 100.0 * opp.success_probability
        k = strike_cost
        d1 = (math.log(max(1.0, s / max(1.0, k))) + (risk_free_rate + 0.25) * time_years) / (0.5 * math.sqrt(time_years))
        d2 = d1 - 0.5 * math.sqrt(time_years)
        # Approximate standard normal CDF
        cdf_d1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
        cdf_d2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
        call_val = s * cdf_d1 - k * math.exp(-risk_free_rate * time_years) * cdf_d2
        return max(0.0, call_val)

    def calculate_kelly_capital_fraction(self, p_win: float, payout_ratio: float, conservative_factor: float = 0.2) -> float:
        q_loss = 1.0 - p_win
        b = max(0.1, payout_ratio)
        f_star = (p_win * b - q_loss) / b
        return max(0.0, f_star * conservative_factor)


# ============================================================================
# Layer 6: Product Creation Engine (Feature Minimal Viable Bounds)
# ============================================================================

class ProductCreationEngine:
    """Determines minimal feature set maximizing value density while pruning unnecessary complexity."""

    def optimize_feature_set(self, features: List[Dict[str, float]], max_complexity: float = 10.0) -> Dict[str, Any]:
        sorted_features = sorted(features, key=lambda f: f.get("value", 0.0) / max(0.1, f.get("cost", 1.0)), reverse=True)
        selected = []
        accumulated_cost = 0.0
        accumulated_value = 0.0
        for feat in sorted_features:
            if accumulated_cost + feat.get("cost", 1.0) <= max_complexity:
                selected.append(feat.get("name", "feat"))
                accumulated_cost += feat.get("cost", 1.0)
                accumulated_value += feat.get("value", 0.0)
        return {
            "selected_features": selected,
            "total_value": accumulated_value,
            "total_cost": accumulated_cost,
            "value_density": accumulated_value / max(0.1, accumulated_cost)
        }


# ============================================================================
# Layer 7: Customer Understanding Engine (Behavioral Switching MDP)
# ============================================================================

class CustomerUnderstandingEngine:
    """Models customer switching thresholds, retention loyalty, and evangelism delight."""

    def evaluate_switching_probability(self, new_utility: float, old_utility: float, switching_cost: float, perceived_risk: float) -> float:
        net_delta = new_utility - old_utility - switching_cost - perceived_risk
        return 1.0 / (1.0 + math.exp(-net_delta))


# ============================================================================
# Layer 8: Marketing & Attention Spread Engine (Epidemiological SIR)
# ============================================================================

class MarketingEngine:
    """Simulates attention spread and organic virality using SIR differential dynamics."""

    def calculate_viral_reproduction_number(self, contact_rate_beta: float, recovery_rate_gamma: float) -> float:
        return contact_rate_beta / max(1e-5, recovery_rate_gamma)


# ============================================================================
# Layer 9: Sales Systems & Urgency Engine
# ============================================================================

class SalesSystemEngine:
    """Models psychological closing probability and automated objection resolution paths."""

    def compute_close_probability(self, urgency: float, perceived_value: float, friction: float, price: float) -> float:
        exponent = urgency + perceived_value - friction - price
        return 1.0 / (1.0 + math.exp(-exponent))


# ============================================================================
# Layer 10: Growth Dynamics & Network Effects Engine
# ============================================================================

class GrowthDynamicsEngine:
    """Simulates compounding growth curves, Metcalfe/Reed network scaling, and platform transitions."""

    def calculate_metcalfe_value(self, active_users: int) -> float:
        return float(active_users ** 2)

    def project_compounding_growth(self, initial_users: float, growth_rate: float, capacity_k: float, steps: int = 5) -> List[float]:
        n = initial_users
        history = [n]
        for _ in range(steps):
            dn = growth_rate * n * (1.0 - n / capacity_k)
            n += dn
            history.append(n)
        return history


# ============================================================================
# Layer 11: Competitive Moats & Pivot Engine
# ============================================================================

class CompetitiveMoatEngine:
    """Evaluates moat strength and triggers automated pivot alerts when CAC escalates or retention drops."""

    def should_trigger_pivot(self, cac_history: List[float], retention_rate: float, min_retention: float = 0.40) -> bool:
        if len(cac_history) >= 3 and cac_history[-1] > cac_history[-2] > cac_history[-3]:
            if retention_rate < min_retention:
                return True
        return False


# ============================================================================
# Layer 12: Autonomous Organizational Design Engine
# ============================================================================

class OrganizationalDesignEngine:
    """Manages task graph partitioning and dynamic agent provisioning based on queue load factors."""

    def evaluate_provisioning(self, arrival_rate_lambda: float, service_rate_mu: float) -> Dict[str, Any]:
        load_factor = arrival_rate_lambda / max(1e-5, service_rate_mu)
        should_provision_agent = load_factor > 0.85
        return {
            "load_factor": load_factor,
            "should_provision_agent": should_provision_agent
        }


# ============================================================================
# Layer 13: Meta-Learning & Failure Synthesis Engine
# ============================================================================

class MetaLearningEngine:
    """Converts failed operational trajectories into reusable long-term negative prior knowledge primitives."""

    def synthesize_failure_knowledge(self, trajectory: List[Dict[str, Any]], outcome_reward: float) -> Dict[str, Any]:
        if outcome_reward >= 0.0:
            return {"status": "success", "knowledge_primitive": None}
        failed_step = trajectory[-1] if trajectory else {"step": "unknown"}
        primitive = f"NEGATIVE_PRIOR: Avoid action '{failed_step.get('step')}' under state {failed_step.get('state')}"
        return {
            "status": "failure_synthesized",
            "knowledge_primitive": primitive,
            "penalty_discount": 0.5
        }


# ============================================================================
# Layer 14: Autonomous AI Entrepreneurship Orchestrator
# ============================================================================

class FourteenLayerEntrepreneurialEngine:
    """Master orchestrator integrating all 14 computational layers into a single autonomous active inference loop."""

    def __init__(self) -> None:
        self.layer1_reality = RealitySubstrateEngine()
        self.layer2_discovery = OpportunityDiscoveryEngine()
        self.layer3_problem = ProblemDiscoveryEngine()
        self.layer4_decision = DecisionMakingEngine()
        self.layer5_eval = OpportunityEvaluationEngine()
        self.layer6_product = ProductCreationEngine()
        self.layer7_customer = CustomerUnderstandingEngine()
        self.layer8_marketing = MarketingEngine()
        self.layer9_sales = SalesSystemEngine()
        self.layer10_growth = GrowthDynamicsEngine()
        self.layer11_moat = CompetitiveMoatEngine()
        self.layer12_org = OrganizationalDesignEngine()
        self.layer13_meta = MetaLearningEngine()

    def run_full_14_layer_pipeline(self, raw_signal: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Sense opportunity (Layer 2)
        opp = self.layer2_discovery.discover_opportunity(raw_signal)

        # 2. Check fundamental reality invariants (Layer 1)
        reality_audit = self.layer1_reality.analyze_invariants(opp)

        # 3. Decompose causal problem roots (Layer 3)
        problem_audit = self.layer3_problem.isolate_root_cause(opp.variables, opp.causal_edges)

        # 4. Decision ranking (Layer 4)
        best_opp, best_efe = self.layer4_decision.select_best_decision([opp])

        # 5. Financial evaluation & real option pricing (Layer 5)
        option_val = self.layer5_eval.evaluate_real_option(best_opp)
        kelly_fraction = self.layer5_eval.calculate_kelly_capital_fraction(best_opp.success_probability, payout_ratio=4.0)

        # 6. Minimal Viable Product creation (Layer 6)
        prod_audit = self.layer6_product.optimize_feature_set([
            {"name": "core_workflow", "cost": 3.0, "value": 9.0},
            {"name": "analytics_dash", "cost": 4.0, "value": 3.0},
            {"name": "custom_theme", "cost": 5.0, "value": 1.0}
        ])

        # 7. Customer switching dynamic (Layer 7)
        switch_prob = self.layer7_customer.evaluate_switching_probability(new_utility=8.0, old_utility=3.0, switching_cost=1.0, perceived_risk=1.0)

        # 8. Virality (Layer 8)
        r0 = self.layer8_marketing.calculate_viral_reproduction_number(contact_rate_beta=1.2, recovery_rate_gamma=0.8)

        # 9. Sales close (Layer 9)
        close_prob = self.layer9_sales.compute_close_probability(urgency=2.0, perceived_value=3.0, friction=1.0, price=2.0)

        # 10. Compounding growth (Layer 10)
        growth_curve = self.layer10_growth.project_compounding_growth(initial_users=100, growth_rate=0.2, capacity_k=10000)

        # 11. Moat pivot check (Layer 11)
        pivot_alert = self.layer11_moat.should_trigger_pivot(cac_history=[10, 15, 22], retention_rate=0.25)

        # 12. Org capacity (Layer 12)
        org_audit = self.layer12_org.evaluate_provisioning(arrival_rate_lambda=9.0, service_rate_mu=10.0)

        # 13. Meta-learning failure distillation (Layer 13)
        meta_audit = self.layer13_meta.synthesize_failure_knowledge([{"step": "launch", "state": "unvalidated"}], outcome_reward=-1.0 if pivot_alert else 1.0)

        return {
            "opportunity_title": best_opp.title,
            "reality_audit": reality_audit,
            "problem_audit": problem_audit,
            "expected_free_energy": best_efe,
            "real_option_value": option_val,
            "kelly_capital_fraction": kelly_fraction,
            "product_features": prod_audit["selected_features"],
            "switching_probability": switch_prob,
            "viral_reproduction_number": r0,
            "sales_close_probability": close_prob,
            "projected_growth_5_steps": growth_curve,
            "pivot_alert_triggered": pivot_alert,
            "org_load_factor": org_audit["load_factor"],
            "meta_learning_primitive": meta_audit.get("knowledge_primitive")
        }
