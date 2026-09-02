# Unified Dependency Graph & Inter-Layer Interaction Specification

## 1. Top-Level Module Dependency Topology

The unified APODEX platform enforces a strictly layered dependency graph. Dependencies flow strictly downwards or across explicitly defined cross-layer integration bridges (`ResearchToSystemBridge`).

```
+-------------------------------------------------------------------------------+
| LAYER 1: Research OS                                                          |
| apodex.ai_eos.research -> [research_os.py, integration.py]                    |
| apodex.research_os   -> [statistical_validation.py, reproducibility.py]     |
+-------------------------------------------------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| LAYER 2: EIOS / EOS                                                           |
| apodex.arcs.kernel   -> [kernel.py (EIOS Kernel)]                             |
| apodex.ai_eos.intelligence -> [eos_engine.py, fourteen_layer_engine.py]       |
+-------------------------------------------------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| LAYER 3: AEAN                                                                 |
| apodex.aean          -> [hive_mind.py, swarm.py, map_elites.py]               |
| apodex.memory        -> [cmos.py, semantic_memory.py]                         |
| agent_harness        -> [core.runtime.orchestration, core.runtime.reasoning] |
+-------------------------------------------------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| LAYER 4: APODEX Platform                                                      |
| apodex.world_model   -> [world_model.py, domain/entities.py, beliefs.py]      |
| apodex.skills        -> [runner.py, registry.py]                              |
| apodex.governance    -> [approval.py, cost_tier.py]                           |
+-------------------------------------------------------------------------------+
```

---

## 2. Cross-Layer State Handoff Sequence Diagram

```
Layer 1: ResearchOS       Layer 2: EIOS/EOS        Layer 3: AEAN HiveMind    Layer 4: APODEX WorldModel
       |                         |                          |                            |
       |-- Conduct Literature -->|                          |                            |
       |   Review (500 papers)   |                          |                            |
       |                         |                          |                            |
       |-- Validate Hypothesis ->|                          |                            |
       |   (E-Value > threshold) |                          |                            |
       |                         |-- Sense Opportunity ---->|                            |
       |                         |   via Active Inference   |                            |
       |                         |   Minimizing EFE         |                            |
       |                         |                          |-- Token Bidding ---------->|
       |                         |                          |   Task Dispatch &          |
       |                         |                          |   Swarm Consensus          |
       |                         |                          |                            |-- Execute Skill Protocol
       |                         |                          |                            |   Update Causal Beliefs
       |                         |                          |<-- Executed State Event ---|
       |<------------------------ Feedback Telemetry Loop -------------------------------|
```

---

## 3. Explicit Interface Protocols & Call Signature Contracts

### Protocol 1: Layer 1 to Layer 2 (Scientific Hypothesis Promotion)
- **Sender**: `apodex.ai_eos.research.research_os.ResearchOS`
- **Receiver**: `apodex.arcs.kernel.EIOSKernel` / `apodex.ai_eos.intelligence.eos_engine.EOSEngine`
- **Bridge**: `apodex.ai_eos.research.integration.ResearchToSystemBridge.export_hypothesis_to_kernel`
- **Payload Schema**:
  ```python
  class ValidatedHypothesisPayload(BaseModel):
      hypothesis_id: str
      title: str
      e_value: float
      statistical_power: float
      domain: str
      recommended_action: Dict[str, Any]
  ```

### Protocol 2: Layer 2 to Layer 3 (Opportunity Task Dispatch)
- **Sender**: `apodex.ai_eos.intelligence.eos_engine.EOSEngine`
- **Receiver**: `apodex.aean.coordination.hive_mind.HiveMind`
- **Payload Schema**:
  ```python
  class OpportunityTaskPayload(BaseModel):
      opportunity_id: str
      efe_score: float
      required_capabilities: List[str]
      budget_tokens: int
      execution_dag: Dict[str, Any]
  ```

### Protocol 3: Layer 3 to Layer 4 (Multi-Agent Skill Protocol Execution)
- **Sender**: `apodex.aean.coordination.hive_mind.HiveMind`
- **Receiver**: `apodex.skills.runner.SkillRunner` & `apodex.world_model.world_model.WorldModel`
- **Payload Schema**:
  ```python
  class SkillExecutionPayload(BaseModel):
      task_id: str
      winning_agent_id: str
      skill_name: str
      input_parameters: Dict[str, Any]
      governance_approval_token: str
  ```

### Protocol 4: Layer 4 to Layer 1 (Empirical Verification Telemetry Loop)
- **Sender**: `apodex.world_model.world_model.WorldModel`
- **Receiver**: `apodex.ai_eos.research.research_os.ResearchOS`
- **Payload Schema**:
  ```python
  class TelemetryFeedbackPayload(BaseModel):
      execution_id: str
      observed_outcome: Dict[str, Any]
      delta_kl_divergence: float
      timestamp: str
  ```

---

## 4. Elimination of Legacy Architectural Duplication

By enforcing this 4-layer dependency graph:
1. **Logical Duplication Removed**: Single canonical implementation for Planners, Memory (CMOS), World Model, and Schedulers.
2. **Adapter Wrapping Standardized**: Legacy `agent_harness` modules function exclusively as Layer 3 worker orchestration adapters under AEAN HiveMind.
3. **Circular Dependencies Prevented**: Static analysis and strict layer boundary checks prevent circular imports between Research OS, EIOS, EOS, AEAN, and APODEX.
