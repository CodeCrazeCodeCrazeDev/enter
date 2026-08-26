"""Entrepreneurial Operating System (EOS) - First-Principles Reconstruction Engine.

Implements the executable domain architecture for sensing, building, and compounding
enduring companies, based on:
- 3 Loop Timescales (Fast, Medium, Slow)
- Signal-to-Idea Pipeline & Anomaly Detection (Type I vs Type II Decisions)
- 13 Coupled External Business Loops
- 15-Stage Full Lifecycle Customer Journey
- Integrated Go-to-Market (GTM) System
- 9-Stage Company Growth Classifier State Machine
- Strategic Thinking, Cost Curves, and Moat Durability Models
- 10 Failure Mode Monitors & Automated Corrections
- 10 Discrete AI-Driven Agent Modules & Decision Tree Engine
"""

from __future__ import annotations
import math
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, UTC
from pydantic import BaseModel, Field

logger = logging.getLogger("ai_eos.eos_first_principles")


# =====================================================================
# 0. Timescales & Enums
# =====================================================================

class Timescale(str, Enum):
    FAST = "FAST"        # Days-weeks: product experiments, sales calls, ad tests
    MEDIUM = "MEDIUM"    # Months-quarters: GTM iteration, pricing, org design
    SLOW = "SLOW"        # Years: strategic positioning, moat construction, reinvention


class DecisionType(str, Enum):
    TYPE_I = "TYPE_I"    # Irreversible, high scrutiny required (one-way door)
    TYPE_II = "TYPE_II"  # Reversible, fast cheap tests (two-way door)


class CustomerJourneyStage(str, Enum):
    AWARENESS = "AWARENESS"
    INTEREST = "INTEREST"
    CONSIDERATION = "CONSIDERATION"
    EVALUATION = "EVALUATION"
    PURCHASE = "PURCHASE"
    ONBOARDING = "ONBOARDING"
    ACTIVATION = "ACTIVATION"
    ENGAGEMENT = "ENGAGEMENT"
    HABIT_FORMATION = "HABIT_FORMATION"
    RETENTION = "RETENTION"
    LOYALTY = "LOYALTY"
    ADVOCACY = "ADVOCACY"
    REFERRAL = "REFERRAL"
    EXPANSION = "EXPANSION"
    REPURCHASE = "REPURCHASE"


class GrowthStage(str, Enum):
    IDEA = "IDEA"
    VALIDATION = "VALIDATION"
    STARTUP = "STARTUP"
    PMF = "PMF"
    GROWTH = "GROWTH"
    SCALE = "SCALE"
    PLATFORM = "PLATFORM"
    ECOSYSTEM = "ECOSYSTEM"
    MARKET_LEADERSHIP = "MARKET_LEADERSHIP"


class SystemState(str, Enum):
    SENSING = "SENSING"
    HYPOTHESIS = "HYPOTHESIS"
    CHEAP_TEST = "CHEAP_TEST"
    VALIDATION = "VALIDATION"
    BUILD_GATE = "BUILD_GATE"
    MVP = "MVP"
    GTM_TEST = "GTM_TEST"
    KILL_OR_SCALE = "KILL_OR_SCALE"
    SCALE = "SCALE"
    OPERATE = "OPERATE"
    REINVENT = "REINVENT"
    DISCARD = "DISCARD"


# =====================================================================
# 1. Signal-to-Idea Pipeline & Anomaly Detection
# =====================================================================

class MarketSignal(BaseModel):
    signal_id: str = Field(default_factory=lambda: f"sig_{datetime.now(UTC).timestamp()}")
    description: str
    observed_value: float
    expected_value: float
    is_structural: bool = False
    source: str = "market_observation"

    @property
    def anomaly_magnitude(self) -> float:
        """Kullback-Leibler / Surprise score proxy."""
        if self.expected_value == 0:
            return abs(self.observed_value)
        return abs(self.observed_value - self.expected_value) / abs(self.expected_value)


