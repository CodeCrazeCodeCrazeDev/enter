"""Statistical validation layer for AlphaAlgo Research OS.

Implements multiple testing corrections, Deflated Sharpe Ratio (DSR),
walk-forward splits, and block bootstrapping.
"""
from __future__ import annotations

import math
from typing import List, Tuple, Union
import numpy as np


def adjust_p_values(p_values: List[float], method: str = "HOLM") -> List[float]:
    """Adjust p-values for multiple hypothesis testing.

    Supported methods:
    - "BONFERRONI": Strict Family-Wise Error Rate (FWER) control.
    - "HOLM": Holm-Bonferroni step-down correction.
    - "BH": Benjamini-Hochberg False Discovery Rate (FDR) control.
    """
    n = len(p_values)
    if n == 0:
        return []

    method = method.upper()
    if method == "BONFERRONI":
        return [min(1.0, p * n) for p in p_values]

    elif method == "HOLM":
        # Sort and track indices
        indexed_p = sorted(enumerate(p_values), key=lambda x: x[1])
        adjusted = [0.0] * n
        running_max = 0.0
        for rank, (orig_idx, p) in enumerate(indexed_p):
            # Holm-Bonferroni multiplier: N - rank
            multiplier = n - rank
            adj_p = min(1.0, p * multiplier)
            running_max = max(running_max, adj_p)
            adjusted[orig_idx] = running_max
        return adjusted

    elif method == "BH":
        # Benjamini-Hochberg
        indexed_p = sorted(enumerate(p_values), key=lambda x: x[1])
        adjusted = [0.0] * n
        # Work backward from largest p-value
        running_min = 1.0
        for rank_idx, (orig_idx, p) in reversed(list(enumerate(indexed_p))):
            rank = rank_idx + 1
            adj_p = (p * n) / rank
            running_min = min(running_min, adj_p)
            adjusted[orig_idx] = running_min
        return [min(1.0, p) for p in adjusted]

    else:
        raise ValueError(f"Unknown multiple-testing adjustment method: {method}")


def standard_normal_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def standard_normal_ppf(p: float) -> float:
    """Standard normal inverse cumulative distribution function (approximation)."""
    # Winitzki approximation for inverse error function
    if p <= 0.0 or p >= 1.0:
        raise ValueError("Probability must be strictly between 0 and 1.")

    # Map to [-1, 1] range for erf_inv
    y = 2.0 * p - 1.0
    a = 0.147
    if y == 0.0:
        return 0.0

    # Calculate approximation for erf_inv with boundary hardening
    arg = max(1e-15, 1.0 - y**2)
    term1 = 2.0 / (math.pi * a) + math.log(arg) / 2.0
    term2 = math.log(arg) / a
    inner = term1**2 - term2
    if inner < 0:
        inner = 0
    erf_inv_val = math.copysign(math.sqrt(math.sqrt(inner) - term1), y)
    return math.sqrt(2.0) * erf_inv_val


def calculate_dsr(
    sharpe: float,
    trials: int,
    returns_length: int,
    skewness: float = 0.0,
    kurtosis: float = 3.0,
    trials_variance: float = 0.1,
) -> float:
    """Compute Marcos López de Prado's Deflated Sharpe Ratio (DSR).

    Args:
        sharpe: Estimated annualized Sharpe Ratio.
        trials: Total number of trials (N) performed during research.
        returns_length: Number of returns observations (T).
        skewness: Skewness of returns (defaults to 0 for normal distribution).
        kurtosis: Kurtosis of returns (defaults to 3 for normal distribution).
        trials_variance: Variance of Sharpe Ratios across all executed trials.
    """
    if trials <= 1:
        return 1.0  # If only one trial was run, no deflation is needed

    # Euler-Mascheroni constant
    euler_gamma = 0.5772156649

    # Approximate expected maximum Sharpe Ratio (SR_0) across N trials
    # under the null hypothesis (true SR = 0)
    try:
        z_n = standard_normal_ppf(1.0 - 1.0 / trials)
        z_n_e = standard_normal_ppf(1.0 - 1.0 / (trials * math.e))
    except (ValueError, ZeroDivisionError):
        # Fallback if trials is extremely large or calculation overflows
        z_n = math.sqrt(2.0 * math.log(trials))
        z_n_e = math.sqrt(2.0 * math.log(trials / math.e))

    # Expected maximum Sharpe Ratio under null
    sr_0 = math.sqrt(trials_variance) * ((1.0 - euler_gamma) * z_n + euler_gamma * z_n_e)

    # Standard deviation of the estimated Sharpe Ratio (under non-normality)
    # Annualized Sharpe to daily Sharpe scale (approx) for standard error
    sr_daily = sharpe / math.sqrt(252.0)

    # Variance of estimated daily Sharpe ratio
    # Guard against division by zero for returns series of length 1 or less
    denom = max(1, returns_length - 1)
    var_sr_daily = (1.0 - skewness * sr_daily + (kurtosis - 1.0) / 4.0 * sr_daily**2) / denom
    std_sr_daily = math.sqrt(max(1e-12, var_sr_daily))

    # Scale standard error back to annualized
    std_sr_annual = std_sr_daily * math.sqrt(252.0)

    # Compute Z-score for deflation
    z_score = (sharpe - sr_0) / std_sr_annual

    # Return cumulative probability (DSR value)
    return standard_normal_cdf(z_score)


def walk_forward_split(
    total_length: int,
    train_size: int,
    test_size: int,
    step_size: int,
    rolling: bool = False,
) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Generate train/test bounds for walk-forward validation.

    Args:
        total_length: Total number of observations in dataset.
        train_size: Number of observations for initial training window.
        test_size: Number of observations for test (evaluation) window.
        step_size: Number of observations to advance in each step.
        rolling: If True, uses rolling-window (fixed train size).
                 If False, uses expanding-window (train window starts at 0 and grows).

    Returns:
        List of tuples: ((train_start, train_end), (test_start, test_end))
    """
    splits = []
    current_test_start = train_size

    while current_test_start + test_size <= total_length:
        train_start = 0 if not rolling else (current_test_start - train_size)
        train_end = current_test_start
        test_start = current_test_start
        test_end = current_test_start + test_size

        splits.append(((train_start, train_end), (test_start, test_end)))
        current_test_start += step_size

    return splits


def block_bootstrap(
    returns: Union[List[float], np.ndarray],
    block_size: int = 10,
    num_samples: int = 1000,
    seed: int = 42,
) -> List[float]:
    """Perform Stationary/Moving Block Bootstrap to compute resampled Sharpe Ratios.

    Preserves temporal dependencies (autocorrelation) in financial returns.
    """
    rng = np.random.default_rng(seed)
    ret_arr = np.asarray(returns)
    n = len(ret_arr)
    if n <= block_size:
        # Fallback to standard bootstrap if data is too short
        block_size = max(1, n // 2)

    bootstrapped_sharpes = []

    for _ in range(num_samples):
        resampled = []
        while len(resampled) < n:
            # Randomly select a start index for the block
            start_idx = rng.integers(0, n - block_size + 1)
            block = ret_arr[start_idx : start_idx + block_size]
            resampled.extend(block)

        # Trim to exactly original size
        resampled_arr = np.array(resampled[:n])
        mean_ret = np.mean(resampled_arr)
        std_ret = np.std(resampled_arr, ddof=1)

        if std_ret > 1e-8:
            # Annualized Sharpe Ratio assuming daily returns (252)
            sh = (mean_ret / std_ret) * math.sqrt(252.0)
        else:
            sh = 0.0
        bootstrapped_sharpes.append(sh)

    return bootstrapped_sharpes
