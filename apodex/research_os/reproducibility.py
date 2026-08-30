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
    git_commit = os.environ.get("ALPHAALGO_GIT_COMMIT", "unknown_dev_commit")

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
    Safe-guards against type mismatched or string metric inputs.
    """
    if original.status != "COMPLETED":
        return False

    if len(original.returns_time_series) != len(replayed_returns):
        return False

    for orig_r, rep_r in zip(original.returns_time_series, replayed_returns):
        if abs(float(orig_r) - float(rep_r)) > tolerance:
            return False

    orig_sharpe_raw = original.metrics.get("sharpe", 0.0)
    rep_sharpe_raw = replayed_metrics.get("sharpe", 0.0)

    try:
        orig_sharpe = float(orig_sharpe_raw) if orig_sharpe_raw is not None else 0.0
        rep_sharpe = float(rep_sharpe_raw) if rep_sharpe_raw is not None else 0.0
    except (TypeError, ValueError):
        return False

    if abs(orig_sharpe - rep_sharpe) > tolerance:
        return False

    return True
