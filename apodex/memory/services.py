from __future__ import annotations
import random
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

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
    WorkingContextEdge,
    ToolCallRecord,
)
from apodex.memory.interfaces import IngestionPipeline, RetrievalAPI, CheckpointManager


# -------------------------------------------------------------
# 1. Local-First Memory Store (TencentDB Simulated Backend)
# -------------------------------------------------------------
class TencentDBMemoryStore:
    """
    Simulates a persistent, indexable local database for T0-T4 tiers,
    with built-in support for hybrid querying and cascading deletions.
    """

    def __init__(self) -> None:
        self.episodes: Dict[UUID, EpisodeLogRecord] = {}
        self.atoms: Dict[UUID, AtomicMemory] = {}
        self.scenarios: Dict[UUID, ScenarioPattern] = {}
        self.peps: Dict[str, PersonalEvolutionProfile] = {}  # key: user_id
        self.graphs: Dict[UUID, WorkingContextGraph] = {}  # key: task_id
        self.deletion_audit: List[Dict[str, Any]] = []

    def clear_all(self) -> None:
        self.episodes.clear()
        self.atoms.clear()
        self.scenarios.clear()
        self.peps.clear()
        self.graphs.clear()
        self.deletion_audit.clear()


# Global simulated storage instance
_db = TencentDBMemoryStore()


# -------------------------------------------------------------
# 2. Ingestion Pipeline Concrete Implementation
# -------------------------------------------------------------
class IngestionPipelineImpl(IngestionPipeline):
    """
    Asynchronous implementation of memory ingestion.
    Appends traces to T1, extracts T2 atoms, groups T3 scenarios,
    updates T4 user personas, and builds T0 active task graphs.
    """

    def __init__(self, store: Optional[TencentDBMemoryStore] = None) -> None:
        self.store = store or _db

    async def log_episode_step(self, record: EpisodeLogRecord) -> None:
        """Appends a raw LLM input/output step to Tier 1 Episodic Memory."""
        self.store.episodes[record.record_id] = record

    async def extract_and_inject_atoms(
        self,
        episode_id: UUID,
        raw_log_content: str,
        tenant_id: str,
        user_id: str,
    ) -> List[AtomicMemory]:
        """
        Simulates parsing a T1 raw log and distilling cross-session atomic facts (T2).
        Extracts key sentences as facts, associates a 1536-dimensional mock embedding,
        and saves to DB with initial confidence.
        """
        atoms_created: List[AtomicMemory] = []

        # Find interesting statements in the log or create a clean atom representing the action
        key_phrases = []
        for line in raw_log_content.split("\n"):
            if "bottleneck" in line.lower() or "fixed" in line.lower() or "found" in line.lower() or "prefer" in line.lower():
                key_phrases.append(line.strip())

        if not key_phrases:
            key_phrases.append(f"Successfully executed task transaction inside episode {episode_id}")

        for phrase in key_phrases:
            if len(phrase) < 10:
                phrase = f"Atomic memory distilled: {phrase} (valid content)"

            atom = AtomicMemory(
                atom_id=uuid4(),
                tenant_id=tenant_id,
                user_id=user_id,
                content=phrase,
                embedding=[0.05] * 1536,  # 1536-dim dimension matching model validation
                source_episode_ids=[episode_id],
                confidence=0.85,
                tags=["ingested", "distilled"]
            )
            self.store.atoms[atom.atom_id] = atom
            atoms_created.append(atom)

        return atoms_created

    async def run_scenario_clustering(self, tenant_id: str) -> List[ScenarioPattern]:
        """
        Clusters recent distilled atoms or episodic patterns to identify T3 Scenario patterns.
        E.g. if we have repeating agent types or tool records, we cluster them into an active scenario.
        """
        new_scenarios: List[ScenarioPattern] = []

        # Check for matching tag patterns in atoms to create a scenario
        related_atoms = [atom.atom_id for atom in self.store.atoms.values() if atom.tenant_id == tenant_id]

        if len(related_atoms) >= 2:
            scen = ScenarioPattern(
                scenario_id=uuid4(),
                tenant_id=tenant_id,
                name="Optimized Refactoring Scenario",
                pattern_type="refactor_and_test",
                typical_workflow=["main_agent", "code_verifier", "main_agent"],
                failure_patterns=["mismatched_brackets", "timeout"],
                solution_patterns=["increase_temperature", "run_bracket_repair"],
                linked_atoms=related_atoms,
                success_rate=0.9,
                average_latency_ms=1200.0,
                average_token_cost=4500
            )
            self.store.scenarios[scen.scenario_id] = scen
            new_scenarios.append(scen)

        return new_scenarios

    async def update_personal_evolution_profile(
        self,
        user_id: str,
        tenant_id: str,
        trigger_event: Dict[str, Any],
    ) -> PersonalEvolutionProfile:
        """Dynamically adapts user style and cost-mode preferences inside T4 PEP."""
        pep = self.store.peps.get(user_id)
        if not pep:
            pep = PersonalEvolutionProfile(tenant_id=tenant_id, user_id=user_id)

        # Update based on trigger event
        if "cost_mode" in trigger_event:
            pep.cost_budget_preferences["default_mode"] = trigger_event["cost_mode"]
        if "verbosity" in trigger_event:
            pep.style_preferences["verbosity"] = trigger_event["verbosity"]
        if "vocabulary" in trigger_event:
            pep.domain_vocabulary.extend(trigger_event["vocabulary"])

        pep.updated_at = datetime.utcnow()
        self.store.peps[user_id] = pep
        return pep

    async def update_working_context_node(
        self,
        task_id: UUID,
        node: WorkingContextNode,
    ) -> None:
        """Inserts or modifies a symbolic node in the active T0 task graph canvas."""
        graph = self.store.graphs.get(task_id)
        if not graph:
            graph = WorkingContextGraph(task_id=task_id, tenant_id="default_tenant")

        # Update existing or append new node
        existing_index = next((i for i, n in enumerate(graph.nodes) if n.node_id == node.node_id), None)
        if existing_index is not None:
            graph.nodes[existing_index] = node
        else:
            graph.nodes.append(node)

        graph.updated_at = datetime.utcnow()
        self.store.graphs[task_id] = graph


