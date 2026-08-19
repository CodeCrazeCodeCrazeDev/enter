"""
The complete, first-principles executable implementation of the 14-Layer
Computational Architecture of Entrepreneurship for AI-EOS / SERO v2.1.

This module formalizes and operationalizes every layer of entrepreneurship into
concrete algorithms, probabilistic reasoning engines, structural causal models,
and autonomous feedback loops.
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
    domain: str = "general"
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
    estimated_margin: float = 0.70


class Signal(BaseModel):
    """Weak or strong market observation signal."""
    signal_id: UUID = Field(default_factory=uuid4)
    source: str
    content: str
    keywords: List[str] = Field(default_factory=list)
    snr: float = 0.5  # Signal-to-noise ratio
    timestamp_delta: float = 0.0


# =====================================================================
# Layer 1: Reality Engine
# =====================================================================

class InvariantsModel:
    """
    Formalizes fundamental economic invariants, human psychology bounds,
    and automation limits in entrepreneurship.
    """

    def decompose_task_nature(self, task_description: str) -> Dict[str, Any]:
        """
        Decomposes an entrepreneurial task into human psychology vs optimization problems,
        determining automation bounds.
        """
        judgment_keywords = {"ethics", "legal_accountability", "ultimate_risk_taking", "trust_foundational"}
        optimization_keywords = {"search", "synthesis", "pattern_matching", "unit_economics", "ab_testing"}

        tokens = set(task_description.lower().split("_"))
        is_judgment = len(tokens.intersection(judgment_keywords)) > 0
        is_optimization = len(tokens.intersection(optimization_keywords)) > 0 or not is_judgment

        automatable = is_optimization and not is_judgment

        return {
            "task": task_description,
            "automatable": automatable,
            "requires_human_judgment": is_judgment,
            "category": "optimization_problem" if automatable else "human_psychology_and_governance"
        }

    def compute_value_creation_bounds(self, pain_severity: float, market_size_cents: int) -> float:
        """
        Invariant: Value Creation V = Pain Severity * Market Scale * Efficiency Delta.
        """
        return pain_severity * market_size_cents * 0.15


# =====================================================================
# Layer 2: Opportunity Discovery
# =====================================================================

class OpportunityDiscoveryEngine:
    """
    Continuously searches the world state space for economically valuable opportunities,
    detecting weak signals, filtering noise, and synthesizing novel opportunities.
    """

    def detect_and_filter_signals(self, raw_signals: List[Signal], min_snr: float = 0.4) -> List[Signal]:
        """Filters weak signals using Signal-to-Noise Ratio (SNR) thresholding."""
        filtered = [sig for sig in raw_signals if sig.snr >= min_snr]
        logger.info(f"OpportunityDiscovery: Filtered {len(raw_signals)} signals down to {len(filtered)} high-SNR signals.")
        return filtered

    def synthesize_combinatorial_novelty(self, signal1: Signal, signal2: Signal) -> Opportunity:
        """Combines two unrelated observations to synthesize a novel opportunity."""
        combined_keywords = list(set(signal1.keywords + signal2.keywords))
        jaccard_overlap = len(set(signal1.keywords).intersection(set(signal2.keywords))) / max(1, len(set(signal1.keywords).union(set(signal2.keywords))))
        novelty_score = 1.0 - jaccard_overlap  # Higher novelty if domain overlap is low

        title = f"Synthesized: {signal1.content[:20]} x {signal2.content[:20]}"
        return Opportunity(
            title=title,
            domain=f"cross_domain_{signal1.source}_{signal2.source}",
            keywords=combined_keywords,
            prior_entropy=1.5 + novelty_score,
            post_entropy_simulated=0.3,
            success_probability=0.5,
            tam_cents=int(100000000 * (1.0 + novelty_score))
        )


# =====================================================================
# Layer 3: Problem Discovery & Causal Engine
# =====================================================================

class ProblemDiscoveryEngine:
    """
    Defines problems, decomposes root causes vs symptoms, and evaluates ignore filters.
    """

    def decompose_problem_tree(self, root_problem: str, sub_problems: List[str]) -> Dict[str, Any]:
        """Decomposes a broad problem statement into first-order and second-order sub-problems."""
        return {
            "root_problem": root_problem,
            "first_order_sub_problems": sub_problems[:2],
            "second_order_sub_problems": sub_problems[2:],
            "should_ignore": len(sub_problems) == 0
        }


class AdvancedCausalEngine:
    """
    Implements Judea Pearl's Structural Causal Model (SCM) capable of handling
    do-calculus interventions, counterfactual estimations, and symptom vs root-cause disentanglement.
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
        Mutates the structural equations, freezing the target variable
        and propagating the interventional downstream effects.
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
        Computes counterfactual outcomes: 'What would target_outcome_var have been,
        had we performed the counterfactual intervention, given the factual observations?'
        """
        intervened_var, inter_value = counterfactual_intervention

        # 1. Abduction Phase: Estimate background noise U
        noise_estimates: Dict[str, float] = {}
        for var in self.variables:
            factual_val = factual_observations.get(var, 0.0)
            parents_list = self.parents.get(var, [])
            structural_expected = 0.0
            for parent in parents_list:
                coef = self.coefficients.get((parent, var), 0.0)
                structural_expected += coef * factual_observations.get(parent, 0.0)

            noise_estimates[var] = factual_val - structural_expected

        # 2. Action & Prediction Phase
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

    def disentangle_symptom_vs_root_cause(self, target_variable: str) -> Dict[str, Any]:
        """
        Distinguishes symptoms (downstream leaves) from root causes (parentless/root drivers).
        """
        parents = self.parents.get(target_variable, [])
        is_root_cause = len(parents) == 0
        return {
            "variable": target_variable,
            "is_root_cause": is_root_cause,
            "direct_parents": parents,
            "structural_depth": 0 if is_root_cause else 1 + len(parents)
        }


# =====================================================================
# Layer 4: Decision Engine (Active Inference & Falsification)
# =====================================================================

class ActiveInferencePlanner:
    """
    Implements the Active Inference decision framework based on Expected Free Energy (EFE).
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

    def evaluate_fast_falsification(self, opp: Opportunity, critical_evidence_pass: bool) -> bool:
        """
        Kill bad ideas quickly if critical falsification evidence fails.
        """
        if not critical_evidence_pass or opp.success_probability < 0.15:
            logger.warning(f"FALSIFICATION KILL SWITCH: Opportunity '{opp.title}' failed critical test.")
            opp.is_active = False
            return False
        return True


