"""
Executable implementation of the Complete 14-Layer Computational Architecture
of Entrepreneurship for SERO / AI EOS.

Formalizes all 14 layers from Reality Substrate to Autonomous AI Entrepreneurship Orchestration.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from datetime import datetime, timezone

logger = logging.getLogger("sero.fourteen_layer_engine")


# =====================================================================
# Layer 1: Reality Substrate & Fundamental Principles
# =====================================================================
class RealityMatrixEngine:
    """Evaluates fundamental economic entropy, invariant principles, and task automation boundaries."""

    def assess_invariant_principles(self, venture_state: Dict[str, Any]) -> Dict[str, Any]:
        downside_cents = venture_state.get("max_downside_cents", 1000000)
        upside_cents = venture_state.get("expected_upside_cents", 100000000)
        asymmetry_ratio = upside_cents / max(1, downside_cents)

        loop_latency_days = venture_state.get("experiment_cycle_days", 7.0)
        has_leverage = venture_state.get("has_code_or_media_leverage", True)
        bottleneck_identified = venture_state.get("bottleneck", "customer_acquisition") is not None

        is_aligned = asymmetry_ratio >= 5.0 and loop_latency_days <= 14.0 and has_leverage and bottleneck_identified
        return {
            "asymmetry_ratio": asymmetry_ratio,
            "experiment_latency_days": loop_latency_days,
            "has_leverage": has_leverage,
            "is_aligned_with_invariant_principles": is_aligned
        }

    def classify_automation_boundary(self, task_name: str, characteristics: Dict[str, Any]) -> str:
        """Classifies tasks across deterministic, probabilistic, causal, generative, or human judgment."""
        if characteristics.get("requires_existential_moral_alignment") or characteristics.get("sovereign_capital_authority"):
            return "human_judgment_required"
        if characteristics.get("is_creative_generation"):
            return "generative_creativity"
        if characteristics.get("requires_do_interventions"):
            return "causal_inference"
        if characteristics.get("is_stochastic_prediction"):
            return "probabilistic_reasoning"
        return "deterministic_algorithm"


# =====================================================================
# Layer 2: Opportunity Discovery Engine
# =====================================================================
class OpportunityDiscoveryEngine:
    """Senses weak signals, filters noise, and performs combinatorial state space search."""

    def sense_weak_signals(self, raw_signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered = []
        for signal in raw_signals:
            growth_acceleration = signal.get("acceleration", 0.0)
            noise_ratio = signal.get("noise_ratio", 0.5)

            # High second derivative with low noise ratio signifies a weak signal worth tracking
            if growth_acceleration >= 0.15 and noise_ratio <= 0.4:
                filtered.append(signal)
        return filtered

    def combinatorial_synthesis(self, domain_a: Dict[str, Any], domain_b: Dict[str, Any]) -> Dict[str, Any]:
        name_a = domain_a.get("name", "DomainA")
        name_b = domain_b.get("name", "DomainB")
        distance = abs(domain_a.get("taxonomy_id", 1) - domain_b.get("taxonomy_id", 10))
        feasibility = min(domain_a.get("feasibility", 0.8), domain_b.get("feasibility", 0.8))
        delta_value = (domain_a.get("market_cents", 1000) + domain_b.get("market_cents", 1000)) * distance

        novelty_score = distance * feasibility * delta_value
        return {
            "synthetic_opportunity": f"{name_a} x {name_b}",
            "novelty_score": novelty_score,
            "distance": distance,
            "feasibility": feasibility
        }

    def predict_trend_emergence(self, signal_series: List[float]) -> Dict[str, Any]:
        if len(signal_series) < 2:
            return {"is_emerging": False, "growth_rate": 0.0}

        first_derivative = signal_series[-1] - signal_series[-2]
        is_emerging = first_derivative > 0.1
        return {"is_emerging": is_emerging, "growth_rate": first_derivative}


# =====================================================================
# Layer 3: Problem Discovery & Decomposition Engine
# =====================================================================
class ProblemDecompositionEngine:
    """Decomposes stated problems into causal DAGs, isolates root causes, and computes JTBD friction."""

    def decompose_causal_dag(self, symptoms: List[str], causal_edges: List[Tuple[str, str]]) -> Dict[str, Any]:
        parent_counts: Dict[str, int] = {s: 0 for s in symptoms}
        for parent, child in causal_edges:
            if child in parent_counts:
                parent_counts[child] += 1
            if parent not in parent_counts:
                parent_counts[parent] = 0

        # Root causes are nodes with zero incoming causal parents
        root_causes = [node for node, count in parent_counts.items() if count == 0]
        return {
            "symptoms": symptoms,
            "causal_edges": causal_edges,
            "root_causes": root_causes,
            "is_decomposed": len(root_causes) > 0
        }

    def evaluate_jtbd_vector(self, functional: float, emotional: float, social: float, current_friction: float) -> Dict[str, Any]:
        jtbd_magnitude = math.sqrt(functional**2 + emotional**2 + social**2)
        residual_actionable_friction = max(0.0, current_friction - (jtbd_magnitude * 0.2))
        return {
            "jtbd_magnitude": jtbd_magnitude,
            "residual_actionable_friction": residual_actionable_friction,
            "is_actionable": residual_actionable_friction > 0.3
        }

    def should_ignore_problem(self, wtp_cents: int, cost_cents: int, frequency_per_year: int) -> bool:
        annual_value = wtp_cents * frequency_per_year
        return annual_value < cost_cents or frequency_per_year < 2


# =====================================================================
# Layer 4: Decision Making Engine
# =====================================================================
class DecisionEngine:
    """Calculates EVOI, manages intuition vs data gating, and enforces fast kill switches."""

    def compute_evoi(self, prior_uncertainty: float, experiment_cost_cents: int, potential_gain_cents: int) -> float:
        expected_gain = potential_gain_cents * prior_uncertainty
        evoi = expected_gain - experiment_cost_cents
        return float(evoi)

    def gate_data_vs_intuition(self, sample_size: int, market_novelty_score: float) -> str:
        if sample_size < 30 or market_novelty_score > 0.8:
            return "rely_on_intuition_priors"
        return "rely_on_data"

    def check_kill_switch(self, posterior_confidence: float, threshold: float = 0.20) -> bool:
        return posterior_confidence < threshold


# =====================================================================
# Layer 5: Opportunity Evaluation Engine
# =====================================================================
class OpportunityEvaluationEngine:
    """Computes multi-dimensional opportunity value equations and evaluates timing windows."""

    def calculate_opportunity_value(
        self,
        tam_cents: int,
        urgency: float,
        margin_percent: float,
        defensibility: float,
        risk: float,
        capital_intensity: float
    ) -> float:
        numerator = tam_cents * urgency * margin_percent * defensibility
        denominator = max(0.01, risk * capital_intensity)
        return float(numerator / denominator)

    def evaluate_timing_window(self, platform_shift: bool, cost_threshold_met: bool, regulatory_deadline: bool) -> str:
        triggers = sum([platform_shift, cost_threshold_met, regulatory_deadline])
        if triggers >= 2:
            return "open"
        if triggers == 1:
            return "closing_soon"
        return "premature"


# =====================================================================
# Layer 6: Product Creation & Complexity Engine
# =====================================================================
class ProductCreationEngine:
    """Prunes non-value features and optimizes learning velocity over premature polish."""

    def anti_bloat_feature_prune(self, features: List[Dict[str, Any]], complexity_threshold: float = 1.5) -> List[Dict[str, Any]]:
        approved = []
        for feature in features:
            delta_retention = feature.get("delta_retention", 0.05)
            delta_wtp = feature.get("delta_wtp", 0.05)
            complexity = max(0.1, feature.get("complexity_cost", 1.0))
            roi_ratio = (delta_retention + delta_wtp) / complexity

            if roi_ratio >= complexity_threshold:
                approved.append(feature)
        return approved

    def calculate_learning_velocity(self, experiments_run: int, uncertainty_reduced: float) -> float:
        return float(experiments_run * uncertainty_reduced)


# =====================================================================
# Layer 7: Customer Psychology & Switching Engine
# =====================================================================
class CustomerUnderstandingEngine:
    """Models push-pull-anxiety-habit switching mechanics and evangelism coefficients."""

    def calculate_switching_probability(self, push: float, pull: float, anxiety: float, habit: float) -> float:
        net_force = (push + pull) - (anxiety + habit)
        # Sigmoid activation function
        prob = 1.0 / (1.0 + math.exp(-net_force))
        return float(prob)

    def compute_evangelist_viral_coefficient(self, nps_surplus: float, referral_rate: float) -> float:
        return float(nps_surplus * referral_rate)


# =====================================================================
# Layer 8: Marketing & Attention Propagation Engine
# =====================================================================
class MarketingEngine:
    """Simulates SIR epidemiological attention diffusion and perceptual positioning distance."""

    def simulate_attention_diffusion(
        self,
        initial_aware: int,
        total_population: int,
        transmissibility: float,
        decay_rate: float,
        steps: int = 5
    ) -> List[int]:
        s = total_population - initial_aware
        i = initial_aware
        trajectory = [i]

        for _ in range(steps):
            new_infected = int(transmissibility * s * i / total_population)
            recovered = int(decay_rate * i)
            s = max(0, s - new_infected)
            i = max(0, i + new_infected - recovered)
            trajectory.append(i)

        return trajectory

    def evaluate_positioning_distance(
        self,
        our_vector: List[float],
        competitor_vectors: List[List[float]],
        customer_centroid: List[float]
    ) -> float:
        # Distance to customer centroid (smaller is better)
        dist_customer = math.sqrt(sum((a - b)**2 for a, b in zip(our_vector, customer_centroid)))
        # Distance to competitors (larger is better)
        if competitor_vectors:
            dist_comp = min(math.sqrt(sum((a - b)**2 for a, b in zip(our_vector, c))) for c in competitor_vectors)
        else:
            dist_comp = 1.0

        return float(dist_comp / max(0.1, dist_customer))


# =====================================================================
# Layer 9: Sales Urgency & Repeatable System Engine
# =====================================================================
class SalesEngine:
    """Computes cost-of-inaction urgency ratios and routes sales system complexity."""

    def calculate_urgency_ratio(self, cost_of_inaction_annual_cents: int, cost_of_change_one_time_cents: int) -> float:
        return float(cost_of_inaction_annual_cents / max(1, cost_of_change_one_time_cents))

    def route_sales_model(self, acv_cents: int) -> str:
        if acv_cents < 10000_00:  # < $10k
            return "automated_self_serve"
        elif acv_cents < 50000_00:  # $10k - $50k
            return "inside_sales"
        else:
            return "enterprise_solution_architecture"


# =====================================================================
# Layer 10: Compounding Growth & Network Effects Engine
# =====================================================================
class GrowthEngine:
    """Models network scale value scaling and intentional deceleration triggers."""

    def calculate_network_effect_value(self, user_base: int, network_type: str = "metcalfe") -> float:
        if network_type == "metcalfe":
            return float(user_base ** 2)
        elif network_type == "reed":
            return float(2 ** min(30, user_base))
        return float(user_base)

    def check_intentional_deceleration_trigger(self, churn_spike_rate: float, latency_p99_sec: float) -> bool:
        return churn_spike_rate > 0.15 or latency_p99_sec > 2.0


# =====================================================================
# Layer 11: Competitive Moat & Pivot Engine
# =====================================================================
class CompetitiveMoatEngine:
    """Quantifies structural moats and enforces mandatory pivot triggers."""

    def compute_moat_durability(
        self,
        network_density: float,
        switching_cost_cents: int,
        scale_economies: float,
        proprietary_ip: float
    ) -> float:
        s_net = min(1.0, network_density)
        s_switch = min(1.0, switching_cost_cents / 10000_00)
        s_scale = min(1.0, scale_economies)
        s_ip = min(1.0, proprietary_ip)

        score = 0.3 * s_net + 0.3 * s_switch + 0.2 * s_scale + 0.2 * s_ip
        return float(score)

    def check_pivot_mandate(self, ltv_cac_ratio: float, monthly_attrition: float) -> bool:
        return ltv_cac_ratio < 1.0 or monthly_attrition > 0.20


# =====================================================================
# Layer 12: Organizational Design Engine
# =====================================================================
class OrganizationalDesignEngine:
    """Determines centralization vs delegation split and monitors hiring triggers."""

    def centralization_vs_delegation_split(self, decision_type: str, strategic_impact_score: float) -> str:
        if strategic_impact_score > 0.75 or decision_type in ["capital_allocation", "core_vision"]:
            return "centralized_governance"
        return "delegated_agentic_execution"

    def compute_hiring_trigger(self, capacity_utilization: float, revenue_per_employee_cents: int) -> bool:
        return capacity_utilization > 0.85 and revenue_per_employee_cents >= 200000_00


# =====================================================================
# Layer 13: Meta-Learning & Knowledge Conversion Engine
# =====================================================================
class MetaLearningEngine:
    """Updates Bayesian mental models and converts failed executions into structured anti-patterns."""

    def bayesian_mental_model_update(
        self,
        prior_belief: float,
        experiment_evidence_positive: bool,
        likelihood_ratio: float = 2.0
    ) -> float:
        p = max(0.01, min(0.99, prior_belief))
        odds = p / (1.0 - p)

        if experiment_evidence_positive:
            updated_odds = odds * likelihood_ratio
        else:
            updated_odds = odds / likelihood_ratio

        posterior = updated_odds / (1.0 + updated_odds)
        return float(posterior)

    def convert_failure_to_antipattern(self, failed_action: str, error_context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "anti_pattern_id": str(uuid4()),
            "failed_action": failed_action,
            "root_cause": error_context.get("reason", "unknown_failure"),
            "mitigation_rule": f"Do not execute {failed_action} when {error_context.get('condition', 'default_risk')}",
            "created_at": datetime.now(timezone.utc).isoformat()
        }


# =====================================================================
# Layer 14: Autonomous AI Entrepreneurship Orchestrator
# =====================================================================
class FourteenLayerEntrepreneurshipOrchestrator:
    """
    Master orchestrator coupling all 13 sub-layer engines to execute an autonomous
    end-to-end entrepreneurial loop.
    """

    def __init__(self) -> None:
        self.layer1_reality = RealityMatrixEngine()
        self.layer2_discovery = OpportunityDiscoveryEngine()
        self.layer3_problem = ProblemDecompositionEngine()
        self.layer4_decision = DecisionEngine()
        self.layer5_evaluation = OpportunityEvaluationEngine()
        self.layer6_product = ProductCreationEngine()
        self.layer7_customer = CustomerUnderstandingEngine()
        self.layer8_marketing = MarketingEngine()
        self.layer9_sales = SalesEngine()
        self.layer10_growth = GrowthEngine()
        self.layer11_competition = CompetitiveMoatEngine()
        self.layer12_org = OrganizationalDesignEngine()
        self.layer13_meta = MetaLearningEngine()

    def orchestrate_complete_cycle(self, venture_input: Dict[str, Any]) -> Dict[str, Any]:
        """Runs an end-to-end evaluation across all 14 computational layers."""
        # Layer 1: Invariant Principles
        l1_result = self.layer1_reality.assess_invariant_principles(venture_input)

        # Layer 2: Weak Signal & Novelty Synthesis
        synthetic_opp = self.layer2_discovery.combinatorial_synthesis(
            {"name": venture_input.get("title", "CoreVenture"), "taxonomy_id": 1, "feasibility": 0.9, "market_cents": venture_input.get("tam_cents", 100000000)},
            {"name": "AI_Automation", "taxonomy_id": 10, "feasibility": 0.85, "market_cents": 500000000}
        )

        # Layer 3: Problem Decomposition
        l3_result = self.layer3_problem.evaluate_jtbd_vector(
            functional=0.8, emotional=0.6, social=0.4, current_friction=0.9
        )

        # Layer 4: Decision & EVOI
        evoi = self.layer4_decision.compute_evoi(prior_uncertainty=0.5, experiment_cost_cents=1000_00, potential_gain_cents=50000_00)

        # Layer 5: Opportunity Valuation
        opp_value = self.layer5_evaluation.calculate_opportunity_value(
            tam_cents=venture_input.get("tam_cents", 100000000),
            urgency=0.8,
            margin_percent=0.75,
            defensibility=0.8,
            risk=0.3,
            capital_intensity=0.2
        )

        # Layer 6: Anti-Bloat Feature Pruning
        pruned_features = self.layer6_product.anti_bloat_feature_prune([
            {"name": "Core Dashboard", "delta_retention": 0.2, "delta_wtp": 0.15, "complexity_cost": 0.1},
            {"name": "Vanity Widget", "delta_retention": 0.01, "delta_wtp": 0.0, "complexity_cost": 2.0}
        ])

        # Layer 7: Customer Switching Prob
        switch_prob = self.layer7_customer.calculate_switching_probability(push=0.7, pull=0.8, anxiety=0.2, habit=0.3)

        # Layer 8: Marketing Distance
        pos_dist = self.layer8_marketing.evaluate_positioning_distance(
            our_vector=[1.0, 2.0], competitor_vectors=[[0.0, 0.0]], customer_centroid=[1.1, 2.1]
        )

        # Layer 9: Sales Urgency & Routing
        urgency_ratio = self.layer9_sales.calculate_urgency_ratio(cost_of_inaction_annual_cents=120000_00, cost_of_change_one_time_cents=10000_00)
        sales_route = self.layer9_sales.route_sales_model(acv_cents=venture_input.get("acv_cents", 15000_00))

        # Layer 10: Compounding Network Value
        network_val = self.layer10_growth.calculate_network_effect_value(user_base=100, network_type="metcalfe")

        # Layer 11: Moat Score & Pivot Check
        moat_score = self.layer11_competition.compute_moat_durability(network_density=0.7, switching_cost_cents=5000_00, scale_economies=0.6, proprietary_ip=0.8)
        pivot_mandate = self.layer11_competition.check_pivot_mandate(ltv_cac_ratio=3.5, monthly_attrition=0.03)

        # Layer 12: Delegation Split
        delegation = self.layer12_org.centralization_vs_delegation_split(decision_type="feature_release", strategic_impact_score=0.3)

        # Layer 13: Meta-Learning Posterior
        posterior_belief = self.layer13_meta.bayesian_mental_model_update(prior_belief=0.5, experiment_evidence_positive=True)

        # Layer 14: Final Orchestration Synthesis
        return {
            "status": "success",
            "venture_title": venture_input.get("title", "SERO Venture"),
            "layer1_reality": l1_result,
            "layer2_combinatorial": synthetic_opp,
            "layer3_jtbd": l3_result,
            "layer4_evoi": evoi,
            "layer5_opportunity_value": opp_value,
            "layer6_features_approved": len(pruned_features),
            "layer7_switching_prob": switch_prob,
            "layer8_positioning_distance": pos_dist,
            "layer9_sales_route": sales_route,
            "layer10_network_value": network_val,
            "layer11_moat_score": moat_score,
            "layer11_pivot_mandate": pivot_mandate,
            "layer12_delegation": delegation,
            "layer13_posterior_belief": posterior_belief
        }
