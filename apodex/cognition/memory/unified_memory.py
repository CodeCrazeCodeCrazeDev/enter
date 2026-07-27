from __future__ import annotations
import logging
from typing import List, Dict, Any, Optional
import uuid

from apodex.cognition.shared.schemas import (
    StrategicGoal,
    Hypothesis,
    EvidenceCard,
    DecisionProvenance,
    Lesson
)

logger = logging.getLogger("apodex.cognition.memory")


class UnifiedMemory:
    """
    Rule 1: Only one global memory. No duplicated memory systems.
    Serves as the single repository of truth for all cognitive modules.
    """

    def __init__(self) -> None:
        self.provenance_records: Dict[uuid.UUID, DecisionProvenance] = {}
        self.evidence_pool: Dict[uuid.UUID, EvidenceCard] = {}
        self.hypotheses_pool: Dict[uuid.UUID, Hypothesis] = {}
        self.goals_pool: Dict[uuid.UUID, StrategicGoal] = {}
        self.lessons_pool: List[Lesson] = []

    def clear(self) -> None:
        self.provenance_records.clear()
        self.evidence_pool.clear()
        self.hypotheses_pool.clear()
        self.goals_pool.clear()
        self.lessons_pool.clear()

    def add_goal(self, goal: StrategicGoal) -> None:
        self.goals_pool[goal.id] = goal

    def get_goal(self, goal_id: uuid.UUID) -> Optional[StrategicGoal]:
        return self.goals_pool.get(goal_id)

    def get_all_goals(self) -> List[StrategicGoal]:
        return list(self.goals_pool.values())

    def add_hypothesis(self, hyp: Hypothesis) -> None:
        self.hypotheses_pool[hyp.id] = hyp

    def get_hypotheses_for_goal(self, goal_id: uuid.UUID) -> List[Hypothesis]:
        return [h for h in self.hypotheses_pool.values() if h.goal_id == goal_id]

    def add_evidence(self, ev: EvidenceCard) -> None:
        self.evidence_pool[ev.id] = ev

    def get_all_evidence(self) -> List[EvidenceCard]:
        return list(self.evidence_pool.values())

    def add_provenance(self, prov: DecisionProvenance) -> None:
        self.provenance_records[prov.id] = prov

    def get_provenance(self, prov_id: uuid.UUID) -> Optional[DecisionProvenance]:
        return self.provenance_records.get(prov_id)

    def get_all_provenance(self) -> List[DecisionProvenance]:
        return list(self.provenance_records.values())

    def add_lesson(self, lesson: Lesson) -> None:
        self.lessons_pool.append(lesson)

    def get_lessons_by_category(self, category: str) -> List[Lesson]:
        return [L for L in self.lessons_pool if L.category == category]

    def get_all_lessons(self) -> List[Lesson]:
        return list(self.lessons_pool)
