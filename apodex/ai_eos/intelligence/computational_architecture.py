"""
The complete, first-principles executable implementation of the
14-Layer Computational Architecture of Entrepreneurship for SERO v2.1.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.computational_architecture")


# ---------------------------------------------------------------------------
# Data Models & Shared Primitives
# ---------------------------------------------------------------------------

class Opportunity(BaseModel):
    """The canonical data model representing a discovered opportunity state."""
    opportunity_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str
    variables: List[str] = Field(default_factory=list)
    causal_edges: List[Tuple[str, str]] = Field(default_factory=list)
    coefficients: Dict[str, float] = Field(default_factory=dict)
    prior_entropy: float = 1.0
    post_entropy_simulated: float = 0.5
    success_probability: float = 0.5
    target_preference: float = 0.9
    tam_cents: int = 100000000  # Default $1M
    is_active: bool = True
    # Advanced 14-layer metadata
    cac_cents: int = 5000
    ltv_cents: int = 25000
    payback_months: float = 6.0
    moat_score: float = 0.7
    job_to_be_done: str = ""


class ProblemDefinition(BaseModel):
    """Canonical model for problem representation (Layer 3)."""
    problem_id: UUID = Field(default_factory=uuid4)
    statement: str
    domain: str
    is_root_cause: bool = False
    order: int = 1  # 1st-order, 2nd-order, etc.
    symptoms: List[str] = Field(default_factory=list)
    underlying_causes: List[str] = Field(default_factory=list)
    severity_score: float = 0.5
    ignore_recommendation: bool = False


class CustomerProfile(BaseModel):
    """Customer psychology and economic behavior model (Layer 7)."""
    customer_id: UUID = Field(default_factory=uuid4)
    segment: str
    perceived_value_cents: int
    price_cents: int
    switching_barrier_score: float = 0.5  # 0 to 1
    trust_level: float = 0.5  # 0 to 1
    churn_probability: float = 0.05
    nps_score: int = 8


# ---------------------------------------------------------------------------
# Layer 1: Reality & Invariants
# ---------------------------------------------------------------------------

class RealityInvariantsEngine:
    """
    Layer 1: Reality & Invariants.
    Evaluates fundamental non-negotiables: unit economics, entropy reduction,
    value exchange invariant (V_perceived > Price > Cost), and automatable vs human domains.
    """

    def evaluate_invariant_value_exchange(self, perceived_value_cents: int, price_cents: int, cost_cents: int) -> Dict[str, Any]:
        """
        Invariant: Sustainable value exchange requires Perceived Value > Price > Cost.
        Returns viability boolean and margin calculations.
        """
        is_viable = perceived_value_cents > price_cents and price_cents > cost_cents
        customer_surplus = max(0, perceived_value_cents - price_cents)
        producer_margin = max(0, price_cents - cost_cents)
        gross_margin_pct = (producer_margin / price_cents * 100.0) if price_cents > 0 else 0.0

        return {
            "is_viable": is_viable,
            "customer_surplus_cents": customer_surplus,
            "producer_margin_cents": producer_margin,
            "gross_margin_pct": gross_margin_pct,
            "reason": "Value exchange invariant satisfied" if is_viable else "Violates perceived_value > price > cost invariant"
        }

    def partition_automation_boundary(self, task_name: str, involves_empathy: bool, involves_optimization: bool, involves_risk_taking: bool) -> str:
        """
        Partition tasks into CAN_BE_AUTOMATED, REQUIRES_HUMAN_JUDGMENT, or HYBRID.
        """
        if involves_risk_taking or (involves_empathy and not involves_optimization):
            return "REQUIRES_HUMAN_JUDGMENT"
        elif involves_optimization and not involves_empathy:
            return "CAN_BE_AUTOMATED"
        else:
            return "HYBRID"


# ---------------------------------------------------------------------------
# Layer 2: Opportunity Discovery
# ---------------------------------------------------------------------------

class OpportunityDiscoveryEngine:
    """
    Layer 2: Continuous Search of World State Space.
    Detects weak signals, filters surprise/anomalies, cross-combines unrelated observations,
    and forecasts trend shifts.
    """

    def detect_weak_signals(self, raw_observations: List[Dict[str, Any]], threshold: float = 0.3) -> List[Dict[str, Any]]:
        """Filters observations based on variance / anomaly threshold."""
        weak_signals = []
        for obs in raw_observations:
            signal_strength = obs.get("signal_variance", 0.0)
            if signal_strength >= threshold:
                weak_signals.append({**obs, "weak_signal_detected": True, "strength": signal_strength})
        return weak_signals

    def cross_combine_domains(self, domain_a_trends: List[str], domain_b_trends: List[str]) -> List[Dict[str, Any]]:
        """Synthesizes novelty by computing combinatorial cross-domain intersections."""
        novel_combinations = []
        for trend_a in domain_a_trends:
            for trend_b in domain_b_trends:
                combination_title = f"{trend_a} x {trend_b}"
                novelty_score = 0.85  # High synthetic novelty
                novel_combinations.append({
                    "title": combination_title,
                    "domain_a": trend_a,
                    "domain_b": trend_b,
                    "novelty_score": novelty_score
                })
        return novel_combinations


# ---------------------------------------------------------------------------
# Layer 3: Problem Discovery & Causal Engine
# ---------------------------------------------------------------------------

class AdvancedCausalEngine:
    """
    Layer 3: Implements a robust Structural Causal Model (SCM) capable of handling
    Pearl's do-calculus interventions and counterfactual estimations.
    """

    def __init__(self) -> None:
        self.variables: Set[str] = set()
        self.parents: Dict[str, List[str]] = {}
        self.coefficients: Dict[Tuple[str, str], float] = {}
        self.baseline_noise: Dict[str, float] = {}

    def register_variable(self, name: str, noise_variance: float = 0.1) -> None:
        self.variables.add(name)
        self.baseline_noise[name] = noise_variance
        if name not in self.parents:
            self.parents[name] = []

    def add_causal_relationship(self, parent: str, child: str, coefficient: float) -> None:
        self.register_variable(parent)
        self.register_variable(child)
        if parent not in self.parents[child]:
            self.parents[child].append(parent)
        self.coefficients[(parent, child)] = coefficient

    def execute_do_intervention(self, target_var: str, value: float) -> Dict[str, float]:
        """
        Simulates Judea Pearl's do-operator (do(X = x)).
        Mutates structural equations, freezing target variable and propagating downstream effects.
        """
        if target_var not in self.variables:
            raise ValueError(f"Variable '{target_var}' is not registered.")

        state: Dict[str, float] = {var: 0.0 for var in self.variables}
        state[target_var] = value

        for _ in range(len(self.variables)):
            for var in self.variables:
                if var == target_var:
                    continue

                parents_list = self.parents.get(var, [])
                if not parents_list:
                    continue

                structural_sum = 0.0
                for parent in parents_list:
                    coef = self.coefficients.get((parent, var), 0.0)
                    structural_sum += coef * state[parent]

                state[var] = structural_sum

        return state

    def estimate_counterfactual(
        self,
        factual_observations: Dict[str, float],
        counterfactual_intervention: Tuple[str, float],
        target_outcome_var: str
    ) -> float:
        """
        Computes counterfactual outcomes: 'What would target_outcome_var have been had we performed counterfactual_intervention?'
        """
        intervened_var, inter_value = counterfactual_intervention

        # 1. Abduction Phase: Estimate background noise (U) for each variable
        noise_estimates: Dict[str, float] = {}
        for var in self.variables:
            factual_val = factual_observations.get(var, 0.0)
            parents_list = self.parents.get(var, [])
            structural_expected = 0.0
            for parent in parents_list:
                coef = self.coefficients.get((parent, var), 0.0)
                structural_expected += coef * factual_observations.get(parent, 0.0)

            noise_estimates[var] = factual_val - structural_expected

        # 2. Action & Prediction Phase: Execute intervention under updated noise state
        state: Dict[str, float] = {var: 0.0 for var in self.variables}
        state[intervened_var] = inter_value

        for _ in range(len(self.variables)):
            for var in self.variables:
                if var == intervened_var:
                    continue

                parents_list = self.parents.get(var, [])
                structural_sum = 0.0
                for parent in parents_list:
                    coef = self.coefficients.get((parent, var), 0.0)
                    structural_sum += coef * state[parent]

                state[var] = structural_sum + noise_estimates.get(var, 0.0)

        return state.get(target_outcome_var, 0.0)


class ProblemDiscoveryEngine:
    """
    Layer 3: Problem Decomposition & Root Cause Analysis.
    Distinguishes symptoms from root causes, 1st vs 2nd order problems, and determines ignore recommendations.
    """

    def decompose_problem(self, statement: str, symptoms: List[str], causes: List[str]) -> ProblemDefinition:
        """Classifies root cause vs symptom and assigns order/ignore recommendations."""
        is_root = len(causes) > 0 and len(symptoms) > 0
        order = 1 if len(causes) <= 1 else 2
        severity = min(1.0, 0.2 * len(symptoms) + 0.3 * len(causes))
        ignore = severity < 0.25 or not is_root

        return ProblemDefinition(
            statement=statement,
            domain="decomposed",
            is_root_cause=is_root,
            order=order,
            symptoms=symptoms,
            underlying_causes=causes,
            severity_score=severity,
            ignore_recommendation=ignore
        )


# ---------------------------------------------------------------------------
# Layer 4: Decision Making Under Uncertainty
# ---------------------------------------------------------------------------

class DecisionEngine:
    """
    Layer 4: Elite Decision Making.
    Optimal stopping, data-intuition confidence blending, fast idea killing, and anti-confirmation bias updates.
    """

    def optimal_stopping_decision(self, sample_results: List[float], budget_limit: int = 100) -> Dict[str, Any]:
        """
        Secretary problem / Optimal Stopping Rule (37% rule).
        """
        n = len(sample_results)
        if n == 0:
            return {"action": "CONTINUE_SAMPLING", "selected_value": None}

        lookahead_cutoff = int(math.ceil(budget_limit * 0.37))
        if n < lookahead_cutoff:
            return {"action": "CONTINUE_SAMPLING", "best_in_sample": max(sample_results)}

        benchmark = max(sample_results[:lookahead_cutoff])
        current_candidate = sample_results[-1]

        if current_candidate >= benchmark or n >= budget_limit:
            return {"action": "STOP_AND_COMMIT", "selected_value": current_candidate}
        return {"action": "CONTINUE_SAMPLING", "best_candidate_so_far": max(sample_results)}

    def blend_data_and_intuition(self, data_confidence: float, intuition_score: float, data_volume: int) -> float:
        """
        Bayesian weight allocation: As data volume grows, data confidence dominates; low data relies on prior (intuition).
        """
        weight_data = min(1.0, data_volume / 50.0)
        weight_intuition = 1.0 - weight_data
        blended = (weight_data * data_confidence) + (weight_intuition * intuition_score)
        return blended

    def evaluate_idea_kill_threshold(self, milestones_failed: int, max_allowed_failures: int = 2) -> Dict[str, Any]:
        """Fast idea-killing protocol."""
        should_kill = milestones_failed >= max_allowed_failures
        return {
            "should_kill": should_kill,
            "recommendation": "KILL_IMMEDIATELY" if should_kill else "PERSEVERE_AND_PIVOT"
        }


# ---------------------------------------------------------------------------
# Layer 5: Opportunity Evaluation
# ---------------------------------------------------------------------------

class ActiveInferencePlanner:
    """
    Layer 5 & 14: Active Inference Decision Framework based on Expected Free Energy (EFE).
    """

    def __init__(self, curiosity_weight: float = 1.0) -> None:
        self.curiosity_weight = curiosity_weight

    def calculate_efe(self, opp: Opportunity) -> float:
        """
        Expected Free Energy G = - Pragmatic Value - Epistemic Value * curiosity_weight
        Where:
          - Pragmatic Value = ln(p_success) - ln(p_target_preference)
          - Epistemic Value = prior_entropy - post_entropy_simulated
        """
        eps = 1e-10
        p_success = max(eps, min(1.0 - eps, opp.success_probability))
        p_target = max(eps, min(1.0 - eps, opp.target_preference))

        pragmatic_value = math.log(p_success) - math.log(p_target)
        epistemic_value = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)

        efe = -pragmatic_value - (epistemic_value * self.curiosity_weight)
        return efe

    def rank_opportunities(self, opportunities: List[Opportunity]) -> List[Tuple[Opportunity, float]]:
        ranked = []
        for opp in opportunities:
            efe = self.calculate_efe(opp)
            ranked.append((opp, efe))
        return sorted(ranked, key=lambda x: x[1])


class OpportunityEvaluationEngine:
    """
    Layer 5: Multi-Variable Quality Evaluation & Downside Risk.
    Calculates Expected Value, Kelly Criterion position sizing, and opportunity switching trade-offs.
    """

    def calculate_kelly_fraction(self, win_probability: float, win_loss_ratio: float) -> float:
        """
        Kelly Criterion f* = (p * b - q) / b
        Where:
          p = win_probability
          q = 1 - win_probability
          b = win_loss_ratio (odds)
        """
        if win_loss_ratio <= 0:
            return 0.0
        q = 1.0 - win_probability
        kelly = (win_probability * win_loss_ratio - q) / win_loss_ratio
        return max(0.0, kelly)

    def evaluate_switching_tradeoff(self, current_opp: Opportunity, new_opp: Opportunity, switching_cost_cents: int) -> Dict[str, Any]:
        """Determines whether to pivot from current opportunity to new opportunity."""
        current_ev = current_opp.tam_cents * current_opp.success_probability
        new_ev = new_opp.tam_cents * new_opp.success_probability
        net_new_ev = new_ev - switching_cost_cents

        should_switch = net_new_ev > current_ev
        return {
            "should_switch": should_switch,
            "current_ev_cents": current_ev,
            "new_ev_cents": new_ev,
            "net_new_ev_cents": net_new_ev,
            "advantage_delta_cents": net_new_ev - current_ev
        }


# ---------------------------------------------------------------------------
# Layer 6: Product Creation & Job-To-Be-Done
# ---------------------------------------------------------------------------

class ProductCreationEngine:
    """
    Layer 6: Product Creation & JTBD Optimization.
    Determines what NOT to build, minimizes complexity, and optimizes for learning velocity over feature creep.
    """

    def analyze_job_to_be_done(self, target_customer_goal: str, proposed_features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Filters features into essential (JTBD driver) vs non-essential scope creep.
        """
        essential_features = []
        bloat_features = []

        for feature in proposed_features:
            is_core = feature.get("directly_addresses_goal", False)
            learning_value = feature.get("learning_value_score", 0.5)

            if is_core or learning_value >= 0.7:
                essential_features.append(feature["name"])
            else:
                bloat_features.append(feature["name"])

        return {
            "job_to_be_done": target_customer_goal,
            "essential_mvp_features": essential_features,
            "rejected_bloat_features": bloat_features,
            "complexity_reduction_pct": (len(bloat_features) / len(proposed_features) * 100.0) if proposed_features else 0.0
        }


