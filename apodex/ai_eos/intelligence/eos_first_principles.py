"""Entrepreneurial Operating System (EOS) First-Principles Engine.

Code-formalization of how elite founders sense, build, and compound enduring companies,
as specified in the authoritative EOS specification.
"""

from __future__ import annotations
import uuid
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Set
from pydantic import BaseModel, Field

logger = logging.getLogger("ai_eos.eos_first_principles")


class Timescale(str, Enum):
    FAST = "FAST"        # Days - Weeks
    MEDIUM = "MEDIUM"    # Months - Quarters
    SLOW = "SLOW"        # Years


class RiskType(str, Enum):
    TYPE_I = "TYPE_I"    # Irreversible, high-scrutiny, slow deliberation
    TYPE_II = "TYPE_II"  # Reversible, fast, cheap to execute


class EOSState(str, Enum):
    SENSING = "SENSING"
    HYPOTHESIS = "HYPOTHESIS"
    CHEAP_TEST = "CHEAP_TEST"
    VALIDATION = "VALIDATION"
    BUILD_GATE = "BUILD_GATE"
    MVP = "MVP"
    GTM_TEST = "GTM_TEST"
    KILL_OR_SCALE = "KILL_OR_SCALE"
    SCALE = "SCALE"
    OPERATE = "OPERATE"
    REINVENT = "REINVENT"
    DISCARDED = "DISCARDED"


class WeakSignal(BaseModel):
    signal_id: str = Field(default_factory=lambda: f"sig_{uuid.uuid4().hex[:8]}")
    description: str
    is_anomaly: bool = False  # Over-indexing on anomalies that mismatch mental models
    source: str
    strength: float = 0.5     # 0.0 to 1.0


class Hypothesis(BaseModel):
    hypothesis_id: str = Field(default_factory=lambda: f"hyp_{uuid.uuid4().hex[:8]}")
    claim: str
    is_falsifiable: bool = True
    pre_committed_kill_criteria: str
    prior_confidence: float = 0.5
    posterior_confidence: float = 0.5


class BusinessLoopDef(BaseModel):
    name: str
    inputs: List[str]
    outputs: List[str]
    feedback_signal: str
    core_kpis: List[str]
    dominant_failure_mode: str


class CustomerJourneyStageDef(BaseModel):
    stage_name: str
    founder_objective: str
    customer_psychology: str
    key_metric: str
    common_mistake: str
    optimization_lever: str


class CompanyGrowthStageDef(BaseModel):
    stage_name: str
    primary_objective: str
    org_change: str
    decision_making_change: str
    capital_allocation: str
    key_risk: str
    core_metric: str
    binding_constraint: str


class StrategicMoat(BaseModel):
    moat_type: str  # Network Effects, Switching Costs, Economies of Scale, Brand, Regulatory, Counter-Positioning
    description: str
    durability_score: float = 0.5  # 0.0 to 1.0


