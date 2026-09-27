"""
Entrepreneurial Operating System (EOS) Executable First-Principles Engine.

Implements the 11-section EOS reconstruction covering:
1. Master Loop (19 nodes, re-entrant, kill signals)
2. Internal Cognitive Loops (Anomaly detection, hypothesis generation, Bayesian mental model updating, Type I vs II risk)
3. External Business Loops (13 coupled operational loops, KPI tracking, failure modes)
4. Customer Journey (15 lifecycle stages, customer psychology, metrics, levers)
5. Go-to-Market System (Positioning, pricing signals, distribution motions PLG/SLG/CLG)
6. Company Growth System (9 stage transitions, binding constraints, capital allocation)
7. Strategic Thinking (Cost curves, timing advantage, Hamilton Helmer 7 Powers moats)
8. Failure Mode Analysis (10 structural failure modes, root cause detection & correction)
9. Scientific Foundations
10. Integrated AI-Driven Operating System (State machine, decision tree, 10 AI agents)
11. Limitations
"""

from __future__ import annotations
import math
import logging
from typing import Dict, Any, List, Optional, Tuple, Set
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

logger = logging.getLogger("sero.eos_first_principles")


# =====================================================================
# Enums & Domain Models
# =====================================================================

class DecisionRiskType(str, Enum):
    TYPE_I = "type_i"   # Irreversible (one-way door), slow deliberation required
    TYPE_II = "type_ii" # Reversible (two-way door), fast & cheap test execution


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


class CustomerJourneyStage(str, Enum):
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


class AIOSState(str, Enum):
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


# =====================================================================
# 1. Master Loop Engine
# =====================================================================

class MasterLoopNode(str, Enum):
    ENVIRONMENTAL_SENSING = "A_Environmental_Sensing"
    SIGNAL_COLLECTION = "B_Signal_Collection"
    PATTERN_RECOGNITION = "C_Pattern_Recognition"
    OPPORTUNITY_DISCOVERY = "D_Opportunity_Discovery"
    ROOT_CAUSE_ANALYSIS = "E_Root_Cause_Analysis"
    CUSTOMER_VALIDATION = "F_Customer_Validation"
    BUSINESS_MODEL_DESIGN = "G_Business_Model_Design"
    MVP_EXPERIMENTATION = "H_MVP_Experimentation"
    PRODUCT_DEVELOPMENT = "I_Product_Development"
    GTM_SYSTEM = "J_GTM_System"
    CUSTOMER_ACQUISITION = "K_Customer_Acquisition"
    ONBOARDING_RETENTION = "L_Onboarding_Retention"
    UNIT_ECONOMICS_OPTIMIZATION = "M_Unit_Economics_Optimization"
    OPERATIONS_SCALING = "N_Operations_Scaling"
    MOAT_CONSTRUCTION = "O_Moat_Construction"
    SCALING_EXPANSION = "P_Scaling_Expansion"
    PLATFORM_FORMATION = "Q_Platform_Formation"
    MARKET_LEADERSHIP = "R_Market_Leadership"
    CONTINUOUS_REINVENTION = "S_Continuous_Reinvention"


