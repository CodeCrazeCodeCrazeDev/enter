from __future__ import annotations

from apodex.reasoning.got import GraphOfThoughtEngine, ThoughtNode


def _engine_with_chain() -> GraphOfThoughtEngine:
    """root -> child -> grandchild linear chain."""
    engine = GraphOfThoughtEngine()
    engine.add_thought(ThoughtNode("root", "root idea", 0.9))
    engine.add_thought(ThoughtNode("child", "child idea", 0.8, parent_ids=["root"]))
    engine.add_thought(ThoughtNode("grandchild", "grandchild idea", 0.7, parent_ids=["child"]))
    return engine


def test_thought_node_defaults():
    node = ThoughtNode("t1", "content", 0.5)
    assert node.parent_ids == []
    assert node.status == "active"


def test_add_thought_registers_node():
    engine = GraphOfThoughtEngine()
    node = ThoughtNode("t1", "content", 0.5)
    engine.add_thought(node)
    assert engine.thoughts["t1"] is node


def test_prune_branch_recursively_prunes_descendants():
    engine = _engine_with_chain()
    engine.prune_branch("root")
    assert engine.thoughts["root"].status == "pruned"
    assert engine.thoughts["child"].status == "pruned"
    assert engine.thoughts["grandchild"].status == "pruned"


def test_prune_branch_only_affects_subtree():
    engine = GraphOfThoughtEngine()
    engine.add_thought(ThoughtNode("root", "root", 0.9))
    engine.add_thought(ThoughtNode("a", "a", 0.8, parent_ids=["root"]))
    engine.add_thought(ThoughtNode("b", "b", 0.8, parent_ids=["root"]))
    engine.prune_branch("a")
    assert engine.thoughts["a"].status == "pruned"
    assert engine.thoughts["b"].status == "active"
    assert engine.thoughts["root"].status == "active"


def test_prune_branch_unknown_id_is_noop():
    engine = _engine_with_chain()
    engine.prune_branch("does-not-exist")
    assert all(n.status == "active" for n in engine.thoughts.values())


def test_merge_thoughts_averages_parent_scores():
    engine = GraphOfThoughtEngine()
    engine.add_thought(ThoughtNode("p1", "p1", 0.6))
    engine.add_thought(ThoughtNode("p2", "p2", 0.8))
    merged = engine.merge_thoughts("m", "synthesis", ["p1", "p2"])
    assert merged.score == 0.7
    assert merged.status == "active"
    assert engine.thoughts["p1"].status == "merged"
    assert engine.thoughts["p2"].status == "merged"
    assert engine.thoughts["m"] is merged


def test_merge_thoughts_with_no_valid_parents_defaults_score():
    engine = GraphOfThoughtEngine()
    merged = engine.merge_thoughts("m", "synthesis", ["missing"])
    assert merged.score == 0.5


def test_get_active_leaves_returns_leaf_nodes_only():
    engine = _engine_with_chain()
    leaves = engine.get_active_leaves()
    assert [n.thought_id for n in leaves] == ["grandchild"]


def test_get_active_leaves_ignores_pruned_children():
    engine = _engine_with_chain()
    engine.prune_branch("grandchild")
    leaves = {n.thought_id for n in engine.get_active_leaves()}
    assert leaves == {"child"}
