from __future__ import annotations
import uuid
import logging
from enum import Enum
from datetime import datetime, UTC
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.kernel")


class TimeHorizon(str, Enum):
    VISION_10Y = "VISION_10Y"
    STRATEGY_5Y = "STRATEGY_5Y"
    ROADMAP_1Y = "ROADMAP_1Y"
    QUARTER = "QUARTER"
    MONTH = "MONTH"
    WEEK = "WEEK"
    DAY = "DAY"
    TASK = "TASK"
    ACTION = "ACTION"


class ExecutionNode(BaseModel):
    node_id: str = Field(default_factory=lambda: f"exec_node_{uuid.uuid4().hex[:8]}")
    name: str
    action_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    depends_on: List[str] = Field(default_factory=list)
    status: str = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED


class ExecutionDAG(BaseModel):
    id: str = Field(default_factory=lambda: f"dag_{uuid.uuid4().hex[:8]}")
    nodes: Dict[str, ExecutionNode] = Field(default_factory=dict)

    def add_node(self, node: ExecutionNode) -> None:
        self.nodes[node.node_id] = node

    def get_executable_nodes(self) -> List[ExecutionNode]:
        """Return nodes whose dependencies are fully completed and are pending."""
        executable = []
        for node in self.nodes.values():
            if node.status != "PENDING":
                continue
            deps_met = True
            for dep_id in node.depends_on:
                dep_node = self.nodes.get(dep_id)
                if not dep_node or dep_node.status != "COMPLETED":
                    deps_met = False
                    break
            if deps_met:
                executable.append(node)
        return executable


