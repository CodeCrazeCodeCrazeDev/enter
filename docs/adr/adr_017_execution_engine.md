# ADR 017: Long-Horizon Execution Engine with Checkpointing

## Status
Proposed

## Context
Long-duration software or business executions are highly prone to sudden process interruptions, memory crashes, and rate limiting.

## Decision
We implement a DAG-based Long-Horizon Execution Engine. It supports topological task sequencing, thread-safe transaction locks, and persistent SQLite checkpointing. On interruption, the state is restored from the last validated checkpoint.

## Alternatives Considered
- **Direct Thread-based Sequential Execution (Rejected)**: No checkpointing capability; any crash forces a complete restart.

## Expected Benefits
- $100\%$ task recovery accuracy.
- Safe dynamic resource and budget allocation checks.

## Failure Modes
- **Lock Deadlock**: Prevented by utilizing WAL mode and simple timeout retries.

## Validation Plan
Interrupted execution workflows will be simulated, confirming automatic resume from the checkpoint.
