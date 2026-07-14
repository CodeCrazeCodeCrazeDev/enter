from __future__ import annotations
import json
import logging
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

logger = logging.getLogger("apodex.memory.learning")


class TrajectoryRecord(BaseModel):
    task_id: str
    task_type: str
    goal: str
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    is_success: bool
    learned_insight: Optional[str] = None


class LongTermLearningMemory:
    """Tracks historical cross-session task success rates and learned strategies/insights."""

    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path
        self.registry: Dict[str, List[TrajectoryRecord]] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for task_type, records in data.items():
                    self.registry[task_type] = [TrajectoryRecord(**rec) for rec in records]
        except (OSError, ValueError) as exc:
            logger.warning(
                "Failed to load learning memory from '%s': %s. Starting with empty registry.",
                self.storage_path,
                exc,
                exc_info=True,
            )

    def _save(self) -> None:
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                serialized = {
                    task_type: [rec.dict() for rec in records]
                    for task_type, records in self.registry.items()
                }
                json.dump(serialized, f, indent=2)
        except OSError:
            logger.exception("Failed to persist learning memory to '%s'.", self.storage_path)
            raise

    def record_trajectory(self, record: TrajectoryRecord) -> None:
        """Add a trajectory record and persist it to long-term memory."""
        if record.task_type not in self.registry:
            self.registry[record.task_type] = []
        self.registry[record.task_type].append(record)
        self._save()

    def query_similar_strategies(self, task_type: str, query: str) -> List[TrajectoryRecord]:
        """Query successful historical trajectory cards matching the task type."""
        records = self.registry.get(task_type, [])
        # Simplified query matching based on keyword intersection in goal or insight
        keywords = set(query.lower().split())
        matched = []
        for rec in records:
            # We want to favor successful trials
            target_text = f"{rec.goal} {rec.learned_insight or ''}".lower()
            if any(kw in target_text for kw in keywords):
                matched.append(rec)
        # Sort successful runs first
        matched.sort(key=lambda x: x.is_success, reverse=True)
        return matched
