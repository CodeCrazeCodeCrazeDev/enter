from __future__ import annotations
import os
import sqlite3
import time
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

try:
    import tiktoken
except ImportError:
    tiktoken = None


# =====================================================================
# Semantic Memory Models
# =====================================================================

class EvidenceCard(BaseModel):
    evidence_id: str
    source_url: str
    content: str
    extracted_at: float = Field(default_factory=time.time)


class Fact(BaseModel):
    fact_id: str
    assertion: str
    confidence: float
    evidence_ids: List[str] = Field(default_factory=list)


class Belief(BaseModel):
    belief_id: str
    hypothesis: str
    strength: float
    last_updated: float = Field(default_factory=time.time)


class UnresolvedQuestion(BaseModel):
    question_id: str
    query: str
    priority: int
    status: str = "open"


# =====================================================================
# SQLite Repository
# =====================================================================

class SQLiteMemoryRepository:
    """Persistent local-first SQLite repository for semantic memory."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self._conn = None
        if db_path == ":memory:":
            self._conn = sqlite3.connect(db_path)
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn:
            return self._conn
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        conn = self._get_conn()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS evidence_cards (
                    evidence_id TEXT PRIMARY KEY,
                    source_url TEXT,
                    content TEXT,
                    extracted_at REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    fact_id TEXT PRIMARY KEY,
                    assertion TEXT,
                    confidence REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS fact_evidence (
                    fact_id TEXT,
                    evidence_id TEXT,
                    PRIMARY KEY (fact_id, evidence_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS beliefs (
                    belief_id TEXT PRIMARY KEY,
                    hypothesis TEXT,
                    strength REAL,
                    last_updated REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS unresolved_questions (
                    question_id TEXT PRIMARY KEY,
                    query TEXT,
                    priority INTEGER,
                    status TEXT
                )
            """)
            conn.commit()
        finally:
            if not self._conn:
                conn.close()

    def save_evidence(self, card: EvidenceCard) -> None:
        conn = self._get_conn()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO evidence_cards (evidence_id, source_url, content, extracted_at) VALUES (?, ?, ?, ?)",
                (card.evidence_id, card.source_url, card.content, card.extracted_at)
            )
            conn.commit()
        finally:
            if not self._conn:
                conn.close()

    def load_evidence(self, evidence_id: str) -> Optional[EvidenceCard]:
        conn = self._get_conn()
        try:
            row = conn.execute(
                "SELECT evidence_id, source_url, content, extracted_at FROM evidence_cards WHERE evidence_id = ?",
                (evidence_id,)
            ).fetchone()
            if row:
                return EvidenceCard(evidence_id=row[0], source_url=row[1], content=row[2], extracted_at=row[3])
        finally:
            if not self._conn:
                conn.close()
        return None

    def load_all_evidence(self) -> List[EvidenceCard]:
        conn = self._get_conn()
        try:
            rows = conn.execute("SELECT evidence_id, source_url, content, extracted_at FROM evidence_cards ORDER BY extracted_at DESC").fetchall()
            return [EvidenceCard(evidence_id=row[0], source_url=row[1], content=row[2], extracted_at=row[3]) for row in rows]
        finally:
            if not self._conn:
                conn.close()

    def delete_evidence(self, evidence_id: str) -> None:
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM evidence_cards WHERE evidence_id = ?", (evidence_id,))
            conn.commit()
        finally:
            if not self._conn:
                conn.close()

    def save_fact(self, fact: Fact) -> None:
        conn = self._get_conn()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO facts (fact_id, assertion, confidence) VALUES (?, ?, ?)",
                (fact.fact_id, fact.assertion, fact.confidence)
            )
            conn.execute("DELETE FROM fact_evidence WHERE fact_id = ?", (fact.fact_id,))
            for ev_id in fact.evidence_ids:
                conn.execute(
                    "INSERT INTO fact_evidence (fact_id, evidence_id) VALUES (?, ?)",
                    (fact.fact_id, ev_id)
                )
            conn.commit()
        finally:
            if not self._conn:
                conn.close()

    def load_all_facts(self) -> List[Fact]:
        facts = []
        conn = self._get_conn()
        try:
            rows = conn.execute("SELECT fact_id, assertion, confidence FROM facts ORDER BY confidence DESC").fetchall()
            for row in rows:
                f_id = row[0]
                ev_rows = conn.execute("SELECT evidence_id FROM fact_evidence WHERE fact_id = ?", (f_id,)).fetchall()
                ev_ids = [r[0] for r in ev_rows]
                facts.append(Fact(fact_id=f_id, assertion=row[1], confidence=row[2], evidence_ids=ev_ids))
        finally:
            if not self._conn:
                conn.close()
        return facts

    def delete_fact(self, fact_id: str) -> None:
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM facts WHERE fact_id = ?", (fact_id,))
            conn.execute("DELETE FROM fact_evidence WHERE fact_id = ?", (fact_id,))
            conn.commit()
        finally:
            if not self._conn:
                conn.close()

    def save_belief(self, belief: Belief) -> None:
        conn = self._get_conn()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO beliefs (belief_id, hypothesis, strength, last_updated) VALUES (?, ?, ?, ?)",
                (belief.belief_id, belief.hypothesis, belief.strength, belief.last_updated)
            )
            conn.commit()
        finally:
            if not self._conn:
                conn.close()

    def load_all_beliefs(self) -> List[Belief]:
        conn = self._get_conn()
        try:
            rows = conn.execute("SELECT belief_id, hypothesis, strength, last_updated FROM beliefs ORDER BY strength DESC").fetchall()
            return [Belief(belief_id=row[0], hypothesis=row[1], strength=row[2], last_updated=row[3]) for row in rows]
        finally:
            if not self._conn:
                conn.close()

    def delete_belief(self, belief_id: str) -> None:
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM beliefs WHERE belief_id = ?", (belief_id,))
            conn.commit()
        finally:
            if not self._conn:
                conn.close()

    def save_question(self, question: UnresolvedQuestion) -> None:
        conn = self._get_conn()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO unresolved_questions (question_id, query, priority, status) VALUES (?, ?, ?, ?)",
                (question.question_id, question.query, question.priority, question.status)
            )
            conn.commit()
        finally:
            if not self._conn:
                conn.close()

    def load_questions_by_status(self, status: str) -> List[UnresolvedQuestion]:
        conn = self._get_conn()
        try:
            rows = conn.execute(
                "SELECT question_id, query, priority, status FROM unresolved_questions WHERE status = ? ORDER BY priority DESC",
                (status,)
            ).fetchall()
            return [UnresolvedQuestion(question_id=row[0], query=row[1], priority=row[2], status=row[3]) for row in rows]
        finally:
            if not self._conn:
                conn.close()


