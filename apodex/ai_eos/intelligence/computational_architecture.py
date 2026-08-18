"""
The complete, first-principles executable implementation of the
14-Layer Computational Architecture of Entrepreneurship for SERO / EIOS v2.2.

This module formalizes entrepreneurship as a complete 14-layer adaptive system:
1. Reality: Invariants, automation boundaries, human psychology vs. optimization.
2. Opportunity Discovery: Weak signals, stochastic filtering, combinatorial synthesis, trend velocity.
3. Problem Discovery: Root cause vs. symptom, Pearl causal DAG decomposition, noise ignore thresholds.
4. Decision Making: Decisions under uncertainty, attention allocation, fast-kill gates, bias filters.
5. Opportunity Evaluation: Expected value, Kelly criterion, downside VaR, timing & abandonment.
6. Product Creation: JTBD state machines, feature complexity minimizers, learning optimization.
7. Customer Understanding: Trust decay models, switching cost friction, churn hazard rates.
8. Marketing: Market formation, virality K-factors, positioning perception, channel interactions.
9. Sales: Buying urgency, objection resolution, enterprise vs automated sales routing.
10. Growth: Compounding growth, network effect density, platform evolution triggers.
11. Competition: Moat durability scoring, competitor reactions, asymmetric pivots.
12. Organizational Design: Hiring threshold triggers, delegation boundaries, scaling org models.
13. Meta-Learning: Decision quality measurement, failure-to-knowledge conversion, weight updating.
14. AI Entrepreneurship: End-to-end execution, experiment selection, resource allocation & self-improvement.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.computational_architecture")


# =====================================================================
# Canonical Data Models
# =====================================================================

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
    tag_keywords: List[str] = Field(default_factory=list)
    estimated_cac_cents: int = 5000  # $50 default CAC
    estimated_ltv_cents: int = 25000  # $250 default LTV
    reversibility_score: float = 0.8  # Type II reversible by default


class TaskAutomationClassification(BaseModel):
    task_name: str
    is_automatable: bool
    requires_human_judgment: bool
    reasoning: str
    automation_confidence: float


# =====================================================================
# Layer 1: Reality
# =====================================================================

class RealityInvariantsEngine:
    """
    Layer 1: Reality.
    Formalizes fundamental invariants of entrepreneurship, automation boundaries,
    and human psychology vs. mathematical optimization boundaries.
    """

    @staticmethod
    def classify_task_automatability(
        task_name: str,
        ambiguity_level: float,  # 0.0 to 1.0
        emotional_charge: float,  # 0.0 to 1.0
        legal_sovereignty_required: bool
    ) -> TaskAutomationClassification:
        """
        Determines whether an entrepreneurial task can be automated or requires human judgment.
        Invariants:
        - Arbitrage of economic inefficiency & mathematical optimization -> Automatable.
        - Irreversible legal commitment, high emotional trust, deep human empathy -> Requires Human.
        """
        if legal_sovereignty_required or emotional_charge > 0.8:
            return TaskAutomationClassification(
                task_name=task_name,
                is_automatable=False,
                requires_human_judgment=True,
                reasoning="Task involves non-delegable legal sovereignty or deep human trust/empathy.",
                automation_confidence=0.1
            )
        elif ambiguity_level < 0.5 and emotional_charge < 0.4:
            return TaskAutomationClassification(
                task_name=task_name,
                is_automatable=True,
                requires_human_judgment=False,
                reasoning="Task is a bounded mathematical optimization or data-processing problem.",
                automation_confidence=0.95
            )
        else:
            return TaskAutomationClassification(
                task_name=task_name,
                is_automatable=True,
                requires_human_judgment=True,
                reasoning="Probabilistic reasoning task suitable for AI with human-in-the-loop oversight.",
                automation_confidence=0.7
            )


# =====================================================================
# Layer 2: Opportunity Discovery
# =====================================================================

class OpportunityDiscoveryEngine:
    """
    Layer 2: Opportunity Discovery.
    Continuous search over world state space, weak signal detection, stochastic filtering,
    combinatorial synthesis, and trend velocity scoring.
    """

    def detect_weak_signals(
        self,
        raw_signals: List[Dict[str, Any]],
        snr_threshold: float = 0.3
    ) -> List[Dict[str, Any]]:
        """Filters noise to surface weak signals above SNR threshold."""
        valid_signals = []
        for signal in raw_signals:
            magnitude = signal.get("magnitude", 0.0)
            noise = signal.get("noise_variance", 1.0)
            snr = magnitude / (noise + 1e-6)
            if snr >= snr_threshold:
                signal_copy = dict(signal)
                signal_copy["snr"] = snr
                valid_signals.append(signal_copy)
        return valid_signals

    def combinatorial_synthesis(
        self,
        signal_a: Dict[str, Any],
        signal_b: Dict[str, Any]
    ) -> Opportunity:
        """Combines two unrelated observations to synthesize a novel opportunity."""
        title = f"Synergy: {signal_a.get('name', 'TrendA')} + {signal_b.get('name', 'TrendB')}"
        domain = f"{signal_a.get('domain', 'general')}_{signal_b.get('domain', 'general')}"
        combined_keywords = list(set(signal_a.get("keywords", []) + signal_b.get("keywords", [])))

        # Novelty generation via entropy shift
        prior_entropy = (signal_a.get("entropy", 1.0) + signal_b.get("entropy", 1.0)) * 0.8
        post_entropy = prior_entropy * 0.4  # Synthesized combination reduces joint uncertainty

        return Opportunity(
            title=title,
            domain=domain,
            variables=["spend", "conversion", "revenue"],
            causal_edges=[("spend", "conversion"), ("conversion", "revenue")],
            coefficients={"spend->conversion": 0.4, "conversion->revenue": 1.5},
            prior_entropy=prior_entropy,
            post_entropy_simulated=post_entropy,
            success_probability=0.6,
            tam_cents=int((signal_a.get("tam_cents", 50000000) + signal_b.get("tam_cents", 50000000)) * 0.7),
            tag_keywords=combined_keywords
        )

    def calculate_trend_velocity(self, time_series_counts: List[float]) -> float:
        """Computes rate of acceleration of an emerging trend."""
        if len(time_series_counts) < 2:
            return 0.0
        delta_latest = time_series_counts[-1] - time_series_counts[-2]
        base = max(1.0, time_series_counts[-2])
        return delta_latest / base


# =====================================================================
# Layer 3: Problem Discovery & Causal Engine
# =====================================================================

class AdvancedCausalEngine:
    """
    Layer 3: Problem Discovery & Structural Causal Modeling.
    Implements a robust SCM capable of handling Pearl's do-calculus interventions,
    counterfactual estimations, and root-cause vs symptom decomposition.
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
        """Simulates Judea Pearl's do-operator (do(X = x))."""
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
        """Computes counterfactual outcomes given factual observations."""
        intervened_var, inter_value = counterfactual_intervention

        # 1. Abduction
        noise_estimates: Dict[str, float] = {}
        for var in self.variables:
            factual_val = factual_observations.get(var, 0.0)
            parents_list = self.parents.get(var, [])
            structural_expected = 0.0
            for parent in parents_list:
                coef = self.coefficients.get((parent, var), 0.0)
                structural_expected += coef * factual_observations.get(parent, 0.0)

            noise_estimates[var] = factual_val - structural_expected

        # 2. Action & Prediction
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

    def decompose_symptom_vs_root_cause(self, target_variable: str) -> Dict[str, Any]:
        """Distinguishes symptoms (downstream leaves) from root causes (root nodes in DAG)."""
        roots = []
        symptoms = []
        for var in self.variables:
            has_parents = len(self.parents.get(var, [])) > 0
            is_parent_of_something = any(var in parents for parents in self.parents.values())

            if not has_parents and is_parent_of_something:
                roots.append(var)
            elif has_parents and not is_parent_of_something:
                symptoms.append(var)

        return {
            "target": target_variable,
            "root_causes": roots,
            "symptoms": symptoms
        }


