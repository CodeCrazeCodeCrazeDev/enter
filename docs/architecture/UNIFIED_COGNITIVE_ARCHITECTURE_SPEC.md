# UNIFIED COGNITIVE ARCHITECTURE SPECIFICATION
## Version 3.0.0 — Unified 4-Layer Autonomous Intelligence Platform

---

### Executive Summary

This document specifies the unified, first-principles 4-layer cognitive architecture unifying **Research OS**, **EIOS/EOS**, **AEAN**, and **APODEX** into a single, cohesive autonomous cognitive operating system.

Historically, these 5 frameworks operated as loosely coupled or partially overlapping platforms, resulting in functional duplication across planning, memory, and orchestration. Under this unified specification, each component is assigned strict, non-overlapping architectural ownership within a single 4-layer stack governed by **Active Inference** (Expected Free Energy minimization) and **Causal World Modeling**.

```
+-----------------------------------------------------------------------------------+
| LAYER 1: RESEARCH OS (Scientific Discovery & Active Hypothesis Generation)        |
| - Paper Ingestion & Literature Synthesis  - Null Hypothesis Registration           |
| - Statistical Walk-Forward Validation     - Deflated Sharpe & White's Reality Check|
+-----------------------------------------------------------------------------------+
                                         |
                                         v (Validated Research & Active Hypotheses)
+-----------------------------------------------------------------------------------+
| LAYER 2: EIOS / EOS (Autonomous Orchestration & Execution Layer)                 |
| - Anomaly Sensing & Continuous Monitoring  - Dynamic Workflow DAG Compilation     |
| - Enterprise First-Principles Engine      - Capital Allocation & Risk Management   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v (Executable DAG Tasks & Bidding Specs)
+-----------------------------------------------------------------------------------+
| LAYER 3: AEAN (Cognitive Multi-Agent Intelligence Layer)                         |
| - HiveMind Token-Based Bidding Registry   - Specialized Domain Agents             |
| - Learnable Routing Gate Dispatcher       - Self-Referential AST Code Rewriting  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v (State Changes, Actions & Causal Signals)
+-----------------------------------------------------------------------------------+
| LAYER 4: APODEX (Decision & Execution Platform Layer)                             |
| - Causal DAG World Model                  - Recursive Bayesian Belief Updating    |
| - Credit Halting & Governance Enforcement - Real-time Execution Substrate          |
+-----------------------------------------------------------------------------------+
```

---

### Layer-by-Layer Architecture & Interfaces

#### Layer 1: Research OS (Research & Discovery Layer)
* **Primary Responsibility**: Autonomous scientific inquiry, literature ingestion, hypothesis formulation, experimental design, statistical validation, and principle extraction.
* **Core Mechanisms**:
  - **Autonomous Science Engine**: Literature synthesis and whitespace detection across academic namespaces.
  - **Deflated Sharpe Ratio (DSR) & White's Reality Check (WRC)**: Rigorous statistical testing correcting for multiple-testing bias and backtest overfitting.
  - **Blended Discovery Math**: Priority scoring combining commercial value, expected information gain, and option value ($\text{Priority} = \alpha V_{\text{comm}} + \beta \Delta I + \gamma V_{\text{opt}}$).
* **Cross-Layer Output**: Emits validated or active research hypotheses with expected utility signals to Layer 2.

#### Layer 2: EIOS / EOS (Execution & Orchestration Layer)
* **Primary Responsibility**: Continuous environment sensing, business state machine monitoring, GTM loop execution, dynamic workflow DAG compilation, and capital/resource allocation.
* **Core Mechanisms**:
  - **EIOS Kernel**: High-throughput asynchronous DAG executor converting high-level objectives into executable task graphs.
  - **EOS First-Principles Engine**: 11-stage entrepreneurial lifecycle simulator (customer lifecycle, GTM dynamics, unit economics, moat building, failure diagnostics).
  - **Active Anomaly Sensing**: Continuous Active Inference sensing detecting market drift and operational anomalies.
* **Cross-Layer Output**: Emits compiled task DAGs and task bidding specifications to Layer 3.

#### Layer 3: AEAN (Cognitive Multi-Agent Intelligence Layer)
* **Primary Responsibility**: Multi-agent coordination, specialized agent execution, token-based task bidding, self-referential code synthesis, and genetic prompt optimization.
* **Core Mechanisms**:
  - **HiveMind Coordination Engine**: Token-budgeted task bidding registry where specialized agents bid for execution rights based on confidence and EFE.
  - **Learnable Routing Gate**: Budget-decayed Expected Free Energy (EFE) task dispatcher routing subtasks to cost-optimal specialists.
  - **Self-Referential Code Rewrite Engine**: AST-verified mutation and synthesis with non-Gaussian Hawkes stability constraints.
* **Cross-Layer Output**: Emits executed actions, updated code artifacts, and trajectory trace records to Layer 4.

#### Layer 4: APODEX (Decision & Execution Platform Layer)
* **Primary Responsibility**: State of truth, causal world modeling, recursive Bayesian belief updating, active inference state tracking, and credit/safety governance.
* **Core Mechanisms**:
  - **APODEX WorldModel**: Directed causal graph ($G = (V, E)$) tracking entity states, relationships, and counterfactual intervention paths.
  - **Recursive Bayesian Belief Engine**: Conjugate updating of system beliefs ($P(\theta | \mathcal{D})$) based on empirical outcomes.
  - **Credit Halting & GRC Governance**: Safety layer enforcing financial credit caps, rate limits, and compliance vetoes.
* **Cross-Layer Feedback**: Feeds updated Bayesian belief states and counterfactual information gain back to Layer 1 for hypothesis refinement.

---

### Cross-Layer Active Inference State Handoff Protocol

The unified architecture implements a continuous closed-loop Active Inference cycle across all four layers:

1. **Hypothesis Ingestion (L1 -> L2)**:
   - Research OS registers hypothesis $H_k$ and validates statistical significance ($p < \alpha / N_{\text{exp}}$).
   - $H_k$ is passed to EOS/EIOS via `ingest_validated_research(hypothesis)`.

2. **DAG Compilation & Sensing (L2 -> L3)**:
   - EOS senses market anomalies and EIOS compiles an execution DAG $\mathcal{G}_{\text{DAG}}$.
   - Tasks are published to AEAN HiveMind via `register_research_insight(task_id, confidence)`.

3. **Multi-Agent Task Bidding & Execution (L3 -> L4)**:
   - AEAN HiveMind arbitrates bids from specialized agents using EFE utility scores.
   - Selected agents execute tasks and generate execution state traces.

4. **World Model Update & Belief Propagation (L4 -> L1)**:
   - APODEX WorldModel updates causal nodes and updates Bayesian belief probabilities $P(H_k | \text{outcome})$.
   - Updated belief metrics feed back into Research OS literature review and experiment design.

---

### Non-Functional Guarantees & Engineering Standards

- **Zero Duplicated Responsibilities**: Strict enforcement of single-layer ownership (see `CAPABILITY_OWNERSHIP_MATRIX.md`).
- **Institutional Reliability**: Automated AST compilation checks, GRC security vetoes, and financial credit limits prevent catastrophic runaway loops.
- **Sub-100ms Orchestration Latency**: Direct Python memory pass-through for in-process state handoffs without IPC overhead.
- **100% Test Coverage**: Full integration test validation covering all 4 layers.
