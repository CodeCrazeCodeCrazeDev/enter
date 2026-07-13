from __future__ import annotations
import pytest
from apodex.evolution.common.models import CostMode, MultiObjectiveMetric, calculate_multiobjective_score
from apodex.evolution.harness_loop.optimizers import SelfCritiqueOptimizer


@pytest.mark.asyncio
async def test_self_critique_under_cost_modes():
    """
    Verifies that SelfCritiqueOptimizer accepts/rejects revisions depending on
    the active cost mode.
    """
    optimizer = SelfCritiqueOptimizer()
    prompt = "Create a summary of AEAN architecture."
    initial_comp = "A layered corporate network of multi-agent cognitive systems."

    # For MQ: short, high-quality revised completion is preferred over baseline.
    mock_revised_mq = "{ \"processed\": true, \"summary\": \"An enterprise-grade Autonomous Economic Agent Network.\" }"

    res_mq = await optimizer.run_revision_cycle(
        prompt,
        initial_comp,
        CostMode.MAX_QUALITY,
        mock_revised_completion=mock_revised_mq
    )
    assert res_mq["accepted"] is True
    assert res_mq["final_completion"] == mock_revised_mq

    # For FC: extremely long, high-quality revised completion is rejected because cost/latency penalties outweigh quality.
    mock_revised_fc = (
        "{\n"
        "  \"processed\": true,\n"
        "  \"summary\": \"An enterprise-grade Autonomous Economic Agent Network.\",\n"
        "  \"filler\": \"" + ("A" * 1500) + "\"\n"
        "}"
    )

    res_fc = await optimizer.run_revision_cycle(
        prompt,
        initial_comp,
        CostMode.FAST_CHEAP,
        mock_revised_completion=mock_revised_fc
    )
    assert res_fc["accepted"] is False
    assert res_fc["final_completion"] == initial_comp


def test_score_calculation_across_modes():
    """
    Directly tests that calculate_multiobjective_score shifts weights
    correctly under different cost profiles.
    """
    metrics = MultiObjectiveMetric(quality=0.8, cost=0.6, latency=0.7)

    score_fc = calculate_multiobjective_score(metrics, CostMode.FAST_CHEAP)
    score_bl = calculate_multiobjective_score(metrics, CostMode.BALANCED)
    score_mq = calculate_multiobjective_score(metrics, CostMode.MAX_QUALITY)

    # In FAST_CHEAP, the penalties are largest, yielding the lowest score
    # In MAX_QUALITY, the penalties are tiny, yielding the highest score
    assert score_fc < score_bl
    assert score_bl < score_mq
    # Make sure they are calculated accurately
    assert score_fc == max(0.0, 0.8 - (0.5 * 0.6) - (0.4 * 0.7))  # 0.8 - 0.3 - 0.28 = 0.22
    assert score_bl == max(0.0, 0.8 - (0.2 * 0.6) - (0.2 * 0.7))  # 0.8 - 0.12 - 0.14 = 0.54
    assert score_mq == max(0.0, 0.8 - (0.02 * 0.6) - (0.01 * 0.7))  # 0.8 - 0.012 - 0.007 = 0.781