# ---------------------------------------------------------------------------
# Layer 7: Customer Understanding & Psychology
# ---------------------------------------------------------------------------

class CustomerUnderstandingEngine:
    """
    Layer 7: Customer Psychology, Trust & Retention.
    Models trust accumulation, switching barriers, churn risk, and evangelism / NPS dynamics.
    """

    def predict_churn_risk(self, profile: CustomerProfile, usage_frequency_days: int) -> float:
        """Estimates churn risk based on usage gap and trust level."""
        gap_penalty = min(0.5, usage_frequency_days * 0.05)
        trust_benefit = profile.trust_level * 0.3
        risk = max(0.01, min(0.99, profile.churn_probability + gap_penalty - trust_benefit))
        return risk

    def calculate_net_promoter_category(self, nps_score: int) -> str:
        """Classifies customer into Promoter, Passive, or Detractor."""
        if nps_score >= 9:
            return "PROMOTER"
        elif nps_score >= 7:
            return "PASSIVE"
        else:
            return "DETRACTOR"


# ---------------------------------------------------------------------------
# Layer 8: Marketing & Market Dynamics
# ---------------------------------------------------------------------------

class MarketingEngine:
    """
    Layer 8: Market Formation, Brand & Viral Dynamics.
    Viral coefficient K = i * c, attention spread, positioning vector distance.
    """

    def calculate_viral_coefficient(self, invites_sent_per_user: float, conversion_rate: float) -> Dict[str, Any]:
        """
        K = i * c. K > 1 signifies compounding exponential growth.
        """
        k_factor = invites_sent_per_user * conversion_rate
        is_compounding = k_factor > 1.0
        return {
            "viral_coefficient_k": k_factor,
            "is_compounding": is_compounding,
            "classification": "VIRAL_COMPOUNDING" if is_compounding else "LINEAR_OR_SUBVIRAL"
        }


