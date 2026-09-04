# Unified Cognitive Operating System Dependency Graph

## Subsystem Layer Topology & Data Flow

```
+---------------------------------------------------------------------------------+
|                       LAYER 1: RESEARCH OS (Research)                           |
|                       - ResearchOS Literature Engine                            |
|                       - Reproducibility & Statistical Validator                 |
+---------------------------------------------------------------------------------+
           |                                             |
           | export_validated_hypothesis_to_kernel()      | promote_hypothesis_to_eos()
           v                                             v
+-------------------------------------+     +-------------------------------------+
|      LAYER 2a: EIOS KERNEL          |     |       LAYER 2b: EOS ENGINE          |
|  - Anomaly Sensing & EFE Routing    |     | - 11-Section EOS State Machine      |
|  - Active Inference Hypotheses      |     | - 14-Layer CAE Execution Engine     |
+-------------------------------------+     +-------------------------------------+
           |                                             |
           | sense_opportunity_anomalies()              | compile_opportunity_dag()
           +------------------------------+--------------+
                                          |
                                          v
+---------------------------------------------------------------------------------+
|                         LAYER 3: AEAN (Intelligence)                            |
|                         - HiveMind Task Bidding Engine                          |
|                         - GeneticWorkflowOptimizer & Hawkes Gates               |
+---------------------------------------------------------------------------------+
                                          |
                                          | dispatch_strategy_execution()
                                          v
+---------------------------------------------------------------------------------+
|                         LAYER 4: APODEX (Platform)                              |
|                         - WorldModel Causal Graph & Belief Propagation          |
|                         - Protocol Execution & Skill Registry Flywheel          |
+---------------------------------------------------------------------------------+
```

---

## Direct Call Interfaces

1. **Layer 1 -> Layer 2 Sync**:
   - `ResearchOS.export_validated_hypothesis_to_kernel(hypothesis_id, kernel_instance)`: Ingests validated scientific hypotheses directly into EIOS Active Inference sensing engine.
   - `ResearchOS.promote_hypothesis_to_eos(hypothesis_id, eos_instance)`: Ingests verified strategic insights into the EOS decision tree.

2. **Layer 2 -> Layer 3 Sync**:
   - `EIOSKernel.sense_opportunity_anomalies(market_signals)`: Computes Expected Free Energy (EFE) across research hypotheses and generates market anomaly task candidates.
   - `FirstPrinciplesEOSEngine.compile_opportunity_dag(opportunity_id)`: Transforms business opportunities into a multi-agent execution DAG.

3. **Layer 3 -> Layer 4 Sync**:
   - `HiveMind.dispatch_strategy_execution(task_dag, agent_bids)`: Allocates execution nodes to specialized agents and dispatches actions to APODEX platform handlers.
   - `SkillRegistry.execute_skill(skill_id, params)` & `ProtocolLoader.run_protocol(protocol_id)`: Runs deterministic software and business actions, emitting state update events back to `WorldModel`.

4. **Layer 4 -> Layer 1/2/3 Feedback Loop**:
   - `WorldModel.update_entity()` and `WorldModel.propagate_bayesian_belief()` update global world state beliefs, providing sensory observations back to Layer 2 Active Inference and empirical outcomes to Layer 1 Research OS.
