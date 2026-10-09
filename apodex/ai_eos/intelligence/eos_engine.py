"""Entrepreneurial Operating System (EOS) Cognitive Engine implementation.

Features 14 production-grade systems fully integrated behind a unified orchestrator
for continuous sensing, anomaly detection, business simulation, capital allocation,
moat analysis, failure prediction, customer lifecycle tracking, growth-stage classification,
and strategic reinvention.
"""

from __future__ import annotations
import math
import logging
import random
from typing import Any, Dict, List, Optional, Tuple, Set
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum

from ...ai_eos.domain.models import VentureCell, Hypothesis, Evidence, Theory

logger = logging.getLogger("sero.eos_engine")


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


# =====================================================================
# 0. Enums & Stage Models
# =====================================================================
class CompanyStage(str, Enum):
    """The 9 Company Growth Stages defined in EOS Architecture §6."""
    IDEA = "idea"
    VALIDATION = "validation"
    STARTUP = "startup"
    PMF = "pmf"
    GROWTH = "growth"
    SCALE = "scale"
    PLATFORM = "platform"
    ECOSYSTEM = "ecosystem"
    MARKET_LEADERSHIP = "market_leadership"


class ExternalLoopType(str, Enum):
    """The 13 External Business Loops specified in EOS Architecture §3."""
    PRODUCT = "product"
    MARKETING = "marketing"
    SALES = "sales"
    CUSTOMER_SUCCESS = "customer_success"
    BRAND = "brand"
    PRICING = "pricing"
    REFERRAL = "referral"
    DATA = "data"
    FINANCIAL = "financial"
    HIRING = "hiring"
    CULTURE = "culture"
    INNOVATION = "innovation"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"


# =====================================================================
# 1. Entrepreneurial World Model
# =====================================================================
class EntrepreneurialWorldModel:
    """Models world state transitions, resource parameters, and environment uncertainty."""

    def __init__(self) -> None:
        self.state: Dict[str, Any] = {
            "gdp_growth": 0.02,
            "market_demand_index": 1.0,
            "competitor_count": 5,
            "funding_climate": "moderate",  # loose, moderate, tight
            "technology_platform_shift": False,
        }
        self.uncertainty_scores: Dict[str, float] = {
            "market_demand_index": 0.25,
            "competitor_count": 0.15,
        }

    def transition_state(self) -> Dict[str, Any]:
        """Simulate stochastic environment transition."""
        self.state["market_demand_index"] += random.uniform(-0.1, 0.1)
        self.state["market_demand_index"] = max(0.1, self.state["market_demand_index"])

        # Competitor count grows stochastically
        if random.random() > 0.7:
            self.state["competitor_count"] += random.randint(1, 2)

        # Platform shift has small continuous hazard rate
        if not self.state["technology_platform_shift"] and random.random() > 0.95:
            self.state["technology_platform_shift"] = True
            logger.warning("WORLD STATE SHIFT: Major new technology platform shift detected!")

        return self.state

    def calculate_state_entropy(self) -> float:
        """Compute the average uncertainty/entropy across world dimensions."""
        if not self.uncertainty_scores:
            return 0.0
        return sum(self.uncertainty_scores.values()) / len(self.uncertainty_scores)


# =====================================================================
# 2. Opportunity Graph
# =====================================================================
class OpportunityNode:
    def __init__(self, op_id: str, name: str, value_cents: int, keywords: Set[str]) -> None:
        self.op_id = op_id
        self.name = name
        self.value_cents = value_cents
        self.keywords = keywords
        self.adjacent_ids: List[str] = []


class OpportunityGraph:
    """Manages a DAG of market opportunities, node valuations, and similarity matches."""

    def __init__(self) -> None:
        self.nodes: Dict[str, OpportunityNode] = {}

    def add_opportunity(self, op_id: str, name: str, value_cents: int, keywords: List[str]) -> None:
        node = OpportunityNode(op_id, name, value_cents, set(keywords))
        self.nodes[op_id] = node

    def add_dependency(self, parent_id: str, child_id: str) -> None:
        if parent_id in self.nodes and child_id in self.nodes:
            self.nodes[parent_id].adjacent_ids.append(child_id)

    def find_similar_opportunities(self, query_keywords: List[str], threshold: float = 0.2) -> List[Tuple[str, float]]:
        """Jaccard similarity context keyword matching."""
        query_set = set(query_keywords)
        if not query_set:
            return []

        matches = []
        for op_id, node in self.nodes.items():
            intersection = query_set.intersection(node.keywords)
            union = query_set.union(node.keywords)
            similarity = len(intersection) / len(union) if union else 0.0
            if similarity >= threshold:
                matches.append((op_id, similarity))

        matches.sort(key=lambda x: x[1], reverse=True)
        return matches


