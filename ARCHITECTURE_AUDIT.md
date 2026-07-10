# AgentHarness Architectural Audit (Phase 1)

This document provides a thorough, deep architectural audit of the AgentHarness repository. It breaks down the system into its core subsystems, details their current design, and analyzes their strengths, weaknesses, scalability, upgrade paths, and risks.

---

## 1. Orchestration Topology

### Current Architecture
AgentHarness currently employs a **flat, single-agent/single-solver orchestration topology** for standard ReAct executions (`react_base`). The main orchestrator is implemented in `agent_loop.py` via `run_agent_loop` and `main_agent_node` in `main_agent.py`. It is essentially a centralized, single-actor system where:
- The LLM acts as a monolithic agent (`react_solver`).
- There is no hierarchical delegation or multi-agent coordinator-worker design.
- The single LLM executes tools sequentially (e.g., `web_search`, `web_fetch`, `run_python_code`) and maintains all conversational state directly in its immediate context.

### Strengths
- **Simple & Deterministic**: High predictability and ease of debugging since all actions are sequential and contained in a single message history list.
- **Traceability**: Simple trajectory format. The linear thread makes event logging, rollback, and debugging straightforward.
- **Low Overhead**: Minimizes coordination overhead and saves routing reasoning tokens since there's only one model.

### Weaknesses
- **Monolithic Context Growth**: The single agent has to swallow all raw tool outputs (some of which can be huge), causing context window pressure.
- **Cognitive Overload**: The agent must handle both high-level strategizing/planning and low-level execution/tool-argument details in a single prompt.
- **Sequential Bottleneck**: Lack of parallel execution for non-dependent actions (like retrieving multiple different pages at once).

### Scalability Limits
- Limited by the single model's context length and accuracy retrieval capabilities under high load.
- As problem horizon grows (long-horizon tasks requiring 100+ steps), reasoning accuracy and instruction-following decay rapidly.

### Recommended Upgrade Path
Evolve towards **Hierarchical Multi-Agent Orchestration** where a *Master Orchestrator* delegates sub-tasks to *Coordinator Agents*, which in turn manage groups of specialized *Worker Agents* (e.g., Searcher, Sandbox Exec). State is recursively summarized upwards.

### Estimated Complexity & Risk
- **Complexity**: Medium-High (Requires nested message histories, synchronization of sub-agents, and protocol designs).
- **Risk**: Medium (Risk of cascading agent failures, infinite delegation loops, and complex debugging).

---

## 2. Agent Lifecycle

### Current Architecture
- **Stateless Lifecycles**: Agents are dynamically configured via declarative `AgentDefinition` models and instantiated contextually when a DAG node is triggered.
- **Lifecycle Span**: The runtime lifecycle of an agent is tied to the lifecycle of the single execution turn within the scheduling pipeline.
- **Model Provisioning**: The model client is fetched on-the-fly via the `ResourceManager` service registry.

### Strengths
- **Low Memory Footprint**: No long-running background agent processes.
- **Isolation**: Each step/turn is fully independent, preventing memory leaks between unrelated sessions.

### Weaknesses
- **No Persistence/Continuity**: Since agents are created on-the-fly, they lose all "experience" from step to step unless explicitly packed into the flat context.
- **High Warm-up/Warm-down cost**: Re-reading configurations and prompt assemblies on every invocation.

### Scalability Limits
- Cannot maintain session-level background actions or parallel multi-turn background research threads.

### Recommended Upgrade Path
Introduce a structured **Agent Lifecycle State Machine** (Registered → Active → Suspended → Terminated) with persistent local memory hooks across invocations.

### Estimated Complexity & Risk
- **Complexity**: Low-Medium
- **Risk**: Low (Mainly needs structured session tracking).

---

## 3. Memory Subsystem

### Current Architecture
- **Flat Context-Only Memory**: The system relies purely on the in-memory `messages` list (short-term memory).
- **Message Compaction**: When the context size approaches limit thresholds, a `KeepLastNToolResultsCompactor` is used to truncate old tool outputs into placeholder strings.
- **No Long-Term Semantic Memory**: There are no vector databases, key-value semantic memories, or knowledge graphs.

### Strengths
- **High Context Recency**: Keeps the latest tool outputs highly visible.
- **Zero Database Dependency**: Simple, portable, and runs purely in-memory.

### Weaknesses
- **Information Loss**: Truncation permanently destroys earlier raw data, preventing the model from re-inspecting historical evidence.
- **Hallucinations**: Without structured belief or state records, the model frequently forgets its high-level strategy and enters repetitive loop traps.

### Scalability Limits
- Strictly limited by the model's context window. Highly complex research tasks that span hundreds of web page fetches inevitably suffer from memory loss or severe truncation.

### Recommended Upgrade Path
Implement a **Persistent Semantic Memory** system storing explicitly managed beliefs, verified facts, evidence cards, unresolved questions, and task summaries. Agents read and write to this semantic store instead of raw history.

### Estimated Complexity & Risk
- **Complexity**: Medium
- **Risk**: Low (Easily sandboxed and mocked during tests).

---

## 4. Verifier Pipeline

