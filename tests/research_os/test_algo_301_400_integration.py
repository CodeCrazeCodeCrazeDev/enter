# -*- coding: utf-8 -*-
"""
test_algo_301_400_integration.py: Comprehensive integration test suite verifying
the 100-paper corpus (IDs 301-400), zero corpus overlap across all 400 papers,
transferable engineering principles registration, Research OS literature review,
and runtime component flaw fixes.
"""

import os
import glob
import yaml
import pytest
from apodex.ai_eos.research.integration import (
    CodeRewriteEngine, RewriteProposal,
    GeneticWorkflowOptimizer, ProgramGenome,
    SFTPreferenceCollector, TrajectoryStep,
    LearnableRoutingGateDispatcher, SpecializedAgentProfile,
    register_301_400_paper_corpus_principles, ALPHAALGO_301_400_PRINCIPLES
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_zero_corpus_overlap_across_400_papers():
    """Verifies that across all 400 research papers, there are 0 duplicate titles and 0 duplicate DOIs."""
    yaml_files = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    ]

    titles = {}
    dois = {}
    total_papers = 0

    for path in yaml_files:
        assert os.path.exists(path), f"Corpus YAML file missing: {path}"
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            papers = data.get("papers", [])
            for p in papers:
                total_papers += 1
                pid = p.get("id") or p.get("paper_id")
                meta = p.get("metadata", {})
                title = (meta.get("title") or p.get("title") or "").strip().lower()
                doi = (meta.get("doi") or p.get("doi") or "").strip().lower()

                assert title, f"Paper ID {pid} in {path} missing title"
                assert title not in titles, f"Duplicate title found: '{title}' in {path} (id {pid}) and {titles.get(title)}"
                titles[title] = (path, pid)

                if doi:
                    assert doi not in dois, f"Duplicate DOI found: '{doi}' in {path} (id {pid}) and {dois.get(doi)}"
                    dois[doi] = (path, pid)

    assert total_papers == 400, f"Expected 400 total papers across files, got {total_papers}"
    assert len(titles) == 400, f"Expected 400 unique titles, got {len(titles)}"


def test_principle_registration_301_400():
    """Verifies principle registration and content structure for papers 301-400."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 4
    assert len(ALPHAALGO_301_400_PRINCIPLES) == 4

    p_ids = [p["principle_id"] for p in principles]
    assert "P-301-400-01" in p_ids
    assert "P-301-400-02" in p_ids
    assert "P-301-400-03" in p_ids
    assert "P-301-400-04" in p_ids


def test_research_os_literature_review_integration():
    """Verifies ResearchOS.conduct_literature_review returns principles matching the query domain."""
    ros = ResearchOS()

    # Query matching Hawkes non-Gaussian principle
    res_hawkes = ros.conduct_literature_review("Hawkes")
    assert res_hawkes["domain"] == "Hawkes"
    assert len(res_hawkes["matching_principles"]) >= 1
    assert any("Hawkes" in p["title"] for p in res_hawkes["matching_principles"])

    # Query matching Genetic Search principle
    res_genetic = ros.conduct_literature_review("Genetic")
    assert len(res_genetic["matching_principles"]) >= 1


def test_code_rewrite_engine_hawkes_ast_verification():
    """Verifies Hawkes non-Gaussian recursive call depth checks in CodeRewriteEngine."""
    engine = CodeRewriteEngine(allowed_paths=["/tmp"])

    # Normal function calls - should pass
    normal_code = """
def process_data(x):
    return math.sin(x)

def execute_pipeline(data):
    return [process_data(item) for item in data]
"""
    p_normal = RewriteProposal(
        target_filepath="/tmp/test_normal.py",
        original_snippet="",
        proposed_snippet=normal_code,
        rationale="Normal processing pipeline"
    )
    assert engine.verify_proposal_ast(p_normal) is True

    # Dangerous call (eval) - should fail security linting
    eval_code = "def bad_fn(): return eval('1+1')"
    p_eval = RewriteProposal(
        target_filepath="/tmp/test_eval.py",
        original_snippet="",
        proposed_snippet=eval_code,
        rationale="Security violation test"
    )
    assert engine.verify_proposal_ast(p_eval) is False

    # Excessively recursive function (>10 self calls) - should trigger Hawkes Stability Veto
    recursive_code = "def recursive_fn():\n" + "\n".join(["    recursive_fn()" for _ in range(12)])
    p_rec = RewriteProposal(
        target_filepath="/tmp/test_rec.py",
        original_snippet="",
        proposed_snippet=recursive_code,
        rationale="Excessive recursion test"
    )
    assert engine.verify_proposal_ast(p_rec) is False


def test_genetic_workflow_optimizer_type_safe_mutation_and_sorting():
    """Verifies type-safe bool parameter mutation and MAP-Elites population sorting in GeneticWorkflowOptimizer."""
    optimizer = GeneticWorkflowOptimizer(population_size=5, mutation_rate=1.0)
    base_params = {"active": True, "threshold": 0.5, "count": 10}

    # Verify _mutate_parameters preserves bool type
    mutated = optimizer._mutate_parameters(base_params)
    assert isinstance(mutated["active"], bool)
    assert mutated["active"] is False  # toggled with mutation_rate 1.0

    # Verify initialize_population and evaluate_generation sorting
    optimizer.initialize_population("Base prompt template", base_params)
    assert len(optimizer.population) == 5

    def mock_scoring(genome: ProgramGenome) -> float:
        return float(genome.parameters.get("count", 0))

    evaluated = optimizer.evaluate_generation(mock_scoring)
    # Check descending order sorting
    scores = [g.fitness_score for g in evaluated]
    assert scores == sorted(scores, reverse=True)


def test_sft_preference_collector_advantage_clipping():
    """Verifies clipped trajectory advantage margins in SFTPreferenceCollector."""
    collector = SFTPreferenceCollector(discount_factor=0.95)

    # Large reward leading to high unclipped advantage
    steps = [
        TrajectoryStep(
            action="high_yield_action",
            predicted_expectation=0.0,
            actual_outcome=100.0,
            reward=100.0
        )
    ]

    # With max_clip_margin = 2.0, calculated advantage (100.0) should be clipped to 2.0
    advantages = collector.compute_advantages(steps, max_clip_margin=2.0)
    assert len(advantages) == 1
    assert advantages[0] == 2.0


def test_learnable_routing_gate_dispatcher_efe():
    """Verifies Expected Free Energy task routing in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    p1 = SpecializedAgentProfile(
        agent_id="agent_quant",
        domain_specialty="Quantitative Finance",
        cost_per_token=0.001,
        historical_success_rate=0.9,
        epistemic_curiosity=0.8
    )
    p2 = SpecializedAgentProfile(
        agent_id="agent_general",
        domain_specialty="General",
        cost_per_token=0.0001,
        historical_success_rate=0.5,
        epistemic_curiosity=0.2
    )

    dispatcher.register_subagent(p1)
    dispatcher.register_subagent(p2)

    selected = dispatcher.route_task(task_complexity=100.0, domain="Quantitative Finance")
    assert selected == "agent_quant"

    # Update metrics on task completion
    dispatcher.update_routing_parameters(agent_id="agent_quant", success=True, cost_incurred=0.1)
    assert dispatcher.budget_spent == 0.1
    assert dispatcher.agents["agent_quant"].epistemic_curiosity < 0.8