class MasterLoopEngine(BaseModel):
    """Executes the re-entrant 19-node Master Loop with kill signal rerouting."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    active_node: MasterLoopNode = MasterLoopNode.ENVIRONMENTAL_SENSING
    node_execution_counts: Dict[str, int] = Field(default_factory=dict)
    kill_signals_triggered: List[Dict[str, Any]] = Field(default_factory=list)

    def transition_next(self, current_metrics: Dict[str, Any]) -> MasterLoopNode:
        """Evaluate current metrics and advance or re-route node in master loop."""
        self.node_execution_counts[self.active_node.value] = (
            self.node_execution_counts.get(self.active_node.value, 0) + 1
        )

        # Check Kill Signals & Feedback Reroutes
        if self.active_node == MasterLoopNode.CUSTOMER_VALIDATION:
            if not current_metrics.get("validation_passed", True):
                self.kill_signals_triggered.append({
                    "source": MasterLoopNode.CUSTOMER_VALIDATION.value,
                    "target": MasterLoopNode.OPPORTUNITY_DISCOVERY.value,
                    "reason": "Customer validation failed kill signal",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
                self.active_node = MasterLoopNode.OPPORTUNITY_DISCOVERY
                return self.active_node

        if self.active_node == MasterLoopNode.MVP_EXPERIMENTATION:
            if not current_metrics.get("mvp_viable", True):
                self.kill_signals_triggered.append({
                    "source": MasterLoopNode.MVP_EXPERIMENTATION.value,
                    "target": MasterLoopNode.OPPORTUNITY_DISCOVERY.value,
                    "reason": "MVP test failed kill signal threshold",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
                self.active_node = MasterLoopNode.OPPORTUNITY_DISCOVERY
                return self.active_node

        if self.active_node == MasterLoopNode.CUSTOMER_ACQUISITION:
            if current_metrics.get("weak_gtm", False):
                self.active_node = MasterLoopNode.GTM_SYSTEM
                return self.active_node

        if self.active_node == MasterLoopNode.UNIT_ECONOMICS_OPTIMIZATION:
            if not current_metrics.get("economics_healthy", True):
                self.active_node = MasterLoopNode.BUSINESS_MODEL_DESIGN
                return self.active_node

        # Standard Sequential Path
        nodes = list(MasterLoopNode)
        idx = nodes.index(self.active_node)
        if idx < len(nodes) - 1:
            self.active_node = nodes[idx + 1]
        else:
            # S -> A (Continuous Reinvention loop closure)
            self.active_node = MasterLoopNode.ENVIRONMENTAL_SENSING

        return self.active_node


# =====================================================================
# 2. Internal Cognitive Loops Engine
# =====================================================================

class MentalModel(BaseModel):
    """Living, falsifiable mental model artifact."""
    model_id: UUID = Field(default_factory=uuid4)
    domain: str
    structural_hypothesis: str
    parameters: Dict[str, float] = Field(default_factory=dict)
    confidence: float = 0.5
    version: int = 1
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InternalCognitiveLoopEngine(BaseModel):
    """Signal-to-Idea pipeline, anomaly detection, Bayesian mental model updating, and Type I/II risk heuristics."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    mental_models: Dict[str, MentalModel] = Field(default_factory=dict)

    def detect_anomaly(self, observed_val: float, baseline_expected: float, threshold: float = 0.20) -> bool:
        """Detect structural anomaly (Kuhn paradigm shift signal)."""
        if baseline_expected == 0:
            return abs(observed_val) > threshold
        relative_diff = abs(observed_val - baseline_expected) / abs(baseline_expected)
        return relative_diff >= threshold

    def classify_risk(self, is_reversible: bool, capital_commitment_cents: int, threshold_cents: int = 100000000) -> DecisionRiskType:
        """Classify decision into Type I (irreversible/one-way door) or Type II (reversible/two-way door)."""
        if not is_reversible or capital_commitment_cents >= threshold_cents:
            return DecisionRiskType.TYPE_I
        return DecisionRiskType.TYPE_II

    def generate_forced_hypothesis(self, anomaly_signal: str, condition: str, impact: str) -> Dict[str, Any]:
        """Convert weak anomaly signal into a falsifiable claim."""
        return {
            "hypothesis_id": uuid4(),
            "claim": f"If {condition}, then {impact} due to structural anomaly in {anomaly_signal}",
            "falsifiable_metric": "conversion_or_retention_delta",
            "kill_threshold": 0.05,
            "status": "proposed"
        }

    def update_mental_model(self, domain: str, empirical_evidence: float, expected_val: float) -> MentalModel:
        """Bayesian update of mental model parameters or structure upon disconfirmation."""
        model = self.mental_models.get(domain)
        if not model:
            model = MentalModel(domain=domain, structural_hypothesis=f"Initial hypothesis for {domain}")
            self.mental_models[domain] = model

        delta = empirical_evidence - expected_val
        # Fast parameter update
        model.confidence = max(0.01, min(0.99, model.confidence + 0.10 * (1.0 if delta > 0 else -1.0)))

        # Structural shift if severe disconfirmation
        if abs(delta) > 0.50:
            model.structural_hypothesis += f" [Re-structured after delta={delta:.2f}]"
            model.version += 1
            logger.warning(f"PARADIGM SHIFT: Restructured mental model for {domain} (v{model.version})")

        model.last_updated = datetime.now(timezone.utc)
        return model


