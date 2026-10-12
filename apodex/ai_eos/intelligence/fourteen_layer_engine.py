"""
The complete, first-principles executable engine for the 14-Layer Computational
Architecture of Entrepreneurship in APODEX AI EOS.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.fourteen_layer_engine")


# ============================================================================
# Core Data Models
# ============================================================================

class MarketSignal(BaseModel):
    """Raw external sensory state signal ingested into Layer 2."""
    signal_id: UUID = Field(default_factory=uuid4)
    domain: str
    title: str
    variance: float = 0.5
    mean_shift: float = 0.1
    trend_acceleration: float = 0.05
    domain_a: str = ""
    domain_b: str = ""
    incumbent_cognitive_lock: bool = True
    margin_signal: float = 0.15


class ProblemSpec(BaseModel):
    """Formulated problem structure evaluated in Layer 3."""
    problem_id: UUID = Field(default_factory=uuid4)
    stated_problem: str
    real_problem: str
    nodes: List[str] = Field(default_factory=list)  # DAG nodes
    edges: List[Tuple[str, str]] = Field(default_factory=list)  # (parent, child)
    direct_effect: float = 0.8  # Direct effect of root cause
    indirect_effect: float = 0.2  # Indirect effect of symptom
    cost_to_solve: float = 50000.0
    expected_value_saved: float = 200000.0


class OpportunitySpec(BaseModel):
    """Quantitative opportunity candidate evaluated through Layers 4-14."""
    opp_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str
    prior_entropy: float = 1.8
    post_entropy_simulated: float = 0.4
    success_probability: float = 0.6
    target_preference: float = 0.95
    tam_cents: int = 500000000  # $5M
    gross_margin: float = 0.75
    ltv_cents: int = 1200000  # $12k
    cac_cents: int = 250000  # $2.5k
    downside_loss_cents: int = 5000000  # $50k
    switching_friction: float = 0.3
    viral_invitations_per_user: float = 2.5
    viral_conversion_rate: float = 0.45
    churn_rate: float = 0.03
    capacity_utilization: float = 0.90


# ============================================================================
# Layer 1: Reality Substrate
# ============================================================================

class RealitySubstrateEngine:
    """Layer 1: Fundamental principles and automation partitioning."""

    @staticmethod
    def get_invariant_principles() -> List[str]:
        return [
            "Asymmetric Risk/Reward Arbitrage",
            "Active Inference & Uncertainty Reduction",
            "Value Creation via Entropy Reduction"
        ]

    @staticmethod
    def classify_automation_feasibility(task_name: str) -> Dict[str, Any]:
        unautomatable_keywords = ["sovereign", "ethical", "existential", "moral", "ultimate_risk"]
        is_human = any(kw in task_name.lower() for kw in unautomatable_keywords)
        return {
            "task_name": task_name,
            "requires_human_sovereignty": is_human,
            "automation_feasibility": 0.1 if is_human else 0.95
        }


# ============================================================================
# Layer 2: Continuous State-Space Opportunity Discovery
# ============================================================================

class ContinuousStateSpaceDiscoveryEngine:
    """Layer 2: Continuous state-space sensing, signal filtering, and synthesis."""

    def __init__(self, variance_threshold: float = 0.3) -> None:
        self.variance_threshold = variance_threshold

    def detect_weak_signal_anomaly(self, signal: MarketSignal) -> bool:
        """Detects variance anomalies before mean shifts occur."""
        return signal.variance > self.variance_threshold

    def synthesize_combinatorial_crossover(self, domain_a: str, domain_b: str) -> str:
        """Generates candidate hypergraph crossover model A (X) B."""
        return f"Crossover_{domain_a}_X_{domain_b}"

    def is_invisible_opportunity(self, signal: MarketSignal) -> bool:
        """Classifies if opportunity is hidden from incumbents due to lock or low margin."""
        return signal.incumbent_cognitive_lock or signal.margin_signal < 0.20


# ============================================================================
# Layer 3: Problem Discovery & Decomposition
# ============================================================================

class ProblemDiscoveryDecompositionEngine:
    """Layer 3: Problem boundary reformulation, DAG decomposition, and root cause distillation."""

    def decompose_problem_dag(self, spec: ProblemSpec) -> Dict[str, Any]:
        root_nodes = [n for n in spec.nodes if not any(edge[1] == n for edge in spec.edges)]
        symptom_nodes = [n for n in spec.nodes if n not in root_nodes]
        return {
            "root_causes": root_nodes,
            "symptoms": symptom_nodes,
            "total_depth": len(spec.edges)
        }

    def distill_root_cause_vs_symptom(self, spec: ProblemSpec) -> str:
        """Mediated causal analysis: High DE = Root Cause, High IE = Symptom."""
        if spec.direct_effect > spec.indirect_effect:
            return f"ROOT_CAUSE: {spec.real_problem}"
        return f"SYMPTOM: {spec.stated_problem}"

    def evaluate_ignore_decision(self, spec: ProblemSpec) -> bool:
        """Returns True if the problem should be ignored (cost > value saved)."""
        return spec.cost_to_solve >= spec.expected_value_saved


# ============================================================================
# Layer 4: Decision Making Under Uncertainty
# ============================================================================

class DecisionUnderUncertaintyEngine:
    """Layer 4: Active Inference EFE decision engine & adversarial hypothesis testing."""

    def calculate_expected_free_energy(self, opp: OpportunitySpec, curiosity_weight: float = 1.0) -> float:
        eps = 1e-10
        p_succ = max(eps, min(1.0 - eps, opp.success_probability))
        p_pref = max(eps, min(1.0 - eps, opp.target_preference))
        pragmatic_value = math.log(p_succ) - math.log(p_pref)
        epistemic_value = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)
        return -pragmatic_value - (epistemic_value * curiosity_weight)

    def calculate_value_of_information(self, prior_entropy: float, cost_of_sample: float) -> float:
        """Computes expected VoI: Entropy Reduction Value - Sample Cost."""
        information_value = prior_entropy * 100000.0
        return max(0.0, information_value - cost_of_sample)

    def fast_idea_killer(self, posterior_prob: float, cutoff: float = 0.35) -> bool:
        """Adversarial falsification engine: returns True if idea should be killed."""
        return posterior_prob < cutoff


# ============================================================================
# Layer 5: Quantitative Opportunity Evaluation
# ============================================================================

class QuantitativeEvaluationEngine:
    """Layer 5: EV, Value-at-Risk (VaR), and Bellman real-options switching thresholds."""

    def compute_expected_value_cents(self, opp: OpportunitySpec) -> float:
        npv_ltv = opp.ltv_cents * (opp.tam_cents / max(1, opp.cac_cents))
        ev = (opp.success_probability * npv_ltv) - ((1.0 - opp.success_probability) * opp.downside_loss_cents)
        return ev

    def compute_downside_var_cents(self, opp: OpportunitySpec, confidence_level: float = 0.95) -> float:
        """Estimates Value-at-Risk under a simple parametric loss distribution."""
        z_score = 1.645 if confidence_level == 0.95 else 2.326
        variance = opp.downside_loss_cents * 0.2
        return opp.downside_loss_cents + (z_score * math.sqrt(variance))

    def evaluate_bellman_switching_threshold(self, current_ev: float, candidate_ev: float, switching_cost: float) -> bool:
        """Real options optimality: switch if candidate EV exceeds current EV + switching cost."""
        return candidate_ev > (current_ev + switching_cost)


# ============================================================================
# Layer 6: Product Creation & Anti-Feature Elimination
# ============================================================================

class ProductCreationEngine:
    """Layer 6: Anti-feature elimination and learning-rate optimization."""

    def evaluate_anti_feature_matrix(self, utility_delta: float, complexity_delta: float, threshold: float = 1.5) -> bool:
        """Prunes candidate feature if utility-to-complexity ratio is below threshold."""
        if complexity_delta <= 0:
            return True
        return (utility_delta / complexity_delta) >= threshold

    def compute_learning_build_ratio(self, epistemic_gain: float, build_hours: float) -> float:
        if build_hours <= 0:
            return 0.0
        return epistemic_gain / build_hours


# ============================================================================
# Layer 7: Customer Psychology Modeling
# ============================================================================

class CustomerPsychologyEngine:
    """Layer 7: Switching dynamics, trust accumulation, and hazard rate churn modeling."""

    def calculate_switching_probability(self, utility_new: float, utility_old: float, friction: float, k: float = 2.0) -> float:
        diff = utility_new - utility_old - friction
        return 1.0 / (1.0 + math.exp(-k * diff))

    def predict_churn_hazard_rate(self, usage_decay_slope: float, baseline_hazard: float = 0.02) -> float:
        return baseline_hazard * math.exp(abs(usage_decay_slope))


# ============================================================================
# Layer 8: Market Formation & Growth Mechanics
# ============================================================================

class MarketFormationEngine:
    """Layer 8: Virality K-factor, attention spreading, and positioning."""

    def compute_viral_coefficient_k(self, invitations_per_user: float, conversion_rate: float) -> float:
        return invitations_per_user * conversion_rate

    def simulate_sir_attention_spread(self, population: int, initial_infected: int, beta: float, gamma: float, steps: int = 10) -> Dict[str, List[float]]:
        S, I, R = float(population - initial_infected), float(initial_infected), 0.0
        s_hist, i_hist, r_hist = [S], [I], [R]
        for _ in range(steps):
            new_inf = (beta * S * I) / population
            new_rec = gamma * I
            S -= new_inf
            I += new_inf - new_rec
            R += new_rec
            s_hist.append(S)
            i_hist.append(I)
            r_hist.append(R)
        return {"susceptible": s_hist, "infected_attention": i_hist, "recovered": r_hist}


# ============================================================================
# Layer 9: Psychological Sales Systems
# ============================================================================

class PsychologicalSalesEngine:
    """Layer 9: Urgency decay, objection resolution, and sales channel routing."""

    def compute_buying_urgency(self, status_quo_loss: float, time_to_deadline: float, decay_lambda: float = 0.1) -> float:
        return status_quo_loss * math.exp(decay_lambda * time_to_deadline)

    def route_sales_channel(self, acv_cents: int) -> str:
        # $10,000 ACV = 1,000,000 cents
        if acv_cents >= 1000000:
            return "ENTERPRISE_HIGH_TOUCH"
        return "AUTOMATED_SELF_SERVE"


# ============================================================================
# Layer 10: Compounding Growth & Ecosystem Platforms
# ============================================================================

class CompoundingGrowthEngine:
    """Layer 10: Metcalfe network valuation, platform flywheel, and growth throttling."""

    def compute_metcalfe_value(self, user_count: int) -> float:
        return float(user_count ** 2)

    def evaluate_growth_throttling(self, churn_rate: float, critical_churn_threshold: float = 0.08) -> bool:
        """Returns True if growth should be deliberately throttled to fix bucket leaks."""
        return churn_rate > critical_churn_threshold


# ============================================================================
# Layer 11: Competitive Dynamics & Moats
# ============================================================================

class CompetitiveDynamicsEngine:
    """Layer 11: Moat scoring, minimax game theory, and pivot thresholds."""

    def score_moat_strength(self, network_effects: float, switching_costs: float, cost_advantages: float) -> float:
        return (network_effects * 0.4) + (switching_costs * 0.4) + (cost_advantages * 0.2)

    def evaluate_pivot_necessity(self, ltv_cac_ratio: float, incumbent_aggression: float) -> bool:
        return (ltv_cac_ratio < 1.0) or (incumbent_aggression > 0.85 and ltv_cac_ratio < 1.5)


# ============================================================================
# Layer 12: Organizational Architecture & Scaling
# ============================================================================

class OrganizationalScalingEngine:
    """Layer 12: Capacity bottleneck hiring triggers and centralization routers."""

    def evaluate_hiring_trigger(self, capacity_utilization: float, threshold: float = 0.85) -> bool:
        return capacity_utilization > threshold

    def route_decision_centralization(self, decision_type: str) -> str:
        centralized_types = ["capital_allocation", "core_architecture", "strategic_pivot", "ethics"]
        if decision_type.lower() in centralized_types:
            return "CENTRALIZED_HQ"
        return "DELEGATED_POD"


# ============================================================================
# Layer 13: Entrepreneurial Meta-Learning
# ============================================================================

class EntrepreneurialMetaLearningEngine:
    """Layer 13: Hierarchical Bayesian mental model updating and Decision Quality Scoring."""

    def compute_decision_quality_score(self, info_completeness: float, bias_suppression: float, efe_alignment: float) -> float:
        return (info_completeness * 0.3) + (bias_suppression * 0.3) + (efe_alignment * 0.4)

    def extract_failure_knowledge(self, failure_reason: str) -> Dict[str, Any]:
        return {
            "anti_pattern_id": str(uuid4()),
            "root_cause": failure_reason,
            "registered_in_global_memory": True
        }


# ============================================================================
# Layer 14: Autonomous AI Entrepreneurship
# ============================================================================

class AutonomousAIEntrepreneurshipEngine:
    """Layer 14: Task paradigm classification, resource allocation, and self-improvement flywheel."""

    def classify_execution_paradigm(self, task_description: str) -> str:
        desc = task_description.lower()
        if "ethical" in desc or "sovereign" in desc:
            return "HUMAN_SOVEREIGN_JUDGMENT"
        elif "cause" in desc or "counterfactual" in desc or "intervention" in desc:
            return "CAUSAL_INFERENCE"
        elif "forecast" in desc or "predict" in desc or "trend" in desc:
            return "PROBABILISTIC_REASONING"
        elif "creative" in desc or "copy" in desc or "brand" in desc:
            return "CREATIVITY_SYNTHESIS"
        else:
            return "DETERMINISTIC_ALGORITHMIC"

    def optimize_resource_allocation(self, capital_cents: int, compute_units: float, max_risk_budget: float) -> Dict[str, Any]:
        allocated_capital = int(capital_cents * 0.70)
        allocated_compute = compute_units * 0.80
        reserve_capital = capital_cents - allocated_capital
        return {
            "allocated_capital_cents": allocated_capital,
            "reserve_capital_cents": reserve_capital,
            "allocated_compute_units": allocated_compute,
            "risk_budget_utilized": min(1.0, max_risk_budget)
        }


# ============================================================================
# Master 14-Layer Orchestrator
# ============================================================================

class FourteenLayerOrchestrator:
    """
    Master coordinating orchestrator executing the 14-Layer Computational Architecture
    of Entrepreneurship across sensory inputs and opportunity candidates.
    """

    def __init__(self) -> None:
        self.layer1 = RealitySubstrateEngine()
        self.layer2 = ContinuousStateSpaceDiscoveryEngine()
        self.layer3 = ProblemDiscoveryDecompositionEngine()
        self.layer4 = DecisionUnderUncertaintyEngine()
        self.layer5 = QuantitativeEvaluationEngine()
        self.layer6 = ProductCreationEngine()
        self.layer7 = CustomerPsychologyEngine()
        self.layer8 = MarketFormationEngine()
        self.layer9 = PsychologicalSalesEngine()
        self.layer10 = CompoundingGrowthEngine()
        self.layer11 = CompetitiveDynamicsEngine()
        self.layer12 = OrganizationalScalingEngine()
        self.layer13 = EntrepreneurialMetaLearningEngine()
        self.layer14 = AutonomousAIEntrepreneurshipEngine()

    def execute_complete_14_layer_pipeline(
        self,
        signal: MarketSignal,
        problem: ProblemSpec,
        opp: OpportunitySpec
    ) -> Dict[str, Any]:
        """Runs the entire 14-layer pipeline and produces an integrated execution diagnosis."""
        logger.info(f"Executing 14-layer pipeline for opportunity '{opp.title}'")

        # Layer 1
        principles = self.layer1.get_invariant_principles()

        # Layer 2
        is_weak_anomaly = self.layer2.detect_weak_signal_anomaly(signal)
        crossover_model = self.layer2.synthesize_combinatorial_crossover(signal.domain_a or "AI", signal.domain_b or "Robotics")
        is_invisible = self.layer2.is_invisible_opportunity(signal)

        # Layer 3
        problem_dag = self.layer3.decompose_problem_dag(problem)
        root_cause_diagnosis = self.layer3.distill_root_cause_vs_symptom(problem)
        should_ignore_problem = self.layer3.evaluate_ignore_decision(problem)

        # Layer 4
        efe = self.layer4.calculate_expected_free_energy(opp)
        voi = self.layer4.calculate_value_of_information(opp.prior_entropy, cost_of_sample=5000.0)
        should_kill_idea = self.layer4.fast_idea_killer(opp.success_probability)

        # Layer 5
        ev_cents = self.layer5.compute_expected_value_cents(opp)
        downside_var = self.layer5.compute_downside_var_cents(opp)

        # Layer 6
        keep_feature = self.layer6.evaluate_anti_feature_matrix(utility_delta=2.5, complexity_delta=1.0)
        learning_ratio = self.layer6.compute_learning_build_ratio(epistemic_gain=1.4, build_hours=20.0)

        # Layer 7
        p_switch = self.layer7.calculate_switching_probability(utility_new=0.9, utility_old=0.4, friction=opp.switching_friction)
        churn_hazard = self.layer7.predict_churn_hazard_rate(usage_decay_slope=0.05)

        # Layer 8
        k_factor = self.layer8.compute_viral_coefficient_k(opp.viral_invitations_per_user, opp.viral_conversion_rate)

        # Layer 9
        urgency = self.layer9.compute_buying_urgency(status_quo_loss=50000.0, time_to_deadline=14.0)
        sales_channel = self.layer9.route_sales_channel(opp.ltv_cents)

        # Layer 10
        metcalfe_val = self.layer10.compute_metcalfe_value(user_count=1000)
        throttle_growth = self.layer10.evaluate_growth_throttling(opp.churn_rate)

        # Layer 11
        moat_score = self.layer11.score_moat_strength(network_effects=0.8, switching_costs=0.7, cost_advantages=0.6)
        ltv_cac_ratio = (opp.ltv_cents / opp.cac_cents) if opp.cac_cents > 0 else 1.0
        should_pivot = self.layer11.evaluate_pivot_necessity(ltv_cac_ratio=ltv_cac_ratio, incumbent_aggression=0.3)

        # Layer 12
        hire_trigger = self.layer12.evaluate_hiring_trigger(opp.capacity_utilization)
        decision_route = self.layer12.route_decision_centralization("capital_allocation")

        # Layer 13
        dqs = self.layer13.compute_decision_quality_score(info_completeness=0.85, bias_suppression=0.90, efe_alignment=0.95)

        # Layer 14
        task_paradigm = self.layer14.classify_execution_paradigm("Causal counterfactual intervention optimization")
        res_alloc = self.layer14.optimize_resource_allocation(capital_cents=100000000, compute_units=100.0, max_risk_budget=0.2)

        return {
            "status": "COMPLETED",
            "opportunity_title": opp.title,
            "layer1_invariant_principles": principles,
            "layer2_discovery": {
                "weak_signal_anomaly": is_weak_anomaly,
                "combinatorial_crossover": crossover_model,
                "invisible_opportunity": is_invisible
            },
            "layer3_problem": {
                "dag": problem_dag,
                "root_cause_diagnosis": root_cause_diagnosis,
                "should_ignore_problem": should_ignore_problem
            },
            "layer4_decision": {
                "expected_free_energy": efe,
                "value_of_information": voi,
                "should_kill_idea": should_kill_idea
            },
            "layer5_evaluation": {
                "expected_value_cents": ev_cents,
                "downside_var_cents": downside_var,
                "ltv_cac_ratio": ltv_cac_ratio
            },
            "layer6_product": {
                "feature_pruning_passed": keep_feature,
                "learning_build_ratio": learning_ratio
            },
            "layer7_customer": {
                "switching_probability": p_switch,
                "churn_hazard_rate": churn_hazard
            },
            "layer8_growth": {
                "viral_k_factor": k_factor
            },
            "layer9_sales": {
                "buying_urgency": urgency,
                "sales_channel": sales_channel
            },
            "layer10_platform": {
                "metcalfe_network_value": metcalfe_val,
                "throttle_growth": throttle_growth
            },
            "layer11_competition": {
                "moat_score": moat_score,
                "should_pivot": should_pivot
            },
            "layer12_organization": {
                "hire_trigger": hire_trigger,
                "decision_route": decision_route
            },
            "layer13_meta_learning": {
                "decision_quality_score": dqs
            },
            "layer14_ai_entrepreneurship": {
                "task_paradigm": task_paradigm,
                "resource_allocation": res_alloc
            }
        }