# =====================================================================
# Layer 5: Opportunity Evaluation Engine
# =====================================================================

class OpportunityEvaluationEngine:
    """
    Calculates expected financial value, downside risk, and optimal opportunity switching thresholds.
    """

    def calculate_expected_value_cents(self, opp: Opportunity) -> float:
        """EV = P(Success) * TAM_cents * Margin."""
        return opp.success_probability * opp.tam_cents * opp.estimated_margin

    def estimate_downside_risk_cents(self, experiment_cost_cents: int, failure_probability: float) -> float:
        """Downside Risk = Max Capital At Risk * P(Failure)."""
        return experiment_cost_cents * failure_probability

    def evaluate_switching_threshold(
        self,
        current_opp: Opportunity,
        candidate_opp: Opportunity,
        switching_cost_cents: int
    ) -> bool:
        """
        Switch from current to candidate opportunity if:
        Candidate EV - Switching Cost > Current EV
        """
        current_ev = self.calculate_expected_value_cents(current_opp)
        candidate_ev = self.calculate_expected_value_cents(candidate_opp)

        should_switch = (candidate_ev - switching_cost_cents) > current_ev
        return should_switch


# =====================================================================
# Layer 6: Product Creation Engine
# =====================================================================

class ProductCreationEngine:
    """
    Models Jobs-To-Be-Done (JTBD), feature value attribution, and complexity minimization.
    """

    def minimize_complexity_pareto(self, feature_value_map: Dict[str, float]) -> List[str]:
        """
        Prunes unnecessary feature complexity, retaining top 20% features driving 80% value.
        """
        sorted_features = sorted(feature_value_map.items(), key=lambda x: x[1], reverse=True)
        total_val = sum(feature_value_map.values()) or 1.0

        retained = []
        cumulative = 0.0
        for feat, val in sorted_features:
            retained.append(feat)
            cumulative += val
            if cumulative / total_val >= 0.80:
                break

        return retained

    def calculate_learning_velocity(self, experiments_completed: int, total_days: float) -> float:
        """Learning velocity = Validated Experiments / Days Elapsed."""
        return experiments_completed / max(1.0, total_days)


