# Phased Implementation Plan & Objective Evaluation Criteria

## 1. Executive Summary & Phased Strategy

This plan outlines the 6-phase incremental implementation roadmap for the unified 4-layer cognitive operating system. Each phase enforces strict objective evaluation criteria, automated test benchmarks, and SLA gating thresholds prior to milestone sign-off.

---

## 2. 6-Phase Implementation Roadmap

```
Phase 1: Interface Normalization (P0)
   ├── Type-safe cross-layer handoffs
   └── Duplicate component elimination
            │
            v
Phase 2: Active Inference & Sensing Loop Integration (P0)
   ├── EIOS Kernel EFE minimization
   └── 14-Layer computational engine routing
            │
            v
Phase 3: AEAN Swarm Bidding & GoT Reasoner Unification (P1)
   ├── HiveMind token bidding registry
   └── Graph-of-Thought search & active learning
            │
            v
Phase 4: APODEX Execution & Safety Core Governance (P1)
   ├── 60 canonical skills in SkillRegistry
   └── Hard credit halt & budget enforcement
            │
            v
Phase 5: Self-Improvement Flywheel & Code Rewrite (P2)
   ├── 500-paper principle extraction pipeline
   └── Non-Gaussian Hawkes code stability patches
            │
            v
Phase 6: Institutional-Grade Robustness & Chaos Benchmarking (P2)
   ├── Fault injection & multi-seed ablation
   └── SLA breach automated rollback flywheel
```

---

## 3. Phase Specifications & Milestone Gating Criteria

### Phase 1: Interface Normalization & Core Architecture Standardization
* **Objective**: Establish unified data contracts (`ResearchHypothesisHandoff`, `OpportunityDAGContract`, `SkillExecutionTask`) and eliminate all logical component duplication.
* **Key Tasks**:
  1. Standardize Layer 1 to Layer 4 bridge methods in `apodex.ai_eos.research.integration`.
  2. Enforce single canonical owners according to the Capability Ownership Matrix.
  3. Ensure clean test collection across `tests/`.
* **Objective Evaluation Criteria**:
  - 100% test pass rate across unit and integration test suites (`pytest`).
  - Zero cross-layer module circular dependency warnings.
  - Sub-millisecond interface serialization overhead (<1ms).

### Phase 2: Active Inference & Sensing Loop Integration
* **Objective**: Consolidate sensing and state estimation into `EIOSKernel` and `EOSEngine` using Expected Free Energy minimization.
* **Key Tasks**:
  1. Implement `EIOSKernel.sense_opportunity_anomalies` over research hypotheses.
  2. Map 14 business layers in `FourteenLayerEntrepreneurialEngine`.
* **Objective Evaluation Criteria**:
  - $\ge 40\%$ reduction in exploratory step variance under high epistemic uncertainty.
  - Sensing loop execution latency $\le 50\text{ms}$.

### Phase 3: AEAN Swarm Bidding & Graph-of-Thought Unification
* **Objective**: Deploy auction-based multi-agent coordination in `HiveMind` and non-linear logic verification in `GraphOfThoughtEngine`.
* **Key Tasks**:
  1. Register worker agents (Researcher, Architect, Engineer, Validator) with skill scores.
  2. Integrate active learning uncertainty decomposition into GoT branch pruning.
* **Objective Evaluation Criteria**:
  - Task allocation speedup $\ge 2.0\text{x}$ compared to sequential agent routing.
  - Reasoning contradiction catch rate $\ge 95\%$.

### Phase 4: APODEX Execution & Safety Core Governance
* **Objective**: Unify skill execution around 60 pre-populated skills in `SkillRegistry` with fail-closed governance in `SafetyCore`.
* **Key Tasks**:
  1. Pre-populate 60 strategic and operational skills in `SkillRegistry`.
  2. Wire `CostCuttingEngine` and credit halt thresholds into `SkillRunner`.
* **Objective Evaluation Criteria**:
  - 100% compliance with cost-tier budget halts (zero budget overruns).
  - Skill execution SLA $\le 500\text{ms}$ per invocation.

### Phase 5: Self-Improvement Flywheel & Code Rewrite Pipeline
* **Objective**: Automate code rewrite patches backed by quantitative research principles (Papers 1-500) and workflow optimization.
* **Key Tasks**:
  1. Connect `CodeRewriteEngine` to `ResearchOS` literature querying.
  2. Execute Island MAP-Elites workflow optimization for agent prompt strategies.
* **Objective Evaluation Criteria**:
  - Automated code rewrite pass rate $\ge 90\%$ on unit test verification.
  - Zero syntax or runtime regressions introduced by self-improvement patches.

### Phase 6: Institutional Robustness & Chaos Benchmarking
* **Objective**: Validate end-to-end system resilience against fault injection, network partition simulations, and SLA breaches.
* **Key Tasks**:
  1. Execute chaos injection tests in `tests/ai_eos/test_phase8.py`.
  2. Verify deterministic regression replay in `test_regression_replay_determinism`.
* **Objective Evaluation Criteria**:
  - 100% recovery rate from injected agent faults within 3 execution cycles.
  - Automated rollback triggered within $< 100\text{ms}$ of SLA breach.

---

## 4. Quantitative Summary Gating Table

| Phase | Milestone Name | Primary Evaluation Metric | Target Threshold | Test Suite Target |
| :---: | :--- | :--- | :---: | :--- |
| **P1** | Interface Normalization | Clean Import & Handoff SLA | 100% Pass / <1ms | `tests/integration/` |
| **P2** | Active Inference Sensing | EFE Epistemic Value Gain | $\ge 40\%$ Reduction | `tests/arcs/`, `tests/ai_eos/` |
| **P3** | Swarm Bidding & GoT | Contradiction Detection | $\ge 95\%$ Precision | `tests/aean/`, `tests/reasoning/` |
| **P4** | APODEX Execution & Safety | Budget Halt Compliance | 100% Fail-Closed | `tests/world_model/`, `tests/skills/` |
| **P5** | Self-Improvement Flywheel | Code Patch Verification Rate | $\ge 90\%$ Success | `tests/research_os/` |
| **P6** | Institutional Robustness | Fault Recovery & Replay | 100% Deterministic | `tests/ai_eos/test_phase8.py` |
