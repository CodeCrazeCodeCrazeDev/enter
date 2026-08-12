# Executable Capability-Ownership Matrix
## The Single Source of Truth for Cognitive Operating System Capabilities

To enforce architectural cleanliness and eliminate split-brain duplication, this matrix defines the authoritative canonical owner for every core system capability. Any component wishing to consume a capability must use the designated public interface of its canonical owner.

---

## 1. Subsystem Capability Matrix

| Capability | Canonical Owner | Public Interface | Consumers | Duplicate Implementations (Resolved) | Migration Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Planners** | `apodex/planning/planner_executor.py` | `StrategicPlanner`, `StrategicRoadmap`, `RoadmapStep` | `tests/planner/test_planner.py`, `agent_harness/core/runtime/orchestration/planner_executor.py` | Redundant mock class defined in `agent_harness` adapter has been fully replaced with zero-logic forwards. | **Completed** |
| **Memories** | `apodex/memory/semantic_memory.py` | `SemanticMemory`, `SQLiteMemoryRepository`, `EvidenceCard`, `Fact`, `Belief` | `tests/memory/test_semantic_memory.py`, `agent_harness/core/memory/semantic_memory.py` | Legacy `agent_harness` memories consolidated to direct thin imports. | **Completed** |
| **World Models** | `apodex/world_model/world_model.py` | `WorldModel`, `CausalNode`, `RelationEdge` | `tests/world_model/test_world_model.py` | Unified under `apodex/world_model/world_model.py`. No other active world model exists. | **Completed** |
| **Agent Registries** | `apodex/skills/registry.py` | `SkillRegistry`, `skill_registry` (Singleton) | `tests/world_model/test_skills_flywheel.py` | Registries in `agent_harness` or other local paths consolidated to this single source. | **Completed** |
| **Schedulers** | `apodex/world_model/orchestration/scheduler.py` | `Scheduler`, `IWorldModelScheduler` | `tests/world_model/test_wmc_architecture.py` | Isolated from the main task orchestration loops; owns graph tick timers. | **Completed** |
| **Evaluators** | `apodex/evolution/verifier/judge.py` | `LLMAsAJudgeNode` | `tests/cognition/test_trajectory_verification.py` | Legacy validator files merged into the `apodex/evolution` verifier pipeline. | **Completed** |
| **Research Engines** | `apodex/research_os/pipeline.py` | `ResearchPipeline` | `tests/research_os/test_research_os.py` | Dual pipeline definitions inside older prototype branches have been entirely archived. | **Completed** |
| **Orchestration** | `apodex/orchestration/hierarchical.py` | `HierarchicalOrchestrator`, `CoordinatorAgent`, `WorkerAgent` | `tests/orchestration/test_hierarchical.py` | Core orchestration logic fully migrated from legacy `agent_harness` paths. | **Completed** |
| **Execution Engines** | `apodex/execution/interfaces.py` | `IExecutionEngine` | `tests/verification/test_verification.py` | The base execution context is managed via the canonical `APODEX` execution layer. | **Completed** |
| **Self-Improvement** | `apodex/evolution/self_harness/refiner.py` | `HarnessRefiner` | `tests/evolution/test_emg_memoharness.py` | Prompts are modified strictly under `refiner.py` and saved to `EvolutionChangelog`. | **Completed** |
| **Simulation** | `apodex/world_model/domain/simulation.py` | `Simulation` | `tests/world_model/test_wmc_architecture.py` | All Monte Carlo client simulations route through `domain/simulation.py`. | **Completed** |
| **Governance** | `apodex/world_model/governance/approval.py` | `ApprovalTable` | `tests/world_model/test_wmc_architecture.py` | Non-bypassable safety gates are owned by `apodex/world_model/governance`. | **Completed** |

---

## 2. Boundary Verification & Resolution rules

1.  **Strict Singularity of Planners**: There must never be multiple overlapping planner implementations. The `StrategicPlanner` under `apodex/planning/planner_executor.py` is the single source of truth.
2.  **Stateless Adapters**: The folder `./agent_harness/` is reserved strictly as a backward-compatibility layer. No cognitive decisions, parsing logic, or metric tracking can occur there.
3.  **Cross-Layer Dependency Rule**: Subsystems must import directly from their canonical paths. If duplicate classes with identical names appear (such as `EventBus` or `GovernanceGateway`), they must be namespaces or consolidated. (e.g. `apodex.research_os.events.EventBus` vs `apodex.ai_eos.infrastructure.event_bus.EventBus`).
