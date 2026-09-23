# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite validating the curation of
research papers 301-400, principle registration, ResearchOS literature review querying,
and runtime enhancements in CodeRewriteEngine, GeneticWorkflowOptimizer, SFTPreferenceCollector,
and LearnableRoutingGateDispatcher.
"""

import os
import glob
import yaml
import pytest
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    ProgramGenome,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_400_paper_corpus_zero_overlap():
    """Verify all 400 paper IDs and titles across YAML files are 100% unique."""
    yaml_files = sorted(glob.glob("docs/research/papers/*.yaml"))
    seen_ids = set()
    seen_titles = set()
    seen_dois = set()

    total_papers = 0
    for path in yaml_files:
        if "INGESTION" in path:
            continue
        with open(path, "r", encoding="utf-8") as f:
            db = yaml.safe_load(f)
            papers = db.get("papers", [])
            for p in papers:
                total_papers += 1
                pid = p["id"]
                title = p["metadata"]["title"].lower().strip()
                doi = p["metadata"].get("doi", "").lower().strip()

                assert pid not in seen_ids, f"Duplicate ID found: {pid}"
                assert title not in seen_titles, f"Duplicate title found: {title}"
                if doi:
                    assert doi not in seen_dois, f"Duplicate DOI found: {doi}"

                seen_ids.add(pid)
                seen_titles.add(title)
                if doi:
                    seen_dois.add(doi)

    assert total_papers >= 400, f"Expected at least 400 papers, found {total_papers}"


def test_register_301_400_principles():
    """Verify principles extracted from papers 301-400 are registered correctly."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) >= 5
    categories = {p["category"] for p in principles}
    assert "Market Microstructure" in categories
    assert "Active Inference" in categories
    assert "RL & Alignment" in categories
    assert "Evolutionary Search" in categories
    assert "Multi-Agent Systems" in categories


def test_research_os_multi_field_literature_querying():
    """Verify ResearchOS conduct_literature_review queries across multi-field namespaces."""
    ros = ResearchOS()
    res = ros.conduct_literature_review("hawkes")
    assert "matched_principles" in res
    assert len(res["matched_principles"]) > 0
    matched_ids = [p["paper_id"] for p in res["matched_principles"]]
    assert 301 in matched_ids


def test_code_rewrite_engine_hawkes_ast_call_depth_check(tmp_path):
    """Verify CodeRewriteEngine enforces per-function recursive call depth limits."""
    allowed_dir = str(tmp_path)
    target_file = os.path.join(allowed_dir, "sample.py")
    with open(target_file, "w") as f:
        f.write("def foo():\n    pass\n")

    engine = CodeRewriteEngine(allowed_paths=[allowed_dir], max_call_depth=3)

    # Valid rewrite proposal (non-recursive calls)
    valid_code = "def bar():\n    x = 1\n    y = 2\n    return x + y\n"
    prop_valid = engine.propose_rewrite(
        filepath=target_file,
        original_snippet="def foo():\n    pass\n",
        proposed_snippet=valid_code,
        rationale="Normal non-recursive snippet"
    )
    assert engine.verify_proposal_ast(prop_valid) is True

    # Invalid rewrite proposal (excessive recursive call depth inside function definition)
    recursive_code = (
        "def rec_fn():\n"
        "    rec_fn()\n"
        "    rec_fn()\n"
        "    rec_fn()\n"
        "    rec_fn()\n"
        "    rec_fn()\n"
    )
    prop_invalid = engine.propose_rewrite(
        filepath=target_file,
        original_snippet="def foo():\n    pass\n",
        proposed_snippet=recursive_code,
        rationale="Excessive recursive function snippet"
    )
    assert engine.verify_proposal_ast(prop_invalid) is False


def test_genetic_optimizer_immediate_elite_resorting():
    """Verify GeneticWorkflowOptimizer immediately re-sorts island population on elite insertion."""
    optimizer = GeneticWorkflowOptimizer(population_size=5)
    optimizer.initialize_population(base_template="base", base_params={"a": 1})

    for i, g in enumerate(optimizer.population):
        g.fitness_score = float(i)

    elite = ProgramGenome(prompt_template="elite", parameters={}, fitness_score=100.0)
    optimizer.insert_elite(elite)

    assert optimizer.population[0].fitness_score == 100.0
    assert len(optimizer.population) == 5


def test_sft_preference_collector_clipped_advantage_margin():
    """Verify SFTPreferenceCollector clips trajectory advantage margins."""
    collector = SFTPreferenceCollector(max_margin=2.0)

    steps_a = [
        TrajectoryStep(action="a1", predicted_expectation=0.0, actual_outcome=10.0, reward=10.0),
        TrajectoryStep(action="a2", predicted_expectation=0.0, actual_outcome=10.0, reward=10.0)
    ]
    steps_b = [
        TrajectoryStep(action="b1", predicted_expectation=10.0, actual_outcome=-10.0, reward=-10.0),
        TrajectoryStep(action="b2", predicted_expectation=10.0, actual_outcome=-10.0, reward=-10.0)
    ]

    pref_pair = collector.compile_dpo_preference_pair("test prompt", steps_a, steps_b)
    assert pref_pair["margin"] == 2.0
    assert pref_pair["raw_margin"] > 2.0


def test_learnable_routing_dispatcher_decayed_curiosity():
    """Verify LearnableRoutingGateDispatcher applies budget-decayed epistemic curiosity."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    agent_a = SpecializedAgentProfile(
        agent_id="agent_a", domain_specialty="trading", cost_per_token=0.01, historical_success_rate=0.5, epistemic_curiosity=2.0
    )
    agent_b = SpecializedAgentProfile(
        agent_id="agent_b", domain_specialty="trading", cost_per_token=0.01, historical_success_rate=0.8, epistemic_curiosity=0.01
    )
    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    # High remaining budget -> agent_a (high curiosity)
    selected_1 = dispatcher.route_task(task_complexity=10.0, domain="trading")
    assert selected_1 == "agent_a"

    # Spend 95% of budget
    dispatcher.budget_spent = 9.5

    # Low remaining budget -> agent_b (high pragmatic success rate)
    selected_2 = dispatcher.route_task(task_complexity=10.0, domain="trading")
    assert selected_2 == "agent_b"
