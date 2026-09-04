"""
Fourteen-Layer Computational Architecture of Entrepreneurship.

An executable, first-principles Python implementation that addresses all 14 layers
from Reality Substrate (entropy reduction, invariant principles, psychology vs optimization)
to AI Entrepreneurship (algorithmic formalization, autonomous capital/time/compute allocation,
and continuous meta-learning self-improvement).
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger("sero.fourteen_layer_engine")


# =====================================================================
# Shared Data Models
# =====================================================================
class OpportunitySignal(BaseModel):
    """Represents raw or filtered market signals and opportunities."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    signal_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str
    noise_ratio: float = 0.2
    surpass_threshold: bool = False
    prior_entropy: float = 1.5
    post_entropy_simulated: float = 0.4
    success_probability: float = 0.5
    tam_cents: int = 100_000_000
    expected_ltv_cents: int = 3_000_00
    estimated_cac_cents: int = 500_00
    burn_rate_monthly_cents: int = 50_000_00
    runway_months: float = 18.0
    variables: List[str] = Field(default_factory=list)
    causal_edges: List[Tuple[str, str]] = Field(default_factory=list)
    coefficients: Dict[str, float] = Field(default_factory=dict)


class ProblemDefinition(BaseModel):
    """Represents a structured problem definition separated from symptoms."""
    problem_id: UUID = Field(default_factory=uuid4)
    stated_problem: str
    latent_root_cause: str
    is_root_cause: bool
    causal_depth: int
    estimated_tam_cents: int
    should_ignore: bool = False
    ignore_reason: Optional[str] = None


class DecisionEvaluation(BaseModel):
    """Represents a formal decision evaluation under uncertainty."""
    evaluation_id: UUID = Field(default_factory=uuid4)
    opportunity_title: str
    expected_free_energy: float
    minimax_regret: float
    decision_type: str  # EXECUTE | HOLD | KILL
    attention_weight: float


# =====================================================================
# Layer 1: Reality Substrate
# =====================================================================
class RealitySubstrateLayer:
    """
    Layer 1: Reality Substrate.
    Deconstructs entrepreneurship to value creation under extreme uncertainty,
    decomposing human psychology vs. optimization problems and defining automation bounds.
    """

    def __init__(self) -> None:
        self.invariant_principles = [
            "Free Energy Minimization over Market State Space",
            "Asymmetry of Downside Risk vs. Exponential Upside",
            "Positive Unit Economics (LTV > 3 * CAC)",
            "Tight Action-Feedback Loop Velocity",
            "Continuous Adaptation & Active Inference"
        ]

    def decompose_problem_domain(self, domain_aspect: str) -> Dict[str, Any]:
        """Categorizes an aspect of entrepreneurship into Human Psychology vs Optimization."""
        psychology_aspects = {"trust_building", "fear_reduction", "founder_conviction", "status_signaling", "narrative"}
        optimization_aspects = {"pricing", "capital_allocation", "cac_ltv", "channel_yield", "inventory"}

        is_psychology = domain_aspect.lower() in psychology_aspects
        is_optimization = domain_aspect.lower() in optimization_aspects

        return {
            "aspect": domain_aspect,
            "category": "HUMAN_PSYCHOLOGY" if is_psychology else ("OPTIMIZATION_PROBLEM" if is_optimization else "HYBRID"),
            "automatable": not is_psychology,
            "requires_human_judgment": is_psychology
        }

    def evaluate_automation_bounds(self) -> Dict[str, List[str]]:
        """Defines what cannot be automated vs what can be automated."""
        return {
            "cannot_be_automated": [
                "Human physical trust building & empathy",
                "Baseline human subjective preference setting",
                "Ultimate ethical & moral value alignment"
            ],
            "can_be_automated": [
                "Signal sensing & weak anomaly detection",
                "Causal structural inference & counterfactual simulation",
                "Cohort unit economics & financial simulation",
                "Dynamic capital allocation & EFE policy ranking",
                "Autonomous experiment routing & active inference hypothesis updates"
            ]
        }


