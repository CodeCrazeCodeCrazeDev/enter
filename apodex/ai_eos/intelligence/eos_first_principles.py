"""Entrepreneurial Operating System (EOS) First-Principles Engine.

Implements the 11-section first-principles reconstruction of how elite founders
sense, build, and compound enduring companies into executable code:
- Master Loop & Multi-Timescale Feedback Loops (§1)
- Anomaly Detection & Signal-to-Idea Pipeline (§2.1)
- Mental Model Evolution Engine (§2.2)
- External Business Loops Engine (§3)
- Customer Journey Lifecycle Engine (§4)
- Integrated Go-to-Market (GTM) System Simulator (§5)
- Company Growth State Machine (§6)
- Strategic Moats & Cost Curves Engine (§7)
- Failure Mode Diagnostic Monitor (§8)
- AI Agent Operating State Machine & Decision Tree (§10)
"""

from __future__ import annotations
import math
import logging
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum, auto

logger = logging.getLogger("sero.eos_first_principles")


# =====================================================================
# Enums and Value Objects
# =====================================================================
class RiskType(Enum):
    TYPE_I = "type_i_irreversible"  # One-way door
    TYPE_II = "type_ii_reversible"  # Two-way door


class DecisionOutcome(Enum):
    DISCARD = "discard"
    CHEAP_TEST = "cheap_test"
    VALIDATE = "validate"
    BUILD_MVP = "build_mvp"
    COMMIT_RESOURCES = "commit_resources"


class GrowthStage(Enum):
    IDEA = "idea"
    VALIDATION = "validation"
    STARTUP = "startup"
    PMF = "product_market_fit"
    GROWTH = "growth"
    SCALE = "scale"
    PLATFORM = "platform"
    ECOSYSTEM = "ecosystem"
    LEADERSHIP = "market_leadership"


class SystemState(Enum):
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


