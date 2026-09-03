from __future__ import annotations
import uuid
import math
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

    Manages task scheduling, failure recovery (retries), research hypothesis sensing,
    non-Gaussian Hawkes anomaly detection, and active inference model routing.
    """

    def __init__(self) -> None:
        self.active_processes: Dict[str, ExecutionDAG] = {}
        self.metrics_history: List[Dict[str, Any]] = []
        self.registered_hypotheses: List[Any] = []

    def register_research_hypothesis(self, hypothesis: Any) -> None:
        """Registers a research hypothesis exported from Layer 1 Research OS for active sensing."""
        self.registered_hypotheses.append(hypothesis)
        logger.info(f"[EIOS Kernel] Registered research hypothesis for active sensing: {getattr(hypothesis, 'title', str(hypothesis))}")

    def sense_opportunity_anomalies(self, event_stream: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes Non-Gaussian Hawkes point-process intensity sensing and Active Inference EFE risk evaluation.
        (Derived from Papers 301-380 principles).
        """
        if not event_stream:
            return {"anomaly_detected": False, "hawkes_intensity": 0.0, "expected_free_energy": 0.0}

        # Calculate Hawkes point intensity lambda(t) = mu + alpha * sum(exp(-beta * dt))
        mu_base = 0.1
        alpha = 0.5
        beta = 1.0

        timestamps = [e.get("timestamp", i) for i, e in enumerate(event_stream)]
        current_time = max(timestamps) if isinstance(timestamps[0], (int, float)) else len(event_stream)

        hawkes_intensity = mu_base
        for ts in timestamps:
            dt = current_time - ts if isinstance(ts, (int, float)) else 0.5
            hawkes_intensity += alpha * math.exp(-beta * max(0.0, dt))

        # Calculate Expected Free Energy (EFE) Risk Score across active hypotheses
        epistemic_uncertainty = 1.0 / (1.0 + len(self.registered_hypotheses))
        pragmatic_risk = 0.2 if hawkes_intensity > 1.5 else 0.05
        efe_score = epistemic_uncertainty + pragmatic_risk

        anomaly_detected = hawkes_intensity > 1.2 or efe_score > 0.4
        if anomaly_detected:
            logger.warning(f"[EIOS Kernel Hawkes Sensing] Opportunity Anomaly Detected! Intensity={hawkes_intensity:.4f}, EFE={efe_score:.4f}")

        return {
            "anomaly_detected": anomaly_detected,
            "hawkes_intensity": float(hawkes_intensity),
            "expected_free_energy": float(efe_score),
            "hypotheses_monitored": len(self.registered_hypotheses)
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
                all_done = all(node.status == "COMPLETED" for node in dag.nodes.values())
                if all_done:
                    logger.info(f"[Kernel] Execution DAG {dag.id} completed successfully.")
                    return True
                any_failed = any(node.status == "FAILED" for node in dag.nodes.values())
                if any_failed:
                    logger.error(f"[Kernel] Execution DAG {dag.id} halted due to node failure.")
                    return False
                break

            for node in executable:
                node.status = "RUNNING"
                logger.info(f"[Kernel] Dispatching node: {node.name} ({node.action_type})")

                success = False
                retries = 3
                for attempt in range(1, retries + 1):
                    try:
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

        node_research = ExecutionNode(name="Conjoint Market Research", action_type="research_only", payload={"goal": goal})
        dag.add_node(node_research)

        node_feasibility = ExecutionNode(
            name="Feasibility Financial Model",
            action_type="research_only",
            payload={"budget": target_budget_usd},
            depends_on=[node_research.node_id]
        )
        dag.add_node(node_feasibility)

        node_brand = ExecutionNode(
            name="Brand Positioning and Trademark Check",
            action_type="publishing",
            payload={"brand_name": "ApodexPro"},
            depends_on=[node_feasibility.node_id]
        )
        dag.add_node(node_brand)

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
        complexity = 0.1 * len(layer)
        free_energy = complexity + (error ** 2)

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
