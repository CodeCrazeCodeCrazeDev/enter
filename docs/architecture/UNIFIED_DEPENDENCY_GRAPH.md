# Unified Dependency Graph Specification

## Unidirectional Cross-Layer Dependency Topology

```
+-----------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS (Research Layer)                      |
|                  apodex/ai_eos/research/ | apodex/research_os/                    |
+-----------------------------------------------------------------------------------+
                                          |
                                          | ValidatedHypothesis / EmpiricalPrinciple
                                          v
+-----------------------------------------------------------------------------------+
|                   LAYER 2: EIOS / EOS (Execution & Orchestration)                 |
|                  apodex/arcs/kernel/ | apodex/ai_eos/intelligence/                |
+-----------------------------------------------------------------------------------+
                                          |
                                          | TaskDAGNode / OperationalOpportunity
                                          v
+-----------------------------------------------------------------------------------+
|                 LAYER 3: AEAN (Cognitive Intelligence Layer)                       |
|                  apodex/aean/ | apodex/orchestration/ | apodex/reasoning/         |
+-----------------------------------------------------------------------------------+
                                          |
                                          | ProtocolExecutionRequest / ActionTrajectory
                                          v
+-----------------------------------------------------------------------------------+
|                 LAYER 4: APODEX (Decision & Execution Platform Layer)             |
|                  apodex/world_model/ | apodex/skills/ | apodex/governance/          |
+-----------------------------------------------------------------------------------+
```

---

## Direct Interface Definitions

### 1. Layer 1 -> Layer 2 (`ResearchToSystemBridge`)
* **Interface Method**: `ResearchOS.export_validated_hypothesis_to_kernel(hypothesis_id)`
* **Data Payload**:
  ```python
  class ValidatedHypothesis(BaseModel):
      hypothesis_id: str
      title: str
      confidence_score: float  # e.g., p-value < 0.05
      transferable_principle: str
      target_subsystem: str  # "EIOS", "EOS", "AEAN", "APODEX"
  ```

### 2. Layer 2 -> Layer 3 (`EOS-to-HiveMind Bridge`)
* **Interface Method**: `EOSEngine.dispatch_opportunity_dag(opportunity_id, task_dag)`
* **Data Payload**:
  ```python
  class TaskDAGNode(BaseModel):
      task_id: str
      required_capabilities: list[str]
      token_bidding_budget: float
      parent_task_ids: list[str]
      payload: dict
  ```

### 3. Layer 3 -> Layer 4 (`AEAN-to-APODEX Bridge`)
* **Interface Method**: `HiveMind.execute_skill_protocol(protocol_name, parameters)`
* **Data Payload**:
  ```python
  class ProtocolExecutionRequest(BaseModel):
      protocol_name: str
      executor_agent_id: str
      parameters: dict
      allocated_cost_budget: float
  ```

### 4. Layer 4 -> Layer 1 (`Observation Feedback Loop`)
* **Interface Method**: `WorldModel.publish_observation_residual(entity_id, residual_delta)`
* **Data Payload**:
  ```python
  class ObservationResidual(BaseModel):
      entity_id: str
      predicted_value: float
      observed_value: float
      residual_magnitude: float
  ```
