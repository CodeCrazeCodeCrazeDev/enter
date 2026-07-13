# APODEX 2.0 5-TIER LONG-HORIZON MEMORY & RUNTIME ARCHITECTURE

This document specifies the concrete, production-grade memory and runtime design for **Apodex 2.0**. It is architected to support long-horizon, heavy-duty agent operations (runs exceeding 8 hours, coordinating ~150 sub-agents and ~15,000 steps per task) without experiencing context drift, token bloat, or state-reconstruction failure.

---

## 1. Grounding: Tencent Agent Memory & Cube Sandbox Integration

Apodex 2.0 uses and extends two foundational infrastructure primitives:

1. **TencentDB Agent Memory**:
   - Provides a 4-tier semantic storage core: L0 (Conversation Logs), L1 (Atomic Facts), L2 (Scenario Workflows), and L3 (Persona Profiles).
   - Introduces short-term context layering containing raw tool outputs (`refs/*.md`), step-level JSONL summaries, and a state-transition Mermaid canvas.
   - Executes hybrid retrieval via BM25, semantic embeddings, and Reciprocal Rank Fusion (RRF), achieving up to **61% token reduction** on wide searches, **33% savings** on SWE-bench tasks, and improving profile accuracy from **48% to 76%**.
2. **Cube Sandbox**:
   - High-density Micro-VM environments with `< 5 MB` memory overhead and `~60–90 ms` cold start times.
   - Runs 2,000+ isolated sandboxes on a 96-vCPU host, achieving P99 latency `< 200 ms` under rapid lifecycle churn.
   - Supports millisecond-level memory snapshotting, physical hardware isolation, and transaction-style rollbacks.

### Unified 5-Tier Memory Stack Mapping
Apodex 2.0 maps the TencentDB Agent Memory model and short-term canvas layers directly onto its **5-Tier Long-Horizon Memory Stack**:

| Apodex Memory Tier | Name | Scope / Lifecycle | TencentDB / Context Origin | Core Storage Substrate |
| :--- | :--- | :--- | :--- | :--- |
| **T0** | **Working Context** | Single active task / Live run | Mermaid Canvas + Tool buffer | Redis (hot state) / SQL (durable checkpoint) |
| **T1** | **Episodes** | Session / Temporal segment | L0 - Conversation Logs | TencentDB (Log-Store / JSONL) |
| **T2** | **Atoms** | Cross-session facts & events | L1 - Atomic Facts | TencentDB (Vector + BM25 Indices) |
| **T3** | **Scenarios** | Patterns & reusable workflows | L2 - Scenario Scene | TencentDB (Structured / Relational) |
| **T4** | **Personas (PEP)**| Per user / tenant / organization | L3 - Persona + Custom PEP fields | TencentDB (Document Store) |

---

## 2. Unified Tier Mapping & Schemas

The following sections define the production-ready schemas for T0 through T4, as well as the specialized self-evolution artifacts (Research Tickets and Capability Deltas).

### T0 (Working Context) Graph Representation
T0 sits on top of TencentDB and represents the live, stateful execution context of a running task as a **Mermaid-style symbolic graph**.
- **Nodes** represent sub-tasks, conclusions, specific sub-agents, or identified conflicts.
- **Edges** represent dependency relations, tool invocations, or verifier links.
- Every node has a deterministic `NodeToEpisodeMapping` containing a reference to the active `episode_id` and raw log byte/line offsets in Tier 1.

```
                      +-----------------------------+
                      |      T0 Working Graph       |
                      |  (State, Subtasks, Buffers)  |
                      +--------------+--------------+
                                     |
                                     | node_id maps to
                                     v
                      +--------------+--------------+
                      |          T1 Episodes        |
                      |   (Raw Logs & Tool Buffers) |
                      +--------------+--------------+
                                     |
                                     | distilled into
                                     v
                      +--------------+--------------+
                      |           T2 Atoms          |
                      |  (Semantic Fact Embeddings) |
                      +--------------+--------------+
                                     |
                                     | clustered into
                                     v
                      +--------------+--------------+
                      |         T3 Scenarios        |
                      | (Reusable Workflow Patterns) |
                      +--------------+--------------+
                                     |
                                     | guides behavior
                                     v
                      +--------------+--------------+
                      |    T4 Personas / PEP        |
                      | (Preferences & Cost Gating) |
                      +-----------------------------+
```

### Production Pydantic Schemas (`apodex/memory/models.py`)

These models are implemented directly in the `apodex/memory/models.py` file to act as the canonical programmatic schemas for the storage and retrieval layers:

