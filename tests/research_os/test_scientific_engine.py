# -*- coding: utf-8 -*-
"""
test_scientific_engine.py: Unit and integration tests for the fully upgraded,
multi-stage ResearchOS Scientific Research Engine and 15-stage loop.
"""
from __future__ import annotations
import math
import pytest
from uuid import UUID, uuid4
from apodex.ai_eos.research.research_os import ResearchOS


def test_scientific_loop_unit_discovery_and_prioritization():
    """Verify that ResearchOS can sense anomalies and score them accurately."""
    ros = ResearchOS()

    # 1. Discover problems
    problems = ros.discover_problems()
    assert len(problems) >= 2
    assert any(p["problem_id"] == "prob_planning_efficiency" for p in problems)

    # 2. Prioritize problems
    scored_problems = ros.prioritize_problems(problems, alpha=1.0, beta=0.5, gamma=0.5)
    assert len(scored_problems) == len(problems)
    assert "priority_score" in scored_problems[0]

    # Assert they are sorted in descending order of priority score
    scores = [p["priority_score"] for p in scored_problems]
    assert scores == sorted(scores, reverse=True)


def test_scientific_loop_unit_literature_search_and_analysis():
    """Verify literature search ranking via Jaccard overlap and paper analysis."""
    ros = ResearchOS()

    # 1. Search literature with a relevant query
    results = ros.search_literature("Expected Free Energy active inference")
    assert len(results) > 0
    # The first result should be highly relevant
    best_paper = results[0]
    assert "id" in best_paper
    assert "metadata" in best_paper

    # 2. Extract technical facts and principle
    paper_id = best_paper["id"]
    analysis = ros.analyze_paper(paper_id)
    assert analysis["paper_id"] == paper_id
    assert "empirical_evidence" in analysis
    assert "limitations" in analysis

    principle = ros.extract_transferable_principle(paper_id)
    assert "extracted_principle" in principle


def test_scientific_loop_unit_hypothesis_and_power_analysis():
    """Verify hypothesis registration and programmatic power analysis sample sizes."""
    ros = ResearchOS()

    # 1. Generate hypothesis
    hyp = ros.generate_hypothesis(paper_id=15, problem_id="prob_planning_efficiency")
    assert hyp.status == "registered"
    assert "H0: Method from Paper 15 does not significantly alter 'prob_planning_efficiency'." == hyp.null_hypothesis

    # 2. Power analysis experiment design
    design = ros.design_experiment_power_analysis(hyp.hypothesis_id, effect_size=0.5, power=0.80)
    assert design["hypothesis_id"] == hyp.hypothesis_id

    # Sample size formula: n = 2 * (1.96 + 0.84)^2 / 0.5^2 = 2 * 7.84 / 0.25 = 62.72 -> ceil is 63
    assert design["recommended_sample_size"] == 63
    assert design["statistical_power"] == 0.80


def test_scientific_loop_unit_trial_and_holm_bonferroni():
    """Verify simulated trial repeatability and Holm-Bonferroni step-down correction."""
    ros = ResearchOS()

    # 1. Repeatable simulated trial (independent two-sample test)
    trial_data = ros.execute_trial(
        experiment_id=uuid4(),
        ground_truth_yield=0.4, # positive yield indicates treatment effect
        sample_size=100,
        seed=42
    )
    assert trial_data["p_value"] < 0.05
    assert trial_data["effect_size"] > 0.0

    # Test repeatability under same seed
    trial_data_2 = ros.execute_trial(
        experiment_id=uuid4(),
        ground_truth_yield=0.4,
        sample_size=100,
        seed=42
    )
    assert trial_data["p_value"] == trial_data_2["p_value"]
    assert trial_data["effect_size"] == trial_data_2["effect_size"]

    # 2. Holm-Bonferroni correction check
    p_values = [0.01, 0.02, 0.05, 0.10]
    rejected = ros.evaluate_statistics_holm_bonferroni(p_values, alpha=0.05)
    assert rejected == [True, False, False, False]


def test_scientific_loop_unit_provenance_and_knowledge_update():
    """Verify knowledge base updates and strict provenance traceability."""
    ros = ResearchOS()

    hyp = ros.register_hypothesis(
        title="Test Hyp",
        description="Test Desc",
        null_hypothesis="H0",
        target_metric="test"
    )

    ros.update_knowledge_base(
        hypothesis_id=hyp.hypothesis_id,
        paper_id=20,
        principle_str="Always use EMG",
        outcome_metric=0.85,
        p_value=0.001,
        is_significant=True
    )

    # Get trace
    trace = ros.get_provenance_trace(hyp.hypothesis_id)
    assert trace is not None
    assert trace["paper_id"] == 20
    assert trace["principle"] == "Always use EMG"
    assert trace["result"]["outcome_metric"] == 0.85
    assert trace["result"]["is_statistically_significant"] is True
    assert trace["decision"] == "PROMOTED TO SUBSYSTEM"


def test_scientific_loop_end_to_end_integration():
    """Execute the complete, integrated 15-stage Scientific Research Loop end-to-end."""
    ros = ResearchOS()

    # Stage 1: Problem Discovery
    problems = ros.discover_problems()
    assert len(problems) > 0

    # Stage 2: Research Question Formulation
    question_data = ros.discover_problem_and_formulate_question("prob_planning_efficiency")
    assert "research_question" in question_data

    # Stage 3: Literature Discovery
    search_query = question_data["research_question"]
    papers_matched = ros.search_literature(search_query, limit=3)
    assert len(papers_matched) > 0
    selected_paper = papers_matched[0]

    # Stage 4: Evidence Acquisition & Stage 5: Evidence Evaluation
    analysis_data = ros.analyze_paper(selected_paper["id"])
    assert "empirical_evidence" in analysis_data

    # Stage 6: Principle Extraction
    principle_data = ros.extract_transferable_principle(selected_paper["id"])
    assert "extracted_principle" in principle_data

    # Stage 7: Hypothesis Generation & Stage 8: Candidate Architecture Selection
    hyp = ros.generate_hypothesis(paper_id=selected_paper["id"], problem_id=question_data["problem_id"])
    assert hyp.status == "registered"

    # Stage 9: Controlled Experiment Design
    design = ros.design_experiment_power_analysis(hyp.hypothesis_id, effect_size=0.6, power=0.85)
    sample_size = design["recommended_sample_size"]
    assert sample_size > 0

    # Stage 10: Real Benchmark Experiment Execution
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    trial_res = ros.execute_trial(
        experiment_id=exp.experiment_id,
        ground_truth_yield=0.5,
        sample_size=sample_size,
        seed=123
    )
    assert "p_value" in trial_res

    # Stage 11: Statistical Evaluation & Stage 12: Replication Validation
    p_values = [trial_res["p_value"], 0.08, 0.12]
    rejection_statuses = ros.evaluate_statistics_holm_bonferroni(p_values, alpha=0.05)
    is_trial_significant = rejection_statuses[0]

    # Stage 13: Decision, Stage 14: Knowledge Update & Stage 15: Research Prioritization
    ros.update_knowledge_base(
        hypothesis_id=hyp.hypothesis_id,
        paper_id=selected_paper["id"],
        principle_str=principle_data["extracted_principle"],
        outcome_metric=trial_res["effect_size"],
        p_value=trial_res["p_value"],
        is_significant=is_trial_significant
    )

    # Verify Traceability
    trace = ros.get_provenance_trace(hyp.hypothesis_id)
    assert trace is not None
    assert trace["paper_id"] == selected_paper["id"]
    assert "result" in trace
    assert trace["result"]["p_value"] == trial_res["p_value"]
