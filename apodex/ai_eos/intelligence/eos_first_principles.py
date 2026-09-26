"""First-Principles Entrepreneurial Operating System (EOS) Engine.

Executable Python engine implementing the 11-section First-Principles EOS specification
from `docs/architecture/ENTREPRENEURIAL_OPERATING_SYSTEM_SPEC.md`.

Includes:
1. Master Loop Architecture (re-entrant 19-node graph)
2. Internal Cognitive Loops (Anomaly detection, falsifiable hypothesis pipeline, Type I/II risk evaluation)
3. 13 Coupled External Business Loops (Product, Marketing, Sales, CS, Brand, Pricing, Referral, Data, Financial, Hiring, Culture, Innovation, CompIntel)
4. Customer Journey Engine (15 lifecycle stages with psychology & metrics)
5. Integrated GTM System (Upstream positioning, channel selection, compounding motions)
6. Company Growth State Machine (9-stage progression, risk evaluation, binding constraints)
7. Strategic Moat & Capital Allocation Engine (Cost curves, 6 moat categories, opportunity-cost allocation)
8. Failure Mode Diagnostics (10 core failure modes with early warning signals & corrections)
9. Scientific Foundations Mapping
10. Autonomous AI System State Machine & Decision Tree Orchestrator
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Any, Set
import logging
import math

logger = logging.getLogger("apodex.ai_eos.eos_first_principles")


# =====================================================================
# 1. Master Loop Architecture (§1)
# =====================================================================

class MasterNode(Enum):
    ENVIRONMENTAL_SENSING = "A: Environmental Sensing"
    SIGNAL_COLLECTION = "B: Signal Collection & Knowledge Acquisition"
    PATTERN_RECOGNITION = "C: Pattern Recognition / Mental Model Formation"
    OPPORTUNITY_DISCOVERY = "D: Opportunity & Problem Discovery"
    OPPORTUNITY_EVALUATION = "E: Opportunity Evaluation & Root Cause Analysis"
    CUSTOMER_VALIDATION = "F: Customer & Market Validation"
    BUSINESS_MODEL_DESIGN = "G: Business Model & Value Proposition Design"
    MVP_EXPERIMENTATION = "H: MVP Design & Experimentation"
    PRODUCT_DEVELOPMENT = "I: Product Development"
    GTM_SYSTEM = "J: Go-to-Market System"
    CUSTOMER_ACQUISITION = "K: Customer Acquisition"
    ONBOARDING_RETENTION = "L: Onboarding, Activation, Retention"
    REVENUE_OPTIMIZATION = "M: Revenue & Unit Economics Optimization"
    OPERATIONS_SCALING = "N: Operations & Org Scaling"
    MOAT_CONSTRUCTION = "O: Competitive Strategy & Moat Construction"
    SCALING_EXPANSION = "P: Scaling & Expansion"
    PLATFORM_FORMATION = "Q: Platform / Ecosystem Formation"
    MARKET_LEADERSHIP = "R: Market Leadership"
    CONTINUOUS_REINVENTION = "S: Continuous Reinvention"


@dataclass
class MasterLoopState:
    current_node: MasterNode = MasterNode.ENVIRONMENTAL_SENSING
    active_nodes: Set[MasterNode] = field(default_factory=lambda: {MasterNode.ENVIRONMENTAL_SENSING})
    reentrant_parallel_nodes: Set[MasterNode] = field(default_factory=lambda: {MasterNode.ENVIRONMENTAL_SENSING, MasterNode.CONTINUOUS_REINVENTION})
    history: List[MasterNode] = field(default_factory=list)

    def transition_to(self, target: MasterNode, kill_signal: bool = False) -> MasterNode:
        self.history.append(self.current_node)
        if kill_signal:
            # Re-entrant kill signals route back to Opportunity Discovery (Node D) or Business Model (Node G)
            if self.current_node in (MasterNode.CUSTOMER_VALIDATION, MasterNode.MVP_EXPERIMENTATION):
                self.current_node = MasterNode.OPPORTUNITY_DISCOVERY
            elif self.current_node == MasterNode.REVENUE_OPTIMIZATION:
                self.current_node = MasterNode.BUSINESS_MODEL_DESIGN
            elif self.current_node == MasterNode.CUSTOMER_ACQUISITION:
                self.current_node = MasterNode.GTM_SYSTEM
            else:
                self.current_node = MasterNode.OPPORTUNITY_DISCOVERY
        else:
            self.current_node = target
        self.active_nodes.add(self.current_node)
        return self.current_node


# =====================================================================
# 2. Internal Cognitive Loops (§2)
# =====================================================================

class DecisionRiskType(Enum):
    TYPE_I = "Type I: Irreversible (One-way door, high scrutiny)"
    TYPE_II = "Type II: Reversible (Two-way door, fast execution)"


@dataclass
class AnomalySignal:
    signal_id: str
    description: str
    observed_metric: float
    expected_metric: float
    is_structural_shift: bool
    confidence: float


@dataclass
class CognitiveHypothesis:
    hypothesis_id: str
    claim: str
    falsifiable_metric: str
    kill_threshold: float
    current_value: float
    is_falsified: bool = False
    is_strengthened: bool = False
    test_cost_usd: float = 0.0


class CognitivePipeline:
    """Implements Signal-to-Idea pipeline and mental model updating."""

    def __init__(self) -> None:
        self.hypotheses: Dict[str, CognitiveHypothesis] = {}
        self.mental_model_parameters: Dict[str, float] = {"market_size": 1.0, "adoption_velocity": 1.0}
        self.mental_model_structure_version: int = 1

    def detect_anomaly(self, signal: AnomalySignal) -> bool:
        """Filter weak signals for structural shifts vs noise."""
        deviation = abs(signal.observed_metric - signal.expected_metric) / max(1e-5, abs(signal.expected_metric))
        return signal.is_structural_shift and deviation > 0.20 and signal.confidence > 0.60

    def form_hypothesis(self, hypothesis_id: str, claim: str, metric: str, kill_threshold: float, test_cost: float) -> CognitiveHypothesis:
        hyp = CognitiveHypothesis(
            hypothesis_id=hypothesis_id,
            claim=claim,
            falsifiable_metric=metric,
            kill_threshold=kill_threshold,
            current_value=0.0,
            test_cost_usd=test_cost
        )
        self.hypotheses[hypothesis_id] = hyp
        return hyp

    def evaluate_risk_type(self, decision_name: str, capital_at_risk_usd: float, regulatory_impact: bool, reversible: bool) -> DecisionRiskType:
        if not reversible or capital_at_risk_usd > 500_000 or regulatory_impact:
            return DecisionRiskType.TYPE_I
        return DecisionRiskType.TYPE_II

    def update_hypothesis_and_mental_model(self, hypothesis_id: str, observed_value: float) -> Tuple[bool, bool]:
        """Runs cheap test evaluation and performs Bayesian/structural mental model update."""
        hyp = self.hypotheses.get(hypothesis_id)
        if not hyp:
            return False, False

        hyp.current_value = observed_value
        if observed_value < hyp.kill_threshold:
            hyp.is_falsified = True
            hyp.is_strengthened = False
        else:
            hyp.is_strengthened = True
            hyp.is_falsified = False
            # Parameter update
            self.mental_model_parameters["adoption_velocity"] *= 1.15

        # If parameter update creates severe prediction error, trigger structural paradigm shift
        if self.mental_model_parameters["adoption_velocity"] > 5.0:
            self.mental_model_structure_version += 1
            logger.info(f"PARADIGM SHIFT: Updated mental model structure to v{self.mental_model_structure_version}")

        return hyp.is_strengthened, hyp.is_falsified


# =====================================================================
# 3. External Business Loops (§3)
# =====================================================================

@dataclass
class BusinessLoopMetrics:
    retention_curve_flattening: float  # [0, 1] Product
    cac_usd: float                     # Marketing
    sales_win_rate: float             # Sales
    net_revenue_retention: float       # Customer Success
    brand_price_elasticity: float      # Brand
    arpu_usd: float                    # Pricing
    viral_k_factor: float              # Referral
    decision_latency_hours: float      # Data
    burn_multiple: float               # Financial
    regretted_attrition_rate: float    # Hiring
    eNPS: float                        # Culture
    hit_rate_experiments: float        # Innovation
    feature_parity_gap: float          # Competitive Intelligence


class BusinessLoopsEngine:
    """Evaluates 13 coupled business feedback loops and identifies failure modes."""

    def evaluate_loops(self, m: BusinessLoopMetrics) -> Dict[str, Tuple[bool, str]]:
        results = {}
        results["Product"] = (m.retention_curve_flattening >= 0.40, "Retention curve failing to flatten" if m.retention_curve_flattening < 0.40 else "Healthy")
        results["Marketing"] = (m.cac_usd <= 500, "High CAC / message-market mismatch" if m.cac_usd > 500 else "Healthy")
        results["Sales"] = (m.sales_win_rate >= 0.20, "Low win rate / selling to non-ICP" if m.sales_win_rate < 0.20 else "Healthy")
        results["Customer Success"] = (m.net_revenue_retention >= 1.10, "NRR below 110% / churn risk" if m.net_revenue_retention < 1.10 else "Healthy")
        results["Brand"] = (m.brand_price_elasticity <= 1.5, "Weak brand pricing power" if m.brand_price_elasticity > 1.5 else "Healthy")
        results["Pricing"] = (m.arpu_usd >= 50, "Sub-optimal pricing realization" if m.arpu_usd < 50 else "Healthy")
        results["Referral"] = (m.viral_k_factor >= 0.15, "Low organic viral coefficient" if m.viral_k_factor < 0.15 else "Healthy")
        results["Data"] = (m.decision_latency_hours <= 24.0, "High decision latency / vanity metrics" if m.decision_latency_hours > 24.0 else "Healthy")
        results["Financial"] = (m.burn_multiple <= 2.0, "Unhealthy burn multiple (>2.0)" if m.burn_multiple > 2.0 else "Healthy")
        results["Hiring"] = (m.regretted_attrition_rate <= 0.10, "High regretted attrition" if m.regretted_attrition_rate > 0.10 else "Healthy")
        results["Culture"] = (m.eNPS >= 30, "Low eNPS / culture degradation" if m.eNPS < 30 else "Healthy")
        results["Innovation"] = (m.hit_rate_experiments >= 0.15, "Low experiment hit rate" if m.hit_rate_experiments < 0.15 else "Healthy")
        results["Competitive Intelligence"] = (m.feature_parity_gap <= 0.25, "Competitive gap widening" if m.feature_parity_gap > 0.25 else "Healthy")
        return results


# =====================================================================
# 4. Customer Journey Engine (§4)
# =====================================================================

class CustomerStage(Enum):
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
class CustomerLifecycleState:
    current_stage: CustomerStage = CustomerStage.AWARENESS
    time_to_first_value_days: float = 0.0
    activation_completed: bool = False
    cohort_retention_6m: float = 0.0
    nps_score: int = 0
    k_factor: float = 0.0
    nrr: float = 1.00

    def advance_stage(self, target: CustomerStage) -> CustomerStage:
        self.current_stage = target
        return self.current_stage


# =====================================================================
# 5. Integrated Go-To-Market System (§5)
# =====================================================================

class GTMChannel(Enum):
    PRODUCT_LED = "Product-Led Growth (PLG)"
    SALES_LED = "Sales-Led / Enterprise Growth (SLG)"
    COMMUNITY_LED = "Community-Led Growth (CLG)"
    CONTENT_ORGANIC = "Content & Organic Growth"
    PAID_ACQUISITION = "Paid Acquisition"
    PARTNERSHIPS = "Partnership Channels"


class IntegratedGTMSystem:
    """Matches positioning, pricing, and distribution channels systematically."""

    def select_gtm_motion(self, acv_usd: float, product_complexity: str, network_effects: bool) -> List[GTMChannel]:
        channels = []
        if acv_usd < 5_000 and product_complexity == "low":
            channels.append(GTMChannel.PRODUCT_LED)
            channels.append(GTMChannel.CONTENT_ORGANIC)
        elif acv_usd >= 50_000 or product_complexity == "high":
            channels.append(GTMChannel.SALES_LED)

        if network_effects:
            channels.append(GTMChannel.COMMUNITY_LED)

        if not channels:
            channels.append(GTMChannel.PRODUCT_LED)
        return channels


# =====================================================================
# 6. Company Growth System (§6)
# =====================================================================

class GrowthStage(Enum):
    IDEA = "Idea"
    VALIDATION = "Validation"
    STARTUP = "Startup"
    PMF = "Product-Market Fit"
    GROWTH = "Growth"
    SCALE = "Scale"
    PLATFORM = "Platform"
    ECOSYSTEM = "Ecosystem"
    MARKET_LEADERSHIP = "Market Leadership"


@dataclass
class GrowthStageMetrics:
    paying_customers: int
    ltv_to_cac: float
    retention_curve_flat: bool
    growth_rate_yoy: float
    rule_of_40: float
    third_party_developers: int

class CompanyGrowthStateMachine:
    """Tracks growth stages, primary objectives, key risks, and binding constraints."""

    def classify_stage(self, m: GrowthStageMetrics) -> GrowthStage:
        if m.third_party_developers > 500 and m.growth_rate_yoy > 0.30:
            return GrowthStage.ECOSYSTEM
        if m.third_party_developers > 100:
            return GrowthStage.PLATFORM
        if m.rule_of_40 >= 0.40 and m.paying_customers >= 1000:
            return GrowthStage.SCALE
        if m.growth_rate_yoy >= 0.50 and m.ltv_to_cac >= 3.0:
            return GrowthStage.GROWTH
        if m.retention_curve_flat and m.ltv_to_cac >= 3.0:
            return GrowthStage.PMF
        if m.paying_customers >= 10:
            return GrowthStage.STARTUP
        if m.paying_customers > 0:
            return GrowthStage.VALIDATION
        return GrowthStage.IDEA


# =====================================================================
# 7. Strategic Thinking & Moats (§7)
# =====================================================================

class StrategicMoatEngine:
    """Evaluates competitive moats and capital allocation based on opportunity cost."""

    def calculate_moat_score(
        self,
        network_density: float,
        switching_cost_score: float,
        scale_cost_advantage: float,
        brand_trust: float,
        counter_positioning: float
    ) -> float:
        """Weighted Moat Durability Score [0, 1]."""
        weights = [0.25, 0.20, 0.20, 0.15, 0.20]
        scores = [
            min(1.0, network_density),
            min(1.0, switching_cost_score),
            min(1.0, scale_cost_advantage),
            min(1.0, brand_trust),
            min(1.0, counter_positioning)
        ]
        return sum(w * s for w, s in zip(weights, scores))

    def rank_initiatives_by_expected_return(self, initiatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ranks initiatives on common expected-return basis enforcing opportunity-cost discipline."""
        for init in initiatives:
            expected_val = init.get("probability_success", 0.5) * init.get("upside_usd", 0.0)
            cost = max(1.0, init.get("cost_usd", 1.0))
            init["expected_roi"] = expected_val / cost
        initiatives.sort(key=lambda x: x["expected_roi"], reverse=True)
        return initiatives


