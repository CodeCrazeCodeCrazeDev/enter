# Architecture Invariants

This document establishes the authoritative, single-ownership invariants of our Cognitive Operating System. Every production component must align with these invariants to prevent duplicate abstractions, overlapping planners, registries, memory systems, or conflicting execution authorities.

---

## 1. Single Authoritative Subsystem Ownership

To prevent overlapping logic, our architecture enforces a strict **Single Authority** model. The 8 critical authorities are mapped as follows:

| Subsystem Authority | Single Authorized Implementation Component | File / Location | Ownership Contract |
|---|---|---|---|
| **1. Orchestrator** | `HierarchicalOrchestrator` | `agent_harness/core/runtime/orchestration/hierarchical.py` | Single coordinator/worker routing engine. No other agent-mesh routers exist. |
| **2. Planner** | `UnifiedPlanner` / `StrategicPlanner` | `apodex/cognition/planning/unified_planner.py` | Decomposes task DAGs recursively under HTN bounds. No other planners are permitted. |
| **3. Memory Authority**| `SemanticMemory` | `apodex/memory/semantic_memory.py` | Authority over beliefs, verified facts, evidence cards. |
| **4. World Model** | `WorldModel` / `WorldGraph` | `apodex/world_model/world_model.py` | Evolves entity relationships and causal/temporal beliefs. |
| **5. Evaluation Pipeline**| `HarnessValidator` / `TrajectoryDatasetCompiler`| `agent_harness/core/runtime/dataset_generator.py` | Grades execution steps and compile trajectories. |
| **6. Experiment Manager**| `ExperimentRegistry` | `apodex/research_os/registries.py` | Schedules and tracks hypothesis iterations. |
| **7. Artifact Manager**| `ArtifactRegistry` | `apodex/research_os/registries.py` | Stores scientific outputs, code, and documents. |
| **8. Governance Layer** | `GovernanceGateway` / `ConstitutionalFilter` | `agent_harness/core/runtime/verification/parallel` | Enforces policy invariants on active plans. |

---

## 2. Dynamic Structural Decoupling Guidelines

We mandate strict architectural decoupling checked dynamically via standard test-suites:
1. **No Circular Imports**: Subsystems inside `apodex` must not create cyclic dependencies (e.g., `world_model` calling `orchestration` which imports `world_model`).
2. **Clear Port-Adapter Boundaries**: Legacy benchmark runner logic under `agent_harness` must remain strictly as adapters re-exporting canonical production modules under `apodex`. Under no circumstances is production logic duplicated inside `agent_harness`.
3. **Execution Sandbox Isolation**: Code execution mutations must execute strictly inside secure, isolated sandboxes and cannot pollute the host environment.
