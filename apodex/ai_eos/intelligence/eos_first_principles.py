"""Entrepreneurial Operating System (EOS) First-Principles Executable Engine.

An 11-section executable reconstruction of how elite founders sense, build,
and compound enduring companies, providing state machines, opportunity decision trees,
coupled business loop dynamics, customer lifecycle tracking, growth stage classification,
moat analysis, failure mode diagnostics, and master continuous sensing loops.
"""

from __future__ import annotations
import math
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID, uuid4
from datetime import datetime, timezone

from pydantic import BaseModel, Field

logger = logging.getLogger("sero.eos_first_principles")


# =====================================================================
# Section 10.1: System State Machine
# =====================================================================

class EOSState(str, Enum):
    SENSING = "Sensing"
    HYPOTHESIS = "Hypothesis"
    CHEAP_TEST = "CheapTest"
    DISCARD = "Discard"
    VALIDATION = "Validation"
    BUILD_GATE = "BuildGate"
    MVP = "MVP"
    GTM_TEST = "GTMTest"
    KILL_OR_SCALE = "KillOrScale"
    SCALE = "Scale"
    OPERATE = "Operate"
    REINVENT = "Reinvent"


class EOSStateMachine:
    """Enforces the official 12-state system state machine transition graph."""

    VALID_TRANSITIONS: Dict[EOSState, Set[EOSState]] = {
        EOSState.SENSING: {EOSState.HYPOTHESIS},
        EOSState.HYPOTHESIS: {EOSState.CHEAP_TEST},
        EOSState.CHEAP_TEST: {EOSState.DISCARD, EOSState.VALIDATION},
        EOSState.DISCARD: {EOSState.SENSING},
        EOSState.VALIDATION: {EOSState.BUILD_GATE, EOSState.DISCARD},
        EOSState.BUILD_GATE: {EOSState.MVP, EOSState.DISCARD},
        EOSState.MVP: {EOSState.GTM_TEST},
        EOSState.GTM_TEST: {EOSState.KILL_OR_SCALE},
        EOSState.KILL_OR_SCALE: {EOSState.DISCARD, EOSState.SCALE},
        EOSState.SCALE: {EOSState.OPERATE},
        EOSState.OPERATE: {EOSState.REINVENT},
        EOSState.REINVENT: {EOSState.SENSING},
    }

    def __init__(self, initial_state: EOSState = EOSState.SENSING) -> None:
        self.current_state: EOSState = initial_state
        self.history: List[Tuple[EOSState, datetime]] = [(initial_state, datetime.now(timezone.utc))]

    def can_transition_to(self, target_state: EOSState) -> bool:
        """Check if transition to target state is permissible."""
        valid_targets = self.VALID_TRANSITIONS.get(self.current_state, set())
        return target_state in valid_targets

    def transition_to(self, target_state: EOSState, reason: str = "") -> EOSState:
        """Execute state transition if valid, raising ValueError otherwise."""
        if not self.can_transition_to(target_state):
            raise ValueError(
                f"Invalid state transition from {self.current_state.value} to {target_state.value}. "
                f"Valid targets: {[s.value for s in self.VALID_TRANSITIONS.get(self.current_state, set())]}"
            )
        self.current_state = target_state
        self.history.append((target_state, datetime.now(timezone.utc)))
        logger.info(f"EOS State Transition -> {target_state.value} (Reason: {reason})")
        return self.current_state


# =====================================================================
# Section 10.2: Opportunity Decision Tree
# =====================================================================

