# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py
Comprehensive integration test suite for AlphaAlgo 100-paper corpus (IDs 301-400),
verifying 100% zero corpus overlap, principle registration, ResearchOS literature review lookup,
and runtime enhancements.
"""

import os
import yaml
import pytest
from datetime import datetime, timezone, timedelta

from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    ALPHAALGO_301_400_PRINCIPLES,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    TrajectoryStep,
    ProgramGenome
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.cognition.brain import CognitiveBrain


def test_paper_corpus_zero_overlap():
    """Verifies 100% zero title or DOI overlap across all 400 research papers in the repository."""
    files = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    ]

    seen_titles = set()
    seen_dois = set()
    total_papers = 0

    for f in files:
        assert os.path.exists(f), f"Corpus YAML file missing: {f}"
        with open(f, "r", encoding="utf-8") as fp:
            data = yaml.safe_load(fp)
            papers = data.get("papers", []) if isinstance(data, dict) else data
            total_papers += len(papers)

            for p in papers:
                title = (p.get("metadata", {}).get("title") if isinstance(p.get("metadata"), dict) else None) or p.get("title")
                doi = (p.get("metadata", {}).get("doi") if isinstance(p.get("metadata"), dict) else None) or p.get("doi")

                assert title, f"Missing title in paper {p}"

                t_clean = str(title).strip().lower()
                assert t_clean not in seen_titles, f"Title overlap detected: {title}"
                seen_titles.add(t_clean)

                if doi:
                    d_clean = str(doi).strip().lower()
                    assert d_clean not in seen_dois, f"DOI overlap detected: {doi}"
                    seen_dois.add(d_clean)

    assert total_papers == 400
    assert len(seen_titles) == 400
    assert len(seen_dois) >= 200  # Unique DOIs across papers 201-400


def test_principle_registration_and_research_os_lookup():
    """Tests registration of 301-400 corpus principles and ResearchOS literature review lookup."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 5
    assert principles == ALPHAALGO_301_400_PRINCIPLES

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")

    assert review["domain"] == "Active Inference"
    assert review["reviewed_citations_count"] == 5
    assert review["matched_principles_count"] >= 1
    assert len(review["synthesized_trends"]) == 4


def test_learnable_routing_gate_dispatcher_efe():
    """Tests Expected Free Energy (EFE) task routing and budget bounds in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(
        agent_id="agent_active_inf",
        domain_specialty="Active Inference",
        cost_per_token=0.001,
        historical_success_rate=0.9,
        epistemic_curiosity=0.8
    )
    agent_b = SpecializedAgentProfile(
        agent_id="agent_general",
        domain_specialty="General",
        cost_per_token=0.0001,
        historical_success_rate=0.6,
        epistemic_curiosity=0.2
    )

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    selected = dispatcher.route_task(task_complexity=100.0, domain="Active Inference")
    assert selected == "agent_active_inf"

    dispatcher.update_routing_parameters("agent_active_inf", success=True, cost_incurred=0.1)
    assert dispatcher.budget_spent == 0.1
    assert agent_a.historical_success_rate > 0.9


def test_code_rewrite_engine_ast_verification(tmp_path):
    """Tests AST syntax verification and security checks in CodeRewriteEngine."""
    engine = CodeRewriteEngine(allowed_paths=[str(tmp_path)])

    target_file = tmp_path / "sample.py"
    target_file.write_text("def run():\n    return 42\n")

    proposal = engine.propose_rewrite(
        filepath=str(target_file),
        original_snippet="return 42",
        proposed_snippet="return 100",
        rationale="Upgrade return value."
    )

    assert engine.verify_proposal_ast(proposal) is True
    assert engine.commit_rewrite(proposal) is True
    assert "return 100" in target_file.read_text()


def test_sft_preference_collector_advantages():
    """Tests on-policy advantage estimation and preference pair distillation."""
    collector = SFTPreferenceCollector(discount_factor=0.9)

    steps_a = [
        TrajectoryStep(action="plan", predicted_expectation=1.0, actual_outcome=2.0, reward=2.0),
        TrajectoryStep(action="execute", predicted_expectation=1.5, actual_outcome=3.0, reward=3.0)
    ]
    steps_b = [
        TrajectoryStep(action="plan_err", predicted_expectation=1.0, actual_outcome=0.0, reward=0.0),
        TrajectoryStep(action="fail", predicted_expectation=1.0, actual_outcome=-1.0, reward=-1.0)
    ]

    pair = collector.compile_dpo_preference_pair(
        prompt="Solve task X",
        steps_run_a=steps_a,
        steps_run_b=steps_b
    )

    assert pair["prompt"] == "Solve task X"
    assert "plan, execute" in pair["chosen"]
    assert pair["margin"] > 0.0


def test_cognitive_brain_pydantic_v2_config():
    """Verifies CognitiveBrain model configuration under Pydantic V2."""
    brain = CognitiveBrain()
    assert brain.model_config.get("arbitrary_types_allowed") is True
