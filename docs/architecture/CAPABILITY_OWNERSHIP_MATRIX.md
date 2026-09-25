# Capability Ownership Matrix

## 1. Executive Summary

To eliminate capability duplication across **Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX**, this matrix establishes canonical ownership for every major subsystem function. Legacy adapters and overlapping logic are consolidated under single authoritative canonical owners.

---

## 2. Canonical Ownership Matrix

| System Capability | Primary Canonical Module Path | Layer | Disallowed Duplicate Implementations |
|---|---|---|---|
| **Literature Analysis & Paper Corpus** | `apodex.ai_eos.research.research_os` | Layer 1 | Direct paper parsing in EIOS or AEAN |
| **Statistical Validation (DSR, FDR)** | `apodex.research_os.statistical_validation` | Layer 1 | Ad-hoc statistics in HiveMind or EOS |
| **AST Code Rewrite Proposal Guard** | `apodex.ai_eos.research.integration` | Layer 1 | Manual AST parsing in execution runners |
| **Active Inference Sensing (EFE)** | `apodex.arcs.kernel.kernel` | Layer 2 | Custom sensing loops in AEAN agents |
| **Entrepreneurial State & Capital** | `apodex.ai_eos.intelligence.eos_engine` | Layer 2 | Disjointed state tracking in WorldModel |
| **Multi-Agent Bidding & Auction** | `apodex.aean.coordination.hive_mind` | Layer 3 | Local agent-to-agent prompt routers |
| **Causal Graph & Relation Edges** | `apodex.world_model.world_model` | Layer 4 | Duplicate causal DAGs in Research OS |
| **Recursive Bayesian Belief Engine** | `apodex.world_model.domain.beliefs` | Layer 4 | Local belief arrays in EIOS Kernel |
| **Safety Governance & Approval** | `apodex.world_model.governance.approval` | Layer 4 | Hardcoded approval checks in agent scripts |
| **Skills & Protocol Execution** | `apodex.skills.runner` | Layer 4 | Ephemeral skill scripts in AEAN |

---

## 3. Implementation Guidelines for Engineers

1. **Check Ownership Before Adding Code:** Before introducing a new planner, memory buffer, or world model node, consult this matrix.
2. **Reuse Canonical Modules:** If a module requires causal reasoning, import `WorldModel` from `apodex.world_model`. Do not build a local causal graph.
3. **Cross-Layer Communication via Bridges:** Use `ResearchToSystemBridge` in `apodex/ai_eos/research/integration.py` for cross-layer data transfers.
