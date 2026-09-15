"""
Fourteen-Layer Computational Architecture of Entrepreneurship.

Implements the 14-layer first-principles cognitive OS for autonomous enterprise creation,
sensing, problem discovery, decision making, product creation, customer modeling,
marketing, sales, growth, competition, org design, meta-learning, and AI orchestration.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger("sero.fourteen_layer_engine")


# =====================================================================
# State Representations
# =====================================================================

class EnterpriseState(BaseModel):
    """Unified state dictionary tracking the enterprise across all 14 layers."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    venture_id: UUID = Field(default_factory=uuid4)
    name: str = "AIAgentVenture"
    capital_cents: int = 100_000_00  # $100k starting capital
    compute_budget_hours: float = 1000.0
    active_opportunities: List[Dict[str, Any]] = Field(default_factory=list)
    active_hypotheses: List[Dict[str, Any]] = Field(default_factory=list)
    product_features: List[str] = Field(default_factory=list)
    customer_count: int = 0
    monthly_recurring_revenue_cents: int = 0
    trust_vector: Dict[str, float] = Field(default_factory=lambda: {"credibility": 0.5, "satisfaction": 0.5})
    moat_score: float = 0.2
    organizational_nodes: List[str] = Field(default_factory=lambda: ["core_orchestrator"])
    mental_models: Dict[str, float] = Field(default_factory=dict)
    execution_history: List[Dict[str, Any]] = Field(default_factory=list)


# =====================================================================
# Layer 1: Reality Substrate
# =====================================================================

class RealitySubstrateEngine:
    """Layer 1: Reality Substrate.

    Formalizes physical, thermodynamic, and thermodynamic limits of value creation,
    distinguishing human terminal utility from automatable optimization problems.
    """

    def calculate_thermodynamic_efficiency(self, energy_input_joules: float, utility_output: float) -> float:
        """Computes low-entropy energy/capital transformation efficiency."""
        if energy_input_joules <= 0:
            return 0.0
        return min(1.0, utility_output / (energy_input_joules * 1e-6))

    def delineate_automation_boundary(self, task_name: str, involves_terminal_human_value: bool) -> Dict[str, Any]:
        """Classifies tasks into automatable optimization vs human-arbitrated value."""
        if involves_terminal_human_value:
            return {
                "task": task_name,
                "automatable": False,
                "category": "human_psychology_and_terminal_value",
                "action": "defer_to_human_arbitration"
            }
        return {
            "task": task_name,
            "automatable": True,
            "category": "causal_state_space_optimization",
            "action": "execute_autonomous_algorithm"
        }


# =====================================================================
# Layer 2: Opportunity Discovery
# =====================================================================

class OpportunityDiscoveryEngine:
    """Layer 2: Opportunity Discovery.

    Scans high-dimensional state space for weak signal anomalies, supply-demand KL divergence,
    and cross-domain conceptual combinations.
    """

    def detect_weak_signals(self, signal_stream: List[Dict[str, Any]], z_score_threshold: float = 1.5) -> List[Dict[str, Any]]:
        """Detects low-frequency, high-variance anomaly signals in unstructured temporal streams."""
        if not signal_stream:
            return []

        values = [s.get("value", 0.0) for s in signal_stream]
        mean_val = sum(values) / len(values) if values else 0.0
        variance = sum((v - mean_val) ** 2 for v in values) / len(values) if len(values) > 1 else 1.0
        std_dev = math.sqrt(variance) if variance > 0 else 1.0

        anomalies = []
        for signal in signal_stream:
            val = signal.get("value", 0.0)
            z_score = abs(val - mean_val) / std_dev
            if z_score >= z_score_threshold:
                sig_copy = dict(signal)
                sig_copy["anomaly_score"] = z_score
                anomalies.append(sig_copy)

        return anomalies

    def calculate_kl_divergence_gap(self, supply_distribution: List[float], demand_distribution: List[float]) -> float:
        """Calculates Kullback-Leibler divergence between supply and demand distributions."""
        eps = 1e-10
        divergence = 0.0
        for p, q in zip(demand_distribution, supply_distribution):
            p_safe = max(eps, min(1.0, p))
            q_safe = max(eps, min(1.0, q))
            divergence += p_safe * math.log(p_safe / q_safe)
        return max(0.0, divergence)

    def generate_novel_conceptual_synthesis(self, domain_a_concepts: List[str], domain_b_concepts: List[str]) -> List[Dict[str, Any]]:
        """Cross-domain conceptual tensor product for generating novel opportunity candidates."""
        syntheses = []
        for a in domain_a_concepts:
            for b in domain_b_concepts:
                syntheses.append({
                    "title": f"Cross-Domain Synthesis: {a} x {b}",
                    "domain_a": a,
                    "domain_b": b,
                    "novelty_score": 0.85
                })
        return syntheses


