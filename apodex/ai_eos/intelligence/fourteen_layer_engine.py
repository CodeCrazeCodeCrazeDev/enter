"""
The complete, first-principles executable 14-Layer Computational Engine of
Entrepreneurship for SERO / APODEX AI EOS.

Formalizes all 14 layers of entrepreneurship:
  - Layer 1: Reality Substrate & Invariant Principles
  - Layer 2: Opportunity Search & Weak Signal Detection
  - Layer 3: Problem Discovery & Root Cause Decomposition
  - Layer 4: Decision Engine Under Uncertainty (Active Inference EFE)
  - Layer 5: Opportunity Valuation & Dynamic Real-Options Allocation
  - Layer 6: Product Synthesis & Jobs-To-Be-Done (JTBD)
  - Layer 7: Customer Understanding & Psychological Transitions
  - Layer 8: Marketing & Information Diffusion (Bass / Virality)
  - Layer 9: Repeatable Sales Engine & Objection Graphs
  - Layer 10: Compounding Growth & Network Effects
  - Layer 11: Competitive Dynamics & Moats
  - Layer 12: Adaptive Organizational Scaling & Capacity Limits
  - Layer 13: Meta-Learning & Failure Reusability
  - Layer 14: Autonomous AI Entrepreneurship Orchestration
"""

from __future__ import annotations
import math
import logging
import random
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.fourteen_layer_engine")


# =====================================================================
# Data Models
# =====================================================================
class Signal(BaseModel):
    signal_id: UUID = Field(default_factory=uuid4)
    domain: str
    historical_variance: float = 0.1
    recent_variance: float = 0.5
    delta_mean: float = 1.2
    entropy_kl_div: float = 0.8
    metadata: Dict[str, Any] = Field(default_factory=dict)


class OpportunityCandidate(BaseModel):
    opportunity_id: UUID = Field(default_factory=uuid4)
    title: str
    domain_a: str
    domain_b: str
    vector_embedding: List[float] = Field(default_factory=list)
    tam_cents: int = 100000000
    estimated_ltv_cents: int = 300000
    estimated_cac_cents: int = 50000
    prior_entropy: float = 1.5
    post_entropy_simulated: float = 0.4
    success_probability: float = 0.5
    target_preference: float = 0.90
    novelty_score: float = 0.0
    is_active: bool = True


class CausalNode(BaseModel):
    name: str
    is_root_cause: bool = False
    friction_weight: float = 1.0


class ProblemDAG(BaseModel):
    problem_id: UUID = Field(default_factory=uuid4)
    nodes: Dict[str, CausalNode] = Field(default_factory=dict)
    edges: List[Tuple[str, str, float]] = Field(default_factory=list)  # (parent, child, weight)
    observed_friction: float = 10.0


class JobToBeDone(BaseModel):
    job_id: UUID = Field(default_factory=uuid4)
    target_outcome: str
    functional_delta: float = 0.8
    emotional_delta: float = 0.6
    social_delta: float = 0.4
    current_friction: float = 0.9


class Feature(BaseModel):
    feature_id: str
    name: str
    utility_gain: float
    complexity_cost: float


# =====================================================================
# Layer 1: Reality Substrate & Invariant Principles
# =====================================================================
class Layer1_RealitySubstrate:
    """Evaluates optimization vs. human psychology boundaries & invariant principle checks."""

    def check_invariant_principles(self, ltv_cents: int, cac_cents: int, adaptation_rate: float, decay_rate: float) -> Dict[str, Any]:
        unit_economics_valid = (ltv_cents - cac_cents) > 0
        feedback_velocity_valid = adaptation_rate > decay_rate

        return {
            "unit_economics_valid": unit_economics_valid,
            "ltv_to_cac_ratio": ltv_cents / max(1, cac_cents),
            "feedback_velocity_valid": feedback_velocity_valid,
            "can_automate_execution": True,
            "requires_human_judgment": False if unit_economics_valid and feedback_velocity_valid else True
        }


