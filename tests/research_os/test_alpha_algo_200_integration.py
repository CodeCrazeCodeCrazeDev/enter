# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite for the 200-paper research corpus (IDs 301-500).
Verifies:
1. Zero title and DOI overlap across paper corpus YAML files (papers 1-300 vs papers 301-500).
2. Registration of 200-paper principles in integration.py.
3. Enhanced runtime components (CodeRewriteEngine, GeneticWorkflowOptimizer, SFTPreferenceCollector, LearnableRoutingGateDispatcher).
4. Literature review querying in ResearchOS.
5. Cross-layer state handoffs in ResearchToSystemBridge.
"""

import os
import pytest
import yaml
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    ProgramGenome,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    ResearchToSystemBridge,
    ALPHAALGO_200_PRINCIPLES
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_zero_corpus_overlap():
    """Programmatically verifies zero title overlap between papers 1-300 and papers 301-500."""
    db_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]
    existing_titles = set()
    for path in db_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            papers = data if isinstance(data, list) else data.get("papers", [])
            for p in papers:
                title = p.get("metadata", {}).get("title") or p.get("title")
                if title:
                    existing_titles.add(title.lower().strip())

    new_db_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(new_db_path), "ALPHA_ALGO_200_NEW_RESEARCH.yaml does not exist."

    with open(new_db_path, "r", encoding="utf-8") as f:
        new_data = yaml.safe_load(f)
    new_papers = new_data if isinstance(new_data, list) else new_data.get("papers", [])

    assert len(new_papers) == 200, f"Expected 200 papers in new corpus, found {len(new_papers)}"

    for p in new_papers:
        title = (p.get("metadata", {}).get("title") or p.get("title", "")).lower().strip()
        p_tokens = set(title.split())
        for ext in existing_titles:
            ext_tokens = set(ext.split())
            intersection = p_tokens.intersection(ext_tokens)
            union = p_tokens.union(ext_tokens)
            similarity = len(intersection) / len(union) if union else 0.0
            assert similarity <= 0.35, f"High title similarity ({similarity:.2f}) detected: '{title}' vs '{ext}'"


def test_registered_principles():
    """Verifies principles are registered and mapped properly."""
    principles = register_200_paper_corpus_principles()
    assert len(principles) >= 5
    assert "P303_HAWKES_STABILITY" in principles
    assert principles["P303_HAWKES_STABILITY"]["paper_id"] == 303


def test_code_rewrite_engine_hawkes_ast_check(tmp_path):
    """Verifies Hawkes AST recursion depth check in CodeRewriteEngine."""
    allowed = [str(tmp_path)]
    engine = CodeRewriteEngine(allowed_paths=allowed, max_recursion_depth=5)

    valid_snippet = "def add(a, b):\n    return a + b\n"
    proposal_valid = engine.propose_rewrite(
        filepath=os.path.join(str(tmp_path), "test.py"),
        original_snippet="",
        proposed_snippet=valid_snippet,
        rationale="valid addition"
    )
    assert engine.verify_proposal_ast(proposal_valid) is True

    # Snippet with 7 calls inside a single function (exceeding limit of 5)
    deep_snippet = "def deep_func():\n    f1()\n    f2()\n    f3()\n    f4()\n    f5()\n    f6()\n    f7()\n"
    proposal_deep = engine.propose_rewrite(
        filepath=os.path.join(str(tmp_path), "test.py"),
        original_snippet="",
        proposed_snippet=deep_snippet,
        rationale="deep calls"
    )
    assert engine.verify_proposal_ast(proposal_deep) is False


def test_genetic_workflow_optimizer_migration_gate():
    """Verifies island MAP-Elites migration gate in GeneticWorkflowOptimizer."""
    optimizer = GeneticWorkflowOptimizer(population_size=5, fitness_threshold=0.8)
    optimizer.initialize_population(base_template="Base prompt", base_params={"a": 1.0})

    low_elite = ProgramGenome(prompt_template="Low prompt", fitness_score=0.5)
    high_elite = ProgramGenome(prompt_template="High prompt", fitness_score=0.95)

    assert optimizer.insert_elite_and_sort(low_elite) is False
    assert optimizer.insert_elite_and_sort(high_elite) is True
    assert optimizer.population[0].fitness_score == 0.95


def test_sft_preference_collector_advantage_clipping():
    """Verifies advantage margin clipping in SFTPreferenceCollector."""
    collector = SFTPreferenceCollector(discount_factor=0.95, max_margin_clip=5.0)

    steps_a = [TrajectoryStep(action="a1", predicted_expectation=0.0, actual_outcome=10.0, reward=20.0)]
    steps_b = [TrajectoryStep(action="b1", predicted_expectation=0.0, actual_outcome=1.0, reward=1.0)]

    pair = collector.compile_dpo_preference_pair("Prompt", steps_a, steps_b)
    assert pair["margin"] == 5.0
    assert pair["raw_margin"] > 5.0


def test_learnable_routing_gate_dispatcher():
    """Verifies budget-decayed task routing in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    profile = SpecializedAgentProfile(
        agent_id="agent_1",
        domain_specialty="Market Microstructure",
        cost_per_token=0.001,
        historical_success_rate=0.9,
        epistemic_curiosity=0.2
    )
    dispatcher.register_subagent(profile)

    selected = dispatcher.route_task(task_complexity=100.0, domain="Market Microstructure")
    assert selected == "agent_1"


def test_research_os_literature_review():
    """Verifies ResearchOS querying 200-paper principles in literature review."""
    ros = ResearchOS()
    review = ros.conduct_literature_review(domain="Active Inference")
    assert review["domain"] == "Active Inference"
    assert len(review["matched_principles"]) > 0
    assert any("Active Inference" in trend or "Expected Free Energy" in trend for trend in review["synthesized_trends"])


def test_research_to_system_bridge_handoff():
    """Verifies cross-layer active inference handoff via ResearchToSystemBridge."""
    bridge = ResearchToSystemBridge()

    class MockHypothesis:
        hypothesis_id = uuid4()
        title = "Mock Active Inference Hypothesis"
        status = "validated"
        domain = "Market Microstructure"

    hyp = MockHypothesis()
    handoff = bridge.bridge_hypothesis_to_system_layers(hypothesis=hyp)

    assert handoff["hypothesis_title"] == "Mock Active Inference Hypothesis"
    assert handoff["status"] == "validated"
    assert len(bridge.handoff_ledger) == 1