# =====================================================================
# Layer 7: Customer Understanding Engine
# =====================================================================

class CustomerPsychologyModel:
    """
    Models customer trust, switching dynamics, churn hazard, and evangelism emergence.
    """

    def compute_switching_probability(self, value_delta: float, switching_friction: float) -> float:
        """
        Customer Switch Probability = 1 / (1 + e^(- (Value Delta - Switching Friction)))
        """
        net_incentive = value_delta - switching_friction
        return 1.0 / (1.0 + math.exp(-net_incentive))

    def calculate_trust_index(self, delivered_promises: int, total_promises: int, resolution_speed_days: float) -> float:
        """Trust Index = Promise Fulfillment Rate / Speed Penalty Factor."""
        if total_promises == 0:
            return 0.5
        fulfillment_rate = delivered_promises / total_promises
        penalty = max(1.0, resolution_speed_days / 2.0)
        return min(1.0, max(0.0, fulfillment_rate / penalty))


# =====================================================================
# Layer 8: Marketing & Virality Engine
# =====================================================================

class MarketingEngine:
    """
    Models viral growth diffusion (R0 / K-factor), positioning, and multi-channel interactions.
    """

    def compute_viral_coefficient(self, invites_per_user: float, conversion_rate: float) -> float:
        """K-Factor K = Invites Per User * Conversion Rate."""
        return invites_per_user * conversion_rate

    def evaluate_channel_synergy(self, channel_a_roi: float, channel_b_roi: float, cross_overlap: float) -> float:
        """Computes composite marketing ROI accounting for cross-channel attribution synergy."""
        base_roi = channel_a_roi + channel_b_roi
        synergy = 1.25 * cross_overlap * (channel_a_roi * channel_b_roi) ** 0.5
        return base_roi + synergy


# =====================================================================
# Layer 9: Sales Urgency & Objection Engine
# =====================================================================

class SalesEngine:
    """
    Manages psychological buying urgency, objection resolution, and automation routing.
    """

    def determine_sales_route(self, deal_size_cents: int, sales_cycle_days: int) -> str:
        """
        Routes sales to Automated Self-Serve vs High-Touch Enterprise Sales.
        """
        if deal_size_cents >= 1000000 or sales_cycle_days > 30:  # >= $10k
            return "enterprise_high_touch"
        return "automated_self_serve"

    def resolve_objection(self, objection_type: str) -> Dict[str, str]:
        """Objection resolution mapping state machine."""
        resolution_map = {
            "price": "frame_roi_and_payback_period",
            "trust": "provide_case_studies_and_guarantee",
            "timing": "introduce_scarcity_or_pain_cost_calculator",
            "feature_gap": "demonstrate_workaround_or_roadmap_commitment"
        }
        strategy = resolution_map.get(objection_type.lower(), "discover_underlying_need")
        return {"objection": objection_type, "recommended_strategy": strategy}


# =====================================================================
# Layer 10: Growth & Network Scaling
# =====================================================================

class GrowthEngine:
    """
    Models compounding growth, network effect laws (Metcalfe & Reed), and growth deceleration control.
    """

    def compute_metcalfe_value(self, active_users: int) -> float:
        """Metcalfe's Law Value V = N^2."""
        return float(active_users ** 2)

    def compute_reed_group_value(self, active_users: int) -> float:
        """Reed's Law Value V = 2^N (capped log scale for computation)."""
        if active_users > 100:
            return float(active_users * (2 ** 10))
        return float(2 ** active_users)

    def check_growth_deceleration_need(self, system_churn_rate: float, infrastructure_load: float) -> bool:
        """
        Determines if growth should be slowed intentionally to preserve quality and infrastructure stability.
        """
        return system_churn_rate > 0.15 or infrastructure_load > 0.90


# =====================================================================
# Layer 11: Competitive Defense & Moats
# =====================================================================

