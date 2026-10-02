# PHASED IMPLEMENTATION PLAN
## Objective Evaluation Criteria & Rollout Phases

---

### Implementation Roadmap Overview

```
+-----------------------------------------------------------------------------------+
| PHASE 1: Subsystem Decoupling & Capability Ownership Matrix                      |
| - Eliminate duplicated modules across Research OS, EIOS, EOS, AEAN, APODEX       |
| - Objective Metric: 100% single-layer capability ownership, 0 duplicate classes   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 2: Cross-Layer Active Inference State Handoff Engine                       |
| - Implement ResearchToSystemBridge and unified Layer 1-4 state handoffs          |
| - Objective Metric: Complete closed-loop execution without state dropouts          |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 3: Transferable Principles Integration (600-Paper Corpus)                    |
| - Register 100/200/300/400/500/600 paper principles into ResearchOS & AEAN        |
| - Objective Metric: Zero title/DOI overlap, 100% principle queryability           |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 4: Self-Referential Evolution & Safety Governance Hardening                 |
| - Hawkes AST call depth verification + DPO preference collector + Credit Halting  |
| - Objective Metric: 0 unsafe execution breaches, 0 AST recursive stack overflows  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE 5: Full End-to-End System Benchmarking & Validation                         |
| - Integration test suite execution (390+ unit & integration test cases passing)   |
| - Objective Metric: 100% test suite pass rate, 0 collection errors                |
+-----------------------------------------------------------------------------------+
```

---

### Phase Specifications & Objective Verification Criteria

#### Phase 1: Decoupling & Taxonomy Alignment
- **Milestones**:
  1. Map all 16 core cognitive capabilities to single owning layers.
  2. Re-export core intelligence interfaces via `apodex/ai_eos/intelligence/__init__.py`.
- **Verification Criteria**:
  - `check_layer_imports.py` and `audit_and_verify_unified_architecture.py` pass cleanly.

#### Phase 2: Cross-Layer Bridge & State Handoffs
- **Milestones**:
  1. Implement `ResearchToSystemBridge` in `apodex/ai_eos/research/integration.py`.
  2. Connect Research OS hypotheses to EIOS DAGs, AEAN HiveMind bidding, and APODEX WorldModel updating.
- **Verification Criteria**:
  - `tests/integration/test_unified_cognitive_architecture_spec.py` passes with 100% assertions satisfied.

#### Phase 3: Research Corpus Principles Integration
- **Milestones**:
  1. Register extracted principles from papers 1–600 in `apodex/ai_eos/research/integration.py`.
  2. Implement multi-field domain searching in `ResearchOS.conduct_literature_review`.
- **Verification Criteria**:
  - Corpus verification scripts confirm 0 duplicate DOIs/titles and active principle retrieval.

#### Phase 4: Self-Modification Safety & Credit Halting
- **Milestones**:
  1. Enforce AST static security checks and Hawkes function recursion limits in `CodeRewriteEngine`.
  2. Enforce credit halting and rate limits in `WorldModel` / `CreditHaltEngine`.
- **Verification Criteria**:
  - Dangerous snippet injection fails AST parsing; valid code passes dry run simulation.

#### Phase 5: Verification & System Health
- **Milestones**:
  1. Execute full pytest suite (`python3 -m pytest`).
  2. Confirm clean timezone-aware datetimes across all modules (`datetime.now(timezone.utc)`).
- **Verification Criteria**:
  - 390+ test cases pass without errors.
