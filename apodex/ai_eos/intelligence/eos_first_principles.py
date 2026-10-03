"""First-Principles Entrepreneurial Operating System (EOS) Python Engine.

Implements the 11-section EOS specification covering multi-timescale coupled feedback loops,
signal-to-idea pipelines, customer journey lifecycles, GTM dynamics, company growth stages,
and the AI-EOS system state machine.
"""

from __future__ import annotations
import math
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Set
from uuid import UUID, uuid4
from datetime import datetime

logger = logging.getLogger("apodex.ai_eos.eos_first_principles")


# =====================================================================
# 1. State Machine & Stages
# =====================================================================
class EOSState(Enum):
    SENSING = "Sensing"
    HYPOTHESIS = "Hypothesis"
    CHEAP_TEST = "CheapTest"
    VALIDATION = "Validation"
    BUILD_GATE = "BuildGate"
    MVP = "MVP"
    GTM_TEST = "GTMTest"
    KILL_OR_SCALE = "KillOrScale"
    SCALE = "Scale"
    OPERATE = "Operate"
    REINVENT = "Reinvent"
    DISCARD = "Discard"


class GrowthStage(Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "PMF"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    MARKET_LEADERSHIP = "Market Leadership"


class JourneyStage(Enum):
    AWARENESS = "Awareness"
    INTEREST = "Interest"
    CONSIDERATION = "Consideration"
    EVALUATION = "Evaluation"
    PURCHASE = "Purchase"
    ONBOARDING = "Onboarding"
    ACTIVATION = "Activation"
    ENGAGEMENT = "Engagement"
    HABIT_FORMATION = "Habit Formation"
    RETENTION = "Retention"
    LOYALTY = "Loyalty"
    ADVOCACY = "Advocacy"
    REFERRAL = "Referral"
    EXPANSION = "Expansion"
    REPURCHASE = "Repurchase"


# =====================================================================
# 2. External Business Loops Engine
# =====================================================================
@dataclass
class BusinessLoopMetrics:
    loop_name: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    feedback_signal: float
    kpis: Dict[str, float]
    failure_mode_detected: Optional[str] = None


class ExternalBusinessLoopsEngine:
    """Manages the 13 coupled feedback loops operating across fast, medium, and slow timescales."""

    LOOPS = [
        "Product", "Marketing", "Sales", "Customer Success", "Brand",
        "Pricing", "Referral", "Data", "Financial", "Hiring",
        "Culture", "Innovation", "Competitive Intelligence"
    ]

    def evaluate_all_loops(self, company_metrics: Dict[str, Any]) -> Dict[str, BusinessLoopMetrics]:
        results = {}

        # 1. Product Loop
        retention = company_metrics.get("retention_30d", 0.40)
        nps = company_metrics.get("nps", 45)
        product_failure = "Building for the loudest customer, not the representative one" if nps < 20 else None
        results["Product"] = BusinessLoopMetrics(
            loop_name="Product",
            inputs={"user_behavior": company_metrics.get("active_users", 1000)},
            outputs={"roadmap_velocity": 8.5},
            feedback_signal=retention,
            kpis={"retention_curve": retention, "nps": nps},
            failure_mode_detected=product_failure
        )

        # 2. Marketing Loop
        cac = company_metrics.get("cac_cents", 15000)
        mkt_failure = "Message-market mismatch; scaling spend before message works" if cac > 50000 else None
        results["Marketing"] = BusinessLoopMetrics(
            loop_name="Marketing",
            inputs={"positioning": "Category leader"},
            outputs={"demand_generation": company_metrics.get("leads", 500)},
            feedback_signal=1.0 / (cac / 10000.0 if cac > 0 else 1.0),
            kpis={"cac_cents": cac, "conversion_rate": company_metrics.get("mkt_conversion", 0.03)},
            failure_mode_detected=mkt_failure
        )

        # 3. Sales Loop
        win_rate = company_metrics.get("win_rate", 0.25)
        sales_failure = "Selling to non-ICP to hit quota" if win_rate < 0.15 else None
        results["Sales"] = BusinessLoopMetrics(
            loop_name="Sales",
            inputs={"leads": company_metrics.get("leads", 500)},
            outputs={"closed_revenue_cents": company_metrics.get("revenue_cents", 1000000)},
            feedback_signal=win_rate,
            kpis={"win_rate": win_rate, "acv_cents": company_metrics.get("acv_cents", 1200000)},
            failure_mode_detected=sales_failure
        )

        # 4. Customer Success Loop
        nrr = company_metrics.get("nrr", 1.15)
        cs_failure = "Success != support; reactive-only CS" if nrr < 0.90 else None
        results["Customer Success"] = BusinessLoopMetrics(
            loop_name="Customer Success",
            inputs={"onboarding_data": True},
            outputs={"retention_expansion": nrr},
            feedback_signal=nrr,
            kpis={"nrr": nrr, "time_to_value_days": company_metrics.get("ttv_days", 14)},
            failure_mode_detected=cs_failure
        )

        # 5. Brand Loop
        brand_trust = company_metrics.get("brand_trust", 0.8)
        brand_failure = "Brand as decoration, not strategy" if brand_trust < 0.3 else None
        results["Brand"] = BusinessLoopMetrics(
            loop_name="Brand",
            inputs={"product_experience": True},
            outputs={"pricing_power": brand_trust},
            feedback_signal=brand_trust,
            kpis={"brand_recall": brand_trust, "price_elasticity": 0.5},
            failure_mode_detected=brand_failure
        )

        # 6. Pricing Loop
        arpu = company_metrics.get("arpu_cents", 10000)
        pricing_failure = "Cost-plus pricing instead of value-based" if arpu < 2000 else None
        results["Pricing"] = BusinessLoopMetrics(
            loop_name="Pricing",
            inputs={"value_delivered": True},
            outputs={"revenue_signal": arpu},
            feedback_signal=arpu / 100.0,
            kpis={"arpu_cents": arpu, "expansion_rate": company_metrics.get("expansion_rate", 0.10)},
            failure_mode_detected=pricing_failure
        )

        # 7. Referral Loop
        k_factor = company_metrics.get("k_factor", 0.2)
        ref_failure = "Incentivizing referral volume over referral quality" if k_factor < 0.05 else None
        results["Referral"] = BusinessLoopMetrics(
            loop_name="Referral",
            inputs={"customer_satisfaction": nps},
            outputs={"new_customer_flow": int(k_factor * 100)},
            feedback_signal=k_factor,
            kpis={"viral_coefficient_k": k_factor},
            failure_mode_detected=ref_failure
        )

        # 8. Data Loop
        data_latency = company_metrics.get("decision_latency_days", 2.0)
        data_failure = "Vanity metrics; dashboards no one acts on" if data_latency > 14.0 else None
        results["Data"] = BusinessLoopMetrics(
            loop_name="Data",
            inputs={"all_loops": True},
            outputs={"actionable_decisions": True},
            feedback_signal=1.0 / data_latency if data_latency > 0 else 1.0,
            kpis={"data_latency_days": data_latency},
            failure_mode_detected=data_failure
        )

        # 9. Financial Loop
        burn_multiple = company_metrics.get("burn_multiple", 1.5)
        fin_failure = "Growth at negative unit economics with no path to positive" if burn_multiple > 3.0 else None
        results["Financial"] = BusinessLoopMetrics(
            loop_name="Financial",
            inputs={"revenue_costs": True},
            outputs={"runway_months": company_metrics.get("runway_months", 18)},
            feedback_signal=1.0 / burn_multiple if burn_multiple > 0 else 1.0,
            kpis={"gross_margin": company_metrics.get("gross_margin", 0.75), "burn_multiple": burn_multiple},
            failure_mode_detected=fin_failure
        )

        # 10. Hiring Loop
        regretted_attrition = company_metrics.get("regretted_attrition", 0.05)
        hiring_failure = "Hiring for pedigree over role-fit; hiring ahead of proven need" if regretted_attrition > 0.20 else None
        results["Hiring"] = BusinessLoopMetrics(
            loop_name="Hiring",
            inputs={"org_needs": True},
            outputs={"capability_capacity": True},
            feedback_signal=1.0 - regretted_attrition,
            kpis={"time_to_fill_days": 30.0, "regretted_attrition": regretted_attrition},
            failure_mode_detected=hiring_failure
        )

        # 11. Culture Loop
        enps = company_metrics.get("enps", 50)
        culture_failure = "Values-as-poster (stated but not incentivized)" if enps < 0 else None
        results["Culture"] = BusinessLoopMetrics(
            loop_name="Culture",
            inputs={"values_in_action": True},
            outputs={"decision_speed": True},
            feedback_signal=enps / 100.0,
            kpis={"eNPS": enps},
            failure_mode_detected=culture_failure
        )

        # 12. Innovation Loop
        exp_run = company_metrics.get("experiments_run", 10)
        hit_rate = company_metrics.get("hit_rate", 0.2)
        innov_failure = "Innovation theater — activity without shipped bets" if hit_rate < 0.05 else None
        results["Innovation"] = BusinessLoopMetrics(
            loop_name="Innovation",
            inputs={"rd_and_market_signals": True},
            outputs={"shipped_bets": int(exp_run * hit_rate)},
            feedback_signal=hit_rate,
            kpis={"experiments_run": exp_run, "hit_rate": hit_rate},
            failure_mode_detected=innov_failure
        )

        # 13. Competitive Intelligence Loop
        feature_parity = company_metrics.get("feature_parity", 0.85)
        comp_failure = "Reacting to competitors instead of running own strategy" if feature_parity > 0.95 else None
        results["Competitive Intelligence"] = BusinessLoopMetrics(
            loop_name="Competitive Intelligence",
            inputs={"competitor_data": True},
            outputs={"repositioning": True},
            feedback_signal=feature_parity,
            kpis={"feature_parity_gap": 1.0 - feature_parity},
            failure_mode_detected=comp_failure
        )

        return results


# =====================================================================
# 3. Customer Lifecycle Engine
# =====================================================================
class CustomerLifecycleEngine:
    """Tracks and optimizes the 15-stage customer journey lifecycle."""

    def evaluate_funnel(self, stage_conversions: Dict[JourneyStage, float]) -> Dict[str, Any]:
        bottleneck = None
        min_conversion = 1.0

        for stage, conv in stage_conversions.items():
            if conv < min_conversion:
                min_conversion = conv
                bottleneck = stage

        return {
            "primary_bottleneck_stage": bottleneck.value if bottleneck else "None",
            "lowest_stage_conversion": min_conversion,
            "funnel_health": "Healthy" if min_conversion >= 0.20 else "Needs Optimization"
        }


# =====================================================================
# 4. GTM System Simulator
# =====================================================================
class GTMSystemSimulator:
    """Models positioning, channel fit, and GTM system dynamics."""

    def evaluate_channel_fit(
        self,
        acv_cents: int,
        complexity_score: float,  # 0.0 (low) to 1.0 (high)
        network_density: float
    ) -> Dict[str, Any]:
        recommended_motion = []

        if acv_cents > 50000_00 or complexity_score > 0.7:
            recommended_motion.append("Sales-Led Growth (SLG) / Enterprise")
        if acv_cents < 2000_00 and complexity_score < 0.3:
            recommended_motion.append("Product-Led Growth (PLG) / Self-Serve")
        if network_density > 0.6:
            recommended_motion.append("Community-Led Growth (CLG)")

        if not recommended_motion:
            recommended_motion.append("Hybrid Inbound / Inside Sales")

        return {
            "recommended_gtm_motions": recommended_motion,
            "positioning_alignment": "Enterprise" if "Sales-Led Growth (SLG) / Enterprise" in recommended_motion else "Self-Serve"
        }


# =====================================================================
# 5. Company Growth Classifier
# =====================================================================
class CompanyGrowthStateMachine:
    """Classifies the venture across the 9 growth stages from Idea to Market Leadership."""

    def classify_stage(self, metrics: Dict[str, Any]) -> Tuple[GrowthStage, str]:
        paying_customers = metrics.get("paying_customers", 0)
        revenue_cents = metrics.get("revenue_cents", 0)
        retention_flattened = metrics.get("retention_flattened", False)
        rule_of_40 = metrics.get("rule_of_40", 0.0)
        ecosystem_gmv_cents = metrics.get("ecosystem_gmv_cents", 0)

        if ecosystem_gmv_cents > 100000000_00:
            return GrowthStage.MARKET_LEADERSHIP, "Binding constraint: Innovation velocity vs. incumbency drag"
        if ecosystem_gmv_cents > 10000000_00:
            return GrowthStage.ECOSYSTEM, "Binding constraint: Governance credibility"
        if metrics.get("third_party_devs", 0) > 100:
            return GrowthStage.PLATFORM, "Binding constraint: Trust from ecosystem partners"
        if rule_of_40 >= 0.40 and revenue_cents > 10000000_00:
            return GrowthStage.SCALE, "Binding constraint: Org coordination cost"
        if revenue_cents > 2000000_00:
            return GrowthStage.GROWTH, "Binding constraint: Hiring velocity & systems"
        if retention_flattened:
            return GrowthStage.PMF, "Binding constraint: Team bandwidth"
        if paying_customers >= 10:
            return GrowthStage.STARTUP, "Binding constraint: Cash runway"
        if paying_customers > 0:
            return GrowthStage.VALIDATION, "Binding constraint: Signal quality"

        return GrowthStage.IDEA, "Binding constraint: Founder time"


# =====================================================================
# 6. Strategic Moat Engine
# =====================================================================
class StrategicMoatEngine:
    """Scores moat durability based on 7 Powers and competitive dynamics."""

    def evaluate_moat_durability(
        self,
        network_effects: float,
        switching_costs: float,
        economies_of_scale: float,
        brand_equity: float,
        counter_positioning: float
    ) -> Dict[str, Any]:
        durability_score = float(
            0.25 * network_effects +
            0.20 * switching_costs +
            0.20 * economies_of_scale +
            0.15 * brand_equity +
            0.20 * counter_positioning
        )

        return {
            "durability_score": min(1.0, max(0.0, durability_score)),
            "dominant_moat": max([
                ("Network Effects", network_effects),
                ("Switching Costs", switching_costs),
                ("Economies of Scale", economies_of_scale),
                ("Brand Equity", brand_equity),
                ("Counter-Positioning", counter_positioning)
            ], key=lambda x: x[1])[0]
        }


# =====================================================================
# 7. Failure Mode Monitor
# =====================================================================
class FailureModeMonitor:
    """Monitors 10 core failure modes and outputs early detection signals and corrections."""

    FAILURE_MODES = {
        "Solving the wrong problem": {
            "root_cause": "Skipped root-cause analysis; solved a symptom",
            "signal": "Low engagement despite positive survey feedback",
            "correction": "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)"
        },
        "Building before validating": {
            "root_cause": "Founder conviction substituted for evidence",
            "signal": "High build velocity, flat demand signal",
            "correction": "Enforce a validation gate before build resourcing"
        },
        "Weak positioning": {
            "root_cause": "No clear 'instead of X, use us because Y'",
            "signal": "High CAC, long sales cycles, feature comparison objections",
            "correction": "Rebuild positioning around the real alternative customers compare to"
        },
        "Poor pricing": {
            "root_cause": "Cost-plus instead of value-based pricing",
            "signal": "High conversion at low price, but poor margin/expansion",
            "correction": "Re-anchor price to quantified customer value"
        },
        "Distribution failure": {
            "root_cause": "Great product, no repeatable channel",
            "signal": "High NPS, flat growth",
            "correction": "Systematically test channels against ICP behavior, not founder preference"
        },
        "Lack of product-market fit": {
            "root_cause": "Premature scaling of an unproven loop",
            "signal": "Retention curve never flattens",
            "correction": "Stop scaling; return to cohort-level retention work"
        },
        "Organizational bottlenecks": {
            "root_cause": "Decision rights not delegated as company scales",
            "signal": "Rising decision latency, founder as single point of failure",
            "correction": "Push decision rights down with clear frameworks"
        },
        "Founder bias": {
            "root_cause": "Overconfidence, confirmation bias, sunk cost",
            "signal": "Ignoring disconfirming data, 'just needs more time' pattern",
            "correction": "Pre-committed kill criteria set before launch"
        },
        "Scaling prematurely": {
            "root_cause": "Confusing early demand spike with durable PMF",
            "signal": "CAC rising faster than LTV as spend scales",
            "correction": "Re-test unit economics at each order-of-magnitude of spend"
        },
        "Capital misallocation": {
            "root_cause": "No opportunity-cost discipline in budgeting",
            "signal": "Multiple underperforming bets funded simultaneously",
            "correction": "Rank all initiatives on a common expected-return basis quarterly"
        }
    }

    def audit_operating_metrics(self, company_metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        active_warnings = []

        if company_metrics.get("retention_flattened") is False and company_metrics.get("mkt_spend_cents", 0) > 100000_00:
            fm = self.FAILURE_MODES["Lack of product-market fit"]
            active_warnings.append({"mode": "Lack of product-market fit", **fm})

        if company_metrics.get("decision_latency_days", 0) > 7.0:
            fm = self.FAILURE_MODES["Organizational bottlenecks"]
            active_warnings.append({"mode": "Organizational bottlenecks", **fm})

        if company_metrics.get("cac_cents", 0) > company_metrics.get("ltv_cents", 1):
            fm = self.FAILURE_MODES["Scaling prematurely"]
            active_warnings.append({"mode": "Scaling prematurely", **fm})

        return active_warnings


# =====================================================================
# 8. EOS Opportunity Decision Tree (Section 10.2)
# =====================================================================
class EOSOpportunityDecisionTree:
    """Evaluates whether to pursue an opportunity based on Section 10.2 decision tree."""

    def evaluate_pursuit(
        self,
        is_structural_anomaly: bool,
        is_reversible_decision: bool,
        multi_source_confidence: float,
        cheap_test_available: bool,
        cheap_test_passed: Optional[bool],
        expected_value_positive: bool,
        structural_advantage: bool
    ) -> Tuple[bool, str]:
        # Q1: Structural anomaly or noise?
        if not is_structural_anomaly:
            return False, "Discard: Anomaly is noise, not structural."

        # Q2: Reversible decision?
        if not is_reversible_decision:
            if multi_source_confidence < 0.8:
                return False, "Discard: Irreversible (Type-I) decision lacks high-confidence multi-source signal."
        else:
            if cheap_test_available:
                if cheap_test_passed is not True:
                    return False, "Discard: Cheap test failed or incomplete."
            else:
                if not expected_value_positive:
                    return False, "Discard: Expected value is not positive."

        # Q5: Structural advantage?
        if not structural_advantage:
            return False, "Discard: No structural win advantage."

        return True, "Commit Resources: Passed all decision tree gates."


# =====================================================================
# 9. Main EOSEngineFirstPrinciples Orchestrator
# =====================================================================
class EOSEngineFirstPrinciples:
    """The complete executive orchestrator implementing the 11-section EOS specification."""

    def __init__(self) -> None:
        self.state = EOSState.SENSING
        self.business_loops = ExternalBusinessLoopsEngine()
        self.lifecycle = CustomerLifecycleEngine()
        self.gtm_simulator = GTMSystemSimulator()
        self.growth_classifier = CompanyGrowthStateMachine()
        self.moat_engine = StrategicMoatEngine()
        self.failure_monitor = FailureModeMonitor()
        self.decision_tree = EOSOpportunityDecisionTree()

    def run_master_loop_cycle(self, company_metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if company_metrics is None:
            company_metrics = {
                "active_users": 5000,
                "retention_30d": 0.45,
                "nps": 55,
                "cac_cents": 12000,
                "ltv_cents": 45000,
                "leads": 800,
                "revenue_cents": 2500000,
                "win_rate": 0.30,
                "nrr": 1.18,
                "brand_trust": 0.85,
                "arpu_cents": 12000,
                "k_factor": 0.25,
                "decision_latency_days": 2.5,
                "burn_multiple": 1.2,
                "runway_months": 24,
                "gross_margin": 0.80,
                "regretted_attrition": 0.03,
                "enps": 60,
                "experiments_run": 15,
                "hit_rate": 0.25,
                "feature_parity": 0.88,
                "paying_customers": 45,
                "retention_flattened": True,
                "rule_of_40": 0.42,
                "ecosystem_gmv_cents": 0
            }

        # 1. State transition
        self.state = EOSState.SENSING

        # 2. External business loops
        loop_results = self.business_loops.evaluate_all_loops(company_metrics)

        # 3. Growth stage
        growth_stage, binding_constraint = self.growth_classifier.classify_stage(company_metrics)

        # 4. GTM dynamics
        gtm_eval = self.gtm_simulator.evaluate_channel_fit(
            acv_cents=company_metrics.get("acv_cents", 1200000),
            complexity_score=0.3,
            network_density=0.5
        )

        # 5. Moat Durability
        moat_eval = self.moat_engine.evaluate_moat_durability(
            network_effects=0.6,
            switching_costs=0.7,
            economies_of_scale=0.5,
            brand_equity=0.8,
            counter_positioning=0.9
        )

        # 6. Failure Warnings
        warnings = self.failure_monitor.audit_operating_metrics(company_metrics)

        return {
            "system_state": self.state.value,
            "growth_stage": growth_stage.value,
            "binding_constraint": binding_constraint,
            "business_loops": loop_results,
            "gtm_evaluation": gtm_eval,
            "moat_durability": moat_eval,
            "failure_warnings": warnings
        }
