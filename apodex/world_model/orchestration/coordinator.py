from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID

from apodex.world_model.dependency_injection import DependencyContainer
from apodex.world_model.domain.timelines import Timeline, WorldGraphDelta
from apodex.world_model.domain.simulation import SimulationRunContext
from apodex.world_model.interfaces.engines import IWorldSimulationEngine, IRealityEngine


class WmcOrchestrationCoordinator:
    """The central coordinator managing execution across WMC engines."""

    def __init__(self, container: DependencyContainer) -> None:
        self.container = container

    async def run_scenario_simulation(self, parent_timeline_id: UUID,
                                      scenario_name: str,
                                      hours_to_simulate: float) -> Timeline:
        """Coordinates branching, simulation stepping, and delta application."""
        sim_engine = self.container.resolve(IWorldSimulationEngine)

        # 1. Create a branch timeline
        branch_time = datetime.utcnow()
        timeline = await sim_engine.create_branch(parent_timeline_id, scenario_name, branch_time)

        # 2. Run simulation stepping
        run_context = SimulationRunContext(
            timeline_id=timeline.timeline_id,
            start_sim_time=branch_time,
            end_sim_time=branch_time,
            step_duration_hours=hours_to_simulate
        )
        deltas = await sim_engine.step_simulation(run_context)

        # 3. Apply the compiled deltas to the new timeline
        for delta in deltas:
            timeline.add_delta(delta)

        return timeline
