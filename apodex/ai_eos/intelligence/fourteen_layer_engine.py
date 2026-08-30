"""
Fourteen-Layer Computational Architecture of Entrepreneurship.

This module formalizes the 14-layer computational engine of entrepreneurship:
  - Layer 1: Reality Substrate (Invariants, Knightian Uncertainty vs Risk, Automation Bounds)
  - Layer 2: Opportunity Discovery (Continuous State Space Search, Weak Signal Detection, Noise Filtering)
  - Layer 3: Problem Discovery (Structural Causal Decomposition, Symptom vs Root Cause, Triage)
  - Layer 4: Decision Making (Active Inference EFE, Epistemic/Pragmatic Value, Bias Mitigation, Fast Kill)
  - Layer 5: Opportunity Evaluation (Multi-variable Valuation, TAM, CVaR Downside Risk, Pivot Triggers)
  - Layer 6: Product Creation (Jobs-To-Be-Done, Complexity Budgeting, Feature Value Optimization)
  - Layer 7: Customer Understanding (Psychological State Machine, Trust, Switching Dynamics, Evangelism)
  - Layer 8: Marketing & Attention Dynamics (SIR Attention Spread, Virality, Brand Authority, Channel Synergy)
  - Layer 9: Sales Systems (Conversion Mechanics, Urgency, Objection Resolution, Sales Automation)
  - Layer 10: Growth & Ecosystems (Compounding Growth, Network Effects, Platform Evolution, Throttling)
  - Layer 11: Competitive Dynamics & Moats (Rival Anticipation, Defensibility Scoring, Pivot/Disruption Survival)
  - Layer 12: Organizational Design (Hiring Triggers, Centralization vs Delegation, Scalable Structures)
  - Layer 13: Meta-Learning (Brier Decision Scoring, Hindsight Calibration, Mental Model Updates)
  - Layer 14: AI Autonomous Entrepreneurship (Algorithmic vs Causal vs Creative Task Formalization, Resource Allocation)
  - FourteenLayerEntrepreneurshipEngine: Master Orchestrator executing the complete multi-layer pipeline.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("apodex.ai_eos.fourteen_layer_engine")


# ============================================================================
# LAYER 1: REALITY SUBSTRATE
# ============================================================================
class RealityState(BaseModel):
    invariant_principles: List[str] = Field(
        default_factory=lambda: [
            "Value creation precedes value capture",
            "Energy & capital must be conserved across feedback loops",
            "Customer behavior is driven by latent psychological payoffs",
            "Knightian uncertainty cannot be resolved by data extrapolation alone"
        ]
    )
    human_psychology_weight: float = 0.6
    optimization_problem_weight: float = 0.4
    non_automatable_judgment_bounds: List[str] = Field(
        default_factory=lambda: [
            "Terminal ethical alignment",
            "Existential pivot vision under total informational blackout",
            "High-stakes interpersonal trust negotiation"
        ]
    )
    automatable_workflow_bounds: List[str] = Field(
        default_factory=lambda: [
            "Weak signal trend scanning",
            "Structural causal graph estimation",
            "Price elasticity simulation",
            "A/B experiment scheduling",
            "Resource allocation trade-offs"
        ]
    )


class Layer1_Reality:
    """Formalizes the fundamental substrate and boundary conditions of entrepreneurship."""

    def __init__(self) -> None:
        self.state = RealityState()

    def evaluate_task_automation_boundary(self, task_name: str, uncertainty_level: float) -> Dict[str, Any]:
        """Distinguishes tasks requiring human judgment vs automatable optimization."""
        is_automatable = task_name in self.state.automatable_workflow_bounds or uncertainty_level < 0.85
        requires_human_judgment = not is_automatable
        return {
            "task_name": task_name,
            "uncertainty_level": uncertainty_level,
            "is_automatable": is_automatable,
            "requires_human_judgment": requires_human_judgment,
            "governing_invariants": self.state.invariant_principles
        }


# ============================================================================
# LAYER 2: OPPORTUNITY DISCOVERY
# ============================================================================
class WorldStateSignal(BaseModel):
    signal_id: UUID = Field(default_factory=uuid4)
    source_domain: str
    raw_magnitude: float
    noise_variance: float = 0.1
    timestamp: float = 0.0
    features: Dict[str, float] = Field(default_factory=dict)


class DiscoveredOpportunity(BaseModel):
    opportunity_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str
    detected_weak_signal_strength: float
    novelty_score: float
    trend_relevance_index: float
    fused_features: Dict[str, float] = Field(default_factory=dict)
    is_stealth_invisible: bool = False


class Layer2_OpportunityDiscovery:
    """Continuously searches state space for weak signals, filters noise, and generates novelty."""

    def __init__(self, noise_filter_threshold: float = 0.2) -> None:
        self.noise_filter_threshold = noise_filter_threshold

    def filter_weak_signal(self, signal: WorldStateSignal) -> Optional[float]:
        """Applies Kalman/SNR filtering to isolate true weak signals from background noise."""
        snr = signal.raw_magnitude / (signal.noise_variance + 1e-6)
        if snr < self.noise_filter_threshold:
            return None
        # Denoised signal estimate
        return signal.raw_magnitude * (1.0 - (signal.noise_variance / (signal.noise_variance + snr)))

    def combine_unrelated_observations(self, obs_a: Dict[str, float], obs_b: Dict[str, float]) -> Dict[str, float]:
        """Cross-domain synthesis generating novelty from orthogonal signals."""
        fused = {}
        for k, v in obs_a.items():
            fused[f"a_{k}"] = v
        for k, v in obs_b.items():
            fused[f"b_{k}"] = v
        # Compute cross-product interaction term as novelty proxy
        novelty_interaction = sum(obs_a.values()) * sum(obs_b.values())
        fused["cross_domain_novelty"] = novelty_interaction
        return fused

    def search_state_space(self, signals: List[WorldStateSignal]) -> List[DiscoveredOpportunity]:
        """Searches state space and packages filtered signals into discovered opportunities."""
        discovered = []
        for i, sig in enumerate(signals):
            filtered_val = self.filter_weak_signal(sig)
            if filtered_val is not None:
                novelty = math.tanh(sig.raw_magnitude * (i + 1) * 0.3)
                relevance = min(1.0, filtered_val / 10.0)
                is_stealth = sig.raw_magnitude < 0.5 and relevance > 0.6
                opp = DiscoveredOpportunity(
                    title=f"Opportunity from {sig.source_domain}",
                    domain=sig.source_domain,
                    detected_weak_signal_strength=filtered_val,
                    novelty_score=novelty,
                    trend_relevance_index=relevance,
                    fused_features=sig.features,
                    is_stealth_invisible=is_stealth
                )
                discovered.append(opp)
        return discovered


# ============================================================================
# LAYER 3: PROBLEM DISCOVERY & STRUCTURAL DECOMPOSITION
# ============================================================================
class ProblemDecomposition(BaseModel):
    problem_id: UUID = Field(default_factory=uuid4)
    stated_problem: str
    true_root_cause: str
    is_second_order: bool = False
    symptoms: List[str] = Field(default_factory=list)
    causal_parents: List[str] = Field(default_factory=list)
    triage_action: str = "SOLVE"  # SOLVE, DELEGATE, IGNORE


class Layer3_ProblemDiscovery:
    """Decomposes problems using Structural Causal Models (SCM) to distinguish symptoms from root causes."""

    def decompose_problem(
        self,
        stated_problem: str,
        observed_symptoms: List[str],
        causal_graph: Dict[str, List[str]],
        impact_score: float
    ) -> ProblemDecomposition:
        """Identifies root cause and determines whether to solve or ignore the problem."""
        # Find root node in causal graph (node with no parents)
        all_children = {child for children in causal_graph.values() for child in children}
        potential_roots = [node for node in causal_graph if node not in all_children]
        root_cause = potential_roots[0] if potential_roots else stated_problem

        is_second_order = len(observed_symptoms) > 2 or impact_score > 0.75

        # Ignore triage rule: low impact symptom with no structural downstream effect
        triage = "IGNORE" if impact_score < 0.25 and not is_second_order else "SOLVE"

        return ProblemDecomposition(
            stated_problem=stated_problem,
            true_root_cause=root_cause,
            is_second_order=is_second_order,
            symptoms=observed_symptoms,
            causal_parents=potential_roots,
            triage_action=triage
        )


# ============================================================================
# LAYER 4: DECISION MAKING UNDER UNCERTAINTY
# ============================================================================
class DecisionResult(BaseModel):
    decision_id: UUID = Field(default_factory=uuid4)
    selected_action: str
    expected_free_energy: float
    pragmatic_value: float
    epistemic_value: float
    decision_mode: str  # "DATA_DRIVEN_BAYESIAN" vs "HEURISTIC_INTUITION"
    kill_flag: bool = False
    bias_mitigation_notes: str = ""


class Layer4_DecisionMaking:
    """Active Inference decision engine minimizing Expected Free Energy (EFE) with bias mitigation."""

    def compute_efe(self, p_success: float, p_target: float, prior_entropy: float, post_entropy: float) -> Tuple[float, float, float]:
        """G = - Pragmatic Value - Epistemic Value"""
        eps = 1e-9
        p_s = max(eps, min(1.0 - eps, p_success))
        p_t = max(eps, min(1.0 - eps, p_target))

        pragmatic = math.log(p_s) - math.log(p_t)
        epistemic = max(0.0, prior_entropy - post_entropy)
        efe = -pragmatic - epistemic
        return efe, pragmatic, epistemic

    def make_decision(
        self,
        action_name: str,
        p_success: float,
        p_target: float,
        prior_entropy: float,
        post_entropy: float,
        latency_budget_ms: float = 100.0,
        active_counter_evidence_count: int = 0
    ) -> DecisionResult:
        """Executes dual-process decision making and triggers fast kill mechanisms."""
        efe, pragmatic, epistemic = self.compute_efe(p_success, p_target, prior_entropy, post_entropy)

        # Dual-process routing: latency constraint forces heuristic intuition
        decision_mode = "HEURISTIC_INTUITION" if latency_budget_ms < 10.0 else "DATA_DRIVEN_BAYESIAN"

        # Confirmation bias check: penalize decisions lacking counter-evidence queries
        bias_notes = "Sufficient counter-evidence queried"
        if active_counter_evidence_count == 0 and decision_mode == "DATA_DRIVEN_BAYESIAN":
            efe += 0.5  # Bias penalty
            bias_notes = "Penalized for unverified confirmation bias"

        # Fast kill threshold: if EFE is unacceptably high (or p_success very low)
        kill_flag = p_success < 0.15 or efe > 3.0

        return DecisionResult(
            selected_action=action_name,
            expected_free_energy=efe,
            pragmatic_value=pragmatic,
            epistemic_value=epistemic,
            decision_mode=decision_mode,
            kill_flag=kill_flag,
            bias_mitigation_notes=bias_notes
        )


# ============================================================================
# LAYER 5: OPPORTUNITY EVALUATION
# ============================================================================
class OpportunityEvaluation(BaseModel):
    evaluation_id: UUID = Field(default_factory=uuid4)
    tam_cents: int
    unit_economics_margin: float
    readiness_timing_index: float
    cvar_downside_risk: float
    expected_value_cents: float
    abandonment_pivot_flag: bool = False


class Layer5_OpportunityEvaluation:
    """Evaluates multi-variable opportunity quality, downside risk (CVaR), and pivot triggers."""

    def evaluate_opportunity(
        self,
        tam_cents: int,
        conversion_rate: float,
        arpu_cents: int,
        cogs_cents: int,
        readiness_timing: float,
        risk_variance: float
    ) -> OpportunityEvaluation:
        """Calculates expected value and CVaR downside risk."""
        margin = (arpu_cents - cogs_cents) / max(1.0, float(arpu_cents))
        raw_ev = tam_cents * conversion_rate * margin * readiness_timing

        # CVaR (Conditional Value at Risk) downside estimation at 95% confidence
        downside_cvar = raw_ev * (1.645 * math.sqrt(risk_variance))

        expected_val = raw_ev - downside_cvar
        pivot_flag = expected_val < 0 or margin < 0.1

        return OpportunityEvaluation(
            tam_cents=tam_cents,
            unit_economics_margin=margin,
            readiness_timing_index=readiness_timing,
            cvar_downside_risk=downside_cvar,
            expected_value_cents=expected_val,
            abandonment_pivot_flag=pivot_flag
        )


# ============================================================================
# LAYER 6: PRODUCT CREATION
# ============================================================================
class ProductSpecification(BaseModel):
    product_id: UUID = Field(default_factory=uuid4)
    core_jtbd: str
    essential_features: List[str] = Field(default_factory=list)
    pruned_features: List[str] = Field(default_factory=list)
    complexity_budget_score: float
    value_density: float


class Layer6_ProductCreation:
    """Optimizes product creation for Jobs-To-Be-Done (JTBD) while pruning feature bloat."""

    def build_product_spec(
        self,
        core_jtbd: str,
        proposed_features: Dict[str, float],  # feature -> value_creation_score
        max_complexity_budget: float = 100.0
    ) -> ProductSpecification:
        """Prunes unnecessary features to maximize learning density and value creation."""
        essential = []
        pruned = []
        total_complexity = 0.0
        total_value = 0.0

        for feat, val in sorted(proposed_features.items(), key=lambda x: x[1], reverse=True):
            feat_complexity = 20.0  # Constant complexity per feature
            if total_complexity + feat_complexity <= max_complexity_budget and val >= 0.4:
                essential.append(feat)
                total_complexity += feat_complexity
                total_value += val
            else:
                pruned.append(feat)

        density = total_value / max(1.0, total_complexity)

        return ProductSpecification(
            core_jtbd=core_jtbd,
            essential_features=essential,
            pruned_features=pruned,
            complexity_budget_score=total_complexity,
            value_density=density
        )


# ============================================================================
# LAYER 7: CUSTOMER UNDERSTANDING
# ============================================================================
class CustomerProfileState(BaseModel):
    customer_id: UUID = Field(default_factory=uuid4)
    trust_index: float = 0.5
    switching_friction_barrier: float = 0.7
    perceived_payoff_delta: float = 0.8
    churn_probability: float = 0.1
    evangelist_velocity: float = 0.2


class Layer7_CustomerUnderstanding:
    """Models customer psychological state transitions, trust, churn, and evangelism."""

    def simulate_customer_lifecycle(
        self,
        profile: CustomerProfileState,
        product_quality: float,
        onboarding_friction: float
    ) -> CustomerProfileState:
        """Updates customer trust, churn risk, and evangelism score."""
        new_trust = min(1.0, profile.trust_index + 0.2 * product_quality - 0.1 * onboarding_friction)
        churn = max(0.01, 1.0 - (new_trust * profile.perceived_payoff_delta / max(0.1, profile.switching_friction_barrier)))

        evangelism = max(0.0, (new_trust - 0.7) * 2.0) if new_trust > 0.7 else 0.0

        return CustomerProfileState(
            customer_id=profile.customer_id,
            trust_index=new_trust,
            switching_friction_barrier=profile.switching_friction_barrier,
            perceived_payoff_delta=profile.perceived_payoff_delta,
            churn_probability=churn,
            evangelist_velocity=evangelism
        )


# ============================================================================
# LAYER 8: MARKETING & ATTENTION DYNAMICS
# ============================================================================
class MarketingCampaignResult(BaseModel):
    campaign_id: UUID = Field(default_factory=uuid4)
    attention_reach: float
    virality_r0: float
    brand_authority_score: float
    channel_synergy_multiplier: float


class Layer8_Marketing:
    """Engineers SIR-style attention dynamics, brand authority, and channel synergies."""

    def simulate_attention_dynamics(
        self,
        initial_susceptible: float,
        virality_rate_beta: float,
        decay_rate_gamma: float,
        channel_diversity_count: int
    ) -> MarketingCampaignResult:
        """Simulates viral spreading dynamics (R0 = beta / gamma)."""
        r0 = virality_rate_beta / max(1e-4, decay_rate_gamma)

        # Reach approximation from SIR epidemic final size equation
        reach = initial_susceptible * (1.0 - math.exp(-r0)) if r0 > 1.0 else initial_susceptible * 0.1

        synergy = 1.0 + (0.15 * math.log(1 + channel_diversity_count))
        authority = min(1.0, 0.3 * r0 * synergy)

        return MarketingCampaignResult(
            attention_reach=reach,
            virality_r0=r0,
            brand_authority_score=authority,
            channel_synergy_multiplier=synergy
        )


# ============================================================================
# LAYER 9: SALES SYSTEMS
# ============================================================================
class SalesConversionState(BaseModel):
    deal_id: UUID = Field(default_factory=uuid4)
    urgency_score: float
    objections_count: int
    resolved_objections_count: int
    is_enterprise_deal: bool
    conversion_probability: float
    automation_recommended: bool


class Layer9_Sales:
    """Formalizes psychological sales conversion, objection resolution, and automation thresholds."""

    def process_sales_funnel(
        self,
        urgency: float,
        objections: List[str],
        contract_value_cents: int
    ) -> SalesConversionState:
        """Determines conversion probability and whether to automate vs use enterprise sales."""
        resolved = len([o for o in objections if "pricing" not in o])  # Resolve non-price objections
        remaining = len(objections) - resolved

        base_p = min(0.95, urgency * 0.5 + (resolved / max(1, len(objections))) * 0.4)
        final_p = max(0.05, base_p - (0.15 * remaining))

        is_enterprise = contract_value_cents > 5000000  # $50k+ threshold
        automate = not is_enterprise and final_p > 0.4

        return SalesConversionState(
            urgency_score=urgency,
            objections_count=len(objections),
            resolved_objections_count=resolved,
            is_enterprise_deal=is_enterprise,
            conversion_probability=final_p,
            automation_recommended=automate
        )


# ============================================================================
# LAYER 10: GROWTH & ECOSYSTEM DYNAMICS
# ============================================================================
class GrowthMetrics(BaseModel):
    compounding_rate: float
    network_effect_score: float
    platform_transition_index: float
    intentional_growth_throttle: bool = False


class Layer10_Growth:
    """Engineers compounding feedback loops, Metcalfe network effects, and throttling."""

    def evaluate_growth_engine(
        self,
        user_count: int,
        k_factor: float,
        system_load_capacity: float
    ) -> GrowthMetrics:
        """Computes network effects (N^2) and determines intentional growth throttling."""
        # Metcalfe's Law network effect score normalized
        network_score = math.log10(max(1.0, user_count ** 2))

        compounding = k_factor * network_score
        platform_index = min(1.0, user_count / 100000.0)

        # Growth throttle trigger: capacity over-utilization risks product degradation
        throttle = (user_count / max(1.0, system_load_capacity)) > 0.9

        return GrowthMetrics(
            compounding_rate=compounding,
            network_effect_score=network_score,
            platform_transition_index=platform_index,
            intentional_growth_throttle=throttle
        )


# ============================================================================
# LAYER 11: COMPETITIVE DYNAMICS & MOATS
# ============================================================================
class CompetitiveMoatAnalysis(BaseModel):
    moat_score: float
    replication_barrier_months: float
    disruption_survival_probability: float
    pivot_required_flag: bool = False


class Layer11_Competition:
    """Anticipates competitor moves and calculates structural defensibility moats."""

    def analyze_competition(
        self,
        proprietary_ip_weight: float,
        switching_cost_weight: float,
        competitor_velocity: float
    ) -> CompetitiveMoatAnalysis:
        """Calculates defensibility score and disruption survival odds."""
        moat = (proprietary_ip_weight * 0.6) + (switching_cost_weight * 0.4)
        replication_months = moat * 24.0

        survival_p = max(0.1, min(0.99, moat / max(0.1, competitor_velocity)))
        pivot_req = survival_p < 0.4

        return CompetitiveMoatAnalysis(
            moat_score=moat,
            replication_barrier_months=replication_months,
            disruption_survival_probability=survival_p,
            pivot_required_flag=pivot_req
        )


# ============================================================================
# LAYER 12: ORGANIZATIONAL DESIGN
# ============================================================================
class OrgStructureState(BaseModel):
    total_headcount: int
    centralized_tasks: List[str] = Field(default_factory=list)
    delegated_tasks: List[str] = Field(default_factory=list)
    hiring_trigger_flag: bool = False


class Layer12_OrgDesign:
    """Manages org structure evolution, hiring triggers, and decision delegation boundaries."""

    def optimize_org_structure(
        self,
        workload_units: float,
        current_headcount: int
    ) -> OrgStructureState:
        """Determines when to hire and balances centralized strategy vs delegated execution."""
        capacity_per_person = 10.0
        required_headcount = math.ceil(workload_units / capacity_per_person)
        hiring_needed = required_headcount > current_headcount

        centralized = ["Capital allocation", "Existential pivot vision", "Executive hiring"]
        delegated = ["Feature implementation", "Customer support routing", "Marketing copy generation"]

        return OrgStructureState(
            total_headcount=current_headcount,
            centralized_tasks=centralized,
            delegated_tasks=delegated,
            hiring_trigger_flag=hiring_needed
        )


# ============================================================================
# LAYER 13: META-LEARNING
# ============================================================================
class MetaLearningUpdate(BaseModel):
    brier_decision_score: float
    hindsight_calibration_delta: float
    updated_prior_beliefs: Dict[str, float] = Field(default_factory=dict)
    reusable_knowledge_extracted: List[str] = Field(default_factory=list)


class Layer13_MetaLearning:
    """Evaluates decision quality via Brier score calibration and updates mental models."""

    def evaluate_and_update(
        self,
        predicted_probabilities: List[float],
        actual_outcomes: List[int],
        priors: Dict[str, float]
    ) -> MetaLearningUpdate:
        """Calculates Brier Score = (1/N) * sum((p - y)^2) and updates Bayesian priors."""
        if not predicted_probabilities or len(predicted_probabilities) != len(actual_outcomes):
            return MetaLearningUpdate(brier_decision_score=0.25, hindsight_calibration_delta=0.0, updated_prior_beliefs=priors)

        n = len(predicted_probabilities)
        brier_score = sum((p - y) ** 2 for p, y in zip(predicted_probabilities, actual_outcomes)) / float(n)

        # Hindsight calibration delta (0 is perfect calibration)
        mean_pred = sum(predicted_probabilities) / float(n)
        mean_actual = sum(actual_outcomes) / float(n)
        calibration_delta = mean_pred - mean_actual

        # Update priors towards empirical outcome
        updated_priors = {}
        for k, v in priors.items():
            updated_priors[k] = max(0.05, min(0.95, v - (0.1 * calibration_delta)))

        extracted = [
            f"Brier score evaluated at {brier_score:.4f}",
            "Calibrated Bayesian belief priors based on historical outcome distribution"
        ]

        return MetaLearningUpdate(
            brier_decision_score=brier_score,
            hindsight_calibration_delta=calibration_delta,
            updated_prior_beliefs=updated_priors,
            reusable_knowledge_extracted=extracted
        )


# ============================================================================
# LAYER 14: AI AUTONOMOUS ENTREPRENEURSHIP & MASTER ENGINE
# ============================================================================
class ResourceAllocation(BaseModel):
    capital_allocation_cents: int
    compute_units: float
    talent_hours: float
    time_budget_days: float


class FourteenLayerEntrepreneurshipEngine:
    """
    The master 14-layer computational engine of entrepreneurship.
    Integrates sensing, problem decomposition, decision making, evaluation, product creation,
    customer modeling, marketing, sales, growth, competition, org design, meta-learning, and resource allocation.
    """

    def __init__(self) -> None:
        self.layer1 = Layer1_Reality()
        self.layer2 = Layer2_OpportunityDiscovery()
        self.layer3 = Layer3_ProblemDiscovery()
        self.layer4 = Layer4_DecisionMaking()
        self.layer5 = Layer5_OpportunityEvaluation()
        self.layer6 = Layer6_ProductCreation()
        self.layer7 = Layer7_CustomerUnderstanding()
        self.layer8 = Layer8_Marketing()
        self.layer9 = Layer9_Sales()
        self.layer10 = Layer10_Growth()
        self.layer11 = Layer11_Competition()
        self.layer12 = Layer12_OrgDesign()
        self.layer13 = Layer13_MetaLearning()

    def allocate_resources(self, opportunity_ev_cents: float, urgency: float) -> ResourceAllocation:
        """Formalizes optimal capital, compute, talent, and time allocation."""
        capital = int(max(100000, opportunity_ev_cents * 0.1))
        compute = max(10.0, urgency * 100.0)
        talent = max(40.0, urgency * 160.0)
        time_days = max(7.0, 30.0 / max(0.1, urgency))

        return ResourceAllocation(
            capital_allocation_cents=capital,
            compute_units=compute,
            talent_hours=talent,
            time_budget_days=time_days
        )

    def execute_complete_pipeline(
        self,
        signals: List[WorldStateSignal],
        causal_graph: Dict[str, List[str]],
        priors: Dict[str, float]
    ) -> Dict[str, Any]:
        """Executes end-to-end 14-layer computational entrepreneurship lifecycle."""
        # Layer 1 & 2: Sense and discover
        discovered_opps = self.layer2.search_state_space(signals)
        primary_opp = discovered_opps[0] if discovered_opps else None

        if not primary_opp:
            return {"status": "no_opportunity_found"}

        # Layer 3: Structural problem decomposition
        decomp = self.layer3.decompose_problem(
            stated_problem=f"Solve friction in {primary_opp.domain}",
            observed_symptoms=["Low retention", "High CAC"],
            causal_graph=causal_graph,
            impact_score=primary_opp.trend_relevance_index
        )

        # Layer 4: Active Inference decision
        decision = self.layer4.make_decision(
            action_name=f"Pursue {primary_opp.title}",
            p_success=0.6,
            p_target=0.9,
            prior_entropy=1.2,
            post_entropy=0.4
        )

        # Layer 5: Opportunity evaluation
        eval_res = self.layer5.evaluate_opportunity(
            tam_cents=100000000,
            conversion_rate=0.03,
            arpu_cents=10000,
            cogs_cents=2000,
            readiness_timing=primary_opp.trend_relevance_index,
            risk_variance=0.05
        )

        # Layer 6: Product spec
        prod_spec = self.layer6.build_product_spec(
            core_jtbd="Automate venture opportunity discovery",
            proposed_features={"Weak signal filter": 0.9, "SCM solver": 0.8, "Legacy manual export": 0.1}
        )

        # Layer 7: Customer simulation
        cust = self.layer7.simulate_customer_lifecycle(
            profile=CustomerProfileState(),
            product_quality=0.85,
            onboarding_friction=0.2
        )

        # Layer 8: Marketing simulation
        mkt = self.layer8.simulate_attention_dynamics(
            initial_susceptible=100000.0,
            virality_rate_beta=0.8,
            decay_rate_gamma=0.3,
            channel_diversity_count=4
        )

        # Layer 9: Sales processing
        sales = self.layer9.process_sales_funnel(
            urgency=0.8,
            objections=["pricing_concern", "integration_timeline"],
            contract_value_cents=6000000
        )

        # Layer 10: Growth evaluation
        growth = self.layer10.evaluate_growth_engine(
            user_count=5000,
            k_factor=1.2,
            system_load_capacity=10000.0
        )

        # Layer 11: Competitive moat analysis
        comp = self.layer11.analyze_competition(
            proprietary_ip_weight=0.8,
            switching_cost_weight=0.7,
            competitor_velocity=0.4
        )

        # Layer 12: Org design optimization
        org = self.layer12.optimize_org_structure(
            workload_units=45.0,
            current_headcount=3
        )

        # Layer 13: Meta-learning calibration update
        meta = self.layer13.evaluate_and_update(
            predicted_probabilities=[0.7, 0.6, 0.8],
            actual_outcomes=[1, 1, 0],
            priors=priors
        )

        # Layer 14: Capital and resource allocation
        resources = self.allocate_resources(
            opportunity_ev_cents=eval_res.expected_value_cents,
            urgency=sales.urgency_score
        )

        return {
            "status": "pipeline_executed",
            "layer1_reality_invariants": self.layer1.state.invariant_principles,
            "layer2_discovered_opportunities_count": len(discovered_opps),
            "layer3_root_cause": decomp.true_root_cause,
            "layer4_decision_efe": decision.expected_free_energy,
            "layer5_expected_value_cents": eval_res.expected_value_cents,
            "layer6_product_essential_features": prod_spec.essential_features,
            "layer7_customer_trust": cust.trust_index,
            "layer8_virality_r0": mkt.virality_r0,
            "layer9_sales_conversion_prob": sales.conversion_probability,
            "layer10_network_score": growth.network_effect_score,
            "layer11_moat_score": comp.moat_score,
            "layer12_hiring_needed": org.hiring_trigger_flag,
            "layer13_brier_score": meta.brier_decision_score,
            "layer14_resource_allocation": resources.model_dump()
        }