class FalsifiableHypothesis(BaseModel):
    hypothesis_id: str = Field(default_factory=lambda: f"hyp_{datetime.now(UTC).timestamp()}")
    claim: str
    kill_criteria: str
    prior_belief: float = 0.5  # Beta distribution mean [0, 1]
    posterior_belief: float = 0.5
    tests_run: int = 0
    decision_type: DecisionType = DecisionType.TYPE_II
    status: str = "PROPOSED"  # PROPOSED, CONFIRMED, FALSIFIED, SCALED


class CheapTestResult(BaseModel):
    test_id: str
    hypothesis_id: str
    cost_usd: float
    metric_observed: float
    kill_threshold: float
    passed: bool


class BayesianBeliefUpdater:
    """Updates belief state sequentially using Beta-Binomial conjugacy."""

    @staticmethod
    def update(prior_alpha: float, prior_beta: float, success_count: int, failure_count: int) -> Tuple[float, float, float]:
        new_alpha = prior_alpha + success_count
        new_beta = prior_beta + failure_count
        posterior_mean = new_alpha / (new_alpha + new_beta)
        return new_alpha, new_beta, posterior_mean


# =====================================================================
# 2. 13 External Business Loops
# =====================================================================

@dataclass
class BusinessLoopState:
    loop_name: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    feedback_signal: float  # [-1.0, 1.0]
    kpis: Dict[str, float]
    failure_mode_detected: bool = False
    failure_mode_reason: Optional[str] = None