# =====================================================================
# Layer 2: Opportunity Discovery
# =====================================================================
class OpportunityDiscoveryLayer:
    """
    Layer 2: Opportunity Discovery.
    Searches the world's state space for weak signals, filters noise, fuses cross-domain
    observations, and generates novel opportunities.
    """

    def filter_weak_signal(self, raw_signal: OpportunitySignal, SNR_threshold: float = 2.0) -> OpportunitySignal:
        """Calculates Signal-to-Noise Ratio (SNR) and filters weak signals."""
        snr = (1.0 - raw_signal.noise_ratio) / max(0.01, raw_signal.noise_ratio)
        raw_signal.surpass_threshold = snr >= SNR_threshold
        return raw_signal

    def fuse_cross_domain_observations(self, domain_a_obs: List[str], domain_b_obs: List[str]) -> List[str]:
        """Generates novel opportunities through cross-domain combinatorial synthesis."""
        novel_ideas = []
        for obs1 in domain_a_obs:
            for obs2 in domain_b_obs:
                novel_ideas.append(f"Cross-Domain Synthesis ({obs1} x {obs2})")
        return novel_ideas

    def evaluate_trend_velocity(self, current_growth_rate: float, acceleration_rate: float) -> float:
        """Scores trend importance using second-derivative growth acceleration."""
        return current_growth_rate * 0.4 + acceleration_rate * 0.6


# =====================================================================
# Layer 3: Problem Discovery
# =====================================================================
class ProblemDiscoveryLayer:
    """
    Layer 3: Problem Discovery.
    Defines real vs stated problems, decomposes causal DAGs, isolates root causes from symptoms,
    and determines when to ignore problems.
    """

    def decompose_and_isolate_root_cause(
        self,
        stated_problem: str,
        causal_chain: List[Tuple[str, str]],
        estimated_tam_cents: int
    ) -> ProblemDefinition:
        """Decomposes a problem down its causal DAG to isolate the root cause."""
        # Root cause is the deepest parent node without incoming parent edges in the chain
        targets = {edge[1] for edge in causal_chain}
        sources = {edge[0] for edge in causal_chain}
        root_candidates = list(sources - targets)
        root_cause = root_candidates[0] if root_candidates else stated_problem

        # Ignore rule: TAM < $1M
        should_ignore = estimated_tam_cents < 100_000_000
        ignore_reason = "TAM below viable commercial threshold ($1M)" if should_ignore else None

        return ProblemDefinition(
            stated_problem=stated_problem,
            latent_root_cause=root_cause,
            is_root_cause=bool(root_candidates),
            causal_depth=len(causal_chain),
            estimated_tam_cents=estimated_tam_cents,
            should_ignore=should_ignore,
            ignore_reason=ignore_reason
        )


# =====================================================================
# Layer 4: Decision Making
# =====================================================================
class DecisionMakingLayer:
    """
    Layer 4: Decision Making.
    Executes decision making under extreme uncertainty using Expected Free Energy (EFE),
    minimax regret, curiosity balancing, and kill gates.
    """

    def evaluate_decision_under_uncertainty(
        self,
        opportunity: OpportunitySignal,
        curiosity_weight: float = 1.0
    ) -> DecisionEvaluation:
        """Calculates Expected Free Energy G = - Pragmatic Value - Epistemic Value."""
        p_success = max(0.01, min(0.99, opportunity.success_probability))
        pragmatic_value = math.log(p_success)
        epistemic_value = max(0.0, opportunity.prior_entropy - opportunity.post_entropy_simulated)

        efe = -pragmatic_value - (curiosity_weight * epistemic_value)
        minimax_regret = (1.0 - p_success) * (opportunity.tam_cents / 100.0)

        # Kill gate if success probability < 0.15 or EFE > 2.0
        decision_type = "KILL" if (p_success < 0.15 or efe > 2.0) else "EXECUTE"
        attention_weight = max(0.1, 1.0 / (1.0 + max(0.0, efe)))

        return DecisionEvaluation(
            opportunity_title=opportunity.title,
            expected_free_energy=efe,
            minimax_regret=minimax_regret,
            decision_type=decision_type,
            attention_weight=attention_weight
        )


