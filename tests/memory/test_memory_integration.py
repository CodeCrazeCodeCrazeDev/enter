from __future__ import annotations
import uuid
from datetime import datetime
import pytest

from apodex.memory.models import (
    AtomicMemory,
    CostMode,
    EpisodeLogRecord,
    NodeType,
    PersonalEvolutionProfile,
    WorkingContextGraph,
    WorkingContextNode,
    ScenarioPattern,
    ToolCallRecord,
)
from apodex.memory.services import (
    TencentDBMemoryStore,
    IngestionPipelineImpl,
    RetrievalAPIImpl,
    CheckpointManagerImpl,
    delete_user_data,
)


@pytest.mark.asyncio
async def test_full_memory_ingestion_and_clustering():
    """
    Validates end-to-end ingestion pipeline:
    T1 Logging -> T2 Atom Extraction -> T3 Scenario Clustering -> T4 Persona updates.
    """
    store = TencentDBMemoryStore()
    ingest = IngestionPipelineImpl(store=store)

    tenant_id = "org_a"
    user_id = "user_789"
    episode_id = uuid.uuid4()
    task_id = uuid.uuid4()

    # 1. Log Episode Step (T1)
    record = EpisodeLogRecord(
        record_id=uuid.uuid4(),
        episode_id=episode_id,
        task_id=task_id,
        tenant_id=tenant_id,
        user_id=user_id,
        agent_id="planner_agent",
        role="assistant",
        prompt_raw="Find the bug in fast_parser.py.",
        completion_raw="Found a division by zero bottleneck in fast_parser.py. Pushed a fix and solved the bottleneck.",
        tools_executed=[
            ToolCallRecord(tool_name="read_file", arguments="fast_parser.py", output="def parse(): return 1 / 0")
        ],
        token_usage_input=100,
        token_usage_output=150
    )

    await ingest.log_episode_step(record)
    assert len(store.episodes) == 1

    # 2. Extract and Inject Atoms (T2)
    raw_log = f"User prompted: {record.prompt_raw}. Agent output: {record.completion_raw}"
    atoms = await ingest.extract_and_inject_atoms(episode_id, raw_log, tenant_id, user_id)

    assert len(atoms) == 1
    assert "bottleneck" in atoms[0].content
    assert len(store.atoms) == 1

    # Add a second atom to trigger scenario clustering requirement (minimum 2 atoms)
    atom2 = AtomicMemory(
        atom_id=uuid.uuid4(),
        tenant_id=tenant_id,
        user_id=user_id,
        content="Fixed the second bug in the file parser.",
        embedding=[0.05] * 1536,
        source_episode_ids=[episode_id],
        confidence=0.9,
        tags=["ingested", "refactoring"]
    )
    store.atoms[atom2.atom_id] = atom2

    # 3. Scenario Clustering (T3)
    scenarios = await ingest.run_scenario_clustering(tenant_id)
    assert len(scenarios) == 1
    assert scenarios[0].pattern_type == "refactor_and_test"
    assert len(store.scenarios) == 1

    # 4. Update Personal Evolution Profile (T4 PEP)
    pep = await ingest.update_personal_evolution_profile(
        user_id=user_id,
        tenant_id=tenant_id,
        trigger_event={"cost_mode": "max_quality", "verbosity": "verbose", "vocabulary": ["AEAN", "Oversight"]}
    )
    assert pep.cost_budget_preferences["default_mode"] == "max_quality"
    assert pep.style_preferences["verbosity"] == "verbose"
    assert "AEAN" in pep.domain_vocabulary


