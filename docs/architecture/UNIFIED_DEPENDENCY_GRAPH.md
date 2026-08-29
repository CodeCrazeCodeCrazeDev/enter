# Unified Cognitive Operating System Dependency Graph

## 1. Directed Acyclic Graph (DAG) Structure

The Cognitive OS architecture operates as a strict top-down execution flow with bottom-up state and telemetry feedback. Subsystem dependencies are strictly directed to prevent circular imports, deadlock conditions, or state pollution.

```
                    +------------------------------------------+
                    | LAYER 1: RESEARCH OS (Scientific)        |
                    | - ResearchOS                             |
                    | - ResearchToSystemBridge                 |
                    +------------------------------------------+
                                         |
                                         | Exports Validated Hypotheses (p < 0.05, DSR > 1.0)
                                         v
                    +------------------------------------------+
                    | LAYER 2: EIOS / EOS LAYER (Orchestration)|
                    | - EIOSKernel                             |
                    | - EOSEngine                              |
                    | - FourteenLayerEngine                    |
                    +------------------------------------------+
                                         |
                                         | Dispatches Strategic Goals & EFE Targets
                                         v
                    +------------------------------------------+
                    | LAYER 3: AEAN LAYER (Cognitive Swarm)     |
                    | - HiveMind / Swarm Debate                |
                    | - PlannerExecutor (GoT Engine)           |
                    | - ActiveLearningEngine                   |
                    +------------------------------------------+
                                         |
                                         | Issues Skill Dispatches & Tool Call Requests
                                         v
                    +------------------------------------------+
                    | LAYER 4: APODEX LAYER (Platform Exec)    |
                    | - SkillRegistry (60+ Production Skills)  |
                    | - WorldModel (Causal Node Network)       |
                    | - Tiered Governance & Safety Gateways    |
                    +------------------------------------------+
                                         |
                                         | Real-Time Observation Stream & Bayesian State Feedback
                                         +--------------------------------------------+
                                                                                      |
                                                                                      v
                                                             (Feeds back into Layers 1, 2 & 3)
```

---

## 2. Explicit Subsystem Interfaces & Data Contracts

### Interface Contract 1: Layer 1 -> Layer 2 (`ResearchToSystemBridge`)
* **Source**: `apodex.ai_eos.research.research_os.ResearchOS`
* **Destination**: `apodex.arcs.kernel.kernel.EIOSKernel` & `apodex.ai_eos.intelligence.eos_engine.EOSEngine`
* **Data Contract**:
  ```python
  class ValidatedHypothesis(BaseModel):
      hypothesis_id: str
      domain: str
      statement: str
      p_value: float          # Required: p_value < 0.05
      deflated_sharpe: float # Required: DSR > 1.0
      statistical_power: float
      supporting_paper_ids: List[int]
      expected_free_energy_impact: float
  ```
* **Event Topic**: `research.hypothesis.validated`

### Interface Contract 2: Layer 2 -> Layer 3 (`ActiveInferenceDispatcher`)
* **Source**: `apodex.arcs.kernel.kernel.EIOSKernel`
* **Destination**: `agent_harness.core.runtime.orchestration.planner_executor.PlannerExecutor`
* **Data Contract**:
  ```python
  class ExecutionGoal(BaseModel):
      goal_id: str
      hypothesis_id: str
      target_outcome: Dict[str, Any]
      expected_free_energy: float
      epistemic_weight: float
      pragmatic_weight: float
      complexity_budget: float
  ```
* **Event Topic**: `eios.goal.dispatched`

### Interface Contract 3: Layer 3 -> Layer 4 (`SkillDispatcher`)
* **Source**: `apodex.planning.planner_executor.PlannerExecutor` / `agent_harness`
* **Destination**: `apodex.skills.registry.SkillRegistry`
* **Data Contract**:
  ```python
  class SkillInvocation(BaseModel):
      invocation_id: str
      skill_name: str
      parameters: Dict[str, Any]
      requesting_agent_id: str
      cost_budget: float
  ```
* **Event Topic**: `aean.skill.invoke`

### Interface Contract 4: Layer 4 -> Layers 1–3 (`WorldStatePublisher`)
* **Source**: `apodex.world_model.world_model.WorldModel`
* **Destination**: Event Bus (`apodex.ai_eos.infrastructure.event_bus`)
* **Data Contract**:
  ```python
  class WorldStateUpdatedEvent(BaseModel):
      event_id: str
      node_id: str
      updated_beliefs: Dict[str, float]
      observed_evidence: Dict[str, Any]
      timestamp: datetime
  ```
* **Event Topic**: `world_model.state.updated`

---

## 3. Module Dependency Matrix & Non-Circularity Verification

| Module Path | Allowed Imports | Forbidden Imports | Enforcement Mechanism |
| :--- | :--- | :--- | :--- |
| `apodex/ai_eos/research/` (L1) | Base Python, `pydantic`, `numpy`, `scipy` | `apodex/arcs/`, `apodex/aean/`, `apodex/skills/` | Pre-commit static import graph checking |
| `apodex/arcs/`, `apodex/ai_eos/intelligence/` (L2) | Layer 1 modules, Base Python | `apodex/aean/`, `apodex/skills/` | Strict boundary isolation in `integration.py` |
| `apodex/aean/`, `agent_harness/` (L3) | Layer 1 & 2 modules, Base Python | Direct execution layer code outside interfaces | Modular interface abstraction |
| `apodex/skills/`, `apodex/world_model/` (L4) | All lower layers (as contracts) | Direct modification of Layer 1/2 state | Event-driven pub/sub architecture |

This dependency structure guarantees zero cyclic imports, modular reusability, and clean test isolation across the entire codebase.
