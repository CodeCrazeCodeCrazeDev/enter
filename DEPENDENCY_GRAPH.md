# AgentHarness Architectural Dependency Graph (Phase 1) - Enhanced

This document maps the absolute structural dependencies, package import structures, and external dependency constraints of the AgentHarness orchestration framework.

---

## 1. Class & File Level Topology Graph

```
==========================================================================================
                               [ scheduler.py ]
                                      |
                                      | (compiles & runs)
                                      v
                             [ graph_builder.py ]
                                      |
                                      | (creates runners)
                                      v
                               [ minidag.py ]
                                      |
                     +----------------+----------------+
                     | (executes)                      | (manages state)
                     v                                 v
             [ main_agent.py ]                  [ sqlite.py ] (EventStore)
                     |
                     | (runs ReAct turns)
                     v
             [ agent_loop.py ]
                     |
         +-----------+-----------+---------------------+
         |                       |                     |
         v                       v                     v
   [ compact.py ]          [ llm_client.py ]    [ tool_exec.py ]
   - MessageCompactor      - LLM Call Interf.   - execute_tools
                           - Token Estimator
==========================================================================================
```

---

## 2. Directory & Namespace Structure Mapping

The repository is structured neatly to isolate infrastructural mechanisms from runtime nodes:

- `agent_harness/core/`
  - `runtime/dag/`: Structures `MiniDAG` compilers and transitions (`minidag.py`, `graph_builder.py`).
  - `runtime/loop/`: The core engine driving sequential step-by-step model predictions and tool evaluations (`agent_loop.py`, `compact.py`, `llm_client.py`, `tool_exec.py`).
  - `messages.py`: Clean abstract definitions for System, User, Assistant, and Tool message protocols.
  - `tool.py`: Base wrappers encapsulating custom developer execution schemas.

- `agent_harness/scheduling/`
  - `scheduler.py`: Drives compilation of declarative pipeline profiles into executable subprocess threads.
  - `process_manager.py`: OS-level task status manager.

- `agent_harness/models/`
  - `pipeline_spec.py`: Highly pluggable schema configurations using Pydantic.

---

## 3. Strict Module Decoupling Boundary Constraints

To preserve standard backward compatibility and benchmark isolation during architectural evolution:
1. **The DAG Engine (`minidag.py`)** is entirely decoupled from execution context, runtime loops, and local databases. It must *never* reference `agent_loop.py` or `sqlite.py`.
2. **The ReAct Loop Engine (`agent_loop.py`)** remains a lightweight, domain-agnostic controller. No business logic, benchmark metrics, or task-specific fields (like chem structures, math values, web queries) are allowed within its boundaries. Custom behavior is cleanly injected via observers.
3. **The Scheduler (`scheduler.py`)** delegates task state tracking to the thread-level database without directly evaluating or manipulating the conversational payload.
