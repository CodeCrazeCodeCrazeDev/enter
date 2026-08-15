"""
End-to-End Subsystem Integration Test Suite.

Verifies joint interactions across all decoupled system layers:
1. ResearchOS: Conducts hypothesis registration, experiment pipeline execution, and statistical validation.
2. EIOS Kernel & Active Inference: Computes Expected Free Energy (EFE), minimizes epistemic uncertainty, and compiles DAGs.
3. EOS / Arcs Workflows: Multi-timescale loops, opportunity anomaly sensing, and lifecycle state transitions.
4. AEAN (Autonomous Entrepreneurial Agent Network): HiveMind resource arbitration and multi-agent coordination.
5. APODEX: Unified Memory, WorldGraph, Execution Surface Adapters, and Skill Registry execution.
"""

from __future__ import annotations
import pytest
import asyncio
from datetime import datetime, UTC

from apodex.research_os import (
    Hypothesis,
    Dataset,
    Feature,
    HypothesisRegistry,
    DatasetRegistry,
    FeatureRegistry,
    ExperimentRegistry,
    ModelRegistry,
    StatisticalValidator,
    GovernanceGateway,
    ResearchPipelineOrchestrator,
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel import EIOSKernel, EntrepreneurialCompiler, HierarchicalActiveInference, RecursivePlanner, TimeHorizon
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.arcs.workflows import AutonomousEntrepreneurialActorOS, CapabilityTier
from apodex.arcs.world_graph import WorldGraph
from apodex.arcs.memory.unified_memory import UnifiedMemoryAPI, MemoryType, MemoryEntry
from apodex.skills.registry import SkillRegistry


@pytest.mark.asyncio
async def test_end_to_end_cognitive_os_workflow():
    # -------------------------------------------------------------------------
    # 1. ResearchOS Domain: Scientific Discovery & Hypothesis Pipeline
    # -------------------------------------------------------------------------
    hyp_reg = HypothesisRegistry()
    ds_reg = DatasetRegistry()
    feat_reg = FeatureRegistry()
    exp_reg = ExperimentRegistry()
    mod_reg = ModelRegistry()

    h = Hypothesis(
        hypothesis_id="H_ENTERPRISE_01",
        research_question_id="Q_CAC_REDUCTION",
        title="Enterprise Tier CAC Optimization",
        description="Exploits algorithmic bidding and active inference targeted positioning",
        economic_rationale="MICROSTRUCTURE",
        null_hypothesis="CAC does not decrease with active inference targeting",
        target_variable="enterprise_cac_cents",
    )
    hyp_reg.register_hypothesis(h)

    ds = Dataset(
        dataset_id="DS_GTM_01",
        version="v1.0",
        raw_source="s3://apodex-data/gtm",
        ingestion_pipeline_hash="hash_gtm_123",
    )
    ds_reg.register_dataset(ds)

    f1 = Feature(
        feature_id="F_CONVERT_01",
        name="Conversion_Propensity",
        formula="logistic(gtm_clicks)",
        lineage_dataset_id="DS_GTM_01",
    )
    feat_reg.register_feature(f1)

    def trial_runner(dataset, feature_ids, hyperparameters):
        daily_returns = [0.002, 0.003, 0.001, 0.004, 0.002, 0.003] * 35
        metrics = {"sharpe": 2.2, "max_drawdown": 0.04}
        return daily_returns, metrics

    validator = StatisticalValidator(correction_method="HOLM")
    gateway = GovernanceGateway()

    orchestrator = ResearchPipelineOrchestrator(
        hypotheses=hyp_reg,
        datasets=ds_reg,
        features=feat_reg,
        experiments=exp_reg,
        models=mod_reg,
        validator=validator,
        gateway=gateway,
    )

    exp, report, decision, model = orchestrator.execute_pipeline(
        hypothesis_id="H_ENTERPRISE_01",
        dataset_id="DS_GTM_01",
        feature_ids=["F_CONVERT_01"],
        hyperparameters={"learning_rate": 0.01},
        trial_runner_fn=trial_runner,
        reviewers=["human_reviewer"],
        approvals={"human_reviewer": True},
    )

    assert exp.status == "COMPLETED"
    assert report.is_statistically_significant is True
    assert decision.status == "APPROVED"
    assert model is not None

    # Literature review search via ResearchOS
    research_engine = ResearchOS()
    literature = research_engine.conduct_literature_review(["active_inference", "causal_inference"])
    assert literature is not None

    # -------------------------------------------------------------------------
    # 2. EIOS Kernel & Active Inference Layer: Strategic Compilation & Planning
    # -------------------------------------------------------------------------
    compiler = EntrepreneurialCompiler()
    goal_dag = compiler.compile_goal_to_dag(
        goal="Scale Enterprise Tier CAC Reduction based on Research Hypothesis",
        target_budget_usd=25000
    )
    assert len(goal_dag.nodes) > 0

    kernel = EIOSKernel()
    dag_executed = await kernel.execute_dag(goal_dag)
    assert dag_executed is True

    hierarchy = HierarchicalActiveInference()
    fe_value = hierarchy.calculate_layer_free_energy("company", actual_outcome=0.88, expected_outcome=0.60)
    assert fe_value > 0

    planner = RecursivePlanner()
    planner.cascade_vision_down("Build an autonomous software organization")
    assert len(planner.plan_registry[TimeHorizon.VISION_10Y]) == 1

    # -------------------------------------------------------------------------
    # 3. AEAN Subsystem: HiveMind Resource Arbitration & Token Economics
    # -------------------------------------------------------------------------
    hive = HiveMind(token_budget=100)
    bids = [
        TaskBid(task="sense_demand", priority=0.9, expected_value=0.8, token_cost=30),
        TaskBid(task="run_funnels", priority=0.8, expected_value=0.7, token_cost=40),
        TaskBid(task="rebalance_capital", priority=0.95, expected_value=0.9, token_cost=50),
    ]
    grants = hive.arbitrate(bids)
    granted_map = hive.granted_tasks(grants)
    assert len(grants) == 3
    assert any(granted_map.values())

    # -------------------------------------------------------------------------
    # 4. APODEX Engine, Memory, World Graph & Skill Execution
    # -------------------------------------------------------------------------
    wg = WorldGraph()
    memory = UnifiedMemoryAPI(world_graph=wg)

    mem_entry = MemoryEntry(
        type=MemoryType.STRATEGIC,
        tenant_id="enterprise_core",
        context={"subsystem": "EOS_AEAN_RESEARCH"},
        payload={
            "hypothesis": h.hypothesis_id,
            "allocated_budget": 25000,
            "validated_model_id": model.model_id
        }
    )
    memory.store_memory(mem_entry)

    retrieved_mem = memory.retrieve_memory(MemoryType.STRATEGIC, tenant_id="enterprise_core")
    assert len(retrieved_mem) == 1
    assert retrieved_mem[0].payload["allocated_budget"] == 25000

    skill_reg = SkillRegistry()
    available_skills = skill_reg.list_skills()
    assert len(available_skills) > 0

    # Complete Actor OS Loop
    actor_os = AutonomousEntrepreneurialActorOS(initial_cash_cents=250_000_00)
    assert actor_os.governance is not None