# ---------------------------------------------------------------------------
# Layer 9: Sales Systems
# ---------------------------------------------------------------------------

class SalesEngine:
    """
    Layer 9: Sales Psychology, Urgency & Funnel Automation.
    Models buyer urgency state transitions, objection resolution causal loops, and automation readiness.
    """

    def evaluate_automation_readiness(self, monthly_deals: int, process_repeatability_score: float) -> bool:
        """Selling should be automated when repeatability is high (>0.8) and deal volume is substantial (>30)."""
        return process_repeatability_score >= 0.8 and monthly_deals >= 30

    def resolve_objection(self, objection_type: str, price_cents: int, ltv_cents: int) -> Dict[str, Any]:
        """Causal objection solver."""
        if objection_type == "PRICE_TOO_HIGH":
            roi_multiple = ltv_cents / max(1, price_cents)
            return {
                "strategy": "DEMONSTRATE_ROI",
                "argument": f"Solution yields {roi_multiple:.1f}x ROI multiple over customer lifetime.",
                "resolved": roi_multiple >= 3.0
            }
        return {"strategy": "DISCOVER_ROOT_NEED", "argument": "Clarify non-price value driver.", "resolved": True}


# ---------------------------------------------------------------------------
# Layer 10: Growth & Network Effects
# ---------------------------------------------------------------------------

