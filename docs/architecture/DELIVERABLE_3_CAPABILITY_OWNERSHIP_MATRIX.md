# Deliverable 3 — Capability Ownership Matrix

The following matrix identifies the current, canonical, and target owners for every major functional capability across the five subsystems.

| Functional Capability | Current Owner(s) | Canonical Owner | Duplicate Implementations | Consumers | Dependencies | State Owner | Evaluation Owner | Target Architecture |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Perception** | `world_model.py`, `EIOSKernel` | `apodex/world_model/world_model.py` | None | Active Inference | Event Bus | SQL DB | Validation Platform | Unified Perception Layer |
| **Research** | `research_os.py`, `ResearchLoop` | `apodex/research_os/` | Yes (split-brain) | EIOS | YAML DB | Registry | Benchmarks | Unified Research OS |
| **Knowledge Acquisition** | `knowledge_infrastructure.py` | `apodex/ai_eos/memory/knowledge_infrastructure.py` | None | Research OS | Semantic Memory | SQL DB | Grounded Fact-Checkers | CMOS Knowledge Tier |
| **Memory** | `unified_memory.py`, CMOS | `apodex/memory/unified_memory.py` | None | Cognitive System | SQL DB | Repo | CMOS Verification | CMOS Memory Operating System |
| **Reasoning** | `reasoning/` | `apodex/reasoning/` | None | Planner | World Model | transient | Judge | Unified Graph-of-Thought |
| **Planning** | `unified_planner.py`, `StrategicPlanner` | `apodex/planning/unified_planner.py` | Yes | EIOS, EOS | World Graph | transient | Verifier | Unified Planner Substrate |
| **Scheduling** | `scheduler.py` | `apodex/world_model/orchestration/scheduler.py` | None | EIOS Kernel | DAG | stateful | Monitor | Unified Process Scheduler |
| **World Modeling** | `world_model.py`, `world_graph.py` | `apodex/world_model/world_model.py` | None | Planner, Reasoning | Graph Nodes | stateful | Self-Correction | Continuous World Model (E-K-C-T-U) |
| **Simulation** | `simulation.py` | `apodex/world_model/domain/simulation.py` | None | EIOS Kernel | Models | transient | Critic | Unified Market Simulator |
| **Decision Making** | `controller.py`, `EIOSKernel` | `apodex/cognition/controller.py` | None | Global Host | Central Modules | stateful | Benchmarks | Single Brain central controller |
| **Multi-Agent Coordination** | `hive_mind.py`, `hierarchical.py` | `apodex/orchestration/hierarchical.py` | None | AEAN | Communications | stateful | Audit | Hierarchical Orchestrator |
| **Tool Orchestration** | `runner.py` (`SkillRunner`) | `apodex/skills/runner.py` | None | EIOS Kernel | Executors | transient | Judge | Unified Skill Flywheel |
| **Execution** | `runner.py`, `TaskExecutor` | `apodex/skills/runner.py` | None | EIOS Kernel | Tools | stateful | Verifier | Unified Execution Plane |
| **Evaluation** | `controller.py` (`CognitiveBenchmarkSuite`) | `apodex/cognition/controller.py` | None | Global Host | Judges | stateful | Verifier | Cognitive Benchmark Suite |
| **Learning** | `learning.py` | `apodex/cognition/learning/learning.py` | None | Controller | Lessons | SQL DB | Verifier | Cognitive SFT Curation |
| **Self-Improvement** | `self_improvement_coordinator.py` | `apodex/world_model/orchestration/self_improvement_coordinator.py` | None | World Model | Proposals | SQL DB | Critic | Staged Self-Improvement Flywheel |
| **Software Engineering** | `integration.py` (`self_referential_code_rewrite`) | `apodex/ai_eos/research/integration.py` | None | Research OS | AST parsers | transient | Compiler | Autonomous Program Synthesis |
| **Governance** | `policy.py`, `approval.py`, `governance.py` | `apodex/world_model/governance/` | Yes | EIOS Kernel | Checklists | SQL DB | Gateway | Immutable Governance Layer |
| **Observability** | `rollout.py` (`EvolutionObservabilityMonitor`) | `apodex/evolution/production/rollout.py` | None | Host | Logs | SQL DB | SLA checks | Continuous Observability Monitor |