```python
"""Production-grade data models for Apodex 2.0 5-Tier Long-Horizon Memory system.

This module maps Tencent Agent Memory (L0-L3) into Apodex T0-T4 tiers, extending
the schemas to support 8-hour+ heavy-duty tasks, Personal Evolution Profiles (PEP),
and self-evolution components.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, conlist


class CostMode(str, Enum):
    MAX_QUALITY = "max_quality"
    BALANCED = "balanced"
    FAST_CHEAP = "fast_cheap"


class NodeType(str, Enum):
    SUBTASK = "subtask"
    CONCLUSION = "conclusion"
    AGENT = "agent"
    CONFLICT = "conflict"
    VERDICT = "verdict"


class EdgeType(str, Enum):
    DEPENDENCY = "dependency"
    TOOL_CALL = "tool_call"
    VERIFICATION_LINK = "verification_link"
    CONFLICT_RESOLVED = "conflict_resolved"


# ==========================================
# Tier 0: Working Context (Symbolic Graph)
# ==========================================

class NodeToEpisodeMapping(BaseModel):
    """Maps a symbolic graph node in T0 back to raw Tencent L0 episodic logs."""
    episode_id: UUID = Field(
        ...,
        description="References the T1 episode/session log ID. DB-level index: yes."
    )
    log_offset_start: int = Field(
        ...,
        ge=0,
        description="Byte offset or sequence line number where the node execution trace begins."
    )
    log_offset_end: int = Field(
        ...,
        ge=0,
        description="Byte offset or sequence line number where the node execution trace ends."
    )


class WorkingContextNode(BaseModel):
    """A symbolic entity, active subtask, or conclusion in the working context."""
    node_id: str = Field(
        default_factory=lambda: f"node_{uuid4().hex[:12]}",
        min_length=5,
        max_length=64,
        description="Unique identifier for the node. DB-level index: primary key."
    )
    task_id: UUID = Field(
        ...,
        description="The scoped heavy-duty task ID. DB-level index: yes."
    )
    type: NodeType = Field(..., description="The symbolic type of the node.")
    label: str = Field(..., min_length=2, max_length=256)
    status: str = Field(
        default="active",
        description="State of the subtask (e.g., active, pending, verified, refuted)."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Dynamic runtime state, local memory variables, and active buffers."
    )
    log_mapping: Optional[NodeToEpisodeMapping] = Field(
        None,
        description="Trace link mapping this T0 node to T1/L0 raw log offsets."
    )


class WorkingContextEdge(BaseModel):
    """Dependency, tool interaction, or verifier link between T0 nodes."""
    edge_id: str = Field(
        default_factory=lambda: f"edge_{uuid4().hex[:12]}",
        description="Unique identifier for the edge. DB-level index: primary key."
    )
    task_id: UUID = Field(
        ...,
        description="The scoped heavy-duty task ID. DB-level index: yes."
    )
    source_node_id: str = Field(
        ...,
        description="Source T0 node. DB-level index: yes."
    )
    target_node_id: str = Field(
        ...,
        description="Target T0 node. DB-level index: yes."
    )
    type: EdgeType = Field(..., description="The semantic link type.")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Edge metadata (e.g., verification outcome, tool arguments)."
    )


class WorkingContextGraph(BaseModel):
    """Complete T0 Working Context representable as a Mermaid canvas."""
    task_id: UUID = Field(..., description="Scoped task ID. DB-level index: yes.")
    tenant_id: str = Field(..., description="Tenant namespace filter. DB-level index: yes.")
    nodes: List[WorkingContextNode] = Field(default_factory=list)
    edges: List[WorkingContextEdge] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ==========================================
# Tier 1: Episodes (Raw Session Logs)
# ==========================================

class ToolCallRecord(BaseModel):
    """Snapshot of a tool invocation."""
    tool_name: str = Field(..., min_length=1, max_length=128)
    arguments: str = Field(..., description="Raw string or serialized JSON arguments.")
    output: str = Field(..., description="Full output returned from the execution sandbox.")
    exit_code: int = Field(default=0)


class EpisodeLogRecord(BaseModel):
    """A raw execution trace entry corresponding to Tencent Agent Memory L0."""
    record_id: UUID = Field(
        default_factory=uuid4,
        description="Primary key. DB-level index: yes."
    )
    episode_id: UUID = Field(
        ...,
        description="Identifies the session or segment. DB-level index: yes."
    )
    task_id: UUID = Field(
        ...,
        description="Scope of the overall task. DB-level index: yes."
    )
    tenant_id: str = Field(..., description="Tenant namespace filter. DB-level index: yes.")
    user_id: str = Field(..., description="User ownership tracking. DB-level index: yes.")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Execution timestamp. DB-level index: yes."
    )
    agent_id: str = Field(..., description="The sub-agent that executed this step.")
    role: str = Field(..., description="Role tag, e.g., 'system', 'user', 'assistant'.")
    prompt_raw: str = Field(..., description="Unabridged input prompt sent to the LLM.")
    completion_raw: str = Field(..., description="Unabridged text response from the LLM.")
    tools_executed: List[ToolCallRecord] = Field(default_factory=list)
    token_usage_input: int = Field(0, ge=0)
    token_usage_output: int = Field(0, ge=0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ==========================================
# Tier 2: Atoms (Cross-Session Facts)
# ==========================================

class AtomicMemory(BaseModel):
    """An isolated, verified fact or decision, equivalent to Tencent L1."""
    atom_id: UUID = Field(
        default_factory=uuid4,
        description="Primary key. DB-level index: yes."
    )
    tenant_id: str = Field(..., description="Tenant namespace filter. DB-level index: yes.")
    user_id: str = Field(..., description="User ownership tracking. DB-level index: yes.")
    content: str = Field(
        ...,
        min_length=10,
        description="Concise description of the atomic fact or decision."
    )
    embedding: conlist(float, min_length=1536, max_length=1536) = Field(
        ...,
        description="1536-dimensional semantic representation vector for hybrid retrieval."
    )
    source_episode_ids: List[UUID] = Field(
        default_factory=list,
        description="Pointers to raw T1 logs that confirm this fact. DB-level index: yes."
    )
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Decaying metric updated by usage/verification. DB-level index: yes."
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Keywords representing entities, affected files, and utilized APIs. DB-level index: yes (GIN/Array)."
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_retrieved_at: datetime = Field(default_factory=datetime.utcnow)
    retrieval_count: int = Field(0, ge=0)


# ==========================================
# Tier 3: Scenarios (Patterns & Workflows)
# ==========================================

class ScenarioPattern(BaseModel):
    """A recurring task pattern or workflow schema corresponding to Tencent L2."""
    scenario_id: UUID = Field(
        default_factory=uuid4,
        description="Primary key. DB-level index: yes."
    )
    tenant_id: str = Field(..., description="Tenant namespace filter. DB-level index: yes.")
    name: str = Field(..., min_length=3, max_length=256)
    pattern_type: str = Field(
        ...,
        description="Pattern classification, e.g., 'refactor_and_test', 'adversarial_fuzzing'."
    )
    typical_workflow: List[str] = Field(
        ...,
        description="Sequential list of actions or subtask configurations."
    )
    failure_patterns: List[str] = Field(
        default_factory=list,
        description="Known symptoms that lead to this workflow breaking."
    )
    solution_patterns: List[str] = Field(
        default_factory=list,
        description="Actions or adjustments to run when failure patterns are observed."
    )
    linked_atoms: List[UUID] = Field(
        default_factory=list,
        description="Atoms backing the justification of this scenario."
    )
    success_rate: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Ratio of successful runs using this pattern. DB-level index: yes."
    )
    average_latency_ms: float = Field(0.0, ge=0.0)
    average_token_cost: int = Field(0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ==========================================
# Tier 4: Persona Evolution Profile (PEP)
# ==========================================

class PersonalEvolutionProfile(BaseModel):
    """User/Org profile extending Tencent L3 with cost limits and self-evolution pins."""
    profile_id: UUID = Field(
        default_factory=uuid4,
        description="Primary key. DB-level index: yes."
    )
    tenant_id: str = Field(..., description="Tenant namespace filter. DB-level index: yes.")
    user_id: str = Field(
        ...,
        description="Unique user identifier. DB-level index: yes."
    )
    style_preferences: Dict[str, Any] = Field(
        default_factory=lambda: {
            "verbosity": "concise",
            "depth": "exhaustive",
            "references_required": True
        },
        description="Style guidelines (e.g. verbosity, documentation depth, citations)."
    )
    cost_budget_preferences: Dict[str, Any] = Field(
        default_factory=lambda: {
            "default_mode": "balanced",
            "max_hours_limit": 12,
            "max_token_budget": 5000000
        },
        description="Gating cost, latency, and duration metrics."
    )
    evolution_controls: Dict[str, Any] = Field(
        default_factory=lambda: {
            "pinned_workflows": [],
            "learning_aggressiveness": 0.5,
            "auto_promote_harness_variants": False
        },
        description="Controls governing sub-agent behavioral adaptation and SFT updates."
    )
    domain_vocabulary: List[str] = Field(
        default_factory=list,
        description="Tenant or user-specific business/technical terms."
    )
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ==========================================
# Self-Evolution Artifacts
# ==========================================

class ResearchTicket(BaseModel):
    """An autonomous failure-reporting ticket queued for slow research loop upgrades."""
    ticket_id: UUID = Field(
        default_factory=uuid4,
        description="Primary key. DB-level index: yes."
    )
    tenant_id: str = Field(..., description="Tenant context. DB-level index: yes.")
    title: str = Field(..., min_length=5, max_length=256)
    failure_description: str = Field(..., description="Textual explanation of the persistent bottleneck.")
    related_episode_ids: List[UUID] = Field(
        ...,
        description="Pointers to episodic logs demonstrating the error. DB-level index: yes."
    )
    related_atom_ids: List[UUID] = Field(
        default_factory=list,
        description="Pointers to atomic facts relevant to the ticket. DB-level index: yes."
    )
    priority: int = Field(default=3, ge=1, le=5)
    status: str = Field(default="queued", description="Status of research (e.g., queued, analyzing, patched).")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CapabilityDelta(BaseModel):
    """Upgrade log detailing prompt, tool, or weights modifications in the system."""
    delta_id: UUID = Field(
        default_factory=uuid4,
        description="Primary key. DB-level index: yes."
    )
    tenant_id: str = Field(..., description="Tenant context. DB-level index: yes.")
    target_capability: str = Field(..., description="Identifies the affected sub-agent capability.")
    modification_type: str = Field(..., description="e.g., 'prompt_adaptation', 'tool_injection', 'fine_tuning'")
    baseline_version: str = Field(..., description="Previous version reference.")
    candidate_version: str = Field(..., description="Upgraded version reference.")
    performance_gain_ratio: float = Field(..., description="Observed gain multiplier in verification sandboxes.")
    rollback_sha256: str = Field(..., description="SHA-256 fingerprint of rollback configurations.")
    applied_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## 3. Ingestion for an 8-Hour Task

Managing an 8-hour heavy-duty task requires structured, streaming pipeline logic to prevent high memory usage and context fragmentation.

```
                    +------------------------------------+
                    |        T1 / L0 Streaming Log       |
                    +-----------------+------------------+
                                      |
                                      v
                    +------------------------------------+
                    |       T2 / L1 Atom Extraction      |
                    | (LLM-in-the-loop / Heuristics)     |
                    +-----------------+------------------+
                                      |
                        +-------------+-------------+
                        |                           |
                        v                           v
            +-----------------------+   +-----------------------+
            | T3 Scenario Clustering|   | T4 PEP Style Updates  |
            | (K-Means/Cosine Batch)|   |  (Heuristics/Triggers)|
            +-----------------------+   +-----------------------+
