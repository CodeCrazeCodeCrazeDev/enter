# Unified Dependency Graph & Interface Specification

## 1. Overview & Handoff Principles

This document defines the strict directional dependencies, data flow pipelines, and typed execution contracts connecting Layer 1 (Research OS), Layer 2 (EIOS Sensing & EOS Strategy), Layer 3 (AEAN Multi-Agent Intelligence), and Layer 4 (APODEX WorldModel & Decision Substrate).

Cyclic dependencies between layers are strictly prohibited. Information flows strictly top-down for intent/strategy propagation and bottom-up for observation/state feedback.

---

## 2. Layer Dependency Hierarchy

```
[Layer 1: Research OS]
       │
       │ (1. Validated Hypotheses & Extracted Principles)
       ▼
[Layer 2: EIOS Sensing & EOS Engine]
       │
       │ (2. Strategic Directives & Entrepreneurial Goals)
       ▼
[Layer 3: AEAN Multi-Agent Coordination]
       │
       │ (3. Action Execution & Tool Invocations)
       ▼
[Layer 4: APODEX WorldModel & Governance]
       │
       └────► (4. Reality State Feedback & Updated Beliefs) ────► [Layer 1 & Layer 2]
```

---

## 3. Directional State Handoff Contracts

### 3.1 Layer 1 ➔ Layer 2 Contract (Research to Sensing & Strategy)
* **Method:** `ResearchOS.export_validated_hypothesis_to_kernel(hypothesis_id)` & `EOSEngine.ingest_validated_research(hypothesis)`
* **Payload:** `ResearchHypothesis`
  ```python
  class ResearchHypothesisPayload(BaseModel):
      hypothesis_id: str
      title: str
      extracted_principles: List[str]
      deflected_sharpe_ratio: float
      statistical_p_value: float
      is_reproducible: bool
  ```
* **Semantics:** Research OS verifies statistical validity (DSR > 0.95, $p < 0.05$). Only validated hypotheses are ingested by EIOS Kernel for Active Inference anomaly tracking and by EOS Engine for strategic loop formulation.

### 3.2 Layer 2 ➔ Layer 3 Contract (Strategy to Multi-Agent Execution)
* **Method:** `HiveMind.register_research_insight(insight_dict)` / `HiveMind.submit_task(task_spec)`
* **Payload:** `StrategicDirective`
  ```python
  class StrategicDirective(BaseModel):
      directive_id: str
      target_growth_stage: str
      customer_lifecycle_phase: str
      required_skills: List[str]
      expected_free_energy_threshold: float
      priority_score: float
  ```
* **Semantics:** EOS Engine translates business opportunities and growth bottlenecks into actionable multi-agent tasks. AEAN HiveMind auctions these tasks across registered agent roles based on skill match and token bids.

### 3.3 Layer 3 ➔ Layer 4 Contract (Multi-Agent Execution to WorldModel)
* **Method:** `WorldModel.apply_action(action_payload)`
* **Payload:** `ActionExecutionResult`
  ```python
  class ActionExecutionResult(BaseModel):
      action_id: str
      agent_id: str
      skill_name: str
      execution_trace: List[Dict[str, Any]]
      proposed_entity_changes: Dict[str, Any]
      status: str  # "SUCCESS", "FAILED", "BLOCKED"
  ```
* **Semantics:** AEAN agents execute tools and generate entity state updates. All proposed state mutations are passed to Layer 4 for safety compliance checking and atomic reality state commit.

### 3.4 Layer 4 ➔ Layer 1/2 Feedback Contract (Reality State Updates)
* **Method:** `WorldModel.publish_state_event(event)`
* **Payload:** `RealityStateUpdatedEvent`
  ```python
  class RealityStateUpdatedEvent(BaseModel):
      event_id: str
      entity_id: str
      updated_beliefs: Dict[str, float]
      timestamp: str
  ```
* **Semantics:** WorldModel updates Bayesian belief distributions ($P(B|O)$) and broadcasts state changes back to Layer 2 for continuous Active Inference model updating.

---

## 4. Subsystem Coupling Matrix

| Subsystem | Research OS | EIOS Kernel | EOS Engine | AEAN HiveMind | APODEX WorldModel |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Research OS** | Self | Consumer (Hypotheses) | Consumer (Hypotheses) | Indirect | Indirect |
| **EIOS Kernel** | Provider | Self | Peer (Sensing) | Consumer (Directives) | Indirect |
| **EOS Engine** | Provider | Peer (Sensing) | Self | Consumer (Directives) | Consumer (Beliefs) |
| **AEAN HiveMind** | Indirect | Provider | Provider | Self | Consumer (Actions) |
| **APODEX WorldModel** | Provider | Provider | Provider | Provider | Self |
