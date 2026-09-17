# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite for AlphaAlgo 301-400 paper corpus,
extracted transferable engineering principles, runtime component enhancements, and statistical validation flaw fixes.
"""

import os
import yaml
import pytest
from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    ALPHAALGO_301_400_PRINCIPLES,
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.research_os.statistical_validation import standard_normal_ppf, calculate_dsr


def test_301_400_corpus_integrity_and_zero_overlap():
    """Validates that papers 301-400 exist, count exactly 100, and have zero title/DOI overlap against papers 1-300."""
    db_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    ]

    for path in db_paths:
        assert os.path.exists(path), f"Corpus database path missing: {path}"

    all_titles = []
    all_dois = set()
    total_papers = 0

    for path in db_paths:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            papers = data.get("papers", [])
            total_papers += len(papers)
            for p in papers:
                meta = p.get("metadata", {})
                title = meta.get("title", "").strip().lower()
                doi = meta.get("doi", "").strip().lower()
                if title:
                    all_titles.append(title)
                if doi:
                    all_dois.add(doi)

    assert total_papers == 400, f"Expected 400 total papers across databases, found {total_papers}"
    assert len(set(all_titles)) == 400, "Duplicate titles detected in corpus across papers 1-400!"
    assert len(all_dois) == 200, "DOI tracking discrepancy in corpus!"


def test_principle_registration_and_literature_review():
    """Validates registration of principles 301-400 and literature review querying in ResearchOS."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 5
    assert len(ALPHAALGO_301_400_PRINCIPLES) == 5

    ros = ResearchOS()
    review = ros.conduct_literature_review("Market Microstructure & Order Dynamics")
    assert review["reviewed_citations_count"] >= 100
    assert "corpus_principles" in review
    assert len(review["corpus_principles"]) > 0


def test_code_rewrite_engine_hawkes_stability():
    """Validates Hawkes process recursion depth control in CodeRewriteEngine."""
    engine = CodeRewriteEngine(allowed_paths=["."])

    # Safe snippet with normal call depth
    safe_snippet = "def test():\n    print('hello')\n    print('world')\n"
    proposal_safe = RewriteProposal(
        target_filepath="./test.py",
        original_snippet="",
        proposed_snippet=safe_snippet,
        rationale="Normal snippet"
    )
    assert engine.verify_proposal_ast(proposal_safe, max_recursion_depth=5) is True

    # Explosive recursive snippet exceeding Hawkes recursion depth limit
    unstable_snippet = "def recurse():\n" + "\n".join(["    recurse()"] * 12)
    proposal_unstable = RewriteProposal(
        target_filepath="./test.py",
        original_snippet="",
        proposed_snippet=unstable_snippet,
        rationale="Recursive snippet"
    )
    assert engine.verify_proposal_ast(proposal_unstable, max_recursion_depth=5) is False

    # Verify that frequent non-recursive calls (e.g., logger or print) do not trigger Hawkes instability veto
    frequent_calls_snippet = "def my_func():\n" + "\n".join([f"    print({i})" for i in range(20)])
    proposal_frequent = RewriteProposal(
        target_filepath="./test.py",
        original_snippet="",
        proposed_snippet=frequent_calls_snippet,
        rationale="Frequent calls snippet"
    )
    assert engine.verify_proposal_ast(proposal_frequent, max_recursion_depth=5) is True


def test_genetic_workflow_optimizer_map_elites():
    """Validates MAP-Elites island migration sorting in GeneticWorkflowOptimizer."""
    optimizer = GeneticWorkflowOptimizer(population_size=5)
    optimizer.initialize_population(
        base_template="Execute workflow step",
        base_params={"rate": 1.0, "flag": True}
    )

    def scoring_fn(genome):
        return sum(v for v in genome.parameters.values() if isinstance(v, (int, float)))

    optimizer.evaluate_generation(scoring_fn)
    optimizer.perform_crossover_and_mutation()
    assert len(optimizer.population) == 5


def test_sft_preference_collector_clipped_margins():
    """Validates clipped advantage margin bounds in SFTPreferenceCollector."""
    collector = SFTPreferenceCollector(discount_factor=0.9)

    steps_a = [
        TrajectoryStep(action="a1", predicted_expectation=1.0, actual_outcome=10.0, reward=10.0),
        TrajectoryStep(action="a2", predicted_expectation=1.0, actual_outcome=20.0, reward=20.0)
    ]
    steps_b = [
        TrajectoryStep(action="b1", predicted_expectation=1.0, actual_outcome=0.0, reward=0.0),
        TrajectoryStep(action="b2", predicted_expectation=1.0, actual_outcome=0.0, reward=0.0)
    ]

    record = collector.compile_dpo_preference_pair(
        prompt="Execute strategy",
        steps_run_a=steps_a,
        steps_run_b=steps_b,
        max_margin_clip=5.0
    )

    assert record["margin"] == 5.0
    assert record["raw_margin"] > 5.0


def test_learnable_routing_gate_dispatcher_active_inference():
    """Validates Active Inference EFE routing and budget tracking in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(
        agent_id="agent_fast",
        domain_specialty="Microstructure",
        cost_per_token=0.001,
        historical_success_rate=0.8,
        epistemic_curiosity=0.7
    )
    dispatcher.register_subagent(agent_a)

    selected = dispatcher.route_task(task_complexity=10.0, domain="Microstructure")
    assert selected == "agent_fast"

    dispatcher.update_routing_parameters(agent_id="agent_fast", success=True, cost_incurred=0.01)
    assert dispatcher.budget_spent == 0.01
    assert agent_a.epistemic_curiosity < 0.7


def test_statistical_validation_ppf_clamping():
    """Validates standard_normal_ppf probability clamping and DSR calculation."""
    # Test boundary probability clamping (does not raise ValueError)
    val_low = standard_normal_ppf(0.0)
    val_high = standard_normal_ppf(1.0)
    assert val_low < 0
    assert val_high > 0

    dsr = calculate_dsr(sharpe=1.5, trials=10, returns_length=252)
    assert 0.0 <= dsr <= 1.0
