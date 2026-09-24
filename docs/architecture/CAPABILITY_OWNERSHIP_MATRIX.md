# Capability Ownership Matrix

## Executive Summary

This matrix establishes single-canonical owners for all core cognitive, execution, memory, world modeling, and scheduling capabilities across the unified operating system. Every capability is assigned to exactly one subsystem layer to eliminate logical duplication, reduce maintenance overhead, and guarantee clear interface boundaries.

---

## Canonical Capability Allocations

| Capability Module | Canonical Owner File Path | Layer Assignment | Responsibility & Boundaries |
| :--- | :--- | :--- | :--- |
| **Literature Review & Scientific Mining** | `apodex/ai_eos/research/research_os.py` | **Layer 1 (Research OS)** | Mining, indexing, and multi-field literature querying across research paper corpora (Papers 1–600). |
| **Hypothesis Generation & Statistical Validation** | `apodex/research_os/statistical_validation.py` | **Layer 1 (Research OS)** | Generating scientific hypotheses, probability clamping, CDF/DSR statistical calculations, and empirical reproducibility tracking. |
| **Active Inference & EFE Sensing** | `apodex/arcs/kernel/kernel.py` | **Layer 2 (EIOS Kernel)** | Computing Expected Free Energy (EFE), sensing market/research anomalies, and driving active inference state transitions. |
| **DAG Workflow Synthesis & Orchestration** | `apodex/arcs/kernel/kernel.py` | **Layer 2 (EIOS Kernel)** | Compiling active inference directives into executable Directed Acyclic Graphs (DAGs) and tracking execution nodes. |
| **Entrepreneurial State & Growth Engine** | `apodex/ai_eos/intelligence/eos_first_principles.py` | **Layer 2 (EOS Engine)** | Company lifecycle state transitions, unit economics modeling, market opportunity decision trees, runway tracking, and failure mode diagnostics. |
| **14-Layer Entrepreneurship Framework** | `apodex/ai_eos/intelligence/fourteen_layer_engine.py` | **Layer 2 (EOS Engine)** | End-to-end formalization mapping reality substrate to meta-learning swarms across all 14 layers. |
| **Multi-Agent Token Bidding Registry** | `apodex/aean/coordination/hive_mind.py` | **Layer 3 (AEAN HiveMind)** | Decentralized token auctioning, capability matching, task bidding, and worker agent assignment. |
| **Specialized Agent Swarms & Routing** | `apodex/ai_eos/research/integration.py` | **Layer 3 (AEAN)** | Swarm role specialization, budget-decayed routing gate dispatching (`LearnableRoutingGateDispatcher`), and SFT preference optimization. |
| **Causal World Model & Bayesian Belief Engine** | `apodex/world_model/domain/beliefs.py` | **Layer 4 (APODEX WorldModel)** | Maintaining entity causality graphs, recursive Bayesian prior/posterior belief updates, and time-decayed state filtering. |
| **Stateful Cognitive Processing & Brain** | `apodex/cognition/brain.py` | **Layer 4 (APODEX Cognitive Brain)** | Pydantic V2 stateful cognitive processing, memory consolidation, and action decision selection. |
| **Autonomous Code Modification & AST Safety** | `apodex/ai_eos/research/integration.py` | **Layer 4 (APODEX CodeRewriteEngine)** | AST patch parsing, Hawkes non-Gaussian recursive stability checks, and safe patch application. |
| **Governance, Compliance & Approval Gates** | `apodex/world_model/governance/approval.py` | **Layer 4 (APODEX Governance)** | Rule-based safety verification, approval thresholds, compliance gating, and execution rollback mechanisms. |
| **Cross-Layer State Handoff Bridge** | `apodex/ai_eos/research/integration.py` | **Cross-Layer Bridge (`ResearchToSystemBridge`)** | Orchestrating active inference state handoffs, hypothesis promotion, and cross-subsystem telemetry flow. |

---

## Elimination of Legacy Adapter Duplication

1. **Legacy Harness Memory vs. APODEX WorldModel**:
   - *Resolution*: Legacy harness memory adapters in `agent_harness/core/memory/` are strictly scoped as compatibility wrappers forwarding memory requests to `apodex/world_model/` and `apodex/cognition/brain.py`.
2. **Legacy Harness Planner vs. EIOS Kernel DAG Synthesis**:
   - *Resolution*: Legacy harness planner executors delegate task graph generation directly to `EIOSKernel` DAG synthesis.
3. **Legacy Reasoners vs. AEAN HiveMind Bidding**:
   - *Resolution*: Active learning and Graph-of-Thought reasoning engines delegate agent execution and capability routing to AEAN `HiveMind`.
