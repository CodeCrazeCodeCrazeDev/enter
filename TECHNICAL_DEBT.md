# AgentHarness Technical Debt & Safe Zones (Phase 1) - Enhanced

This document highlights the core areas of technical debt, identified extension points, reusable abstractions, and critical safety guardrails inside the AgentHarness repository.

---

## 1. Identified Legacy Technical Debt

### Lack of Formal Abstract Interfaces for Memory & Graphs
- **Problem**: No formal base classes or interfaces currently exist to represent semantic memory stores or knowledge graph databases.
- **Risk**: Adding custom stores directly into the runtime context could pollute core agent loop logic with database-specific driver dependencies.

### Direct Observer Mutations
- **Problem**: Rollback and normalization observers (e.g. `DuplicateQueryRollbackObserver`) perform direct mutations (pop/append) on raw message histories.
- **Risk**: Highly fragile. A change in the representation format of message arrays would instantly break multiple observer callbacks.

---

## 2. Reusable Abstractions & Extension Points

- **`Observer` Interface**: An exceptionally clean extension point. We can easily implement new architectural capabilities (like the Meta-Reasoner or Self-Improvement Flywheel) as custom, non-intrusive observers.
- **`PipelineSpec` & `NodeDefinition`**: These schema layers are perfectly suited for declarative configurations. We can declare new multi-agent, planner-executor, or verification pipelines entirely via metadata properties.
- **`ResourceManager` Service Registry**: Global service registry pattern allowing any runtime component to cleanly fetch registered LLM endpoints, sandboxes, and databases.

---

## 3. Safe Harbor: Modules to NOT Modify

To ensure benchmark absolute reproducibility and zero API breakages:

1. **`benchmarks/`**: The ground truths, judges, scoring math, and families must be treated as immutable read-only directories. Any changes here would invalidate standard verification comparisons.
2. **`workflows/react_base/`**: This directory implements the baseline ReAct loop. It is crucial for comparative studies. Do not modify.
3. **`MiniDAG` & `MiniDAGRunner` signatures**: To prevent breaking existing external orchestrators.
4. **`scheduler.py` Public Interface**: The scheduler interface must remain intact to prevent scheduling failures across execution sandboxes.
