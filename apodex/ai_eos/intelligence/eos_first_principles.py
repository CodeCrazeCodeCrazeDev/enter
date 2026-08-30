"""First-Principles Entrepreneurial Operating System (EOS) Engine.

Operationalizes the 11-section EOS architecture:
- Master & Cognitive Loops (§1, §2)
- External Business Loops & Coupled Dynamics (§3)
- Full Customer Lifecycle Engine (§4)
- Integrated GTM System Simulator (§5)
- Company Growth Stage Classifier (§6)
- Strategic Thinking & Moat Analyzer (§7)
- Failure Mode Diagnostic Engine (§8)
- AI System State Machine & Opportunity Decision Tree (§10)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Tuple


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


# Valid state transitions as defined in §10.1
VALID_TRANSITIONS: Dict[EOSState, List[EOSState]] = {
    EOSState.SENSING: [EOSState.HYPOTHESIS],
    EOSState.HYPOTHESIS: [EOSState.CHEAP_TEST, EOSState.DISCARD],
    EOSState.CHEAP_TEST: [EOSState.VALIDATION, EOSState.DISCARD],
    EOSState.VALIDATION: [EOSState.BUILD_GATE, EOSState.DISCARD],
    EOSState.BUILD_GATE: [EOSState.MVP, EOSState.DISCARD],
    EOSState.MVP: [EOSState.GTM_TEST, EOSState.DISCARD],
    EOSState.GTM_TEST: [EOSState.KILL_OR_SCALE, EOSState.DISCARD],
    EOSState.KILL_OR_SCALE: [EOSState.SCALE, EOSState.DISCARD],
    EOSState.SCALE: [EOSState.OPERATE, EOSState.DISCARD],
    EOSState.OPERATE: [EOSState.REINVENT, EOSState.DISCARD],
    EOSState.REINVENT: [EOSState.SENSING, EOSState.DISCARD],
    EOSState.DISCARD: [EOSState.SENSING],
}


class EOSStateMachine:
    """System State Machine implementing §10.1."""

    def __init__(self, initial_state: EOSState = EOSState.SENSING) -> None:
        self._current_state: EOSState = initial_state
        self._history: List[Tuple[EOSState, str]] = [(initial_state, "Initial state")]

    @property
    def current_state(self) -> EOSState:
        return self._current_state

    @property
    def history(self) -> List[Tuple[EOSState, str]]:
        return list(self._history)

    def transition_to(self, target_state: EOSState, reason: str = "") -> bool:
        allowed = VALID_TRANSITIONS.get(self._current_state, [])
        if target_state in allowed:
            self._current_state = target_state
            self._history.append((target_state, reason))
            return True
        return False


@dataclass
class OpportunityInput:
    opportunity_id: str
    is_structural_anomaly: bool
    is_reversible: bool  # True = Type II (reversible), False = Type I (irreversible)
    multiple_source_confidence: float = 0.0  # 0.0 to 1.0
    cheap_test_available: bool = True
    test_result_exceeds_kill_threshold: bool = True
    expected_value_positive: bool = True
    has_structural_advantage: bool = True
    market_size_5_10_yr_large: bool = True


@dataclass
class DecisionResult:
    opportunity_id: str
    decision: str  # "COMMIT", "RUN_TEST", or "DISCARD"
    path: List[str]
    reason: str
    recommended_action: str


class OpportunityDecisionTree:
    """Decision Tree implementation for §10.2 ('Should We Pursue This Opportunity?')."""

    def evaluate(self, opp: OpportunityInput) -> DecisionResult:
        path: List[str] = []

        # Q1: Structural anomaly or just noise?
        if not opp.is_structural_anomaly:
            path.append("Q1: Noise -> Discard")
            return DecisionResult(
                opportunity_id=opp.opportunity_id,
                decision="DISCARD",
                path=path,
                reason="Signal classified as noise rather than a structural anomaly.",
                recommended_action="Discard signal and continue environmental sensing."
            )
        path.append("Q1: Structural Anomaly")

        # Q2: Reversible decision?
        if not opp.is_reversible:
            path.append("Q2: Irreversible (Type I risk)")
            # Q2a: High-confidence signal from multiple sources?
            if opp.multiple_source_confidence < 0.7:
                path.append("Q2a: Low confidence -> Discard")
                return DecisionResult(
                    opportunity_id=opp.opportunity_id,
                    decision="DISCARD",
                    path=path,
                    reason="Type I (irreversible) decision lacks high-confidence multi-source signal.",
                    recommended_action="Discard or pause until higher signal confidence is acquired."
                )
            path.append("Q2a: High confidence signal verified")
        else:
            path.append("Q2: Reversible (Type II risk)")

        # Q3: Cheap test available?
        if opp.cheap_test_available:
            path.append("Q3: Cheap test available")
            # Q4: Result exceeds kill threshold?
            if not opp.test_result_exceeds_kill_threshold:
                path.append("Q4: Below kill threshold -> Discard")
                return DecisionResult(
                    opportunity_id=opp.opportunity_id,
                    decision="DISCARD",
                    path=path,
                    reason="Cheap test failed to exceed pre-committed kill threshold.",
                    recommended_action="Discard opportunity per pre-committed kill criteria."
                )
            path.append("Q4: Exceeds kill threshold")
        else:
            path.append("Q3: No cheap test available")
            # Q4b: Expected value clearly positive?
            if not opp.expected_value_positive:
                path.append("Q4b: EV not positive -> Discard")
                return DecisionResult(
                    opportunity_id=opp.opportunity_id,
                    decision="DISCARD",
                    path=path,
                    reason="No cheap test available and expected value is not clearly positive.",
                    recommended_action="Discard opportunity due to negative/uncertain EV."
                )
            path.append("Q4b: Positive EV verified")

        # Q5: Do we have or can we build a structural advantage here?
        if not opp.has_structural_advantage or not opp.market_size_5_10_yr_large:
            path.append("Q5: No structural advantage / small market -> Discard")
            return DecisionResult(
                opportunity_id=opp.opportunity_id,
                decision="DISCARD",
                path=path,
                reason="Lacks defensible structural advantage or 5-10 year market potential.",
                recommended_action="Discard opportunity due to lack of moat/market scale."
            )
        path.append("Q5: Structural advantage confirmed")

        return DecisionResult(
            opportunity_id=opp.opportunity_id,
            decision="COMMIT",
            path=path,
            reason="All criteria passed across anomaly, risk, validation, EV, and structural advantage.",
            recommended_action="Commit capital and resources to build MVP / GTM test."
        )


class CustomerLifecycleStage(str, Enum):
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


@dataclass
class LifecycleMetrics:
    stage_conversions: Dict[CustomerLifecycleStage, float] = field(default_factory=dict)
    time_to_first_value_days: float = 3.0
    activation_rate: float = 0.40
    dau_mau_ratio: float = 0.25
    cohort_retention_flattening: bool = True
    nps_score: float = 45.0
    viral_coefficient_k: float = 0.8
    net_revenue_retention_nrr: float = 1.15
    ltv_to_cac_ratio: float = 3.5


class CustomerLifecycleEngine:
    """Full 15-stage Customer Lifecycle Engine (§4)."""

    STAGES = list(CustomerLifecycleStage)

    def analyze_lifecycle(self, metrics: LifecycleMetrics) -> Dict[str, Any]:
        bottlenecks: List[str] = []

        if metrics.time_to_first_value_days > 7.0:
            bottlenecks.append("Onboarding: Excessive time-to-first-value (>7 days)")
        if metrics.activation_rate < 0.30:
            bottlenecks.append("Activation: Activation rate below 30% threshold")
        if metrics.dau_mau_ratio < 0.15:
            bottlenecks.append("Engagement: DAU/MAU below 15% habit threshold")
        if not metrics.cohort_retention_flattening:
            bottlenecks.append("Retention: Cohort retention curve does not flatten (leaky bucket)")
        if metrics.viral_coefficient_k < 0.5:
            bottlenecks.append("Referral: K-factor below 0.5 organic growth target")
        if metrics.net_revenue_retention_nrr < 1.0:
            bottlenecks.append("Expansion: NRR below 100% (negative net expansion)")

        overall_health = "HEALTHY" if not bottlenecks else ("WARNING" if len(bottlenecks) <= 2 else "CRITICAL")

        return {
            "overall_health": overall_health,
            "bottlenecks": bottlenecks,
            "total_stages_tracked": len(self.STAGES),
            "activation_rate": metrics.activation_rate,
            "nrr": metrics.net_revenue_retention_nrr,
            "k_factor": metrics.viral_coefficient_k,
        }


class GTMChannel(str, Enum):
    ORGANIC = "Organic"
    PAID = "Paid"
    PARTNER = "Partner"
    CONTENT = "Content"
    PLG = "Product-Led Growth"
    SLG = "Sales-Led Growth"
    CLG = "Community-Led Growth"


class GTMMotionConfig:
    def __init__(
        self,
        positioning: str,
        target_segment: str,
        pricing_model: str,  # "self_serve", "usage", "enterprise_tier"
        primary_channel: GTMChannel,
        product_complexity: str = "low",  # "low", "medium", "high"
        contract_value_acv: float = 5000.0,
    ) -> None:
        self.positioning = positioning
        self.target_segment = target_segment
        self.pricing_model = pricing_model
        self.primary_channel = primary_channel
        self.product_complexity = product_complexity
        self.contract_value_acv = contract_value_acv


class GTMSystemSimulator:
    """Integrated Go-to-Market System Simulator (§5)."""

    def evaluate_fit(self, config: GTMMotionConfig) -> Dict[str, Any]:
        mismatches: List[str] = []

        # Channel vs Complexity/Price checks (§5)
        if config.product_complexity == "low" and config.contract_value_acv < 10000:
            if config.primary_channel == GTMChannel.SLG:
                mismatches.append("Channel Mismatch: Sales-Led Growth is inefficient for low-complexity / low-ACV product.")
        elif config.product_complexity == "high" and config.contract_value_acv > 50000:
            if config.primary_channel == GTMChannel.PLG:
                mismatches.append("Channel Mismatch: Pure PLG without enterprise sales is insufficient for high-complexity / high-ACV product.")

        # Pricing vs Segmentation check
        if config.pricing_model == "self_serve" and config.primary_channel == GTMChannel.SLG:
            mismatches.append("Pricing Mismatch: Self-serve pricing conflicts with sales-led high-touch motion.")

        compounding_potentials = []
        if config.primary_channel in (GTMChannel.PLG, GTMChannel.CONTENT):
            compounding_potentials.append("Land via PLG/Content -> Expand via Sales (Slack/Figma pattern)")
        if config.primary_channel == GTMChannel.CLG:
            compounding_potentials.append("Community feeds referral, product feedback, and organic acquisition")

        fit_score = 1.0 - (len(mismatches) * 0.35)
        fit_score = max(0.0, min(1.0, fit_score))

        return {
            "fit_score": fit_score,
            "mismatches": mismatches,
            "compounding_potentials": compounding_potentials,
            "is_viable": len(mismatches) == 0,
        }


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


class CompanyGrowthStageClassifier:
    """Company Growth System Classifier (§6)."""

    STAGES_ORDER = list(CompanyGrowthStage)

    def classify_stage(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        arr = metrics.get("arr", 0.0)
        retention_flattened = metrics.get("retention_flattened", False)
        paying_customers = metrics.get("paying_customers", 0)
        has_ecosystem_devs = metrics.get("third_party_developers", 0) > 50
        cac_payback_months = metrics.get("cac_payback_months", 24.0)

        if arr > 50_000_000 and has_ecosystem_devs:
            stage = CompanyGrowthStage.MARKET_LEADERSHIP
        elif arr > 20_000_000 and has_ecosystem_devs:
            stage = CompanyGrowthStage.ECOSYSTEM
        elif arr > 10_000_000:
            stage = CompanyGrowthStage.PLATFORM
        elif arr > 5_000_000:
            stage = CompanyGrowthStage.SCALE
        elif arr > 1_000_000:
            stage = CompanyGrowthStage.GROWTH
        elif retention_flattened or paying_customers >= 10:
            stage = CompanyGrowthStage.PMF
        elif paying_customers > 0:
            stage = CompanyGrowthStage.STARTUP
        elif metrics.get("validated_learnings", 0) > 3:
            stage = CompanyGrowthStage.VALIDATION
        else:
            stage = CompanyGrowthStage.IDEA

        # Risk check: premature scaling (§6, §8)
        premature_scaling_risk = False
        if stage in (CompanyGrowthStage.GROWTH, CompanyGrowthStage.SCALE) and not retention_flattened:
            premature_scaling_risk = True

        return {
            "current_stage": stage.value,
            "premature_scaling_risk": premature_scaling_risk,
            "binding_constraint": self._get_binding_constraint(stage),
            "primary_objective": self._get_primary_objective(stage),
        }

    def _get_binding_constraint(self, stage: CompanyGrowthStage) -> str:
        constraints = {
            CompanyGrowthStage.IDEA: "Founder time",
            CompanyGrowthStage.VALIDATION: "Signal quality",
            CompanyGrowthStage.STARTUP: "Cash runway",
            CompanyGrowthStage.PMF: "Team bandwidth",
            CompanyGrowthStage.GROWTH: "Hiring velocity, systems",
            CompanyGrowthStage.SCALE: "Org coordination cost",
            CompanyGrowthStage.PLATFORM: "Trust from ecosystem partners",
            CompanyGrowthStage.ECOSYSTEM: "Governance credibility",
            CompanyGrowthStage.MARKET_LEADERSHIP: "Innovation velocity vs. incumbency drag",
        }
        return constraints.get(stage, "Unknown")

    def _get_primary_objective(self, stage: CompanyGrowthStage) -> str:
        objectives = {
            CompanyGrowthStage.IDEA: "Falsify or strengthen hypothesis",
            CompanyGrowthStage.VALIDATION: "Prove willingness to pay",
            CompanyGrowthStage.STARTUP: "Build repeatable acquisition",
            CompanyGrowthStage.PMF: "Reach retention/growth threshold",
            CompanyGrowthStage.GROWTH: "Scale what works",
            CompanyGrowthStage.SCALE: "Institutionalize repeatability",
            CompanyGrowthStage.PLATFORM: "Enable others to build on you",
            CompanyGrowthStage.ECOSYSTEM: "Orchestrate a multi-sided network",
            CompanyGrowthStage.MARKET_LEADERSHIP: "Defend and extend category",
        }
        return objectives.get(stage, "Unknown")


class MoatType(str, Enum):
    NETWORK_EFFECTS = "Network Effects"
    SWITCHING_COSTS = "Switching Costs"
    ECONOMIES_OF_SCALE = "Economies of Scale"
    BRAND = "Brand"
    REGULATORY_IP = "Regulatory/IP"
    COUNTER_POSITIONING = "Counter-Positioning"


class StrategicMoatAnalyzer:
    """Strategic Moat Analyzer (§7)."""

    def analyze_moats(self, moat_scores: Dict[MoatType, float]) -> Dict[str, Any]:
        """moat_scores values range from 0.0 (none) to 1.0 (impregnable)."""
        weighted_score = 0.0
        weights = {
            MoatType.NETWORK_EFFECTS: 0.25,
            MoatType.SWITCHING_COSTS: 0.20,
            MoatType.COUNTER_POSITIONING: 0.20,
            MoatType.ECONOMIES_OF_SCALE: 0.15,
            MoatType.BRAND: 0.10,
            MoatType.REGULATORY_IP: 0.10,
        }

        for moat, weight in weights.items():
            score = moat_scores.get(moat, 0.0)
            weighted_score += score * weight

        durability_rating = "WEAK" if weighted_score < 0.25 else ("MODERATE" if weighted_score < 0.50 else "STRONG")

        return {
            "durability_score": round(weighted_score, 3),
            "durability_rating": durability_rating,
            "strongest_moats": [m.value for m, s in moat_scores.items() if s >= 0.6],
            "vulnerabilities": [m.value for m, s in moat_scores.items() if s < 0.2],
        }


class FailureModeMonitor:
    """Failure Mode Diagnostic Engine (§8)."""

    def audit_operating_metrics(self, metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        detected: List[Dict[str, str]] = []

        # 1. Solving the wrong problem
        if metrics.get("survey_satisfaction", 0.0) > 0.8 and metrics.get("daily_engagement", 0.0) < 0.1:
            detected.append({
                "failure_mode": "Solving the wrong problem",
                "root_cause": "Skipped root-cause analysis; solved a symptom",
                "detection_signal": "Low engagement despite positive survey feedback",
                "correction_mechanism": "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)"
            })

        # 2. Building before validating
        if metrics.get("build_velocity_high", False) and metrics.get("demand_signal_flat", False):
            detected.append({
                "failure_mode": "Building before validating",
                "root_cause": "Founder conviction substituted for evidence",
                "detection_signal": "High build velocity, flat demand signal",
                "correction_mechanism": "Enforce a validation gate before build resourcing"
            })

        # 3. Weak positioning
        if metrics.get("cac", 0.0) > 3000 and metrics.get("sales_cycle_days", 0) > 120 and metrics.get("feature_comparison_objections", False):
            detected.append({
                "failure_mode": "Weak positioning",
                "root_cause": "No clear 'instead of X, use us because Y'",
                "detection_signal": "High CAC, long sales cycles, feature comparison objections",
                "correction_mechanism": "Rebuild positioning around the real alternative customers compare to"
            })

        # 4. Poor pricing
        if metrics.get("conversion_rate", 0.0) > 0.30 and metrics.get("gross_margin", 1.0) < 0.40:
            detected.append({
                "failure_mode": "Poor pricing",
                "root_cause": "Cost-plus instead of value-based pricing",
                "detection_signal": "High conversion at low price, but poor margin/expansion",
                "correction_mechanism": "Re-anchor price to quantified customer value"
            })

        # 5. Distribution failure
        if metrics.get("nps", 0.0) > 60.0 and metrics.get("growth_rate_mom", 0.0) < 0.02:
            detected.append({
                "failure_mode": "Distribution failure",
                "root_cause": "Great product, no repeatable channel",
                "detection_signal": "High NPS, flat growth",
                "correction_mechanism": "Systematically test channels against ICP behavior, not founder preference"
            })

        # 6. Lack of product-market fit
        if metrics.get("scaling_spend", False) and not metrics.get("retention_curve_flattens", False):
            detected.append({
                "failure_mode": "Lack of product-market fit",
                "root_cause": "Premature scaling of an unproven loop",
                "detection_signal": "Retention curve never flattens while scaling",
                "correction_mechanism": "Stop scaling; return to cohort-level retention work"
            })

        # 7. Organizational bottlenecks
        if metrics.get("decision_latency_days", 0) > 14:
            detected.append({
                "failure_mode": "Organizational bottlenecks",
                "root_cause": "Decision rights not delegated as company scales",
                "detection_signal": "Rising decision latency, founder as single point of failure",
                "correction_mechanism": "Push decision rights down with clear frameworks"
            })

        # 8. Capital misallocation
        if metrics.get("underperforming_bets_funded", 0) >= 3:
            detected.append({
                "failure_mode": "Capital misallocation",
                "root_cause": "No opportunity-cost discipline in budgeting",
                "detection_signal": "Multiple underperforming bets funded simultaneously",
                "correction_mechanism": "Rank all initiatives on a common expected-return basis quarterly"
            })

        return detected


class MasterEOSOrchestrator:
    """Master Orchestrator connecting all sub-engines (§1 - §10)."""

    def __init__(self) -> None:
        self.state_machine = EOSStateMachine()
        self.decision_tree = OpportunityDecisionTree()
        self.lifecycle_engine = CustomerLifecycleEngine()
        self.gtm_simulator = GTMSystemSimulator()
        self.growth_classifier = CompanyGrowthStageClassifier()
        self.moat_analyzer = StrategicMoatAnalyzer()
        self.failure_monitor = FailureModeMonitor()

    def process_opportunity(self, opp: OpportunityInput) -> DecisionResult:
        result = self.decision_tree.evaluate(opp)
        if result.decision == "COMMIT":
            if self.state_machine.current_state == EOSState.SENSING:
                self.state_machine.transition_to(EOSState.HYPOTHESIS, "Opportunity anomaly confirmed")
        elif result.decision == "DISCARD":
            self.state_machine.transition_to(EOSState.DISCARD, result.reason)
        return result

    def get_kpi_stack(self, operating_data: Dict[str, Any]) -> Dict[str, Any]:
        """Rolled up KPI Stack (§10.4)."""
        metrics = LifecycleMetrics(
            time_to_first_value_days=operating_data.get("time_to_first_value_days", 3.0),
            activation_rate=operating_data.get("activation_rate", 0.40),
            dau_mau_ratio=operating_data.get("dau_mau_ratio", 0.25),
            cohort_retention_flattening=operating_data.get("retention_flattened", True),
            nps_score=operating_data.get("nps", 45.0),
            viral_coefficient_k=operating_data.get("k_factor", 0.8),
            net_revenue_retention_nrr=operating_data.get("nrr", 1.15),
        )

        lifecycle_analysis = self.lifecycle_engine.analyze_lifecycle(metrics)
        growth_analysis = self.growth_classifier.classify_stage(operating_data)
        failure_diagnostics = self.failure_monitor.audit_operating_metrics(operating_data)

        moat_scores = operating_data.get("moat_scores", {})
        moat_analysis = self.moat_analyzer.analyze_moats(moat_scores)

        return {
            "system_state": self.state_machine.current_state.value,
            "sensing_kpis": {
                "signal_to_noise_ratio": operating_data.get("signal_to_noise_ratio", 0.85),
                "anomaly_detection_lead_time_days": operating_data.get("anomaly_lead_time_days", 5),
            },
            "validation_kpis": {
                "cost_per_validated_learning": operating_data.get("cost_per_learning", 1500.0),
                "false_positive_rate": operating_data.get("false_positive_rate", 0.10),
            },
            "product_kpis": {
                "activation_rate": metrics.activation_rate,
                "retention_curve_slope": operating_data.get("retention_curve_slope", 0.0),
            },
            "gtm_kpis": {
                "cac": operating_data.get("cac", 1200.0),
                "cac_payback_months": operating_data.get("cac_payback_months", 8.5),
            },
            "financial_kpis": {
                "gross_margin": operating_data.get("gross_margin", 0.75),
                "burn_multiple": operating_data.get("burn_multiple", 1.2),
                "runway_months": operating_data.get("runway_months", 24.0),
            },
            "org_kpis": {
                "decision_latency_days": operating_data.get("decision_latency_days", 2),
                "regretted_attrition": operating_data.get("regretted_attrition", 0.02),
            },
            "strategic_kpis": {
                "moat_durability_score": moat_analysis["durability_score"],
                "growth_stage": growth_analysis["current_stage"],
            },
            "system_level_kpis": {
                "loop_closure_time_days": operating_data.get("loop_closure_time_days", 14),
                "detected_failure_modes_count": len(failure_diagnostics),
            },
            "diagnostics": {
                "lifecycle_health": lifecycle_analysis["overall_health"],
                "lifecycle_bottlenecks": lifecycle_analysis["bottlenecks"],
                "premature_scaling_risk": growth_analysis["premature_scaling_risk"],
                "detected_failure_modes": failure_diagnostics,
            }
        }
