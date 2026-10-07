# Unified Dependency Graph & Interface Contracts Specification

## Overview

This document specifies the exact dependency topology, data flows, event contracts, and interface definitions connecting the four layers of the Unified Cognitive Operating System (**Research OS**, **EIOS Kernel / EOS Engine**, **AEAN HiveMind**, and **APODEX WorldModel**).

---

## 1. Unified Subsystem Dependency Graph

```
                   +---------------------------------------+
                   |       Layer 1: Research OS            |
                   |  (Hypothesis Discovery & Validation)  |
                   +---------------------------------------+
                                   │         ▲
             Validated Hypothesis  │         │ Active Inference
                   Handoff         │         │ Empirical Feedback
                                   ▼         │
                   +---------------------------------------+
                   |       Layer 2: EIOS / EOS             |
                   |  (Sensing, EFE Scheduling, Growth)    |
                   +---------------------------------------+
                                   │         ▲
              Execution DAG /      │         │ Agent Bids &
              Opportunity Task     │         │ Performance Signals
                                   ▼         │
                   +---------------------------------------+
                   |       Layer 3: AEAN HiveMind          |
                   |  (Multi-Agent Bidding & Evolution)    |
                   +---------------------------------------+
                                   │         ▲
               Action Execution    │         │ Causal State &
               & Code Patch        │         │ Belief Probability
                                   ▼         │
                   +---------------------------------------+
                   |    Layer 4: APODEX WorldModel         |
                   |  (Causal Indexing & Bayesian Updates) |
                   +---------------------------------------+
```

---

## 2. Cross-Layer Interface Contracts & Data DTOs

### Interface 1: Layer 1 $\to$ Layer 2 (Hypothesis Registration)
* **Bridge Method**: `EIOSKernel.register_research_hypothesis(hypothesis)`
* **Data Transfer Object**:
```python
class ResearchHypothesisDTO:
    hypothesis_id: str
    title: str
    paper_citations: list[str]
    p_value: float
    effect_size: float
    target_subsystem: str  # "EIOS", "EOS", "AEAN", "APODEX"
    extracted_principle: str
    implementation_module: str
    status: str  # "validated", "active"
```

### Interface 2: Layer 2 $\to$ Layer 3 (Task Delegation & Bidding)
* **Bridge Method**: `HiveMind.register_research_insight(insight)` / `HiveMind.submit_task_for_bidding(task)`
* **Data Transfer Object**:
```python
class TaskBiddingDTO:
    task_id: str
    hypothesis_id: str
    required_capabilities: list[str]
    budget_tokens: float
    expected_free_energy: float
    deadline_timestamp: float
```

### Interface 3: Layer 3 $\to$ Layer 4 (World Model Belief & Entity Update)
* **Bridge Method**: `WorldModel.update_belief(node_id, new_probability)` / `WorldModel.create_node(node)`
* **Data Transfer Object**:
```python
class WorldModelUpdateDTO:
    node_id: str
    entity_type: str  # "hypothesis", "opportunity", "agent_strategy"
    prior_probability: float
    posterior_probability: float
    evidence_payload: dict
    causal_relationships: list[str]
```

### Interface 4: Layer 4 $\to$ Layer 1 (Active Inference State Handoff)
* **Bridge Method**: `ResearchToSystemBridge.orchestrate_closed_loop_cycle(hypothesis, context)`
* **Data Transfer Object**:
```python
class SystemStateHandoffDTO:
    cycle_id: str
    research_hypothesis_id: str
    eios_opportunity_id: str
    aean_winning_agent_id: str
    world_model_updated_node_id: str
    belief_posterior: float
    execution_success: bool
```

---

## 3. Python Module Binding Matrix

| Source Layer | Target Layer | Module Binding | Interface Class / Protocol |
|---|---|---|---|
| Layer 1 (Research OS) | Layer 2 (EIOS/EOS) | `apodex.ai_eos.research.integration` | `ResearchToSystemBridge` |
| Layer 1 (Research OS) | Layer 2 (EIOS) | `apodex.arcs.kernel.kernel` | `EIOSKernel.register_research_hypothesis` |
| Layer 2 (EOS Engine) | Layer 1 (Research OS) | `apodex.ai_eos.intelligence.eos_engine` | `EOSEngine.ingest_validated_research` |
| Layer 2 (EIOS/EOS) | Layer 3 (AEAN) | `apodex.aean.coordination.hive_mind` | `HiveMind.register_research_insight` |
| Layer 3 (AEAN) | Layer 4 (APODEX) | `apodex.world_model.world_model` | `WorldModel.create_node` & `update_belief` |
| Layer 4 (APODEX) | Layer 1/2/3 | `apodex.cognition.brain` | `CognitiveBrain.process_sensory_input` |

---

## 4. Elimination of Duplicate Responsibilities

1. **Hypothesis Generation**: Exclusively owned by **Layer 1 (Research OS)**. AEAN and EIOS consume hypotheses; they do not generate literature hypotheses.
2. **Execution Scheduling & Sensing**: Exclusively owned by **Layer 2 (EIOS Kernel & EOS Engine)**. Research OS does not schedule DAG tasks.
3. **Multi-Agent Auction & Strategy**: Exclusively owned by **Layer 3 (AEAN HiveMind)**. WorldModel does not run task bidding auctions.
4. **Causal Graph & Belief Updating**: Exclusively owned by **Layer 4 (APODEX WorldModel)**. Individual agents in AEAN query WorldModel for causal context rather than maintaining duplicate local graphs.
