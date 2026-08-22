# Phased Implementation Plan: Unified Cognitive Operating System

## Executive Summary

This document specifies the end-to-end phased implementation, migration, and verification plan for deploying the **Unified Cognitive Operating System** (**Research OS**, **AEAN**, **EIOS/EOS**, and **APODEX**).

The plan ensures zero downtime, backwards compatibility for legacy interfaces, and rigorous quantitative verification at every phase transition.

---

## 1. Phase Structure & Milestones

```
+-------------------------------------------------------------------------------+
| PHASE 1: Architectural Boundary Enforcement & Legacy Adapter Consolidation     |
| Duration: Weeks 1 - 2                                                         |
| Focus: Layer boundary validation, single-source registry, test alignment      |
+-------------------------------------------------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| PHASE 2: Active Inference & Multi-Tier Memory Integration                     |
| Duration: Weeks 3 - 5                                                         |
| Focus: EFE formulation, Ebbinghaus memory decay, GoT planner optimization     |
+-------------------------------------------------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| PHASE 3: Causal Execution Engine & Risk-Gated Orchestration                   |
| Duration: Weeks 6 - 8                                                         |
| Focus: Pearl Do-calculus, 14-Layer Engine, Kelly Criterion portfolio sizing   |
+-------------------------------------------------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| PHASE 4: Scientific Research OS Engine & Self-Improvement Flywheel            |
| Duration: Weeks 9 - 12                                                        |
| Focus: Hypothesis engine, Welch's t-test verification, APODEX code synthesis  |
+-------------------------------------------------------------------------------+
```

---

## 2. Detailed Phase Specifications

### Phase 1: Boundary Enforcement & Legacy Consolidation
* **Target Subsystems:** `apodex/aean/`, `agent_harness/`, `apodex/skills/`
* **Key Deliverables:**
  1. Validate non-overlapping responsibilities across Layer 1 (Research OS), Layer 2 (AEAN), Layer 3 (EIOS/EOS), and Layer 4 (APODEX).
  2. Maintain `agent_harness` adapter shims for legacy protocol compatibility without code duplication.
  3. Ensure all 60 skills in `SkillRegistry` map strictly to canonical execution targets in APODEX.
* **Objective Evaluation Criteria:**
  - `python3 scripts/validate_dependencies.py` passes with 0 circular imports.
  - 100% pass rate on existing 397 unit and integration tests.

### Phase 2: Active Inference & Multi-Tier Memory Integration
* **Target Subsystems:** `apodex/cognition/`, `apodex/memory/`, `apodex/planning/`
* **Key Deliverables:**
  1. Standardize `CognitiveBrain` policy selection on Expected Free Energy (EFE = Pragmatic Value + Epistemic Gain).
  2. Implement Ebbinghaus memory decay $R(t) = \exp(-t/S)$ in CMOS memory stores.
  3. Wire Graph-of-Thought (GoT) planner into AEAN cognitive loop.
* **Objective Evaluation Criteria:**
  - EFE KL-divergence calibration error $< 0.05$.
  - Context retrieval efficiency improvement $\ge 45\%$ against flat RAG baselines.

### Phase 3: Causal Execution & Risk-Gated Orchestration
* **Target Subsystems:** `apodex/ai_eos/intelligence/`, `apodex/arcs/`
* **Key Deliverables:**
  1. Complete 14-Layer Computational Architecture engine (`fourteen_layer_engine.py`).
  2. Implement Judea Pearl's do-calculus intervention operator $P(Y | do(X))$.
  3. Apply Advanced Fractional Kelly Criterion for multi-venture capital allocation.
* **Objective Evaluation Criteria:**
  - Causal intervention error reduction $\ge 12\%$.
  - Execution time $\le 0.003$s per decision loop.

### Phase 4: Scientific Research OS & Self-Improvement Flywheel
* **Target Subsystems:** `apodex/ai_eos/research/`, `apodex/execution/`
* **Key Deliverables:**
  1. Integrate 300-paper research corpus (`AI_EOS_RESEARCH_DB.yaml` and `ALPHA_ALGO_100_NEW_RESEARCH.yaml`).
  2. Operationalize `ExperimentRecord` with automated Welch's t-test and Holm-Bonferroni correction.
  3. Enable APODEX sandboxed program rewrite and self-repair loops.
* **Objective Evaluation Criteria:**
  - Statistically validated performance gains ($p < 0.05$) required for all system updates.
  - Zero regression on benchmark test suites.

---

## 3. Verification & Gate Criteria Matrix

| Phase Transition | Automated Gate Check Command | Success Threshold | Required Artifact |
| :--- | :--- | :--- | :--- |
| **Phase 1 -> Phase 2** | `PYTHONPATH=.:AgentHarness pytest tests/` | 100% Pass (397/397) | Dependency Audit Report |
| **Phase 2 -> Phase 3** | `PYTHONPATH=.:AgentHarness pytest tests/cognition/ tests/memory/` | 100% Pass | EFE Calibration Log |
| **Phase 3 -> Phase 4** | `PYTHONPATH=.:AgentHarness pytest tests/ai_eos/ tests/arcs/` | 100% Pass | Causal Benchmark Report |
| **Phase 4 -> Production** | `PYTHONPATH=.:AgentHarness pytest tests/` | 100% Pass | Master Verification Evidence |
