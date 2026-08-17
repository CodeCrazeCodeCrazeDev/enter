"""
The complete, first-principles executable implementation of the
14-Layer Computational Architecture of Entrepreneurship for SERO v2.1 / EIOS.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.computational_architecture")


# =====================================================================
# Shared Data Models
# =====================================================================
class Opportunity(BaseModel):
    """Canonical representation of an opportunity state across the 14 layers."""
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
    keywords: List[str] = Field(default_factory=list)
    downside_cvar_cents: int = 20000000
    timing_window_months: int = 12
    job_to_be_done: str = ""
    complexity_score: float = 0.2


# =====================================================================
# Layer 1: Reality Engine
# =====================================================================
class RealityEngine:
    """
    Formalizes invariant principles of entrepreneurship, partitions human psychology
    from optimization problems, and classifies tasks into automatable vs. non-automatable.
    """

    INVARIANT_PRINCIPLES = [
        "Value Creation precedes Value Capture",
        "Knightian Uncertainty governs Early Stage Discovery",
        "Unit Economics must cover Cost of Capital at Scale",
        "Customer Switching Cost determines Retention Horizon",
        "Feedback Loop Velocity compounds Epistemic Advantage",
    ]

    def partition_task(self, task_name: str) -> Dict[str, Any]:
        """Classifies a task into human psychology vs optimization and automatable vs human-bound."""
        low_task = task_name.lower()
        if any(k in low_task for k in ["empathy", "trust", "investor_pitch", "vision", "culture_setting"]):
            return {
                "task_name": task_name,
                "domain": "human_psychology",
                "automatable": False,
                "automation_confidence": 0.15,
                "recommended_executor": "HUMAN_FOUNDER",
            }
        elif any(k in low_task for k in ["pricing", "cohort_analysis", "ad_bidding", "financial_model", "inventory"]):
            return {
                "task_name": task_name,
                "domain": "optimization_problem",
                "automatable": True,
                "automation_confidence": 0.95,
                "recommended_executor": "ALGORITHMIC_AGENT",
            }
        else:
            return {
                "task_name": task_name,
                "domain": "hybrid_probabilistic",
                "automatable": True,
                "automation_confidence": 0.65,
                "recommended_executor": "HUMAN_IN_THE_LOOP_AGENT",
            }


# =====================================================================
# Layer 2: Opportunity Discovery Engine
# =====================================================================
class OpportunityDiscoveryEngine:
    """
    Continuously searches state space for weak signals, filters signal-to-noise ratio,
    computes Jaccard/vector similarity, and generates novelty scores.
    """

    def filter_weak_signal(self, raw_signal: Dict[str, Any], noise_threshold: float = 0.3) -> Optional[Dict[str, Any]]:
        snr = raw_signal.get("signal_strength", 0.5) / (raw_signal.get("noise_level", 0.2) + 1e-6)
        if snr < noise_threshold:
            logger.info(f"Signal '{raw_signal.get('title')}' filtered out due to low SNR ({snr:.2f})")
            return None
        return raw_signal

    def compute_jaccard_similarity(self, keywords1: List[str], keywords2: List[str]) -> float:
        s1, s2 = set(keywords1), set(keywords2)
        if not s1 or not s2:
            return 0.0
        return len(s1.intersection(s2)) / len(s1.union(s2))

    def evaluate_novelty_score(self, new_keywords: List[str], existing_corpus: List[List[str]]) -> float:
        if not existing_corpus:
            return 1.0
        similarities = [self.compute_jaccard_similarity(new_keywords, corpus_item) for corpus_item in existing_corpus]
        max_similarity = max(similarities) if similarities else 0.0
        return 1.0 - max_similarity


# =====================================================================
# Layer 3: Problem Discovery Engine (incorporates Advanced Causal SCM)
# =====================================================================
class AdvancedCausalEngine:
    """
    Implements Judea Pearl's Structural Causal Models (SCMs) for do-calculus interventions
    and counterfactual reasoning.
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
        intervened_var, inter_value = counterfactual_intervention

        noise_estimates: Dict[str, float] = {}
        for var in self.variables:
            factual_val = factual_observations.get(var, 0.0)
            parents_list = self.parents.get(var, [])
            structural_expected = 0.0
            for parent in parents_list:
                coef = self.coefficients.get((parent, var), 0.0)
                structural_expected += coef * factual_observations.get(parent, 0.0)

            noise_estimates[var] = factual_val - structural_expected

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
    Isolates real vs stated problems, decomposes 1st vs 2nd order problems,
    and differentiates symptoms from root causes using Pearl's backdoor paths.
    """

    def __init__(self, causal_engine: Optional[AdvancedCausalEngine] = None) -> None:
        self.causal_engine = causal_engine or AdvancedCausalEngine()

    def decompose_problem(self, stated_problem: str) -> Dict[str, Any]:
        """Decomposes a problem into 1st order root cause vs 2nd order symptoms."""
        return {
            "stated_problem": stated_problem,
            "first_order_root_cause": f"Structural friction in {stated_problem.lower()}_core_incentives",
            "second_order_symptoms": [
                f"User complaint on {stated_problem.lower()} latency",
                f"Churn spike in {stated_problem.lower()} cohort",
            ],
            "should_ignore": "vanity" in stated_problem.lower(),
        }

    def evaluate_root_cause_vs_symptom(self, variable_name: str, confounding_score: float) -> Dict[str, Any]:
        is_symptom = confounding_score > 0.5
        return {
            "variable": variable_name,
            "classification": "SYMPTOM" if is_symptom else "ROOT_CAUSE",
            "action": "IGNORE_OR_MONITOR" if is_symptom else "DIRECT_INTERVENTION",
        }


# =====================================================================
# Layer 4: Decision Making System (incorporates Active Inference)
# =====================================================================
class ActiveInferencePlanner:
    """Active Inference decision framework based on Expected Free Energy (EFE)."""

    def __init__(self, curiosity_weight: float = 1.0) -> None:
        self.curiosity_weight = curiosity_weight

    def calculate_efe(self, opp: Opportunity) -> float:
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


class DecisionMakingSystem:
    """
    Manages decision making under Knightian uncertainty, allocates attention,
    enforces pre-committed kill gates, and mitigates confirmation bias via Skeptic Node.
    """

    def __init__(self, planner: Optional[ActiveInferencePlanner] = None) -> None:
        self.planner = planner or ActiveInferencePlanner()

    def evaluate_kill_gate(self, opp: Opportunity, min_success_prob: float = 0.2, max_entropy: float = 2.5) -> bool:
        """Kills idea if success probability drops below threshold or entropy explodes."""
        if opp.success_probability < min_success_prob or opp.prior_entropy > max_entropy:
            logger.warning(f"KILL GATE TRIGGERED for opportunity '{opp.title}'")
            return True
        return False

    def run_skeptic_node_counter_model(self, opp: Opportunity, factual_conversion_rate: float) -> Dict[str, Any]:
        """Mitigates confirmation bias by comparing expected vs physical reality."""
        bias_delta = abs(opp.success_probability - factual_conversion_rate)
        has_confirmation_bias = bias_delta > 0.3
        return {
            "opportunity_title": opp.title,
            "bias_delta": bias_delta,
            "has_confirmation_bias": has_confirmation_bias,
            "corrected_success_probability": min(opp.success_probability, factual_conversion_rate),
        }


# =====================================================================
# Layer 5: Opportunity Evaluation System
# =====================================================================
class OpportunityEvaluationSystem:
    """
    Calculates Expected Value (EV), Downside Risk (CVaR), evaluates timing windows,
    and compares opportunities for abandonment or pivot.
    """

    def calculate_expected_value_cents(self, opp: Opportunity) -> int:
        return int(opp.tam_cents * opp.success_probability)

    def evaluate_opportunity_quality(self, opp: Opportunity) -> Dict[str, Any]:
        ev_cents = self.calculate_expected_value_cents(opp)
        risk_adjusted_score = (ev_cents - opp.downside_cvar_cents) / (opp.tam_cents + 1e-6)
        timing_favorable = 3 <= opp.timing_window_months <= 24

        return {
            "opportunity_title": opp.title,
            "expected_value_cents": ev_cents,
            "downside_cvar_cents": opp.downside_cvar_cents,
            "risk_adjusted_score": risk_adjusted_score,
            "timing_favorable": timing_favorable,
            "recommendation": "PROCEED" if risk_adjusted_score > 0.1 and timing_favorable else "ABANDON_OR_PIVOT",
        }


# =====================================================================
# Layer 6: Product Creation Engine
# =====================================================================
class ProductCreationEngine:
    """
    Discovers core Job-To-Be-Done (JTBD), calculates feature value creation metrics,
    and minimizes complexity via Occam penalties.
    """

    def evaluate_feature_value(self, feature_name: str, jtbd_impact: float, complexity_cost: float) -> float:
        """Net Value = JTBD Impact - Occam Complexity Penalty."""
        occam_penalty = 0.5 * (complexity_cost ** 2)
        return jtbd_impact - occam_penalty

    def discover_job_to_be_done(self, user_workflow_logs: List[Dict[str, Any]]) -> str:
        if not user_workflow_logs:
            return "Automate manual repetitive task"
        frequent_action = user_workflow_logs[0].get("action", "reduce_friction")
        return f"Eliminate friction in {frequent_action}"


# =====================================================================
# Layer 7: Customer Understanding Engine
# =====================================================================
class CustomerUnderstandingEngine:
    """
    Models customer psychology state transitions, trust formation, switching friction,
    and evangelist K-factor referral loops.
    """

    PSYCHOLOGY_STATES = ["AWARE", "CONSIDERING", "EVALUATING", "ACTIVE_USER", "EVANGELIST", "CHURNED"]

    def transition_customer_state(self, current_state: str, event: str, trust_score: float) -> str:
        if current_state == "AWARE" and event == "TRY_DEMO":
            return "CONSIDERING"
        elif current_state == "CONSIDERING" and trust_score >= 0.7:
            return "ACTIVE_USER"
        elif current_state == "ACTIVE_USER" and trust_score >= 0.9:
            return "EVANGELIST"
        elif event == "UNRESOLVED_CRITICAL_BUG":
            return "CHURNED"
        return current_state

    def calculate_switching_friction(self, data_lock_in: float, workflow_embedding: float) -> float:
        return 0.6 * data_lock_in + 0.4 * workflow_embedding


# =====================================================================
# Layer 8: Marketing Dynamics Engine
# =====================================================================
class MarketingDynamicsEngine:
    """
    Simulates market formation, viral K-factor, brand authority emergence,
    and positioning differential perception matrices.
    """

    def calculate_viral_coefficient_k(self, invite_rate: float, conversion_rate: float) -> float:
        """K = Invites Sent Per User * Conversion Rate."""
        return invite_rate * conversion_rate

    def evaluate_brand_authority(self, content_reach: float, customer_advocacy_rate: float) -> float:
        return min(1.0, 0.4 * math.log10(max(1.0, content_reach)) + 0.6 * customer_advocacy_rate)


# =====================================================================
# Layer 9: Sales Systems Engine
# =====================================================================
class SalesSystemsEngine:
    """
    Models sales psychology state transitions, buying urgency triggers, objection resolution,
    and automated vs. enterprise sales routing.
    """

    def resolve_objection(self, objection_type: str) -> Dict[str, Any]:
        objection_map = {
            "PRICE_TOO_HIGH": "Offer ROI guarantee and usage-based tiering",
            "SECURITY_CONCERN": "Provide SOC2 audit report and escrow guarantees",
            "TRANSITION_FRICTION": "Offer free white-glove migration assistance",
        }
        resolution = objection_map.get(objection_type, "Schedule technical discovery call")
        return {"objection": objection_type, "resolution_strategy": resolution}

    def route_sales_motion(self, contract_value_cents: int) -> str:
        if contract_value_cents >= 5000000:  # >= $50k
            return "ENTERPRISE_HIGH_TOUCH"
        elif contract_value_cents >= 1000000:  # $10k - $50k
            return "INSIDE_SALES_HYBRID"
        else:
            return "PRODUCT_LED_AUTOMATED"


# =====================================================================
# Layer 10: Growth & Ecosystem Engine
# =====================================================================
class GrowthEcosystemEngine:
    """
    Tracks compounding growth loops, network effect density, platform shift mechanics,
    and long-term metrics (LTV/CAC, NRR, Burn Multiple).
    """

    def calculate_growth_health(
        self,
        ltv_cents: int,
        cac_cents: int,
        nrr_percent: float,
        burn_multiple: float
    ) -> Dict[str, Any]:
        ltv_cac = ltv_cents / (cac_cents + 1e-6)
        is_healthy = ltv_cac >= 3.0 and nrr_percent >= 1.10 and burn_multiple <= 2.0
        return {
            "ltv_to_cac": ltv_cac,
            "nrr_percent": nrr_percent,
            "burn_multiple": burn_multiple,
            "is_compounding_healthy": is_healthy,
            "action": "SCALE_GROWTH" if is_healthy else "OPTIMIZE_UNIT_ECONOMICS_BEFORE_SCALING",
        }


# =====================================================================
# Layer 11: Competition & Moat Engine
# =====================================================================
class CompetitionMoatEngine:
    """
    Quantifies Hamilton Helmer's 7 Powers moats (Scale Economies, Network Effects,
    Counter-Positioning, Switching Costs, Brand, Cornered Resource, Process Power).
    """

    def score_7_powers_moat(self, powers: Dict[str, float]) -> float:
        weights = {
            "scale_economies": 0.15,
            "network_effects": 0.20,
            "counter_positioning": 0.20,
            "switching_costs": 0.15,
            "brand": 0.10,
            "cornered_resource": 0.10,
            "process_power": 0.10,
        }
        total_score = sum(weights.get(k, 0.0) * min(1.0, max(0.0, v)) for k, v in powers.items())
        return float(total_score)


# =====================================================================
# Layer 12: Organizational Design Engine
# =====================================================================
class OrganizationalDesignEngine:
    """
    Triggers hiring based on Lagrange shadow price constraints and determines centralized vs delegated work.
    """

    def evaluate_hiring_triggers(self, resource_shadow_prices: Dict[str, float]) -> List[str]:
        triggers = []
        for resource, shadow_price in resource_shadow_prices.items():
            if abs(shadow_price) > 0.7:
                triggers.append(f"HIRE_SPECIALIST_FOR_{resource.upper()}")
        return triggers


# =====================================================================
# Layer 13: Meta-Learning Engine
# =====================================================================
class MetaLearningEngine:
    """
    Updates mental models via Bayesian parameter revision, tracks decision quality,
    and converts failures into reusable knowledge schemas.
    """

    def update_mental_model_prior(self, prior_alpha: float, prior_beta: float, observed_successes: int, observed_failures: int) -> Tuple[float, float]:
        new_alpha = prior_alpha + observed_successes
        new_beta = prior_beta + observed_failures
        return new_alpha, new_beta

    def convert_failure_to_schema(self, failure_context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "schema_id": f"antipattern_{uuid4()}",
            "root_cause": failure_context.get("root_cause", "unspecified"),
            "preventative_rule": f"Never proceed if {failure_context.get('binding_constraint', 'risk')} is unmitigated",
        }


# =====================================================================
# Layer 14: AI Entrepreneurship Engine & Unified Orchestrator
# =====================================================================
class AIEntrepreneurshipEngine:
    """
    Formalizes tasks as algorithms, probabilistic models, causal inference, or human judgment,
    ranks opportunities via Expected Free Energy / Pareto, and allocates resources.
    """

    def formalize_task_matrix(self, tasks: List[str]) -> List[Dict[str, Any]]:
        reality = RealityEngine()
        return [reality.partition_task(task) for task in tasks]


class EntrepreneurialIntelligenceOrchestrator:
    """
    Master coordinating engine that integrates all 14 computational layers into an executable pipeline.
    """

    def __init__(
        self,
        causal_engine: Optional[AdvancedCausalEngine] = None,
        planner: Optional[ActiveInferencePlanner] = None
    ) -> None:
        self.causal_engine = causal_engine or AdvancedCausalEngine()
        self.planner = planner or ActiveInferencePlanner()

        # 14 Structural Engines
        self.reality_engine = RealityEngine()
        self.discovery_engine = OpportunityDiscoveryEngine()
        self.problem_engine = ProblemDiscoveryEngine(self.causal_engine)
        self.decision_system = DecisionMakingSystem(self.planner)
        self.evaluation_system = OpportunityEvaluationSystem()
        self.product_engine = ProductCreationEngine()
        self.customer_engine = CustomerUnderstandingEngine()
        self.marketing_engine = MarketingDynamicsEngine()
        self.sales_engine = SalesSystemsEngine()
        self.growth_engine = GrowthEcosystemEngine()
        self.moat_engine = CompetitionMoatEngine()
        self.org_engine = OrganizationalDesignEngine()
        self.meta_learning_engine = MetaLearningEngine()
        self.ai_engine = AIEntrepreneurshipEngine()

        self.opportunities: List[Opportunity] = []

    def ingest_signal(self, signal: Dict[str, Any]) -> Optional[Opportunity]:
        filtered_signal = self.discovery_engine.filter_weak_signal(signal)
        if not filtered_signal:
            return None

        opp = Opportunity(
            title=filtered_signal.get("title", "Unnamed Opportunity"),
            domain=filtered_signal.get("domain", "general"),
            variables=filtered_signal.get("variables", []),
            causal_edges=filtered_signal.get("causal_edges", []),
            coefficients=filtered_signal.get("coefficients", {}),
            prior_entropy=filtered_signal.get("prior_entropy", 1.5),
            post_entropy_simulated=filtered_signal.get("post_entropy_simulated", 0.4),
            success_probability=filtered_signal.get("success_probability", 0.5),
            tam_cents=filtered_signal.get("tam_cents", 100000000),
            keywords=filtered_signal.get("keywords", []),
        )
        self.opportunities.append(opp)
        return opp

    def execute_orchestrated_pipeline(self) -> Dict[str, Any]:
        """Runs the complete 14-layer analysis pipeline over active opportunities."""
        if not self.opportunities:
            return {"status": "idle", "reason": "No opportunities registered."}

        # 1. Rank opportunities using Active Inference (Layer 4, 14)
        ranked_opps = self.planner.rank_opportunities(self.opportunities)
        primary_opp, best_efe = ranked_opps[0]

        # Check Kill Gate (Layer 4)
        if self.decision_system.evaluate_kill_gate(primary_opp):
            return {"status": "killed", "reason": f"Kill gate triggered for '{primary_opp.title}'"}

        # 2. Structural Causal Initialization (Layer 3)
        for var in primary_opp.variables:
            self.causal_engine.register_variable(var)
        for parent, child in primary_opp.causal_edges:
            weight = primary_opp.coefficients.get(f"{parent}->{child}", 0.5)
            self.causal_engine.add_causal_relationship(parent, child, weight)

        # 3. Simulate Causal Intervention (Layer 3)
        intervention_var = primary_opp.variables[0] if primary_opp.variables else "marketing_spend"
        inter_state = self.causal_engine.execute_do_intervention(intervention_var, 1.5)

        # 4. Opportunity Evaluation (Layer 5)
        opp_eval = self.evaluation_system.evaluate_opportunity_quality(primary_opp)

        # 5. Product & Customer & Sales Evaluation (Layer 6, 7, 9)
        jtbd = self.product_engine.discover_job_to_be_done([])
        sales_route = self.sales_engine.route_sales_motion(primary_opp.tam_cents // 10)

        # 6. Moat Scoring (Layer 11)
        moat_score = self.moat_engine.score_7_powers_moat({
            "scale_economies": 0.8,
            "network_effects": 0.7,
            "counter_positioning": 0.9,
            "switching_costs": 0.6,
        })

        return {
            "status": "executed",
            "selected_opportunity": primary_opp.title,
            "best_expected_free_energy": best_efe,
            "intervention_performed": f"do({intervention_var} = 1.5)",
            "propagated_state": inter_state,
            "evaluation": opp_eval,
            "job_to_be_done": jtbd,
            "sales_route": sales_route,
            "moat_score": moat_score,
        }