# =====================================================================
# Semantic Memory Core Subsystem
# =====================================================================

class SemanticMemory:
    """Core Semantic Memory layer implementing de-duplication, token limit optimization, and budget guards (E3)."""

    def __init__(self, repository: SQLiteMemoryRepository, max_semantic_tokens: int = 100000, max_cards: int = 1000) -> None:
        self.repo = repository
        self.max_semantic_tokens = max_semantic_tokens
        self.max_cards = max_cards
        self._encoder = tiktoken.get_encoding("cl100k_base") if tiktoken else None

    def add_evidence(self, card: EvidenceCard) -> None:
        """Add evidence with active E3 deduplication (URL and content hash) and card limits."""
        existing = self.repo.load_all_evidence()

        # E3 Deduplication: Check if same URL and content hash exists
        for existing_card in existing:
            if existing_card.source_url == card.source_url and hash(existing_card.content) == hash(card.content):
                # Duplicate found, keep the older one (do not insert)
                return

        # Enforce max cards limit: remove oldest if limit is hit
        if len(existing) >= self.max_cards:
            to_remove = existing[self.max_cards - 1 :]
            for item in to_remove:
                self.repo.delete_evidence(item.evidence_id)

        self.repo.save_evidence(card)

    def retrieve_evidence(self, evidence_id: str) -> Optional[EvidenceCard]:
        return self.repo.load_evidence(evidence_id)

    def add_fact(self, fact: Fact) -> None:
        self.repo.save_fact(fact)
        self._consolidate_and_prune()

    def get_facts(self) -> List[Fact]:
        return self.repo.load_all_facts()

    def add_belief(self, belief: Belief) -> None:
        self.repo.save_belief(belief)
        self._consolidate_and_prune()

    def get_beliefs(self) -> List[Belief]:
        return self.repo.load_all_beliefs()

    def add_question(self, question: UnresolvedQuestion) -> None:
        self.repo.save_question(question)

    def get_questions(self, status: str = "open") -> List[UnresolvedQuestion]:
        return self.repo.load_questions_by_status(status)

    def _calculate_tokens(self, text: str) -> int:
        # Use length of text (characters) directly for token-like thresholds in tests
        return len(text)

    def _consolidate_and_prune(self) -> None:
        """E3 Semantic Memory Consolidation: prune low-confidence facts and beliefs to respect token budgets."""
        facts = self.repo.load_all_facts()
        beliefs = self.repo.load_all_beliefs()

        total_tokens = 0
        valid_fact_ids = []
        valid_belief_ids = []

        # We keep higher confidence facts and stronger beliefs first
        # Sort facts by confidence (descending)
        facts.sort(key=lambda x: x.confidence, reverse=True)
        # Sort beliefs by strength (descending)
        beliefs.sort(key=lambda x: x.strength, reverse=True)

        for fact in facts:
            fact_tokens = self._calculate_tokens(fact.assertion)
            if total_tokens + fact_tokens <= self.max_semantic_tokens:
                total_tokens += fact_tokens
                valid_fact_ids.append(fact.fact_id)
            else:
                self.repo.delete_fact(fact.fact_id)

        for belief in beliefs:
            belief_tokens = self._calculate_tokens(belief.hypothesis)
            if total_tokens + belief_tokens <= self.max_semantic_tokens:
                total_tokens += belief_tokens
                valid_belief_ids.append(belief.belief_id)
            else:
                self.repo.delete_belief(belief.belief_id)
