# Capability Ownership Matrix
**Canonical Ownership Mapping & Elimination of Legacy Logical Duplication**
**Version:** 4.0.0
**Scope:** Research OS (Layer 1) | EIOS & EOS (Layer 2) | AEAN (Layer 3) | APODEX (Layer 4)

---

## 1. Executive Summary

This document establishes the authoritative **Capability Ownership Matrix** for the Unified Cognitive Operating System.

To eliminate logical duplication, every core cognitive capability—including planners, schedulers, world models, memories, reasoning engines, and safety frameworks—is assigned to exactly one canonical layer owner. Legacy adapter modules and standalone duplicate implementations are explicitly mapped to their canonical home or designated for deprecation.

---

## 2. Capability Ownership Matrix

| Functional Capability | Subsystem Owner | Primary Layer | Canonical Module Location | Status & Elimination Strategy |
| :--- | :--- | :---: | :--- | :--- |
| **500-Paper Corpus Principles** | Research OS | **Layer 1** | `apodex.ai_eos.research.integration` | Authoritative single source for paper principles & literature reviews. |
| **Scientific Hypothesis Engine** | Research OS | **Layer 1** | `apodex.ai_eos.research.research_os` | Generates & validates scientific hypotheses ($DSR$, $p < 0.05$). |
| **Statistical Validation** | Research OS | **Layer 1** | `apodex.research_os.statistical_validation` | Authoritative safe probability clamping & DSR calculation. |
| **Active Inference DAG Scheduler** | EIOS Kernel | **Layer 2** | `apodex.arcs.kernel.kernel` | Consolidated single planner evaluating Expected Free Energy ($G(u)$). |
| **11-Section EOS State Engine** | EOS Engine | **Layer 2** | `apodex.ai_eos.intelligence.eos_engine` | Authoritative entrepreneurial growth state machine & capital allocator. |
| **Opportunity Graph Sensing** | EOS Engine | **Layer 2** | `apodex.ai_eos.intelligence.computational_architecture` | Senses opportunity anomalies & evaluates financial value loops. |
| **Multi-Agent Token Bidding** | AEAN HiveMind | **Layer 3** | `apodex.aean.coordination.hive_mind` | Authoritative market-based agent auction & task allocation engine. |
| **MAP-Elites Workflow Search** | AEAN HiveMind | **Layer 3** | `apodex.ai_eos.research.integration` | Genetic island workflow topology optimizer. |
| **AST Rewrite Verification** | AEAN HiveMind | **Layer 3** | `apodex.ai_eos.research.integration` | Authoritative Hawkes process recursive AST stability checker. |
| **Causal Graph World Model** | WorldModel | **Layer 4** | `apodex.world_model.world_model` | Single authoritative source of truth for reality states ($G=(V,E)$). |
| **Recursive Bayesian Beliefs** | WorldModel | **Layer 4** | `apodex.world_model.domain.beliefs` | Single authoritative belief update engine ($\text{Prior} \to \text{Posterior}$). |
| **Cognitive Brain & CMOS Store** | APODEX Brain | **Layer 4** | `apodex.cognition.brain` | Consolidated long-term memory & episodic state store. |
| **Skills Protocol Runner** | APODEX Skills | **Layer 4** | `apodex.skills.runner` | Executes verified skill protocols with budget enforcement. |
| **Credit & Cost Halter** | Governance | **Layer 4** | `apodex.world_model.governance.approval` | Authoritative budget halting & compliance gatekeeper. |

---

## 3. Legacy Duplication Audit & Deprecation Map

| Legacy Component / Adapter | Historical Location | Duplicated Capability | Canonical Replacement Module | Action Taken |
| :--- | :--- | :--- | :--- | :--- |
| `ActiveInferencePlanner` | `agent_harness.core.runtime.orchestration` | Task DAG Planning | `apodex.arcs.kernel.EIOSKernel` (Layer 2) | Consolidated into Layer 2 kernel. |
| `ActiveLearningEngine` | `agent_harness.core.runtime.reasoning` | Active Learning / Uncertainty | `apodex.arcs.kernel.EIOSKernel` (Layer 2) | Consolidated into Layer 2 kernel. |
| `PlannerExecutor` | `agent_harness.core.runtime.orchestration` | Step Decomposition | `apodex.arcs.kernel.EIOSKernel` (Layer 2) | Consolidated into Layer 2 kernel. |
| Isolated `BeliefState` | `agent_harness.core.memory` | Belief Tracking | `apodex.world_model.domain.beliefs` (Layer 4) | Unified in Layer 4 WorldModel. |
| Standalone `AgentHarness` Memory | `agent_harness.components` | Semantic Memory Store | `apodex.cognition.brain.CognitiveBrain` (Layer 4) | Consolidated into Layer 4 CMOS. |

---

## 4. Operational Principles

1. **Single Canonical Module Rule:** No new cognitive module may be introduced if its core capability belongs to an existing canonical layer owner.
2. **Explicit Layer Crossings:** Cross-layer communication must strictly utilize the exposed interfaces specified in `UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md`.
3. **Automated Audit Scripting:** Structural audits (`verify_architecture_docs.py` and `check_layer_imports.py`) enforce zero circular dependencies and verify documentation integrity.
