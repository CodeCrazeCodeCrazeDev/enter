"""Unit tests for Phase 5 Execution Systems (AEAN & ARCS Integration) orchestration adapters."""

import pytest
from uuid import uuid4
from apodex.ai_eos.orchestration.backend import ExecutionBackendAdapter
from apodex.aean.flywheel import Organism


def test_aean_organism_backend_adapter():
    """Verify that the execution adapter coordinates AEAN step cycle correctly and returns translated metrics."""
    # Build a stable mock or light seed Organism
    organism = Organism(initial_capital_cents=500000, seed=12)
    adapter = ExecutionBackendAdapter(organism=organism)

    cell_id = uuid4()
    metrics = adapter.run_cycle(cell_id, capital_cents=100000)

    # Verify return schema
    assert metrics["cell_id"] == cell_id
    assert "capital_deployed_cents" in metrics
    assert "earned_revenue_cents" in metrics
    assert "signals_detected" in metrics
    assert metrics["cycle_number"] == 1
