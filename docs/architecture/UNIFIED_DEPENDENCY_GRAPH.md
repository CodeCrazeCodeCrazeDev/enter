# Unified Cognitive Operating System Dependency Graph & Data Flow
**Version:** 2026.1.0
**Status:** Authoritative Specification
**Scope:** Layers 1–4 Interaction Topography & Interface Protocols

---

## 1. Directional Interaction Graph

```
+-----------------------------------------------------------------------------------+
|                        LAYER 4: APODEX PLATFORM & WORLD MODEL                     |
|  - World Model Engine (apodex.world_model)                                        |
|  - Skills Flywheel & Tool Registry (apodex.skills)                                |
|  - Governance & Safety Guardrails (apodex.world_model.governance)                |
+-----------------------------------------------------------------------------------+
       ^                                                                   |
       | Bayesian Updates &                                                | Tool Execution,
       | Causal Edge Observations                                          | World State Context
       |                                                                   v
+-----------------------------------------------------------------------------------+
|                     LAYER 3: AEAN COGNITIVE INTELLIGENCE LAYER                    |
|  - HiveMind Coordinator & Bidding Engine (apodex.aean.coordination)              |
|  - Graph-of-Thought & Reasoning Engines (agent_harness.core.runtime)              |
|  - Multi-Tier Memory Systems (agent_harness.core.memory)                         |
+-----------------------------------------------------------------------------------+
       ^                                                                   |
       | Token Bidding Results &                                           | Task Decomposition &
       | Subtask Completion Events                                         | Worker Allocation
       |                                                                   v
+-----------------------------------------------------------------------------------+
|               LAYER 2: EIOS / EOS EXECUTION & ORCHESTRATION LAYER                  |
|  - EIOS Kernel Active Inference Sensing (apodex.arcs.kernel)                      |
|  - EOS Strategy & 14-Layer Engine (apodex.ai_eos.intelligence)                   |
|  - ResearchOS-to-System Bridge (apodex.ai_eos.research.integration)              |
+-----------------------------------------------------------------------------------+
       ^                                                                   |
       | Validated Research Hypotheses &                                   | Strategic Objectives &
       | Extracted Corpus Principles                                       | Experiment Demands
       |                                                                   v
+-----------------------------------------------------------------------------------+
|                         LAYER 1: RESEARCH OS (RESEARCH LAYER)                     |
|  - Hypothesis Engine & Literature Review (apodex.ai_eos.research)                 |
|  - Statistical Validation & Reproducibility (apodex.research_os)                  |
|  - Code Mutation & AST Verification Engine (apodex.ai_eos.research)              |
+-----------------------------------------------------------------------------------+
```

---

## 2. Layer-by-Layer Data Flow Specifications

### 2.1 Layer 1 $\rightarrow$ Layer 2 (Research to Execution Handoff)
- **Data Payload:** `ValidatedHypothesis`, `EngineeringPrinciple`, `CodeMutationProposal`.
- **Primary Mechanism:** `ResearchToSystemBridge` in `apodex/ai_eos/research/integration.py`.
- **Flow Description:**
  1. Layer 1 validates a hypothesis via `StatisticalValidator` (computing $p$-values, Deflated Sharpe Ratio, and statistical power).
  2. The bridge calls `export_validated_hypothesis_to_kernel()`, registering an anomaly node in `EIOSKernel`.
  3. The bridge calls `promote_hypothesis_to_eos()`, updating the `EOSEngine` state machine.

### 2.2 Layer 2 $\rightarrow$ Layer 3 (Execution to Intelligence Handoff)
- **Data Payload:** `OpportunityDAG`, `EFEActiveInferencePlan`, `ResourceBudget`.
- **Primary Mechanism:** `FourteenLayerEntrepreneurialEngine` and `EntrepreneurialIntelligenceOrchestrator`.
- **Flow Description:**
  1. Layer 2 compiles opportunity anomalies into a directed acyclic graph (DAG) of execution steps.
  2. Active Inference Expected Free Energy (EFE) ranks task priorities.
  3. The compiled DAG is submitted to Layer 3 `HiveMind` for token auctioning and swarm agent distribution.

### 2.3 Layer 3 $\rightarrow$ Layer 4 (Intelligence to World Model Handoff)
- **Data Payload:** `ActionObservationPair`, `TrajectoryRecord`, `SkillExecutionEvent`.
- **Primary Mechanism:** `SkillsRunner` and `WorldModelCoordinator`.
- **Flow Description:**
  1. Layer 3 workers execute subtasks using Graph-of-Thought reasoning and tool invocation.
  2. Execution outcomes (success/failure, execution latency, environment observations) emit events to Layer 4.
  3. Layer 4 `WorldModel` ingests observations, performs recursive Bayesian belief propagation, and updates causal edges in the World Graph.

### 2.4 Layer 4 $\rightarrow$ Layer 1–3 (World Model Feedback Loop)
- **Data Payload:** `RealityStateUpdate`, `BeliefUncertaintySignal`, `PolicyViolationNotice`.
- **Primary Mechanism:** `EventBus` and `BayesianBeliefEngine`.
- **Flow Description:**
  1. High epistemic uncertainty in Layer 4 triggers Layer 1 Research OS to formulate new research queries.
  2. Pragmatic shift signals in Layer 4 trigger Layer 2 EOS Engine to adapt market positioning or capital allocation.
  3. Safety/Governance blocks in Layer 4 halt active worker tasks in Layer 3 AEAN.

---

## 3. Explicit Interface Contracts & Schema Mapping

| Interface Name | Source Module | Target Module | Data Schema |
| :--- | :--- | :--- | :--- |
| `HypothesisExport` | `apodex.ai_eos.research.research_os` | `apodex.arcs.kernel.kernel` | `HypothesisNode(id, confidence, p_value)` |
| `EOSPromotion` | `apodex.ai_eos.research.research_os` | `apodex.ai_eos.intelligence.eos_engine` | `OpportunityNode(id, expected_value, risk)` |
| `DAGDispatch` | `apodex.arcs.kernel.kernel` | `apodex.aean.coordination.hive_mind` | `TaskDAG(nodes, edges, total_budget)` |
| `WorldModelObservation` | `agent_harness.core.runtime` | `apodex.world_model.domain` | `ObservationEvent(entity_id, delta, timestamp)` |
| `SkillRegistration` | `apodex.aean.coordination` | `apodex.skills.runner` | `SkillDefinition(name, schema, python_fn)` |

---

## 4. Subsystem Dependency Isolation Rules

1. **No Circular Import Dependencies:** Layer 1 must never import modules from Layer 2, 3, or 4 directly. Communication upwards is exclusively via event pub/sub or registered bridge interfaces (`ResearchToSystemBridge`).
2. **Canonical State Ownership:** World state resides strictly in Layer 4 (`apodex.world_model`). Intermediate agent task states reside in Layer 3 (`agent_harness`). Strategic company stage states reside in Layer 2 (`apodex.ai_eos`). Research DB state resides in Layer 1 (`docs/research/papers/`).
3. **Strict Type Safety:** All inter-layer messages must be validated using Pydantic V2 models (`pydantic.BaseModel` with `ConfigDict(arbitrary_types_allowed=True)`).