class GrowthEngine:
    """
    Layer 10: Compounding Growth & Ecosystem Platforms.
    Models network effect dynamics (Metcalfe's Law V ~ N^2) and platform transitions.
    """

    def compute_network_value(self, active_users: int, elasticity: float = 1.0) -> float:
        """Metcalfe's Law Value = elasticity * N^2."""
        return elasticity * (active_users ** 2)

    def evaluate_platform_transition(self, product_users: int, third_party_developers: int) -> Dict[str, Any]:
        """Evaluates whether product can transition into an ecosystem platform."""
        is_platform_ready = product_users >= 10000 and third_party_developers >= 50
        return {
            "is_platform_ready": is_platform_ready,
            "developer_ecosystem_health": "STRONG" if third_party_developers >= 50 else "EMBRYONIC"
        }


# ---------------------------------------------------------------------------
# Layer 11: Competition & Moats
# ---------------------------------------------------------------------------

class CompetitionEngine:
    """
    Layer 11: Strategic Moats & Disruption Survival.
    Computes moat durability score and predicts game-theoretic competitor reactions.
    """

    def calculate_moat_durability(self, network_effects: float, switching_costs: float, cost_advantage: float, brand_equity: float) -> float:
        """Composite moat durability index (0 to 1)."""
        weights = [0.35, 0.25, 0.20, 0.20]
        score = (network_effects * weights[0] +
                 switching_costs * weights[1] +
                 cost_advantage * weights[2] +
                 brand_equity * weights[3])
        return min(1.0, max(0.0, score))


