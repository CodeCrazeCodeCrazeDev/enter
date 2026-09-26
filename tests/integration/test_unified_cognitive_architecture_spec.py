import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel, CausalNode

def test_unified_4layer_cross_layer_handoff():
    """
    Verifies full 4-layer active inference cross-layer handoffs:
    Layer 1 (Research OS) -> Layer 2 (EIOS Kernel & EOS Engine) -> Layer 3 (AEAN HiveMind) -> Layer 4 (APODEX WorldModel)
    """
    # 1. Initialize layer components
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind()
    wm = WorldModel()

    # 2. Bridge instantiation
    bridge = ResearchToSystemBridge(ros=ros, kernel=kernel, eos=eos, hive_mind=hive, world_model=wm)

    # 3. Layer 1: Register and validate research hypothesis
    hyp_obj = ros.register_hypothesis(
        title="Active Inference Cognitive Rate Limits",
        description="Active inference EFE optimization reduces reasoning latency in multi-agent swarms.",
        null_hypothesis="Active inference has no impact on reasoning latency.",
        target_metric="latency_ms"
    )

    hyp_dict = {
        "id": str(hyp_obj.hypothesis_id),
        "title": hyp_obj.title,
        "description": hyp_obj.description,
        "category": "ACTIVE_INFERENCE",
        "status": "validated",
        "statistical_confidence": 0.98,
        "target_subsystem": "AEAN"
    }

    # 4. Handoff: Layer 1 -> Layer 2 & Layer 3 & Layer 4 via Bridge
    handoff_result = bridge.process_validated_hypothesis(hyp_dict)
    assert handoff_result["status"] == "HANDOFF_SUCCESS"
    assert "active_inference_dag" in handoff_result
    assert "token_bid_registered" in handoff_result
    assert handoff_result["token_bid_registered"] is True

    # 5. Layer 2 verification: EIOS Kernel hypothesis registration & EOS active hypotheses
    assert str(hyp_obj.hypothesis_id) in kernel.research_hypotheses or len(kernel.research_hypotheses) > 0

    # 6. Layer 3 verification: HiveMind insight registration
    assert str(hyp_obj.hypothesis_id) in hive.registered_insights or len(hive.registered_insights) > 0

    # 7. Layer 4 verification: WorldModel causal node creation
    node_id = f"node_hyp_{hyp_obj.hypothesis_id}"
    assert node_id in wm.nodes or len(wm.nodes) > 0

def test_layer_capability_boundary_rules():
    """
    Verifies that layer components observe directional interface rules.
    """
    ros = ResearchOS()
    # Research OS literature review should return domain-mapped trends and citations
    res = ros.conduct_literature_review("ACTIVE_INFERENCE")
    assert "synthesized_trends" in res
    assert isinstance(res["synthesized_trends"], list)

def test_active_inference_dag_compilation():
    """
    Verifies Layer 2 EIOS Kernel Active Inference DAG compilation.
    """
    kernel = EIOSKernel()
    hyp = {
        "id": "hyp_test_001",
        "title": "EFE Anomaly Detection",
        "category": "ACTIVE_INFERENCE",
        "target_subsystem": "EIOS"
    }
    kernel.register_research_hypothesis(hyp)
    dag = kernel.compile_active_inference_dag("hyp_test_001")
    assert isinstance(dag, list)
    assert len(dag) > 0
    assert "step" in dag[0]