class OpportunityDecisionTree:
    """Implements the hierarchical decision tree for opportunity pursue/discard evaluations."""

    @staticmethod
    def evaluate_opportunity(
        is_structural_anomaly: bool,
        is_reversible: bool,
        has_multi_source_signal: bool = False,
        cheap_test_available: bool = True,
        test_result_exceeds_kill_threshold: Optional[bool] = None,
        expected_value_clearly_positive: Optional[bool] = None,
        has_structural_advantage: bool = False,
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Evaluates whether to commit resources to an opportunity according to Section 10.2 logic.

        Returns:
            Tuple of (pursue_decision: bool, decision_code: str, audit_trail: dict)
        """
        audit: Dict[str, Any] = {
            "is_structural_anomaly": is_structural_anomaly,
            "is_reversible": is_reversible,
            "has_multi_source_signal": has_multi_source_signal,
            "cheap_test_available": cheap_test_available,
            "has_structural_advantage": has_structural_advantage,
        }

        # Q1: Structural anomaly or just noise?
        if not is_structural_anomaly:
            return False, "DISCARD_NOISE", {**audit, "reason": "Signal classified as noise, not structural anomaly."}

        # Q2: Reversible decision (Type II) or Irreversible (Type I)?
        if not is_reversible:
            # Q2a: High-confidence signal from multiple sources?
            if not has_multi_source_signal:
                return False, "DISCARD_UNCONFIRMED_TYPE_I", {
                    **audit,
                    "reason": "Irreversible decision lacks multi-source high-confidence signal."
                }

        # Q3: Cheap test available?
        if cheap_test_available:
            if test_result_exceeds_kill_threshold is None:
                return True, "RUN_CHEAP_TEST", {**audit, "action": "Run cheap test before proceeding."}
            elif not test_result_exceeds_kill_threshold:
                return False, "DISCARD_TEST_FAILED", {
                    **audit,
                    "reason": "Cheap test result failed to exceed kill threshold."
                }
        else:
            if expected_value_clearly_positive is not None and not expected_value_clearly_positive:
                return False, "DISCARD_NEGATIVE_EV", {
                    **audit,
                    "reason": "No cheap test available and Expected Value is not clearly positive."
                }

        # Q5: Do we have or can we build a structural advantage here?
        if not has_structural_advantage:
            return False, "DISCARD_NO_MOAT", {
                **audit,
                "reason": "Lacks structural advantage or defensible moat potential."
            }

        return True, "COMMIT_RESOURCES", {**audit, "reason": "All decision criteria satisfied. Commit resources."}


# =====================================================================
# Section 3: Coupled Business Loops Engine
# =====================================================================

class CoupledBusinessLoopsEngine:
    """Models stock/flow dynamics and loop interactions across all 13 business loops."""

    LOOPS = [
        "Product", "Marketing", "Sales", "Customer Success", "Brand",
        "Pricing", "Referral", "Data", "Financial", "Hiring",
        "Culture", "Innovation", "Competitive Intelligence"
    ]

    def __init__(self) -> None:
        self.stocks: Dict[str, float] = {
            "cash_cents": 1_000_000_00.0,  # $1,000,000
            "talent_score": 0.8,
            "trust_brand_score": 0.7,
            "data_assets_score": 0.5,
        }

    def simulate_coupling_cycle(self, inputs: Dict[str, float]) -> Dict[str, Any]:
        """Runs one coupling iteration over stocks and flows.

        Leverage points: Pricing (ARPU) -> Financial -> Hiring -> Product velocity.
        """
        arpu = inputs.get("arpu_cents", 100_00)  # $100
        cac = inputs.get("cac_cents", 300_00)    # $300
        acquired_users = inputs.get("acquired_users", 100.0)
        retention_rate = inputs.get("retention_rate", 0.90)
        hiring_budget = inputs.get("hiring_budget_cents", 100_000_00)

        # Revenue flow
        gross_revenue = acquired_users * arpu
        total_cac_spend = acquired_users * cac
        net_cash_flow = gross_revenue - total_cac_spend

        # Stock updates
        self.stocks["cash_cents"] += net_cash_flow

        # Hiring loop leverage
        if hiring_budget > 0 and self.stocks["cash_cents"] > hiring_budget:
            talent_gain = min(0.05, hiring_budget / 2_000_000_00)
            self.stocks["talent_score"] = min(1.0, self.stocks["talent_score"] + talent_gain)

        # Data stock accumulation
        self.stocks["data_assets_score"] = min(1.0, self.stocks["data_assets_score"] + (acquired_users * 0.0001))

        # Brand trust stock from retention
        if retention_rate > 0.85:
            self.stocks["trust_brand_score"] = min(1.0, self.stocks["trust_brand_score"] + 0.01)
        else:
            self.stocks["trust_brand_score"] = max(0.0, self.stocks["trust_brand_score"] - 0.02)

        # High leverage metrics
        burn_multiple = total_cac_spend / gross_revenue if gross_revenue > 0 else 99.0
        ltv_to_cac = (arpu / (1.0 - retention_rate)) / cac if (1.0 - retention_rate) > 0 and cac > 0 else 1.0

        return {
            "updated_stocks": dict(self.stocks),
            "gross_revenue_cents": gross_revenue,
            "net_cash_flow_cents": net_cash_flow,
            "burn_multiple": burn_multiple,
            "ltv_to_cac": ltv_to_cac,
            "high_leverage_loops_status": {
                "pricing_financial_leverage": arpu > cac * 0.3,
                "hiring_product_velocity_leverage": self.stocks["talent_score"] > 0.75,
            }
        }


# =====================================================================
# Section 4: Customer Journey Lifecycle Engine
# =====================================================================

class CustomerLifecycleEngine:
    """Tracks customer progression across the 15-stage lifecycle."""

    STAGES = [
        "Awareness", "Interest", "Consideration", "Evaluation", "Purchase",
        "Onboarding", "Activation", "Engagement", "Habit Formation", "Retention",
        "Loyalty", "Advocacy", "Referral", "Expansion", "Repurchase"
    ]

    @classmethod
    def evaluate_cohort_progression(cls, cohort_data: Dict[str, float]) -> Dict[str, Any]:
        """Evaluates customer metrics and flags conversion bottlenecks."""
        activation_rate = cohort_data.get("activation_rate", 0.4)
        retention_rate = cohort_data.get("retention_rate", 0.8)
        nrr = cohort_data.get("net_revenue_retention", 1.1)
        viral_k = cohort_data.get("viral_coefficient_k", 0.2)

        bottlenecks = []
        if activation_rate < 0.5:
            bottlenecks.append({
                "stage": "Activation",
                "mistake": "Defining activation as login, not value delivery.",
                "lever": "Instrument true 'aha' moment via cohort analysis."
            })
        if retention_rate < 0.7:
            bottlenecks.append({
                "stage": "Retention",
                "mistake": "Measuring retention in aggregate rather than cohort flattening point.",
                "lever": "Cohort-level retention curves and flattening point analysis."
            })
        if nrr < 1.0:
            bottlenecks.append({
                "stage": "Expansion",
                "mistake": "Under-selling adjacent value and lack of usage triggers.",
                "lever": "Usage-based expansion triggers and account expansion strategy."
            })

        return {
            "activation_rate": activation_rate,
            "retention_rate": retention_rate,
            "net_revenue_retention": nrr,
            "viral_k_coefficient": viral_k,
            "identified_bottlenecks": bottlenecks,
            "healthy_funnel": len(bottlenecks) == 0
        }


# =====================================================================
# Section 6: Company Growth Stage Classifier
# =====================================================================

class CompanyGrowthStage(str, Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "Product-Market Fit"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    MARKET_LEADERSHIP = "Market Leadership"


class GrowthStageClassifier:
    """Classifies company growth stage and identifies primary binding constraints."""

    STAGE_MAP = [
        (CompanyGrowthStage.MARKET_LEADERSHIP, lambda m: m.get("category_share", 0.0) >= 0.40 and m.get("moat_durability", 0.0) >= 0.8),
        (CompanyGrowthStage.ECOSYSTEM, lambda m: m.get("ecosystem_gmv_cents", 0) > 10_000_000_00 and m.get("network_density", 0.0) > 0.7),
        (CompanyGrowthStage.PLATFORM, lambda m: m.get("third_party_dev_count", 0) > 100),
        (CompanyGrowthStage.SCALE, lambda m: m.get("arr_cents", 0) >= 10_000_000_00 and m.get("rule_of_40", 0.0) >= 0.40),
        (CompanyGrowthStage.GROWTH, lambda m: m.get("arr_cents", 0) >= 2_000_000_00 and m.get("growth_rate_yoy", 0.0) >= 1.0),
        (CompanyGrowthStage.PMF, lambda m: m.get("retention_curve_flattened", False) and m.get("nrr", 0.0) >= 1.0),
        (CompanyGrowthStage.STARTUP, lambda m: m.get("paying_customers", 0) >= 10),
        (CompanyGrowthStage.VALIDATION, lambda m: m.get("paying_customers", 0) > 0 or m.get("loi_count", 0) > 0),
        (CompanyGrowthStage.IDEA, lambda m: True),
    ]

    BINDING_CONSTRAINTS = {
        CompanyGrowthStage.IDEA: "Founder time",
        CompanyGrowthStage.VALIDATION: "Signal quality",
        CompanyGrowthStage.STARTUP: "Cash runway",
        CompanyGrowthStage.PMF: "Team bandwidth",
        CompanyGrowthStage.GROWTH: "Hiring velocity & systems",
        CompanyGrowthStage.SCALE: "Org coordination cost",
        CompanyGrowthStage.PLATFORM: "Trust from ecosystem partners",
        CompanyGrowthStage.ECOSYSTEM: "Governance credibility",
        CompanyGrowthStage.MARKET_LEADERSHIP: "Innovation velocity vs. incumbency drag",
    }

    @classmethod
    def classify_stage(cls, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Determine venture growth stage from metrics and return stage metadata."""
        for stage, evaluator in cls.STAGE_MAP:
            if evaluator(metrics):
                return {
                    "stage": stage.value,
                    "binding_constraint": cls.BINDING_CONSTRAINTS[stage],
                    "core_metric": cls._get_core_metric(stage, metrics),
                }
        return {
            "stage": CompanyGrowthStage.IDEA.value,
            "binding_constraint": cls.BINDING_CONSTRAINTS[CompanyGrowthStage.IDEA],
            "core_metric": "validated_learnings_count",
        }

    @staticmethod
    def _get_core_metric(stage: CompanyGrowthStage, metrics: Dict[str, Any]) -> Any:
        metrics_map = {
            CompanyGrowthStage.IDEA: metrics.get("validated_learnings_count", 0),
            CompanyGrowthStage.VALIDATION: metrics.get("paying_customers", 0),
            CompanyGrowthStage.STARTUP: metrics.get("ltv_to_cac", 0.0),
            CompanyGrowthStage.PMF: metrics.get("retention_flattening_point_percent", 0.0),
            CompanyGrowthStage.GROWTH: metrics.get("growth_rate_yoy", 0.0),
            CompanyGrowthStage.SCALE: metrics.get("rule_of_40", 0.0),
            CompanyGrowthStage.PLATFORM: metrics.get("third_party_dev_count", 0),
            CompanyGrowthStage.ECOSYSTEM: metrics.get("ecosystem_gmv_cents", 0),
            CompanyGrowthStage.MARKET_LEADERSHIP: metrics.get("category_share", 0.0),
        }
        return metrics_map.get(stage, 0)


# =====================================================================
# Section 7: Moat Durability Analyzer
# =====================================================================

class MoatAnalyzer:
    """Quantifies structural competitive advantages across six modern moat types."""

    @staticmethod
    def score_moat_durability(
        network_density: float = 0.0,
        avg_switching_cost_cents: int = 0,
        scale_economies_cost_advantage_percent: float = 0.0,
        brand_trust_score: float = 0.0,
        regulatory_ip_score: float = 0.0,
        counter_positioning_score: float = 0.0,
    ) -> Dict[str, Any]:
        """Calculates composite moat durability score [0.0, 1.0]."""
        s_network = min(1.0, max(0.0, network_density))
        s_switch = min(1.0, max(0.0, avg_switching_cost_cents / 10_000_00))  # Normalized at $10k
        s_scale = min(1.0, max(0.0, scale_economies_cost_advantage_percent))
        s_brand = min(1.0, max(0.0, brand_trust_score))
        s_ip = min(1.0, max(0.0, regulatory_ip_score))
        s_counter = min(1.0, max(0.0, counter_positioning_score))

        composite_score = (
            0.25 * s_network +
            0.20 * s_switch +
            0.15 * s_scale +
            0.15 * s_brand +
            0.10 * s_ip +
            0.15 * s_counter
        )

        primary_moat = "None"
        max_sub = max(
            ("Network Effects", s_network),
            ("Switching Costs", s_switch),
            ("Economies of Scale", s_scale),
            ("Brand Trust", s_brand),
            ("Regulatory / IP", s_ip),
            ("Counter-Positioning", s_counter),
            key=lambda x: x[1]
        )
        if max_sub[1] > 0.3:
            primary_moat = max_sub[0]

        return {
            "composite_moat_durability_score": round(composite_score, 4),
            "primary_moat_type": primary_moat,
            "component_scores": {
                "network_effects": s_network,
                "switching_costs": s_switch,
                "scale_economies": s_scale,
                "brand_trust": s_brand,
                "regulatory_ip": s_ip,
                "counter_positioning": s_counter,
            },
            "is_defensible": composite_score >= 0.50,
        }


# =====================================================================
# Section 8: Failure Mode Diagnostics
# =====================================================================

class FailureModeMonitor:
    """Pattern matches operating metrics against the Section 8 failure matrix."""

    FAILURE_PATTERNS = [
        {
            "name": "Solving the wrong problem",
            "root_cause": "Skipped root-cause analysis; solved a symptom",
            "condition": lambda m: m.get("survey_satisfaction", 0) > 0.8 and m.get("daily_active_usage", 0) < 0.1,
            "correction": "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)",
        },
        {
            "name": "Building before validating",
            "root_cause": "Founder conviction substituted for evidence",
            "condition": lambda m: m.get("build_velocity_features_per_month", 0) > 10 and m.get("paying_customers", 0) == 0,
            "correction": "Enforce a validation gate before build resourcing",
        },
        {
            "name": "Weak positioning",
            "root_cause": "No clear 'instead of X, use us because Y'",
            "condition": lambda m: m.get("sales_cycle_days", 0) > 90 and m.get("feature_comparison_objections_percent", 0) > 0.5,
            "correction": "Rebuild positioning around the real alternative customers compare to",
        },
        {
            "name": "Poor pricing",
            "root_cause": "Cost-plus instead of value-based pricing",
            "condition": lambda m: m.get("conversion_rate", 0) > 0.4 and m.get("gross_margin", 0) < 0.3,
            "correction": "Re-anchor price to quantified customer value",
        },
        {
            "name": "Distribution failure",
            "root_cause": "Great product, no repeatable channel",
            "condition": lambda m: m.get("nps", 0) > 60 and m.get("mom_growth_percent", 0) < 0.02,
            "correction": "Systematically test channels against ICP behavior, not founder preference",
        },
        {
            "name": "Lack of product-market fit",
            "root_cause": "Premature scaling of an unproven loop",
            "condition": lambda m: not m.get("retention_curve_flattened", True) and m.get("marketing_spend_cents", 0) > 100_000_00,
            "correction": "Stop scaling; return to cohort-level retention work",
        },
        {
            "name": "Organizational bottlenecks",
            "root_cause": "Decision rights not delegated as company scales",
            "condition": lambda m: m.get("decision_latency_days", 0) > 7.0 and m.get("team_size", 0) > 15,
            "correction": "Push decision rights down with clear frameworks (not ad hoc delegation)",
        },
        {
            "name": "Founder bias",
            "root_cause": "Overconfidence, confirmation bias, sunk cost",
            "condition": lambda m: m.get("disconfirming_experiments_ignored", 0) >= 3,
            "correction": "Pre-committed kill criteria set before launch",
        },
        {
            "name": "Scaling prematurely",
            "root_cause": "Confusing early demand spike with durable PMF",
            "condition": lambda m: m.get("cac_growth_rate", 0) > m.get("ltv_growth_rate", 0),
            "correction": "Re-test unit economics at each order-of-magnitude of spend",
        },
        {
            "name": "Capital misallocation",
            "root_cause": "No opportunity-cost discipline in budgeting",
            "condition": lambda m: m.get("underperforming_bets_count", 0) >= 3 and m.get("burn_multiple", 0) > 3.0,
            "correction": "Rank all initiatives on a common expected-return basis quarterly",
        },
    ]

    @classmethod
    def diagnose_failure_modes(cls, metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        """Scans venture metrics and returns detected failure mode alerts."""
        alerts = []
        for pat in cls.FAILURE_PATTERNS:
            try:
                if pat["condition"](metrics):
                    alerts.append({
                        "failure_mode": pat["name"],
                        "root_cause": pat["root_cause"],
                        "correction_mechanism": pat["correction"],
                    })
            except Exception as err:
                logger.debug(f"Error evaluating failure pattern '{pat['name']}': {err}")
        return alerts


# =====================================================================
# Master Orchestrator: FirstPrinciplesEOSEngine
# =====================================================================

class FirstPrinciplesEOSEngine:
    """Master Continuous Operating Orchestrator embodying the entire 11-section EOS specification."""

    def __init__(self) -> None:
        self.state_machine = EOSStateMachine()
        self.coupled_loops = CoupledBusinessLoopsEngine()
        self.memory_store: List[Dict[str, Any]] = []

    def run_master_sensing_cycle(
        self,
        venture_state: Dict[str, Any],
        opportunity_signal: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Executes one continuous sensing, decision, simulation, diagnostic, and state transition cycle."""

        # 1. Decision Tree Evaluation on Signal (if provided)
        decision_result = None
        if opportunity_signal:
            pursue, code, audit = OpportunityDecisionTree.evaluate_opportunity(
                is_structural_anomaly=opportunity_signal.get("is_structural_anomaly", False),
                is_reversible=opportunity_signal.get("is_reversible", True),
                has_multi_source_signal=opportunity_signal.get("has_multi_source_signal", False),
                cheap_test_available=opportunity_signal.get("cheap_test_available", True),
                test_result_exceeds_kill_threshold=opportunity_signal.get("test_result_exceeds_kill_threshold"),
                expected_value_clearly_positive=opportunity_signal.get("expected_value_clearly_positive"),
                has_structural_advantage=opportunity_signal.get("has_structural_advantage", False),
            )
            decision_result = {"pursue": pursue, "code": code, "audit": audit}

            # State transition based on decision tree
            if self.state_machine.current_state == EOSState.SENSING and opportunity_signal.get("is_structural_anomaly"):
                self.state_machine.transition_to(EOSState.HYPOTHESIS, "Structural anomaly sensed.")
                if pursue and code == "RUN_CHEAP_TEST":
                    self.state_machine.transition_to(EOSState.CHEAP_TEST, "Hypothesis formulated; executing cheap test.")

        # 2. Coupled Business Loops Simulation
        loops_result = self.coupled_loops.simulate_coupling_cycle(venture_state)

        # 3. Customer Journey Lifecycle Diagnostics
        customer_result = CustomerLifecycleEngine.evaluate_cohort_progression(venture_state)

        # 4. Growth Stage Classification
        growth_stage = GrowthStageClassifier.classify_stage(venture_state)

        # 5. Moat Durability Score
        moat_result = MoatAnalyzer.score_moat_durability(
            network_density=venture_state.get("network_density", 0.0),
            avg_switching_cost_cents=venture_state.get("avg_switching_cost_cents", 0),
            scale_economies_cost_advantage_percent=venture_state.get("scale_economies_cost_advantage_percent", 0.0),
            brand_trust_score=venture_state.get("brand_trust_score", 0.0),
            regulatory_ip_score=venture_state.get("regulatory_ip_score", 0.0),
            counter_positioning_score=venture_state.get("counter_positioning_score", 0.0),
        )

        # 6. Failure Mode Diagnostics
        failure_alerts = FailureModeMonitor.diagnose_failure_modes({**venture_state, **loops_result})

        # Record cycle in memory
        cycle_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "state": self.state_machine.current_state.value,
            "decision": decision_result,
            "growth_stage": growth_stage["stage"],
            "moat_durability": moat_result["composite_moat_durability_score"],
            "failure_alerts_count": len(failure_alerts),
        }
        self.memory_store.append(cycle_record)

        return {
            "current_state": self.state_machine.current_state.value,
            "decision_result": decision_result,
            "business_loops": loops_result,
            "customer_lifecycle": customer_result,
            "growth_stage": growth_stage,
            "moat_analysis": moat_result,
            "failure_alerts": failure_alerts,
            "memory_cycle_count": len(self.memory_store),
        }
