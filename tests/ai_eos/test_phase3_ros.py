"""Unit tests for Phase 3 Research Operating System (ROS) scientific features."""

import pytest
from uuid import uuid4
from apodex.ai_eos.research.research_os import ResearchOS


def test_blended_discovery_mathematics():
    """Verify that opportunity priority is computed correctly using the blended objective."""
    ros = ResearchOS()

    # Priority = alpha * E[commercial] + beta * ExpectedInformationGain + gamma * OptionValue
    # In Tier 1: alpha = 1.0, beta = 0.1, gamma = 0.1
    p1 = ros.score_opportunity(
        commercial_value=100.0,
        expected_info_gain=10.0,
        option_value=5.0,
        alpha=1.0,
        beta=0.1,
        gamma=0.1
    )
    # p1 = 100.0 + 1.0 + 0.5 = 101.5
    assert p1 == pytest.approx(101.5)

    # In Tier 3: alpha = 0.5, beta = 2.0, gamma = 1.5 (exploration-focused)
    p3 = ros.score_opportunity(
        commercial_value=100.0,
        expected_info_gain=10.0,
        option_value=5.0,
        alpha=0.5,
        beta=2.0,
        gamma=1.5
    )
    # p3 = 50.0 + 20.0 + 7.5 = 77.5
    assert p3 == pytest.approx(77.5)


def test_autonomous_science_engine_features():
    """Verify literature synthesis, power analysis experimental design, and critiques."""
    ros = ResearchOS()

    # 1. Literature review
    review = ros.conduct_literature_review("reinforcement_learning")
    assert review["domain"] == "reinforcement_learning"
    assert len(review["synthesized_trends"]) >= 2
    assert "whitespace_found" in review

    # 2. Experimental design
    hyp = ros.register_hypothesis(
        title="Conversion Optimization",
        description="Fewer clicks yields higher conversion",
        null_hypothesis="H0: Clicks do not yield conversion boost",
        target_metric="conversion"
    )
    design = ros.design_experiment(hyp.hypothesis_id)
    assert design["hypothesis_id"] == hyp.hypothesis_id
    assert design["recommended_sample_size"] > 0
    assert design["statistical_power"] == 0.80

    # 3. Methodology critique
    critique_clean = ros.critique_methodology(errors_encountered=0)
    assert critique_clean["needs_refinement"] is False

    critique_faulty = ros.critique_methodology(errors_encountered=5)
    assert critique_faulty["needs_refinement"] is True
    assert "Propose increasing the real pilot weight" in critique_faulty["critique"]
