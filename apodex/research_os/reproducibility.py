"""Reproducibility tracking and environment validation for AlphaAlgo Research OS.

Captures system fingerprints, Python configurations, and verifies deterministic
replays of past experiments.
"""
from __future__ import annotations

import os
import platform
import sys
from typing import Any, Dict, List
from .models import Experiment


def capture_environment_fingerprint(seed: int = 42) -> Dict[str, Any]:
    """Capture the exact OS, Python, and package configuration of the current runtime."""
    # Attempt to capture a clean git commit or use environment variable
    git_commit = os.environ.get("ALPHAALGO_GIT_COMMIT", "unknown_dev_commit")

    # Retrieve top package versions that are critical to research reproducibility
    packages = {}
    for pkg in ["numpy", "pandas", "pydantic", "scipy", "torch", "transformers"]:
        try:
            mod = __import__(pkg)
            packages[pkg] = getattr(mod, "__version__", "unknown")
        except ImportError:
            packages[pkg] = "not_installed"

    return {
        "os_platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "cpu_architecture": platform.machine(),
        "git_commit": git_commit,
        "seed": seed,
        "critical_packages": packages,
    }


def verify_reproducibility(
    original: Experiment,
    replayed_returns: List[float],
    replayed_metrics: Dict[str, float],
    tolerance: float = 1e-6,
) -> bool:
    """Compare replayed outcomes with the original registered experiment.

    Verifies that the returns time-series and final Sharpe ratio are within the
    allowable floating-point tolerance limit.
    """
    if original.status != "COMPLETED":
        return False

    orig_returns = original.returns_time_series or []
    rep_returns = replayed_returns or []

    # Check length of returns series
    if len(orig_returns) != len(rep_returns):
        return False

    # Check individual returns values under tolerance
    for orig_r, rep_r in zip(orig_returns, rep_returns):
        try:
            val_orig = float(orig_r)
            val_rep = float(rep_r)
            if abs(val_orig - val_rep) > tolerance:
                return False
        except (ValueError, TypeError):
            return False

    # Compare key metrics
    try:
        orig_sharpe = float(original.metrics.get("sharpe", 0.0))
        rep_sharpe = float(replayed_metrics.get("sharpe", 0.0))
        if abs(orig_sharpe - rep_sharpe) > tolerance:
            return False
    except (ValueError, TypeError):
        return False

    return True
