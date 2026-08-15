# Risk Analysis and Mitigation Strategies

This document provides a comprehensive risk assessment for the hierarchical orchestration upgrade.

---

## 1. Risk: Orchestration Overhead & Cascading Failures
- **Description**: Managing multiple layers of agents increases coordination latency and can trigger infinite delegation loops.
- **Severity**: Medium-High
- **Mitigation**: Implement strict coordination budget guards (`max_coordinators`, `max_workers_per_coordinator`) directly inside the `HierarchicalOrchestrator` to restrict agent sprawl.

## 2. Risk: Context Window Inflation via Memory Duplication
- **Description**: Active retrieval of historical evidence cards could inject repetitive or massive context blocks into the agent's prompt.
- **Severity**: Low-Medium
- **Mitigation**: Enforce automatic deduplication inside `SemanticMemory` (skipping identical cards) and cap raw cards at `max_cards`.

## 3. Risk: Model-Collapse on Flywheel SFT Tuning
- **Description**: Training subsequent models on low-quality self-generated trajectories causes cumulative degradation of reasoning capabilities.
- **Severity**: High
- **Mitigation**: Deploy the `TrajectoryDatasetCompiler` with strict `Model-Collapse Guards` to raise errors or downsample low-scoring self-generated training data before exporting to SFT format.
