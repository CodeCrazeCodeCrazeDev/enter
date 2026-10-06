# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite verifying the 200-paper corpus (IDs 301-500),
zero duplicate title/DOI overlap, Research OS principle registration and querying, runtime component
enhancements across AEAN, EOS, EIOS, and Research OS, and cross-layer state handoffs via ResearchToSystemBridge.
"""

from __future__ import annotations
import os
import yaml
import pytest
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    ResearchToSystemBridge,
    ProgramGenome,
    TrajectoryStep,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel


def test_500_paper_corpus_zero_overlap() -> None:
    """Verifies that all 500 research papers across YAML databases have zero title/DOI overlap."""
    db_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    ]

    all_papers = []
    all_titles = []
    all_dois = []

    for path in db_paths:
        assert os.path.exists(path), f"Corpus YAML file missing: {path}"
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            papers = data.get("papers", [])
            assert len(papers) > 0, f"No papers found in {path}"
            all_papers.extend(papers)

    assert len(all_papers) == 500, f"Expected exactly 500 papers across corpus, found {len(all_papers)}"

    # Perform strict duplicate check
    for p in all_papers:
        title = (p.get("metadata", {}).get("title") or p.get("title")).lower()
        doi = p.get("metadata", {}).get("doi") or p.get("doi")

        assert title not in all_titles, f"Duplicate title detected in corpus: '{title}'"
        if doi:
            assert doi not in all_dois, f"Duplicate DOI detected in corpus: '{doi}'"
            all_dois.append(doi)

        all_titles.append(title)


def test_research_os_200_paper_principle_registration_and_review() -> None:
    """Verifies principle registration and multi-field literature review querying in Research OS."""
    principles = register_200_paper_corpus_principles()
    assert len(principles) >= 6

    ros = ResearchOS()

    # Literature review query by category
    review_ai = ros.conduct_literature_review("Active Inference")
    assert review_ai["domain"] == "Active Inference"
    assert review_ai["reviewed_citations_count"] >= 1
    assert any("dirichlet" in t.lower() or "active inference" in t.lower() for t in review_ai["synthesized_trends"])

    # Literature review query by target subsystem
    review_eos = ros.conduct_literature_review("EOS")
    assert review_eos["reviewed_citations_count"] >= 1


def test_runtime_components_200_paper_principles() -> None:
    """Verifies runtime enhancements across CodeRewriteEngine, GeneticWorkflowOptimizer, and LearnableRoutingGateDispatcher."""
    # 1. CodeRewriteEngine Hawkes non-Gaussian call depth check
    engine = CodeRewriteEngine(allowed_paths=[os.getcwd()])
    recursive_code = """
def bad_recursion(n):
    if n <= 0: return 0
    return bad_recursion(n-1) + bad_recursion(n-2) + bad_recursion(n-3) + bad_recursion(n-4)
"""
    prop_bad = engine.propose_rewrite(".", "orig", recursive_code, "Unbounded recursive call")
    assert engine.verify_proposal_ast(prop_bad) is False

    clean_code = """
def clean_fn(n):
    return n * 2
"""
    prop_clean = engine.propose_rewrite(".", "orig", clean_code, "Safe function")
    assert engine.verify_proposal_ast(prop_clean) is True

    # 2. GeneticWorkflowOptimizer MAP-Elites boolean parameter mutation
    optimizer = GeneticWorkflowOptimizer(population_size=4, mutation_rate=1.0)
    optimizer.initialize_population("Base prompt template", {"is_active": True, "learning_rate": 0.05})
    assert len(optimizer.population) == 4
    # Boolean parameter was correctly mutated without type error
    assert isinstance(optimizer.population[1].parameters["is_active"], bool)

    # 3. LearnableRoutingGateDispatcher EFE Routing
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=2.0)
    agent = SpecializedAgentProfile(
        agent_id="agent_1",
        domain_specialty="EIOS",
        cost_per_token=0.002,
        historical_success_rate=0.8,
        epistemic_curiosity=0.7
    )
    dispatcher.register_subagent(agent)
    selected = dispatcher.route_task(task_complexity=10, domain="EIOS")
    assert selected == "agent_1"


def test_cross_layer_active_inference_bridge() -> None:
    """Verifies end-to-end active inference state handoffs via ResearchToSystemBridge."""
    ros = ResearchOS()
    eios = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind(token_budget=500)
    wm = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=eios,
        eos_engine=eos,
        hive_mind=hive,
        world_model=wm
    )

    # Register and validate hypothesis in Research OS
    hyp = ros.register_hypothesis(
        title="Dirichlet Epistemic Surprise Bounds",
        description="EFE precision weighting minimizes active sensing variance.",
        null_hypothesis="No variance reduction.",
        target_metric="FreeEnergy"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert hyp.status == "validated"

    # Execute cross-layer bridge handoff
    handoff_results = bridge.bridge_validated_hypothesis(hyp.hypothesis_id)

    assert handoff_results["hypothesis_id"] == str(hyp.hypothesis_id)
    assert "L2_EIOS_Kernel" in handoff_results["layer_handoffs"]
    assert "L2_EOS_Engine" in handoff_results["layer_handoffs"]
    assert "L3_AEAN_HiveMind" in handoff_results["layer_handoffs"]
    assert "L4_APODEX_WorldModel" in handoff_results["layer_handoffs"]

    # Verify state updates across layers
    assert len(eios.registered_hypotheses) == 1
    assert len(eos.active_hypotheses) == 1
    assert len(hive.registered_insights) == 1
    assert len(wm.beliefs) == 1

    # Verify AEAN HiveMind synergy evaluation
    bids = [
        TaskBid(task="task_1", priority=0.9, expected_value=0.8, token_cost=10),
        TaskBid(task="task_2", priority=0.7, expected_value=0.6, token_cost=15)
    ]
    synergy = hive.evaluate_synergy(bids)
    assert synergy > 0.0
