# Unified Cognitive Operating System Specification

## Executive Summary
This document defines the unified 4-layer computational architecture of the Autonomous Intelligence Platform, eliminating architectural duplication and establishing explicit single-responsibility layer boundaries across:
- **Layer 1: Scientific Research Layer (Research OS)**
- **Layer 2: Execution & Orchestration Layer (EIOS / EOS)**
- **Layer 3: Cognitive Intelligence Layer (AEAN)**
- **Layer 4: Decision & Execution Platform Layer (APODEX)**

---

## 1. Single Layered Architectural Framework

```
+---------------------------------------------------------------------------------+
|               LAYER 4: DECISION & EXECUTION PLATFORM (APODEX)                   |
|  - World Model State (Entities, Beliefs, Relations)                             |
|  - Skill Registry & Executable Flywheel (60 Pre-populated Skills)              |
|  - Safety Core, Tiered Approval & Institutional Reliability Governance          |
+---------------------------------------------------------------------------------+
                                       ^
                                       | Beliefs, Skills & Governance Controls
                                       v
+---------------------------------------------------------------------------------+
|               LAYER 3: COGNITIVE INTELLIGENCE LAYER (AEAN)                      |
|  - HiveMind Multi-Agent Coordination & Token Bidding Auction                    |
|  - Graph-of-Thought (GoT) & Active Learning Reasoning                           |
|  - Episodic & Semantic Memory Engines (EMG / CMOS / MemoHarness)                |
+---------------------------------------------------------------------------------+
                                       ^
                                       | Cognition & Task Decomposition
                                       v
+---------------------------------------------------------------------------------+
|            LAYER 2: EXECUTION & ORCHESTRATION LAYER (EIOS / EOS)                |
|  - EIOS Kernel: Active Inference Anomaly Sensing & Opportunity Sensing          |
|  - EOS Engine: 14-Layer Computational Engine & Business Loop Dynamics          |
|  - State Machine Transition & Budget-Bounded Dispatching                        |
+---------------------------------------------------------------------------------+
                                       ^
                                       | Sensing Anomalies & Business State
                                       v
+---------------------------------------------------------------------------------+
|                 LAYER 1: SCIENTIFIC RESEARCH LAYER (Research OS)                |
|  - 500-Paper Corpus Literature Review & Active Evidence Ingestion               |
|  - Hypothesis Generation, Verification & Statistical Bound Validations          |
|  - Do-Calculus Causal Interventions & Reproducibility Metrics                   |
+---------------------------------------------------------------------------------+
```

---

## 2. Comprehensive Layer Definitions & Responsibilities

### Layer 1: Scientific Research Layer (Research OS)
- **Primary Function:** Continuous acquisition of empirical AI research, hypothesis synthesis, do-calculus causal inference, and statistical validation.
- **Key Modules:** `apodex/ai_eos/research/research_os.py`, `apodex/research_os/statistical_validation.py`, `apodex/research_os/reproducibility.py`.
- **Inputs:** Raw research papers (corpus DBs 1-500), empirical experiment outcomes.
- **Outputs:** Verified scientific hypotheses, transferable engineering principles, statistical significance bounds.

### Layer 2: Execution & Orchestration Layer (EIOS / EOS)
- **Primary Function:** Active inference sensing (EIOS Kernel), system state machine transition management, and 14-layer computational entrepreneurship orchestration (EOS Engine).
- **Key Modules:** `apodex/arcs/kernel/kernel.py`, `apodex/ai_eos/intelligence/eos_engine.py`, `apodex/ai_eos/intelligence/fourteen_layer_engine.py`.
- **Inputs:** Hypotheses from Layer 1, market & operational anomaly signals from Layer 4.
- **Outputs:** System state transitions, Active Inference Expected Free Energy (EFE) task delegations, loop control directives.

### Layer 3: Cognitive Intelligence Layer (AEAN)
- **Primary Function:** Multi-agent swarm coordination, epistemic curiosity bidding, high-level planning, Graph-of-Thought reasoning, and multi-scale memory retrieval.
- **Key Modules:** `apodex/aean/coordination/hive_mind.py`, `apodex/cognition/brain.py`, `agent_harness/core/memory/emg_engine.py`.
- **Inputs:** Task delegations & state transitions from Layer 2.
- **Outputs:** Multi-agent task plans, synthesized reasoning paths, structured context from EMG/CMOS memory.

### Layer 4: Decision & Execution Platform Layer (APODEX)
- **Primary Function:** Authoritative state model of reality (WorldModel), bayesian belief updating, skill execution flywheel, safety policy enforcement, and final tool interaction.
- **Key Modules:** `apodex/world_model/world_model.py`, `apodex/skills/registry.py`, `apodex/world_model/governance/approval.py`.
- **Inputs:** Execution plans from Layer 3.
- **Outputs:** Real-world tool actions, updated entity states, compliance approvals, feedback metrics to Layer 1.

---

## 3. Trade-off & Failure Mode Analysis

| Layer | Primary Failure Mode | Mitigation Strategy |
|---|---|---|
| Layer 1 (Research OS) | Hypothesis overfitting / invalid p-hacking | Clamped probability PPF inverse CDF & Deflating Sharpe Ratio (DSR) checks |
| Layer 2 (EIOS/EOS) | State machine deadlock or budget depletion | Budget-bounded fallbacks & active inference EFE priority queues |
| Layer 3 (AEAN) | Multi-agent sycophancy & infinite reasoning loops | Token-bidding auction mechanisms & depth-bounded Graph-of-Thought pruning |
| Layer 4 (APODEX) | Out-of-bounds entity updates or safety breaches | Tiered compliance approval gates & transactional rollback logs |
