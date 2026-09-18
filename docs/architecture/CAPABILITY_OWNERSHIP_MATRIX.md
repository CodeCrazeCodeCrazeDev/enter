# Capability Ownership Matrix: Unified Cognitive Operating System

## 1. Primary Component Canonical Ownership

To enforce strict non-duplication across the 4-layer architecture, every core cognitive capability is assigned a single canonical owner layer and primary Python module path.

| Cognitive Capability Domain | Canonical Layer Owner | Primary Module Implementation | Direct Interface Consumers | Legacy / Submodule Stubs Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Research Ingestion & DSR Validation** | **Layer 1: Research OS** | `apodex.research_os.statistical_validation` & `apodex.ai_eos.research.research_os` | EIOS Kernel, EOS Engine, HiveMind | Lightweight compatibility adapter in `agent_harness` |
| **AST Hawkes Stability & Safe Code Rewrite** | **Layer 1: Research OS** | `apodex.ai_eos.research.integration.CodeRewriteEngine` | AEAN Swarms, System Evolver | Re-exported via `apodex.ai_eos.research` |
| **Active Inference EFE Sensing & Opportunity DAGs** | **Layer 2: EIOS / EOS** | `apodex.arcs.kernel.kernel.EIOSKernel` & `apodex.ai_eos.intelligence.computational_architecture` | EOS Engine, AEAN HiveMind | Canonical active inference implementation |
| **14-Layer Entrepreneurial Intelligence** | **Layer 2: EIOS / EOS** | `apodex.ai_eos.intelligence.fourteen_layer_engine` | EOS State Machine, ARCS Executive Agents | Re-exported in `apodex.ai_eos.intelligence` |
| **Multi-Agent Token Bidding & Coordination** | **Layer 3: AEAN** | `apodex.aean.coordination.hive_mind.HiveMind` | Executive Agents, Active Inference Planner | Adapter wrapper in `agent_harness.core.runtime` |
| **Genetic Workflow MAP-Elites Optimization** | **Layer 3: AEAN** | `apodex.aean.optimization.GeneticWorkflowOptimizer` | Workflow Orchestrator, SFT Preference Collector | Native AEAN component |
| **Causal Graph World Model & Bayesian Beliefs** | **Layer 4: APODEX Platform** | `apodex.world_model.world_model.WorldModel` & `apodex.world_model.domain` | Cognitive Brain, EIOS Sensor, AEAN Swarm | Adapter wrapper in `agent_harness.core.world_model` |
| **Skill Execution & Protocol Budgeting** | **Layer 4: APODEX Platform** | `apodex.skills.runner.ProtocolRunner` & `apodex.skills.implementation` | Cognitive Brain, Executive Agents | Native APODEX Skills Engine |

---

## 2. Enforcement Rules

1. **No Parallel Implementations**: Components outside the canonical owner module must import or delegate to the canonical implementation rather than reimplementing business logic.
2. **Adapter Boundary**: Submodule adapters (such as legacy `agent_harness` modules) must act solely as thin, stateless wrappers mapping old interface signatures to canonical `apodex` domain calls.
