# Apodex Next-Generation Cognitive Architecture: Autonomous Economic Agent Network (AEAN)

> ### ⚠️ DOCUMENT STATUS: CONSOLIDATED & UNIFIED
> This architecture specification has been fully consolidated into the authoritative, single-source-of-truth **Unified Cognitive Operating System Architecture Specification**.
>
> All development, capability mappings, and system designs are governed by the unified 4-layer taxonomy defined at:
> **[docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md](docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md)**

---

## 1. The Unified 4-Layer Cognitive Operating System

To eliminate architectural duplication, simplify systemic maintenance, and enforce clean domain boundaries, the five legacy systems (Research OS, EIOS, EOS, AEAN, APODEX) have been unified into a single layered stack:

1.  **Layer 1: Research OS (The Research Layer)**: Hypothesis generation, literature review, theory validation, and academic/arXiv indexing.
2.  **Layer 2: AEAN (The Cognitive Intelligence Layer)**: Multi-graph continuous world modeling (E-K-C-T-U), Active Inference planning under uncertainty, expected free energy evaluation, and 6-paradigm collective intelligence.
3.  **Layer 3: EIOS / EOS (The Execution & Orchestration Layer)**: 14-Layer Computational Architecture of Entrepreneurship, 13 multi-timescale business loops, customer discovery, GTM strategy, brand and pricing models.
4.  **Layer 4: APODEX (The Decision & Execution Layer)**: ReAct execution loops, isolated sandbox python runners, SLA telemetry monitoring, staged canary rollouts, and automated transparent rollbacks.

```
+-----------------------------------------------------------------------------------+
| 1. RESEARCH OS (The Research Layer)                                               |
|    - Hypothesis Generation · Literature Indexing · Theory Promotion · arXiv      |
+-----------------------------------------------------------------------------------+
                                      │
                                      ▼
+-----------------------------------------------------------------------------------+
| 2. AEAN (The Cognitive Intelligence Layer)                                        |
|    - Active Inference · World Modeling (E-K-C-T-U) · 6-Paradigm Reasoning         |
+-----------------------------------------------------------------------------------+
                                      │
                                      ▼
+-----------------------------------------------------------------------------------+
| 3. EIOS / EOS (The Execution & Orchestration Layer)                               |
|    - 14-Layer Computational Architecture · 13 Multi-Timescale Business Loops     |
+-----------------------------------------------------------------------------------+
                                      │
                                      ▼
+-----------------------------------------------------------------------------------+
| 4. APODEX (The Decision & Execution Layer)                                        |
|    - ReAct Loops · Sandbox Tool Execution · SLA Telemetry · Canary Rollbacks      |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Integration Rules & API Contracts

*   **Explicit Interface Boundaries**: All communications between layers must traverse the official event bus or use the unified Python API interfaces. Dual-maintenance and split-brain model state copy are strictly prohibited.
*   **Decoupled Memory Tiering**: Memory is structured from short-term Working memory (Layer 4 ReAct context) up to persistent Semantic and Procedural memory blocks (Layers 1 and 2), maintained asynchronously.
*   **SLA-Driven Self-Improvement**: Low-level execution failures in Layer 4 trigger automatic rollback of configurations, while persisting discrepancy logs back to Layer 1 to spawn targeted research and parameter optimization.

For the exhaustive specification including typed interfaces, interactive data flow diagrams, and continuous evolution policies, refer to the master contract at **[docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md](docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md)**.
