"""
First-Principles Entrepreneurial Operating System (EOS) Implementation

This module operationalizes the 11-part theoretical framework of the
Entrepreneurial Operating System (EOS), modeling elite founder behavior through
nested feedback loops, decision trees, customer lifecycle state machines,
GTM dependency graphs, growth stage classification, moat analysis,
failure mode active monitoring, and autonomous AI-EOS agent orchestration.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple


# ============================================================================
# Section 0 & 1: Timescales & Master Loop
# ============================================================================

class LoopTimescale(str, Enum):
    FAST = "fast"       # days - weeks (experiments, sales calls, hiring interviews)
    MEDIUM = "medium"   # months - quarters (GTM iteration, pricing, org design, capital)
    SLOW = "slow"       # years (strategic positioning, moat, category, reinvention)


@dataclass
class TimescaleLoop:
    name: str
    timescale: LoopTimescale
    cycle_time_days: float
    signal_fidelity: float  # [0.0, 1.0]
    compounding_score: float # rate of value accumulation
    is_active: bool = True

    def execute_cycle(self, feedback_quality: float) -> float:
        """Executes a loop cycle and returns the updated compounding score."""
        if not self.is_active:
            return self.compounding_score

        # Velocity and signal fidelity drive compounding
        velocity_factor = 30.0 / max(self.cycle_time_days, 1.0)
        effective_gain = feedback_quality * self.signal_fidelity * velocity_factor * 0.1
        self.compounding_score += effective_gain
        return self.compounding_score


# ============================================================================
# Section 2: Internal Cognitive Loops (Decision Trees & Hypothesis Engine)
# ============================================================================

class DecisionRiskType(str, Enum):
    TYPE_I = "type_1_irreversible"  # One-way door
    TYPE_II = "type_2_reversible"    # Two-way door


@dataclass
class AnomalySignal:
    signal_id: str
    description: str
    is_structural_shift: bool
    observed_value: float
    expected_value: float
    confidence: float


@dataclass
class FalsifiableHypothesis:
    hypothesis_id: str
    claim: str
    metric: str
    target_threshold: float
    cheap_test_cost: float
    is_reversible: bool
    precommitted_kill_criteria: str
    is_falsified: bool = False
    is_validated: bool = False


class SignalToIdeaPipeline:
    def __init__(self):
        self.hypotheses: List[FalsifiableHypothesis] = []

    def evaluate_signal(self, signal: AnomalySignal) -> Optional[FalsifiableHypothesis]:
        """Filters weak signals into forced falsifiable claims if structural shift detected."""
        if not signal.is_structural_shift or signal.confidence < 0.6:
            return None

        hypothesis = FalsifiableHypothesis(
            hypothesis_id=f"hyp_{signal.signal_id}",
            claim=f"Exploit structural shift in {signal.description}",
            metric="conversion_delta",
            target_threshold=0.15,
            cheap_test_cost=500.0,
            is_reversible=True,
            precommitted_kill_criteria="conversion_delta < 0.05 after 100 trials"
        )
        self.hypotheses.append(hypothesis)
        return hypothesis

    def execute_cheap_test(self, hypothesis: FalsifiableHypothesis, test_result_value: float) -> str:
        """Executes a cheap real-option test and updates belief."""
        if test_result_value >= hypothesis.target_threshold:
            hypothesis.is_validated = True
            hypothesis.is_falsified = False
            return "STRENGTHENED"
        else:
            hypothesis.is_falsified = True
            hypothesis.is_validated = False
            return "FALSIFIED"


class OpportunityDecisionTree:
    """Implements §10.2 Decision Tree: Should We Pursue This Opportunity?"""

    @staticmethod
    def evaluate_opportunity(
        is_structural_anomaly: bool,
        is_reversible: bool,
        cheap_test_available: bool,
        test_passed: Optional[bool],
        expected_value_positive: bool,
        has_moat_advantage: bool,
        high_confidence_signal: bool = False
    ) -> Dict[str, Any]:

        if not is_structural_anomaly:
            return {"decision": "DISCARD", "reason": "Noise, not a structural anomaly"}

        if is_reversible:
            if cheap_test_available:
                if test_passed is True:
                    if has_moat_advantage:
                        return {"decision": "COMMIT", "reason": "Cheap test passed with structural moat advantage"}
                    else:
                        return {"decision": "DISCARD", "reason": "No structural moat advantage"}
                else:
                    return {"decision": "DISCARD", "reason": "Cheap test failed or below kill threshold"}
            else:
                if expected_value_positive and has_moat_advantage:
                    return {"decision": "COMMIT", "reason": "EV positive with structural moat advantage"}
                else:
                    return {"decision": "DISCARD", "reason": "EV negative or lack of moat advantage"}
        else:
            # Irreversible decision (Type I)
            if not high_confidence_signal:
                return {"decision": "DISCARD", "reason": "Type I irreversible decision without high-confidence multi-source signal"}
            if has_moat_advantage and expected_value_positive:
                return {"decision": "COMMIT", "reason": "Type I high-confidence opportunity with moat advantage"}
            return {"decision": "DISCARD", "reason": "Lacks required EV or moat criteria for Type I decision"}


# ============================================================================
# Section 3: External Business Loops (13 Coupled Loops)
# ============================================================================

@dataclass
class ExternalLoop:
    name: str
    inputs: List[str]
    outputs: List[str]
    feedback_signal: str
    kpis: Dict[str, float]
    failure_mode: str

    def update_kpi(self, key: str, value: float):
        self.kpis[key] = value


class ExternalBusinessLoopSystem:
    def __init__(self):
        self.loops: Dict[str, ExternalLoop] = {
            "Product": ExternalLoop("Product", ["user_behavior", "support_tickets"], ["feature_changes", "roadmap"], "retention_deltas", {"retention_slope": 0.45, "nps": 52.0}, "Building for loud user, not ICP"),
            "Marketing": ExternalLoop("Marketing", ["positioning", "market_data"], ["awareness", "demand"], "cac_trends", {"cac": 120.0, "conversion_rate": 0.035}, "Scaling spend before messaging works"),
            "Sales": ExternalLoop("Sales", ["qualified_leads", "product"], ["closed_revenue", "customer_feedback"], "win_loss_reasons", {"win_rate": 0.28, "acv": 15000.0}, "Selling to non-ICP to hit quota"),
            "CustomerSuccess": ExternalLoop("CustomerSuccess", ["onboarding_data", "usage"], ["retention", "expansion"], "churn_reasons", {"nrr": 1.15, "churn_rate": 0.02}, "Reactive support mistaken for CS"),
            "Brand": ExternalLoop("Brand", ["product_experience", "comms"], ["trust", "pricing_power"], "sentiment", {"share_of_voice": 0.18, "price_elasticity": 0.6}, "Brand as decoration, not strategy"),
            "Pricing": ExternalLoop("Pricing", ["value_delivered", "wtp_data"], ["revenue", "positioning_signal"], "price_point_conversion", {"arpu": 450.0, "price_realization": 0.92}, "Cost-plus pricing instead of value-based"),
            "Referral": ExternalLoop("Referral", ["customer_satisfaction", "incentives"], ["organic_growth"], "k_factor_signal", {"viral_coefficient": 1.2, "referral_cac": 25.0}, "Incentivizing referral volume over quality"),
            "Data": ExternalLoop("Data", ["operational_telemetry"], ["decisions"], "model_accuracy", {"data_latency_s": 0.5, "decision_cycle_s": 1.2}, "Vanity metrics without actionability"),
            "Financial": ExternalLoop("Financial", ["revenue", "costs", "capital"], ["runway", "reinvestment"], "burn_multiple_trend", {"gross_margin": 0.78, "burn_multiple": 1.1, "runway_months": 24.0}, "Growth at negative unit economics"),
            "Hiring": ExternalLoop("Hiring", ["org_needs", "culture"], ["capability", "capacity"], "performance_90d", {"time_to_fill_days": 35.0, "retention_rate": 0.94}, "Hiring pedigree over role-fit"),
            "Culture": ExternalLoop("Culture", ["values_in_action", "incentives"], ["behavior_consistency"], "decision_speed", {"enps": 65.0, "decision_latency_hrs": 4.0}, "Values-as-poster non-alignment"),
            "Innovation": ExternalLoop("Innovation", ["rd", "market_signals"], ["new_products"], "time_to_market", {"experiment_hit_rate": 0.22, "time_to_signal_days": 14.0}, "Innovation theater without shipped bets"),
            "CompetitiveIntelligence": ExternalLoop("CompetitiveIntelligence", ["competitor_data"], ["repositioning"], "win_loss_vs_rivals", {"relative_market_share": 0.32, "parity_gap": 0.05}, "Reacting to competitors vs running own playbook")
        }

    def simulate_coupled_step(self) -> Dict[str, Any]:
        """Simulates coupled feedback propagation across all 13 loops."""
        # e.g. Pricing loop output (ARPU) feeds Financial loop (Runway & Burn Multiple)
        arpu = self.loops["Pricing"].kpis.get("arpu", 400.0)
        self.loops["Financial"].kpis["gross_margin"] = min(0.95, 0.60 + (arpu / 2000.0))

        # Financial loop feeds Hiring budget
        runway = self.loops["Financial"].kpis.get("runway_months", 12.0)
        self.loops["Hiring"].kpis["time_to_fill_days"] = max(10.0, 45.0 - (runway / 2.0))

        return {name: loop.kpis for name, loop in self.loops.items()}


# ============================================================================
# Section 4: Customer Journey (15 Stages)
# ============================================================================

class CustomerStage(str, Enum):
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


@dataclass
class CustomerLifecycleState:
    customer_id: str
    current_stage: CustomerStage
    time_in_stage_days: float = 0.0
    health_score: float = 1.0
    activated: bool = False
    retained: bool = True

    def transition_next(self) -> CustomerStage:
        stages = list(CustomerStage)
        idx = stages.index(self.current_stage)
        if idx < len(stages) - 1:
            self.current_stage = stages[idx + 1]
            self.time_in_stage_days = 0.0
            if self.current_stage == CustomerStage.ACTIVATION:
                self.activated = True
        return self.current_stage


# ============================================================================
# Section 5 & 6: GTM & Growth Stage Classification
# ============================================================================

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


@dataclass
class VentureMetrics:
    validated_learnings_count: int
    paying_customers_count: int
    retention_curve_flattened: bool
    cac_payback_months: float
    nrr: float
    rule_of_40_score: float
    third_party_developer_count: int
    category_market_share: float


class GrowthStageClassifier:
    @staticmethod
    def classify_stage(metrics: VentureMetrics) -> Tuple[GrowthStage, str]:
        """Classifies venture growth stage and identifies binding constraints."""
        if metrics.category_market_share >= 0.50 and metrics.third_party_developer_count > 1000:
            return GrowthStage.MARKET_LEADERSHIP, "Binding constraint: Innovation velocity vs incumbency drag"
        if metrics.third_party_developer_count > 500:
            return GrowthStage.ECOSYSTEM, "Binding constraint: Governance credibility & network density"
        if metrics.third_party_developer_count > 50:
            return GrowthStage.PLATFORM, "Binding constraint: Ecosystem trust & API platform design"
        if metrics.rule_of_40_score >= 0.40 and metrics.nrr >= 1.20:
            return GrowthStage.SCALE, "Binding constraint: Organizational coordination cost & culture dilution"
        if metrics.cac_payback_months <= 12.0 and metrics.retention_curve_flattened:
            return GrowthStage.GROWTH, "Binding constraint: Hiring velocity & scaling broken funnels"
        if metrics.retention_curve_flattened:
            return GrowthStage.PMF, "Binding constraint: Team bandwidth & scaling premature channels"
        if metrics.paying_customers_count >= 10:
            return GrowthStage.STARTUP, "Binding constraint: Cash runway & CAC:LTV signal ratio"
        if metrics.paying_customers_count > 0:
            return GrowthStage.VALIDATION, "Binding constraint: Signal quality & false-positive validation"
        return GrowthStage.IDEA, "Binding constraint: Founder time & hypothesis falsification"


# ============================================================================
# Section 7: Strategic Moat Analyzer
# ============================================================================

class MoatType(str, Enum):
    NETWORK_EFFECTS = "network_effects"
    SWITCHING_COSTS = "switching_costs"
    ECONOMIES_OF_SCALE = "economies_of_scale"
    BRAND_TRUST = "brand_trust"
    COUNTER_POSITIONING = "counter_positioning"


@dataclass
class StrategicMoatProfile:
    primary_moat: MoatType
    durability_score: float  # [0.0, 1.0]
    switching_cost_barrier: float
    network_density: float
    cost_structure_advantage: float

    def evaluate_durability(self) -> float:
        """Computes comprehensive moat durability score."""
        scores = [
            self.durability_score,
            min(1.0, self.switching_cost_barrier / 10.0),
            min(1.0, self.network_density),
            min(1.0, self.cost_structure_advantage)
        ]
        return sum(scores) / len(scores)


# ============================================================================
# Section 8: Failure Mode Active Monitor
# ============================================================================

@dataclass
class FailureModeAlert:
    failure_mode: str
    root_cause: str
    detection_signal: str
    correction_mechanism: str
    severity: str  # HIGH, CRITICAL, MEDIUM


class FailureModeMonitor:
    @staticmethod
    def audit_telemetry(telemetry: Dict[str, float]) -> List[FailureModeAlert]:
        alerts = []

        # 1. Building before validating
        if telemetry.get("build_velocity", 0.0) > 8.0 and telemetry.get("demand_signal", 1.0) < 2.0:
            alerts.append(FailureModeAlert(
                failure_mode="Building before validating",
                root_cause="Founder conviction substituted for evidence",
                detection_signal="High build velocity, flat demand signal",
                correction_mechanism="Enforce a validation gate before build resourcing",
                severity="CRITICAL"
            ))

        # 2. Lack of PMF / Premature Scaling
        if telemetry.get("growth_spend_scaling", 0.0) > 5.0 and not telemetry.get("retention_curve_flattened", False):
            alerts.append(FailureModeAlert(
                failure_mode="Lack of product-market fit / Premature scaling",
                root_cause="Premature scaling of an unproven loop",
                detection_signal="Retention curve never flattens while spend scales",
                correction_mechanism="Stop scaling; return to cohort-level retention work",
                severity="CRITICAL"
            ))

        # 3. Poor Pricing
        if telemetry.get("conversion_rate", 0.0) > 0.40 and telemetry.get("gross_margin", 1.0) < 0.30:
            alerts.append(FailureModeAlert(
                failure_mode="Poor pricing",
                root_cause="Cost-plus instead of value-based pricing",
                detection_signal="High conversion at low price, but poor margin/expansion",
                correction_mechanism="Re-anchor price to quantified customer value",
                severity="HIGH"
            ))

        # 4. Organizational Bottlenecks
        if telemetry.get("decision_latency_hrs", 0.0) > 72.0:
            alerts.append(FailureModeAlert(
                failure_mode="Organizational bottlenecks",
                root_cause="Decision rights not delegated as company scales",
                detection_signal="Rising decision latency, founder as single point of failure",
                correction_mechanism="Push decision rights down with clear frameworks",
                severity="HIGH"
            ))

        return alerts


# ============================================================================
# Section 10: Integrated AI-EOS Agent Orchestrator
# ============================================================================

class AIEOSKernel:
    def __init__(self):
        self.pipeline = SignalToIdeaPipeline()
        self.external_loops = ExternalBusinessLoopSystem()
        self.moat_profile = StrategicMoatProfile(
            primary_moat=MoatType.SWITCHING_COSTS,
            durability_score=0.85,
            switching_cost_barrier=8.5,
            network_density=0.75,
            cost_structure_advantage=0.80
        )
        self.venture_metrics = VentureMetrics(
            validated_learnings_count=12,
            paying_customers_count=25,
            retention_curve_flattened=True,
            cac_payback_months=8.5,
            nrr=1.22,
            rule_of_40_score=0.45,
            third_party_developer_count=120,
            category_market_share=0.15
        )

    def process_opportunity(self, anomaly: AnomalySignal) -> Dict[str, Any]:
        """Runs an anomaly through the end-to-end AI-EOS decision engine."""
        hypothesis = self.pipeline.evaluate_signal(anomaly)
        if not hypothesis:
            return {"status": "DISCARDED", "reason": "Signal not structural or low confidence"}

        # Run cheap test
        test_outcome = self.pipeline.execute_cheap_test(hypothesis, test_result_value=0.20)

        # Evaluate decision tree
        decision = OpportunityDecisionTree.evaluate_opportunity(
            is_structural_anomaly=anomaly.is_structural_shift,
            is_reversible=hypothesis.is_reversible,
            cheap_test_available=True,
            test_passed=(test_outcome == "STRENGTHENED"),
            expected_value_positive=True,
            has_moat_advantage=(self.moat_profile.evaluate_durability() > 0.60)
        )

        # Classify current stage
        stage, binding_constraint = GrowthStageClassifier.classify_stage(self.venture_metrics)

        # Audit failure modes
        telemetry_sample = {
            "build_velocity": 4.0,
            "demand_signal": 6.5,
            "retention_curve_flattened": self.venture_metrics.retention_curve_flattened,
            "gross_margin": 0.78,
            "decision_latency_hrs": 12.0
        }
        alerts = FailureModeMonitor.audit_telemetry(telemetry_sample)

        return {
            "status": decision["decision"],
            "decision_reason": decision["reason"],
            "hypothesis": hypothesis.claim,
            "growth_stage": stage.value,
            "binding_constraint": binding_constraint,
            "active_alerts_count": len(alerts),
            "moat_durability": self.moat_profile.evaluate_durability()
        }
