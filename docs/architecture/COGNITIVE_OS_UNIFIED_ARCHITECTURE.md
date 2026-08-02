# Unified Cognitive OS: Architectural Specification & System Mapping
## Evolving APODEX, AEAN, EOS, and EIOS into a Unified, Single-Owner Cognitive Substrate

---

## 1. Executive Summary & Core Design Principles

This document establishes the canonical **Unified Cognitive OS Architecture Specification** for the platform. We reject the fragmented view of APODEX, AEAN, EOS, and EIOS as independent projects. Instead, they are mapped as tightly integrated layers of a single, non-duplicative cognitive system governed by **Expected Free Energy minimization**, **SCM Causal Intervention**, and **Strict Division of Powers**.

### 1.1 Core Principles of the Unified System
1. **Single Capability Ownership:** Every strategic, cognitive, or operational capability must have exactly one authoritative subsystem owner. No duplicate planners, orchestrators, memory systems, or world models are permitted.
2. **Epistemic vs. Operational Isolation:** Epistemic discovery (Research OS / Layer 3) must be strictly insulated from operational execution (EOS / Layer 1) to prevent experimental failures from destabilizing active business processes.
3. **Control-Theory Calibration:** Strategic choices are treated as active inference trajectories, continuously calibrated via prediction error tracking (KL-Divergence) and bounded by a non-bypassable safety core.

---

## 2. Layered Architecture & Subsystem Responsibilities

```
+-------------------------------------------------------------------------+
| Layer 3: EIOS (Strategic Reasoning & Epistemic Governance)              |
| - Imperative: Optimize Portfolio Allocation, Capital & SCM Interventions|
| - Key Subsystems: Venture Engine, SCM do-calculus, Lagrange Multipliers |
+-------------------------------------------------------------------------+
                                    | Promoted Strategies
                                    v
+-------------------------------------------------------------------------+
| Layer 2: APODEX (Cognitive Control Plane & Task Orchestration)          |
| - Imperative: Plan-and-Act isolation, GoT reasoning, Self-Improvement   |
| - Key Subsystems: StrategicPlanner, ActiveLearning, MetaReasoner        |
+-------------------------------------------------------------------------+
                                    | Executable Workflows & Prompts
                                    v
+-------------------------------------------------------------------------+
| Layer 1: EOS (Operational Execution & Execution Loops)                  |
| - Imperative: Run local business loops, trace steps, log metrics        |
| - Key Subsystems: Operational Loops, EMG Engine (L1 Tracing)            |
+-------------------------------------------------------------------------+
                                    | Traces, Facts & Beliefs
                                    v
+-------------------------------------------------------------------------+
| Layer 0: AEAN (Multi-Agent Substrate & Safety Core)                     |
| - Imperative: Relational SQLite Storage, Parallel Verification, GRC     |
| - Key Subsystems: SemanticMemory, ParallelVerifier, SafetyCore          |
+-------------------------------------------------------------------------+
```

### 2.1 EIOS (Layer 3: Strategic Reasoning & Epistemic Governance)
- **Primary Responsibilities:** High-level venture capital portfolio scheduling, SCM causal diagram formulation, backdoor/frontdoor do-calculus interventions, Lagrange dual shadow price bottleneck identification, and expected originality scoring.
- **Epistemic Boundary:** Formulates macroeconomic and competitive hypotheses, directing Research OS to validate them via isolated simulation sandboxes.

### 2.2 APODEX (Layer 2: Cognitive Control Plane & Task Orchestration)
- **Primary Responsibilities:** Cognitive planning (MCTS exploration-exploitation search trees), Graph-of-Thought (GoT) dialectical debate orchestration, text-based backpropagation (TextGrad prompt editing) based on mined weaknesses, and multi-agent swarm scheduling.
- **Orchestration Boundary:** Consolidates all execution coordination, preventing AEAN or EOS from spawning independent planners or orchestrators.

### 2.3 EOS (Layer 1: Operational Execution & Loops)
- **Primary Responsibilities:** Runs the 13 continuous business operational loops (Product, GTM, CS, Sales, Finance, etc.). Logs fine-grained step telemetry and metrics (tokens, latency, thinking blocks) as uniquely identified DAG nodes in the Experience Memory Graph (EMG).
- **Execution Boundary:** Serves as the stable runtime target, executing tasks mapped to active venture and GTM plans.

### 2.4 AEAN (Layer 0: Multi-Agent Substrate & Safety Core)
- **Primary Responsibilities:** Thread-safe, transaction-secure persistent storage via the relational SQLite Semantic Memory repository, context-matching evidence retrieval, parallel correctness verifiers, and Hendrycks-compliant Safety Core audit gates.
- **Physical Boundary:** Manages the low-level model APIs, DB connections, and process sandboxes.

---

## 3. Singular Capability Ownership Matrix

To eliminate overlapping responsibilities and redundant implementations, we establish a strict, non-waivable singular ownership mapping:

| Core Subsystem / Capability | Authoritative Owner | Redundant Duplications Eliminated |
| :--- | :--- | :--- |
| **Cognitive Planner** | `StrategicPlanner` (APODEX) | Eliminated independent planning logic in AEAN and EOS. |
| **Swarm Orchestrator** | `CognitiveSystemController` (APODEX) | Consolidated competing agent controllers into a single manager. |
| **Active Inference Engine**| `ActiveInferenceEngine` (EIOS) | Merged redundant free energy math across the active loops. |
| **Causal Inference / SCM** | `DecisionEngine` (EIOS) | Prevented local loops from attempting heuristic causal adjustments. |
| **Execution Trace Graph** | `EMGEngine` (EOS) | Merged separate ad-hoc step-logging hooks into one tracing engine. |
| **Persistent Memory DB** | `SQLiteMemoryRepository` (AEAN) | Eliminated in-memory transient dictionaries and separate databases. |
| **Self-Improvement Loop** | `HarnessRefiner` (APODEX) | Consolidated separate prompt and parameter edit generators. |
| **Safety & GRC Gate** | `ConstitutionalFilter` (AEAN) | Consolidated isolated compliance and boundary filters. |
