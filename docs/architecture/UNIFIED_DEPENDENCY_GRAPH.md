# UNIFIED DEPENDENCY GRAPH & INTERACTION SPECIFICATION
## Unified 4-Layer Cognitive Operating System

---

### Graphical System Architecture & Signal Flow

```
===================================================================================
                       LAYER 1: RESEARCH OS (Discovery)
-----------------------------------------------------------------------------------
 [ ResearchOS ]  <--->  [ 600-Paper Corpus ]
       |                   (Transferable Principles)
       |
       | 1. Ingest Validated Hypotheses & Active Research Insights
       v
===================================================================================
                       LAYER 2: EIOS / EOS (Orchestration)
-----------------------------------------------------------------------------------
 [ EOS First-Principles ]  <--->  [ EIOS Kernel ]
 (Continuous Sensing &             (Asynchronous DAG Compiler)
  Business Loops Engine)
       |
       | 2. Submit Execution Tasks & DAG Nodes
       v
===================================================================================
                       LAYER 3: AEAN (Cognitive Intelligence)
-----------------------------------------------------------------------------------
 [ HiveMind Bidding ]  <--->  [ Learnable Routing Dispatcher ]
       |                                   |
       v                                   v
 [ CodeRewriteEngine ]             [ Specialized Domain Agents ]
 (AST-Verified Rewriting)           (Cost/EFE-Optimized Workers)
       |
       | 3. Action Traces, State Changes & Executed Results
       v
===================================================================================
                       LAYER 4: APODEX (Decision & Platform)
-----------------------------------------------------------------------------------
 [ WorldModel Causal Graph ]  <--->  [ Recursive Bayesian Belief Engine ]
       |                                              |
       v                                              v
 [ Credit Halting Governance ]              [ Active Inference State ]
       |
       +==============================================+
         4. Bayesian Belief Updates & Info Gain Feedback
         (Closes Loop back to Layer 1 Research OS)
```

---

### Detailed Interface Call Graph

```
ResearchOS.register_hypothesis(title, description, null_hypothesis, target_metric)
  │
  ├─► ResearchOS.execute_experiment_simulation(experiment_id, ground_truth)
  │      │
  │      └─► Hypothesis.status = "validated" / "refuted"
  │
  └─► ResearchToSystemBridge.execute_cross_layer_cycle(hypothesis)
         │
         ├─► Layer 2: EOSEngine.ingest_validated_research(hypothesis)
         │            EIOSKernel.register_research_hypothesis(hypothesis_id, statement)
         │            EIOSKernel.execute_dag(tasks)
         │
         ├─► Layer 3: HiveMind.register_research_insight(task_id, confidence)
         │            HiveMind.arbitrate()
         │            LearnableRoutingGateDispatcher.route_task(complexity, domain)
         │
         └─► Layer 4: WorldModel.create_node(node_id, label, attributes)
                      WorldModel.update_belief(hypothesis_id, prior, likelihood)
```

---

### Component Interaction Matrix

| Source Layer | Target Layer | Mechanism / Method | Data Payload | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1 (ResearchOS)** | Layer 2 (EIOS/EOS) | `ingest_validated_research()` | Hypothesis ID, Title, Effect Size, P-value | Hands off verified insights for commercial execution |
| **Layer 2 (EIOS/EOS)** | Layer 3 (AEAN) | `register_research_insight()` | Task ID, Domain, Confidence, Token Budget | Submits executable tasks to multi-agent bidding registry |
| **Layer 3 (AEAN)** | Layer 4 (APODEX) | `create_node()` / `update_belief()` | Node ID, Causal Edges, Prior, Likelihood | Records state updates and causal interventions in World Model |
| **Layer 4 (APODEX)** | Layer 1 (ResearchOS) | `conduct_literature_review()` | Bayesian Belief, EFE Info Gain, White Space | Informs next-cycle research hypothesis generation |

---

### Coupling & Isolation Guarantees

1. **Unidirectional Control Flow**: Information and tasks flow strictly downwards from Layer 1 through Layer 4 during execution, while Bayesian belief and evaluation metrics flow upwards from Layer 4 back to Layer 1 to complete the active inference loop.
2. **Explicit Interfaces**: Subsystems do not access internal state variables of other layers directly. All state transitions pass through explicit bridge methods (`ResearchToSystemBridge`).
3. **Fail-Safe Isolation**: Faults in Layer 3 multi-agent execution are caught and handled by Layer 4 Credit Halting without corrupting Layer 1 research registries.
