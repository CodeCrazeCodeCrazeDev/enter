# Unified System Dependency Graph & Interface Specification
**Author:** Jules (Autonomous Strategic Architecture Engineer)
**Version:** 2.0.0-UNIFIED
**Subsystems:** Research OS, AEAN, EIOS / EOS, APODEX

---

## 1. Directed Acyclic Graph (DAG) of the Cognitive Operating System

```
                         [ USER / STRATEGIC GOAL ]
                                     |
                                     v
                 +---------------------------------------+
                 |       LAYER 1: RESEARCH OS            |
                 | - Hypothesis Ledger                   |
                 | - Literature Review (Jaccard Index)   |
                 | - Statistical Power Analysis          |
                 +-------------------+-------------------+
                                     |
                                     v  (Validated Hypotheses)
                 +---------------------------------------+
                 |         LAYER 2: AEAN COGNITION       |
                 | - Active Inference (EFE Engine)       |
                 | - Pearl's Do-Calculus Causal Model    |
                 | - Swarm Debate & Nash Clearing        |
                 | - Skill Flywheel (60 Skills)          |
                 +-------------------+-------------------+
                                     |
                                     v  (Informed Action Policies)
                 +---------------------------------------+
                 |       LAYER 3: EIOS / EOS KERNEL      |
                 | - Multi-Timescale Loops (T1, T2, T3)  |
                 | - Capital Downshifting / Halting      |
                 | - Opportunity Anomaly Sensing         |
                 | - Enterprise Lifecycle State Machines |
                 +-------------------+-------------------+
                                     |
                                     v  (Approved Operational Commands)
                 +---------------------------------------+
                 |         LAYER 4: APODEX RUNTIME       |
                 | - Deterministic Tool Execution        |
                 | - CMOS / EMG Memory System            |
                 | - Safety & Pre-Commit Enforcement     |
                 +---------------------------------------+
```

---

## 2. Strict Coupling & Layer Separation Rules

To prevent spaghetti architecture and circular dependencies:
1. **Unidirectional Control Flow:** Downward flow only (Layer 1 -> Layer 2 -> Layer 3 -> Layer 4).
2. **Feedback Flow via Event Subscriptions:** Upward information flow occurs strictly through observable event logs (e.g. `RealityStateUpdatedEvent` processed by CMOS/EMG in Layer 4 and observed by Layer 2 & Layer 3).
3. **No Core-to-Adapter Violations:** `apodex` core modules must NEVER import from legacy compatibility adapters in `agent_harness`. All compatibility adapters wrap core modules, not vice versa.
4. **Zero Capability Duplication:**
   - **Research & Hypothesis Validation** belongs strictly to **Layer 1 (Research OS)**.
   - **Cognitive Reasoning & Active Inference** belongs strictly to **Layer 2 (AEAN)**.
   - **Business Strategy & Capital Allocation** belongs strictly to **Layer 3 (EIOS / EOS)**.
   - **Tool Execution & Memory Storage** belongs strictly to **Layer 4 (APODEX)**.

---

## 3. Interface Contract Matrix

| Source Layer | Target Layer | Interface Method | Payload Type | Return Type |
| :--- | :--- | :--- | :--- | :--- |
| Layer 1 (Research OS) | Layer 2 (AEAN) | `get_validated_hypotheses()` | Domain Filter | `List[Hypothesis]` |
| Layer 2 (AEAN) | Layer 3 (EIOS/EOS) | `evaluate_policy_efe(policy)` | `PolicyCandidate` | `EFEEvaluationResult` |
| Layer 3 (EIOS/EOS) | Layer 4 (APODEX) | `dispatch_action(action)` | `ActionCommand` | `ExecutionSummary` |
| Layer 4 (APODEX) | Layer 2 (AEAN) | `query_memory_context(query)` | `ContextQuery` | `MemoryRetrievalCard` |

---

## 4. Verification and Dependency Analysis

Static dependency checks via `scripts/validate_dependencies.py` confirm:
- Circular dependencies: **0**
- Maximum dependency depth: **4** (SOTA limit $\le 6$)
- Core-to-adapter violations: **0**
- Split-brain duplicate classes: **0**