```

### 3.1 Step 1: Logging (T1 / L0)
Every sub-agent reasoning step (representing prompts, raw tool calls, tool results, completions, token usage, and latency metrics) is streamed directly to a structured, append-only JSONL log backed by **TencentDB L0 log storage**.
* **Compression**: Logs are chunked on a per-step basis. For older steps (older than 100 steps in the current execution), raw tool outputs exceeding 5,000 characters are compressed using `zstandard` inside TencentDB to save storage space while maintaining byte-range pointers.
* **Pagination**: Instead of reading the entire raw history, sub-agents load episodic slices using temporal or index-based cursors (sliding windows of the last $N$ turns).

### 3.2 Step 2: Atom Extraction (T2 / L1)
To prevent context drift, raw logs are processed through a background **LLM-in-the-loop extraction pipeline** that operates asynchronously relative to the main harness execution.
* **Extraction Prompt**:
  ```
  You are an expert cognitive compiler. Extract key factual assertions, critical decisions, and verified bug resolutions from the execution step below.
  Format each assertion as an independent, context-free atomic statement.

  Execution Step:
  {step_raw}

  Output JSON format:
  {{
    "atoms": [
      {{
        "content": "Bug fixed in config.py by replacing standard json parsing with rapidjson.",
        "salience": 0.95,
        "tags": ["config.py", "JSON-parsing", "optimization"]
      }}
    ]
  }}
  ```
* **Embedding**: Extracted atoms are transformed into 1536-dimensional semantic vectors and indexed in TencentDB's vector layer alongside key metadata.
* **Salience & Confidence**: Each atom is given a `confidence` rating derived from the extraction confidence (usually initialized at 0.8) and is linked back to the originating `episode_id`.

### 3.3 Step 3: Scenario Formation (T3 / L2)
At periodic step thresholds (e.g., every 50 steps), or upon successful completion of a major milestone (e.g., a subtask node transitioning to `verified` status), a batch clustering job is triggered.
* **Clustering**: The algorithm analyzes similar sub-agent paths using semantic distance on the sequence of tool execution types.
* If a sequence of operations (e.g., "Write test -> Fail -> Refactor code -> Run test -> Pass") repeats across several sessions with high performance, it is consolidated into a **T3 Scenario Pattern** representing a reusable workflow.
* This pattern maps typical workflow sequences, potential failure modes, and dynamic recovery scripts.

### 3.4 Step 4: Persona/PEP Updates (T4 / L3)
Updates to the **T4 Personal Evolution Profile (PEP)** are event-driven:
* **Trigger Conditions**: If a user/org changes cost preferences manually, or if the verifier repeatedly notes that conciseness guidelines are violated (causing user adjustments), a PEP update event is published.
* **Overfitting Prevention**: To avoid overfitting transient user behavior, style weights are adjusted via an exponential moving average (EMA) with a decay factor $\alpha = 0.2$. Only persistent, recurring style feedback shifts the baseline preferences in PEP.

### 3.5 Step 5: Symbolic Graph Updates (T0)
The **T0 Working Graph** is updated in real-time as tasks progress:
* When a new subtask is scheduled by the Orchestrator, a new `WorkingContextNode` of type `NodeType.SUBTASK` is written to Redis.
* Dependencies between subtasks are recorded as `WorkingContextEdge` links.
* **Trace Links**: As steps are written to Tier 1, the `log_mapping` of active nodes is updated to track the precise start and end lines (`log_offset_start` to `log_offset_end`) of corresponding raw episodic logs, ensuring trace drill-down functionality.

---

## 4. Retrieval for Long-Horizon Reasoning

Long-horizon reasoning relies on a top-down pipeline that reduces context clutter by selectively pulling high-signal memories.

```
                      Query / Active Subtask
                                 │
                                 ▼
                     Step 1: Check T4 PEP Style
                                 │
                                 ▼
                     Step 2: Match T3 Scenarios
                                 │
                                 ▼
                     Step 3: Query T2 Atoms
                                 │
                                 ▼
                     Step 4: Resolve T1 Logs (Trace)
                                 │
                                 ▼
                     Step 5: Inject "Support Pack"