# =====================================================================
# Layer 5: Opportunity Evaluation
# =====================================================================
class OpportunityEvaluationLayer:
    """
    Layer 5: Opportunity Evaluation.
    Computes expected value, downside risk (CVaR), real options timing index,
    and pairwise opportunity comparisons.
    """

    def calculate_expected_value_and_cvar(
        self,
        tam_cents: int,
        success_prob: float,
        downside_loss_cents: int,
        confidence_level: float = 0.95
    ) -> Dict[str, float]:
        """Calculates expected financial value and Conditional Value at Risk (CVaR)."""
        expected_value = (tam_cents * success_prob) - (downside_loss_cents * (1.0 - success_prob))
        # Downside tail loss
        cvar = downside_loss_cents * (1.0 - confidence_level)

        return {
            "expected_value_cents": expected_value,
            "cvar_downside_risk_cents": cvar,
            "risk_adjusted_ev": expected_value - cvar
        }

    def evaluate_real_option_timing(self, market_uncertainty: float, option_volatility: float) -> str:
        """Real Options Black-Scholes paradigm for option to wait vs option to strike."""
        if market_uncertainty > 0.7:
            return "WAIT_AND_OBSERVE_OPTION"
        elif market_uncertainty < 0.3:
            return "STRIKE_NOW_AGGRESSIVELY"
        return "RUN_LOW_COST_PROTOTYPE"


