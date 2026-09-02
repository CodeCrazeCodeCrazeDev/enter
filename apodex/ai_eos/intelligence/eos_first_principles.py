"""First-Principles Entrepreneurial Operating System (EOS) Python Engine.

Implements executable state machines, decision trees, coupled business loops,
customer lifecycle tracking, growth stage classification, moat analysis, and failure mode monitoring
for the 11-section Entrepreneurial Operating System specification.
"""

from __future__ import annotations
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Set
from uuid import UUID, uuid4
from datetime import datetime

logger = logging.getLogger("apodex.ai_eos.eos_first_principles")


# =====================================================================
# Section 10.1 System State Machine
# =====================================================================
class EOSMasterLoopState(str, Enum):
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


class EOSStateMachine:
    """State machine governing venture evolution across master loop nodes."""

    def __init__(self, initial_state: EOSMasterLoopState = EOSMasterLoopState.SENSING) -> None:
        self.current_state = initial_state
        self.state_history: List[Dict[str, Any]] = [
            {"state": initial_state, "timestamp": datetime.utcnow(), "reason": "Initial state"}
        ]

    def transition(self, target_state: EOSMasterLoopState, reason: str) -> EOSMasterLoopState:
        """Transitions state and records historical trajectory with re-entrant loop tracking."""
        logger.info(f"EOS State Transition: {self.current_state.value} -> {target_state.value} ({reason})")
        self.current_state = target_state
        self.state_history.append({
            "state": target_state,
            "timestamp": datetime.utcnow(),
            "reason": reason
        })
        return self.current_state

    def process_signal(self, anomaly_detected: bool, test_passed: bool, economic_viable: bool, scale_signal: bool) -> EOSMasterLoopState:
        """Evaluates incoming signals to drive state transitions."""
        if self.current_state == EOSMasterLoopState.SENSING and anomaly_detected:
            return self.transition(EOSMasterLoopState.HYPOTHESIS, "Anomaly detected vs baseline")

        elif self.current_state == EOSMasterLoopState.HYPOTHESIS:
            return self.transition(EOSMasterLoopState.CHEAP_TEST, "Falsifiable hypothesis formed")

        elif self.current_state == EOSMasterLoopState.CHEAP_TEST:
            if test_passed:
                return self.transition(EOSMasterLoopState.VALIDATION, "Cheap test strengthened belief")
            else:
                return self.transition(EOSMasterLoopState.DISCARD, "Cheap test falsified hypothesis")

        elif self.current_state == EOSMasterLoopState.VALIDATION:
            if economic_viable:
                return self.transition(EOSMasterLoopState.BUILD_GATE, "Economic viability confirmed")
            else:
                return self.transition(EOSMasterLoopState.DISCARD, "No viable economics")

        elif self.current_state == EOSMasterLoopState.BUILD_GATE:
            return self.transition(EOSMasterLoopState.MVP, "Build resources committed")

        elif self.current_state == EOSMasterLoopState.MVP:
            return self.transition(EOSMasterLoopState.GTM_TEST, "MVP shipped to market")

        elif self.current_state == EOSMasterLoopState.GTM_TEST:
            return self.transition(EOSMasterLoopState.KILL_OR_SCALE, "GTM signal collected")

        elif self.current_state == EOSMasterLoopState.KILL_OR_SCALE:
            if scale_signal:
                return self.transition(EOSMasterLoopState.SCALE, "Above threshold signal - scaling")
            else:
                return self.transition(EOSMasterLoopState.DISCARD, "Below threshold signal - killing loop")

        elif self.current_state == EOSMasterLoopState.SCALE:
            return self.transition(EOSMasterLoopState.OPERATE, "Repeatable loop confirmed")

        elif self.current_state == EOSMasterLoopState.OPERATE:
            return self.transition(EOSMasterLoopState.REINVENT, "Market maturity / reinvention triggered")

        elif self.current_state == EOSMasterLoopState.REINVENT:
            return self.transition(EOSMasterLoopState.SENSING, "Re-entrant sensing cycle initiated")

        elif self.current_state == EOSMasterLoopState.DISCARD:
            return self.transition(EOSMasterLoopState.SENSING, "Re-entrant sensing after discard")

        return self.current_state


