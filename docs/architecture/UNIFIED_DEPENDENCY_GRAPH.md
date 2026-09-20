# Unified Cognitive Operating System Dependency Graph
**Data Flows, Control Flows, State Transitions, and Event Propagation**
**Version:** 4.0.0
**Scope:** Research OS (Layer 1) | EIOS & EOS (Layer 2) | AEAN (Layer 3) | APODEX (Layer 4)

---

## 1. Subsystem Interaction Architecture

The dependency graph below illustrates the precise topological data flows, control flows, state transitions, and event propagation paths across the 4 layers.

```
+---------------------------------------------------------------------------------------------------+
| LAYER 1: RESEARCH LAYER (Research OS)                                                             |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
|   | 500-Paper Corpus      | --> | Literature Review Engine | --> | Hypothesis Generator       |   |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
|                                                                                |                  |
|                                                                                v                  |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
|   | Reproducibility Audit | <-- | Statistical Validation   | <-- | Empirical Experiment Engine|   |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
+-----------------------------------------------+---------------------------------------------------+
                                                |
                                                | Validated Hypothesis & Active Principles
                                                v
+---------------------------------------------------------------------------------------------------+
| LAYER 2: EXECUTION & ORCHESTRATION LAYER (EIOS Kernel & EOS Engine)                               |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
|   | Hypothesis Ingestion  | --> | Active Inference Sensing | --> | EFE Policy Evaluator       |   |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
|                                                                                |                  |
|                                                                                v                  |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
|   | Capital Allocation    | <-- | EOS 11-Stage State Machine| <--| DAG Workflow Scheduler     |   |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
+-----------------------------------------------+---------------------------------------------------+
                                                |
                                                | Task DAGs & Token Bidding Requests
                                                v
+---------------------------------------------------------------------------------------------------+
| LAYER 3: COGNITIVE INTELLIGENCE LAYER (AEAN HiveMind)                                             |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
|   | Bidding Auction Reg   | --> | Consensus Engine         | --> | Specialized Agent Swarm    |   |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
|                                                                                |                  |
|                                                                                v                  |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
|   | SFT/DPO Preference    | <-- | Hawkes AST Rewrite Verif | <-- | MAP-Elites Island Optimizer|   |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
+-----------------------------------------------+---------------------------------------------------+
                                                |
                                                | Executable Action Proposals & Code Rewrites
                                                v
+---------------------------------------------------------------------------------------------------+
| LAYER 4: DECISION & EXECUTION PLATFORM LAYER (APODEX WorldModel & Cognitive Brain)                |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
|   | Causal Node Graph     | --> | Recursive Bayesian Belief| --> | Skills Protocol Runner     |   |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
|                                                                                |                  |
|                                                                                v                  |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
|   | Feedback to Layer 1   | <-- | Credit & Cost Halter     | <-- | Regulatory Governance Gate |   |
|   +-----------------------+     +--------------------------+     +----------------------------+   |
+-----------------------------------------------+---------------------------------------------------+
                                                |
                                                +---> Realized Outcomes & Causal Evidence ---> [Loop Back to Layer 1]
```

---

## 2. Detailed Data Flow & Event Propagation

### 2.1 Forward Propagation Path (Hypothesis -> Decision -> Action)
1. **Layer 1 to Layer 2:**
   - **Trigger:** Scientific hypothesis validated ($DSR > 1.0, p < 0.05$).
   - **Payload:** `ResearchHypothesis` object containing expected outcome distributions, parameter bounds, and underlying 500-paper principles.
   - **Method:** `ResearchToSystemBridge.export_validated_hypothesis_to_kernel()`.
   - **Layer 2 Event:** `HypothesisRegisteredEvent` emitted in `EIOSKernel`.

2. **Layer 2 to Layer 3:**
   - **Trigger:** Active Inference EFE evaluation yields optimal policy $u^*$.
   - **Payload:** Task DAG specification, budget constraints, expected epistemic gain.
   - **Method:** `EIOSKernel.execute_workflow_dag()` -> `HiveMind.submit_bidding_auction()`.
   - **Layer 3 Event:** `TaskAuctionOpenedEvent` emitted in `HiveMind`.

3. **Layer 3 to Layer 4:**
   - **Trigger:** Bidding consensus reached and AST rewrite verified.
   - **Payload:** Action plan, parameter updates, code patch proposals.
   - **Method:** `CodeRewriteEngine.verify_proposal_ast()` -> `WorldModelCoordinator.apply_action()`.
   - **Layer 4 Event:** `RealityStateUpdatedEvent` emitted in `WorldModel`.

### 2.2 Backward Feedback & Belief Update Path (Outcome -> Belief -> Research Refinement)
1. **Layer 4 to Layer 4 (Recursive Belief Update):**
   - **Trigger:** Skill execution completes with empirical outcome observation $o_t$.
   - **Payload:** Evidence tensor $e_t$, execution cost, execution time.
   - **Method:** `BayesianBeliefEngine.update_belief(belief_id, evidence)`.
   - **State Update:** Prior belief distribution updated to Posterior $P(\theta | o_t)$.

2. **Layer 4 to Layer 2 (EOS Stage Transition & Risk Audit):**
   - **Trigger:** Causal belief probability crosses confidence threshold or failure mode detected.
   - **Payload:** Growth metrics, unit economics, risk exposure.
   - **Method:** `EOSStateMachine.transition_eos_state()`.
   - **State Update:** EOS stage transitions (e.g. Stage 3 Validation -> Stage 4 Scaled Growth) or triggers failure mode rollback.

3. **Layer 4 to Layer 1 (Research Literature Refinement):**
   - **Trigger:** Empirical execution results deviate from Layer 1 hypothesis expectations by $>2\sigma$.
   - **Payload:** Anomaly delta, execution logs, causal graph diff.
   - **Method:** `Research OS.ingest_anomaly_feedback()`.
   - **State Update:** Layer 1 triggers literature search and hypothesis refinement.

---

## 3. Directional Module Dependency Matrix

| Source Module | Target Module | Dependency Type | Interface Method / Event |
| :--- | :--- | :--- | :--- |
| `apodex.research_os.research_os` | `apodex.arcs.kernel.kernel` | State Export | `export_validated_hypothesis_to_kernel` |
| `apodex.research_os.research_os` | `apodex.ai_eos.intelligence.eos_engine` | State Promotion | `promote_hypothesis_to_eos` |
| `apodex.arcs.kernel.kernel` | `apodex.aean.coordination.hive_mind` | Auction Bidding | `submit_bidding_auction` |
| `apodex.aean.coordination.hive_mind` | `apodex.ai_eos.research.integration` | Code Verification | `verify_proposal_ast` |
| `apodex.ai_eos.research.integration` | `apodex.world_model.world_model` | Causal Update | `update_entity_state` |
| `apodex.world_model.world_model` | `apodex.world_model.domain.beliefs` | Recursive Bayesian | `update_bayesian_belief` |
| `apodex.skills.runner` | `apodex.world_model.governance.approval` | Safety Gate | `evaluate_governance_compliance` |

---

## 4. Circular Dependency Audit & Architectural Guarantees

1. **Acyclic Module Graph:** All inter-module dependencies flow strictly top-down (Layer 1 -> Layer 2 -> Layer 3 -> Layer 4) for direct control execution.
2. **Asynchronous Feedback Event Bus:** Reverse feedback (Layer 4 -> Layer 1) is decoupled via asynchronous event handling (`EventDispatcher`), preventing circular import locks.
3. **Canonical Ownership:** No module in Layer 3 or Layer 4 duplicates planning or scheduling algorithms reserved for Layer 2.
