# Long-Horizon Execution Specification
## Durable Task Queues, Checkpoint Resumability & Failure Recovery (v3.0.0)

This document specifies the execution architecture required to sustain and coordinate projects lasting hours, days, weeks, and months.

---

## 1. Durable Task Coordination

The `EIOSKernel` coordinates executing complex, long-horizon plans through transactional, database-backed DAG states:

```
                  ┌─────────────────────────────────┐
                  │       Strategic Planner         │
                  └────────────────┬────────────────┘
                                   │  (Compiles Goal to DAG)
                                   ▼
                  ┌─────────────────────────────────┐
                  │       Durable Task Queue        │  ◀─── [Checkpoint Store]
                  └────────────────┬────────────────┘
                                   │  (Schedules Node Steps)
                                   ▼
                  ┌─────────────────────────────────┐
                  │       Isolated Executor         │
                  └─────────────────────────────────┘
```

1.  **Durable Task Queue**: All DAG steps are persisted to a transactional task table inside the SQLite database, carrying status tags (`PENDING`, `RUNNING`, `SUCCESS`, `FAILED`).
2.  **Checkpoint Store**: Every successful step execution triggers an async checkpoint state save, storing variables, files, and outputs. If the system crashes, it resumes from the last completed checkpoint.
3.  **Subprocess Isolation**: Heavyweight agent tasks are run inside isolated, sandboxed subprocess environments to prevent memory leaks and coordinate clean runtime resources.

---

## 2. Failure Recovery & Backtracking

*   **Automatic Replanning**: If an active step fails or times out, the `TaskExecutor` logs the exception and routes the failure signature to the `StrategicPlanner`. The planner branches alternative steps and updates the active DAG.
*   **Graph Backtracking**: The system leverages the Experience Memory Graph (EMG) to identify if the failure path matches any known historical pattern, applying the compiled edit operations (`ADD_STEP` or `REPLACE_STEP`) rather than engaging in a repetitive retry loop.
*   **Human HITL Escalation**: If the failure is non-transient (e.g., authentication error or API limits exhausted), the item is escalated to the centralized `UnifiedHITLFramework` queue for human operator intervention.
