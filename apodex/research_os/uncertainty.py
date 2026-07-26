from __future__ import annotations
import math
import time
from typing import Any, Dict

# =====================================================================
# Bayesian Belief Engine & Uncertainty Framework
# =====================================================================

def update_belief(
    current_alpha: float,
    current_beta: float,
    evidence_support: float,  # weight of supporting evidence [0.0, 1.0]
    evidence_conflict: float, # weight of conflicting/falsifying evidence [0.0, 1.0]
    evidence_reliability: float = 1.0  # source reliability multiplier [0.0, 1.0]
) -> tuple[float, float]:
    """
    Performs conjugate Bayesian updating over Beta priors/posteriors.
    Incorporates source reliability scale to discount uncertain evidence.
    """
    updated_alpha = current_alpha + (evidence_support * evidence_reliability)
    updated_beta = current_beta + (evidence_conflict * evidence_reliability)
    return updated_alpha, updated_beta


def calculate_expected_probability(alpha: float, beta: float) -> float:
    """
    Returns the expected probability of hypothesis validity based on Beta parameters.
    E[p] = alpha / (alpha + beta).
    """
    total = alpha + beta
    return alpha / total if total > 0 else 0.5


def calculate_epistemic_entropy(alpha: float, beta: float) -> float:
    """
    Measures the epistemic uncertainty (lack of information) vs aleatoric uncertainty.
    A lower alpha + beta represents high epistemic uncertainty (ignorance).
    """
    total = alpha + beta
    # Normalized epistemic index, bounded [0, 1] where 1.0 is total ignorance
    return 1.0 / (1.0 + total)


def apply_temporal_decay(
    initial_confidence: float,
    creation_timestamp: float,
    current_timestamp: float = None,
    lambda_decay: float = 0.02
) -> float:
    """
    Models confidence decay over time, modeling the decay of unverified historical memory.
    C(t) = C0 * e^(-lambda * delta_t).
    """
    if current_timestamp is None:
        current_timestamp = time.time()

    delta_t = max(0.0, current_timestamp - creation_timestamp)
    # Scale delta_t appropriately for simulated/real time
    decay_factor = math.exp(-lambda_decay * delta_t)
    return max(0.0, initial_confidence * decay_factor)
