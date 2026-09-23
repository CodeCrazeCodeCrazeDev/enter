"""
Entrepreneurial Operating System (EOS) - First-Principles Reconstruction Engine

This module implements the 11-section Entrepreneurial Operating System (EOS) specification,
formalizing sensing, hypothesis testing, loop velocity, customer lifecycle, GTM dynamics,
company growth stages, moat evaluation, failure mode monitoring, and opportunity decision trees.
"""

from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import math


class RiskType(str, Enum):
    TYPE_I = "type_1_irreversible"  # One-way door: high scrutiny, slow deliberation
    TYPE_II = "type_2_reversible"  # Two-way door: rapid, cheap execution


class GrowthStage(str, Enum):
    IDEA = "idea"
    VALIDATION = "validation"
    STARTUP = "startup"
    PMF = "product_market_fit"
    GROWTH = "growth"
    SCALE = "scale"
    PLATFORM = "platform"
    ECOSYSTEM = "ecosystem"
    MARKET_LEADERSHIP = "market_leadership"


class LifecycleStage(str, Enum):
    AWARENESS = "awareness"
    INTEREST = "interest"
    CONSIDERATION = "consideration"
    EVALUATION = "evaluation"
    PURCHASE = "purchase"
    ONBOARDING = "onboarding"
    ACTIVATION = "activation"
    ENGAGEMENT = "engagement"
    HABIT_FORMATION = "habit_formation"
    RETENTION = "retention"
    LOYALTY = "loyalty"
    ADVOCACY = "advocacy"
    REFERRAL = "referral"
    EXPANSION = "expansion"
    REPURCHASE = "repurchase"


class FailureMode(str, Enum):
    SOLVING_WRONG_PROBLEM = "solving_wrong_problem"
    BUILDING_BEFORE_VALIDATING = "building_before_validating"
    WEAK_POSITIONING = "weak_positioning"
    POOR_PRICING = "poor_pricing"
    DISTRIBUTION_FAILURE = "distribution_failure"
    LACK_OF_PMF = "lack_of_pmf"
    ORGANIZATIONAL_BOTTLENECKS = "organizational_bottlenecks"
    FOUNDER_BIAS = "founder_bias"
    SCALING_PREMATURELY = "scaling_prematurely"
    CAPITAL_MISALLOCATION = "capital_misallocation"


@dataclass
class AnomalySignal:
    signal_id: str
    description: str
    is_structural_shift: bool
    observed_magnitude: float
    expected_magnitude: float
    domain: str
    timestamp: str = ""

    @property
    def anomaly_score(self) -> float:
        if self.expected_magnitude == 0:
            return abs(self.observed_magnitude)
        return abs(self.observed_magnitude - self.expected_magnitude) / abs(self.expected_magnitude)


@dataclass
class EOSHypothesis:
    hypothesis_id: str
    falsifiable_claim: str
    risk_type: RiskType
    pre_committed_kill_criteria: str
    cheap_test_description: str
    estimated_test_cost: float
    confidence_score: float = 0.5
    status: str = "formed"  # formed, testing, validated, falsified, discarded
    test_results: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ExternalBusinessLoopState:
    loop_name: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    feedback_signal: float  # scale -1.0 to +1.0
    core_kpis: Dict[str, float]
    failure_mode_flag: Optional[FailureMode] = None


@dataclass
class CustomerLifecycleState:
    stage: LifecycleStage
    founder_objective: str
    customer_psychology: str
    key_metric_value: float
    common_mistake: str
    optimization_lever: str


@dataclass
class GTMStrategyConfig:
    positioning_statement: str
    target_segment: str
    pricing_model: str  # e.g., "value_based", "usage_based", "cost_plus"
    price_point: float
    primary_motion: str  # "PLG", "SLG", "CLG"
    selected_channels: List[str]
    cac: float = 0.0
    conversion_rate: float = 0.0


