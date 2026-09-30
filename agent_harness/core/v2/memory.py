"""Modular Durable Memory Subsystem for AgentHarness v2.

Supports:
- Persistent Semantic Memory (beliefs, verified facts, evidence, unresolved questions, task summaries)
- Long-Term Learning Memory (successful strategies, failed strategies, cross-session retrieval)
- Durable SQLite persistent backend by default (saved to 'logs/agent_harness_v2_memory.db').
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class PersistentMemoryManager:
    """Interchangeable Durable Persistent Storage Layer for semantic & learning memories."""

    def __init__(self, db_path: str | Path = "logs/agent_harness_v2_memory.db") -> None:
        self.db_path = str(db_path)
        # Ensure directories exist for the durable DB
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            self._shared_conn = None
        else:
            self._shared_conn = sqlite3.connect(self.db_path)
            self._shared_conn.row_factory = sqlite3.Row
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        if self._shared_conn is not None:
            return self._shared_conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        conn = self._get_connection()
        # Semantic memory table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS semantic_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                category TEXT NOT NULL, -- 'belief', 'fact', 'evidence', 'question', 'summary'
                content TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Learning memory table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS learning_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_category TEXT NOT NULL,
                strategy TEXT NOT NULL,
                outcome_score REAL NOT NULL,
                tool_performance_json TEXT,
                retrieval_quality REAL,
                planner_performance REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Evolving World Model table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS world_model (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                graph_type TEXT NOT NULL, -- 'knowledge', 'entity', 'causal', 'temporal', 'uncertainty'
                source_entity TEXT NOT NULL,
                relation TEXT NOT NULL,
                target_entity TEXT NOT NULL,
                uncertainty_score REAL DEFAULT 0.0,
                evidence TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        if self._shared_conn is None:
            conn.close()

    # --- Semantic Memory Operations ---

    def store_semantic(
        self, task_id: str, category: str, content: str, confidence: float = 1.0, source: str | None = None,
    ) -> None:
        conn = self._get_connection()
        conn.execute(
            "INSERT INTO semantic_memory (task_id, category, content, confidence, source) VALUES (?, ?, ?, ?, ?)",
            (task_id, category, content, confidence, source),
        )
        conn.commit()
        if self._shared_conn is None:
            conn.close()

    def retrieve_semantic(self, task_id: str, category: str | None = None) -> list[dict[str, Any]]:
        conn = self._get_connection()
        if category:
            cursor = conn.execute(
                "SELECT * FROM semantic_memory WHERE task_id = ? AND category = ? ORDER BY created_at DESC",
                (task_id, category),
            )
        else:
            cursor = conn.execute(
                "SELECT * FROM semantic_memory WHERE task_id = ? ORDER BY created_at DESC",
                (task_id,),
            )
        rows = [dict(row) for row in cursor.fetchall()]
        if self._shared_conn is None:
            conn.close()
        return rows

    # --- Long-Term Learning Memory Operations ---

    def store_learning_strategy(
        self,
        task_category: str,
        strategy: str,
        outcome_score: float,
        tool_performance: dict[str, Any] | None = None,
        retrieval_quality: float = 1.0,
        planner_performance: float = 1.0,
    ) -> None:
        conn = self._get_connection()
        conn.execute(
            "INSERT INTO learning_memory (task_category, strategy, outcome_score, tool_performance_json, retrieval_quality, planner_performance) VALUES (?, ?, ?, ?, ?, ?)",
            (
                task_category,
                strategy,
                outcome_score,
                json.dumps(tool_performance or {}),
                retrieval_quality,
                planner_performance,
            ),
        )
        conn.commit()
        if self._shared_conn is None:
            conn.close()

    def retrieve_learning_strategies(self, task_category: str) -> list[dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT * FROM learning_memory WHERE task_category = ? ORDER BY outcome_score DESC",
            (task_category,),
        )
        results = []
        for row in cursor.fetchall():
            d = dict(row)
            d["tool_performance"] = json.loads(d.pop("tool_performance_json") or "{}")
            results.append(d)
        if self._shared_conn is None:
            conn.close()
        return results

    # --- World Model Graph Operations ---

    def store_world_relation(
        self,
        task_id: str,
        graph_type: str,
        source: str,
        relation: str,
        target: str,
        uncertainty: float = 0.0,
        evidence: str | None = None,
    ) -> None:
        conn = self._get_connection()
        conn.execute(
            "INSERT INTO world_model (task_id, graph_type, source_entity, relation, target_entity, uncertainty_score, evidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (task_id, graph_type, source, relation, target, uncertainty, evidence),
        )
        conn.commit()
        if self._shared_conn is None:
            conn.close()

    def retrieve_world_relations(self, task_id: str, graph_type: str | None = None) -> list[dict[str, Any]]:
        conn = self._get_connection()
        if graph_type:
            cursor = conn.execute(
                "SELECT * FROM world_model WHERE task_id = ? AND graph_type = ?",
                (task_id, graph_type),
            )
        else:
            cursor = conn.execute(
                "SELECT * FROM world_model WHERE task_id = ?",
                (task_id,),
            )
        rows = [dict(row) for row in cursor.fetchall()]
        if self._shared_conn is None:
            conn.close()
        return rows
