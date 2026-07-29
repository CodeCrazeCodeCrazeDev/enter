# Architecture Audit: AgentHarness Orchestration Framework

This document presents a comprehensive, deep architectural audit of the standard ReAct evaluation harness (`AgentHarness`).

---

## 1. Orchestration Flow & Topologies

The baseline framework operates on a **Single-Agent ReAct topology** (defined in `workflows/react_base`).
- **Entry Point**: The orchestration is managed by `main_agent_node` (`workflows/react_base/nodes/main_agent.py`), conforming to the `PipelineSpec` declared in `workflows/react_base/spec.py`.
- **DAG Definition**: The execution topology is modeled declaratively using `PipelineSpec`. Nodes (represented by `NodeDefinition`) are compiled into a directed acyclic graph (MiniDAG) via `DynamicGraphBuilder`.
- **Node Execution**: In the standard ReAct setup, the entry-point node `main_agent` wraps `run_agent_loop` (defined in `agent_harness/core/runtime/loop/agent_loop.py`), which drives the single-agent step-by-step thinking, tool call generation, and tool response processing.

---

## 2. Scheduling & Process Management

- **Scheduler Component**: The `Scheduler` class (`agent_harness/scheduling/scheduler.py`) manages DAG execution. It wraps the compiled `MiniDAG` execution with OS-level semantics (run, suspend, resume, abort).
- **Task Isolation**: Tasks are run in separate processes via a process-isolated subprocess execution model (`benchmarks/runner/run_subprocess.py`). This prevents asyncio saturation and resource leaking across tasks.
- **Wall-time Deadlines**: The scheduler enforces hard wall-time timeouts using an asynchronous interval-checking wrapper (`_astream_with_wall_time`), reading bounds from `AGENT_HARNESS_TASK_WALL_TIME_S`.

---

## 3. Agent Lifecycle

- **Agent Registry**: Agent roles and definitions (e.g., `react_solver`) are managed by `AgentRegistry` (`agent_harness/core/runtime/registries/agents.py`).
- **Lifecycle Phases**:
  1. **Initialization**: Loading model profiles, building the system prompt, and instantiating the LLM client.
  2. **Active Loop**: Generating assistant reasoning/tool calls (`on_llm_response`), matching tools via `ResourceManager`, executing them, and feeding output back (`on_turn_end`).
  3. **Termination**: Ending naturally when the LLM emits a plain text content payload without tool calls (`no_tool` behavior), or when constrained by max turns / token limits.
  4. **Post-processing / Recovery**: Forcing final answer extraction (`_force_final_answer`) by appending a summarization nudge.

---

## 4. Memory Model

- **Conversation History**: Standard raw list-of-dicts conversation history (`List[dict]`) passed to OpenAI/Anthropic APIs.
- **Compaction & Hygiene**: The context growth is managed strictly by the `KeepLastNToolResultsCompactor` compactor (`workflows/react_base/compactors.py`). It replaces old tool execution results beyond a threshold `N` with compact placeholders, saving valuable context window tokens.
- **No Semantic Memory**: The baseline lacks any vector-search, key-value, or semantic caching memory. It relies purely on the truncated/compacted linear chat context.

---

## 5. Verifier Pipeline & Quality Guardrails

- **Verifier Mechanism**: The baseline single-agent ReAct setup does not feature an active, automated verification pipeline or intermediate verify nodes. Output quality depends entirely on the LLM's self-correction.
- **Rollback Guardrails**: Robust rollbacks are implemented as state observers (`workflows/react_base/observers/`):
  - **DuplicateQueryRollback**: Wipes history and rolls back state if the agent repeats the exact same search query.
  - **EmptySearchRollback**: Rollback on empty results.
  - **RefusalRollback**: Rollback on AI refusal strings.

---

## 6. Tool Routing & Permissions

- **Tool Discovery**: Managed by `ResourceManager` (`agent_harness/core/runtime/resources/manager.py`). Tools are registered under roles (e.g., `react_solver`).
- **Execution Mechanism**: Tool calls are parsed from standard LLM response shapes (such as XML blocks or JSON) by `tool_call_parser.py`, and run dynamically by `tool_exec.py`.
- **Gating / Security**: Permissions are checked before execution (`permissions.py`), ensuring that tasks can restrict access to sensitive capabilities.

---

## 7. Checkpoint System

- **State Persistence**: The state of execution (nodes, variables, outputs) is periodically persisted utilizing the SQLite-based `EventStore` (`agent_harness/state/event_store/sqlite.py`).
- **Recovery & Resumption**: If interrupted or suspended, the graph state can be recovered using checkpoint databases, allowing deep research runs to resume from the last known-good state.

---

## 8. Benchmarks & Evaluation Pipeline

- **Benchmark Suite**: Supports high-difficulty research benchmarks such as `BrowseComp`, `HLE-text`, `DeepSearchQA`, and `WideSearch`.
- **Task Generators**: Custom task loaders (`benchmarks/core/harbor_task_generator.py`) standardize dataset question layouts.
- **Judges**: Configured under `benchmarks/judges/` (e.g., `hle.py`, `browsecomp.py`), utilizing LLM-as-a-judge or exact-match parsing.

---

## 9. Failure Recovery & Concurrency Model

- **Retry Strategy**: Fixed-interval and retriable client wrappers handle network timeouts or rate limits (e.g., 15 retries at 90s interval).
- **Concurrency**: Concurrency is managed at the benchmark-runner level via process limits (`--concurrency 30` in `run_subprocess.py`). There is no multi-threaded or async task multiplexing inside a single process, completely avoiding thread-safety issues.