@dataclass
class StrategicMoatProfile:
    network_effects_score: float = 0.0  # 0.0 to 1.0
    switching_costs_score: float = 0.0
    economies_of_scale_score: float = 0.0
    brand_trust_score: float = 0.0
    counter_positioning_score: float = 0.0
    regulatory_ip_score: float = 0.0

    @property
    def overall_moat_durability(self) -> float:
        scores = [
            self.network_effects_score,
            self.switching_costs_score,
            self.economies_of_scale_score,
            self.brand_trust_score,
            self.counter_positioning_score,
            self.regulatory_ip_score,
        ]
        return sum(scores) / len(scores)


class AnomaliesAndSensingEngine:
    """Implements §1–2: Environmental sensing, anomaly detection & signal-to-idea pipeline."""

    def __init__(self):
        self.detected_anomalies: List[AnomalySignal] = []
        self.active_hypotheses: List[EOSHypothesis] = []

    def evaluate_signal(self, signal: AnomalySignal) -> Optional[EOSHypothesis]:
        self.detected_anomalies.append(signal)
        if not signal.is_structural_shift or signal.anomaly_score < 0.2:
            return None  # Discard noise or non-structural signals

        # Forced hypothesis generation
        risk_type = RiskType.TYPE_I if signal.domain in ["regulatory", "safety", "core_architecture"] else RiskType.TYPE_II
        hypothesis = EOSHypothesis(
            hypothesis_id=f"hyp_{len(self.active_hypotheses)+1:03d}",
            falsifiable_claim=f"Structural shift in {signal.domain} enables viable opportunity: {signal.description}",
            risk_type=risk_type,
            pre_committed_kill_criteria="Target metric fails to exceed baseline by >= 25% in cheap test",
            cheap_test_description=f"Run small-scale market test in {signal.domain}",
            estimated_test_cost=500.0 if risk_type == RiskType.TYPE_II else 5000.0,
        )
        self.active_hypotheses.append(hypothesis)
        return hypothesis

    def run_cheap_test(self, hypothesis_id: str, test_outcome_metric: float, baseline_metric: float) -> str:
        hyp = next((h for h in self.active_hypotheses if h.hypothesis_id == hypothesis_id), None)
        if not hyp:
            raise ValueError(f"Hypothesis {hypothesis_id} not found")

        delta = (test_outcome_metric - baseline_metric) / (baseline_metric if baseline_metric > 0 else 1.0)
        hyp.test_results.append({"test_metric": test_outcome_metric, "baseline": baseline_metric, "delta": delta})

        if delta >= 0.25:
            hyp.status = "validated"
            hyp.confidence_score = min(1.0, hyp.confidence_score + 0.35)
        else:
            hyp.status = "falsified"
            hyp.confidence_score = max(0.0, hyp.confidence_score - 0.4)

        return hyp.status


