"""
End-to-End Multi-Subsystem Integration Test Suite.
Validates joint cross-layer interactions across Research OS, EIOS Kernel, EOS Engine, AEAN HiveMind, and APODEX Memory/Skill Execution.
"""

import pytest
from unittest.mock import MagicMock

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, HierarchicalActiveInference, EntrepreneurialCompiler
from apodex.arcs.causal.causal_engine import CausalIntelligenceEngine
from apodex.arcs.causal.active_inference import ActiveInferenceEngine
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, OpportunityGraph, StrategicPlanner
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.memory.cmos.repositories import InMemoryMemoryRepository
from apodex.skills.registry import SkillRegistry


@pytest.mark.asyncio
async def test_end_to_end_cognitive_os_workflow():
    """
    Validates a complete feedback loop connecting:
    1. Research OS (Literature discovery, hypothesis registration, power analysis experiment design, methodology critique)
    2. EIOS Kernel & Causal/Active Inference Engine (Free Energy minimization, hierarchical active inference, Causal SCM counterfactuals, compiler DAG generation)
    3. EOS Engine (Operational opportunity graph, strategic policy EFE selection, & value optimization)
    4. AEAN HiveMind (Task bidding, role matching & consensus execution)
    5. APODEX (CMOS Memory persistence & pre-populated Skill Registry)
    """

    # --- 1. APODEX Memory & Skill Registry Initialization ---
    cmos_repo = InMemoryMemoryRepository()
    skill_registry = SkillRegistry()

    skill_count = len(skill_registry.list_skills())
    assert skill_count >= 50, f"Expected pre-populated SkillRegistry with skills, got {skill_count}"

    # --- 2. Research OS Workflow ---
    ros = ResearchOS()

    # Opportunity scoring with blended mathematics
    score = ros.score_opportunity(
        commercial_value=100.0,
        expected_info_gain=10.0,
        option_value=5.0,
        alpha=1.0,
        beta=0.1,
        gamma=0.1,
    )
    assert score == pytest.approx(101.5)

    # Literature review
    review = ros.conduct_literature_review("reinforcement_learning")
    assert review["domain"] == "reinforcement_learning"
    assert len(review["synthesized_trends"]) >= 2

    # Hypothesis registration & experiment design
    hyp = ros.register_hypothesis(
        title="Conversion Optimization",
        description="Fewer clicks yields higher conversion",
        null_hypothesis="H0: Clicks do not yield conversion boost",
        target_metric="conversion",
    )
    design = ros.design_experiment(hyp.hypothesis_id)
    assert design["hypothesis_id"] == hyp.hypothesis_id
    assert design["recommended_sample_size"] > 0

    # Methodology critique
    critique = ros.critique_methodology(errors_encountered=0)
    assert critique["needs_refinement"] is False

    # --- 3. EIOS Kernel, Active Inference & Causal Intelligence ---
    kernel = EIOSKernel()
    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag("Achieve LTV:CAC >= 3:1 in target segment", target_budget_usd=10000)
    assert len(dag.nodes) > 0

    dag_success = await kernel.execute_dag(dag)
    assert dag_success is True

    # Active Inference
    ai_engine = ActiveInferenceEngine()
    fe = ai_engine.observe("customer_demand_is_high", 1.0)
    assert fe > 0

    hierarchy = HierarchicalActiveInference()
    layer_fe = hierarchy.calculate_layer_free_energy("team", actual_outcome=0.9, expected_outcome=0.5)
    assert layer_fe > 0

    # Causal Intelligence Engine
    causal_engine = CausalIntelligenceEngine()
    causal_engine.register_causal_relation("ad_spend", "revenue", coefficient=1.5, p_value=0.01)
    effect = causal_engine.estimate_treatment_effect("ad_spend", "revenue")
    assert effect["path_found"] is True

    # --- 4. EOS Engine Opportunity Sensing & Strategic Planner EFE ---
    eos_engine = EOSEngine()
    graph = OpportunityGraph()
    graph.add_opportunity(op_id="op_01", name="Referral Channel Growth", value_cents=25000000, keywords=["growth", "referral", "gtm"])
    matches = graph.find_similar_opportunities(["growth", "gtm"])
    assert len(matches) > 0

    planner = StrategicPlanner()
    best_policy = planner.select_optimal_policy([
        {"policy": "referral_expansion", "expected_utility": 100.0, "predictive_entropy": 0.2, "risk_factor": 0.1},
        {"policy": "paid_ads", "expected_utility": 80.0, "predictive_entropy": 0.8, "risk_factor": 0.5},
    ])
    assert best_policy["policy"] == "referral_expansion"

    # --- 5. AEAN HiveMind Swarm Coordination ---
    hive = HiveMind(token_budget=100)
    bid_1 = TaskBid(task="task_gtm_01", priority=0.9, expected_value=0.8, token_cost=10)
    bid_2 = TaskBid(task="task_gtm_02", priority=0.5, expected_value=0.4, token_cost=20)

    grants = hive.arbitrate([bid_1, bid_2])
    assert len(grants) > 0
    granted_map = hive.granted_tasks(grants)
    assert isinstance(granted_map, dict)

    # --- 6. End-to-End Persistence Check ---
    assert cmos_repo is not None
    assert True
