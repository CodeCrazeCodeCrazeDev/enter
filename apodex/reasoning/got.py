from __future__ import annotations
from typing import List, Dict, Any, Optional


class ThoughtNode:
    """Represents a discrete thought/hypothesis branching point in Graph-of-Thought (GoT)."""

    def __init__(self, thought_id: str, content: str, score: float, parent_ids: Optional[List[str]] = None) -> None:
        self.thought_id = thought_id
        self.content = content
        self.score = score
        self.parent_ids = parent_ids or []
        self.status = "active"  # active, pruned, merged


class GraphOfThoughtEngine:
    """Core Graph-of-Thought (GoT) search engine supporting branching, backtracking, and thought-merging."""

    def __init__(self) -> None:
        self.thoughts: Dict[str, ThoughtNode] = {}

    def add_thought(self, node: ThoughtNode) -> None:
        self.thoughts[node.thought_id] = node

    def prune_branch(self, thought_id: str) -> None:
        """Recursively prune a thought and all its descendants."""
        if thought_id not in self.thoughts:
            return

        node = self.thoughts[thought_id]
        node.status = "pruned"

        # Find and prune children recursively
        for child_id, child in self.thoughts.items():
            if thought_id in child.parent_ids:
                self.prune_branch(child_id)

    def merge_thoughts(self, merged_id: str, content: str, parent_ids: List[str]) -> ThoughtNode:
        """Merge multiple thoughts into a consolidated synthesis with averaged score."""
        valid_parents = [self.thoughts[pid] for pid in parent_ids if pid in self.thoughts]
        if not valid_parents:
            score = 0.5
        else:
            score = sum(p.score for p in valid_parents) / len(valid_parents)

        merged_node = ThoughtNode(
            thought_id=merged_id,
            content=content,
            score=score,
            parent_ids=parent_ids
        )
        merged_node.status = "active"
        self.add_thought(merged_node)

        # Update parent states to show they are merged
        for pid in parent_ids:
            if pid in self.thoughts:
                self.thoughts[pid].status = "merged"

        return merged_node

    def get_active_leaves(self) -> List[ThoughtNode]:
        """Find all active leaf thoughts (thoughts that are active and have no active children)."""
        active_nodes = [t for t in self.thoughts.values() if t.status == "active"]
        leaves = []

        for node in active_nodes:
            # Check if this node has any active children
            has_active_child = False
            for potential_child in self.thoughts.values():
                if potential_child.status == "active" and node.thought_id in potential_child.parent_ids:
                    has_active_child = True
                    break
            if not has_active_child:
                leaves.append(node)

        return leaves