# ------------------------------------------------------------------
# Business Loops Database & Coupling Registry
# ------------------------------------------------------------------
EXTERNAL_BUSINESS_LOOPS: Dict[str, BusinessLoopDef] = {
    "Product": BusinessLoopDef(
        name="Product",
        inputs=["User behavior", "support tickets", "usage data"],
        outputs=["Feature changes", "roadmap"],
        feedback_signal="Activation/retention deltas",
        core_kpis=["Retention curve", "NPS", "feature adoption"],
        dominant_failure_mode="Building for the loudest customer, not the representative one"
    ),
    "Marketing": BusinessLoopDef(
        name="Marketing",
        inputs=["Positioning", "market data"],
        outputs=["Awareness", "demand"],
        feedback_signal="CAC, traffic quality, message resonance",
        core_kpis=["CAC", "brand recall", "conversion rate"],
        dominant_failure_mode="Message-market mismatch; scaling spend before message works"
    ),
    "Sales": BusinessLoopDef(
        name="Sales",
        inputs=["Qualified leads", "product"],
        outputs=["Closed revenue", "customer feedback"],
        feedback_signal="Win/loss reasons",
        core_kpis=["Win rate", "sales cycle length", "ACV"],
        dominant_failure_mode="Selling to non-ICP to hit quota"
    ),
    "Customer Success": BusinessLoopDef(
        name="Customer Success",
        inputs=["Onboarding data", "usage"],
        outputs=["Retention", "expansion"],
        feedback_signal="Churn reasons, health scores",
        core_kpis=["NRR", "churn rate", "time-to-value"],
        dominant_failure_mode="Success != support; reactive-only CS"
    ),
    "Brand": BusinessLoopDef(
        name="Brand",
        inputs=["Product experience", "comms"],
        outputs=["Trust", "pricing power"],
        feedback_signal="Sentiment, unaided recall",
        core_kpis=["Share of voice", "price elasticity"],
        dominant_failure_mode="Brand as decoration, not strategy"
    ),
    "Pricing": BusinessLoopDef(
        name="Pricing",
        inputs=["Value delivered", "WTP data"],
        outputs=["Revenue", "positioning signal"],
        feedback_signal="Conversion by price point, expansion rate",
        core_kpis=["ARPU", "price realization", "elasticity"],
        dominant_failure_mode="Cost-plus pricing instead of value-based"
    ),
    "Referral": BusinessLoopDef(
        name="Referral",
        inputs=["Customer satisfaction", "incentive design"],
        outputs=["New customer flow"],
        feedback_signal="Referral rate, K-factor",
        core_kpis=["Viral coefficient", "referral CAC"],
        dominant_failure_mode="Incentivizing referral volume over referral quality"
    ),
    "Data": BusinessLoopDef(
        name="Data",
        inputs=["All business activity"],
        outputs=["Decisions"],
        feedback_signal="Model accuracy vs. outcomes",
        core_kpis=["Data latency", "decision cycle time"],
        dominant_failure_mode="Vanity metrics; dashboards no one acts on"
    ),
    "Financial": BusinessLoopDef(
        name="Financial",
        inputs=["Revenue", "costs", "capital"],
        outputs=["Runway", "reinvestment capacity"],
        feedback_signal="Burn multiple, margin trend",
        core_kpis=["Gross margin", "burn multiple", "runway"],
        dominant_failure_mode="Growth at negative unit economics with no path to positive"
    ),
    "Hiring": BusinessLoopDef(
        name="Hiring",
        inputs=["Org needs", "culture"],
        outputs=["Capability", "capacity"],
        feedback_signal="90-day performance, regretted attrition",
        core_kpis=["Time-to-fill", "quality of hire", "retention"],
        dominant_failure_mode="Hiring for pedigree over role-fit; hiring ahead of proven need"
    ),
    "Culture": BusinessLoopDef(
        name="Culture",
        inputs=["Values-in-action", "incentives"],
        outputs=["Behavior consistency at scale"],
        feedback_signal="Employee sentiment, decision speed",
        core_kpis=["eNPS", "decision latency"],
        dominant_failure_mode="Values-as-poster (stated but not incentivized)"
    ),
    "Innovation": BusinessLoopDef(
        name="Innovation",
        inputs=["R&D", "market signals", "internal ideas"],
        outputs=["New products/features/lines"],
        feedback_signal="Time-to-market, cannibalization rate",
        core_kpis=["# experiments run", "hit rate", "time-to-signal"],
        dominant_failure_mode="Innovation theater — activity without shipped bets"
    ),
    "Competitive Intelligence": BusinessLoopDef(
        name="Competitive Intelligence",
        inputs=["Market/competitor data"],
        outputs=["Strategic repositioning"],
        feedback_signal="Win/loss vs. named competitors",
        core_kpis=["Relative share trend", "feature parity gap"],
        dominant_failure_mode="Reacting to competitors instead of running own strategy"
    )
}

