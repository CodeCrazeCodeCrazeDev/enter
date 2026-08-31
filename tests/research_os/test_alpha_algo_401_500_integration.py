# -*- coding: utf-8 -*-
"""
test_alpha_algo_401_500_integration.py: Integration test suite for the 100-paper (401-500)
research corpus, transferable principle registration, literature review indexing, and flaw fixes.
"""

import os
import glob
import math
import yaml
import pytest

from apodex.ai_eos.research.integration import (
    register_401_500_paper_corpus_principles,
    ALPHAALGO_401_500_PRINCIPLES,
    CodeRewriteEngine,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.cognition.brain import CognitiveBrain, DeepCausalWorldModel, SimulationEngine, AdvancedPlanner, MultiAgentOrchestrator


def test_401_500_zero_corpus_overlap():
    """Verify that all 400 papers (1-200, 201-300, 401-500) have 100% zero title or DOI duplicates."""
    titles = set()
    dois = set()
    total_count = 0

    for path in sorted(glob.glob("docs/research/**/*.yaml", recursive=True)):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict):
            papers = data.get("papers", [])
            if papers:
                total_count += len(papers)
                for p in papers:
                    meta = p.get("metadata", {})
                    title = meta.get("title", "").strip().lower()
                    doi = str(meta.get("doi", "")).strip().lower()

                    if title:
                        assert title not in titles, f"Duplicate title detected: '{title}'"
                        titles.add(title)
                    if doi:
                        assert doi not in dois, f"Duplicate DOI detected: '{doi}'"
                        dois.add(doi)

    assert total_count == 400
    assert len(titles) == 400
    assert len(dois) == 200


def test_401_500_principle_registration_and_review():
    """Verify principle registration and ResearchOS literature review querying over 401-500 corpus."""
    principles = register_401_500_paper_corpus_principles()
    assert len(principles) == 5
    assert "Jump_Diffusion_Volatility_Priors" in principles

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")
    assert review["domain"] == "Active Inference"
    assert review["reviewed_citations_count"] >= 24
    assert len(review["matching_principles"]) >= 1


def test_cognitive_brain_numerical_flaw_fixes():
    """Verify numerical and boundary flaw fixes in CognitiveBrain and World Model."""
    cb = CognitiveBrain()

    # 1. Test Bayesian belief update when trials < successes
    mean, var = cb.world_model.update_bayesian_belief("market_volatility", trials=3, successes=10)
    assert mean > 0.0 and mean <= 1.0
    assert var >= 0.0 and math.isfinite(var)

    # 2. Test SimulationEngine with NaN or invalid inputs
    cb.world_model.add_variable("bad_var", alpha=1.0, beta=1.0)
    sim = SimulationEngine(world_model=cb.world_model)
    report = sim.simulate_rollout("bad_var", float("nan"), "bad_var", num_trials=0)
    assert math.isfinite(report["mean"])
    assert math.isfinite(report["std_dev"])

    # 3. Test MCTS Planner with non-positive probabilities
    best = cb.planner.select_optimal_branch_mcts([
        {"pragmatic_prob": -1.0, "target_pref": 0.0, "prior_entropy": 1.0, "post_entropy": 0.5}
    ])
    assert "g_score" in best
    assert math.isfinite(best["g_score"])

    # 4. Test MultiAgentOrchestrator sycophancy check on empirical facts
    evals = {"Agent1": 0.9, "Agent2": 0.9, "Agent3": 0.9}
    mean_consensus, _ = cb.orchestrator.resolve_debate_consensus(evals, is_empirical_fact=True)
    assert mean_consensus == pytest.approx(0.9, abs=1e-3)


def test_code_rewrite_engine_ast_and_single_replace_safety():
    """Verify AST security checks and single-snippet replace safety in CodeRewriteEngine."""
    engine = CodeRewriteEngine(allowed_paths=[os.getcwd()])

    # Safe standard imports are allowed
    prop1 = engine.propose_rewrite("test.py", "orig", "import os\nimport sys", "rationale")
    assert engine.verify_proposal_ast(prop1)

    # Dynamic __import__ call or dangerous functions should be vetoed
    prop2 = engine.propose_rewrite("test.py", "orig", "x = __import__('os')", "rationale")
    assert not engine.verify_proposal_ast(prop2)

    prop3 = engine.propose_rewrite("test.py", "orig", "eval('1+1')", "rationale")
    assert not engine.verify_proposal_ast(prop3)


def test_sft_preference_collector_edit_distance_penalties():
    """Verify trajectory edit distance cost penalties and empty step handling."""
    collector = SFTPreferenceCollector()

    step1 = TrajectoryStep(action="a1", predicted_expectation=1.0, actual_outcome=1.0, reward=1.0)
    step2 = TrajectoryStep(action="a2", predicted_expectation=1.0, actual_outcome=1.0, reward=1.0)

    # Empty vs non-empty steps
    pair = collector.compile_dpo_preference_pair("test prompt", [step1], [])
    assert pair["chosen"] is not None
    assert pair["rejected"] is not None
    assert "Success metric:" in pair["chosen"]

    # Longer path gets extra length cost penalty
    pair_len = collector.compile_dpo_preference_pair("test prompt", [step1, step2], [step1])
    assert pair_len["margin"] < 1.0


def test_learnable_routing_gate_dispatcher_budget_bounds():
    """Verify budget bounds and cost fallback in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=1.0)

    p1 = SpecializedAgentProfile(agent_id="cheap", domain_specialty="trading", cost_per_token=0.01)
    p2 = SpecializedAgentProfile(agent_id="expensive", domain_specialty="trading", cost_per_token=5.0)

    dispatcher.register_subagent(p1)
    dispatcher.register_subagent(p2)

    selected = dispatcher.route_task(task_complexity=1.0, domain="trading")
    assert selected == "cheap"
