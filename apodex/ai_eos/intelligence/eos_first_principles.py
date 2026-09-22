"""First-Principles Entrepreneurial Operating System (EOS) Executable Engine.

An executable Python engine operationalizing the 11-section First-Principles EOS model
for elite founders sensing, building, and compounding enduring companies.
"""

from __future__ import annotations
from enum import Enum
import logging
from typing import Any, Dict, List, Optional, Tuple, Set
from datetime import datetime, timezone

logger = logging.getLogger("apodex.ai_eos.eos_first_principles")


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
    """System State Machine implementing §10.1 lifecycle transitions."""

    VALID_TRANSITIONS: Dict[EOSState, List[EOSState]] = {
        EOSState.SENSING: [EOSState.HYPOTHESIS],
        EOSState.HYPOTHESIS: [EOSState.CHEAP_TEST, EOSState.DISCARD],
        EOSState.CHEAP_TEST: [EOSState.VALIDATION, EOSState.DISCARD],
        EOSState.DISCARD: [EOSState.SENSING],
        EOSState.VALIDATION: [EOSState.BUILD_GATE, EOSState.DISCARD],
        EOSState.BUILD_GATE: [EOSState.MVP, EOSState.DISCARD],
        EOSState.MVP: [EOSState.GTM_TEST],
        EOSState.GTM_TEST: [EOSState.KILL_OR_SCALE],
        EOSState.KILL_OR_SCALE: [EOSState.SCALE, EOSState.DISCARD],
        EOSState.SCALE: [EOSState.OPERATE],
        EOSState.OPERATE: [EOSState.REINVENT, EOSState.SENSING],
        EOSState.REINVENT: [EOSState.SENSING, EOSState.HYPOTHESIS],
    }

    def __init__(self, initial_state: EOSState = EOSState.SENSING) -> None:
        self.current_state = initial_state
        self.history: List[Tuple[EOSState, datetime, str]] = [
            (initial_state, datetime.now(timezone.utc), "Initialization")
        ]

    def transition(self, target_state: EOSState, reason: str = "") -> bool:
        """Attempt transition to target_state. Returns True if valid transition occurred."""
        valid_targets = self.VALID_TRANSITIONS.get(self.current_state, [])
        if target_state not in valid_targets:
            logger.warning(
                f"Invalid transition attempted: {self.current_state.value} -> {target_state.value}. "
                f"Valid targets: {[s.value for s in valid_targets]}"
            )
            return False

        logger.info(f"State transition: {self.current_state.value} -> {target_state.value} ({reason})")
        self.current_state = target_state
        self.history.append((target_state, datetime.now(timezone.utc), reason))
        return True