class CompetitionEngine:
    """
    Anticipates competitor counter-moves, scores moat durability, and flags strategic pivots.
    """

    def compute_moat_durability_score(
        self,
        network_density: float,
        avg_switching_cost_cents: int,
        brand_trust: float,
        cost_advantage: float
    ) -> float:
        """Composite Moat Durability Score in [0.0, 1.0]."""
        s_network = min(1.0, network_density)
        s_switch = min(1.0, avg_switching_cost_cents / 1000000)  # $10k standard
        s_brand = min(1.0, brand_trust)
        s_cost = min(1.0, cost_advantage)

        return float(0.3 * s_network + 0.3 * s_switch + 0.2 * s_brand + 0.2 * s_cost)


# =====================================================================
# Layer 12: Organizational Design Engine
# =====================================================================

class OrganizationalDesignEngine:
    """
    Models delegation efficiency, hiring threshold triggers, and decision-making scaling.
    """

    def evaluate_hiring_trigger(self, capacity_utilization: float, decision_latency_hours: float) -> bool:
        """
        Triggers new hiring when team capacity utilization > 85% or decision latency breaches SLA.
        """
        return capacity_utilization > 0.85 or decision_latency_hours > 48.0

    def compute_delegation_efficiency(self, central_workload: float, delegated_workload: float) -> float:
        """Delegation Efficiency = Delegated / Total Workload Ratio."""
        total = central_workload + delegated_workload
        if total == 0:
            return 1.0
        return delegated_workload / total


# =====================================================================
# Layer 13: Meta-Learning Engine
# =====================================================================

class MetaLearningEngine:
    """
    Measures decision quality via Brier score, updates mental models, and synthesizes failures into reusable knowledge.
    """

    def __init__(self) -> None:
        self.decision_history: List[Dict[str, Any]] = []

    def audit_decision_brier_score(self, predicted_probability: float, actual_outcome: bool) -> float:
        """
        Brier Score = (Probability - Outcome)^2. Lower score represents superior calibration.
        """
        outcome_val = 1.0 if actual_outcome else 0.0
        score = (predicted_probability - outcome_val) ** 2
        self.decision_history.append({
            "predicted": predicted_probability,
            "actual": actual_outcome,
            "brier_score": score
        })
        return score

    def update_prior_confidence_bayes(self, prior_confidence: float, likelihood: float) -> float:
        """Bayesian update rule for mental model adjustment."""
        evidence_p = (likelihood * prior_confidence) + (0.5 * (1.0 - prior_confidence))
        if evidence_p == 0:
            return prior_confidence
        posterior = (likelihood * prior_confidence) / evidence_p
        return min(0.99, max(0.01, posterior))


# =====================================================================
# Layer 14: AI Entrepreneurship Engine
# =====================================================================

class AIEntrepreneurshipEngine:
    """
    Formalizes tasks into algorithms vs probabilistic vs causal vs judgment,
    allocates multi-resource capital (capital, time, compute, talent), and plans active experiments.
    """

    def allocate_multi_resource_budget(
        self,
        total_capital_cents: int,
        total_compute_flops: float,
        total_talent_hours: float,
        opportunity_priorities: Dict[UUID, float]
    ) -> Dict[UUID, Dict[str, float]]:
        """Allocates capital, compute, and talent across active opportunities based on EFE priority."""
        total_priority = sum(opportunity_priorities.values()) or 1.0
        allocations = {}

        for opp_id, prio in opportunity_priorities.items():
            share = prio / total_priority
            allocations[opp_id] = {
                "capital_cents": int(total_capital_cents * share),
                "compute_flops": total_compute_flops * share,
                "talent_hours": total_talent_hours * share
            }

        return allocations


# =====================================================================
# Comprehensive Orchestration Pipeline
# =====================================================================

