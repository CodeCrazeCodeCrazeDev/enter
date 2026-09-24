"""
Executable 14-Layer Engine for the Computational Architecture of Entrepreneurship.

This module formalizes and executes all 14 layers of entrepreneurship:
1. Reality Substrate
2. Opportunity Discovery
3. Problem Discovery
4. Decision Making
5. Opportunity Evaluation
6. Product Creation
7. Customer Understanding
8. Marketing
9. Sales
10. Growth
11. Competition
12. Organizational Design
13. Meta-Learning
14. AI Entrepreneurship & Autonomous Orchestration
"""

from __future__ import annotations

import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.fourteen_layer_engine")


# ============================================================================
# Layer 1: Reality Substrate
# ============================================================================

class RealitySubstrate(BaseModel):
    """Layer 1: Formalizes non-automatable vs automatable invariants."""
    asymmetric_value_ratio: float = 10.0  # Value created / cost
    captured_value_fraction: float = 0.2  # Fraction of value captured
    skin_in_the_game_weight: float = 1.0  # Loss penalty multiplier
    non_linear_leverage_multiplier: float = 5.0  # Capital/software/network multiplier

    def evaluate_entropy_reduction(self, initial_disorder: float, final_disorder: float) -> float:
        """Calculates economic entropy reduction delta."""
        return max(0.0, initial_disorder - final_disorder)


# ============================================================================
# Layer 2: Opportunity Discovery
# ============================================================================

class WeakSignal(BaseModel):
    """Represents a weak external signal sensed in state space."""
    signal_id: UUID = Field(default_factory=uuid4)
    domain: str
    intensity: float
    reconstruction_error: float
    economic_relevance: float


class OpportunityDiscoveryEngine:
    """Layer 2: Continuous state-space search and weak signal filtering."""

    def filter_weak_signals(self, signals: List[WeakSignal], anomaly_threshold: float = 2.0) -> List[WeakSignal]:
        """Filters weak signals using reconstruction error thresholds."""
        return [s for s in signals if s.reconstruction_error >= anomaly_threshold and s.economic_relevance > 0.5]

    def compute_opportunity_delta_u(self, utility_before: float, utility_after: float, cost: float) -> float:
        """Calculates net utility gain from state intervention."""
        return utility_after - utility_before - cost


# ============================================================================
# Layer 3: Problem Discovery
# ============================================================================

class ProblemNode(BaseModel):
    """Represents a problem in a Causal DAG."""
    node_id: str
    is_root_cause: bool = False
    observed_friction: float = 0.0


class ProblemDiscoveryEngine:
    """Layer 3: Structural Causal Model problem decomposition and do-calculus."""

    def identify_root_cause(self, nodes: List[ProblemNode], causal_weights: Dict[str, float]) -> Optional[ProblemNode]:
        """Identifies root cause node with highest causal derivative impact."""
        if not nodes:
            return None
        return max(nodes, key=lambda n: causal_weights.get(n.node_id, 0.0))

    def should_ignore_problem(self, expected_value_delta: float, intervention_cost: float, opportunity_cost: float) -> bool:
        """Determines if a problem should be ignored entirely."""
        return expected_value_delta < (intervention_cost + opportunity_cost)


# ============================================================================
# Layer 4: Decision Making
# ============================================================================

class DecisionState(BaseModel):
    """Layer 4: Active Inference decision state."""
    prior_entropy: float = 1.5
    posterior_entropy: float = 0.3
    pragmatic_value: float = 2.0  # Goal alignment utility
    curiosity_weight: float = 1.0

    def compute_expected_free_energy(self) -> float:
        """Calculates Active Inference EFE (G = - Pragmatic - Epistemic * Curiosity)."""
        epistemic_value = max(0.0, self.prior_entropy - self.posterior_entropy)
        return -self.pragmatic_value - (epistemic_value * self.curiosity_weight)


# ============================================================================
# Layer 5: Opportunity Evaluation
# ============================================================================

class OpportunityEvaluator:
    """Layer 5: Expected Value, downside risk, and abandonment thresholding."""

    def calculate_net_present_value(
        self, tam: float, success_prob: float, discount_rate: float = 0.1, duration_years: int = 5
    ) -> float:
        """Calculates discounted Expected Value over project horizon."""
        npv = 0.0
        annual_cash_flow = tam * 0.05 * success_prob  # 5% market capture assumption
        for t in range(1, duration_years + 1):
            npv += annual_cash_flow / math.pow(1.0 + discount_rate, t)
        return npv

    def check_abandonment_threshold(self, current_posterior: float, alternative_ev: float, current_ev: float) -> bool:
        """Checks whether an active opportunity should be killed."""
        if current_ev <= 0.0:
            return True
        threshold = alternative_ev / current_ev
        return current_posterior < min(0.9, threshold * 0.5)


# ============================================================================
# Layer 6: Product Creation
# ============================================================================

class FeatureSpec(BaseModel):
    """Specification of a proposed product feature."""
    feature_id: str
    causal_path_length: int  # Path length to core value delivery
    complexity_penalty: float


class ProductCreationEngine:
    """Layer 6: Minimal critical path feature rejection and JTBD transformation."""

    def filter_essential_features(self, features: List[FeatureSpec], max_path_length: int = 3) -> List[FeatureSpec]:
        """Rejects non-essential features that lie outside the core critical path."""
        return [f for f in features if f.causal_path_length <= max_path_length and f.complexity_penalty < 1.0]


# ============================================================================
# Layer 7: Customer Understanding
# ============================================================================

