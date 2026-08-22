"""Integration and validation tests for AlphaAlgo 100-paper research corpus and extracted principles."""

import os
import math
import pytest
import yaml

from apodex.research_os.statistical_validation import (
    adjust_p_values,
    calculate_dsr,
    standard_normal_cdf,
    standard_normal_ppf,
)


def test_alpha_algo_100_paper_uniqueness():
    """Verify that the 100 AlphaAlgo papers (IDs 201-300) have zero overlap with the 200 baseline papers."""
    db1_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    db2_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"

    assert os.path.exists(db1_path), f"Base DB {db1_path} not found"
    assert os.path.exists(db2_path), f"AlphaAlgo DB {db2_path} not found"

    with open(db1_path, "r", encoding="utf-8") as f:
        db1 = yaml.safe_load(f)
    with open(db2_path, "r", encoding="utf-8") as f:
        db2 = yaml.safe_load(f)

    p1 = db1["papers"]
    p2 = db2["papers"]

    assert len(p1) == 200, f"Expected 200 papers in base DB, got {len(p1)}"
    assert len(p2) == 100, f"Expected 100 papers in AlphaAlgo DB, got {len(p2)}"

    ids1 = {p["id"] for p in p1}
    ids2 = {p["id"] for p in p2}
    assert len(ids1.intersection(ids2)) == 0, "ID overlap detected between DB1 and DB2"

    titles1 = {p["metadata"]["title"].strip().lower() for p in p1}
    titles2 = {p["metadata"]["title"].strip().lower() for p in p2}
    title_overlap = titles1.intersection(titles2)
    assert len(title_overlap) == 0, f"Title overlap detected: {title_overlap}"

    dois1 = {p["metadata"].get("doi") for p in p1 if p["metadata"].get("doi")}
    dois2 = {p["metadata"].get("doi") for p in p2 if p["metadata"].get("doi")}
    doi_overlap = dois1.intersection(dois2)
    assert len(doi_overlap) == 0, f"DOI overlap detected: {doi_overlap}"


def test_standard_normal_cdf_accuracy():
    """Verify exact standard normal CDF calculation using math.erf."""
    assert abs(standard_normal_cdf(0.0) - 0.5) < 1e-7
    assert abs(standard_normal_cdf(1.959963984540054) - 0.975) < 1e-4
    assert standard_normal_cdf(3.0) > 0.998
    assert standard_normal_cdf(-3.0) < 0.002


def test_standard_normal_ppf_bounds_clamping():
    """Verify safe standard normal inverse cumulative function handling boundary values without raising math domain error."""
    assert abs(standard_normal_ppf(0.5) - 0.0) < 1e-5
    assert standard_normal_ppf(0.975) > 1.9

    with pytest.raises(ValueError):
        standard_normal_ppf(0.0)

    with pytest.raises(ValueError):
        standard_normal_ppf(1.0)

    # Edge probabilities near bounds
    p_high = 0.9999999999
    p_low = 1e-10
    val_high = standard_normal_ppf(p_high)
    val_low = standard_normal_ppf(p_low)
    assert not math.isnan(val_high) and not math.isinf(val_high)
    assert not math.isnan(val_low) and not math.isinf(val_low)


def test_calculate_dsr_zero_and_short_returns():
    """Verify calculate_dsr handles ultra-short return time series (returns_length <= 1) safely without zero division."""
    dsr_single = calculate_dsr(sharpe=1.5, trials=10, returns_length=1)
    assert 0.0 <= dsr_single <= 1.0

    dsr_zero = calculate_dsr(sharpe=1.5, trials=10, returns_length=0)
    assert 0.0 <= dsr_zero <= 1.0

    dsr_normal = calculate_dsr(sharpe=1.5, trials=10, returns_length=252)
    assert 0.0 <= dsr_normal <= 1.0
