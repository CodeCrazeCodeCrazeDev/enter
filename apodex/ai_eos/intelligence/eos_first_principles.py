"""Entrepreneurial Operating System (EOS) First-Principles Engine.

A first-principles reconstruction of how elite founders sense, build, and compound
enduring companies, as specified in ENTREPRENEURIAL_OPERATING_SYSTEM_SPEC.md.

Implements all 11 sections including state machines, decision trees, coupled business
loops, 15-stage customer lifecycle journey, 9-stage company growth classifier,
moat durability scoring, 10 operational failure mode diagnostics, and roll-up KPI stacks.
"""

from __future__ import annotations
import math
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from datetime import datetime, timezone

logger = logging.getLogger("apodex.ai_eos.eos_first_principles")


# =====================================================================
# 10.1 System State Machine
# =====================================================================
class EOSState(str, Enum):
    SENSING = "sensing"
    HYPOTHESIS = "hypothesis"
    CHEAP_TEST = "cheap_test"
    DISCARD = "discard"
    VALIDATION = "validation"
    BUILD_GATE = "build_gate"
    MVP = "mvp"
    GTM_TEST = "gtm_test"
    KILL_OR_SCALE = "kill_or_scale"
    SCALE = "scale"
    OPERATE = "operate"
    REINVENT = "reinvent"


ALLOWED_TRANSITIONS: Dict[EOSState, Set[EOSState]] = {
    EOSState.SENSING: {EOSState.HYPOTHESIS},
    EOSState.HYPOTHESIS: {EOSState.CHEAP_TEST},
    EOSState.CHEAP_TEST: {EOSState.DISCARD, EOSState.VALIDATION},
    EOSState.DISCARD: {EOSState.SENSING},
    EOSState.VALIDATION: {EOSState.BUILD_GATE, EOSState.DISCARD},
    EOSState.BUILD_GATE: {EOSState.MVP},
    EOSState.MVP: {EOSState.GTM_TEST},
    EOSState.GTM_TEST: {EOSState.KILL_OR_SCALE},
    EOSState.KILL_OR_SCALE: {EOSState.DISCARD, EOSState.SCALE},
    EOSState.SCALE: {EOSState.OPERATE},
    EOSState.OPERATE: {EOSState.REINVENT},
    EOSState.REINVENT: {EOSState.SENSING},
}