class ExternalBusinessLoopsEngine:
    """Implements §3: External Business Loops & System Coupling."""

    def __init__(self):
        self.loops: Dict[str, ExternalBusinessLoopState] = {}
        self._initialize_default_loops()

    def _initialize_default_loops(self):
        default_loops = [
            ("Product", {"retention_curve": 0.4, "nps": 50.0, "feature_adoption": 0.6}),
            ("Marketing", {"cac": 120.0, "brand_recall": 0.3, "conversion_rate": 0.05}),
            ("Sales", {"win_rate": 0.25, "sales_cycle_days": 45.0, "acv": 12000.0}),
            ("Customer Success", {"nrr": 1.15, "churn_rate": 0.02, "time_to_value_days": 14.0}),
            ("Brand", {"share_of_voice": 0.15, "price_elasticity": -0.8}),
            ("Pricing", {"arpu": 100.0, "price_realization": 0.9, "elasticity": -1.1}),
            ("Referral", {"viral_coefficient": 0.3, "referral_cac": 20.0}),
            ("Data", {"data_latency_hours": 1.0, "decision_cycle_days": 3.0}),
            ("Financial", {"gross_margin": 0.75, "burn_multiple": 1.5, "runway_months": 18.0}),
            ("Hiring", {"time_to_fill_days": 30.0, "quality_of_hire": 0.85, "retention_rate": 0.9}),
            ("Culture", {"enps": 45.0, "decision_latency_days": 2.0}),
            ("Innovation", {"experiments_run": 12.0, "hit_rate": 0.25, "time_to_signal_days": 7.0}),
            ("Competitive Intelligence", {"relative_share": 0.2, "feature_parity_gap": 0.1}),
        ]
        for name, kpis in default_loops:
            self.loops[name] = ExternalBusinessLoopState(
                loop_name=name,
                inputs={"raw_signal": "active"},
                outputs={"system_value": 1.0},
                feedback_signal=0.5,
                core_kpis=kpis,
            )

    def evaluate_loop_coupling(self) -> Dict[str, Any]:
        """Calculates system coupling effects across stocks and flows."""
        arpu = self.loops["Pricing"].core_kpis.get("arpu", 100.0)
        gross_margin = self.loops["Financial"].core_kpis.get("gross_margin", 0.75)
        runway = self.loops["Financial"].core_kpis.get("runway_months", 18.0)

        # ARPU & Gross Margin determine hiring capacity
        hiring_budget_score = (arpu * gross_margin) / 100.0
        time_to_fill = self.loops["Hiring"].core_kpis.get("time_to_fill_days", 30.0)

        # Hiring velocity feeds Product loop velocity
        product_velocity = (100.0 / time_to_fill) * hiring_budget_score

        return {
            "hiring_capacity_score": hiring_budget_score,
            "product_velocity_index": product_velocity,
            "runway_months": runway,
            "financial_health": "strong" if gross_margin >= 0.7 and runway >= 12 else "constrained",
        }


class CustomerLifecycleEngine:
    """Implements §4: Customer Journey Lifecycle."""

    LIFECYCLE_MAPPING = {
        LifecycleStage.AWARENESS: ("Enter consideration set", "Pattern-matching against known categories", "Reach, unaided recall", "Generic category messaging", "Sharp category framing / naming a new category"),
        LifecycleStage.INTEREST: ("Earn attention", "Curiosity vs. skepticism", "CTR, engagement rate", "Feature-dumping", "Lead with the pain, not the product"),
        LifecycleStage.CONSIDERATION: ("Differentiate", "Comparing against status quo & alternatives", "Time-on-site, content depth", "Competing on features competitors also have", "Reframe the comparison axis"),
        LifecycleStage.EVALUATION: ("Reduce perceived risk", "Loss aversion dominates gain-seeking", "Trial starts, demo requests", "Ignoring risk-reduction (guarantees, trials)", "Make failure cheap and reversible"),
        LifecycleStage.PURCHASE: ("Convert intent to commitment", "Decision fatigue, need for certainty", "Conversion rate", "Friction in checkout/contracting", "Remove steps, not add persuasion"),
        LifecycleStage.ONBOARDING: ("Deliver first value fast", "Anxiety about wasted decision", "Time-to-first-value", "Feature-tour instead of outcome-tour", "Anchor onboarding to specific JTBD"),
        LifecycleStage.ACTIVATION: ("Cross the 'aha' threshold", "Forming initial habit loop", "Activation rate", "Defining activation as login, not value", "Instrument true 'aha' moment via cohort analysis"),
        LifecycleStage.ENGAGEMENT: ("Build usage depth", "Reinforcement learning (reward loop)", "DAU/MAU, session depth", "Engagement metrics not correlating with retention", "Optimize for behavior predicting retention"),
        LifecycleStage.HABIT_FORMATION: ("Make usage automatic", "Cue-routine-reward loop", "Habit strength / frequency", "No external trigger cadence", "Build reliable internal + external triggers"),
        LifecycleStage.RETENTION: ("Prevent churn", "Switching cost perception, sunk value", "Retention curve, churn", "Measuring retention only in aggregate", "Cohort-level retention curves & flattening point analysis"),
        LifecycleStage.LOYALTY: ("Deepen emotional/economic lock-in", "Identity alignment with brand", "Repeat purchase rate", "Assuming satisfaction = loyalty", "Build genuine switching costs"),
        LifecycleStage.ADVOCACY: ("Convert satisfaction to voice", "Social proof-seeking, reciprocity", "NPS, UGC volume", "Asking for advocacy before value is proven", "Ask at peak-value moments"),
        LifecycleStage.REFERRAL: ("Convert advocacy to acquisition", "Trust transfer peer-to-peer", "Viral coefficient (K)", "Generic referral programs", "Incentive aligned with genuine value"),
        LifecycleStage.EXPANSION: ("Grow account value", "Anchoring to current spend", "Net revenue retention (NRR)", "Under-selling adjacent value", "Usage-based expansion triggers"),
        LifecycleStage.REPURCHASE: ("Sustain lifetime value", "Habitual trust, low re-evaluation cost", "LTV, repurchase rate", "Treating repurchase as passive", "Proactive lifecycle marketing tied to usage signals"),
    }

    def get_stage_details(self, stage: LifecycleStage, current_metric_val: float = 0.0) -> CustomerLifecycleState:
        obj, psych, metric_name, mistake, lever = self.LIFECYCLE_MAPPING[stage]
        return CustomerLifecycleState(
            stage=stage,
            founder_objective=obj,
            customer_psychology=psych,
            key_metric_value=current_metric_val,
            common_mistake=mistake,
            optimization_lever=lever,
        )


