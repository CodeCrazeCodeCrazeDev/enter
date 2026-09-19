"""
The First-Principles Executable Engine for the Entrepreneurial Operating System (EOS).

Reconstructs founder sensing, building, customer lifecycle, GTM system dynamics,
company growth stages, failure mode diagnostics, strategic moats, and AI state machine.
"""

from __future__ import annotations
import math
import logging
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger("sero.eos_first_principles")


class EOSState(str, Enum):
    """The 12 states of the EOS System State Machine (§10.1)."""
    SENSING = "sensing"
    HYPOTHESIS = "hypothesis"
    CHEAP_TEST = "cheap_test"
    VALIDATION = "validation"
    BUILD_GATE = "build_gate"
    MVP = "mvp"
    GTM_TEST = "gtm_test"
    KILL_OR_SCALE = "kill_or_scale"
    SCALE = "scale"
    OPERATE = "operate"
    REINVENT = "reinvent"
    DISCARD = "discard"


class EOSStateMachine(BaseModel):
    """
    Executes and tracks transitions across the AI-driven system state machine (§10.1).
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    current_state: EOSState = EOSState.SENSING
    history: List[Dict[str, Any]] = Field(default_factory=list)

    # Valid transitions mapping per state diagram
    VALID_TRANSITIONS: Dict[EOSState, List[EOSState]] = {
        EOSState.SENSING: [EOSState.HYPOTHESIS],
        EOSState.HYPOTHESIS: [EOSState.CHEAP_TEST],
        EOSState.CHEAP_TEST: [EOSState.DISCARD, EOSState.VALIDATION],
        EOSState.DISCARD: [EOSState.SENSING],
        EOSState.VALIDATION: [EOSState.BUILD_GATE, EOSState.DISCARD],
        EOSState.BUILD_GATE: [EOSState.MVP],
        EOSState.MVP: [EOSState.GTM_TEST],
        EOSState.GTM_TEST: [EOSState.KILL_OR_SCALE],
        EOSState.KILL_OR_SCALE: [EOSState.DISCARD, EOSState.SCALE],
        EOSState.SCALE: [EOSState.OPERATE],
        EOSState.OPERATE: [EOSState.REINVENT],
        EOSState.REINVENT: [EOSState.SENSING]
    }

    def can_transition_to(self, target_state: EOSState) -> bool:
        """Checks if transitioning to target state is valid from current state."""
        allowed = self.VALID_TRANSITIONS.get(self.current_state, [])
        return target_state in allowed

    def transition(self, target_state: EOSState, reason: str = "") -> EOSState:
        """
        Transitions system to a new state if valid.
        Logs transition in history.
        """
        if not self.can_transition_to(target_state):
            raise ValueError(
                f"Invalid transition from {self.current_state.value} to {target_state.value}."
            )

        prev_state = self.current_state
        self.current_state = target_state
        entry = {
            "from": prev_state.value,
            "to": target_state.value,
            "reason": reason
        }
        self.history.append(entry)
        logger.info(f"EOS State Machine transitioned: {prev_state.value} -> {target_state.value} ({reason})")
        return self.current_state

    def reset_to_sensing(self, reason: str = "reset") -> EOSState:
        """Resets the state machine back to SENSING from DISCARD or REINVENT."""
        if self.current_state in [EOSState.DISCARD, EOSState.REINVENT]:
            return self.transition(EOSState.SENSING, reason=reason)
        self.current_state = EOSState.SENSING
        self.history.append({"from": "forced_reset", "to": EOSState.SENSING.value, "reason": reason})
        return self.current_state


class OpportunityDecisionTree:
    """
    Executes the decision tree flowchart (§10.2): 'Should We Pursue This Opportunity?'
    """

    def evaluate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Traverses the opportunity pursuit decision tree logic.
        """
        path = []

        # Q1: Structural anomaly or just noise?
        is_structural = payload.get("is_structural_anomaly", False)
        if not is_structural:
            path.append("Q1: Noise detected -> Discard")
            return {
                "pursue": False,
                "recommendation": "Discard opportunity as noise.",
                "decision_path": path
            }
        path.append("Q1: Structural anomaly confirmed")

        # Q2: Reversible decision?
        is_reversible = payload.get("is_reversible_decision", True) # Type II vs Type I
        if not is_reversible:
            path.append("Q2: Irreversible / High Stakes (Type I)")
            # Q2a: High-confidence signal from multiple sources?
            high_conf = payload.get("high_confidence_multi_source", False)
            if not high_conf:
                path.append("Q2a: Insufficient high-confidence multi-source signal -> Discard")
                return {
                    "pursue": False,
                    "recommendation": "Discard due to high irreversible risk without multi-source confidence.",
                    "decision_path": path
                }
            path.append("Q2a: High-confidence multi-source signal validated")
        else:
            path.append("Q2: Reversible / Low Stakes (Type II)")

        # Q3: Cheap test available?
        cheap_test_avail = payload.get("cheap_test_available", True)
        if cheap_test_avail:
            path.append("Q3: Cheap test available -> Execute test")
            # Q4: Result exceeds kill threshold?
            test_passed = payload.get("test_result_exceeds_kill_threshold", False)
            if not test_passed:
                path.append("Q4: Cheap test failed kill threshold -> Discard")
                return {
                    "pursue": False,
                    "recommendation": "Discard; cheap test failed to meet kill threshold.",
                    "decision_path": path
                }
            path.append("Q4: Cheap test passed kill threshold")
        else:
            path.append("Q3: No cheap test available")
            # Q4b: Expected value clearly positive?
            ev_positive = payload.get("expected_value_positive", False)
            if not ev_positive:
                path.append("Q4b: Expected value not clearly positive -> Discard")
                return {
                    "pursue": False,
                    "recommendation": "Discard; EV is not clearly positive given available data.",
                    "decision_path": path
                }
            path.append("Q4b: Expected value clearly positive")

        # Q5: Structural advantage exist or buildable?
        structural_adv = payload.get("structural_advantage_exists", False)
        if not structural_adv:
            path.append("Q5: No structural advantage existing or buildable -> Discard")
            return {
                "pursue": False,
                "recommendation": "Discard; lack of defensible structural advantage.",
                "decision_path": path
            }

        path.append("Q5: Structural advantage validated -> Commit resources")
        return {
            "pursue": True,
            "recommendation": "Commit resources to pursue opportunity.",
            "decision_path": path
        }


