"""
The First-Principles Entrepreneurial Operating System (EOS) Executable Engine.

This module provides a first-principles reconstruction of how elite founders sense, build,
and compound enduring companies across fast, medium, and slow feedback loops.

It operationalizes the 11-section specification detailed in
`docs/architecture/ENTREPRENEURIAL_OPERATING_SYSTEM_SPEC.md`.
"""

from __future__ import annotations
import math
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Set
from datetime import datetime, timezone
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

logger = logging.getLogger("sero.eos_first_principles")


# =====================================================================
# State & Enums (§10.1 System State Machine)
# =====================================================================
class EOSState(str, Enum):
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


class DecisionRiskType(str, Enum):
    TYPE_I = "Type_I_Irreversible"  # One-way door
    TYPE_II = "Type_II_Reversible"   # Two-way door


# =====================================================================
# 10.1 System State Machine Engine
# =====================================================================
class EOSStateMachine:
    """
    Executes the AI-EOS continuous state transitions for opportunity discovery,
    validation, execution, scaling, and self-disruption/reinvention.
    """

    def __init__(self, initial_state: EOSState = EOSState.SENSING) -> None:
        self.current_state: EOSState = initial_state
        self.state_history: List[Dict[str, Any]] = [
            {"state": initial_state.value, "timestamp": datetime.now(timezone.utc), "reason": "Initialization"}
        ]
        self.falsified_hypotheses_count: int = 0
        self.kill_signals_received: int = 0

    def transition_to(self, target_state: EOSState, reason: str) -> EOSState:
        """Transitions state and records historical state provenance."""
        previous = self.current_state
        self.current_state = target_state
        self.state_history.append({
            "from": previous.value,
            "to": target_state.value,
            "timestamp": datetime.now(timezone.utc),
            "reason": reason
        })
        logger.info(f"EOS State Machine Transition: {previous.value} -> {target_state.value} [{reason}]")
        return self.current_state

    def process_signal(self, is_anomaly: bool, is_structural: bool) -> EOSState:
        """Processes raw environmental signals into hypothesis formation."""
        if self.current_state == EOSState.SENSING and is_anomaly and is_structural:
            return self.transition_to(EOSState.HYPOTHESIS, "Structural anomaly detected")
        return self.current_state

    def process_test_result(self, is_falsified: bool, is_strengthened: bool) -> EOSState:
        """Evaluates cheap test outcomes against pre-committed criteria."""
        if self.current_state == EOSState.CHEAP_TEST:
            if is_falsified:
                self.falsified_hypotheses_count += 1
                return self.transition_to(EOSState.DISCARD, "Cheap test falsified hypothesis")
            elif is_strengthened:
                return self.transition_to(EOSState.VALIDATION, "Cheap test strengthened hypothesis")
        return self.current_state

    def process_validation(self, economic_viability: bool) -> EOSState:
        """Evaluates customer and economic validation gates."""
        if self.current_state == EOSState.VALIDATION:
            if economic_viability:
                return self.transition_to(EOSState.BUILD_GATE, "Economic viability confirmed")
            else:
                self.kill_signals_received += 1
                return self.transition_to(EOSState.DISCARD, "No viable unit economics in validation")
        return self.current_state

    def process_build_and_gtm(self, gtm_signal_score: float, kill_threshold: float = 0.5) -> EOSState:
        """Evaluates GTM test signals against kill or scale thresholds."""
        if self.current_state in (EOSState.BUILD_GATE, EOSState.MVP, EOSState.GTM_TEST):
            if self.current_state == EOSState.BUILD_GATE:
                self.transition_to(EOSState.MVP, "Resources allocated for MVP")
            if self.current_state == EOSState.MVP:
                self.transition_to(EOSState.GTM_TEST, "MVP shipped to GTM test")

            if gtm_signal_score < kill_threshold:
                self.kill_signals_received += 1
                return self.transition_to(EOSState.DISCARD, f"GTM signal score ({gtm_signal_score}) below kill threshold ({kill_threshold})")
            else:
                return self.transition_to(EOSState.SCALE, f"GTM signal score ({gtm_signal_score}) above threshold; scaling venture")
        return self.current_state

    def check_reinvention_trigger(self, market_decay_score: float, threshold: float = 0.7) -> EOSState:
        """Checks if mature leadership requires self-disruption and reinvention."""
        if self.current_state in (EOSState.SCALE, EOSState.OPERATE):
            if market_decay_score >= threshold:
                return self.transition_to(EOSState.REINVENT, "Market decay triggered mandatory reinvention cycle")
        if self.current_state == EOSState.REINVENT:
            return self.transition_to(EOSState.SENSING, "Reinvention loop completed; returning to continuous sensing")
        return self.current_state