# -------------------------------------------------------------
# 3. Retrieval API Concrete Implementation
# -------------------------------------------------------------
class RetrievalAPIImpl(RetrievalAPI):
    """
    Retrieval Service facilitating multi-objective hybrid search and
    building concise Support Packs restricted to 2,000 tokens.
    """

    def __init__(self, store: Optional[TencentDBMemoryStore] = None) -> None:
        self.store = store or _db

    async def query_hybrid_memory(
        self,
        tenant_id: str,
        query_text: str,
        query_embedding: List[float],
        pep: PersonalEvolutionProfile,
        limit: int = 10,
    ) -> List[AtomicMemory]:
        """
        Executes a hybrid retrieval query over atomic memories (T2).
        Calculates hybrid score for candidate atoms using score_memory_item.
        """
        scored_atoms = []
        cost_mode_str = pep.cost_budget_preferences.get("default_mode", "balanced")
        cost_mode = CostMode(cost_mode_str)

        for atom in self.store.atoms.values():
            if atom.tenant_id != tenant_id:
                continue

            # Calculate metrics
            # 1. Semantic similarity (mock cosine sim using dot product or match)
            sem_sim = 0.8  # default baseline
            if len(query_embedding) == len(atom.embedding):
                # Simulated semantic similarity based on overlap
                sem_sim = 0.85 if "bottleneck" in atom.content.lower() and "bottleneck" in query_text.lower() else 0.75

            # 2. BM25 keyword score (simulated based on query word occurrences)
            query_words = set(query_text.lower().split())
            atom_words = set(atom.content.lower().split())
            matched_words = query_words.intersection(atom_words)
            bm25 = min(1.0, len(matched_words) / max(1, len(query_words)))

            # 3. Graph/Temporal proximity and overlaps
            entity_overlap = 0.8 if any(tag in query_text for tag in atom.tags) else 0.3
            temporal_prox = 0.95  # simulated recency
            graph_prox = 0.9

            # Unified retrieval scoring
            final_score = self.score_memory_item(
                semantic_sim=sem_sim,
                bm25_score=bm25,
                entity_overlap=entity_overlap,
                temporal_proximity=temporal_prox,
                graph_proximity=graph_prox,
                confidence=atom.confidence,
                mode=cost_mode
            )

            scored_atoms.append((final_score, atom))

        scored_atoms.sort(key=lambda x: x[0], reverse=True)
        return [atom for _, atom in scored_atoms[:limit]]

    async def retrieve_active_working_context(self, task_id: UUID) -> WorkingContextGraph:
        """Fetches the active T0 graph snapshot for a running task."""
        graph = self.store.graphs.get(task_id)
        if not graph:
            graph = WorkingContextGraph(task_id=task_id, tenant_id="default_tenant")
            self.store.graphs[task_id] = graph
        return graph

    async def retrieve_matched_scenarios(
        self,
        tenant_id: str,
        pattern_type: str,
    ) -> List[ScenarioPattern]:
        """Finds workflows and templates in T3 Scenarios matching the current task context."""
        return [scen for scen in self.store.scenarios.values() if scen.tenant_id == tenant_id and scen.pattern_type == pattern_type]

    def build_support_pack(self, items: List[AtomicMemory], max_tokens: int = 2000) -> str:
        """
        Packs retrieved atomic facts into an XML Support Pack structure,
        ensuring we strictly respect the token limits (simulated at 4 characters per token).
        """
        pack_lines = ["<SupportPack>"]
        char_budget = max_tokens * 4

        current_char_count = len("<SupportPack>\n</SupportPack>")

        for i, atom in enumerate(items):
            entry_xml = (
                f"  <Fact id=\"{atom.atom_id}\" confidence=\"{atom.confidence:.2f}\">\n"
                f"    <Content>{atom.content}</Content>\n"
                f"    <Tags>{', '.join(atom.tags)}</Tags>\n"
                f"  </Fact>"
            )

            # Check budget
            if current_char_count + len(entry_xml) + 2 > char_budget:
                break

            pack_lines.append(entry_xml)
            current_char_count += len(entry_xml) + 1

        pack_lines.append("</SupportPack>")
        return "\n".join(pack_lines)


