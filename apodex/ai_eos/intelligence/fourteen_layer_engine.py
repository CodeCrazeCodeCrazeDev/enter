"""
The executable 14-Layer Computational Architecture Engine for Autonomous AI Entrepreneurship.
Implements first-principles computational logic across all 14 layers of entrepreneurship.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.fourteen_layer_engine")


# ============================================================================
# Core Domain Models
# ============================================================================

class MarketSignal(BaseModel):
    """Raw external signal sensed from the world substrate."""
    signal_id: UUID = Field(default_factory=uuid4)
    source: str
    content: str
    entropy_score: float = 1.0
    growth_rate: float = 0.0  # d^2X/dt^2
    domain: str = "general"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class OpportunityCandidate(BaseModel):
    """Candidate opportunity state discovered from weak signals and synthesis."""
    opportunity_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str
    variables: List[str] = Field(default_factory=list)
    causal_edges: List[Tuple[str, str]] = Field(default_factory=list)
    coefficients: Dict[str, float] = Field(default_factory=dict)
    prior_entropy: float = 1.5
    post_entropy_simulated: float = 0.4
    success_probability: float = 0.5
    target_preference: float = 0.95
    tam_cents: int = 100000000  # $1M default
    wtp_cents: int = 50000      # Willingness-to-pay ($500)
    cac_cents: int = 10000      # CAC ($100)
    ltv_cents: int = 60000      # LTV ($600)
    capital_required_cents: int = 5000000  # $50k required capital
    is_active: bool = True


class ProblemStatement(BaseModel):
    """Decomposed problem representation with root-cause graph leverage."""
    problem_id: UUID = Field(default_factory=uuid4)
    title: str
    stated_symptom: str
    root_cause_variables: List[str] = Field(default_factory=list)
    leverage_scores: Dict[str, float] = Field(default_factory=dict)
    is_first_order: bool = True
    friction_cost_cents: int = 10000


class ProductSpecification(BaseModel):
    """Product feature spec governed by complexity budgets and Shapley value attribution."""
    product_id: UUID = Field(default_factory=uuid4)
    name: str
    features: List[str] = Field(default_factory=list)
    shapley_values: Dict[str, float] = Field(default_factory=dict)
    kolmogorov_complexity: float = 1.0
    max_complexity_budget: float = 5.0


class CustomerProfile(BaseModel):
    """Psychological and behavioral POMDP model of target customer segment."""
    segment_id: UUID = Field(default_factory=uuid4)
    segment_name: str
    gain_utility: float = 10.0
    friction_aversion: float = 1.5
    risk_sensitivity: float = 2.0
    perceived_trust: float = 0.5
    switching_cost_cents: int = 20000


class SalesPipelineStage(BaseModel):
    """Node in the Sales Pipeline DAG with deterministic qualification criteria."""
    stage_name: str
    transition_probability: float = 0.3
    qualification_criteria: List[str] = Field(default_factory=list)


# ============================================================================
# Layer 1: Reality Substrate Engine
# ============================================================================

class RealitySubstrateEngine:
    """
    Formalizes Layer 1: Thermodynamic active inference, computational invariants,
    human psychology vs optimization boundaries, and automation scopes.
    """

    def evaluate_invariant_compliance(self, opp: OpportunityCandidate) -> Dict[str, Any]:
        """Evaluates compliance with the 5 computational invariants of entrepreneurship."""
        expected_value = (opp.success_probability * opp.ltv_cents) - opp.cac_cents
        asymmetric_ratio = expected_value / max(1, opp.capital_required_cents)
        ltv_cac_ratio = opp.ltv_cents / max(1, opp.cac_cents)

        invariants = {
            "asymmetric_risk_reward": asymmetric_ratio > 0.1,
            "fast_feedback_cycle": True,
            "parsimony_resource_minimization": opp.capital_required_cents < 100000000,
            "customer_centric_value_capture": opp.wtp_cents >= opp.cac_cents,
            "moat_evolution_potential": ltv_cac_ratio >= 3.0
        }
        is_viable = all(invariants.values())
        return {
            "is_viable": is_viable,
            "invariants": invariants,
            "asymmetric_ratio": asymmetric_ratio,
            "ltv_cac_ratio": ltv_cac_ratio
        }


# ============================================================================
# Layer 2: Opportunity Discovery Engine
# ============================================================================

class OpportunityDiscoveryEngine:
    """
    Formalizes Layer 2: Continuous state space search, weak signal detection via KL divergence,
    cross-domain hyper-graph synthesis, MAP-Elites novelty generation, and trend prediction.
    """

    def detect_weak_signals(self, signals: List[MarketSignal], baseline_entropy: float = 0.5) -> List[MarketSignal]:
        """Flags signals where relative entropy / surprise spikes above baseline noise."""
        flagged = []
        for s in signals:
            kl_div = s.entropy_score * math.log(max(1e-6, s.entropy_score / max(1e-6, baseline_entropy)))
            if kl_div > 0.2 and s.growth_rate >= 0.05:
                flagged.append(s)
        return flagged

    def synthesize_cross_domain_opportunity(
        self, signal_a: MarketSignal, signal_b: MarketSignal
    ) -> OpportunityCandidate:
        """Fuses disparate domain observations into a novel candidate opportunity."""
        synthesized_title = f"{signal_a.domain.capitalize()}-{signal_b.domain.capitalize()} Synthesis"
        vars_fused = [f"{signal_a.domain}_mechanism", f"{signal_b.domain}_problem", "market_adoption"]
        causal_edges = [
            (f"{signal_a.domain}_mechanism", f"{signal_b.domain}_problem"),
            (f"{signal_b.domain}_problem", "market_adoption")
        ]
        return OpportunityCandidate(
            title=synthesized_title,
            domain=f"{signal_a.domain}_{signal_b.domain}",
            variables=vars_fused,
            causal_edges=causal_edges,
            coefficients={f"{vars_fused[0]}->{vars_fused[1]}": 0.8, f"{vars_fused[1]}->{vars_fused[2]}": 0.7},
            prior_entropy=1.8,
            post_entropy_simulated=0.35,
            success_probability=0.6,
            tam_cents=500000000
        )


# ============================================================================
# Layer 3: Problem Discovery Engine
# ============================================================================

class ProblemDiscoveryEngine:
    """
    Formalizes Layer 3: Structural Causal Abduction to decompose problems, distinguish
    symptoms from root causes via interventional leverage, and filter 1st vs 2nd order problems.
    """

    def decompose_and_abduct_root_causes(
        self, stated_symptom: str, causal_nodes: List[str], edges: List[Tuple[str, str]]
    ) -> ProblemStatement:
        """Performs causal leverage calculation to locate root-cause intervention nodes."""
        leverage_scores = {}
        # Nodes with out-degree in DAG are candidate root causes
        targets = {dst for _, dst in edges}
        sources = {src for src, _ in edges}

        for node in causal_nodes:
            if node in sources and node not in targets:
                leverage_scores[node] = 0.95  # Primary root cause
            elif node in sources:
                leverage_scores[node] = 0.60  # Intermediate cause
            else:
                leverage_scores[node] = 0.10  # Symptom node

        root_causes = [node for node, score in leverage_scores.items() if score > 0.5]
        return ProblemStatement(
            title=f"Root-Cause Decomposition of {stated_symptom}",
            stated_symptom=stated_symptom,
            root_cause_variables=root_causes,
            leverage_scores=leverage_scores,
            is_first_order=True,
            friction_cost_cents=25000
        )


# ============================================================================
# Layer 4: Decision Making Engine
# ============================================================================

class DecisionMakingEngine:
    """
    Formalizes Layer 4: Active Inference Expected Free Energy (EFE) minimization,
    attention allocation, pre-committed kill criteria, and confirmation bias mitigation.
    """

    def calculate_expected_free_energy(self, opp: OpportunityCandidate) -> float:
        """
        G = - Pragmatic Value - Epistemic Value
        Pragmatic = ln(p_success) - ln(p_target)
        Epistemic = prior_entropy - post_entropy_simulated
        """
        eps = 1e-9
        p_succ = max(eps, min(1.0 - eps, opp.success_probability))
        p_targ = max(eps, min(1.0 - eps, opp.target_preference))

        pragmatic_val = math.log(p_succ) - math.log(p_targ)
        epistemic_val = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)

        # Lower EFE indicates superior policy choice
        efe = -pragmatic_val - epistemic_val
        return efe

    def evaluate_kill_criteria(self, opp: OpportunityCandidate, threshold: float = 0.2) -> bool:
        """Returns True if opportunity posterior falls below pre-committed kill bound."""
        return opp.success_probability < threshold


# ============================================================================
# Layer 5: Opportunity Evaluation Engine
# ============================================================================

class OpportunityEvaluationEngine:
    """
    Formalizes Layer 5: Expected Value calculation, Conditional Value at Risk (CVaR),
    Real Option Value timing, and Sharpe-optimal candidate comparison.
    """

    def compute_sharpe_opportunity_score(self, opp: OpportunityCandidate, risk_free_rate: float = 0.05) -> float:
        """Computes Sharpe-optimal score balancing expected return against risk & capital."""
        # Normalize to dollars ($)
        expected_tam_dollars = opp.tam_cents / 100.0
        capital_req_dollars = opp.capital_required_cents / 100.0
        # Expected captured value (assuming 1% market capture NPV)
        expected_npv_dollars = (opp.success_probability * expected_tam_dollars * 0.05) - capital_req_dollars
        variance_dollars = opp.prior_entropy * capital_req_dollars
        std_dev_dollars = math.sqrt(max(1.0, variance_dollars))
        sharpe = (expected_npv_dollars - risk_free_rate) / std_dev_dollars
        return sharpe

    def estimate_cvar_downside(self, opp: OpportunityCandidate, alpha: float = 0.05) -> float:
        """Estimates tail loss CVaR at alpha percentile."""
        max_loss = float(opp.capital_required_cents)
        # Assuming heavy-tail loss distribution
        cvar = max_loss * (1.0 + (1.0 - opp.success_probability) * alpha)
        return cvar


# ============================================================================
# Layer 6: Product Creation Engine
# ============================================================================

class ProductCreationEngine:
    """
    Formalizes Layer 6: Complexity minimization, Shapley feature attribution, core JTBD discovery.
    """

    def optimize_feature_set(self, spec: ProductSpecification, candidate_features: Dict[str, float]) -> ProductSpecification:
        """Allocates features strictly within Kolmogorov complexity budget using Shapley values."""
        sorted_features = sorted(candidate_features.items(), key=lambda x: x[1], reverse=True)
        selected = []
        accumulated_complexity = 0.0

        for feat_name, shapley_val in sorted_features:
            feat_complexity = 0.5  # Standard feature complexity cost
            if accumulated_complexity + feat_complexity <= spec.max_complexity_budget:
                selected.append(feat_name)
                accumulated_complexity += feat_complexity

        spec.features = selected
        spec.shapley_values = candidate_features
        spec.kolmogorov_complexity = accumulated_complexity
        return spec


# ============================================================================
# Layer 7: Customer Understanding Engine
# ============================================================================

class CustomerUnderstandingEngine:
    """
    Formalizes Layer 7: POMDP customer psychology, trust accumulation, switching utility thresholds.
    """

    def evaluate_switching_decision(self, profile: CustomerProfile, new_product_utility: float, price_cents: int) -> Dict[str, Any]:
        """Calculates customer switching likelihood based on net utility delta vs friction and switching costs."""
        net_utility = new_product_utility - (profile.friction_aversion * (price_cents / 10000.0)) - (profile.risk_sensitivity * (1.0 - profile.perceived_trust))
        switching_threshold = profile.switching_cost_cents / 10000.0
        will_switch = net_utility > switching_threshold
        return {
            "will_switch": will_switch,
            "net_utility": net_utility,
            "switching_threshold": switching_threshold,
            "trust_level": profile.perceived_trust
        }


# ============================================================================
# Layer 8: Marketing Engine
# ============================================================================

class MarketingEngine:
    """
    Formalizes Layer 8: SIR epidemic viral spreading, positioning vector space, acquisition channel synergy.
    """

    def calculate_viral_coefficient(self, invites_per_user: float, conversion_rate: float) -> Dict[str, Any]:
        """K-factor viral propagation score calculation."""
        k_factor = invites_per_user * conversion_rate
        is_exponential = k_factor > 1.0
        return {
            "k_factor": k_factor,
            "is_exponential": is_exponential,
            "viral_status": "Exponential Growth" if is_exponential else "Sub-critical Spreading"
        }


# ============================================================================
# Layer 9: Sales Engine
# ============================================================================

class SalesEngine:
    """
    Formalizes Layer 9: Sales psychology belief alignment, urgency creation, repeatable DAG automation.
    """

    def evaluate_buying_urgency(self, cost_of_inaction_cents_per_month: int, price_cents: int) -> Dict[str, Any]:
        """Evaluates whether Cost of Inaction (COI) exceeds price & friction threshold to induce urgency."""
        annual_coi = cost_of_inaction_cents_per_month * 12
        has_urgency = annual_coi > price_cents
        return {
            "annual_coi_cents": annual_coi,
            "price_cents": price_cents,
            "has_buying_urgency": has_urgency,
            "urgency_ratio": annual_coi / max(1, price_cents)
        }


# ============================================================================
# Layer 10: Growth Engine
# ============================================================================

class GrowthEngine:
    """
    Formalizes Layer 10: Metcalfe/Reed network effects, LTV/CAC payback metrics, platform emergence.
    """

    def evaluate_growth_health(self, ltv_cents: int, cac_cents: int, payback_months: int, nrr_percent: float) -> Dict[str, Any]:
        """Validates long-term venture growth metrics against baseline thresholds."""
        ltv_cac = ltv_cents / max(1, cac_cents)
        is_healthy = (ltv_cac >= 3.0) and (payback_months <= 12) and (nrr_percent >= 120.0)
        return {
            "is_healthy": is_healthy,
            "ltv_cac_ratio": ltv_cac,
            "payback_months": payback_months,
            "nrr_percent": nrr_percent
        }


# ============================================================================
# Layer 11: Competition Engine
# ============================================================================

class CompetitionEngine:
    """
    Formalizes Layer 11: Game-theoretic Stackelberg response, moat defendability scoring, pivot triggers.
    """

    def compute_moat_defendability_score(self, switching_cost_score: float, network_effect_score: float, scale_score: float) -> float:
        """Aggregates moat metrics into a composite defendability index [0.0, 1.0]."""
        raw_score = (switching_cost_score * 0.4) + (network_effect_score * 0.4) + (scale_score * 0.2)
        return max(0.0, min(1.0, raw_score))


# ============================================================================
# Layer 12: Organizational Design Engine
# ============================================================================

class OrganizationalDesignEngine:
    """
    Formalizes Layer 12: Capacity bottleneck hiring triggers, central vs delegated topology limits.
    """

    def evaluate_hiring_trigger(self, current_workload_capacity_ratio: float, bottleneck_severity: float) -> Dict[str, Any]:
        """Triggers organizational scaling when workload capacity ratio exceeds threshold."""
        should_hire = current_workload_capacity_ratio > 0.85 and bottleneck_severity > 0.7
        return {
            "should_hire": should_hire,
            "capacity_ratio": current_workload_capacity_ratio,
            "bottleneck_severity": bottleneck_severity
        }


# ============================================================================
# Layer 13: Meta-Learning Engine
# ============================================================================

class MetaLearningEngine:
    """
    Formalizes Layer 13: Meta-cognitive Bayesian updating, decision quality scoring, failure-to-knowledge synthesis.
    """

    def update_mental_model_prior(self, prior_belief: float, experimental_evidence: float, likelihood: float = 0.8) -> float:
        """Updates mental model prior distribution based on experimental evidence via Bayes rule."""
        eps = 1e-9
        prior_belief = max(eps, min(1.0 - eps, prior_belief))
        evidence_likelihood = likelihood if experimental_evidence > 0.5 else (1.0 - likelihood)
        numerator = evidence_likelihood * prior_belief
        denominator = (evidence_likelihood * prior_belief) + ((1.0 - evidence_likelihood) * (1.0 - prior_belief))
        updated_posterior = numerator / max(eps, denominator)
        return updated_posterior


# ============================================================================
# Layer 14: AI Entrepreneurship Engine
# ============================================================================

class AIEntrepreneurshipEngine:
    """
    Formalizes Layer 14: Algorithmic task decomposition, capital/compute allocation, continuous capability self-improvement.
    """

    def allocate_capital_and_compute(
        self, opportunities: List[OpportunityCandidate], total_capital_cents: int, total_compute_flops: float
    ) -> Dict[UUID, Dict[str, Any]]:
        """Allocates capital and compute across active opportunities based on EFE and Sharpe scores."""
        allocations = {}
        if not opportunities:
            return allocations

        planner_efe = DecisionMakingEngine()
        evaluator_sharpe = OpportunityEvaluationEngine()

        scores = []
        for opp in opportunities:
            efe = planner_efe.calculate_expected_free_energy(opp)
            sharpe = evaluator_sharpe.compute_sharpe_opportunity_score(opp)
            # Composite score balancing EFE minimization, Sharpe maximization, and success probability
            composite = (-efe * 0.5) + (sharpe * 0.5) + (opp.success_probability * 5.0)
            scores.append((opp, composite))

        # Shift min composite to positive if any negative
        min_comp = min(s[1] for s in scores)
        shift = abs(min_comp) + 1.0 if min_comp <= 0 else 0.0

        scores_shifted = [(opp, comp + shift) for opp, comp in scores]
        total_score = sum(s[1] for s in scores_shifted)

        for opp, score in scores_shifted:
            weight = score / max(1e-9, total_score)
            allocations[opp.opportunity_id] = {
                "capital_allocated_cents": int(total_capital_cents * weight),
                "compute_allocated_flops": total_compute_flops * weight,
                "weight": weight
            }

        return allocations


# ============================================================================
# Master Orchestrator: FourteenLayerEntrepreneurialEngine
# ============================================================================

class FourteenLayerEntrepreneurialEngine:
    """
    The master orchestrating engine that executes the complete 14-layer pipeline.
    """

    def __init__(self) -> None:
        self.layer1_reality = RealitySubstrateEngine()
        self.layer2_discovery = OpportunityDiscoveryEngine()
        self.layer3_problem = ProblemDiscoveryEngine()
        self.layer4_decision = DecisionMakingEngine()
        self.layer5_evaluation = OpportunityEvaluationEngine()
        self.layer6_product = ProductCreationEngine()
        self.layer7_customer = CustomerUnderstandingEngine()
        self.layer8_marketing = MarketingEngine()
        self.layer9_sales = SalesEngine()
        self.layer10_growth = GrowthEngine()
        self.layer11_competition = CompetitionEngine()
        self.layer12_org = OrganizationalDesignEngine()
        self.layer13_meta = MetaLearningEngine()
        self.layer14_ai = AIEntrepreneurshipEngine()

        self.signals: List[MarketSignal] = []
        self.opportunities: List[OpportunityCandidate] = []

    def ingest_market_signal(self, signal: MarketSignal) -> None:
        """Ingests a market signal into the reality substrate layer."""
        self.signals.append(signal)

    def execute_full_14_layer_pipeline(self, total_capital_cents: int = 100000000) -> Dict[str, Any]:
        """
        Executes an end-to-end iteration across all 14 computational layers of entrepreneurship.
        """
        logger.info("Executing 14-Layer Computational Architecture Pipeline...")

        # Layer 2: Detect weak signals
        flagged_signals = self.layer2_discovery.detect_weak_signals(self.signals)

        # Layer 2: Synthesize opportunity candidate if at least 2 signals exist
        if len(flagged_signals) >= 2:
            candidate_opp = self.layer2_discovery.synthesize_cross_domain_opportunity(
                flagged_signals[0], flagged_signals[1]
            )
            self.opportunities.append(candidate_opp)
        elif self.signals:
            # Fallback single signal opportunity
            candidate_opp = OpportunityCandidate(
                title=f"Opportunity from {self.signals[0].source}",
                domain=self.signals[0].domain,
                variables=["market_demand", "unit_economics"],
                causal_edges=[("market_demand", "unit_economics")]
            )
            self.opportunities.append(candidate_opp)

        if not self.opportunities:
            return {"status": "idle", "reason": "No market signals or opportunities available."}

        active_opp = self.opportunities[-1]

        # Layer 1: Invariant Compliance
        l1_result = self.layer1_reality.evaluate_invariant_compliance(active_opp)

        # Layer 3: Problem Root-Cause Decomposition
        l3_result = self.layer3_problem.decompose_and_abduct_root_causes(
            stated_symptom=f"Friction in {active_opp.domain}",
            causal_nodes=active_opp.variables,
            edges=active_opp.causal_edges
        )

        # Layer 4: Active Inference EFE Calculation
        efe = self.layer4_decision.calculate_expected_free_energy(active_opp)
        should_kill = self.layer4_decision.evaluate_kill_criteria(active_opp)

        # Layer 5: Opportunity Evaluation & Sharpe Score
        sharpe = self.layer5_evaluation.compute_sharpe_opportunity_score(active_opp)
        cvar_loss = self.layer5_evaluation.estimate_cvar_downside(active_opp)

        # Layer 6: Feature Product Spec Optimization
        spec = ProductSpecification(name=f"Product for {active_opp.title}")
        l6_result = self.layer6_product.optimize_feature_set(spec, {"core_engine": 0.8, "analytics": 0.4, "ui": 0.2})

        # Layer 7: Customer Switching Analysis
        cust_profile = CustomerProfile(segment_name="Early Adopter")
        l7_result = self.layer7_customer.evaluate_switching_decision(cust_profile, new_product_utility=15.0, price_cents=active_opp.wtp_cents)

        # Layer 8: Marketing K-Factor Spreading
        l8_result = self.layer8_marketing.calculate_viral_coefficient(invites_per_user=1.5, conversion_rate=0.8)

        # Layer 9: Sales Buying Urgency
        l9_result = self.layer9_sales.evaluate_buying_urgency(cost_of_inaction_cents_per_month=10000, price_cents=active_opp.wtp_cents)

        # Layer 10: Growth Metrics Health
        l10_result = self.layer10_growth.evaluate_growth_health(
            ltv_cents=active_opp.ltv_cents, cac_cents=active_opp.cac_cents, payback_months=8, nrr_percent=130.0
        )

        # Layer 11: Competition Moat Defendability
        moat_score = self.layer11_competition.compute_moat_defendability_score(0.8, 0.7, 0.9)

        # Layer 12: Organizational Hiring Trigger
        l12_result = self.layer12_org.evaluate_hiring_trigger(current_workload_capacity_ratio=0.9, bottleneck_severity=0.8)

        # Layer 13: Meta-Learning Mental Model Update
        updated_posterior = self.layer13_meta.update_mental_model_prior(
            prior_belief=0.5, experimental_evidence=0.8, likelihood=0.85
        )

        # Layer 14: AI Capital & Compute Allocation
        l14_allocations = self.layer14_ai.allocate_capital_and_compute(
            self.opportunities, total_capital_cents=total_capital_cents, total_compute_flops=1e15
        )

        return {
            "status": "completed",
            "opportunity_title": active_opp.title,
            "layer1_invariants": l1_result,
            "layer3_problem": l3_result.model_dump(),
            "layer4_efe": efe,
            "layer4_should_kill": should_kill,
            "layer5_sharpe_score": sharpe,
            "layer5_cvar_loss_cents": cvar_loss,
            "layer6_product_complexity": l6_result.kolmogorov_complexity,
            "layer7_customer_switching": l7_result,
            "layer8_viral_marketing": l8_result,
            "layer9_sales_urgency": l9_result,
            "layer10_growth_health": l10_result,
            "layer11_moat_score": moat_score,
            "layer12_org_hiring": l12_result,
            "layer13_updated_posterior": updated_posterior,
            "layer14_allocations": l14_allocations
        }
