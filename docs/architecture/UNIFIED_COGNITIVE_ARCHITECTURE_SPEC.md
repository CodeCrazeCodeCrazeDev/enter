# Unified Cognitive Operating System Architecture Specification
**Version:** 4.0.0
**Status:** Canonical Reference Architecture
**Scope:** Research OS, EIOS, EOS, AEAN, APODEX

---

## Executive Summary & System Philosophy

The Apodex platform unifies five historically standalone subsystems—**Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX World Model**—into a single, layered, continuous-learning cognitive operating system.

Rather than maintaining separate platforms with overlapping responsibilities, the architecture is structured into **four distinct functional layers**:

```
+-----------------------------------------------------------------------------------+
|  LAYER 4: APODEX (Decision Engine & Execution Platform)                           |
|  - Causal World Model, Recursive Bayesian Beliefs, Safety & Compliance Gates      |
+-----------------------------------------------------------------------------------+
                                         ^
                                         | Policy & Action Directives
                                         v
+-----------------------------------------------------------------------------------+
|  LAYER 3: AEAN (Cognitive Intelligence & Multi-Agent Subsystem)                  |
|  - HiveMind Bidding Engine, Energy-Constrained Dynamic Workflows, Task Allocation |
+-----------------------------------------------------------------------------------+
                                         ^
                                         | Opportunities & Strategy
                                         v
+-----------------------------------------------------------------------------------+
|  LAYER 2: EIOS & EOS (Execution & Strategic Orchestration)                       |
|  - EIOS Active Inference DAG Kernel, EOS Capital & Lifecycle Engine, Market Sensing|
+-----------------------------------------------------------------------------------+
                                         ^
                                         | Validated Research Principles
                                         v
+-----------------------------------------------------------------------------------+
|  LAYER 1: RESEARCH OS (Scientific Research Layer)                                |
|  - Literature Mining, Hypothesis Engine, WDL Execution, Statistical Validation   |
+-----------------------------------------------------------------------------------+
```

---

## Layer Definitions & Interface Contracts

### Layer 1: Scientific Research Layer (Research OS)
- **Primary Responsibility:** Autonomous scientific research, hypothesis generation, paper ingestion, workflow execution, statistical validation, and principle extraction.
- **Key Modules:** `apodex.research_os.*`
- **Exposed Interface:** `ResearchOS`
- **Output Artifacts:** Validated research hypotheses (`ResearchHypothesis`), extracted principles (`ResearchPrinciple`), empirical benchmarks.
- **Handoff Contract:** Exports validated hypotheses to Layer 2 via `export_validated_hypothesis_to_kernel()` and `promote_hypothesis_to_eos()`.

### Layer 2: Execution & Strategic Orchestration Layer (EIOS / EOS)
- **Primary Responsibility:** Entrepreneurial sensing, Active Inference Expected Free Energy (EFE) calculation, Opportunity Graph expansion, capital allocation, and DAG execution.
- **Key Modules:** `apodex.arcs.kernel.*` (EIOS), `apodex.ai_eos.intelligence.*` (EOS Engine)
- **Exposed Interface:** `EIOSKernel`, `FirstPrinciplesEOSEngine`
- **Output Artifacts:** Opportunity DAGs, capital allocation plans, strategic directives.
- **Handoff Contract:** Dispatches opportunity nodes and strategy tokens to Layer 3 (`AEAN HiveMind`).

### Layer 3: Cognitive Intelligence Subsystem (AEAN)
- **Primary Responsibility:** Swarm intelligence, multi-agent token bidding, agent role specialization, budget-decayed task routing, and energetic workflow optimization.
- **Key Modules:** `apodex.aean.coordination.hive_mind.*`, `apodex.aean.core.*`
- **Exposed Interface:** `HiveMind`, `AEANFlywheel`
- **Output Artifacts:** Agent execution trajectories, token allocations, swarm consensus decisions.
- **Handoff Contract:** Translates strategy tokens into action executions evaluated against Layer 4 APODEX World Model.

### Layer 4: Decision Engine & Execution Platform Layer (APODEX World Model)
- **Primary Responsibility:** Causal world modeling, recursive Bayesian belief updates, counterfactual simulation, safety verification, and environment state transitions.
- **Key Modules:** `apodex.world_model.*`, `apodex.cognition.*`
- **Exposed Interface:** `WorldModel`, `CognitiveBrain`
- **Output Artifacts:** Updated causal graphs, Bayesian belief posteriors, state transitions, audit logs.

---

## Core Cross-Layer Flow: Active Inference Bridge

Active Inference forms the mathematical framework for closed-loop state propagation across layers:

$$\mathcal{G}(\pi) = \sum_\tau \left( \underbrace{D_{\text{KL}}\left[ Q(o_\tau | \pi) \parallel P(o_\tau) \right]}_{\text{Epistemic Value (Uncertainty Reduction)}} + \underbrace{\mathbb{E}_{Q(o_\tau | \pi)}\left[ \ln P(o_\tau) \right]}_{\text{Pragmatic Value (Goal Realization)}} \right)$$

1. **Layer 1 (Research OS)** validates a scientific insight and estimates prior uncertainty $P(\theta)$.
2. **Layer 2 (EIOS/EOS)** computes Expected Free Energy (EFE) for executing the insight in market/code space.
3. **Layer 3 (AEAN)** dispatches agents via HiveMind bidding to execute actions minimizing EFE.
4. **Layer 4 (APODEX World Model)** observes outcome $o_\tau$, updates Bayesian beliefs $Q(\theta)$, and feeds back structural risk anomalies to Layer 1 and 2.