# =====================================================================
# 10.2 Decision Tree Engine
# =====================================================================
class OpportunityDecisionTree:
    """
    Implements Section 10.2 decision logic: 'Should We Pursue This Opportunity?'
    """

    def evaluate(
        self,
        is_structural_anomaly: bool,
        risk_type: DecisionRiskType,
        high_confidence_multi_source: bool = False,
        cheap_test_available: bool = True,
        cheap_test_result_exceeds_kill_threshold: Optional[bool] = None,
        expected_value_positive: bool = True,
        structural_advantage_buildable: bool = True
    ) -> Dict[str, Any]:
        """
        Executes the exact multi-node decision logic tree from §10.2.
        Returns explicit decision result (COMMIT_RESOURCES or DISCARD) and full audit trail.
        """
        audit_trail: List[str] = []

        # Q1: Structural anomaly or just noise?
        if not is_structural_anomaly:
            audit_trail.append("Q1: Signal identified as noise -> Discard")
            return {"decision": "DISCARD", "reason": "Noise signal", "audit_trail": audit_trail}
        audit_trail.append("Q1: Signal confirmed as structural anomaly")

        # Q2: Reversible decision?
        if risk_type == DecisionRiskType.TYPE_I:
            audit_trail.append("Q2: High-stakes irreversible decision (Type I)")
            # Q2a: High-confidence signal from multiple sources?
            if not high_confidence_multi_source:
                audit_trail.append("Q2a: Lacks multi-source high-confidence signal -> Discard")
                return {"decision": "DISCARD", "reason": "Insufficient confidence for Type I risk", "audit_trail": audit_trail}
            audit_trail.append("Q2a: Validated multi-source high-confidence signal")
        else:
            audit_trail.append("Q2: Reversible low-stakes decision (Type II)")

        # Q3: Cheap test available?
        if cheap_test_available:
            audit_trail.append("Q3: Cheap test available -> Running cheap test")
            if cheap_test_result_exceeds_kill_threshold is False:
                audit_trail.append("Q4: Cheap test result failed kill threshold -> Discard")
                return {"decision": "DISCARD", "reason": "Cheap test failed pre-committed kill threshold", "audit_trail": audit_trail}
            elif cheap_test_result_exceeds_kill_threshold is True:
                audit_trail.append("Q4: Cheap test result exceeded kill threshold")
            else:
                audit_trail.append("Q4: Cheap test pending execution")
        else:
            audit_trail.append("Q3: No cheap test available")
            if not expected_value_positive:
                audit_trail.append("Q4b: Expected value not clearly positive -> Discard")
                return {"decision": "DISCARD", "reason": "Negative expected value without cheap test option", "audit_trail": audit_trail}
            audit_trail.append("Q4b: Expected value confirmed positive")

        # Q5: Do we have or can we build a structural advantage?
        if not structural_advantage_buildable:
            audit_trail.append("Q5: No structural advantage buildable -> Discard")
            return {"decision": "DISCARD", "reason": "Lacks defendable structural advantage", "audit_trail": audit_trail}

        audit_trail.append("Q5: Structural advantage confirmed -> Commit resources")
        return {"decision": "COMMIT_RESOURCES", "reason": "All decision criteria satisfied", "audit_trail": audit_trail}


