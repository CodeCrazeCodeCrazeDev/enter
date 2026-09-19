# Capability Ownership Matrix Across 4-Layer Cognitive Operating System
**Version:** 2026.1.0
**Status:** Authoritative Specification
**Scope:** Canonical Owner Mapping for Planners, Memory, World Model, Schedulers & Engines

---

## 1. Executive Summary

To eliminate logical duplication and prevent overlapping responsibilities across legacy adapter layers, this matrix specifies the single canonical module owner for every core system capability within the unified 4-layer taxonomy.

```
+-----------------------------------------------------------------------------------+
|                        CANONICAL CAPABILITY MAPPING SUMMARY                       |
|                                                                                   |
|  - Planning & Scheduling  --> Layer 2 (EIOS/EOS) & Layer 3 (AEAN GoT)            |
|  - World Model & Reality   --> Layer 4 (APODEX WorldModel Engine)                 |
|  - Swarm Multi-Agent       --> Layer 3 (AEAN HiveMind Coordinator)                |
|  - Memory Systems          --> Layer 3 (AEAN Working/Episodic/Semantic Memory)    |
|  - Research & Verification --> Layer 1 (Research OS & StatisticalValidator)       |
|  - Tool & Skill Execution  --> Layer 4 (APODEX SkillsFlywheel Engine)             |
+-----------------------------------------------------------------------------------+
```

---

## 2. Comprehensive Capability Ownership Matrix

| Capability Category | Canonical Capability Name | Layer | Canonical Module Location | Obsoleted / Replaced Adapter Module |
| :--- | :--- | :--- | :--- | :--- |
| **Research & Literature** | Literature Review & Corpus Query | Layer 1 | `apodex.ai_eos.research.research_os.ResearchOS` | Legacy static paper dictionaries |
| **Research & Literature** | Statistical Validation & DSR | Layer 1 | `apodex.research_os.statistical_validation.StatisticalValidator` | Mock statistical scripts |
| **Research & Literature** | AST Code Mutation Verification | Layer 1 | `apodex.ai_eos.research.integration.CodeRewriteEngine` | Unsafe string replacements |
| **Execution & Orchestration**| Active Inference Sensing & EFE | Layer 2 | `apodex.arcs.kernel.kernel.EIOSKernel` | Legacy heuristic opportunity metrics |
| **Execution & Orchestration**| 14-Layer Entrepreneurial Engine| Layer 2 | `apodex.ai_eos.intelligence.fourteen_layer_engine` | Fragmented strategy classes |
| **Execution & Orchestration**| 11-Section EOS Engine State | Layer 2 | `apodex.ai_eos.intelligence.eos_engine.EOSEngine` | Static decision trees |
| **Execution & Orchestration**| Cross-Layer Active Inference Bridge| Layer 2 | `apodex.ai_eos.research.integration.ResearchToSystemBridge` | Isolated event handlers |
| **Cognitive Intelligence** | Swarm Token Bidding & Auction | Layer 3 | `apodex.aean.coordination.hive_mind.HiveMind` | Static worker role assigners |
| **Cognitive Intelligence** | Graph-of-Thought Decomposition | Layer 3 | `agent_harness.core.runtime.orchestration.planner_executor` | Hardcoded step lists |
| **Cognitive Intelligence** | Uncertainty & Active Learning | Layer 3 | `agent_harness.core.runtime.reasoning.active_learning` | Constant confidence stubs |
| **Cognitive Intelligence** | Learnable Task Routing Gate | Layer 3 | `agent_harness.core.runtime.orchestration.parallel` | Round-robin dispatchers |
| **Memory Systems** | Episodic Action-Decision Graph | Layer 3 | `agent_harness.core.memory.emg_engine.EMGEngine` | Unindexed task logs |
| **Memory Systems** | Long-Term Semantic Memory | Layer 3 | `agent_harness.core.memory.learning_memory.LongTermLearningMemory` | Flat text files |
| **World Model & Decision** | Causal World Graph Engine | Layer 4 | `apodex.world_model.domain.entities.WorldEntity` / `relationships` | Disconnected state stores |
| **World Model & Decision** | Recursive Bayesian Belief Engine| Layer 4 | `apodex.world_model.domain.beliefs.BayesianBeliefEngine` | Static probability tables |
| **World Model & Decision** | Skills Flywheel & Protocol Runner| Layer 4 | `apodex.skills.runner.SkillsRunner` | Bare tool execution scripts |
| **World Model & Decision** | Safety, Governance & Approval | Layer 4 | `apodex.world_model.governance.approval.ApprovalEngine` | Manual approval prompts |

---

## 3. Governance Rules for Capability Modifications

1. **Single Source of Truth:** No new feature or module may be added if its core capability belongs to an existing canonical owner listed in this matrix.
2. **Deprecation Policy:** Any legacy module attempting to duplicate canonical functionality must act as a transparent wrapper re-exporting from the canonical location or be deprecated immediately.
3. **Audit Enforcers:** The test suite enforces canonical module importability and verifies that legacy adapter paths redirect cleanly to standard layer modules.
