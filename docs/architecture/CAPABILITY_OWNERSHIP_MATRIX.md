# Capability Ownership Matrix & Subsystem Boundaries

## Overview

This matrix establishes single-point capability ownership across all four layers of the **Unified Cognitive Operating System**, explicitly resolving historical overlaps and eliminating duplicated responsibilities between Research OS, EIOS, EOS, AEAN, and APODEX.

---

## 1. Single-Point Capability Ownership Matrix

| System Capability | Primary Owner Layer | Delegated Subsystem Module | Non-Owner Prohibited Subsystems | Rationale & Boundary Enforcement |
|---|---|---|---|---|
| **Academic Paper Ingestion & Literature Synthesis** | **Layer 1** | `apodex.research_os.pipeline` | AEAN, EIOS, WorldModel | Prevents duplicate literature databases. AEAN and EIOS consume processed insights, not raw literature. |
| **Statistical Hypothesis Generation & Power Testing** | **Layer 1** | `apodex.research_os.statistical_validation` | EOS, WorldModel | Guarantees single statistical control authority ($\alpha=0.05$ FWER). |
| **Hawkes Process Event & Anomaly Sensing** | **Layer 2** | `apodex.arcs.kernel.kernel` | Research OS, AEAN | Ensures single high-frequency event intake pipeline. |
| **EFE DAG Task Scheduling & Capital Allocation** | **Layer 2** | `apodex.ai_eos.intelligence.eos_engine` | WorldModel, AEAN | Centralizes economic decisions and Active Inference expected free energy scheduling. |
| **Multi-Agent Token Bidding & Auction Allocation** | **Layer 3** | `apodex.aean.coordination.hive_mind` | EIOS, Research OS | Centralizes multi-agent coordination into a single bidding registry. |
| **MAP-Elites Evolutionary Strategy Search** | **Layer 3** | `apodex.aean.evolution` | WorldModel, EOS | Strategy evolution belongs in the cognitive intelligence layer. |
| **Causal Graph Indexing & Relationship Traversal** | **Layer 4** | `apodex.world_model.world_model` | AEAN, EIOS, Research OS | Prevents fragmented local causal graphs across agents. All agents query central WorldModel. |
| **Recursive Bayesian Belief State Updates** | **Layer 4** | `apodex.world_model.domain.beliefs` | EOS, AEAN | Single point of truth for state probabilities $P(H|E)$. |
| **Unified Memory (CMOS / Epistemic Memory Graph)** | **Layer 4** | `apodex.memory.learning_memory` | Research OS, EIOS | Centralized long-term memory substrate. |

---

## 2. Boundary Enforcement Protocols

1. **Direct Subsystem Bypass Prohibition**: Subsystems must interact via standardized DTOs and registered interfaces (e.g., `ResearchToSystemBridge`) rather than importing internal helper modules across layer boundaries.
2. **Duplicated Storage Prohibition**: No subsystem outside Layer 4 may maintain a persistent graph store or separate memory repository. All persistent world state resides in `WorldModel` and `CMOS`.
3. **Single Statistical Authority**: All hypothesis tests must pass through Layer 1's statistical validation engine to prevent inflated false-positive discovery rates.
