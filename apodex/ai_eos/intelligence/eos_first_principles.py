"""First-Principles Reconstruction of the Entrepreneurial Operating System (EOS).

Implements multi-timescale loops, cognitive signal-to-idea pipelines, 13 coupled business loops,
15 customer journey stages, 9 growth stages, failure mode monitoring, decision trees, and system state machine.
"""

from __future__ import annotations
import uuid
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

logger = logging.getLogger("apodex.ai_eos.eos_first_principles")


class Timescale(str, Enum):
    FAST = "FAST"        # Days–weeks: experiments, sales calls, ad tests
    MEDIUM = "MEDIUM"    # Months–quarters: GTM iteration, pricing, org design
    SLOW = "SLOW"        # Years: strategic positioning, moats, category creation


class DecisionRiskType(str, Enum):
    TYPE_I_ONE_WAY = "TYPE_I_ONE_WAY"   # Irreversible, high stakes (slow, high scrutiny)
    TYPE_II_TWO_WAY = "TYPE_II_TWO_WAY" # Reversible, low stakes (fast, cheap test)


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


class CompanyGrowthStage(str, Enum):
    IDEA = "IDEA"
    VALIDATION = "VALIDATION"
    STARTUP = "STARTUP"
    PMF = "PMF"
    GROWTH = "GROWTH"
    SCALE = "SCALE"
    PLATFORM = "PLATFORM"
    ECOSYSTEM = "ECOSYSTEM"
    MARKET_LEADERSHIP = "MARKET_LEADERSHIP"


class EOSState(str, Enum):
    SENSING = "SENSING"
    HYPOTHESIS = "HYPOTHESIS"
    CHEAP_TEST = "CHEAP_TEST"
    DISCARD = "DISCARD"
    VALIDATION = "VALIDATION"
    BUILD_GATE = "BUILD_GATE"
    MVP = "MVP"
    GTM_TEST = "GTM_TEST"
    KILL_OR_SCALE = "KILL_OR_SCALE"
    SCALE = "SCALE"
    OPERATE = "OPERATE"
    REINVENT = "REINVENT"


# --- 1. Cognitive Signal-to-Idea Engine ---

class WeakSignal(BaseModel):
    signal_id: str = Field(default_factory=lambda: f"sig_{uuid.uuid4().hex[:8]}")
    description: str
    source: str
    is_structural_anomaly: bool = False
    confidence: float = 0.5


class FalsifiableHypothesis(BaseModel):
    hypothesis_id: str = Field(default_factory=lambda: f"hyp_{uuid.uuid4().hex[:8]}")
    claim: str
    cheap_test_description: str
    kill_threshold_metric: str
    kill_threshold_value: float
    risk_type: DecisionRiskType = DecisionRiskType.TYPE_II_TWO_WAY
    expected_value: float = 0.0
    structural_advantage: str = ""
    status: str = "PENDING"  # PENDING, STRENGTHENED, FALSIFIED


class AnomalyFilter:
    """Filters market/tech weak signals to detect structural anomalies vs noise."""

    def evaluate_signal(self, signal: WeakSignal, mental_model_predictions: Dict[str, Any]) -> bool:
        """Determines if a weak signal contradicts baseline predictions structurally."""
        if signal.is_structural_anomaly and signal.confidence >= 0.6:
            logger.info(f"[AnomalyFilter] Flagged structural anomaly: {signal.description}")
            return True
        return False


class SignalToIdeaPipeline:
    """Converts weak signals into falsifiable hypotheses and cheap tests."""

    def __init__(self) -> None:
        self.anomaly_filter = AnomalyFilter()
        self.active_hypotheses: List[FalsifiableHypothesis] = []

    def process_signal(self, signal: WeakSignal, claim: str, kill_metric: str, kill_val: float) -> Optional[FalsifiableHypothesis]:
        if not self.anomaly_filter.evaluate_signal(signal, {}):
            logger.info(f"[SignalToIdeaPipeline] Signal discarded as noise: {signal.description}")
            return None

        hyp = FalsifiableHypothesis(
            claim=claim,
            cheap_test_description=f"Run cheap validation test for: {claim}",
            kill_threshold_metric=kill_metric,
            kill_threshold_value=kill_val,
            risk_type=DecisionRiskType.TYPE_II_TWO_WAY if signal.confidence > 0.5 else DecisionRiskType.TYPE_I_ONE_WAY
        )
        self.active_hypotheses.append(hyp)
        return hyp

    def update_belief(self, hypothesis: FalsifiableHypothesis, test_result_value: float) -> str:
        if test_result_value < hypothesis.kill_threshold_value:
            hypothesis.status = "FALSIFIED"
            logger.info(f"[SignalToIdeaPipeline] Hypothesis {hypothesis.hypothesis_id} FALSIFIED ({test_result_value} < {hypothesis.kill_threshold_value}).")
        else:
            hypothesis.status = "STRENGTHENED"
            logger.info(f"[SignalToIdeaPipeline] Hypothesis {hypothesis.hypothesis_id} STRENGTHENED ({test_result_value} >= {hypothesis.kill_threshold_value}).")
        return hypothesis.status


