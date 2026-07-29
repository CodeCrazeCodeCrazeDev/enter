"""Graph-of-Thought (GoT) Reasoning and World Model Modules for AgentHarness v2.

Allows branching, merging, and pruning of thought nodes, and maintains causal,
entity, temporal, knowledge, and uncertainty graphs for reasoning.
"""

from __future__ import annotations

from typing import Any


class ThoughtNode:
    """A single node representing a thought, strategy, or partial conclusion in the reasoning graph."""

    def __init__(self, node_id: str, content: str, score: float = 1.0, metadata: dict[str, Any] | None = None) -> None:
        self.node_id = node_id
        self.content = content
        self.score = score
        self.metadata = metadata or {}
        self.is_pruned = False


class ThoughtGraph:
    """Manages ThoughtNodes and their relationships (dependencies as edges)."""

    def __init__(self) -> None:
        self.nodes: dict[str, ThoughtNode] = {}
        self.edges: dict[str, list[str]] = {}  # source -> targets (dependencies)

    def add_thought(self, node_id: str, content: str, score: float = 1.0, metadata: dict[str, Any] | None = None) -> ThoughtNode:
        node = ThoughtNode(node_id, content, score, metadata)
        self.nodes[node_id] = node
        if node_id not in self.edges:
            self.edges[node_id] = []
        return node

    def add_dependency(self, source_id: str, target_id: str) -> None:
        """Adds a directed edge indicating that target_id depends on source_id."""
        if source_id in self.nodes and target_id in self.nodes:
            self.edges[source_id].append(target_id)

    def prune_branch(self, node_id: str) -> None:
        """Prunes a node and recursively prunes all downstream dependencies."""
        if node_id in self.nodes:
            self.nodes[node_id].is_pruned = True
            for dependent_id in self.edges.get(node_id, []):
                self.prune_branch(dependent_id)

    def merge_thoughts(self, source_ids: list[str], target_id: str) -> None:
        """Merges multiple verified thoughts as dependencies of a new unified target thought."""
        for src in source_ids:
            self.add_dependency(src, target_id)

    def get_valid_thoughts(self) -> list[ThoughtNode]:
        """Returns all thoughts that have not been pruned."""
        return [node for node in self.nodes.values() if not node.is_pruned]


class WorldModelRepresentation:
    """Conceptual continuously evolving World Model representing conceptual causal, temporal, knowledge and entity graphs."""

    def __init__(self, memory_manager: Any, task_id: str) -> None:
        self.mem = memory_manager
        self.task_id = task_id

    def add_knowledge(self, concept: str, relation: str, related_concept: str, confidence: float = 1.0) -> None:
        self.mem.store_world_relation(
            self.task_id, "knowledge", concept, relation, related_concept, 1.0 - confidence, "WorldModelUpdate"
        )

    def add_causal_link(self, cause: str, effect: str, weight: float = 1.0) -> None:
        self.mem.store_world_relation(
            self.task_id, "causal", cause, "causes", effect, 1.0 - weight, "CausalAnalysis"
        )

    def add_temporal_sequence(self, event_a: str, relation: str, event_b: str) -> None:
        self.mem.store_world_relation(
            self.task_id, "temporal", event_a, relation, event_b, 0.0, "TemporalTimeline"
        )

    def get_world_snapshot(self) -> list[dict[str, Any]]:
        return self.mem.retrieve_world_relations(self.task_id)
