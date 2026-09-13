"""
End-to-End Multi-Layer Integration Test Suite for the Unified Cognitive Operating System.

Validates joint interactions across all 4 layers:
- Layer 1: Research OS (scientific hypothesis validation, statistical walk-forward simulation)
- Layer 2: EIOS Kernel & EOS Engine (Active Inference EFE sensing, 14-layer DAG compilation)
- Layer 3: AEAN HiveMind (compute token arbitration, multi-agent swarm execution)
- Layer 4: APODEX World Model (entity state, recursive Bayesian beliefs, Pearl do-calculus, GRC governance)
"""

import pytest
import uuid
import math
from datetime import datetime

# Layer 1
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import ResearchToSystemBridge

# Layer 2
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler, ExecutionDAG
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, StrategicPlanner
from apodex.ai_eos.domain.models import VentureCell

# Layer 3
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid

# Layer 4
from apodex.world_model.domain.beliefs import Belief
from apodex.cognition.brain import CognitiveBrain, DeepCausalWorldModel, SimulationEngine, AdvancedMemoryEngine


@pytest.mark.asyncio
async def test_layer1_research_to_layer2_kernel_bridge():
    """Validates Layer 1 hypothesis validation and bridge handoff to Layer 2 EIOS Kernel & EOS Engine."""
    research_os = ResearchOS()

    # 1. Register scientific hypothesis in Layer 1
    hyp = research_os.register_hypothesis(
        title="Active Inference Context Routing Reduction",
        description="Active Inference EFE context routing reduces LLM token consumption by 35%",
        null_hypothesis="Active Inference context routing has no effect on LLM token consumption",
        target_metric="token_consumption_reduction",
        significance_alpha=0.05
    )
    assert hyp.status == "registered"

    # 2. Run sandbox walk-forward simulation
    exp = research_os.create_experiment(hyp.hypothesis_id, seed=123)
    completed_exp = research_os.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.8)

    assert completed_exp.status in ["completed", "COMPLETED"] or getattr(completed_exp.status, "value", completed_exp.status) in ["completed", "COMPLETED"]
    assert hyp.status in ["validated", "refuted"]

    # 3. Test ResearchToSystemBridge handoff to Layer 2
    kernel = EIOSKernel()
    eos_engine = EOSEngine()

    promoted_node = ResearchToSystemBridge.export_validated_hypothesis_to_kernel(hyp, completed_exp, kernel)
    assert promoted_node is not None
    assert promoted_node.action_type == "research_hypothesis"

    # Verify hypothesis ingestion in EOS Engine
    eos_engine.hypothesis_engine.add_hypothesis(hyp)
    assert hyp.hypothesis_id in eos_engine.hypothesis_engine.hypotheses


@pytest.mark.asyncio
async def test_layer2_eios_dag_compilation_and_active_inference():
    """Validates Layer 2 DAG compilation, Active Inference EFE policy scoring, and sensing cycles."""
    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag("Deploy Autonomous Agent Platform", target_budget_usd=100000)

    assert isinstance(dag, ExecutionDAG)
    assert len(dag.nodes) == 4

    # Execute DAG with EIOS Kernel
    kernel = EIOSKernel()
    success = await kernel.execute_dag(dag)
    assert success is True

    # Active Inference EFE Policy Scoring
    planner = StrategicPlanner()
    candidates = [
        {"policy_id": "policy_a", "expected_utility": 0.85, "predictive_entropy": 0.20, "risk_factor": 0.10},
        {"policy_id": "policy_b", "expected_utility": 0.50, "predictive_entropy": 0.60, "risk_factor": 0.40},
    ]
    optimal_policy = planner.select_optimal_policy(candidates)
    assert optimal_policy["policy_id"] == "policy_a"
    assert "computed_efe" in optimal_policy


@pytest.mark.asyncio
async def test_layer3_aean_hivemind_token_bidding():
    """Validates Layer 3 AEAN HiveMind second-price compute token bidding arbitration."""
    hive_mind = HiveMind(token_budget=100)

    bids = [
        TaskBid(task="research_synthesis", priority=0.9, expected_value=0.8, token_cost=40),
        TaskBid(task="gtm_campaign", priority=0.7, expected_value=0.6, token_cost=50),
        TaskBid(task="brand_trademark_check", priority=0.5, expected_value=0.4, token_cost=30),
    ]

    grants = hive_mind.arbitrate(bids)
    granted_dict = hive_mind.granted_tasks(grants)

    assert granted_dict["research_synthesis"] is True
    assert granted_dict["gtm_campaign"] is True
    # Low priority bid exceeding remaining token budget is denied
    assert granted_dict["brand_trademark_check"] is False


@pytest.mark.asyncio
async def test_layer4_apodex_world_model_causal_and_beliefs():
    """Validates Layer 4 APODEX World Model entity belief updates, Pearl do-calculus, and GRC governance."""
    # 1. Recursive Bayesian Belief Update
    belief = Belief(target_id=uuid.uuid4(), probability=0.6)
    belief.update_confidence(likelihood=0.8, prior_probability=0.6)
    assert belief.probability > 0.6

    # 2. Deep Causal World Model & Judea Pearl do-calculus
    causal_model = DeepCausalWorldModel()
    causal_model.add_variable("active_inference_routing")
    causal_model.add_variable("token_efficiency")
    causal_model.add_causal_relation("active_inference_routing", "token_efficiency", coefficient=0.75)

    do_results = causal_model.query_do_calculus("active_inference_routing", intervention_val=2.0)
    assert do_results["token_efficiency"] == 1.5

    # Monte Carlo Rollout simulation
    sim_engine = SimulationEngine(world_model=causal_model)
    sim_report = sim_engine.simulate_rollout("active_inference_routing", 2.0, "token_efficiency", num_trials=30)
    assert "mean" in sim_report
    assert "value_at_risk_95" in sim_report

    # 3. Unified CognitiveBrain Strategic Cycle
    brain = CognitiveBrain()
    brain_cycle_res = brain.run_strategic_cycle("Scale Cognitive OS Substrate")

    assert brain_cycle_res["plan_length"] == 4
    assert brain_cycle_res["claim_verified"] is True
    assert "optimized_prompt" in brain_cycle_res
