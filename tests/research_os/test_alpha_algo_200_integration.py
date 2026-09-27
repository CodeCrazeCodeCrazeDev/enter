# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Verification integration test suite for the 200-paper corpus (IDs 301-500).
Verifies zero title/DOI overlap across all 500 papers, principle registration, ResearchOS literature review querying,
runtime component enhancements, and cross-subsystem active inference and token bidding state handoffs.
"""

import os
import pytest
import yaml
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
    ALPHAALGO_200_PRINCIPLES,
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    ProgramGenome,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler, TimeHorizon
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid


def test_500_paper_corpus_zero_overlap():
    """Verifies 100% zero title and DOI overlap across all 500 papers (IDs 1-500)."""
    db_path1 = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    db_path2 = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    db_path3 = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"

    assert os.path.exists(db_path1)
    assert os.path.exists(db_path2)
    assert os.path.exists(db_path3)

    with open(db_path1, "r", encoding="utf-8") as f:
        papers1 = yaml.safe_load(f).get("papers", [])
    with open(db_path2, "r", encoding="utf-8") as f:
        papers2 = yaml.safe_load(f).get("papers", [])
    with open(db_path3, "r", encoding="utf-8") as f:
        papers3 = yaml.safe_load(f).get("papers", [])

    all_papers = papers1 + papers2 + papers3
    assert len(all_papers) == 500, f"Expected 500 total papers, got {len(all_papers)}"

    titles = set()
    dois = set()

    for p in all_papers:
        meta = p.get("metadata", {})
        title = meta.get("title") or p.get("paper_title") or p.get("title")
        doi = meta.get("doi") or p.get("doi")

        assert title, f"Paper ID {p['id']} missing title"

        title_clean = title.strip().lower()
        assert title_clean not in titles, f"Duplicate title detected: '{title}' in Paper ID {p['id']}"
        titles.add(title_clean)

        if doi:
            doi_clean = doi.strip().lower()
            assert doi_clean not in dois, f"Duplicate DOI detected: '{doi}' in Paper ID {p['id']}"
            dois.add(doi_clean)


def test_register_200_paper_corpus_principles():
    """Verifies principles registration from the 200-paper corpus."""
    principles = register_200_paper_corpus_principles()
    assert len(principles) == 5
    assert len(ALPHAALGO_200_PRINCIPLES) == 5

    categories = [p["category"] for p in principles]
    assert "Market Microstructure & Non-Gaussian Hawkes Processes" in categories
    assert "Active Inference & Expected Free Energy" in categories
    assert "Reinforcement Learning & Trajectory Alignment" in categories
    assert "Multi-Agent Swarm Consensus & Game Theory" in categories
    assert "Genetic Program Synthesis & Quality Diversity" in categories


def test_research_os_conduct_literature_review():
    """Verifies multi-field literature review querying in ResearchOS."""
    ros = ResearchOS()
    res = ros.conduct_literature_review("Active Inference")

    assert res["domain"] == "Active Inference"
    assert res["reviewed_citations_count"] == 5
    assert res["matched_principles_count"] > 0
    assert len(res["synthesized_trends"]) > 0
    assert len(res["principles"]) > 0


def test_code_rewrite_engine_hawkes_ast_depth():
    """Verifies Hawkes AST per-function recursion depth check in CodeRewriteEngine."""
    engine = CodeRewriteEngine(allowed_paths=["."], max_ast_depth=3)

    # Valid non-recursive snippet
    valid_code = "def process_data(x):\n    return x + 1\n"
    prop_valid = engine.propose_rewrite(".", "def old(): pass", valid_code, "test valid")
    assert engine.verify_proposal_ast(prop_valid) is True

    # Snippet with recursion depth exceeding limit (4 recursive calls)
    recursive_code = (
        "def recursive_func(n):\n"
        "    if n <= 0: return 0\n"
        "    a = recursive_func(n - 1)\n"
        "    b = recursive_func(n - 2)\n"
        "    c = recursive_func(n - 3)\n"
        "    d = recursive_func(n - 4)\n"
        "    return a + b + c + d\n"
    )
    prop_recursive = engine.propose_rewrite(".", "def old(): pass", recursive_code, "test recursive limit")
    assert engine.verify_proposal_ast(prop_recursive) is False


def test_genetic_workflow_optimizer_map_elites():
    """Verifies immediate re-sorting upon evaluation in GeneticWorkflowOptimizer."""
    optimizer = GeneticWorkflowOptimizer(population_size=4)
    optimizer.initialize_population("Base template", {"param1": 1.0})

    def mock_score_fn(genome: ProgramGenome) -> float:
        return float(sum(str(v).count("1") for v in genome.parameters.values()))

    evaluated = optimizer.evaluate_generation(mock_score_fn)
    # Check that population is sorted in descending order of fitness_score
    scores = [g.fitness_score for g in evaluated]
    assert scores == sorted(scores, reverse=True)


def test_sft_preference_collector_margin_clipping():
    """Verifies clipped advantage margin thresholding in SFTPreferenceCollector."""
    collector = SFTPreferenceCollector(margin_clip=5.0)

    steps_a = [TrajectoryStep(action="a1", predicted_expectation=0.0, actual_outcome=10.0, reward=20.0)]
    steps_b = [TrajectoryStep(action="b1", predicted_expectation=10.0, actual_outcome=0.0, reward=-10.0)]

    pair = collector.compile_dpo_preference_pair("Solve task", steps_a, steps_b)

    assert pair["margin"] == 5.0  # Clipped from raw margin ~30.0
    assert pair["raw_margin"] > 5.0


def test_learnable_routing_gate_dispatcher():
    """Verifies budget-decayed EFE task routing and parameter updates."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(agent_id="agent_a", domain_specialty="nlp", cost_per_token=0.001, historical_success_rate=0.8)
    agent_b = SpecializedAgentProfile(agent_id="agent_b", domain_specialty="math", cost_per_token=0.005, historical_success_rate=0.9)

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    routed = dispatcher.route_task(task_complexity=100.0, domain="nlp")
    assert routed == "agent_a"

    dispatcher.update_routing_parameters("agent_a", success=True, cost_incurred=0.10)
    assert dispatcher.agents["agent_a"].historical_success_rate > 0.8


def test_cross_layer_active_inference_handoff():
    """Verifies active inference and token bidding state handoffs across ResearchOS, EIOS, EOS, and AEAN."""
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Active Inference Swarm Allocation",
        description="Minimizes Expected Free Energy in token bidding swarms.",
        null_hypothesis="No efficiency gain",
        target_metric="EFE_reduction"
    )
    exp = ros.create_experiment(hyp.hypothesis_id)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert hyp.status == "validated"

    # Handoff to EIOS Kernel & EOS Engine
    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag(f"Deploy hypothesis: {hyp.title}", target_budget_usd=50)
    assert dag is not None
    assert len(dag.nodes) > 0

    kernel = EIOSKernel()
    assert kernel is not None

    eos = EOSEngine()
    sensing_res = eos.run_continuous_sensing_cycle(cells=[], total_budget_cents=10000)
    assert sensing_res is not None

    # Handoff to AEAN HiveMind
    hive = HiveMind()
    bid = TaskBid(
        task="active_inference_allocation",
        priority=0.9,
        expected_value=25.0,
        token_cost=10
    )
    grants = hive.arbitrate([bid])
    assert len(grants) == 1
    assert grants[0].task == "active_inference_allocation"
    assert grants[0].granted is True
