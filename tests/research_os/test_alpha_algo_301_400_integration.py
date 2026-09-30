# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Verification and integration test suite
validating zero corpus overlap across 400 research papers, principle registration,
ResearchOS literature review querying, and runtime component flaw fixes.
"""

import os
import tempfile
import pytest
import yaml

from apodex.ai_eos.research.integration import (
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    RewriteProposal,
    ProgramGenome,
    TrajectoryStep,
    SpecializedAgentProfile,
    register_301_400_paper_corpus_principles,
    ALPHAALGO_301_400_PRINCIPLES,
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_400_paper_corpus_zero_overlap() -> None:
    """Verifies that all 400 papers across YAML files have unique IDs, unique titles, and unique DOIs."""
    yaml_files = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml",
    ]

    all_ids = set()
    all_titles = set()
    all_dois = set()
    total_papers = 0

    for yf in yaml_files:
        assert os.path.exists(yf), f"Missing corpus file: {yf}"
        with open(yf, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        papers = data.get("papers", [])
        total_papers += len(papers)

        for p in papers:
            pid = p["id"]
            meta = p["metadata"]
            title = meta["title"].strip().lower()
            doi = meta.get("doi", "").strip().lower() if meta.get("doi") else None

            assert pid not in all_ids, f"Duplicate paper ID found: {pid}"
            all_ids.add(pid)

            assert title not in all_titles, f"Duplicate paper title found: '{title}'"
            all_titles.add(title)

            if doi:
                assert doi not in all_dois, f"Duplicate paper DOI found: '{doi}'"
                all_dois.add(doi)

    assert total_papers == 400
    assert len(all_ids) == 400
    assert len(all_titles) == 400
    assert len(all_dois) == 200  # DOIs provided for 200 papers across 201-400


def test_principle_registration_and_research_os_literature_review() -> None:
    """Verifies principles registration and querying in ResearchOS.conduct_literature_review."""
    principles = register_301_400_paper_corpus_principles()
    assert "hawkes_ast_recursion_control" in principles
    assert "map_elites_island_migration" in principles
    assert "clipped_advantage_margins" in principles
    assert "budget_decayed_efe_routing" in principles

    ros = ResearchOS()
    review = ros.conduct_literature_review(domain="Evolutionary")
    assert review["domain"] == "Evolutionary"
    assert review["reviewed_citations_count"] >= 101
    assert len(review["matching_principles"]) >= 1
    assert any("MAP-Elites" in p.get("paper_title", "") or "MAP-Elites" in p.get("description", "") or "MAP-Elites" in p.get("extracted_principle", "") for p in review["matching_principles"])


def test_hawkes_ast_recursion_call_depth_veto() -> None:
    """Verifies that CodeRewriteEngine vetoes proposals with excessive recursive function calls."""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = CodeRewriteEngine(allowed_paths=[tmpdir])
        target_file = os.path.join(tmpdir, "recursive_script.py")

        with open(target_file, "w") as f:
            f.write("def recurse():\n    pass\n")

        # Create proposal with excessive recursive calls (6 calls > limit 5)
        excessive_recursive_code = (
            "def recurse():\n"
            "    recurse()\n"
            "    recurse()\n"
            "    recurse()\n"
            "    recurse()\n"
            "    recurse()\n"
            "    recurse()\n"
        )
        proposal = engine.propose_rewrite(
            filepath=target_file,
            original_snippet="def recurse():\n    pass",
            proposed_snippet=excessive_recursive_code,
            rationale="Test Hawkes recursion depth check"
        )

        assert engine.verify_proposal_ast(proposal) is False
        assert engine.commit_rewrite(proposal) is False

        # Moderate recursion (1 call) should pass
        moderate_code = "def recurse(n):\n    if n > 0:\n        return recurse(n - 1)\n    return 0\n"
        valid_proposal = engine.propose_rewrite(
            filepath=target_file,
            original_snippet="def recurse():\n    pass",
            proposed_snippet=moderate_code,
            rationale="Valid bounded recursion"
        )
        assert engine.verify_proposal_ast(valid_proposal) is True


def test_map_elites_population_sorting() -> None:
    """Verifies that GeneticWorkflowOptimizer re-sorts population on elite crossover/mutation."""
    optimizer = GeneticWorkflowOptimizer(population_size=6, mutation_rate=0.3)
    optimizer.initialize_population("Execute step", {"lr": 0.01})

    def mock_score(g: ProgramGenome) -> float:
        return float(g.parameters.get("lr", 0.01) * 10.0)

    optimizer.evaluate_generation(mock_score)
    optimizer.perform_crossover_and_mutation()

    # Population must remain sorted descending by fitness_score
    scores = [g.fitness_score for g in optimizer.population]
    assert scores == sorted(scores, reverse=True)


def test_clipped_advantage_margins() -> None:
    """Verifies that SFTPreferenceCollector clips trajectory advantage margins."""
    collector = SFTPreferenceCollector(discount_factor=0.99)

    # Trajectory A with extreme rewards
    traj_a = [
        TrajectoryStep(action="a1", predicted_expectation=0.0, actual_outcome=10.0, reward=10.0),
        TrajectoryStep(action="a2", predicted_expectation=0.0, actual_outcome=10.0, reward=10.0),
    ]

    # Trajectory B with negative rewards
    traj_b = [
        TrajectoryStep(action="b1", predicted_expectation=0.0, actual_outcome=-10.0, reward=-10.0),
        TrajectoryStep(action="b2", predicted_expectation=0.0, actual_outcome=-10.0, reward=-10.0),
    ]

    pair = collector.compile_dpo_preference_pair(
        prompt="Execute task",
        steps_run_a=traj_a,
        steps_run_b=traj_b
    )

    assert pair["margin"] == 2.0  # Clipped to max +2.0
    assert pair["raw_margin"] > 2.0


def test_budget_decayed_efe_task_routing() -> None:
    """Verifies that LearnableRoutingGateDispatcher incorporates budget decay into routing."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    expensive_agent = SpecializedAgentProfile(
        agent_id="expensive",
        domain_specialty="AI",
        cost_per_token=0.01,
        historical_success_rate=0.95,
        epistemic_curiosity=0.1
    )
    cheap_agent = SpecializedAgentProfile(
        agent_id="cheap",
        domain_specialty="AI",
        cost_per_token=0.001,
        historical_success_rate=0.50,
        epistemic_curiosity=0.1
    )

    dispatcher.register_subagent(expensive_agent)
    dispatcher.register_subagent(cheap_agent)

    # With zero budget spent, expensive agent is selected due to high success rate
    selected_0 = dispatcher.route_task(task_complexity=10, domain="AI")
    assert selected_0 == "expensive"

    # As budget spent reaches 90% ($9.00), cost penalty factor rises to >5.0x
    dispatcher.budget_spent = 9.0
    selected_90 = dispatcher.route_task(task_complexity=10, domain="AI")
    assert selected_90 == "cheap"
