"""
The complete, executable implementation of the Fourteen-Layer Computational Architecture
of Entrepreneurship for the Autonomous AI Entrepreneurial Operating System (AI-EOS).
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.fourteen_layer_engine")


# =====================================================================
# Data Models
# =====================================================================
class Signal(BaseModel):
    signal_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str = "general"
    raw_intensity: float = 0.5
    spectral_entropy: float = 0.8
    keywords: List[str] = Field(default_factory=list)


class OpportunityState(BaseModel):
    opportunity_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str = "general"
    tam_cents: int = 100_000_000  # Default $1M
    win_probability: float = 0.5
    margin_pct: float = 0.7
    prior_entropy: float = 1.5
    post_entropy_simulated: float = 0.4
    expected_utility: float = 0.8
    risk_factor: float = 0.2
    is_active: bool = True


class CustomerProfile(BaseModel):
    customer_id: UUID = Field(default_factory=uuid4)
    perceived_new_utility: float = 0.8
    current_utility: float = 0.4
    switching_friction: float = 0.2
    prediction_accuracy_history: List[float] = Field(default_factory=list)


# =====================================================================
# Layer 1: Reality Substrate & Invariants Engine
# =====================================================================
class Layer1RealitySubstrateEngine:
    """Formalizes fundamental entrepreneurial invariants and task boundary limits."""

    def evaluate_invariants(self, ltv_cac_ratio: float, customer_value_surplus: float) -> Dict[str, Any]:
        unit_economics_healthy = ltv_cac_ratio >= 3.0
        surplus_positive = customer_value_surplus > 0.0
        invariant_pass = unit_economics_healthy and surplus_positive

        return {
            "invariant_pass": invariant_pass,
            "ltv_cac_ratio": ltv_cac_ratio,
            "unit_economics_healthy": unit_economics_healthy,
            "customer_value_surplus": customer_value_surplus,
            "surplus_positive": surplus_positive,
        }

    def classify_task_automation(self, task_type: str) -> str:
        non_automatable = {"normative_value_judgment", "human_empathy", "legal_moral_accountability"}
        if task_type.lower() in non_automatable:
            return "HUMAN_ONLY"
        return "AUTOMATABLE_AI"


# =====================================================================
# Layer 2: Opportunity Discovery Engine
# =====================================================================
class Layer2OpportunityDiscoveryEngine:
    """Continuous search in world state space, weak signal detection, and signal filtering."""

    def detect_weak_signals(self, raw_signals: List[Signal]) -> List[Signal]:
        # Weak signals have spectral entropy between 0.6 and 0.95
        weak_signals = [s for s in raw_signals if 0.6 <= s.spectral_entropy <= 0.95]
        logger.info(f"Layer 2 detected {len(weak_signals)} weak signals out of {len(raw_signals)} total.")
        return weak_signals

    def filter_signals(self, signals: List[Signal], min_intensity: float = 0.3) -> List[Signal]:
        filtered = [s for s in signals if s.raw_intensity >= min_intensity]
        return filtered

    def generate_novelty_combinations(self, domain_a_features: List[str], domain_b_features: List[str]) -> List[str]:
        combinations = []
        for a in domain_a_features:
            for b in domain_b_features:
                combinations.append(f"{a}_X_{b}")
        return combinations


# =====================================================================
# Layer 3: Problem Discovery Engine
# =====================================================================
class Layer3ProblemDiscoveryEngine:
    """Problem definition, DAG decomposition, and root cause isolation."""

    def define_problem(self, current_state: Dict[str, float], target_state: Dict[str, float]) -> Dict[str, Any]:
        gap_magnitude = 0.0
        for k, v_target in target_state.items():
            v_curr = current_state.get(k, 0.0)
            gap_magnitude += abs(v_target - v_curr)

        return {
            "current_state": current_state,
            "target_state": target_state,
            "gap_magnitude": gap_magnitude,
            "is_valid_problem": gap_magnitude > 0.05
        }

    def decompose_problem_dag(self, problem_key: str) -> List[Dict[str, Any]]:
        # Decomposes problem into root drivers (depth 1) and downstream symptoms (depth 2)
        return [
            {"node": f"{problem_key}_root_driver", "depth": 1, "is_root_cause": True},
            {"node": f"{problem_key}_symptom_alpha", "depth": 2, "is_root_cause": False},
            {"node": f"{problem_key}_symptom_beta", "depth": 2, "is_root_cause": False},
        ]


# =====================================================================
# Layer 4: Decision Making Under Uncertainty Engine
# =====================================================================
class Layer4DecisionMakingEngine:
    """Active inference Expected Free Energy (EFE) decision making."""

    def compute_active_inference_efe(
        self,
        pragmatic_utility: float,
        epistemic_information_gain: float,
        curiosity_weight: float = 1.0
    ) -> float:
        """
        EFE G = - Pragmatic Utility - (Curiosity Weight * Epistemic Information Gain)
        Lower EFE indicates superior policy (minimizing variational surprise).
        """
        efe = -pragmatic_utility - (curiosity_weight * max(0.0, epistemic_information_gain))
        return efe

    def select_information_first_experiments(self, candidate_experiments: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Ranks candidate experiments by epistemic value per unit cost
        scored = []
        for exp in candidate_experiments:
            info_gain = exp.get("info_gain", 0.5)
            cost = max(1.0, exp.get("cost", 10.0))
            score = info_gain / cost
            scored.append((exp, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[0][0] if scored else {}


# =====================================================================
# Layer 5: Opportunity Evaluation Engine
# =====================================================================
class Layer5OpportunityEvaluationEngine:
    """Evaluates Expected Value (EV) and Real Options Analysis timing."""

    def calculate_opportunity_ev(
        self,
        tam_cents: int,
        win_probability: float,
        margin_pct: float,
        capital_at_risk_cents: int
    ) -> int:
        ev = int((win_probability * tam_cents * margin_pct) - ((1.0 - win_probability) * capital_at_risk_cents))
        return ev

    def evaluate_real_options_timing(self, uncertainty: float, option_cost_cents: int) -> str:
        if uncertainty > 0.6:
            return "DEFER_AND_STAGE_EXPERIMENT"
        elif uncertainty < 0.2:
            return "SCALE_PHYSICAL_LAUNCH"
        return "HOLD_PLATFORM_OPTION"


# =====================================================================
# Layer 6: Product Creation Engine
# =====================================================================
class Layer6ProductCreationEngine:
    """What-not-to-build filtering and Job-to-be-Done (JTBD) discovery."""

    def filter_what_not_to_build(
        self,
        candidate_features: List[Dict[str, Any]],
        max_complexity_budget: float = 10.0
    ) -> List[Dict[str, Any]]:
        accepted = []
        current_complexity = 0.0

        # Sort features by value to complexity ratio
        sorted_features = sorted(
            candidate_features,
            key=lambda f: f.get("value", 1.0) / max(0.1, f.get("complexity", 1.0)),
            reverse=True
        )

        for feature in sorted_features:
            comp = feature.get("complexity", 1.0)
            if current_complexity + comp <= max_complexity_budget:
                accepted.append(feature)
                current_complexity += comp

        return accepted

    def discover_jtbd(self, friction_signals: List[str]) -> str:
        if not friction_signals:
            return "GENERAL_EFFICIENCY"
        return f"AUTOMATE_AND_ELIMINATE_{friction_signals[0].upper()}"


# =====================================================================
# Layer 7: Customer Understanding Engine
# =====================================================================
class Layer7CustomerUnderstandingEngine:
    """Customer psychology modeling, trust scores, and switching mechanics."""

    def model_customer_switching(self, profile: CustomerProfile) -> Dict[str, Any]:
        net_switch_gain = profile.perceived_new_utility - profile.current_utility
        should_switch = net_switch_gain > profile.switching_friction
        return {
            "net_switch_gain": net_switch_gain,
            "switching_friction": profile.switching_friction,
            "should_switch": should_switch
        }

    def calculate_trust_score(self, accuracy_history: List[float]) -> float:
        if not accuracy_history:
            return 0.5
        return float(sum(accuracy_history) / len(accuracy_history))


# =====================================================================
# Layer 8: Marketing Dynamics Engine
# =====================================================================
class Layer8MarketingEngine:
    """Bass diffusion dynamics and Virality K-factor calculation."""

    def simulate_bass_diffusion(
        self,
        potential_market: int,
        p: float = 0.03,
        q: float = 0.38,
        steps: int = 5
    ) -> List[int]:
        adopted = [0]
        cumulative = 0

        for _ in range(1, steps):
            remaining = potential_market - cumulative
            new_adoptions = int((p + q * (cumulative / potential_market if potential_market > 0 else 0)) * remaining)
            cumulative += new_adoptions
            adopted.append(cumulative)

        return adopted

    def calculate_virality_k_factor(self, invites_per_user: float, conversion_rate: float) -> float:
        k_factor = invites_per_user * conversion_rate
        return float(k_factor)


# =====================================================================
# Layer 9: Sales Systems Engine
# =====================================================================
class Layer9SalesEngine:
    """Objection resolution decision trees and pipeline routing."""

    def resolve_objection_tree(self, objection_type: str) -> str:
        resolutions = {
            "price": "OFFER_ROI_GUARANTEE_OR_TIERED_TRIAL",
            "trust": "PROVIDE_SOC2_AND_CUSTOMER_CASE_STUDIES",
            "complexity": "PROVIDE_WHITE_GLOVE_ONBOARDING_MIGRATION",
        }
        return resolutions.get(objection_type.lower(), "PROVIDE_CUSTOM_DEMO")

    def route_sales_pipeline(self, deal_size_cents: int) -> str:
        if deal_size_cents >= 10000_00:  # $10k+
            return "CONSULTATIVE_ENTERPRISE_HUMAN_SALES"
        return "AUTOMATED_SELF_SERVE_PLG"


# =====================================================================
# Layer 10: Growth Systems Engine
# =====================================================================
class Layer10GrowthEngine:
    """Network effects value models and Net Revenue Retention (NRR)."""

    def calculate_network_effects_value(self, node_count: int, network_type: str = "metcalfe") -> float:
        if network_type == "metcalfe":
            return float(node_count ** 2)
        elif network_type == "reed":
            return float(2 ** min(node_count, 30))  # Cap exponent to avoid overflow
        return float(node_count)

    def predict_retention_nrr(self, initial_mrr: float, expansion_mrr: float, churn_mrr: float) -> float:
        if initial_mrr <= 0:
            return 100.0
        nrr = ((initial_mrr + expansion_mrr - churn_mrr) / initial_mrr) * 100.0
        return float(nrr)


# =====================================================================
# Layer 11: Competitive Moats Engine
# =====================================================================
class Layer11CompetitionEngine:
    """Moat durability scores and pivot triggers."""

    def compute_moat_durability(
        self,
        network_density: float,
        switching_costs_cents: int,
        brand_trust: float,
        scale_cost_advantage_pct: float
    ) -> float:
        s_network = min(1.0, network_density)
        s_switch = min(1.0, switching_costs_cents / 10000_00)
        s_brand = min(1.0, brand_trust)
        s_scale = min(1.0, scale_cost_advantage_pct)

        score = 0.3 * s_network + 0.2 * s_switch + 0.2 * s_brand + 0.3 * s_scale
        return float(score)

    def check_pivot_trigger(self, revenue_decay_pct: float, customer_attrition_pct: float) -> bool:
        return revenue_decay_pct > 0.15 and customer_attrition_pct > 0.20


# =====================================================================
# Layer 12: Organizational Design Engine
# =====================================================================
class Layer12OrganizationalDesignEngine:
    """Agent spawning triggers and task delegation boundaries."""

    def check_hiring_and_spawning_trigger(self, capacity_utilization: float, forecast_error_ratio: float) -> List[str]:
        actions = []
        if capacity_utilization > 0.85:
            actions.append("SPAWN_WORKER_AGENT_INSTANCE")
        if forecast_error_ratio > 0.15:
            actions.append("SPAWN_SPECIALIZED_PRICING_AGENT")
        if forecast_error_ratio > 0.30:
            actions.append("SPLIT_GENERALIST_INTO_PEER_REVIEW_TRIAD")
        return actions

    def delegate_task_execution(self, strategic_intent: str) -> Dict[str, Any]:
        return {
            "centralized_intent": strategic_intent,
            "delegated_execution_layer": "AEAN_MULTI_AGENT_WORKERS",
            "autonomy_level": "BOUNDED_EXECUTION"
        }


# =====================================================================
# Layer 13: Meta-Learning Engine
# =====================================================================
class Layer13MetaLearningEngine:
    """Brier score calibration and trajectory mental model updates."""

    def evaluate_brier_score(self, predicted_probs: List[float], actual_outcomes: List[int]) -> float:
        if not predicted_probs or len(predicted_probs) != len(actual_outcomes):
            return 0.25

        total_sq_error = sum((p - o) ** 2 for p, o in zip(predicted_probs, actual_outcomes))
        brier_score = total_sq_error / len(predicted_probs)
        return float(brier_score)

    def update_mental_models_from_trajectories(self, trajectory_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        success_count = sum(1 for t in trajectory_history if t.get("success", False))
        total = len(trajectory_history)
        win_rate = success_count / total if total > 0 else 0.5

        return {
            "processed_trajectories": total,
            "historical_win_rate": win_rate,
            "updated_prior_alpha": 10.0 + success_count,
            "updated_prior_beta": 10.0 + (total - success_count)
        }


# =====================================================================
# Layer 14: AI Entrepreneurship Engine
# =====================================================================
class Layer14AIEntrepreneurshipEngine:
    """Master orchestrator formalizing autonomous AI entrepreneurship."""

    def formalize_entrepreneurial_pipeline(self, opportunity: OpportunityState) -> Dict[str, Any]:
        return {
            "opportunity_title": opportunity.title,
            "tam_cents": opportunity.tam_cents,
            "status": "FORMALIZED_INTO_ACTIVE_INFERENCE_DAG"
        }


# =====================================================================
# Master Orchestrator: FourteenLayerEntrepreneurialEngine
# =====================================================================
class FourteenLayerEntrepreneurialEngine:
    """
    Unified 14-layer computational engine for autonomous AI entrepreneurship.
    Couples all 14 computational layers into an end-to-end active inference system.
    """

    def __init__(self) -> None:
        self.layer1 = Layer1RealitySubstrateEngine()
        self.layer2 = Layer2OpportunityDiscoveryEngine()
        self.layer3 = Layer3ProblemDiscoveryEngine()
        self.layer4 = Layer4DecisionMakingEngine()
        self.layer5 = Layer5OpportunityEvaluationEngine()
        self.layer6 = Layer6ProductCreationEngine()
        self.layer7 = Layer7CustomerUnderstandingEngine()
        self.layer8 = Layer8MarketingEngine()
        self.layer9 = Layer9SalesEngine()
        self.layer10 = Layer10GrowthEngine()
        self.layer11 = Layer11CompetitionEngine()
        self.layer12 = Layer12OrganizationalDesignEngine()
        self.layer13 = Layer13MetaLearningEngine()
        self.layer14 = Layer14AIEntrepreneurshipEngine()

    def execute_full_14_layer_pipeline(
        self,
        raw_signals: List[Signal],
        total_budget_cents: int = 1_000_000_00
    ) -> Dict[str, Any]:
        """Runs continuous execution pipeline across all 14 layers."""
        # Layer 1: Invariants check
        l1_res = self.layer1.evaluate_invariants(ltv_cac_ratio=3.5, customer_value_surplus=150.0)

        # Layer 2: Discovery
        weak_signals = self.layer2.detect_weak_signals(raw_signals)
        filtered = self.layer2.filter_signals(weak_signals if weak_signals else raw_signals, min_intensity=0.2)
        primary_signal = filtered[0] if filtered else Signal(title="Default Frontier Venture", domain="deeptech")

        # Layer 3: Problem
        l3_res = self.layer3.define_problem(
            current_state={"efficiency": 0.2},
            target_state={"efficiency": 0.9}
        )

        # Layer 4: Decision Making
        efe = self.layer4.compute_active_inference_efe(
            pragmatic_utility=0.8,
            epistemic_information_gain=0.6,
            curiosity_weight=1.2
        )

        # Layer 5: Evaluation
        ev = self.layer5.calculate_opportunity_ev(
            tam_cents=500_000_000,
            win_probability=0.6,
            margin_pct=0.8,
            capital_at_risk_cents=total_budget_cents // 10
        )

        # Layer 6: Product
        accepted_features = self.layer6.filter_what_not_to_build([
            {"name": "core_engine", "value": 5.0, "complexity": 2.0},
            {"name": "advanced_dashboard", "value": 2.0, "complexity": 4.0},
        ], max_complexity_budget=5.0)

        # Layer 7: Customer
        cust_profile = CustomerProfile(perceived_new_utility=0.9, current_utility=0.3, switching_friction=0.2)
        l7_res = self.layer7.model_customer_switching(cust_profile)

        # Layer 8: Marketing
        virality_k = self.layer8.calculate_virality_k_factor(invites_per_user=5.0, conversion_rate=0.25)

        # Layer 9: Sales
        sales_route = self.layer9.route_sales_pipeline(deal_size_cents=15000_00)

        # Layer 10: Growth
        predicted_nrr = self.layer10.predict_retention_nrr(initial_mrr=10000, expansion_mrr=3000, churn_mrr=500)

        # Layer 11: Moat
        moat_score = self.layer11.compute_moat_durability(
            network_density=0.8,
            switching_costs_cents=12000_00,
            brand_trust=0.85,
            scale_cost_advantage_pct=0.3
        )

        # Layer 12: Org Design
        org_actions = self.layer12.check_hiring_and_spawning_trigger(capacity_utilization=0.90, forecast_error_ratio=0.20)

        # Layer 13: Meta-Learning
        brier = self.layer13.evaluate_brier_score(predicted_probs=[0.8, 0.7, 0.9], actual_outcomes=[1, 1, 1])

        # Layer 14: Autonomous AI
        opp = OpportunityState(title=primary_signal.title, domain=primary_signal.domain)
        l14_res = self.layer14.formalize_entrepreneurial_pipeline(opp)

        return {
            "status": "SUCCESS",
            "primary_signal_title": primary_signal.title,
            "layer_1_invariants": l1_res,
            "layer_3_problem": l3_res,
            "layer_4_expected_free_energy": efe,
            "layer_5_expected_value_cents": ev,
            "layer_6_accepted_features_count": len(accepted_features),
            "layer_7_customer_should_switch": l7_res["should_switch"],
            "layer_8_virality_k_factor": virality_k,
            "layer_9_sales_route": sales_route,
            "layer_10_predicted_nrr_pct": predicted_nrr,
            "layer_11_moat_score": moat_score,
            "layer_12_org_actions": org_actions,
            "layer_13_brier_score": brier,
            "layer_14_formalization": l14_res,
        }
