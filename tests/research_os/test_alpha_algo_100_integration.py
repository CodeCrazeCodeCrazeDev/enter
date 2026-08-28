"""Integration tests for AlphaAlgo 100-paper quantitative research corpus and statistical validation.

Verifies:
1. Zero overlap between 200-paper base DB and 100-paper AlphaAlgo corpus.
2. Transferable principle registration and literature review synthesis.
3. Probability clamping and DSR calculations in statistical validation.
4. Active inference research hypothesis handoffs to EIOS Kernel and EOS Engine.
"""

import pytest
import yaml
import math
from apodex.ai_eos.research.integration import register_100_paper_alphaalgo_principles, ALPHAALGO_100_PRINCIPLES
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.research_os.statistical_validation import (
    standard_normal_ppf,
    standard_normal_cdf,
    calculate_dsr,
    adjust_p_values
)


def test_alpha_algo_100_corpus_uniqueness():
    """Verify zero title/DOI overlap between base 200 DB and AlphaAlgo 100 DB."""
    with open('docs/research/papers/AI_EOS_RESEARCH_DB.yaml', 'r') as f:
        db1 = yaml.safe_load(f)
    with open('docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml', 'r') as f:
        db2 = yaml.safe_load(f)

    papers1 = db1.get('papers', []) if isinstance(db1, dict) else db1
    papers2 = db2.get('papers', []) if isinstance(db2, dict) else db2

    assert len(papers1) == 200, f"Expected 200 base papers, got {len(papers1)}"
    assert len(papers2) == 100, f"Expected 100 AlphaAlgo papers, got {len(papers2)}"

    titles1 = set(p['title'].strip().lower() for p in papers1 if 'title' in p)
    titles2 = set(p['title'].strip().lower() for p in papers2 if 'title' in p)

    overlap = titles1.intersection(titles2)
    assert len(overlap) == 0, f"Found overlapping titles: {overlap}"


def test_principle_registration_and_literature_review():
    """Verify registration of 100-paper principles and ResearchOS synthesis."""
    principles = register_100_paper_alphaalgo_principles()
    assert len(principles) == 5
    assert principles == ALPHAALGO_100_PRINCIPLES

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")
    assert review["reviewed_citations_count"] == 100
    assert len(review["extracted_principles"]) > 0


def test_statistical_validation_clamping_and_dsr():
    """Verify probability clamping in standard_normal_ppf and calculate_dsr."""
    # Test boundary probability clamping
    val_zero = standard_normal_ppf(0.0)
    val_one = standard_normal_ppf(1.0)
    assert math.isfinite(val_zero)
    assert math.isfinite(val_one)

    # Test DSR with T=1 and normal trials
    dsr = calculate_dsr(sharpe=1.5, trials=10, returns_length=1)
    assert 0.0 <= dsr <= 1.0

    # Test p-value adjustments
    p_vals = [0.01, 0.04, 0.03, 0.20]
    adj_p = adjust_p_values(p_vals, method="HOLM")
    assert len(adj_p) == len(p_vals)
    assert all(0.0 <= p <= 1.0 for p in adj_p)


def test_research_to_kernel_and_eos_handoff():
    """Verify research hypothesis handoffs to EIOS Kernel and EOS Engine."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()

    hyp = ros.register_hypothesis(
        title="Hawkes Alpha Strategy",
        description="Self-exciting order flow imbalance strategy",
        null_hypothesis="Alpha <= 0",
        target_metric="Sharpe"
    )

    exp = ros.create_experiment(hyp.hypothesis_id, seed=42)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert hyp.status == "validated"

    # Export to Kernel
    exported_kernel = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, kernel)
    assert exported_kernel is True

    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) > 0

    # Promote to EOS Engine
    promoted_eos = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    assert promoted_eos is True
    assert len(eos.active_hypotheses) > 0
