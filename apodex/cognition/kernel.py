from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from apodex.planning.planner_executor import StrategicPlanner
from apodex.world_model.world_model import WorldModel
from apodex.memory.semantic_memory import SemanticMemory, SQLiteMemoryRepository
from apodex.cognition.meta_reasoner import MetaReasonerObserver

logger = logging.getLogger("apodex.cognition.kernel")

class CognitiveKernel(BaseModel):
    """
    Authoritative Cognitive Kernel owning the entire unified cognitive state.
    Goal management, planning, reasoning, world modeling, simulation, memory,
    decision making, execution, evaluation, and learning are unified here.
    """
    goals: List[str] = Field(default_factory=list)
    intentions: List[str] = Field(default_factory=list)
    beliefs: Dict[str, Any] = Field(default_factory=dict)
    uncertainty_metrics: Dict[str, float] = Field(default_factory=dict)
    resource_budget: float = 1000.0

    # Lazy loaded dependency components
    _planner: Optional[StrategicPlanner] = None
    _world_model: Optional[WorldModel] = None
    _memory: Optional[SemanticMemory] = None
    _meta_reasoner: Optional[MetaReasonerObserver] = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def planner(self) -> StrategicPlanner:
        if not self._planner:
            self._planner = StrategicPlanner()
        return self._planner

    @property
    def world_model(self) -> WorldModel:
        if not self._world_model:
            self._world_model = WorldModel()
        return self._world_model

    @property
    def memory(self) -> SemanticMemory:
        if not self._memory:
            repo = SQLiteMemoryRepository(db_path=":memory:")
            self._memory = SemanticMemory(repository=repo)
        return self._memory

    @property
    def meta_reasoner(self) -> MetaReasonerObserver:
        if not self._meta_reasoner:
            self._meta_reasoner = MetaReasonerObserver()
        return self._meta_reasoner

    def set_goal(self, goal: str) -> None:
        """Sets a new strategic goal and adds it to intentions."""
        self.goals.append(goal)
        self.intentions.append(goal)
        logger.info(f"CognitiveKernel: Strategic goal registered: '{goal}'")

    async def deliberate_and_plan(self) -> Any:
        """Runs deliberate-and-plan loops across planning and causal transition estimation."""
        if not self.goals:
            return None
        active_goal = self.goals[-1]
        roadmap = await self.planner.create_roadmap(active_goal)
        logger.info(f"CognitiveKernel: Multi-step roadmap successfully generated for goal '{active_goal}'")
        return roadmap