# =====================================================================
# 2. Decision Tree — "Should We Pursue This Opportunity?" (§10.2, §2.1)
# =====================================================================
class OpportunityDecisionTree:
    """Executable decision tree implementing §10.2 and Type I/II risk heuristics (§2.1)."""

    def evaluate_opportunity(
        self,
        anomaly_is_structural: bool,
        is_reversible: bool,
        high_confidence_signal: bool = False,
        cheap_test_available: bool = True,
        test_exceeds_kill_threshold: Optional[bool] = None,
        ev_clearly_positive: Optional[bool] = None,
        structural_advantage_exists: bool = False,
    ) -> Dict[str, Any]:
        """Evaluate an opportunity based on §10.2 decision flow.

        Returns decision dictionary with pursuit outcome, decision path, and risk categorization.
        """
        path: List[str] = []

        # Q1: Structural anomaly or just noise?
        if not anomaly_is_structural:
            path.append("Q1: Anomaly is noise -> Discard")
            return {"pursue": False, "reason": "Noise signal, not structural anomaly", "path": path, "risk_type": "None"}

        path.append("Q1: Structural anomaly confirmed")

        # Q2: Reversible decision? (Type I vs Type II)
        risk_type = "Type II (Reversible)" if is_reversible else "Type I (Irreversible)"

        if not is_reversible:
            path.append("Q2: Irreversible decision (Type I / High Stakes)")
            if not high_confidence_signal:
                path.append("Q2a: Lack of high-confidence multi-source signal -> Discard")
                return {
                    "pursue": False,
                    "reason": "Irreversible decision without high-confidence multi-source signal",
                    "path": path,
                    "risk_type": risk_type,
                }
            path.append("Q2a: High-confidence multi-source signal confirmed")
        else:
            path.append("Q2: Reversible decision (Type II / Low Stakes)")

        # Q3: Cheap test available?
        if cheap_test_available:
            path.append("Q3: Cheap test available -> Run test")
            if test_exceeds_kill_threshold is False:
                path.append("Q4: Cheap test result failed kill threshold -> Discard")
                return {
                    "pursue": False,
                    "reason": "Cheap test failed pre-committed kill threshold",
                    "path": path,
                    "risk_type": risk_type,
                }
            elif test_exceeds_kill_threshold is True:
                path.append("Q4: Cheap test result exceeded kill threshold")
            else:
                path.append("Q4: Pending cheap test execution")
                return {
                    "pursue": False,
                    "reason": "Pending cheap test execution",
                    "path": path,
                    "risk_type": risk_type,
                }
        else:
            path.append("Q3: No cheap test available")
            if not ev_clearly_positive:
                path.append("Q4b: Expected value NOT clearly positive -> Discard")
                return {
                    "pursue": False,
                    "reason": "Expected value not clearly positive in absence of cheap test",
                    "path": path,
                    "risk_type": risk_type,
                }
            path.append("Q4b: Expected value clearly positive confirmed")

        # Q5: Structural advantage?
        if not structural_advantage_exists:
            path.append("Q5: No structural advantage existing or buildable -> Discard")
            return {
                "pursue": False,
                "reason": "Lacks defendable structural advantage",
                "path": path,
                "risk_type": risk_type,
            }

        path.append("Q5: Structural advantage confirmed -> Commit Resources")
        return {
            "pursue": True,
            "reason": "Passed all decision tree criteria; commit resources",
            "path": path,
            "risk_type": risk_type,
        }


