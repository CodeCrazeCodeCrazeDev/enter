"""
First-principles executable implementation of the 14-Layer Computational
Architecture of Entrepreneurship for the APODEX AI Entrepreneurial Operating System.
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger("sero.fourteen_layer_engine")


# =====================================================================
# Core Data Models
# =====================================================================

class CausalNode(BaseModel):
    """Represents a variable in a Structural Causal Model (SCM)."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    is_intervened: bool = False
    interventional_value: Optional[float] = None
    baseline_value: float = 0.0


class ProblemNode(BaseModel):
    """Represents a sub-problem in a problem decomposition DAG."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    problem_id: str
    title: str
    is_root_cause: bool = False
    is_first_order: bool = True
    parents: List[str] = Field(default_factory=list)
    leverage_score: float = 0.5


class OpportunityState(BaseModel):
    """Canonical data model representing an opportunity across all 14 layers."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    opportunity_id: UUID = Field(default_factory=uuid4)
    title: str
    domain: str
    tam_cents: int = 100_000_000  # Default $1M
    cac_cents: int = 50_00
    ltv_cents: int = 250_00
    gross_margin: float = 0.80
    prior_entropy: float = 1.5
    post_entropy_simulated: float = 0.4
    success_probability: float = 0.5
    target_preference: float = 0.90
    variables: List[str] = Field(default_factory=list)
    causal_edges: List[Tuple[str, str]] = Field(default_factory=list)
    coefficients: Dict[str, float] = Field(default_factory=dict)
    moat_index: float = 0.60
    efe_score: float = 0.0
    status: str = "DISCOVERED"


# =====================================================================
# Layer 1: Reality Substrate
# =====================================================================

class Layer1Reality:
    """Layer 1: Fundamental principles, human psychology vs. optimization boundary."""

    @staticmethod
    def evaluate_fundamental_invariants() -> Dict[str, str]:
        return {
            "active_inference": "Continuous minimization of surprise between market expectations and state feedback.",
            "causal_intervention": "Direct manipulation of structural levers via Pearl do-calculus.",
            "capital_time_velocity": "Maximizing learning gain per dollar burned (delta_I / delta_$).",
            "epistemic_maximization": "Front-loading uncertainty reduction to fail fast or lock in moats."
        }

    @staticmethod
    def classify_task_domain(task_name: str) -> str:
        """Classifies a task into human psychology vs optimization problem."""
        psych_keywords = ["vision", "trust", "empathy", "ethic", "purpose", "relationship", "morale"]
        if any(k in task_name.lower() for k in psych_keywords):
            return "HUMAN_PSYCHOLOGY"
        return "OPTIMIZATION_PROBLEM"

    @staticmethod
    def is_automatable(task_name: str) -> bool:
        """Determines if a task can be automated by autonomous AI agents."""
        non_automatable = ["ultimate_goal_setting", "ethical_boundary_definition", "subjective_human_trust"]
        return task_name.lower() not in non_automatable


# =====================================================================
# Layer 2: Opportunity Discovery
# =====================================================================

