# Prioritized Return-on-Effort Engineering Upgrade Roadmap

**Version:** 2.0.0
**Status:** Canonical Engineering Prioritization Standard
**Target:** `docs/architecture/PRIORITIZED_ROI_ROADMAP.md`

---

## 1. Quantitative Return-on-Effort Framework

Architectural modifications are strictly prioritized based on their **Return-on-Engineering-Effort Index ($ROI$)**:

$$ROI = \frac{\Delta \text{Capability Score} \times \text{Reliability Impact}}{\text{Engineering Complexity Cost} \times \text{Maintenance Risk}}$$

Where:
- $\Delta \text{Capability Score} \in [1, 10]$: Measured improvement in long-horizon task completion, accuracy, or intelligence.
- $\text{Reliability Impact} \in [1, 5]$: Reduction in operational failure rate, data corruption, or execution crashes.
- $\text{Engineering Complexity Cost} \in [1, 10]$: Estimated story points, refactoring breadth, and implementation difficulty.
- $\text{Maintenance Risk} \in [1, 5]$: System fragility and risk of technical debt accumulation.

---

## 2. Ranked Capability Upgrade Matrix

| Priority Rank | Proposed Upgrade Subsystem | Target Layer | Expected Capability Gain ($\Delta C$) | Reliability Impact ($R$) | Complexity Cost ($K$) | Maintenance Risk ($M$) | $ROI$ Score | Architectural Justification |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Thread-Safe Async SQLite WAL Engine** | L1 | 8 | 5 | 3 | 1 | **13.33** | Eliminates database thread-locks and data loss during concurrent multi-agent executions. |
| **2** | **Real-Time Step Token & Latency Interceptor** | L2 | 7 | 5 | 2 | 1 | **17.50** | Enforces hard real-time execution halts, preventing runaway API consumption and budget exhaustion. |
| **3** | **Local Sub-Process Sandbox Task Validator** | L2/L4 | 9 | 4 | 4 | 2 | **4.50** | Replaces mock prompt evaluation with physical sub-process task execution, eliminating hallucinatory self-improvement. |
| **4** | **Uncertainty-Discounted Kelly Capital Sizing** | L2 | 8 | 4 | 3 | 2 | **5.33** | Prevents overallocation of capital to unproven, high-variance exploratory ventures. |
| **5** | **MemoHarness Jaccard Context Retrieval** | L1 | 8 | 3 | 3 | 2 | **4.00** | Retrieves relevant historical decisions and failure trajectories dynamically during ReAct turns. |
| **6** | **NetworkX EMG Failure Path Recovery** | L3 | 9 | 4 | 7 | 3 | **1.71** | Mines execution subgraphs to bypass tool error loops via graph-edit operations (`REPLACE_STEP`). |
| **7** | **3D Pareto Frontier Prompt Optimizer** | L3/L4 | 8 | 3 | 5 | 2 | **2.40** | Optimizes prompts simultaneously across Quality, Latency, and Cost, rejecting bloatware proposals. |

---

## 3. Engineering Implementation Milestones

### Milestone 1: Substrate Hardening & Operational Safety (Target: Sprint 1-2)
- **Deliverables:**
  1. Async SQLite connection pool with WAL mode (`PRAGMA journal_mode=WAL;`).
  2. Persistent trajectory schema (`trajectories` table with `step_id` indexing).
  3. Real-time token consumption stream interceptor in `VentureExecutionSystem`.
- **Validation Criteria:** 50 concurrent write threads execute without database locking, zero memory leaks across 10,000 steps.

### Milestone 2: Active Inference & Grounded Verification (Target: Sprint 3-4)
- **Deliverables:**
  1. Local `subprocess` Python sandbox validator executing deterministic task test suites.
  2. Beta posterior variance-weighted Fractional Kelly Criterion sizing in `PortfolioManager`.
  3. MemoHarness Jaccard overlap context retrieval engine in `SemanticMemory`.
- **Validation Criteria:** 100% of proposed prompt mutations are validated against physical test tasks before promotion.

### Milestone 3: SOTA Meta-Reasoning & Failure Recovery (Target: Sprint 5-6)
- **Deliverables:**
  1. NetworkX-backed Experience Memory Graph (EMG) error-bypass engine.
  2. 3D Pareto Frontier scoring engine ($S = w_q Q - w_t T - w_l L$).
  3. Welch's t-test statistical validation pipeline for automated rollout/rollback decisions.
- **Validation Criteria:** Automated single-shot error recovery on simulated API failure scenarios.
