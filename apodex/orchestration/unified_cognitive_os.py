"""Unified Cognitive Operating System (UnifiedCognitiveOS).

Master orchestrator unifying Layer 1 (Research OS), Layer 2 (EIOS Kernel & EOS Engine),
Layer 3 (AEAN HiveMind), and Layer 4 (APODEX WorldModel) into a closed-loop Active Inference cycle.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge

logger = logging.getLogger("apodex.orchestration.unified_cognitive_os")


class UnifiedCognitiveOS:
    """Master orchestrator for the 5-subsystem Unified Cognitive Operating System."""

    def __init__(self) -> None:
        self.research_os = ResearchOS()
        self.eios_kernel = EIOSKernel()
        self.eos_engine = EOSEngine()
        self.hive_mind = HiveMind()
        self.world_model = WorldModel()
        self.compiler = EntrepreneurialCompiler()

        self.bridge = ResearchToSystemBridge(
            research_os=self.research_os,
            eios_kernel=self.eios_kernel,
            eos_engine=self.eos_engine,
            hive_mind=self.hive_mind,
            world_model=self.world_model
        )

    async def run_cognitive_cycle(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Runs a complete closed-loop Active Inference cycle across all 5 cognitive subsystems."""
        title = input_data.get("title", "Unified Cognitive Probe")
        description = input_data.get("description", "Cross-layer active inference probe")
        null_hypothesis = input_data.get("null_hypothesis", "No strategic advantage")
        target_metric = input_data.get("target_metric", "expected_utility")
        keywords = input_data.get("keywords", ["ai_os", "active_inference"])
        value_cents = input_data.get("value_cents", 10000_00)
        expected_value = input_data.get("expected_value", 0.85)

        logger.info(f"[UnifiedCognitiveOS] Initiating closed-loop cognitive cycle for: {title}")

        # Layer 1: Research OS Hypothesis Registration & Simulation
        hypothesis = self.research_os.register_hypothesis(
            title=title,
            description=description,
            null_hypothesis=null_hypothesis,
            target_metric=target_metric
        )
        experiment = self.research_os.create_experiment(hypothesis.hypothesis_id)
        exp_result = self.research_os.execute_experiment_simulation(experiment.experiment_id, ground_truth_yield=2.5)

        # Layer 1 -> Layer 2 Bridge: Hypothesis to EIOS Kernel Active Inference Sensing
        eios_handoff = self.bridge.bridge_hypothesis_to_eios(hypothesis)

        # Layer 2: EIOS Compiler & DAG Execution
        dag = self.compiler.compile_goal_to_dag(title, target_budget_usd=int(value_cents / 100))
        dag_success = await self.eios_kernel.execute_dag(dag)

        # Layer 2: Bridge Opportunity to EOS Engine
        opportunity_id = f"op_{uuid4().hex[:8]}"
        eos_handoff = self.bridge.bridge_opportunity_to_eos(
            opportunity_id=opportunity_id,
            name=title,
            value_cents=value_cents,
            keywords=keywords
        )

        # Layer 2 -> Layer 3 Bridge: Insight to AEAN HiveMind Bidding & Token Arbitration
        insight_id = f"ins_{uuid4().hex[:8]}"
        aean_handoff = self.bridge.bridge_insight_to_aean(
            insight_id=insight_id,
            domain=target_metric,
            expected_value=expected_value
        )

        # Layer 3 -> Layer 4 Bridge: Execution Outcome to APODEX WorldModel Graph & Beliefs
        node_id = f"node_{uuid4().hex[:8]}"
        target_id = f"target_{uuid4().hex[:8]}"
        belief_key = f"belief_{target_metric}"
        wm_handoff = self.bridge.bridge_execution_to_world_model(
            node_id=node_id,
            node_type="cognitive_cycle_execution",
            relation_type="validates_hypothesis",
            target_id=target_id,
            belief_key=belief_key,
            belief_val={"validated": exp_result.is_statistically_significant, "effect_size": exp_result.effect_size}
        )

        logger.info(f"[UnifiedCognitiveOS] Cycle completed successfully for '{title}'.")

        return {
            "status": "SUCCESS",
            "cycle_title": title,
            "hypothesis_id": str(hypothesis.hypothesis_id),
            "statistically_significant": exp_result.is_statistically_significant,
            "dag_executed_successfully": dag_success,
            "eios_handoff": eios_handoff,
            "eos_handoff": eos_handoff,
            "aean_handoff": aean_handoff,
            "world_model_handoff": wm_handoff
        }
