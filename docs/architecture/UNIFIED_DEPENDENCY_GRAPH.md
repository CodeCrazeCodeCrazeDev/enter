# Strategic Dependency Graph & Interaction Specification

**Version:** 2.0.0
**Status:** Canonical Strategic Dependency Standard
**Target:** `docs/architecture/UNIFIED_DEPENDENCY_GRAPH.md`

---

## 1. Top-Down Unidirectional Architecture Topology

The Unified Cognitive Operating System enforces strict **unidirectional dependency layers**. Higher-level cognitive abstractions consume lower-level execution and persistence runtimes. Lower layers never import or directly reference higher-level orchestrators, eliminating circular dependencies.

```
+---------------------------------------------------------------------------------------------------+
| LAYER 4: RESEARCH OS (Scientific Research & Truth Engine)                                          |
| Subsystems: ResearchIngestionPipeline, LiteratureDatabase, WalkForwardValidator, HypothesisEngine  |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  | Ingests Verified Evidence & Hypotheses
                                                  v
+---------------------------------------------------------------------------------------------------+
| LAYER 3: AEAN (Cognitive Intelligence & Reasoning Engine)                                         |
| Subsystems: ActiveInferenceEngine, SCMEngine, SwarmDebateCoordinator, GraphOfThoughtPlanner       |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  | Dispatches Evaluated Causal Policies
                                                  v
+---------------------------------------------------------------------------------------------------+
| LAYER 2: EIOS / EOS (Venture Execution & Governance Engine)                                      |
| Subsystems: VentureExecutionSystem, KellyPortfolioManager, RiskManager, GovernanceGateway         |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  | Directs Bounded Tool Jobs & Capital
                                                  v
+---------------------------------------------------------------------------------------------------+
| LAYER 1: APODEX (Decision, Memory & World Model Runtime Engine)                                   |
| Subsystems: UnifiedMemoryRepository, EKTUWorldModelGraph, SkillRegistry, SandboxToolExecutor      |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Cross-Layer Interaction Matrix

| Source Layer | Target Layer | Call Protocol | Inter-System Contract Payload | Failure Mode & Recovery Fallback |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 4 (Research OS)** | **Layer 3 (AEAN)** | Async Push / Event Bus | `EvidenceNode` (Paper ID, Principle, $p$-value, Confidence) | Fall back to default wide priors ($\text{Beta}(1, 1)$) if research corpus query returns null. |
| **Layer 3 (AEAN)** | **Layer 2 (EOS)** | Async Request / Response | `CausalInterventionRequest` ($do(A)$, Expected Utility, Token Limit) | Fall back to heuristic rule-based planner if active inference optimization fails to converge. |
| **Layer 2 (EOS)** | **Layer 1 (APODEX)** | Synchronous / Async Task | `ExecutionDirective` (Skill ID, Parameters, Timeout, Budget) | Trigger step-level `ResourceLimitException` and halt execution if budget is exceeded. |
| **Layer 1 (APODEX)** | **Layer 2 (EOS)** | Event Callback | `TrajectoryStepRecord` (Output, Latency, Token Count, Status) | Write failure state to SQLite trajectory table and escalate to Layer 2 Governance. |

---

## 3. Communication Protocols & Data Invariant Rules

### Rule 1: No Upward Direct Imports
Layer 1 (`apodex/memory/`, `apodex/world_model/`) MUST NOT import modules from Layer 2 (`apodex/ai_eos/`), Layer 3 (`apodex/aean/`), or Layer 4 (`apodex/research_os/`). Violations are flagged automatically during CI via dependency static analysis (`scripts/validate_dependencies.py`).

### Rule 2: Pydantic Boundaries
All inter-layer communication must pass validated Pydantic models. Raw dictionaries or un-typed tuples across layer boundaries are strictly prohibited.

### Rule 3: Single-Threaded Write Queue for SQLite Memory
To avoid database lock contention under multi-agent execution, all memory write events dispatches from Layer 2/3 to Layer 1 pass through an asynchronous single-threaded event queue (`AsyncWriteQueue`) in WAL mode (`PRAGMA journal_mode=WAL;`).

---

## 4. Subsystem Dependency Rules & Import Paths

```
apodex/
  ├── research_os/              # Layer 4: Depends on common/ models only
  ├── aean/                     # Layer 3: Depends on research_os/ (L4), common/
  ├── ai_eos/                   # Layer 2: Depends on aean/ (L3), research_os/ (L4), common/
  └── memory/, world_model/     # Layer 1: Base runtime. Zero dependencies on higher layers.
```