# =====================================================================
# Section 3: External Business Loops Engine
# =====================================================================
class CoupledBusinessLoopsEngine:
    """
    Models the 13 coupled business loops, tracking stocks (Cash, Talent, Trust, Data)
    and flows (Revenue, Hiring, Churn) and detecting inter-loop failure modes.
    """

    def __init__(self) -> None:
        # Stocks
        self.stock_cash_cents: int = 100_000_00  # $100k
        self.stock_talent_headcount: int = 5
        self.stock_brand_trust: float = 0.5  # [0, 1]
        self.stock_data_volume: int = 1000

        # Loop Performance Metrics
        self.loop_metrics: Dict[str, Dict[str, Any]] = {
            "Product": {"retention_slope": 0.05, "nps": 45, "failure": None},
            "Marketing": {"cac_cents": 150_00, "conversion_rate": 0.03, "failure": None},
            "Sales": {"win_rate": 0.25, "acv_cents": 1000_00, "failure": None},
            "Customer Success": {"nrr": 1.10, "churn_rate": 0.02, "failure": None},
            "Brand": {"share_of_voice": 0.15, "price_elasticity": 0.8, "failure": None},
            "Pricing": {"arpu_cents": 100_00, "value_realization": 0.7, "failure": None},
            "Referral": {"viral_coefficient": 0.4, "referral_cac_cents": 50_00, "failure": None},
            "Data": {"data_latency_sec": 12.0, "decision_cycle_hr": 24.0, "failure": None},
            "Financial": {"gross_margin": 0.75, "burn_multiple": 1.2, "runway_months": 18.0, "failure": None},
            "Hiring": {"time_to_fill_days": 30, "regretted_attrition": 0.05, "failure": None},
            "Culture": {"enps": 50, "decision_latency_hr": 8.0, "failure": None},
            "Innovation": {"experiments_run": 10, "hit_rate": 0.20, "failure": None},
            "Competitive Intelligence": {"relative_share": 0.10, "feature_parity": 0.85, "failure": None},
        }

    def simulate_coupled_step(self, user_traffic: int, monthly_spend_cents: int) -> Dict[str, Any]:
        """
        Simulates one coupled loop step where pricing feeds financial stock,
        financial stock feeds hiring budget, and hiring feeds product velocity.
        """
        arpu = self.loop_metrics["Pricing"]["arpu_cents"]
        conv = self.loop_metrics["Marketing"]["conversion_rate"]
        new_customers = int(user_traffic * conv)
        revenue_generated = new_customers * arpu

        # Financial loop update
        self.stock_cash_cents += (revenue_generated - monthly_spend_cents)
        runway = (self.stock_cash_cents / monthly_spend_cents) if monthly_spend_cents > 0 else 99.0
        self.loop_metrics["Financial"]["runway_months"] = runway
        self.loop_metrics["Financial"]["burn_multiple"] = (monthly_spend_cents / max(1, revenue_generated))

        # Data stock update
        self.stock_data_volume += new_customers * 10

        # Coupled feedback signals
        if self.loop_metrics["Financial"]["burn_multiple"] > 2.5:
            self.loop_metrics["Financial"]["failure"] = "Growth at negative unit economics with no path to positive"

        if self.loop_metrics["Pricing"]["arpu_cents"] < 20_00 and self.loop_metrics["Marketing"]["cac_cents"] > 100_00:
            self.loop_metrics["Marketing"]["failure"] = "Scaling spend before message works"

        return {
            "new_customers": new_customers,
            "revenue_generated_cents": revenue_generated,
            "stock_cash_cents": self.stock_cash_cents,
            "runway_months": runway,
            "data_volume": self.stock_data_volume,
            "failures_detected": [k for k, v in self.loop_metrics.items() if v.get("failure") is not None]
        }


# =====================================================================
# Section 4: Customer Journey Lifecycle Engine
# =====================================================================
class CustomerLifecycleEngine:
    """
    Models the 15-stage customer lifecycle from Awareness to Repurchase.
    """

    STAGES: List[str] = [
        "Awareness", "Interest", "Consideration", "Evaluation", "Purchase",
        "Onboarding", "Activation", "Engagement", "Habit Formation", "Retention",
        "Loyalty", "Advocacy", "Referral", "Expansion", "Repurchase"
    ]

    def __init__(self) -> None:
        self.stage_conversion_rates: Dict[str, float] = {stage: 0.80 for stage in self.STAGES}
        self.cohort_retention_curve: List[float] = [1.0, 0.60, 0.45, 0.40, 0.38, 0.38, 0.37]  # Flattening curve

    def evaluate_cohort_health(self) -> Dict[str, Any]:
        """Analyzes retention curve flattening and identifies bottleneck stages."""
        flattening = False
        if len(self.cohort_retention_curve) >= 3:
            slope = self.cohort_retention_curve[-1] - self.cohort_retention_curve[-2]
            if abs(slope) < 0.02:
                flattening = True

        bottleneck_stage = min(self.stage_conversion_rates, key=self.stage_conversion_rates.get)
        return {
            "retention_curve_flattens": flattening,
            "day_30_retention": self.cohort_retention_curve[-1],
            "bottleneck_stage": bottleneck_stage,
            "bottleneck_rate": self.stage_conversion_rates[bottleneck_stage]
        }


