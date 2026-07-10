# AgentHarness Dependency Graph (Phase 1)

This document visualizes and outlines the key file and module import relationships within AgentHarness, along with third-party library dependencies.

```
                  +--------------------------------+
                  |    scheduling/scheduler.py     |
                  +---------------+----------------+
                                  |
                                  v
                  +--------------------------------+
                  |  core/runtime/dag/minidag.py   |
                  +---------------+----------------+
                                  |
                                  v
                  +--------------------------------+
                  | core/runtime/loop/agent_loop.py|
                  +---------------+----------------+
                                  |
            +---------------------+---------------------+
            |                     |                     |
            v                     v                     v
+-----------------------+ +---------------+ +-----------------------+
|  core/messages.py     | |  core/tool.py | |  core/llm.py          |
+-----------------------+ +---------------+ +-----------------------+
```

---

## 1. Module-by-Module Import Chains

### `agent_harness/scheduling/`
- `scheduler.py`
  - Imports from `agent_harness.core.types` (events and status tracking)
  - Imports from `agent_harness.state.event_store.sqlite`
  - Imports from `agent_harness.scheduling.process_manager`
  - Instantiates or triggers `MiniDAGRunner` from `agent_harness.core.runtime.dag.minidag`

### `agent_harness/core/runtime/dag/`
- `graph_builder.py`
  - Imports from `agent_harness.core.protocols` (`PhaseContext`, `PhaseMiddlewareChain`)
  - Imports from `agent_harness.models.pipeline_spec`
  - Imports from `agent_harness.core.runtime.dag.minidag`
- `minidag.py`
  - Exposes `MiniDAG` and `MiniDAGRunner`
  - Fully decoupled, zero dependency on scheduling or loops (acts as a pure state engine)

### `agent_harness/core/runtime/loop/`
- `agent_loop.py`
  - Imports from `agent_harness.core.llm` and `agent_harness.core.messages`
  - Imports from `agent_harness.core.runtime.loop.compact` (compactor mechanisms)
  - Imports from `agent_harness.core.runtime.loop.llm_client` (token estimators, usage parsers)
  - Imports from `agent_harness.core.runtime.loop.model_profile` (thinking tags and normalizers)
  - Imports from `agent_harness.core.runtime.loop.tool_call_parser` (XML tool-argument parsers)
  - Imports from `agent_harness.core.runtime.loop.tool_exec` (Python sandbox/local tool execution)
  - Imports from `agent_harness.core.tool`
  - Imports from `agent_harness.core.loop_types`

---

## 2. Key External Dependencies
- **Pydantic**: Heavily utilized in `pipeline_spec.py` and `agent_definition.py` for input/configuration structure declaration.
- **SQLite (sqlite3)**: Core of state persistence in `agent_harness/state/event_store/sqlite.py`.
- **Jinja2**: Templating engine used to generate prompt chains from declarations in `graph_builder.py`.
- **OpenAI / SGLang compatible client**: Interfaced in `agent_harness/core/llm.py` to route chat commands.