# =====================================================================
# 1. Anomaly Sensing & Signal-to-Idea Pipeline (§1, §2.1)
# =====================================================================
class SignalAnomalyDetector:
    """Detects market anomalies, classifies structural vs noise signals, and generates hypotheses."""

    def __init__(self, sensitivity: float = 0.75) -> None:
        self.sensitivity = sensitivity
        self.observed_signals: List[Dict[str, Any]] = []

    def evaluate_signal(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Classify weak signal into structural shift vs noise, evaluate Type I vs Type II risk."""
        is_anomaly = signal.get("deviation", 0.0) >= self.sensitivity
        is_structural = is_anomaly and signal.get("structural_confidence", 0.0) >= 0.60
        risk_type = RiskType.TYPE_I if signal.get("irreversible", False) else RiskType.TYPE_II

        result = {
            "signal_id": signal.get("id", str(uuid4())),
            "is_anomaly": is_anomaly,
            "is_structural": is_structural,
            "risk_type": risk_type.value,
            "recommended_action": DecisionOutcome.DISCARD.value
        }

        if is_structural:
            if risk_type == RiskType.TYPE_II:
                result["recommended_action"] = DecisionOutcome.CHEAP_TEST.value
            else:
                # Type I risk requires multi-source verification
                if signal.get("multi_source_verified", False):
                    result["recommended_action"] = DecisionOutcome.VALIDATE.value
                else:
                    result["recommended_action"] = DecisionOutcome.DISCARD.value

        self.observed_signals.append(result)
        return result

    def form_falsifiable_hypothesis(
        self,
        claim: str,
        kill_threshold: float,
        metric: str
    ) -> Dict[str, Any]:
        """Constructs a structured hypothesis with pre-committed kill criteria."""
        return {
            "hypothesis_id": str(uuid4()),
            "claim": claim,
            "metric": metric,
            "kill_threshold": kill_threshold,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "proposed",
            "test_results": []
        }


# =====================================================================
# 2. Mental Model Evolution Engine (§2.2)
# =====================================================================
class MentalModelEvolutionEngine:
    """Tracks founder mental models, parameter tuning, and structural paradigm updates."""

    def __init__(self, initial_structure: Dict[str, Any]) -> None:
        self.structure = initial_structure
        self.parameters: Dict[str, float] = {
            "customer_acquisition_efficiency": 1.0,
            "retention_flatline_level": 0.30,
            "market_growth_rate": 0.15
        }
        self.contradictions_count: int = 0
        self.paradigm_shifts: int = 0

    def process_feedback(self, actual_metric: str, expected_val: float, actual_val: float) -> str:
        """Update parameter (fast) or trigger structural update (paradigm shift)."""
        error = abs(actual_val - expected_val) / max(1e-5, abs(expected_val))

        if error < 0.25:
            # Minor variance: tune parameter
            if actual_metric in self.parameters:
                self.parameters[actual_metric] = 0.8 * self.parameters[actual_metric] + 0.2 * actual_val
            return "parameter_tuned"
        else:
            # Significant contradiction
            self.contradictions_count += 1
            if self.contradictions_count >= 3:
                # Structural paradigm shift required
                self.paradigm_shifts += 1
                self.contradictions_count = 0
                logger.warning("PARADIGM SHIFT: Structural mental model shift triggered!")
                return "structural_paradigm_shift"
            return "contradiction_recorded"


# =====================================================================
# 3. External Business Loops Engine (§3)
# =====================================================================
class ExternalBusinessLoopsEngine:
    """Models and couples all 13 external business loops with stocks and flows."""

    def __init__(self) -> None:
        self.stocks = {
            "cash_cents": 1_000_000_00,  # $1M
            "talent_score": 1.0,
            "brand_trust": 0.50,
            "data_assets": 100
        }
        self.loop_kpis: Dict[str, float] = {
            "product_retention": 0.40,
            "marketing_cac_cents": 5000,
            "sales_win_rate": 0.25,
            "cs_nrr": 1.10,
            "brand_recall": 0.20,
            "pricing_arpu_cents": 20000,
            "referral_k_factor": 0.15,
            "data_latency_sec": 3.0,
            "financial_gross_margin": 0.75,
            "financial_burn_multiple": 1.2,
            "hiring_time_to_fill_days": 30.0,
            "culture_enps": 45.0,
            "innovation_experiments_run": 5.0,
            "competitive_feature_parity": 0.80
        }

    def execute_coupled_cycle(self, R_and_D_investment_cents: int) -> Dict[str, Any]:
        """Execute one cycle updating coupled loops and stocks."""
        # Pricing ARPU & Financials
        arpu = self.loop_kpis["pricing_arpu_cents"]
        gross_margin = self.loop_kpis["financial_gross_margin"]

        # Product retention feeds CS NRR
        self.loop_kpis["cs_nrr"] = 0.90 + 0.50 * self.loop_kpis["product_retention"]

        # R&D investment feeds innovation & product retention
        if R_and_D_investment_cents > 0:
            self.loop_kpis["innovation_experiments_run"] += 1.0
            self.loop_kpis["product_retention"] = min(0.95, self.loop_kpis["product_retention"] + 0.01)

        # Financial stock update
        revenue_generated = int(arpu * gross_margin * 50)  # assume 50 active accounts
        self.stocks["cash_cents"] += revenue_generated - R_and_D_investment_cents

        return {
            "stocks": self.stocks,
            "loop_kpis": self.loop_kpis
        }


# =====================================================================
# 4. Customer Journey Lifecycle Engine (§4)
# =====================================================================
class CustomerLifecycleEngine:
    """Manages full 15-stage customer journey transitions and lever optimizations."""

    STAGES = [
        "awareness", "interest", "consideration", "evaluation", "purchase",
        "onboarding", "activation", "engagement", "habit_formation",
        "retention", "loyalty", "advocacy", "referral", "expansion", "repurchase"
    ]

    def __init__(self) -> None:
        self.conversion_rates: Dict[str, float] = {
            "awareness_to_interest": 0.10,
            "interest_to_consideration": 0.30,
            "consideration_to_evaluation": 0.40,
            "evaluation_to_purchase": 0.20,
            "purchase_to_onboarding": 0.95,
            "onboarding_to_activation": 0.60,
            "activation_to_retention": 0.50,
            "retention_to_expansion": 0.25
        }

    def simulate_funnel(self, initial_awareness: int) -> Dict[str, int]:
        """Run cohort flow through the customer lifecycle."""
        funnel = {"awareness": initial_awareness}
        curr = initial_awareness

        for i in range(len(self.STAGES) - 1):
            s_from = self.STAGES[i]
            s_to = self.STAGES[i + 1]
            key = f"{s_from}_to_{s_to}"
            rate = self.conversion_rates.get(key, 0.50)
            curr = int(curr * rate)
            funnel[s_to] = curr

        return funnel

    def optimize_lever(self, bottleneck_stage: str) -> str:
        """Return optimization lever for identified bottleneck stage (§4)."""
        levers = {
            "awareness": "Sharp category framing / naming a new category",
            "interest": "Lead with the pain, not the product",
            "consideration": "Reframe the comparison axis",
            "evaluation": "Make failure cheap and reversible",
            "purchase": "Remove steps, not add persuasion",
            "onboarding": "Anchor onboarding to JTBD",
            "activation": "Instrument true 'aha' moment via cohort analysis",
            "retention": "Cohort-level retention curve flattening point analysis",
            "expansion": "Usage-based expansion triggers"
        }
        return levers.get(bottleneck_stage, "Run targeted customer discovery")


# =====================================================================
# 5. Integrated Go-to-Market (GTM) System Simulator (§5)
# =====================================================================
class GTMSystemSimulator:
    """Models positioning, channel fit, pricing signal, and motion compounding."""

    def __init__(self) -> None:
        pass

    def evaluate_motion_fit(
        self,
        acv_cents: int,
        complexity_score: float  # 0 (low) to 1 (high)
    ) -> Dict[str, Any]:
        """Determine primary GTM motion based on ACV and product complexity."""
        if acv_cents >= 100000_00 or complexity_score > 0.7:
            primary_motion = "Sales-Led Growth (SLG / Enterprise)"
            channels = ["Outbound Enterprise Sales", "Account-Based Marketing", "Executive Briefings"]
        elif acv_cents <= 5000_00 and complexity_score <= 0.3:
            primary_motion = "Product-Led Growth (PLG)"
            channels = ["Self-Serve Onboarding", "SEO / Content", "Virality / Referral"]
        else:
            primary_motion = "Hybrid Motion (PLG Land, SLG Expand)"
            channels = ["Self-Serve Trial", "Inside Sales", "Community-Led Growth"]

        return {
            "acv_cents": acv_cents,
            "complexity_score": complexity_score,
            "primary_motion": primary_motion,
            "recommended_channels": channels,
            "pricing_positioning_signal": "High Intent Filter" if acv_cents >= 50000_00 else "Low Friction Volume Filter"
        }


# =====================================================================
# 6. Company Growth State Machine (§6)
# =====================================================================
class CompanyGrowthStateMachine:
    """Models stage transitions across the 9 company growth stages (§6)."""

    def __init__(self) -> None:
        self.current_stage: GrowthStage = GrowthStage.IDEA
        self.history: List[Tuple[GrowthStage, datetime]] = [(self.current_stage, datetime.now(timezone.utc))]

    def evaluate_stage_transition(self, metrics: Dict[str, Any]) -> Tuple[GrowthStage, bool]:
        """Evaluate if venture meets criteria to advance to next growth stage."""
        prev_stage = self.current_stage

        if self.current_stage == GrowthStage.IDEA:
            if metrics.get("validated_learnings", 0) >= 5:
                self.current_stage = GrowthStage.VALIDATION
        elif self.current_stage == GrowthStage.VALIDATION:
            if metrics.get("paying_customers", 0) >= 3:
                self.current_stage = GrowthStage.STARTUP
        elif self.current_stage == GrowthStage.STARTUP:
            if metrics.get("ltv_to_cac", 0.0) >= 3.0 and metrics.get("runway_months", 0) >= 12:
                self.current_stage = GrowthStage.PMF
        elif self.current_stage == GrowthStage.PMF:
            if metrics.get("retention_curve_flattened", False) and metrics.get("growth_rate_mom", 0.0) >= 0.15:
                self.current_stage = GrowthStage.GROWTH
        elif self.current_stage == GrowthStage.GROWTH:
            if metrics.get("arr_cents", 0) >= 10000000_00:  # $10M ARR
                self.current_stage = GrowthStage.SCALE
        elif self.current_stage == GrowthStage.SCALE:
            if metrics.get("third_party_devs", 0) >= 100:
                self.current_stage = GrowthStage.PLATFORM

        advanced = self.current_stage != prev_stage
        if advanced:
            self.history.append((self.current_stage, datetime.now(timezone.utc)))
            logger.info(f"GROWTH STAGE ADVANCED: {prev_stage.value} -> {self.current_stage.value}")

        return self.current_stage, advanced


# =====================================================================
# 7. Strategic Moats & Cost Curves Engine (§7)
# =====================================================================
class StrategicMoatEngine:
    """Calculates Hamilton Helmer 7 Powers durability and tech shift timing."""

    def __init__(self) -> None:
        pass

    def calculate_7_powers_score(self, power_metrics: Dict[str, float]) -> float:
        """Composite 7 Powers Moat Durability Score [0, 1].

        Powers: Network Effects, Switching Costs, Cornered Resource, Scale Economies,
        Counter-Positioning, Brand, Process Power.
        """
        weights = {
            "network_effects": 0.20,
            "switching_costs": 0.15,
            "cornered_resource": 0.15,
            "scale_economies": 0.15,
            "counter_positioning": 0.15,
            "brand": 0.10,
            "process_power": 0.10
        }
        total_score = 0.0
        for power, weight in weights.items():
            val = min(1.0, max(0.0, power_metrics.get(power, 0.0)))
            total_score += val * weight
        return float(total_score)

    def evaluate_cost_curve_crossing(
        self,
        current_unit_cost: float,
        cost_decline_rate_per_year: float,
        viability_threshold: float
    ) -> float:
        """Calculate years until technology cost curve crosses commercial viability threshold."""
        if current_unit_cost <= viability_threshold:
            return 0.0
        if cost_decline_rate_per_year <= 0.0:
            return float("inf")

        # logarithmic decay: cost(t) = cost(0) * (1 - decline_rate)^t
        years = math.log(viability_threshold / current_unit_cost) / math.log(1.0 - cost_decline_rate_per_year)
        return max(0.0, float(years))


# =====================================================================
# 8. Failure Mode Diagnostic Monitor (§8)
# =====================================================================
class FailureModeMonitor:
    """Diagnostic pattern-matching for 10 core failure modes with early warnings."""

    def __init__(self) -> None:
        pass

    def audit_operating_metrics(self, metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify failure modes from operating metrics (§8)."""
        warnings = []

        # Premature scaling
        if metrics.get("cac_cents", 0) > 0 and metrics.get("ltv_cents", 0) > 0:
            if metrics.get("growth_rate_mom", 0.0) > 0.30 and (metrics["ltv_cents"] / metrics["cac_cents"]) < 2.0:
                warnings.append({
                    "failure_mode": "Premature Scaling",
                    "root_cause": "Confusing early demand spike with durable PMF",
                    "detection_signal": "CAC rising faster than LTV as spend scales",
                    "correction": "Re-test unit economics at each order-of-magnitude of spend"
                })

        # Solving the wrong problem
        if metrics.get("survey_satisfaction", 0.0) > 0.80 and metrics.get("activation_rate", 0.0) < 0.15:
            warnings.append({
                "failure_mode": "Solving the Wrong Problem",
                "root_cause": "Skipped root-cause analysis; solved a symptom",
                "detection_signal": "Low engagement despite 'positive' survey feedback",
                "correction": "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)"
            })

        # Distribution failure
        if metrics.get("nps", 0) > 50 and metrics.get("organic_growth_rate", 0.0) <= 0.02:
            warnings.append({
                "failure_mode": "Distribution Failure",
                "root_cause": "Great product, no repeatable channel",
                "detection_signal": "High NPS, flat growth",
                "correction": "Systematically test channels against ICP behavior"
            })

        # Organizational bottlenecks
        if metrics.get("decision_latency_days", 0) > 14:
            warnings.append({
                "failure_mode": "Organizational Bottlenecks",
                "root_cause": "Decision rights not delegated as company scales",
                "detection_signal": "Rising decision latency, founder as single point of failure",
                "correction": "Push decision rights down with clear frameworks"
            })

        return warnings


# =====================================================================
# 9. AI Operating Decision Tree & System State Machine (§10)
# =====================================================================
class EOSOpportunityDecisionTree:
    """Evaluates 'Should We Pursue This Opportunity?' (§10.2)."""

    def evaluate_opportunity(self, opp_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tree evaluation returning outcome and decision path."""
        path = []

        # Q1: Structural anomaly or just noise?
        if not opp_data.get("is_structural_anomaly", False):
            path.append("Q1: Noise -> Discard")
            return {"outcome": DecisionOutcome.DISCARD.value, "path": path}
        path.append("Q1: Structural Anomaly")

        # Q2: Reversible decision?
        if opp_data.get("is_reversible", True):
            path.append("Q2: Reversible (Type II)")
            # Q3: Cheap test available?
            if opp_data.get("cheap_test_available", True):
                path.append("Q3: Cheap test available -> Run Cheap Test")
                return {"outcome": DecisionOutcome.CHEAP_TEST.value, "path": path}
            else:
                path.append("Q3: No cheap test")
                if opp_data.get("expected_value_positive", False):
                    path.append("Q4b: Expected value positive")
                else:
                    path.append("Q4b: Expected value negative -> Discard")
                    return {"outcome": DecisionOutcome.DISCARD.value, "path": path}
        else:
            path.append("Q2: Irreversible (Type I)")
            # Q2a: High confidence signal from multiple sources?
            if not opp_data.get("multi_source_verified", False):
                path.append("Q2a: Unverified multi-source -> Discard")
                return {"outcome": DecisionOutcome.DISCARD.value, "path": path}
            path.append("Q2a: Verified multi-source")

        # Q5: Structural advantage?
        if opp_data.get("structural_advantage_possible", False):
            path.append("Q5: Structural advantage possible -> Commit Resources")
            return {"outcome": DecisionOutcome.COMMIT_RESOURCES.value, "path": path}
        else:
            path.append("Q5: No structural advantage -> Discard")
            return {"outcome": DecisionOutcome.DISCARD.value, "path": path}


# =====================================================================
# 10. Coordinating Orchestrator (`EOSEngineFirstPrinciples`)
# =====================================================================
class EOSEngineFirstPrinciples:
    """Unified Orchestrator coupling all 11 sections into closed-loop cycles."""

    def __init__(self) -> None:
        self.signal_detector = SignalAnomalyDetector()
        self.mental_model_engine = MentalModelEvolutionEngine(initial_structure={"paradigm": "v1_default"})
        self.business_loops = ExternalBusinessLoopsEngine()
        self.customer_lifecycle = CustomerLifecycleEngine()
        self.gtm_simulator = GTMSystemSimulator()
        self.growth_state_machine = CompanyGrowthStateMachine()
        self.moat_engine = StrategicMoatEngine()
        self.failure_monitor = FailureModeMonitor()
        self.decision_tree = EOSOpportunityDecisionTree()

        self.current_state: SystemState = SystemState.SENSING
        self.state_history: List[Tuple[SystemState, datetime]] = [(self.current_state, datetime.now(timezone.utc))]

    def transition_system_state(self, new_state: SystemState) -> None:
        """Record system state machine transitions (§10.1)."""
        self.current_state = new_state
        self.state_history.append((new_state, datetime.now(timezone.utc)))
        logger.info(f"SYSTEM STATE TRANSITION: -> {new_state.value}")

    def run_fast_loop(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Fast Loop (days-weeks): anomaly detection & cheap experiment decision."""
        self.transition_system_state(SystemState.SENSING)
        sig_result = self.signal_detector.evaluate_signal(signal)

        if sig_result["is_structural"]:
            self.transition_system_state(SystemState.HYPOTHESIS)
            hyp = self.signal_detector.form_falsifiable_hypothesis(
                claim=f"Structural shift: {signal.get('name', 'anomaly')}",
                kill_threshold=0.20,
                metric="conversion_rate"
            )
            self.transition_system_state(SystemState.CHEAP_TEST)
            return {"hypothesis": hyp, "signal_evaluation": sig_result}

        self.transition_system_state(SystemState.DISCARD)
        return {"signal_evaluation": sig_result}

    def run_medium_loop(self, gtm_input: Dict[str, Any], operating_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Medium Loop (months-quarters): GTM alignment, lifecycle, and failure diagnostics."""
        gtm_fit = self.gtm_simulator.evaluate_motion_fit(
            acv_cents=gtm_input.get("acv_cents", 10000_00),
            complexity_score=gtm_input.get("complexity_score", 0.5)
        )
        funnel = self.customer_lifecycle.simulate_funnel(initial_awareness=10000)
        warnings = self.failure_monitor.audit_operating_metrics(operating_metrics)
        stage, advanced = self.growth_state_machine.evaluate_stage_transition(operating_metrics)

        return {
            "gtm_fit": gtm_fit,
            "funnel": funnel,
            "failure_warnings": warnings,
            "current_growth_stage": stage.value,
            "advanced_stage": advanced
        }

    def run_slow_loop(self, moat_power_metrics: Dict[str, float]) -> Dict[str, Any]:
        """Slow Loop (years): strategic positioning, moat score, and mental model checks."""
        moat_score = self.moat_engine.calculate_7_powers_score(moat_power_metrics)

        if moat_score < 0.30:
            self.transition_system_state(SystemState.REINVENT)
            return {"moat_score": moat_score, "action": "Mandatory Self-Disruption Review"}

        return {"moat_score": moat_score, "action": "Defend & Extend Category"}
