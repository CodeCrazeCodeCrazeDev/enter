from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ExecutionTrace:
    """Represents a structured execution trace from an AEAN task run."""
    task_id: str
    steps: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    agent_config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FailureSignature:
    """Represents a detected and clustered failure signature."""
    signature_id: str
    error_pattern: str
    occurrence_count: int
    affected_tasks: List[str] = field(default_factory=list)


@dataclass
class DistilledLesson:
    """Represents a semantic lesson distilled from past trials."""
    lesson_id: str
    domain: str
    description: str
    trigger_conditions: List[str] = field(default_factory=list)
    actionable_guidelines: List[str] = field(default_factory=list)


class ExperienceDatabase:
    """
    Central database and cognition base for Apodex.
    Stores raw traces, clustered failure signatures, and distilled lessons.
    """

    def __init__(self, connection_uri: str = "sqlite:///:memory:") -> None:
        self.connection_uri = connection_uri
        self._traces: Dict[str, ExecutionTrace] = {}
        self._signatures: Dict[str, FailureSignature] = {}
        self._lessons: List[DistilledLesson] = []

    async def save_trace(self, trace: ExecutionTrace) -> None:
        """
        Persists a completed task execution trace.

        Args:
            trace: The ExecutionTrace object containing steps, metrics, and errors.
        """
        self._traces[trace.task_id] = trace

    async def get_trace(self, task_id: str) -> Optional[ExecutionTrace]:
        """
        Retrieves an execution trace by task ID.

        Args:
            task_id: Unique task identifier.

        Returns:
            The ExecutionTrace if found, otherwise None.
        """
        return self._traces.get(task_id)

    async def save_failure_signature(self, signature: FailureSignature) -> None:
        """
        Registers or updates a failure signature cluster.

        Args:
            signature: The FailureSignature to register.
        """
        self._signatures[signature.signature_id] = signature

    async def get_all_failure_signatures(self) -> List[FailureSignature]:
        """
        Retrieves all active failure signatures registered in the system.

        Returns:
            List of active FailureSignatures.
        """
        return list(self._signatures.values())

    async def save_distilled_lesson(self, lesson: DistilledLesson) -> None:
        """
        Saves a distilled lesson to the Cognition Base.

        Args:
            lesson: The DistilledLesson to store.
        """
        self._lessons.append(lesson)

    async def query_lessons_for_domain(self, domain: str) -> List[DistilledLesson]:
        """
        Queries distilled lessons applicable to a specific task domain.

        Args:
            domain: The target domain (e.g., 'coding', 'mathematics').

        Returns:
            A list of relevant DistilledLessons.
        """
        return [lesson for lesson in self._lessons if lesson.domain == domain]