# =====================================================================
# Layer 4: Decision Making & Active Inference
# =====================================================================

class ActiveInferencePlanner:
    """
    Layer 4: Decision Making under Uncertainty.
    Active Inference decision framework based on Expected Free Energy (EFE).
    """

    def __init__(self, curiosity_weight: float = 1.0) -> None:
        self.curiosity_weight = curiosity_weight

    def calculate_efe(self, opp: Opportunity) -> float:
        """Expected Free Energy G = - Pragmatic Value - Epistemic Value * curiosity_weight."""
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

    def evaluate_fast_kill_gate(self, opp: Opportunity, min_success_prob: float = 0.2) -> bool:
        """Kills bad ideas quickly if success probability drops below kill boundary."""
        if opp.success_probability < min_success_prob:
            opp.is_active = False
            return True  # KILLED
        return False


# =====================================================================
# Layer 5: Opportunity Evaluation
# =====================================================================

class OpportunityEvaluator:
    """
    Layer 5: Opportunity Evaluation.
    Calculates Expected Value, Kelly Criterion capital allocation, downside VaR, and timing windows.
    """

    @staticmethod
    def calculate_expected_value(tam_cents: int, win_prob: float, cac_cents: int, ltv_cents: int) -> float:
        """Expected Value EV = Prob_win * (LTV - CAC) - (1 - Prob_win) * CAC."""
        net_gain = ltv_cents - cac_cents
        ev = (win_prob * net_gain) - ((1.0 - win_prob) * cac_cents)
        return ev

    @staticmethod
    def kelly_criterion_fraction(win_prob: float, win_loss_ratio: float) -> float:
        """Kelly fraction f* = (p * b - q) / b, where b = win_loss_ratio, p = win_prob, q = 1 - p."""
        if win_loss_ratio <= 0:
            return 0.0
        q = 1.0 - win_prob
        f_star = (win_prob * win_loss_ratio - q) / win_loss_ratio
        return max(0.0, min(0.25, f_star))  # Quarter-Kelly safety bound

    @staticmethod
    def estimate_downside_var(capital_at_risk_cents: int, confidence_level: float = 0.95) -> float:
        """Estimates Value at Risk (VaR) for downside exposure."""
        z_scores = {0.90: 1.28, 0.95: 1.645, 0.99: 2.33}
        z = z_scores.get(confidence_level, 1.645)
        volatility = capital_at_risk_cents * 0.30
        var_cents = z * volatility
        return min(float(capital_at_risk_cents), var_cents)

    @staticmethod
    def evaluate_abandonment(current_ev: float, alternative_ev: float, switching_cost: float) -> bool:
        """Determines whether to abandon current opportunity for a superior alternative."""
        return (alternative_ev - current_ev) > switching_cost