# =====================================================================
# Layer 2: Opportunity Search Engine
# =====================================================================
class Layer2_OpportunitySearchEngine:
    """Searches state space for weak signals, filters entropy, and performs bisociative combinations."""

    def detect_weak_signals(self, signals: List[Signal], kl_threshold: float = 0.5) -> List[Signal]:
        detected = []
        for sig in signals:
            signal_score = (sig.recent_variance / max(1e-5, sig.historical_variance)) * abs(sig.delta_mean)
            if sig.entropy_kl_div >= kl_threshold and signal_score > 1.5:
                detected.append(sig)
        return detected

    def bisociative_combination(self, signal_a: Signal, signal_b: Signal) -> OpportunityCandidate:
        """Combines disparate domain signals to create a novel candidate opportunity."""
        title = f"Bisociative Arbitrage: {signal_a.domain} x {signal_b.domain}"
        novelty = (signal_a.entropy_kl_div + signal_b.entropy_kl_div) / 2.0
        return OpportunityCandidate(
            title=title,
            domain_a=signal_a.domain,
            domain_b=signal_b.domain,
            novelty_score=novelty,
            prior_entropy=1.8,
            post_entropy_simulated=0.5
        )


# =====================================================================
# Layer 3: Problem Decomposition Engine
# =====================================================================
class Layer3_ProblemDecompositionEngine:
    """Uses Structural Causal Model graphs to decompose symptoms into root causes."""

    def analyze_root_cause(self, dag: ProblemDAG) -> Tuple[str, float]:
        """Identifies the root cause node that maximizes friction reduction under intervention."""
        best_node = ""
        max_friction_reduction = -1.0

        for node_name, node in dag.nodes.items():
            # Calculate incoming and outgoing weights
            out_weight = sum(w for p, c, w in dag.edges if p == node_name)
            reduction = node.friction_weight * (1.0 + out_weight)
            if reduction > max_friction_reduction:
                max_friction_reduction = reduction
                best_node = node_name

        return best_node, max_friction_reduction

    def evaluate_active_ignore(self, solve_cost_cents: int, recovery_value_cents: int) -> bool:
        """Returns True if the problem should be actively ignored (cost > value)."""
        return solve_cost_cents > recovery_value_cents


# =====================================================================
# Layer 4: Active Inference Decision Engine
# =====================================================================
class Layer4_ActiveInferenceDecisionEngine:
    """Minimizes Expected Free Energy (EFE) G = - Pragmatic Value - Curiosity * Epistemic Value."""

    def calculate_efe(self, opp: OpportunityCandidate, curiosity_weight: float = 1.0) -> float:
        eps = 1e-10
        p_success = max(eps, min(1.0 - eps, opp.success_probability))
        p_target = max(eps, min(1.0 - eps, opp.target_preference))

        pragmatic_value = math.log(p_success) - math.log(p_target)
        epistemic_value = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)

        efe = -pragmatic_value - (epistemic_value * curiosity_weight)
        return efe

    def check_fast_kill_gate(self, posterior_confidence: float, kill_threshold: float = 0.25) -> bool:
        """Triggers fast kill gate if posterior confidence falls below threshold."""
        return posterior_confidence < kill_threshold


