# -*- coding: utf-8 -*-
"""
test_alpha_algo_100_integration.py: Integration test suite for the 100-paper AlphaAlgo quantitative research corpus,
transferable principles, statistical validation fixes, and batch ingestion pipeline.
"""
from __future__ import annotations

import os
import yaml
import pytest
import numpy as np

from apodex.ai_eos.research.integration import register_100_paper_alphaalgo_principles, ALPHAALGO_100_PRINCIPLES
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.research_os.statistical_validation import (
    standard_normal_ppf,
    calculate_dsr,
    walk_forward_split,
    block_bootstrap,
    adjust_p_values
)
from apodex.research_os.research_ingestion import ResearchIngestionPipeline


def test_corpus_uniqueness():
    """Verify zero overlap between AI_EOS 200 papers and AlphaAlgo 100 new papers."""
    db1_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    db2_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"

    assert os.path.exists(db1_path)
    assert os.path.exists(db2_path)

    with open(db1_path, "r", encoding="utf-8") as f:
        db1 = yaml.safe_load(f).get("papers", [])

    with open(db2_path, "r", encoding="utf-8") as f:
        db2 = yaml.safe_load(f).get("papers", [])

    assert len(db1) == 200
    assert len(db2) == 100

    titles1 = {p["metadata"]["title"].strip().lower() for p in db1}
    titles2 = {p["metadata"]["title"].strip().lower() for p in db2}

    overlap = titles1.intersection(titles2)
    assert len(overlap) == 0, f"Found title overlap: {overlap}"


def test_registered_alphaalgo_principles():
    """Verify principles extracted from AlphaAlgo 100-paper corpus."""
    principles = register_100_paper_alphaalgo_principles()
    assert len(principles) >= 5
    assert "DeflatedSharpeRatio" in principles
    assert "WalkForwardValidation" in principles
    assert "StationaryBlockBootstrap" in principles
    assert "MultipleTestingCorrections" in principles
    assert "ProbabilityClamping" in principles


def test_research_os_literature_review_alphaalgo():
    """Verify ResearchOS literature review returns quantitative AlphaAlgo principles."""
    ros = ResearchOS()
    review = ros.conduct_literature_review("Quantitative Finance")

    assert review["domain"] == "Quantitative Finance"
    assert review["reviewed_citations_count"] == 100
    assert len(review["matching_alphaalgo_principles"]) >= 5


def test_statistical_validation_edge_cases():
    """Verify fixes for mathematical edge cases in statistical validation module."""
    # 1. Probability clamping at 0 and 1 boundaries
    ppf_zero = standard_normal_ppf(0.0)
    ppf_one = standard_normal_ppf(1.0)
    assert ppf_zero < -5.0
    assert ppf_one > 5.0

    # 2. Deflated Sharpe Ratio calculation
    dsr = calculate_dsr(sharpe=1.5, trials=50, returns_length=500, trials_variance=0.05)
    assert 0.0 <= dsr <= 1.0

    # 3. Single trial DSR fallback
    dsr_single = calculate_dsr(sharpe=1.5, trials=1, returns_length=500)
    assert dsr_single == 1.0

    # 4. Walk-forward split generation
    splits = walk_forward_split(total_length=100, train_size=50, test_size=10, step_size=10, rolling=True)
    assert len(splits) == 5
    assert splits[0] == ((0, 50), (50, 60))

    # 5. Stationary block bootstrap handling short/empty array
    empty_bs = block_bootstrap([], block_size=5, num_samples=10)
    assert empty_bs == []

    short_bs = block_bootstrap([0.01, -0.02, 0.03], block_size=10, num_samples=50)
    assert len(short_bs) == 50

    # 6. Multiple testing adjustments
    p_vals = [0.01, 0.04, 0.10, 0.20]
    holm = adjust_p_values(p_vals, method="HOLM")
    bh = adjust_p_values(p_vals, method="BH")
    assert len(holm) == 4
    assert len(bh) == 4


def test_research_ingestion_pipeline_batches():
    """Verify batch partitioning and simulation execution in ResearchIngestionPipeline."""
    pipeline = ResearchIngestionPipeline()
    batches = pipeline.get_batches(batch_size=20)
    assert len(batches) == 5

    res = pipeline.run_pipeline()
    assert res["pipeline_status"] == "SUCCESS"
    assert len(res["batches_results"]) == 5