# ------------------------------------------------------------------
# Customer Journey Lifecycle Database
# ------------------------------------------------------------------
CUSTOMER_JOURNEY_STAGES: Dict[str, CustomerJourneyStageDef] = {
    "Awareness": CustomerJourneyStageDef(
        stage_name="Awareness",
        founder_objective="Enter consideration set",
        customer_psychology="Pattern-matching against known categories",
        key_metric="Reach, unaided recall",
        common_mistake="Generic category messaging",
        optimization_lever="Sharp category framing / naming a new category"
    ),
    "Interest": CustomerJourneyStageDef(
        stage_name="Interest",
        founder_objective="Earn attention",
        customer_psychology="Curiosity vs. skepticism",
        key_metric="CTR, engagement rate",
        common_mistake="Feature-dumping",
        optimization_lever="Lead with the pain, not the product"
    ),
    "Consideration": CustomerJourneyStageDef(
        stage_name="Consideration",
        founder_objective="Differentiate",
        customer_psychology="Comparing against status quo & alternatives",
        key_metric="Time-on-site, content depth",
        common_mistake="Competing on features competitors also have",
        optimization_lever="Reframe the comparison axis"
    ),
    "Evaluation": CustomerJourneyStageDef(
        stage_name="Evaluation",
        founder_objective="Reduce perceived risk",
        customer_psychology="Loss aversion dominates gain-seeking",
        key_metric="Trial starts, demo requests",
        common_mistake="Ignoring risk-reduction (guarantees, trials)",
        optimization_lever="Make failure cheap and reversible"
    ),
    "Purchase": CustomerJourneyStageDef(
        stage_name="Purchase",
        founder_objective="Convert intent to commitment",
        customer_psychology="Decision fatigue, need for certainty",
        key_metric="Conversion rate",
        common_mistake="Friction in checkout/contracting",
        optimization_lever="Remove steps, not add persuasion"
    ),
    "Onboarding": CustomerJourneyStageDef(
        stage_name="Onboarding",
        founder_objective="Deliver first value fast",
        customer_psychology="Anxiety about wasted decision",
        key_metric="Time-to-first-value",
        common_mistake="Feature-tour instead of outcome-tour",
        optimization_lever="Anchor onboarding to the customer's specific job-to-be-done"
    ),
    "Activation": CustomerJourneyStageDef(
        stage_name="Activation",
        founder_objective="Cross the 'aha' threshold",
        customer_psychology="Forming initial habit loop",
        key_metric="Activation rate",
        common_mistake="Defining activation as login, not value",
        optimization_lever="Instrument the true 'aha' moment via cohort analysis"
    ),
    "Engagement": CustomerJourneyStageDef(
        stage_name="Engagement",
        founder_objective="Build usage depth",
        customer_psychology="Reinforcement learning (reward loop)",
        key_metric="DAU/MAU, session depth",
        common_mistake="Engagement metrics that don't correlate with retention",
        optimization_lever="Optimize for the behavior that predicts retention, not raw activity"
    ),
    "Habit Formation": CustomerJourneyStageDef(
        stage_name="Habit Formation",
        founder_objective="Make usage automatic",
        customer_psychology="Cue-routine-reward loop",
        key_metric="Habit strength / frequency",
        common_mistake="No external trigger cadence",
        optimization_lever="Build reliable internal + external triggers"
    ),
    "Retention": CustomerJourneyStageDef(
        stage_name="Retention",
        founder_objective="Prevent churn",
        customer_psychology="Switching cost perception, sunk value",
        key_metric="Retention curve, churn",
        common_mistake="Measuring retention only in aggregate, not cohort",
        optimization_lever="Cohort-level retention curves, flattening point analysis"
    ),
    "Loyalty": CustomerJourneyStageDef(
        stage_name="Loyalty",
        founder_objective="Deepen emotional/economic lock-in",
        customer_psychology="Identity alignment with brand",
        key_metric="Repeat purchase rate",
        common_mistake="Assuming satisfaction = loyalty",
        optimization_lever="Build genuine switching costs (data, workflow, community)"
    ),
    "Advocacy": CustomerJourneyStageDef(
        stage_name="Advocacy",
        founder_objective="Convert satisfaction to voice",
        customer_psychology="Social proof-seeking, reciprocity",
        key_metric="NPS, UGC volume",
        common_mistake="Asking for advocacy before value is proven",
        optimization_lever="Ask at peak-value moments"
    ),
    "Referral": CustomerJourneyStageDef(
        stage_name="Referral",
        founder_objective="Convert advocacy to acquisition",
        customer_psychology="Trust transfer from peer to peer",
        key_metric="Viral coefficient (K)",
        common_mistake="Generic referral programs",
        optimization_lever="Incentive aligned with genuine value, not just cash"
    ),
    "Expansion": CustomerJourneyStageDef(
        stage_name="Expansion",
        founder_objective="Grow account value",
        customer_psychology="Anchoring to current spend",
        key_metric="Net revenue retention (NRR)",
        common_mistake="Under-selling adjacent value",
        optimization_lever="Usage-based expansion triggers"
    ),
    "Repurchase": CustomerJourneyStageDef(
        stage_name="Repurchase",
        founder_objective="Sustain lifetime value",
        customer_psychology="Habitual trust, low re-evaluation cost",
        key_metric="LTV, repurchase rate",
        common_mistake="Treating repurchase as passive",
        optimization_lever="Proactive lifecycle marketing tied to usage signals"
    )
}

