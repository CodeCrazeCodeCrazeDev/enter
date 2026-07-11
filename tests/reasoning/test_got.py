"""Unit and integration tests for the Graph-of-Thought reasoning engine."""

from __future__ import annotations

import pytest
from agent_harness.core.runtime.reasoning.got import GraphOfThoughtEngine, ThoughtNode


def test_got_exploration_and_pruning():
    got = GraphOfThoughtEngine()

    # Root thought
    root = ThoughtNode(thought_id="t_0", content="Initial research hypothesis", score=0.8)
    got.add_thought(root)

    # Branch 1
    t1_1 = ThoughtNode(thought_id="t1_1", content="Explore internet search path A", score=0.4, parent_ids=["t_0"])
    t1_2 = ThoughtNode(thought_id="t1_2", content="Sub-findings under path A", score=0.3, parent_ids=["t1_1"])
    got.add_thought(t1_1)
    got.add_thought(t1_2)

    # Branch 2
    t2_1 = ThoughtNode(thought_id="t2_1", content="Explore local file sandbox path B", score=0.9, parent_ids=["t_0"])
    got.add_thought(t2_1)

    # Verify active leaf thoughts before pruning
    leaves = got.get_active_leaves()
    leaf_ids = {n.thought_id for n in leaves}
    assert leaf_ids == {"t1_2", "t2_1"}

    # Prune Branch 1 recursively
    got.prune_branch("t1_1")

    # Verify that both t1_1 and t1_2 are pruned
    assert got.thoughts["t1_1"].status == "pruned"
    assert got.thoughts["t1_2"].status == "pruned"
    assert got.thoughts["t2_1"].status == "active"

    # Verify active leaf thoughts after pruning
    new_leaves = got.get_active_leaves()
    assert len(new_leaves) == 1
    assert new_leaves[0].thought_id == "t2_1"


def test_got_path_merging():
    got = GraphOfThoughtEngine()

    t1 = ThoughtNode(thought_id="t1", content="Partial chemistry formula A", score=0.9)
    t2 = ThoughtNode(thought_id="t2", content="Partial chemistry formula B", score=0.7)
    got.add_thought(t1)
    got.add_thought(t2)

    # Merge t1 and t2
    merged = got.merge_thoughts(
        merged_id="merged_t1_t2",
        content="Combined unified chemistry formula",
        parent_ids=["t1", "t2"]
    )

    assert merged.score == 0.8  # (0.9 + 0.7) / 2
    assert "merged_t1_t2" in got.thoughts
