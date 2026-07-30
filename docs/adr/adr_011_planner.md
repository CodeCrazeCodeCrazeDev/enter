# ADR 011: HTN + MCTS Planner Architecture

## Status
Proposed

## Context
Long-horizon, multi-day task planning is prone to execution failures, error propagation, and infinite loop traps. Standard reactive planning policies lack topological safety and multi-hour consistency.

## Decision
We implement a hybrid Hierarchical Task Network (HTN) and Monte Carlo Tree Search (MCTS) Planner. HTN decomposes abstract strategic goals into primitive task schemas under deterministic constraints. MCTS performs dynamic tree exploration over valid state actions to optimize planning sequences.

## Alternatives Considered
- **Pure ReAct loops (Rejected)**: Suffers from high loop drift, does not guarantee goal convergence, and incurs massive API token overhead.
- **Classic A* Search (Rejected)**: Inflexible to stochastic state changes and high-dimensional action spaces.

## Expected Benefits
- Topologically sorted plan steps with strict dependency resolution.
- Dynamic replanning on task failures within a $< 150\text{ ms}$ latency budget.

## Failure Modes
- **HTN Schema Discrepancy**: Triggered when preconditions cannot be resolved. Mitigated by publishing a fallback event to the Evaluation Engine.

## Validation Plan
Verified via testing with synthetic step failures to guarantee $100\%$ plan repair rate.
