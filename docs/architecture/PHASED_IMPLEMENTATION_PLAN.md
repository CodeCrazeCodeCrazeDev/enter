# Phased Implementation Plan & Evaluation Criteria

## Phase 1: Foundation Standardization & Layer Unification
* **Deliverables:**
  1. Unified 4-layer architecture specification suite under `docs/architecture/`.
  2. Integration bridge (`ResearchToSystemBridge`) for seamless active inference state handoffs.
  3. Pydantic V2 migration and Python 3.12 datetime UTC standardization across codebase.
* **Evaluation Gate:**
  - Zero deprecation warnings during pytest suite.
  - $100\%$ pass rate across all existing 397 unit and integration tests.

---

## Phase 2: Active Inference Orchestration & Swarm Intelligence
* **Deliverables:**
  1. Closed-loop active inference state handoff test suite (`tests/integration/test_unified_cognitive_architecture_spec.py`).
  2. System audit verification script (`check_unified_cognitive_architecture.py`).
  3. HiveMind token bidding optimization with budget-decayed Expected Free Energy routing.
* **Evaluation Gate:**
  - Complete end-to-end multi-layer execution test passing in $< 10$ seconds.
  - Zero module import circular dependencies.

---

## Phase 3: Continuous Self-Improvement & World Model Validation
* **Deliverables:**
  1. Non-Gaussian Hawkes recursive AST call-depth checks in `CodeRewriteEngine`.
  2. Island MAP-Elites genetic workflow optimization with elite population re-sorting.
  3. Dynamic CausalNode update and Bayesian belief validation in `APODEX WorldModel`.
* **Evaluation Gate:**
  - Pass AST stability verification on $100\%$ of synthetic self-edit proposals.
  - Verification of counterfactual belief updates under simulated noise.
