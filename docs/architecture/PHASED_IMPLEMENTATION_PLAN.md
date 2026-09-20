# Phased Implementation Plan & Evaluation Criteria
**Step-by-Step Execution Plan with Benchmarkable Milestones**
**Version:** 4.0.0
**Scope:** Research OS (Layer 1) | EIOS & EOS (Layer 2) | AEAN (Layer 3) | APODEX (Layer 4)

---

## 1. Executive Overview

This plan details the phased execution roadmap for deploying, verifying, and maintaining the **Unified 4-Layer Cognitive Operating System Architecture**. Each phase specifies clear objectives, target layers, deliverables, complexity budgets, failure modes, and objective evaluation criteria.

---

## 2. Implementation Phases

### Phase 1: Layer Consolidation & Boundary Enforcement (Weeks 1 - 2)
- **Primary Objective:** Enforce strict layer boundaries across Layer 1 (Research OS), Layer 2 (EIOS/EOS), Layer 3 (AEAN), and Layer 4 (APODEX). Deprecate legacy logical duplication in adapters and standalone planners.
- **Deliverables:**
  - Standardized module imports across all 4 layers.
  - Creation of `ResearchToSystemBridge` for formal hypothesis handoffs.
  - Canonical state management in Layer 4 `APODEX.WorldModel`.
- **Complexity Budget:** Net reduction of $>1,500$ lines of duplicated adapter code.
- **Evaluation Criteria:**
  1. `check_layer_imports.py` passes with zero import errors or circular dependencies.
  2. All 397+ existing pytest unit tests pass cleanly without regressions.

### Phase 2: Active Inference Scheduling & Token Bidding Auction Engine (Weeks 3 - 4)
- **Primary Objective:** Upgrade Layer 2 workflow scheduling to formal Active Inference Expected Free Energy ($G(u)$) minimization and deploy Layer 3 market-based token bidding auctions.
- **Deliverables:**
  - Integrated `EIOSKernel` active inference DAG scheduler.
  - Token bidding auction mechanism in `HiveMind` (`submit_bidding_auction`).
  - Hawkes process AST call-depth tracking in `CodeRewriteEngine`.
- **Complexity Budget:** Max execution latency $< 20\text{ms}$ per scheduling/bidding iteration.
- **Evaluation Criteria:**
  1. Task scheduling throughput increases by $\ge 35\%$ under high task loads.
  2. Zero infinite AST recursion errors during automated code modification tests.

### Phase 3: Unified Causal World Modeling & Recursive Bayesian Inference (Weeks 5 - 6)
- **Primary Objective:** Consolidate all state representations and belief tracking into Layer 4 `APODEX.WorldModel`, providing continuous Bayesian belief updating and multi-tier budget governance.
- **Deliverables:**
  - Causal graph node/edge entity representation.
  - Recursive Bayesian belief update engine ($\text{Prior} \to \text{Likelihood} \to \text{Posterior}$).
  - Multi-tier credit halting and governance approval gates.
- **Complexity Budget:** Memory footprint for causal graph updates stays under $250\text{MB}$ for 10,000 entities.
- **Evaluation Criteria:**
  1. Belief update accuracy reaches $\ge 98\%$ on synthetic evidence benchmarks.
  2. 100% enforcement of daily compute/credit halting when budget thresholds are breached.

### Phase 4: Full Cross-Layer Integration & Continuous Benchmark Suite (Weeks 7 - 8)
- **Primary Objective:** Execute end-to-end integration across all 4 layers, validating joint multi-subsystem workflows from Layer 1 hypothesis validation to Layer 4 execution and feedback loops.
- **Deliverables:**
  - Comprehensive end-to-end test suites (`test_unified_cognitive_os_e2e.py` and `test_unified_4layer_integration.py`).
  - Automated continuous benchmark script (`verify_architecture_docs.py`).
- **Complexity Budget:** Total test suite runtime $< 15$ seconds.
- **Evaluation Criteria:**
  1. 100% test pass rate across all unit, integration, and performance benchmarks.
  2. Zero title/DOI overlap across the 500-paper research corpus.

---

## 3. Failure Mode Diagnostics & Recovery Protocols

| Failure Mode ID | Failure Scenario | Detection Mechanism | Automated Recovery Protocol |
| :---: | :--- | :--- | :--- |
| **FM-01** | Circular import lock between Layer 2 and Layer 3 | Module collection error in `pytest` | Enforce asynchronous event bus dispatching (`EventDispatcher`) |
| **FM-02** | Infinite AST recursion during self-improvement | Hawkes process depth exceedance ($D > 10$) | Reject proposal, roll back AST patch, log anomaly |
| **FM-03** | Credit / Token budget breach during long-horizon tasks | Layer 4 `CreditHalter` trigger | Immediately downshift execution to safe mode or halt execution |
| **FM-04** | Divergent causal beliefs across layers | Bayesian variance check $\sigma^2 > 0.8$ | Re-query Layer 1 literature corpus and reset belief priors |