class CustomerPsychologyEngine:
    """Layer 7: Prospect theory utility and switching friction dynamics."""

    def compute_prospect_utility(self, value: float, loss_aversion: float = 2.25) -> float:
        """Prospect theory value function."""
        if value >= 0.0:
            return math.pow(value, 0.88)
        else:
            return -loss_aversion * math.pow(abs(value), 0.88)

    def will_customer_switch(self, new_utility: float, current_utility: float, switching_cost: float) -> bool:
        """Evaluates customer switching threshold."""
        return (new_utility - current_utility) > switching_cost


# ============================================================================
# Layer 8: Marketing
# ============================================================================

class MarketingEngine:
    """Layer 8: Virality epidemiological SIR dynamics and brand emergence."""

    def compute_viral_reproduction_number(self, invites_per_user: float, conversion_rate: float) -> float:
        """Computes K-factor (K = i * c). K > 1 indicates viral compounding growth."""
        return invites_per_user * conversion_rate


# ============================================================================
# Layer 9: Sales
# ============================================================================

class SalesEngine:
    """Layer 9: Customer uncertainty resolution and cost of inaction."""

    def calculate_cost_of_inaction(self, monthly_inefficiency: float, duration_months: int, rate: float = 0.02) -> float:
        """Calculates compounding financial cost of customer inaction."""
        total = 0.0
        for m in range(1, duration_months + 1):
            total += monthly_inefficiency * math.exp(rate * m)
        return total


# ============================================================================
# Layer 10: Growth
# ============================================================================

class GrowthEngine:
    """Layer 10: Compounding growth and intentional operational throttling."""

    def should_throttle_growth(self, acquisition_rate: float, ops_capacity_rate: float) -> bool:
        """Triggers growth throttling if acquisition exceeds operational fulfillment capacity."""
        return acquisition_rate > ops_capacity_rate


# ============================================================================
# Layer 11: Competition
# ============================================================================

class CompetitionEngine:
    """Layer 11: Competitor anticipation, moats, and pivot triggers."""

    def evaluate_pivot_necessity(self, ltv_cac_ratios: List[float], min_threshold: float = 3.0) -> bool:
        """Triggers pivot if mean LTV/CAC systematically falls below threshold."""
        if not ltv_cac_ratios:
            return False
        avg_ratio = sum(ltv_cac_ratios) / len(ltv_cac_ratios)
        return avg_ratio < min_threshold


# ============================================================================
# Layer 12: Organizational Design
# ============================================================================

class OrgDesignEngine:
    """Layer 12: Hiring triggers and delegation mechanics."""

    def should_hire_agent(self, task_workload_hours: float, delegation_overhead: float, capacity_per_agent: float = 40.0) -> bool:
        """Evaluates whether to spawn an autonomous sub-agent/hire."""
        effective_capacity = capacity_per_agent - delegation_overhead
        return task_workload_hours > effective_capacity


# ============================================================================
# Layer 13: Meta-Learning
# ============================================================================

class MetaLearningEngine:
    """Layer 13: Hyper-parameter mental model updates from historical episodes."""

    def update_system_priors(self, prior_weight: float, episode_outcome: float, learning_rate: float = 0.1) -> float:
        """Updates global system strategic prior weight."""
        return prior_weight + learning_rate * (episode_outcome - prior_weight)


# ============================================================================
# Layer 14: AI Entrepreneurship & Autonomous Orchestration
# ============================================================================

class ResourceAllocationPlan(BaseModel):
    """Resource allocation budget across projects."""
    capital_usd: float
    compute_flops: float
    time_hours: float
    talent_agents: int


class AutonomousAIEntrepreneurEngine:
    """
    Layer 14: Complete 14-layer master orchestrator formalizing AI entrepreneurship.
    Executes capital, compute, time, and talent allocation and EROICC tracking.
    """

    def __init__(self) -> None:
        self.reality = RealitySubstrate()
        self.opportunity_discovery = OpportunityDiscoveryEngine()
        self.problem_discovery = ProblemDiscoveryEngine()
        self.evaluator = OpportunityEvaluator()
        self.product_engine = ProductCreationEngine()
        self.customer_engine = CustomerPsychologyEngine()
        self.marketing = MarketingEngine()
        self.sales = SalesEngine()
        self.growth = GrowthEngine()
        self.competition = CompetitionEngine()
        self.org_design = OrgDesignEngine()
        self.meta_learning = MetaLearningEngine()

    def allocate_resources(
        self,
        total_capital: float,
        total_flops: float,
        total_time: float,
        opportunities: List[Dict[str, Any]]
    ) -> Dict[str, ResourceAllocationPlan]:
        """Allocates capital, compute, and time across competing opportunities proportional to EV."""
        if not opportunities:
            return {}

        total_ev = sum(opp.get("ev", 1.0) for opp in opportunities)
        allocations: Dict[str, ResourceAllocationPlan] = {}

        for opp in opportunities:
            opp_id = opp.get("id", "opp_default")
            ev = opp.get("ev", 1.0)
            share = ev / max(1e-6, total_ev)

            allocations[opp_id] = ResourceAllocationPlan(
                capital_usd=total_capital * share,
                compute_flops=total_flops * share,
                time_hours=total_time * share,
                talent_agents=max(1, int(10 * share))
            )

        return allocations

    def calculate_eroicc(
        self,
        valuation_change: float,
        free_cash_flow_change: float,
        capital_consumed: float,
        flops_consumed: float,
        flops_cost_weight: float = 1e-12
    ) -> float:
        """
        Calculates Entrepreneurial Return on Invested Compute and Capital (EROICC):
        EROICC = (Delta Valuation + Delta FCF) / (Capital Consumed + beta * Compute FLOPS)
        """
        total_denominator = capital_consumed + (flops_consumed * flops_cost_weight)
        if total_denominator <= 0.0:
            return 0.0
        return (valuation_change + free_cash_flow_change) / total_denominator