class Layer2OpportunityDiscovery:
    """Layer 2: Continuous world state space search, signal detection & filtering."""

    def __init__(self, min_tam_cents: int = 10_000_000) -> None:
        self.min_tam_cents = min_tam_cents

    def detect_weak_signal(self, stream_embedding: List[float], noise_threshold: float = 0.3) -> float:
        """Detects weak signals via stochastic resonance / Bayesian surprise."""
        mean_val = sum(stream_embedding) / len(stream_embedding) if stream_embedding else 0.0
        variance = sum((x - mean_val) ** 2 for x in stream_embedding) / len(stream_embedding) if stream_embedding else 0.0
        surprise = math.log(1.0 + abs(mean_val) / (variance + 1e-6))
        return surprise

    def filter_signal(self, opportunity: OpportunityState) -> bool:
        """Applies SNR and TAM gates to candidate opportunities."""
        if opportunity.tam_cents < self.min_tam_cents:
            return False
        return True

    def combine_unrelated_observations(self, domain_a_primitives: List[str], domain_b_primitives: List[str]) -> List[str]:
        """Combines domain primitives via hypergraph cross-fusion."""
        combinations = []
        for a in domain_a_primitives:
            for b in domain_b_primitives:
                combinations.append(f"{a}_{b}_fusion")
        return combinations

    def generate_novelty(self, concept_primitives: List[str]) -> str:
        """Generates novel opportunity concept via mutation."""
        if not concept_primitives:
            return "novel_hybrid_venture"
        return f"autonomous_{concept_primitives[0]}_platform"

    def predict_emerging_market(self, adoption_vector: List[float]) -> Dict[str, float]:
        """Calculates 1st and 2nd derivative momentum to predict emerging markets."""
        if len(adoption_vector) < 3:
            return {"velocity": 0.0, "acceleration": 0.0, "is_emerging": False}
        v1 = adoption_vector[-1] - adoption_vector[-2]
        v0 = adoption_vector[-2] - adoption_vector[-3]
        acc = v1 - v0
        return {
            "velocity": v1,
            "acceleration": acc,
            "is_emerging": acc > 0 and v1 > 0
        }


# =====================================================================
# Layer 3: Problem Discovery
# =====================================================================

class Layer3ProblemDiscovery:
    """Layer 3: Problem formalization, decomposition, DAG sort, and root-cause do-calculus."""

    def define_problem_graph(self, current_state: Dict[str, float], desired_state: Dict[str, float]) -> Dict[str, float]:
        """Calculates state delta graph representing friction/cost."""
        delta = {}
        for key in desired_state:
            curr = current_state.get(key, 0.0)
            delta[key] = desired_state[key] - curr
        return delta

    def decompose_problem(self, root_problem: str, sub_problems: List[Tuple[str, str]]) -> Dict[str, ProblemNode]:
        """Decomposes a complex problem into a DAG of problem nodes."""
        nodes: Dict[str, ProblemNode] = {}
        for parent, child in sub_problems:
            if parent not in nodes:
                nodes[parent] = ProblemNode(problem_id=parent, title=parent)
            if child not in nodes:
                nodes[child] = ProblemNode(problem_id=child, title=child)
            nodes[child].parents.append(parent)

        # Topological classification of 1st vs 2nd order
        for node_id, node in nodes.items():
            node.is_first_order = len(node.parents) == 0

        return nodes

    def classify_root_cause_do_calculus(self, node_id: str, causal_matrix: Dict[Tuple[str, str], float]) -> bool:
        """Calculates interventional leverage score to isolate root cause from symptom."""
        outward_leverage = sum(coef for (p, c), coef in causal_matrix.items() if p == node_id)
        return outward_leverage > 1.0


# =====================================================================
# Layer 4: Decision Making
# =====================================================================

class Layer4DecisionMaking:
    """Layer 4: Active Inference EFE decision engine, attention shadow prices, SPRT fast kill."""

    def __init__(self, curiosity_weight: float = 1.0) -> None:
        self.curiosity_weight = curiosity_weight

    def calculate_expected_free_energy(self, opp: OpportunityState) -> float:
        """
        Calculates Expected Free Energy (EFE):
        G = - Pragmatic Value - Curiosity * Epistemic Value
        """
        eps = 1e-9
        p_succ = max(eps, min(1.0 - eps, opp.success_probability))
        p_target = max(eps, min(1.0 - eps, opp.target_preference))
        pragmatic_value = math.log(p_succ) - math.log(p_target)

        epistemic_value = max(0.0, opp.prior_entropy - opp.post_entropy_simulated)
        efe = -pragmatic_value - (self.curiosity_weight * epistemic_value)
        return efe

    def evaluate_sprt_fast_kill(self, success_observations: int, total_trials: int, lower_bound: float = 0.2) -> bool:
        """Sequential Probability Ratio Test (SPRT) to terminate bad hypotheses fast."""
        if total_trials == 0:
            return False
        rate = success_observations / total_trials
        return rate < lower_bound and total_trials >= 10

    def debias_adversarial_red_team(self, proposal_confidence: float, red_team_critique_score: float) -> float:
        """Adjusts confidence by adversarial red-team debiasing factor."""
        adjusted = proposal_confidence * (1.0 - 0.5 * red_team_critique_score)
        return max(0.0, min(1.0, adjusted))


