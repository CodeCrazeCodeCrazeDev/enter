from __future__ import annotations

import json

import pytest

from apodex.cognition.dataset_generator import TrajectoryDatasetCompiler


def test_compile_trajectory_skips_failed_runs():
    compiler = TrajectoryDatasetCompiler()
    assert compiler.compile_trajectory([{"role": "user", "content": "hi"}], is_success=False) == []


def test_compile_trajectory_rewrites_tool_messages():
    compiler = TrajectoryDatasetCompiler()
    history = [
        {"role": "user", "content": "question"},
        {"role": "tool", "content": "result"},
        {"role": "assistant", "content": "answer"},
    ]
    formatted = compiler.compile_trajectory(history, is_success=True)
    assert formatted == [
        {"role": "user", "content": "question"},
        {"role": "user", "content": "[Tool Output] result"},
        {"role": "assistant", "content": "answer"},
    ]


def _read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def test_export_to_jsonl_writes_messages(tmp_path):
    compiler = TrajectoryDatasetCompiler()
    out = tmp_path / "data.jsonl"
    trajectories = [[{"role": "user", "content": "hi"}]]
    compiler.export_to_jsonl(trajectories, str(out))
    records = _read_jsonl(out)
    assert records == [{"messages": [{"role": "user", "content": "hi"}]}]


def test_export_to_jsonl_strict_mode_raises_on_collapse(tmp_path):
    compiler = TrajectoryDatasetCompiler(max_self_generated_ratio=0.5, strict_mode=True)
    out = tmp_path / "data.jsonl"
    trajectories = [
        {"messages": [{"role": "user", "content": "a"}], "is_self_generated": True, "score": 1.0},
        {"messages": [{"role": "user", "content": "b"}], "is_self_generated": True, "score": 1.0},
    ]
    with pytest.raises(ValueError, match="Model-Collapse Guard"):
        compiler.export_to_jsonl(trajectories, str(out))


def test_export_to_jsonl_non_strict_downsamples(tmp_path):
    compiler = TrajectoryDatasetCompiler(max_self_generated_ratio=0.5, strict_mode=False)
    out = tmp_path / "data.jsonl"
    trajectories = [
        {"messages": [{"role": "user", "content": "real"}], "is_self_generated": False, "score": 1.0},
        {"messages": [{"role": "user", "content": "s-high"}], "is_self_generated": True, "score": 0.9},
        {"messages": [{"role": "user", "content": "s-low"}], "is_self_generated": True, "score": 0.1},
    ]
    compiler.export_to_jsonl(trajectories, str(out))
    records = _read_jsonl(out)
    # 1 real allows floor((1 * 0.5)/0.5) = 1 self-generated (the higher score kept)
    contents = {m["content"] for rec in records for m in rec["messages"]}
    assert "real" in contents
    assert "s-high" in contents
    assert "s-low" not in contents


def test_export_to_jsonl_under_limit_keeps_all(tmp_path):
    compiler = TrajectoryDatasetCompiler(max_self_generated_ratio=0.5, strict_mode=True)
    out = tmp_path / "data.jsonl"
    trajectories = [
        {"messages": [{"role": "user", "content": "a"}], "is_self_generated": False, "score": 1.0},
        {"messages": [{"role": "user", "content": "b"}], "is_self_generated": True, "score": 1.0},
    ]
    compiler.export_to_jsonl(trajectories, str(out))
    assert len(_read_jsonl(out)) == 2