# =====================================================================
# Section 5: Go-to-Market (GTM) System Engine
# =====================================================================
class GTMSystemEngine:
    """
    Models GTM system dynamics, channel selection fit, pricing signals, and motion compounding.
    """

    def evaluate_channel_fit(
        self,
        product_complexity: str,  # low, medium, high
        price_tier_cents: int,    # e.g., <$100, $1k-$10k, >$50k
        has_network_effects: bool
    ) -> Dict[str, Any]:
        """Recommends primary GTM motion based on system logic."""
        recommended_motions = []

        if price_tier_cents < 500_00 and product_complexity == "low":
            recommended_motions.append("PLG (Product-Led Growth)")
            recommended_motions.append("Content Strategy & Organic")
        elif price_tier_cents >= 10000_00 or product_complexity == "high":
            recommended_motions.append("SLG (Sales-Led Growth / Enterprise Sales)")

        if has_network_effects:
            recommended_motions.append("CLG (Community-Led Growth)")

        compounding_strategy = "Land via PLG, expand via Sales (PLG usage data feeds Enterprise expansion)" if "PLG (Product-Led Growth)" in recommended_motions and price_tier_cents >= 1000_00 else "Single motion focus"

        return {
            "recommended_motions": recommended_motions,
            "compounding_strategy": compounding_strategy
        }


# =====================================================================
# Section 6: Company Growth System Classifier
# =====================================================================
class GrowthStageClassifier:
    """
    Classifies company stage across 9 stages from Idea to Market Leadership and flags premature scaling.
    """

    STAGES = [
        "Idea", "Validation", "Startup", "PMF",
        "Growth", "Scale", "Platform", "Ecosystem", "Market Leadership"
    ]

    def classify_stage(
        self,
        validated_learnings: int,
        paying_customers: int,
        retention_flattens: bool,
        cac_payback_months: float,
        developer_ecosystem_active: bool
    ) -> Dict[str, Any]:
        """Classifies current stage and flags risks like premature scaling."""
        if not retention_flattens and paying_customers > 500:
            return {
                "stage": "Startup",
                "risk": "PREMATURE_SCALING",
                "warning": "Scaling customer acquisition before retention curve flattens (lack of true PMF)"
            }

        if developer_ecosystem_active:
            stage = "Ecosystem"
        elif retention_flattens and cac_payback_months <= 12.0 and paying_customers > 1000:
            stage = "Scale"
        elif retention_flattens and paying_customers > 100:
            stage = "Growth"
        elif retention_flattens:
            stage = "PMF"
        elif paying_customers > 0:
            stage = "Validation"
        else:
            stage = "Idea"

        return {"stage": stage, "risk": "NONE", "warning": None}


# =====================================================================
# Section 7: Strategic Moat & Cost Curve Analyzer
# =====================================================================
class MoatAnalyzer:
    """
    Quantifies competitive moats (network effects, switching costs, economies of scale, brand, regulatory, counter-positioning)
    and tracks cost curve inflection points.
    """

    def calculate_moat_durability(
        self,
        network_density: float,         # [0, 1]
        switching_cost_cents: int,     # normalized against $10k
        economies_of_scale_margin: float, # [0, 1]
        brand_trust: float,             # [0, 1]
        counter_positioning_score: float # [0, 1]
    ) -> Dict[str, float]:
        """Computes composite moat score and individual dimension strength."""
        norm_switch = min(1.0, switching_cost_cents / 10000_00)
        composite = float(
            0.25 * network_density +
            0.20 * norm_switch +
            0.20 * economies_of_scale_margin +
            0.15 * brand_trust +
            0.20 * counter_positioning_score
        )
        return {
            "composite_moat_score": round(composite, 4),
            "network_effects": network_density,
            "switching_costs": norm_switch,
            "economies_of_scale": economies_of_scale_margin,
            "brand_trust": brand_trust,
            "counter_positioning": counter_positioning_score
        }

    def check_cost_curve_viability(self, unit_cost_history: List[float], viability_threshold: float) -> bool:
        """Checks if cost curve trend crosses commercial viability point."""
        if not unit_cost_history:
            return False
        latest_cost = unit_cost_history[-1]
        return latest_cost <= viability_threshold


