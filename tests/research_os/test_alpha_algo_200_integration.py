# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Comprehensive integration test suite for
the 200-paper research corpus (IDs 301-500) and cross-layer cognitive OS subsystems.
"""

import os
import yaml
import pytest
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    TrajectoryStep,
    RewriteProposal
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, VentureCell
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid


def test_200_paper_database_structure_and_zero_overlap():
    """Validates 200-paper YAML database integrity and zero title/DOI overlap against baseline."""
    db_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(db_path), "ALPHA_ALGO_200_NEW_RESEARCH.yaml missing!"

    with open(db_path, "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    papers = db.get("papers", [])
    assert len(papers) == 200, f"Expected 200 papers, found {len(papers)}"

    ids = [p["id"] for p in papers]
    assert min(ids) == 301 and max(ids) == 500, f"Paper IDs must range 301-500, got {min(ids)}-{max(ids)}"

    # Check zero overlap against papers 1-300
    baseline_titles = set()
    baseline_dois = set()
    for base_path in ["docs/research/papers/AI_EOS_RESEARCH_DB.yaml", "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"]:
        if os.path.exists(base_path):
            with open(base_path, "r", encoding="utf-8") as f:
                base_db = yaml.safe_load(f)
            for p in base_db.get("papers", []):
                baseline_titles.add(p["metadata"]["title"].lower())
                if "doi" in p["metadata"]:
                    baseline_dois.add(p["metadata"]["doi"].lower())

    for p in papers:
        title = p["metadata"]["title"].lower()
        doi = p["metadata"]["doi"].lower()
        assert title not in baseline_titles, f"Title overlap detected: '{title}'"
        assert doi not in baseline_dois, f"DOI overlap detected: '{doi}'"


def test_200_paper_principle_registration_and_lit_review():
    """Verifies registration of 200 principles and Research OS literature review querying."""
    principles = register_200_paper_corpus_principles()
    assert len(principles) == 200, f"Expected 200 registered principles, got {len(principles)}"

    ros = ResearchOS()
    review = ros.conduct_literature_review("AEAN HiveMind")
    assert review["reviewed_citations_count"] > 0
    assert len(review["principles_applied"]) > 0
    assert "AEAN" in review["principles_applied"][0]["target_subsystem"] or "HiveMind" in review["principles_applied"][0]["target_subsystem"]


def test_integration_runtime_components():
    """Verifies enhancements to CodeRewriteEngine, GeneticWorkflowOptimizer, SFTPreferenceCollector, and LearnableRoutingGateDispatcher."""
    # 1. CodeRewriteEngine AST verification
    rewrite_engine = CodeRewriteEngine(allowed_paths=["."])
    proposal = RewriteProposal(
        target_filepath="./test_sample.py",
        original_snippet="def foo(): pass",
        proposed_snippet="def foo():\n    return 42",
        rationale="Optimize foo return"
    )
    assert rewrite_engine.verify_proposal_ast(proposal) is True

    # 2. GeneticWorkflowOptimizer MAP-Elites sorting
    optimizer = GeneticWorkflowOptimizer(population_size=5)
    optimizer.initialize_population("Base prompt template", {"lr": 0.01})
    eval_pop = optimizer.evaluate_generation(lambda g: len(g.prompt_template))
    assert len(eval_pop) == 5
    optimizer.perform_crossover_and_mutation()
    assert len(optimizer.population) == 5

    # 3. SFTPreferenceCollector clipped trajectory margin
    collector = SFTPreferenceCollector(advantage_clip_margin=0.05)
    step_a = TrajectoryStep(action="a1", predicted_expectation=1.0, actual_outcome=1.2, reward=1.0)
    step_b = TrajectoryStep(action="b1", predicted_expectation=1.0, actual_outcome=1.1, reward=0.9)
    dpo_pair = collector.compile_dpo_preference_pair("Prompt test", [step_a], [step_b])
    assert dpo_pair["margin"] >= 0.05

    # 4. LearnableRoutingGateDispatcher budget-decayed EFE routing
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0, budget_decay_factor=0.9)
    agent = SpecializedAgentProfile(
        agent_id="agent_1",
        domain_specialty="Research OS",
        cost_per_token=0.001,
        historical_success_rate=0.8,
        epistemic_curiosity=0.4
    )
    dispatcher.register_subagent(agent)
    routed = dispatcher.route_task(task_complexity=10.0, domain="Research OS")
    assert routed == "agent_1"


@pytest.mark.asyncio
async def test_cross_subsystem_active_inference_handoffs():
    """Validates cross-subsystem state handoffs across ResearchOS, EIOSKernel, EOSEngine, and AEAN HiveMind."""
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="200 Paper Active Inference Handoff",
        description="Validating 200 paper principles across cognitive layers",
        null_hypothesis="H0: No performance gain",
        target_metric="active_inference_yield"
    )

    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)
    assert completed_exp.is_statistically_significant is True

    # EIOS Kernel DAG execution
    kernel = EIOSKernel()
    node = ExecutionNode(name="sense_node", action_type="sense", payload={"hypothesis_id": str(hyp.hypothesis_id)})
    dag = ExecutionDAG(nodes={node.node_id: node})
    execution_success = await kernel.execute_dag(dag)
    assert execution_success is True

    # EOS Engine continuous sensing cycle
    eos = EOSEngine()
    cell = VentureCell(cell_id=uuid4(), name="Cell One", namespace="b2b_saas")
    eos_metrics = eos.run_continuous_sensing_cycle(cells=[cell], total_budget_cents=50000)
    assert isinstance(eos_metrics, dict)

    # AEAN HiveMind token bidding arbitrate
    hive = HiveMind(token_budget=100.0)
    bid = TaskBid(task="execute_hypothesis", priority=1, expected_value=10.0, token_cost=5.0)
    arbitrated = hive.arbitrate([bid])
    assert isinstance(arbitrated, list)