```

### 4.1 Top-down Pipeline Flow
1. **Query Ingestion**: The agent begins with a specific reasoning query or active subtask context.
2. **PEP Customization (T4)**: The system reads the user's `PersonalEvolutionProfile` to set retrieval limits (e.g., `limit` boundaries and weight shifts matching current cost preferences).
3. **Scenario Matching (T3)**: The query matches against T3 Scenario templates. If a workflow matches, its step-by-step guideline and success/failure mitigations are pre-loaded.
4. **Factual Retrieval (T2)**: Semantic vector and BM25 hybrid search are executed on the T2 database to find specific verified facts.
5. **Episodic Drill-Down (T1)**: If a retrieved atom requires deeper validation, the system follows the `source_episode_ids` link to fetch specific log snippets from the T1 repository.

### 4.2 Hybrid Retrieval and Cost-Sensitive Scoring Formula
To retrieve high-impact contexts within the strict performance SLA, Apodex 2.0 leverages a unified multi-metric ranking formula executed in TencentDB. The ranking function integrates six distinct dimensions:

$$Score = w_{semantic} \cdot Sim_{semantic} + w_{bm25} \cdot Sim_{bm25} + w_{entity} \cdot Overlap_{entity} + w_{temporal} \cdot Prox_{temporal} + w_{graph} \cdot Prox_{graph} + w_{confidence} \cdot Conf$$

The weights shift dynamically based on the active `CostMode` to prioritize either correctness/validation or token reduction:

| Weight Parameter | `max_quality` Mode | `balanced` Mode | `fast_cheap` Mode | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| $w_{semantic}$ | **0.40** | **0.30** | **0.15** | Captures deep conceptual relevance. |
| $w_{bm25}$ | **0.15** | **0.15** | **0.10** | Ensures exact keyword matching (filenames, class names). |
| $w_{entity}$ | **0.15** | **0.15** | **0.10** | Boosts matches containing exact overlapping identifiers. |
| $w_{temporal}$ | **0.05** | **0.15** | **0.35** | Prioritizes recent events (critical for fast loop convergence). |
| $w_{graph}$ | **0.10** | **0.15** | **0.25** | Prioritizes items closely linked to the active T0 subtask. |
| $w_{confidence}$ | **0.15** | **0.10** | **0.05** | Down-ranks unverified or decaying memories. |

#### scoring implementation (`apodex/memory/interfaces.py`)
```python
def score_memory_item(
    semantic_sim: float,
    bm25_score: float,
    entity_overlap: float,
    temporal_proximity: float,
    graph_proximity: float,
    confidence: float,
    mode: CostMode,
) -> float:
    """Calculates a unified hybrid memory retrieval score.

    Weights are dynamically tuned based on the specified CostMode:
    - max_quality: priorizes comprehensive context, high semantic match, and deep confidence.
    - balanced: even weighting across factors with short-horizon decay.
    - fast_cheap: prioritizes temporal/graph proximity to reduce retrieval depth and token load.
    """
    # Define weights per cost mode
    if mode == CostMode.MAX_QUALITY:
        w_semantic = 0.40
        w_bm25 = 0.15
        w_entity = 0.15
        w_temporal = 0.05
        w_graph = 0.10
        w_confidence = 0.15
    elif mode == CostMode.FAST_CHEAP:
        # Under fast_cheap, we emphasize temporal and graph locality (recent and related)
        w_semantic = 0.15
        w_bm25 = 0.10
        w_entity = 0.10
        w_temporal = 0.35
        w_graph = 0.25
        w_confidence = 0.05
    else:  # CostMode.BALANCED
        w_semantic = 0.30
        w_bm25 = 0.15
        w_entity = 0.15
        w_temporal = 0.15
        w_graph = 0.15
        w_confidence = 0.10

    score = (
        (semantic_sim * w_semantic)
        + (bm25_score * w_bm25)
        + (entity_overlap * w_entity)
        + (temporal_proximity * w_temporal)
        + (graph_proximity * w_graph)
        + (confidence * w_confidence)
    )
    return float(score)
