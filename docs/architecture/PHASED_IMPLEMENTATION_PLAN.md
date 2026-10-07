# Phased Implementation Plan & Evaluation Criteria

## Overview

This specification details the 4-Phase implementation rollout for the **Unified Cognitive Operating System**. Each phase defines explicit deliverables, target completion windows, exit criteria, and objective quantitative benchmarks.

---

## Phase Rollout Timeline

```
Phase 1: Architecture Consolidation & Interface Binding  (Weeks 1 - 4)
Phase 2: Closed-Loop Active Inference & Sensing          (Weeks 5 - 8)
Phase 3: Multi-Agent Evolutionary Intelligence          (Weeks 9 - 12)
Phase 4: World Model Autonomy & Continuous Self-Improvement (Weeks 13 - 16)
```

---

## 1. Phase Breakdown & Objective Criteria

### Phase 1: Architecture Consolidation & Interface Standardization
* **Timeline**: Weeks 1 - 4
* **Focus Areas**:
  - Eliminate subsystem duplication between Research OS, EIOS, EOS, AEAN, and APODEX.
  - Standardize all domain models to Pydantic V2 (`ConfigDict`, `model_dump_json`).
  - Implement and verify `ResearchToSystemBridge` cross-layer state handoffs.
* **Objective Evaluation Criteria**:
  - **100% Import Health**: All 4 layer modules import without warnings or errors.
  - **Zero Deprecation Warnings**: All Pydantic V1 legacy usage eliminated.
  - **100% Test Pass Rate**: Full test suite (`pytest tests/`) passes clean.

---

### Phase 2: Closed-Loop Active Inference & Sensing Execution
* **Timeline**: Weeks 5 - 8
* **Focus Areas**:
  - Bind Research OS hypothesis registration directly to EIOS Kernel sensing DAGs.
  - Non-Gaussian Hawkes process anomaly detection with AST call depth bounds.
  - Dynamic capital allocation tree transitions in EOS Engine.
* **Objective Evaluation Criteria**:
  - **Anomalous Signal Latency**: Anomaly detection to hypothesis mapping $< 50\text{ ms}$.
  - **Statistical Control Rigor**: FWER controlled at $\alpha = 0.05$ across all generated hypothesis tests.
  - **Free Energy Reduction**: Mean Expected Free Energy (EFE) reduction $\ge 25\%$ across execution cycles.

---

### Phase 3: Multi-Agent Evolutionary Intelligence & Task Bidding
* **Timeline**: Weeks 9 - 12
* **Focus Areas**:
  - Token-based auction task allocation in AEAN HiveMind.
  - PAEAN evolutionary optimization with MAP-Elites island migration.
  - Epistemic, pre-trade, and RGAE critic gates.
* **Objective Evaluation Criteria**:
  - **Bidding Efficiency**: Token allocation efficiency improved by $\ge 35\%$.
  - **Strategy Diversity**: Behavioral coverage in MAP-Elites grid $\ge 60\%$.
  - **Critic Accuracy**: Pre-trade critic catches $100\%$ of simulated policy violations.

---

### Phase 4: World Model Autonomy & Continuous Self-Improvement
* **Timeline**: Weeks 13 - 16
* **Focus Areas**:
  - Causal graph indexing and digital twin predictive simulation in APODEX WorldModel.
  - Recursive Bayesian belief updating over execution telemetry.
  - Automated benchmark regression suite execution.
* **Objective Evaluation Criteria**:
  - **Belief Convergence**: Posterior probabilities converge within $\le 5$ observation cycles.
  - **Zero Regression Guarantee**: $0\%$ regression rate on historical benchmark suites during self-improvement rollouts.
  - **End-to-End Execution**: Successful 100-cycle autonomous closed-loop run without human intervention.

---

## 2. Quantitative Verification Benchmark Matrix

| Benchmark Metric | Target Value | Verification Tool / Script | Phase |
|---|---|---|---|
| Module Importability | 100% Clean | `audit_and_verify_unified_architecture.py` | Phase 1 |
| Unit & Integration Test Pass Rate | 100% Pass | `PYTHONPATH=.:AgentHarness pytest tests/` | Phase 1 |
| Active Inference EFE Reduction | $\ge 25\%$ | `tests/integration/test_unified_5layer_integration.py` | Phase 2 |
| Bidding Token Efficiency | $\ge 35\%$ Gain | `tests/aean/test_aean.py` | Phase 3 |
| Causal Belief Convergence | $\le 5$ Steps | `tests/world_model/test_wmc_architecture.py` | Phase 4 |