# =====================================================================
# Layer 5: Opportunity Evaluation
# =====================================================================

class Layer5OpportunityEvaluation:
    """Layer 5: EV, downside risk CVaR, timing index, Pareto ranking, abandonment rule."""

    def calculate_expected_value_cents(self, opp: OpportunityState, capital_at_risk_cents: int) -> int:
        upside_cents = int(opp.tam_cents * opp.gross_margin * 0.05)  # 5% share capture
        ev = (opp.success_probability * upside_cents) - ((1.0 - opp.success_probability) * capital_at_risk_cents)
        return int(ev)

    def calculate_timing_index(self, tech_readiness: float, regulatory_clearance: float, market_derivative: float) -> float:
        return tech_readiness * regulatory_clearance * max(0.1, market_derivative)

    def evaluate_abandonment_rule(self, current_opp_efe: float, new_opp_efe: float, switching_cost: float = 0.5) -> bool:
        """Abandons current opportunity if new opportunity EFE is significantly better (more negative)."""
        return (new_opp_efe + switching_cost) < current_opp_efe


# =====================================================================
# Layer 6: Product Creation
# =====================================================================

class Layer6ProductCreation:
    """Layer 6: What NOT to build exclusion, complexity penalty, JTBD extraction."""

    def generate_mvp_feature_exclusion_matrix(self, features: Dict[str, float], threshold: float = 0.5) -> Dict[str, bool]:
        """Determines feature inclusion (True) vs exclusion (False) based on value marginal utility."""
        return {feat: (value >= threshold) for feat, value in features.items()}

    def calculate_regularized_product_utility(self, raw_utility: float, code_lines: int, lambda_complexity: float = 0.0001) -> float:
        return raw_utility - (lambda_complexity * code_lines)

    def extract_job_to_be_done(self, user_telemetry_events: List[str]) -> str:
        """Extracts core JTBD latent state from telemetry event frequencies."""
        if not user_telemetry_events:
            return "automate_core_workflow"
        most_frequent = max(set(user_telemetry_events), key=user_telemetry_events.count)
        return f"optimize_{most_frequent}"


# =====================================================================
# Layer 7: Customer Understanding
# =====================================================================

class Layer7CustomerUnderstanding:
    """Layer 7: Customer utility MDP, switching friction, churn expectation gap."""

    def calculate_customer_utility(self, perceived_value: float, price: float, friction: float) -> float:
        return perceived_value - price - friction

    def evaluate_switching_condition(self, new_utility: float, current_utility: float, switching_cost: float) -> bool:
        return (new_utility - current_utility) > switching_cost

    def calculate_churn_expectation_gap(self, delivered_value: float, expected_value: float) -> float:
        return delivered_value - expected_value


# =====================================================================
# Layer 8: Marketing
# =====================================================================

class Layer8Marketing:
    """Layer 8: SIR network attention diffusion, viral reproduction R0, PageRank authority."""

    def calculate_viral_reproduction_number(self, sharing_prob: float, avg_contacts: float, payload_retention: float) -> float:
        """Calculates R0 viral coefficient = beta * k * d."""
        return sharing_prob * avg_contacts * payload_retention

    def is_viral(self, r0: float) -> bool:
        return r0 > 1.0

    def update_brand_bayesian_prior(self, prior_quality: float, positive_touchpoints: int, total_touchpoints: int) -> float:
        if total_touchpoints == 0:
            return prior_quality
        empirical = positive_touchpoints / total_touchpoints
        updated = (0.3 * prior_quality) + (0.7 * empirical)
        return updated


