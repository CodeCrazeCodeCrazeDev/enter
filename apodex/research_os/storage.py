from __future__ import annotations
import collections
from uuid import UUID
from typing import Any, Dict, List, Optional, Type, TypeVar
from pydantic import BaseModel
from .models import (
    BaseArtifact,
    ResearchProject,
    Publication,
    LiteratureCorpus,
    ExperimentResult,
    ClaimNode,
    EvidenceNode,
    ConceptNode,
    TheoryNode,
    ContradictionNode,
)

T = TypeVar("T", bound=BaseArtifact)

# =====================================================================
# Physical Storage Abstractions
# =====================================================================

class DocumentStore:
    """Stores full text and serializations of immutable scientific artifacts."""
    def __init__(self) -> None:
        self._store: Dict[UUID, BaseArtifact] = {}

    def put(self, uuid: UUID, doc: BaseArtifact) -> None:
        self._store[uuid] = doc

    def get(self, uuid: UUID) -> Optional[BaseArtifact]:
        return self._store.get(uuid)

    def list_all(self) -> List[BaseArtifact]:
        return list(self._store.values())


class VectorDB:
    """Simple in-memory vector similarity index (simulated using Jaccard text overlap)."""
    def __init__(self) -> None:
        self._index: Dict[UUID, str] = {}

    def upsert(self, uuid: UUID, text: str) -> None:
        self._index[uuid] = text.lower()

    def search(self, query: str, limit: int = 5) -> List[UUID]:
        query_words = set(query.lower().split())
        if not query_words:
            return list(self._index.keys())[:limit]

        scores = []
        for uuid, text in self._index.items():
            text_words = set(text.split())
            intersection = query_words.intersection(text_words)
            union = query_words.union(text_words)
            jaccard = len(intersection) / len(union) if union else 0.0
            scores.append((uuid, jaccard))

        # Sort by Jaccard overlap descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return [uuid for uuid, score in scores if score > 0.0][:limit]


class RelationalDB:
    """Manages tabular mappings, active running states, funding, and indexes."""
    def __init__(self) -> None:
        self._tables: Dict[str, Dict[Any, Any]] = collections.defaultdict(dict)

    def insert(self, table: str, key: Any, value: Any) -> None:
        self._tables[table][key] = value

    def query_table(self, table: str) -> Dict[Any, Any]:
        return self._tables[table]


class ArtifactStore:
    """Simulates binary store for high-volume datasets or model weights."""
    def __init__(self) -> None:
        self._blobs: Dict[UUID, bytes] = {}

    def save_binary(self, uuid: UUID, data: bytes) -> None:
        self._blobs[uuid] = data

    def load_binary(self, uuid: UUID) -> Optional[bytes]:
        return self._blobs.get(uuid)


class PhysicalKnowledgeGraph:
    """Physical representation of the evolving scientific understanding."""
    def __init__(self) -> None:
        self.nodes: Dict[UUID, BaseArtifact] = {}
        # adjacency list: source_uuid -> list of (target_uuid, relationship_type)
        self.edges: Dict[UUID, List[tuple[UUID, str]]] = collections.defaultdict(list)

    def add_node(self, node: BaseArtifact) -> None:
        self.nodes[node.uuid] = node

    def add_edge(self, source: UUID, target: UUID, rel_type: str) -> None:
        if source in self.nodes and target in self.nodes:
            self.edges[source].append((target, rel_type))


# =====================================================================
# The Decoupled Repository Layer
# =====================================================================

class ResearchRepository:
    """
    Decoupled Repository Proxy acting as the single gateway for workflows and plugins.
    Intelligently routes reads and writes to physical storage subsystems.
    """

    def __init__(self) -> None:
        self.doc_store = DocumentStore()
        self.vector_db = VectorDB()
        self.relational_db = RelationalDB()
        self.artifact_store = ArtifactStore()
        self.kg = PhysicalKnowledgeGraph()

    def save_artifact(self, artifact: BaseArtifact) -> None:
        """Saves and indexes any immutable research artifact, automatically routing to proper backends."""
        uuid = artifact.uuid

        # 1. Save globally to document store
        self.doc_store.put(uuid, artifact)

        # 2. Add to Relational DB maps by class name
        self.relational_db.insert("by_type", uuid, artifact)

        # 3. Vector DB index logic for documents/literature
        if isinstance(artifact, Publication):
            self.vector_db.upsert(uuid, f"{artifact.title} {artifact.content}")
        elif isinstance(artifact, LiteratureCorpus):
            content = " ".join(artifact.paper_titles) + " " + " ".join(artifact.abstracts)
            self.vector_db.upsert(uuid, content)

        # 4. Routing to Physical Knowledge Graph for ontological artifacts
        if isinstance(artifact, (ClaimNode, EvidenceNode, ConceptNode, TheoryNode, ContradictionNode)):
            self.kg.add_node(artifact)

            # Automatically establish ontologies
            if isinstance(artifact, ClaimNode):
                for evidence_uuid in artifact.evidence_ids:
                    self.kg.add_edge(artifact.uuid, evidence_uuid, "GROUNDED_IN")
            elif isinstance(artifact, TheoryNode):
                for claim_uuid in artifact.linked_claims:
                    self.kg.add_edge(artifact.uuid, claim_uuid, "SUPPORTS")

        # 5. Routing heavy result payloads to binary storage
        if isinstance(artifact, ExperimentResult):
            serialized_logs = "\n".join(artifact.logs).encode("utf-8")
            self.artifact_store.save_binary(uuid, serialized_logs)

    def get_artifact(self, uuid: UUID) -> Optional[BaseArtifact]:
        return self.doc_store.get(uuid)

    def list_artifacts_by_type(self, cls: Type[T]) -> List[T]:
        """Queries Relational index to return all artifacts matching a given class."""
        all_artifacts = self.relational_db.query_table("by_type")
        return [art for art in all_artifacts.values() if isinstance(art, cls)]

    def get_lineage_tree(self, uuid: UUID) -> List[BaseArtifact]:
        """Traverses backwards through parents, building a list representing the lineage trace."""
        tree = []
        visited = set()

        def _trace(curr_uuid: UUID) -> None:
            if curr_uuid in visited:
                return
            visited.add(curr_uuid)
            art = self.get_artifact(curr_uuid)
            if art:
                tree.append(art)
                for parent_uuid in art.lineage_parent_uuids:
                    _trace(parent_uuid)

        _trace(uuid)
        return tree

    def search_papers(self, query: str, limit: int = 5) -> List[BaseArtifact]:
        """Queries vector index, returning full documents matching query."""
        matching_uuids = self.vector_db.search(query, limit)
        results = []
        for uuid in matching_uuids:
            art = self.get_artifact(uuid)
            if art:
                results.append(art)
        return results
