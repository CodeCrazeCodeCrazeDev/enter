# AgentHarness Execution Flow (Phase 1)

This document maps out the precise, turn-by-turn execution flow of AgentHarness during standard research runs.

---

## 1. High-Level Pipeline Initiation

```
[Runner Entry]
       |
       v
[Scheduler.execute]  ---> Instantiates MiniDAGRunner
       |
       v
[MiniDAGRunner.astream] ---> Navigates Nodes based on Transitions
       |
       v
[main_agent_node]    ---> Triggers main ReAct loop
       |
       v
[run_agent_loop]     ---> Iterates LLM calls and Tool actions
```

---

## 2. Low-Level Turn Execution Sequence (ReAct)

Inside `agent_loop.py` (`_run_loop_inner`), the turn-by-turn process executes with fine-grained event hooks:

1. **LLM Query Phase**:
   - Compiles chat history (`messages`).
   - Requests delta completion from `LLMClient` (calls `call_llm`).
   - Parses native reasoning (`<think>...</think>`) using `ThinkingParser`.

2. **Parsing Phase**:
   - Strips leaked private XML blocks.
   - Evaluates text for structural tool targets via `MultiFormatToolCallParser`.

3. **Observer Response Interventions**:
   - Triggers `on_llm_response` event to all observers.
   - Allows observers to intervene:
     - **Rollback**: Pop messages and re-issue prompt (e.g. on refusal, duplicate search, or empty search).
     - **Immediate Stop**: Set `stop_reason` (e.g. on budget exhaustion).

4. **Tool Execution Phase**:
   - Executes structural tool calls sequentially.
   - Caps results length via `DefaultToolResultPostProcessor`.
   - Records tool output messages in context memory.

5. **Context Overflow Guard**:
   - Assesses expected token consumption for the next completion.
   - If limits are reached, truncates older tool outputs using the compactor and raises `stopped_by="context_limit_reached"`.

6. **Compaction Phase**:
   - Invokes `MessageCompactor` to clean up oversized histories.

7. **Completion Probe Hooks**:
   - Triggers persistent `on_turn_complete` callbacks.
   - Validates whether pause signals (`pause_check()`) are requested.