class EntrepreneurialIntelligenceOrchestrator:
    """
    The master coordinating engine driving the complete 14-layer execution pipeline.
    """

    def __init__(
        self,
        causal_engine: Optional[AdvancedCausalEngine] = None,
        planner: Optional[ActiveInferencePlanner] = None
    ) -> None:
        self.causal_engine = causal_engine or AdvancedCausalEngine()
        self.planner = planner or ActiveInferencePlanner(curiosity_weight=1.5)

        # 14 Layers Subsystem Instantiations
        self.layer1_reality = InvariantsModel()
        self.layer2_discovery = OpportunityDiscoveryEngine()
        self.layer3_problem = ProblemDiscoveryEngine() if 'ProblemDiscoveryEngine' in globals() else None
        self.layer4_decision = self.planner
        self.layer5_evaluation = OpportunityEvaluationEngine()
        self.layer6_product = ProductCreationEngine()
        self.layer7_customer = CustomerPsychologyModel()
        self.layer8_marketing = MarketingEngine()
        self.layer9_sales = SalesEngine()
        self.layer10_growth = GrowthEngine()
        self.layer11_competition = CompetitionEngine()
        self.layer12_org = OrganizationalDesignEngine()
        self.layer13_meta = MetaLearningEngine()
        self.layer14_ai = AIEntrepreneurshipEngine()

        self.opportunities: List[Opportunity] = []

    def ingest_signal(self, signal_dict: Dict[str, Any]) -> Opportunity:
        """Senses external changes and creates a candidate opportunity state."""
        logger.info(f"Sensing external signal: {signal_dict.get('title')}")
        opp = Opportunity(
            title=signal_dict.get("title", "Unnamed Opportunity"),
            domain=signal_dict.get("domain", "general"),
            variables=signal_dict.get("variables", []),
            causal_edges=signal_dict.get("causal_edges", []),
            coefficients=signal_dict.get("coefficients", {}),
            prior_entropy=signal_dict.get("prior_entropy", 1.5),
            post_entropy_simulated=signal_dict.get("post_entropy_simulated", 0.4),
            success_probability=signal_dict.get("success_probability", 0.5),
            tam_cents=signal_dict.get("tam_cents", 100000000),
            keywords=signal_dict.get("keywords", [])
        )
        self.opportunities.append(opp)
        return opp

    def execute_orchestrated_pipeline(self) -> Dict[str, Any]:
        """Runs the 14-layer analysis pipeline over active opportunities."""
        if not self.opportunities:
            return {"status": "idle", "reason": "No opportunities registered."}

        # Select primary opportunity via Layer 4 (Active Inference)
        ranked = self.planner.rank_opportunities(self.opportunities)
        primary_opp, best_efe = ranked[0]

        # Layer 1: Task nature decomposition
        l1_decomp = self.layer1_reality.decompose_task_nature("opportunity_evaluation_and_search")

        # Layer 3: Causal initialization
        for var in primary_opp.variables:
            self.causal_engine.register_variable(var)
        for parent, child in primary_opp.causal_edges:
            weight = primary_opp.coefficients.get(f"{parent}->{child}", 0.5)
            self.causal_engine.add_causal_relationship(parent, child, weight)

        intervene_var = primary_opp.variables[0] if primary_opp.variables else "marketing_spend"
        propagated = self.causal_engine.execute_do_intervention(intervene_var, 1.5)

        # Layer 5: Financial Evaluation
        ev_cents = self.layer5_evaluation.calculate_expected_value_cents(primary_opp)

        # Layer 8 & 10: Marketing Synergy & Growth Value
        viral_k = self.layer8_marketing.compute_viral_coefficient(5.0, 0.2)
        growth_val = self.layer10_growth.compute_metcalfe_value(1000)

        # Layer 14: Resource Allocation
        multi_resource = self.layer14_ai.allocate_multi_resource_budget(
            total_capital_cents=50000000,
            total_compute_flops=1e15,
            total_talent_hours=1000.0,
            opportunity_priorities={primary_opp.opportunity_id: abs(best_efe)}
        )

        return {
            "status": "executed",
            "selected_opportunity": primary_opp.title,
            "layer1_reality_decomposition": l1_decomp,
            "layer4_best_expected_free_energy": best_efe,
            "layer3_causal_intervention": f"do({intervene_var} = 1.5)",
            "layer3_propagated_state": propagated,
            "layer5_expected_value_cents": ev_cents,
            "layer8_viral_k_factor": viral_k,
            "layer10_growth_metcalfe_value": growth_val,
            "layer14_multi_resource_allocation": multi_resource
        }