# =====================================================================
# Section 10.2 Decision Tree Evaluator
# =====================================================================
class OpportunityDecisionTree:
    """Evaluates opportunities: 'Should We Pursue This Opportunity?'"""

    def evaluate(
        self,
        is_structural_anomaly: bool,
        is_reversible_decision: bool,
        high_confidence_multi_source: bool,
        cheap_test_available: bool,
        cheap_test_result_exceeds_kill: Optional[bool],
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> Dict[str, Any]:
        """Runs decision tree evaluation path per Section 10.2 flowchart."""
        # Q1: Structural anomaly or just noise?
        if not is_structural_anomaly:
            return {"decision": "Discard", "reason": "Noise, not structural anomaly", "commit": False}

        # Q2: Reversible decision? (Type I vs Type II risk)
        if not is_reversible_decision:
            # Irreversible / Type I decision path -> requires high confidence signal
            if not high_confidence_multi_source:
                return {"decision": "Discard", "reason": "Irreversible decision lacking high-confidence multi-source signal", "commit": False}

        # Q3: Cheap test available?
        if cheap_test_available:
            if cheap_test_result_exceeds_kill is False:
                return {"decision": "Discard", "reason": "Cheap test result failed kill threshold", "commit": False}
            elif cheap_test_result_exceeds_kill is None:
                return {"decision": "Run cheap test", "reason": "Execute cheap test before resource commitment", "commit": False}
        else:
            if not expected_value_positive:
                return {"decision": "Discard", "reason": "Expected value not clearly positive", "commit": False}

        # Q5: Do we have or can we build a structural advantage here? (Moat filter)
        if not has_structural_advantage:
            return {"decision": "Discard", "reason": "No defensible structural advantage or moat potential", "commit": False}

        return {"decision": "Commit resources", "reason": "Opportunity passed all strategic and economic filters", "commit": True}


# =====================================================================
# Section 3 External Business Loops Engine
# =====================================================================
class CoupledBusinessLoopsEngine:
    """Evaluates and couples all 13 external business loops."""

    LOOPS = [
        "Product", "Marketing", "Sales", "Customer Success", "Brand",
        "Pricing", "Referral", "Data", "Financial", "Hiring",
        "Culture", "Innovation", "Competitive Intelligence"
    ]

    def evaluate_loops(self, loop_metrics: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Evaluates individual and coupled feedback loops across the 13 business dimensions."""
        results: Dict[str, Any] = {}
        health_scores: Dict[str, float] = {}

        # 1. Product Loop
        retention_slope = loop_metrics.get("Product", {}).get("retention_curve_slope", 0.0)
        nps = loop_metrics.get("Product", {}).get("nps", 0.0)
        health_scores["Product"] = min(1.0, max(0.0, (retention_slope + 0.5) * 0.5 + (nps / 100.0) * 0.5))

        # 2. Marketing Loop
        cac = loop_metrics.get("Marketing", {}).get("cac_cents", 10000)
        conversion_rate = loop_metrics.get("Marketing", {}).get("conversion_rate", 0.02)
        health_scores["Marketing"] = min(1.0, max(0.0, conversion_rate * 20.0 - (cac / 50000.0)))

        # 3. Sales Loop
        win_rate = loop_metrics.get("Sales", {}).get("win_rate", 0.20)
        health_scores["Sales"] = min(1.0, win_rate / 0.40)

        # 4. Customer Success Loop
        nrr = loop_metrics.get("Customer Success", {}).get("nrr", 1.0)
        churn_rate = loop_metrics.get("Customer Success", {}).get("churn_rate", 0.05)
        health_scores["Customer Success"] = min(1.0, max(0.0, (nrr - 0.8) + (0.10 - churn_rate)))

        # 5. Brand Loop
        price_elasticity = loop_metrics.get("Brand", {}).get("price_elasticity", -1.0)
        health_scores["Brand"] = min(1.0, max(0.0, 1.0 - abs(price_elasticity + 0.5)))

        # 6. Pricing Loop
        arpu_cents = loop_metrics.get("Pricing", {}).get("arpu_cents", 5000)
        price_realization = loop_metrics.get("Pricing", {}).get("price_realization", 0.8)
        health_scores["Pricing"] = min(1.0, (arpu_cents / 10000.0) * price_realization)

        # 7. Referral Loop
        k_factor = loop_metrics.get("Referral", {}).get("k_factor", 0.2)
        health_scores["Referral"] = min(1.0, k_factor / 1.0)

        # 8. Data Loop
        decision_cycle_time = loop_metrics.get("Data", {}).get("decision_cycle_time_hours", 24.0)
        health_scores["Data"] = min(1.0, max(0.0, 1.0 - (decision_cycle_time / 168.0)))

        # 9. Financial Loop
        burn_multiple = loop_metrics.get("Financial", {}).get("burn_multiple", 1.5)
        gross_margin = loop_metrics.get("Financial", {}).get("gross_margin", 0.7)
        health_scores["Financial"] = min(1.0, max(0.0, gross_margin - (burn_multiple / 5.0)))

        # 10. Hiring Loop
        time_to_fill = loop_metrics.get("Hiring", {}).get("time_to_fill_days", 45.0)
        health_scores["Hiring"] = min(1.0, max(0.0, 1.0 - (time_to_fill / 90.0)))

        # 11. Culture Loop
        decision_latency = loop_metrics.get("Culture", {}).get("decision_latency_hours", 12.0)
        enps = loop_metrics.get("Culture", {}).get("enps", 40.0)
        health_scores["Culture"] = min(1.0, max(0.0, (enps / 100.0) * 0.6 + (1.0 - decision_latency / 72.0) * 0.4))

        # 12. Innovation Loop
        experiments_run = loop_metrics.get("Innovation", {}).get("experiments_run", 5.0)
        hit_rate = loop_metrics.get("Innovation", {}).get("hit_rate", 0.2)
        health_scores["Innovation"] = min(1.0, (experiments_run / 20.0) * hit_rate * 5.0)

        # 13. Competitive Intelligence Loop
        feature_parity_gap = loop_metrics.get("Competitive Intelligence", {}).get("feature_parity_gap", 0.1)
        health_scores["Competitive Intelligence"] = min(1.0, max(0.0, 1.0 - feature_parity_gap))

        # Coupled interaction computation: Pricing (ARPU) -> Financial -> Hiring -> Product velocity
        arpu_impact = health_scores["Pricing"]
        financial_capacity = health_scores["Financial"] * arpu_impact
        hiring_velocity = health_scores["Hiring"] * financial_capacity
        coupled_system_health = sum(health_scores.values()) / len(health_scores)

        results["loop_health_scores"] = health_scores
        results["coupled_system_health"] = coupled_system_health
        results["pricing_to_product_coupling_factor"] = hiring_velocity
        return results


# =====================================================================
# Section 4 Customer Journey Lifecycle Engine
# =====================================================================
class CustomerLifecycleEngine:
    """Models cohort progression across all 15 customer journey stages."""

    STAGES = [
        "Awareness", "Interest", "Consideration", "Evaluation", "Purchase",
        "Onboarding", "Activation", "Engagement", "Habit Formation", "Retention",
        "Loyalty", "Advocacy", "Referral", "Expansion", "Repurchase"
    ]

    def evaluate_lifecycle_cohort(self, stage_conversions: Dict[str, float]) -> Dict[str, Any]:
        """Calculates funnel efficiency and identifies bottlenecks across the 15 stages."""
        stage_retention = 1.0
        funnel_drops: Dict[str, float] = {}

        for stage in self.STAGES:
            rate = stage_conversions.get(stage, 0.8)
            funnel_drops[stage] = 1.0 - rate
            stage_retention *= rate

        bottleneck_stage = max(funnel_drops.items(), key=lambda x: x[1])

        return {
            "overall_funnel_retention": stage_retention,
            "stage_drop_rates": funnel_drops,
            "primary_bottleneck_stage": bottleneck_stage[0],
            "primary_bottleneck_drop_rate": bottleneck_stage[1]
        }


# =====================================================================
# Section 6 Company Growth System Classifier
# =====================================================================
class GrowthStageClassifier:
    """Classifies venture stage across the 9 company growth stages."""

    STAGES = [
        "Idea", "Validation", "Startup", "Product-Market Fit",
        "Growth", "Scale", "Platform", "Ecosystem", "Market Leadership"
    ]

    def classify_stage(
        self,
        paying_customers: int,
        retention_curve_flattened: bool,
        monthly_growth_rate: float,
        rule_of_40: float,
        has_third_party_developers: bool,
        ecosystem_gmv_cents: int
    ) -> Dict[str, Any]:
        """Scores and classifies venture stage based on binding constraints and metrics."""
        if ecosystem_gmv_cents > 100_000_000_00 and has_third_party_developers:
            stage = "Market Leadership"
        elif ecosystem_gmv_cents > 10_000_000_00:
            stage = "Ecosystem"
        elif has_third_party_developers:
            stage = "Platform"
        elif rule_of_40 >= 0.40 and paying_customers > 1000:
            stage = "Scale"
        elif monthly_growth_rate >= 0.15 and retention_curve_flattened:
            stage = "Growth"
        elif retention_curve_flattened:
            stage = "Product-Market Fit"
        elif paying_customers >= 10:
            stage = "Startup"
        elif paying_customers > 0:
            stage = "Validation"
        else:
            stage = "Idea"

        # Detect premature scaling risk
        premature_scaling_risk = False
        if stage in ["Growth", "Scale"] and not retention_curve_flattened:
            premature_scaling_risk = True

        return {
            "classified_stage": stage,
            "stage_index": self.STAGES.index(stage),
            "premature_scaling_risk": premature_scaling_risk
        }


# =====================================================================
# Section 7 Moat Analyzer
# =====================================================================
class MoatAnalyzer:
    """Scores competitive moats across the 7 core strategic power types."""

    def score_moats(
        self,
        network_effects_score: float,
        switching_costs_score: float,
        scale_economies_score: float,
        brand_equity_score: float,
        regulatory_ip_score: float,
        counter_positioning_score: float,
        cornered_resource_score: float
    ) -> Dict[str, Any]:
        """Calculates composite moat durability index."""
        scores = {
            "network_effects": min(1.0, max(0.0, network_effects_score)),
            "switching_costs": min(1.0, max(0.0, switching_costs_score)),
            "scale_economies": min(1.0, max(0.0, scale_economies_score)),
            "brand_equity": min(1.0, max(0.0, brand_equity_score)),
            "regulatory_ip": min(1.0, max(0.0, regulatory_ip_score)),
            "counter_positioning": min(1.0, max(0.0, counter_positioning_score)),
            "cornered_resource": min(1.0, max(0.0, cornered_resource_score)),
        }

        # Weighted composite index
        weights = {
            "network_effects": 0.20,
            "switching_costs": 0.20,
            "scale_economies": 0.15,
            "brand_equity": 0.10,
            "regulatory_ip": 0.10,
            "counter_positioning": 0.15,
            "cornered_resource": 0.10
        }

        composite_moat_index = sum(scores[k] * weights[k] for k in scores)

        return {
            "individual_moat_scores": scores,
            "composite_moat_durability_index": composite_moat_index,
            "dominant_moat_type": max(scores.items(), key=lambda x: x[1])[0]
        }


# =====================================================================
# Section 8 Failure Mode Monitor
# =====================================================================
class FailureModeMonitor:
    """Pattern-matches operating metrics against the 10 failure modes."""

    FAILURE_MODES = [
        "Solving the wrong problem",
        "Building before validating",
        "Weak positioning",
        "Poor pricing",
        "Distribution failure",
        "Lack of product-market fit",
        "Organizational bottlenecks",
        "Founder bias",
        "Scaling prematurely",
        "Capital misallocation"
    ]

    def audit_operating_metrics(
        self,
        survey_vs_usage_gap: float,
        build_velocity_high_demand_flat: bool,
        sales_cycle_days: float,
        cac_rising_faster_than_ltv: bool,
        retention_never_flattens: bool,
        decision_latency_hours: float,
        precommitted_kill_criteria_ignored: bool,
        underperforming_bets_funded: int
    ) -> List[Dict[str, str]]:
        """Audits operating parameters and returns active failure warnings with corrective mechanisms."""
        warnings: List[Dict[str, str]] = []

        if survey_vs_usage_gap > 0.40:
            warnings.append({
                "failure_mode": "Solving the wrong problem",
                "root_cause": "Skipped root-cause analysis; solved a symptom",
                "detection_signal": "Low engagement despite positive survey feedback",
                "correction_mechanism": "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)"
            })

        if build_velocity_high_demand_flat:
            warnings.append({
                "failure_mode": "Building before validating",
                "root_cause": "Founder conviction substituted for evidence",
                "detection_signal": "High build velocity, flat demand signal",
                "correction_mechanism": "Enforce a validation gate before build resourcing"
            })

        if sales_cycle_days > 120.0:
            warnings.append({
                "failure_mode": "Weak positioning",
                "root_cause": "No clear 'instead of X, use us because Y'",
                "detection_signal": "High CAC, long sales cycles, feature comparison objections",
                "correction_mechanism": "Rebuild positioning around real alternative customers compare to"
            })

        if retention_never_flattens:
            warnings.append({
                "failure_mode": "Lack of product-market fit",
                "root_cause": "Premature scaling of an unproven loop",
                "detection_signal": "Retention curve never flattens",
                "correction_mechanism": "Stop scaling; return to cohort-level retention work"
            })

        if decision_latency_hours > 48.0:
            warnings.append({
                "failure_mode": "Organizational bottlenecks",
                "root_cause": "Decision rights not delegated as company scales",
                "detection_signal": "Rising decision latency, founder as single point of failure",
                "correction_mechanism": "Push decision rights down with clear frameworks"
            })

        if precommitted_kill_criteria_ignored:
            warnings.append({
                "failure_mode": "Founder bias",
                "root_cause": "Overconfidence, confirmation bias, sunk cost",
                "detection_signal": "Ignoring disconfirming data, 'just needs more time' pattern",
                "correction_mechanism": "Enforce pre-committed kill criteria set before launch"
            })

        if cac_rising_faster_than_ltv:
            warnings.append({
                "failure_mode": "Scaling prematurely",
                "root_cause": "Confusing early demand spike with durable PMF",
                "detection_signal": "CAC rising faster than LTV as spend scales",
                "correction_mechanism": "Re-test unit economics at each order-of-magnitude of spend"
            })

        if underperforming_bets_funded > 2:
            warnings.append({
                "failure_mode": "Capital misallocation",
                "root_cause": "No opportunity-cost discipline in budgeting",
                "detection_signal": "Multiple underperforming bets funded simultaneously",
                "correction_mechanism": "Rank all initiatives on a common expected-return basis quarterly"
            })

        return warnings


# =====================================================================
# First-Principles Entrepreneurial Operating System Orchestrator
# =====================================================================
class FirstPrinciplesEOSEngine:
    """Master Orchestrator integrating all 11 sections of the Entrepreneurial Operating System."""

    def __init__(self) -> None:
        self.state_machine = EOSStateMachine()
        self.decision_tree = OpportunityDecisionTree()
        self.business_loops = CoupledBusinessLoopsEngine()
        self.customer_lifecycle = CustomerLifecycleEngine()
        self.growth_classifier = GrowthStageClassifier()
        self.moat_analyzer = MoatAnalyzer()
        self.failure_monitor = FailureModeMonitor()

    def run_cycle(self, telemetry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Runs a complete first-principles EOS sensing, decision, evaluation, and diagnostic loop."""
        # 1. Evaluate opportunity decision tree
        opportunity_eval = self.decision_tree.evaluate(
            is_structural_anomaly=telemetry_data.get("is_structural_anomaly", True),
            is_reversible_decision=telemetry_data.get("is_reversible_decision", True),
            high_confidence_multi_source=telemetry_data.get("high_confidence_multi_source", True),
            cheap_test_available=telemetry_data.get("cheap_test_available", True),
            cheap_test_result_exceeds_kill=telemetry_data.get("cheap_test_result_exceeds_kill", True),
            expected_value_positive=telemetry_data.get("expected_value_positive", True),
            has_structural_advantage=telemetry_data.get("has_structural_advantage", True)
        )

        # 2. State machine processing
        state = self.state_machine.process_signal(
            anomaly_detected=telemetry_data.get("anomaly_detected", True),
            test_passed=telemetry_data.get("test_passed", True),
            economic_viable=telemetry_data.get("economic_viable", True),
            scale_signal=telemetry_data.get("scale_signal", True)
        )

        # 3. External business loops evaluation
        loops_eval = self.business_loops.evaluate_loops(telemetry_data.get("loop_metrics", {}))

        # 4. Customer journey lifecycle evaluation
        lifecycle_eval = self.customer_lifecycle.evaluate_lifecycle_cohort(telemetry_data.get("stage_conversions", {}))

        # 5. Growth stage classification
        growth_eval = self.growth_classifier.classify_stage(
            paying_customers=telemetry_data.get("paying_customers", 50),
            retention_curve_flattened=telemetry_data.get("retention_curve_flattened", True),
            monthly_growth_rate=telemetry_data.get("monthly_growth_rate", 0.10),
            rule_of_40=telemetry_data.get("rule_of_40", 0.25),
            has_third_party_developers=telemetry_data.get("has_third_party_developers", False),
            ecosystem_gmv_cents=telemetry_data.get("ecosystem_gmv_cents", 0)
        )

        # 6. Strategic moat evaluation
        moats_eval = self.moat_analyzer.score_moats(
            network_effects_score=telemetry_data.get("network_effects_score", 0.5),
            switching_costs_score=telemetry_data.get("switching_costs_score", 0.6),
            scale_economies_score=telemetry_data.get("scale_economies_score", 0.4),
            brand_equity_score=telemetry_data.get("brand_equity_score", 0.7),
            regulatory_ip_score=telemetry_data.get("regulatory_ip_score", 0.3),
            counter_positioning_score=telemetry_data.get("counter_positioning_score", 0.8),
            cornered_resource_score=telemetry_data.get("cornered_resource_score", 0.5)
        )

        # 7. Failure mode diagnostic audit
        failure_warnings = self.failure_monitor.audit_operating_metrics(
            survey_vs_usage_gap=telemetry_data.get("survey_vs_usage_gap", 0.1),
            build_velocity_high_demand_flat=telemetry_data.get("build_velocity_high_demand_flat", False),
            sales_cycle_days=telemetry_data.get("sales_cycle_days", 30.0),
            cac_rising_faster_than_ltv=telemetry_data.get("cac_rising_faster_than_ltv", False),
            retention_never_flattens=telemetry_data.get("retention_never_flattens", False),
            decision_latency_hours=telemetry_data.get("decision_latency_hours", 12.0),
            precommitted_kill_criteria_ignored=telemetry_data.get("precommitted_kill_criteria_ignored", False),
            underperforming_bets_funded=telemetry_data.get("underperforming_bets_funded", 0)
        )

        return {
            "current_state": state.value,
            "opportunity_decision": opportunity_eval,
            "business_loops": loops_eval,
            "customer_lifecycle": lifecycle_eval,
            "growth_stage": growth_eval,
            "moat_durability": moats_eval,
            "failure_warnings": failure_warnings,
            "timestamp": datetime.utcnow()
        }