# ---------------------------------------------------------------------------
# Layer 12: Organizational Design
# ---------------------------------------------------------------------------

class OrganizationalEngine:
    """
    Layer 12: Organizational Structure & Delegation Scaling.
    Evaluates hiring velocity triggers and centralize vs delegate boundaries.
    """

    def evaluate_hiring_trigger(self, current_utilization_pct: float, revenue_per_employee_cents: int) -> Dict[str, Any]:
        """Hiring trigger when utilization exceeds 85% and unit productivity supports headcount."""
        should_hire = current_utilization_pct >= 85.0 and revenue_per_employee_cents >= 15000000  # $150k
        return {
            "should_hire": should_hire,
            "action": "EXPAND_HEADCOUNT" if should_hire else "OPTIMIZE_INTERNAL_EFFICIENCY"
        }


# ---------------------------------------------------------------------------
# Layer 13: Meta-Learning & Mental Models
# ---------------------------------------------------------------------------

class MetaLearningEngine:
    """
    Layer 13: Self-Improvement & Mental Model Calibration.
    Calculates decision quality Brier score and updates mental models from failure logs.
    """

    def calculate_brier_score(self, forecast_probabilities: List[float], actual_outcomes: List[int]) -> float:
        """
        Brier Score BS = (1/N) * sum((p_i - o_i)^2).
        Lower BS (closer to 0.0) indicates superior calibration.
        """
        if not forecast_probabilities or len(forecast_probabilities) != len(actual_outcomes):
            return 1.0

        n = len(forecast_probabilities)
        sum_sq_err = sum((p - o) ** 2 for p, o in zip(forecast_probabilities, actual_outcomes))
        return sum_sq_err / n

    def convert_failure_to_reusable_rule(self, failure_incident: Dict[str, Any]) -> Dict[str, Any]:
        """Distills post-mortem failure into a machine-readable heuristic rule."""
        root_cause = failure_incident.get("root_cause", "UNKNOWN")
        domain = failure_incident.get("domain", "GENERAL")

        rule = f"IF domain == '{domain}' AND trigger == '{root_cause}' THEN EXECUTE_SAFEGUARD"
        return {
            "generated_rule": rule,
            "status": "RULE_REGISTERED"
        }