# ------------------------------------------------------------------
# Company Growth System Database
# ------------------------------------------------------------------
COMPANY_GROWTH_STAGES: Dict[str, CompanyGrowthStageDef] = {
    "Idea": CompanyGrowthStageDef(
        stage_name="Idea",
        primary_objective="Falsify or strengthen hypothesis",
        org_change="Founder(s) only",
        decision_making_change="Founder intuition, fast",
        capital_allocation="Near-zero, sweat equity",
        key_risk="Solving a non-problem",
        core_metric="# of validated learnings",
        binding_constraint="Founder time"
    ),
    "Validation": CompanyGrowthStageDef(
        stage_name="Validation",
        primary_objective="Prove willingness to pay",
        org_change="First 1–3 hires",
        decision_making_change="Still founder-centric",
        capital_allocation="Pre-seed/seed capital",
        key_risk="False positive validation (friends/family bias)",
        core_metric="Paying customers / LOIs",
        binding_constraint="Signal quality"
    ),
    "Startup": CompanyGrowthStageDef(
        stage_name="Startup",
        primary_objective="Build repeatable acquisition",
        org_change="Functional roles emerge",
        decision_making_change="Founder + small team, high context-sharing",
        capital_allocation="Seed/Series A",
        key_risk="Premature scaling before PMF",
        core_metric="CAC:LTV early signal",
        binding_constraint="Cash runway"
    ),
    "PMF": CompanyGrowthStageDef(
        stage_name="PMF",
        primary_objective="Reach retention/growth threshold",
        org_change="First managers",
        decision_making_change="Data starts overriding intuition",
        capital_allocation="Growth capital",
        key_risk="Mistaking early traction for PMF",
        core_metric="Retention curve flattening",
        binding_constraint="Team bandwidth"
    ),
    "Growth": CompanyGrowthStageDef(
        stage_name="Growth",
        primary_objective="Scale what works",
        org_change="Middle management layer",
        decision_making_change="Process + data-driven",
        capital_allocation="Series B/C, aggressive if unit economics hold",
        key_risk="Scaling a broken funnel",
        core_metric="Growth rate, CAC payback",
        binding_constraint="Hiring velocity, systems"
    ),
    "Scale": CompanyGrowthStageDef(
        stage_name="Scale",
        primary_objective="Institutionalize repeatability",
        org_change="Departments, specialized functions",
        decision_making_change="Delegated, framework-driven",
        capital_allocation="Efficient growth capital",
        key_risk="Culture dilution, bureaucracy creep",
        core_metric="Rule of 40, NRR",
        binding_constraint="Org coordination cost"
    ),
    "Platform": CompanyGrowthStageDef(
        stage_name="Platform",
        primary_objective="Enable others to build on you",
        org_change="Platform/ecosystem teams",
        decision_making_change="Governance structures, APIs-as-product",
        capital_allocation="Infrastructure investment",
        key_risk="Platform without ecosystem demand",
        core_metric="Third-party developer/partner activity",
        binding_constraint="Trust from ecosystem partners"
    ),
    "Ecosystem": CompanyGrowthStageDef(
        stage_name="Ecosystem",
        primary_objective="Orchestrate a multi-sided network",
        org_change="Ecosystem management, BD at scale",
        decision_making_change="Distributed decision rights",
        capital_allocation="Strategic/M&A capital",
        key_risk="Ecosystem fragmentation, partner conflict",
        core_metric="Ecosystem GMV / network density",
        binding_constraint="Governance credibility"
    ),
    "Market Leadership": CompanyGrowthStageDef(
        stage_name="Market Leadership",
        primary_objective="Defend and extend category",
        org_change="Full corporate structure",
        decision_making_change="Board-level strategic governance",
        capital_allocation="Diversified, defensive + offensive",
        key_risk="Complacency, disruption from below",
        core_metric="Category share, moat durability score",
        binding_constraint="Innovation velocity vs. incumbency drag"
    )
}