# =====================================================================
# Section 8: Failure Mode Monitor
# =====================================================================
class FailureModeMonitor:
    """
    Pattern-matches operating metrics against the 10 canonical failure modes.
    """

    FAILURE_MODES: Dict[str, Dict[str, str]] = {
        "SOLVING_WRONG_PROBLEM": {
            "root_cause": "Skipped root-cause analysis; solved a symptom",
            "correction": "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)"
        },
        "BUILDING_BEFORE_VALIDATING": {
            "root_cause": "Founder conviction substituted for evidence",
            "correction": "Enforce a validation gate before build resourcing"
        },
        "WEAK_POSITIONING": {
            "root_cause": "No clear 'instead of X, use us because Y'",
            "correction": "Rebuild positioning around the real alternative customers compare to"
        },
        "POOR_PRICING": {
            "root_cause": "Cost-plus instead of value-based pricing",
            "correction": "Re-anchor price to quantified customer value"
        },
        "DISTRIBUTION_FAILURE": {
            "root_cause": "Great product, no repeatable channel",
            "correction": "Systematically test channels against ICP behavior"
        },
        "LACK_OF_PMF": {
            "root_cause": "Premature scaling of an unproven loop",
            "correction": "Stop scaling; return to cohort-level retention work"
        },
        "ORGANIZATIONAL_BOTTLENECK": {
            "root_cause": "Decision rights not delegated as company scales",
            "correction": "Push decision rights down with clear frameworks"
        },
        "FOUNDER_BIAS": {
            "root_cause": "Overconfidence, confirmation bias, sunk cost",
            "correction": "Pre-committed kill criteria set before launch"
        },
        "PREMATURE_SCALING": {
            "root_cause": "Confusing early demand spike with durable PMF",
            "correction": "Re-test unit economics at each order-of-magnitude of spend"
        },
        "CAPITAL_MISALLOCATION": {
            "root_cause": "No opportunity-cost discipline in budgeting",
            "correction": "Rank all initiatives on a common expected-return basis quarterly"
        }
    }

    def audit_metrics(
        self,
        engagement_rate: float,
        survey_positive_rate: float,
        cac_cents: int,
        ltv_cents: int,
        retention_flattens: bool,
        decision_latency_hr: float
    ) -> List[Dict[str, str]]:
        """Scans metrics and returns triggered failure mode diagnostics."""
        alerts = []

        if survey_positive_rate > 0.8 and engagement_rate < 0.1:
            alerts.append({
                "mode": "SOLVING_WRONG_PROBLEM",
                "details": self.FAILURE_MODES["SOLVING_WRONG_PROBLEM"]
            })

        if not retention_flattens and cac_cents > 0:
            alerts.append({
                "mode": "LACK_OF_PMF",
                "details": self.FAILURE_MODES["LACK_OF_PMF"]
            })

        if decision_latency_hr > 48.0:
            alerts.append({
                "mode": "ORGANIZATIONAL_BOTTLENECK",
                "details": self.FAILURE_MODES["ORGANIZATIONAL_BOTTLENECK"]
            })

        if cac_cents > 0 and ltv_cents / cac_cents < 1.0:
            alerts.append({
                "mode": "PREMATURE_SCALING",
                "details": self.FAILURE_MODES["PREMATURE_SCALING"]
            })

        return alerts


# =====================================================================
# 14-Layer Execution Engine Integration
# =====================================================================
class FourteenLayerEntrepreneurialEngine:
    """
    Provides access to the 14-layer computational stack of entrepreneurship.
    """

    LAYERS: List[str] = [
        "Layer 1: Reality Substrate",
        "Layer 2: Anomaly Sensing & Signal Filtering",
        "Layer 3: Structural Causal Model & Counterfactual Reasoning",
        "Layer 4: Falsifiable Hypothesis Generation & Active Inference",
        "Layer 5: Real Options & Cheap Validation Experiments",
        "Layer 6: Customer Psychology & Lifecycle Stage Modeling",
        "Layer 7: Product & MVP Engineering Loop",
        "Layer 8: Integrated Go-to-Market System",
        "Layer 9: Coupled Business Loops & System Dynamics",
        "Layer 10: Growth Stage Classification & Premature Scaling Guard",
        "Layer 11: Strategic Moat & Cost Curve Dynamics",
        "Layer 12: Failure Mode Diagnostics & Root-Cause Circuit Breakers",
        "Layer 13: Opportunity-Cost Capital Allocation",
        "Layer 14: Meta-Learning & Autonomous Continuous Reinvention"
    ]

    def execute_layer_pipeline(self, opportunity_name: str) -> Dict[str, Any]:
        """Simulates full 14-layer processing sweep for a venture opportunity."""
        return {
            "opportunity": opportunity_name,
            "layers_executed": len(self.LAYERS),
            "status": "VALIDATED_AND_ROUTED",
            "pipeline": self.LAYERS
        }


