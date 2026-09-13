from __future__ import annotations

class ThoughtNode:
    def __init__(self, thought_id: str, content: str, score: float, parent_ids: list[str] | None = None) -> None:
        self.thought_id = thought_id
        self.content = content
        self.score = score
        self.parent_ids = parent_ids or []
        self.status = "active"

class GraphOfThoughtEngine:
    def __init__(self) -> None:
        self.thoughts = {}

    def add_thought(self, node: ThoughtNode) -> None:
        self.thoughts[node.thought_id] = node

    def get_active_leaves(self) -> list[ThoughtNode]:
        # Find all active nodes that are not parents of any other active node
        active_nodes = {tid: node for tid, node in self.thoughts.items() if node.status == "active"}
        parent_ids = set()
        for node in active_nodes.values():
            for pid in node.parent_ids:
                parent_ids.add(pid)
        return [node for tid, node in active_nodes.items() if tid not in parent_ids]

    def prune_branch(self, thought_id: str) -> None:
        if thought_id in self.thoughts:
            self.thoughts[thought_id].status = "pruned"
            # Find any node that has this as parent and prune recursively
            for tid, node in self.thoughts.items():
                if thought_id in node.parent_ids:
                    self.prune_branch(tid)

    def merge_thoughts(self, merged_id: str, content: str, parent_ids: list[str]) -> ThoughtNode:
        scores = [self.thoughts[pid].score for pid in parent_ids if pid in self.thoughts]
        score = sum(scores) / len(scores) if scores else 0.0
        node = ThoughtNode(thought_id=merged_id, content=content, score=score, parent_ids=parent_ids)
        self.add_thought(node)
        return node