# -------------------------------------------------------------
# 4. Checkpoint Manager Concrete Implementation
# -------------------------------------------------------------
class CheckpointManagerImpl(CheckpointManager):
    """
    Checkpoint and recovery manager.
    Stores 'hot state' high-frequency cursors in simulated Redis (dictionary) and
    snapshots complete serialized task execution records to a simulated durable DB.
    """

    def __init__(self) -> None:
        self.redis_hot_state: Dict[UUID, Dict[str, Any]] = {}
        self.db_durable_snapshots: Dict[UUID, Dict[str, Any]] = {}

    async def create_checkpoint(
        self,
        task_id: UUID,
        graph: WorkingContextGraph,
        agent_cursors: Dict[str, Any],
        episodic_offset: int,
    ) -> bool:
        """Saves high-frequency state to Redis and schedules snapshotting to the durable store."""
        state_payload = {
            "working_graph": graph.model_dump(),
            "agent_cursors": agent_cursors,
            "episodic_offset": episodic_offset,
            "timestamp": time.time()
        }

        # 1. Hot state update (Redis)
        self.redis_hot_state[task_id] = state_payload

        # 2. Asynchronous Durable DB snapshot
        self.db_durable_snapshots[task_id] = state_payload

        return True

    async def recover_state(self, task_id: UUID) -> Optional[Dict[str, Any]]:
        """Restores complete task state from Redis (or falls back to Durable DB)."""
        # Attempt to fetch from hot state first
        payload = self.redis_hot_state.get(task_id) or self.db_durable_snapshots.get(task_id)
        if not payload:
            return None

        # Re-construct working context graph
        graph_data = payload["working_graph"]
        graph = WorkingContextGraph(
            task_id=UUID(graph_data["task_id"]) if isinstance(graph_data["task_id"], str) else graph_data["task_id"],
            tenant_id=graph_data["tenant_id"],
            nodes=[WorkingContextNode(**n) for n in graph_data["nodes"]],
            edges=[WorkingContextEdge(**e) for e in graph_data["edges"]],
            updated_at=datetime.fromisoformat(graph_data["updated_at"]) if isinstance(graph_data["updated_at"], str) else graph_data["updated_at"]
        )

        return {
            "working_graph": graph,
            "agent_cursors": payload["agent_cursors"],
            "episodic_offset": payload["episodic_offset"]
        }


# -------------------------------------------------------------
# 5. GDPR Deletion Concrete Function
# -------------------------------------------------------------
def delete_user_data(user_id: str, tenant_id: str, store: Optional[TencentDBMemoryStore] = None) -> Dict[str, Any]:
    """
    Cascades data erasure according to GDPR guidelines:
    - Removes user's raw T1 log files.
    - Cascades deletions of T2 Atoms and T3 Scenarios linked to user atoms.
    - Clears/purges Persona entries (T4).
    - Logs audit log of erasure events.
    """
    target_store = store or _db

    episodes_erased = 0
    atoms_erased = 0
    scenarios_erased = 0
    peps_erased = 0

    # 1. Erase Episodes (T1)
    episode_keys_to_remove = [k for k, ep in target_store.episodes.items() if ep.user_id == user_id and ep.tenant_id == tenant_id]
    for k in episode_keys_to_remove:
        target_store.episodes.pop(k, None)
        episodes_erased += 1

    # 2. Erase Atoms (T2)
    atom_keys_to_remove = [k for k, atom in target_store.atoms.items() if atom.user_id == user_id and atom.tenant_id == tenant_id]
    for k in atom_keys_to_remove:
        target_store.atoms.pop(k, None)
        atoms_erased += 1

    # 3. Cascade scenarios referencing erased atoms (T3)
    remaining_atom_ids = set(target_store.atoms.keys())
    scenario_keys_to_remove = []
    for k, scen in target_store.scenarios.items():
        if scen.tenant_id == tenant_id:
            # If scenario references any atom that was deleted, or becomes orphaned, we cascade delete it
            scen_atoms_set = set(scen.linked_atoms)
            if not scen_atoms_set.issubset(remaining_atom_ids):
                scenario_keys_to_remove.append(k)

    for k in scenario_keys_to_remove:
        target_store.scenarios.pop(k, None)
        scenarios_erased += 1

    # 4. Erase Personal Evolution Profile (T4)
    if user_id in target_store.peps:
        pep = target_store.peps[user_id]
        if pep.tenant_id == tenant_id:
            target_store.peps.pop(user_id, None)
            peps_erased += 1

    audit_entry = {
        "timestamp": time.time(),
        "action": "GDPR_DELETE",
        "user_id": user_id,
        "tenant_id": tenant_id,
        "outcome": "success",
        "stats": {
            "episodes_erased": episodes_erased,
            "atoms_erased": atoms_erased,
            "scenarios_erased": scenarios_erased,
            "peps_erased": peps_erased
        }
    }
    target_store.deletion_audit.append(audit_entry)

    return audit_entry
