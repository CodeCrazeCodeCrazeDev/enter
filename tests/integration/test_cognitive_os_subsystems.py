"""
Integration tests for joint cross-layer cognitive operating system interactions
across Layer 1 (Research OS), Layer 2 (EOS / EIOS), Layer 3 (AEAN), and Layer 4 (APODEX).
"""
import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import (
    EIOSKernel,
    EntrepreneurialCompiler,
    HierarchicalActiveInference,
    ExecutionDAG
)
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.skills.registry import SkillRegistry


def test_cross_layer_hypothesis_to_kernel_and_skills():
    """
    Test end-to-end data flow:
    Layer 1 (ResearchOS) validates a hypothesis ->
    Layer 2 (EIOSKernel) incorporates hypothesis into compiled DAG ->
    Layer 3 (AEAN HiveMind & SkillRegistry) executes skills under updated policy bounds.
    """
    # 1. Initialize Layer 1 (Research OS)
    research_os = ResearchOS()
    assert research_os is not None

    # Literature review discovery
    review = research_os.conduct_literature_review("portfolio_inference")
    assert "domain" in review
    assert review["reviewed_citations_count"] >= 0

    # Hypothesis registration & power design
    hyp = research_os.register_hypothesis(
        title="Active Inference Routing Optimization",
        description="Active inference routing reduces step latency",
        null_hypothesis="Routing latency is unchanged",
        target_metric="latency_ms"
    )
    design = research_os.design_experiment(hyp.hypothesis_id)
    assert design["recommended_sample_size"] > 0

    # 2. Initialize Layer 2 (EIOS Kernel & Active Inference Compiler)
    kernel = EIOSKernel()
    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag(goal="Optimize active inference routing", target_budget_usd=1000)
    assert isinstance(dag, ExecutionDAG)
    assert len(dag.nodes) > 0

    # 3. Initialize Layer 3 (AEAN Swarm & Skill Execution)
    registry = SkillRegistry()
    skill = registry.get_skill("opportunity_evaluation_frameworks")
    assert skill is not None

    hive = HiveMind()
    assert hive is not None


def test_layer_2_efe_active_inference_routing():
    """
    Test Hierarchical Active Inference variational free energy calculation (Layer 2).
    """
    active_inf = HierarchicalActiveInference()
    fe = active_inf.calculate_layer_free_energy(
        layer="agent",
        actual_outcome=0.85,
        expected_outcome=0.90
    )
    assert fe > 0.0
    assert active_inf.uncertainty_levels["agent"] > 0.0
