# Phased Migration Plan: Flat ReAct to Hierarchical Planning

This document provides a highly detailed, risk-minimized migration strategy to transition from legacy flat ReAct pipelines to our hierarchical, decoupled planning framework.

---

## Stage 1: Compatibility Layer Deployment (Immediate)
- **Action**: Deploy `agent_harness` capability upgrades alongside the existing flat pipelines. Keep public APIs strictly compatible.
- **Verification**: Run unit and integration tests to ensure existing benchmarks execute correctly.

## Stage 2: Shadow Evaluation Phase (Milestone 2)
- **Action**: Route a fraction (e.g., 10%) of live benchmark tasks to the hierarchical orchestrator in "Shadow Mode" (evaluating outputs without updating production registers).
- **Verification**: Compare latency, token efficiency, and correctness metrics between the flat ReAct baseline and the shadow coordinator.

## Stage 3: Canary Deployments (Milestone 3)
- **Action**: Use the `SelectiveRollout` component to canary-deploy the new `max_llm_retries` and planner parameters to 20% of traffic.
- **Verification**: If any latency SLA regression (> 5s) occurs, the `RollbackManager` automatically triggers a rollback.

## Stage 4: Full Production Cutover (Milestone 4)
- **Action**: Deprecate the old flat ReAct pipelines gradually, transferring 100% of tasks to the master hierarchical orchestrator.
