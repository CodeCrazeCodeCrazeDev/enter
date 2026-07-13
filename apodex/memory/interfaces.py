"""Abstract Base Interfaces for the Apodex 2.0 5-Tier Memory & Runtime Architecture.

Defines the interfaces for Ingestion Pipelines, Retrieval API, and the Checkpoint Manager.
Includes a fully implemented, production-ready hybrid scoring method reflecting cost modes.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

from apodex.memory.models import (
    AtomicMemory,
    CostMode,
    EpisodeLogRecord,
    NodeType,
    PersonalEvolutionProfile,
    ResearchTicket,
    ScenarioPattern,
    WorkingContextGraph,
    WorkingContextNode,
)


class IngestionPipeline(ABC):
    """Asynchronous pipeline responsible for real-time memory ingestion and consolidation."""

    @abstractmethod
    async def log_episode_step(self, record: EpisodeLogRecord) -> None:
        """Appends a raw LLM input/output step to Tier 1 Episodic Memory."""
        pass

    @abstractmethod
    async def extract_and_inject_atoms(
        self,
        episode_id: UUID,
        raw_log_content: str,
        tenant_id: str,
        user_id: str,
    ) -> List[AtomicMemory]:
        """Extracts atomic facts (T2) from raw T1 logs, attaches embeddings and confidence, and saves to DB."""
        pass

    @abstractmethod
    async def run_scenario_clustering(self, tenant_id: str) -> List[ScenarioPattern]:
        """Scans recent atomic memories and episodic patterns to discover/update T3 Scenarios."""
        pass

    @abstractmethod
    async def update_personal_evolution_profile(
        self,
        user_id: str,
        tenant_id: str,
        trigger_event: Dict[str, Any],
    ) -> PersonalEvolutionProfile:
        """Triggers adaptive style or cost updates on the user's T4 Personal Evolution Profile (PEP)."""
        pass

    @abstractmethod
    async def update_working_context_node(
        self,
        task_id: UUID,
        node: WorkingContextNode,
    ) -> None:
        """Dynamically inserts or updates a node in the live T0 working context graph."""
        pass


class RetrievalAPI(ABC):
    """Primary retrieval service interfacing with TencentDB Agent Memory and graph indices."""

    @abstractmethod
    async def query_hybrid_memory(
        self,
        tenant_id: str,
        query_text: str,
        query_embedding: List[float],
        pep: PersonalEvolutionProfile,
        limit: int = 10,
    ) -> List[AtomicMemory]:
        """Executes a hybrid retrieval across TencentDB applying PEP scoring preferences."""
        pass

    @abstractmethod
    async def retrieve_active_working_context(self, task_id: UUID) -> WorkingContextGraph:
        """Fetches the in-memory T0 symbolic graph for a running task."""
        pass

    @abstractmethod
    async def retrieve_matched_scenarios(
        self,
        tenant_id: str,
        pattern_type: str,
    ) -> List[ScenarioPattern]:
        """Finds workflows and templates in T3 Scenarios matching the current task context."""
        pass

    def score_memory_item(
        self,
        semantic_sim: float,
        bm25_score: float,
        entity_overlap: float,
        temporal_proximity: float,
        graph_proximity: float,
        confidence: float,
        mode: CostMode,
    ) -> float:
        """Calculates a unified hybrid memory retrieval score.

        Weights are dynamically tuned based on the specified CostMode:
        - max_quality: priorizes comprehensive context, high semantic match, and deep confidence.
        - balanced: even weighting across factors with short-horizon decay.
        - fast_cheap: prioritizes temporal/graph proximity to reduce retrieval depth and token load.
        """
        # Define weights per cost mode
        if mode == CostMode.MAX_QUALITY:
            w_semantic = 0.40
            w_bm25 = 0.15
            w_entity = 0.15
            w_temporal = 0.05
            w_graph = 0.10
            w_confidence = 0.15
        elif mode == CostMode.FAST_CHEAP:
            # Under fast_cheap, we emphasize temporal and graph locality (recent and related)
            w_semantic = 0.15
            w_bm25 = 0.10
            w_entity = 0.10
            w_temporal = 0.35
            w_graph = 0.25
            w_confidence = 0.05
        else:  # CostMode.BALANCED
            w_semantic = 0.30
            w_bm25 = 0.15
            w_entity = 0.15
            w_temporal = 0.15
            w_graph = 0.15
            w_confidence = 0.10

        score = (
            (semantic_sim * w_semantic)
            + (bm25_score * w_bm25)
            + (entity_overlap * w_entity)
            + (temporal_proximity * w_temporal)
            + (graph_proximity * w_graph)
            + (confidence * w_confidence)
        )
        return float(score)


class CheckpointManager(ABC):
    """Orchestrates crash-recovery checkpoints, storing hot state in Redis and snapshots in Durable DB."""

    @abstractmethod
    async def create_checkpoint(
        self,
        task_id: UUID,
        graph: WorkingContextGraph,
        agent_cursors: Dict[str, Any],
        episodic_offset: int,
    ) -> bool:
        """Saves highly-frequent state to Redis and schedules an asynchronous snapshot to Durable DB."""
        pass

    @abstractmethod
    async def recover_state(self, task_id: UUID) -> Optional[Dict[str, Any]]:
        """Restores the complete task state, loading from Redis (or falling back to Durable DB).

        Returns:
            A dictionary containing:
            - 'working_graph': WorkingContextGraph
            - 'agent_cursors': Dict[str, Any]
            - 'episodic_offset': int
        """
        pass
