from __future__ import annotations
import uuid
import logging
from enum import Enum
from datetime import datetime, UTC
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from apodex.ai_eos.intelligence.eos_first_principles import (
    AIEOSAutonomousModules,
    RiskType,
    CustomerStage,
    GrowthStage
)

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
    and native first-principles EOS cognitive capabilities.
    """

    def __init__(self) -> None:
        self.active_processes: Dict[str, ExecutionDAG] = {}
        self.metrics_history: List[Dict[str, Any]] = []
        self.eos_modules = AIEOSAutonomousModules()

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

    # Native First-Principles EOS Cognitive Capabilities

    def sense_opportunity_anomalies(self, description: str, observed: float, expected: float) -> Dict[str, Any]:
        """Detects anomalies and evaluates Kuhn paradigm threshold."""
        anomaly, is_structural = self.eos_modules.signal_engine.detect_anomaly(description, observed, expected)
        return {
            "anomaly_id": anomaly.anomaly_id,
            "surprise_score": anomaly.kuhn_surprise_score,
            "is_structural": is_structural
        }

    def generate_falsifiable_hypothesis(self, claim: str, risk_type: str, test_cost: float, info_val: float) -> Dict[str, Any]:
        """Formulates a mathematically falsifiable hypothesis with risk classification."""
        rt = RiskType.TYPE_I if risk_type.upper() == "TYPE_I" else RiskType.TYPE_II
        hyp = self.eos_modules.signal_engine.form_hypothesis(claim, rt, test_cost, info_val)
        return {
            "hypothesis_id": hyp.hypothesis_id,
            "claim": hyp.claim,
            "risk_type": hyp.risk_type.value,
            "prior_prob": hyp.prior_probability
        }

    def validate_opportunity_economics(self, hypothesis_claim: str, likelihood_true: float, likelihood_false: float) -> Dict[str, Any]:
        """Executes Bayesian belief updates and checks for falsification."""
        hyp = self.eos_modules.signal_engine.form_hypothesis(hypothesis_claim, RiskType.TYPE_II, 100.0, 1000.0)
        hyp = self.eos_modules.signal_engine.update_bayesian_belief(hyp, likelihood_true, likelihood_false)
        return {
            "hypothesis_id": hyp.hypothesis_id,
            "posterior_probability": hyp.posterior_probability,
            "is_falsified": hyp.is_falsified
        }

    def allocate_capital_opportunity(self, telemetry: Dict[str, Any], claim: str) -> Dict[str, Any]:
        """Runs the full 10-module autonomous cycle from sensing to capital allocation."""
        return self.eos_modules.run_full_sensing_to_allocation_cycle(telemetry, claim)

    def reason_gtm_channel(self, price_usd: float, complexity: str) -> str:
        """Determines channel motion based on positioning and price point."""
        if price_usd >= 25000.0 or complexity.lower() == "high":
            return "ENTERPRISE_SALES_LED"
        elif price_usd <= 1000.0 and complexity.lower() == "low":
            return "PRODUCT_LED_GROWTH_PLG"
        else:
            return "HYBRID_CONTENT_SALES"

    def analyze_moat_durability(self, power_type: str) -> float:
        """Scores moat durability based on Helmer's 7 Powers framework."""
        powers_durability = {
            "NETWORK_EFFECTS": 0.95,
            "CORNERED_RESOURCE": 0.90,
            "SWITCHING_COSTS": 0.85,
            "SCALE_ECONOMIES": 0.80,
            "COUNTER_POSITIONING": 0.80,
            "PROCESS_POWER": 0.75,
            "BRAND": 0.70
        }
        return powers_durability.get(power_type.upper(), 0.50)

    def evaluate_lifecycle_stage(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates company growth stage and binding constraint."""
        stage, constraint = self.eos_modules.stage_classifier.classify_stage(metrics)
        return {
            "growth_stage": stage.value,
            "binding_constraint": constraint
        }

    def trigger_reinvention_review(self, current_stage: str, market_share: float) -> bool:
        """Triggers self-disruption/reinvention review during market leadership."""
        if current_stage == GrowthStage.MARKET_LEADERSHIP.value and market_share >= 0.35:
            logger.info("[Kernel] Continuous Reinvention review triggered for market leader.")
            return True
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
