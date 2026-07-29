# Dependency Graph: AgentHarness Modules

This document outlines the dependency tree and architectural layering of the `AgentHarness` framework.

---

## 1. Architectural Layers

The system is constructed in a strictly layered fashion:

```
+--------------------------------------------------------------+
|                         Workflows                            |
|             (e.g., workflows/react_base)                     |
+------------------------------+-------------------------------+
                               |
                               v
+------------------------------+-------------------------------+
|                       Scheduling                             |
|          (Scheduler, ProcessManager, WorkflowLoader)          |
+------------------------------+-------------------------------+
                               |
                               v
+------------------------------+-------------------------------+
|                      Core Runtime                            |
|             (MiniDAG, AgentLoop, ResourceManager)            |
+------------------------------+-------------------------------+
                               |
                               v
+------------------------------+-------------------------------+
|                   Infrastructure & Models                     |
|            (LLM Client adapters, SQLite, Pydantic)           |
+--------------------------------------------------------------+
```

---

## 2. Core Module Dependencies

Below is the structured dependency mapping for major modules:

- **`agent_harness/core/runtime/loop/agent_loop.py`**
  - Depends on:
    - `agent_harness/core/loop_types.py` (LoopConfig, LoopPolicy)
    - `agent_harness/core/messages.py` (Message formats, text_of)
    - `agent_harness/components/observers/*` (Budget, Context size)
    - `agent_harness/core/runtime/resources/manager.py` (ResourceManager)

- **`agent_harness/scheduling/scheduler.py`**
  - Depends on:
    - `agent_harness/core/runtime/dag/minidag.py` (MiniDAGRunner)
    - `agent_harness/scheduling/process_manager.py` (ProcessManager)
    - `agent_harness/state/event_store/sqlite.py` (EventStore)

- **`workflows/react_base/nodes/main_agent.py`**
  - Depends on:
    - `agent_harness/core/runtime/loop/agent_loop.py`
    - `workflows/react_base/compactors.py`
    - `workflows/react_base/observers/*`
    - `workflows/react_base/prompts.py`

- **`agent_harness/core/runtime/dag/graph_builder.py`**
  - Depends on:
    - `agent_harness/models/pipeline_spec.py`
    - `agent_harness/core/runtime/dag/minidag.py`

---

## 3. Strict Layering Enforcement

1. **Upward Dependency Rule**: Low-level layers (Infrastructure, Core Runtime) MUST NOT import from high-level layers (Scheduling, Workflows).
2. **Backward Compatibility Rule**: Any additions to `agent_harness/core` must preserve the method signatures and schemas expected by `workflows/react_base`.