```

### 4.3 Context Injection and Gating Limits
* **Gating**: Total memory context injected per reasoning step is hard-gated at **$\le$ 2,000 tokens** (translates roughly to 5 to 20 highly distilled memory items).
* **Synthesis ("Support Pack")**: Retrieved items are not dumped raw. They are formatted as a structured XML "Support Pack" that clearly separates current plans from factual reference:
  ```xml
  <memory_support_pack>
    <scenario name="Python Refactor" success_rate="0.94">
      Use rapidjson and run validation script `test_all.sh` immediately.
    </scenario>
    <verified_facts>
      <fact id="atom_0823f" confidence="0.98">
        Base configuration is stored in /etc/config.json.
      </fact>
    </verified_facts>
  </memory_support_pack>
  ```

---

## 5. Retention, Forgetting, Consolidation

To prevent index pollution and ensure long-term performance, Apodex 2.0 incorporates active retention decay rules and automated background consolidation jobs.

### 5.1 Confidence Dynamics
The `confidence` of T2 Atoms and T3 Scenarios is dynamically adjusted using a reinforcement and temporal decay model:

$$Conf_{t+1} = \lambda \cdot Conf_t \cdot e^{-\gamma \cdot \Delta t} + (1 - \lambda) \cdot Feedback$$

Where:
* $\Delta t$ is the time elapsed since the last retrieval (expressed in days).
* $\gamma$ is the base decay constant (default: $0.05$, yielding mild decay over time).
* $Feedback$ represents the score assigned by the verifier or operator during subsequent steps:
  * $+1.0$ if the memory directly led to a verified correct solution.
  * $-1.0$ if the memory led to a verified error, contradiction, or required a correction.
* $\lambda$ is the inertia coefficient (default: $0.80$), protecting facts from being discarded due to a single anomalous error.

### 5.2 Background Consolidation
Asynchronous background jobs run during periods of low activity:
1. **Fact Merging**: Scans T2 for highly redundant atoms (e.g., semantic similarity $> 0.92$) and merges them, combining their `source_episode_ids` and keeping the maximum confidence score.
2. **Episodic Summarization**: Older T1 logs (exceeding the active retention threshold) are compressed or summarized into concise factual gists, with raw traces deleted unless flagged as persistent audit items.
3. **Index Compaction**: Clears out stale vector nodes whose confidence has decayed below $0.15$, rebuilding the TencentDB HNSW vector indices to maintain rapid `< 200 ms` lookup speeds.

### 5.3 User Controls and Compliance (GDPR/Cascading Erasure)
* **GDPR Erasure (Right-to-be-Forgotten)**: Operators can trigger a complete erasure request scoped to a specific `user_id` and `tenant_id`.
* **Cascading Erasure Flow**:
  1. Locates and deletes the `PersonalEvolutionProfile` (T4) or anonymizes it.
  2. Purges all raw episodic traces (T1) belonging to the user.
  3. Deletes any atomic fact (T2) whose sole verification source depends on the user's deleted episodic logs.
  4. Scans T3 Scenarios: if a scenario's success rates or workflows were heavily derived from deleted atoms, it is flagged for automatic re-clustering.
* **Audit Metadata**: A minimal, immutable audit trail is saved in the central durable database indicating *that* an erasure occurred (timestamp, UUID hash of the user ID) for security compliance, without retaining any user content.

---

## 6. Integration with LLM-as-a-Verifier & Self-Evolution

The memory architecture acts as the central feedback system linking the fast execution harness loop with the slow scientific research loop.

```
                         Harness Loop (Fast)
                     ┌────────────────────────┐
                     │   TaskExecutor         │
                     │   Executes Workflow    │
                     └───────────┬────────────┘
                                 │
                                 │ outputs logs & trace
                                 ▼
                     ┌────────────────────────┐
                     │   LLM-as-a-Verifier    │
                     │   Queries Memory T0-T3 ◄─────── Check consistency &
                     │   & Computes Verdict   │        detect contradictions
                     └───────────┬────────────┘
                                 │
                                 ├────────────────────────────┐
                                 │ writes back                │ writes back
                                 ▼                            ▼
                     ┌────────────────────────┐   ┌────────────────────────┐
                     │       T2 Atoms         │   │       T3 Scenarios     │
                     │  "Conclusion verified" │   │  "Adjust workflow"     │
                     └────────────────────────┘   └────────────────────────┘
                                                              │
                                                              │ triggers if
                                                              │ persistent failure
                                                              ▼
                                                  ┌────────────────────────┐
                                                  │   Research Loop (Slow) │
                                                  │   Generates Tickets    │
                                                  └────────────────────────┘