class GTMSystemSimulator:
    """Implements §5: Go-to-Market System as an Integrated System."""

    def evaluate_gtm_fit(self, config: GTMStrategyConfig) -> Dict[str, Any]:
        # Upstream positioning check
        positioning_valid = len(config.positioning_statement.strip()) > 20

        # Channel fit rule: low price / self-serve -> PLG; high price -> SLG
        recommended_motion = "PLG" if config.price_point < 1000.0 else "SLG"
        motion_aligned = config.primary_motion == recommended_motion

        # Pricing signal check
        if config.pricing_model == "cost_plus":
            pricing_recommendation = "Switch to value-based or usage-based pricing to capture upside"
        else:
            pricing_recommendation = "Pricing model aligned with value proposition"

        # Compounding motions score
        compounding_score = len(config.selected_channels) * 0.25 if len(config.selected_channels) <= 4 else 1.0

        return {
            "positioning_valid": positioning_valid,
            "recommended_motion": recommended_motion,
            "motion_aligned": motion_aligned,
            "pricing_recommendation": pricing_recommendation,
            "compounding_score": compounding_score,
            "gtm_readiness_score": (0.4 if positioning_valid else 0.0) + (0.4 if motion_aligned else 0.0) + (0.2 * compounding_score),
        }


class CompanyGrowthStateMachine:
    """Implements §6: Company Growth System (8 stages & stage transitions)."""

    STAGE_ORDER = [
        GrowthStage.IDEA,
        GrowthStage.VALIDATION,
        GrowthStage.STARTUP,
        GrowthStage.PMF,
        GrowthStage.GROWTH,
        GrowthStage.SCALE,
        GrowthStage.PLATFORM,
        GrowthStage.ECOSYSTEM,
        GrowthStage.MARKET_LEADERSHIP,
    ]

    STAGE_CONSTRAINTS = {
        GrowthStage.IDEA: ("Falsify or strengthen hypothesis", "Founder time", "# of validated learnings"),
        GrowthStage.VALIDATION: ("Prove willingness to pay", "Signal quality", "Paying customers / LOIs"),
        GrowthStage.STARTUP: ("Build repeatable acquisition", "Cash runway", "CAC:LTV early signal"),
        GrowthStage.PMF: ("Reach retention/growth threshold", "Team bandwidth", "Retention curve flattening"),
        GrowthStage.GROWTH: ("Scale what works", "Hiring velocity, systems", "Growth rate, CAC payback"),
        GrowthStage.SCALE: ("Institutionalize repeatability", "Org coordination cost", "Rule of 40, NRR"),
        GrowthStage.PLATFORM: ("Enable others to build on you", "Trust from ecosystem partners", "Third-party developer activity"),
        GrowthStage.ECOSYSTEM: ("Orchestrate a multi-sided network", "Governance credibility", "Ecosystem GMV / network density"),
        GrowthStage.MARKET_LEADERSHIP: ("Defend and extend category", "Innovation velocity vs. incumbency drag", "Category share, moat durability"),
    }

    def __init__(self, initial_stage: GrowthStage = GrowthStage.IDEA):
        self.current_stage = initial_stage

    def can_transition_next(self, key_metric_value: float, metric_threshold: float) -> Tuple[bool, str]:
        if key_metric_value >= metric_threshold:
            curr_idx = self.STAGE_ORDER.index(self.current_stage)
            if curr_idx < len(self.STAGE_ORDER) - 1:
                next_stage = self.STAGE_ORDER[curr_idx + 1]
                return True, f"Ready to transition from {self.current_stage.value} to {next_stage.value}"
            return False, "Already at final Market Leadership stage"

        curr_obj, constraint, metric_name = self.STAGE_CONSTRAINTS[self.current_stage]
        return False, f"Cannot transition from {self.current_stage.value}: {metric_name} ({key_metric_value}) below threshold ({metric_threshold}). Binding constraint: {constraint}"

    def transition(self, key_metric_value: float, metric_threshold: float) -> GrowthStage:
        allowed, msg = self.can_transition_next(key_metric_value, metric_threshold)
        if allowed:
            curr_idx = self.STAGE_ORDER.index(self.current_stage)
            self.current_stage = self.STAGE_ORDER[curr_idx + 1]
        return self.current_stage


