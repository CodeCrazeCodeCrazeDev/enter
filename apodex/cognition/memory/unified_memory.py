from __future__ import annotations
import logging
import math
from typing import List, Dict, Any, Optional, Set
import uuid

from apodex.cognition.shared.schemas import (
    StrategicGoal,
    Hypothesis,
    EvidenceCard,
    DecisionProvenance,
    Lesson
)

logger = logging.getLogger("apodex.cognition.memory")


class MemoryNode:
    """Represents a unified memory node in our structural semantic knowledge/episodic store."""
    def __init__(
        self,
        node_id: uuid.UUID,
        category: str,  # 'working', 'episodic', 'semantic', 'procedural'
        content: Dict[str, Any],
        confidence: float = 1.0,
        timestamp: float = 0.0,
        provenance_source: str = "unspecified"
    ) -> None:
        self.node_id = node_id
        self.category = category
        self.content = content
        self.confidence = confidence
        self.timestamp = timestamp
        self.provenance_source = provenance_source


class UnifiedMemory:
    """
    The Single Memory Engine for AEAN, EIOS, and EOS (Redesigned).
    Upgraded for 5-Year continuous operational resilience:
    1. Active memory consolidation & recall reinforcement loops (offsetting infinite Ebbinghaus decay).
    2. Numerical overflow/underflow safe temporal limits.
    3. High-throughput Jaccard context lookup.
    """

    def __init__(self) -> None:
        self.provenance_records: Dict[uuid.UUID, DecisionProvenance] = {}
        self.evidence_pool: Dict[uuid.UUID, EvidenceCard] = {}
        self.hypotheses_pool: Dict[uuid.UUID, Hypothesis] = {}
        self.goals_pool: Dict[uuid.UUID, StrategicGoal] = {}
        self.lessons_pool: List[Lesson] = []

        # Advanced multi-tier collections
        self.memory_nodes: Dict[uuid.UUID, MemoryNode] = {}
        self.decay_rate: float = 0.005

    def clear(self) -> None:
        self.provenance_records.clear()
        self.evidence_pool.clear()
        self.hypotheses_pool.clear()
        self.goals_pool.clear()
        self.lessons_pool.clear()
        self.memory_nodes.clear()

    # --- Standard backward-compatible API ---
    def add_goal(self, goal: StrategicGoal) -> None:
        self.goals_pool[goal.id] = goal
        self.register_node(goal.id, "working", {"title": goal.title, "description": goal.description})

    def get_goal(self, goal_id: uuid.UUID) -> Optional[StrategicGoal]:
        return self.goals_pool.get(goal_id)

    def get_all_goals(self) -> List[StrategicGoal]:
        return list(self.goals_pool.values())

    def add_hypothesis(self, hyp: Hypothesis) -> None:
        self.hypotheses_pool[hyp.id] = hyp
        self.register_node(hyp.id, "semantic", {"statement": hyp.statement, "confidence": hyp.confidence})

    def get_hypotheses_for_goal(self, goal_id: uuid.UUID) -> List[Hypothesis]:
        return [h for h in self.hypotheses_pool.values() if h.goal_id == goal_id]

    def add_evidence(self, ev: EvidenceCard) -> None:
        self.evidence_pool[ev.id] = ev
        self.register_node(ev.id, "episodic", {"source": ev.source, "description": ev.description}, confidence=ev.reliability)

    def get_all_evidence(self) -> List[EvidenceCard]:
        return list(self.evidence_pool.values())

    def add_provenance(self, prov: DecisionProvenance) -> None:
        self.provenance_records[prov.id] = prov
        self.register_node(prov.id, "episodic", {"decision": prov.final_decision, "objective": prov.objective.title})

    def get_provenance(self, prov_id: uuid.UUID) -> Optional[DecisionProvenance]:
        return self.provenance_records.get(prov_id)

    def get_all_provenance(self) -> List[DecisionProvenance]:
        return list(self.provenance_records.values())

    def add_lesson(self, lesson: Lesson) -> None:
        self.lessons_pool.append(lesson)
        self.register_node(uuid.uuid4(), "procedural", {"summary": lesson.summary, "action": lesson.context})

    def get_lessons_by_category(self, category: str) -> List[Lesson]:
        return [L for L in self.lessons_pool if L.category == category]

    def get_all_lessons(self) -> List[Lesson]:
        return list(self.lessons_pool)

    # --- Phase 4 Advanced Memory Capabilities ---
    def register_node(
        self,
        node_id: uuid.UUID,
        category: str,
        content: Dict[str, Any],
        confidence: float = 1.0,
        timestamp: float = 0.0,
        provenance_source: str = "unspecified"
    ) -> MemoryNode:
        node = MemoryNode(node_id, category, content, confidence, timestamp, provenance_source)
        self.memory_nodes[node_id] = node
        return node

    def retrieve_similar_evidence(self, query: str, threshold: float = 0.1) -> List[EvidenceCard]:
        """High-throughput Jaccard overlap lookup."""
        def get_tokens(text: str) -> Set[str]:
            return {w.strip(".,;:?!()\"'").lower() for w in text.split() if len(w) > 2}

        query_tokens = get_tokens(query)
        if not query_tokens:
            return []

        scored_evidence = []
        for ev in self.get_all_evidence():
            ev_tokens = get_tokens(ev.description)
            if not ev_tokens:
                continue

            intersection = query_tokens.intersection(ev_tokens)
            union = query_tokens.union(ev_tokens)
            jaccard = len(intersection) / len(union)

            if jaccard >= threshold:
                # Active memory retrieval reinforcement loop:
                # Whenever a memory is successfully retrieved, we boost its node confidence to offset Ebbinghaus decay
                if ev.id in self.memory_nodes:
                    node = self.memory_nodes[ev.id]
                    node.confidence = min(1.0, node.confidence * 1.3)
                    ev.reliability = node.confidence

                scored_evidence.append((jaccard, ev))

        scored_evidence.sort(key=lambda x: x[0], reverse=True)
        return [ev for _, ev in scored_evidence]

    def consolidate_beliefs_and_decay(self, current_timestamp: float) -> None:
        """Applies Ebbinghaus forgetting curve decay, protected against overflow limits."""
        logger.info(f"Consolidating memory nodes and applying Ebbinghaus forgetting at timestamp: {current_timestamp}")
        for node in self.memory_nodes.values():
            delta_t = max(0.0, current_timestamp - node.timestamp)
            # Safe temporal bound to prevent exponent overflow/underflow under 5-year execution
            delta_t_safe = min(100000.0, delta_t)

            decay_factor = math.exp(-self.decay_rate * delta_t_safe)
            node.confidence = max(0.05, node.confidence * decay_factor)

            if node.category == "semantic" and node.node_id in self.hypotheses_pool:
                self.hypotheses_pool[node.node_id].confidence = node.confidence
            elif node.category == "episodic" and node.node_id in self.evidence_pool:
                self.evidence_pool[node.node_id].reliability = node.confidence
