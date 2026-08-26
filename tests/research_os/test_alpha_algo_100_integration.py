# -*- coding: utf-8 -*-
"""
test_alpha_algo_100_integration.py: Integration test suite for the 100-paper AlphaAlgo research corpus,
transferable principles registration, ResearchOS literature review synthesis, and statistical validation edge cases.
"""

import os
import yaml
import pytest
import numpy as np
from apodex.ai_eos.research.integration import (
    register_100_paper_alphaalgo_principles,
    register_300_paper_corpus_principles,
    ALPHAALGO_100_PRINCIPLES
)
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.research_os.statistical_validation import standard_normal_ppf, calculate_dsr


def test_corpus_uniqueness_and_zero_overlap():
    """Verify zero title and DOI overlap between 200-paper AI_EOS_RESEARCH_DB and 100-paper ALPHA_ALGO_100_NEW_RESEARCH."""
    db1_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    db2_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"

    assert os.path.exists(db1_path), f"Missing {db1_path}"
    assert os.path.exists(db2_path), f"Missing {db2_path}"

    with open(db1_path, "r", encoding="utf-8") as f:
        db1 = yaml.safe_load(f)["papers"]

    with open(db2_path, "r", encoding="utf-8") as f:
        db2 = yaml.safe_load(f)["papers"]

    assert len(db1) == 200, f"Expected 200 papers in db1, got {len(db1)}"
    assert len(db2) == 100, f"Expected 100 papers in db2, got {len(db2)}"

    titles1 = set(p["metadata"]["title"].lower().strip() for p in db1)
    titles2 = set(p["metadata"]["title"].lower().strip() for p in db2)

    overlap_titles = titles1.intersection(titles2)
    assert len(overlap_titles) == 0, f"Detected title overlap between databases: {overlap_titles}"

    dois1 = set(p["metadata"].get("doi", "").lower().strip() for p in db1 if p["metadata"].get("doi"))
    dois2 = set(p["metadata"].get("doi", "").lower().strip() for p in db2 if p["metadata"].get("doi"))

    overlap_dois = dois1.intersection(dois2)
    assert len(overlap_dois) == 0, f"Detected DOI overlap between databases: {overlap_dois}"


def test_principles_registration():
    """Test principles registration functions return valid structures for the 100 and 300 paper corpora."""
    p100 = register_100_paper_alphaalgo_principles()
    assert isinstance(p100, dict)
    assert "Quantitative Finance" in p100
    assert "Active Inference" in p100
    assert "RL & Alignment" in p100

    p300 = register_300_paper_corpus_principles()
    assert p300["core_corpus_count"] == 200
    assert p300["alphaalgo_corpus_count"] == 100
    assert p300["total_corpus_count"] == 300
    assert p300["principles_by_domain"] == ALPHAALGO_100_PRINCIPLES


def test_research_os_dynamic_literature_review():
    """Test ResearchOS.conduct_literature_review dynamically matches domain keywords to extracted principles."""
    ros = ResearchOS()

    # Query domain present in ALPHAALGO_100_PRINCIPLES
    res = ros.conduct_literature_review("Active Inference")
    assert res["domain"] == "Active Inference"
    assert res["reviewed_citations_count"] > 0
    assert len(res["synthesized_trends"]) > 0
    assert any("Expected Free Energy" in trend for trend in res["synthesized_trends"])

    # Query domain matching Market Microstructure
    res_micro = ros.conduct_literature_review("Market Microstructure")
    assert any("Order flow imbalance" in trend for trend in res_micro["synthesized_trends"])


def test_statistical_validation_boundary_clamping():
    """Test standard_normal_ppf boundary clamping handles extreme p values without throwing errors."""
    val_zero = standard_normal_ppf(0.0)
    assert not np.isnan(val_zero) and not np.isinf(val_zero)

    val_one = standard_normal_ppf(1.0)
    assert not np.isnan(val_one) and not np.isinf(val_one)

    val_extreme_low = standard_normal_ppf(-0.5)
    assert not np.isnan(val_extreme_low)

    val_extreme_high = standard_normal_ppf(1.5)
    assert not np.isnan(val_extreme_high)


def test_dsr_zero_variance_protection():
    """Test calculate_dsr handles zero or near-zero trials variance gracefully."""
    dsr_val = calculate_dsr(
        sharpe=1.5,
        trials=100,
        returns_length=252,
        trials_variance=0.0
    )
    assert isinstance(dsr_val, float)
    assert 0.0 <= dsr_val <= 1.0
