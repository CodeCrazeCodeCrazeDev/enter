# Prioritized ROI Roadmap Specification

## Overview

This roadmap prioritizes platform evolution projects by **Expected Return on Engineering Effort (ROI)** across four primary criteria:
1. **Capability Gain** ($\Delta C$)
2. **System Reliability** ($\Delta R$)
3. **Scalability & Performance** ($\Delta S$)
4. **Maintainability & Tech Debt Reduction** ($\Delta M$)

ROI is scored using the formal metric:

$$\text{ROI Score} = \frac{w_c \Delta C + w_r \Delta R + w_s \Delta S + w_m \Delta M}{\text{Engineering Effort (Person-Weeks)}}$$

where $w_c = 0.35, w_r = 0.30, w_s = 0.20, w_m = 0.15$.

---

## Ranked Initiative Backlog

```
 Rank │ Initiative Title                             │ Layer Impact │ Effort │ ROI Score │ Priority Tier
──────┼──────────────────────────────────────────────┼──────────────┼────────┼───────────┼───────────────
   1  │ Active Inference Closed-Loop Bridge Binding  │ L1-L2-L3-L4  │ 2 wks  │   9.4/10  │ P0 (Immediate)
   2  │ Clean Up Pydantic V2 Models & Type Schemas   │ L1, L2, L4   │ 1 wk   │   9.1/10  │ P0 (Immediate)
   3  │ Unified Multi-Layer Integration Suite        │ L1-L4        │ 2 wks  │   8.8/10  │ P0 (Immediate)
   4  │ Non-Gaussian Hawkes Process AST Recursion    │ L2, L3       │ 2 wks  │   8.5/10  │ P1 (Near-Term)
   5  │ Token-Based AEAN Task Bidding Optimization   │ L3           │ 3 wks  │   8.1/10  │ P1 (Near-Term)
   6  │ Recursive Bayesian Belief Updates in APODEX  │ L4           │ 3 wks  │   7.8/10  │ P1 (Near-Term)
   7  │ Island MAP-Elites Cross-Population Migration │ L3           │ 4 wks  │   7.2/10  │ P2 (Mid-Term)
   8  │ Automated Paper Corpus 600+ Expansion        │ L1           │ 4 wks  │   6.9/10  │ P2 (Mid-Term)
```

---

## Detailed Initiative Breakdown

### Tier P0: Immediate High-ROI Initiatives (Weeks 1-4)

#### 1. Active Inference Closed-Loop Bridge Binding
* **Target Layer**: Cross-Layer (`ResearchToSystemBridge` in `apodex.ai_eos.research.integration`).
* **Objective**: Binds Research OS hypothesis discovery directly into EIOS Kernel EFE sensing, AEAN task bidding, and APODEX WorldModel belief updating.
* **Expected Returns**:
  - $\Delta C$: +30% autonomous hypothesis execution.
  - $\Delta R$: +25% state validation across layers.
  - Effort: 2 person-weeks.
  - **ROI Score**: **9.4 / 10**.

#### 2. Clean Up Pydantic V2 Models & Type Schemas
* **Target Layer**: All Layers (`apodex.cognition.brain`, `apodex.world_model`).
* **Objective**: Replace deprecated Pydantic V1 `class Config` and `.json()` usages with `model_config = ConfigDict(arbitrary_types_allowed=True)` and `model_dump_json()`.
* **Expected Returns**:
  - $\Delta R$: Eliminates all 26,000+ runtime deprecation warnings and prevents future Pydantic V3 breakage.
  - $\Delta M$: +40% code maintainability.
  - Effort: 1 person-week.
  - **ROI Score**: **9.1 / 10**.

#### 3. Unified Multi-Layer Integration Test Suite
* **Target Layer**: Test Subsystem (`tests/integration/`).
* **Objective**: Validates closed-loop interactions from Layer 1 through Layer 4 in automated end-to-end integration tests.
* **Expected Returns**:
  - $\Delta R$: +35% regression prevention.
  - Effort: 2 person-weeks.
  - **ROI Score**: **8.8 / 10**.

---

### Tier P1: Near-Term Enhancements (Weeks 5-10)

#### 4. Non-Gaussian Hawkes Process AST Recursion Guard
* **Target Layer**: Layer 2 & 3 (`CodeRewriteEngine`).
* **Objective**: Restrict Hawkes stability AST recursion checks specifically to function definitions to prevent false positives on standard library calls while guaranteeing AST safety.
* **Expected Returns**:
  - $\Delta R$: +20% rewrite safety.
  - Effort: 2 person-weeks.
  - **ROI Score**: **8.5 / 10**.

#### 5. Token-Based AEAN Task Bidding Optimization
* **Target Layer**: Layer 3 (`HiveMind`).
* **Objective**: Implement budget-decayed Expected Free Energy (EFE) task routing to assign tasks to the most specialized agent at minimum token cost.
* **Expected Returns**:
  - $\Delta S$: +40% token efficiency.
  - Effort: 3 person-weeks.
  - **ROI Score**: **8.1 / 10**.

#### 6. Recursive Bayesian Belief Updates in APODEX
* **Target Layer**: Layer 4 (`WorldModel`).
* **Objective**: Optimize causal graph updates using sparse matrix conjugate gradient updates for large-scale digital twin graph simulations.
* **Expected Returns**:
  - $\Delta C$: +25% belief accuracy.
  - $\Delta S$: +50% graph update speed.
  - Effort: 3 person-weeks.
  - **ROI Score**: **7.8 / 10**.

---

### Tier P2: Mid-Term Evolution (Weeks 11-16)

#### 7. Island MAP-Elites Cross-Population Migration
* **Target Layer**: Layer 3 (`GeneticWorkflowOptimizer`).
* **Objective**: Enable asynchronous migration gates across genetic strategy populations to avoid local optima in strategy evolution.
* **Expected Returns**:
  - $\Delta C$: +15% policy quality.
  - Effort: 4 person-weeks.
  - **ROI Score**: **7.2 / 10**.

#### 8. Paper Corpus Expansion (600+ Publications)
* **Target Layer**: Layer 1 (`Research OS`).
* **Objective**: Continuously ingest and extract transferable principles from new AI/ML papers into `ALPHA_ALGO` research databases.
* **Expected Returns**:
  - $\Delta C$: +20% domain coverage.
  - Effort: 4 person-weeks.
  - **ROI Score**: **6.9 / 10**.