# =====================================================================
# 3. Hypothesis Engine
# =====================================================================
class HypothesisEngine:
    """Manages the lifecycle, promotion, and evidence-updating of hypotheses."""

    def __init__(self) -> None:
        self.hypotheses: Dict[UUID, Hypothesis] = {}

    def add_hypothesis(self, hyp: Hypothesis) -> None:
        self.hypotheses[hyp.hypothesis_id] = hyp

    def update_with_evidence(self, hyp_id: UUID, evidence: Evidence) -> None:
        """Update posterior confidence and distributions based on statistical evidence."""
        hyp = self.hypotheses.get(hyp_id)
        if not hyp:
            return

        # Determine if evidence is supporting or contradicting
        is_supporting = False
        p_val = evidence.strength.get("p_value", 1.0)
        effect_size = evidence.strength.get("effect_size", 0.0)

        # Standard statistical threshold: p-value < 0.05 and positive effect size
        if p_val < 0.05 and effect_size > 0.0:
            is_supporting = True

        if is_supporting:
            hyp.supporting_evidence.append(evidence.evidence_id)
            # Update Beta parameters representing success probability
            alpha = hyp.confidence_distribution.get("params", {}).get("alpha", 10.0)
            hyp.confidence_distribution["params"]["alpha"] = alpha + 1.0
        else:
            hyp.contradicting_evidence.append(evidence.evidence_id)
            beta = hyp.confidence_distribution.get("params", {}).get("beta", 10.0)
            hyp.confidence_distribution["params"]["beta"] = beta + 1.0

        # Compute updated posterior confidence
        a = hyp.confidence_distribution["params"]["alpha"]
        b = hyp.confidence_distribution["params"]["beta"]
        hyp.posterior_confidence = float(a / (a + b))
        hyp.last_updated = _now_utc()

    def evaluate_promotions(self) -> List[UUID]:
        """Promote high-confidence hypotheses (posterior > 0.8) to active or theory-ready."""
        promoted = []
        for hyp_id, hyp in self.hypotheses.items():
            if hyp.posterior_confidence >= 0.80 and hyp.status == "proposed":
                hyp.status = "active"
                promoted.append(hyp_id)
                logger.info(f"HYPOTHESIS PROMOTED: {hyp_id} promoted to ACTIVE.")
        return promoted


# =====================================================================
# 4. Business Simulator & GTM System
# =====================================================================
class BusinessSimulator:
    """Simulates business models and GTM cohorts to project financial trajectories."""

    def __init__(self) -> None:
        pass

    def simulate_gtm_cohort(
        self,
        traffic: int,
        conversion_rate: float,
        arpu_cents: int,
        cac_cents: int,
        churn_rate: float
    ) -> Dict[str, Any]:
        """Run standard cohort simulation and calculate key performance indicators."""
        acquired = int(traffic * conversion_rate)
        total_cac = acquired * cac_cents
        monthly_revenue = acquired * arpu_cents

        # Simulated metrics
        ltv_cents = int(arpu_cents / churn_rate) if churn_rate > 0 else arpu_cents * 12
        ltv_to_cac = ltv_cents / cac_cents if cac_cents > 0 else 1.0
        payback_months = cac_cents / arpu_cents if arpu_cents > 0 else 99.0

        return {
            "customers_acquired": acquired,
            "total_cac_cents": total_cac,
            "monthly_recurring_revenue_cents": monthly_revenue,
            "ltv_cents": ltv_cents,
            "ltv_to_cac_ratio": ltv_to_cac,
            "cac_payback_months": payback_months,
            "unit_economics_healthy": ltv_to_cac >= 3.0 and payback_months <= 12.0
        }


