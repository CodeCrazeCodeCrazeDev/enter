# Phased Implementation Plan

## Phase Overview

The unified cognitive operating system evolution is structured into three concrete phases, ensuring zero regression and continuous empirical validation at each step.

---

## Phase 1: Architecture Formalization & Zero-Duplication Cleanroom
* **Goal**: Establish the authoritative 4-layer taxonomy and eliminate logical duplication across `ResearchOS`, `EIOS`, `EOS`, `AEAN`, and `APODEX`.
* **Actions**:
  1. Draft comprehensive specs: `UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md`, `UNIFIED_DEPENDENCY_GRAPH.md`, `PRIORITIZED_ROI_ROADMAP.md`, `SOTA_GAP_ANALYSIS_2026.md`, `PHASED_IMPLEMENTATION_PLAN.md`, `CONTINUOUS_EVOLUTION_STRATEGY.md`.
  2. Map legacy adapters and ensure canonical module ownership in `apodex/`.
* **Verification Criteria**:
  - All 6 specification documents exist in `docs/architecture/` with complete first-principles coverage.
  - Zero duplicate world state or task-bidding code across layers.

---

## Phase 2: Unified Cross-Layer Bridge Implementation
* **Goal**: Refactor and strengthen cross-layer handoff mechanisms (`ResearchToSystemBridge`).
* **Actions**:
  1. Expose explicit handoff methods: `export_validated_hypothesis_to_kernel`, `dispatch_opportunity_dag`, `execute_skill_protocol`, `publish_observation_residual`.
  2. Ensure clean active inference loop flow from Layer 1 through Layer 4.
* **Verification Criteria**:
  - Modules import cleanly without circular dependency errors.
  - Bridge methods correctly pass structured Pydantic V2 payloads.

---

## Phase 3: Cross-Layer Integration Testing & Benchmark Verification
* **Goal**: Implement end-to-end multi-layer integration tests validating unified cognitive operations.
* **Actions**:
  1. Construct `tests/integration/test_unified_4layer_integration.py`.
  2. Verify full execution pass across all 397+ repository unit/integration tests.
* **Verification Criteria**:
  - 100% test pass rate via `PYTHONPATH=.:AgentHarness python3 -m pytest -q --import-mode=importlib`.
