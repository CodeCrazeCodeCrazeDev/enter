"""Implementations of physical storage adapters backing CMOS.

Provides local InMemory memory repositories and persistent SQLite repositories.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Dict, List, Optional
from pydantic import ValidationError

from apodex.memory.cmos.models import MemoryNode, MemoryEdge, CMOSNodeType, CMOSEdgeType, NodeState, ProvenanceBlock
from apodex.memory.cmos.interfaces import MemoryRepository


class InMemoryMemoryRepository(MemoryRepository):
    """Simple in-memory dictionary-backed store for testing and fast runs."""

    def __init__(self) -> None:
        self.nodes: Dict[str, MemoryNode] = {}
        self.edges: List[MemoryEdge] = []

    async def save_node(self, node: MemoryNode) -> None:
        self.nodes[node.node_id] = node

    async def get_node(self, node_id: str) -> Optional[MemoryNode]:
        return self.nodes.get(node_id)

    async def delete_node(self, node_id: str) -> None:
        self.nodes.pop(node_id, None)
        # Cascade delete edges
        self.edges = [e for e in self.edges if e.source_id != node_id and e.target_id != node_id]

    async def save_edge(self, edge: MemoryEdge) -> None:
        # Enforce Referential Integrity
        if edge.source_id not in self.nodes or edge.target_id not in self.nodes:
            raise ValueError(f"Referential Integrity broken: Source {edge.source_id} or Target {edge.target_id} does not exist.")
        self.edges.append(edge)

    async def get_edges(self, source_id: str) -> List[MemoryEdge]:
        return [e for e in self.edges if e.source_id == source_id]

    async def query_nodes(self, filters: Dict[str, Any]) -> List[MemoryNode]:
        results = []
        for node in self.nodes.values():
            match = True
            for k, v in filters.items():
                if hasattr(node, k) and getattr(node, k) == v:
                    continue
                elif k in node.metadata and node.metadata[k] == v:
                    continue
                else:
                    match = False
                    break
            if match:
                results.append(node)
        return results


class SQLiteMemoryRepository(MemoryRepository):
    """Durable, persistent SQLite-backed relational Memory Repository."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._get_conn() as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cmos_nodes (
                    node_id TEXT PRIMARY KEY,
                    node_type TEXT NOT NULL,
                    state TEXT NOT NULL,
                    label TEXT NOT NULL,
                    content TEXT NOT NULL,
                    utility REAL NOT NULL,
                    retrieval_count INTEGER NOT NULL,
                    last_retrieved_at TEXT NOT NULL,
                    provenance TEXT NOT NULL,
                    metadata TEXT NOT NULL
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cmos_edges (
                    edge_id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    edge_type TEXT NOT NULL,
                    strength REAL NOT NULL,
                    provenance TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    FOREIGN KEY (source_id) REFERENCES cmos_nodes(node_id) ON DELETE CASCADE,
                    FOREIGN KEY (target_id) REFERENCES cmos_nodes(node_id) ON DELETE CASCADE
                );
            """)
            conn.commit()

    async def save_node(self, node: MemoryNode) -> None:
        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO cmos_nodes
                (node_id, node_type, state, label, content, utility, retrieval_count, last_retrieved_at, provenance, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    node.node_id,
                    node.node_type.value,
                    node.state.value,
                    node.label,
                    node.content,
                    node.utility,
                    node.retrieval_count,
                    node.last_retrieved_at.isoformat(),
                    node.provenance.model_dump_json(),
                    json.dumps(node.metadata),
                ),
            )
            conn.commit()

    async def get_node(self, node_id: str) -> Optional[MemoryNode]:
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT node_id, node_type, state, label, content, utility, retrieval_count, last_retrieved_at, provenance, metadata FROM cmos_nodes WHERE node_id = ?",
                (node_id,),
            ).fetchone()
            if not row:
                return None
            return MemoryNode(
                node_id=row[0],
                node_type=CMOSNodeType(row[1]),
                state=NodeState(row[2]),
                label=row[3],
                content=row[4],
                utility=row[5],
                retrieval_count=row[6],
                last_retrieved_at=row[7],
                provenance=ProvenanceBlock.model_validate_json(row[8]),
                metadata=json.loads(row[9]),
            )

    async def delete_node(self, node_id: str) -> None:
        with self._get_conn() as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute("DELETE FROM cmos_nodes WHERE node_id = ?", (node_id,))
            conn.commit()

    async def save_edge(self, edge: MemoryEdge) -> None:
        with self._get_conn() as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            try:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO cmos_edges
                    (edge_id, source_id, target_id, edge_type, strength, provenance, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        edge.edge_id,
                        edge.source_id,
                        edge.target_id,
                        edge.edge_type.value,
                        edge.strength,
                        edge.provenance.model_dump_json(),
                        json.dumps(edge.metadata),
                    ),
                )
                conn.commit()
            except sqlite3.IntegrityError as err:
                raise ValueError(f"Referential Integrity broken: {err}")

    async def get_edges(self, source_id: str) -> List[MemoryEdge]:
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT edge_id, source_id, target_id, edge_type, strength, provenance, metadata FROM cmos_edges WHERE source_id = ?",
                (source_id,),
            ).fetchall()
            edges = []
            for r in rows:
                edges.append(
                    MemoryEdge(
                        edge_id=r[0],
                        source_id=r[1],
                        target_id=r[2],
                        edge_type=CMOSEdgeType(r[3]),
                        strength=r[4],
                        provenance=ProvenanceBlock.model_validate_json(r[5]),
                        metadata=json.loads(r[6]),
                    )
                )
            return edges

    async def query_nodes(self, filters: Dict[str, Any]) -> List[MemoryNode]:
        query = "SELECT node_id, node_type, state, label, content, utility, retrieval_count, last_retrieved_at, provenance, metadata FROM cmos_nodes"
        params = []
        if filters:
            conditions = []
            for k, v in filters.items():
                if k in ["node_type", "state", "label"]:
                    conditions.append(f"{k} = ?")
                    params.append(v)
                # metadata matching can be handled post-query for simplification
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        with self._get_conn() as conn:
            rows = conn.execute(query, params).fetchall()
            results = []
            for row in rows:
                node = MemoryNode(
                    node_id=row[0],
                    node_type=CMOSNodeType(row[1]),
                    state=NodeState(row[2]),
                    label=row[3],
                    content=row[4],
                    utility=row[5],
                    retrieval_count=row[6],
                    last_retrieved_at=row[7],
                    provenance=ProvenanceBlock.model_validate_json(row[8]),
                    metadata=json.loads(row[9]),
                )
                # Apply metadata post-filtering
                meta_match = True
                for k, v in filters.items():
                    if k not in ["node_type", "state", "label"]:
                        if k not in node.metadata or node.metadata[k] != v:
                            meta_match = False
                            break
                if meta_match:
                    results.append(node)
            return results