```

### 6.1 LLM-as-a-Verifier Core Flow
* **Verification Querying**: During execution, the Verifier queries the T0 graph and T2 factual database to check for factual consistency and semantic contradictions (e.g., ensuring a newly proposed solution does not violate a restriction confirmed in a previous segment).
* **Feedback Writeback**: After running verification, the outcome is recorded:
  * A successful verification creates a new T2 Atom (e.g., "Verification passed for patch X") and boosts the confidence of the utilized scenario.
  * A failed verification decreases the confidence of the utilized scenario, adjusts workflow success metrics, and inserts a `NodeType.VERDICT` node in the T0 working context graph.

### 6.2 Fast-Evolution Harness Loop
* **Behavior Adaptation**: When a task starts, the harness retrieves T3 Scenario patterns to see which workflow configurations achieved the highest success rates for the target pattern type.
* **Prompt Optimization**: The harness reads `evolution_controls` inside the PEP to apply optimized prompt adaptations or inject dynamic tools.
* **Logging Attempts**: Every adaptation is logged as an "attempt" in the T1 log. If successful, it is promoted to a system-wide capability delta.

### 6.3 Slow-Evolution Research Loop
* **Research Tickets**: If a particular workflow fails repeatedly (indicated by scenario success rates dipping below 0.60 or verifier errors repeating), the system automatically compiles a `ResearchTicket` containing:
  * Description of the persistent bottleneck.
  * Pointers to the offending `episode_id` traces.
  * Key historical atoms.
* **Model Training Evaluator**: The slow research loop processes these tickets by generating SFT training sets (compiled from successful trajectories in other namespaces) or fine-tuning models, evaluating them inside Cube Sandbox test domains before deployment.

---

## 7. Cube Sandbox Integration

Cube Sandbox provides a secure, lightweight micro-VM runtime to execute, verify, and shadow-test agent operations.

```
       Incoming Request / Live Traffic
                    │
           ┌────────┴────────┐
           ▼                 ▼
   ┌───────────────┐ ┌───────────────┐
   │ Baseline VM   │ │ Candidate VM  │
   │ (Current App) │ │ (New Prompt)  │
   └───────┬───────┘ └───────┬───────┘
           │                 │
           ▼                 ▼
   ┌───────────────┐ ┌───────────────┐
   │ Real Output   │ │ Shadow Output │
   └───────┬───────┘ └───────┬───────┘
           │                 │
           ▼                 ▼
   ┌─────────────────────────────────┐
   │     Verifier + Metric Comparison│
   │      (Promote or Rollback)      │
   └─────────────────────────────────┘
