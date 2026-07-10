# AgentHarness Execution Flow (Phase 1) - Enhanced

This document maps out the precise, sequence-by-sequence execution paths of AgentHarness during standard research runs, from initial process creation to terminal results generation.

---

## 1. High-Level Subprocess Orchestration

```
[Main OS Process]
       |
       | (Fork/Spawns subprocess per task sample)
       v
[Subprocess Runner] -> invokes run_subprocess.py
       |
       | (loads pipeline configuration)
       v
[Scheduler.execute] -> compiles MiniDAGRunner
       |
       | (initiates state streams)
       v
[MiniDAGRunner.astream] -> traverses DAG nodes sequentially
       |
       | (executes main_agent_node)
       v
[main_agent_node] -> run_agent_loop
```

---

## 2. Low-Level ReAct Turn Execution Sequence

Within `agent_loop.py` (`_run_loop_inner`), every individual turn goes through a highly structured 10-step lifecycle:

```
     [Start ReAct Turn]
             |
             v
   1. [Compile History] --------> Estimates current token load
             |
             v
   2. [call_llm] --------------> Stream tokens or run synchronous chats
             |
             v
   3. [ThinkingParser] --------> Strips and captures <think> reasoning
             |
             v
   4. [Leaked Tag Filter] -----> Stashes XML and private tag anomalies
             |
             v
   5. [on_llm_response] -------> Observers evaluate prompt response
             |                   (Can raise Rollbacks or Aborts)
             |
             +---- (If Rollback Intervention is triggered)
             |     - Pop last message from history
             |     - Inject nudge / fix message
             |     - Restart turn boundary (turn -= 1, continue)
             |
             v
   6. [ToolCallParser] --------> Extracts target tool names & args
             |
             v
   7. [execute_tools] ---------> Resolves in sandboxed environments
             |
             v
   8. [on_turn_end] -----------> Observers execute turn-completion logic
             |
             v
   9. [Context Guard] ---------> Triggers compaction if limits are close
             |
             v
  10. [on_turn_complete] ------> Persists local state to checkpoint db
```

---

## 3. Concurrency Model Breakdown

AgentHarness does not rely on a monolithic async loop inside a single process to execute multiple tasks concurrently.
- Instead, **Subprocess Isolation** is enforced at the harness layer.
- This prevents asyncio loop starvation, eliminates thread-safety issues during shared SQLite operations, and allows the OS to cleanly kill hanging or blocked individual sample runs without affecting the wider benchmark session.
