# Architecture Ownership Matrix
## Institutional Disambiguation & Duplicate Resolution Register (v1.0)

This matrix formally catalogs all major platform capabilities and maps them to a single authoritative canonical owner module. It resolves structural overlaps by classifying every legacy or duplicate implementation as **Canonical**, **Adapter (temporary)**, **Archive**, or **Delete**.

---

## 1. Disambiguation and Single Ownership Mapping

| Capability Area | Canonical Owner Path | Legacy / Overlapping Paths | Disposition Status |
| :--- | :--- | :--- | :--- |
| **Active Inference & EFE** | `apodex/ai_eos/active_inference/engine.py` | `apodex/cognition/research/autonomous_institution.py` (ExpectedFreeEnergyPlanner) | **Canonical** (Active Inference engine resides exclusively under Layer 3 Active Inference context). Overlapping implementations are archived. |
| **Structural Causal Models & counterfactual do-calculus** | `apodex/ai_eos/intelligence/decision_engine.py` | `apodex/cognition/research/autonomous_institution.py` (StructuralCausalModel) | **Canonical** (Decision Engine handles Pearl's do-calculus, shadow prices, and Lagrange multipliers). Overlapping academic copies are archived. |
| **Cognitive Memory Consolidation & Ebbinghaus decay** | `apodex/memory/learning_memory.py` | `apodex/cognition/research/autonomous_institution.py` (EbbinghausMemoryConsolidator) | **Canonical** (Consolidation routines operate directly in the persistent SQLite-backed database layer under `apodex/memory`). |
| **Multi-Mind Reasoning & Consensus** | `apodex/ai_eos/intelligence/collective.py` | `apodex/cognition/research/autonomous_institution.py` (ConsensAgentEngine) | **Canonical** (The Multi-Mind Consensus Deliberation engine coordinates consensus models, sycophancy mitigation, and agent interaction layers). |
| **Constitutional Safety & GRC Audits** | `apodex/aean/governance.py` | `apodex/safety/core.py` | **Canonical** (ConstitutionalFilter resides under Layer 1 GRC governance). The duplicate `apodex/safety/core.py` is archived. |
| **Experience Memory Graph (EMG) Sequence Mining** | `apodex/memory/emg_engine.py` | `agent_harness/core/memory/emg_engine.py` | **Canonical** (Sequence pattern-mining and sequence edit paths belong exclusively to the shared multi-tier memory layer under `apodex/memory`). Temporary adapter under `agent_harness.core.memory` bridges legacy tests. |
| **Inference-Time Keyword Context Matching (MemoHarness)** | `apodex/memory/semantic_memory.py` (Jaccard context matching) | `agent_harness/core/memory/semantic_memory.py` | **Canonical** (Jaccard token overlap query matching is handled exclusively inside the canonical `SemanticMemory` database). Temporary adapter bridges legacy tests. |
| **Sovereign Entrepreneurial Organization Registry (IES)** | `apodex/ai_eos/governance/gateway.py` | `apodex/aean/governance.py` (Partially overlapping) | **Canonical** (The starting roster of all 29 specialized cross-cutting agents belongs to Layer 1 GRC Gateway). |

---

## 2. Duplicate Resolution Register

### 1. `apodex/cognition/research/autonomous_institution.py`
- **Classifications**: Academic/Reference Models
- **Action**: **Archive** (The exact active inference planner, structural causal model, memory consolidator, and consensus engines here are kept for academic reference but are superseded by the canonical, optimized modules under `apodex/ai_eos/active_inference/`, `apodex/ai_eos/intelligence/`, `apodex/memory/`, and `apodex/ai_eos/intelligence/collective.py` respectively).

### 2. `agent_harness/core/memory/`
- **Classifications**: Compatibility Adapter
- **Action**: **Adapter** (Create a lightweight, temporary adapter package under `agent_harness.core.memory` that dynamically maps older import structures to their corresponding canonical implementations under `apodex/memory/emg_engine.py` and `apodex/memory/semantic_memory.py`. This package will contain absolutely no duplicated logic).

### 3. `agent_harness/core/cost_tier.py`
- **Classifications**: Compatibility Adapter
- **Action**: **Adapter** (Redirect to `apodex/skills/models.py:CostTier` to resolve import failures).

### 4. `agent_harness/core/runtime/verification/parallel.py`
- **Classifications**: Compatibility Adapter
- **Action**: **Adapter** (Redirect to `apodex/governance/parallel_verification.py` to bridge legacy tests cleanly).

---

## 3. Strict Boundary Reinforcement

To maintain high maintainability and prevent further architectural drift:
1. No developer or automated rewrite is allowed to duplicate logic across layer boundaries.
2. If a legacy pipeline requires custom memory, planners, or verifiers, it must use the Compatibility Adapter layer to access the canonical `apodex` structures rather than importing them directly or creating new local copies.
3. Every future pull request must reduce duplication and enforce complete capability ownership.
