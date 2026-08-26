# Unified Cognitive Operating System Dependency Graph

## Overview

This document defines the formal dependency graph, control flows, data pipelines, and active inference state handoffs for the **Unified Cognitive Operating System** (Research OS, EIOS/EOS, AEAN, APODEX).

---

## 1. High-Level Subsystem Dependency Graph

```
+-------------------------------------------------------------------------------+
|                       LAYER 4: APODEX DECISION PLATFORM                       |
|  [Governance Veto] <---> [Credit Halt / Budget] <---> [Sandbox Tool Runner]   |
+-------------------------------------------------------------------------------+
                                       ^
                                       | Decision Approval / Audit Trail
                                       v
+-------------------------------------------------------------------------------+
|                      LAYER 3: AEAN COGNITIVE INTELLIGENCE                     |
|  [Swarm Debate] <---> [Graph-of-Thought (GoT)] <---> [EMG/CMOS Memory Store]  |
+-------------------------------------------------------------------------------+
                                       ^
                                       | Execution Strategy & Task Decomposition
                                       v
+-------------------------------------------------------------------------------+
|                      LAYER 2: EIOS / EOS ORCHESTRATION                        |
|  [Active Inference EFE] <---> [13 Business Loops] <---> [Causal SCM Engine]   |
+-------------------------------------------------------------------------------+
                                       ^
                                       | Scientific Principles & Validated Hyps
                                       v
+-------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS LAYER                             |
|  [Literature DB (300 Papers)] <---> [Active Inference] <---> [Stat Audit]     |
+-------------------------------------------------------------------------------+
```

---

## 2. Active Inference State Handoff Pipeline

```
+--------------------+      +--------------------+      +--------------------+
|  Layer 1 Research  |      |   Layer 2 EIOS     |      |    Layer 2 EOS     |
|  - Lit Ingestion   | ---> |  - Sense Anomaly   | ---> | - Evaluate Loops   |
|  - Validate Hyp    |      |  - Minimize EFE    |      | - Causal Do-Calc   |
+--------------------+      +--------------------+      +--------------------+
                                                                  |
                                                                  v
+--------------------+      +--------------------+      +--------------------+
|   Layer 4 APODEX   |      |    Layer 3 AEAN    |      |    Layer 3 AEAN    |
| - Governance Check | <--- | - Skill Selection  | <--- |  - Swarm Debate    |
| - Sandbox Execution|      | - CMOS Memory Sync |      |  - GoT Plan Gen    |
+--------------------+      +--------------------+      +--------------------+
          |
          v
+-------------------------------------------------------------------------------+
|                       FEEDBACK & CONTINUOUS LEARNING LOOP                     |
| Outcome -> Learning Memory -> Research OS Literature Graph Update             |
+-------------------------------------------------------------------------------+
```

---

## 3. Detailed Data & Control Flow Specifications

### Flow 1: Scientific Hypothesis Handoff (Layer 1 -> Layer 2)
1. Layer 1 (`ResearchOS.conduct_literature_review`) queries the 300-paper corpus (`AI_EOS_RESEARCH_DB.yaml` and `ALPHA_ALGO_100_NEW_RESEARCH.yaml`).
2. Synthesizes falsifiable hypotheses $H = \{h_1, h_2, \dots, h_n\}$ with associated statistical confidence $c \in [0, 1]$.
3. Calls `ResearchToSystemBridge.export_validated_hypothesis_to_kernel()` to pass hypotheses into Layer 2 EIOS Kernel.

### Flow 2: Active Inference Sensing & Business Loop Routing (Layer 2)
1. Layer 2 (`EIOSKernel`) evaluates Expected Free Energy:
   $$\text{EFE}(\pi) = -\mathbb{E}_{q(o, \theta|\pi)}[\ln p(o)] - \mathbb{E}_{q(\theta|\pi)}[D_{\text{KL}}(q(o|\theta) \parallel p(o))] $$
   minimizing expected uncertainty and maximizing pragmatic reward.
2. Directs state to `EOSFirstPrinciplesEngine` across 13 coupled business loops (e.g., product-market fit, capital allocation, unit economics).
3. Invokes Pearl's Causal Do-Calculus $P(Y | \text{do}(X))$ interventions to evaluate counterfactual scenarios.

### Flow 3: Cognitive Task Allocation & Memory Retrieval (Layer 2 -> Layer 3)
1. Layer 2 delegates multi-agent tasks to Layer 3 (`AEAN`).
2. Layer 3 invokes `GraphOfThoughtEngine` for step decomposition and `HiveMind` for multi-agent swarm debate (incorporating sycophancy mitigation).
3. Connects to `CMOS` (Cognitive Memory Operating System) and `EMGEngine` (Epistemic Memory Graph) with Ebbinghaus exponential decay filtering:
   $$R(t) = \exp\left(-\frac{t}{S}\right)$$

### Flow 4: Governance Verification & Execution (Layer 3 -> Layer 4)
1. Layer 3 submits execution plan to Layer 4 (`APODEX` Governance).
2. Layer 4 executes non-bypassable Rule 6 check (`CognitiveSystemController.verify_governance_rules()`):
   - Check 1: Budget limit validation ($\text{budget} \le \text{budget}_{\text{cap}}$).
   - Check 2: Command injection and policy check.
   - Check 3: Research confidence lower threshold ($c \ge 0.40$).
3. If approved, executes in isolated sandbox environment and returns audited `DecisionProvenance`.

---

## 4. Subsystem Module Coupling Map

```
apodex/
├── ai_eos/research/      [Layer 1] -> Imports: common
├── research_os/          [Layer 1] -> Imports: common
├── arcs/kernel/          [Layer 2] -> Imports: ai_eos/research, research_os
├── ai_eos/intelligence/  [Layer 2] -> Imports: arcs/kernel
├── aean/                 [Layer 3] -> Imports: ai_eos/intelligence
├── cognition/            [Layer 3] -> Imports: aean, memory, skills
├── skills/               [Layer 3] -> Imports: common
├── memory/               [Layer 3] -> Imports: common
├── governance/           [Layer 4] -> Imports: cognition, world_model
├── safety/               [Layer 4] -> Imports: governance
└── execution/            [Layer 4] -> Imports: safety, harness
```

---

## 5. Summary

The dependency graph enforces unidirectionality across data flow (Layer 1 $\to$ Layer 2 $\to$ Layer 3 $\to$ Layer 4) with clear feedback channels for memory decay, learning, and self-improvement.