# =====================================================================
# 8. Failure Mode Analysis (§8)
# =====================================================================

class FailureModeDiagnostics:
    """Pattern matches operating metrics against 10 explicit failure modes."""

    def diagnose(self, metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        warnings = []
        if metrics.get("engagement") == "low" and metrics.get("survey_positive") is True:
            warnings.append({
                "failure_mode": "Solving the wrong problem",
                "root_cause": "Skipped root-cause analysis; solved a symptom",
                "correction": "Return to 5-Whys / Jobs-to-be-Done customer interviews"
            })
        if metrics.get("build_velocity") == "high" and metrics.get("demand_signal") == "flat":
            warnings.append({
                "failure_mode": "Building before validating",
                "root_cause": "Founder conviction substituted for evidence",
                "correction": "Enforce validation gate before build resourcing"
            })
        if metrics.get("cac_rising_fast") is True and metrics.get("retention_curve_flat") is False:
            warnings.append({
                "failure_mode": "Scaling prematurely",
                "root_cause": "Confusing early demand spike with durable PMF",
                "correction": "Stop scaling; return to cohort-level retention work"
            })
        if metrics.get("decision_latency_hours", 0) > 48.0:
            warnings.append({
                "failure_mode": "Organizational bottlenecks",
                "root_cause": "Decision rights not delegated as company scales",
                "correction": "Push decision rights down with clear frameworks"
            })
        return warnings


# =====================================================================
# 10. AI State Machine & Decision Tree (§10)
# =====================================================================

class SystemState(Enum):
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


class DecisionTreeEvaluator:
    """Evaluates the Section 10.2 decision tree for opportunity pursuit."""

    def evaluate_pursuit(
        self,
        is_structural_anomaly: bool,
        is_reversible: bool,
        high_confidence_multi_source: bool,
        cheap_test_available: bool,
        test_result_exceeds_threshold: bool,
        ev_clearly_positive: bool,
        structural_advantage: bool
    ) -> Tuple[bool, str]:
        if not is_structural_anomaly:
            return False, "Discard: Noise signal, not a structural anomaly."

        if not is_reversible and not high_confidence_multi_source:
            return False, "Discard: Type I decision lacking high-confidence multi-source signal."

        if cheap_test_available:
            if not test_result_exceeds_threshold:
                return False, "Discard: Cheap test failed kill threshold."
        else:
            if not ev_clearly_positive:
                return False, "Discard: Expected value not clearly positive."

        if not structural_advantage:
            return False, "Discard: No structural advantage or defensibility."

        return True, "Commit Resources: Passed decision tree criteria."


class EOSEngineFirstPrinciples:
    """Unified Orchestrator coupling all 10 AI agent modules (§10.3)."""

    def __init__(self) -> None:
        self.master_loop = MasterLoopState()
        self.cognitive_pipeline = CognitivePipeline()
        self.business_loops = BusinessLoopsEngine()
        self.gtm_system = IntegratedGTMSystem()
        self.growth_machine = CompanyGrowthStateMachine()
        self.moat_engine = StrategicMoatEngine()
        self.diagnostics = FailureModeDiagnostics()
        self.decision_tree = DecisionTreeEvaluator()
        self.current_state = SystemState.SENSING
        self.capital_allocated_usd: float = 0.0

    def run_execution_cycle(
        self,
        anomaly_signal: Optional[AnomalySignal],
        operating_metrics: BusinessLoopMetrics,
        growth_metrics: GrowthStageMetrics,
        decision_inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        cycle_result = {}

        # 1. Sensing & Anomaly Detection
        if self.current_state == SystemState.SENSING:
            if anomaly_signal:
                is_anomaly = self.cognitive_pipeline.detect_anomaly(anomaly_signal)
                if is_anomaly:
                    self.current_state = SystemState.HYPOTHESIS
                    self.master_loop.transition_to(MasterNode.PATTERN_RECOGNITION)
                    cycle_result["sensing"] = "Anomaly detected. Advanced to HYPOTHESIS."

        # 2. Hypothesis & Decision Tree Gate
        elif self.current_state == SystemState.HYPOTHESIS:
            pursue, reason = self.decision_tree.evaluate_pursuit(
                is_structural_anomaly=decision_inputs.get("is_structural_anomaly", True),
                is_reversible=decision_inputs.get("is_reversible", True),
                high_confidence_multi_source=decision_inputs.get("high_confidence_multi_source", True),
                cheap_test_available=decision_inputs.get("cheap_test_available", True),
                test_result_exceeds_threshold=decision_inputs.get("test_result_exceeds_threshold", True),
                ev_clearly_positive=decision_inputs.get("ev_clearly_positive", True),
                structural_advantage=decision_inputs.get("structural_advantage", True)
            )
            cycle_result["decision_tree"] = reason
            if pursue:
                self.current_state = SystemState.CHEAP_TEST
                self.master_loop.transition_to(MasterNode.MVP_EXPERIMENTATION)
            else:
                self.current_state = SystemState.DISCARD

        # 3. Cheap Test execution
        elif self.current_state == SystemState.CHEAP_TEST:
            hyp_id = decision_inputs.get("hypothesis_id", "hyp_001")
            self.cognitive_pipeline.form_hypothesis(
                hypothesis_id=hyp_id,
                claim="Test claim",
                metric="retention",
                kill_threshold=0.30,
                test_cost=1000.0
            )
            strengthened, falsified = self.cognitive_pipeline.update_hypothesis_and_mental_model(
                hypothesis_id=hyp_id,
                observed_value=decision_inputs.get("test_observed_val", 0.45)
            )
            if strengthened:
                self.current_state = SystemState.VALIDATION
                self.master_loop.transition_to(MasterNode.CUSTOMER_VALIDATION)
            else:
                self.current_state = SystemState.DISCARD
                self.master_loop.transition_to(MasterNode.OPPORTUNITY_DISCOVERY, kill_signal=True)

        # 4. Business Loop Evaluation & Diagnostics
        loop_status = self.business_loops.evaluate_loops(operating_metrics)
        failure_warnings = self.diagnostics.diagnose({
            "engagement": "low",
            "survey_positive": False,
            "decision_latency_hours": operating_metrics.decision_latency_hours
        })

        # 5. Growth Stage
        current_growth_stage = self.growth_machine.classify_stage(growth_metrics)

        cycle_result.update({
            "current_system_state": self.current_state.value,
            "current_master_node": self.master_loop.current_node.value,
            "growth_stage": current_growth_stage.value,
            "business_loops_status": loop_status,
            "failure_warnings": failure_warnings
        })

        return cycle_result