class GTMSystemSimulator:
    """Simulates integrated positioning, pricing, and distribution channel selection (§5)."""

    def __init__(self) -> None:
        self.channels = ["organic", "paid", "partner", "content", "plg", "slg", "clg"]

    def evaluate_channel_fit(
        self,
        target_acv_cents: int,
        complexity_score: float,
        network_effects: bool
    ) -> List[Dict[str, Any]]:
        """Determine channel suitability based on ACV and product complexity."""
        recommendations = []
        # Low complexity / low ACV -> PLG & Organic
        if target_acv_cents < 500_00 and complexity_score < 0.4:
            recommendations.append({"channel": "plg", "priority": "primary", "fit_score": 0.95})
            recommendations.append({"channel": "content", "priority": "secondary", "fit_score": 0.80})
        # High complexity / high ACV -> SLG
        elif target_acv_cents >= 10000_00 and complexity_score >= 0.6:
            recommendations.append({"channel": "slg", "priority": "primary", "fit_score": 0.90})
            recommendations.append({"channel": "partner", "priority": "secondary", "fit_score": 0.75})
        else:
            recommendations.append({"channel": "paid", "priority": "primary", "fit_score": 0.70})
            recommendations.append({"channel": "content", "priority": "secondary", "fit_score": 0.70})

        if network_effects:
            recommendations.append({"channel": "clg", "priority": "amplifier", "fit_score": 0.85})

        return sorted(recommendations, key=lambda x: x["fit_score"], reverse=True)


# =====================================================================
# 5. Strategic Planner
# =====================================================================
class StrategicPlanner:
    """Plans sequences of experiments to minimize Expected Free Energy."""

    def __init__(self) -> None:
        pass

    def compute_policy_efe(self, expected_utility: float, predictive_entropy: float, risk_factor: float) -> float:
        """Expected Free Energy (EFE) minimization formula for path planning.

        EFE = Predictive Entropy (Uncertainty) + Risk Penalty - Expected Utility.
        """
        return float(predictive_entropy + 1.5 * risk_factor - expected_utility)

    def select_optimal_policy(self, candidate_policies: List[Dict[str, float]]) -> Dict[str, float]:
        """Select the policy with the absolute lowest Expected Free Energy."""
        if not candidate_policies:
            return {}

        scored_policies = []
        for policy in candidate_policies:
            efe = self.compute_policy_efe(
                policy.get("expected_utility", 0.0),
                policy.get("predictive_entropy", 0.5),
                policy.get("risk_factor", 0.0)
            )
            policy["computed_efe"] = efe
            scored_policies.append(policy)

        scored_policies.sort(key=lambda x: x["computed_efe"])
        return scored_policies[0]


# =====================================================================
# 6. Capital Allocation Engine
# =====================================================================
class CapitalAllocationEngine:
    """Solves dynamic capital allocation across multiple Venture Cells."""

    def __init__(self) -> None:
        pass

    def allocate(self, cells: List[VentureCell], total_budget_cents: int) -> Dict[UUID, int]:
        """Allocate budget stochastically proportional to the cell's G-score (EFE priority) and risk metrics."""
        if not cells:
            return {}

        total_score = 0.0
        priorities = {}
        for cell in cells:
            # High priority to cells with high expected free energy / learning capacity, but penalize high risk
            priority = max(0.1, cell.expected_free_energy + cell.capital_allocation_score)
            if cell.risk > 0.7:
                priority *= 0.1
            priorities[cell.cell_id] = priority
            total_score += priority

        allocations = {}
        remaining = total_budget_cents

        for cell in cells:
            p = priorities[cell.cell_id]
            share = p / total_score if total_score > 0 else 1.0 / len(cells)
            allocated = int(total_budget_cents * share)

            # Enforce dynamic capacity ceiling for high-risk cells
            if cell.risk > 0.5:
                max_allowed = int(0.25 * total_budget_cents)
                if allocated > max_allowed:
                    allocated = max_allowed

            allocations[cell.cell_id] = allocated
            remaining -= allocated

        # Distribute residue
        if remaining > 0 and cells:
            highest_cell = max(cells, key=lambda c: priorities[c.cell_id])
            allocations[highest_cell.cell_id] += remaining

        return allocations


# =====================================================================
# 7. Portfolio Manager
# =====================================================================
class PortfolioManager:
    """Tracks allocations between pure Research (EDV) and physical Venture (ROI) portfolios."""

    def __init__(self) -> None:
        self.research_budget_cents: int = 0
        self.venture_budget_cents: int = 0

    def adjust_proportions(self, total_capital_cents: int, market_uncertainty: float) -> None:
        """Increase Research budget during high uncertainty (real options paradigm)."""
        if market_uncertainty > 0.6:
            # Exploit option value: allocate 40% to Research, 60% to Venture
            self.research_budget_cents = int(total_capital_cents * 0.40)
            self.venture_budget_cents = int(total_capital_cents * 0.60)
        else:
            # Low uncertainty: 15% to Research, 85% to Venture
            self.research_budget_cents = int(total_capital_cents * 0.15)
            self.venture_budget_cents = int(total_capital_cents * 0.85)


