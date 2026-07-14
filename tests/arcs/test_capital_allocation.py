from __future__ import annotations

from apodex.arcs.capital.allocation_engine import CapitalAllocationEngine


def test_proportional_allocation_by_score():
    engine = CapitalAllocationEngine(initial_reserves_cents=10000)
    allocations = engine.optimize_allocations({"sales": 3.0, "eng": 1.0}, 8000)
    assert sum(allocations.values()) == 8000
    # sales has 75% score share; last dept (eng) receives the remainder
    assert allocations["sales"] == 6000
    assert allocations["eng"] == 2000


def test_reserves_are_deducted():
    engine = CapitalAllocationEngine(initial_reserves_cents=10000)
    engine.optimize_allocations({"sales": 1.0}, 4000)
    assert engine.reserves_cents == 6000


def test_allocation_capped_at_reserves():
    engine = CapitalAllocationEngine(initial_reserves_cents=5000)
    allocations = engine.optimize_allocations({"sales": 1.0, "eng": 1.0}, 8000)
    assert sum(allocations.values()) == 5000
    assert engine.reserves_cents == 0


def test_empty_scores_returns_empty():
    engine = CapitalAllocationEngine(initial_reserves_cents=10000)
    assert engine.optimize_allocations({}, 5000) == {}


def test_zero_total_score_distributes_equally():
    engine = CapitalAllocationEngine(initial_reserves_cents=10000)
    allocations = engine.optimize_allocations({"a": 0.0, "b": 0.0}, 6000)
    assert allocations == {"a": 3000, "b": 3000}