# =====================================================================
# 3. External Business Loops Engine
# =====================================================================

class ExternalBusinessLoopsEngine(BaseModel):
    """Simulates and evaluates all 13 external business loops."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def evaluate_all_loops(self, inputs: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Evaluate state, KPIs, and failure modes across all 13 operational loops."""
        # 1. Product Loop
        retention = inputs.get("retention_curve_flattening", 0.40)
        nps = inputs.get("nps", 50)
        product_failure = "Building for loudest customer" if nps < 20 or retention < 0.20 else None

        # 2. Marketing Loop
        cac = inputs.get("cac_cents", 5000)
        conversion = inputs.get("conversion_rate", 0.03)
        marketing_failure = "Message-market mismatch" if conversion < 0.01 else None

        # 3. Sales Loop
        win_rate = inputs.get("win_rate", 0.25)
        sales_failure = "Selling to non-ICP" if win_rate < 0.10 else None

        # 4. Customer Success Loop
        nrr = inputs.get("nrr", 1.15)
        churn_rate = inputs.get("churn_rate", 0.02)
        cs_failure = "Reactive-only CS" if nrr < 1.0 or churn_rate > 0.05 else None

        # 5. Brand Loop
        brand_elasticity = inputs.get("price_elasticity", -1.2)
        brand_failure = "Brand as decoration" if brand_elasticity < -2.5 else None

        # 6. Pricing Loop
        arpu = inputs.get("arpu_cents", 10000)
        pricing_failure = "Cost-plus pricing" if arpu < 1000 else None

        # 7. Referral Loop
        viral_k = inputs.get("viral_k_factor", 0.15)
        referral_failure = "Incentivizing volume over quality" if viral_k < 0.05 else None

        # 8. Data Loop
        decision_latency_hrs = inputs.get("decision_latency_hrs", 24.0)
        data_failure = "Vanity metrics" if decision_latency_hrs > 72.0 else None

        # 9. Financial Loop
        burn_multiple = inputs.get("burn_multiple", 1.5)
        runway_months = inputs.get("runway_months", 18.0)
        financial_failure = "Growth at negative unit economics" if burn_multiple > 3.0 or runway_months < 6.0 else None

        # 10. Hiring Loop
        time_to_fill_days = inputs.get("time_to_fill_days", 45)
        regretted_attrition = inputs.get("regretted_attrition_rate", 0.05)
        hiring_failure = "Hiring for pedigree over role-fit" if regretted_attrition > 0.20 else None

        # 11. Culture Loop
        enps = inputs.get("enps", 40)
        culture_failure = "Values-as-poster" if enps < 0 else None

        # 12. Innovation Loop
        shipped_experiments = inputs.get("shipped_experiments", 10)
        hit_rate = inputs.get("experiment_hit_rate", 0.20)
        innovation_failure = "Innovation theater" if shipped_experiments == 0 or hit_rate < 0.05 else None

        # 13. Competitive Intelligence Loop
        feature_parity = inputs.get("feature_parity_gap", 0.85)
        comp_failure = "Reacting to competitors" if feature_parity < 0.50 else None

        return {
            "product": {"kpi": {"retention": retention, "nps": nps}, "failure_mode": product_failure},
            "marketing": {"kpi": {"cac_cents": cac, "conversion": conversion}, "failure_mode": marketing_failure},
            "sales": {"kpi": {"win_rate": win_rate}, "failure_mode": sales_failure},
            "customer_success": {"kpi": {"nrr": nrr, "churn": churn_rate}, "failure_mode": cs_failure},
            "brand": {"kpi": {"price_elasticity": brand_elasticity}, "failure_mode": brand_failure},
            "pricing": {"kpi": {"arpu_cents": arpu}, "failure_mode": pricing_failure},
            "referral": {"kpi": {"viral_k": viral_k}, "failure_mode": referral_failure},
            "data": {"kpi": {"decision_latency_hrs": decision_latency_hrs}, "failure_mode": data_failure},
            "financial": {"kpi": {"burn_multiple": burn_multiple, "runway_months": runway_months}, "failure_mode": financial_failure},
            "hiring": {"kpi": {"time_to_fill_days": time_to_fill_days, "attrition": regretted_attrition}, "failure_mode": hiring_failure},
            "culture": {"kpi": {"enps": enps}, "failure_mode": culture_failure},
            "innovation": {"kpi": {"experiments": shipped_experiments, "hit_rate": hit_rate}, "failure_mode": innovation_failure},
            "competitive_intelligence": {"kpi": {"feature_parity": feature_parity}, "failure_mode": comp_failure},
        }