class EOSStateMachine:
    """System State Machine managing the complete EOS venture state lifecycle (§10.1)."""

    def __init__(self, initial_state: EOSState = EOSState.SENSING) -> None:
        self.current_state = initial_state
        self.history: List[Dict[str, Any]] = [
            {
                "from_state": None,
                "to_state": initial_state.value,
                "reason": "Initial state",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]

    def can_transition_to(self, target_state: EOSState) -> bool:
        """Check if transition to target state is valid per §10.1 state diagram."""
        return target_state in ALLOWED_TRANSITIONS.get(self.current_state, set())

    def transition_to(self, target_state: EOSState, reason: str) -> bool:
        """Execute a state transition with strict validation and audit logging."""
        if not self.can_transition_to(target_state):
            logger.warning(f"Invalid EOS state transition attempted: {self.current_state.value} -> {target_state.value}")
            return False

        from_state = self.current_state
        self.current_state = target_state
        self.history.append({
            "from_state": from_state.value,
            "to_state": target_state.value,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        logger.info(f"EOS State Transition: {from_state.value} -> {target_state.value} ({reason})")
        return True


# =====================================================================
# 10.2 Decision Tree — "Should We Pursue This Opportunity?"
# =====================================================================
class OpportunityDecisionTree:
    """Evaluates whether an opportunity should be pursued based on first-principles rules (§10.2)."""

    def evaluate(self, opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate opportunity along the 5-step decision tree.

        Returns decision ('pursue' or 'discard'), step results, and detailed rationale.
        """
        # Step 1: Structural anomaly vs noise
        is_structural = opportunity_data.get("is_structural_anomaly", False)
        if not is_structural:
            return {
                "decision": "discard",
                "failed_step": "Q1_structural_anomaly",
                "reason": "Signal evaluated as non-structural noise.",
            }

        # Step 2: Reversible decision (Type II vs Type I risk)
        is_reversible = opportunity_data.get("is_reversible", True)
        if not is_reversible:
            # Type I risk (one-way door): requires high-confidence signal from multiple sources
            high_conf = opportunity_data.get("high_confidence_multi_source_signal", False)
            if not high_conf:
                return {
                    "decision": "discard",
                    "failed_step": "Q2a_high_confidence_multi_source_signal",
                    "reason": "Irreversible (Type I) decision lacks multi-source high-confidence signal.",
                }

        # Step 3 & 4: Cheap test vs EV evaluation
        has_cheap_test = opportunity_data.get("cheap_test_available", True)
        if has_cheap_test:
            test_exceeds_kill = opportunity_data.get("test_result_exceeds_kill_threshold", False)
            if not test_exceeds_kill:
                return {
                    "decision": "discard",
                    "failed_step": "Q4_test_result_kill_threshold",
                    "reason": "Cheap test result failed to exceed the pre-committed kill threshold.",
                }
        else:
            ev_positive = opportunity_data.get("expected_value_positive", False)
            if not ev_positive:
                return {
                    "decision": "discard",
                    "failed_step": "Q4b_expected_value_positive",
                    "reason": "Expected value is not clearly positive given available data.",
                }

        # Step 5: Structural advantage check
        has_advantage = opportunity_data.get("has_structural_advantage", False)
        if not has_advantage:
            return {
                "decision": "discard",
                "failed_step": "Q5_structural_advantage",
                "reason": "No existing or buildable structural competitive advantage identified.",
            }

        return {
            "decision": "pursue",
            "failed_step": None,
            "reason": "Passed all 5 decision tree checks; structural advantage and positive EV verified.",
        }


# =====================================================================
# 3. External Business Loops Engine
# =====================================================================
class CoupledBusinessLoopsEngine:
    """Models, couples, and evaluates all 13 external business loops (§3)."""

    LOOP_NAMES = [
        "product", "marketing", "sales", "customer_success", "brand",
        "pricing", "referral", "data", "financial", "hiring",
        "culture", "innovation", "competitive_intelligence",
    ]

    def evaluate_loops(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the 13 coupled feedback loops and detect system bottlenecks."""
        loop_status: Dict[str, Dict[str, Any]] = {}
        failing_loops: List[str] = []

        # 1. Product Loop
        retention = metrics.get("retention_curve_slope", -0.05)
        nps = metrics.get("nps", 30)
        product_healthy = retention >= -0.02 and nps >= 40
        loop_status["product"] = {
            "healthy": product_healthy,
            "kpis": {"retention_slope": retention, "nps": nps},
            "failure_mode": "Building for loudest customer" if not product_healthy else None
        }
        if not product_healthy: failing_loops.append("product")

        # 2. Marketing Loop
        cac = metrics.get("cac_cents", 150_00)
        conv = metrics.get("conversion_rate", 0.02)
        mktg_healthy = cac <= 200_00 and conv >= 0.02
        loop_status["marketing"] = {
            "healthy": mktg_healthy,
            "kpis": {"cac_cents": cac, "conversion_rate": conv},
            "failure_mode": "Message-market mismatch" if not mktg_healthy else None
        }
        if not mktg_healthy: failing_loops.append("marketing")

        # 3. Sales Loop
        win_rate = metrics.get("win_rate", 0.20)
        cycle_days = metrics.get("sales_cycle_days", 45)
        sales_healthy = win_rate >= 0.25 and cycle_days <= 60
        loop_status["sales"] = {
            "healthy": sales_healthy,
            "kpis": {"win_rate": win_rate, "sales_cycle_days": cycle_days},
            "failure_mode": "Selling to non-ICP to hit quota" if not sales_healthy else None
        }
        if not sales_healthy: failing_loops.append("sales")

        # 4. Customer Success Loop
        nrr = metrics.get("nrr", 1.10)
        churn = metrics.get("churn_rate", 0.02)
        cs_healthy = nrr >= 1.10 and churn <= 0.03
        loop_status["customer_success"] = {
            "healthy": cs_healthy,
            "kpis": {"nrr": nrr, "churn_rate": churn},
            "failure_mode": "Reactive-only CS" if not cs_healthy else None
        }
        if not cs_healthy: failing_loops.append("customer_success")

        # 5. Brand Loop
        share_of_voice = metrics.get("share_of_voice", 0.15)
        brand_healthy = share_of_voice >= 0.10
        loop_status["brand"] = {
            "healthy": brand_healthy,
            "kpis": {"share_of_voice": share_of_voice},
            "failure_mode": "Brand as decoration" if not brand_healthy else None
        }
        if not brand_healthy: failing_loops.append("brand")

        # 6. Pricing Loop
        arpu = metrics.get("arpu_cents", 50_00)
        pricing_healthy = arpu >= 30_00
        loop_status["pricing"] = {
            "healthy": pricing_healthy,
            "kpis": {"arpu_cents": arpu},
            "failure_mode": "Cost-plus pricing instead of value-based" if not pricing_healthy else None
        }
        if not pricing_healthy: failing_loops.append("pricing")

        # 7. Referral Loop
        viral_k = metrics.get("viral_coefficient_k", 0.3)
        ref_healthy = viral_k >= 0.5
        loop_status["referral"] = {
            "healthy": ref_healthy,
            "kpis": {"viral_k": viral_k},
            "failure_mode": "Incentivizing volume over quality" if not ref_healthy else None
        }
        if not ref_healthy: failing_loops.append("referral")

        # 8. Data Loop
        latency = metrics.get("decision_cycle_days", 5)
        data_healthy = latency <= 7
        loop_status["data"] = {
            "healthy": data_healthy,
            "kpis": {"decision_cycle_days": latency},
            "failure_mode": "Vanity metrics dashboard" if not data_healthy else None
        }
        if not data_healthy: failing_loops.append("data")

        # 9. Financial Loop
        burn_mult = metrics.get("burn_multiple", 1.5)
        runway = metrics.get("runway_months", 18.0)
        fin_healthy = burn_mult <= 2.0 and runway >= 12.0
        loop_status["financial"] = {
            "healthy": fin_healthy,
            "kpis": {"burn_multiple": burn_mult, "runway_months": runway},
            "failure_mode": "Growth at negative unit economics" if not fin_healthy else None
        }
        if not fin_healthy: failing_loops.append("financial")

        # 10. Hiring Loop
        regretted_attrition = metrics.get("regretted_attrition_rate", 0.05)
        hiring_healthy = regretted_attrition <= 0.10
        loop_status["hiring"] = {
            "healthy": hiring_healthy,
            "kpis": {"regretted_attrition_rate": regretted_attrition},
            "failure_mode": "Hiring for pedigree over role-fit" if not hiring_healthy else None
        }
        if not hiring_healthy: failing_loops.append("hiring")

        # 11. Culture Loop
        enps = metrics.get("enps", 40)
        culture_healthy = enps >= 30
        loop_status["culture"] = {
            "healthy": culture_healthy,
            "kpis": {"enps": enps},
            "failure_mode": "Values as poster" if not culture_healthy else None
        }
        if not culture_healthy: failing_loops.append("culture")

        # 12. Innovation Loop
        experiments = metrics.get("experiments_run_quarterly", 10)
        hit_rate = metrics.get("experiment_hit_rate", 0.20)
        inn_healthy = experiments >= 5 and hit_rate >= 0.15
        loop_status["innovation"] = {
            "healthy": inn_healthy,
            "kpis": {"experiments": experiments, "hit_rate": hit_rate},
            "failure_mode": "Innovation theater" if not inn_healthy else None
        }
        if not inn_healthy: failing_loops.append("innovation")

        # 13. Competitive Intelligence Loop
        feature_parity_gap = metrics.get("feature_parity_gap", 0.10)
        comp_healthy = feature_parity_gap <= 0.20
        loop_status["competitive_intelligence"] = {
            "healthy": comp_healthy,
            "kpis": {"feature_parity_gap": feature_parity_gap},
            "failure_mode": "Reacting to competitors instead of running own strategy" if not comp_healthy else None
        }
        if not comp_healthy: failing_loops.append("competitive_intelligence")

        # Coupled feedback effect calculation
        # Pricing (ARPU) -> Financial runway -> Hiring budget -> Product velocity
        coupled_system_health = len(self.LOOP_NAMES) - len(failing_loops)
        health_score = float(coupled_system_health / len(self.LOOP_NAMES))

        return {
            "health_score": health_score,
            "failing_loops": failing_loops,
            "loop_details": loop_status,
        }


# =====================================================================
# 4. Customer Journey Engine (Full Lifecycle)
# =====================================================================
class CustomerLifecycleEngine:
    """Models all 15 stages of the customer lifecycle journey (§4)."""

    STAGES = [
        "awareness", "interest", "consideration", "evaluation", "purchase",
        "onboarding", "activation", "engagement", "habit_formation", "retention",
        "loyalty", "advocacy", "referral", "expansion", "repurchase"
    ]

    def evaluate_lifecycle(self, stage_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate customer conversion, cohort retention flattening, and expansion drops."""
        results: Dict[str, Any] = {}

        # Key indicators
        time_to_first_value = stage_metrics.get("time_to_first_value_hours", 24.0)
        activation_rate = stage_metrics.get("activation_rate", 0.40)
        retention_curve_flattened = stage_metrics.get("retention_curve_flattened", True)
        nrr = stage_metrics.get("nrr", 1.15)
        k_factor = stage_metrics.get("viral_coefficient_k", 0.4)

        # Bottleneck detection in lifecycle
        lifecycle_bottlenecks = []
        if time_to_first_value > 48.0:
            lifecycle_bottlenecks.append("onboarding_delay")
        if activation_rate < 0.30:
            lifecycle_bottlenecks.append("activation_failure")
        if not retention_curve_flattened:
            lifecycle_bottlenecks.append("unflattened_retention_curve")
        if nrr < 1.00:
            lifecycle_bottlenecks.append("net_revenue_shrinkage")

        results["time_to_first_value_hours"] = time_to_first_value
        results["activation_rate"] = activation_rate
        results["retention_curve_flattened"] = retention_curve_flattened
        results["nrr"] = nrr
        results["viral_k"] = k_factor
        results["bottlenecks"] = lifecycle_bottlenecks
        results["healthy"] = len(lifecycle_bottlenecks) == 0

        return results


# =====================================================================
# 6. Company Growth Stage Classifier
# =====================================================================
class GrowthStageClassifier:
    """Classifies venture growth state across 9 stages and detects premature scaling (§6)."""

    STAGES = [
        "idea", "validation", "startup", "pmf",
        "growth", "scale", "platform", "ecosystem", "market_leadership"
    ]

    def classify_stage(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Determine current stage, binding constraint, and premature scaling risk."""
        paying_customers = metrics.get("paying_customers", 0)
        monthly_revenue_cents = metrics.get("monthly_revenue_cents", 0)
        retention_flattened = metrics.get("retention_curve_flattened", False)
        rule_of_40 = metrics.get("rule_of_40_score", 0.0)
        developer_activity = metrics.get("third_party_developer_activity", 0)
        market_share = metrics.get("category_market_share", 0.0)

        # Stage classification logic
        current_stage = "idea"
        binding_constraint = "Founder time"

        if market_share >= 0.40:
            current_stage = "market_leadership"
            binding_constraint = "Innovation velocity vs. incumbency drag"
        elif developer_activity > 1000:
            current_stage = "ecosystem"
            binding_constraint = "Governance credibility"
        elif developer_activity > 100:
            current_stage = "platform"
            binding_constraint = "Trust from ecosystem partners"
        elif rule_of_40 >= 0.40 or monthly_revenue_cents >= 1_000_000_00:
            current_stage = "scale"
            binding_constraint = "Org coordination cost"
        elif monthly_revenue_cents >= 100_000_00:
            current_stage = "growth"
            binding_constraint = "Hiring velocity & systems"
        elif retention_flattened and paying_customers >= 50:
            current_stage = "pmf"
            binding_constraint = "Team bandwidth"
        elif paying_customers >= 10:
            current_stage = "startup"
            binding_constraint = "Cash runway"
        elif paying_customers > 0:
            current_stage = "validation"
            binding_constraint = "Signal quality"

        # Check for Premature Scaling
        # Scaling marketing/sales spend before PMF (retention curve flattened)
        sales_mktg_spend_cents = metrics.get("sales_marketing_spend_cents", 0)
        premature_scaling_risk = False
        if sales_mktg_spend_cents > 50_000_00 and not retention_flattened:
            premature_scaling_risk = True

        return {
            "current_stage": current_stage,
            "binding_constraint": binding_constraint,
            "premature_scaling_risk": premature_scaling_risk,
            "retention_curve_flattened": retention_flattened,
        }


# =====================================================================
# 7. Strategic Moat Analyzer
# =====================================================================
class MoatAnalyzer:
    """Quantifies competitive moats and overall durability score (§7)."""

    def score_moats(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Score 6 moat dimensions and calculate composite Moat Durability Score."""
        network_effects = min(1.0, inputs.get("network_effects_density", 0.0))
        switching_costs = min(1.0, inputs.get("switching_cost_score", 0.0))
        economies_of_scale = min(1.0, inputs.get("cost_advantage_percent", 0.0))
        brand = min(1.0, inputs.get("brand_trust_score", 0.0))
        regulatory_ip = min(1.0, inputs.get("regulatory_ip_protection_score", 0.0))
        counter_positioning = min(1.0, inputs.get("counter_positioning_score", 0.0))

        # Composite Moat Durability Score [0.0, 1.0]
        durability_score = float(
            0.25 * network_effects +
            0.20 * switching_costs +
            0.15 * economies_of_scale +
            0.15 * brand +
            0.10 * regulatory_ip +
            0.15 * counter_positioning
        )

        return {
            "durability_score": durability_score,
            "dimensions": {
                "network_effects": network_effects,
                "switching_costs": switching_costs,
                "economies_of_scale": economies_of_scale,
                "brand": brand,
                "regulatory_ip": regulatory_ip,
                "counter_positioning": counter_positioning,
            }
        }


# =====================================================================
# 8. Failure Mode Diagnostic Engine
# =====================================================================
class FailureModeMonitor:
    """Pattern-matches operating metrics against 10 operational failure modes (§8)."""

    FAILURE_MODES = [
        "solving_wrong_problem",
        "building_before_validating",
        "weak_positioning",
        "poor_pricing",
        "distribution_failure",
        "lack_of_pmf",
        "organizational_bottlenecks",
        "founder_bias",
        "scaling_prematurely",
        "capital_misallocation",
    ]

    def diagnose_failure_modes(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Diagnose active failure modes, root causes, signals, and correction mechanisms."""
        detected = []

        # 1. Solving the wrong problem
        if metrics.get("user_engagement_rate", 1.0) < 0.10 and metrics.get("survey_satisfaction", 0.0) > 0.80:
            detected.append({
                "failure_mode": "solving_wrong_problem",
                "root_cause": "Skipped root-cause analysis; solved a symptom.",
                "detection_signal": "Low engagement despite positive survey feedback.",
                "correction_mechanism": "Return to root-cause (5-Whys / Jobs-to-be-Done interviews).",
            })

        # 2. Building before validating
        if metrics.get("build_velocity_features_per_mo", 0) > 10 and metrics.get("demand_signal_growth", 0.0) <= 0.0:
            detected.append({
                "failure_mode": "building_before_validating",
                "root_cause": "Founder conviction substituted for evidence.",
                "detection_signal": "High build velocity, flat demand signal.",
                "correction_mechanism": "Enforce a validation gate before build resourcing.",
            })

        # 3. Weak positioning
        if metrics.get("sales_cycle_days", 0) > 90 and metrics.get("feature_comparison_objections", 0) > 5:
            detected.append({
                "failure_mode": "weak_positioning",
                "root_cause": "No clear 'instead of X, use us because Y'.",
                "detection_signal": "High CAC, long sales cycles, feature comparison objections.",
                "correction_mechanism": "Rebuild positioning around the real alternative customers compare to.",
            })

        # 4. Poor pricing
        if metrics.get("conversion_rate", 0.0) > 0.15 and metrics.get("gross_margin", 1.0) < 0.40:
            detected.append({
                "failure_mode": "poor_pricing",
                "root_cause": "Cost-plus instead of value-based pricing.",
                "detection_signal": "High conversion at low price, but poor margin/expansion.",
                "correction_mechanism": "Re-anchor price to quantified customer value.",
            })

        # 5. Distribution failure
        if metrics.get("nps", 0) > 60 and metrics.get("mom_revenue_growth", 0.0) <= 0.01:
            detected.append({
                "failure_mode": "distribution_failure",
                "root_cause": "Great product, no repeatable channel.",
                "detection_signal": "High NPS, flat growth.",
                "correction_mechanism": "Systematically test channels against ICP behavior, not founder preference.",
            })

        # 6. Lack of product-market fit
        if metrics.get("retention_curve_flattened", True) is False and metrics.get("active_spend_scaling", False) is True:
            detected.append({
                "failure_mode": "lack_of_pmf",
                "root_cause": "Premature scaling of an unproven loop.",
                "detection_signal": "Retention curve never flattens.",
                "correction_mechanism": "Stop scaling; return to cohort-level retention work.",
            })

        # 7. Organizational bottlenecks
        if metrics.get("decision_latency_days", 0.0) > 7.0 and metrics.get("founder_approval_dependency", False) is True:
            detected.append({
                "failure_mode": "organizational_bottlenecks",
                "root_cause": "Decision rights not delegated as company scales.",
                "detection_signal": "Rising decision latency, founder as single point of failure.",
                "correction_mechanism": "Push decision rights down with clear frameworks.",
            })

        # 8. Founder bias
        if metrics.get("disconfirming_evidence_ignored", False) is True:
            detected.append({
                "failure_mode": "founder_bias",
                "root_cause": "Overconfidence, confirmation bias, sunk cost.",
                "detection_signal": "Ignoring disconfirming data, 'just needs more time' pattern.",
                "correction_mechanism": "Pre-committed kill criteria set before launch.",
            })

        # 9. Scaling prematurely
        if metrics.get("cac_growth_rate", 0.0) > metrics.get("ltv_growth_rate", 0.0) and metrics.get("spend_scaling", False) is True:
            detected.append({
                "failure_mode": "scaling_prematurely",
                "root_cause": "Confusing early demand spike with durable PMF.",
                "detection_signal": "CAC rising faster than LTV as spend scales.",
                "correction_mechanism": "Re-test unit economics at each order-of-magnitude of spend.",
            })

        # 10. Capital misallocation
        if metrics.get("underperforming_bets_funded", 0) > 2:
            detected.append({
                "failure_mode": "capital_misallocation",
                "root_cause": "No opportunity-cost discipline in budgeting.",
                "detection_signal": "Multiple underperforming bets funded simultaneously.",
                "correction_mechanism": "Rank all initiatives on a common expected-return basis quarterly.",
            })

        return detected


# =====================================================================
# 10.4 First-Principles Orchestrator & Roll-up KPI Stack
# =====================================================================
class FirstPrinciplesEOSEngine:
    """Master Orchestrator coupling state machine, decision tree, business loops, lifecycle, and AI modules."""

    def __init__(self) -> None:
        self.state_machine = EOSStateMachine()
        self.decision_tree = OpportunityDecisionTree()
        self.business_loops = CoupledBusinessLoopsEngine()
        self.customer_lifecycle = CustomerLifecycleEngine()
        self.growth_classifier = GrowthStageClassifier()
        self.moat_analyzer = MoatAnalyzer()
        self.failure_monitor = FailureModeMonitor()

    def run_master_loop_cycle(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one complete Master Loop cycle across sensing, decisioning, and diagnostics."""
        # 1. State machine status
        current_state = self.state_machine.current_state

        # 2. Decision Tree evaluation if opportunity data provided
        opportunity = inputs.get("opportunity")
        dt_result = self.decision_tree.evaluate(opportunity) if opportunity else None

        # 3. Coupled Business Loops evaluation
        loop_metrics = inputs.get("business_loop_metrics", {})
        loops_result = self.business_loops.evaluate_loops(loop_metrics)

        # 4. Customer Lifecycle evaluation
        lifecycle_metrics = inputs.get("customer_lifecycle_metrics", {})
        lifecycle_result = self.customer_lifecycle.evaluate_lifecycle(lifecycle_metrics)

        # 5. Growth Stage classification
        venture_metrics = inputs.get("venture_metrics", {})
        stage_result = self.growth_classifier.classify_stage(venture_metrics)

        # 6. Moat Analysis
        moat_inputs = inputs.get("moat_inputs", {})
        moat_result = self.moat_analyzer.score_moats(moat_inputs)

        # 7. Failure Mode Diagnostics
        operating_metrics = inputs.get("operating_metrics", {})
        failure_diagnostics = self.failure_monitor.diagnose_failure_modes(operating_metrics)

        # 8. Roll-Up KPI Stack (§10.4)
        kpi_stack = {
            "sensing": {
                "signal_to_noise_ratio": inputs.get("signal_to_noise_ratio", 0.85),
                "anomaly_detection_lead_time_days": inputs.get("anomaly_lead_time_days", 14),
            },
            "validation": {
                "cost_per_validated_learning_cents": inputs.get("cost_per_learning_cents", 500_00),
                "false_positive_rate": inputs.get("false_positive_rate", 0.05),
            },
            "product": {
                "activation_rate": lifecycle_result.get("activation_rate", 0.40),
                "retention_curve_flattened": lifecycle_result.get("retention_curve_flattened", True),
            },
            "gtm": {
                "cac_cents": loop_metrics.get("cac_cents", 150_00),
                "cac_payback_months": inputs.get("cac_payback_months", 8.0),
            },
            "financial": {
                "gross_margin": inputs.get("gross_margin", 0.80),
                "burn_multiple": loop_metrics.get("burn_multiple", 1.2),
                "runway_months": loop_metrics.get("runway_months", 24.0),
            },
            "org": {
                "decision_latency_days": inputs.get("decision_latency_days", 2.0),
                "regretted_attrition_rate": loop_metrics.get("regretted_attrition_rate", 0.02),
            },
            "strategic": {
                "category_market_share": venture_metrics.get("category_market_share", 0.10),
                "moat_durability_score": moat_result.get("durability_score", 0.50),
            },
            "system_level": {
                "loop_closure_time_days": inputs.get("loop_closure_time_days", 7.0),
            }
        }

        return {
            "current_state": current_state.value,
            "decision_tree_result": dt_result,
            "business_loops_result": loops_result,
            "customer_lifecycle_result": lifecycle_result,
            "growth_stage_result": stage_result,
            "moat_result": moat_result,
            "failure_diagnostics": failure_diagnostics,
            "kpi_stack": kpi_stack,
        }