class BusinessLoopEngine:
    """Evaluates the 13 coupled feedback loops and checks coupling dependencies."""

    def __init__(self) -> None:
        self.loops: Dict[str, BusinessLoopState] = {}

    def evaluate_product_loop(self, retention_slope: float, nps: float, feature_adoption_rate: float) -> BusinessLoopState:
        kpis = {"retention_slope": retention_slope, "nps": nps, "feature_adoption_rate": feature_adoption_rate}
        feedback = (retention_slope + (nps / 100.0) + feature_adoption_rate) / 3.0
        failure = retention_slope < 0.0 or nps < 0
        reason = "Building for loudest customer, retention not flattening" if failure else None
        state = BusinessLoopState("Product", {}, {}, feedback, kpis, failure, reason)
        self.loops["Product"] = state
        return state

    def evaluate_marketing_loop(self, cac_usd: float, brand_recall: float, conversion_rate: float) -> BusinessLoopState:
        kpis = {"cac_usd": cac_usd, "brand_recall": brand_recall, "conversion_rate": conversion_rate}
        feedback = conversion_rate - (cac_usd / 500.0)
        failure = cac_usd > 1000.0 and conversion_rate < 0.01
        reason = "Message-market mismatch or scaling spend prematurely" if failure else None
        state = BusinessLoopState("Marketing", {}, {}, feedback, kpis, failure, reason)
        self.loops["Marketing"] = state
        return state

    def evaluate_sales_loop(self, win_rate: float, sales_cycle_days: float, acv_usd: float) -> BusinessLoopState:
        kpis = {"win_rate": win_rate, "sales_cycle_days": sales_cycle_days, "acv_usd": acv_usd}
        feedback = win_rate * (acv_usd / max(1.0, sales_cycle_days * 10.0))
        failure = win_rate < 0.15 or sales_cycle_days > 180
        reason = "Selling to non-ICP customers to hit quota" if failure else None
        state = BusinessLoopState("Sales", {}, {}, feedback, kpis, failure, reason)
        self.loops["Sales"] = state
        return state

    def evaluate_customer_success_loop(self, nrr: float, churn_rate: float, ttv_days: float) -> BusinessLoopState:
        kpis = {"nrr": nrr, "churn_rate": churn_rate, "time_to_value_days": ttv_days}
        feedback = nrr - churn_rate
        failure = nrr < 1.0 or churn_rate > 0.05
        reason = "Reactive-only CS mistaking support for success" if failure else None
        state = BusinessLoopState("Customer Success", {}, {}, feedback, kpis, failure, reason)
        self.loops["Customer Success"] = state
        return state

    def evaluate_brand_loop(self, share_of_voice: float, price_elasticity: float) -> BusinessLoopState:
        kpis = {"share_of_voice": share_of_voice, "price_elasticity": price_elasticity}
        feedback = share_of_voice - abs(price_elasticity)
        failure = price_elasticity < -2.0  # High price sensitivity indicates weak brand
        reason = "Brand treated as decoration rather than trust/pricing power asset" if failure else None
        state = BusinessLoopState("Brand", {}, {}, feedback, kpis, failure, reason)
        self.loops["Brand"] = state
        return state

    def evaluate_pricing_loop(self, arpu_usd: float, price_realization: float, elasticity: float) -> BusinessLoopState:
        kpis = {"arpu_usd": arpu_usd, "price_realization": price_realization, "elasticity": elasticity}
        feedback = price_realization * arpu_usd
        failure = price_realization < 0.6
        reason = "Cost-plus pricing instead of value-based pricing" if failure else None
        state = BusinessLoopState("Pricing", {}, {}, feedback, kpis, failure, reason)
        self.loops["Pricing"] = state
        return state

    def evaluate_referral_loop(self, viral_coefficient_k: float, referral_cac_usd: float) -> BusinessLoopState:
        kpis = {"viral_coefficient_k": viral_coefficient_k, "referral_cac_usd": referral_cac_usd}
        feedback = viral_coefficient_k
        failure = viral_coefficient_k < 0.1
        reason = "Incentivizing referral volume over referral quality" if failure else None
        state = BusinessLoopState("Referral", {}, {}, feedback, kpis, failure, reason)
        self.loops["Referral"] = state
        return state

    def evaluate_data_loop(self, data_latency_sec: float, decision_cycle_days: float) -> BusinessLoopState:
        kpis = {"data_latency_sec": data_latency_sec, "decision_cycle_days": decision_cycle_days}
        feedback = 1.0 / max(1.0, decision_cycle_days)
        failure = decision_cycle_days > 30.0
        reason = "Vanity metrics and unacted dashboards" if failure else None
        state = BusinessLoopState("Data", {}, {}, feedback, kpis, failure, reason)
        self.loops["Data"] = state
        return state

    def evaluate_financial_loop(self, gross_margin: float, burn_multiple: float, runway_months: float) -> BusinessLoopState:
        kpis = {"gross_margin": gross_margin, "burn_multiple": burn_multiple, "runway_months": runway_months}
        feedback = gross_margin - burn_multiple / 3.0
        failure = burn_multiple > 2.5 or runway_months < 6.0 or gross_margin < 0.4
        reason = "Growth at negative unit economics with no path to profitability" if failure else None
        state = BusinessLoopState("Financial", {}, {}, feedback, kpis, failure, reason)
        self.loops["Financial"] = state
        return state

    def evaluate_hiring_loop(self, time_to_fill_days: float, quality_of_hire: float, retention_90d: float) -> BusinessLoopState:
        kpis = {"time_to_fill_days": time_to_fill_days, "quality_of_hire": quality_of_hire, "retention_90d": retention_90d}
        feedback = quality_of_hire * retention_90d
        failure = retention_90d < 0.80 or quality_of_hire < 0.6
        reason = "Hiring for pedigree over role-fit or hiring ahead of proven need" if failure else None
        state = BusinessLoopState("Hiring", {}, {}, feedback, kpis, failure, reason)
        self.loops["Hiring"] = state
        return state

    def evaluate_culture_loop(self, enps: float, decision_latency_days: float) -> BusinessLoopState:
        kpis = {"enps": enps, "decision_latency_days": decision_latency_days}
        feedback = (enps / 100.0) - (decision_latency_days / 14.0)
        failure = enps < 0 or decision_latency_days > 14.0
        reason = "Values-as-poster: stated values not incentivized in practice" if failure else None
        state = BusinessLoopState("Culture", {}, {}, feedback, kpis, failure, reason)
        self.loops["Culture"] = state
        return state

    def evaluate_innovation_loop(self, num_experiments: int, hit_rate: float, time_to_signal_days: float) -> BusinessLoopState:
        kpis = {"num_experiments": num_experiments, "hit_rate": hit_rate, "time_to_signal_days": time_to_signal_days}
        feedback = num_experiments * hit_rate
        failure = hit_rate < 0.05 or num_experiments == 0
        reason = "Innovation theater — high activity without shipped winning bets" if failure else None
        state = BusinessLoopState("Innovation", {}, {}, feedback, kpis, failure, reason)
        self.loops["Innovation"] = state
        return state

    def evaluate_competitive_intelligence_loop(self, relative_share_trend: float, feature_parity_gap: float) -> BusinessLoopState:
        kpis = {"relative_share_trend": relative_share_trend, "feature_parity_gap": feature_parity_gap}
        feedback = relative_share_trend - feature_parity_gap
        failure = feature_parity_gap > 0.5 and relative_share_trend < 0
        reason = "Reacting passively to competitors instead of running unique strategy" if failure else None
        state = BusinessLoopState("Competitive Intelligence", {}, {}, feedback, kpis, failure, reason)
        self.loops["Competitive Intelligence"] = state
        return state