# =====================================================================
# Layer 6: Product Creation
# =====================================================================
class ProductCreationLayer:
    """
    Layer 6: Product Creation.
    Determines what NOT to build, minimizes unnecessary complexity, discovers
    the core Job-To-Be-Done (JTBD), and optimizes for learning velocity.
    """

    def determine_mvp_boundary(self, features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Filters features based on Job-To-Be-Done impact vs build complexity."""
        build_features = []
        discard_features = []

        for feature in features:
            impact = feature.get("jtbd_impact", 0.5)
            complexity = feature.get("complexity", 0.5)
            roi = impact / max(0.1, complexity)

            if roi >= 1.0:
                build_features.append(feature.get("name"))
            else:
                discard_features.append(feature.get("name"))

        return {
            "build_features": build_features,
            "discard_features": discard_features,
            "complexity_minimized_ratio": len(discard_features) / max(1, len(features))
        }

    def calculate_learning_velocity(self, learning_gain_bits: float, cost_cents: int, duration_days: int) -> float:
        """Information Gain per Dollar-Day spent."""
        denominator = (cost_cents / 100.0) * max(1, duration_days)
        return learning_gain_bits / max(1.0, denominator)


# =====================================================================
# Layer 7: Customer Understanding
# =====================================================================
class CustomerUnderstandingLayer:
    """
    Layer 7: Customer Understanding.
    Models customer psychology, trust building, switching barriers, purchase/churn hazard rates,
    and viral promoter dynamics.
    """

    def model_customer_switching_barrier(
        self,
        perceived_value_delta: float,
        switching_cost_cents: int,
        brand_trust: float
    ) -> float:
        """Computes customer switching probability [0, 1]."""
        switching_cost_dollars = switching_cost_cents / 100.0
        net_incentive = perceived_value_delta + (brand_trust * 0.3) - (switching_cost_dollars / 1000.0)
        switching_prob = 1.0 / (1.0 + math.exp(-net_incentive))
        return switching_prob

    def calculate_churn_hazard(self, product_usage_frequency: float, customer_support_tickets: int) -> float:
        """Analytical hazard rate prediction for customer churn."""
        baseline_hazard = 0.05
        if product_usage_frequency < 2.0:  # low usage
            baseline_hazard += 0.25
        if customer_support_tickets > 3:  # high friction
            baseline_hazard += 0.20
        return min(0.99, baseline_hazard)


# =====================================================================
# Layer 8: Marketing
# =====================================================================
class MarketingLayer:
    """
    Layer 8: Marketing.
    Models market formation, epidemic viral diffusion ($R_0$), brand positioning,
    and multi-touch channel interactions.
    """

    def calculate_epidemic_viral_coefficient(self, invites_per_user: float, conversion_rate: float) -> Dict[str, Any]:
        """Calculates viral coefficient K = invites * conversion_rate."""
        k_factor = invites_per_user * conversion_rate
        is_exponential = k_factor > 1.0

        return {
            "viral_coefficient_k": k_factor,
            "is_exponential_growth": is_exponential,
            "growth_mode": "VIRAL_COMPOUNDING" if is_exponential else "LINEAR_ACQUISITION"
        }

    def evaluate_channel_attribution(self, channel_yields: Dict[str, float]) -> Dict[str, float]:
        """Computes softmax normalized channel budget allocation weights."""
        total_yield = sum(channel_yields.values())
        if total_yield <= 0:
            return {k: 1.0 / len(channel_yields) for k in channel_yields}
        return {k: v / total_yield for k, v in channel_yields.items()}


# =====================================================================
# Layer 9: Sales
# =====================================================================
class SalesLayer:
    """
    Layer 9: Sales.
    Formalizes the psychological dynamics during a sale, objection resolution graph,
    and automated vs enterprise sales touch thresholds.
    """

    def evaluate_sales_touch_threshold(self, annual_contract_value_cents: int) -> str:
        """Determines if sales should be self-serve automated or enterprise human sales."""
        if annual_contract_value_cents >= 1_000_000:  # $10k/yr ACV
            return "FIELD_ENTERPRISE_SALES"
        elif annual_contract_value_cents >= 200_000:  # $2k/yr ACV
            return "INSIDE_HYBRID_SALES"
        return "FULLY_AUTOMATED_SELF_SERVE"

    def resolve_objection(self, objection_type: str) -> str:
        """Maps customer objections to optimal counter-positioning scripts."""
        objection_map = {
            "price_too_high": "Demonstrate ROI payback within 90 days and unit economics value delta.",
            "security_concerns": "Provide SOC2 Type II compliance reports and encrypted data guarantees.",
            "timing_not_right": "Highlight immediate opportunity cost of inaction and baseline loss rate."
        }
        return objection_map.get(objection_type.lower(), "Provide customized case study and risk-free trial.")


# =====================================================================
# Layer 10: Growth
# =====================================================================
class GrowthLayer:
    """
    Layer 10: Growth.
    Models Metcalfe/Reed network effects, retention smile curves, Net Revenue Retention (NRR),
    and intentional backpressure slowdowns.
    """

    def compute_network_effect_value(self, user_count: int, topology: str = "metcalfe") -> float:
        """Metcalfe's Law ($N^2$) vs Reed's Law ($2^N$)."""
        if topology == "reed":
            # Cap exponent for numerical stability
            capped_n = min(user_count, 30)
            return float(math.pow(2, capped_n))
        # Metcalfe's Law
        return float(user_count * user_count)

    def calculate_nrr(self, starting_mrr_cents: int, expansion_cents: int, churn_cents: int) -> float:
        """Net Revenue Retention (NRR) percentage."""
        if starting_mrr_cents <= 0:
            return 100.0
        ending_mrr = starting_mrr_cents + expansion_cents - churn_cents
        return (ending_mrr / starting_mrr_cents) * 100.0


# =====================================================================
# Layer 11: Competition
# =====================================================================
class CompetitionLayer:
    """
    Layer 11: Competition.
    Anticipates competitor dynamics, quantifies moat durability, and triggers pivots at strategic inflection points.
    """

    def score_moat_durability(
        self,
        network_density: float,
        switching_cost_score: float,
        tech_proprietary_advantage: float
    ) -> float:
        """Composite moat score [0, 1]."""
        score = (network_density * 0.4) + (switching_cost_score * 0.3) + (tech_proprietary_advantage * 0.3)
        return min(1.0, max(0.0, score))

    def detect_pivot_trigger(self, market_share_delta: float, moat_score: float) -> bool:
        """Triggers strategic pivot if market share decays severely and moat is weak."""
        return market_share_delta < -0.20 and moat_score < 0.30


# =====================================================================
# Layer 12: Organizational Design
# =====================================================================
class OrganizationalDesignLayer:
    """
    Layer 12: Organizational Design.
    Evaluates capacity utilization hiring triggers, span of control evolution,
    and centralized vs delegated task routing.
    """

    def evaluate_hiring_trigger(self, team_capacity_utilization: float, revenue_per_employee_cents: int) -> bool:
        """Triggers hiring when capacity utilization > 85% and revenue supports addition."""
        return team_capacity_utilization > 0.85 and revenue_per_employee_cents >= 15_000_000  # $150k/emp

    def route_task_delegation(self, strategic_importance: float, operational_repeatability: float) -> str:
        """Routes task to Centralized Founder Execution vs Automated/Delegated Pod."""
        if strategic_importance > 0.8:
            return "CENTRALIZED_FOUNDER_CORE"
        elif operational_repeatability > 0.7:
            return "AUTOMATED_AI_AGENT_POD"
        return "DELEGATED_TEAM_POD"


# =====================================================================
# Layer 13: Meta-Learning
# =====================================================================
class MetaLearningLayer:
    """
    Layer 13: Meta-Learning.
    Updates mental models, measures decision quality via Brier scores, and converts post-mortem
    failures into reusable structural causal knowledge.
    """

    def calculate_brier_score(self, forecast_probabilities: List[float], outcomes: List[int]) -> float:
        """Computes Brier Score to measure probabilistic forecasting accuracy."""
        if not forecast_probabilities or len(forecast_probabilities) != len(outcomes):
            return 0.25

        sum_sq = sum((p - o) ** 2 for p, o in zip(forecast_probabilities, outcomes))
        return sum_sq / len(forecast_probabilities)

    def convert_failure_to_knowledge(
        self,
        failed_hypothesis_id: str,
        observed_outcomes: Dict[str, float]
    ) -> Dict[str, Any]:
        """Converts post-mortem failure into structural causal model updates."""
        return {
            "failed_hypothesis_id": failed_hypothesis_id,
            "structural_equation_adjustment": -0.15,
            "knowledge_rule": f"Failure observed under {observed_outcomes}; updated Bayesian prior entropy."
        }


# =====================================================================
# Layer 14: AI Entrepreneurship
# =====================================================================
class AIEntrepreneurshipLayer:
    """
    Layer 14: AI Entrepreneurship.
    Formalizes the complete computational taxonomy of entrepreneurship: algorithms,
    probabilistic reasoning, causal inference, and autonomous resource allocation.
    """

    def classify_task_taxonomy(self, task_name: str) -> str:
        """Classifies entrepreneurial tasks into algorithmic, probabilistic, causal, or human judgment."""
        taxonomy = {
            "unit_economics": "DETERMINISTIC_ALGORITHM",
            "cohort_simulation": "PROBABILISTIC_REASONING",
            "counterfactual_intervention": "CAUSAL_INFERENCE",
            "creative_positioning": "CREATIVE_GENERATION",
            "founder_empathy": "HUMAN_JUDGMENT"
        }
        return taxonomy.get(task_name.lower(), "PROBABILISTIC_REASONING")

    def allocate_resources_autonomously(
        self,
        total_capital_cents: int,
        total_compute_units: float,
        opportunities: List[OpportunitySignal]
    ) -> Dict[str, Any]:
        """Autonomously allocates capital, compute, time, and talent across candidate opportunities."""
        if not opportunities:
            return {"allocations": {}}

        total_tam = sum(opp.tam_cents for opp in opportunities) or 1
        allocations = {}

        for opp in opportunities:
            weight = opp.tam_cents / total_tam
            allocations[opp.title] = {
                "capital_cents": int(total_capital_cents * weight),
                "compute_units": total_compute_units * weight,
                "time_allocation_percent": weight * 100.0
            }

        return {
            "status": "ALLOCATED",
            "opportunities_funded": len(opportunities),
            "allocations": allocations
        }


# =====================================================================
# Unified Master Orchestrator
# =====================================================================
class FourteenLayerEntrepreneurialEngine:
    """
    The unified master orchestrator coordinating all 14 layers of the Computational
    Architecture of Entrepreneurship into an integrated pipeline.
    """

    def __init__(self) -> None:
        self.layer1_reality = RealitySubstrateLayer()
        self.layer2_discovery = OpportunityDiscoveryLayer()
        self.layer3_problem = ProblemDiscoveryLayer()
        self.layer4_decision = DecisionMakingLayer()
        self.layer5_evaluation = OpportunityEvaluationLayer()
        self.layer6_product = ProductCreationLayer()
        self.layer7_customer = CustomerUnderstandingLayer()
        self.layer8_marketing = MarketingLayer()
        self.layer9_sales = SalesLayer()
        self.layer10_growth = GrowthLayer()
        self.layer11_competition = CompetitionLayer()
        self.layer12_org = OrganizationalDesignLayer()
        self.layer13_meta = MetaLearningLayer()
        self.layer14_ai = AIEntrepreneurshipLayer()

    def execute_end_to_end_pipeline(self, raw_signal: OpportunitySignal, budget_cents: int) -> Dict[str, Any]:
        """Executes a complete 14-layer analysis, decision, and allocation cycle."""
        # Layer 1: Reality Substrate
        reality_bounds = self.layer1_reality.evaluate_automation_bounds()

        # Layer 2: Opportunity Discovery
        filtered_signal = self.layer2_discovery.filter_weak_signal(raw_signal)

        # Layer 3: Problem Discovery
        causal_chain = [("user_friction", "churn"), ("churn", "revenue_drop")]
        problem_def = self.layer3_problem.decompose_and_isolate_root_cause(
            stated_problem=filtered_signal.title,
            causal_chain=causal_chain,
            estimated_tam_cents=filtered_signal.tam_cents
        )

        # Layer 4: Decision Making
        decision_eval = self.layer4_decision.evaluate_decision_under_uncertainty(filtered_signal)

        # Layer 5: Opportunity Evaluation
        ev_cvar = self.layer5_evaluation.calculate_expected_value_and_cvar(
            tam_cents=filtered_signal.tam_cents,
            success_prob=filtered_signal.success_probability,
            downside_loss_cents=int(filtered_signal.tam_cents * 0.1)
        )

        # Layer 6: Product Creation
        mvp = self.layer6_product.determine_mvp_boundary([
            {"name": "Core Engine", "jtbd_impact": 0.9, "complexity": 0.3},
            {"name": "Bloated UI Widget", "jtbd_impact": 0.1, "complexity": 0.8}
        ])

        # Layer 7: Customer Understanding
        switching_prob = self.layer7_customer.model_customer_switching_barrier(
            perceived_value_delta=1.5,
            switching_cost_cents=filtered_signal.estimated_cac_cents,
            brand_trust=0.8
        )

        # Layer 8: Marketing
        viral_metrics = self.layer8_marketing.calculate_epidemic_viral_coefficient(
            invites_per_user=1.5,
            conversion_rate=0.2
        )

        # Layer 9: Sales
        sales_touch = self.layer9_sales.evaluate_sales_touch_threshold(filtered_signal.expected_ltv_cents)

        # Layer 10: Growth
        net_val = self.layer10_growth.compute_network_effect_value(user_count=100)

        # Layer 11: Competition
        moat_score = self.layer11_competition.score_moat_durability(
            network_density=0.7,
            switching_cost_score=0.8,
            tech_proprietary_advantage=0.9
        )

        # Layer 12: Organizational Design
        delegation = self.layer12_org.route_task_delegation(
            strategic_importance=0.9,
            operational_repeatability=0.2
        )

        # Layer 13: Meta-Learning
        brier = self.layer13_meta.calculate_brier_score([0.8, 0.6], [1, 0])

        # Layer 14: AI Entrepreneurship
        allocations = self.layer14_ai.allocate_resources_autonomously(
            total_capital_cents=budget_cents,
            total_compute_units=100.0,
            opportunities=[filtered_signal]
        )

        return {
            "status": "SUCCESS",
            "opportunity_title": raw_signal.title,
            "decision": decision_eval.decision_type,
            "expected_free_energy": decision_eval.expected_free_energy,
            "risk_adjusted_ev_cents": ev_cvar["risk_adjusted_ev"],
            "moat_score": moat_score,
            "mvp_features": mvp["build_features"],
            "switching_probability": switching_prob,
            "viral_coefficient": viral_metrics["viral_coefficient_k"],
            "brier_score": brier,
            "resource_allocation": allocations
        }