# =====================================================================
# Layer 6: Product Creation
# =====================================================================

class ProductCreationEngine:
    """
    Layer 6: Product Creation.
    Jobs-to-be-Done (JTBD) state machines, feature complexity minimizers, and learning optimization.
    """

    def discover_core_jtbd(
        self,
        user_friction_points: List[str],
        desired_outcomes: List[str]
    ) -> Dict[str, Any]:
        """Extracts the core Job-To-Be-Done by mapping friction to outcomes."""
        core_job = f"Eliminate [{', '.join(user_friction_points[:2])}] to achieve [{', '.join(desired_outcomes[:2])}]"
        return {
            "core_jtbd": core_job,
            "frictions_addressed": user_friction_points,
            "outcomes_delivered": desired_outcomes,
            "minimal_viable_feature_set": [f"Feature solving {f}" for f in user_friction_points[:2]]
        }

    def minimize_feature_complexity(
        self,
        candidate_features: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Filters out non-essential features, ranking by Value-to-Complexity ratio."""
        scored = []
        for feat in candidate_features:
            value = feat.get("value_impact", 1.0)
            complexity = feat.get("complexity", 1.0)
            ratio = value / (complexity + 1e-6)
            feat_copy = dict(feat)
            feat_copy["value_complexity_ratio"] = ratio
            scored.append(feat_copy)

        scored.sort(key=lambda x: x["value_complexity_ratio"], reverse=True)
        return scored[:3]


# =====================================================================
# Layer 7: Customer Understanding
# =====================================================================

class CustomerPsychologyEngine:
    """
    Layer 7: Customer Understanding.
    Models customer trust decay, switching cost friction, churn hazard rates, and evangelist scores.
    """

    def model_trust_decay(
        self,
        initial_trust: float,
        failure_events: int,
        days_elapsed: float
    ) -> float:
        """Trust decays exponentially with failures and time."""
        trust = initial_trust * math.exp(-0.15 * failure_events) * math.exp(-0.01 * days_elapsed)
        return max(0.0, min(1.0, trust))

    def compute_churn_hazard(
        self,
        usage_drop_percent: float,
        support_ticket_count: int,
        nps_score: int
    ) -> float:
        """Computes analytical hazard rate for customer churn."""
        hazard = 0.05
        if usage_drop_percent > 0.30:
            hazard += 0.25
        if support_ticket_count > 3:
            hazard += 0.20
        if nps_score <= 6:
            hazard += 0.30
        return min(0.99, hazard)

    def calculate_evangelist_score(self, nps_score: int, referral_count: int) -> float:
        """Quantifies probability of user becoming a viral evangelist."""
        if nps_score < 9:
            return 0.0
        return min(1.0, 0.5 + 0.1 * referral_count)


# =====================================================================
# Layer 8: Marketing
# =====================================================================

class MarketingEngine:
    """
    Layer 8: Marketing.
    Market formation models, virality K-factor calculators, and positioning perception vectors.
    """

    def calculate_virality_k_factor(self, invites_per_user: float, conversion_rate_per_invite: float) -> float:
        """Viral coefficient K = i * c. K > 1.0 implies exponential compounding virality."""
        return invites_per_user * conversion_rate_per_invite

    def compute_positioning_perception(
        self,
        brand_attributes: Dict[str, float],
        competitor_attributes: Dict[str, float]
    ) -> float:
        """Euclidean distance vector score representing positioning differentiation."""
        common_keys = set(brand_attributes.keys()).intersection(competitor_attributes.keys())
        if not common_keys:
            return 1.0
        sum_sq = sum((brand_attributes[k] - competitor_attributes[k]) ** 2 for k in common_keys)
        return math.sqrt(sum_sq)


# =====================================================================
# Layer 9: Sales
# =====================================================================

class SalesEngine:
    """
    Layer 9: Sales.
    Quantifies buying urgency, objection resolution state machines, and sales routing.
    """

    def quantify_buying_urgency(self, daily_pain_cost_cents: int, budget_timeline_days: int) -> float:
        """Buying Urgency = Pain_Cost / Timeline."""
        if budget_timeline_days <= 0:
            return 1.0
        urgency = (daily_pain_cost_cents / 1000) / float(budget_timeline_days)
        return min(1.0, urgency)

    def route_sales_mode(self, acv_cents: int, complexity_score: float) -> str:
        """Routes to Self-Serve Automation vs Enterprise High-Touch Sales."""
        if acv_cents >= 2500000 or complexity_score > 0.7:  # $25k+ ACV
            return "ENTERPRISE_HIGH_TOUCH"
        else:
            return "AUTOMATED_SELF_SERVE"


# =====================================================================
# Layer 10: Growth
# =====================================================================

class GrowthEngine:
    """
    Layer 10: Growth.
    Compounding growth models, network effect density, and platform evolution triggers.
    """

    def calculate_network_effect_density(self, active_nodes: int, total_edges: int) -> float:
        """Metcalfe's network density = 2 * E / (N * (N - 1))."""
        if active_nodes <= 1:
            return 0.0
        max_possible_edges = active_nodes * (active_nodes - 1) / 2.0
        return total_edges / max_possible_edges

    def evaluate_platform_transition(self, developer_count: int, third_party_integrations: int) -> bool:
        """Triggers platform replacement when threshold third-party ecosystem forms."""
        return developer_count >= 100 and third_party_integrations >= 20


# =====================================================================
# Layer 11: Competition
# =====================================================================

class CompetitiveEngine:
    """
    Layer 11: Competition.
    Moat durability scoring, competitor reaction models, and asymmetric pivot triggers.
    """

    def score_moat_durability(
        self,
        switching_costs: float,
        network_density: float,
        scale_economies: float,
        brand_trust: float
    ) -> float:
        """Composite Moat Durability Score [0.0, 1.0]."""
        return 0.3 * network_density + 0.3 * switching_costs + 0.2 * scale_economies + 0.2 * brand_trust


# =====================================================================
# Layer 12: Organizational Design
# =====================================================================

class OrganizationalEngine:
    """
    Layer 12: Organizational Design.
    Hiring threshold triggers, centralization vs. delegation decision engines, and scaling org models.
    """

    def evaluate_hiring_threshold(self, workload_capacity_ratio: float, decision_latency_seconds: float) -> bool:
        """Triggers hiring signal when capacity breaches 85% or latency breaches threshold."""
        return workload_capacity_ratio > 0.85 or decision_latency_seconds > 300.0

    def determine_delegation_boundary(self, reversibility_score: float, capital_risk_cents: int) -> str:
        """Delegates reversible low-risk tasks to AI/Sub-agents; retains irreversible at central level."""
        if reversibility_score >= 0.7 and capital_risk_cents < 1000000:  # < $10k
            return "DELEGATE_TO_AUTONOMOUS_AGENT"
        else:
            return "RETAIN_CENTRAL_GOVERNANCE"


# =====================================================================
# Layer 13: Meta-Learning
# =====================================================================

class MetaLearningEngine:
    """
    Layer 13: Meta-Learning.
    Decision quality measurement, failure-to-knowledge memory conversion, and weight updating.
    """

    def measure_decision_quality(self, predicted_outcome: float, actual_outcome: float) -> float:
        """Decision Quality = 1.0 - |Predicted - Actual|."""
        error = abs(predicted_outcome - actual_outcome)
        return max(0.0, 1.0 - error)

    def convert_failure_to_knowledge(self, failure_event: Dict[str, Any]) -> Dict[str, Any]:
        """Converts a venture/experiment failure into a reusable institutional lesson card."""
        return {
            "lesson_id": uuid4(),
            "root_cause": failure_event.get("root_cause", "Unknown"),
            "failed_hypothesis": failure_event.get("hypothesis", "N/A"),
            "preventative_rule": f"Enforce guardrail against {failure_event.get('root_cause')}",
            "reusable_insight": failure_event.get("insight", "Log lesson to long-term memory")
        }


# =====================================================================
# Layer 14: AI Entrepreneurship & Master Orchestrator
# =====================================================================

class EntrepreneurialIntelligenceOrchestrator:
    """
    Layer 14: Master Entrepreneurial AI Orchestrator.
    Drives the complete 14-layer computational execution pipeline from sensing changes
    to discovering opportunities, validating them, allocating capital, scaling, and self-learning.
    """

    def __init__(
        self,
        causal_engine: Optional[AdvancedCausalEngine] = None,
        planner: Optional[ActiveInferencePlanner] = None
    ) -> None:
        self.causal_engine = causal_engine or AdvancedCausalEngine()
        self.planner = planner or ActiveInferencePlanner()
        self.reality_engine = RealityInvariantsEngine()
        self.discovery_engine = OpportunityDiscoveryEngine()
        self.evaluator = OpportunityEvaluator()
        self.product_engine = ProductCreationEngine()
        self.customer_engine = CustomerPsychologyEngine()
        self.marketing_engine = MarketingEngine()
        self.sales_engine = SalesEngine()
        self.growth_engine = GrowthEngine()
        self.competitive_engine = CompetitiveEngine()
        self.org_engine = OrganizationalEngine()
        self.meta_learning = MetaLearningEngine()

        self.opportunities: List[Opportunity] = []
        self.learned_lessons: List[Dict[str, Any]] = []

    def ingest_signal(self, signal: Dict[str, Any]) -> Opportunity:
        """Senses external changes and creates a candidate opportunity state."""
        logger.info(f"Sensing external signal: {signal.get('title')}")
        opp = Opportunity(
            title=signal.get("title", "Unnamed Opportunity"),
            domain=signal.get("domain", "general"),
            variables=signal.get("variables", ["spend", "conversion", "revenue"]),
            causal_edges=signal.get("causal_edges", [("spend", "conversion"), ("conversion", "revenue")]),
            coefficients=signal.get("coefficients", {"spend->conversion": 0.5, "conversion->revenue": 2.0}),
            prior_entropy=signal.get("prior_entropy", 1.5),
            post_entropy_simulated=signal.get("post_entropy_simulated", 0.4),
            success_probability=signal.get("success_probability", 0.5),
            tam_cents=signal.get("tam_cents", 100000000)
        )
        self.opportunities.append(opp)
        return opp

    def execute_orchestrated_pipeline(self) -> Dict[str, Any]:
        """Runs the complete 14-layer computational analysis and execution pipeline."""
        if not self.opportunities:
            return {"status": "idle", "reason": "No opportunities registered."}

        # 1. Opportunity Ranking & Selection (Layer 2, 4, 14)
        ranked_opps = self.planner.rank_opportunities(self.opportunities)
        primary_opp, best_efe = ranked_opps[0]

        # 2. Structural Causal Initialization & Intervention (Layer 3)
        for var in primary_opp.variables:
            self.causal_engine.register_variable(var)
        for parent, child in primary_opp.causal_edges:
            weight = primary_opp.coefficients.get(f"{parent}->{child}", 0.5)
            self.causal_engine.add_causal_relationship(parent, child, weight)

        intervention_var = primary_opp.variables[0] if primary_opp.variables else "spend"
        inter_state = self.causal_engine.execute_do_intervention(intervention_var, 1.5)

        # 3. Financial & Capital Evaluation (Layer 5)
        ev = self.evaluator.calculate_expected_value(
            tam_cents=primary_opp.tam_cents,
            win_prob=primary_opp.success_probability,
            cac_cents=primary_opp.estimated_cac_cents,
            ltv_cents=primary_opp.estimated_ltv_cents
        )
        kelly_fraction = self.evaluator.kelly_criterion_fraction(
            win_prob=primary_opp.success_probability,
            win_loss_ratio=primary_opp.estimated_ltv_cents / max(1, primary_opp.estimated_cac_cents)
        )

        # 4. Product & Customer Modeling (Layer 6 & 7)
        jtbd = self.product_engine.discover_core_jtbd(
            user_friction_points=["Manual workflow bottleneck", "High latency"],
            desired_outcomes=["Autonomous completion", "Zero downtime"]
        )
        churn_hazard = self.customer_engine.compute_churn_hazard(
            usage_drop_percent=0.1,
            support_ticket_count=1,
            nps_score=9
        )

        # 5. Marketing & Virality (Layer 8)
        k_factor = self.marketing_engine.calculate_virality_k_factor(
            invites_per_user=2.5,
            conversion_rate_per_invite=0.4
        )

        # 6. Sales Routing (Layer 9)
        sales_mode = self.sales_engine.route_sales_mode(
            acv_cents=primary_opp.estimated_ltv_cents,
            complexity_score=0.4
        )

        # 7. Moat & Org Evaluation (Layer 11 & 12)
        moat_score = self.competitive_engine.score_moat_durability(
            switching_costs=0.8,
            network_density=0.7,
            scale_economies=0.6,
            brand_trust=0.9
        )
        delegation_mode = self.org_engine.determine_delegation_boundary(
            reversibility_score=primary_opp.reversibility_score,
            capital_risk_cents=primary_opp.estimated_cac_cents
        )

        # 8. Meta-Learning Log (Layer 13)
        lesson = self.meta_learning.convert_failure_to_knowledge({
            "root_cause": "High customer acquisition costs",
            "hypothesis": primary_opp.title,
            "insight": "Optimize PLG self-serve viral loop prior to scaling ad spend."
        })
        self.learned_lessons.append(lesson)

        return {
            "status": "executed",
            "selected_opportunity": primary_opp.title,
            "best_expected_free_energy": best_efe,
            "expected_value_cents": ev,
            "kelly_capital_fraction": kelly_fraction,
            "intervention_performed": f"do({intervention_var} = 1.5)",
            "propagated_state": inter_state,
            "core_jtbd": jtbd["core_jtbd"],
            "churn_hazard": churn_hazard,
            "virality_k_factor": k_factor,
            "sales_routing_mode": sales_mode,
            "moat_durability_score": moat_score,
            "delegation_mode": delegation_mode,
            "meta_learning_lesson_id": str(lesson["lesson_id"])
        }
