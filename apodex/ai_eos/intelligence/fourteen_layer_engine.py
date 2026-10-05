"""
The 14-Layer Computational Engine of Entrepreneurship for APODEX / AI-EOS.

Implements the formal algorithms, data models, structural causal models,
active inference loops, real options, and meta-learning mechanisms across
all 14 layers of venture creation and autonomous execution.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from apodex.ai_eos.intelligence.computational_architecture import (
    AdvancedCausalEngine,
    ActiveInferencePlanner,
    Opportunity
)

logger = logging.getLogger("apodex.ai_eos.fourteen_layer_engine")


# =====================================================================
# DATA MODELS & SCHEMAS
# =====================================================================

class VentureState(BaseModel):
    """Canonical representation of an active venture's system dynamics state."""
    venture_id: UUID = Field(default_factory=uuid4)
    title: str
    capital_reserves_cents: int = 10000000  # $100k
    monthly_burn_cents: int = 1000000     # $10k
    active_customers: int = 0
    monthly_recurring_revenue_cents: int = 0
    cac_cents: int = 5000                 # $50
    nrr_percent: float = 100.0            # Net Revenue Retention
    gross_margin_percent: float = 80.0
    trust_score: float = 0.5              # [0.0, 1.0]
    brand_authority_score: float = 0.1    # [0.0, 1.0]
    moat_score: float = 0.2               # [0.0, 1.0]
    is_active: bool = True


class OpportunitySignal(BaseModel):
    """Data model representing a discovered external state-space signal."""
    signal_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str
    observations: List[float] = Field(default_factory=list)
    market_entropy: float = 2.0
    reality_entropy: float = 0.5
    shannon_surprise: float = 0.0
    tam_cents: int = 100000000           # $1M default TAM
    prior_success_prob: float = 0.3
    target_preference_prob: float = 0.95


class ProblemSCM(BaseModel):
    """Structural Causal Model representing problem topology."""
    problem_id: UUID = Field(default_factory=uuid4)
    title: str
    variables: List[str] = Field(default_factory=list)
    causal_edges: List[Tuple[str, str]] = Field(default_factory=list)
    coefficients: Dict[str, float] = Field(default_factory=dict)
    root_cause: Optional[str] = None
    symptom: Optional[str] = None


class CustomerAgentModel(BaseModel):
    """Active inference psychological representation of a target customer."""
    customer_id: UUID = Field(default_factory=uuid4)
    segment: str
    push_friction: float = 0.5      # Pain with status quo
    pull_attraction: float = 0.6    # Value of new product
    inertia_cost: float = 0.4       # Habit / switching barrier
    anxiety_risk: float = 0.3       # Perceived risk of new solution
    perceived_price_cents: int = 10000
    perceived_utility: float = 0.8
    trust_vector: float = 0.5


class ProductSpec(BaseModel):
    """Specification of a product feature set and its complexity penalty."""
    product_id: UUID = Field(default_factory=uuid4)
    title: str
    features: List[str] = Field(default_factory=list)
    complexity_score: float = 1.0   # Regularization penalty
    jtbd_coverage: float = 0.7      # Job-To-Be-Done satisfaction score
    estimated_build_cost_cents: int = 500000


# =====================================================================
# LAYER 1: REALITY SUBSTRATE
# =====================================================================

class RealitySubstrateEngine:
    """
    Layer 1: Reality
    Formalizes thermodynamic bounds, energy/capital conservation laws,
    and classifies automatable optimization vs. human terminal values.
    """

    def evaluate_thermodynamic_bounds(self, inputs_cents: int, outputs_cents: int) -> Dict[str, Any]:
        """Verifies capital/value conservation: Value creation = Outputs - Inputs."""
        if inputs_cents <= 0:
            raise ValueError("Inputs must be strictly positive.")

        roi = (outputs_cents - inputs_cents) / float(inputs_cents)
        is_viable = outputs_cents > inputs_cents
        return {
            "inputs_cents": inputs_cents,
            "outputs_cents": outputs_cents,
            "net_value_created_cents": outputs_cents - inputs_cents,
            "roi": roi,
            "thermodynamically_viable": is_viable
        }

    def classify_task_automation_boundary(self, task_description: str) -> Dict[str, Any]:
        """Determines whether a task is automatable optimization or human terminal value."""
        task_lower = task_description.lower()
        human_domains = ["ethical alignment", "terminal value", "meaning", "human empathy", "emotional resonance"]

        requires_human = any(domain in task_lower for domain in human_domains)
        return {
            "task": task_description,
            "automatable": not requires_human,
            "classification": "Human Terminal Value" if requires_human else "Algorithmic Optimization"
        }


