from __future__ import annotations
import pytest
from apodex.evolution.common.models import CostMode, EvolutionChangelog
from apodex.evolution.harness_loop.optimizers import PromptParameter, DeclarativeOptimizer
from apodex.evolution.verifier.judge import EvolutionVerifier


@pytest.mark.asyncio
async def test_prompt_optimization_selection():
    """
    Test that DeclarativeOptimizer selects a prompt candidate that yields better
    structures (such as enclosed in braces) and has higher quality, leading to a higher score.
    """
    verifier = EvolutionVerifier()
    changelog = EvolutionChangelog()
    optimizer = DeclarativeOptimizer(verifier=verifier, changelog=changelog)

    param = PromptParameter(
        parameter_id="system_instruction_01",
        current_value="baseline prompt format",
        candidates=["baseline prompt format", "optimized format with braces {}"]
    )

    test_inputs = ["Process transaction 123", "Verify account 456"]

    # Map candidate values to mocked output strings that the verifier can score
    # "optimized format with braces {}" yields brace enclosed outputs -> higher score
    mock_completions = {
        "baseline prompt format": "Standard output text.",
        "optimized format with braces {}": "{ \"processed\": true, \"account\": 456 }"
    }

    res = await optimizer.optimize_parameter(
        param,
        test_inputs,
        CostMode.BALANCED,
        mock_completions=mock_completions
    )

    assert res["improved"] is True
    assert res["best_value"] == "optimized format with braces {}"
    assert res["best_score"] > res["baseline_score"]
    assert len(changelog.history) == 1
    assert changelog.history[0].applied_deltas[0].old_value == "baseline prompt format"
    assert changelog.history[0].applied_deltas[0].new_value == "optimized format with braces {}"
