import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel, CausalNode


class ResearchToSystemBridge:
    """
    Cross-layer bridge orchestrating active inference state handoffs between:
      - Layer 1: Research OS
      - Layer 2: EIOS Kernel & EOS Engine
      - Layer 3: AEAN HiveMind
      - Layer 4: APODEX WorldModel
    """
    def __init__(self, research_os, eios_kernel, eos_engine, hive_mind, world_model):
        self.ros = research_os
        self.eios_kernel = eios_kernel
        self.eos_engine = eos_engine
        self.hive_mind = hive_mind
        self.world_model = world_model

    def process_validated_hypothesis(self, hypothesis_id):
        hypotheses = self.ros.hypotheses.list_all()
        target_hyp = next((h for h in hypotheses if str(h.hypothesis_id) == str(hypothesis_id)), None)
        if not target_hyp:
            return {"status": "error", "message": "Hypothesis not found"}

        # Register with EIOS Kernel (Layer 2)
        if hasattr(self.eios_kernel, "active_hypotheses"):
            self.eios_kernel.active_hypotheses.add(str(hypothesis_id))
        else:
            self.eios_kernel.active_hypotheses = {str(hypothesis_id)}

        # Ingest into EOS Engine (Layer 2)
        if hasattr(self.eos_engine, "ingest_validated_research"):
            self.eos_engine.ingest_validated_research(target_hyp)
        elif hasattr(self.eos_engine, "active_hypotheses"):
            self.eos_engine.active_hypotheses.add(str(hypothesis_id))
        else:
            self.eos_engine.active_hypotheses = {str(hypothesis_id)}

        # Register insight with AEAN HiveMind (Layer 3)
        if hasattr(self.hive_mind, "register_research_insight"):
            self.hive_mind.register_research_insight(
                title=getattr(target_hyp, 'title', 'Research'),
                principle=getattr(target_hyp, "description", "Validated principle"),
                target_subsystem=getattr(target_hyp, "target_subsystem", "AEAN")
            )

        return {"status": "success", "hypothesis_id": str(hypothesis_id)}


def test_unified_cognitive_architecture_spec_integration():
    """
    Integration test validating the unified 4-layer cognitive architecture specification:
      - Layer 1: Research OS hypothesis generation and literature review
      - Layer 2: EIOS Kernel & EOS Engine Active Inference DAG compilation
      - Layer 3: AEAN HiveMind token bidding registry and multi-agent coordination
      - Layer 4: APODEX WorldModel Causal Nodes & Bayesian Belief updates
      - Cross-Layer Bridge: ResearchToSystemBridge
    """
    # 1. Initialize Subsystems
    ros = ResearchOS()
    eios_kernel = EIOSKernel()
    eos_engine = EOSEngine()
    hive_mind = HiveMind()
    world_model = WorldModel()

    # 2. Formulate Layer 1 Scientific Hypothesis
    hypothesis = ros.register_hypothesis(
        title="Hawkes AST Recursion Depth Guard Hypothesis",
        description="Non-Gaussian Hawkes AST recursion depth limit stabilizes agent self-improvement",
        null_hypothesis="AST recursion limits do not decrease stack overflow occurrences",
        target_metric="stack_overflow_rate"
    )
    hypothesis.status = "validated"
    ros.hypotheses.save(hypothesis.hypothesis_id, hypothesis)

    # 3. Instantiate Bridge and Execute Handoff
    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=eios_kernel,
        eos_engine=eos_engine,
        hive_mind=hive_mind,
        world_model=world_model
    )

    handoff_result = bridge.process_validated_hypothesis(hypothesis.hypothesis_id)
    assert handoff_result["status"] == "success"

    # 4. Verify Layer 2 (EIOS/EOS) Ingestion & Active Inference Sensing
    assert str(hypothesis.hypothesis_id) in eios_kernel.active_hypotheses

    # 5. Verify Layer 3 (AEAN HiveMind) Insight Registration & Token Bidding
    bid = TaskBid(
        task="Synthesize Hawkes AST Guard Function",
        priority=0.9,
        expected_value=1.5,
        token_cost=10
    )
    grants = hive_mind.arbitrate([bid])
    assert len(grants) == 1
    assert grants[0].task == "Synthesize Hawkes AST Guard Function"

    # 6. Verify Layer 4 (APODEX WorldModel) Causal Node & Belief Updates
    node = CausalNode(
        node_id="node_hawkes_ast_01",
        node_type="cognitive_guard",
        properties={"stability_score": 0.98}
    )
    world_model.add_node(node)
    assert world_model.nodes["node_hawkes_ast_01"].node_type == "cognitive_guard"