# =====================================================================
# 3. Customer Journey (15 Stages)
# =====================================================================

@dataclass
class CustomerCohortStageMetric:
    stage: CustomerJourneyStage
    conversion_rate: float
    dropoff_rate: float
    time_in_stage_days: float
    key_metric_value: float


class CustomerJourneyTracker:
    """Tracks cohort progression across the 15-stage lifecycle."""

    def __init__(self) -> None:
        self.stage_metrics: Dict[CustomerJourneyStage, CustomerCohortStageMetric] = {}

    def update_stage(self, stage: CustomerJourneyStage, conversion_rate: float, dropoff_rate: float, time_days: float, metric_val: float) -> None:
        self.stage_metrics[stage] = CustomerCohortStageMetric(
            stage=stage,
            conversion_rate=conversion_rate,
            dropoff_rate=dropoff_rate,
            time_in_stage_days=time_days,
            key_metric_value=metric_val,
        )

    def calculate_overall_funnel_health(self) -> float:
        if not self.stage_metrics:
            return 0.0
        avg_conversion = sum(m.conversion_rate for m in self.stage_metrics.values()) / len(self.stage_metrics)
        return avg_conversion


# =====================================================================
# 4. Integrated Go-to-Market (GTM) System
# =====================================================================

class GTMConfiguration(BaseModel):
    positioning_statement: str
    target_segment: str
    price_usd: float
    product_complexity: str  # LOW, MEDIUM, HIGH
    primary_channel: str     # PLG, CONTENT, SALES_LED, COMMUNITY

    def validate_channel_fit(self) -> bool:
        """Enforces channel fit logic matching buyer behavior:

        - Low complexity/price -> PLG, Content, Organic
        - High complexity/price -> Sales-Led / Enterprise
        - Network effect -> Community-Led
        """
        if self.product_complexity == "HIGH" and self.price_usd >= 10000.0:
            return self.primary_channel in ["SALES_LED", "ENTERPRISE"]
        if self.product_complexity == "LOW" and self.price_usd < 500.0:
            return self.primary_channel in ["PLG", "CONTENT", "ORGANIC", "COMMUNITY"]
        return True


# =====================================================================
# 5. Company Growth System State Machine
# =====================================================================

class CompanyGrowthClassifier:
    """Classifies company stage and flags risks and constraints."""

    @staticmethod
    def classify_stage(
        paying_customers: int,
        mrr_usd: float,
        retention_flattened: bool,
        growth_rate_mom: float,
        developer_ecosystem_active: bool,
        market_share_percent: float,
    ) -> Tuple[GrowthStage, str]:
        if market_share_percent >= 40.0:
            return GrowthStage.MARKET_LEADERSHIP, "Binding constraint: Innovation velocity vs incumbency drag"
        if developer_ecosystem_active and market_share_percent >= 20.0:
            return GrowthStage.ECOSYSTEM, "Binding constraint: Governance credibility"
        if developer_ecosystem_active:
            return GrowthStage.PLATFORM, "Binding constraint: Trust from ecosystem partners"
        if mrr_usd >= 100000.0 and growth_rate_mom >= 0.15:
            return GrowthStage.GROWTH, "Binding constraint: Hiring velocity & operational systems"
        if retention_flattened and mrr_usd >= 10000.0:
            return GrowthStage.PMF, "Binding constraint: Team bandwidth"
        if paying_customers >= 10:
            return GrowthStage.STARTUP, "Binding constraint: Cash runway"
        if paying_customers > 0:
            return GrowthStage.VALIDATION, "Binding constraint: Signal quality"
        return GrowthStage.IDEA, "Binding constraint: Founder time"


