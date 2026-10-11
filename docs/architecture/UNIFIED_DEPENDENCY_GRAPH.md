# Unified Dependency Graph & Topology Architecture
## Structural Imports, Module Boundaries & Event Bus Interconnections

---

## 1. High-Level Topological Interconnection Graph

```
====================================================================================================
                                      [ USER / GOAL DIRECTIVE ]
                                                  |
                                                  v
+--------------------------------------------------------------------------------------------------+
| LAYER 1: RESEARCH OS (Scientific Research & Hypothesis Engine)                                   |
| Package: apodex.ai_eos.research, apodex.research_os                                              |
| Key Modules: research_os.py, integration.py, statistical_validation.py                           |
+--------------------------------------------------------------------------------------------------+
                                                  |  (Publishes Hypotheses & Research Principles)
                                                  v
+--------------------------------------------------------------------------------------------------+
| LAYER 2: EIOS / EOS (Execution, Orchestration & Venture Engine)                                  |
| Package: apodex.arcs.kernel, apodex.ai_eos.intelligence                                         |
| Key Modules: kernel.py, eos_engine.py, computational_architecture.py, fourteen_layer_engine.py    |
+--------------------------------------------------------------------------------------------------+
                                                  |  (Publishes Executable Workflow DAG Nodes)
                                                  v
+--------------------------------------------------------------------------------------------------+
| LAYER 3: AEAN (Autonomous Economic Agent Network)                                                |
| Package: apodex.aean.coordination, apodex.orchestration                                          |
| Key Modules: hive_mind.py, hierarchical.py, market_simulator.py                                  |
+--------------------------------------------------------------------------------------------------+
                                                  |  (Publishes Observation Events & Action Trajectories)
                                                  v
+--------------------------------------------------------------------------------------------------+
| LAYER 4: APODEX (World Model & Decision Substrate)                                               |
| Package: apodex.world_model, apodex.cognition, apodex.memory, apodex.governance                 |
| Key Modules: world_model.py, brain.py, domain/entities.py, beliefs.py, approval.py               |
+--------------------------------------------------------------------------------------------------+
                                                  |
                                                  |  (Asynchronous Feedback Loop / Belief Updates)
                                                  +-----------------+
                                                                    |
                                                                    v
                                                     [ LAYER 1: RESEARCH OS ]
====================================================================================================
```

---

## 2. Strict Package & Module Import Dependencies

To maintain absolute structural decoupling, imports across layers follow strict unidirectional rules:

```
+-------------------+
|  Layer 1 (Research|
+---------+---------+
          |  Imports
          v
+-------------------+      +-------------------+
|  Layer 2 (EIOS/EOS| <--- |  Layer 3 (AEAN)   |
+---------+---------+      +---------+---------+
          |                          |
          +------------+-------------+
                       |
                       v
            +--------------------+
            | Layer 4 (APODEX)   |
            +--------------------+
```

### Dependency Rules:
1. **Layer 4 (APODEX Substrate)** MUST NOT import from Layers 1, 2, or 3. It provides base domain entities, beliefs, memory, and causal models.
2. **Layer 3 (AEAN Network)** MAY import from Layer 4 for belief queries, but MUST NOT import from Layer 2 or Layer 1.
3. **Layer 2 (EIOS/EOS Engine)** MAY import from Layer 4 and Layer 3 interfaces.
4. **Layer 1 (Research OS)** MAY import from Layers 2, 3, and 4 to query execution status and update research hypotheses.
5. **Cross-Layer Orchestrator (`apodex.orchestration.unified_cognitive_os`)** sits above all 4 layers and orchestrates closed-loop active inference state handoffs without circular dependencies.

---

## 3. Event Bus Interconnection Protocols

Communication between decoupled modules is managed asynchronously over the **Unified Event Bus**:

| Event Type | Publisher Layer | Subscriber Layer(s) | Payload Content |
|---|---|---|---|
| `HypothesisRegisteredEvent` | Layer 1 (Research OS) | Layer 2 (EIOS/EOS) | Hypothesis ID, target domain, prior confidence, mathematical bounds |
| `OpportunitySensedEvent` | Layer 2 (EIOS/EOS) | Layer 3 (AEAN) | Opportunity ID, Expected Free Energy ($G$), workflow DAG nodes |
| `TaskBiddingCompletedEvent` | Layer 3 (AEAN) | Layer 2 & Layer 4 | Task ID, winning agent ID, bid amount, execution parameters |
| `ActionExecutedEvent` | Layer 3 (AEAN) | Layer 4 (APODEX) | Trajectory step, tool output, execution cost, duration |
| `BeliefUpdatedEvent` | Layer 4 (APODEX) | Layer 1 & Layer 2 | Variable ID, updated Beta $(\alpha, \beta)$ parameters, posterior mean/variance |
| `SafetyViolationTriggeredEvent` | Layer 4 (APODEX) | All Layers | Violation type, agent ID, blocked action, rollback checkpoint ID |

---

## 4. Database Schema & Persistence Topology

```
+---------------------------------------------------------------------------------+
| PRIMARY SQLITE / DATABASE STORE (apodex.db)                                    |
+---------------------------------------------------------------------------------+
  ├── research_hypotheses (Layer 1): id, paper_ref, title, status, p_value
  ├── execution_dags (Layer 2): dag_id, opportunity_id, nodes_json, efe_score
  ├── agent_bids (Layer 3): bid_id, task_id, agent_id, token_amount, score
  ├── causal_nodes (Layer 4): node_id, name, alpha, beta, updated_at
  ├── causal_edges (Layer 4): cause_id, effect_id, coefficient
  └── episodic_memory (Layer 4): step_id, action, params_json, outcome_json
```