class SignalToIdeaPipeline:
    """Processes weak signals and converts them into falsifiable hypotheses."""

    def __init__(self) -> None:
        self.hypotheses: List[Hypothesis] = []

    def filter_signal(self, signal: WeakSignal) -> Optional[Hypothesis]:
        """Filters a signal.

        Returns a newly formed Hypothesis if it is a structural anomaly,
        otherwise discards it.
        """
        if not signal.is_anomaly:
            logger.info(f"Discarding weak signal: {signal.description} (Not flagged as anomaly).")
            return None

        # Build structural hypothesis
        claim = f"If structural shifts related to '{signal.description}' occur, it unlocks a compounding advantage."
        hyp = Hypothesis(
            claim=claim,
            pre_committed_kill_criteria="Cheap-test conversion metrics fall below 5% or CAC payback > 18 months",
            prior_confidence=0.3 * signal.strength
        )
        self.hypotheses.append(hyp)
        logger.info(f"Signal promoted to falsifiable hypothesis: {hyp.claim}")
        return hyp

    def evaluate_risk_profile(self, decision_name: str, irreversible_regulatory_safety: bool) -> RiskType:
        """Bezos's One-Way vs Two-Way doors heuristic.

        Type I: Irreversible, high-scrutiny, slow deliberation.
        Type II: Reversible, fast, cheap.
        """
        if irreversible_regulatory_safety:
            logger.info(f"Decision '{decision_name}' classified as TYPE I (one-way door). High-scrutiny required.")
            return RiskType.TYPE_I
        else:
            logger.info(f"Decision '{decision_name}' classified as TYPE II (two-way door). Reversible; proceed fast.")
            return RiskType.TYPE_II