# --- 2. Coupled Business Loops Engine ---

class BusinessLoop(BaseModel):
    name: str
    timescale: Timescale
    inputs: List[str]
    outputs: List[str]
    feedback_signal: str
    core_kpis: List[str]
    failure_mode: str


class CoupledBusinessLoopsEngine:
    """Manages 13 coupled business loops and tracks stocks and flows."""

    def __init__(self) -> None:
        self.stocks: Dict[str, float] = {
            "cash": 1000000.0,
            "talent": 10.0,
            "trust": 0.8,
            "data": 100.0
        }
        self.flows: Dict[str, float] = {
            "revenue": 50000.0,
            "hiring_rate": 1.0,
            "churn_rate": 0.03
        }
        self.loops: Dict[str, BusinessLoop] = self._init_13_loops()

    def _init_13_loops(self) -> Dict[str, BusinessLoop]:
        definitions = [
            ("Product", Timescale.FAST, ["User behavior", "support tickets"], ["Feature changes"], "Activation/retention deltas", ["Retention curve", "NPS"], "Building for loudest customer"),
            ("Marketing", Timescale.MEDIUM, ["Positioning", "market data"], ["Awareness", "demand"], "CAC, traffic quality", ["CAC", "Brand recall"], "Scaling spend before message works"),
            ("Sales", Timescale.FAST, ["Qualified leads", "product"], ["Closed revenue"], "Win/loss reasons", ["Win rate", "ACV"], "Selling to non-ICP"),
            ("Customer Success", Timescale.MEDIUM, ["Onboarding data"], ["Retention", "expansion"], "Churn reasons", ["NRR", "Time-to-value"], "Reactive-only CS"),
            ("Brand", Timescale.SLOW, ["Product experience"], ["Trust", "pricing power"], "Sentiment", ["Share of voice", "price elasticity"], "Brand as decoration"),
            ("Pricing", Timescale.MEDIUM, ["Value delivered"], ["Revenue", "positioning"], "Conversion by price point", ["ARPU", "Price realization"], "Cost-plus pricing"),
            ("Referral", Timescale.FAST, ["Customer satisfaction"], ["New customer flow"], "Referral rate", ["Viral coefficient (K)"], "Incentivizing volume over quality"),
            ("Data", Timescale.FAST, ["All loop data"], ["Decisions"], "Model accuracy vs outcomes", ["Data latency", "decision cycle"], "Vanity metrics"),
            ("Financial", Timescale.MEDIUM, ["Revenue", "costs"], ["Runway", "reinvestment"], "Burn multiple, margin", ["Gross margin", "Runway"], "Growth at negative unit economics"),
            ("Hiring", Timescale.MEDIUM, ["Org needs"], ["Capability", "capacity"], "90-day performance", ["Quality of hire", "retention"], "Hiring for pedigree over fit"),
            ("Culture", Timescale.SLOW, ["Values-in-action"], ["Behavior consistency"], "Employee sentiment", ["eNPS", "decision latency"], "Values-as-poster"),
            ("Innovation", Timescale.SLOW, ["R&D", "market signals"], ["New products"], "Time-to-market", ["# experiments", "hit rate"], "Innovation theater"),
            ("Competitive Intelligence", Timescale.MEDIUM, ["Competitor data"], ["Strategic repositioning"], "Win/loss vs competitors", ["Relative share trend"], "Reacting instead of running own strategy")
        ]
        res = {}
        for name, timescale, inputs, outputs, feedback, kpis, fail in definitions:
            res[name] = BusinessLoop(
                name=name,
                timescale=timescale,
                inputs=inputs,
                outputs=outputs,
                feedback_signal=feedback,
                core_kpis=kpis,
                failure_mode=fail
            )
        return res

    def step_simulation(self, delta_revenue: float, delta_hiring: float, delta_churn: float) -> Dict[str, float]:
        """Updates stock values according to feedback flows."""
        self.flows["revenue"] += delta_revenue
        self.flows["hiring_rate"] += delta_hiring
        self.flows["churn_rate"] = max(0.001, self.flows["churn_rate"] + delta_churn)

        # Coupled effects
        self.stocks["cash"] += self.flows["revenue"] - (self.stocks["talent"] * 10000.0)
        self.stocks["talent"] += self.flows["hiring_rate"] - (self.stocks["talent"] * self.flows["churn_rate"])
        self.stocks["trust"] = min(1.0, max(0.0, self.stocks["trust"] - (self.flows["churn_rate"] * 2.0) + 0.01))
        self.stocks["data"] += 10.0

        return self.stocks


