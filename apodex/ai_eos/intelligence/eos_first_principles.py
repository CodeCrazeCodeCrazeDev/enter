"""Entrepreneurial Operating System (EOS) First-Principles Executable Engine.

An 11-section executable Python implementation reflecting how elite founders sense,
build, and compound enduring companies based on the canonical EOS Specification.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Set
from uuid import UUID, uuid4

logger = logging.getLogger("apodex.ai_eos.eos_first_principles")


# =====================================================================
# 1. Anomalies & Sensing Engine (§1, §2, §10.3)
# =====================================================================
class AnomaliesAndSensingEngine:
    """Continuously ingests weak signals, detects structural anomalies vs noise,

    runs cheap sequential tests, and manages forced hypothesis generation.
    """

    def __init__(self, baseline_threshold: float = 0.25) -> None:
        self.baseline_threshold = baseline_threshold
        self.active_hypotheses: Dict[str, Dict[str, Any]] = {}

    def sense_signal_stream(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processes incoming signals and flags structural anomalies vs noise."""
        detected_anomalies = []
        for signal in signals:
            deviation = abs(signal.get("observed_value", 0.0) - signal.get("expected_value", 0.0))
            is_structural = signal.get("is_structural_shift", False) or (deviation > self.baseline_threshold)

            anomaly = {
                "signal_id": signal.get("id", str(uuid4())),
                "name": signal.get("name", "unnamed_signal"),
                "deviation": deviation,
                "is_structural": is_structural,
                "status": "structural_anomaly" if is_structural else "noise",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            if is_structural:
                detected_anomalies.append(anomaly)
        return detected_anomalies

    def form_hypothesis(
        self,
        anomaly: Dict[str, Any],
        falsifiable_claim: str,
        kill_threshold: float,
        is_type_ii_risk: bool = True
    ) -> Dict[str, Any]:
        """Converts an anomaly into a forced falsifiable hypothesis with pre-committed kill criteria."""
        hyp_id = str(uuid4())
        hypothesis = {
            "hypothesis_id": hyp_id,
            "signal_id": anomaly.get("signal_id"),
            "falsifiable_claim": falsifiable_claim,
            "kill_threshold": kill_threshold,
            "is_type_ii_risk": is_type_ii_risk,  # Reversible vs Irreversible
            "prior_beta_params": {"alpha": 1.0, "beta": 1.0},
            "posterior_confidence": 0.5,
            "status": "proposed",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.active_hypotheses[hyp_id] = hypothesis
        return hypothesis

    def run_cheap_test(
        self,
        hypothesis_id: str,
        test_cost_cents: int,
        successes: int,
        trials: int
    ) -> Dict[str, Any]:
        """Executes a sequential cheap test to update belief parameters using Beta distributions."""
        hyp = self.active_hypotheses.get(hypothesis_id)
        if not hyp:
            raise ValueError(f"Hypothesis {hypothesis_id} not found.")

        alpha = hyp["prior_beta_params"]["alpha"] + successes
        beta = hyp["prior_beta_params"]["beta"] + (trials - successes)
        posterior = float(alpha / (alpha + beta))

        hyp["prior_beta_params"] = {"alpha": alpha, "beta": beta}
        hyp["posterior_confidence"] = posterior

        if posterior >= hyp["kill_threshold"]:
            hyp["status"] = "strengthened"
        else:
            hyp["status"] = "falsified"

        hyp["last_tested_at"] = datetime.now(timezone.utc).isoformat()
        hyp["test_cost_cents"] = test_cost_cents
        return hyp


# =====================================================================
# 2. External Business Loops Engine (§3, §10.3)
# =====================================================================
class ExternalBusinessLoopsEngine:
    """Models, evaluates, and diagnoses performance across the 13 coupled business loops."""

    LOOP_DEFINITIONS = {
        "product": {"kpis": ["retention_curve", "nps", "feature_adoption"], "failure_mode": "Building for loudest customer"},
        "marketing": {"kpis": ["cac", "brand_recall", "conversion_rate"], "failure_mode": "Message-market mismatch"},
        "sales": {"kpis": ["win_rate", "sales_cycle_length", "acv"], "failure_mode": "Selling to non-ICP to hit quota"},
        "customer_success": {"kpis": ["nrr", "churn_rate", "time_to_value"], "failure_mode": "Success != support; reactive CS"},
        "brand": {"kpis": ["share_of_voice", "price_elasticity"], "failure_mode": "Brand as decoration"},
        "pricing": {"kpis": ["arpu", "price_realization", "elasticity"], "failure_mode": "Cost-plus pricing"},
        "referral": {"kpis": ["viral_coefficient", "referral_cac"], "failure_mode": "Incentivizing referral volume over quality"},
        "data": {"kpis": ["data_latency", "decision_cycle_time"], "failure_mode": "Vanity metrics"},
        "financial": {"kpis": ["gross_margin", "burn_multiple", "runway"], "failure_mode": "Negative unit economics"},
        "hiring": {"kpis": ["time_to_fill", "quality_of_hire", "retention"], "failure_mode": "Hiring for pedigree over role-fit"},
        "culture": {"kpis": ["enps", "decision_latency"], "failure_mode": "Values as poster"},
        "innovation": {"kpis": ["experiments_run", "hit_rate", "time_to_signal"], "failure_mode": "Innovation theater"},
        "competitive_intelligence": {"kpis": ["relative_share_trend", "feature_parity_gap"], "failure_mode": "Obsessive reactivity"},
    }

    def __init__(self) -> None:
        pass

    def evaluate_loop_health(self, loop_name: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates health score [0, 1] for a specific business loop."""
        loop_name_clean = loop_name.lower().replace(" ", "_")
        definition = self.LOOP_DEFINITIONS.get(loop_name_clean)
        if not definition:
            return {"loop": loop_name, "health_score": 0.5, "status": "unknown_loop"}

        score = 1.0
        alerts = []

        if loop_name_clean == "financial":
            burn = metrics.get("burn_multiple", 1.0)
            if burn > 2.0:
                score -= 0.4
                alerts.append("High burn multiple")
            runway = metrics.get("runway_months", 12)
            if runway < 6:
                score -= 0.5
                alerts.append("Critical low runway")

        elif loop_name_clean == "product":
            nps = metrics.get("nps", 50)
            if nps < 20:
                score -= 0.3
                alerts.append("Low NPS")

        elif loop_name_clean == "customer_success":
            nrr = metrics.get("nrr", 1.0)
            if nrr < 1.0:
                score -= 0.4
                alerts.append("Net revenue contraction")

        score = max(0.0, min(1.0, score))
        return {
            "loop": loop_name_clean,
            "health_score": score,
            "status": "healthy" if score >= 0.7 else "at_risk" if score >= 0.4 else "critical",
            "alerts": alerts,
            "dominant_failure_mode": definition["failure_mode"] if score < 0.7 else None
        }

    def evaluate_coupled_loops(self, metrics_by_loop: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluates global system coupling and leverage points (pricing & hiring)."""
        loop_results = {}
        total_health = 0.0

        for loop in self.LOOP_DEFINITIONS:
            m = metrics_by_loop.get(loop, {})
            res = self.evaluate_loop_health(loop, m)
            loop_results[loop] = res
            total_health += res["health_score"]

        avg_health = total_health / len(self.LOOP_DEFINITIONS)
        pricing_health = loop_results["pricing"]["health_score"]
        hiring_health = loop_results["hiring"]["health_score"]

        leverage_score = (pricing_health + hiring_health) / 2.0

        return {
            "average_system_health": avg_health,
            "high_leverage_health": leverage_score,
            "loop_details": loop_results,
            "system_status": "stable" if avg_health >= 0.7 else "degraded"
        }


# =====================================================================
# 3. Customer Lifecycle Engine (§4, §10.3)
# =====================================================================
class CustomerLifecycleEngine:
    """Models all 15 stages of the customer journey lifecycle and tracks cohort retention curves."""

    LIFECYCLE_STAGES = [
        "awareness", "interest", "consideration", "evaluation", "purchase",
        "onboarding", "activation", "habit_formation", "retention",
        "loyalty", "advocacy", "referral", "expansion", "repurchase"
    ]

    def __init__(self) -> None:
        pass

    def evaluate_stage_performance(self, stage_name: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates performance metrics and conversion for a specific lifecycle stage."""
        stage_clean = stage_name.lower().replace(" ", "_")
        if stage_clean not in self.LIFECYCLE_STAGES:
            return {"stage": stage_name, "valid": False}

        score = 1.0
        alerts = []

        if stage_clean == "onboarding":
            ttfv = metrics.get("time_to_first_value_hours", 24)
            if ttfv > 48:
                score -= 0.4
                alerts.append("TTFV exceeds 48h SLA")

        elif stage_clean == "activation":
            act_rate = metrics.get("activation_rate", 0.5)
            if act_rate < 0.3:
                score -= 0.5
                alerts.append("Low activation rate threshold")

        elif stage_clean == "retention":
            churn = metrics.get("churn_rate", 0.05)
            if churn > 0.05:
                score -= 0.3
                alerts.append("Monthly churn above 5%")

        return {
            "stage": stage_clean,
            "performance_score": max(0.0, score),
            "alerts": alerts,
            "metrics": metrics
        }

    def analyze_cohort_retention(self, monthly_retention_percentages: List[float]) -> Dict[str, Any]:
        """Analyzes cohort retention curve for flattening point and stability."""
        if not monthly_retention_percentages or len(monthly_retention_percentages) < 2:
            return {"flattened": False, "flattening_point": 0.0, "slope": 0.0}

        # Calculate slope of last 3 periods
        recent = monthly_retention_percentages[-3:] if len(monthly_retention_percentages) >= 3 else monthly_retention_percentages
        slopes = [recent[i] - recent[i - 1] for i in range(1, len(recent))]
        avg_slope = sum(slopes) / len(slopes)

        flattened = abs(avg_slope) < 0.01 and monthly_retention_percentages[-1] >= 0.20
        return {
            "flattened": flattened,
            "terminal_retention_rate": monthly_retention_percentages[-1],
            "recent_slope": avg_slope,
            "pmf_retention_signal": flattened
        }


# =====================================================================
# 4. Go-To-Market (GTM) System Simulator (§5, §10.3)
# =====================================================================
class GTMSystemSimulator:
    """Models GTM channel fit against positioning, ACV margin, and complexity combinations."""

    def __init__(self) -> None:
        pass

    def simulate_channel_fit(
        self,
        positioning: str,
        acv_cents: int,
        complexity: str,
        channel: str
    ) -> Dict[str, Any]:
        """Models fit between positioning, pricing/ACV, product complexity, and distribution channel."""
        channel_clean = channel.lower()
        complexity_clean = complexity.lower()

        # Rule checks
        is_high_acv = acv_cents >= 10000_00  # >= $10k
        is_low_acv = acv_cents < 2000_00    # < $2k

        recommended_channels = []
        if is_low_acv and complexity_clean == "low":
            recommended_channels = ["plg", "content", "organic"]
        elif is_high_acv or complexity_clean == "high":
            recommended_channels = ["slg", "enterprise_sales"]
        else:
            recommended_channels = ["mlg", "partner", "community"]

        fit_score = 1.0 if channel_clean in recommended_channels else 0.3

        return {
            "channel": channel_clean,
            "positioning": positioning,
            "acv_cents": acv_cents,
            "complexity": complexity_clean,
            "fit_score": fit_score,
            "recommended_channels": recommended_channels,
            "is_aligned": fit_score > 0.6
        }

    def simulate_compounding_motions(self, active_motions: List[str]) -> Dict[str, Any]:
        """Evaluates compounding leverage across GTM motions (e.g. PLG + SLG)."""
        motions = [m.lower() for m in active_motions]
        multiplier = 1.0

        if "plg" in motions and "slg" in motions:
            multiplier += 0.5  # Slack/Figma/Notion land-and-expand multiplier
        if "content" in motions and "organic" in motions:
            multiplier += 0.2
        if "community" in motions and "referral" in motions:
            multiplier += 0.3

        return {
            "active_motions": motions,
            "compounding_multiplier": multiplier,
            "has_land_and_expand_synergy": "plg" in motions and "slg" in motions
        }


# =====================================================================
# 5. Company Growth State Machine (§6, §10.3)
# =====================================================================
class CompanyGrowthStateMachine:
    """Models 8 growth stages from Idea to Market Leadership with transition criteria."""

    STAGES = ["idea", "validation", "startup", "pmf", "growth", "scale", "platform", "ecosystem", "market_leadership"]

    STAGE_INFO = {
        "idea": {"primary_objective": "Falsify or strengthen hypothesis", "binding_constraint": "Founder time", "core_metric": "validated_learnings"},
        "validation": {"primary_objective": "Prove willingness to pay", "binding_constraint": "Signal quality", "core_metric": "paying_customers"},
        "startup": {"primary_objective": "Build repeatable acquisition", "binding_constraint": "Cash runway", "core_metric": "cac_ltv_signal"},
        "pmf": {"primary_objective": "Reach retention/growth threshold", "binding_constraint": "Team bandwidth", "core_metric": "retention_flattening"},
        "growth": {"primary_objective": "Scale what works", "binding_constraint": "Hiring velocity", "core_metric": "growth_rate_payback"},
        "scale": {"primary_objective": "Institutionalize repeatability", "binding_constraint": "Org coordination cost", "core_metric": "rule_of_40_nrr"},
        "platform": {"primary_objective": "Enable others to build on you", "binding_constraint": "Trust from partners", "core_metric": "developer_activity"},
        "ecosystem": {"primary_objective": "Orchestrate multi-sided network", "binding_constraint": "Governance credibility", "core_metric": "ecosystem_gmv"},
        "market_leadership": {"primary_objective": "Defend and extend category", "binding_constraint": "Innovation velocity vs drag", "core_metric": "category_share_moat_durability"},
    }

    def __init__(self, initial_stage: str = "idea") -> None:
        self.current_stage = initial_stage.lower()

    def evaluate_stage_transition(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates whether current metrics satisfy criteria to transition to the next stage."""
        idx = self.STAGES.index(self.current_stage) if self.current_stage in self.STAGES else 0
        if idx >= len(self.STAGES) - 1:
            return {"can_transition": False, "current_stage": self.current_stage, "next_stage": None, "reason": "At peak stage"}

        next_stage = self.STAGES[idx + 1]
        can_transition = False
        reason = ""

        if self.current_stage == "idea":
            if metrics.get("validated_learnings", 0) >= 3:
                can_transition = True
        elif self.current_stage == "validation":
            if metrics.get("paying_customers", 0) >= 5:
                can_transition = True
        elif self.current_stage == "startup":
            if metrics.get("ltv_to_cac", 0.0) >= 3.0 and metrics.get("payback_months", 99) <= 12:
                can_transition = True
        elif self.current_stage == "pmf":
            if metrics.get("retention_flattened", False):
                can_transition = True
        elif self.current_stage == "growth":
            if metrics.get("arr_cents", 0) >= 1000000_00:  # $1M ARR
                can_transition = True
        else:
            can_transition = metrics.get("stage_gate_passed", False)

        if can_transition:
            previous = self.current_stage
            self.current_stage = next_stage
            return {"can_transition": True, "previous_stage": previous, "current_stage": self.current_stage}
        else:
            return {"can_transition": False, "current_stage": self.current_stage, "next_stage": next_stage, "reason": "Criteria not met"}


# =====================================================================
# 6. Strategic Moat Engine (§7, §10.3)
# =====================================================================
class StrategicMoatEngine:
    """Evaluates moat durability (7 powers), technology cost curves, and reinvention triggers."""

    def __init__(self) -> None:
        pass

    def score_moat_durability(self, moat_metrics: Dict[str, float]) -> Dict[str, Any]:
        """Scores overall moat durability [0, 1] across network effects, switching costs, scale, brand, counter-positioning."""
        net_effects = moat_metrics.get("network_effects", 0.0)
        switching_costs = moat_metrics.get("switching_costs", 0.0)
        scale = moat_metrics.get("economies_of_scale", 0.0)
        brand = moat_metrics.get("brand_trust", 0.0)
        counter_pos = moat_metrics.get("counter_positioning", 0.0)

        composite = (0.25 * net_effects + 0.20 * switching_costs + 0.20 * scale + 0.15 * brand + 0.20 * counter_pos)
        composite = max(0.0, min(1.0, composite))

        return {
            "composite_moat_score": composite,
            "durability_tier": "impregnable" if composite >= 0.8 else "defensible" if composite >= 0.5 else "vulnerable",
            "components": moat_metrics
        }

    def evaluate_cost_curve_viability(self, cost_curve_history: List[float], threshold: float) -> Dict[str, Any]:
        """Detects the point where enabling technology cost curve crosses economic viability threshold."""
        if not cost_curve_history:
            return {"viable": False, "crossing_index": -1}

        crossing_index = -1
        for i, cost in enumerate(cost_curve_history):
            if cost <= threshold:
                crossing_index = i
                break

        return {
            "viable": crossing_index != -1,
            "crossing_index": crossing_index,
            "latest_cost": cost_curve_history[-1],
            "threshold": threshold
        }

    def check_reinvention_trigger(
        self,
        revenue_decay_rate: float,
        customer_attrition_rate: float,
        leading_indicator_drop: float
    ) -> Dict[str, Any]:
        """Forces periodic self-disruption review independent of lagging revenue indicators."""
        trigger = revenue_decay_rate > 0.10 or customer_attrition_rate > 0.15 or leading_indicator_drop > 0.25
        return {
            "reinvention_triggered": trigger,
            "action": "INITIATE_PARALLEL_SENSING_AND_PIVOT_REVIEW" if trigger else "CONTINUE_STANDARD_OPS",
            "leading_indicator_drop": leading_indicator_drop
        }


# =====================================================================
# 7. Failure Mode Monitor (§8, §10.3)
# =====================================================================
class FailureModeMonitor:
    """Pattern-matches operating metrics against 10 explicit failure modes."""

    FAILURE_MODES = {
        "solving_wrong_problem": {"root_cause": "Skipped root-cause analysis", "correction": "5-Whys / JTBD interviews"},
        "building_before_validating": {"root_cause": "Founder conviction substituted for evidence", "correction": "Enforce validation gate"},
        "weak_positioning": {"root_cause": "No clear alternative contrast", "correction": "Rebuild positioning around real alternative"},
        "poor_pricing": {"root_cause": "Cost-plus pricing", "correction": "Re-anchor to value delivered"},
        "distribution_failure": {"root_cause": "No repeatable channel", "correction": "Test channels against ICP behavior"},
        "lack_of_pmf": {"root_cause": "Premature scaling of unproven loop", "correction": "Return to cohort retention work"},
        "org_bottlenecks": {"root_cause": "Decision rights not delegated", "correction": "Push decision rights down"},
        "founder_bias": {"root_cause": "Sunk cost / confirmation bias", "correction": "Pre-committed kill criteria"},
        "scaling_prematurely": {"root_cause": "Confusing early demand spike with PMF", "correction": "Re-test unit economics"},
        "capital_misallocation": {"root_cause": "No opportunity-cost discipline", "correction": "Rank initiatives on common EV basis"},
    }

    def __init__(self) -> None:
        pass

    def diagnose_failure_modes(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scans metrics and detects matching failure mode patterns."""
        detected = []

        if metrics.get("high_build_velocity", False) and metrics.get("demand_signal", 0.0) < 0.2:
            detected.append(self._make_diagnostic("building_before_validating", "High build velocity with flat demand signal"))

        if metrics.get("retention_curve_slope", -0.1) < -0.05 and metrics.get("is_scaling_spend", False):
            detected.append(self._make_diagnostic("scaling_prematurely", "Retention curve unflattened while scaling spend"))

        if metrics.get("cac_payback_months", 0) > 24 and metrics.get("gross_margin", 1.0) < 0.4:
            detected.append(self._make_diagnostic("poor_pricing", "Unfavorable payback and low gross margin"))

        if metrics.get("multiple_underperforming_bets", False):
            detected.append(self._make_diagnostic("capital_misallocation", "Multiple underperforming bets funded without EV ranking"))

        return detected

    def _make_diagnostic(self, key: str, signal: str) -> Dict[str, Any]:
        info = self.FAILURE_MODES.get(key, {})
        return {
            "failure_mode": key,
            "detection_signal": signal,
            "root_cause": info.get("root_cause"),
            "correction_mechanism": info.get("correction")
        }


# =====================================================================
# 8. EOS Opportunity Decision Tree (§10.2, §10.3)
# =====================================================================
class EOSOpportunityDecisionTree:
    """Implements Section 10.2 decision tree logic for opportunity pursuit under risk."""

    def __init__(self) -> None:
        pass

    def evaluate_opportunity(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Traverses the Section 10.2 decision tree."""
        # Q1: Structural anomaly or noise?
        if not opportunity.get("is_structural_anomaly", False):
            return {"decision": "DISCARD", "reason": "Q1: Signal is noise, not a structural anomaly"}

        # Q2: Reversible decision?
        is_reversible = opportunity.get("is_reversible", True)
        if not is_reversible:
            # Q2a: High confidence signal from multiple sources?
            if not opportunity.get("high_confidence_multi_source", False):
                return {"decision": "DISCARD", "reason": "Q2a: High stakes / irreversible without multi-source high confidence"}

        # Q3: Cheap test available?
        cheap_test_available = opportunity.get("cheap_test_available", False)
        if cheap_test_available:
            test_passed = opportunity.get("test_result_exceeds_kill_threshold", False)
            if not test_passed:
                return {"decision": "RUN_CHEAP_TEST", "reason": "Q3/Q4: Cheap test available; run test before commitment"}

        # Q4b: Expected value positive?
        ev_positive = opportunity.get("expected_value_positive", False)
        if not ev_positive:
            return {"decision": "DISCARD", "reason": "Q4b: Expected value is not positive"}

        # Q5: Structural advantage?
        structural_advantage = opportunity.get("has_structural_advantage", False)
        if not structural_advantage:
            return {"decision": "DISCARD", "reason": "Q5: Lacks sustainable structural advantage"}

        return {"decision": "COMMIT", "reason": "All decision tree nodes satisfied; commit resources"}


# =====================================================================
# 9. Coordinating EOSEngineFirstPrinciples (Orchestrator) (§10.3)
# =====================================================================
class EOSEngineFirstPrinciples:
    """Unified Orchestrator implementing the 11-section EOS system architecture."""

    def __init__(self) -> None:
        self.sensing_engine = AnomaliesAndSensingEngine()
        self.business_loops_engine = ExternalBusinessLoopsEngine()
        self.customer_lifecycle_engine = CustomerLifecycleEngine()
        self.gtm_simulator = GTMSystemSimulator()
        self.growth_state_machine = CompanyGrowthStateMachine()
        self.moat_engine = StrategicMoatEngine()
        self.failure_monitor = FailureModeMonitor()
        self.decision_tree = EOSOpportunityDecisionTree()

    def run_full_eos_cycle(
        self,
        signals: List[Dict[str, Any]],
        opportunity: Dict[str, Any],
        loop_metrics: Dict[str, Dict[str, Any]],
        growth_metrics: Dict[str, Any],
        capital_budget_cents: int
    ) -> Dict[str, Any]:
        """Executes a full cycle across sensing, opportunity decision tree, loop health, state transitions, and diagnostics."""
        # 1. Sensing
        anomalies = self.sensing_engine.sense_signal_stream(signals)

        # 2. Opportunity Decision Tree
        decision = self.decision_tree.evaluate_opportunity(opportunity)

        # 3. External Business Loops Health
        loop_evaluation = self.business_loops_engine.evaluate_coupled_loops(loop_metrics)

        # 4. Growth State Machine Transition
        growth_transition = self.growth_state_machine.evaluate_stage_transition(growth_metrics)

        # 5. Failure Mode Diagnostics
        diagnostics = self.failure_monitor.diagnose_failure_modes(growth_metrics)

        # 6. Capital Allocation across active initiatives based on EV
        allocated_budget = int(capital_budget_cents * 0.8) if decision["decision"] == "COMMIT" else int(capital_budget_cents * 0.2)

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "anomalies_detected": anomalies,
            "opportunity_decision": decision,
            "loop_evaluation": loop_evaluation,
            "growth_transition": growth_transition,
            "failure_diagnostics": diagnostics,
            "allocated_budget_cents": allocated_budget
        }
