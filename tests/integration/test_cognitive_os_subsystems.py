"""Cross-Layer Cognitive Operating System Integration Test Suite.

Verifies end-to-end multi-layer handoffs and joint behaviors across:
- Layer 1: Research OS (scientific hypothesis generation & statistical validation)
- Layer 2: EIOS Kernel (DAG process execution) & EOS Engine (opportunity & capital management)
- Layer 3: AEAN HiveMind (task bidding & token budget arbitration)
- Layer 4: APODEX WorldModel (causal graph nodes, domain entities, and Bayesian belief tracking)
"""

from __future__ import annotations

import pytest
import asyncio
from datetime import datetime
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.ai_eos.intelligence.computational_architecture import Opportunity
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel, CausalNode, RelationEdge
from apodex.world_model.domain.entities import Entity
from apodex.world_model.domain.beliefs import Belief
from apodex.ai_eos.research.integration import (
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    TrajectoryStep,
)


@pytest.mark.asyncio
async def test_research_os_to_eios_kernel_and_eos_handoff():
    """Validates hypothesis registration & simulation in Research OS and handoff to EIOS Kernel & EOS Engine."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()

    # 1. Register scientific hypothesis in Research OS
    hyp = ros.register_hypothesis(
        title="High-Yield Active Inference Opportunity",
        description="Active inference routing reduces latent friction in market execution",
        null_hypothesis="Routing method has no effect on execution latency",
        target_metric="latency_reduction_ms",
        significance_alpha=0.05
    )
    assert hyp.status == "registered"

    # 2. Execute statistical validation simulation
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.2)
    assert hyp.status == "validated"

    # 3. Compile hypothesis execution into EIOS Kernel Execution DAG and execute
    dag = ExecutionDAG(id=str(hyp.hypothesis_id))
    dag.add_node(ExecutionNode(node_id="n_sense", name=hyp.title, action_type="sensing"))

    execution_success = await kernel.execute_dag(dag)
    assert execution_success is True
    assert str(hyp.hypothesis_id) in kernel.active_processes

    # 4. Verify EOS Engine continuous sensing cycle execution
    cycle_result = eos.run_continuous_sensing_cycle(cells=[], total_budget_cents=10000)
    assert "world_state" in cycle_result
    assert "market_uncertainty" in cycle_result


def test_aean_hivemind_task_bidding_and_arbitration():
    """Validates AEAN HiveMind token bidding, arbitration, and granted tasks."""
    hive = HiveMind(token_budget=100)

    # Submit task bids from autonomous agents
    bid_a = TaskBid(task="market_analysis", priority=0.8, expected_value=1.5, token_cost=30)
    bid_b = TaskBid(task="risk_audit", priority=0.9, expected_value=2.0, token_cost=40)

    grants = hive.arbitrate([bid_a, bid_b])
    assert len(grants) == 2
    granted_map = hive.granted_tasks(grants)
    assert granted_map["risk_audit"] is True
    assert granted_map["market_analysis"] is True


def test_world_model_causal_graph_and_bayesian_beliefs():
    """Validates APODEX WorldModel causal graph nodes, relations, pathfinding, and Bayesian beliefs."""
    wm = WorldModel()

    # Create causal nodes
    node_a = CausalNode(node_id="n_research", node_type="hypothesis", value=1.0)
    node_b = CausalNode(node_id="n_revenue", node_type="metric", value=0.8)

    wm.add_node(node_a)
    wm.add_node(node_b)
    assert "n_research" in wm.nodes
    assert "n_revenue" in wm.nodes

    # Add relation edge
    edge = RelationEdge(
        source_id="n_research",
        target_id="n_revenue",
        relation_type="causal_drives",
        weight=0.85
    )
    wm.add_relation(edge)

    # Query relations and pathfinding
    relations_from = wm.get_relations_from("n_research")
    assert len(relations_from) == 1
    assert relations_from[0].target_id == "n_revenue"

    path = wm.find_path("n_research", "n_revenue")
    assert path == ["n_research", "n_revenue"]

    # Add recursive Bayesian belief
    target_ent_id = uuid4()
    belief = Belief(
        belief_id=uuid4(),
        target_id=target_ent_id,
        probability=0.82,
        evidence=["trace_hash_001", "exp_yield_3.2"]
    )
    wm.beliefs[str(belief.belief_id)] = belief.model_dump()
    assert str(belief.belief_id) in wm.beliefs
    assert wm.beliefs[str(belief.belief_id)]["probability"] == 0.82


def test_transferable_engineering_principles_runtime_integration():
    """Validates execution of 200-paper transferable principles engines (AST rewrite, Genetic, SFT, Routing)."""

    # 1. Code Rewrite Engine
    import tempfile, os
    with tempfile.TemporaryDirectory() as tmpdir:
        sample_file = os.path.join(tmpdir, "sample.py")
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("def calculate_sum(a, b):\n    return a + b\n")

        rewrite_engine = CodeRewriteEngine(allowed_paths=[tmpdir])
        proposal = rewrite_engine.propose_rewrite(
            filepath=sample_file,
            original_snippet="return a + b",
            proposed_snippet="return float(a + b)",
            rationale="Enforce floating point return type safety"
        )
        success = rewrite_engine.commit_rewrite(proposal)
        assert success is True

        with open(sample_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert "return float(a + b)" in content

    # 2. Genetic Workflow Optimizer
    genetic_opt = GeneticWorkflowOptimizer(population_size=5, mutation_rate=0.1)
    genetic_opt.initialize_population(
        base_template="Analyze market trends: {params}",
        base_params={"temperature": 0.2, "top_p": 0.9}
    )
    assert len(genetic_opt.population) == 5

    def dummy_scoring(genome):
        return genome.parameters.get("temperature", 0.0) * 10.0

    genetic_opt.evaluate_generation(dummy_scoring)
    genetic_opt.perform_crossover_and_mutation()
    assert len(genetic_opt.population) == 5

    # 3. SFT Preference Collector
    sft_collector = SFTPreferenceCollector(discount_factor=0.95)
    steps_a = [TrajectoryStep(action="Search", predicted_expectation=0.5, actual_outcome=0.8, reward=0.8)]
    steps_b = [TrajectoryStep(action="Direct Answer", predicted_expectation=0.5, actual_outcome=0.3, reward=0.2)]

    pref_pair = sft_collector.compile_dpo_preference_pair("Query", steps_a, steps_b)
    assert "Search" in pref_pair["chosen"]
    assert "Direct Answer" in pref_pair["rejected"]

    # 4. Learnable Routing Gate Dispatcher
    router = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    router.register_subagent(SpecializedAgentProfile(agent_id="expert_sec", domain_specialty="security", cost_per_token=0.001, historical_success_rate=0.9))
    router.register_subagent(SpecializedAgentProfile(agent_id="general_bot", domain_specialty="general", cost_per_token=0.0001, historical_success_rate=0.6))

    selected_agent = router.route_task(task_complexity=100.0, domain="security")
    assert selected_agent == "expert_sec"
