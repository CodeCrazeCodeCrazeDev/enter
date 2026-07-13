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


@dataclass
class PersonalEvolutionProfile:
    """Represents a user's persistent, versioned Personal Evolution Profile (PEP)."""
    user_id: str
    version: int = 1
    typical_tasks: List[Dict[str, Any]] = field(default_factory=list)
    effective_workflows: List[Dict[str, Any]] = field(default_factory=list)
    style_preferences: Dict[str, Any] = field(default_factory=dict)
    cost_latency_preferences: Dict[str, Any] = field(default_factory=dict)
    domain_vocabulary: Dict[str, str] = field(default_factory=dict)
    evolution_controls: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchTicket:
    """A research ticket escalated from the harness loop to the research loop."""
    ticket_id: str
    created_at: str
    failure_pattern: str
    example_traces: List[str]
    user_impact: str
    harness_attempts: List[Dict[str, str]]
    suggested_direction: str


@dataclass
class CapabilityDelta:
    """A capability update payload published by the research loop back to the harness."""
    model_version: str
    released_at: str
    capabilities_delta: Dict[str, List[str]]
    recommended_harness_changes: List[str]


class ExperienceDatabase:
    """
    Central database and cognition base for Apodex.
    Stores raw traces, failure signatures, distilled lessons, PEPs, and loop feedback signals.
    """

    def __init__(self, connection_uri: str = "sqlite:///:memory:") -> None:
        self.connection_uri = connection_uri
        self._traces: Dict[str, ExecutionTrace] = {}
        self._signatures: Dict[str, FailureSignature] = {}
        self._lessons: List[DistilledLesson] = []
        self._peps: Dict[str, PersonalEvolutionProfile] = {}
        self._tickets: Dict[str, ResearchTicket] = {}
        self._deltas: List[CapabilityDelta] = []

    async def save_trace(self, trace: ExecutionTrace) -> None:
        """Persists a completed task execution trace."""
        self._traces[trace.task_id] = trace

    async def get_trace(self, task_id: str) -> Optional[ExecutionTrace]:
        """Retrieves an execution trace by task ID."""
        return self._traces.get(task_id)

    async def save_failure_signature(self, signature: FailureSignature) -> None:
        """Registers or updates a failure signature cluster."""
        self._signatures[signature.signature_id] = signature

    async def get_all_failure_signatures(self) -> List[FailureSignature]:
        """Retrieves all active failure signatures registered in the system."""
        return list(self._signatures.values())

    async def save_distilled_lesson(self, lesson: DistilledLesson) -> None:
        """Saves a distilled lesson to the Cognition Base."""
        self._lessons.append(lesson)

    async def query_lessons_for_domain(self, domain: str) -> List[DistilledLesson]:
        """Queries distilled lessons applicable to a specific task domain."""
        return [lesson for lesson in self._lessons if lesson.domain == domain]

    async def get_pep(self, user_id: str) -> Optional[PersonalEvolutionProfile]:
        """Retrieves the Personal Evolution Profile (PEP) for a user."""
        return self._peps.get(user_id)

    async def save_pep(self, pep: PersonalEvolutionProfile) -> None:
        """Saves or updates a user's Personal Evolution Profile."""
        self._peps[pep.user_id] = pep

    async def create_research_ticket(self, ticket: ResearchTicket) -> None:
        """Registers a new research ticket."""
        self._tickets[ticket.ticket_id] = ticket

    async def get_research_tickets(self) -> List[ResearchTicket]:
        """Retrieves all open research tickets."""
        return list(self._tickets.values())

    async def publish_capability_delta(self, delta: CapabilityDelta) -> None:
        """Publishes a new model capability delta to the harness loop."""
        self._deltas.append(delta)

    async def get_latest_capability_deltas(self) -> List[CapabilityDelta]:
        """Gets all published capability deltas."""
        return self._deltas
