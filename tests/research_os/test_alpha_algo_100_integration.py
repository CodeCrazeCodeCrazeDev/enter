"""Unit and integration tests for AlphaAlgo 100 research papers and statistical validation layer."""
import math
import os
import yaml
import pytest
import numpy as np

from apodex.research_os.statistical_validation import (
    adjust_p_values,
    standard_normal_cdf,
    standard_normal_ppf,
    calculate_dsr,
    walk_forward_split,
    block_bootstrap,
)
from apodex.cognition.brain import CognitiveBrain


def test_alpha_algo_100_yaml_db_integrity():
    """Verify 100 new research papers database schema, completeness, and zero overlap with base DB."""
    new_db_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    base_db_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"

    assert os.path.exists(new_db_path), f"New research DB missing at {new_db_path}"
    assert os.path.exists(base_db_path), f"Base research DB missing at {base_db_path}"

    with open(new_db_path, "r", encoding="utf-8") as f:
        new_data = yaml.safe_load(f)

    with open(base_db_path, "r", encoding="utf-8") as f:
        base_data = yaml.safe_load(f)

    new_papers = new_data.get("papers", [])
    base_papers = base_data.get("papers", [])

    assert len(new_papers) == 100, f"Expected 100 papers in new DB, got {len(new_papers)}"
    assert len(base_papers) == 200, f"Expected 200 papers in base DB, got {len(base_papers)}"

    # Check zero title overlap
    base_titles = {p["metadata"]["title"].lower().strip() for p in base_papers}
    new_titles = [p["metadata"]["title"].lower().strip() for p in new_papers]

    overlaps = [t for t in new_titles if t in base_titles]
    assert len(overlaps) == 0, f"Found title overlaps between DBs: {overlaps}"

    # Check paper ID continuity (IDs 201..300)
    new_ids = [p["id"] for p in new_papers]
    assert min(new_ids) == 201
    assert max(new_ids) == 300
    assert len(set(new_ids)) == 100


def test_standard_normal_cdf_and_ppf():
    """Verify standard normal CDF and inverse cumulative function (PPF)."""
    # Standard normal CDF properties
    assert math.isclose(standard_normal_cdf(0.0), 0.5, abs_tol=1e-5)
    assert standard_normal_cdf(1.96) > 0.97
    assert standard_normal_cdf(-1.96) < 0.03

    # PPF properties and bounds handling
    assert math.isclose(standard_normal_ppf(0.5), 0.0, abs_tol=1e-5)
    assert standard_normal_ppf(0.975) > 1.8
    assert standard_normal_ppf(0.025) < -1.8

    # Edge cases (should be clipped safely without raising exception)
    val_near_zero = standard_normal_ppf(0.0)
    val_near_one = standard_normal_ppf(1.0)
    assert isinstance(val_near_zero, float)
    assert isinstance(val_near_one, float)


def test_multiple_p_value_adjustments():
    """Verify Holm, Bonferroni, and Benjamini-Hochberg p-value adjustments."""
    p_vals = [0.01, 0.04, 0.03, 0.20]

    bonf = adjust_p_values(p_vals, method="BONFERRONI")
    assert bonf == [0.04, 0.16, 0.12, 0.80]

    holm = adjust_p_values(p_vals, method="HOLM")
    assert holm[0] <= holm[2] <= holm[1] <= holm[3]

    bh = adjust_p_values(p_vals, method="BH")
    assert all(bh[i] <= bonf[i] for i in range(len(p_vals)))


def test_deflated_sharpe_ratio():
    """Verify Marcos Lopez de Prado's Deflated Sharpe Ratio calculation."""
    # Single trial -> no deflation
    dsr_single = calculate_dsr(sharpe=2.0, trials=1, returns_length=252)
    assert dsr_single == 1.0

    # Multiple trials -> deflation expected
    dsr_multi = calculate_dsr(sharpe=1.5, trials=100, returns_length=252, trials_variance=0.2)
    assert 0.0 <= dsr_multi <= 1.0

    # Short return length guard test
    dsr_short = calculate_dsr(sharpe=1.0, trials=10, returns_length=1)
    assert isinstance(dsr_short, float)


def test_walk_forward_split_and_bootstrap():
    """Verify walk forward splits and stationary block bootstrap."""
    splits = walk_forward_split(total_length=100, train_size=40, test_size=10, step_size=10)
    assert len(splits) == 6
    assert splits[0] == ((0, 40), (40, 50))
    assert splits[-1] == ((0, 90), (90, 100))

    returns = np.random.normal(0.001, 0.01, 100)
    bootstrapped = block_bootstrap(returns, block_size=10, num_samples=50, seed=42)
    assert len(bootstrapped) == 50


def test_cognitive_brain_instantiation():
    """Verify CognitiveBrain instantiates with Pydantic V2 ConfigDict."""
    brain = CognitiveBrain()
    assert brain is not None
    res = brain.run_strategic_cycle("Test AlphaAlgo Integration")
    assert res["goal"] == "Test AlphaAlgo Integration"
    assert res["plan_length"] == 4
