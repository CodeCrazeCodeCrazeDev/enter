# Phased Implementation Plan & Evaluation Criteria

## 1. Phase Overview

The migration to the unified 4-layer cognitive operating system is executed across four incremental, zero-downtime phases:

```
+-------------------+     +-------------------+     +-------------------+     +-------------------+
|     PHASE 1       | --> |     PHASE 2       | --> |     PHASE 3       | --> |     PHASE 4       |
| Architecture &    |     | Layer 1 <-> 2     |     | Layer 2 <-> 3     |     | Layer 3 <-> 4     |
| Specification     |     | Active Inference |     | HiveMind Auction  |     | World Model Sync  |
+-------------------+     +-------------------+     +-------------------+     +-------------------+
```

---

## 2. Detailed Phase Specifications

### Phase 1: Architectural Formalization & Interface Contracts (Completed)
* **Scope:** Design, author, and audit the 7 authoritative cognitive architecture specifications. Establish strict import boundaries and data flow contracts.
* **Deliverables:**
  - `UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md`
  - `UNIFIED_DEPENDENCY_GRAPH.md`
  - `PRIORITIZED_ROI_ROADMAP.md`
  - `SOTA_GAP_ANALYSIS_2026.md`
  - `PHASED_IMPLEMENTATION_PLAN.md`
  - `CONTINUOUS_EVOLUTION_STRATEGY.md`
  - `CAPABILITY_OWNERSHIP_MATRIX.md`
* **Evaluation Criteria:** Architectural audit script `verify_architecture_docs.py` passes with 100% compliance.

### Phase 2: Layer 1 to Layer 2 Integration (`ResearchToSystemBridge`)
* **Scope:** Implement `ResearchToSystemBridge` in `apodex/ai_eos/research/integration.py`. Wire `ResearchOS.export_validated_hypothesis_to_kernel` and `promote_hypothesis_to_eos`.
* **Deliverables:**
  - Cross-layer handoff methods in `ResearchOS`, `EIOSKernel`, and `EOSEngine`.
  - Integration unit tests validating research hypothesis propagation to sensing DAGs.
* **Evaluation Criteria:** Validated research hypotheses seamlessly convert into active EFE sensing nodes without manual translation.

### Phase 3: Layer 2 to Layer 3 Integration (`EOSToHiveMindBridge`)
* **Scope:** Connect `EOSEngine` opportunity nodes to `AEAN HiveMind` token bidding auctions.
* **Deliverables:**
  - `register_research_insight` and opportunity bidding handlers in `HiveMind`.
  - Automated worker agent assignment based on token bids and capability match.
* **Evaluation Criteria:** Opportunity tasks trigger competitive agent token auctions with < 50ms latency.

### Phase 4: Layer 3 to Layer 4 Integration & Full-Loop Validation
* **Scope:** Connect `HiveMind` execution outcomes to `APODEX WorldModel` causal graph and Bayesian belief updates.
* **Deliverables:**
  - End-to-end integration test suite `tests/integration/test_unified_4layer_integration.py`.
  - Automated belief update feedback loop to Research OS.
* **Evaluation Criteria:** All 397+ repository unit/integration tests pass cleanly with zero regression errors.
