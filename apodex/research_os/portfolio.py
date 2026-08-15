from __future__ import annotations
from uuid import UUID
from typing import Dict, List
from pydantic import BaseModel
from .models import ResearchProject

# =====================================================================
# Scheduler & Portfolio Orchestration
# =====================================================================

class ProjectAllocation(BaseModel):
    project_uuid: UUID
    compute_quota: float  # [0.0, 1.0] proportion of total cluster power
    allocated_tokens: int


class PortfolioScheduler:
    """
    Manages competing scientific projects, optimizing allocations based on
    Expected Discovery Value (EDV), opportunity cost, and strict resource quotas.
    """

    def __init__(self, total_gpu_tokens_budget: int = 1000000) -> None:
        self.total_budget = total_gpu_tokens_budget
        self.active_projects: Dict[UUID, ResearchProject] = {}

    def add_project(self, project: ResearchProject) -> None:
        self.active_projects[project.uuid] = project

    def remove_project(self, project_uuid: UUID) -> None:
        self.active_projects.pop(project_uuid, None)

    def calculate_project_priority(self, project: ResearchProject, success_rate: float) -> float:
        """
        Computes dynamic priority score incorporating Expected Discovery Value (EDV)
        and opportunity cost of capital/compute.
        EDV = Success Probability * Expected Impact.
        """
        # Estimated Success Probability (prioritized by historical success_rate)
        p_success = max(0.1, min(0.99, success_rate))
        impact = project.expected_discovery_value

        # Calculate Expected Discovery Value
        edv = p_success * impact

        # Opportunity cost: penalties for overspent funding budget
        opportunity_penalty = 0.0
        if project.funding_budget > 100000.0:
            opportunity_penalty = 0.1 * (project.funding_budget / 100000.0)

        # Final Priority score
        priority = edv - opportunity_penalty
        return max(0.01, priority)

    def optimize_portfolio(self, historical_success_rates: Dict[UUID, float]) -> List[ProjectAllocation]:
        """
        Allocates token quotas proportionally across competing projects
        based on optimized priority scores.
        """
        if not self.active_projects:
            return []

        priority_scores = {}
        total_priority = 0.0

        for uuid, project in self.active_projects.items():
            success = historical_success_rates.get(uuid, 0.5)
            score = self.calculate_project_priority(project, success)
            priority_scores[uuid] = score
            total_priority += score

        allocations = []
        for uuid, project in self.active_projects.items():
            score = priority_scores[uuid]
            quota = score / total_priority if total_priority > 0 else (1.0 / len(self.active_projects))
            tokens = int(quota * self.total_budget)

            allocations.append(ProjectAllocation(
                project_uuid=uuid,
                compute_quota=quota,
                allocated_tokens=tokens
            ))

        return allocations

    def check_for_terminations(self, historical_success_rates: Dict[UUID, float], min_edv_threshold: float = 10.0) -> List[UUID]:
        """Identifies and terminates projects whose expected discovery value falls below threshold."""
        terminated = []
        for uuid, project in list(self.active_projects.items()):
            success = historical_success_rates.get(uuid, 0.5)
            edv = success * project.expected_discovery_value
            if edv < min_edv_threshold:
                terminated.append(uuid)
                self.remove_project(uuid)
        return terminated
