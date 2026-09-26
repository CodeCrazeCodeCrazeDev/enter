# Unified Capability Ownership Matrix

## 1. Overview

To eliminate architectural duplication across **Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX**, this matrix assigns **100% of system capabilities** to exactly **one primary owning layer**.

No two layers are permitted to duplicate core capability logic. Shared utilities (e.g., logging, basic math utilities) reside in common infrastructure, but business/cognitive reasoning logic is strictly single-owned.

---

## 2. Comprehensive Capability Mapping Matrix

| Capability ID | Capability Name | Primary Owning Layer | System Component | Status / Resolution of Duplicate Logic |
|---|---|---|---|---|
| CAP-01 | Paper Ingestion & Literature Search | Layer 1 | `ResearchOS.conduct_literature_review` | **Canonical.** (Removed duplicate paper lookup in AEAN). |
| CAP-02 | Empirical Hypothesis Generation | Layer 1 | `ResearchOS.formulate_hypothesis` | **Canonical.** Generates research hypotheses. |
| CAP-03 | Deflated Sharpe Ratio Validation | Layer 1 | `statistical_validation.py` | **Canonical.** Performs statistical p-hacking checks. |
| CAP-04 | Active Inference Sensing | Layer 2 | `EIOSKernel.sense_opportunity_anomalies` | **Canonical.** Senses market & environment anomalies. |
| CAP-05 | Active Inference DAG Compilation | Layer 2 | `EIOSKernel.compile_active_inference_dag` | **Canonical.** Replaces legacy redundant planners. |
| CAP-06 | Unit Economics & GTM Dynamics | Layer 2 | `EOSEngine.evaluate_opportunities` | **Canonical.** Evaluates TAM, LTV/CAC, capital burn. |
| CAP-07 | Company Growth State Machine | Layer 2 | `CompanyGrowthStateMachine` | **Canonical.** Manages funding & growth stages. |
| CAP-08 | Swarm Token Bidding | Layer 3 | `HiveMind.submit_task_bid` | **Canonical.** Bids for task execution rights. |
| CAP-09 | Multi-Agent Strategy Consensus | Layer 3 | `HiveMind.resolve_bids_and_execute` | **Canonical.** Resolves agent execution consensus. |
| CAP-10 | Working Context Memory | Layer 3 | `CMOSMemory` | **Canonical.** Manages short-term agent scratchpad. |
| CAP-11 | Long-Term Trajectory Memory | Layer 3 | `LongTermLearningMemory` | **Canonical.** Stores execution trajectory records. |
| CAP-12 | AST Code Rewrite & Hawkes Bounds | Layer 3 | `CodeRewriteEngine` | **Canonical.** Handles automated software engineering. |
| CAP-13 | Causal World Graph Maintenance | Layer 4 | `WorldModel.create_node` | **Canonical.** Single source of truth for causal state. |
| CAP-14 | Recursive Bayesian Belief Update | Layer 4 | `WorldModel.update_belief` | **Canonical.** Single source of truth for belief priors. |
| CAP-15 | Meta-Reasoning & Active State | Layer 4 | `CognitiveBrain.step` | **Canonical.** Orchestrates top-level meta-cognition. |
| CAP-16 | Institutional Safety & Governance | Layer 4 | `ApprovalEngine` & `SafetyCore` | **Canonical.** Enforces cost halts & tier approvals. |

---

## 3. Legacy Duplication Resolution Audit

1. **Resolution 1 (Hypothesis Evaluation):**
   - *Legacy State:* Research OS, EOS Engine, and APODEX all had separate hypothesis validation functions.
   - *Unified State:* Research OS owns scientific research hypothesis validation (Layer 1). EOS Engine owns entrepreneurial opportunity evaluation (Layer 2). APODEX WorldModel maintains causal beliefs about verified hypotheses (Layer 4).

2. **Resolution 2 (Task Planning):**
   - *Legacy State:* EIOS Kernel, AEAN Planner, and AgentHarness had duplicate planning loops.
   - *Unified State:* EIOS Kernel owns Active Inference EFE DAG compilation (Layer 2). AEAN agents execute assigned DAG nodes via HiveMind bidding (Layer 3).

3. **Resolution 3 (Memory & State):**
   - *Legacy State:* CMOS and AgentHarness memory modules had overlapping vector/working memory stores.
   - *Unified State:* All working & episodic agent memory is consolidated in AEAN CMOS Memory (Layer 3). All environmental/causal belief state is consolidated in APODEX WorldModel (Layer 4).
