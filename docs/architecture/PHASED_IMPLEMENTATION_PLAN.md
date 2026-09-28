# Phased Migration & Implementation Plan
**Document Version:** 2.0.0 (2026 Edition)
**Status:** Approved

---

## 1. Phased Migration Milestones

The transition from legacy decoupled modules to the Unified Cognitive Operating System follows a 4-phase zero-downtime implementation schedule.

```
+-----------------------------------------------------------------------------------+
| PHASE 1: Layer Stratification & Boundary Enforcement                              |
| Target: Strict module directory reorganization and import linting.                |
| Criterion: Zero circular imports across Layer 1 -> Layer 2 -> Layer 3 -> Layer 4. |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
| PHASE 2: State Hand-off Bridge & Pydantic Schema Contracts                         |
| Target: Standardize ResearchToSystemBridge and Pydantic DTOs across all layers.  |
| Criterion: 100% test coverage on cross-layer state serialization & validation.   |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
| PHASE 3: Single-Capability Ownership Consolidation                                |
| Target: Deprecate duplicate active inference loops and causal node factories.      |
| Criterion: All causal nodes routed through APODEX WorldModel; single HiveMind.   |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
| PHASE 4: End-to-End Closed-Loop Active Inference Benchmarking                    |
| Target: Continuous research-to-execution flywheel validation.                    |
| Criterion: All 397+ unit/integration tests pass cleanly under pytest.             |
+-----------------------------------------------------------------------------------+
```

---

## 2. Objective Evaluation & Benchmark Criteria

| Milestone Phase | Primary Deliverable | Objective Evaluation Benchmark | Success Target |
|---|---|---|---|
| **Phase 1** | Layer Import Cleanliness | Static AST dependency import checker | 0 import violation warnings |
| **Phase 2** | Inter-Layer State Handoff | Cross-layer integration test suite (`test_unified_5layer_integration.py`) | 100% handoff contract pass rate |
| **Phase 3** | Capability Consolidation | Capability ownership audit script (`audit_and_verify_unified_architecture.py`) | 0 duplicate capability warnings |
| **Phase 4** | End-to-End Flywheel Execution | Full project pytest suite (`pytest -q --import-mode=importlib`) | 100% test pass rate across 397+ tests |
