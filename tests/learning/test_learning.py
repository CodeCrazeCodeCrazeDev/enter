"""Unit and integration tests for the Long-Term Learning and Self-Improvement Flywheel subsystems."""

from __future__ import annotations

import json
import os
import pytest
from apodex.memory.learning_memory import LongTermLearningMemory, TrajectoryRecord
from apodex.cognition.dataset_generator import TrajectoryDatasetCompiler


def test_long_term_learning_query(tmp_path):
    storage_file = os.path.join(tmp_path, "learning_mem.json")
    memory = LongTermLearningMemory(storage_path=storage_file)

    rec1 = TrajectoryRecord(
        task_id="task_abc_1",
        task_type="chemistry",
        goal="Determine heat index of compound X",
        steps=[{"step": 1, "action": "search"}],
        is_success=True,
        learned_insight="Compound X is volatile above 50C"
    )
    rec2 = TrajectoryRecord(
        task_id="task_abc_2",
        task_type="chemistry",
        goal="Synthesize helium isotopes",
        steps=[{"step": 1, "action": "sandbox_run"}],
        is_success=False,
        learned_insight="Isotopes decay immediately"
    )

    memory.record_trajectory(rec1)
    memory.record_trajectory(rec2)

    # Reload memory from local storage to verify persistent behavior
    new_memory = LongTermLearningMemory(storage_path=storage_file)
    assert "chemistry" in new_memory.registry

    # Query matching strategy
    results = new_memory.query_similar_strategies("chemistry", "volatility compound X heat")
    assert len(results) >= 1
    assert results[0].task_id == "task_abc_1"


def test_trajectory_dataset_compiler(tmp_path):
    compiler = TrajectoryDatasetCompiler(output_format="openai")

    history = [
        {"role": "system", "content": "You are a research agent."},
        {"role": "user", "content": "Perform the calculation."},
        {"role": "tool", "content": "Calculation result is 42"},
        {"role": "assistant", "content": "The answer is 42."}
    ]

    # Skip failed runs
    empty_trace = compiler.compile_trajectory(history, is_success=False)
    assert len(empty_trace) == 0

    # Compile successful runs
    trace = compiler.compile_trajectory(history, is_success=True)
    assert len(trace) == 4
    assert trace[0]["role"] == "system"
    assert trace[2]["role"] == "user"  # Tool converted to user with prefix [Tool Output]
    assert "[Tool Output]" in trace[2]["content"]

    # Export to jsonl
    jsonl_file = os.path.join(tmp_path, "ft_dataset.jsonl")
    compiler.export_to_jsonl([trace], jsonl_file)

    assert os.path.exists(jsonl_file)
    with open(jsonl_file, "r", encoding="utf-8") as f:
        line = f.readline()
        record = json.loads(line)
        assert "messages" in record
        assert len(record["messages"]) == 4