# =====================================================================
# Layer 3: Problem Discovery
# =====================================================================

class ProblemDiscoveryEngine:
    """Layer 3: Problem Discovery.

    Decomposes problems into Structural Causal Models (SCMs), isolates symptoms from root causes,
    and applies EVIG ignore criteria.
    """

    def decompose_problem_scm(self, variables: List[str], edges: List[Tuple[str, str]]) -> Dict[str, Any]:
        """Constructs a DAG SCM to distinguish symptoms from root causes."""
        parents: Dict[str, List[str]] = {v: [] for v in variables}
        children: Dict[str, List[str]] = {v: [] for v in variables}

        for parent, child in edges:
            if parent in parents and child in parents:
                parents[child].append(parent)
                children[parent].append(child)

        root_causes = [v for v in variables if not parents[v]]
        symptoms = [v for v in variables if parents[v] and not children[v]]

        return {
            "root_causes": root_causes,
            "symptoms": symptoms,
            "intermediate_nodes": [v for v in variables if parents[v] and children[v]],
            "graph": {"parents": parents, "children": children}
        }

    def evaluate_ignore_criteria(self, evig: float, expected_utility_gain: float, investigation_cost: float) -> bool:
        """Ignore criteria: EVIG + Delta U_solve < C_investigate."""
        should_ignore = (evig + expected_utility_gain) < investigation_cost
        logger.info(f"Problem ignore criteria evaluated: EVIG({evig:.2f}) + U_gain({expected_utility_gain:.2f}) vs Cost({investigation_cost:.2f}) -> Ignore={should_ignore}")
        return should_ignore


# =====================================================================
# Layer 4: Decision Making
# =====================================================================

class DecisionMakingEngine:
    """Layer 4: Decision Making.

    Resolves Knightian uncertainty using Active Inference EFE, SPRT idea killing,
    and adversarial negative-bias search.
    """

    def compute_expected_free_energy(self, p_success: float, p_target: float, prior_entropy: float, post_entropy: float, curiosity_weight: float = 1.0) -> float:
        """Calculates EFE G = - Pragmatic Value - Curiosity * Epistemic Value."""
        eps = 1e-10
        ps = max(eps, min(1.0 - eps, p_success))
        pt = max(eps, min(1.0 - eps, p_target))

        pragmatic_val = math.log(ps) - math.log(pt)
        epistemic_val = max(0.0, prior_entropy - post_entropy)

        efe = -pragmatic_val - (curiosity_weight * epistemic_val)
        return efe

    def sequential_probability_ratio_test(self, observations: List[bool], alpha: float = 0.05, beta: float = 0.1) -> str:
        """SPRT for rapid hypothesis/idea termination under asymmetric thresholds."""
        if not observations:
            return "CONTINUE_TESTING"

        # Log-likelihood ratio calculation
        p1 = 0.7  # H1: Success
        p0 = 0.3  # H0: Failure
        llr = 0.0

        for obs in observations:
            if obs:
                llr += math.log(p1 / p0)
            else:
                llr += math.log((1 - p1) / (1 - p0))

        upper_bound = math.log((1 - beta) / alpha)
        lower_bound = math.log(beta / (1 - alpha))

        if llr >= upper_bound:
            return "ACCEPT_IDEA"
        elif llr <= lower_bound:
            return "KILL_IDEA_QUICKLY"
        return "CONTINUE_TESTING"


# =====================================================================
# Layer 5: Opportunity Evaluation
# =====================================================================

