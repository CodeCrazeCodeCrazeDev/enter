# Capability Ownership Matrix
## Canonical Single-Source-of-Truth Module Allocations (v3.0.0)

This matrix enforces strict single ownership for all major cognitive, planning, memory, and governance capabilities across the Unified Cognitive OS, eliminating duplicate implementations and technical debt.

---

## 1. Single Ownership Allocation

| Capability / Domain | Canonical Owner Component | File Path / Package Location | Responsibility Description |
| :--- | :--- | :--- | :--- |
| **Recursive Planning** | `UnifiedPlanner` / `RecursivePlanner` | `apodex/planning/planner_executor.py` | Handles multi-timescale goal-conditioned hierarchical task decomposition, Tree of Thoughts tree searches, and checkpoint recovery. |
| **Persistent Memory** | `SemanticMemory` | `apodex/memory/semantic_memory.py` | Handles SQL-backed persistent storage and Jaccard-overlap keyword query retrieval for Evidence, Beliefs, Facts, and Questions. |
| **Epistemic Substrate**| `KnowledgeInfrastructure` | `apodex/ai_eos/memory/knowledge_infrastructure.py`| Maintains non-private joint belief states, executes Bayesian belief propagation updates, and performs theory promotion. |
| **Market World Model** | `WorldGraph` | `apodex/arcs/world_graph.py` | Tracks external entities, macro signals, user cohorts, competitor metrics, and causal relationships. |
| **Active Inference** | `ActiveInferenceEngine` | `apodex/arcs/causal/active_inference.py` | Performs Expected Free Energy minimization and selects uncertainty-reducing actions. |
| **Venture Execution**  | `VentureExecutionSystem` | `apodex/arcs/workflows/subsystems.py` | Handles day-to-day multi-agent sales, marketing, and GTM execution. |
| **Research OS Compiler**| `ResearchCompiler` | `apodex/ai_eos/research/compiler.py` | Translates raw academic literature and patents into normalized, deduplicated Evidence nodes. |
| **Self-Improvement** | `SelfImprovementEngine` / `EMGEngine` | `apodex/aean/core.py` & `apodex/memory/emg_engine.py` | Logs execution traces to Action-Decision Graphs, extracts workflow patterns, and proposes prompt edits. |
| **Constitutional Gates**| `ConstitutionalFilter` | `apodex/aean/governance.py` | Monitors and throttles capital allocation, content policies, and system-wide security limits. |
| **Substrate Engine** | `Organism` / `EIOSKernel` | `apodex/aean/flywheel.py` & `apodex/arcs/kernel/kernel.py` | Runs the master async schedule, schedules DAG nodes, and manages subprocess isolation. |

---

## 2. Consolidation & Anti-Duplication Strategy

### 2.1 The "One System, One Owner" Principle
*   **Planning Consolidation**: Flat ReAct conversation popping and linear index popping (found in legacy observers) are deprecated. All long-horizon task decompositions are compiled to structured DAGs and handled by the canonical `StrategicPlanner` and `TaskExecutor`.
*   **Memory Consolidation**: All vector or relational memory stores are consolidated to use SQLite-backed `SemanticMemory` (L1) and `KnowledgeInfrastructure` (L2/KOS). No agent may hold private, non-graphed, or non-versioned belief states.
*   **Validation & Rollback Consolidation**: Overlapping SLA and performance metrics checks are unified under the `RollbackManager` leveraging extensible `RollbackPolicy` protocols, avoiding split-brain verification logic.

### 2.2 Invariant Verification Tests
We enforce automated capability ownership via a dedicated test suite (`tests/governance/test_capability_ownership.py`). This test executes AST (Abstract Syntax Tree) checks to guarantee that no duplicate implementations of Tier-0 components exist inside legacy or experimental paths, failing immediately if multiple conflicting implementations try to execute.
