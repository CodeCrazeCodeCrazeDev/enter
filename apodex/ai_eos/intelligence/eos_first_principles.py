"""Entrepreneurial Operating System (EOS) First-Principles Engine.

Implements an 11-section executable architecture reflecting how elite founders sense,
build, compound, and continuously reinvent enduring technology companies.
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger("sero.eos_first_principles")


# =====================================================================
# 1. State Machine (§10.1)
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
    """Manages system state transitions for autonomous entrepreneurial execution."""

    VALID_TRANSITIONS: Dict[EOSState, Set[EOSState]] = {
        EOSState.SENSING: {EOSState.HYPOTHESIS},
        EOSState.HYPOTHESIS: {EOSState.CHEAP_TEST},
        EOSState.CHEAP_TEST: {EOSState.DISCARD, EOSState.VALIDATION},
        EOSState.DISCARD: {EOSState.SENSING},
        EOSState.VALIDATION: {EOSState.BUILD_GATE, EOSState.DISCARD},
        EOSState.BUILD_GATE: {EOSState.MVP},
        EOSState.MVP: {EOSState.GTM_TEST},
        EOSState.GTM_TEST: {EOSState.KILL_OR_SCALE},
        EOSState.KILL_OR_SCALE: {EOSState.DISCARD, EOSState.SCALE},
        EOSState.SCALE: {EOSState.OPERATE},
        EOSState.OPERATE: {EOSState.REINVENT},
        EOSState.REINVENT: {EOSState.SENSING},
    }

    def __init__(self, initial_state: EOSState = EOSState.SENSING) -> None:
        self.current_state = initial_state
        self.history: List[Tuple[EOSState, EOSState, str]] = []

    def transition_to(self, target_state: EOSState, reason: str = "") -> EOSState:
        """Transitions to target_state if valid, logging history."""
        allowed = self.VALID_TRANSITIONS.get(self.current_state, set())
        if target_state not in allowed:
            raise ValueError(
                f"Invalid transition from state '{self.current_state.value}' to '{target_state.value}'. "
                f"Allowed target states: {[s.value for s in allowed]}"
            )
        old_state = self.current_state
        self.current_state = target_state
        self.history.append((old_state, target_state, reason))
        logger.info(f"EOS STATE TRANSITION: {old_state.value} -> {target_state.value} ({reason})")
        return self.current_state


# =====================================================================
# 2. Decision Tree (§10.2)
# =====================================================================
class DecisionTreeResult(BaseModel):
    decision: str  # "COMMIT_RESOURCES", "RUN_CHEAP_TEST", or "DISCARD"
    path: List[str]
    confidence_score: float
    risk_type: str  # "Type_I" (irreversible) or "Type_II" (reversible)


class OpportunityDecisionTree:
    """Evaluates whether to pursue an opportunity according to §10.2 logic."""

    def __init__(self) -> None:
        pass

    def evaluate(
        self,
        is_structural_anomaly: bool,
        is_reversible: bool,
        high_confidence_signals: bool,
        cheap_test_available: bool,
        cheap_test_passed: Optional[bool] = None,
        expected_value_positive: bool = True,
        structural_advantage: bool = False,
    ) -> DecisionTreeResult:
        path: List[str] = []

        # Q1: Structural anomaly or just noise?
        if not is_structural_anomaly:
            path.append("Q1: Noise signal -> Discard")
            return DecisionTreeResult(
                decision="DISCARD",
                path=path,
                confidence_score=0.1,
                risk_type="Type_II" if is_reversible else "Type_I",
            )
        path.append("Q1: Structural anomaly confirmed")

        risk_type = "Type_II" if is_reversible else "Type_I"

        # Q2: Reversible decision?
        if not is_reversible:
            path.append("Q2: Irreversible / Type I decision")
            # Q2a: High confidence signal from multiple sources?
            if not high_confidence_signals:
                path.append("Q2a: Insufficient multi-source confidence -> Discard")
                return DecisionTreeResult(
                    decision="DISCARD",
                    path=path,
                    confidence_score=0.2,
                    risk_type=risk_type,
                )
            path.append("Q2a: High-confidence multi-source signal verified")
        else:
            path.append("Q2: Reversible / Type II decision")

        # Q3: Cheap test available?
        if cheap_test_available:
            path.append("Q3: Cheap test available")
            if cheap_test_passed is None:
                path.append("Execute cheap test next")
                return DecisionTreeResult(
                    decision="RUN_CHEAP_TEST",
                    path=path,
                    confidence_score=0.6,
                    risk_type=risk_type,
                )
            elif cheap_test_passed is False:
                path.append("Q4: Cheap test result below kill threshold -> Discard")
                return DecisionTreeResult(
                    decision="DISCARD",
                    path=path,
                    confidence_score=0.2,
                    risk_type=risk_type,
                )
            path.append("Q4: Cheap test result exceeded kill threshold")
        else:
            path.append("Q3: No cheap test available")
            # Q4b: Expected value positive?
            if not expected_value_positive:
                path.append("Q4b: Negative expected value -> Discard")
                return DecisionTreeResult(
                    decision="DISCARD",
                    path=path,
                    confidence_score=0.3,
                    risk_type=risk_type,
                )
            path.append("Q4b: Expected value clearly positive")

        # Q5: Structural advantage?
        if not structural_advantage:
            path.append("Q5: No defensible structural advantage -> Discard")
            return DecisionTreeResult(
                decision="DISCARD",
                path=path,
                confidence_score=0.4,
                risk_type=risk_type,
            )
        path.append("Q5: Structural advantage confirmed -> Commit resources")

        return DecisionTreeResult(
            decision="COMMIT_RESOURCES",
            path=path,
            confidence_score=0.9,
            risk_type=risk_type,
        )


# =====================================================================
# 3. Coupled Business Loops (§3)
# =====================================================================
class SystemStocks(BaseModel):
    cash_cents: int = 10_000_000  # Default $100k
    talent_headcount: int = 5
    brand_trust_score: float = 0.5
    data_points: int = 1000

    model_config = ConfigDict(arbitrary_types_allowed=True)


class BusinessLoopState(BaseModel):
    loop_name: str
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    feedback_signal: str = ""
    kpis: Dict[str, float] = Field(default_factory=dict)
    failure_flag: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)


class CoupledBusinessLoopsEngine:
    """Simulates the 13 coupled business feedback loops and stock/flow dynamics."""

    LOOP_NAMES = [
        "Product",
        "Marketing",
        "Sales",
        "Customer Success",
        "Brand",
        "Pricing",
        "Referral",
        "Data",
        "Financial",
        "Hiring",
        "Culture",
        "Innovation",
        "Competitive Intelligence",
    ]

    def __init__(self) -> None:
        self.stocks = SystemStocks()
        self.loops: Dict[str, BusinessLoopState] = {
            name: BusinessLoopState(loop_name=name) for name in self.LOOP_NAMES
        }

    def update_loops(self, metrics: Dict[str, Any]) -> Dict[str, BusinessLoopState]:
        """Updates states, coupled interactions, and stocks across all 13 loops."""
        # 1. Product Loop
        retention = metrics.get("retention_rate", 0.60)
        nps = metrics.get("nps", 40.0)
        self.loops["Product"].kpis = {"retention_rate": retention, "nps": nps}
        self.loops["Product"].failure_flag = retention < 0.30

        # 2. Marketing Loop
        cac = metrics.get("cac_cents", 5000)
        conv_rate = metrics.get("conversion_rate", 0.03)
        self.loops["Marketing"].kpis = {"cac_cents": float(cac), "conversion_rate": conv_rate}
        self.loops["Marketing"].failure_flag = cac > 50000 and conv_rate < 0.01

        # 3. Sales Loop
        win_rate = metrics.get("win_rate", 0.25)
        acv = metrics.get("acv_cents", 120000)
        self.loops["Sales"].kpis = {"win_rate": win_rate, "acv_cents": float(acv)}
        self.loops["Sales"].failure_flag = win_rate < 0.10

        # 4. Customer Success Loop
        nrr = metrics.get("nrr", 1.10)
        churn = metrics.get("churn_rate", 0.02)
        self.loops["Customer Success"].kpis = {"nrr": nrr, "churn_rate": churn}
        self.loops["Customer Success"].failure_flag = nrr < 0.85

        # 5. Brand Loop
        price_elasticity = metrics.get("price_elasticity", -0.5)
        self.loops["Brand"].kpis = {"trust_score": self.stocks.brand_trust_score, "price_elasticity": price_elasticity}

        # 6. Pricing Loop
        arpu = metrics.get("arpu_cents", 10000)
        self.loops["Pricing"].kpis = {"arpu_cents": float(arpu)}
        self.loops["Pricing"].outputs = {"arpu_cents": arpu}

        # 7. Referral Loop
        k_factor = metrics.get("k_factor", 0.8)
        self.loops["Referral"].kpis = {"k_factor": k_factor}
        self.loops["Referral"].failure_flag = k_factor < 0.1

        # 8. Data Loop
        decision_latency = metrics.get("decision_latency_sec", 12.0)
        self.loops["Data"].kpis = {"data_points": float(self.stocks.data_points), "decision_latency_sec": decision_latency}

        # 9. Financial Loop
        burn_multiple = metrics.get("burn_multiple", 1.5)
        runway = metrics.get("runway_months", 18.0)
        gross_margin = metrics.get("gross_margin", 0.75)
        self.loops["Financial"].kpis = {
            "burn_multiple": burn_multiple,
            "runway_months": runway,
            "gross_margin": gross_margin,
        }
        self.loops["Financial"].failure_flag = burn_multiple > 3.0 or runway < 4.0

        # 10. Hiring Loop
        time_to_fill = metrics.get("time_to_fill_days", 30.0)
        self.loops["Hiring"].kpis = {"headcount": float(self.stocks.talent_headcount), "time_to_fill_days": time_to_fill}

        # 11. Culture Loop
        enps = metrics.get("enps", 50.0)
        self.loops["Culture"].kpis = {"enps": enps, "decision_latency_sec": decision_latency}

        # 12. Innovation Loop
        exp_count = metrics.get("experiments_run", 10.0)
        hit_rate = metrics.get("experiment_hit_rate", 0.20)
        self.loops["Innovation"].kpis = {"experiments_run": exp_count, "hit_rate": hit_rate}

        # 13. Competitive Intelligence Loop
        parity_gap = metrics.get("feature_parity_gap", 0.15)
        self.loops["Competitive Intelligence"].kpis = {"feature_parity_gap": parity_gap}

        # Update Stock flows
        revenue = metrics.get("monthly_revenue_cents", 500000)
        monthly_burn = metrics.get("monthly_burn_cents", 300000)
        self.stocks.cash_cents += int(revenue - monthly_burn)
        self.stocks.data_points += int(metrics.get("new_data_points", 50))
        if nps > 50:
            self.stocks.brand_trust_score = min(1.0, self.stocks.brand_trust_score + 0.02)
        elif nps < 0:
            self.stocks.brand_trust_score = max(0.0, self.stocks.brand_trust_score - 0.05)

        return self.loops


# =====================================================================
# 4. Customer Journey (§4)
# =====================================================================
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


class CustomerLifecycleEngine(BaseModel):
    """Tracks cohort progression across the 15 customer lifecycle stages."""

    stage_counts: Dict[CustomerLifecycleStage, int] = Field(
        default_factory=lambda: {s: 0 for s in CustomerLifecycleStage}
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def update_lifecycle(self, stage_volumes: Dict[str, int]) -> Dict[str, float]:
        """Sets stage counts and computes step-by-step conversion ratios."""
        for name, vol in stage_volumes.items():
            try:
                st = CustomerLifecycleStage(name)
                self.stage_counts[st] = vol
            except ValueError:
                pass

        conversion_rates: Dict[str, float] = {}
        stages = list(CustomerLifecycleStage)
        for i in range(len(stages) - 1):
            curr_st, next_st = stages[i], stages[i + 1]
            curr_v = self.stage_counts[curr_st]
            next_v = self.stage_counts[next_st]
            rate = (next_v / curr_v) if curr_v > 0 else 0.0
            conversion_rates[f"{curr_st.value}->{next_st.value}"] = rate

        return conversion_rates

    def identify_bottleneck_stage(self) -> Tuple[Optional[str], float]:
        """Identifies the stage transition with the sharpest conversion drop."""
        convs = self.update_lifecycle({})
        if not convs:
            return (None, 0.0)
        lowest = min(convs.items(), key=lambda x: x[1])
        return lowest


# =====================================================================
# 5. Go-To-Market System (§5)
# =====================================================================
class GTMSystemEngine:
    """Models GTM fit, positioning alignment, and distribution channel compounding."""

    def evaluate_motion(
        self,
        acv_cents: int,
        complexity: str,  # "low", "medium", "high"
        has_network_effects: bool = False,
        has_community: bool = False,
    ) -> Dict[str, Any]:
        """Recommends primary and secondary GTM distribution motions based on buyer behavior."""
        primary_motion = "PLG"
        secondary_motions: List[str] = []

        if acv_cents >= 10_000_00:  # $10k+
            if complexity == "high":
                primary_motion = "Sales-Led Growth (SLG / Enterprise)"
                secondary_motions.append("Content Strategy")
            else:
                primary_motion = "PLG + Sales-Led Expansion"
        elif acv_cents <= 1_000_00:  # Under $1k
            primary_motion = "Product-Led Growth (PLG)"
            secondary_motions.extend(["Organic Content", "Paid Acquisition"])

        if has_network_effects or has_community:
            secondary_motions.append("Community-Led Growth (CLG)")

        compounding_score = 0.5
        if primary_motion.startswith("PLG") and "Community-Led Growth (CLG)" in secondary_motions:
            compounding_score = 0.95
        elif primary_motion.startswith("Sales-Led"):
            compounding_score = 0.80

        return {
            "primary_motion": primary_motion,
            "secondary_motions": secondary_motions,
            "channel_compounding_score": compounding_score,
            "alignment_rationale": f"ACV: ${acv_cents/100:.2f}, Complexity: {complexity}",
        }


# =====================================================================
# 6. Company Growth System (§6)
# =====================================================================
class GrowthStage(str, Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "Product-Market Fit"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    MARKET_LEADERSHIP = "Market Leadership"


class StageCharacteristics(BaseModel):
    stage: GrowthStage
    primary_objective: str
    org_structure: str
    decision_mode: str
    key_risk: str
    core_metric: str
    binding_constraint: str


class GrowthStageClassifier:
    """Classifies company maturity stage across the 9-stage continuum."""

    STAGE_TABLE: Dict[GrowthStage, StageCharacteristics] = {
        GrowthStage.IDEA: StageCharacteristics(
            stage=GrowthStage.IDEA,
            primary_objective="Falsify or strengthen hypothesis",
            org_structure="Founder(s) only",
            decision_mode="Founder intuition, fast",
            key_risk="Solving a non-problem",
            core_metric="# of validated learnings",
            binding_constraint="Founder time",
        ),
        GrowthStage.VALIDATION: StageCharacteristics(
            stage=GrowthStage.VALIDATION,
            primary_objective="Prove willingness to pay",
            org_structure="First 1–3 hires",
            decision_mode="Still founder-centric",
            key_risk="False positive validation (friends/family bias)",
            core_metric="Paying customers / LOIs",
            binding_constraint="Signal quality",
        ),
        GrowthStage.STARTUP: StageCharacteristics(
            stage=GrowthStage.STARTUP,
            primary_objective="Build repeatable acquisition",
            org_structure="Functional roles emerge",
            decision_mode="Founder + small team, high context-sharing",
            key_risk="Premature scaling before PMF",
            core_metric="CAC:LTV early signal",
            binding_constraint="Cash runway",
        ),
        GrowthStage.PMF: StageCharacteristics(
            stage=GrowthStage.PMF,
            primary_objective="Reach retention/growth threshold",
            org_structure="First managers",
            decision_mode="Data starts overriding intuition",
            key_risk="Mistaking early traction for PMF",
            core_metric="Retention curve flattening",
            binding_constraint="Team bandwidth",
        ),
        GrowthStage.GROWTH: StageCharacteristics(
            stage=GrowthStage.GROWTH,
            primary_objective="Scale what works",
            org_structure="Middle management layer",
            decision_mode="Process + data-driven",
            key_risk="Scaling a broken funnel",
            core_metric="Growth rate, CAC payback",
            binding_constraint="Hiring velocity, systems",
        ),
        GrowthStage.SCALE: StageCharacteristics(
            stage=GrowthStage.SCALE,
            primary_objective="Institutionalize repeatability",
            org_structure="Departments, specialized functions",
            decision_mode="Delegated, framework-driven",
            key_risk="Culture dilution, bureaucracy creep",
            core_metric="Rule of 40, NRR",
            binding_constraint="Org coordination cost",
        ),
        GrowthStage.PLATFORM: StageCharacteristics(
            stage=GrowthStage.PLATFORM,
            primary_objective="Enable others to build on you",
            org_structure="Platform/ecosystem teams",
            decision_mode="Governance structures, APIs-as-product",
            key_risk="Platform without ecosystem demand",
            core_metric="Third-party developer/partner activity",
            binding_constraint="Trust from ecosystem partners",
        ),
        GrowthStage.ECOSYSTEM: StageCharacteristics(
            stage=GrowthStage.ECOSYSTEM,
            primary_objective="Orchestrate a multi-sided network",
            org_structure="Ecosystem management, BD at scale",
            decision_mode="Distributed decision rights",
            key_risk="Ecosystem fragmentation, partner conflict",
            core_metric="Ecosystem GMV / network density",
            binding_constraint="Governance credibility",
        ),
        GrowthStage.MARKET_LEADERSHIP: StageCharacteristics(
            stage=GrowthStage.MARKET_LEADERSHIP,
            primary_objective="Defend and extend category",
            org_structure="Full corporate structure",
            decision_mode="Board-level strategic governance",
            key_risk="Complacency, disruption from below",
            core_metric="Category share, moat durability",
            binding_constraint="Innovation velocity vs. incumbency drag",
        ),
    }

    def classify(self, metrics: Dict[str, Any]) -> StageCharacteristics:
        paying_customers = metrics.get("paying_customers", 0)
        retention_flattened = metrics.get("retention_curve_flattened", False)
        arr_cents = metrics.get("arr_cents", 0)
        developer_activity = metrics.get("developer_activity_count", 0)
        market_share = metrics.get("market_share", 0.0)

        if market_share >= 0.40 and arr_cents >= 100_000_000_00:  # $100M+ ARR & 40%+ share
            return self.STAGE_TABLE[GrowthStage.MARKET_LEADERSHIP]
        elif developer_activity >= 1000:
            return self.STAGE_TABLE[GrowthStage.ECOSYSTEM]
        elif developer_activity >= 100:
            return self.STAGE_TABLE[GrowthStage.PLATFORM]
        elif arr_cents >= 10_000_000_00:  # $10M+ ARR
            return self.STAGE_TABLE[GrowthStage.SCALE]
        elif retention_flattened and arr_cents >= 1_000_000_00:  # $1M+ ARR
            return self.STAGE_TABLE[GrowthStage.GROWTH]
        elif retention_flattened:
            return self.STAGE_TABLE[GrowthStage.PMF]
        elif paying_customers >= 5:
            return self.STAGE_TABLE[GrowthStage.STARTUP]
        elif paying_customers > 0:
            return self.STAGE_TABLE[GrowthStage.VALIDATION]
        return self.STAGE_TABLE[GrowthStage.IDEA]


# =====================================================================
# 7. Strategic Moats (§7)
# =====================================================================
class StrategicMoatEngine:
    """Scores structural competitive advantage (7 Powers + Porter's forces)."""

    def score_moats(
        self,
        network_effects_score: float,
        switching_costs_cents: int,
        scale_economies_score: float,
        brand_trust_score: float,
        counter_positioning_score: float,
        cornered_resources_score: float = 0.0,
        process_power_score: float = 0.0,
    ) -> Dict[str, Any]:
        s_net = min(1.0, max(0.0, network_effects_score))
        s_switch = min(1.0, max(0.0, switching_costs_cents / 10000_00))  # Normalized at $10k
        s_scale = min(1.0, max(0.0, scale_economies_score))
        s_brand = min(1.0, max(0.0, brand_trust_score))
        s_counter = min(1.0, max(0.0, counter_positioning_score))
        s_cornered = min(1.0, max(0.0, cornered_resources_score))
        s_process = min(1.0, max(0.0, process_power_score))

        composite_moat = (
            0.20 * s_net
            + 0.15 * s_switch
            + 0.15 * s_scale
            + 0.15 * s_brand
            + 0.15 * s_counter
            + 0.10 * s_cornered
            + 0.10 * s_process
        )

        return {
            "composite_moat_durability_score": round(composite_moat, 4),
            "dominant_moat_source": max(
                [
                    ("Network Effects", s_net),
                    ("Switching Costs", s_switch),
                    ("Scale Economies", s_scale),
                    ("Brand Trust", s_brand),
                    ("Counter-Positioning", s_counter),
                    ("Cornered Resources", s_cornered),
                    ("Process Power", s_process),
                ],
                key=lambda x: x[1],
            )[0],
            "sub_scores": {
                "network_effects": s_net,
                "switching_costs": s_switch,
                "scale_economies": s_scale,
                "brand_trust": s_brand,
                "counter_positioning": s_counter,
                "cornered_resources": s_cornered,
                "process_power": s_process,
            },
        }


# =====================================================================
# 8. Failure Mode Analysis (§8)
# =====================================================================
class FailureModeAlert(BaseModel):
    failure_mode: str
    root_cause: str
    detection_signal: str
    correction_mechanism: str
    severity: str  # "HIGH", "CRITICAL"


class FailureModeMonitor:
    """Audits operating metrics against the 10 core failure modes from §8."""

    FAILURE_TABLE = [
        ("Solving the wrong problem", "Skipped root-cause analysis; solved a symptom", "Low engagement despite positive survey feedback", "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)"),
        ("Building before validating", "Founder conviction substituted for evidence", "High build velocity, flat demand signal", "Enforce a validation gate before build resourcing"),
        ("Weak positioning", "No clear 'instead of X, use us because Y'", "High CAC, long sales cycles, feature comparison objections", "Rebuild positioning around the real alternative customers compare to"),
        ("Poor pricing", "Cost-plus instead of value-based pricing", "High conversion at low price, but poor margin/expansion", "Re-anchor price to quantified customer value"),
        ("Distribution failure", "Great product, no repeatable channel", "High NPS, flat growth", "Systematically test channels against ICP behavior, not founder preference"),
        ("Lack of product-market fit", "Premature scaling of an unproven loop", "Retention curve never flattens", "Stop scaling; return to cohort-level retention work"),
        ("Organizational bottlenecks", "Decision rights not delegated as company scales", "Rising decision latency, founder as single point of failure", "Push decision rights down with clear frameworks (not ad hoc delegation)"),
        ("Founder bias", "Overconfidence, confirmation bias, sunk cost", "Ignoring disconfirming data, 'just needs more time' pattern", "Pre-committed kill criteria set before launch"),
        ("Scaling prematurely", "Confusing early demand spike with durable PMF", "CAC rising faster than LTV as spend scales", "Re-test unit economics at each order-of-magnitude of spend"),
        ("Capital misallocation", "No opportunity-cost discipline in budgeting", "Multiple underperforming bets funded simultaneously", "Rank all initiatives on a common expected-return basis quarterly"),
    ]

    def audit(self, metrics: Dict[str, Any]) -> List[FailureModeAlert]:
        alerts: List[FailureModeAlert] = []

        retention_flattened = metrics.get("retention_curve_flattened", True)
        growth_rate = metrics.get("growth_rate", 0.0)
        if not retention_flattened and growth_rate > 0.30:
            fm, rc, ds, cm = self.FAILURE_TABLE[5]  # Lack of PMF / Premature scaling
            alerts.append(FailureModeAlert(failure_mode=fm, root_cause=rc, detection_signal=ds, correction_mechanism=cm, severity="CRITICAL"))

        cac_growth = metrics.get("cac_growth_rate", 0.0)
        ltv_growth = metrics.get("ltv_growth_rate", 0.0)
        if cac_growth > ltv_growth and growth_rate > 0.20:
            fm, rc, ds, cm = self.FAILURE_TABLE[8]  # Scaling prematurely
            alerts.append(FailureModeAlert(failure_mode=fm, root_cause=rc, detection_signal=ds, correction_mechanism=cm, severity="HIGH"))

        decision_latency = metrics.get("decision_latency_sec", 0.0)
        if decision_latency > 86400:  # > 24 hours
            fm, rc, ds, cm = self.FAILURE_TABLE[6]  # Org bottlenecks
            alerts.append(FailureModeAlert(failure_mode=fm, root_cause=rc, detection_signal=ds, correction_mechanism=cm, severity="HIGH"))

        burn_multiple = metrics.get("burn_multiple", 1.0)
        if burn_multiple > 3.0:
            fm, rc, ds, cm = self.FAILURE_TABLE[9]  # Capital misallocation
            alerts.append(FailureModeAlert(failure_mode=fm, root_cause=rc, detection_signal=ds, correction_mechanism=cm, severity="HIGH"))

        return alerts


# =====================================================================
# 9. Master Engine Orchestrator (§10)
# =====================================================================
class FirstPrinciplesEOSEngine:
    """Master orchestrator integrating sensing, decision tree, business loops, GTM, moats, and state machine."""

    def __init__(self) -> None:
        self.state_machine = EOSStateMachine()
        self.decision_tree = OpportunityDecisionTree()
        self.business_loops = CoupledBusinessLoopsEngine()
        self.customer_lifecycle = CustomerLifecycleEngine()
        self.gtm_engine = GTMSystemEngine()
        self.growth_classifier = GrowthStageClassifier()
        self.moat_engine = StrategicMoatEngine()
        self.failure_monitor = FailureModeMonitor()

    def run_cycle(self, opportunity_inputs: Dict[str, Any], operational_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Runs a complete first-principles sensing, decision, simulation, and diagnostic cycle."""
        # 1. Evaluate Decision Tree (§10.2)
        dt_res = self.decision_tree.evaluate(
            is_structural_anomaly=opportunity_inputs.get("is_structural_anomaly", True),
            is_reversible=opportunity_inputs.get("is_reversible", True),
            high_confidence_signals=opportunity_inputs.get("high_confidence_signals", True),
            cheap_test_available=opportunity_inputs.get("cheap_test_available", True),
            cheap_test_passed=opportunity_inputs.get("cheap_test_passed", True),
            expected_value_positive=opportunity_inputs.get("expected_value_positive", True),
            structural_advantage=opportunity_inputs.get("structural_advantage", True),
        )

        # 2. State machine transition based on decision
        if dt_res.decision == "COMMIT_RESOURCES":
            if self.state_machine.current_state == EOSState.SENSING:
                self.state_machine.transition_to(EOSState.HYPOTHESIS, "Anomaly detected & hypothesis formed")
                self.state_machine.transition_to(EOSState.CHEAP_TEST, "Cheap test initiated")
                self.state_machine.transition_to(EOSState.VALIDATION, "Test strengthened belief")
                self.state_machine.transition_to(EOSState.BUILD_GATE, "Economic viability confirmed")
                self.state_machine.transition_to(EOSState.MVP, "MVP resourced")
                self.state_machine.transition_to(EOSState.GTM_TEST, "Shipped to GTM test")
                self.state_machine.transition_to(EOSState.KILL_OR_SCALE, "Signal collected")
                self.state_machine.transition_to(EOSState.SCALE, "Above threshold -> Scale")
                self.state_machine.transition_to(EOSState.OPERATE, "Repeatable loop confirmed")

        # 3. Simulate Coupled Business Loops
        loops_state = self.business_loops.update_loops(operational_metrics)

        # 4. GTM Alignment
        gtm_res = self.gtm_engine.evaluate_motion(
            acv_cents=operational_metrics.get("acv_cents", 120000),
            complexity=operational_metrics.get("complexity", "medium"),
            has_network_effects=operational_metrics.get("has_network_effects", False),
        )

        # 5. Growth Stage Classification
        growth_stage = self.growth_classifier.classify(operational_metrics)

        # 6. Moat Analysis
        moat_res = self.moat_engine.score_moats(
            network_effects_score=operational_metrics.get("network_effects_score", 0.5),
            switching_costs_cents=operational_metrics.get("switching_costs_cents", 5000_00),
            scale_economies_score=operational_metrics.get("scale_economies_score", 0.4),
            brand_trust_score=self.business_loops.stocks.brand_trust_score,
            counter_positioning_score=operational_metrics.get("counter_positioning_score", 0.6),
        )

        # 7. Failure Mode Monitoring
        failure_alerts = self.failure_monitor.audit(operational_metrics)

        return {
            "current_eos_state": self.state_machine.current_state.value,
            "decision_tree_result": dt_res.model_dump(),
            "business_loops_summary": {k: v.kpis for k, v in loops_state.items()},
            "gtm_recommendation": gtm_res,
            "growth_stage": growth_stage.model_dump(),
            "moat_analysis": moat_res,
            "failure_alerts": [a.model_dump() for a in failure_alerts],
            "system_stocks": self.business_loops.stocks.model_dump(),
        }
