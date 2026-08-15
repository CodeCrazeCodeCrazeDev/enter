# Target Architecture Blueprint

This document specifies the target architecture for the evolved `AgentHarness` framework, detailing the interaction layers, state-space representations, and multi-tier memory flow.

---

## 1. System Interaction Layers

```
        +-------------------------------------------------+
        |               User / Benchmark                  |
        +-----------------------+-------------------------+
                                |
                                v
        +-------------------------------------------------+
        |             HierarchicalOrchestrator            |
        +-----------------------+-------------------------+
                                |
                                v
        +-------------------------------------------------+
        |                CoordinatorAgent                 |
        +------------+-----------------------+------------+
                     |                       |
                     v                       v
        +-----------------------+ +-----------------------+
        |     WorkerAgent A     | |     WorkerAgent B     |
        +-----------+-----------+ +-----------+-----------+
                    |                         |
                    +------------+------------+
                                 |
                                 v
        +-------------------------------------------------+
        |           StrategicPlanner / Executor           |
        +-----------------------+-------------------------+
                                |
                                v
        +-------------------------------------------------+
        |                 SemanticMemory                  |
        +-------------------------------------------------+
```

## 2. Multi-Tier Memory Flow
1. **Episodic Tracing**: The `HarnessObserver` captures every tool result and builds an `ActionDecisionGraph` via the `EMGEngine`.
2. **Weakness Mining**: Failed trajectories are compared against successful reference runs to extract graph-edit repair paths.
3. **Semantic Consolidation**: Fact nodes are written to the database. If total tokens exceed `max_semantic_tokens`, the lowest-confidence facts are consolidated and pruned.
4. **Context Retrieval**: During runs, the `SemanticMemory` performs Jaccard-overlap search over historical evidence cards to inject relevant context.
