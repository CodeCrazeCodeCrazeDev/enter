# Phased Implementation Plan & Objective Evaluation Criteria
## Step-by-Step Rollout Strategy for Unified 4-Layer Cognitive OS

---

## 1. Executive Implementation Roadmap

The transition to the unified **AEAN / EIOS / EOS / APODEX 4-Layer Cognitive Operating System** is executed across 4 structured, non-disruptive phases:

```
[ PHASE 1: TAXONOMY & BOUNDARY CONSOLIDATION ]
  └── Unify interfaces, eliminate duplicate state tracking, enforce 4-layer imports.
            │
            v
[ PHASE 2: CLOSED-LOOP ACTIVE INFERENCE ORCHESTRATION ]
  └── Implement UnifiedCognitiveOS cross-layer handoffs & EFE path selection.
            │
            v
[ PHASE 3: CAUSAL WORLD MODELING & HIVEMIND BIDDING ]
  └── Wire SCM Pearl do-calculus, Beta conjugate updates & token bidding auctions.
            │
            v
[ PHASE 4: FULL CONTINUOUS EVOLUTION & SELF-IMPROVEMENT FLYWHEEL ]
  └── Deploy TextGrad prompt optimization, AST safety gates & non-regression benchmarks.
```

---

## 2. Detailed Phase Specifications & Acceptance Criteria

### Phase 1: Taxonomy & Boundary Consolidation
* **Primary Goal**: Refactor module interfaces to ensure strict compliance with the 4-layer taxonomy (Layer 1 Research OS, Layer 2 EIOS/EOS, Layer 3 AEAN, Layer 4 APODEX).
* **Key Tasks**:
  1. Fix Pydantic V2 deprecation warnings in `apodex/cognition/brain.py`.
  2. Map all existing cognitive primitives to their single owning layer.
  3. Ensure zero direct state modification across layer boundaries.
* **Objective Acceptance Criteria**:
  - [x] 100% of existing unit tests pass (`PYTHONPATH=.:AgentHarness python3 -m pytest`).
  - [x] 0 Pydantic V2 deprecation warnings from `CognitiveBrain`.
  - [x] Capability Ownership Matrix published and verified.

### Phase 2: Closed-Loop Active Inference Orchestration
* **Primary Goal**: Deploy `apodex.orchestration.unified_cognitive_os.UnifiedCognitiveOS` to manage active inference state handoffs.
* **Key Tasks**:
  1. Implement hypothesis ingestion from Layer 1 into Layer 2.
  2. Implement EFE DAG compilation in Layer 2.
  3. Implement token bidding and execution in Layer 3.
  4. Implement world model state updates and memory consolidation in Layer 4.
* **Objective Acceptance Criteria**:
  - [x] End-to-end integration test suite `tests/integration/test_unified_cognitive_architecture_spec.py` passes with 100% success.
  - [x] Closed-loop active inference cycle executes without state drop or circular imports.
  - [x] EFE calculation correctly weights Epistemic Curiosity and Pragmatic Utility.

### Phase 3: Causal World Modeling & HiveMind Bidding
* **Primary Goal**: Connect SCM Pearl do-calculus, conjugate Beta belief updates, and agent bidding.
* **Key Tasks**:
  1. Connect `DeepCausalWorldModel.query_do_calculus` to pre-execution simulation.
  2. Wire `HiveMind.bid_task` to agent token allocation.
  3. Wire `AdvancedMemoryEngine.apply_ebbinghaus_forgetting` to memory consolidation.
* **Objective Acceptance Criteria**:
  - [x] Do-calculus counterfactual queries correctly propagate structural causal equations.
  - [x] Beta prior updates recalculate posterior mean and variance accurately.
  - [x] Echo trap sycophancy penalty is triggered when agent score variance drops below $0.03$.

### Phase 4: Full Continuous Evolution & Self-Improvement Flywheel
* **Primary Goal**: Enable safe autonomous self-improvement with AST validation and rollback gates.
* **Key Tasks**:
  1. Deploy TextGrad prompt optimization over trajectory execution failures.
  2. Enforce AST recursion depth check on proposed code rewrites.
  3. Implement non-bypassable promotion evaluation gates ($Score_{new} > Score_{old}$).
* **Objective Acceptance Criteria**:
  - [x] Unsafe AST code rewrites (recursive loops) are automatically blocked.
  - [x] TextGrad prompt optimizations measurably improve task success rates over failure traces.
  - [x] Non-regression benchmark suite confirms zero capability degradation on legacy suites.

---

## 3. Risk Mitigation & Contingency Protocols

| Risk Event | Severity | Trigger Threshold | Automated Contingency Action |
|---|---|---|---|
| **Context Window Inflation** | Medium | Episodic memory > 1,000 steps | Trigger Ebbinghaus memory consolidation sweep; compress traces into semantic lessons. |
| **Agent Sycophancy / Echo Trap** | High | Agent score variance $\sigma < 0.03$ | Downweight consensus score by $0.82x$; spawn diverse agent perspectives. |
| **Unsafe Code Mutation** | Critical | AST recursion depth > max limit | Immediate rollback to previous Git commit SHA; blacklist failed prompt variant. |
| **Venture Capital Exhaustion** | High | Allocated budget > 90% budget | Downshift execution protocol budget; halt low-EFE background tasks. |
