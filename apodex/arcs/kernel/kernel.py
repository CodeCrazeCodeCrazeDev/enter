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

    Manages task scheduling, failure recovery (retries), model routing,
    and native cognitive entrepreneurial capabilities.
    """

    def __init__(self) -> None:
        self.active_processes: Dict[str, ExecutionDAG] = {}
        self.metrics_history: List[Dict[str, Any]] = []

    def sense_opportunity_anomalies(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters incoming signals for structural anomalies vs noise."""
        from ...ai_eos.intelligence.eos_first_principles import Signal, SignalToIdeaPipeline
        pipeline = SignalToIdeaPipeline()
        anomalies = []
        for s in signals:
            sig = Signal(
                signal_id=s.get("id", uuid.uuid4().hex[:8]),
                source=s.get("source", "unknown"),
                content=s.get("content", ""),
                is_anomaly=s.get("is_anomaly", True),
                structural_shift_probability=s.get("structural_shift_probability", 0.8),
                noise_level=s.get("noise_level", 0.2)
            )
            if pipeline.filter_signal(sig):
                anomalies.append(s)
        return anomalies

    def generate_falsifiable_hypothesis(self, anomaly: Dict[str, Any]) -> Dict[str, Any]:
        """Converts an anomaly signal into a structured falsifiable hypothesis with kill criteria."""
        content = anomaly.get("content", "Structural Shift Opportunity")
        return {
            "hypothesis_id": f"hyp_{uuid.uuid4().hex[:8]}",
            "claim": f"If structural shift holds: {content}",
            "falsification_condition": "Cheap test CTR < 2% or conversion < 1%",
            "status": "PROPOSED",
            "created_at": datetime.now(UTC).isoformat()
        }

    def validate_opportunity_economics(self, hypothesis: Dict[str, Any], test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates unit economics and cheap real-option test results."""
        from ...ai_eos.intelligence.eos_first_principles import SignalToIdeaPipeline
        pipeline = SignalToIdeaPipeline()
        test_cost = test_data.get("cost_usd", 100.0)
        info_gain = test_data.get("expected_info_gain", 10.0)
        valid = pipeline.evaluate_cheap_test(test_cost, info_gain)

        arpu = test_data.get("arpu_usd", 50.0)
        cac = test_data.get("cac_usd", 30.0)
        healthy = (arpu / max(1.0, cac)) >= 1.5

        return {
            "hypothesis_id": hypothesis.get("hypothesis_id"),
            "cheap_test_passed": valid,
            "unit_economics_viable": healthy,
            "decision": "PROCEED" if (valid and healthy) else "DISCARD"
        }

    def allocate_capital_opportunity(self, initiatives: List[Dict[str, Any]], total_budget_cents: int) -> Dict[str, int]:
        """Allocates budget across active initiatives based on expected return and risk."""
        if not initiatives:
            return {}
        total_score = sum(i.get("expected_return_score", 1.0) for i in initiatives)
        allocations = {}
        for i in initiatives:
            init_id = i.get("id", uuid.uuid4().hex[:8])
            share = i.get("expected_return_score", 1.0) / max(0.001, total_score)
            allocations[init_id] = int(total_budget_cents * share)
        return allocations

    def reason_gtm_channel(
        self,
        product_complexity: str,
        price_point_cents: int,
        network_effects: bool
    ) -> List[str]:
        """Determines optimal distribution channels using GTMSystem rules."""
        from ...ai_eos.intelligence.eos_first_principles import GTMSystem
        gtm = GTMSystem()
        price_usd = price_point_cents / 100.0
        channels = gtm.select_optimal_distribution_channels(product_complexity, price_usd, network_effects)
        return [c.value for c in channels]

    def analyze_moat_durability(self, moat_metrics: Dict[str, float]) -> float:
        """Calculates normalized composite moat durability score [0, 1]."""
        from ...ai_eos.intelligence.eos_first_principles import MoatEvaluator
        evaluator = MoatEvaluator()
        return evaluator.calculate_composite_moat_score(
            network_density=moat_metrics.get("network_density", 0.5),
            avg_switching_cost_usd=moat_metrics.get("avg_switching_cost_usd", 1000.0),
            brand_trust_score=moat_metrics.get("brand_trust_score", 0.5),
            cost_advantage_percent=moat_metrics.get("cost_advantage_percent", 0.2),
            ip_protection_score=moat_metrics.get("ip_protection_score", 0.3),
            counter_positioning_score=moat_metrics.get("counter_positioning_score", 0.4)
        )

    def evaluate_lifecycle_stage(self, company_metrics: Dict[str, Any]) -> str:
        """Classifies venture stage across the 9 company growth stages."""
        from ...ai_eos.intelligence.eos_first_principles import CompanyGrowthEngine
        engine = CompanyGrowthEngine()
        stage = engine.classify_stage(
            paying_customers=company_metrics.get("paying_customers", 0),
            nrr=company_metrics.get("nrr", 1.0),
            retention_flattens=company_metrics.get("retention_flattens", False),
            annual_revenue_usd=company_metrics.get("annual_revenue_usd", 0.0)
        )
        return stage.value

    def trigger_reinvention_review(self, revenue_decay: float, churn_rate: float) -> bool:
        """Checks whether structural metric decay mandates a self-disruption review."""
        return (revenue_decay > 0.15 and churn_rate > 0.20)

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
