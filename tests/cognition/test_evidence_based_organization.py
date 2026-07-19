from __future__ import annotations
import pytest
import uuid

from apodex.cognition.shared.schemas import (
    StrategicGoal,
    CognitiveContext,
    EvidenceCard
)
from apodex.cognition.controller import CognitiveSystemController


@pytest.mark.asyncio
async def test_evidence_based_organization_protocol_rejection():
    """Verify that a strategic decision constrained by require_evidence is vetoed if no evidence cards are present."""
    controller = CognitiveSystemController()

    # Executing without evidence should fail
    provenance = await controller.execute_decision_cycle(
        goal_title="Uncorroborated Strategic Strategy",
        goal_description="Launch high-frequency dynamic pricing variant.",
        budget_cents=100_000,
        constraints=["require_evidence"],
        simulate_success=True
    )

    assert "REJECTED" in provenance.final_decision
    assert "Evidence-based self-improving organization protocol" in provenance.final_decision
    assert provenance.execution_outcome is None


@pytest.mark.asyncio
async def test_evidence_based_organization_protocol_success():
    """Verify that execution is approved and fully measured/compared/fed back when supporting evidence is present."""
    controller = CognitiveSystemController()

    # Supplying high-quality supporting evidence
    obs_data = {
        "evidence": [
            {
                "source": "Academic Literature Review",
                "description": "Dynamic pricing with localized elasticity has been proven to increase revenue by 14%.",
                "reliability": 0.95
            }
        ]
    }

    provenance = await controller.execute_decision_cycle(
        goal_title="Corroborated Strategic Strategy",
        goal_description="Launch high-frequency dynamic pricing variant.",
        budget_cents=200_000,
        constraints=["require_evidence"],
        observation_data=obs_data,
        simulate_success=True
    )

    # 1. Supported by Evidence
    assert provenance.final_decision == "APPROVED"
    assert len(provenance.evidence) == 1
    assert provenance.evidence[0].source == "Academic Literature Review"

    # 2. Simulated before Execution
    assert "expected_cost_cents" in provenance.predicted_expectations
    assert "expected_roi_multiple" in provenance.predicted_expectations

    # 3. Measured after Execution
    assert provenance.execution_outcome is not None
    assert provenance.execution_outcome.success is True
    assert provenance.execution_outcome.actual_cost_cents == int(200_000 * 0.95)

    # 4. Compared against Expectations (discrepancy analysis)
    assert "cost_variance_cents" in provenance.discrepancy_analysis
    assert "roi_variance_multiple" in provenance.discrepancy_analysis
    assert provenance.discrepancy_analysis["cost_variance_cents"] == 0 # Perfect estimate match

    # 5. Fed back to Memory
    assert len(provenance.lessons_learned) > 0
    assert len(controller.memory.get_all_lessons()) > 0

    # Verify that the world model has adapted under positive reinforcement feedback (market_saturation updated)
    assert controller.world_model.base_parameters["market_saturation"] == 0.12


@pytest.mark.asyncio
async def test_evidence_based_organization_protocol_discrepancy_on_failure():
    """Verify correct discrepancy tracking and model adjustment on strategic execution failure."""
    controller = CognitiveSystemController()

    obs_data = {
        "evidence": [
            {
                "source": "Internal Pilot Trial",
                "description": "Initial tests support baseline database caching.",
                "reliability": 0.85
            }
        ]
    }

    provenance = await controller.execute_decision_cycle(
        goal_title="Cached Query Pipeline",
        goal_description="Integrate cache buffers for static queries.",
        budget_cents=150_000,
        constraints=["require_evidence"],
        observation_data=obs_data,
        simulate_success=False # Force execution failure
    )

    assert provenance.final_decision == "APPROVED"
    assert provenance.execution_outcome.success is False

    # Measured & Compared
    assert provenance.discrepancy_analysis["performance_gap_detected"] is True
    assert provenance.discrepancy_analysis["cost_variance_cents"] > 0 # Cost overrun on failure

    # Fed back & Tuned
    assert controller.world_model.base_parameters["complexity_cost_multiplier"] == 1.4
    assert controller.world_model.base_parameters["failure_probability_offset"] == 0.12
