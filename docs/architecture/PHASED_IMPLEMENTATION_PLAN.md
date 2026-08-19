# Phased Implementation Plan & Migration Strategy
**Author:** Jules, Lead Architect & Software Engineer
**Status:** Canonical Approved Standard
**Version:** 2.0.0
**Target Architecture:** Research OS / AEAN / EIOS & EOS / APODEX

---

## Executive Summary

This document outlines the phased migration roadmap for transitioning legacy agent modules into the unified 4-layer Cognitive Operating System. To guarantee continuous operational stability and zero test regressions, migration follows a strict **"Implement -> Verify -> Promote -> Refactor"** pipeline.

---

## 1. Migration Phase Overview

```
+-----------------------------------------------------------------------------------+
| PHASE 1: SUBSTRATE HARDENING & CORE RELIABILITY                                   |
| - Async SQLite WAL thread-pooling, single-writer queues, persistent trajectories   |
| - Status: COMPLETED | Verification: 100% pass on memory & concurrency tests        |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| PHASE 2: DE-DUPLICATION & LAYER ALIGNMENT                                         |
| - Eliminate duplicate SCM/causal engines, consolidate 60 skills in Layer 4        |
| - Integrate Active Inference EFE in Layer 2 & Kelly Allocation in Layer 3         |
| - Status: COMPLETED | Verification: 100% pass across skills flywheel & integration  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| PHASE 3: PHYSICAL SANDBOX EXECUTOR & GRAPH ERROR RECOVERY                         |
| - Sub-process virtual sandbox executor for prompt/code proposals                  |
| - NetworkX EMG failure path matching for one-shot error bypass                    |
| - Status: IN PROGRESS | Target Completion: Phase 3 Release                          |
+-----------------------------------------------------------------------------------+
```

---

## 2. Objective Evaluation Criteria & Success Metrics

Every migration phase must satisfy objective, non-negotiable success gates before promotion to production:

| Migration Milestone | Objective Success Metric | Minimum Passing Threshold | Evaluation Test Suite |
| :--- | :--- | :--- | :--- |
| **Phase 1: Memory & Concurrency** | Zero database locks under 50 concurrent async writers; flat RSS memory | 0 lock errors, RSS delta < 50MB per 1k loops | `tests/memory/test_cmos_infrastructure.py` |
| **Phase 2: Active Inference & SCM** | EFE calibration accuracy; reduction in capital allocation overestimation | EFE accuracy > +30%, alloc error < -10% | `tests/arcs/test_arcs_core.py`, `test_capital_allocation.py` |
| **Phase 2: Skills & Integration** | Execution pass rate across all 60 registered skills; end-to-end multi-layer cycle | 100% skill execution pass rate | `tests/world_model/test_skills_flywheel.py`, `test_cognitive_os_subsystems.py` |
| **Phase 3: Sub-process Sandbox** | Physical test execution of evolved prompt candidates before promotion | 100% sandboxed verification pass rate | `tests/evolution/test_self_harness.py` |

---

## 3. Failure Modes & Rollback Strategies

1. **Database Lock Exception / Lock Timeout:**
   - *Failure Trigger:* Concurrent SQLite writes exceed the async queue timeout.
   - *Automated Safeguard:* Single-threaded write queue automatically buffers pending transactions; if queue depth > 1,000, execution falls back to WAL synchronous checkpointing.
2. **Evolved Prompt Regression:**
   - *Failure Trigger:* An evolved agent prompt degrades performance on edge-case tasks.
   - *Automated Safeguard:* Immutable `EvolutionChangelog` maintains SHA256 hashes of all past prompt states. Failed benchmarks trigger instant automatic rollback to the last verified prompt version.
3. **Execution Latency Breach:**
   - *Failure Trigger:* Active inference MCTS search depth exceeds SLA latency threshold (> 500ms).
   - *Automated Safeguard:* MCTS engine dynamically downshifts search depth from $d=5$ to $d=2$ when latency budget is 80% consumed.