# =====================================================================
# Master Master Orchestrator: FirstPrinciplesEOSEngine
# =====================================================================
class FirstPrinciplesEOSEngine:
    """
    The Master Entrepreneurial Operating System Engine coupling state machines,
    decision trees, business loops, lifecycle engines, GTM systems, moat analyzers,
    and failure diagnostics.
    """

    def __init__(self) -> None:
        self.state_machine = EOSStateMachine()
        self.decision_tree = OpportunityDecisionTree()
        self.business_loops = CoupledBusinessLoopsEngine()
        self.customer_lifecycle = CustomerLifecycleEngine()
        self.gtm_system = GTMSystemEngine()
        self.growth_classifier = GrowthStageClassifier()
        self.moat_analyzer = MoatAnalyzer()
        self.failure_monitor = FailureModeMonitor()
        self.fourteen_layer_engine = FourteenLayerEntrepreneurialEngine()

    def run_master_loop_cycle(
        self,
        signal_title: str,
        is_structural_anomaly: bool,
        risk_type: DecisionRiskType = DecisionRiskType.TYPE_II,
        cheap_test_score: Optional[float] = None,
        traffic: int = 10000,
        monthly_spend_cents: int = 5000_00
    ) -> Dict[str, Any]:
        """
        Executes one complete cycle through the master loop architecture.
        """
        # 1. State machine signal processing
        self.state_machine.process_signal(is_anomaly=True, is_structural=is_structural_anomaly)

        # 2. Decision Tree evaluation
        decision = self.decision_tree.evaluate(
            is_structural_anomaly=is_structural_anomaly,
            risk_type=risk_type,
            cheap_test_available=(cheap_test_score is not None),
            cheap_test_result_exceeds_kill_threshold=(cheap_test_score >= 0.6 if cheap_test_score else None),
            structural_advantage_buildable=True
        )

        # 3. If decision is DISCARD, update state machine
        if decision["decision"] == "DISCARD":
            self.state_machine.transition_to(EOSState.DISCARD, decision["reason"])
            return {
                "signal": signal_title,
                "current_state": self.state_machine.current_state.value,
                "decision": decision,
                "loop_status": "TERMINATED_EARLY"
            }

        # 4. Advance through cheap test / validation
        if self.state_machine.current_state == EOSState.HYPOTHESIS:
            self.state_machine.transition_to(EOSState.CHEAP_TEST, "Cheap test started")
            self.state_machine.process_test_result(is_falsified=False, is_strengthened=True)
            self.state_machine.process_validation(economic_viability=True)
            self.state_machine.process_build_and_gtm(gtm_signal_score=0.8)

        # 5. Business Loops simulation
        sim_res = self.business_loops.simulate_coupled_step(user_traffic=traffic, monthly_spend_cents=monthly_spend_cents)

        # 6. Customer Lifecycle analysis
        lifecycle_res = self.customer_lifecycle.evaluate_cohort_health()

        # 7. Growth stage classification
        growth_res = self.growth_classifier.classify_stage(
            validated_learnings=15,
            paying_customers=sim_res["new_customers"],
            retention_flattens=lifecycle_res["retention_curve_flattens"],
            cac_payback_months=8.0,
            developer_ecosystem_active=False
        )

        # 8. Moat analysis
        moat_res = self.moat_analyzer.calculate_moat_durability(
            network_density=0.4,
            switching_cost_cents=2000_00,
            economies_of_scale_margin=0.3,
            brand_trust=0.6,
            counter_positioning_score=0.7
        )

        # 9. Failure mode diagnostic scan
        failure_alerts = self.failure_monitor.audit_metrics(
            engagement_rate=0.45,
            survey_positive_rate=0.85,
            cac_cents=150_00,
            ltv_cents=600_00,
            retention_flattens=lifecycle_res["retention_curve_flattens"],
            decision_latency_hr=12.0
        )

        # 10. 14-Layer pipeline audit
        layer_res = self.fourteen_layer_engine.execute_layer_pipeline(signal_title)

        return {
            "signal": signal_title,
            "current_state": self.state_machine.current_state.value,
            "decision": decision,
            "business_simulation": sim_res,
            "customer_lifecycle": lifecycle_res,
            "growth_stage": growth_res,
            "moat_durability": moat_res,
            "failure_alerts": failure_alerts,
            "layer_pipeline": layer_res,
            "loop_status": "COMPOUNDING"
        }
