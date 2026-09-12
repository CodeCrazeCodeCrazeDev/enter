# Unified Cognitive Architecture Specification

## 1. Executive Summary & Vision

The Autonomous Intelligence Platform operates as a single, unified, four-layer cognitive operating system rather than a collection of disparate projects. Legacy software paradigms treat research, sensing, strategy, multi-agent execution, and world modeling as siloed systems. In contrast, this unified architecture treats all components as tightly integrated layers of one autonomous reasoning substrate.

By applying first-principles cognitive science, Active Inference (Free Energy Principle), causal DAG modeling, and multi-agent mechanism design, this architecture eliminates redundant capabilities, enforces explicit state handoff contracts, and delivers long-horizon autonomous execution.

---

## 2. The 4-Layer Cognitive Operating System Hierarchy

```
+-----------------------------------------------------------------------+
| LAYER 1: RESEARCH OS (Scientific Discovery & Evidence Synthesis)      |
| - Paper Corpus (500+ Papers) & Transferable Principle Extraction     |
| - Hypothesis Generation, Verification & DSR Calculation               |
+-----------------------------------------------------------------------+
                                  │ Validated Hypotheses / Principles
                                  ▼
+-----------------------------------------------------------------------+
| LAYER 2: EIOS & EOS ENGINE (Execution & Orchestration Layer)          |
| - EIOS Kernel: Active Inference Sensing & Anomaly Expected Free Energy|
| - EOS Engine: 11-Section Entrepreneurial State Machine & Moat Analysis|
+-----------------------------------------------------------------------+
                                  │ Formulated Strategies / Directives
                                  ▼
+-----------------------------------------------------------------------+
| LAYER 3: AEAN (Cognitive Intelligence & Multi-Agent Execution)        |
| - HiveMind: Token Bidding Registry & Strategic Routing                |
| - SkillRegistry & Executor: Dynamic Task Decomposition                |
+-----------------------------------------------------------------------+
                                  │ Actions & Tool Executions
                                  ▼
+-----------------------------------------------------------------------+
| LAYER 4: APODEX WORLDMODEL (Decision, Reality & Belief Substrate)     |
| - Recursive Bayesian Belief Engine & Entity State Management          |
| - Governance, Safety Guards & Audit Trail                             |
+-----------------------------------------------------------------------+
```

### Layer 1: Research OS (Scientific Discovery Layer)
* **Primary Responsibility:** Literature ingestion, paper corpus reconciliation, transferable principle extraction, empirical hypothesis formulation, and Deflated Sharpe Ratio (DSR) statistical validation.
* **Key Components:** `ResearchOS`, `LiteratureReviewer`, `StatisticalValidationEngine`, `ReproducibilityTracker`.
* **Zero-Duplication Boundary:** Research OS *only* produces validated scientific hypotheses and extracted transferable engineering principles. It does not execute business decisions or route live agent tasks.

### Layer 2: EIOS & EOS Engine (Execution & Orchestration Layer)
* **Primary Responsibility:** Active Inference sensing (`EIOSKernel`) and entrepreneurial strategy orchestration (`EOSEngine`).
* **Key Components:** `EIOSKernel` (Active Inference sensing, Expected Free Energy calculation), `FirstPrinciplesEOSEngine` (11-section business state machine, growth stage classification, customer lifecycle loops, moat analysis).
* **Zero-Duplication Boundary:** EIOS senses environmental anomalies and market shifts using Active Inference over hypotheses exported from Layer 1. EOS transforms these signals into actionable business strategies and operational goals. Neither layer directly runs low-level multi-agent bidding or code execution.

### Layer 3: AEAN (Cognitive Intelligence Layer)
* **Primary Responsibility:** Multi-agent strategy execution, token-bidding task allocation, dynamic skill decomposition, and self-improving cognitive workflows.
* **Key Components:** `HiveMind` (bidding registry and strategic router), `SkillRegistry` (canonical library of 60+ strategic/operational skills), `CodeRewriteEngine`, `GeneticWorkflowOptimizer`.
* **Zero-Duplication Boundary:** AEAN coordinates specialized agents to execute directives issued by Layer 2. It consumes strategies and outputs structured execution traces and tool outputs.

### Layer 4: APODEX WorldModel (Decision & Reality Substrate)
* **Primary Responsibility:** Ground-truth entity tracking, recursive Bayesian belief updating, safety/compliance auditing, and execution state persistence.
* **Key Components:** `WorldModel`, `EntityManager`, `RecursiveBayesianBeliefEngine`, `ComplianceGovernor`, `ApprovalEngine`.
* **Zero-Duplication Boundary:** APODEX maintains the canonical state of reality and enforces non-bypassable safety constraints. All state changes resulting from AEAN execution must be validated and committed through APODEX.

---

## 3. Core Subsystem Elimination of Duplication

Prior iterations exhibited logical duplication across planners, memories, and schedulers. Under this specification:

1. **Memory Single Source of Truth:**
   - Epistemic research memory resides exclusively in **Layer 1** (`ResearchOS`).
   - Strategic market memory resides exclusively in **Layer 2** (`EOS`).
   - Agent execution history resides in **Layer 3** (`AEAN`).
   - Ground-truth entity state and Bayesian beliefs reside exclusively in **Layer 4** (`APODEX WorldModel`).

2. **Planner Single Source of Truth:**
   - Scientific hypothesis planning belongs to **Layer 1**.
   - Strategic entrepreneurial goal planning belongs to **Layer 2**.
   - Task decomposition and step execution belong to **Layer 3**.
   - State transition validation belongs to **Layer 4**.

---

## 4. Mathematical & Scientific Foundations

### Active Inference & Free Energy Minimization (Layer 2 EIOS Kernel)
Sensory observations $o$ and hidden states $s$ are integrated via Expected Free Energy (EFE) calculation:
$$G(\pi) = \sum_\tau E_{q(o_\tau, s_\tau | \pi)} \left[ \ln q(s_\tau | \pi) - \ln q(s_\tau | o_\tau, \pi) - \ln p(o_\tau) \right]$$
Where:
- The first term represents **epistemic value** (information gain regarding market/system state).
- The second term represents **pragmatic value** (realization of preferred strategic outcomes).

### Recursive Bayesian Belief Updating (Layer 4 APODEX)
Prior belief $P(B)$ is updated given new observation $O$ from agent execution:
$$P(B | O) = \frac{P(O | B) P(B)}{P(O)}$$
Belief variance decays deterministically over time via exponential decay when unverified, ensuring belief staleness is bounded.

---

## 5. Architectural Quality Attributes & SLA Guarantees

| Quality Attribute | Target SLA Metric | Enforcement Mechanism |
| :--- | :--- | :--- |
| **Cross-Layer Latency** | < 50ms per handoff | In-memory zero-copy state references |
| **Statistical Rigor** | DSR > 0.95 | Non-parametric bootstrap in Layer 1 |
| **Safety Violation Rate** | 0.00% | Hard guardrail checks in Layer 4 Compliance Governor |
| **Agent Bidding Latency** | < 15ms | Token-bidding registry in Layer 3 HiveMind |
| **State Consistency** | 100% ACID | Single state writer pattern in Layer 4 WorldModel |