class EIOSKernel:
    """The central core of the Entrepreneurial Intelligence Operating System.

    Manages task scheduling, failure recovery (retries), and model routing.
    """

    def __init__(self) -> None:
        self.active_processes: Dict[str, ExecutionDAG] = {}
        self.metrics_history: List[Dict[str, Any]] = []

    def sense_opportunity_anomalies(self, signals: List[Dict[str, Any]], baseline: float = 1.0, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Analyzes input signals for structural anomalies vs noise, flagging high-surprise shifts."""
        anomalies = []
        for sig in signals:
            value = sig.get("value", 1.0)
            deviation = abs(value - baseline)
            is_anomaly = deviation > threshold
            if is_anomaly:
                anomalies.append({
                    "signal_id": sig.get("id", f"sig_{uuid.uuid4().hex[:4]}"),
                    "value": value,
                    "deviation": deviation,
                    "type": "structural_shift" if deviation > threshold * 2 else "significant_anomaly",
                    "description": sig.get("description", "Unnamed signal")
                })
        logger.info(f"[Kernel] Sensed {len(anomalies)} anomalies out of {len(signals)} signals.")
        return anomalies

    def generate_falsifiable_hypothesis(self, anomaly: Dict[str, Any], risk_type: str = "Type_II") -> Dict[str, Any]:
        """Converts an anomaly into a falsifiable claim with pre-committed kill criteria."""
        hyp_id = f"hyp_{uuid.uuid4().hex[:8]}"
        statement = f"If the observed anomaly '{anomaly.get('description')}' continues, pursuing this opportunity leads to compounding growth."

        # Pre-committed kill criteria based on risk types
        if risk_type == "Type_I":
            # Type I risk: high stakes, irreversible. Enforce slow, high-scrutiny criteria
            kill_criteria = "Fails to reach positive unit economics or clear legal trademark validation within 14 days."
            deliberation_speed = "slow_high_scrutiny"
        else:
            # Type II risk: reversible, low stakes. Fast, cheap experimentation
            kill_criteria = "Click-through rate (CTR) below 1.5% or interest validation fails within 72 hours."
            deliberation_speed = "fast_cheap"

        hypothesis = {
            "hypothesis_id": hyp_id,
            "anomaly_id": anomaly.get("signal_id"),
            "statement": statement,
            "risk_type": risk_type,
            "deliberation_speed": deliberation_speed,
            "kill_criteria": kill_criteria,
            "status": "under_test"
        }
        logger.info(f"[Kernel] Generated falsifiable hypothesis: {hyp_id}")
        return hypothesis

    def validate_opportunity_economics(self, cac: float, ltv: float, payback_months: float, gross_margin: float, threshold_cac_ltv: float = 3.0, max_payback: float = 12.0) -> Dict[str, Any]:
        """Calculates CAC, LTV, payback period, and gross margin, checking against economic viability thresholds."""
        ratio = ltv / cac if cac > 0 else float("inf")
        is_viable = (ratio >= threshold_cac_ltv) and (payback_months <= max_payback) and (gross_margin >= 0.5)

        result = {
            "cac_ltv_ratio": ratio,
            "payback_months": payback_months,
            "gross_margin": gross_margin,
            "is_viable": is_viable,
            "reasons": []
        }
        if ratio < threshold_cac_ltv:
            result["reasons"].append(f"CAC:LTV ratio {ratio:.2f} is below the threshold of {threshold_cac_ltv:.2f}")
        if payback_months > max_payback:
            result["reasons"].append(f"Payback period of {payback_months} months exceeds max allowed of {max_payback} months")
        if gross_margin < 0.5:
            result["reasons"].append(f"Gross margin {gross_margin:.2%} is below minimum requirement of 50%")

        logger.info(f"[Kernel] Validated economics: Viable={is_viable}")
        return result

    def allocate_capital_opportunity(self, treasury_total: float, request_amount: float, active_allocations: List[float]) -> Dict[str, Any]:
        """Implements capital allocation with a hard 35% treasury cap and 10% reserve governance ruleset."""
        cap_35 = treasury_total * 0.35
        reserve_10 = treasury_total * 0.10
        total_allocated = sum(active_allocations)
        available_treasury = treasury_total - total_allocated

        # Check if allocation would violate the 10% reserve or 35% single-cap rules
        if request_amount > cap_35:
            approved_amount = cap_35
            status = "PARTIALLY_APPROVED_CAPPED"
            reason = "Requested amount exceeded the maximum 35% single allocation cap."
        elif available_treasury - request_amount < reserve_10:
            approved_amount = max(0.0, available_treasury - reserve_10)
            status = "PARTIALLY_APPROVED_RESERVE_LIMIT"
            reason = "Requested amount would violate the mandatory 10% treasury reserve."
        else:
            approved_amount = request_amount
            status = "APPROVED"
            reason = "Allocation fully approved within governance limits."

        if approved_amount <= 0:
            status = "REJECTED"
            approved_amount = 0.0

        logger.info(f"[Kernel] Capital allocation check: {status} (Approved={approved_amount})")
        return {
            "status": status,
            "approved_amount": approved_amount,
            "reason": reason,
            "remaining_available": available_treasury - approved_amount
        }

    def reason_gtm_channel(self, product_price: float, complexity: str, network_effects: bool) -> Dict[str, Any]:
        """Recommends GTM motion (PLG vs SLG vs CLG) based on product price, complexity, and network effects."""
        # Simple strategic logic tree
        if network_effects and product_price < 100:
            motion = "CLG" # Community-Led Growth
            reason = "Low price combined with network effects favors a community-led strategy."
        elif product_price < 250 and complexity in ["low", "medium"]:
            motion = "PLG" # Product-Led Growth
            reason = "Low to medium complexity and self-serve pricing favors a product-led motion."
        else:
            motion = "SLG" # Sales-Led Growth
            reason = "High price or complexity warrants a high-touch, sales-led enterprise motion."

        logger.info(f"[Kernel] GTM Recommendation: {motion}")
        return {
            "recommended_motion": motion,
            "reason": reason,
            "channels": ["content", "referral"] if motion == "PLG" else ["enterprise_sales", "partnerships"] if motion == "SLG" else ["community", "referral"]
        }

    def analyze_moat_durability(self, active_moats: List[str], metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates moat types and calculates a durability score, scanning for competitive/positioning failure modes."""
        score = 0.0
        details = {}
        for moat in active_moats:
            if moat == "network_effects":
                score += 0.3
                details["network_effects"] = "Direct or indirect network density increases lock-in."
            elif moat == "switching_costs":
                score += 0.25
                details["switching_costs"] = "High workflow or data embedding prevents migration."
            elif moat == "economies_of_scale":
                score += 0.2
                details["economies_of_scale"] = "Cost structures provide insurmountable volume advantages."
            elif moat == "brand":
                score += 0.15
                details["brand"] = "Trust-based pricing power reduces choice risk."
            elif moat == "counter_positioning":
                score += 0.1
                details["counter_positioning"] = "Superior model that incumbents cannot copy without business damage."

        # Scan for failure modes
        failure_modes = []
        customer_retention = metrics.get("retention_rate", 1.0)
        competitor_pricing_undercut = metrics.get("competitor_undercut", False)

        if customer_retention < 0.8:
            failure_modes.append({
                "type": "weak_positioning",
                "severity": "high",
                "description": "Retention rate is below 80%. High churn indicates building for the loudest customer rather than representative ICP."
            })
        if competitor_pricing_undercut and "counter_positioning" not in active_moats:
            failure_modes.append({
                "type": "poor_pricing_resistance",
                "severity": "medium",
                "description": "Competitor undercutting threatens revenue. Lack of counter-positioning leaves pricing vulnerable."
            })

        durability = "strong" if score >= 0.5 else "moderate" if score >= 0.25 else "weak"
        logger.info(f"[Kernel] Moat Durability analyzed: Score={score:.2f} ({durability})")
        return {
            "durability_score": min(1.0, score),
            "durability_level": durability,
            "active_moats": active_moats,
            "moat_descriptions": details,
            "failure_modes_detected": failure_modes
        }

    def evaluate_lifecycle_stage(self, active_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Identifies current growth stage and flags risks of premature scaling."""
        has_validated_learnings = active_metrics.get("validated_learnings", 0) > 0
        paying_customers = active_metrics.get("paying_customers", 0)
        has_repeatable_acquisition = active_metrics.get("repeatable_acquisition", False)
        is_retention_flat = active_metrics.get("retention_curve_flattened", False)
        scale_spend = active_metrics.get("marketing_scale_spend", False)

        stage = "Idea"
        risk_flags = []

        if has_validated_learnings:
            stage = "Validation"
        if paying_customers >= 5:
            stage = "Startup"
        if has_repeatable_acquisition and is_retention_flat:
            stage = "PMF"
        if stage == "PMF" and scale_spend:
            stage = "Growth"

        # Check for premature scaling
        if scale_spend and stage != "Growth" and stage != "PMF":
            risk_flags.append({
                "type": "premature_scaling",
                "severity": "critical",
                "description": f"Scaling marketing spend while company is classified in the '{stage}' stage. Enforce PMF/retention-curve flattening beforehand."
            })

        logger.info(f"[Kernel] Lifecycle Stage: {stage} (Risk Flags Count={len(risk_flags)})")
        return {
            "current_stage": stage,
            "is_ready_to_scale": stage in ["PMF", "Growth"],
            "detected_risks": risk_flags
        }

    def trigger_reinvention_review(self, leading_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Checks leading indicators of decline/disruption to trigger periodic self-disruption and reinvention reviews."""
        nps_trend = leading_indicators.get("nps_trend", "stable")
        cac_trend = leading_indicators.get("cac_trend", "stable")
        market_share_trend = leading_indicators.get("market_share_trend", "stable")
        decision_latency = leading_indicators.get("decision_latency_days", 1.0)

        trigger_reasons = []
        if nps_trend == "declining":
            trigger_reasons.append("NPS is in decline, indicating customer value erosion.")
        if cac_trend == "rising_rapidly":
            trigger_reasons.append("CAC is rising rapidly, implying channels are reaching saturation or ad exhaustion.")
        if market_share_trend == "declining":
            trigger_reasons.append("Market share trend is negative, suggesting competitive displacement.")
        if decision_latency > 7.0:
            trigger_reasons.append("Decision latency exceeds 7 days, indicating organizational bureaucratic creep.")

        must_reinvent = len(trigger_reasons) >= 2
        logger.info(f"[Kernel] Reinvention trigger check: {must_reinvent} (Reasons={len(trigger_reasons)})")
        return {
            "trigger_reinvention": must_reinvent,
            "reasons": trigger_reasons,
            "action_recommended": "Initiate continuous reinvention phase (S) immediately" if must_reinvent else "Maintain standard operational monitoring (R)"
        }

    async def execute_dag(self, dag: ExecutionDAG) -> bool:
        """Schedules and executes the compiled DAG with failure recovery."""
        logger.info(f"[Kernel] Initiating execution DAG: {dag.id}")
        self.active_processes[dag.id] = dag

        max_loops = 50
        loop_count = 0

        while loop_count < max_loops:
            executable = dag.get_executable_nodes()
            if not executable:
                # Check if all nodes are completed
                all_done = all(node.status == "COMPLETED" for node in dag.nodes.values())
                if all_done:
                    logger.info(f"[Kernel] Execution DAG {dag.id} completed successfully.")
                    return True
                # If some failed or circular reference
                any_failed = any(node.status == "FAILED" for node in dag.nodes.values())
                if any_failed:
                    logger.error(f"[Kernel] Execution DAG {dag.id} halted due to node failure.")
                    return False
                break

            for node in executable:
                node.status = "RUNNING"
                logger.info(f"[Kernel] Dispatching node: {node.name} ({node.action_type})")

                # Simple simulated execution with auto-retry recovery logic
                success = False
                retries = 3
                for attempt in range(1, retries + 1):
                    try:
                        # Success simulations
                        success = True
                        break
                    except Exception as e:
                        logger.warning(f"[Kernel] Retry {attempt}/{retries} for node {node.node_id} failed: {e}")

                if success:
                    node.status = "COMPLETED"
                    logger.info(f"[Kernel] Node {node.node_id} completed successfully.")
                else:
                    node.status = "FAILED"
                    logger.error(f"[Kernel] Node {node.node_id} failed permanently after {retries} retries.")

            loop_count += 1

        return False


class EntrepreneurialCompiler:
    """Translates high-level business goals into a structured, executable DAG (Layer 18 Compiler)."""

    def compile_goal_to_dag(self, goal: str, target_budget_usd: int) -> ExecutionDAG:
        logger.info(f"[Compiler] Compiling strategic goal: '{goal}'")
        dag = ExecutionDAG()

        # Step 1: Research Node
        node_research = ExecutionNode(name="Conjoint Market Research", action_type="research_only", payload={"goal": goal})
        dag.add_node(node_research)

        # Step 2: Feasibility Node (Depends on Research)
        node_feasibility = ExecutionNode(
            name="Feasibility Financial Model",
            action_type="research_only",
            payload={"budget": target_budget_usd},
            depends_on=[node_research.node_id]
        )
        dag.add_node(node_feasibility)

        # Step 3: Brand & Positioning Node (Depends on Feasibility)
        node_brand = ExecutionNode(
            name="Brand Positioning and Trademark Check",
            action_type="publishing",
            payload={"brand_name": "ApodexPro"},
            depends_on=[node_feasibility.node_id]
        )
        dag.add_node(node_brand)

        # Step 4: Execution Node (Depends on Brand)
        node_exec = ExecutionNode(
            name="Deploy GTM Ads Campaign",
            action_type="spending",
            payload={"spend_cents": 5000_00},
            depends_on=[node_brand.node_id]
        )
        dag.add_node(node_exec)

        return dag


class HierarchicalActiveInference:
    """Cascading active inference tracking uncertainty reduction across organization layers (Layer 13)."""

    def __init__(self) -> None:
        # Layer levels: Company -> Department -> Team -> Agent -> Action
        self.uncertainty_levels = {
            "company": 0.8,
            "department": 0.7,
            "team": 0.6,
            "agent": 0.5,
            "action": 0.4
        }

    def calculate_layer_free_energy(self, layer: str, actual_outcome: float, expected_outcome: float) -> float:
        """Compute the Variational Free Energy for a specific layer."""
        error = actual_outcome - expected_outcome
        complexity = 0.1 * len(layer)  # simple complexity heuristic
        free_energy = complexity + (error ** 2)

        # Adjust estimated uncertainty based on prediction accuracy
        current_uncertainty = self.uncertainty_levels.get(layer, 0.5)
        self.uncertainty_levels[layer] = max(0.01, min(0.99, current_uncertainty + 0.1 * error))

        logger.info(f"[Active Inference Hierarchy] Layer {layer} Free Energy: {free_energy:.4f}, New Uncertainty: {self.uncertainty_levels[layer]:.2f}")
        return free_energy


class RecursivePlanner:
    """Synchronizes strategic milestones across multi-scale time horizons (Layer 14)."""

    def __init__(self) -> None:
        self.plan_registry: Dict[TimeHorizon, List[str]] = {th: [] for th in TimeHorizon}

    def register_plan(self, horizon: TimeHorizon, items: List[str]) -> None:
        self.plan_registry[horizon] = items
        logger.info(f"[Recursive Planner] Registered {len(items)} items for timescale: {horizon.value}")

    def cascade_vision_down(self, vision: str) -> None:
        """Cascade 10-year vision down to strategy, roadmap, and daily execution tasks."""
        self.register_plan(TimeHorizon.VISION_10Y, [vision])
        self.register_plan(TimeHorizon.STRATEGY_5Y, [f"Scale SaaS core based on: {vision}"])
        self.register_plan(TimeHorizon.ROADMAP_1Y, ["Target LTV:CAC >= 3:1 in SMB segment", "Establish trademark clearance"])
        self.register_plan(TimeHorizon.QUARTER, ["Conjoint survey validation", "Incorporate brand identity"])
        self.register_plan(TimeHorizon.WEEK, ["Run RCT price elasticity experiments", "Validate advertising CTRs"])
        self.register_plan(TimeHorizon.DAY, ["Track social trends", "Observe cohort feedback metrics"])