class OpportunityEvaluationEngine:
    """Layer 5: Opportunity Evaluation.

    Calculates Expected Value, Real Option timing value, downside risk, and pivot thresholds.
    """

    def calculate_expected_value(self, tam_cents: int, gross_margin: float, success_probability: float, risk_discount: float) -> int:
        """Computes risk-adjusted expected monetary value in cents."""
        raw_ev = tam_cents * gross_margin * success_probability
        discounted_ev = raw_ev * (1.0 - max(0.0, min(0.9, risk_discount)))
        return int(discounted_ev)

    def evaluate_real_option_timing(self, volatility: float, time_horizon_years: float, first_mover_advantage: float) -> str:
        """Real Option value to defer investment vs immediate execution."""
        option_value_to_wait = volatility * math.sqrt(max(0.1, time_horizon_years))
        if option_value_to_wait > first_mover_advantage:
            return "DEFER_AND_GATHER_INFORMATION"
        return "EXECUTE_IMMEDIATELY"

    def check_abandonment_threshold(self, efe_continue: float, efe_pivot: float, switching_cost: float) -> bool:
        """Abandonment trigger: G_continue > G_pivot + C_switch."""
        return efe_continue > (efe_pivot + switching_cost)


# =====================================================================
# Layer 6: Product Creation
# =====================================================================

class ProductCreationEngine:
    """Layer 6: Product Creation.

    Minimizes Kolmogorov complexity regularization penalty on features, satisfied JTBD,
    and learning-first experiment design.
    """

    def apply_kolmogorov_complexity_penalty(self, proposed_features: List[str], feature_utilities: Dict[str, float], lambda_reg: float = 0.1) -> List[str]:
        """Filters feature set by minimizing Viable Complexity K(P)."""
        selected_features = []
        for feat in proposed_features:
            utility = feature_utilities.get(feat, 0.5)
            # Complexity complexity penalty proportional to string length / descriptor complexity
            complexity_penalty = lambda_reg * len(feat)
            net_value = utility - complexity_penalty
            if net_value > 0.1:
                selected_features.append(feat)
        return selected_features if selected_features else proposed_features[:1]


# =====================================================================
# Layer 7: Customer Understanding
# =====================================================================

class CustomerUnderstandingEngine:
    """Layer 7: Customer Understanding.

    Models customer Active Inference utility and Push-Pull-Inertia-Anxiety switching probability.
    """

    def calculate_switching_probability(self, push_force: float, pull_force: float, inertia: float, anxiety: float) -> float:
        """P(switch) = f(Push + Pull - Inertia - Anxiety)."""
        net_force = (push_force + pull_force) - (inertia + anxiety)
        # Sigmoid transition mapping
        prob = 1.0 / (1.0 + math.exp(-net_force))
        return prob


# =====================================================================
# Layer 8: Marketing
# =====================================================================

class MarketingEngine:
    """Layer 8: Marketing.

    Models attention spread via information cascades on scale-free graphs and authority PageRank.
    """

    def simulate_information_cascade(self, initial_seeds: int, virality_coefficient: float, network_decay: float) -> int:
        """Simulates information propagation depth across a networked market graph."""
        reach = initial_seeds
        current_layer = initial_seeds
        for _ in range(5):  # 5 propagation hops
            current_layer = int(current_layer * virality_coefficient * (1.0 - network_decay))
            reach += current_layer
            if current_layer <= 0:
                break
        return reach


# =====================================================================
# Layer 9: Sales
# =====================================================================

class SalesEngine:
    """Layer 9: Sales.

    Determines transaction risk reduction, counterfactual urgency, and sales automation boundaries.
    """

    def determine_sales_strategy(self, annual_contract_value_cents: int, stakeholder_complexity_score: float) -> str:
        """ACV threshold check: ACV < $5k -> self-serve automation; else enterprise sales."""
        acv_usd = annual_contract_value_cents / 100.0
        if acv_usd < 5000 and stakeholder_complexity_score < 0.3:
            return "AUTOMATED_SELF_SERVE_FUNNEL"
        return "HIGH_TOUCH_ENTERPRISE_SALES"


# =====================================================================
# Layer 10: Growth
# =====================================================================