@pytest.mark.asyncio
async def test_hybrid_retrieval_and_support_pack():
    """
    Validates hybrid querying and 2,000-token Support Pack packaging.
    """
    store = TencentDBMemoryStore()
    retrieval = RetrievalAPIImpl(store=store)

    tenant_id = "org_b"
    user_id = "user_456"

    # Add 3 distinct atomic memories
    for i in range(3):
        atom = AtomicMemory(
            atom_id=uuid.uuid4(),
            tenant_id=tenant_id,
            user_id=user_id,
            content=f" Distilled factual atom entry number {i} regarding performance bottlenecks in parsing.",
            embedding=[0.05] * 1536,
            source_episode_ids=[uuid.uuid4()],
            confidence=0.85 + (i * 0.05),
            tags=["performance", f"tag_{i}"]
        )
        store.atoms[atom.atom_id] = atom

    pep = PersonalEvolutionProfile(tenant_id=tenant_id, user_id=user_id)
    pep.cost_budget_preferences["default_mode"] = "balanced"

    # Query hybrid memory
    results = await retrieval.query_hybrid_memory(
        tenant_id=tenant_id,
        query_text="performance bottlenecks in parsing",
        query_embedding=[0.05] * 1536,
        pep=pep,
        limit=2
    )

    assert len(results) == 2

    # Generate XML Support Pack with a small limit of 500 characters (max 125 tokens)
    support_pack = retrieval.build_support_pack(results, max_tokens=125)
    assert "<SupportPack>" in support_pack
    assert "</SupportPack>" in support_pack
    assert "Distilled factual atom entry" in support_pack


@pytest.mark.asyncio
async def test_checkpoint_creation_and_recovery():
    """
    Verifies checkpoint creation (Redis and Durable DB) and complete crash recovery.
    """
    manager = CheckpointManagerImpl()
    task_id = uuid.uuid4()

    graph = WorkingContextGraph(
        task_id=task_id,
        tenant_id="org_c",
        nodes=[
            WorkingContextNode(task_id=task_id, type=NodeType.SUBTASK, label="Active database indexing"),
            WorkingContextNode(task_id=task_id, type=NodeType.CONCLUSION, label="Refuted slow scan pattern")
        ]
    )

    agent_cursors = {"planner": "segment_2", "verifier": "final_consensus"}
    episodic_offset = 1200

    # Create checkpoint
    success = await manager.create_checkpoint(task_id, graph, agent_cursors, episodic_offset)
    assert success is True
    assert task_id in manager.redis_hot_state
    assert task_id in manager.db_durable_snapshots

    # Recover state and verify completeness
    recovered = await manager.recover_state(task_id)
    assert recovered is not None
    assert len(recovered["working_graph"].nodes) == 2
    assert recovered["agent_cursors"]["planner"] == "segment_2"
    assert recovered["episodic_offset"] == 1200


def test_gdpr_cascading_deletion():
    """
    Validates GDPR data deletion cascading to child levels.
    """
    store = TencentDBMemoryStore()
    tenant_id = "org_d"
    user_id = "user_999"

    # Seed T1 episode
    episode_id = uuid.uuid4()
    record = EpisodeLogRecord(
        record_id=uuid.uuid4(),
        episode_id=episode_id,
        task_id=uuid.uuid4(),
        tenant_id=tenant_id,
        user_id=user_id,
        agent_id="re-agent",
        role="user",
        prompt_raw="A",
        completion_raw="B"
    )
    store.episodes[record.record_id] = record

    # Seed T2 atom
    atom_id = uuid.uuid4()
    atom = AtomicMemory(
        atom_id=atom_id,
        tenant_id=tenant_id,
        user_id=user_id,
        content="Personal confidential information of user_999",
        embedding=[0.01] * 1536,
        source_episode_ids=[episode_id]
    )
    store.atoms[atom_id] = atom

    # Seed T3 Scenario referencing user atom
    scen_id = uuid.uuid4()
    scen = ScenarioPattern(
        scenario_id=scen_id,
        tenant_id=tenant_id,
        name="Personalized Workflow Pattern",
        pattern_type="p_type",
        typical_workflow=["re-agent"],
        linked_atoms=[atom_id]
    )
    store.scenarios[scen_id] = scen

    # Seed T4 PEP
    store.peps[user_id] = PersonalEvolutionProfile(tenant_id=tenant_id, user_id=user_id)

    # Perform Deletion
    audit = delete_user_data(user_id=user_id, tenant_id=tenant_id, store=store)

    assert audit["action"] == "GDPR_DELETE"
    assert audit["stats"]["episodes_erased"] == 1
    assert audit["stats"]["atoms_erased"] == 1
    assert audit["stats"]["scenarios_erased"] == 1
    assert audit["stats"]["peps_erased"] == 1

    # Verify everything was purged from memory store
    assert len(store.episodes) == 0
    assert len(store.atoms) == 0
    assert len(store.scenarios) == 0
    assert len(store.peps) == 0
