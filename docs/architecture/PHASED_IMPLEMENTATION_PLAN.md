# Phased Implementation Plan & Evaluation Criteria

**Version:** 2.0.0
**Status:** Canonical Implementation Plan Standard
**Target:** `docs/architecture/PHASED_IMPLEMENTATION_PLAN.md`

---

## 1. Executive Implementation Strategy

The transition to the **Unified 4-Layer Cognitive Operating System Architecture** is executed across three non-disruptive, backward-compatible phases. Every phase enforces strict gate criteria, objective benchmark evaluations, and isolated verification runtimes.

---

## 2. Phase Breakdown & Capability Ownership Matrix

### Phase 1: Substrate Hardening & Operational Safety
- **Focus:** Infrastructure thread-safety, persistence, and real-time execution bounds.
- **Key Modules Modified / Created:**
  - `apodex/memory/sqlite_repository.py`: Async connection pool with WAL mode (`PRAGMA journal_mode=WAL;`).
  - `AgentHarness/agent_harness/core/memory/`: SQLite-backed persistent trajectory table schema.
  - `apodex/ai_eos/orchestration/backend.py`: Real-time step token & latency interceptor raising `ResourceLimitException`.
- **Capability Ownership Matrix:**
  - **L1 Runtime Owner:** `UnifiedMemoryRepository` (Persistence & WAL queue).
  - **L2 Execution Owner:** `VentureExecutionSystem` (Resource limits & execution bounds).
- **Objective Evaluation Criteria:**
  - Zero SQLite connection locks or write errors across 50 concurrent async writer threads.
  - Complete memory usage stability (zero RAM growth) across 10,000 ReAct trajectory steps.
  - Hard execution halt within 1 step boundary upon reaching maximum token budget.

---

### Phase 2: Active Inference & Grounded Verification
- **Focus:** Physical task verification, Kelly capital allocation, and dynamic memory matching.
- **Key Modules Modified / Created:**
  - `apodex/ai_eos/validation/platform.py`: Local `subprocess` Python sandbox task validator (`SandboxValidator`).
  - `apodex/ai_eos/portfolio/manager.py`: Beta variance-weighted Fractional Kelly Criterion capital sizing.
  - `apodex/memory/semantic_memory.py`: MemoHarness decay-weighted Jaccard overlap context retrieval.
- **Capability Ownership Matrix:**
  - **L1 Runtime Owner:** `SemanticMemory` (MemoHarness Jaccard overlap retrieval).
  - **L2 Orchestration Owner:** `PortfolioManager` (Uncertainty-discounted Kelly allocation).
  - **L4 Research Owner:** `SandboxValidator` (Grounded sub-process task execution).
- **Objective Evaluation Criteria:**
  - 100% of prompt mutations tested against physical sub-process tasks prior to promotion.
  - High-variance (unproven) ventures receive $< 5\%$ exploratory budget allocations under Kelly sizing.
  - ReAct prompt context retrieves top-3 historically relevant failure/success trajectories.

---

### Phase 3: Meta-Evolution & Failure Recovery
- **Focus:** Graph-edit failure recovery, 3D Pareto frontier optimization, and statistical rollout governance.
- **Key Modules Modified / Created:**
  - `AgentHarness/agent_harness/core/memory/emg_engine.py`: NetworkX Experience Memory Graph (EMG) error bypass.
  - `apodex/ai_eos/capability_intelligence/manager.py`: 3D Pareto Frontier Optimizer ($S = w_q Q - w_t T - w_l L$).
  - `apodex/ai_eos/research/experiment_framework.py`: Welch's t-test statistical promotion engine ($p < 0.05$).
- **Capability Ownership Matrix:**
  - **L3 Reasoning Owner:** `NetworkXEMGEngine` (Graph-edit error path bypass).
  - **L3/L4 Meta-Cognition Owner:** `EvolutionEngine` (3D Pareto frontier scoring).
  - **L4 Scientific Owner:** `ExperimentRecord` (Welch's t-test statistical validation).
- **Objective Evaluation Criteria:**
  - Automated single-shot recovery on simulated tool API errors using `REPLACE_STEP` graph edits.
  - Rejection of prompt modifications that improve accuracy by $< 2\%$ while increasing token cost by $> 20\%$.
  - 100% test pass rate across all 397 repository unit and integration tests.

---

## 3. Milestone Verification Gates

```
+------------------------------------+
| PHASE 1: SUBSTRATE HARDENING       |
| Gate: Concurrent WAL & Hard Halt   |
+-----------------+------------------+
                  |
                  v
+------------------------------------+
| PHASE 2: GROUNDED VERIFICATION     |
| Gate: Sub-process Task Verification|
+-----------------+------------------+
                  |
                  v
+------------------------------------+
| PHASE 3: META-EVOLUTION & RECOVERY |
| Gate: Welch's t-test & EMG Bypass  |
+------------------------------------+
```
