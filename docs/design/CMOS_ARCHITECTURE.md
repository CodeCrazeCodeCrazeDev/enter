# CMOS Executable Specification & Compatibility Contracts

This document contains the executable specification for the **Cognitive Memory Operating System (CMOS)**. It establishes public APIs, state machines, complexity/performance targets, telemetry structures, compatibility contracts, and test scenarios.

---

## 1. System Topology & Public APIs

The CMOS is exposed as a cohesive, pluggable service that wraps repository storage, an operator registry, a query planner, and a scheduler.

```
+---------------------------------------------------------------------------------+
|                                    CMOS                                         |
|  +--------------------+  +----------------------+  +-------------------------+  |
|  |  MemoryRepository  |  |   OperatorRegistry   |  |   MemoryQueryPlanner    |  |
|  +--------------------+  +----------------------+  +-------------------------+  |
|  +--------------------+  +----------------------+  +-------------------------+  |
|  |  MemoryScheduler   |  |  ProvenanceEngine    |  |   ObservabilityManager  |  |
|  +--------------------+  +----------------------+  +-------------------------+  |
+---------------------------------------------------------------------------------+
```

### 1.1 MemoryRepository
```python
class MemoryRepository(ABC):
    @abstractmethod
    async def save_node(self, node: MemoryNode) -> None: ...
    @abstractmethod
    async def get_node(self, node_id: str) -> Optional[MemoryNode]: ...
    @abstractmethod
    async def save_edge(self, edge: MemoryEdge) -> None: ...
    @abstractmethod
    async def get_edges(self, source_id: str) -> List[MemoryEdge]: ...
    @abstractmethod
    async def query_nodes(self, filters: Dict[str, Any]) -> List[MemoryNode]: ...
```

### 1.2 CognitiveOperator
```python
class CognitiveOperator(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    @abstractmethod
    async def execute(self, ctx: OperatorContext, **kwargs) -> OperatorResult: ...
```

---

## 2. Pluggable Operator Registry & Query Planner

The `MemoryQueryPlanner` receives a natural or programmatic high-level query goal and generates an `ExecutionPlan` containing sequential cognitive operator instances.

### 2.1 Query Planner Flow
```
High-Level Objective (e.g., "Compare Strategy A with Strategy B under Bear market conditions")
  │
  ▼
MemoryQueryPlanner.plan()
  │
  ├─► Check Active Registry for Operators [Recall, Compare, Recall]
  │
  ▼
ExecutionPlan (Sequential executable chain of operators)
  │
  ▼
Pluggable Operator Execution (with Telemetry context)
```

---

## 3. Telemetry & Observability Context

Every operator execution records rich telemetry to enable benchmarking and strict auditing:
```json
{
  "operator": "CompareOperator",
  "execution_id": "uuid",
  "latency_ms": 14.5,
  "memory_usage_bytes": 1024,
  "graph_mutations": 1,
  "cache_hits": 4,
  "status": "success",
  "confidence_changes": [
    {"node_id": "node_abc", "prev": 0.8, "new": 0.85}
  ]
}
```

---

## 4. Hierarchy State Machine

The lifetime of a Claim, Theory, or Strategy within the Memory Graph transitions through explicit states:

```
    [Proposed]
        │
        ▼ (Gather Evidence)
    [Validated] ◄──────┐ (Re-evaluate)
        │              │
        ▼ (Refute)     │
    [Refuted] ─────────┘
        │
        ▼ (Exceeds retention / drift)
    [Archived]
```

---

## 5. Compatibility Contracts

CMOS guarantees absolute compatibility across repository implementations:
1.  **Schema Completeness**: Any adapter (SQLite, Remote, InMemory) must execute identical schemas and preserve type constraints.
2.  **Referential Integrity**: An edge cannot exist without valid source and target node records.
3.  **Deterministic Replayability**: Given identical initial database seeds and operator parameters, sequential queries must return identical serialized output payloads.
4.  **No Side-Effects on Refusal**: If validation fails during transactional writes, the repository must perform automatic transactional rollbacks.

---

## 6. Target Acceptance Criteria (Success Gates)

| Metric | Target | Verification Method |
| :--- | :--- | :--- |
| **Recall Accuracy** | $\ge 95\%$ | Offline test vectors (PersonaMem & LoCoMo subsets) |
| **Deterministic Replay** | $100\%$ | Identical transaction hashes after rollback & retry |
| **Referential Integrity** | $0$ dangling edges | SQLite schema checks and post-validation scripts |
| **Provenance Completeness**| $100\%$ mutations | Verify provenance attributes on all save operations |
| **P95 Latency (Local)** | $< 50$ ms | Benchmark with 10,000 injected mock nodes |
