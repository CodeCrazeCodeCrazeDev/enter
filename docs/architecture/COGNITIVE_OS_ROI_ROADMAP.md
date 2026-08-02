# Cognitive OS Phase 5 — ROI-Based Evolutionary Implementation Roadmap

This document ranks and priorities all proposed capability enhancements and refactorings within the Cognitive Operating System based on an objective engineering Return on Investment (ROI) matrix.

---

## 1. Engineering ROI Matrix

We prioritize tasks by comparing their capability gains, structural simplification, and long-term leverage against their implementation cost and migration complexity.

$$\text{ROI Score} = \frac{\text{Capability Gain} + \text{Simplification} + \text{Leverage}}{\text{Implementation Cost} + \text{Migration Complexity}}$$

| Improvement Task / Component | Capability Gain (1-10) | Structural Simplification (1-10) | Implementation Cost (1-10) | Migration Complexity (1-10) | Expected ROI Score (Out of 10) | Priority |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Hierarchical Strategic Planner Decomposition** | 9.5 | 9.0 | 2.0 | 1.5 | **9.6 / 10** | **1 (Immediate)** |
| **SQLite durable multi-tier Memory (CMOS)** | 9.0 | 8.5 | 3.0 | 2.0 | **8.8 / 10** | **2 (Phase 1)** |
| **do-calculus Causal SCM Simulation Engine** | 8.5 | 8.0 | 4.0 | 2.5 | **7.4 / 10** | **3 (Phase 1)** |
| **Autonomous Research OS Discovery Loops** | 9.0 | 7.5 | 5.0 | 3.5 | **6.6 / 10** | **4 (Phase 2)** |
| **Multi-Agent ConsensAgent Debate Protocols** | 8.0 | 7.0 | 4.5 | 3.0 | **6.4 / 10** | **5 (Phase 2)** |
| **Automated Suitability Rollback Gateway** | 8.5 | 6.5 | 5.5 | 4.0 | **5.9 / 10** | **6 (Phase 3)** |

---

## 2. Phase-by-Phase Roadmap

### Priority 1: Hierarchical Strategic Planner Decomposition (Phase 1 — Immediate)
* **Goal**: Refactor standard flat strategic planner to recursively decompose compound goals into primitives with strict pre-conditions.
* **Component**: `apodex/planning/planner_executor.py`.
* **Impact**: Eliminates task execution deadlocks and context-window pollution.

### Priority 2: SQLite durable multi-tier Memory (CMOS) (Phase 1)
* **Goal**: Bind short-term memory traces to persistent SQLite database structures with Jaccard overlap indexing.
* **Component**: `apodex/memory/semantic_memory.py`.
* **Impact**: Decreases system memory foot-print and maintains transaction safety.

### Priority 3: do-calculus Causal SCM Simulation Engine (Phase 1)
* **Goal**: Build explicit causal equations with Pearl do-operators for forecasting scenario utility offline.
* **Component**: `apodex/world_model/world_model.py`.
* **Impact**: Safe offline business planning with zero execution token waste.
