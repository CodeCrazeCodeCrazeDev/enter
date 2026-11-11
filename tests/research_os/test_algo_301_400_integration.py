# -*- coding: utf-8 -*-
"""
test_algo_301_400_integration.py: Verification test suite for Papers 301-400 corpus curation,
100% zero-overlap audit, principle registration, ResearchOS literature review querying, and bug fixes.
"""

import os
import yaml
import pytest
from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
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
from apodex.cognition.brain import CognitiveBrain
from apodex.skills.runner import LearnFeedLoopEngine
from apodex.world_model.domain.entities import Entity


def test_papers_301_400_corpus_integrity_and_zero_overlap():
    """Verify that all 400 papers (1-400) exist, have valid metadata, and 100% zero title and DOI overlap."""
    db_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    ]

    all_titles = []
    all_dois = set()
    total_papers = 0

    for path in db_paths:
        assert os.path.exists(path), f"File {path} does not exist!"
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        papers = data.get("papers", []) if isinstance(data, dict) else data
        total_papers += len(papers)

        for p in papers:
            meta = p["metadata"]
            title = meta["title"].strip().lower()
            doi = meta.get("doi", "").strip().lower()

            assert title, f"Paper ID {p.get('id')} has empty title!"

            # Strict duplicate checks across title and non-empty DOIs
            assert title not in all_titles, f"Duplicate title found: '{meta['title']}' in paper {p.get('id')}!"
            if doi:
                assert doi not in all_dois, f"Duplicate DOI found: '{meta['doi']}' in paper {p.get('id')}!"
                all_dois.add(doi)

            all_titles.append(title)

    assert total_papers == 400, f"Expected 400 total papers, got {total_papers}"


def test_principles_registration_and_research_os_querying():
    """Verify that Papers 301-400 principles are registered and searchable via ResearchOS."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 6

    ros = ResearchOS()

    # Search literature review for Causal Inference / SCM
    causal_review = ros.conduct_literature_review("causal")
    assert causal_review["reviewed_citations_count"] > 0
    assert any("causal" in p["category"].lower() for p in causal_review["matched_principles"])

    # Search literature review for Hawkes / Point Processes
    hawkes_review = ros.conduct_literature_review("hawkes")
    assert hawkes_review["reviewed_citations_count"] > 0
    assert any("hawkes" in p["description"].lower() for p in hawkes_review["matched_principles"])


def test_hawkes_ast_recursive_depth_checking():
    """Verify Hawkes non-Gaussian recursive AST call depth limit in CodeRewriteEngine."""
    engine = CodeRewriteEngine(allowed_paths=["/app"])

    # Safe snippet
    safe_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""
    prop_safe = RewriteProposal(
        target_filepath="/app/test.py",
        original_snippet="",
        proposed_snippet=safe_code,
        rationale="Safe single recursion"
    )
    assert engine.verify_proposal_ast(prop_safe, max_recursive_depth=5) is True

    # Dangerous recursive call depth snippet (> 5 recursive calls in function)
    unstable_code = """
def runaway_recursion(n):
    return runaway_recursion(n) + runaway_recursion(n) + runaway_recursion(n) + runaway_recursion(n) + runaway_recursion(n) + runaway_recursion(n)
"""
    prop_unstable = RewriteProposal(
        target_filepath="/app/test.py",
        original_snippet="",
        proposed_snippet=unstable_code,
        rationale="Unstable recursion"
    )
    assert engine.verify_proposal_ast(prop_unstable, max_recursive_depth=5) is False


def test_genetic_optimizer_elite_insertion_and_bool_mutations():
    """Verify MAP-Elites elite insertion sorting and type safety in parameter mutation."""
    opt = GeneticWorkflowOptimizer(population_size=3, mutation_rate=1.0)
    opt.initialize_population(
        base_template="Base Prompt",
        base_params={"threshold": 0.5, "flag": True}
    )

    # Evaluate current generation to score base genomes
    opt.evaluate_generation(lambda g: 1.0)

    # Insert higher fitness elite
    elite = ProgramGenome(prompt_template="Elite", parameters={"threshold": 0.9}, fitness_score=10.0)
    opt.insert_elite(elite)
    assert opt.population[0].fitness_score == 10.0

    # Verify bool vs int mutation handling
    mutated = opt._mutate_parameters({"flag": True, "count": 10})
    assert isinstance(mutated["flag"], bool)
    assert isinstance(mutated["count"], int)


def test_sft_preference_collector_clipped_advantages():
    """Verify clipped advantage margins in SFTPreferenceCollector."""
    collector = SFTPreferenceCollector(discount_factor=0.9, max_advantage_clip=2.0)
    steps = [
        TrajectoryStep(action="a1", predicted_expectation=0.0, actual_outcome=100.0, reward=100.0)
    ]
    advantages = collector.compute_advantages(steps)
    assert advantages[0] == 2.0  # Clipped to max_advantage_clip (2.0) from 100.0


def test_pydantic_v2_brain_config_and_entity_timestamps():
    """Verify Pydantic V2 ConfigDict migration in CognitiveBrain and timezone-aware Entity updates."""
    brain = CognitiveBrain()
    assert brain.model_config.get("arbitrary_types_allowed") is True

    entity = Entity(name="TestEntity", entity_type="METRIC")
    orig_updated = entity.updated_at
    entity.update_property("val", 100)
    assert entity.updated_at >= orig_updated
