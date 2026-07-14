from __future__ import annotations

from apodex.memory.learning_memory import LongTermLearningMemory, TrajectoryRecord


def _record(task_type="research", goal="find best pricing", success=True, insight=None):
    return TrajectoryRecord(
        task_id="t1",
        task_type=task_type,
        goal=goal,
        is_success=success,
        learned_insight=insight,
    )


def test_record_trajectory_persists_and_reloads(tmp_path):
    path = tmp_path / "mem.json"
    mem = LongTermLearningMemory(str(path))
    mem.record_trajectory(_record())
    assert path.exists()

    reloaded = LongTermLearningMemory(str(path))
    assert "research" in reloaded.registry
    assert reloaded.registry["research"][0].goal == "find best pricing"


def test_load_missing_file_is_empty(tmp_path):
    mem = LongTermLearningMemory(str(tmp_path / "missing.json"))
    assert mem.registry == {}


def test_load_corrupt_file_is_ignored(tmp_path):
    path = tmp_path / "corrupt.json"
    path.write_text("not valid json", encoding="utf-8")
    mem = LongTermLearningMemory(str(path))
    assert mem.registry == {}


def test_query_similar_strategies_keyword_match(tmp_path):
    mem = LongTermLearningMemory(str(tmp_path / "mem.json"))
    mem.record_trajectory(_record(goal="optimize pricing model"))
    mem.record_trajectory(_record(goal="unrelated deployment task"))
    matched = mem.query_similar_strategies("research", "pricing")
    assert len(matched) == 1
    assert matched[0].goal == "optimize pricing model"


def test_query_similar_strategies_matches_insight(tmp_path):
    mem = LongTermLearningMemory(str(tmp_path / "mem.json"))
    mem.record_trajectory(_record(goal="do a thing", insight="cache results heavily"))
    matched = mem.query_similar_strategies("research", "cache")
    assert len(matched) == 1


def test_query_similar_strategies_unknown_task_type(tmp_path):
    mem = LongTermLearningMemory(str(tmp_path / "mem.json"))
    assert mem.query_similar_strategies("nope", "anything") == []


def test_query_sorts_successful_first(tmp_path):
    mem = LongTermLearningMemory(str(tmp_path / "mem.json"))
    mem.record_trajectory(_record(goal="pricing failed run", success=False))
    mem.record_trajectory(_record(goal="pricing good run", success=True))
    matched = mem.query_similar_strategies("research", "pricing")
    assert matched[0].is_success is True
