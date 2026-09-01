# Unified Cognitive System Dependency Graph & Interaction Protocols

## Executive Summary
This document establishes the strict Directed Acyclic Graph (DAG) for data, control flow, and inter-layer messaging across the 4 unified cognitive layers of the Autonomous Intelligence Platform.

---

## 1. Directional Dependency Graph (DAG)

```
[ Layer 1: Research OS ]
        |
        |  1. Export Validated Hypothesis & Principles
        v
[ Layer 2: EIOS Kernel & EOS Engine ]
        |
        |  2. Dispatch Active Inference Tasks & State Machine Commands
        v
[ Layer 3: AEAN Cognitive Intelligence ]
        |
        |  3. Dispatch Executable Action Plan & Memory Context
        v
[ Layer 4: APODEX Decision & WorldModel ]
        |
        |  4. Feedback Loop: Empirical Outcomes & Trajectory Traces
        +-------------------------------------------------------------+ (To Layer 1)
```

---

## 2. API Interface & Data Payload Contracts

### Layer 1 -> Layer 2 Handoff Interface
- **Method:** `ResearchOS.export_hypothesis_to_eios(hypothesis_id: str, efe_delta: float, principles: List[Dict])`
- **Data Payload:**
  - `hypothesis_id`: Unique identifier of scientifically validated research hypothesis.
  - `efe_delta`: Expected Free Energy delta improvement bound.
  - `principles`: Array of extracted transferable engineering principles.

### Layer 2 -> Layer 3 Handoff Interface
- **Method:** `EOSEngine.dispatch_active_inference_task(task_id: str, domain: str, budget_limit_usd: float)`
- **Data Payload:**
  - `task_id`: Orchestrated task identifier.
  - `domain`: Agent domain specialty requirement (e.g., `software_engineering`, `market_sensing`).
  - `budget_limit_usd`: Parsimonious budget limit.

### Layer 3 -> Layer 4 Handoff Interface
- **Method:** `HiveMind.execute_cognitive_plan(plan_id: str, actions: List[Dict], target_entities: List[str])`
- **Data Payload:**
  - `plan_id`: Multi-agent Graph-of-Thought synthesized plan.
  - `actions`: Sequential executable skill actions.
  - `target_entities`: WorldModel entity UUIDs to be modified.

### Layer 4 -> Layer 1 Feedback Loop Interface
- **Method:** `ResearchToSystemBridge.record_empirical_outcome(run_id: str, trajectory_steps: List[Dict], actual_vs_predicted: float)`
- **Data Payload:**
  - `run_id`: Execution trajectory ID.
  - `trajectory_steps`: Full trace of state transitions and tool outputs.
  - `actual_vs_predicted`: Empirical reward delta for DPO/SFT preference optimization.
