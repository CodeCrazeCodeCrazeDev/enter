# -*- coding: utf-8 -*-
"""Integration and robustness tests for AlphaAlgo 100 research papers, statistical validation, and reproducibility."""

import os
import math
import pytest
import numpy as np
import yaml
from uuid import uuid4
from apodex.research_os.statistical_validation import (
    adjust_p_values,
    standard_normal_cdf,
    standard_normal_ppf,
    calculate_dsr,
    walk_forward_split,
    block_bootstrap,
)
from apodex.research_os.reproducibility import (
    capture_environment_fingerprint,
    verify_reproducibility,
)
from apodex.research_os.models import Experiment
from apodex.ai_eos.research.integration import (
    register_300_paper_corpus_principles,
    ALPHAALGO_RESEARCH_PRINCIPLES,
)


def test_alphaalgo_100_paper_database_uniqueness_and_integrity():
    """Verify that the 100-paper AlphaAlgo database has 0 title and 0 DOI overlaps against AI_EOS_RESEARCH_DB.yaml."""
    db1_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    db2_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"

    assert os.path.exists(db1_path), "AI_EOS_RESEARCH_DB.yaml missing"
    assert os.path.exists(db2_path), "ALPHA_ALGO_100_NEW_RESEARCH.yaml missing"

    with open(db1_path, "r", encoding="utf-8") as f:
        db1 = yaml.safe_load(f)
    with open(db2_path, "r", encoding="utf-8") as f:
        db2 = yaml.safe_load(f)

    papers1 = db1.get("papers", [])
    papers2 = db2.get("papers", [])

    assert len(papers1) == 200, f"Expected 200 papers in DB1, got {len(papers1)}"
    assert len(papers2) == 100, f"Expected 100 papers in DB2, got {len(papers2)}"

    dois1 = {p["metadata"]["doi"].strip().lower() for p in papers1 if p.get("metadata", {}).get("doi")}
    dois2 = {p["metadata"]["doi"].strip().lower() for p in papers2 if p.get("metadata", {}).get("doi")}
    doi_overlap = dois1.intersection(dois2)
    assert len(doi_overlap) == 0, f"DOI overlap detected: {doi_overlap}"

    titles1 = {p["metadata"]["title"].strip().lower() for p in papers1 if p.get("metadata", {}).get("title")}
    titles2 = {p["metadata"]["title"].strip().lower() for p in papers2 if p.get("metadata", {}).get("title")}
    title_overlap = titles1.intersection(titles2)
    assert len(title_overlap) == 0, f"Title overlap detected: {title_overlap}"

    # Check non-generic technical facts
    for p in papers2:
        assert p["id"] >= 201 and p["id"] <= 300
        problem = p["technical_facts"]["problem"]
        assert "A major unresolved limitation" not in problem, f"Generic placeholder in paper {p['id']}"


def test_statistical_validation_edge_cases():
    """Test standard normal PPF probability clamping and DSR calculations."""
    # Test boundary probabilities for PPF
    assert standard_normal_ppf(0.0) < -6.0
    assert standard_normal_ppf(1.0) > 6.0
    assert math.isclose(standard_normal_ppf(0.5), 0.0, abs_tol=1e-5)

    # DSR single trial should be 1.0
    dsr_single = calculate_dsr(sharpe=1.5, trials=1, returns_length=252)
    assert dsr_single == 1.0

    # DSR with 100 trials and high sharpe
    dsr_high = calculate_dsr(sharpe=2.5, trials=100, returns_length=500, trials_variance=0.2)
    assert 0.0 <= dsr_high <= 1.0

    # DSR with zero or negative variance protection
    dsr_zero_var = calculate_dsr(sharpe=1.0, trials=50, returns_length=252, trials_variance=0.0)
    assert 0.0 <= dsr_zero_var <= 1.0


def test_multiple_testing_adjustments():
    """Test Holm, Bonferroni, and BH adjustments on p-values."""
    p_vals = [0.01, 0.04, 0.03, 0.20]
    adj_bonf = adjust_p_values(p_vals, method="BONFERRONI")
    assert adj_bonf == [0.04, 0.16, 0.12, 0.80]

    adj_holm = adjust_p_values(p_vals, method="HOLM")
    assert all(0.0 <= p <= 1.0 for p in adj_holm)

    adj_bh = adjust_p_values(p_vals, method="BH")
    assert all(0.0 <= p <= 1.0 for p in adj_bh)


def test_block_bootstrap_robustness():
    """Test block bootstrap on empty, single, and normal returns arrays."""
    # Empty array
    boot_empty = block_bootstrap([], block_size=5, num_samples=10)
    assert len(boot_empty) == 10
    assert boot_empty == [0.0] * 10

    # Single return
    boot_single = block_bootstrap([0.05], block_size=5, num_samples=10)
    assert len(boot_single) == 10

    # Normal returns array
    np.random.seed(42)
    returns = np.random.normal(0.001, 0.02, 100)
    boot_res = block_bootstrap(returns, block_size=10, num_samples=50)
    assert len(boot_res) == 50
    assert all(isinstance(x, float) for x in boot_res)


def test_reproducibility_fingerprint_and_verification():
    """Test environment fingerprinting and experiment reproducibility check."""
    fp = capture_environment_fingerprint(seed=123)
    assert fp["seed"] == 123
    assert "os_platform" in fp
    assert "python_version" in fp

    exp = Experiment(
        experiment_id=str(uuid4()),
        hypothesis_id=str(uuid4()),
        dataset_id=str(uuid4()),
        name="AlphaAlgo Test Experiment",
        status="COMPLETED",
        parameters={},
        returns_time_series=[0.01, -0.005, 0.02, 0.015],
        metrics={"sharpe": 1.25},
    )

    # Valid replay
    assert verify_reproducibility(
        original=exp,
        replayed_returns=[0.01, -0.005, 0.02, 0.015],
        replayed_metrics={"sharpe": 1.25},
    )

    # Mismatched returns
    assert not verify_reproducibility(
        original=exp,
        replayed_returns=[0.01, -0.005, 0.02],
        replayed_metrics={"sharpe": 1.25},
    )


def test_corpus_principles_registration():
    """Test memory registration of extracted 300-paper corpus principles."""
    count = register_300_paper_corpus_principles("docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml")
    assert count == 100
    assert len(ALPHAALGO_RESEARCH_PRINCIPLES) >= 100
    assert 201 in ALPHAALGO_RESEARCH_PRINCIPLES
    assert ALPHAALGO_RESEARCH_PRINCIPLES[201]["domain"] == "Quantitative Finance"
