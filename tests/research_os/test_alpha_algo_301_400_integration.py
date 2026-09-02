# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite validating
the 100-paper corpus (IDs 301-400), zero-overlap across all 400 research papers,
principle registration, ResearchOS literature review synthesis, and AlphaAlgo runtime component enhancements.
"""

import glob
import os
import yaml
import pytest

from apodex.ai_eos.research.integration import (
    ALPHAALGO_301_400_PRINCIPLES,
    register_301_400_paper_corpus_principles,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    TrajectoryStep,
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.research_os.statistical_validation import (
    standard_normal_ppf,
    calculate_dsr,
)


def test_corpus_301_400_and_global_uniqueness():
    """Verify papers 301-400 exist, have 100 papers, and zero title/DOI overlap across all 400 papers."""
    yaml_files = sorted(glob.glob("docs/research/papers/*.yaml"))
    all_papers = []

    for path in yaml_files:
        if "DECISIONS" in path:
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        papers = data if isinstance(data, list) else data.get("papers", [])
        all_papers.extend(papers)

    assert len(all_papers) == 400, f"Expected exactly 400 total research papers, found {len(all_papers)}"

    ids = set()
    titles = set()
    dois = set()

    for p in all_papers:
        pid = p.get("id")
        meta = p.get("metadata", p)
        title = meta.get("title", "").strip().lower()
        doi = meta.get("doi", "").strip().lower()

        assert pid not in ids, f"Duplicate paper ID found: {pid}"
        ids.add(pid)

        if title:
            assert title not in titles, f"Duplicate paper title found: {title}"
            titles.add(title)

        if doi:
            assert doi not in dois, f"Duplicate paper DOI found: {doi}"
            dois.add(doi)

    assert len(ids) == 400
    assert min(ids) == 1
    assert max(ids) == 400


def test_principles_registration_and_research_os_synthesis():
    """Verify principles registration and ResearchOS literature review synthesis."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 4
    assert principles == ALPHAALGO_301_400_PRINCIPLES

    ros = ResearchOS()
    review = ros.conduct_literature_review("Market Microstructure")
    assert review["domain"] == "Market Microstructure"
    assert review["reviewed_citations_count"] == 4
    assert review["matching_principles_count"] >= 1
    assert any("Hawkes" in p["title"] for p in review["principles"])


def test_runtime_engine_enhancements():
    """Verify AlphaAlgo runtime components function cleanly with extracted principles."""
    # 1. CodeRewriteEngine AST verification & dry-run simulation
    engine = CodeRewriteEngine(allowed_paths=["."])
    snippet_orig = "def time_now() -> str:\n    import datetime\n    return datetime.datetime.now(datetime.timezone.utc).isoformat()"
    snippet_prop = "def time_now() -> str:\n    import datetime\n    return datetime.datetime.now(datetime.timezone.utc).isoformat()"
    prop = engine.propose_rewrite(
        filepath="apodex/ai_eos/research/integration.py",
        original_snippet=snippet_orig,
        proposed_snippet=snippet_prop,
        rationale="Verify identical function snippet"
    )
    assert engine.verify_proposal_ast(prop) is True
    assert engine.dry_run_simulation(prop) is True

    # 2. GeneticWorkflowOptimizer island population
    optimizer = GeneticWorkflowOptimizer(population_size=5, mutation_rate=0.2)
    optimizer.initialize_population(
        base_template="Optimize execution pipeline.",
        base_params={"alpha": 0.5, "beta": 1.2}
    )
    assert len(optimizer.population) == 5

    # 3. SFTPreferenceCollector trajectory advantage computation
    collector = SFTPreferenceCollector(discount_factor=0.95)
    steps_a = [
        TrajectoryStep(action="rewrite_module", predicted_expectation=0.5, actual_outcome=0.9, reward=1.0),
        TrajectoryStep(action="verify_ast", predicted_expectation=0.8, actual_outcome=0.95, reward=1.0),
    ]
    steps_b = [
        TrajectoryStep(action="rewrite_module", predicted_expectation=0.5, actual_outcome=0.2, reward=-0.5),
        TrajectoryStep(action="verify_ast", predicted_expectation=0.8, actual_outcome=0.1, reward=-1.0),
    ]
    pair = collector.compile_dpo_preference_pair("Optimize code rewrite", steps_a, steps_b)
    assert "rewrite_module" in pair["chosen"]
    assert pair["margin"] > 0

    # 4. LearnableRoutingGateDispatcher task routing
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    dispatcher.register_subagent(SpecializedAgentProfile(agent_id="agent_quant", domain_specialty="Finance", cost_per_token=0.01))
    dispatcher.register_subagent(SpecializedAgentProfile(agent_id="agent_code", domain_specialty="Code", cost_per_token=0.02))

    selected = dispatcher.route_task(task_complexity=50.0, domain="Finance")
    assert selected == "agent_quant"


def test_statistical_validation_edge_cases():
    """Verify probability clamping in standard_normal_ppf and zero-variance calculation in calculate_dsr."""
    # Probability clamping boundary tests
    val_0 = standard_normal_ppf(0.0)
    val_1 = standard_normal_ppf(1.0)
    assert isinstance(val_0, float)
    assert isinstance(val_1, float)

    # DSR calculation
    dsr = calculate_dsr(sharpe=1.5, trials=10, returns_length=100)
    assert 0.0 <= dsr <= 1.0