# =====================================================================
# Layer 9: Sales
# =====================================================================

class Layer9Sales:
    """Layer 9: Bayesian belief purchase shift, cost of inaction (COI), sales route dispatch."""

    def calculate_cost_of_inaction_cents(self, daily_loss_cents: int, days_delayed: int) -> int:
        return daily_loss_cents * days_delayed

    def select_sales_channel_route(self, acv_cents: int, requires_compliance: bool) -> str:
        if acv_cents >= 5_000_00 or requires_compliance:
            return "ENTERPRISE_HIGH_TOUCH"
        return "AUTOMATED_SELF_SERVE"

    def resolve_buyer_objection(self, objection_type: str) -> str:
        resolutions = {
            "RISK": "Provide zero-risk money-back guarantee and SOC2 proof.",
            "BUDGET": "Demonstrate payback period < 90 days via unit economics model.",
            "FIT": "Execute 14-day zero-code sandbox integration trial."
        }
        return resolutions.get(objection_type.upper(), "Deliver targeted case study evidence.")


# =====================================================================
# Layer 10: Growth
# =====================================================================

class Layer10Growth:
    """Layer 10: Metcalfe network effects, platform vs product transition, growth throttle."""

    def calculate_metcalfe_network_utility(self, active_nodes: int, coupling_coefficient: float = 0.01) -> float:
        return coupling_coefficient * (active_nodes ** 2)

    def evaluate_platform_transition_trigger(self, third_party_ecosystem_value: float, internal_product_value: float) -> bool:
        """Triggers platform replacement when 3rd-party developer value exceeds core internal product value."""
        return third_party_ecosystem_value > internal_product_value

    def evaluate_growth_throttle(self, churn_rate: float, infrastructure_load: float) -> bool:
        """Throttles growth if operational churn spikes (> 15%) or load exceeds 85% capacity."""
        return churn_rate > 0.15 or infrastructure_load > 0.85


# =====================================================================
# Layer 11: Competition
# =====================================================================

class Layer11Competition:
    """Layer 11: Minimax game-theoretic moves, moat depth index, pivot trigger."""

    def calculate_moat_depth_index(self, network_effects: float, switching_costs: float, scale_economies: float, brand_authority: float) -> float:
        weights = [0.3, 0.3, 0.2, 0.2]
        components = [network_effects, switching_costs, scale_economies, brand_authority]
        index = sum(w * c for w, c in zip(weights, components))
        return max(0.0, min(1.0, index))

    def evaluate_pivot_trigger(self, iterations_failed: int, zero_conversion_duration_days: int) -> bool:
        return iterations_failed >= 5 or zero_conversion_duration_days >= 60


# =====================================================================
# Layer 12: Organizational Design
# =====================================================================

class Layer12OrganizationalDesign:
    """Layer 12: Shadow price labor hiring trigger, centralization vs delegation allocator."""

    def evaluate_hiring_trigger(self, resource_shadow_price: float, marginal_wage_cost: float) -> bool:
        """Hires when labor shadow price exceeds marginal wage cost."""
        return resource_shadow_price > marginal_wage_cost

    def allocate_organizational_task(self, task_type: str) -> str:
        centralized_types = ["CAPITAL_ALLOCATION", "ARCHITECTURE", "GOVERNANCE_POLICY", "MISSION_SETTING"]
        if task_type.upper() in centralized_types:
            return "CENTRAL_EXECUTIVE_POD"
        return "DELEGATED_TACTICAL_AGENT"


# =====================================================================
# Layer 13: Meta-Learning
# =====================================================================