# --- 3. Full Customer Journey System ---

class CustomerJourneyTracker:
    """Tracks cohort dynamics across all 15 customer journey stages."""

    def __init__(self) -> None:
        self.stage_counts: Dict[CustomerJourneyStage, int] = {stage: 0 for stage in CustomerJourneyStage}
        self.stage_counts[CustomerJourneyStage.AWARENESS] = 1000

    def transition_cohort(self, from_stage: CustomerJourneyStage, to_stage: CustomerJourneyStage, conversion_rate: float) -> int:
        current = self.stage_counts[from_stage]
        converted = int(current * max(0.0, min(1.0, conversion_rate)))
        self.stage_counts[from_stage] -= converted
        self.stage_counts[to_stage] += converted
        logger.info(f"[CustomerJourney] Shifted {converted} users from {from_stage.value} -> {to_stage.value}")
        return converted

    def get_funnel_summary(self) -> Dict[str, int]:
        return {stage.value: count for stage, count in self.stage_counts.items()}


# --- 4. Company Growth Stage Classifier ---

class GrowthStageClassifier:
    """Classifies company growth stage and identifies binding constraints & key risks."""

    def classify_stage(self, metrics: Dict[str, float]) -> Tuple[CompanyGrowthStage, str, str]:
        paying_customers = metrics.get("paying_customers", 0)
        retention_flattening = metrics.get("retention_curve_flat", 0.0)
        arr_usd = metrics.get("arr_usd", 0.0)
        rule_of_40 = metrics.get("rule_of_40", 0.0)
        ecosystem_gmv = metrics.get("ecosystem_gmv", 0.0)

        if ecosystem_gmv > 100_000_000:
            return CompanyGrowthStage.ECOSYSTEM, "Governance credibility", "Ecosystem fragmentation"
        if arr_usd > 50_000_000 and rule_of_40 > 0.4:
            return CompanyGrowthStage.SCALE, "Org coordination cost", "Culture dilution"
        if arr_usd > 10_000_000:
            return CompanyGrowthStage.GROWTH, "Hiring velocity", "Scaling a broken funnel"
        if retention_flattening > 0.4 and paying_customers >= 50:
            return CompanyGrowthStage.PMF, "Team bandwidth", "Mistaking early traction for PMF"
        if paying_customers >= 5:
            return CompanyGrowthStage.STARTUP, "Cash runway", "Premature scaling before PMF"
        if paying_customers > 0:
            return CompanyGrowthStage.VALIDATION, "Signal quality", "False positive validation"
        return CompanyGrowthStage.IDEA, "Founder time", "Solving a non-problem"


# --- 5. Opportunity Decision Tree & State Machine ---

class OpportunityDecisionTree:
    """Evaluates whether to pursue an opportunity using §10.2 decision logic."""

    def evaluate_opportunity(
        self,
        is_structural_anomaly: bool,
        is_reversible: bool,
        high_confidence_multi_source: bool,
        cheap_test_available: bool,
        test_exceeds_kill_threshold: bool,
        ev_positive: bool,
        has_structural_advantage: bool
    ) -> Tuple[bool, str]:
        if not is_structural_anomaly:
            return False, "Discarded: Signal is noise, not structural anomaly"

        if not is_reversible:
            if not high_confidence_multi_source:
                return False, "Discarded: Irreversible decision lacking high-confidence multi-source signal"

        if cheap_test_available:
            if not test_exceeds_kill_threshold:
                return False, "Discarded: Cheap test result failed kill threshold"
        else:
            if not ev_positive:
                return False, "Discarded: No cheap test and expected value not positive"

        if not has_structural_advantage:
            return False, "Discarded: Lacks structural advantage or defensible moat"

        return True, "Commit resources: Opportunity passed all decision tree filters"


