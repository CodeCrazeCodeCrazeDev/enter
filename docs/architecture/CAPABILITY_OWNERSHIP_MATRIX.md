# Capability Ownership Matrix

## Overview

To eliminate architectural overlap and capability duplication across Research OS, EIOS, EOS, AEAN, and APODEX, this matrix establishes the canonical owning module for every core cognitive capability within the `apodex/` package hierarchy.

---

## Canonical Ownership Matrix

| Cognitive Capability | Canonical Owner Module | Layer | Deprecated / Replaced Legacy Component | Interface / Primary Class |
|---|---|---|---|---|
| **Scientific Hypothesis Validation** | `apodex.research_os.hypothesis` & `apodex.ai_eos.research.integration` | **Layer 1** | Duplicate standalone scripts | `ResearchOS`, `ResearchToSystemBridge` |
| **Active Inference EFE Sensing** | `apodex.arcs.kernel.kernel` | **Layer 2** | Mock sensing adapters | `EIOSKernel.sense_opportunity_anomalies()` |
| **Process DAG Compilation & Scheduling** | `apodex.arcs.kernel.dag_compiler` | **Layer 2** | Hardcoded step lists | `ProcessDAGCompiler` |
| **Entrepreneurial Operating Engine** | `apodex.ai_eos.intelligence.eos_first_principles` | **Layer 2** | Hardcoded business rules | `FirstPrinciplesEOSEngine`, `FourteenLayerEntrepreneurialEngine` |
| **Multi-Agent Task Bidding & Auction** | `apodex.aean.coordination.hive_mind` | **Layer 3** | Static round-robin dispatcher | `HiveMind.submit_task()` |
| **Meta-Reasoning & Loop Intervention** | `apodex.cognition.brain` & `agent_harness.components.observers` | **Layer 3** | Hardcoded turn counters | `MetaReasonerObserver` |
| **AST Code Mutation & Rewrites** | `apodex.ai_eos.research.integration` | **Layer 3** | Regex string replacements | `CodeRewriteEngine.verify_proposal_ast()` |
| **Causal Graph & World Modeling** | `apodex.world_model.world_model` | **Layer 4** | Mock graph dictionaries | `WorldModel`, `CausalNode`, `RelationEdge` |
| **Recursive Bayesian Belief Updating** | `apodex.world_model.domain.beliefs` | **Layer 4** | Fixed probability constants | `RecursiveBayesianBelief` |
| **Unified Memory System (CMOS)** | `apodex.memory.cmos` | **Layer 4** | Isolated vector stores | `CMOSMemory` |
| **Protocol Execution & Budget Downshifting**| `apodex.skills.runner` | **Layer 4** | Hardcoded budget timeouts | `SkillsRunner` |
| **Cost Tier & Multi-Sig Safety Governance**| `apodex.world_model.governance` & `apodex.safety` | **Layer 4** | Ad-hoc threshold checks | `ApprovalWorkflowManager`, `CostTierEnforcer` |

---

## Architectural Rules

1. **No Duplicate Classes**: Logical capabilities listed above MUST NOT be reimplemented in secondary adapters or mock packages.
2. **Canonical Imports**: All components requiring a capability must import directly from the Canonical Owner Module.
3. **Layer Unidirectionality**: High-level orchestrators (Layers 1-3) depend on Layer 4 substrate, but Layer 4 substrate MUST NEVER import higher-level business orchestrators.
