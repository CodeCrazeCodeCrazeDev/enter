# Unified Cognitive Operating System: Dependency & Flow Graph Specification
**Document ID:** ARCH-GRAPH-2026-V4
**Target Systems:** Research OS | EIOS | EOS | AEAN | APODEX

---

## 1. Top-Level Architectural Dependency Graph

```
                   +-------------------------------------------------------+
                   |                 EXTERNAL REALITY & DATA                |
                   |       (Academic Papers, Market Feeds, Code repos)      |
                   +-------------------------------------------------------+
                                               |
                                               v
+---------------------------------------------------------------------------------------------------+
| LAYER 1: SCIENTIFIC RESEARCH & HYPOTHESIS DISCOVERY (Research OS)                                 |
|                                                                                                   |
|   +--------------------------+    +-------------------------------+    +----------------------+   |
|   | Literature Ingestion     | -> | Statistical Validation        | -> | ResearchToSystem     |   |
|   | (400 Research Papers DB) |    | Engine (DSR & Welch's t-test) |    | Bridge               |   |
|   +--------------------------+    +-------------------------------+    +----------------------+   |
+---------------------------------------------------------------------------------------------------+
                                               |
                                               | Validated Hypothesis & Active Inference Priors
                                               v
+---------------------------------------------------------------------------------------------------+
| LAYER 2: EXECUTION & ORCHESTRATION (EIOS / EOS)                                                   |
|                                                                                                   |
|   +--------------------------+    +-------------------------------+    +----------------------+   |
|   | EIOS Kernel (Active      | -> | EOS Engine (14-Layer          | -> | Learnable Routing    |   |
|   | Inference EFE Sensing)   |    | Entrepreneurial State Machine)|    | Gate Dispatcher      |   |
|   +--------------------------+    +-------------------------------+    +----------------------+   |
+---------------------------------------------------------------------------------------------------+
                                               |
                                               | Active Inference Task DAG & Budget Allocation
                                               v
+---------------------------------------------------------------------------------------------------+
| LAYER 3: COGNITIVE INTELLIGENCE (AEAN)                                                            |
|                                                                                                   |
|   +--------------------------+    +-------------------------------+    +----------------------+   |
|   | HiveMind Token-Bidding   | <->| Graph-of-Thought Reasoning    | <->| CMOS Epistemic &     |   |
|   | Multi-Agent Auction      |    | & Contradiction Resolver      |    | Ebbinghaus Memory    |   |
|   +--------------------------+    +-------------------------------+    +----------------------+   |
|                                              |                                                    |
|                                              v                                                    |
|                               +-------------------------------+                                   |
|                               | World Model Simulator &       |                                   |
|                               | Counterfactual Credit Halt    |                                   |
|                               +-------------------------------+                                   |
+---------------------------------------------------------------------------------------------------+
                                               |
                                               | Skill Directives & Verified Tool Requests
                                               v
+---------------------------------------------------------------------------------------------------+
| LAYER 4: DECISION & PLATFORM EXECUTION (APODEX)                                                   |
|                                                                                                   |
|   +--------------------------+    +-------------------------------+    +----------------------+   |
|   | Skill Registry & Runner  | -> | Governance & Safety Gateway   | -> | Self-Healing Code    |   |
|   | (60 Pre-populated skills)|    | (Tiered Approvals & Audit)    |    | Rewrite Engine       |   |
|   +--------------------------+    +-------------------------------+    +----------------------+   |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. End-to-End Control & Data Flow Cycle

### Step 1: Hypothesis Ingestion & Statistical Validation (Layer 1)
1. `ResearchOS` ingests research documents from the 400-paper corpus (`AI_EOS_RESEARCH_DB.yaml` and `ALPHA_ALGO_301_400_RESEARCH.yaml`).
2. `StatisticalValidationEngine` computes statistical significance metrics ($p < 0.01$, Deflated Sharpe Ratio $DSR \ge 0.95$).
3. `ResearchToSystemBridge` converts validated findings into active inference priors $P(S)$ and exports them to Layer 2 via `export_validated_hypothesis_to_kernel()`.

### Step 2: Environmental Sensing & State Orchestration (Layer 2)
1. `EIOSKernel` receives hypothesis priors and senses environment anomalies.
2. `EIOSKernel` computes Expected Free Energy ($EFE = \text{Ambiguity} + \text{Risk}$).
3. `EOSEngine` ingests validated hypotheses into `active_hypotheses`, updating the 14-Layer Computational Architecture state.
4. `LearnableRoutingGateDispatcher` compiles an optimized Task DAG and dispatches it to Layer 3.

### Step 3: Swarm Coordination, Reasoning & Memory Retrieval (Layer 3)
1. `HiveMind` receives the Task DAG and triggers a sealed token-bidding auction among specialized worker agents.
2. Winning agents invoke `GraphOfThoughtEngine` to execute step-by-step reasoning branches.
3. Agents query `CMOS` memory, retrieving relevant contextual facts adjusted for Ebbinghaus retention decay ($R = e^{-t / S}$).
4. Proposed action sequences are evaluated inside `WorldModel` counterfactual simulations. If trajectory variance exceeds risk thresholds, a `CreditHalt` is enforced.

### Step 4: Governance-Enforced Skill Execution (Layer 4)
1. Validated action sequences are passed to `SkillRegistry` as `SkillExecutionDirective` objects.
2. `InstitutionalGovernanceGateway` evaluates approval tiers (Automated vs Human-in-the-Loop) and enforces SLA performance budgets.
3. `SkillRunner` executes the operational tool or invokes `CodeRewriteEngine` for self-healing code refactoring.
4. Execution results, performance telemetry, and SLA metrics are piped back to Layer 3 `CMOS` memory and Layer 2 `EOSEngine` for continuous state feedback.

---

## 3. Subsystem Inter-Module Interface Protocol Summary

| Source Subsystem | Destination Subsystem | Interface Method / Contract | Primary Payload |
| :--- | :--- | :--- | :--- |
| **Research OS (Layer 1)** | **EIOS Kernel (Layer 2)** | `ResearchToSystemBridge.export_to_kernel()` | `ScientificHypothesisPayload` |
| **Research OS (Layer 1)** | **EOS Engine (Layer 2)** | `ResearchToSystemBridge.promote_to_eos()` | `ValidatedHypothesis` |
| **EIOS Kernel (Layer 2)** | **AEAN HiveMind (Layer 3)** | `EOSEngine.dispatch_task_dag()` | `OrchestrationTaskDAG` |
| **AEAN Swarm (Layer 3)** | **CMOS Memory (Layer 3)** | `CMOS.query_and_update_memory()` | `ContextFact` & Decay Weights |
| **AEAN Swarm (Layer 3)** | **APODEX Skill Registry (Layer 4)**| `SkillRunner.execute_skill()` | `SkillExecutionDirective` |
| **APODEX Governance (Layer 4)**| **EOS Engine (Layer 2)** | `GovernanceGateway.log_telemetry()` | `SLATelemetryRecord` |
