# Phased Implementation Plan & Evaluation Criteria

## 1. Overview

The APODEX Cognitive Operating System evolution is executed in four structured phases, each governed by objective evaluation criteria, strict validation benchmarks, and zero-regression gates.

---

## 2. Implementation Phases

### Phase 1: Architectural Foundation & Single Cognitive Taxonomy
- **Focus**: Unify Layer 1 Research OS, Layer 2 EIOS/EOS, Layer 3 AEAN, and Layer 4 APODEX under single-source-of-truth specs and interfaces.
- **Key Deliverables**:
  - `UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md`
  - `UNIFIED_DEPENDENCY_GRAPH.md`
  - `CAPABILITY_OWNERSHIP_MATRIX.md`
- **Objective Evaluation Criteria**:
  - Zero duplicated module boundaries across layers.
  - 100% clean importability across all layer modules (`apodex.research_os`, `apodex.arcs.kernel`, `apodex.ai_eos.intelligence`, `apodex.aean`, `apodex.world_model`).

### Phase 2: First-Principles Subsystem Upgrades & Mathematical Hardening
- **Focus**: Harden statistical validation, AST recursion detection, evolutionary workflow optimization, and EFE routing.
- **Key Deliverables**:
  - `StatisticalValidator` with inverse CDF probability clamping.
  - `CodeRewriteEngine` function-scoped recursive call depth AST check.
  - `GeneticWorkflowOptimizer` island MAP-Elites migration gate sorting.
- **Objective Evaluation Criteria**:
  - Zero false positives on standard library call chains during AST rewrite verification.
  - 100% mathematical edge case handling (zero division, overflow/underflow protection).

### Phase 3: End-to-End Cross-Layer Active Inference Integration
- **Focus**: Validate continuous state handoffs from research hypothesis creation through sensing, bidding, execution, and world model belief updates.
- **Key Deliverables**:
  - `ResearchToSystemBridge` orchestration.
  - Cross-layer integration test suite (`tests/integration/test_unified_4layer_integration.py`).
- **Objective Evaluation Criteria**:
  - Unbroken causal trajectory from Layer 1 hypothesis export to Layer 4 causal graph update.
  - 100% integration test suite pass rate.

### Phase 4: Continuous Evaluation & Benchmark Suite
- **Focus**: Execute baseline evaluation suites, regression testing, and system health checks.
- **Key Deliverables**:
  - Execution of all 397+ domain and integration unit/integration tests.
  - Automated system health audit tool (`check_layer_imports.py`).
- **Objective Evaluation Criteria**:
  - Zero test failures across entire codebase (`PYTHONPATH=.:AgentHarness pytest`).
  - Zero deprecation or boundary runtime errors.