```

### 7.1 Isolated Multi-Tenant Experiments
* Each agent run is allocated a dedicated, hardware-isolated Cube Sandbox instance with a secure, local-first view of its assigned tenant.
* **Namespace Isolation**: The container is isolated from raw database hosts. All semantic query calls go through the **Immutable Safety Core** (enforcing logical `tenant_id` namespace filters) residing outside the sandbox.
* Sandboxes cannot access neighboring tenants' memory nodes, databases, or processes.

### 7.2 Shadow-Mode Testing & Automated Promotion
1. **Duplication**: When a new prompt variant or fine-tuned model (a `CapabilityDelta`) is proposed, the system forks incoming live requests.
2. **Parallel Runs**: The request is processed simultaneously in two parallel Cube Sandboxes:
   - One running the verified baseline.
   - One running the candidate configuration.
3. **Validation**: The LLM-as-a-Verifier evaluates both outputs, comparing execution latency, token efficiency, and correctness metrics.
4. **Promotion/Rollback**: If the candidate exhibits a significant performance increase without causing regressions, the `CapabilityDelta` is promoted to production. If errors occur, the sandbox is rolled back immediately.

### 7.3 Instant Rollbacks & Incident Diagnostics
* Cube Sandbox supports millisecond-level memory snapshots. If an agent execution causes a fatal loop or memory leak, the system reverts the sandbox to the last healthy state snapshot.
* **Drill-down Diagnostic**: Operators investigating failures can use the T0 `node_id` to retrieve the snapshot state and correlate it with the exact byte offsets of the T1 logs. This allows reproducing and debugging the failure in an isolated test sandbox.

---

## 8. Operational Plan for 8-Hour Tasks

This operational plan guarantees reliability, manages resource limits, and ensures observability across heavy-duty runs.

### 8.1 Checkpoint & Crash Recovery Strategy
To recover from network interruptions, system crashes, or hardware failures:

```
                      Active Execution Loop
                                │
              ┌─────────────────┴─────────────────┐
              ▼ (Every 10-30 seconds)             ▼ (Every 5 minutes)
     ┌─────────────────┐                 ┌─────────────────┐
     │  Redis Hot Save │                 │   Durable SQL   │
     │  - T0 graph     │                 │   - Snapshot    │
     │  - Cursors      │                 │   - Logs Offset │
     └─────────────────┘                 └─────────────────┘