class StrategicMoatEngine:
    """Implements §7: Strategic Thinking & Moat Construction."""

    def evaluate_cost_curve_viability(self, baseline_cost: float, annual_decay_rate: float, years: int, target_threshold: float) -> Dict[str, Any]:
        projected_cost = baseline_cost * ((1.0 - annual_decay_rate) ** years)
        is_viable = projected_cost <= target_threshold
        return {
            "baseline_cost": baseline_cost,
            "projected_cost": projected_cost,
            "target_threshold": target_threshold,
            "is_commercially_viable": is_viable,
            "crossing_year": self._calculate_crossing_year(baseline_cost, annual_decay_rate, target_threshold),
        }

    def _calculate_crossing_year(self, baseline: float, decay_rate: float, threshold: float) -> Optional[int]:
        if baseline <= threshold:
            return 0
        if decay_rate <= 0 or decay_rate >= 1:
            return None
        years = math.log(threshold / baseline) / math.log(1.0 - decay_rate)
        return math.ceil(years)

    def calculate_moat_durability(self, profile: StrategicMoatProfile) -> float:
        return profile.overall_moat_durability


class FailureModeMonitor:
    """Implements §8: Failure Mode Analysis & Diagnostics."""

    FAILURE_MAP = {
        FailureMode.SOLVING_WRONG_PROBLEM: ("Low engagement despite positive survey feedback", "Return to root-cause (5-Whys / Jobs-to-be-Done)"),
        FailureMode.BUILDING_BEFORE_VALIDATING: ("High build velocity, flat demand signal", "Enforce a validation gate before build resourcing"),
        FailureMode.WEAK_POSITIONING: ("High CAC, long sales cycles, feature comparison objections", "Rebuild positioning around real alternative customers compare to"),
        FailureMode.POOR_PRICING: ("High conversion at low price, but poor margin/expansion", "Re-anchor price to quantified customer value"),
        FailureMode.DISTRIBUTION_FAILURE: ("High NPS, flat growth", "Systematically test channels against ICP behavior"),
        FailureMode.LACK_OF_PMF: ("Retention curve never flattens", "Stop scaling; return to cohort-level retention work"),
        FailureMode.ORGANIZATIONAL_BOTTLENECKS: ("Rising decision latency, founder single point of failure", "Push decision rights down with clear frameworks"),
        FailureMode.FOUNDER_BIAS: ("Ignoring disconfirming data, 'just needs more time' pattern", "Enforce pre-committed kill criteria set before launch"),
        FailureMode.SCALING_PREMATURELY: ("CAC rising faster than LTV as spend scales", "Re-test unit economics at each order-of-magnitude spend"),
        FailureMode.CAPITAL_MISALLOCATION: ("Multiple underperforming bets funded simultaneously", "Rank all initiatives on common expected-return basis quarterly"),
    }

    def diagnose_operational_metrics(self, metrics: Dict[str, float]) -> List[Dict[str, str]]:
        warnings = []

        if metrics.get("survey_satisfaction", 0.0) > 0.8 and metrics.get("daily_engagement", 1.0) < 0.2:
            signal, fix = self.FAILURE_MAP[FailureMode.SOLVING_WRONG_PROBLEM]
            warnings.append({"failure_mode": FailureMode.SOLVING_WRONG_PROBLEM.value, "signal": signal, "correction": fix})

        if metrics.get("retention_curve_flattened", 1.0) == 0.0 and metrics.get("marketing_spend", 0.0) > 10000.0:
            signal, fix = self.FAILURE_MAP[FailureMode.LACK_OF_PMF]
            warnings.append({"failure_mode": FailureMode.LACK_OF_PMF.value, "signal": signal, "correction": fix})

        if metrics.get("cac", 0.0) > 3.0 * metrics.get("arpu", 1.0) and metrics.get("sales_cycle_days", 0.0) > 60:
            signal, fix = self.FAILURE_MAP[FailureMode.WEAK_POSITIONING]
            warnings.append({"failure_mode": FailureMode.WEAK_POSITIONING.value, "signal": signal, "correction": fix})

        if metrics.get("burn_multiple", 0.0) > 3.0 and metrics.get("growth_rate", 0.0) < 0.1:
            signal, fix = self.FAILURE_MAP[FailureMode.CAPITAL_MISALLOCATION]
            warnings.append({"failure_mode": FailureMode.CAPITAL_MISALLOCATION.value, "signal": signal, "correction": fix})

        return warnings


