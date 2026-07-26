from __future__ import annotations
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ResearchProject(BaseModel):
    project_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    expected_discovery_value_usd: float = 1000.0
    cost_estimate_tokens: int = 500000
    probability_of_success: float = 0.5
    epistemic_information_gain: float = 1.2


class ResearchPortfolioScheduler:
    """
    Coordinates scheduling and prioritizes capital allocation across competing research projects
    by calculating a robust utility index:
    Score = (Expected_Discovery_Value * Probability_Success) - Expected_Cost + Information_Gain
    """

    def __init__(self, token_cost_coefficient: float = 0.0001) -> None:
        self.token_cost_coefficient = token_cost_coefficient

    def calculate_priority_index(self, project: ResearchProject) -> float:
        """
        Computes the prioritized utility score of a research project.
        """
        success_payout = project.expected_discovery_value_usd * project.probability_of_success
        cost_penalty = project.cost_estimate_tokens * self.token_cost_coefficient
        exploration_bonus = project.epistemic_information_gain * 100.0  # weighted epistemic value

        return success_payout - cost_penalty + exploration_bonus

    def prioritize_projects(self, projects: List[ResearchProject]) -> List[tuple[ResearchProject, float]]:
        """Sorts projects in descending order based on their priority score."""
        scored_projects = []
        for proj in projects:
            score = self.calculate_priority_index(proj)
            scored_projects.append((proj, score))

        return sorted(scored_projects, key=lambda x: x[1], reverse=True)
