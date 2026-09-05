"""
The Complete 14-Layer Computational Architecture of Entrepreneurship for SERO / AI EOS.

Implements explicit computational engines for every layer of entrepreneurship:
  Layer 1: Reality Substrate
  Layer 2: Opportunity Discovery
  Layer 3: Problem Discovery
  Layer 4: Decision Making Under Uncertainty
  Layer 5: Opportunity Evaluation
  Layer 6: Product Creation
  Layer 7: Customer Understanding
  Layer 8: Marketing & Brand Dynamics
  Layer 9: Sales Systems
  Layer 10: Growth & Scaling
  Layer 11: Competition & Moats
  Layer 12: Organizational Design
  Layer 13: Meta-Learning
  Layer 14: AI Entrepreneur Orchestrator
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.ai_eos.fourteen_layer_engine")


# =====================================================================
# Layer 1: Reality Substrate
# =====================================================================
class RealitySubstrateEngine:
    """Layer 1: Analyzes thermodynamic substrate, automation boundaries, and invariant principles."""

    def classify_automation_boundary(self, task_name: str, characteristics: Dict[str, Any]) -> Dict[str, Any]:
        """Classifies tasks into human psychology vs optimization algorithm vs hybrid."""
        requires_empathy = characteristics.get("requires_empathy", False)
        is_terminal_goal = characteristics.get("is_terminal_goal", False)
        is_convex_optimization = characteristics.get("is_convex_optimization", True)

        if requires_empathy or is_terminal_goal:
            category = "HUMAN_JUDGMENT_REQUIRED"
            can_automate = False
        elif is_convex_optimization:
            category = "FULLY_AUTOMATABLE_OPTIMIZATION"
            can_automate = True
        else:
            category = "HYBRID_PROBABILISTIC_AI"
            can_automate = True

        return {
            "task_name": task_name,
            "category": category,
            "can_automate": can_automate
        }

    def evaluate_invariant_principles(self, venture_state: Dict[str, Any]) -> Dict[str, bool]:
        """Evaluates whether core invariant principles are satisfied."""
        downside = venture_state.get("max_downside_cents", 100)
        upside = venture_state.get("max_upside_cents", 1000)
        has_asymmetric_payoff = (upside / max(1, downside)) >= 5.0
        actively_minimizing_free_energy = venture_state.get("prediction_error", 1.0) < 0.5
        executing_interventions = venture_state.get("active_experiments_count", 0) > 0

        return {
            "asymmetric_risk_reward": has_asymmetric_payoff,
            "variational_free_energy_minimization": actively_minimizing_free_energy,
            "causal_agency": executing_interventions
        }


# =====================================================================
# Layer 2: Opportunity Discovery
# =====================================================================
class OpportunityDiscoveryEngine:
    """Layer 2: Continuous search of world state space, weak signals, and recombination."""

    def detect_weak_signals(self, spectral_amplitudes: List[float], anomaly_threshold: float = 1.5) -> List[int]:
        """Identifies spectral density anomalies (weak market signals)."""
        if not spectral_amplitudes:
            return []
        mean_amp = sum(spectral_amplitudes) / len(spectral_amplitudes)
        variance = sum((x - mean_amp) ** 2 for x in spectral_amplitudes) / len(spectral_amplitudes)
        std_dev = math.sqrt(variance) if variance > 0 else 1.0

        anomaly_indices = []
        for i, amp in enumerate(spectral_amplitudes):
            z_score = (amp - mean_amp) / std_dev
            if z_score >= anomaly_threshold:
                anomaly_indices.append(i)
        return anomaly_indices

    def recombine_unrelated_observations(self, domain_a_concepts: List[str], domain_b_concepts: List[str]) -> List[str]:
        """Generates novel concept recombinations across independent domains."""
        recombinations = []
        for a in domain_a_concepts:
            for b in domain_b_concepts:
                recombinations.append(f"Hybrid({a} + {b})")
        return recombinations


# =====================================================================
# Layer 3: Problem Discovery
# =====================================================================
class ProblemDiscoveryEngine:
    """Layer 3: Distinguishes stated vs real problems, root cause analysis, and decomposition."""

    def decompose_problem_dag(self, stated_problem: str, causal_links: List[Tuple[str, str]]) -> Dict[str, Any]:
        """Decomposes stated problem into root causes and symptoms using causal graph analysis."""
        children = set()
        parents = set()
        for parent, child in causal_links:
            parents.add(parent)
            children.add(child)

        root_causes = list(parents - children)
        symptoms = list(children)

        return {
            "stated_problem": stated_problem,
            "root_causes": root_causes if root_causes else [stated_problem],
            "symptoms": symptoms,
            "is_stated_same_as_real": (stated_problem in root_causes)
        }


# =====================================================================
# Layer 4: Decision Making
# =====================================================================
class DecisionMakingEngine:
    """Layer 4: Decision making under uncertainty, intuition/data blending, fast-kill."""

    def calculate_expected_free_energy(self, prior_entropy: float, post_entropy: float, success_prob: float) -> float:
        """Computes Expected Free Energy (G = -Pragmatic - Epistemic)."""
        p_success = max(1e-6, min(1.0 - 1e-6, success_prob))
        pragmatic_value = math.log(p_success)
        epistemic_value = max(0.0, prior_entropy - post_entropy)
        return -pragmatic_value - epistemic_value

    def blend_intuition_and_data(self, intuition_prior: float, data_likelihood: float, sample_size: int) -> float:
        """Bayesian dynamic weighting between founder intuition prior and observed data."""
        # Weight of data increases with sample size (n / (n + 10))
        data_weight = sample_size / (sample_size + 10.0)
        prior_weight = 1.0 - data_weight
        return (prior_weight * intuition_prior) + (data_weight * data_likelihood)

    def fast_kill_check(self, posterior_belief: float, kill_threshold: float = 0.20) -> bool:
        """Determines if a hypothesis should be killed immediately."""
        return posterior_belief < kill_threshold


# =====================================================================
# Layer 5: Opportunity Evaluation
# =====================================================================
class OpportunityEvaluationEngine:
    """Layer 5: Expected value, downside CVaR risk, timing evaluation, and pivot triggers."""

    def calculate_expected_value(self, tam_cents: int, win_rate: float, margin: float, exp_cost_cents: int) -> float:
        """Calculates expected financial value of an opportunity."""
        expected_revenue = tam_cents * win_rate * margin
        return expected_revenue - exp_cost_cents

    def calculate_cvar_downside(self, scenarios: List[float], alpha: float = 0.05) -> float:
        """Calculates Conditional Value at Risk (CVaR) at alpha quantile."""
        if not scenarios:
            return 0.0
        sorted_scenarios = sorted(scenarios)
        cutoff_index = max(1, int(len(sorted_scenarios) * alpha))
        tail = sorted_scenarios[:cutoff_index]
        return sum(tail) / len(tail)

    def evaluate_pivot_trigger(self, current_efe: float, alternative_efe: float, switching_cost: float) -> bool:
        """Evaluates whether to pivot from current opportunity to an alternative."""
        # Pivot if alternative EFE plus switching cost is superior (more negative)
        return (alternative_efe + switching_cost) < current_efe


# =====================================================================
# Layer 6: Product Creation
# =====================================================================
class ProductCreationEngine:
    """Layer 6: Job-To-Be-Done (JTBD) core abstraction, complexity budget enforcement."""

    def extract_core_jtbd(self, customer_narrative: str) -> Dict[str, str]:
        """Extracts functional, emotional, and social jobs to be done."""
        return {
            "functional_job": f"Automate task in '{customer_narrative[:30]}...'",
            "emotional_job": "Eliminate anxiety around execution errors",
            "social_job": "Demonstrate technical excellence to stakeholders"
        }

    def prune_feature_complexity(self, features: List[Dict[str, Any]], complexity_budget: float) -> List[Dict[str, Any]]:
        """Prunes low-utility features exceeding complexity budget."""
        sorted_features = sorted(features, key=lambda f: f.get("utility_per_complexity", 0.0), reverse=True)
        pruned = []
        current_complexity = 0.0
        for feat in sorted_features:
            comp = feat.get("complexity", 1.0)
            if current_complexity + comp <= complexity_budget:
                pruned.append(feat)
                current_complexity += comp
        return pruned


# =====================================================================
# Layer 7: Customer Understanding
# =====================================================================
class CustomerUnderstandingEngine:
    """Layer 7: Customer psychology, trust dynamics, switching friction, and churn."""

    def calculate_switching_probability(self, u_new: float, u_old: float, switching_friction: float) -> float:
        """Models customer switching probability using logistic choice model."""
        net_delta = (u_new - u_old) - switching_friction
        # Logistic sigmoid transition
        prob = 1.0 / (1.0 + math.exp(-net_delta))
        return prob

    def update_trust_score(self, current_trust: float, promised_utility: float, delivered_utility: float) -> float:
        """Updates customer trust based on forecast error between promised and delivered utility."""
        forecast_error = abs(promised_utility - delivered_utility)
        if forecast_error <= 0.1:
            trust_delta = 0.05
        else:
            trust_delta = -0.10 * forecast_error
        return max(0.0, min(1.0, current_trust + trust_delta))


# =====================================================================
# Layer 8: Marketing & Brand Dynamics
# =====================================================================
class MarketingEngine:
    """Layer 8: Market formation, viral epidemic attention spread (SIR), positioning vector."""

    def calculate_viral_r0(self, transmission_rate: float, active_retention_days: float) -> float:
        """Calculates basic viral reproduction number R0 = beta * tau."""
        return transmission_rate * active_retention_days

    def compute_positioning_distance(self, brand_vector: List[float], competitor_vectors: List[List[float]]) -> float:
        """Calculates mean Euclidean positioning distance from incumbent competitors."""
        if not competitor_vectors:
            return 1.0
        distances = []
        for comp in competitor_vectors:
            dist = math.sqrt(sum((b - c) ** 2 for b, c in zip(brand_vector, comp)))
            distances.append(dist)
        return sum(distances) / len(distances)


# =====================================================================
# Layer 9: Sales Systems
# =====================================================================
class SalesEngine:
    """Layer 9: Sales psychology, objection resolution, urgency index, automation vs enterprise."""

    def resolve_objection(self, objection: str) -> str:
        """Maps customer objections to causal risk mitigation strategies."""
        objection_map = {
            "TOO_EXPENSIVE": "Demonstrate ROI payback < 90 days with guaranteed performance SLA.",
            "SECURITY_RISK": "Provide SOC2 Type II compliance evidence and isolated deployment sandbox.",
            "INTEGRATION_FRICTION": "Deliver zero-code adapter hooks and turn-key integration API."
        }
        return objection_map.get(objection, "Schedule technical discovery session to clarify requirements.")

    def calculate_buying_urgency_index(self, cost_of_inaction_cents: int, implementation_friction: float) -> float:
        """Calculates buying urgency index."""
        friction = max(0.1, implementation_friction)
        urgency = (cost_of_inaction_cents / 100000.0) / friction
        return min(1.0, urgency)


# =====================================================================
# Layer 10: Growth & Scaling
# =====================================================================
class GrowthEngine:
    """Layer 10: Compounding loops, network effects scaling, platform transitions."""

    def simulate_compounding_growth(self, initial_users: int, viral_k: float, retention_rate: float, cycles: int) -> List[int]:
        """Simulates compounding cohort retention and viral loop growth."""
        cohorts = [initial_users]
        current_users = initial_users
        for _ in range(cycles):
            retained = current_users * retention_rate
            new_viral_users = retained * viral_k
            current_users = int(retained + new_viral_users)
            cohorts.append(current_users)
        return cohorts

    def evaluate_platform_transition(self, user_base: int, active_developers: int) -> bool:
        """Determines if product is ready to transition to a platform model."""
        return user_base >= 10000 and active_developers >= 50


# =====================================================================
# Layer 11: Competition & Moats
# =====================================================================
class CompetitionEngine:
    """Layer 11: Game-theoretic competitor response, moat strength quantification."""

    def calculate_moat_score(self, switching_costs: float, network_effects: float, scale_moat: float) -> float:
        """Quantifies structural moat score [0.0, 1.0]."""
        raw_score = (switching_costs * 0.4) + (network_effects * 0.4) + (scale_moat * 0.2)
        return max(0.0, min(1.0, raw_score))

    def predict_competitor_payoff(self, response_type: str) -> float:
        """Calculates expected payoff of competitor response tactic."""
        payoffs = {
            "PRICE_CUT": -0.2,
            "FEATURE_CLONE": 0.1,
            "ACQUISITION_OFFER": 0.8,
            "IGNORE": 0.0
        }
        return payoffs.get(response_type, 0.0)


# =====================================================================
# Layer 12: Organizational Design
# =====================================================================
class OrganizationalDesignEngine:
    """Layer 12: Centralized vs delegated work allocation, hiring signal threshold."""

    def evaluate_hiring_demand(self, shadow_price_talent: float, threshold: float = 1.5) -> bool:
        """Determines if dual shadow price warrants hiring specialized talent."""
        return shadow_price_talent >= threshold

    def determine_delegation_level(self, task_risk_score: float) -> str:
        """Determines delegation level based on risk score."""
        if task_risk_score >= 0.8:
            return "CENTRALIZED_FOUNDER_DIRECTED"
        elif task_risk_score >= 0.4:
            return "DELEGATED_TO_SPECIALIZED_AGENT_WITH_REVIEW"
        else:
            return "FULLY_AUTONOMOUS_DELEGATED_EXECUTION"


# =====================================================================
# Layer 13: Meta-Learning
# =====================================================================
class MetaLearningEngine:
    """Layer 13: Decision quality Brier score calibration, failure-to-axiom conversion."""

    def calculate_brier_score(self, forecast_probs: List[float], actual_outcomes: List[int]) -> float:
        """Computes Brier score measuring forecast calibration quality."""
        if not forecast_probs or len(forecast_probs) != len(actual_outcomes):
            return 1.0
        total_sq_err = sum((p - o) ** 2 for p, o in zip(forecast_probs, actual_outcomes))
        return total_sq_err / len(forecast_probs)

    def convert_failure_to_axiom(self, experiment_id: str, failure_reason: str) -> Dict[str, Any]:
        """Converts an experimental failure into a reusable domain axiom."""
        return {
            "experiment_id": experiment_id,
            "failure_reason": failure_reason,
            "domain_axiom": f"AXIOM_NEVER: Avoid conditions leading to '{failure_reason}'",
            "status": "Axiom Registered in Knowledge Store"
        }


# =====================================================================
# Layer 14: Master AI Entrepreneur Orchestrator
# =====================================================================
class FourteenLayerEntrepreneurialEngine(BaseModel):
    """
    Master closed-loop engine implementing the complete 14-Layer Computational
    Architecture of Entrepreneurship.
    """

    engine_id: UUID = Field(default_factory=uuid4)
    active_cycle: int = 1

    model_config = {"arbitrary_types_allowed": True}

    # Engines for each layer
    layer1_reality: RealitySubstrateEngine = Field(default_factory=RealitySubstrateEngine)
    layer2_opportunity: OpportunityDiscoveryEngine = Field(default_factory=OpportunityDiscoveryEngine)
    layer3_problem: ProblemDiscoveryEngine = Field(default_factory=ProblemDiscoveryEngine)
    layer4_decision: DecisionMakingEngine = Field(default_factory=DecisionMakingEngine)
    layer5_evaluation: OpportunityEvaluationEngine = Field(default_factory=OpportunityEvaluationEngine)
    layer6_product: ProductCreationEngine = Field(default_factory=ProductCreationEngine)
    layer7_customer: CustomerUnderstandingEngine = Field(default_factory=CustomerUnderstandingEngine)
    layer8_marketing: MarketingEngine = Field(default_factory=MarketingEngine)
    layer9_sales: SalesEngine = Field(default_factory=SalesEngine)
    layer10_growth: GrowthEngine = Field(default_factory=GrowthEngine)
    layer11_competition: CompetitionEngine = Field(default_factory=CompetitionEngine)
    layer12_org: OrganizationalDesignEngine = Field(default_factory=OrganizationalDesignEngine)
    layer13_metalearning: MetaLearningEngine = Field(default_factory=MetaLearningEngine)

    def execute_full_entrepreneurial_cycle(
        self,
        market_signal: Dict[str, Any],
        available_capital_cents: int,
        compute_budget: float
    ) -> Dict[str, Any]:
        """
        Executes a closed-loop entrepreneurial cycle across all 14 layers.
        """
        logger.info(f"Executing 14-Layer Entrepreneurial Cycle #{self.active_cycle}")

        # Layer 1: Boundary & Invariant Check
        boundary = self.layer1_reality.classify_automation_boundary(
            task_name=market_signal.get("title", "Signal"),
            characteristics={"is_convex_optimization": True}
        )
        invariants = self.layer1_reality.evaluate_invariant_principles({
            "max_downside_cents": 100000,
            "max_upside_cents": 1000000,
            "prediction_error": 0.2,
            "active_experiments_count": 3
        })

        # Layer 2: Signal Filtering & Concept Recombination
        spectral_data = market_signal.get("spectral_amplitudes", [0.2, 0.4, 4.2, 0.5])
        weak_signals = self.layer2_opportunity.detect_weak_signals(spectral_data, anomaly_threshold=1.5)
        recombinations = self.layer2_opportunity.recombine_unrelated_observations(
            domain_a_concepts=["AI_Agent", "Active_Inference"],
            domain_b_concepts=["Enterprise_SaaS", "Autonomous_Robotics"]
        )

        # Layer 3: Problem Discovery
        stated_problem = market_signal.get("stated_problem", "High Operational Friction in Enterprise Workflows")
        causal_links = market_signal.get("causal_links", [("Legacy_Architecture", "Manual_Data_Entry"), ("Manual_Data_Entry", "High Operational Friction in Enterprise Workflows")])
        problem_decomposition = self.layer3_problem.decompose_problem_dag(stated_problem, causal_links)

        # Layer 4: Decision Engine EFE calculation
        efe = self.layer4_decision.calculate_expected_free_energy(
            prior_entropy=1.8,
            post_entropy=0.4,
            success_prob=0.75
        )
        blended_score = self.layer4_decision.blend_intuition_and_data(
            intuition_prior=0.8,
            data_likelihood=0.65,
            sample_size=25
        )

        # Layer 5: Opportunity Evaluation
        ev = self.layer5_evaluation.calculate_expected_value(
            tam_cents=market_signal.get("tam_cents", 500000000),
            win_rate=0.05,
            margin=0.8,
            exp_cost_cents=2000000
        )
        cvar = self.layer5_evaluation.calculate_cvar_downside([-100.0, -50.0, 10.0, 50.0, 200.0])

        # Layer 6: Product Creation JTBD & Complexity Pruning
        jtbd = self.layer6_product.extract_core_jtbd("Customers want seamless autonomous decision intelligence.")
        pruned_features = self.layer6_product.prune_feature_complexity([
            {"name": "Core Engine", "complexity": 2.0, "utility_per_complexity": 5.0},
            {"name": "Dashboard UI", "complexity": 1.5, "utility_per_complexity": 2.0},
            {"name": "Fancy Animations", "complexity": 3.0, "utility_per_complexity": 0.2}
        ], complexity_budget=4.0)

        # Layer 7: Customer Understanding
        p_switch = self.layer7_customer.calculate_switching_probability(u_new=0.9, u_old=0.4, switching_friction=0.2)
        trust_score = self.layer7_customer.update_trust_score(current_trust=0.7, promised_utility=0.9, delivered_utility=0.88)

        # Layer 8: Marketing & Brand Dynamics
        viral_r0 = self.layer8_marketing.calculate_viral_r0(transmission_rate=0.15, active_retention_days=14.0)
        positioning_dist = self.layer8_marketing.compute_positioning_distance([0.9, 0.8], [[0.2, 0.3], [0.1, 0.4]])

        # Layer 9: Sales Systems
        resolved_objection = self.layer9_sales.resolve_objection("TOO_EXPENSIVE")
        urgency = self.layer9_sales.calculate_buying_urgency_index(cost_of_inaction_cents=5000000, implementation_friction=0.5)

        # Layer 10: Growth & Scaling
        compounding_sim = self.layer10_growth.simulate_compounding_growth(initial_users=100, viral_k=0.15, retention_rate=0.9, cycles=4)
        is_platform_ready = self.layer10_growth.evaluate_platform_transition(user_base=15000, active_developers=60)

        # Layer 11: Competition & Moats
        moat_score = self.layer11_competition.calculate_moat_score(switching_costs=0.8, network_effects=0.7, scale_moat=0.5)

        # Layer 12: Organizational Design
        hiring_needed = self.layer12_org.evaluate_hiring_demand(shadow_price_talent=1.8)
        delegation = self.layer12_org.determine_delegation_level(task_risk_score=0.3)

        # Layer 13: Meta-Learning Calibration
        brier = self.layer13_metalearning.calculate_brier_score(forecast_probs=[0.8, 0.7, 0.9], actual_outcomes=[1, 1, 0])
        axiom = self.layer13_metalearning.convert_failure_to_axiom("EXP_001", "High churn due to slow onboarding")

        self.active_cycle += 1

        # Layer 14: AI Entrepreneur Synthesis Result
        return {
            "cycle_number": self.active_cycle - 1,
            "layer1_automation_boundary": boundary,
            "layer1_invariants_satisfied": invariants,
            "layer2_weak_signal_indices": weak_signals,
            "layer2_recombinations_count": len(recombinations),
            "layer3_problem_root_causes": problem_decomposition["root_causes"],
            "layer4_expected_free_energy": efe,
            "layer4_blended_belief": blended_score,
            "layer5_expected_value_cents": ev,
            "layer5_cvar_downside": cvar,
            "layer6_pruned_feature_count": len(pruned_features),
            "layer7_switching_probability": p_switch,
            "layer7_updated_trust": trust_score,
            "layer8_viral_r0": viral_r0,
            "layer8_positioning_distance": positioning_dist,
            "layer9_urgency_index": urgency,
            "layer10_compounding_final_users": compounding_sim[-1],
            "layer10_is_platform_ready": is_platform_ready,
            "layer11_moat_score": moat_score,
            "layer12_hiring_needed": hiring_needed,
            "layer12_delegation_level": delegation,
            "layer13_brier_score": brier,
            "layer13_registered_axiom": axiom["domain_axiom"]
        }