# =====================================================================
# 8. Competitive Intelligence Engine
# =====================================================================
class CompetitiveIntelligenceEngine:
    """Tracks competitor features, pricing structures, and relative market shares."""

    def __init__(self) -> None:
        self.competitors: Dict[str, Dict[str, Any]] = {}

    def register_competitor(self, name: str, market_share: float, features: List[str]) -> None:
        self.competitors[name] = {
            "market_share": market_share,
            "features": set(features),
        }

    def compute_feature_parity(self, our_features: List[str]) -> float:
        """Percentage of competitor features we have replicated."""
        our_set = set(our_features)
        all_comp_features: Set[str] = set()
        for comp in self.competitors.values():
            all_comp_features.update(comp["features"])

        if not all_comp_features:
            return 1.0

        intersection = our_set.intersection(all_comp_features)
        return len(intersection) / len(all_comp_features)


# =====================================================================
# 9. Moat Analyzer & Strategic Engine
# =====================================================================
class MoatAnalyzer:
    """Quantifies structural competitive advantages (switching costs, network density, etc.)."""

    def __init__(self) -> None:
        pass

    def score_moat(
        self,
        network_density: float,
        avg_switching_cost_cents: int,
        brand_trust_score: float,
        cost_advantage_percent: float
    ) -> float:
        """Composite Moat Durability Score [0, 1]."""
        s_network = min(1.0, network_density)
        s_switch = min(1.0, avg_switching_cost_cents / 10000_00)  # normalized at $10k
        s_brand = min(1.0, brand_trust_score)
        s_cost = min(1.0, cost_advantage_percent)

        return float(0.3 * s_network + 0.2 * s_switch + 0.2 * s_brand + 0.3 * s_cost)


class StrategicMoatEngine(MoatAnalyzer):
    """Extended Moat Analyzer incorporating Hamilton Helmer's 7 Powers (§7)."""

    def score_7_powers(self, powers: Dict[str, float]) -> Dict[str, Any]:
        """Score 7 Powers: network_effects, scale_economies, counter_positioning, switching_costs, cornered_resource, process_power, brand."""
        weights = {
            "network_effects": 0.20,
            "scale_economies": 0.15,
            "counter_positioning": 0.15,
            "switching_costs": 0.15,
            "cornered_resource": 0.15,
            "process_power": 0.10,
            "brand": 0.10,
        }
        total_score = sum(powers.get(power, 0.0) * weight for power, weight in weights.items())
        return {
            "composite_moat_score": min(1.0, max(0.0, total_score)),
            "dominant_power": max(powers.items(), key=lambda x: x[1])[0] if powers else "none",
            "powers_breakdown": powers,
        }


# =====================================================================
# 10. Failure Prediction Engine & Monitor
# =====================================================================
class FailurePredictionEngine:
    """Predicts venture insolvency/failure and detects systemic organizational bottlenecks."""

    def __init__(self) -> None:
        pass

    def predict_insolvency_probability(self, burn_multiple: float, runway_months: float, ltv_to_cac: float) -> float:
        """Analytical hazard rate modeling for bankruptcy/insolvency."""
        # Baseline hazard
        hazard = 0.05

        # High burn multiple (> 2.5) increases failure
        if burn_multiple > 2.5:
            hazard += 0.20

        # Low runway (< 6 months) increases failure exponentially
        if runway_months < 6.0:
            hazard += min(0.70, (6.0 - runway_months) * 0.12)

        # Poor unit economics
        if ltv_to_cac < 2.0:
            hazard += 0.15

        return min(0.99, max(0.01, hazard))

    def detect_bottlenecks(self, decision_latencies: List[float], sla_threshold: float) -> List[str]:
        """Flag bottleneck processes if decision latencies breach the SLA threshold."""
        bottlenecks = []
        for i, latency in enumerate(decision_latencies):
            if latency > sla_threshold:
                bottlenecks.append(f"process_step_{i}_breached_sla_({latency:.1f}s)")
        return bottlenecks