class EOSOpportunityDecisionTree:
    """Implements §10.2: Executable Decision Tree - 'Should We Pursue This Opportunity?'."""

    def evaluate_opportunity(
        self,
        is_structural_anomaly: bool,
        is_reversible_decision: bool,
        high_confidence_multi_source_signal: bool,
        cheap_test_available: bool,
        cheap_test_result_exceeds_kill_threshold: bool,
        expected_value_clearly_positive: bool,
        has_or_can_build_structural_advantage: bool,
    ) -> Tuple[bool, str]:
        # Step 1: Anomaly check
        if not is_structural_anomaly:
            return False, "Discard: Signal is noise, not a structural anomaly."

        # Step 2: Risk / Reversibility check
        if not is_reversible_decision:
            if not high_confidence_multi_source_signal:
                return False, "Discard: Irreversible decision (Type I) lacks high-confidence multi-source signal."

        # Step 3: Testability / EV check
        if cheap_test_available:
            if not cheap_test_result_exceeds_kill_threshold:
                return False, "Discard: Cheap test result failed to exceed pre-committed kill threshold."
        else:
            if not expected_value_clearly_positive:
                return False, "Discard: No cheap test available and Expected Value is not clearly positive."

        # Step 4: Structural Advantage check
        if not has_or_can_build_structural_advantage:
            return False, "Discard: Lacks defensible structural advantage / moat."

        return True, "Commit Resources: Opportunity satisfies all decision criteria."


