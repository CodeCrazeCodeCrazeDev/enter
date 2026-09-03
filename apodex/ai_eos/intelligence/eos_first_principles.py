"""
The Entrepreneurial Operating System (EOS) First-Principles Engine.

A executable Python implementation of the 11-section Entrepreneurial
Operating System specification for elite founder decision-making, coupled loop
simulation, customer lifecycle dynamics, growth stage classification, failure mode
diagnostics, and AI-driven autonomous research & execution.
"""

from __future__ import annotations
import math
import logging
from enum import Enum
from typing import Dict, Any, List, Tuple, Optional, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger("apodex.ai_eos.eos_first_principles")


# ============================================================================
# Section 10.1: System State Machine
# ============================================================================

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


class EOSStateMachine(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    current_state: EOSState = EOSState.SENSING
    history: List[Tuple[EOSState, str]] = Field(default_factory=list)

    # Valid transitions matching §10.1 state diagram
    VALID_TRANSITIONS: Dict[EOSState, Set[EOSState]] = {
        EOSState.SENSING: {EOSState.HYPOTHESIS, EOSState.DISCARD},
        EOSState.HYPOTHESIS: {EOSState.CHEAP_TEST, EOSState.DISCARD},
        EOSState.CHEAP_TEST: {EOSState.VALIDATION, EOSState.DISCARD, EOSState.SENSING},
        EOSState.VALIDATION: {EOSState.BUILD_GATE, EOSState.DISCARD},
        EOSState.BUILD_GATE: {EOSState.MVP, EOSState.DISCARD},
        EOSState.MVP: {EOSState.GTM_TEST, EOSState.DISCARD},
        EOSState.GTM_TEST: {EOSState.KILL_OR_SCALE, EOSState.DISCARD},
        EOSState.KILL_OR_SCALE: {EOSState.SCALE, EOSState.DISCARD, EOSState.SENSING},
        EOSState.SCALE: {EOSState.OPERATE, EOSState.DISCARD},
        EOSState.OPERATE: {EOSState.REINVENT, EOSState.SENSING},
        EOSState.REINVENT: {EOSState.SENSING, EOSState.HYPOTHESIS},
        EOSState.DISCARD: {EOSState.SENSING},
    }

    def can_transition(self, target_state: EOSState) -> bool:
        allowed = self.VALID_TRANSITIONS.get(self.current_state, set())
        return target_state in allowed

    def transition_to(self, target_state: EOSState, reason: str = "") -> bool:
        if self.can_transition(target_state):
            old = self.current_state
            self.current_state = target_state
            self.history.append((target_state, f"From {old.value}: {reason}"))
            logger.info(f"EOS State Machine transitioned from {old.value} to {target_state.value}. Reason: {reason}")
            return True
        else:
            logger.warning(f"Invalid EOS state transition from {self.current_state.value} to {target_state.value}")
            return False


# ============================================================================
# Section 2: Internal Cognitive Loops & Signal Pipeline
# ============================================================================

class DecisionRiskType(str, Enum):
    TYPE_I = "Type_I_Irreversible"   # Slow, high scrutiny deliberation
    TYPE_II = "Type_II_Reversible"   # Quick, cheap experiments


class WeakSignal(BaseModel):
    signal_id: UUID = Field(default_factory=uuid4)
    description: str
    is_structural_shift: bool
    source: str = "Market Signal"
    confidence: float = 0.5


class FalsifiableHypothesis(BaseModel):
    hypothesis_id: UUID = Field(default_factory=uuid4)
    claim: str
    enabling_condition: str
    kill_threshold: float
    cheap_test_cost_usd: float
    belief_prior: float = 0.5
    belief_posterior: float = 0.5


class MentalModelEvaluator(BaseModel):
    structure_name: str
    parameters: Dict[str, float] = Field(default_factory=dict)
    structural_assumptions: List[str] = Field(default_factory=list)
    falsification_events: int = 0

    def predict_outcome(self, input_signal: float) -> float:
        weight = self.parameters.get("sensitivity", 1.0)
        return input_signal * weight

    def update_parameters(self, actual_outcome: float, predicted_outcome: float, learning_rate: float = 0.1):
        err = actual_outcome - predicted_outcome
        if "sensitivity" in self.parameters:
            self.parameters["sensitivity"] += learning_rate * err
        if abs(err) > 2.0:
            self.falsification_events += 1

    def requires_structural_reinvention(self) -> bool:
        return self.falsification_events >= 3


# ============================================================================
# Section 3: External Business Loops Engine
# ============================================================================

class BusinessLoopName(str, Enum):
    PRODUCT = "Product"
    MARKETING = "Marketing"
    SALES = "Sales"
    CUSTOMER_SUCCESS = "CustomerSuccess"
    BRAND = "Brand"
    PRICING = "Pricing"
    REFERRAL = "Referral"
    DATA = "Data"
    FINANCIAL = "Financial"
    HIRING = "Hiring"
    CULTURE = "Culture"
    INNOVATION = "Innovation"
    COMPETITIVE_INTEL = "CompetitiveIntelligence"


class BusinessLoopState(BaseModel):
    name: BusinessLoopName
    inputs: List[str]
    outputs: List[str]
    feedback_signal: str
    core_kpis: Dict[str, float]
    dominant_failure_mode: str
    compounding_factor: float = 1.0


class ExternalBusinessLoopsEngine(BaseModel):
    loops: Dict[BusinessLoopName, BusinessLoopState] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.loops:
            self._initialize_default_loops()

    def _initialize_default_loops(self):
        defaults = [
            BusinessLoopState(
                name=BusinessLoopName.PRODUCT,
                inputs=["User behavior", "Support tickets", "Usage data"],
                outputs=["Feature changes", "Roadmap"],
                feedback_signal="Activation/retention deltas",
                core_kpis={"retention_curve": 0.60, "nps": 55.0, "feature_adoption": 0.45},
                dominant_failure_mode="Building for loudest customer, not representative one"
            ),
            BusinessLoopState(
                name=BusinessLoopName.MARKETING,
                inputs=["Positioning", "Market data"],
                outputs=["Awareness", "Demand"],
                feedback_signal="CAC, traffic quality, message resonance",
                core_kpis={"cac": 250.0, "brand_recall": 0.30, "conversion_rate": 0.04},
                dominant_failure_mode="Message-market mismatch; scaling spend before message works"
            ),
            BusinessLoopState(
                name=BusinessLoopName.SALES,
                inputs=["Qualified leads", "Product"],
                outputs=["Closed revenue", "Customer feedback"],
                feedback_signal="Win/loss reasons",
                core_kpis={"win_rate": 0.28, "sales_cycle_days": 45.0, "acv": 12000.0},
                dominant_failure_mode="Selling to non-ICP to hit quota"
            ),
            BusinessLoopState(
                name=BusinessLoopName.CUSTOMER_SUCCESS,
                inputs=["Onboarding data", "Usage"],
                outputs=["Retention", "Expansion"],
                feedback_signal="Churn reasons, health scores",
                core_kpis={"nrr": 1.15, "churn_rate": 0.02, "time_to_value_days": 14.0},
                dominant_failure_mode="Success != support; reactive-only CS"
            ),
            BusinessLoopState(
                name=BusinessLoopName.BRAND,
                inputs=["Product experience", "Comms"],
                outputs=["Trust", "Pricing power"],
                feedback_signal="Sentiment, unaided recall",
                core_kpis={"share_of_voice": 0.25, "price_elasticity": 0.8},
                dominant_failure_mode="Brand as decoration, not strategy"
            ),
            BusinessLoopState(
                name=BusinessLoopName.PRICING,
                inputs=["Value delivered", "WTP data"],
                outputs=["Revenue", "Positioning signal"],
                feedback_signal="Conversion by price point, expansion rate",
                core_kpis={"arpu": 500.0, "price_realization": 0.90},
                dominant_failure_mode="Cost-plus pricing instead of value-based"
            ),
            BusinessLoopState(
                name=BusinessLoopName.REFERRAL,
                inputs=["Customer satisfaction", "Incentive design"],
                outputs=["New customer flow"],
                feedback_signal="Referral rate, K-factor",
                core_kpis={"viral_coefficient_k": 0.35, "referral_cac": 50.0},
                dominant_failure_mode="Incentivizing referral volume over referral quality"
            ),
            BusinessLoopState(
                name=BusinessLoopName.DATA,
                inputs=["All system signals"],
                outputs=["Decisions"],
                feedback_signal="Model accuracy vs outcomes",
                core_kpis={"data_latency_hrs": 2.0, "decision_cycle_days": 3.0},
                dominant_failure_mode="Vanity metrics; dashboards no one acts on"
            ),
            BusinessLoopState(
                name=BusinessLoopName.FINANCIAL,
                inputs=["Revenue", "Costs", "Capital"],
                outputs=["Runway", "Reinvestment capacity"],
                feedback_signal="Burn multiple, margin trend",
                core_kpis={"gross_margin": 0.78, "burn_multiple": 1.2, "runway_months": 18.0},
                dominant_failure_mode="Growth at negative unit economics with no path to positive"
            ),
            BusinessLoopState(
                name=BusinessLoopName.HIRING,
                inputs=["Org needs", "Culture"],
                outputs=["Capability", "Capacity"],
                feedback_signal="90-day performance, regretted attrition",
                core_kpis={"time_to_fill_days": 30.0, "retention_rate": 0.92},
                dominant_failure_mode="Hiring for pedigree over role-fit; hiring ahead of proven need"
            ),
            BusinessLoopState(
                name=BusinessLoopName.CULTURE,
                inputs=["Values-in-action", "Incentives"],
                outputs=["Behavior consistency at scale"],
                feedback_signal="Employee sentiment, decision speed",
                core_kpis={"enps": 60.0, "decision_latency_hrs": 12.0},
                dominant_failure_mode="Values-as-poster (stated but not incentivized)"
            ),
            BusinessLoopState(
                name=BusinessLoopName.INNOVATION,
                inputs=["R&D", "Market signals", "Internal ideas"],
                outputs=["New products/features/lines"],
                feedback_signal="Time-to-market, cannibalization rate",
                core_kpis={"experiments_run": 24.0, "hit_rate": 0.25},
                dominant_failure_mode="Innovation theater - activity without shipped bets"
            ),
            BusinessLoopState(
                name=BusinessLoopName.COMPETITIVE_INTEL,
                inputs=["Market/competitor data"],
                outputs=["Strategic repositioning"],
                feedback_signal="Win/loss vs named competitors",
                core_kpis={"relative_share_trend": 0.05, "feature_parity_gap": 0.10},
                dominant_failure_mode="Reacting to competitors instead of running own strategy"
            )
        ]
        for loop in defaults:
            self.loops[loop.name] = loop

    def evaluate_system_health(self) -> Dict[str, Any]:
        """Calculates system-wide leverage points and highlights vulnerable loops."""
        unhealthy_loops = []
        for name, loop in self.loops.items():
            if name == BusinessLoopName.FINANCIAL and loop.core_kpis.get("burn_multiple", 1.0) > 2.5:
                unhealthy_loops.append((name, "High burn multiple"))
            elif name == BusinessLoopName.CUSTOMER_SUCCESS and loop.core_kpis.get("nrr", 1.0) < 1.0:
                unhealthy_loops.append((name, "Net churn (NRR < 100%)"))
            elif name == BusinessLoopName.PRODUCT and loop.core_kpis.get("retention_curve", 0.0) < 0.4:
                unhealthy_loops.append((name, "Poor retention curve"))

        # Coupled leverage impact: ARPU (Pricing) -> Burn Multiple (Financial) -> Hiring
        arpu = self.loops[BusinessLoopName.PRICING].core_kpis.get("arpu", 100.0)
        runway = self.loops[BusinessLoopName.FINANCIAL].core_kpis.get("runway_months", 12.0)
        system_leverage_score = (arpu / 100.0) * (runway / 12.0)

        return {
            "unhealthy_loops": unhealthy_loops,
            "system_leverage_score": system_leverage_score,
            "total_loops_tracked": len(self.loops)
        }


# ============================================================================
# Section 4: Customer Lifecycle Engine
# ============================================================================

class JourneyStage(str, Enum):
    AWARENESS = "Awareness"
    INTEREST = "Interest"
    CONSIDERATION = "Consideration"
    EVALUATION = "Evaluation"
    PURCHASE = "Purchase"
    ONBOARDING = "Onboarding"
    ACTIVATION = "Activation"
    ENGAGEMENT = "Engagement"
    HABIT_FORMATION = "HabitFormation"
    RETENTION = "Retention"
    LOYALTY = "Loyalty"
    ADVOCACY = "Advocacy"
    REFERRAL = "Referral"
    EXPANSION = "Expansion"
    REPURCHASE = "Repurchase"


class StageDetail(BaseModel):
    stage: JourneyStage
    founder_objective: str
    customer_psychology: str
    key_metric: str
    conversion_rate: float = 0.5
    common_mistake: str
    optimization_lever: str


class CustomerLifecycleEngine(BaseModel):
    stages: Dict[JourneyStage, StageDetail] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.stages:
            self._initialize_stages()

    def _initialize_stages(self):
        definitions = [
            StageDetail(
                stage=JourneyStage.AWARENESS,
                founder_objective="Enter consideration set",
                customer_psychology="Pattern-matching against known categories",
                key_metric="Reach, unaided recall",
                conversion_rate=0.20,
                common_mistake="Generic category messaging",
                optimization_lever="Sharp category framing / naming new category"
            ),
            StageDetail(
                stage=JourneyStage.INTEREST,
                founder_objective="Earn attention",
                customer_psychology="Curiosity vs skepticism",
                key_metric="CTR, engagement rate",
                conversion_rate=0.15,
                common_mistake="Feature-dumping",
                optimization_lever="Lead with pain, not product"
            ),
            StageDetail(
                stage=JourneyStage.CONSIDERATION,
                founder_objective="Differentiate",
                customer_psychology="Comparing against status quo",
                key_metric="Time-on-site, content depth",
                conversion_rate=0.25,
                common_mistake="Competing on features competitors have",
                optimization_lever="Reframe comparison axis"
            ),
            StageDetail(
                stage=JourneyStage.EVALUATION,
                founder_objective="Reduce perceived risk",
                customer_psychology="Loss aversion dominates gain-seeking",
                key_metric="Trial starts, demo requests",
                conversion_rate=0.30,
                common_mistake="Ignoring risk-reduction",
                optimization_lever="Make failure cheap and reversible"
            ),
            StageDetail(
                stage=JourneyStage.PURCHASE,
                founder_objective="Convert intent to commitment",
                customer_psychology="Decision fatigue, need for certainty",
                key_metric="Conversion rate",
                conversion_rate=0.40,
                common_mistake="Friction in checkout/contracting",
                optimization_lever="Remove steps, not add persuasion"
            ),
            StageDetail(
                stage=JourneyStage.ONBOARDING,
                founder_objective="Deliver first value fast",
                customer_psychology="Anxiety about wasted decision",
                key_metric="Time-to-first-value",
                conversion_rate=0.70,
                common_mistake="Feature-tour instead of outcome-tour",
                optimization_lever="Anchor onboarding to specific JTBD"
            ),
            StageDetail(
                stage=JourneyStage.ACTIVATION,
                founder_objective="Cross the aha threshold",
                customer_psychology="Forming initial habit loop",
                key_metric="Activation rate",
                conversion_rate=0.65,
                common_mistake="Defining activation as login",
                optimization_lever="Instrument true aha moment via cohorts"
            ),
            StageDetail(
                stage=JourneyStage.ENGAGEMENT,
                founder_objective="Build usage depth",
                customer_psychology="Reinforcement learning",
                key_metric="DAU/MAU, session depth",
                conversion_rate=0.60,
                common_mistake="Metrics that don't correlate with retention",
                optimization_lever="Optimize for behavior predicting retention"
            ),
            StageDetail(
                stage=JourneyStage.HABIT_FORMATION,
                founder_objective="Make usage automatic",
                customer_psychology="Cue-routine-reward loop",
                key_metric="Habit frequency",
                conversion_rate=0.55,
                common_mistake="No external trigger cadence",
                optimization_lever="Build reliable internal + external triggers"
            ),
            StageDetail(
                stage=JourneyStage.RETENTION,
                founder_objective="Prevent churn",
                customer_psychology="Switching cost perception",
                key_metric="Retention curve, churn",
                conversion_rate=0.80,
                common_mistake="Measuring retention only in aggregate",
                optimization_lever="Cohort-level retention curve flattening"
            ),
            StageDetail(
                stage=JourneyStage.LOYALTY,
                founder_objective="Deepen emotional/economic lock-in",
                customer_psychology="Identity alignment with brand",
                key_metric="Repeat purchase rate",
                conversion_rate=0.50,
                common_mistake="Assuming satisfaction = loyalty",
                optimization_lever="Build genuine switching costs"
            ),
            StageDetail(
                stage=JourneyStage.ADVOCACY,
                founder_objective="Convert satisfaction to voice",
                customer_psychology="Social proof-seeking",
                key_metric="NPS, UGC volume",
                conversion_rate=0.25,
                common_mistake="Asking for advocacy before value proven",
                optimization_lever="Ask at peak-value moments"
            ),
            StageDetail(
                stage=JourneyStage.REFERRAL,
                founder_objective="Convert advocacy to acquisition",
                customer_psychology="Trust transfer peer-to-peer",
                key_metric="Viral coefficient (K)",
                conversion_rate=0.20,
                common_mistake="Generic referral programs",
                optimization_lever="Incentive aligned with genuine value"
            ),
            StageDetail(
                stage=JourneyStage.EXPANSION,
                founder_objective="Grow account value",
                customer_psychology="Anchoring to current spend",
                key_metric="Net revenue retention",
                conversion_rate=0.35,
                common_mistake="Under-selling adjacent value",
                optimization_lever="Usage-based expansion triggers"
            ),
            StageDetail(
                stage=JourneyStage.REPURCHASE,
                founder_objective="Sustain lifetime value",
                customer_psychology="Habitual trust",
                key_metric="LTV, repurchase rate",
                conversion_rate=0.75,
                common_mistake="Treating repurchase as passive",
                optimization_lever="Proactive lifecycle marketing"
            )
        ]
        for d in definitions:
            self.stages[d.stage] = d

    def analyze_funnel_bottlenecks(self) -> Dict[str, Any]:
        bottlenecks = []
        for stage, detail in self.stages.items():
            if detail.conversion_rate < 0.25:
                bottlenecks.append({
                    "stage": stage.value,
                    "conversion_rate": detail.conversion_rate,
                    "lever": detail.optimization_lever,
                    "mistake": detail.common_mistake
                })
        return {"bottlenecks": bottlenecks, "count": len(bottlenecks)}


# ============================================================================
# Section 5 & 6: GTM & Company Growth System
# ============================================================================

class GrowthStage(str, Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "PMF"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    MARKET_LEADERSHIP = "MarketLeadership"


class StageConfig(BaseModel):
    stage: GrowthStage
    primary_objective: str
    org_change: str
    decision_making_change: str
    capital_allocation: str
    key_risk: str
    core_metric: str
    binding_constraint: str


class GrowthStageClassifier(BaseModel):
    configs: Dict[GrowthStage, StageConfig] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.configs:
            self._initialize_configs()

    def _initialize_configs(self):
        stage_list = [
            StageConfig(
                stage=GrowthStage.IDEA,
                primary_objective="Falsify or strengthen hypothesis",
                org_change="Founder(s) only",
                decision_making_change="Founder intuition, fast",
                capital_allocation="Near-zero, sweat equity",
                key_risk="Solving a non-problem",
                core_metric="# of validated learnings",
                binding_constraint="Founder time"
            ),
            StageConfig(
                stage=GrowthStage.VALIDATION,
                primary_objective="Prove willingness to pay",
                org_change="First 1-3 hires",
                decision_making_change="Still founder-centric",
                capital_allocation="Pre-seed / seed capital",
                key_risk="False positive validation",
                core_metric="Paying customers / LOIs",
                binding_constraint="Signal quality"
            ),
            StageConfig(
                stage=GrowthStage.STARTUP,
                primary_objective="Build repeatable acquisition",
                org_change="Functional roles emerge",
                decision_making_change="Founder + small team",
                capital_allocation="Seed / Series A",
                key_risk="Premature scaling before PMF",
                core_metric="CAC:LTV early signal",
                binding_constraint="Cash runway"
            ),
            StageConfig(
                stage=GrowthStage.PMF,
                primary_objective="Reach retention/growth threshold",
                org_change="First managers",
                decision_making_change="Data starts overriding intuition",
                capital_allocation="Growth capital",
                key_risk="Mistaking early traction for PMF",
                core_metric="Retention curve flattening",
                binding_constraint="Team bandwidth"
            ),
            StageConfig(
                stage=GrowthStage.GROWTH,
                primary_objective="Scale what works",
                org_change="Middle management layer",
                decision_making_change="Process + data-driven",
                capital_allocation="Series B/C",
                key_risk="Scaling a broken funnel",
                core_metric="Growth rate, CAC payback",
                binding_constraint="Hiring velocity"
            ),
            StageConfig(
                stage=GrowthStage.SCALE,
                primary_objective="Institutionalize repeatability",
                org_change="Departments, specialized functions",
                decision_making_change="Delegated, framework-driven",
                capital_allocation="Efficient growth capital",
                key_risk="Culture dilution, bureaucracy",
                core_metric="Rule of 40, NRR",
                binding_constraint="Org coordination cost"
            ),
            StageConfig(
                stage=GrowthStage.PLATFORM,
                primary_objective="Enable others to build on you",
                org_change="Platform/ecosystem teams",
                decision_making_change="Governance structures, APIs-as-product",
                capital_allocation="Infrastructure investment",
                key_risk="Platform without ecosystem demand",
                core_metric="Third-party developer activity",
                binding_constraint="Trust from partners"
            ),
            StageConfig(
                stage=GrowthStage.ECOSYSTEM,
                primary_objective="Orchestrate multi-sided network",
                org_change="Ecosystem management, BD at scale",
                decision_making_change="Distributed decision rights",
                capital_allocation="Strategic / M&A capital",
                key_risk="Ecosystem fragmentation",
                core_metric="Ecosystem GMV / network density",
                binding_constraint="Governance credibility"
            ),
            StageConfig(
                stage=GrowthStage.MARKET_LEADERSHIP,
                primary_objective="Defend and extend category",
                org_change="Full corporate structure",
                decision_making_change="Board-level governance",
                capital_allocation="Diversified capital",
                key_risk="Complacency, disruption from below",
                core_metric="Category share, moat durability",
                binding_constraint="Innovation velocity"
            )
        ]
        for cfg in stage_list:
            self.configs[cfg.stage] = cfg

    def classify_current_stage(self, metrics: Dict[str, float]) -> StageConfig:
        paying_cust = metrics.get("paying_customers", 0)
        retention_flat = metrics.get("retention_flattened", 0.0)
        arr = metrics.get("arr_usd", 0.0)
        dev_activity = metrics.get("developer_activity", 0.0)

        if dev_activity > 1000 and arr > 50_000_000:
            return self.configs[GrowthStage.PLATFORM]
        elif arr > 10_000_000:
            return self.configs[GrowthStage.SCALE]
        elif arr > 1_000_000 and retention_flat >= 1.0:
            return self.configs[GrowthStage.GROWTH]
        elif retention_flat >= 1.0:
            return self.configs[GrowthStage.PMF]
        elif paying_cust > 0:
            return self.configs[GrowthStage.STARTUP]
        elif metrics.get("validated_learnings", 0) > 0:
            return self.configs[GrowthStage.VALIDATION]
        else:
            return self.configs[GrowthStage.IDEA]


class GTMSystemEngine(BaseModel):
    positioning: str = "Category Framing"
    pricing_model: str = "Value-based"
    primary_channel: str = "PLG"

    def select_optimal_channel(self, product_complexity: float, price_level_usd: float) -> str:
        """
        Determines channel selection:
        Low complexity / low price -> PLG / Content / Organic
        High complexity / high price -> Enterprise Sales (SLG)
        Network effects -> Community-Led (CLG)
        """
        if product_complexity > 0.7 or price_level_usd > 25000:
            return "Sales-Led Growth (Enterprise SLG)"
        elif product_complexity < 0.3 and price_level_usd < 1000:
            return "Product-Led Growth (PLG) & Organic"
        else:
            return "Hybrid PLG + Mid-Market Sales"


# ============================================================================
# Section 10.2: Opportunity Decision Tree
# ============================================================================

class OpportunityDecisionTree(BaseModel):

    def evaluate(
        self,
        is_structural_anomaly: bool,
        is_reversible_decision: bool,
        high_confidence_multi_source_signal: bool = False,
        cheap_test_available: bool = True,
        cheap_test_exceeds_kill_threshold: bool = True,
        expected_value_clearly_positive: bool = True,
        has_structural_advantage: bool = True
    ) -> Dict[str, Any]:
        """
        Executes section 10.2 flowchart decision logic.
        """
        audit_trail = []

        # Q1: Structural anomaly or just noise?
        if not is_structural_anomaly:
            audit_trail.append("Q1: Noise detected -> Discard")
            return {"decision": "Discard", "reason": "Not a structural anomaly", "audit": audit_trail}
        audit_trail.append("Q1: Structural anomaly confirmed")

        # Q2: Reversible decision?
        if not is_reversible_decision:
            audit_trail.append("Q2: Irreversible decision (Type I)")
            if not high_confidence_multi_source_signal:
                audit_trail.append("Q2a: Lack of high-confidence multi-source signal -> Discard")
                return {"decision": "Discard", "reason": "Type I decision lacks high-confidence multi-source signal", "audit": audit_trail}
            audit_trail.append("Q2a: High-confidence multi-source signal verified")
        else:
            audit_trail.append("Q2: Reversible decision (Type II)")

        # Q3: Cheap test available?
        if cheap_test_available:
            audit_trail.append("Q3: Cheap test executed")
            if not cheap_test_exceeds_kill_threshold:
                audit_trail.append("Q4: Cheap test failed kill threshold -> Discard")
                return {"decision": "Discard", "reason": "Cheap test failed kill threshold", "audit": audit_trail}
            audit_trail.append("Q4: Cheap test passed kill threshold")
        else:
            audit_trail.append("Q3: No cheap test available")
            if not expected_value_clearly_positive:
                audit_trail.append("Q4b: Expected value not clearly positive -> Discard")
                return {"decision": "Discard", "reason": "Expected value not clearly positive", "audit": audit_trail}
            audit_trail.append("Q4b: Positive expected value verified")

        # Q5: Structural advantage?
        if not has_structural_advantage:
            audit_trail.append("Q5: No structural advantage -> Discard")
            return {"decision": "Discard", "reason": "No structural advantage or moat buildability", "audit": audit_trail}

        audit_trail.append("Q5: Structural advantage confirmed -> Commit Resources")
        return {"decision": "Commit Resources", "reason": "All decision criteria satisfied", "audit": audit_trail}


# ============================================================================
# Section 8: Failure Mode Monitor
# ============================================================================

class FailureModeMonitor(BaseModel):
    FAILURE_MODES: List[Dict[str, str]] = [
        {"mode": "Solving the wrong problem", "root_cause": "Skipped root-cause analysis; solved symptom", "signal": "Low engagement despite positive survey feedback", "correction": "Return to root cause JTBD interviews"},
        {"mode": "Building before validating", "root_cause": "Founder conviction substituted for evidence", "signal": "High build velocity, flat demand signal", "correction": "Enforce validation gate before build resourcing"},
        {"mode": "Weak positioning", "root_cause": "No clear 'instead of X, use us because Y'", "signal": "High CAC, long sales cycles, feature objections", "correction": "Rebuild positioning around real customer alternative"},
        {"mode": "Poor pricing", "root_cause": "Cost-plus instead of value-based pricing", "signal": "High conversion at low price, poor margin/expansion", "correction": "Re-anchor price to quantified value"},
        {"mode": "Distribution failure", "root_cause": "Great product, no repeatable channel", "signal": "High NPS, flat growth", "correction": "Systematically test channels against ICP behavior"},
        {"mode": "Lack of product-market fit", "root_cause": "Premature scaling of unproven loop", "signal": "Retention curve never flattens", "correction": "Stop scaling; return to cohort retention work"},
        {"mode": "Organizational bottlenecks", "root_cause": "Decision rights not delegated as company scales", "signal": "Rising decision latency, founder bottleneck", "correction": "Push decision rights down with clear frameworks"},
        {"mode": "Founder bias", "root_cause": "Overconfidence, confirmation bias, sunk cost", "signal": "Ignoring disconfirming data", "correction": "Pre-committed kill criteria set before launch"},
        {"mode": "Scaling prematurely", "root_cause": "Confusing early demand spike with durable PMF", "signal": "CAC rising faster than LTV as spend scales", "correction": "Re-test unit economics at each order of magnitude"},
        {"mode": "Capital misallocation", "root_cause": "No opportunity-cost discipline in budgeting", "signal": "Multiple underperforming bets funded simultaneously", "correction": "Rank all initiatives on expected-return basis quarterly"}
    ]

    def audit_metrics(self, operating_metrics: Dict[str, float]) -> List[Dict[str, str]]:
        alerts = []
        if operating_metrics.get("retention_curve_slope", -0.1) < -0.05:
            alerts.append(self.FAILURE_MODES[5]) # Lack of PMF
        if operating_metrics.get("cac_to_ltv_growth_ratio", 1.0) > 1.8:
            alerts.append(self.FAILURE_MODES[8]) # Premature scaling
        if operating_metrics.get("decision_latency_days", 1.0) > 7.0:
            alerts.append(self.FAILURE_MODES[6]) # Org bottlenecks
        if operating_metrics.get("simultaneous_underperforming_bets", 0) >= 3:
            alerts.append(self.FAILURE_MODES[9]) # Capital misallocation
        return alerts


# ============================================================================
# Section 10.3: Master AI-Driven Entrepreneurial System Engine
# ============================================================================

class FirstPrinciplesEOSEngine(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    state_machine: EOSStateMachine = Field(default_factory=EOSStateMachine)
    business_loops: ExternalBusinessLoopsEngine = Field(default_factory=ExternalBusinessLoopsEngine)
    customer_lifecycle: CustomerLifecycleEngine = Field(default_factory=CustomerLifecycleEngine)
    growth_classifier: GrowthStageClassifier = Field(default_factory=GrowthStageClassifier)
    gtm_engine: GTMSystemEngine = Field(default_factory=GTMSystemEngine)
    decision_tree: OpportunityDecisionTree = Field(default_factory=OpportunityDecisionTree)
    failure_monitor: FailureModeMonitor = Field(default_factory=FailureModeMonitor)
    mental_model: MentalModelEvaluator = Field(default_factory=lambda: MentalModelEvaluator(structure_name="Core Venture Strategy", parameters={"sensitivity": 1.0}))

    active_hypotheses: List[FalsifiableHypothesis] = Field(default_factory=list)

    def process_signal(self, signal: WeakSignal) -> Dict[str, Any]:
        """Sensing Agent + Hypothesis Engine pipeline (§10.3)."""
        if not signal.is_structural_shift:
            logger.info(f"Signal '{signal.description}' filtered out as non-structural noise.")
            return {"status": "discarded", "reason": "Signal is noise"}

        # Form falsifiable hypothesis
        hyp = FalsifiableHypothesis(
            claim=f"Structural shift from: {signal.description}",
            enabling_condition="Enabling cost curve threshold crossed",
            kill_threshold=0.6,
            cheap_test_cost_usd=500.0,
            belief_prior=signal.confidence
        )
        self.active_hypotheses.append(hyp)
        self.state_machine.transition_to(EOSState.HYPOTHESIS, reason="Anomaly detected & hypothesis formed")
        return {"status": "hypothesis_formed", "hypothesis": hyp}

    def evaluate_opportunity(
        self,
        hypothesis: FalsifiableHypothesis,
        is_reversible: bool = True,
        high_confidence: bool = False,
        test_result: float = 0.8,
        has_moat: bool = True
    ) -> Dict[str, Any]:
        """Validation Agent + Decision Tree execution (§10.2 & §10.3)."""
        self.state_machine.transition_to(EOSState.CHEAP_TEST, reason="Running cheap test")

        passed_test = test_result >= hypothesis.kill_threshold

        decision_result = self.decision_tree.evaluate(
            is_structural_anomaly=True,
            is_reversible_decision=is_reversible,
            high_confidence_multi_source_signal=high_confidence,
            cheap_test_available=True,
            cheap_test_exceeds_kill_threshold=passed_test,
            expected_value_clearly_positive=True,
            has_structural_advantage=has_moat
        )

        if decision_result["decision"] == "Commit Resources":
            self.state_machine.transition_to(EOSState.VALIDATION, reason="Cheap test passed")
            self.state_machine.transition_to(EOSState.BUILD_GATE, reason="Economic viability confirmed")
            self.state_machine.transition_to(EOSState.MVP, reason="Resources allocated to MVP")
        else:
            self.state_machine.transition_to(EOSState.DISCARD, reason=decision_result["reason"])

        return decision_result

    def run_kpi_stack(self) -> Dict[str, Any]:
        """Rolled up KPI stack across all subsystems (§10.4)."""
        loops_health = self.business_loops.evaluate_system_health()
        funnel = self.customer_lifecycle.analyze_funnel_bottlenecks()
        return {
            "current_state": self.state_machine.current_state.value,
            "system_leverage_score": loops_health["system_leverage_score"],
            "unhealthy_loops": loops_health["unhealthy_loops"],
            "funnel_bottlenecks_count": funnel["count"],
            "active_hypotheses_count": len(self.active_hypotheses)
        }