# =====================================================================
# 6. Failure Mode Analysis
# =====================================================================

class FailureModeDetector:
    """Pattern-matches metrics against the 10 core failure modes."""

    @staticmethod
    def audit_system(
        engagement_score: float,
        build_velocity: float,
        demand_signal: float,
        cac_usd: float,
        win_rate: float,
        gross_margin: float,
        retention_flattened: bool,
        decision_latency_days: float,
        disconfirming_data_ignored: bool,
        ltv_to_cac: float,
        underperforming_bets_count: int,
    ) -> List[Dict[str, str]]:
        alerts = []

        if engagement_score < 0.2:
            alerts.append({
                "failure_mode": "Solving the wrong problem",
                "root_cause": "Skipped root-cause analysis; solved a symptom",
                "correction": "Return to root cause via 5-Whys / Jobs-to-be-Done interviews",
            })

        if build_velocity > 0.8 and demand_signal < 0.2:
            alerts.append({
                "failure_mode": "Building before validating",
                "root_cause": "Founder conviction substituted for evidence",
                "correction": "Enforce a validation gate before build resourcing",
            })

        if cac_usd > 500.0 and win_rate < 0.10:
            alerts.append({
                "failure_mode": "Weak positioning",
                "root_cause": "No clear differentiation vs alternatives",
                "correction": "Rebuild positioning around real competitive alternative",
            })

        if gross_margin < 0.40:
            alerts.append({
                "failure_mode": "Poor pricing",
                "root_cause": "Cost-plus instead of value-based pricing",
                "correction": "Re-anchor price to quantified customer value",
            })

        if not retention_flattened and ltv_to_cac < 2.0:
            alerts.append({
                "failure_mode": "Lack of product-market fit",
                "root_cause": "Premature scaling of an unproven loop",
                "correction": "Stop scaling; return to cohort retention analysis",
            })

        if decision_latency_days > 14.0:
            alerts.append({
                "failure_mode": "Organizational bottlenecks",
                "root_cause": "Decision rights not delegated as company scales",
                "correction": "Push decision rights down with clear decision frameworks",
            })

        if disconfirming_data_ignored:
            alerts.append({
                "failure_mode": "Founder bias",
                "root_cause": "Overconfidence, confirmation bias, sunk cost fallacy",
                "correction": "Pre-committed kill criteria set before launching",
            })

        if underperforming_bets_count >= 3:
            alerts.append({
                "failure_mode": "Capital misallocation",
                "root_cause": "No opportunity-cost discipline in budgeting",
                "correction": "Rank all initiatives on a common expected-return basis quarterly",
            })

        return alerts


# =====================================================================
# 7. AI-Driven Implementation Modules (§10.3)
# =====================================================================

class SensingAgent:
    """Continuously ingests market/tech signals and flags anomalies (§10.3)."""

    def detect_anomalies(self, signals: List[MarketSignal], threshold: float = 0.25) -> List[MarketSignal]:
        anomalies = [s for s in signals if s.anomaly_magnitude >= threshold]
        for a in anomalies:
            logger.info(f"[SensingAgent] Anomaly detected: {a.description} (Magnitude: {a.anomaly_magnitude:.2f})")
        return anomalies