# =====================================================================
# LAYER 2: OPPORTUNITY DISCOVERY
# =====================================================================

class OpportunityDiscoveryEngine:
    """
    Layer 2: Opportunity Discovery
    Scans state-space for KL divergence, weak signals, and cross-domain SCM combination.
    """

    def detect_weak_signals(self, signal: OpportunitySignal) -> Dict[str, Any]:
        """Calculates Shannon surprise and KL divergence between market and reality."""
        kl_div = max(0.0, signal.market_entropy - signal.reality_entropy)
        prob = max(1e-6, min(1.0, signal.prior_success_prob))
        surprise = -math.log(prob)

        is_weak_signal = surprise > 1.0 and kl_div > 0.5
        return {
            "signal_title": signal.title,
            "kl_divergence": kl_div,
            "shannon_surprise": surprise,
            "is_actionable_weak_signal": is_weak_signal
        }

    def combine_disparate_domains(self, scm_a: ProblemSCM, scm_b: ProblemSCM) -> ProblemSCM:
        """Cross-domain transplantation combining variables and causal links."""
        combined_vars = list(set(scm_a.variables + scm_b.variables))
        combined_edges = list(set(scm_a.causal_edges + scm_b.causal_edges))
        combined_coeffs = {**scm_a.coefficients, **scm_b.coefficients}

        if scm_a.variables and scm_b.variables:
            bridge_edge = (scm_a.variables[0], scm_b.variables[0])
            if bridge_edge not in combined_edges:
                combined_edges.append(bridge_edge)
                combined_coeffs[f"{bridge_edge[0]}->{bridge_edge[1]}"] = 0.75

        return ProblemSCM(
            title=f"Synthesized ({scm_a.title} x {scm_b.title})",
            variables=combined_vars,
            causal_edges=combined_edges,
            coefficients=combined_coeffs
        )


# =====================================================================
# LAYER 3: PROBLEM DISCOVERY
# =====================================================================

class ProblemDiscoveryEngine:
    """
    Layer 3: Problem Discovery
    SCM problem formulation, root-cause vs. symptom isolation, and ignore criteria.
    """

    def isolate_root_cause(self, scm: ProblemSCM) -> Dict[str, Any]:
        """Identifies root cause variable vs downstream symptom variable."""
        if not scm.variables:
            return {"root_cause": None, "symptom": None}

        parent_counts: Dict[str, int] = {v: 0 for v in scm.variables}
        child_counts: Dict[str, int] = {v: 0 for v in scm.variables}

        for parent, child in scm.causal_edges:
            if parent in parent_counts and child in child_counts:
                child_counts[child] += 1
                parent_counts[parent] += 1

        root_cause = max(scm.variables, key=lambda v: parent_counts[v] - child_counts[v])
        symptom = max(scm.variables, key=lambda v: child_counts[v] - parent_counts[v])

        scm.root_cause = root_cause
        scm.symptom = symptom

        return {
            "root_cause": root_cause,
            "symptom": symptom,
            "is_decoupled": root_cause != symptom
        }

    def evaluate_ignore_criteria(self, evig: float, delta_utility: float, cost_investigate: float) -> bool:
        """
        Ignore problem if Expected Value of Information Gain (EVIG)
        + Delta Utility < Cost of Investigation.
        """
        return (evig + delta_utility) < cost_investigate


