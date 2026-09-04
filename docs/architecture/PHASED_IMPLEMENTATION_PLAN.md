# Phased Implementation Plan & Evaluation Criteria

## Overview

The transformation of Research OS, EIOS, EOS, AEAN, and APODEX into a unified cognitive operating system is executed across four distinct phases.

---

## Phase 1: Subsystem Unification & Interface Formalization (Completed / Verification Stage)
* **Scope**: Formalize single-responsibility layer boundaries across Layer 1 (Research OS), Layer 2 (EIOS/EOS), Layer 3 (AEAN), and Layer 4 (APODEX). Eliminate legacy duplicate adapters.
* **Objective Evaluation Criteria**:
  - 0% capability duplication across codebase.
  - 100% test pass rate across unit and integration test suites (`pytest`).
  - Active inference state handoffs validated via end-to-end integration tests.

## Phase 2: Active Inference & Causal Bidding Optimization
* **Scope**: Upgrade `EIOSKernel` and `HiveMind` task bidding with Causal Do-Calculus EFE scoring and Non-Gaussian Hawkes stability constraints.
* **Objective Evaluation Criteria**:
  - Task allocation efficiency improvement > +15%.
  - Budget overestimation error reduction < -10%.
  - Zero unhandled numerical exceptions under edge-case probability inputs.

## Phase 3: WorldModel Autonomous Skill Flywheel Scaling
* **Scope**: Scale pre-populated `SkillRegistry` from 60 to 120 strategic skills and integrate recursive Bayesian belief propagation with APODEX protocol execution.
* **Objective Evaluation Criteria**:
  - Skill execution success rate > 98%.
  - Entity belief convergence time reduced by > 25%.

## Phase 4: Full Multi-Agent Self-Improvement Loop
* **Scope**: Deploy continuous MAP-Elites island search with automated research hypothesis synthesis and real-time active inference feedback.
* **Objective Evaluation Criteria**:
  - Continuous execution without agent stagnation over 100+ task iterations.
  - Measurable capability gain on long-horizon benchmarks.