### Current Architecture
- **Post-Execution Judgement**: Verification is largely decoupled from the live reasoning loop. It is handled after execution via offline judges (e.g., `xbench.py`, `widesearch.py` under `benchmarks/judges/`).
- **No Inline Verification**: The active agent does not have nested verifiers validating its intermediate steps before taking the next action.

### Strengths
- **Benchmark Consistency**: Decoupled verification ensures that evaluation metrics remain untainted by runtime modifications.

### Weaknesses
- **Error Cascading**: No self-correction during the execution loop; if the agent makes an erroneous logical leap at step 5, it continues building on that falsehood until step 100.

### Scalability Limits
- Severely limits performance on hard benchmarks like HLE where rigorous multi-step mathematical/factual validation is mandatory.

### Recommended Upgrade Path
Build an **Inline Parallel Verification** pipeline with domain-specific verifiers and a meta-verifier that review planner outputs and tool arguments before execution.

### Estimated Complexity & Risk
- **Complexity**: Medium
- **Risk**: Low-Medium (Requires careful prompt and parser tuning to avoid false negatives).

---

## 5. Tool Routing Pipeline

### Current Architecture
- **Direct ReAct Tool Binding**: Tools are directly bound to the single LLM role (`react_solver`) via the `ResourceManager`.
- **Parsing**: `MultiFormatToolCallParser` parses XML-like tags (e.g., `<tool_call>...`) from the LLM content stream.
- **Execution**: Run in-process or via sandboxes (E2B for Python).

### Strengths
- **Fast Execution**: Minimal routing latency.
- **Highly Standardized**: Matches standard ReAct protocols perfectly.

### Weaknesses
- **No Specialized Routing**: Every tool schema must be exposed to the main agent, diluting the context window with API parameters that might never be used.

### Scalability Limits
- Limit on the number of tools that can be registered before the model's performance degrades due to "tool pollution" in the system prompt.

### Recommended Upgrade Path
Build a **Route-to-Worker** model where the main planner delegates complex actions to specialized worker agents, who alone have access to specialized tool categories.

### Estimated Complexity & Risk
- **Complexity**: Low
- **Risk**: Low

---

## 6. Checkpoint System & State Persistence

### Current Architecture
- **SQLite Event Store**: `EventStore` in `sqlite.py` records pipeline event transitions (e.g., node entries, outputs, errors).
- **MiniDAG Checkpointing**: Checkpointing is handled via MiniDAG's state-saving mechanisms, which store state mappings using thread IDs.

### Strengths
- **Resumability**: The `Scheduler` can fetch the state mapping for a specific thread, allowing paused or interrupted tasks to resume.
- **Audit Trails**: Fully persistent database records of every high-level state change.

### Weaknesses
- **Coarse Granularity**: Checkpointing is done at DAG node boundaries, not at individual ReAct turn boundaries inside a node.
- **Heavy Payloads**: Large state blobs are written to SQLite, which can degrade database I/O performance.

### Scalability Limits
- If a single node executes 600 ReAct turns and fails at turn 599, the scheduler has to restart the node from turn 0.

### Recommended Upgrade Path
Enable **Fine-Grained Checkpoint Persistence** at the individual turn level, separating large tool payloads from core metadata.

### Estimated Complexity & Risk
- **Complexity**: Medium
- **Risk**: Low

---

## 7. Failure Recovery

### Current Architecture
- **Retry Middleware**: `LeakedToolCallRetryObserver` handles common LLM syntax leaks.
- **Rollback Observers**: Includes observers like `DuplicateQueryRollbackObserver`, `EmptySearchRollbackObserver`, and `RefusalRollbackObserver` that rollback the message history by popping the last assistant message when issues are detected.
- **LLM Failover**: Supports multi-retry and LLM fallback clients.

### Strengths
- **Robustness**: Outstanding capability to survive transient API errors, empty searches, or formatting issues.

### Weaknesses
- **Brittle Rollbacks**: Rollbacks rely on popping the raw message list directly. If structural indices get out of sync, the conversation history becomes corrupt.

### Scalability Limits
- Limited to simple recovery strategies. Cannot handle multi-step back-tracking (e.g., "if search branch A is a dead end, backtrack 15 steps and try branch B").

### Recommended Upgrade Path
Build a formal **Causal Rollback / Backtracking Engine** based on a Graph-of-Thought representation where agents can prune branches and resume from any historical node.

### Estimated Complexity & Risk
- **Complexity**: High
- **Risk**: High (Can break existing simple linear ReAct compatibility if not isolated).

---

## 8. Extension Points & Reusable Abstractions

### Current Architecture
- **PipelineSpec & NodeDefinition**: Outstanding declarative configuration models.
- **Observers**: Turn-level hooks (`on_llm_response`, `on_turn_end`, etc.) are extremely clean and extensible.
- **Services Registry**: Portable global resource sharing via `agent_harness.core.runtime.registry`.

---

## 9. Modules that should NOT be modified
To guarantee perfect backward compatibility and benchmark stability, the following must remain intact:
- `benchmarks/judges/` and `benchmarks/families/` (Ensures eval metric definitions are identical).
- Public signatures of `Scheduler.execute`, `run_agent_loop`, and core Pydantic specifications in `pipeline_spec.py`.
- The existing `react_base` workflow under `workflows/react_base/`.