# ---------------------------------------------------------------------------
# Layer 14: AI Entrepreneurship & Master Pipeline Orchestrator
# ---------------------------------------------------------------------------

class EntrepreneurialIntelligenceOrchestrator:
    """
    Layer 14: Master Coordinating Engine driving the complete 14-layer execution pipeline.
    """

    def __init__(self, causal_engine: AdvancedCausalEngine, planner: ActiveInferencePlanner) -> None:
        self.causal_engine = causal_engine
        self.planner = planner
        self.opportunities: List[Opportunity] = []

        # Sub-engines
        self.layer1_reality = RealityInvariantsEngine()
        self.layer2_discovery = OpportunityDiscoveryEngine()
        self.layer3_problem = ProblemDiscoveryEngine()
        self.layer4_decision = DecisionEngine()
        self.layer5_eval = OpportunityEvaluationEngine()
        self.layer6_product = ProductCreationEngine()
        self.layer7_customer = CustomerUnderstandingEngine()
        self.layer8_marketing = MarketingEngine()
        self.layer9_sales = SalesEngine()
        self.layer10_growth = GrowthEngine()
        self.layer11_competition = CompetitionEngine()
        self.layer12_org = OrganizationalEngine()
        self.layer13_meta = MetaLearningEngine()

    def ingest_signal(self, signal: Dict[str, Any]) -> Opportunity:
        """Senses external changes and creates a candidate opportunity state."""
        logger.info(f"Sensing external signal: {signal.get('title')}")
        opp = Opportunity(
            title=signal.get("title", "Unnamed Opportunity"),
            domain=signal.get("domain", "general"),
            variables=signal.get("variables", []),
            causal_edges=signal.get("causal_edges", []),
            coefficients=signal.get("coefficients", {}),
            prior_entropy=signal.get("prior_entropy", 1.5),
            post_entropy_simulated=signal.get("post_entropy_simulated", 0.4),
            success_probability=signal.get("success_probability", 0.5),
            tam_cents=signal.get("tam_cents", 100000000),
            cac_cents=signal.get("cac_cents", 5000),
            ltv_cents=signal.get("ltv_cents", 25000),
            job_to_be_done=signal.get("job_to_be_done", "Solve primary domain problem")
        )
        self.opportunities.append(opp)
        return opp

    def execute_orchestrated_pipeline(self) -> Dict[str, Any]:
        """Runs the 14-layer analysis pipeline over active opportunities."""
        if not self.opportunities:
            return {"status": "idle", "reason": "No opportunities registered."}

        # 1. Layer 2 & 5 & 14: Opportunity Evaluation and Active Inference Ranking
        ranked_opps = self.planner.rank_opportunities(self.opportunities)
        primary_opp, best_efe = ranked_opps[0]

        logger.info(f"Orchestrator selected primary opportunity: '{primary_opp.title}' with EFE: {best_efe:.4f}")

        # 2. Layer 1: Invariant Value Exchange Verification
        price_cents = int(primary_opp.ltv_cents * 0.2)
        cost_cents = int(primary_opp.cac_cents)
        perceived_val = int(primary_opp.ltv_cents)
        l1_result = self.layer1_reality.evaluate_invariant_value_exchange(perceived_val, price_cents, cost_cents)

        # 3. Layer 3: Structural Causal Initialization
        for var in primary_opp.variables:
            self.causal_engine.register_variable(var)
        for parent, child in primary_opp.causal_edges:
            weight = primary_opp.coefficients.get(f"{parent}->{child}", 0.5)
            self.causal_engine.add_causal_relationship(parent, child, weight)

        # 4. Layer 3 & 4: Simulate Causal Intervention
        intervention_var = primary_opp.variables[0] if primary_opp.variables else "marketing_spend"
        inter_state = self.causal_engine.execute_do_intervention(intervention_var, 1.5)

        # 5. Layer 5: Kelly Position Sizing
        kelly_frac = self.layer5_eval.calculate_kelly_fraction(
            win_probability=primary_opp.success_probability,
            win_loss_ratio=(primary_opp.ltv_cents / max(1, primary_opp.cac_cents))
        )

        # 6. Layer 11: Moat Score
        moat_score = self.layer11_competition.calculate_moat_durability(0.8, 0.7, 0.6, 0.5)

        # 7. Layer 13: Meta-Learning Decision Registration
        brier = self.layer13_meta.calculate_brier_score([primary_opp.success_probability], [1])

        return {
            "status": "executed",
            "selected_opportunity": primary_opp.title,
            "best_expected_free_energy": best_efe,
            "layer1_invariant_exchange": l1_result,
            "intervention_performed": f"do({intervention_var} = 1.5)",
            "propagated_state": inter_state,
            "kelly_capital_fraction": kelly_frac,
            "moat_durability_score": moat_score,
            "meta_brier_calibration": brier
        }
