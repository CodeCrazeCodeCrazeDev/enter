# Executable Capability Ownership Matrix
## Single Canonical Ownership and Duplication Elimination Blueprint

---

## 1. Executive Summary

To eliminate logical duplication and boundary overlap across **Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX**, this matrix maps every cognitive capability to a **single canonical python module owner** in the `apodex/` package hierarchy.

---

## 2. Canonical Capability Mapping Matrix

| Capability Category | Cognitive Function | Canonical Python Module Owner | Primary Class / Component | Deprecated Duplicate Locations (Eliminated/Refactored) |
|---|---|---|---|---|
| **Research & Discovery** | Academic Paper Parsing & Ingestion | `apodex.research_os.ingestion` | `ResearchIngestionPipeline` | Duplicate scripts in root |
| **Research & Discovery** | Statistical Hypothesis Testing | `apodex.research_os.statistical_validation` | `StatisticalValidator` | Hardcoded p-value checks |
| **Research & Discovery** | Code AST Self-Rewrite | `apodex.ai_eos.research.integration` | `CodeRewriteEngine` | Unrestricted eval/exec calls |
| **Execution & Orchestration**| Active Inference DAG Compiler | `apodex.arcs.kernel` | `EIOSKernel` | Generic DAG runners |
| **Execution & Orchestration**| 14-Layer Entrepreneurial Engine | `apodex.ai_eos.intelligence` | `FourteenLayerEntrepreneurialEngine` | Dispersed business logic |
| **Execution & Orchestration**| Capital & Resource Allocation | `apodex.arcs.capital` | `CapitalAllocationEngine` | Mock financial calculators |
| **Cognitive Intelligence** | Multi-Agent Token Bidding | `apodex.aean.coordination.hive_mind` | `HiveMind` | Static message broadcasts |
| **Cognitive Intelligence** | Budget-Bounded Task Routing | `apodex.ai_eos.research.integration` | `LearnableRoutingGateDispatcher` | Random agent dispatchers |
| **Cognitive Intelligence** | Genetic Workflow Optimization | `apodex.ai_eos.research.integration` | `GeneticWorkflowOptimizer` | Manual prompt tweaking |
| **Decision & Platform** | Persistent Multi-Graph State | `apodex.world_model` | `WorldModel` | Disjointed dictionary stores |
| **Decision & Platform** | Multi-Tier Memory Consolidation | `apodex.memory.cmos` | `CMOSMemory` | Temporary local buffers |
| **Decision & Platform** | Safety & AST Static Linting | `apodex.safety` / `apodex.ai_eos.research.integration` | `CodeRewriteEngine` | Unsafe dynamic code evaluation |
| **Cross-Layer Integration** | Multi-Layer Active Inference State Bridge | `apodex.ai_eos.research.integration` | `ResearchToSystemBridge` | Fragmented manual state transfers |

---

## 3. Structural Rules for Maintaining Clean Boundaries

1. **No Parallel Memory Implementations**: All persistent state and episodic memory queries must resolve through `apodex.memory.cmos` or `apodex.world_model`.
2. **No Duplicated Planners**: High-level active inference task decomposition belongs exclusively to Layer 2 (`EIOSKernel` / `ActiveInferencePlanner`).
3. **Canonical Imports**: System components must import canonical components directly from their owner modules rather than creating re-implementations.
