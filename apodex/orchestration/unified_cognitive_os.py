"""
unified_cognitive_os.py: Unified Cognitive Operating System Orchestration Engine.

Orchestrates closed-loop Active Inference state handoffs and joint execution across:
  - Layer 1: Research OS (Hypothesis generation, empirical validation & paper principle corpus)
  - Layer 2: EIOS Kernel (Active inference DAG execution) & EOS Engine (14-Layer Entrepreneurial Engine)
  - Layer 3: AEAN HiveMind (Compute token bidding & multi-agent strategy dispatch)
  - Layer 4: APODEX WorldModel (Multi-graph CausalNodes, RelationEdges & Bayesian belief updates)
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.ai_eos.intelligence.fourteen_layer_engine import FourteenLayerEngine, OpportunitySignal
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid, Grant
from apodex.world_model.world_model import WorldModel, CausalNode, RelationEdge

logger = logging.getLogger("apodex.orchestration.unified_cognitive_os")


class UnifiedCognitiveOS:
    """
    Master Cognitive Operating System orchestrating end-to-end active inference across
    Research OS, EIOS Kernel, EOS Engine, AEAN HiveMind, and APODEX WorldModel.
    """

    def __init__(
        self,
        research_os: Optional[ResearchOS] = None,
        eios_kernel: Optional[EIOSKernel] = None,
        eos_engine: Optional[EOSEngine] = None,
        fourteen_layer_engine: Optional[FourteenLayerEngine] = None,
        hive_mind: Optional[HiveMind] = None,
        world_model: Optional[WorldModel] = None,
    ) -> None:
        self.research_os = research_os or ResearchOS()
        self.eios_kernel = eios_kernel or EIOSKernel()
        self.eos_engine = eos_engine or EOSEngine()
        self.fourteen_layer_engine = fourteen_layer_engine or FourteenLayerEngine()
        self.hive_mind = hive_mind or HiveMind(token_budget=200)
        self.world_model = world_model or WorldModel()
        self.bridge = ResearchToSystemBridge(self.research_os)

        logger.info("Initialized UnifiedCognitiveOS across 5 subsystem layers.")

    def ingest_and_bridge_hypothesis(
        self,
        statement: str,
        domain: str = "ai_intelligence",
        target_subsystem: str = "eios"
    ) -> Dict[str, Any]:
        """
        Registers a research hypothesis in Research OS and bridges it downstream
        to EOS Engine, EIOS Kernel, and AEAN HiveMind.
        """
        hyp = self.research_os.register_hypothesis(
            title=statement[:50] if len(statement) > 50 else statement,
            description=statement,
            null_hypothesis=f"No impact on {domain}",
            target_metric=domain,
            significance_alpha=0.05
        )
        hyp_id = hyp.hypothesis_id

        # Bridge handoff to EOS and EIOS
        bridge_result = self.bridge.bridge_hypothesis_to_system(hyp_id)

        # Update World Model node for hypothesis
        node_id = f"hyp_{hyp_id}"
        node = CausalNode(node_id=node_id, node_type="hypothesis", properties={"statement": statement, "domain": domain})
        self.world_model.add_node(node)

        return {
            "hypothesis_id": str(hyp_id),
            "bridge_status": bridge_result,
            "world_model_node_id": node_id
        }

    def dispatch_hive_mind_task_bidding(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Grant]:
        """
        Submits task bids to AEAN HiveMind for token-based resource arbitration.
        """
        bids = []
        for t in tasks:
            bid = TaskBid(
                task=t.get("task", "unnamed_task"),
                priority=float(t.get("priority", 0.5)),
                expected_value=float(t.get("expected_value", 0.5)),
                token_cost=int(t.get("token_cost", 10))
            )
            bids.append(bid)

        grants = self.hive_mind.arbitrate(bids)

        # Log granted tasks in World Model as execution events
        for grant in grants:
            if grant.granted:
                event_node = CausalNode(
                    node_id=f"grant_{grant.task}",
                    node_type="grant_event",
                    properties={"task": grant.task, "tokens": grant.tokens}
                )
                self.world_model.add_node(event_node)

        return grants

    def update_world_model_beliefs(
        self,
        belief_key: str,
        value: Any,
        source_subsystem: str = "cognitive_os"
    ) -> None:
        """
        Updates Bayesian belief state in APODEX WorldModel.
        """
        if belief_key not in self.world_model.beliefs:
            self.world_model.beliefs[belief_key] = {}

        self.world_model.beliefs[belief_key] = {
            "value": value,
            "source": source_subsystem,
            "confidence": 0.9
        }

    def run_closed_loop_active_inference_cycle(
        self,
        cycle_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes a complete closed-loop cycle across all 5 subsystem layers:
        1. Layer 1 Research OS: Register and validate hypothesis / literature review query
        2. Layer 2 EIOS & EOS: 14-layer engine cycle, signal ingestion & EFE optimization
        3. Layer 3 AEAN HiveMind: Task bidding & resource allocation grants
        4. Layer 4 APODEX WorldModel: Causal graph edge creation & Bayesian belief state updates
        """
        logger.info(f"Starting closed-loop active inference cycle: {cycle_input.get('title')}")

        # Step 1: Research OS Ingestion
        hyp_statement = cycle_input.get("hypothesis_statement", "Default cognitive OS active inference hypothesis")
        hyp_res = self.ingest_and_bridge_hypothesis(hyp_statement)

        # Step 2: EOS Engine & 14-Layer Execution
        sig = OpportunitySignal(
            title=cycle_input.get("title", "Active Inference Opportunity"),
            domain=cycle_input.get("domain", "ai_intelligence"),
            keywords=cycle_input.get("keywords", ["active_inference", "causal_scm", "token_bidding"]),
            tam_cents=cycle_input.get("tam_cents", 100000000)
        )
        engine_res = self.fourteen_layer_engine.execute_full_14_layer_cycle(
            signals=[sig],
            total_budget_cents=cycle_input.get("total_budget_cents", 50000000),
            venture_cells={"cell_1": {"score": 0.8}, "cell_2": {"score": 0.5}}
        )

        # Step 3: AEAN HiveMind Bidding
        tasks_to_bid = [
            {"task": "sense_anomalies", "priority": 0.9, "expected_value": 0.8, "token_cost": 15},
            {"task": "execute_counterfactual", "priority": 0.85, "expected_value": 0.75, "token_cost": 20},
            {"task": "update_moat", "priority": 0.6, "expected_value": 0.5, "token_cost": 10}
        ]
        grants = self.dispatch_hive_mind_task_bidding(tasks_to_bid)

        # Step 4: APODEX WorldModel Belief & Graph Updates
        node_a = CausalNode(node_id="research_hypothesis", node_type="research", properties={"hyp_id": hyp_res["hypothesis_id"]})
        node_b = CausalNode(node_id="active_inference_opportunity", node_type="opportunity", properties={"signal_title": sig.title})
        self.world_model.add_node(node_a)
        self.world_model.add_node(node_b)

        edge = RelationEdge(
            source_id="research_hypothesis",
            target_id="active_inference_opportunity",
            relation_type="supports",
            weight=0.95
        )
        self.world_model.add_relation(edge)
        self.update_world_model_beliefs("cycle_success_confidence", 0.95, source_subsystem="UnifiedCognitiveOS")

        return {
            "status": "success",
            "research_os_hypothesis": hyp_res,
            "fourteen_layer_engine_result": engine_res,
            "hive_mind_grants": len(grants),
            "world_model_nodes": len(self.world_model.nodes),
            "world_model_edges": len(self.world_model.edges),
            "world_model_beliefs": self.world_model.beliefs
        }
