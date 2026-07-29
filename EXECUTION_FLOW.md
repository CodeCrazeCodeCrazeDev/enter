# Execution Flow: AgentHarness

This document provides a trace of how a deep research task is scheduled, initiated, processed, and finalized in `AgentHarness`.

---

## 1. Task Lifecycle Sequence

```
[User Command / Benchmark Runner]
                |
                v
       (Subprocess Spawn)
                |
                v
      [ProcessManager / SQLite]  <--- Instantiates Task with RUNNING status
                |
                v
          [Scheduler]            <--- Compiles MiniDAG from PipelineSpec
                |
                v
         [MiniDAG Runner]        <--- Invokes entry point node ("main_agent")
                |
                v
         [main_agent_node]       <--- Prepares prompts, configures compactor
                |
                v
        [run_agent_loop]         <--- Begins Turn-by-Turn ReAct Execution
                |
     +----------+----------+
     |                     |
     v                     v
[LLM Call]           [Observers]  <--- Evaluates rollbacks, budgets, & context
     |
     v
[Tool Execution]
     |
     v
[Loop Termination (No tool / Max turns)]
                |
                v
     [_force_final_answer]       <--- Runs summarization model if required
                |
                v
      [ProcessManager]           <--- Updates status to COMPLETED
```

---

## 2. Phase-by-Phase Trace

### Phase A: Setup & Scheduling
1. `run_subprocess.py` compiles the target benchmark list and spawns execution subprocesses with `--pipeline react_base`.
2. `Scheduler.execute()` is invoked with `task_id` and the raw question input.
3. The Scheduler fetches the compiled `MiniDAG` for `react_base` and registers standard tools (`web_search`, `web_fetch`, `run_python_code`).

### Phase B: Node Execution
1. The `main_agent_node` is entered.
2. The initial system prompt is loaded with the current date, and the user question is formatted.
3. The custom state observers (Console, SSE, Trajectory, Rollbacks) are instanced and appended.

### Phase C: ReAct Loop
1. The `run_agent_loop` executes a `while turn < max_turns` cycle.
2. LLM response is requested. If it generates thoughts and tool calls, the ToolCall parser decodes them.
3. Observers process the action (e.g., checks for duplicate query rollback).
4. Tool is executed, returning output text.
5. Old tool results are compacted via `KeepLastNToolResultsCompactor`.

### Phase D: Finalization
1. LLM decides to emit the answer directly (returns a response with no tool calls).
2. `_force_final_answer` verifies that a clean answer exists. If the loop was interrupted due to max turns, a summarization call extracts the final answer.
3. Task is finalized with status `COMPLETED`.