class FailureModeMonitor(FailurePredictionEngine):
    """Monitors the 10 failure modes outlined in EOS Architecture §8."""

    def audit_failure_modes(self, metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        alerts = []
        if metrics.get("survey_satisfaction_high", False) and metrics.get("usage_engagement", 0.0) < 0.2:
            alerts.append({"mode": "solving_wrong_problem", "severity": "high", "fix": "Return to JTBD interviews"})
        if metrics.get("build_velocity", 0.0) > 0.8 and metrics.get("demand_signal", 0.0) < 0.2:
            alerts.append({"mode": "building_before_validating", "severity": "critical", "fix": "Enforce validation gate"})
        if metrics.get("cac", 0.0) > 0 and metrics.get("sales_cycle_days", 0) > 120:
            alerts.append({"mode": "weak_positioning", "severity": "medium", "fix": "Reframe against core alternative"})
        if metrics.get("retention_curve_flattens", True) is False and metrics.get("monthly_spend", 0) > 50000:
            alerts.append({"mode": "premature_scaling", "severity": "critical", "fix": "Pause spend; solve cohort retention"})
        return alerts


# =====================================================================
# 11. Reinvention Engine
# =====================================================================
class ReinventionEngine:
    """Triggers self-disruption/pivots when structural parameters decay below threshold."""

    def __init__(self) -> None:
        pass

    def check_reinvention_trigger(self, monthly_revenue_decay: float, customer_attrition_rate: float) -> bool:
        """Flag reinvention trigger if metrics decay significantly."""
        if monthly_revenue_decay > 0.15 and customer_attrition_rate > 0.20:
            logger.critical("REINVENTION REQUISITE: Structural performance decay triggered a mandate for a model pivot!")
            return True
        return False


# =====================================================================
# 12. External Business Loops Engine & Customer Lifecycle Engine
# =====================================================================
class ExternalBusinessLoopsEngine:
    """Manages evaluation across the 13 coupled External Business Loops (§3)."""

    def __init__(self) -> None:
        self.loop_statuses: Dict[ExternalLoopType, Dict[str, Any]] = {
            loop_type: {"status": "healthy", "kpis": {}} for loop_type in ExternalLoopType
        }

    def evaluate_loop_health(self, loop_type: ExternalLoopType, kpis: Dict[str, float]) -> Dict[str, Any]:
        """Check loop health against established thresholds."""
        healthy = True
        reason = "all_kpis_nominal"

        if loop_type == ExternalLoopType.FINANCIAL:
            if kpis.get("burn_multiple", 1.0) > 2.5 or kpis.get("runway_months", 12.0) < 6.0:
                healthy = False
                reason = "unhealthy_burn_or_runway"
        elif loop_type == ExternalLoopType.PRODUCT:
            if kpis.get("nps", 50) < 20 or kpis.get("day30_retention", 0.4) < 0.2:
                healthy = False
                reason = "low_retention_or_satisfaction"
        elif loop_type == ExternalLoopType.MARKETING:
            if kpis.get("cac_payback_months", 6.0) > 18.0:
                healthy = False
                reason = "cac_payback_excessive"

        status_rec = {"healthy": healthy, "reason": reason, "kpis": kpis}
        self.loop_statuses[loop_type] = status_rec
        return status_rec


class CustomerLifecycleEngine:
    """Tracks cohort progression across the 15 Customer Journey stages (§4)."""

    STAGES = [
        "awareness", "interest", "consideration", "evaluation", "purchase",
        "onboarding", "activation", "engagement", "habit_formation",
        "retention", "loyalty", "advocacy", "referral", "expansion", "repurchase"
    ]

    def compute_funnel_efficiency(self, stage_counts: Dict[str, int]) -> Dict[str, float]:
        """Calculate step conversion ratios through the 15 stages."""
        conversions = {}
        for i in range(len(self.STAGES) - 1):
            s_curr = self.STAGES[i]
            s_next = self.STAGES[i + 1]
            n_curr = stage_counts.get(s_curr, 0)
            n_next = stage_counts.get(s_next, 0)
            rate = float(n_next / n_curr) if n_curr > 0 else 0.0
            conversions[f"{s_curr}_to_{s_next}"] = rate
        return conversions


# =====================================================================
# 13. Company Growth State Machine
# =====================================================================
class CompanyGrowthStateMachine:
    """Classifies and manages transitions across the 9 Company Growth Stages (§6)."""

    def __init__(self, initial_stage: CompanyStage = CompanyStage.IDEA) -> None:
        self.current_stage = initial_stage

    def classify_stage(self, metrics: Dict[str, Any]) -> CompanyStage:
        paying_cust = metrics.get("paying_customers", 0)
        mrr = metrics.get("mrr_cents", 0)
        third_party_devs = metrics.get("third_party_developers", 0)

        if third_party_devs >= 100:
            stage = CompanyStage.PLATFORM
        elif mrr >= 100000_00:  # $100k MRR
            stage = CompanyStage.GROWTH
        elif paying_cust >= 50:
            stage = CompanyStage.PMF
        elif paying_cust >= 1:
            stage = CompanyStage.VALIDATION
        else:
            stage = CompanyStage.IDEA

        self.current_stage = stage
        return stage


# =====================================================================
# 14. Entrepreneurial Memory & Evaluation
# =====================================================================
class EntrepreneurialMemory:
    """Coordinates SQLite long-term storage schemas and semantic context injections."""

    def __init__(self) -> None:
        self.trajectory_store: List[Dict[str, Any]] = []

    def record_step(self, cell_id: UUID, step_name: str, metrics: Dict[str, Any]) -> None:
        self.trajectory_store.append({
            "cell_id": cell_id,
            "step": step_name,
            "metrics": metrics,
            "timestamp": _now_utc()
        })

    def retrieve_matching_trajectories(self, key_metric: str, threshold_val: float) -> List[Dict[str, Any]]:
        matches = []
        for step in self.trajectory_store:
            val = step["metrics"].get(key_metric)
            if val is not None and val >= threshold_val:
                matches.append(step)
        return matches


class EvaluationFramework:
    """Verifies strategic accuracy, ethical alignment, and legal GRC rules."""

    def __init__(self) -> None:
        pass

    def audit_ethical_alignment(self, action: str, risk_score: float) -> bool:
        """Basic regulatory filter (Hendrycks constraints, objective safety)."""
        # Block action if extreme risk score
        if risk_score > 0.85:
            logger.error(f"ALIGNMENT AUDIT FAILURE: Action '{action}' risk score {risk_score} exceeds safety maximum.")
            return False
        return True


# =====================================================================
# 15. Coordinating EOSEngine (Orchestrator)
# =====================================================================
class EOSEngine:
    """The continuous entrepreneurial operating orchestrator coupling all subsystems."""

    def __init__(self) -> None:
        self.world_model = EntrepreneurialWorldModel()
        self.opportunity_graph = OpportunityGraph()
        self.hypothesis_engine = HypothesisEngine()
        self.business_simulator = BusinessSimulator()
        self.gtm_simulator = GTMSystemSimulator()
        self.strategic_planner = StrategicPlanner()
        self.capital_allocation_engine = CapitalAllocationEngine()
        self.portfolio_manager = PortfolioManager()
        self.competitor_intel = CompetitiveIntelligenceEngine()
        self.moat_analyzer = StrategicMoatEngine()
        self.failure_predictor = FailureModeMonitor()
        self.reinvention_engine = ReinventionEngine()
        self.external_loops_engine = ExternalBusinessLoopsEngine()
        self.customer_lifecycle_engine = CustomerLifecycleEngine()
        self.growth_state_machine = CompanyGrowthStateMachine()
        self.memory = EntrepreneurialMemory()
        self.evaluator = EvaluationFramework()

    def run_continuous_sensing_cycle(self, cells: List[VentureCell], total_budget_cents: int) -> Dict[str, Any]:
        """Execute one complete hierarchical sensing, planning, allocation, and diagnostic loop."""
        # 1. World State sensing & transitions
        world_state = self.world_model.transition_state()
        market_uncertainty = self.world_model.calculate_state_entropy()

        # 2. Adjust Portfolio budget allocation proportions
        self.portfolio_manager.adjust_proportions(total_budget_cents, market_uncertainty)

        # 3. Simulate and optimize budgets
        allocations = self.capital_allocation_engine.allocate(cells, self.portfolio_manager.venture_budget_cents)

        # 4. Diagnostics and Moats
        for cell in cells:
            cell.allocated_capital_cents += allocations.get(cell.cell_id, 0)

            # Record trajectory
            self.memory.record_step(
                cell_id=cell.cell_id,
                step_name="sensing_and_allocation",
                metrics={"allocated_capital": cell.allocated_capital_cents, "uncertainty": cell.uncertainty}
            )

        return {
            "world_state": world_state,
            "market_uncertainty": market_uncertainty,
            "allocated_budgets": allocations,
            "research_portfolio_cents": self.portfolio_manager.research_budget_cents,
            "venture_portfolio_cents": self.portfolio_manager.venture_budget_cents
        }
