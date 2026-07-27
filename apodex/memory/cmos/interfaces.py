"""Core interfaces and contracts for CMOS components.

Includes repositories, pluggable operators, registrars, query planners, and schedulers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from apodex.memory.cmos.models import MemoryNode, MemoryEdge, MemoryGraph


class RepositoryConfig(BaseModel):
    storage_uri: str = ":memory:"


class OperatorTelemetry(BaseModel):
    operator_name: str
    execution_id: UUID = Field(default_factory=uuid4)
    latency_ms: float = 0.0
    memory_usage_bytes: int = 0
    graph_mutations: int = 0
    cache_hits: int = 0
    status: str = "success"
    error_message: Optional[str] = None
    confidence_changes: List[Dict[str, Any]] = Field(default_factory=list)


class OperatorContext(BaseModel):
    task_id: UUID
    tenant_id: str
    user_id: str
    telemetry: List[OperatorTelemetry] = Field(default_factory=list)
    graph_overlay: MemoryGraph = Field(default_factory=MemoryGraph)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class OperatorResult(BaseModel):
    success: bool = True
    output_nodes: List[MemoryNode] = Field(default_factory=list)
    output_edges: List[MemoryEdge] = Field(default_factory=list)
    telemetry: OperatorTelemetry
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemoryRepository(ABC):
    """Abstraction for CMOS persistent backends."""

    @abstractmethod
    async def save_node(self, node: MemoryNode) -> None:
        """Saves or updates a MemoryNode in storage."""
        pass

    @abstractmethod
    async def get_node(self, node_id: str) -> Optional[MemoryNode]:
        """Loads a single MemoryNode from storage."""
        pass

    @abstractmethod
    async def delete_node(self, node_id: str) -> None:
        """Erases a MemoryNode from storage, cascading associated edges."""
        pass

    @abstractmethod
    async def save_edge(self, edge: MemoryEdge) -> None:
        """Saves a MemoryEdge in storage."""
        pass

    @abstractmethod
    async def get_edges(self, source_id: str) -> List[MemoryEdge]:
        """Retrieves all outbound edges starting from the source_id."""
        pass

    @abstractmethod
    async def query_nodes(self, filters: Dict[str, Any]) -> List[MemoryNode]:
        """Queries nodes matching given structured filter values."""
        pass


class CognitiveOperator(ABC):
    """Contract for pluggable CMOS operators."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier name of the operator."""
        pass

    @abstractmethod
    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        """Executes active memory reasoning logic."""
        pass


class OperatorRegistry(ABC):
    """Catalog of active pluggable CMOS operators."""

    @abstractmethod
    def register(self, op: Type[CognitiveOperator]) -> None:
        pass

    @abstractmethod
    def get_operator(self, name: str) -> CognitiveOperator:
        pass

    @abstractmethod
    def list_operators(self) -> List[str]:
        pass


class MemoryQueryPlanner(ABC):
    """Translates natural objective targets into executable operator chains."""

    @abstractmethod
    async def plan(self, objective: str, ctx: OperatorContext) -> List[Dict[str, Any]]:
        """Compiles objective to serializable Execution Plan steps."""
        pass


class MemoryScheduler(ABC):
    """First-class scheduler managing immediate, short, medium, and long-term background work."""

    @abstractmethod
    async def schedule_task(self, tier: str, coro_name: str, **kwargs) -> None:
        """Queues a task in the specified temporal queue (immediate, short, medium, long)."""
        pass

    @abstractmethod
    async def run_pending(self, tier: str) -> int:
        """Triggers and completes all pending scheduled tasks in a given tier."""
        pass