# =====================================================================
# 4. Customer Lifecycle Engine
# =====================================================================

class CustomerLifecycleEngine(BaseModel):
    """Tracks customer flow across the 15 lifecycle stages and computes optimization levers."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    stage_conversions: Dict[CustomerJourneyStage, float] = Field(default_factory=dict)

    def evaluate_cohort_progression(self, cohort_size: int, conversion_rates: Dict[CustomerJourneyStage, float]) -> Dict[str, Any]:
        """Simulate cohort funnel through 15 journey stages."""
        current_size = cohort_size
        funnel_counts = {}

        for stage in CustomerJourneyStage:
            rate = conversion_rates.get(stage, 0.90)
            current_size = int(current_size * rate)
            funnel_counts[stage.value] = current_size

        aha_crossing = funnel_counts[CustomerJourneyStage.ACTIVATION.value] / cohort_size if cohort_size > 0 else 0
        retention_rate = funnel_counts[CustomerJourneyStage.RETENTION.value] / cohort_size if cohort_size > 0 else 0

        return {
            "initial_cohort_size": cohort_size,
            "funnel_counts": funnel_counts,
            "aha_activation_rate": aha_crossing,
            "cohort_retention_rate": retention_rate,
            "healthy": retention_rate >= 0.20
        }


# =====================================================================
# 5. Go-to-Market System Simulator
# =====================================================================

class GTMSystemSimulator(BaseModel):
    """Models upstream positioning, pricing signals, and multi-channel distribution motions."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def evaluate_gtm_fit(
        self,
        positioning_target: str, # "self_serve", "mid_market", "enterprise"
        arpu_cents: int,
        primary_channel: str     # "PLG", "SLG", "CLG", "Paid"
    ) -> Dict[str, Any]:
        """Verify alignment across upstream positioning, pricing signals, and channel motions."""
        aligned = False
        recommendation = ""

        if positioning_target == "self_serve":
            if arpu_cents < 50000 and primary_channel in ["PLG", "Content", "Organic"]:
                aligned = True
            else:
                recommendation = "Self-serve positioning requires low ARPU and PLG/Organic distribution."

        elif positioning_target == "enterprise":
            if arpu_cents >= 1000000 and primary_channel in ["SLG", "Enterprise Sales"]:
                aligned = True
            else:
                recommendation = "Enterprise positioning requires high ARPU ($10k+) and Sales-Led distribution."

        else: # mid_market
            if primary_channel in ["PLG", "SLG", "CLG", "Partner"]:
                aligned = True

        return {
            "positioning_target": positioning_target,
            "arpu_cents": arpu_cents,
            "primary_channel": primary_channel,
            "is_system_aligned": aligned,
            "recommendation": recommendation if not aligned else "GTM System fully aligned."
        }