```

1. **Redis Hot Store**: Every 10-30 seconds, or after every step completion, the orchestrator serializes the active T0 Working Graph, agent cursors, and current step offsets, saving them to Redis with a 24-hour Time-To-Live (TTL).
2. **Durable DB Snapshots**: Every 5 minutes, or upon completing a major graph subtask node, a full task checkpoint is written to a persistent relational SQL database (e.g., SQLite or Postgres).
3. **Recovery Protocol**:
   - Upon restarting after a failure, the system attempts to load the state from Redis.
   - If Redis is unavailable, it restores the latest snapshot from the Durable SQL database.
   - The orchestrator reconstructs the T0 working graph, updates sub-agent state cursors, and resumes log streaming from the exact episodic offset recorded in the checkpoint.

### 8.2 Performance, Cost, & Storage Guardrails
To prevent cost overruns, the system enforces hard-coded limits:

* **Latency SLA**: Hybrid retrieval (BM25 + Semantic Vector Search in TencentDB) must resolve in **$< 200\text{ ms}$ (P95)** in `balanced` mode, and **$< 300\text{ ms}$** in `max_quality` mode.
* **Token Budget Gating**:
  - `balanced` mode: Max **5M tokens** per 8-hour task.
  - `max_quality` mode: Max **10M tokens** per 8-hour task.
  - `fast_cheap` mode: Max **2.5M tokens** per 8-hour task.
* **Memory Footprint Limit**: Through aggressive background consolidation, older log pruning, and duplicate fact merging, the active memory footprint is restricted to **$< 500\text{ MB}$ per tenant/month** before cold archival.

### 8.3 Observability, Monitoring & Debugging
* **Observability Dashboard**: Tracks key performance indicators including retrieval latency, search hit-rates, token usage, and memory database growth.
* **Mermaid Graph Visualization**: Operators can render the T0 Working Graph directly from Redis, providing a visual representation of the active task topology, subtask dependencies, and execution states.
* **End-to-End Diagnostics**: Allows tracing any final system response back through its supporting verification verdicts, the atomic facts that justified the decision, and the raw episodic logs where the actions took place:

$$\text{Final Answer} \;\longrightarrow\; \text{Verifier Verdict (T0)} \;\longrightarrow\; \text{Supporting Atoms (T2)} \;\longrightarrow\; \text{Raw Episode Logs (T1)}$$