class HypothesisEngineModule:
    """Converts anomalies into falsifiable claims with kill criteria (§10.3)."""

    def generate_hypothesis(self, signal: MarketSignal, decision_type: DecisionType = DecisionType.TYPE_II) -> FalsifiableHypothesis:
        claim = f"Hypothesis based on structural anomaly in {signal.description}"
        kill_criteria = f"Falsify if test metric remains < {signal.expected_value * 1.2:.2f}"
        hyp = FalsifiableHypothesis(
            claim=claim,
            kill_criteria=kill_criteria,
            prior_belief=0.5,
            decision_type=decision_type,
        )
        logger.info(f"[HypothesisEngine] Generated hypothesis {hyp.hypothesis_id}: '{claim}'")
        return hyp


class ValidationAgent:
    """Runs cheap tests and scores economic viability (§10.3)."""

    def evaluate_test(self, hyp: FalsifiableHypothesis, test_cost_usd: float, observed_metric: float, kill_threshold: float) -> CheapTestResult:
        passed = observed_metric >= kill_threshold
        result = CheapTestResult(
            test_id=f"test_{datetime.now(UTC).timestamp()}",
            hypothesis_id=hyp.hypothesis_id,
            cost_usd=test_cost_usd,
            metric_observed=observed_metric,
            kill_threshold=kill_threshold,
            passed=passed,
        )

        # Update hypothesis belief
        if passed:
            hyp.posterior_belief = min(0.99, hyp.posterior_belief + 0.2)
            hyp.status = "CONFIRMED" if hyp.posterior_belief >= 0.8 else "PROPOSED"
        else:
            hyp.posterior_belief = max(0.01, hyp.posterior_belief - 0.3)
            hyp.status = "FALSIFIED"

        hyp.tests_run += 1
        return result


class GTMSimulator:
    """Models channel fit against segment/pricing combinations (§10.3)."""

    def simulate_gtm(self, config: GTMConfiguration, monthly_ad_spend_usd: float) -> Dict[str, float]:
        fit = config.validate_channel_fit()
        base_cac = config.price_usd * 0.3 if fit else config.price_usd * 1.2
        projected_conversions = monthly_ad_spend_usd / max(10.0, base_cac)
        projected_mrr = projected_conversions * (config.price_usd / 12.0)

        return {
            "channel_fit_valid": 1.0 if fit else 0.0,
            "projected_cac_usd": base_cac,
            "projected_conversions": projected_conversions,
            "projected_mrr_usd": projected_mrr,
        }


class MoatAnalyzerModule:
    """Tracks competitive data to score durability of advantage (§10.3)."""

    @staticmethod
    def calculate_moat_score(
        network_density: float,     # [0, 1]
        switching_cost_score: float, # [0, 1]
        brand_trust: float,         # [0, 1]
        cost_advantage: float,       # [0, 1]
    ) -> float:
        """7 Powers composite moat durability score."""
        return 0.35 * network_density + 0.25 * switching_cost_score + 0.20 * brand_trust + 0.20 * cost_advantage


class CapitalAllocator:
    """Ranks all active initiatives on common expected-return basis (§10.3)."""

    def allocate_capital(self, initiatives: List[Dict[str, Any]], total_budget_usd: float) -> Dict[str, float]:
        if not initiatives:
            return {}

        # Rank by Expected Return = (Prob_Success * Payoff - Cost) / Cost
        scored = []
        for item in initiatives:
            cost = item.get("cost_usd", 1.0)
            prob = item.get("prob_success", 0.5)
            payoff = item.get("expected_payoff_usd", 0.0)
            expected_roi = (prob * payoff - cost) / max(1.0, cost)
            scored.append((item["id"], expected_roi, item))

        scored.sort(key=lambda x: x[1], reverse=True)

        allocations = {}
        remaining_budget = total_budget_usd

        for init_id, roi, item in scored:
            if roi <= 0:
                allocations[init_id] = 0.0
                continue

            requested = item.get("cost_usd", 0.0)
            allocated = min(remaining_budget, requested)
            allocations[init_id] = allocated
            remaining_budget -= allocated

        return allocations