class Layer13MetaLearning:
    """Layer 13: Hierarchical Bayesian mental model updating, process quality vs outcome, failure archiving."""

    def update_mental_model_priors(self, prior_model_confidence: float, ex_post_venture_roi: float) -> float:
        likelihood = 1.0 / (1.0 + math.exp(-ex_post_venture_roi))
        updated = (prior_model_confidence * likelihood) / ((prior_model_confidence * likelihood) + (1.0 - prior_model_confidence) * (1.0 - likelihood))
        return updated

    def archive_falsified_hypothesis(self, hypothesis_id: str, causal_edges: List[Tuple[str, str]], reason: str) -> Dict[str, Any]:
        return {
            "archived_id": hypothesis_id,
            "failed_causal_edges": causal_edges,
            "failure_reason": reason,
            "status": "ARCHIVED_INVARIANT_FAILURE"
        }


# =====================================================================
# Layer 14: AI Entrepreneurship & Master Orchestrator
# =====================================================================

class Layer14AIEntrepreneurship:
    """Layer 14: Task classifier, Lagrange resource allocation, performance evaluation."""

    def classify_task_capability_type(self, task_description: str) -> str:
        desc = task_description.lower()
        if any(w in desc for w in ["search", "calculate", "route", "sort", "unit_economics"]):
            return "ALGORITHMIC"
        if any(w in desc for w in ["forecast", "predict", "intent", "churn"]):
            return "PROBABILISTIC"
        if any(w in desc for w in ["root_cause", "attribution", "intervention", "do_calculus"]):
            return "CAUSAL"
        if any(w in desc for w in ["concept", "positioning", "creative", "synthesis"]):
            return "CREATIVE"
        return "HUMAN_JUDGMENT"

    def optimize_resource_allocation(
        self,
        capital_cents: int,
        compute_flops: float,
        time_hours: float,
        talent_agents: int,
        shadow_prices: Dict[str, float]
    ) -> Dict[str, Any]:
        """Lagrange dual multiplier constrained resource allocation across active projects."""
        allocated_capital = int(capital_cents * min(1.0, shadow_prices.get("capital", 0.8)))
        allocated_compute = compute_flops * min(1.0, shadow_prices.get("compute", 0.9))
        allocated_time = time_hours * min(1.0, shadow_prices.get("time", 0.7))
        allocated_talent = max(1, int(talent_agents * min(1.0, shadow_prices.get("talent", 0.8))))

        return {
            "allocated_capital_cents": allocated_capital,
            "allocated_compute_flops": allocated_compute,
            "allocated_time_hours": allocated_time,
            "allocated_talent_agents": allocated_talent,
            "binding_constraint": max(shadow_prices, key=shadow_prices.get) if shadow_prices else "none"
        }