class EOSEngineFirstPrinciples:
    """
    Top-Level Master Orchestrator for the Entrepreneurial Operating System (EOS).
    Integrates Sensing, Hypothesis Testing, Business Loops, Customer Lifecycle, GTM,
    Growth State Machine, Moats, Failure Diagnostics, Decision Tree, and KPI Stack Rollup.
    """

    def __init__(self, initial_stage: GrowthStage = GrowthStage.IDEA):
        self.sensing = AnomaliesAndSensingEngine()
        self.loops = ExternalBusinessLoopsEngine()
        self.lifecycle = CustomerLifecycleEngine()
        self.gtm = GTMSystemSimulator()
        self.growth_machine = CompanyGrowthStateMachine(initial_stage)
        self.moats = StrategicMoatEngine()
        self.failure_monitor = FailureModeMonitor()
        self.decision_tree = EOSOpportunityDecisionTree()

    def process_anomaly_and_decide(
        self,
        signal: AnomalySignal,
        cheap_test_metric: float,
        baseline_metric: float,
        has_moat_advantage: bool,
    ) -> Dict[str, Any]:
        """Runs the Master Loop from Sensing to Opportunity Decision."""
        hypothesis = self.sensing.evaluate_signal(signal)
        if not hypothesis:
            return {"action": "discard", "reason": "Signal discarded as non-structural noise"}

        test_status = self.sensing.run_cheap_test(hypothesis.hypothesis_id, cheap_test_metric, baseline_metric)
        test_passed = test_status == "validated"

        pursue, reason = self.decision_tree.evaluate_opportunity(
            is_structural_anomaly=signal.is_structural_shift,
            is_reversible_decision=(hypothesis.risk_type == RiskType.TYPE_II),
            high_confidence_multi_source_signal=True,
            cheap_test_available=True,
            cheap_test_result_exceeds_kill_threshold=test_passed,
            expected_value_clearly_positive=test_passed,
            has_or_can_build_structural_advantage=has_moat_advantage,
        )

        return {
            "hypothesis_id": hypothesis.hypothesis_id,
            "falsifiable_claim": hypothesis.falsifiable_claim,
            "test_status": test_status,
            "pursue_decision": pursue,
            "decision_reason": reason,
        }

    def get_rolled_up_kpi_stack(self) -> Dict[str, Dict[str, float]]:
        """Implements §10.4: KPI Stack (Rolled Up by Subsystem)."""
        return {
            "sensing": {
                "signal_to_noise_ratio": 0.82,
                "anomaly_detection_lead_time_days": 14.0,
            },
            "validation": {
                "cost_per_validated_learning": 350.0,
                "false_positive_rate": 0.08,
            },
            "product": {
                "activation_rate": self.loops.loops["Product"].core_kpis.get("feature_adoption", 0.6),
                "retention_curve_slope": self.loops.loops["Product"].core_kpis.get("retention_curve", 0.4),
            },
            "gtm": {
                "cac": self.loops.loops["Marketing"].core_kpis.get("cac", 120.0),
                "cac_payback_months": 8.5,
            },
            "financial": {
                "gross_margin": self.loops.loops["Financial"].core_kpis.get("gross_margin", 0.75),
                "burn_multiple": self.loops.loops["Financial"].core_kpis.get("burn_multiple", 1.5),
                "runway_months": self.loops.loops["Financial"].core_kpis.get("runway_months", 18.0),
            },
            "org": {
                "decision_latency_days": self.loops.loops["Culture"].core_kpis.get("decision_latency_days", 2.0),
                "regretted_attrition_rate": 0.05,
            },
            "strategic": {
                "relative_market_share": self.loops.loops["Competitive Intelligence"].core_kpis.get("relative_share", 0.2),
                "moat_durability_score": 0.78,
            },
            "system_level": {
                "overall_loop_closure_time_days": 5.2,
            },
        }
