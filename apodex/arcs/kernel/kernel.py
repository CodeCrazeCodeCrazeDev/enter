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
        # Active SCM Structural Causal Model paths
        self.causal_graph_edges: Dict[str, List[str]] = {
            "traffic_growth": ["conversions"],
            "pricing": ["unit_margins", "conversions"],
            "spend_cents": ["traffic_growth", "cac"],
            "retention": ["ltv"],
            "ltv": ["unit_margins"],
        }
        # SOTA cost curve mappings (baseline multipliers)
        self.cost_curves: Dict[str, float] = {
            "compute": 0.85,    # 15% YoY reduction
            "storage": 0.90,    # 10% YoY reduction
            "bandwidth": 0.95,  # 5% YoY reduction
            "batteries": 0.80,  # 20% YoY reduction
        }

    # ------------------------------------------------------------------
    # Native Cognitive Capabilities (Integrated EOS loops)
    # ------------------------------------------------------------------
    def sense_opportunity_anomalies(self, signal_name: str, actual_value: float, model_expectation: float) -> Dict[str, Any]:
        """Detect structural shifts or anomalies from environmental signals.

        Refences Kuhn's paradigm-shift theory and Bayesian surprise literature.
        """
        surprise = abs(actual_value - model_expectation) / max(1e-9, model_expectation)
        is_anomaly = surprise > 0.25  # Anomaly threshold: 25% deviation

        result = {
            "signal": signal_name,
            "actual": actual_value,
            "expected": model_expectation,
            "surprise_ratio": surprise,
            "is_anomaly": is_anomaly,
            "classification": "STRUCTURAL_SHIFT" if is_anomaly else "NOISE",
            "timestamp": datetime.now(UTC).isoformat()
        }
        logger.info(f"[EIOS Sensing] Signal '{signal_name}' anomaly test: {result['classification']} (surprise: {surprise:.2%})")
        return result

    def generate_falsifiable_hypothesis(self, anomaly_report: Dict[str, Any], target_metric: str) -> Dict[str, Any]:
        """Convert anomalies into falsifiable claims with pre-committed kill criteria.

        Utilizes McGrath's Discovery-Driven Planning and Real Options theory.
        """
        signal_name = anomaly_report.get("signal", "unknown")
        # Formulation of structured falsifiable hypothesis
        statement = f"If we intervene on {signal_name}, we will observe a positive shift in {target_metric}."

        hypothesis = {
            "id": f"hyp_{uuid.uuid4().hex[:8]}",
            "statement": statement,
            "kill_criteria": {
                "max_test_cost_usd": 150.0,
                "min_success_threshold": 0.05,  # 5% target conversion
                "max_sample_size": 200
            },
            "risk_type": "TYPE_II" if signal_name in ["pricing", "features"] else "TYPE_I",
            "belief_prior": 0.50,  # Default neutral prior
            "status": "PROPOSED"
        }
        logger.info(f"[EIOS Hypothesis] Generated {hypothesis['risk_type']} hypothesis {hypothesis['id']}: '{statement}'")
        return hypothesis

    def validate_opportunity_economics(self, smoke_test_conversions: int, total_visits: int, ltv_cents: int, test_spend_cents: int) -> Dict[str, Any]:
        """Evaluate smoke-test conversion rates, project CAC, LTV, and economic viability.

        Formula:
          Conversion Rate = conversions / visits
          CAC = spend / conversions
          LTV_to_CAC = LTV / CAC
        """
        conversion_rate = smoke_test_conversions / max(1, total_visits)
        cac_cents = test_spend_cents / max(1, smoke_test_conversions)
        ltv_to_cac = ltv_cents / max(1, cac_cents)

        is_viable = ltv_to_cac >= 3.0 and conversion_rate >= 0.03

        result = {
            "conversion_rate": conversion_rate,
            "projected_cac_cents": cac_cents,
            "projected_ltv_cents": ltv_cents,
            "ltv_to_cac_ratio": ltv_to_cac,
            "is_viable": is_viable,
            "decision": "VALIDATED" if is_viable else "KILL_SIGNAL"
        }
        logger.info(f"[EIOS Validation] Opportunity economics validated: {is_viable} (LTV:CAC ratio: {ltv_to_cac:.2f})")
        return result

    def allocate_capital_opportunity(self, validated_result: Dict[str, Any], available_budget_cents: int) -> Dict[str, Any]:
        """Enforces opportunity-cost discipline in budgeting using risk-adjusted return weighting."""
        ltv_to_cac = validated_result.get("ltv_to_cac_ratio", 0.0)
        is_viable = validated_result.get("is_viable", False)

        # Risk-adjusted return metric
        allocation_weight = min(1.0, ltv_to_cac / 10.0) if is_viable else 0.0
        allocated_cents = int(available_budget_cents * allocation_weight)

        result = {
            "allocation_weight": allocation_weight,
            "allocated_cents": allocated_cents,
            "reinvestment_capacity_cents": available_budget_cents - allocated_cents,
            "opportunity_cost_met": allocated_cents > 0
        }
        logger.info(f"[EIOS Capital] Allocated {allocated_cents / 100:.2f} USD based on allocation weight {allocation_weight:.2%}")
        return result

    def reason_gtm_channel(self, product_complexity_score: float, acv_usd: int) -> str:
        """Determine the optimal GTM channel (PLG vs SLG) based on product complexity and ACV.

        Rules:
          - High ACV (>= $5000) and High Complexity (>= 0.7) -> Sales-Led Growth (SLG) / Enterprise
          - Low ACV and Low Complexity -> Product-Led Growth (PLG)
          - Else -> Hybrid Growth (SLG-PLG land & expand)
        """
        if acv_usd >= 5000 and product_complexity_score >= 0.7:
            channel = "SALES_LED_GROWTH"
        elif acv_usd < 1000 and product_complexity_score < 0.4:
            channel = "PRODUCT_LED_GROWTH"
        else:
            channel = "HYBRID_GROWTH"

        logger.info(f"[EIOS GTM] Recompiling channel decision: {channel} (ACV: ${acv_usd}, Complexity: {product_complexity_score})")
        return channel

    def analyze_moat_durability(self, network_coefficient: float, user_switching_cost_usd: float) -> Dict[str, Any]:
        """Score the durability of the competitive moat (Brand, Switching, Scale, Regulatory)."""
        moat_score = (network_coefficient * 50) + (user_switching_cost_usd / 10)
        durability = "WEAK"
        if moat_score >= 80:
            durability = "UNASSAILABLE"
        elif moat_score >= 40:
            durability = "DEFENSIBLE"

        result = {
            "moat_score": moat_score,
            "durability": durability,
            "has_network_effects": network_coefficient > 0.5,
            "switching_cost_usd": user_switching_cost_usd
        }
        logger.info(f"[EIOS Moat] Competitive moat scored: {durability} (Score: {moat_score:.2f})")
        return result

    def evaluate_lifecycle_stage(self, active_months: int, monthly_active_users: int, monthly_revenue_usd: int) -> str:
        """Classify the venture's exact organizational stage and flag premature scaling risks.

        Stages: IDEA -> VALIDATION -> STARTUP -> PMF -> GROWTH -> SCALE -> PLATFORM -> ECOSYSTEM -> LEADERSHIP
        """
        if monthly_active_users >= 100000 and monthly_revenue_usd >= 1000000:
            stage = "MARKET_LEADERSHIP"
        elif monthly_active_users >= 50000:
            stage = "SCALE"
        elif monthly_active_users >= 10000 and monthly_revenue_usd >= 20000:
            stage = "GROWTH"
        elif monthly_active_users >= 1000:
            stage = "PRODUCT_MARKET_FIT"
        elif monthly_active_users >= 100:
            stage = "STARTUP"
        elif active_months >= 1:
            stage = "VALIDATION"
        else:
            stage = "IDEA"

        logger.info(f"[EIOS Lifecycle] Venture stage classified: {stage} (MAU: {monthly_active_users}, Rev: ${monthly_revenue_usd})")
        return stage

    def trigger_reinvention_review(self, market_share_delta: float, customer_satisfaction_index: float) -> bool:
        """Forcibly trigger a strategic self-disruption review before external disruption occurs."""
        # Trigger review if market share is declining (> 5% drop) or customer satisfaction dips below 70%
        trigger = market_share_delta < -0.05 or customer_satisfaction_index < 0.70
        if trigger:
            logger.warning("[EIOS Reinvention] ALERT: Strategic self-disruption review TRIGGERED due to leading risk indicators!")
        else:
            logger.info("[EIOS Reinvention] Leading indicators healthy. Strategic reinvention running in parallel.")
        return trigger

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
