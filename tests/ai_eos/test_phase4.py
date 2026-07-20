"""Unit tests for Phase 4 Executive Intelligence & Active Inference optimization layer."""

import pytest
from uuid import uuid4
from apodex.ai_eos.domain.models import VentureCell
from apodex.ai_eos.active_inference.engine import ExecutiveOptimizer


def test_bayesian_belief_updating():
    """Verify conjugate update of belief state distributions based on prediction error."""
    opt = ExecutiveOptimizer()
    cell = VentureCell(
        name="VentureBeta",
        namespace="namespace_beta",
        belief_state={"alpha": 10.0, "beta": 10.0},
        uncertainty=0.6931  # - (0.5 * log(0.5) + 0.5 * log(0.5))
    )

    # Simulated revenue exceeds expected revenue (Success outcome)
    updated_cell = opt.update_beliefs(cell, actual_revenue=1500, expected_revenue=1000)

    # Alpha must be incremented by 1 (11.0), Beta remains 10.0
    assert updated_cell.belief_state["alpha"] == 11.0
    assert updated_cell.belief_state["beta"] == 10.0

    # Uncertainty (entropy) should decrease due to information gain
    assert updated_cell.uncertainty < 0.6931
    assert updated_cell.information_gain > 0.0


def test_composite_objective_calculation():
    """Verify calculation of composite objective G score including penalties."""
    opt = ExecutiveOptimizer(w_risk=1.0, w_compute=0.5, w_info=2.0, w_gov=3.0)
    cell = VentureCell(
        name="VentureBeta",
        namespace="namespace_beta",
        sub_agent_ids=["agent_ceo", "agent_cfo"],  # 2 agents => compute cost = 0.1 * 2 = 0.2
        information_gain=0.10,
        risk=0.20
    )

    # G = Utility - w_risk*risk - w_compute*compute + w_info*info - w_gov*gov
    # G = 10.0 - 1.0*0.50 - 0.5*0.2 + 2.0*0.10 - 0.0
    # G = 10.0 - 0.50 - 0.10 + 0.20 - 0.0 = 9.60
    g = opt.compute_composite_objective(cell, policy_expected_utility=10.0, policy_risk=0.50)

    assert g == pytest.approx(9.60)
    assert cell.expected_free_energy == pytest.approx(9.60)


def test_constrained_portfolio_optimization():
    """Verify budget distribution satisfies risk caps and budget limits."""
    opt = ExecutiveOptimizer()

    cell_low_risk = VentureCell(
        name="CellLowRisk",
        namespace="ns_low",
        expected_free_energy=10.0,
        capital_allocation_score=1.0,
        risk=0.1
    )

    cell_high_risk = VentureCell(
        name="CellHighRisk",
        namespace="ns_high",
        expected_free_energy=20.0,
        capital_allocation_score=2.0,
        risk=0.8  # Exceeds the 0.7 risk threshold => priority penalized by 0.1, allocation capped
    )

    total_budget_cents = 100_000_00  # $100,000.00
    allocations = opt.optimize_allocations([cell_low_risk, cell_high_risk], total_budget_cents)

    # Low risk cell priority = 10.0 + 1.0 = 11.0
    # High risk cell priority = (20.0 + 2.0) * 0.1 = 2.2
    # High risk cell risk > 0.5 => budget is also hard-capped at 20% of total ($20,000.00)
    # Total score = 11.0 + 2.2 = 13.2
    # Shared allocations must respect these constraints and sum exactly to $100,000.00
    assert sum(allocations.values()) == total_budget_cents
    assert allocations[cell_high_risk.cell_id] <= int(0.20 * total_budget_cents)
    assert allocations[cell_low_risk.cell_id] > allocations[cell_high_risk.cell_id]