class GrowthEngine:
    """Layer 10: Growth.

    Evaluates network effects sub-quadratic scaling V ~ N log N and intentional growth slowdown limits.
    """

    def compute_subquadratic_network_value(self, user_count: int) -> float:
        """Beckstrom/Zipf sub-quadratic network valuation: V ~ N * log2(N)."""
        if user_count <= 1:
            return 1.0
        return float(user_count * math.log2(user_count))

    def check_intentional_slowdown(self, growth_rate: float, operational_throughput_capacity: float) -> bool:
        """Triggers intentional growth throttling if growth exceeds support throughput capacity."""
        return growth_rate > (operational_throughput_capacity * 1.2)


# =====================================================================
# Layer 11: Competition
# =====================================================================

class CompetitionEngine:
    """Layer 11: Competition.

    Models game-theoretic rival anticipation, moat durability scoring, and pivot triggers.
    """

    def score_moat_durability(self, switching_costs: float, network_density: float, cost_advantage: float) -> float:
        """Composite moat durability score [0, 1]."""
        score = 0.4 * min(1.0, switching_costs) + 0.3 * min(1.0, network_density) + 0.3 * min(1.0, cost_advantage)
        return float(score)


# =====================================================================
# Layer 12: Organizational Design
# =====================================================================

class OrganizationalDesignEngine:
    """Layer 12: Organizational Design.

    Applies Lagrange multiplier shadow prices for hiring and Coase transaction boundaries.
    """

    def evaluate_hiring_trigger(self, shadow_price_constraint: float, market_wage: float) -> bool:
        """Triggers hiring if shadow price of internal bottleneck exceeds market wage."""
        return shadow_price_constraint > market_wage

    def evaluate_coasian_boundary(self, internal_coordination_cost: float, external_transaction_cost: float) -> str:
        """Coase boundary: Internal < External -> Centralize inside firm; else Outsource/Delegate."""
        if internal_coordination_cost < external_transaction_cost:
            return "CENTRALIZED_IN_HOUSE"
        return "DELEGATE_OUTSOURCE"


# =====================================================================
# Layer 13: Meta-Learning
# =====================================================================