class CoupledBusinessLoopsEngine:
    """
    Models and simulates the 13 coupled external business loops (§3)
    and system stocks/flows.
    """

    LOOPS = [
        "product", "marketing", "sales", "customer_success",
        "brand", "pricing", "referral", "data", "financial",
        "hiring", "culture", "innovation", "competitive_intelligence"
    ]

    def evaluate_system_dynamics(
        self,
        stocks: Dict[str, float],
        flows: Dict[str, float],
        loop_signals: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Computes loop health, stock balances, and leverage point analysis.
        Stocks: cash, talent, trust, data
        Flows: revenue, hiring_rate, churn_rate, experiment_velocity
        """
        cash = stocks.get("cash", 100000.0)
        talent = stocks.get("talent", 10.0)
        trust = stocks.get("trust", 0.8)  # 0.0 - 1.0
        data_asset = stocks.get("data", 50.0)

        revenue_flow = flows.get("revenue", 20000.0)
        hiring_flow = flows.get("hiring_rate", 1.0)
        churn_flow = flows.get("churn_rate", 0.05)

        # High-leverage coupling points
        pricing_arpu = loop_signals.get("pricing", {}).get("arpu", 100.0)
        hiring_quality = loop_signals.get("hiring", {}).get("quality_score", 0.8)

        # Coupled effects
        financial_capacity = cash + (revenue_flow * 12)
        hiring_leverage = hiring_quality * talent
        product_loop_velocity = (data_asset / 100.0) * trust * hiring_leverage

        burn_multiple = loop_signals.get("financial", {}).get("burn_multiple", 1.5)
        runway_months = cash / max(1.0, flows.get("burn_rate", 10000.0))

        leverage_points = {
            "pricing_to_financial": pricing_arpu * (1.0 - churn_flow),
            "hiring_to_execution": hiring_leverage,
            "data_to_product": product_loop_velocity
        }

        loop_health = {}
        for loop_name in self.LOOPS:
            sig = loop_signals.get(loop_name, {})
            score = sig.get("health_score", 0.7)
            loop_health[loop_name] = {
                "health_score": score,
                "status": "healthy" if score >= 0.7 else ("warning" if score >= 0.4 else "critical")
            }

        return {
            "stocks": {
                "cash": cash,
                "talent": talent,
                "trust": trust,
                "data": data_asset
            },
            "financial_runway_months": runway_months,
            "burn_multiple": burn_multiple,
            "leverage_points": leverage_points,
            "loop_health": loop_health
        }


class CustomerLifecycleEngine:
    """
    Models the 15 stages of the full customer journey lifecycle (§4).
    """

    STAGES = [
        "awareness", "interest", "consideration", "evaluation", "purchase",
        "onboarding", "activation", "engagement", "habit_formation",
        "retention", "loyalty", "advocacy", "referral", "expansion", "repurchase"
    ]

    def evaluate_lifecycle(self, stage_conversions: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyzes customer lifecycle stage conversions, identifying bottlenecks and aha moments.
        """
        bottlenecks = []
        lowest_stage = "awareness"
        lowest_conversion = 1.0

        for stage in self.STAGES:
            conv = stage_conversions.get(stage, 0.5)
            if conv < lowest_conversion:
                lowest_conversion = conv
                lowest_stage = stage
            if conv < 0.2:
                bottlenecks.append({"stage": stage, "conversion": conv})

        activation_rate = stage_conversions.get("activation", 0.4)
        nrr = stage_conversions.get("expansion", 1.1)  # Net Revenue Retention ratio e.g. 1.15
        viral_k = stage_conversions.get("referral", 0.1)  # K-factor

        return {
            "primary_bottleneck_stage": lowest_stage,
            "lowest_stage_conversion": lowest_conversion,
            "critical_bottlenecks": bottlenecks,
            "activation_rate": activation_rate,
            "net_revenue_retention": nrr,
            "viral_coefficient_k": viral_k,
            "retention_flattened": stage_conversions.get("retention", 0.5) >= 0.3
        }


class GrowthStageClassifier:
    """
    Classifies company growth stages (Idea -> Market Leadership) per §6.
    """

    STAGES = [
        "idea", "validation", "startup", "pmf",
        "growth", "scale", "platform", "ecosystem", "market_leadership"
    ]

    def classify(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classifies venture stage and detects premature scaling risks.
        """
        arr = metrics.get("arr_cents", 0)
        retention_flattened = metrics.get("retention_curve_flattened", False)
        paying_customers = metrics.get("paying_customers", 0)
        cac_payback_months = metrics.get("cac_payback_months", 24.0)

        # Stage determination logic
        if arr == 0 and paying_customers == 0:
            stage = "idea" if metrics.get("validated_learnings", 0) < 5 else "validation"
        elif paying_customers < 20 and not retention_flattened:
            stage = "startup"
        elif retention_flattened and arr < 100000000:  # < $1M ARR
            stage = "pmf"
        elif arr < 1000000000:  # < $10M ARR
            stage = "growth"
        elif arr < 5000000000:  # < $50M ARR
            stage = "scale"
        elif metrics.get("has_developer_platform", False):
            stage = "platform" if not metrics.get("multi_sided_network", False) else "ecosystem"
        else:
            stage = "market_leadership"

        # Check premature scaling
        premature_scaling = (
            (stage in ["startup", "validation"]) and
            (metrics.get("monthly_marketing_spend", 0) > 50000) and
            not retention_flattened
        )

        stage_details = {
            "idea": {"primary_objective": "Falsify or strengthen hypothesis", "constraint": "Founder time"},
            "validation": {"primary_objective": "Prove willingness to pay", "constraint": "Signal quality"},
            "startup": {"primary_objective": "Build repeatable acquisition", "constraint": "Cash runway"},
            "pmf": {"primary_objective": "Reach retention/growth threshold", "constraint": "Team bandwidth"},
            "growth": {"primary_objective": "Scale what works", "constraint": "Hiring velocity, systems"},
            "scale": {"primary_objective": "Institutionalize repeatability", "constraint": "Org coordination cost"},
            "platform": {"primary_objective": "Enable others to build on you", "constraint": "Trust from ecosystem partners"},
            "ecosystem": {"primary_objective": "Orchestrate multi-sided network", "constraint": "Governance credibility"},
            "market_leadership": {"primary_objective": "Defend and extend category", "constraint": "Innovation velocity vs incumbency drag"}
        }

        details = stage_details.get(stage, stage_details["idea"])

        return {
            "current_stage": stage,
            "primary_objective": details["primary_objective"],
            "binding_constraint": details["constraint"],
            "premature_scaling_alert": premature_scaling,
            "cac_payback_months": cac_payback_months
        }


class MoatAnalyzer:
    """
    Evaluates competitive moats and advantage durability (§7).
    """

    MOAT_TYPES = [
        "network_effects", "switching_costs", "economies_of_scale",
        "brand", "regulatory_ip", "counter_positioning"
    ]

    def analyze(self, moat_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Computes total moat durability score and identifies primary competitive moat.
        """
        weights = {
            "network_effects": 0.25,
            "switching_costs": 0.20,
            "counter_positioning": 0.20,
            "economies_of_scale": 0.15,
            "brand": 0.10,
            "regulatory_ip": 0.10
        }

        total_score = 0.0
        dominant_moat = "none"
        max_score = -1.0

        for moat_type in self.MOAT_TYPES:
            score = max(0.0, min(1.0, moat_scores.get(moat_type, 0.0)))
            weight = weights.get(moat_type, 0.1)
            total_score += score * weight

            if score > max_score:
                max_score = score
                dominant_moat = moat_type

        return {
            "moat_durability_score": round(total_score, 4),
            "dominant_moat": dominant_moat,
            "has_defensible_moat": total_score >= 0.4,
            "vulnerabilities": [m for m, s in moat_scores.items() if s < 0.2]
        }


class FailureModeMonitor:
    """
    Diagnostic engine pattern-matching operating metrics against the 10 failure modes (§8).
    """

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
        "capital_misallocation"
    ]

    def diagnose(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identifies active failure mode risks and prescribes corrective mechanisms.
        """
        alerts = []

        # 1. Solving wrong problem: Low engagement despite survey interest
        if metrics.get("survey_satisfaction", 0.0) > 0.8 and metrics.get("daumau_ratio", 1.0) < 0.1:
            alerts.append({
                "failure_mode": "solving_wrong_problem",
                "root_cause": "Skipped root-cause analysis; solved a symptom",
                "detection_signal": "Low engagement despite positive survey feedback",
                "correction_mechanism": "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)"
            })

        # 2. Building before validating: High velocity, flat demand
        if metrics.get("feature_ship_velocity", 0) > 10 and metrics.get("demand_growth_rate", 0.0) <= 0.0:
            alerts.append({
                "failure_mode": "building_before_validating",
                "root_cause": "Founder conviction substituted for evidence",
                "detection_signal": "High build velocity, flat demand signal",
                "correction_mechanism": "Enforce a validation gate before build resourcing"
            })

        # 3. Weak positioning: High CAC, long sales cycle
        if metrics.get("sales_cycle_days", 0) > 90 and metrics.get("cac_dollars", 0) > 5000:
            alerts.append({
                "failure_mode": "weak_positioning",
                "root_cause": "No clear 'instead of X, use us because Y'",
                "detection_signal": "High CAC, long sales cycles, feature comparison objections",
                "correction_mechanism": "Rebuild positioning around the real alternative customers compare to"
            })

        # 4. Poor pricing: High conversion at low price, poor margin
        if metrics.get("trial_conversion_rate", 0.0) > 0.5 and metrics.get("gross_margin", 1.0) < 0.3:
            alerts.append({
                "failure_mode": "poor_pricing",
                "root_cause": "Cost-plus instead of value-based pricing",
                "detection_signal": "High conversion at low price, but poor margin/expansion",
                "correction_mechanism": "Re-anchor price to quantified customer value"
            })

        # 5. Distribution failure: High NPS, flat growth
        if metrics.get("nps", 0) > 60 and metrics.get("mom_growth_rate", 0.0) < 0.02:
            alerts.append({
                "failure_mode": "distribution_failure",
                "root_cause": "Great product, no repeatable channel",
                "detection_signal": "High NPS, flat growth",
                "correction_mechanism": "Systematically test channels against ICP behavior"
            })

        # 6. Lack of PMF: Retention curve never flattens
        if metrics.get("retention_curve_flat", None) is False:
            alerts.append({
                "failure_mode": "lack_of_pmf",
                "root_cause": "Premature scaling of an unproven loop",
                "detection_signal": "Retention curve never flattens",
                "correction_mechanism": "Stop scaling; return to cohort-level retention work"
            })

        # 7. Organizational bottlenecks: Rising decision latency
        if metrics.get("decision_latency_days", 0) > 14:
            alerts.append({
                "failure_mode": "organizational_bottlenecks",
                "root_cause": "Decision rights not delegated as company scales",
                "detection_signal": "Rising decision latency, founder as single point of failure",
                "correction_mechanism": "Push decision rights down with clear frameworks"
            })

        # 8. Founder bias: Ignoring disconfirming data
        if metrics.get("disconfirming_data_ignored_count", 0) > 2:
            alerts.append({
                "failure_mode": "founder_bias",
                "root_cause": "Overconfidence, confirmation bias, sunk cost",
                "detection_signal": "Ignoring disconfirming data, 'just needs more time' pattern",
                "correction_mechanism": "Pre-committed kill criteria set before launch"
            })

        # 9. Scaling prematurely: CAC rising faster than LTV
        if metrics.get("cac_growth_vs_ltv_ratio", 1.0) > 1.5:
            alerts.append({
                "failure_mode": "scaling_prematurely",
                "root_cause": "Confusing early demand spike with durable PMF",
                "detection_signal": "CAC rising faster than LTV as spend scales",
                "correction_mechanism": "Re-test unit economics at each order-of-magnitude of spend"
            })

        # 10. Capital misallocation: Multiple underperforming bets
        if metrics.get("underperforming_bets_count", 0) >= 3:
            alerts.append({
                "failure_mode": "capital_misallocation",
                "root_cause": "No opportunity-cost discipline in budgeting",
                "detection_signal": "Multiple underperforming bets funded simultaneously",
                "correction_mechanism": "Rank all initiatives on a common expected-return basis quarterly"
            })

        return alerts


class FirstPrinciplesEOSEngine:
    """
    Master Entrepreneurial Operating System Engine.
    Integrates State Machine, Decision Tree, Business Loops, Customer Lifecycle,
    Growth Classifier, Moat Analyzer, and Failure Mode Monitor.
    """

    def __init__(self) -> None:
        self.state_machine = EOSStateMachine()
        self.decision_tree = OpportunityDecisionTree()
        self.loops_engine = CoupledBusinessLoopsEngine()
        self.lifecycle_engine = CustomerLifecycleEngine()
        self.growth_classifier = GrowthStageClassifier()
        self.moat_analyzer = MoatAnalyzer()
        self.failure_monitor = FailureModeMonitor()

    def process_opportunity(self, opportunity_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a candidate opportunity signal through state machine and decision tree.
        """
        # Step 1: Sensing -> Hypothesis
        if self.state_machine.current_state == EOSState.SENSING:
            self.state_machine.transition(EOSState.HYPOTHESIS, reason="Anomaly detected")

        # Step 2: Decision Tree Evaluation
        decision = self.decision_tree.evaluate(opportunity_payload)

        # Step 3: Transition state machine based on decision
        if self.state_machine.current_state == EOSState.HYPOTHESIS:
            self.state_machine.transition(EOSState.CHEAP_TEST, reason="Hypothesis formed")

        if decision["pursue"]:
            if self.state_machine.current_state == EOSState.CHEAP_TEST:
                self.state_machine.transition(EOSState.VALIDATION, reason="Cheap test strengthened belief")
        else:
            if self.state_machine.current_state == EOSState.CHEAP_TEST:
                self.state_machine.transition(EOSState.DISCARD, reason=decision["recommendation"])

        return {
            "current_state": self.state_machine.current_state.value,
            "opportunity_decision": decision,
            "state_history": self.state_machine.history
        }

    def run_full_diagnostic(self, system_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs comprehensive system diagnostic across loops, lifecycle, growth stage, moats, and failure modes.
        """
        stocks = system_metrics.get("stocks", {})
        flows = system_metrics.get("flows", {})
        loop_signals = system_metrics.get("loop_signals", {})
        stage_conversions = system_metrics.get("stage_conversions", {})
        venture_metrics = system_metrics.get("venture_metrics", {})
        moat_scores = system_metrics.get("moat_scores", {})

        loops_res = self.loops_engine.evaluate_system_dynamics(stocks, flows, loop_signals)
        lifecycle_res = self.lifecycle_engine.evaluate_lifecycle(stage_conversions)
        growth_res = self.growth_classifier.classify(venture_metrics)
        moat_res = self.moat_analyzer.analyze(moat_scores)
        failure_alerts = self.failure_monitor.diagnose(system_metrics)

        return {
            "system_state": self.state_machine.current_state.value,
            "coupled_loops": loops_res,
            "customer_lifecycle": lifecycle_res,
            "growth_stage": growth_res,
            "moat_analysis": moat_res,
            "failure_mode_alerts": failure_alerts,
            "is_system_healthy": len(failure_alerts) == 0 and moat_res["has_defensible_moat"]
        }