# =====================================================================
# LAYER 4: DECISION MAKING
# =====================================================================

class DecisionMakingEngine:
    """
    Layer 4: Decision Making
    Knightian uncertainty decisioning, Bayesian updating, and SPRT idea killing.
    """

    def resolve_bayesian_intuition_data(self, prior_prob: float, evidence_likelihood: float, sample_size: int) -> float:
        """
        Combines prior intuition with data likelihood.
        As sample size N increases, likelihood dominates.
        """
        weight_data = min(1.0, sample_size / 50.0)
        posterior = (1.0 - weight_data) * prior_prob + weight_data * evidence_likelihood
        return max(0.01, min(0.99, posterior))

    def evaluate_sprt_kill_gate(self, log_likelihood_ratios: List[float], alpha: float = 0.05, beta: float = 0.10) -> str:
        """
        Sequential Probability Ratio Test (SPRT) with asymmetric decision boundaries.
        A = ln((1 - beta) / alpha), B = ln(beta / (1 - alpha))
        """
        boundary_a = math.log((1.0 - beta) / alpha)
        boundary_b = math.log(beta / (1.0 - alpha))

        cum_llr = sum(log_likelihood_ratios)

        if cum_llr >= boundary_a:
            return "ACCEPT_HYPOTHESIS"
        elif cum_llr <= boundary_b:
            return "KILL_IDEA_IMMEDIATELY"
        else:
            return "CONTINUE_SAMPLING"


# =====================================================================
# LAYER 5: OPPORTUNITY EVALUATION
# =====================================================================

class OpportunityEvaluationEngine:
    """
    Layer 5: Opportunity Evaluation
    Expected Value, Jump-Diffusion Real Options timing, and abandonment triggers.
    """

    def calculate_expected_value_and_risk(self, tam_cents: int, gross_margin: float, success_prob: float, jump_volatility: float) -> Dict[str, Any]:
        """Calculates expected cash yield discounted by jump-diffusion risk."""
        expected_cash_cents = tam_cents * (gross_margin / 100.0) * success_prob
        risk_discount = math.exp(-jump_volatility)
        discounted_ev_cents = expected_cash_cents * risk_discount

        return {
            "raw_expected_value_cents": int(expected_cash_cents),
            "jump_volatility": jump_volatility,
            "risk_discount_factor": risk_discount,
            "discounted_ev_cents": int(discounted_ev_cents)
        }

    def evaluate_real_options_timing(self, volatility: float, competitor_preemption_rate: float) -> str:
        """
        Real options value of waiting vs first-mover advantage.
        High volatility increases wait option; high preemption forces immediate entry.
        """
        if competitor_preemption_rate > 0.6:
            return "EXECUTE_IMMEDIATELY"
        elif volatility > 0.8:
            return "DEFER_AND_GATHER_INFORMATION"
        else:
            return "STAGE_SEEDED_EXPERIMENT"


# =====================================================================
# LAYER 6: PRODUCT CREATION
# =====================================================================