class DecisionTreeEvaluator:
    """Implements §10.2 Decision Tree: 'Should We Pursue This Opportunity?'."""

    def evaluate(
        self,
        is_structural_anomaly: bool,
        is_reversible: bool,
        has_high_confidence_multi_source: bool,
        cheap_test_available: bool,
        cheap_test_result_exceeds_kill_threshold: bool,
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> Tuple[bool, str]:
        """Runs the deterministic decision tree logic.

        Returns a tuple of (should_pursue: bool, rationale: str).
        """
        # Q1: Structural anomaly or just noise?
        if not is_structural_anomaly:
            return False, "Discard: Flagged as noise, not a structural anomaly."

        # Q2: Reversible decision?
        if not is_reversible:
            # Q2a: High-confidence signal from multiple sources?
            if not has_high_confidence_multi_source:
                return False, "Discard: Irreversible decision without high-confidence multi-source signals."
            # If yes, proceed to Q3

        # Q3: Cheap test available?
        if cheap_test_available:
            # Run cheap test -> Q4: Result exceeds kill threshold?
            if not cheap_test_result_exceeds_kill_threshold:
                return False, "Discard: Cheap test did not exceed pre-committed kill threshold."
            # If yes, proceed to Q5
        else:
            # Q4b: Expected value clearly positive?
            if not expected_value_positive:
                return False, "Discard: Cheap test unavailable and expected value is not positive."
            # If yes, proceed to Q5

        # Q5: Do we have or can we build a structural advantage here?
        if not has_structural_advantage:
            return False, "Discard: No clear structural advantage available or buildable."

        return True, "Commit resources: Opportunity passed all decision tree filters."


class EOSStateMachine:
    """System State Machine (§10.1) driving opportunity through lifecycle stages."""

    def __init__(self, initial_state: EOSState = EOSState.SENSING) -> None:
        self.state = initial_state
        self.transition_history: List[Tuple[EOSState, EOSState, str]] = []

    def transition_to(self, target_state: EOSState, reason: str) -> bool:
        """Validates and applies state transitions per the defined state machine logic."""
        allowed = self._is_transition_allowed(self.state, target_state)
        if allowed:
            old_state = self.state
            self.state = target_state
            self.transition_history.append((old_state, target_state, reason))
            logger.info(f"EOS State Transition: {old_state.name} -> {target_state.name} | Reason: {reason}")
            return True
        else:
            logger.warning(f"Illegal state transition attempted: {self.state.name} -> {target_state.name}")
            return False

    def _is_transition_allowed(self, current: EOSState, target: EOSState) -> bool:
        # Discard state is always accessible except from DISCARDED itself
        if target == EOSState.DISCARDED:
            return current != EOSState.DISCARDED

        # Sensing can only go to Hypothesis
        if current == EOSState.SENSING:
            return target in [EOSState.HYPOTHESIS, EOSState.DISCARDED]

        # Hypothesis can go to CheapTest
        if current == EOSState.HYPOTHESIS:
            return target in [EOSState.CHEAP_TEST, EOSState.DISCARDED]

        # CheapTest can go to Validation or back to Sensing (if falsified/discarded internally)
        if current == EOSState.CHEAP_TEST:
            return target in [EOSState.VALIDATION, EOSState.DISCARDED, EOSState.SENSING]

        # Validation can go to BuildGate
        if current == EOSState.VALIDATION:
            return target in [EOSState.BUILD_GATE, EOSState.DISCARDED]

        # BuildGate can go to MVP
        if current == EOSState.BUILD_GATE:
            return target in [EOSState.MVP, EOSState.DISCARDED]

        # MVP can go to GTMTest
        if current == EOSState.MVP:
            return target in [EOSState.GTM_TEST, EOSState.DISCARDED]

        # GTMTest can go to KillOrScale
        if current == EOSState.GTM_TEST:
            return target in [EOSState.KILL_OR_SCALE, EOSState.DISCARDED]

        # KillOrScale can go to Scale or Discarded
        if current == EOSState.KILL_OR_SCALE:
            return target in [EOSState.SCALE, EOSState.DISCARDED]

        # Scale can go to Operate
        if current == EOSState.SCALE:
            return target in [EOSState.OPERATE, EOSState.DISCARDED]

        # Operate can go to Reinvent
        if current == EOSState.OPERATE:
            return target in [EOSState.REINVENT, EOSState.DISCARDED]

        # Reinvent can go back to Sensing
        if current == EOSState.REINVENT:
            return target in [EOSState.SENSING, EOSState.DISCARDED]

        return False


class FailureModeMonitor:
    """Monitors metrics against the 10 core failure modes and suggests corrections."""

    def __init__(self) -> None:
        pass

    def inspect_metrics(self, metrics: Dict[str, Any]) -> List[Tuple[str, str, str]]:
        """Scans metrics.

        Returns list of (Failure Mode, Root Cause, Suggested Correction Mechanism).
        """
        flags = []

        # 1. Solving the wrong problem
        if metrics.get("user_engagement", 1.0) < 0.10 and metrics.get("survey_satisfaction_score", 0.0) >= 0.80:
            flags.append((
                "Solving the wrong problem",
                "Skipped root-cause analysis; solved a symptom",
                "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)"
            ))

        # 2. Building before validating
        if metrics.get("build_velocity_high", False) and metrics.get("demand_clicks", 0) < 10:
            flags.append((
                "Building before validating",
                "Founder conviction substituted for evidence",
                "Enforce a validation gate before build resourcing"
            ))

        # 3. Weak positioning
        if metrics.get("cac_usd", 0) > 200 and metrics.get("sales_cycle_days", 0) > 90 and metrics.get("feature_comparison_objections", 0) > 5:
            flags.append((
                "Weak positioning",
                "No clear 'instead of X, use us because Y'",
                "Rebuild positioning around the real alternative customers compare to"
            ))

        # 4. Poor pricing
        if metrics.get("price_conversion_rate", 0.0) > 0.40 and metrics.get("gross_margin_pct", 1.0) < 0.30:
            flags.append((
                "Poor pricing",
                "Cost-plus instead of value-based pricing",
                "Re-anchor price to quantified customer value"
            ))

        # 5. Distribution failure
        if metrics.get("net_promoter_score", 0) >= 50 and metrics.get("growth_rate_pct", 0.0) <= 2.0:
            flags.append((
                "Distribution failure",
                "Great product, no repeatable channel",
                "Systematically test channels against ICP behavior, not founder preference"
            ))

        # 6. Lack of product-market fit
        if metrics.get("retention_curve_slope", 0.0) < -0.15 and metrics.get("is_scaling_budget", False):
            flags.append((
                "Lack of product-market fit",
                "Premature scaling of an unproven loop",
                "Stop scaling; return to cohort-level retention work"
            ))

        # 7. Organizational bottlenecks
        if metrics.get("decision_latency_days", 0) > 14 and metrics.get("founder_is_single_point_of_failure", False):
            flags.append((
                "Organizational bottlenecks",
                "Decision rights not delegated as company scales",
                "Push decision rights down with clear frameworks (not ad hoc delegation)"
            ))

        # 8. Founder bias
        if metrics.get("disconfirming_data_points_ignored", 0) >= 3:
            flags.append((
                "Founder bias",
                "Overconfidence, confirmation bias, sunk cost",
                "Pre-committed kill criteria set before launch"
            ))

        # 9. Scaling prematurely
        if metrics.get("order_of_magnitude_spend_scale", 1) >= 2 and metrics.get("cac_to_ltv_ratio", 0.0) > 0.60:
            flags.append((
                "Scaling prematurely",
                "Confusing early demand spike with durable PMF",
                "Re-test unit economics at each order-of-magnitude of spend"
            ))

        # 10. Capital misallocation
        if metrics.get("underperforming_bets_funded", 0) >= 3:
            flags.append((
                "Capital misallocation",
                "No opportunity-cost discipline in budgeting",
                "Rank all initiatives on a common expected-return basis quarterly"
            ))

        return flags


class EOSKPIDashboard:
    """Subsystem-level KPI Stack (§10.4) rolled up to overall health."""

    def __init__(self) -> None:
        self.sensing_metrics: Dict[str, float] = {}
        self.validation_metrics: Dict[str, float] = {}
        self.product_metrics: Dict[str, float] = {}
        self.gtm_metrics: Dict[str, float] = {}
        self.financial_metrics: Dict[str, float] = {}
        self.org_metrics: Dict[str, float] = {}
        self.strategic_metrics: Dict[str, float] = {}

    def update_sensing(self, signal_to_noise: float, anomaly_lead_time_days: float) -> None:
        self.sensing_metrics["signal_to_noise_ratio"] = signal_to_noise
        self.sensing_metrics["anomaly_detection_lead_time_days"] = anomaly_lead_time_days

    def update_validation(self, cost_per_learning_usd: float, false_positive_rate: float) -> None:
        self.validation_metrics["cost_per_validated_learning"] = cost_per_learning_usd
        self.validation_metrics["false_positive_rate"] = false_positive_rate

    def update_product(self, activation_rate: float, retention_slope: float) -> None:
        self.product_metrics["activation_rate"] = activation_rate
        self.product_metrics["retention_curve_slope"] = retention_slope

    def update_gtm(self, cac: float, payback_months: float, organic_share: float) -> None:
        self.gtm_metrics["cac_usd"] = cac
        self.gtm_metrics["cac_payback_period_months"] = payback_months
        self.gtm_metrics["channel_contribution_organic"] = organic_share

    def update_financial(self, gross_margin: float, burn_multiple: float, runway_months: float) -> None:
        self.financial_metrics["gross_margin_pct"] = gross_margin
        self.financial_metrics["burn_multiple"] = burn_multiple
        self.financial_metrics["runway_months"] = runway_months

    def update_org(self, decision_latency_days: float, attrition_rate: float) -> None:
        self.org_metrics["decision_latency_days"] = decision_latency_days
        self.org_metrics["regretted_attrition_rate"] = attrition_rate

    def update_strategic(self, market_share_pct: float, moat_durability: float) -> None:
        self.strategic_metrics["relative_market_share_pct"] = market_share_pct
        self.strategic_metrics["moat_durability_score"] = moat_durability

    def get_loop_closure_time_days(self) -> float:
        """System-level overall loop-closure time (idea -> validated learning -> decision)."""
        sensing_time = self.sensing_metrics.get("anomaly_detection_lead_time_days", 5.0)
        decision_time = self.org_metrics.get("decision_latency_days", 3.0)
        # return overall sum
        return sensing_time + decision_time + 4.5  # base validation offset
