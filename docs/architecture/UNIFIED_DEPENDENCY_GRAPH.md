# Unified Dependency Graph & Inter-Subsystem Interaction Matrix
**Authoritative Architectural Standard for Information & Control Flow**
**Version:** 4.0.0
**Status:** Canonical Reference Specification

---

## Executive Overview

This document specifies the formal directional dependencies, control loops, event streams, and data contracts between the four layers of the unified cognitive operating system.

---

## 1. Directional Data Flow Diagram

```
 +-----------------------------------------------------------------------+
 |                 LAYER 1: RESEARCH OS (Research Layer)                |
 |                                                                       |
 | - Hypotheses ($H_0$ / $H_1$)        - Power Analysis & Exp. Design   |
 | - Walk-Forward Validation Results   - Deflated Sharpe Ratios (DSR)    |
 +-----------------------------------------------------------------------+
                                    |
                                    | ResearchToSystemBridge
                                    | Promotes Validated Insights
                                    v
 +-----------------------------------------------------------------------+
 |               LAYER 2: EIOS / EOS (Execution & Decision Layer)        |
 |                                                                       |
 | - EFE Active Inference Sensing      - Coupled Business Loops          |
 | - Opportunity Decision Trees        - Capital Allocation Vectors      |
 +-----------------------------------------------------------------------+
                                    |
                                    | Dynamic Task DAGs &
                                    | Resource Allocation Bids
                                    v
 +-----------------------------------------------------------------------+
 |              LAYER 3: AEAN HIVEMIND (Intelligence Layer)              |
 |                                                                       |
 | - Agent Token Arbitration           - Non-Gaussian Hawkes Scheduler   |
 | - Learnable EFE Dispatcher          - Graph-of-Thought (GoT) Search   |
 +-----------------------------------------------------------------------+
                                    |
                                    | Tool Actions, Prompts &
                                    | Code Rewrite Proposals
                                    v
 +-----------------------------------------------------------------------+
 |            LAYER 4: APODEX WORLDMODEL (Platform & Execution)          |
 |                                                                       |
 | - Causal Entity Graph Updates       - Recursive Bayesian Beliefs      |
 | - Micro-VM Sandbox Runtime          - DPO Preference Trajectory Logs  |
 +-----------------------------------------------------------------------+
                                    |
                                    | Empirical Outcomes, Telemetry &
                                    | Preference Trajectories
                                    +-----------------------+
                                                            |
                                                            v
                                            Feedback Loop to Layers 1, 2 & 3
```

---

## 2. Layer Interaction Matrix

| Source Layer | Target Layer | Mechanism / Protocol | Content / Payload |
| :--- | :--- | :--- | :--- |
| **Layer 1 (Research OS)** | **Layer 2 (EIOS/EOS)** | `ResearchToSystemBridge.promote_and_disseminate_hypothesis` | Validated research hypotheses, statistical significance bounds, and utility parameters. |
| **Layer 2 (EIOS/EOS)** | **Layer 3 (AEAN)** | `EIOSKernel.compile_task_dag` | Structured execution DAGs, task complexity estimates, domain requirements, and financial budgets. |
| **Layer 3 (AEAN)** | **Layer 4 (APODEX)** | `HiveMind.arbitrate` & `CodeRewriteEngine` | Evaluated agent tool calls, GoT reasoning traces, and AST-verified code rewrite proposals. |
| **Layer 4 (APODEX)** | **Layer 1 (Research OS)** | `SFTPreferenceCollector.compile_dpo_preference_pair` | Empirical execution telemetry, actual vs predicted outcome gaps, and DPO training pairs. |
| **Layer 4 (APODEX)** | **Layer 2 (EIOS/EOS)** | `WorldGraphManager.update_entity` | Real-time state updates, causal graph weights, and Bayesian belief confidence adjustments. |

---

## 3. Active Inference Control Loops

### A. Primary Active Inference Loop
1. **Sensory Ingestion (Layer 2):** EIOS Kernel senses environmental signals ($y_t$) and measures prediction error relative to generative world model expectations.
2. **EFE Evaluation (Layer 2 & 3):** Tasks are evaluated for Expected Free Energy ($G(\pi) = \text{Epistemic} + \text{Pragmatic} - \text{Cost}$).
3. **Token Arbitration & Execution (Layer 3 & 4):** AEAN HiveMind allocates compute tokens to high-EFE actions; APODEX micro-VM executes tool calls.
4. **World Model Belief Update (Layer 4):** Outcome observations ($o_t$) trigger recursive Bayesian belief propagation in `WorldGraphManager`.

### B. Scientific Hypothesis Flywheel Loop
1. **Discovery (Layer 1):** Research OS identifies epistemic whitespace through automated literature review synthesis.
2. **Hypothesis Registration & Sandbox Testing (Layer 1):** Scientific experiments are designed with power analysis and executed in walk-forward sandboxes.
3. **Statistical Promotion (Layer 1 -> Layer 2):** Hypotheses satisfying Bonferroni-corrected significance ($\alpha_{\text{corrected}}$) and positive Deflated Sharpe Ratio are promoted via `ResearchToSystemBridge`.
4. **System Integration (Layer 2, 3, 4):** Validated principles are ingested into EIOS sensing rules, AEAN routing parameters, and APODEX causal belief nodes.