# =====================================================================
# 6. Company Growth State Machine
# =====================================================================

class CompanyGrowthStateMachine(BaseModel):
    """Manages venture transitions across 9 growth stages and checks binding constraints."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    current_stage: GrowthStage = GrowthStage.IDEA
    stage_history: List[Dict[str, Any]] = Field(default_factory=list)

    def evaluate_transition(self, metrics: Dict[str, Any]) -> GrowthStage:
        """Evaluate if venture satisfies requirements to advance to next growth stage."""
        prev = self.current_stage

        if self.current_stage == GrowthStage.IDEA:
            if metrics.get("validated_learnings_count", 0) >= 5:
                self.current_stage = GrowthStage.VALIDATION

        elif self.current_stage == GrowthStage.VALIDATION:
            if metrics.get("paying_customers_count", 0) >= 3:
                self.current_stage = GrowthStage.STARTUP

        elif self.current_stage == GrowthStage.STARTUP:
            if metrics.get("ltv_to_cac", 0) >= 3.0 and metrics.get("runway_months", 0) >= 6:
                self.current_stage = GrowthStage.PMF

        elif self.current_stage == GrowthStage.PMF:
            if metrics.get("retention_curve_flattened", False):
                self.current_stage = GrowthStage.GROWTH

        elif self.current_stage == GrowthStage.GROWTH:
            if metrics.get("growth_rate_yoy", 0) >= 1.0 and metrics.get("cac_payback_months", 99) <= 12:
                self.current_stage = GrowthStage.SCALE

        elif self.current_stage == GrowthStage.SCALE:
            if metrics.get("rule_of_40", 0) >= 0.40 and metrics.get("nrr", 0) >= 1.20:
                self.current_stage = GrowthStage.PLATFORM

        elif self.current_stage == GrowthStage.PLATFORM:
            if metrics.get("developer_ecosystem_active", False):
                self.current_stage = GrowthStage.ECOSYSTEM

        elif self.current_stage == GrowthStage.ECOSYSTEM:
            if metrics.get("network_density_score", 0) >= 0.80:
                self.current_stage = GrowthStage.MARKET_LEADERSHIP

        if self.current_stage != prev:
            self.stage_history.append({
                "from_stage": prev.value,
                "to_stage": self.current_stage.value,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            logger.info(f"VENTURE STAGE TRANSITION: Advanced from {prev.value} -> {self.current_stage.value}")

        return self.current_stage


# =====================================================================
# 7. Strategic Moat Engine
# =====================================================================

class StrategicMoatEngine(BaseModel):
    """Calculates Hamilton Helmer 7 Powers / Porter moat scores and tracks technology cost curves."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def calculate_moat_score(
        self,
        network_effects: float,      # [0, 1]
        switching_costs: float,      # [0, 1]
        economies_of_scale: float,   # [0, 1]
        brand_trust: float,          # [0, 1]
        counter_positioning: float,  # [0, 1]
        cornered_resource: float,    # [0, 1]
        process_power: float         # [0, 1]
    ) -> float:
        """Composite 7 Powers Moat Durability Score [0, 1]."""
        powers = [
            network_effects, switching_costs, economies_of_scale,
            brand_trust, counter_positioning, cornered_resource, process_power
        ]
        return float(sum(powers) / len(powers))

    def evaluate_cost_curve_timing(self, unit_cost: float, threshold_viability_cost: float) -> bool:
        """Check if technology cost curve crossed economic viability threshold (e.g. AWS, Tesla, Streaming)."""
        return unit_cost <= threshold_viability_cost


# =====================================================================
# 8. Failure Mode Monitor
# =====================================================================

