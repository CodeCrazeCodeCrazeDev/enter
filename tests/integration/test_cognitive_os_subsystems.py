"""Cross-layer integration tests for the Unified 4-Layer Cognitive OS architecture.

Validates joint interactions across:
- Layer 1: Research OS (hypothesis validation & literature synthesis)
- Layer 2: EIOS Kernel & EOS Engine (active inference sensing & entrepreneurial decisions)
- Layer 3: AEAN HiveMind (multi-agent token bidding & coordination)
- Layer 4: APODEX World Model (causal entity graphs & Bayesian belief propagation)
"""

from __future__ import annotations

import pytest
import asyncio
from uuid import uuid4
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.graph.world_graph import WorldGraphManager
from apodex.world_model.domain.beliefs import Belief
from apodex.ai_eos.research.integration import ResearchToSystemBridge


@pytest.mark.asyncio
async def test_cross_layer_active_inference_handoff():
    # Initialize Layer 1 (Research OS)
    research_os = ResearchOS()
    hypothesis = research_os.register_hypothesis(
        title="Hawkes Multi-Agent Token Bidding Convergence",
        description="Self-exciting Hawkes dynamics stabilize multi-agent resource allocations under peak loads.",
        null_hypothesis="Hawkes dynamics provide zero stability gain compared to uniform round-robin allocation.",
        target_metric="allocation_convergence_latency_ms",
        significance_alpha=0.01
    )
    assert hypothesis.hypothesis_id is not None

    # Initialize Layer 2 (EIOS Kernel & EOS Engine)
    kernel = EIOSKernel()
    eos_engine = EOSEngine()

    # Initialize Layer 3 (AEAN HiveMind)
    hive_mind = HiveMind()

    # Initialize Layer 4 (APODEX World Graph & Beliefs)
    graph_mgr = WorldGraphManager()

    # Bridge orchestration
    bridge = ResearchToSystemBridge(
        research_os=research_os,
        kernel=kernel,
        eos_engine=eos_engine,
        hive_mind=hive_mind,
        graph_manager=graph_mgr
    )

    handoff_result = await bridge.promote_and_disseminate_hypothesis(str(hypothesis.hypothesis_id))

    assert handoff_result["status"] == "success"
    assert handoff_result["hypothesis_id"] == str(hypothesis.hypothesis_id)
    assert handoff_result["registered_in_kernel"] is True
    assert handoff_result["ingested_in_eos"] is True
    assert handoff_result["registered_in_hive_mind"] is True
    assert handoff_result["registered_in_world_model"] is True


@pytest.mark.asyncio
async def test_end_to_end_causal_belief_propagation():
    target_id = uuid4()
    belief = Belief(
        target_id=target_id,
        probability=0.7,
        evidence=["paper_ref_101", "empirical_benchmark_02"]
    )

    prior = belief.probability
    belief.update_confidence(likelihood=0.9, prior_probability=prior)

    assert belief.probability > prior
    assert len(belief.evidence) == 2
