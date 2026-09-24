# Unified Cognitive Operating System Dependency Graph

## Overview

This document specifies the exact dependency graph, data flows, and subsystem boundary constraints governing the unified 4-layer cognitive architecture.

```
+---------------------------------------------------------------------------------------------------------+
|                                    LAYER 1: RESEARCH OS (Research Layer)                                |
|  - Paper Corpus & Literature Review                                                                     |
|  - Hypothesis Generation & Statistical Validation                                                        |
|  - Reproducibility & Experimentation Engine                                                             |
+---------------------------------------------------------------------------------------------------------+
         |                                                 |                                      |
         | Validated Hypotheses                            | Research Tokens                      | Telemetry Loop
         v                                                 v                                      ^
+-----------------------------------+             +-----------------------------------+           |
| LAYER 2: EIOS / EOS (Orchestration) |             | LAYER 3: AEAN (Intelligence Swarm)|           |
|  - Active Inference Sensing (EFE) |             |  - HiveMind Token Bidding         |           |
|  - DAG Workflow Synthesis         |             |  - Specialized Agent Swarms       |           |
|  - Entrepreneurial State Engine   |             |  - Learnable Routing Gate          |           |
+-----------------------------------+             +-----------------------------------+           |
         |                                                 |                                      |
         | Task DAGs & Allocation                          | Action Proposals & Code Diffs        |
         +-------------------------> + <-------------------+                                      |
                                     |                                                            |
                                     v                                                            |
+---------------------------------------------------------------------------------------------------------+
|                                LAYER 4: APODEX (Decision & Execution Platform)                          |
|  - WorldModel Causal Graph & Bayesian Belief Engine                                                     |
|  - CognitiveBrain & Memory System                                                                       |
|  - CodeRewriteEngine & AST Verification                                                                 |
|  - Governance, Safety & Compliance Gates                                                                |
+---------------------------------------------------------------------------------------------------------+
```

---

## Data Flow & Interface Contracts

### 1. Layer 1 -> Layer 2 (Hypothesis Handoff)
* **Method**: `ResearchToSystemBridge.export_validated_hypothesis_to_kernel()`
* **Payload**: Validated Hypothesis ID, Confidence Score, Expected Utility, Target Subsystem.
* **Effect**: Instantiates active inference observation signal in `EIOSKernel`.

### 2. Layer 1 -> Layer 3 (Insight Registration)
* **Method**: `HiveMind.register_research_insight()`
* **Payload**: Research Principle, Domain Vector, Performance Delta.
* **Effect**: Updates token bidding weight matrix in `HiveMind` for agent task matching.

### 3. Layer 2 -> Layer 3 (Workflow Dispatch)
* **Method**: `EIOSKernel.compile_dag_to_bids()`
* **Payload**: Executable DAG Task Nodes, Token Budget, Expected Free Energy Bound.
* **Effect**: Triggers token auction in AEAN `HiveMind`.

### 4. Layer 3 -> Layer 4 (Action Execution Proposal)
* **Method**: `WorldModel.process_action_proposal()` & `CodeRewriteEngine.verify_proposal_ast()`
* **Payload**: AST Code Patch, Causal Delta Hypothesis, Safety Boundary Verification.
* **Effect**: Executes AST patch with Hawkes recursion depth validation and updates Bayesian belief nodes in `WorldModel`.

### 5. Layer 4 -> Layer 1 & 2 (Feedback Telemetry)
* **Method**: `ResearchOS.ingest_execution_telemetry()` & `EIOSKernel.sense_opportunity_anomalies()`
* **Payload**: Empirical Execution Outcome, Performance Benchmarks, State Anomaly Metrics.
* **Effect**: Triggers Bayesian prior updates in `WorldModel` and drives next-cycle literature review in Research OS.

---

## Boundary Safeguards

* **Zero Duplication**:
  - `Research OS` exclusively owns statistical validation and academic literature querying.
  - `EIOS Kernel` exclusively owns EFE calculation and DAG synthesis.
  - `AEAN HiveMind` exclusively owns token bidding and agent swarm routing.
  - `APODEX WorldModel` exclusively owns causal belief state updates and AST code modifications.
