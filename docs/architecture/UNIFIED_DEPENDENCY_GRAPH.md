# Unified Cognitive Architecture Dependency Graph

```
+-----------------------------------------------------------------------------------+
| LAYER 4: APODEX (Decision & World Modeling)                                        |
| Modules: apodex.world_model.WorldModel, CausalEngine, ActiveInferencePlanner     |
+-----------------------------------------------------------------------------------+
       | ^                                                            ^ |
       | | Causal Interventions & EFE Utility                         | | Bayesian Belief Updates
       v |                                                            | v
+-----------------------------------------------------------------------------------+
| LAYER 3: AEAN (Cognitive Intelligence & Multi-Agent Orchestration)               |
| Modules: apodex.aean.coordination.HiveMind, SemanticMemory, CodeRewriteEngine     |
+-----------------------------------------------------------------------------------+
       | ^                                                            ^ |
       | | Agent Execution Logs & Refactored ASTs                     | | Swarm Bidding & Strategy
       v |                                                            | v
+-----------------------------------------------------------------------------------+
| LAYER 2: EIOS / EOS (Execution, Resource Scheduling & Capital Engine)              |
| Modules: apodex.arcs.kernel.EIOSKernel, apodex.ai_eos.intelligence.EOSEngine     |
+-----------------------------------------------------------------------------------+
       | ^                                                            ^ |
       | | Execution DAG Status & Anomaly Signals                      | | Hypothesis Ingestion & Proofs
       v |                                                            | v
+-----------------------------------------------------------------------------------+
| LAYER 1: RESEARCH OS (Research, Empirical Discovery & Hypothesis Engine)          |
| Modules: apodex.ai_eos.research.ResearchOS, LiteratureExtractor, Integration      |
+-----------------------------------------------------------------------------------+
```

## Data Flow Protocol & Interface Contracts

### 1. Layer 1 -> Layer 2 Handshake Protocol
- **Interface:** `ResearchOS.export_hypotheses()` -> `EOSEngine.ingest_validated_research()`
- **Payload Schema:** `Hypothesis(id, title, status='validated', confidence_score, transferable_principles)`
- **Guarantee:** At most once delivery with formal schema validation; only hypotheses exceeding statistical significance threshold $p < 0.01$ are forwarded.

### 2. Layer 2 -> Layer 3 Handshake Protocol
- **Interface:** `EIOSKernel.schedule_dag()` -> `HiveMind.submit_task_auction()`
- **Payload Schema:** `DAGNode(node_id, capability_requirement, expected_latency, resource_budget)`
- **Guarantee:** Second-price auction guarantees optimal agent assignment within $\Delta t < 50\text{ms}$.

### 3. Layer 3 -> Layer 4 Handshake Protocol
- **Interface:** `HiveMind.publish_execution_result()` -> `WorldModel.update_belief()`
- **Payload Schema:** `ExecutionObservation(agent_id, task_id, output, actual_cost, runtime, metric_deltas)`
- **Guarantee:** Asynchronous Bayesian belief update ensuring non-blocking real-time agent execution.

### 4. Layer 4 -> Layer 1/2/3 Control Loop (Active Inference Signals)
- **Interface:** `WorldModel.calculate_efe()` -> `ResearchToSystemBridge.distribute_active_inference_signals()`
- **Payload Schema:** `EFESignal(target_layer, uncertainty_vector, target_hypothesis_id, risk_bound)`
- **Guarantee:** Directs exploratory literature discovery in Layer 1 and execution risk bounds in Layers 2 and 3.