# =====================================================================
# 3. External Business Loops (§3)
# =====================================================================
class CoupledBusinessLoopsEngine:
    """Simulates and evaluates all 13 coupled external business feedback loops (§3)."""

    LOOP_NAMES = [
        "product",
        "marketing",
        "sales",
        "customer_success",
        "brand",
        "pricing",
        "referral",
        "data",
        "financial",
        "hiring",
        "culture",
        "innovation",
        "competitive_intelligence",
    ]

    def evaluate_all_loops(self, metrics: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Evaluate status, feedback signals, KPIs, and failure modes across all 13 loops."""
        results: Dict[str, Dict[str, Any]] = {}

        # 1. Product Loop
        retention = metrics.get("retention_rate", 0.5)
        nps = metrics.get("nps", 30)
        loudest_cust_bias = metrics.get("loudest_customer_feature_bias", False)
        results["product"] = {
            "inputs": "User behavior, support tickets, usage data",
            "outputs": "Feature changes, roadmap",
            "feedback_signal": "Activation/retention deltas",
            "kpis": {"retention_rate": retention, "nps": nps},
            "healthy": retention >= 0.40 and nps >= 40 and not loudest_cust_bias,
            "failure_mode": "Building for loudest customer, not representative one" if loudest_cust_bias else None,
        }

        # 2. Marketing Loop
        cac = metrics.get("cac_cents", 100_00)
        conversion = metrics.get("marketing_conversion_rate", 0.02)
        scaled_before_msg = metrics.get("spend_scaled_before_message_fit", False)
        results["marketing"] = {
            "inputs": "Positioning, market data",
            "outputs": "Awareness, demand",
            "feedback_signal": "CAC, traffic quality, message resonance",
            "kpis": {"cac_cents": cac, "conversion_rate": conversion},
            "healthy": conversion >= 0.03 and not scaled_before_msg,
            "failure_mode": "Message-market mismatch; scaling spend before message works" if scaled_before_msg else None,
        }

        # 3. Sales Loop
        win_rate = metrics.get("win_rate", 0.20)
        non_icp_sales = metrics.get("selling_to_non_icp", False)
        results["sales"] = {
            "inputs": "Qualified leads, product",
            "outputs": "Closed revenue, customer feedback",
            "feedback_signal": "Win/loss reasons",
            "kpis": {"win_rate": win_rate, "sales_cycle_days": metrics.get("sales_cycle_days", 30)},
            "healthy": win_rate >= 0.25 and not non_icp_sales,
            "failure_mode": "Selling to non-ICP to hit quota" if non_icp_sales else None,
        }

        # 4. Customer Success Loop
        nrr = metrics.get("nrr", 1.10)
        reactive_only = metrics.get("cs_reactive_only", False)
        results["customer_success"] = {
            "inputs": "Onboarding data, usage",
            "outputs": "Retention, expansion",
            "feedback_signal": "Churn reasons, health scores",
            "kpis": {"nrr": nrr, "churn_rate": metrics.get("churn_rate", 0.02)},
            "healthy": nrr >= 1.15 and not reactive_only,
            "failure_mode": "Success != support; reactive-only CS" if reactive_only else None,
        }

        # 5. Brand Loop
        brand_elasticity = metrics.get("price_elasticity", -1.0)
        brand_as_decor = metrics.get("brand_as_decoration", False)
        results["brand"] = {
            "inputs": "Product experience, comms",
            "outputs": "Trust, pricing power",
            "feedback_signal": "Sentiment, unaided recall",
            "kpis": {"share_of_voice": metrics.get("share_of_voice", 0.1), "price_elasticity": brand_elasticity},
            "healthy": abs(brand_elasticity) < 1.5 and not brand_as_decor,
            "failure_mode": "Brand as decoration, not strategy" if brand_as_decor else None,
        }

        # 6. Pricing Loop
        arpu = metrics.get("arpu_cents", 50_00)
        cost_plus = metrics.get("cost_plus_pricing", False)
        results["pricing"] = {
            "inputs": "Value delivered, WTP data",
            "outputs": "Revenue, positioning signal",
            "feedback_signal": "Conversion by price point, expansion rate",
            "kpis": {"arpu_cents": arpu, "price_realization": metrics.get("price_realization", 0.85)},
            "healthy": arpu > 0 and not cost_plus,
            "failure_mode": "Cost-plus pricing instead of value-based" if cost_plus else None,
        }

        # 7. Referral Loop
        k_factor = metrics.get("viral_coefficient_k", 0.5)
        incentivized_junk = metrics.get("incentivizing_volume_over_quality", False)
        results["referral"] = {
            "inputs": "Customer satisfaction, incentive design",
            "outputs": "New customer flow",
            "feedback_signal": "Referral rate, K-factor",
            "kpis": {"viral_coefficient_k": k_factor},
            "healthy": k_factor >= 0.8 and not incentivized_junk,
            "failure_mode": "Incentivizing referral volume over referral quality" if incentivized_junk else None,
        }

        # 8. Data Loop
        decision_latency = metrics.get("decision_latency_hours", 24)
        vanity_metrics_only = metrics.get("vanity_metrics_only", False)
        results["data"] = {
            "inputs": "All loop operational data",
            "outputs": "Decisions",
            "feedback_signal": "Model accuracy vs. outcomes",
            "kpis": {"decision_latency_hours": decision_latency},
            "healthy": decision_latency <= 48 and not vanity_metrics_only,
            "failure_mode": "Vanity metrics; dashboards no one acts on" if vanity_metrics_only else None,
        }

        # 9. Financial Loop
        burn_multiple = metrics.get("burn_multiple", 1.5)
        gross_margin = metrics.get("gross_margin", 0.70)
        runway_months = metrics.get("runway_months", 18)
        neg_unit_econ = gross_margin < 0 or burn_multiple > 3.0
        results["financial"] = {
            "inputs": "Revenue, costs, capital",
            "outputs": "Runway, reinvestment capacity",
            "feedback_signal": "Burn multiple, margin trend",
            "kpis": {"gross_margin": gross_margin, "burn_multiple": burn_multiple, "runway_months": runway_months},
            "healthy": gross_margin >= 0.60 and burn_multiple <= 2.0 and runway_months >= 12,
            "failure_mode": "Growth at negative unit economics with no path to positive" if neg_unit_econ else None,
        }

        # 10. Hiring Loop
        time_to_fill = metrics.get("time_to_fill_days", 45)
        hiring_pedigree = metrics.get("hiring_pedigree_over_fit", False)
        results["hiring"] = {
            "inputs": "Org needs, culture",
            "outputs": "Capability, capacity",
            "feedback_signal": "90-day performance, regretted attrition",
            "kpis": {"time_to_fill_days": time_to_fill, "regretted_attrition": metrics.get("regretted_attrition", 0.05)},
            "healthy": time_to_fill <= 60 and not hiring_pedigree,
            "failure_mode": "Hiring for pedigree over role-fit; hiring ahead of proven need" if hiring_pedigree else None,
        }

        # 11. Culture Loop
        enps = metrics.get("enps", 40)
        values_as_poster = metrics.get("values_as_poster", False)
        results["culture"] = {
            "inputs": "Values-in-action, incentives",
            "outputs": "Behavior consistency at scale",
            "feedback_signal": "Employee sentiment, decision speed",
            "kpis": {"enps": enps},
            "healthy": enps >= 30 and not values_as_poster,
            "failure_mode": "Values-as-poster (stated but not incentivized)" if values_as_poster else None,
        }

        # 12. Innovation Loop
        exp_count = metrics.get("experiments_run_quarterly", 10)
        innovation_theater = metrics.get("innovation_theater", False)
        results["innovation"] = {
            "inputs": "R&D, market signals, internal ideas",
            "outputs": "New products/features/lines",
            "feedback_signal": "Time-to-market, cannibalization rate",
            "kpis": {"experiments_run_quarterly": exp_count, "hit_rate": metrics.get("experiment_hit_rate", 0.2)},
            "healthy": exp_count >= 5 and not innovation_theater,
            "failure_mode": "Innovation theater — activity without shipped bets" if innovation_theater else None,
        }

        # 13. Competitive Intelligence Loop
        share_trend = metrics.get("relative_share_trend", 0.05)
        reactive_comp = metrics.get("reactive_to_competitors", False)
        results["competitive_intelligence"] = {
            "inputs": "Market/competitor data",
            "outputs": "Strategic repositioning",
            "feedback_signal": "Win/loss vs. named competitors",
            "kpis": {"relative_share_trend": share_trend, "feature_parity_gap": metrics.get("feature_parity_gap", 0.1)},
            "healthy": share_trend >= 0 and not reactive_comp,
            "failure_mode": "Reacting to competitors instead of running own strategy" if reactive_comp else None,
        }

        return results


# =====================================================================
# 4. Customer Journey Lifecycle (§4)
# =====================================================================
class CustomerLifecycleEngine:
    """Tracks and optimizes all 15 stages of the full customer lifecycle (§4)."""

    STAGES = [
        "Awareness",
        "Interest",
        "Consideration",
        "Evaluation",
        "Purchase",
        "Onboarding",
        "Activation",
        "Engagement",
        "Habit Formation",
        "Retention",
        "Loyalty",
        "Advocacy",
        "Referral",
        "Expansion",
        "Repurchase",
    ]

    STAGE_SPECIFICATIONS = {
        "Awareness": {
            "objective": "Enter consideration set",
            "psychology": "Pattern-matching against known categories",
            "metric": "Reach, unaided recall",
            "mistake": "Generic category messaging",
            "lever": "Sharp category framing / naming a new category",
        },
        "Interest": {
            "objective": "Earn attention",
            "psychology": "Curiosity vs. skepticism",
            "metric": "CTR, engagement rate",
            "mistake": "Feature-dumping",
            "lever": "Lead with the pain, not the product",
        },
        "Consideration": {
            "objective": "Differentiate",
            "psychology": "Comparing against status quo & alternatives",
            "metric": "Time-on-site, content depth",
            "mistake": "Competing on features competitors also have",
            "lever": "Reframe the comparison axis",
        },
        "Evaluation": {
            "objective": "Reduce perceived risk",
            "psychology": "Loss aversion dominates gain-seeking",
            "metric": "Trial starts, demo requests",
            "mistake": "Ignoring risk-reduction (guarantees, trials)",
            "lever": "Make failure cheap and reversible",
        },
        "Purchase": {
            "objective": "Convert intent to commitment",
            "psychology": "Decision fatigue, need for certainty",
            "metric": "Conversion rate",
            "mistake": "Friction in checkout/contracting",
            "lever": "Remove steps, not add persuasion",
        },
        "Onboarding": {
            "objective": "Deliver first value fast",
            "psychology": "Anxiety about wasted decision",
            "metric": "Time-to-first-value",
            "mistake": "Feature-tour instead of outcome-tour",
            "lever": "Anchor onboarding to the customer's specific job-to-be-done",
        },
        "Activation": {
            "objective": "Cross the 'aha' threshold",
            "psychology": "Forming initial habit loop",
            "metric": "Activation rate",
            "mistake": "Defining activation as login, not value",
            "lever": "Instrument the true 'aha' moment via cohort analysis",
        },
        "Engagement": {
            "objective": "Build usage depth",
            "psychology": "Reinforcement learning (reward loop)",
            "metric": "DAU/MAU, session depth",
            "mistake": "Engagement metrics that don't correlate with retention",
            "lever": "Optimize for the behavior that predicts retention, not raw activity",
        },
        "Habit Formation": {
            "objective": "Make usage automatic",
            "psychology": "Cue-routine-reward loop (Hook Model, BJ Fogg)",
            "metric": "Habit strength / frequency",
            "mistake": "No external trigger cadence",
            "lever": "Build reliable internal + external triggers",
        },
        "Retention": {
            "objective": "Prevent churn",
            "psychology": "Switching cost perception, sunk value",
            "metric": "Retention curve, churn",
            "mistake": "Measuring retention only in aggregate, not cohort",
            "lever": "Cohort-level retention curves, flattening point analysis",
        },
        "Loyalty": {
            "objective": "Deepen emotional/economic lock-in",
            "psychology": "Identity alignment with brand",
            "metric": "Repeat purchase rate",
            "mistake": "Assuming satisfaction = loyalty",
            "lever": "Build genuine switching costs (data, workflow, community)",
        },
        "Advocacy": {
            "objective": "Convert satisfaction to voice",
            "psychology": "Social proof-seeking, reciprocity",
            "metric": "NPS, UGC volume",
            "mistake": "Asking for advocacy before value is proven",
            "lever": "Ask at peak-value moments",
        },
        "Referral": {
            "objective": "Convert advocacy to acquisition",
            "psychology": "Trust transfer from peer to peer",
            "metric": "Viral coefficient (K)",
            "mistake": "Generic referral programs",
            "lever": "Incentive aligned with genuine value, not just cash",
        },
        "Expansion": {
            "objective": "Grow account value",
            "psychology": "Anchoring to current spend",
            "metric": "Net revenue retention",
            "mistake": "Under-selling adjacent value",
            "lever": "Usage-based expansion triggers",
        },
        "Repurchase": {
            "objective": "Sustain lifetime value",
            "psychology": "Habitual trust, low re-evaluation cost",
            "metric": "LTV, repurchase rate",
            "mistake": "Treating repurchase as passive",
            "lever": "Proactive lifecycle marketing tied to usage signals",
        },
    }

    def evaluate_journey(self, stage_metrics: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """Evaluate performance and optimization levers across all 15 stages."""
        results = {}
        for stage, spec in self.STAGE_SPECIFICATIONS.items():
            value = stage_metrics.get(stage.lower().replace(" ", "_"), 0.5)
            results[stage] = {
                "specification": spec,
                "current_metric_value": value,
                "needs_optimization": value < 0.60,
                "actionable_lever": spec["lever"],
            }
        return results


# =====================================================================
# 5. Company Growth System (§6)
# =====================================================================
class GrowthStageClassifier:
    """Classifies growth stage across the 9 stages and identifies binding constraints (§6)."""

    STAGES = [
        "Idea",
        "Validation",
        "Startup",
        "PMF",
        "Growth",
        "Scale",
        "Platform",
        "Ecosystem",
        "Market Leadership",
    ]

    STAGE_TABLE = {
        "Idea": {
            "primary_objective": "Falsify or strengthen hypothesis",
            "org_change": "Founder(s) only",
            "decision_making": "Founder intuition, fast",
            "capital_allocation": "Near-zero, sweat equity",
            "key_risk": "Solving a non-problem",
            "core_metric": "# of validated learnings",
            "binding_constraint": "Founder time",
        },
        "Validation": {
            "primary_objective": "Prove willingness to pay",
            "org_change": "First 1–3 hires",
            "decision_making": "Still founder-centric",
            "capital_allocation": "Pre-seed/seed capital",
            "key_risk": "False positive validation (friends/family bias)",
            "core_metric": "Paying customers / LOIs",
            "binding_constraint": "Signal quality",
        },
        "Startup": {
            "primary_objective": "Build repeatable acquisition",
            "org_change": "Functional roles emerge",
            "decision_making": "Founder + small team, high context-sharing",
            "capital_allocation": "Seed/Series A",
            "key_risk": "Premature scaling before PMF",
            "core_metric": "CAC:LTV early signal",
            "binding_constraint": "Cash runway",
        },
        "PMF": {
            "primary_objective": "Reach retention/growth threshold",
            "org_change": "First managers",
            "decision_making": "Data starts overriding intuition",
            "capital_allocation": "Growth capital",
            "key_risk": "Mistaking early traction for PMF",
            "core_metric": "Retention curve flattening",
            "binding_constraint": "Team bandwidth",
        },
        "Growth": {
            "primary_objective": "Scale what works",
            "org_change": "Middle management layer",
            "decision_making": "Process + data-driven",
            "capital_allocation": "Series B/C, aggressive if unit economics hold",
            "key_risk": "Scaling a broken funnel",
            "core_metric": "Growth rate, CAC payback",
            "binding_constraint": "Hiring velocity, systems",
        },
        "Scale": {
            "primary_objective": "Institutionalize repeatability",
            "org_change": "Departments, specialized functions",
            "decision_making": "Delegated, framework-driven",
            "capital_allocation": "Efficient growth capital",
            "key_risk": "Culture dilution, bureaucracy creep",
            "core_metric": "Rule of 40, NRR",
            "binding_constraint": "Org coordination cost",
        },
        "Platform": {
            "primary_objective": "Enable others to build on you",
            "org_change": "Platform/ecosystem teams",
            "decision_making": "Governance structures, APIs-as-product",
            "capital_allocation": "Infrastructure investment",
            "key_risk": "Platform without ecosystem demand",
            "core_metric": "Third-party developer/partner activity",
            "binding_constraint": "Trust from ecosystem partners",
        },
        "Ecosystem": {
            "primary_objective": "Orchestrate a multi-sided network",
            "org_change": "Ecosystem management, BD at scale",
            "decision_making": "Distributed decision rights",
            "capital_allocation": "Strategic/M&A capital",
            "key_risk": "Ecosystem fragmentation, partner conflict",
            "core_metric": "Ecosystem GMV / network density",
            "binding_constraint": "Governance credibility",
        },
        "Market Leadership": {
            "primary_objective": "Defend and extend category",
            "org_change": "Full corporate structure",
            "decision_making": "Board-level strategic governance",
            "capital_allocation": "Diversified, defensive + offensive",
            "key_risk": "Complacency, disruption from below",
            "core_metric": "Category share, moat durability",
            "binding_constraint": "Innovation velocity vs. incumbency drag",
        },
    }

    def classify_stage(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Classify current venture growth stage based on metrics."""
        paying_customers = metrics.get("paying_customers", 0)
        retention_flattened = metrics.get("retention_curve_flattened", False)
        arr_cents = metrics.get("arr_cents", 0)
        platform_api_users = metrics.get("platform_api_users", 0)
        ecosystem_partners = metrics.get("ecosystem_partners", 0)
        category_share = metrics.get("category_share", 0.0)

        stage_name = "Idea"
        if category_share >= 0.40:
            stage_name = "Market Leadership"
        elif ecosystem_partners >= 50:
            stage_name = "Ecosystem"
        elif platform_api_users >= 500:
            stage_name = "Platform"
        elif arr_cents >= 10_000_000_00:  # $10M ARR
            stage_name = "Scale"
        elif arr_cents >= 1_000_000_00:   # $1M ARR
            stage_name = "Growth"
        elif retention_flattened:
            stage_name = "PMF"
        elif paying_customers >= 10:
            stage_name = "Startup"
        elif paying_customers > 0:
            stage_name = "Validation"

        details = self.STAGE_TABLE[stage_name]
        return {
            "current_stage": stage_name,
            "stage_details": details,
            "primary_objective": details["primary_objective"],
            "binding_constraint": details["binding_constraint"],
            "key_risk": details["key_risk"],
            "core_metric": details["core_metric"],
        }


# =====================================================================
# 6. Moat Analyzer (§7)
# =====================================================================
class FirstPrinciplesMoatAnalyzer:
    """Evaluates the 6 competitive moat sources and technology cost curves (§7)."""

    MOAT_SOURCES = [
        "Network effects (direct, indirect, data)",
        "Switching costs (data lock-in, workflow embedding)",
        "Economies of scale (cost structure advantages)",
        "Brand (trust as a risk-reduction asset)",
        "Regulatory/IP protection",
        "Counter-positioning (Christensen model)",
    ]

    def evaluate_moats(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Compute moat strength across all 6 dimensions and composite durability score."""
        network_effects = min(1.0, metrics.get("network_density", 0.0))
        switching_costs = min(1.0, metrics.get("avg_switching_cost_cents", 0) / 10000_00)
        economies_of_scale = min(1.0, metrics.get("cost_advantage_percent", 0.0))
        brand = min(1.0, metrics.get("brand_trust_score", 0.0))
        regulatory_ip = min(1.0, metrics.get("patent_regulatory_moat_score", 0.0))
        counter_positioning = min(1.0, metrics.get("counter_positioning_score", 0.0))

        composite_score = float(
            0.25 * network_effects
            + 0.20 * switching_costs
            + 0.20 * economies_of_scale
            + 0.15 * brand
            + 0.10 * regulatory_ip
            + 0.10 * counter_positioning
        )

        return {
            "composite_moat_durability_score": round(composite_score, 4),
            "breakdown": {
                "network_effects": network_effects,
                "switching_costs": switching_costs,
                "economies_of_scale": economies_of_scale,
                "brand": brand,
                "regulatory_ip": regulatory_ip,
                "counter_positioning": counter_positioning,
            },
            "technology_shift_timing": {
                "cost_curve_viability_reached": metrics.get("cost_curve_viability_reached", True),
                "enabling_conditions_met": metrics.get("enabling_conditions_met", True),
            },
        }


# =====================================================================
# 7. Failure Mode Monitor (§8)
# =====================================================================
class FailureModeMonitor:
    """Pattern-matches operating metrics against the 10 failure modes (§8)."""

    FAILURE_MODES = {
        "solving_wrong_problem": {
            "root_cause": "Skipped root-cause analysis; solved a symptom",
            "detection_signal": "Low engagement despite positive survey feedback",
            "correction_mechanism": "Return to root-cause (5-Whys / Jobs-to-be-Done interviews)",
        },
        "building_before_validating": {
            "root_cause": "Founder conviction substituted for evidence",
            "detection_signal": "High build velocity, flat demand signal",
            "correction_mechanism": "Enforce a validation gate before build resourcing",
        },
        "weak_positioning": {
            "root_cause": "No clear 'instead of X, use us because Y'",
            "detection_signal": "High CAC, long sales cycles, feature comparison objections",
            "correction_mechanism": "Rebuild positioning around real alternative customers compare to",
        },
        "poor_pricing": {
            "root_cause": "Cost-plus instead of value-based pricing",
            "detection_signal": "High conversion at low price, but poor margin/expansion",
            "correction_mechanism": "Re-anchor price to quantified customer value",
        },
        "distribution_failure": {
            "root_cause": "Great product, no repeatable channel",
            "detection_signal": "High NPS, flat growth",
            "correction_mechanism": "Systematically test channels against ICP behavior, not founder preference",
        },
        "lack_of_pmf": {
            "root_cause": "Premature scaling of an unproven loop",
            "detection_signal": "Retention curve never flattens",
            "correction_mechanism": "Stop scaling; return to cohort-level retention work",
        },
        "organizational_bottlenecks": {
            "root_cause": "Decision rights not delegated as company scales",
            "detection_signal": "Rising decision latency, founder as single point of failure",
            "correction_mechanism": "Push decision rights down with clear frameworks",
        },
        "founder_bias": {
            "root_cause": "Overconfidence, confirmation bias, sunk cost",
            "detection_signal": "Ignoring disconfirming data, 'just needs more time' pattern",
            "correction_mechanism": "Pre-committed kill criteria set before launch",
        },
        "scaling_prematurely": {
            "root_cause": "Confusing early demand spike with durable PMF",
            "detection_signal": "CAC rising faster than LTV as spend scales",
            "correction_mechanism": "Re-test unit economics at each order-of-magnitude of spend",
        },
        "capital_misallocation": {
            "root_cause": "No opportunity-cost discipline in budgeting",
            "detection_signal": "Multiple underperforming bets funded simultaneously",
            "correction_mechanism": "Rank all initiatives on common expected-return basis quarterly",
        },
    }

    def diagnose_failure_modes(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Diagnose active failure modes based on operating metrics."""
        diagnoses: List[Dict[str, Any]] = []

        # 1. Solving wrong problem
        if metrics.get("survey_positive", False) and metrics.get("engagement_rate", 1.0) < 0.10:
            diagnoses.append({"failure_mode": "solving_wrong_problem", **self.FAILURE_MODES["solving_wrong_problem"]})

        # 2. Building before validating
        if metrics.get("build_velocity_high", False) and metrics.get("demand_growth", 0.0) <= 0.0:
            diagnoses.append(
                {"failure_mode": "building_before_validating", **self.FAILURE_MODES["building_before_validating"]}
            )

        # 3. Weak positioning
        if metrics.get("sales_cycle_days", 0) > 90 and metrics.get("feature_comparison_objections", False):
            diagnoses.append({"failure_mode": "weak_positioning", **self.FAILURE_MODES["weak_positioning"]})

        # 4. Poor pricing
        if metrics.get("cost_plus_pricing", False) or (
            metrics.get("conversion_rate", 0) > 0.20 and metrics.get("gross_margin", 1.0) < 0.40
        ):
            diagnoses.append({"failure_mode": "poor_pricing", **self.FAILURE_MODES["poor_pricing"]})

        # 5. Distribution failure
        if metrics.get("nps", 0) >= 60 and metrics.get("revenue_growth", 0.0) <= 0.0:
            diagnoses.append({"failure_mode": "distribution_failure", **self.FAILURE_MODES["distribution_failure"]})

        # 6. Lack of PMF
        if metrics.get("retention_curve_flattened") is False and metrics.get("spend_scaling", False):
            diagnoses.append({"failure_mode": "lack_of_pmf", **self.FAILURE_MODES["lack_of_pmf"]})

        # 7. Organizational bottlenecks
        if metrics.get("decision_latency_hours", 0) > 72 or metrics.get("founder_spof", False):
            diagnoses.append(
                {"failure_mode": "organizational_bottlenecks", **self.FAILURE_MODES["organizational_bottlenecks"]}
            )

        # 8. Founder bias
        if metrics.get("ignoring_disconfirming_data", False):
            diagnoses.append({"failure_mode": "founder_bias", **self.FAILURE_MODES["founder_bias"]})

        # 9. Scaling prematurely
        cac_growth = metrics.get("cac_growth_rate", 0.0)
        ltv_growth = metrics.get("ltv_growth_rate", 0.0)
        if cac_growth > ltv_growth and metrics.get("spend_scaling", False):
            diagnoses.append({"failure_mode": "scaling_prematurely", **self.FAILURE_MODES["scaling_prematurely"]})

        # 10. Capital misallocation
        if metrics.get("multiple_underperforming_bets", False):
            diagnoses.append({"failure_mode": "capital_misallocation", **self.FAILURE_MODES["capital_misallocation"]})

        return diagnoses


# =====================================================================
# 8. First-Principles EOS Engine (Unified Orchestrator)
# =====================================================================
class FirstPrinciplesEOSEngine:
    """Unified Orchestrator implementing the full 11-section EOS first-principles architecture."""

    def __init__(self) -> None:
        self.state_machine = EOSStateMachine()
        self.decision_tree = OpportunityDecisionTree()
        self.business_loops = CoupledBusinessLoopsEngine()
        self.customer_lifecycle = CustomerLifecycleEngine()
        self.growth_classifier = GrowthStageClassifier()
        self.moat_analyzer = FirstPrinciplesMoatAnalyzer()
        self.failure_monitor = FailureModeMonitor()

    def evaluate_venture_state(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Execute complete holistic first-principles evaluation across all EOS subsystems."""
        growth_stage = self.growth_classifier.classify_stage(metrics)
        moats = self.moat_analyzer.evaluate_moats(metrics)
        loops = self.business_loops.evaluate_all_loops(metrics)
        journey = self.customer_lifecycle.evaluate_journey(metrics)
        failures = self.failure_monitor.diagnose_failure_modes(metrics)

        return {
            "current_state": self.state_machine.current_state.value,
            "growth_stage": growth_stage,
            "moats": moats,
            "coupled_loops": loops,
            "customer_journey": journey,
            "failure_diagnoses": failures,
            "healthy": len(failures) == 0 and moats["composite_moat_durability_score"] >= 0.3,
        }