class ReinventionTrigger:
    """Forces periodic self-disruption reviews at leadership stage (§10.3)."""

    def evaluate_reinvention_necessity(self, revenue_growth_yoy: float, market_share_decay: float, tech_shift_detected: bool) -> bool:
        if tech_shift_detected or (revenue_growth_yoy < 0.0 and market_share_decay > 0.05):
            logger.warning("[ReinventionTrigger] MANDATE: Self-disruption and reinvention review triggered!")
            return True
        return False


class GovernanceSafetyLayer:
    """Enforces kill criteria and human sign-off on Type-I decisions (§10.3)."""

    def evaluate_governance_gate(
        self,
        decision_type: DecisionType,
        capital_requested_usd: float,
        capital_threshold_type_i: float,
        human_approved: bool,
    ) -> bool:
        if decision_type == DecisionType.TYPE_I or capital_requested_usd >= capital_threshold_type_i:
            if not human_approved:
                logger.error("[GovernanceSafetyLayer] BLOCKED: Type-I or high-capital decision requires human approval!")
                return False
        return True


# =====================================================================
# 8. Decision Tree & Master Orchestrator Engine
# =====================================================================

class DecisionTreeEngine:
    """Evaluates the §10.2 Pursual Decision Tree."""

    @staticmethod
    def evaluate_pursuit(
        is_structural_anomaly: bool,
        is_reversible: bool,
        high_confidence_multi_source: bool,
        cheap_test_available: bool,
        test_exceeds_kill_threshold: bool,
        ev_clearly_positive: bool,
        has_structural_advantage: bool,
    ) -> Tuple[bool, str]:
        # Q1: Structural anomaly or noise?
        if not is_structural_anomaly:
            return False, "Discarded: Signal is market noise, not a structural anomaly."

        # Q2: Reversible decision?
        if not is_reversible:
            # Q2a: High confidence from multiple sources?
            if not high_confidence_multi_source:
                return False, "Discarded: Irreversible decision lacking multi-source high-confidence signal."

        # Q3: Cheap test available?
        if cheap_test_available:
            if not test_exceeds_kill_threshold:
                return False, "Discarded: Cheap test result failed to exceed kill threshold."
        else:
            if not ev_clearly_positive:
                return False, "Discarded: No cheap test available and Expected Value is not clearly positive."

        # Q5: Structural advantage?
        if not has_structural_advantage:
            return False, "Discarded: No structural advantage or defendable moat."

        return True, "Approved: Opportunity satisfies all decision tree criteria. Commit resources."


class EOSFirstPrinciplesEngine:
    """The master Entrepreneurial Operating System engine coordinating all loops and AI modules."""

    def __init__(self) -> None:
        self.system_state: SystemState = SystemState.SENSING
        self.sensing_agent = SensingAgent()
        self.hypothesis_module = HypothesisEngineModule()
        self.validation_agent = ValidationAgent()
        self.gtm_simulator = GTMSimulator()
        self.capital_allocator = CapitalAllocator()
        self.reinvention_trigger = ReinventionTrigger()
        self.governance_layer = GovernanceSafetyLayer()
        self.business_loops = BusinessLoopEngine()
        self.customer_journey = CustomerJourneyTracker()

    def run_full_sensing_and_execution_cycle(
        self,
        signals: List[MarketSignal],
        initiatives: List[Dict[str, Any]],
        total_budget_usd: float,
    ) -> Dict[str, Any]:
        """Runs a complete first-principles cycle across sensing, hypotheses, allocation, and failure checks."""
        # 1. Sensing & Anomaly Detection
        anomalies = self.sensing_agent.detect_anomalies(signals)

        # 2. Hypothesis Formation for anomalies
        hypotheses = []
        for anomaly in anomalies:
            hyp = self.hypothesis_module.generate_hypothesis(anomaly)
            hypotheses.append(hyp)

        # 3. Capital Allocation
        allocations = self.capital_allocator.allocate_capital(initiatives, total_budget_usd)

        # 4. Return summary
        return {
            "system_state": self.system_state.value,
            "anomalies_detected": len(anomalies),
            "hypotheses_generated": len(hypotheses),
            "capital_allocations_usd": allocations,
        }