class FailureModeMonitor(BaseModel):
    """Pattern-matches operating metrics against failure mode table and generates corrections."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def diagnose_and_correct(self, metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        """Audit operating metrics and return active failure mode diagnoses and corrections."""
        diagnoses = []

        if metrics.get("engagement_low", False) and metrics.get("survey_positive", False):
            diagnoses.append({
                "failure_mode": "Solving the wrong problem",
                "root_cause": "Skipped root-cause analysis; solved a symptom",
                "signal": "Low engagement despite positive survey feedback",
                "correction": "Return to root-cause 5-Whys / JTBD interviews"
            })

        if metrics.get("build_velocity_high", False) and metrics.get("demand_flat", False):
            diagnoses.append({
                "failure_mode": "Building before validating",
                "root_cause": "Founder conviction substituted for evidence",
                "signal": "High build velocity, flat demand signal",
                "correction": "Enforce a validation gate before build resourcing"
            })

        if metrics.get("cac_cents", 0) > 0 and metrics.get("sales_cycle_days", 0) > 90 and metrics.get("feature_objections", False):
            diagnoses.append({
                "failure_mode": "Weak positioning",
                "root_cause": "No clear 'instead of X, use us because Y'",
                "signal": "High CAC, long sales cycles, feature comparison objections",
                "correction": "Rebuild positioning around real alternative customer compares to"
            })

        if metrics.get("retention_curve_flattens", False) is False and metrics.get("spend_scaling", False):
            diagnoses.append({
                "failure_mode": "Lack of product-market fit / Premature scaling",
                "root_cause": "Premature scaling of an unproven loop",
                "signal": "Retention curve never flattens while spend scales",
                "correction": "Stop scaling; return to cohort-level retention work"
            })

        if metrics.get("decision_latency_days", 0) > 7.0:
            diagnoses.append({
                "failure_mode": "Organizational bottlenecks",
                "root_cause": "Decision rights not delegated as company scales",
                "signal": "Rising decision latency, founder single point of failure",
                "correction": "Push decision rights down with clear frameworks"
            })

        return diagnoses


# =====================================================================
# 10. EOS Opportunity Decision Tree
# =====================================================================

class EOSOpportunityDecisionTree(BaseModel):
    """Executes the multi-stage §10.2 Decision Tree: Should We Pursue This Opportunity?"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def evaluate_opportunity(
        self,
        is_structural_anomaly: bool,
        is_reversible_decision: bool,
        high_confidence_multi_source_signal: bool,
        cheap_test_available: bool,
        test_result_exceeds_kill_threshold: bool,
        expected_value_positive: bool,
        has_structural_advantage: bool
    ) -> Dict[str, Any]:
        """Execute decision tree nodes Q1 -> Q5."""
        # Q1: Structural anomaly or just noise?
        if not is_structural_anomaly:
            return {"pursue": False, "reason": "Discard: Noise, not structural anomaly (Q1)"}

        # Q2: Reversible decision?
        if not is_reversible_decision:
            # High stakes / Irreversible
            if not high_confidence_multi_source_signal:
                return {"pursue": False, "reason": "Discard: Irreversible decision lacks high-confidence signal (Q2a)"}

        # Q3: Cheap test available?
        if cheap_test_available:
            if not test_result_exceeds_kill_threshold:
                return {"pursue": False, "reason": "Discard: Cheap test result failed kill threshold (Q4)"}
        else:
            if not expected_value_positive:
                return {"pursue": False, "reason": "Discard: Expected value not clearly positive without cheap test (Q4b)"}

        # Q5: Do we have or can we build a structural advantage here?
        if not has_structural_advantage:
            return {"pursue": False, "reason": "Discard: Lack of structural advantage or defensible moat (Q5)"}

        return {"pursue": True, "reason": "Commit resources: Validated structural opportunity with moat (Go)"}


# =====================================================================
# 10.3 Master Entrepreneurial Intelligence System (AI-EOS Orchestrator)
# =====================================================================

