from __future__ import annotations
import pytest
import uuid

from apodex.cognition.shared.schemas import StrategicGoal, CognitiveContext
from apodex.cognition.controller import CognitiveSystemController


@pytest.mark.asyncio
async def test_research_portfolio_opportunity_metrics():
    """Verify that hypothesis generation produces a prioritized research portfolio based on expected value and information gain."""
    controller = CognitiveSystemController()

    goal = StrategicGoal(
        title="Optimize Model Size",
        description="Scale model parameters to match optimal budget tiers.",
        priority_score=0.75,
        budget_cents=500_000
    )
    context = CognitiveContext(active_goal=goal)

    # 1. Propose and generate research hypotheses
    hyps = await controller.research.plan(context)

    # Verify that multiple candidate hypotheses are generated (portfolio model)
    assert len(hyps) >= 3

    # 2. Verify existence of continuous opportunity metrics on each hypothesis (arXiv:2605.15245)
    for h in hyps:
        assert h.expected_scientific_value > 0.0
        assert h.expected_engineering_impact > 0.0
        assert h.expected_business_value > 0.0
        assert h.cost_of_investigation_cents > 0
        assert h.probability_of_success > 0.0
        assert h.information_gain > 0.0
        assert h.priority_score > 0.0

    # 3. Assert that hypotheses are strictly sorted in descending order of priority_score
    priorities = [h.priority_score for h in hyps]
    assert priorities == sorted(priorities, reverse=True)


@pytest.mark.asyncio
async def test_research_recommendation_corresponds_to_highest_priority():
    """Verify that research recommendations are mapped strictly to the highest-priority portfolio item."""
    controller = CognitiveSystemController()

    goal = StrategicGoal(
        title="Model Fine-Tuning SFT",
        description="Run lora adapters on task data.",
        priority_score=0.80,
        budget_cents=100_000
    )
    context = CognitiveContext(active_goal=goal)

    # Plan and recommend
    await controller.research.plan(context)
    recs = await controller.research.recommend(context)

    assert len(recs) == 1
    best_rec = recs[0]

    assert best_rec.title == "Launch Bounded Experimental Sandbox"

    # Target hypothesis should match the highest priority score
    highest_priority_score = max(h.priority_score for h in context.hypotheses)
    assert best_rec.payload["priority_score"] == highest_priority_score