# =====================================================================
# Layer 5: Opportunity Valuation Engine
# =====================================================================
class Layer5_OpportunityValuationEngine:
    """Computes Expected Value, Downside CVaR, and Black-Scholes Real Options pricing."""

    def calculate_probabilistic_ev(self, opp: OpportunityCandidate) -> float:
        ev = (opp.success_probability * opp.tam_cents) - opp.estimated_cac_cents
        return float(ev)

    def estimate_cvar(self, downside_losses: List[float], alpha: float = 0.95) -> float:
        """Computes Conditional Value at Risk at alpha confidence level."""
        if not downside_losses:
            return 0.0
        sorted_losses = sorted(downside_losses, reverse=True)
        cutoff_index = max(1, int(len(sorted_losses) * (1.0 - alpha)))
        cvar = sum(sorted_losses[:cutoff_index]) / cutoff_index
        return float(cvar)

    def black_scholes_real_option(self, S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Black-Scholes call option pricing formula for real options evaluation."""
        if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
            return max(0.0, S - K)

        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        # Approximate normal CDF
        def norm_cdf(x: float) -> float:
            return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

        call_price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
        return max(0.0, float(call_price))


# =====================================================================
# Layer 6: Product Synthesis Engine
# =====================================================================
class Layer6_ProductSynthesisEngine:
    """Enforces complexity budgets and optimizes learning velocity per unit feature."""

    def select_features_under_budget(self, candidate_features: List[Feature], complexity_budget: float) -> List[Feature]:
        # Sort features by efficiency: utility_gain / complexity_cost
        sorted_features = sorted(candidate_features, key=lambda f: f.utility_gain / max(0.01, f.complexity_cost), reverse=True)

        selected = []
        used_budget = 0.0
        for f in sorted_features:
            if used_budget + f.complexity_cost <= complexity_budget:
                selected.append(f)
                used_budget += f.complexity_cost

        return selected


# =====================================================================
# Layer 7: Customer Psychology Engine
# =====================================================================
class Layer7_CustomerPsychologyEngine:
    """Models discrete choice customer decision logits and trust accumulation."""

    def calculate_purchase_probability(self, value_score: float, price: float, friction: float, switching_cost: float) -> float:
        net_utility = value_score - price
        net_friction = friction + switching_cost
        logit = net_utility - net_friction

        # Sigmoid probability
        prob = 1.0 / (1.0 + math.exp(-max(-20.0, min(20.0, logit))))
        return float(prob)

    def accumulate_trust(self, current_trust: float, delight_signal: float, retention_rate: float = 0.90) -> float:
        updated = (retention_rate * current_trust) + (0.2 * delight_signal)
        return float(min(1.0, max(0.0, updated)))


# =====================================================================
# Layer 8: Marketing Diffusion Engine
# =====================================================================
class Layer8_MarketingDiffusionEngine:
    """Implements Bass Diffusion model and K-factor virality calculation."""

    def bass_diffusion_step(self, N_t: float, M: float, p: float = 0.03, q: float = 0.38) -> float:
        """Bass Diffusion: dN/dt = (p + q * N/M) * (M - N)."""
        adoption_rate = (p + q * (N_t / max(1.0, M))) * (M - N_t)
        return float(N_t + max(0.0, adoption_rate))

    def calculate_k_factor(self, invites_sent_per_user: float, conversion_rate: float) -> float:
        """K-factor = invites per user * conversion rate."""
        return float(invites_sent_per_user * conversion_rate)


# =====================================================================
# Layer 9: Repeatable Sales Engine
# =====================================================================
class Layer9_RepeatableSalesEngine:
    """Sales state transition Markov chain and Cost of Inaction (COI) urgency engine."""

    def calculate_cost_of_inaction(self, monthly_bleed_cents: int, duration_months: float) -> int:
        return int(monthly_bleed_cents * duration_months)

    def resolve_objection(self, objection_type: str) -> str:
        playbook = {
            "price_too_high": "Demonstrate ROI payback < 3 months with counterfactual case study.",
            "implementation_complexity": "Offer zero-integration turnkey pilot script.",
            "security_compliance": "Provide SOC2 Type II compliance audit packet."
        }
        return playbook.get(objection_type, "Standard consultation discovery workflow.")


# =====================================================================
# Layer 10: Compounding Growth Engine
# =====================================================================
class Layer10_CompoundingGrowthEngine:
    """Models Metcalfe's Law network value and retention asymptotics."""

    def metcalfe_value(self, active_users: int) -> float:
        """Metcalfe's Law: V = k * N^2."""
        return float(0.01 * (active_users ** 2))

    def predict_day30_retention_asymptote(self, day1_retention: float, day7_retention: float) -> float:
        """Log-decay extrapolation for long-term cohort asymptote."""
        asymptote = day7_retention * (day7_retention / max(0.01, day1_retention))
        return float(max(0.05, min(0.95, asymptote)))


# =====================================================================
# Layer 11: Competitive Moat Engine
# =====================================================================
class Layer11_CompetitiveMoatEngine:
    """Calculates composite Moat Durability Score (MDS)."""

    def calculate_mds(self, switching_cost: float, network_density: float, cost_advantage: float, brand_equity: float) -> float:
        mds = (0.3 * switching_cost) + (0.3 * network_density) + (0.2 * cost_advantage) + (0.2 * brand_equity)
        return float(min(1.0, max(0.0, mds)))


# =====================================================================
# Layer 12: Adaptive Organizational Scaling Engine
# =====================================================================
class Layer12_OrganizationalScalingEngine:
    """Kingman queue latency model to trigger hiring or autonomous agent delegation."""

    def calculate_queue_wait_time(self, utilization: float, service_time_mean: float) -> float:
        """Kingman's formula approximation for queue wait latency."""
        if utilization >= 0.99:
            return 999.0
        wait_time = (utilization / (1.0 - utilization)) * service_time_mean
        return float(wait_time)

    def evaluate_delegation_threshold(self, utilization: float) -> str:
        if utilization > 0.85:
            return "DELEGATE_TO_AI_WORKERS"
        elif utilization > 0.70:
            return "SCALE_ORGANIZATIONAL_PODS"
        return "OPTIMAL_CAPACITY"


# =====================================================================
# Layer 13: Meta-Learning Engine
# =====================================================================
class Layer13_MetaLearningEngine:
    """Bayesian hierarchical meta-learning and failure graph constraint updates."""

    def compute_counterfactual_skill_score(self, actual_return: float, benchmark_return: float) -> float:
        """Isolates true founder skill score from environmental market luck."""
        alpha_skill = actual_return - benchmark_return
        return float(alpha_skill)

    def update_failure_memory(self, failure_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extracts reusable structural constraints from failure records."""
        constrained_rules = []
        for rec in failure_records:
            rule = f"Constraint rule: avoid {rec.get('trigger_cause')} under condition {rec.get('condition')}"
            constrained_rules.append(rule)
        return {"reusable_constraints": constrained_rules, "failure_count": len(failure_records)}


# =====================================================================
# Layer 14: Autonomous AI Entrepreneurship Orchestrator
# =====================================================================
class Layer14_AutonomousAIEntrepreneur:
    """Orchestrates multi-agent execution, experiment design, and dynamic resource allocation."""

    def allocate_resources(self, opportunities: List[OpportunityCandidate], total_budget_cents: int) -> Dict[UUID, int]:
        if not opportunities:
            return {}

        total_score = sum(opp.success_probability * opp.novelty_score + 0.1 for opp in opportunities)
        allocations = {}
        for opp in opportunities:
            score = opp.success_probability * opp.novelty_score + 0.1
            share = score / total_score if total_score > 0 else 1.0 / len(opportunities)
            allocations[opp.opportunity_id] = int(total_budget_cents * share)

        return allocations


# =====================================================================
# Master Orchestrating Engine
# =====================================================================
class FourteenLayerEntrepreneurialEngine:
    """The unified master engine coordinating all 14 computational layers."""

    def __init__(self) -> None:
        self.l1 = Layer1_RealitySubstrate()
        self.l2 = Layer2_OpportunitySearchEngine()
        self.l3 = Layer3_ProblemDecompositionEngine()
        self.l4 = Layer4_ActiveInferenceDecisionEngine()
        self.l5 = Layer5_OpportunityValuationEngine()
        self.l6 = Layer6_ProductSynthesisEngine()
        self.l7 = Layer7_CustomerPsychologyEngine()
        self.l8 = Layer8_MarketingDiffusionEngine()
        self.l9 = Layer9_RepeatableSalesEngine()
        self.l10 = Layer10_CompoundingGrowthEngine()
        self.l11 = Layer11_CompetitiveMoatEngine()
        self.l12 = Layer12_OrganizationalScalingEngine()
        self.l13 = Layer13_MetaLearningEngine()
        self.l14 = Layer14_AutonomousAIEntrepreneur()

    def execute_full_14_layer_pipeline(
        self,
        raw_signals: List[Signal],
        available_capital_cents: int
    ) -> Dict[str, Any]:
        """Runs the complete end-to-end 14-layer analysis and orchestration cycle."""
        # Layer 1: Invariant Principles Check
        l1_status = self.l1.check_invariant_principles(300000, 50000, 2.0, 0.5)

        # Layer 2: Weak Signal Detection & Bisociation
        weak_signals = self.l2.detect_weak_signals(raw_signals)
        if len(weak_signals) >= 2:
            opp_candidate = self.l2.bisociative_combination(weak_signals[0], weak_signals[1])
        else:
            opp_candidate = OpportunityCandidate(
                title="Synthetic High-Growth Opportunity",
                domain_a="AI", domain_b="SaaS", novelty_score=0.9
            )

        # Layer 3: Causal Problem DAG
        dag = ProblemDAG(
            nodes={
                "high_latency": CausalNode(name="high_latency", is_root_cause=True, friction_weight=3.0),
                "customer_churn": CausalNode(name="customer_churn", friction_weight=2.0)
            },
            edges=[("high_latency", "customer_churn", 1.5)]
        )
        root_cause, reduction = self.l3.analyze_root_cause(dag)

        # Layer 4: Active Inference EFE
        efe = self.l4.calculate_efe(opp_candidate)

        # Layer 5: Opportunity Valuation
        ev = self.l5.calculate_probabilistic_ev(opp_candidate)
        real_option_val = self.l5.black_scholes_real_option(ev, available_capital_cents * 0.1, 1.0, 0.05, 0.3)

        # Layer 6: Product Synthesis
        selected_features = self.l6.select_features_under_budget([
            Feature(feature_id="f1", name="Core Engine", utility_gain=0.9, complexity_cost=2.0),
            Feature(feature_id="f2", name="Bloat Feature", utility_gain=0.1, complexity_cost=5.0)
        ], complexity_budget=3.0)

        # Layer 7: Customer Psychology
        buy_prob = self.l7.calculate_purchase_probability(value_score=10.0, price=2.0, friction=1.0, switching_cost=1.0)

        # Layer 8: Marketing Diffusion
        bass_n1 = self.l8.bass_diffusion_step(N_t=100.0, M=10000.0)

        # Layer 9: Sales Engine
        coi = self.l9.calculate_cost_of_inaction(monthly_bleed_cents=1000000, duration_months=3.0)

        # Layer 10: Compounding Growth
        metcalfe_v = self.l10.metcalfe_value(active_users=1000)

        # Layer 11: Competitive Moats
        mds = self.l11.calculate_mds(switching_cost=0.8, network_density=0.7, cost_advantage=0.6, brand_equity=0.5)

        # Layer 12: Organizational Design
        delegation_action = self.l12.evaluate_delegation_threshold(utilization=0.88)

        # Layer 13: Meta-Learning
        skill_score = self.l13.compute_counterfactual_skill_score(actual_return=0.35, benchmark_return=0.10)

        # Layer 14: AI Orchestration Capital Allocation
        allocations = self.l14.allocate_resources([opp_candidate], available_capital_cents)

        return {
            "status": "success",
            "layer1_invariants": l1_status,
            "layer2_weak_signals_count": len(weak_signals),
            "opportunity_title": opp_candidate.title,
            "layer3_root_cause": root_cause,
            "layer4_efe": efe,
            "layer5_probabilistic_ev": ev,
            "layer5_real_option_value": real_option_val,
            "layer6_features_selected": [f.name for f in selected_features],
            "layer7_purchase_probability": buy_prob,
            "layer8_bass_diffusion_next": bass_n1,
            "layer9_cost_of_inaction": coi,
            "layer10_metcalfe_value": metcalfe_v,
            "layer11_moat_durability_score": mds,
            "layer12_delegation_action": delegation_action,
            "layer13_skill_score": skill_score,
            "layer14_allocations": allocations
        }