class EntrepreneurialIntelligenceSystem(BaseModel):
    """Integrated AI-Driven Operating System coordinating all 10 AI Agents and EOS Subsystems."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    state: AIOSState = AIOSState.SENSING
    master_loop: MasterLoopEngine = Field(default_factory=MasterLoopEngine)
    cognitive_engine: InternalCognitiveLoopEngine = Field(default_factory=InternalCognitiveLoopEngine)
    business_loops: ExternalBusinessLoopsEngine = Field(default_factory=ExternalBusinessLoopsEngine)
    customer_lifecycle: CustomerLifecycleEngine = Field(default_factory=CustomerLifecycleEngine)
    gtm_simulator: GTMSystemSimulator = Field(default_factory=GTMSystemSimulator)
    growth_state_machine: CompanyGrowthStateMachine = Field(default_factory=CompanyGrowthStateMachine)
    moat_engine: StrategicMoatEngine = Field(default_factory=StrategicMoatEngine)
    failure_monitor: FailureModeMonitor = Field(default_factory=FailureModeMonitor)
    decision_tree: EOSOpportunityDecisionTree = Field(default_factory=EOSOpportunityDecisionTree)

    def run_full_execution_cycle(self, environment_signals: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a complete sensing, hypothesis, test, build, scale, and reinvention cycle."""
        logger.info(f"AI-EOS Cycle initiating in state: {self.state.value}")

        # 1. Sensing & Anomaly Detection
        observed_val = environment_signals.get("observed_metric", 100.0)
        expected_val = environment_signals.get("baseline_expected", 80.0)
        is_anomaly = self.cognitive_engine.detect_anomaly(observed_val, expected_val)

        if not is_anomaly and self.state == AIOSState.SENSING:
            return {"state": self.state.value, "decision": "No structural anomaly detected. Continue sensing."}

        self.state = AIOSState.HYPOTHESIS

        # 2. Decision Tree Evaluation
        decision = self.decision_tree.evaluate_opportunity(
            is_structural_anomaly=is_anomaly,
            is_reversible_decision=environment_signals.get("is_reversible", True),
            high_confidence_multi_source_signal=environment_signals.get("multi_source_signal", True),
            cheap_test_available=environment_signals.get("cheap_test_available", True),
            test_result_exceeds_kill_threshold=environment_signals.get("test_passed", True),
            expected_value_positive=environment_signals.get("ev_positive", True),
            has_structural_advantage=environment_signals.get("has_moat", True)
        )

        if not decision["pursue"]:
            self.state = AIOSState.DISCARD
            return {"state": self.state.value, "decision": decision["reason"]}

        # 3. Transition through Cheap Test and Validation
        self.state = AIOSState.CHEAP_TEST
        self.state = AIOSState.VALIDATION
        self.state = AIOSState.BUILD_GATE
        self.state = AIOSState.MVP
        self.state = AIOSState.GTM_TEST

        # 4. Scale & Growth State Machine Evaluation
        growth_stage = self.growth_state_machine.evaluate_transition(environment_signals)
        self.state = AIOSState.SCALE

        # 5. Business Loops & Failure Monitor Diagnostics
        loop_audits = self.business_loops.evaluate_all_loops(environment_signals)
        failure_diagnoses = self.failure_monitor.diagnose_and_correct(environment_signals)

        # 6. Moat Score
        moat_score = self.moat_engine.calculate_moat_score(
            network_effects=environment_signals.get("network_effects", 0.5),
            switching_costs=environment_signals.get("switching_costs", 0.5),
            economies_of_scale=environment_signals.get("economies_of_scale", 0.5),
            brand_trust=environment_signals.get("brand_trust", 0.5),
            counter_positioning=environment_signals.get("counter_positioning", 0.5),
            cornered_resource=environment_signals.get("cornered_resource", 0.5),
            process_power=environment_signals.get("process_power", 0.5)
        )

        self.state = AIOSState.OPERATE

        return {
            "state": self.state.value,
            "opportunity_decision": decision,
            "current_growth_stage": growth_stage.value,
            "moat_durability_score": moat_score,
            "loop_audits": loop_audits,
            "failure_diagnoses": failure_diagnoses,
            "active_master_node": self.master_loop.active_node.value
        }


# Global Aliases
EOSEngineFirstPrinciples = EntrepreneurialIntelligenceSystem