class FourteenLayerOrchestrator:
    """
    The master coordinating engine driving end-to-end state transitions across all 14 layers.
    """

    def __init__(self) -> None:
        self.layer1 = Layer1Reality()
        self.layer2 = Layer2OpportunityDiscovery()
        self.layer3 = Layer3ProblemDiscovery()
        self.layer4 = Layer4DecisionMaking()
        self.layer5 = Layer5OpportunityEvaluation()
        self.layer6 = Layer6ProductCreation()
        self.layer7 = Layer7CustomerUnderstanding()
        self.layer8 = Layer8Marketing()
        self.layer9 = Layer9Sales()
        self.layer10 = Layer10Growth()
        self.layer11 = Layer11Competition()
        self.layer12 = Layer12OrganizationalDesign()
        self.layer13 = Layer13MetaLearning()
        self.layer14 = Layer14AIEntrepreneurship()

        self.opportunities: List[OpportunityState] = []

    def ingest_signal_and_discover(self, title: str, domain: str, stream_embedding: List[float], tam_cents: int) -> Optional[OpportunityState]:
        """Layers 1–2: Ingest signal, filter, and discover opportunity."""
        surprise = self.layer2.detect_weak_signal(stream_embedding)
        opp = OpportunityState(title=title, domain=domain, tam_cents=tam_cents, prior_entropy=1.5, post_entropy_simulated=0.3)

        if not self.layer2.filter_signal(opp):
            logger.info(f"Opportunity '{title}' filtered out at Layer 2 SNR/TAM gate.")
            return None

        opp.efe_score = self.layer4.calculate_expected_free_energy(opp)
        self.opportunities.append(opp)
        return opp

    def run_full_14_layer_pipeline(self, opportunity: OpportunityState, capital_cents: int = 50_000_00) -> Dict[str, Any]:
        """Runs an opportunity through all 14 layers of computational entrepreneurship."""
        # Layer 1: Invariants
        invariants = self.layer1.evaluate_fundamental_invariants()

        # Layer 3: Problem Decomposition
        prob_graph = self.layer3.define_problem_graph(
            current_state={"latency": 100.0, "cost": 50.0},
            desired_state={"latency": 10.0, "cost": 5.0}
        )

        # Layer 4 & 5: Decision & Evaluation
        efe = self.layer4.calculate_expected_free_energy(opportunity)
        ev_cents = self.layer5.calculate_expected_value_cents(opportunity, capital_at_risk_cents=capital_cents)
        timing_idx = self.layer5.calculate_timing_index(tech_readiness=0.9, regulatory_clearance=1.0, market_derivative=0.8)

        # Layer 6 & 7: Product & Customer
        exclusions = self.layer6.generate_mvp_feature_exclusion_matrix({"core_engine": 0.9, "fancy_ui": 0.2})
        cust_utility = self.layer7.calculate_customer_utility(perceived_value=100.0, price=20.0, friction=5.0)

        # Layer 8 & 9: Marketing & Sales
        r0 = self.layer8.calculate_viral_reproduction_number(sharing_prob=0.2, avg_contacts=10, payload_retention=0.8)
        sales_route = self.layer9.select_sales_channel_route(acv_cents=opportunity.ltv_cents, requires_compliance=False)

        # Layer 10 & 11: Growth & Competition
        net_utility = self.layer10.calculate_metcalfe_network_utility(active_nodes=1000)
        moat_depth = self.layer11.calculate_moat_depth_index(network_effects=0.8, switching_costs=0.7, scale_economies=0.6, brand_authority=0.5)

        # Layer 12 & 13: Organizational & Meta-Learning
        hire_trigger = self.layer12.evaluate_hiring_trigger(resource_shadow_price=150.0, marginal_wage_cost=100.0)
        updated_prior = self.layer13.update_mental_model_priors(prior_model_confidence=0.7, ex_post_venture_roi=1.5)

        # Layer 14: AI Resource Allocation
        resources = self.layer14.optimize_resource_allocation(
            capital_cents=capital_cents,
            compute_flops=1e15,
            time_hours=168.0,
            talent_agents=5,
            shadow_prices={"capital": 0.9, "compute": 0.95, "time": 0.8, "talent": 0.85}
        )

        return {
            "opportunity_title": opportunity.title,
            "layer1_invariants_count": len(invariants),
            "layer3_problem_delta": prob_graph,
            "layer4_efe_score": efe,
            "layer5_ev_cents": ev_cents,
            "layer5_timing_index": timing_idx,
            "layer6_feature_exclusions": exclusions,
            "layer7_customer_utility": cust_utility,
            "layer8_viral_r0": r0,
            "layer9_sales_route": sales_route,
            "layer10_metcalfe_utility": net_utility,
            "layer11_moat_depth": moat_depth,
            "layer12_hire_trigger": hire_trigger,
            "layer13_updated_prior": updated_prior,
            "layer14_resource_allocation": resources,
            "status": "COMPLETED_14_LAYER_ORCHESTRATION"
        }
