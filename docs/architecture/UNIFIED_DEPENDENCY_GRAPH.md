# Unified Dependency Graph
**Subsystem Interaction and Data Flow Specification**

---

## Interactive Dependency Topology

The unified cognitive operating system enforces a strict unidirectional state and execution flow, accompanied by a bidirectional Active Inference feedback loop.

```
                          [ External Academic & Code Corpus ]
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS (Research Layer)                      |
|                                                                                   |
|  +-----------------------+     +-----------------------+     +-----------------+  |
|  | ResearchOS Literature | --> | StatisticalValidation | --> | CodeRewrite     |  |
|  | Synthesis & Principles |     | (DSR, White's Check)  |     | & Genetic Engine|  |
|  +-----------------------+     +-----------------------+     +-----------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                        Promoted Hypotheses & Code Proposals
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     LAYER 2: EIOS / EOS (Execution & Orchestration)               |
|                                                                                   |
|  +-----------------------+                                   +-----------------+  |
|  | EIOSKernel Sensing    | --------------------------------> | EOSEngine       |  |
|  | & Active Inference EFE|                                   | Entrepreneurial |  |
|  +-----------------------+                                   | State Machine   |  |
|              |                                               +-----------------+  |
|              v                                                        |           |
|  +-----------------------+                                            |           |
|  | DAG Task Compiler     | <------------------------------------------+           |
|  +-----------------------+                                                        |
+-----------------------------------------------------------------------------------+
                                          |
                           DAG Sub-Tasks & Priority Vectors
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     LAYER 3: AEAN (Cognitive Intelligence Layer)                  |
|                                                                                   |
|  +-----------------------+     +-----------------------+     +-----------------+  |
|  | HiveMind Token        | --> | Swarm Agent           | --> | Learnable Routing| |
|  | Bidding Registry      |     | Task Negotiation      |     | Gate Dispatcher | |
|  +-----------------------+     +-----------------------+     +-----------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                         Agent Assignment & Skill Execution Orders
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                  LAYER 4: APODEX (Decision & Execution Platform Layer)            |
|                                                                                   |
|  +-----------------------+     +-----------------------+     +-----------------+  |
|  | WorldModel Causal     | --> | Recursive Bayesian    | --> | Skills Runner   |  |
|  | Graph (CausalNodes)   |     | Belief Updating       |     | & GRC Governance|  |
|  +-----------------------+     +-----------------------+     +-----------------+  |
|                                            ^                                      |
|                                            |                                      |
|                            ResearchToSystemBridge Orchestration                   |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
                     System State Updates & Feedback Observations
                               (Fed back to Layers 1, 2, 3)
```

---

## Detailed Call Graph and Cross-Layer Handoff Contracts

### 1. Layer 1 -> Layer 2 Handoff
- **Caller:** `ResearchOS.execute_experiment_simulation`
- **Receiver:** `EOSEngine.ingest_validated_research` / `EIOSKernel.register_research_hypothesis`
- **Contract Data:** `Hypothesis` Pydantic model containing `hypothesis_id`, `status='validated'`, `effect_size`, `deflated_sharpe_ratio`, `p_value`.

### 2. Layer 2 -> Layer 3 Handoff
- **Caller:** `EIOSKernel.execute_dag` / `EOSEngine.evaluate_growth_milestones`
- **Receiver:** `HiveMind.submit_task_bid`
- **Contract Data:** Opportunity task dictionary with `task_id`, `complexity`, `required_domain`, `budget_tokens`, `reward_value`.

### 3. Layer 3 -> Layer 4 Handoff
- **Caller:** `LearnableRoutingGateDispatcher.route_task`
- **Receiver:** `WorldModel.create_node` & `SkillRunner.execute_protocol`
- **Contract Data:** `AgentAssignment` specifying `agent_id`, `skill_name`, `target_entity_id`, `efe_score`.

### 4. Layer 4 -> Layers 1-3 Feedback
- **Caller:** `ResearchToSystemBridge.execute_active_inference_handoff`
- **Receiver:** `WorldModel.update_belief` & Active Inference EFE sensors in Layers 1, 2, 3
- **Contract Data:** `BeliefUpdateResult` containing `node_id`, `prior_prob`, `posterior_prob`, `observation_surprise`.

---

## Module Import Hierarchy Standards

```
apodex/ai_eos/research/ (Layer 1)
   └── imports domain models, common utilities

apodex/arcs/kernel/ & apodex/ai_eos/intelligence/ (Layer 2)
   └── imports Layer 1 domain models (Hypothesis)

apodex/aean/ (Layer 3)
   └── imports Layer 1 & 2 models for bidding contracts

apodex/world_model/ & apodex/cognition/ (Layer 4)
   └── imports models from Layers 1, 2, 3 via ResearchToSystemBridge
```