class EOSStateMachine:
    """Tracks top-level state transitions of the AI-EOS runtime system."""

    VALID_TRANSITIONS: Dict[EOSState, List[EOSState]] = {
        EOSState.SENSING: [EOSState.HYPOTHESIS],
        EOSState.HYPOTHESIS: [EOSState.CHEAP_TEST, EOSState.DISCARD],
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

    def __init__(self) -> None:
        self.current_state: EOSState = EOSState.SENSING

    def transition_to(self, new_state: EOSState) -> bool:
        allowed = self.VALID_TRANSITIONS.get(self.current_state, [])
        if new_state in allowed:
            logger.info(f"[EOSStateMachine] Transition: {self.current_state.value} -> {new_state.value}")
            self.current_state = new_state
            return True
        logger.warning(f"[EOSStateMachine] Invalid transition attempted: {self.current_state.value} -> {new_state.value}")
        return False


# --- 6. Failure Mode Monitor & System KPI Stack ---

class FailureModeMonitor:
    """Monitors operating metrics against §8 failure modes."""

    FAILURE_PATTERNS = [
        ("Solving the wrong problem", "engagement < 0.2 and survey_positive > 0.8", "5-Whys / Jobs-to-be-Done interviews"),
        ("Building before validating", "build_velocity > 0.8 and demand_signal < 0.2", "Enforce validation gate before build resourcing"),
        ("Weak positioning", "cac > 500 and sales_cycle_days > 90", "Rebuild positioning around real alternative"),
        ("Lack of product-market fit", "retention_curve_slope < 0.01", "Stop scaling; return to cohort retention work"),
        ("Capital misallocation", "active_bets > 5 and avg_expected_return < 0.1", "Rank initiatives on expected return; enforce opportunity cost")
    ]

    def check_failure_modes(self, metrics: Dict[str, float]) -> List[Dict[str, str]]:
        warnings = []
        engagement = metrics.get("engagement", 0.5)
        survey_pos = metrics.get("survey_positive", 0.5)
        build_vel = metrics.get("build_velocity", 0.5)
        demand_sig = metrics.get("demand_signal", 0.5)
        cac = metrics.get("cac", 100.0)
        sales_cycle = metrics.get("sales_cycle_days", 30.0)
        retention_slope = metrics.get("retention_curve_slope", 0.05)
        active_bets = metrics.get("active_bets", 2)
        avg_er = metrics.get("avg_expected_return", 0.3)

        if engagement < 0.2 and survey_pos > 0.8:
            warnings.append({"failure_mode": "Solving the wrong problem", "correction": "5-Whys / Jobs-to-be-Done interviews"})

        if build_vel > 0.8 and demand_sig < 0.2:
            warnings.append({"failure_mode": "Building before validating", "correction": "Enforce validation gate before build resourcing"})

        if cac > 500 and sales_cycle > 90:
            warnings.append({"failure_mode": "Weak positioning", "correction": "Rebuild positioning around real alternative"})

        if retention_slope < 0.01:
            warnings.append({"failure_mode": "Lack of product-market fit", "correction": "Stop scaling; return to cohort retention work"})

        if active_bets > 5 and avg_er < 0.1:
            warnings.append({"failure_mode": "Capital misallocation", "correction": "Rank initiatives on expected return; enforce opportunity cost"})

        return warnings


class EOSKPIStack:
    """Computes and rolls up system KPIs across all 8 EOS operational areas."""

    def compute_kpi_stack(self, raw_data: Dict[str, Any]) -> Dict[str, float]:
        return {
            "sensing_signal_to_noise": float(raw_data.get("valid_signals", 10) / max(1, raw_data.get("total_signals", 20))),
            "validation_cost_per_learning": float(raw_data.get("validation_spend", 5000) / max(1, raw_data.get("learnings_count", 10))),
            "product_activation_rate": float(raw_data.get("activated_users", 80) / max(1, raw_data.get("onboarded_users", 100))),
            "gtm_cac_payback_months": float(raw_data.get("cac", 300) / max(1.0, raw_data.get("arpu_monthly", 50))),
            "financial_burn_multiple": float(raw_data.get("net_burn", 50000) / max(1.0, raw_data.get("net_new_arr", 25000))),
            "org_decision_latency_days": float(raw_data.get("decision_latency_days", 3.5)),
            "strategic_moat_durability_score": float(raw_data.get("moat_score", 0.85)),
            "system_loop_closure_time_days": float(raw_data.get("loop_closure_days", 14.0))
        }