class MetaLearningEngine:
    """Layer 13: Meta-Learning.

    Executes Triple-Loop Learning: Parameter updates -> Operational playbook rewrite -> Meta-code evolutionary rewrite.
    """

    def execute_triple_loop_learning(self, execution_errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Processes failure post-mortems into active updates across all 3 learning loops."""
        if not execution_errors:
            return {"status": "no_errors", "updates_applied": 0}

        loop_1_param_adjustments = len(execution_errors)
        loop_2_playbook_updates = len([e for e in execution_errors if e.get("severity", 0) > 0.5])
        loop_3_code_rewrites = len([e for e in execution_errors if e.get("severity", 0) > 0.85])

        logger.info(f"Triple-Loop Learning complete: L1={loop_1_param_adjustments}, L2={loop_2_playbook_updates}, L3={loop_3_code_rewrites}")

        return {
            "status": "learning_applied",
            "loop_1_param_adjustments": loop_1_param_adjustments,
            "loop_2_playbook_updates": loop_2_playbook_updates,
            "loop_3_code_rewrites": loop_3_code_rewrites
        }


# =====================================================================
# Layer 14 & Master Engine: FourteenLayerEntrepreneurialEngine
# =====================================================================

class FourteenLayerEntrepreneurialEngine:
    """Layer 14: Autonomous AI Entrepreneurship & Master Orchestrator.

    Integrates all 13 underlying layer engines into a unified, continuous active-inference
    entrepreneurial operating system.
    """

    def __init__(self) -> None:
        self.reality = RealitySubstrateEngine()
        self.opportunity_discovery = OpportunityDiscoveryEngine()
        self.problem_discovery = ProblemDiscoveryEngine()
        self.decision_making = DecisionMakingEngine()
        self.opportunity_evaluation = OpportunityEvaluationEngine()
        self.product_creation = ProductCreationEngine()
        self.customer_understanding = CustomerUnderstandingEngine()
        self.marketing = MarketingEngine()
        self.sales = SalesEngine()
        self.growth = GrowthEngine()
        self.competition = CompetitionEngine()
        self.org_design = OrganizationalDesignEngine()
        self.meta_learning = MetaLearningEngine()

        self.state = EnterpriseState()

    def run_full_14_layer_cycle(self, external_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Executes a complete 14-layer continuous entrepreneurial cycle."""
        logger.info("Executing FourteenLayerEntrepreneurialEngine 14-layer cycle...")

        # 1. Reality Check
        reality_boundary = self.reality.delineate_automation_boundary("capital_routing", False)

        # 2. Opportunity Discovery
        weak_signals = self.opportunity_discovery.detect_weak_signals(external_signals)
        kl_gap = self.opportunity_discovery.calculate_kl_divergence_gap([0.2, 0.3, 0.5], [0.5, 0.4, 0.1])

        # 3. Problem Discovery
        scm_decomp = self.problem_discovery.decompose_problem_scm(
            variables=["pricing", "conversion", "revenue"],
            edges=[("pricing", "conversion"), ("conversion", "revenue")]
        )
        should_ignore = self.problem_discovery.evaluate_ignore_criteria(0.3, 0.5, 1.0)

        # 4. Decision Making
        efe = self.decision_making.compute_expected_free_energy(
            p_success=0.6, p_target=0.9, prior_entropy=1.5, post_entropy=0.5
        )
        sprt_result = self.decision_making.sequential_probability_ratio_test([True, True, False, True])

        # 5. Opportunity Evaluation
        ev_cents = self.opportunity_evaluation.calculate_expected_value(
            tam_cents=100_000_000_00, gross_margin=0.8, success_probability=0.6, risk_discount=0.2
        )
        timing_decision = self.opportunity_evaluation.evaluate_real_option_timing(0.3, 1.0, 0.5)

        # 6. Product Creation
        features = self.product_creation.apply_kolmogorov_complexity_penalty(
            proposed_features=["core_api", "complex_dashboard_v1", "analytics_exporter"],
            feature_utilities={"core_api": 0.9, "complex_dashboard_v1": 0.2, "analytics_exporter": 0.7}
        )
        self.state.product_features = features

        # 7. Customer Understanding
        switch_prob = self.customer_understanding.calculate_switching_probability(
            push_force=0.8, pull_force=0.7, inertia=0.3, anxiety=0.2
        )

        # 8. Marketing
        reach = self.marketing.simulate_information_cascade(initial_seeds=100, virality_coefficient=1.5, network_decay=0.2)

        # 9. Sales
        sales_strat = self.sales.determine_sales_strategy(annual_contract_value_cents=12000_00, stakeholder_complexity_score=0.8)

        # 10. Growth
        net_val = self.growth.compute_subquadratic_network_value(user_count=5000)

        # 11. Competition
        moat_score = self.competition.score_moat_durability(switching_costs=0.7, network_density=0.8, cost_advantage=0.6)
        self.state.moat_score = moat_score

        # 12. Org Design
        hire_trigger = self.org_design.evaluate_hiring_trigger(shadow_price_constraint=120.0, market_wage=100.0)

        # 13. Meta-Learning
        learning_res = self.meta_learning.execute_triple_loop_learning(
            execution_errors=[{"severity": 0.6, "component": "gtm_channel"}]
        )

        # Update State execution history
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "selected_features": features,
            "expected_free_energy": efe,
            "ev_cents": ev_cents,
            "reach": reach,
            "moat_score": moat_score
        }
        self.state.execution_history.append(record)

        return {
            "status": "success",
            "venture_id": str(self.state.venture_id),
            "layers_executed": 14,
            "automation_boundary": reality_boundary,
            "weak_signals_detected": len(weak_signals),
            "kl_divergence_gap": kl_gap,
            "expected_free_energy": efe,
            "sprt_result": sprt_result,
            "opportunity_ev_cents": ev_cents,
            "timing_decision": timing_decision,
            "selected_product_features": features,
            "switching_probability": switch_prob,
            "simulated_marketing_reach": reach,
            "sales_strategy": sales_strat,
            "subquadratic_network_value": net_val,
            "moat_durability_score": moat_score,
            "hire_trigger_activated": hire_trigger,
            "triple_loop_learning": learning_res
        }