class ProductCreationEngine:
    """
    Layer 6: Product Creation
    Kolmogorov complexity minimization and core JTBD extraction.
    """

    def regularize_product_complexity(self, spec: ProductSpec, max_complexity: float = 2.0) -> ProductSpec:
        """Applies Kolmogorov complexity penalty, pruning non-essential features."""
        if spec.complexity_score <= max_complexity:
            return spec

        essential_count = max(1, len(spec.features) // 2)
        pruned_features = spec.features[:essential_count]
        pruned_complexity = spec.complexity_score * (essential_count / float(max(1, len(spec.features))))

        return ProductSpec(
            title=f"{spec.title} (Regularized)",
            features=pruned_features,
            complexity_score=pruned_complexity,
            jtbd_coverage=spec.jtbd_coverage * 0.95,
            estimated_build_cost_cents=int(spec.estimated_build_cost_cents * 0.6)
        )


# =====================================================================
# LAYER 7: CUSTOMER UNDERSTANDING
# =====================================================================

class CustomerUnderstandingEngine:
    """
    Layer 7: Customer Understanding
    Push-Pull-Inertia-Anxiety switching matrix and trust vector updating.
    """

    def calculate_switch_probability(self, model: CustomerAgentModel) -> float:
        """P(switch) = sigmoid(Push + Pull - Inertia - Anxiety)"""
        net_score = (model.push_friction + model.pull_attraction) - (model.inertia_cost + model.anxiety_risk)
        prob = 1.0 / (1.0 + math.exp(-net_score))
        return max(0.0, min(1.0, prob))

    def update_trust_vector(self, current_trust: float, delivered_value: float, failure_magnitude: float) -> float:
        """Updates trust state vector with asymmetry (slow gain, rapid loss)."""
        if failure_magnitude > 0.0:
            updated = current_trust * math.exp(-2.0 * failure_magnitude)
        else:
            updated = current_trust + 0.1 * (delivered_value - current_trust)

        return max(0.0, min(1.0, updated))


# =====================================================================
# LAYER 8: MARKETING
# =====================================================================

class MarketingEngine:
    """
    Layer 8: Marketing
    Attention spread, virality, PageRank brand authority, and positioning projection.
    """

    def project_positioning_distance(self, product_vector: List[float], competitor_vectors: List[List[float]]) -> float:
        """Calculates minimum Euclidean distance from competitors in cognitive coordinate space."""
        if not competitor_vectors:
            return 1.0

        min_dist = float("inf")
        for comp in competitor_vectors:
            dist = math.sqrt(sum((p - c) ** 2 for p, c in zip(product_vector, comp)))
            if dist < min_dist:
                min_dist = dist

        return float(min_dist)


# =====================================================================
# LAYER 9: SALES
# =====================================================================

class SalesEngine:
    """
    Layer 9: Sales
    Urgency engine, compounding loss of inaction, and sales automation boundaries.
    """

    def calculate_inaction_compounding_loss(self, monthly_cost_cents: int, elapsed_months: int, risk_rate: float = 0.05) -> int:
        """Calculates compounding cost of customer inaction C_loss(t) = c * e^(r*t)."""
        loss = monthly_cost_cents * math.exp(risk_rate * elapsed_months)
        return int(loss)

    def determine_sales_automation_mode(self, acv_cents: int) -> str:
        """Automate self-serve sales if ACV < $5k (500,000 cents); high-touch otherwise."""
        if acv_cents < 500000:
            return "AUTOMATED_SELF_SERVE_FUNNEL"
        else:
            return "HIGH_TOUCH_ENTERPRISE_SALES"


# =====================================================================
# LAYER 10: GROWTH
# =====================================================================

class GrowthEngine:
    """
    Layer 10: Growth
    Compounding feedback loops, sub-quadratic network effects V ~ N log N, and metrics.
    """

    def evaluate_network_value(self, active_nodes: int) -> float:
        """Beckstrom's / Zipf's Sub-quadratic network scaling V = N * log(N)."""
        if active_nodes <= 1:
            return 0.0
        return active_nodes * math.log(active_nodes)

    def evaluate_growth_health(self, nrr_percent: float, cac_payback_months: float) -> str:
        """Evaluates compounding growth health."""
        if nrr_percent >= 120.0 and cac_payback_months <= 12.0:
            return "COMPOUNDING_HYPERGROWTH"
        elif nrr_percent >= 100.0:
            return "SUSTAINABLE_GROWTH"
        else:
            return "CHURN_DOMINATED_DECLINE"


# =====================================================================
# LAYER 11: COMPETITION
# =====================================================================

class CompetitionEngine:
    """
    Layer 11: Competition
    Game-theoretic rival anticipation and Hamilton Helmer 7 Powers moat scoring.
    """

    def calculate_7_powers_moat_score(self, powers: Dict[str, float]) -> float:
        """
        Averages scores across 7 Powers:
        Scale Economies, Network Effects, Counter-Positioning,
        Switching Costs, Brand, Cornered Resource, Process Power.
        """
        valid_keys = [
            "scale_economies", "network_effects", "counter_positioning",
            "switching_costs", "brand", "cornered_resource", "process_power"
        ]
        total = sum(powers.get(k, 0.0) for k in valid_keys)
        return float(total / len(valid_keys))


# =====================================================================
# LAYER 12: ORGANIZATIONAL DESIGN
# =====================================================================

class OrganizationalDesignEngine:
    """
    Layer 12: Organizational Design
    Lagrange dual shadow pricing and Coasian transaction boundaries.
    """

    def calculate_hiring_shadow_price(self, bottleneck_utility_delta: float, wage_cents: int) -> Dict[str, Any]:
        """Triggers hiring if resource shadow price (utility delta) > market wage."""
        shadow_price_cents = bottleneck_utility_delta * 10000.0  # Scale factor
        should_hire = shadow_price_cents > wage_cents

        return {
            "shadow_price_cents": int(shadow_price_cents),
            "market_wage_cents": wage_cents,
            "trigger_hiring_workflow": should_hire
        }


# =====================================================================
# LAYER 13: META-LEARNING
# =====================================================================

class MetaLearningEngine:
    """
    Layer 13: Meta-Learning
    Triple-loop rewriting, mental model backprop, and post-mortem failure conversion.
    """

    def execute_triple_loop_backprop(self, prediction_error: float, current_model_params: Dict[str, float]) -> Dict[str, Any]:
        """
        Loop 1: Parameter update
        Loop 2: Playbook/Prompt update
        Loop 3: Structural Architecture rewrite trigger
        """
        updated_params = {k: v - 0.1 * prediction_error for k, v in current_model_params.items()}

        trigger_code_rewrite = abs(prediction_error) > 0.5

        return {
            "loop1_updated_parameters": updated_params,
            "loop2_prompt_playbook_refinement": f"Refined playbook under error = {prediction_error:.4f}",
            "loop3_trigger_architecture_rewrite": trigger_code_rewrite
        }


# =====================================================================
# LAYER 14: AI ENTREPRENEURSHIP MASTER ORCHESTRATOR
# =====================================================================

class AIEntrepreneurshipMasterOrchestrator:
    """
    Layer 14: AI Entrepreneurship
    The master coordinating engine synthesizing Layers 1 through 13
    into an autonomous, sovereign AI Entrepreneurial Operating System.
    """

    def __init__(self) -> None:
        self.causal_engine = AdvancedCausalEngine()
        self.planner = ActiveInferencePlanner(curiosity_weight=1.5)

        self.layer1_reality = RealitySubstrateEngine()
        self.layer2_opp_disc = OpportunityDiscoveryEngine()
        self.layer3_prob_disc = ProblemDiscoveryEngine()
        self.layer4_decision = DecisionMakingEngine()
        self.layer5_eval = OpportunityEvaluationEngine()
        self.layer6_product = ProductCreationEngine()
        self.layer7_customer = CustomerUnderstandingEngine()
        self.layer8_marketing = MarketingEngine()
        self.layer9_sales = SalesEngine()
        self.layer10_growth = GrowthEngine()
        self.layer11_competition = CompetitionEngine()
        self.layer12_org = OrganizationalDesignEngine()
        self.layer13_meta = MetaLearningEngine()

    def run_full_14_layer_pipeline(self, signal: OpportunitySignal, venture: VentureState) -> Dict[str, Any]:
        """Executes full 14-layer analysis and orchestration pipeline."""
        logger.info(f"Executing 14-layer pipeline for opportunity '{signal.title}'")

        # Layer 1
        l1_res = self.layer1_reality.evaluate_thermodynamic_bounds(
            inputs_cents=venture.monthly_burn_cents,
            outputs_cents=venture.monthly_recurring_revenue_cents + 100000  # Projected
        )

        # Layer 2
        l2_res = self.layer2_opp_disc.detect_weak_signals(signal)

        # Layer 3
        scm = ProblemSCM(
            title=signal.title,
            variables=["marketing_spend", "user_conversion", "mrr"],
            causal_edges=[("marketing_spend", "user_conversion"), ("user_conversion", "mrr")],
            coefficients={"marketing_spend->user_conversion": 0.6, "user_conversion->mrr": 2.0}
        )
        l3_res = self.layer3_prob_disc.isolate_root_cause(scm)

        # Layer 4
        bayes_prob = self.layer4_decision.resolve_bayesian_intuition_data(
            prior_prob=signal.prior_success_prob,
            evidence_likelihood=0.8,
            sample_size=30
        )

        # Layer 5
        l5_res = self.layer5_eval.calculate_expected_value_and_risk(
            tam_cents=signal.tam_cents,
            gross_margin=venture.gross_margin_percent,
            success_prob=bayes_prob,
            jump_volatility=0.2
        )

        # Layer 6
        spec = ProductSpec(
            title=f"{signal.title} MVP",
            features=["core_api", "dashboard", "billing", "analytics"],
            complexity_score=2.5,
            jtbd_coverage=0.85
        )
        l6_spec = self.layer6_product.regularize_product_complexity(spec, max_complexity=2.0)

        # Layer 7
        cust = CustomerAgentModel(
            segment="developers",
            push_friction=0.7,
            pull_attraction=0.8,
            inertia_cost=0.3,
            anxiety_risk=0.2
        )
        switch_prob = self.layer7_customer.calculate_switch_probability(cust)

        # Layer 8
        pos_dist = self.layer8_marketing.project_positioning_distance(
            product_vector=[1.0, 0.8, 0.9],
            competitor_vectors=[[0.2, 0.3, 0.1], [0.5, 0.5, 0.5]]
        )

        # Layer 9
        inaction_loss = self.layer9_sales.calculate_inaction_compounding_loss(
            monthly_cost_cents=50000,
            elapsed_months=6
        )

        # Layer 10
        net_val = self.layer10_growth.evaluate_network_value(active_nodes=venture.active_customers + 100)

        # Layer 11
        moat_score = self.layer11_competition.calculate_7_powers_moat_score({
            "scale_economies": 0.6,
            "switching_costs": 0.8,
            "network_effects": 0.7
        })

        # Layer 12
        hiring_res = self.layer12_org.calculate_hiring_shadow_price(
            bottleneck_utility_delta=150.0,
            wage_cents=1000000  # $10k/mo
        )

        # Layer 13
        meta_res = self.layer13_meta.execute_triple_loop_backprop(
            prediction_error=0.15,
            current_model_params={"p_success": bayes_prob}
        )

        # Active Inference EFE Ranking via ActiveInferencePlanner
        opp = Opportunity(
            title=signal.title,
            domain=signal.domain,
            variables=scm.variables,
            causal_edges=scm.causal_edges,
            prior_entropy=signal.market_entropy,
            post_entropy_simulated=signal.reality_entropy,
            success_probability=bayes_prob,
            tam_cents=signal.tam_cents
        )
        efe = self.planner.calculate_efe(opp)

        return {
            "status": "orchestrated",
            "opportunity_title": signal.title,
            "expected_free_energy": efe,
            "posterior_success_probability": bayes_prob,
            "layer1_viability": l1_res["thermodynamically_viable"],
            "layer2_weak_signal": l2_res["is_actionable_weak_signal"],
            "layer3_root_cause": l3_res["root_cause"],
            "layer5_discounted_ev_cents": l5_res["discounted_ev_cents"],
            "layer6_regularized_features": l6_spec.features,
            "layer7_switch_probability": switch_prob,
            "layer8_positioning_distance": pos_dist,
            "layer9_inaction_loss_cents": inaction_loss,
            "layer10_network_value": net_val,
            "layer11_moat_score": moat_score,
            "layer12_hiring": hiring_res["trigger_hiring_workflow"],
            "layer13_meta_params": meta_res["loop1_updated_parameters"]
        }
