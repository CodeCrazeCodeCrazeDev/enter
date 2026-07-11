"""Unit and integration tests for the Semantic Memory subsystem."""

from __future__ import annotations

import time
import pytest
from agent_harness.core.memory.semantic_memory import (
    Belief,
    EvidenceCard,
    Fact,
    SemanticMemory,
    SQLiteMemoryRepository,
    UnresolvedQuestion,
)


def test_sqlite_semantic_memory():
    # In-memory SQLite to test production repository logic
    repo = SQLiteMemoryRepository(db_path=":memory:")
    memory = SemanticMemory(repository=repo)

    # 1. Evidence Cards
    card = EvidenceCard(
        evidence_id="ev_001",
        source_url="https://apodex.ai/docs",
        content="Apodex model has 35B active parameters.",
        extracted_at=time.time()
    )
    memory.add_evidence(card)
    retrieved_card = memory.retrieve_evidence("ev_001")
    assert retrieved_card is not None
    assert retrieved_card.content == card.content

    # 2. Facts
    fact = Fact(
        fact_id="fact_001",
        assertion="Apodex-1.0 is verification-centric.",
        confidence=0.98,
        evidence_ids=["ev_001"]
    )
    memory.add_fact(fact)
    facts = memory.get_facts()
    assert len(facts) == 1
    assert facts[0].assertion == fact.assertion
    assert facts[0].evidence_ids == ["ev_001"]

    # 3. Beliefs
    belief = Belief(
        belief_id="belief_001",
        hypothesis="Multi-agent architectures reduce token overhead.",
        strength=0.85,
        last_updated=time.time()
    )
    memory.add_belief(belief)
    beliefs = memory.get_beliefs()
    assert len(beliefs) == 1
    assert beliefs[0].hypothesis == belief.hypothesis

    # 4. Unresolved Questions
    question = UnresolvedQuestion(
        question_id="q_001",
        query="What is the precise latency overhead of multi-agent verification?",
        priority=4
    )
    memory.add_question(question)
    questions = memory.get_questions(status="open")
    assert len(questions) == 1
    assert questions[0].priority == 4
