# UNIFIED DEPENDENCY GRAPH & INTERFACE PROTOCOLS

## Directed Layer Dependency Graph

The Unified Cognitive Operating System enforces a strict acyclic dependency flow from upper research abstraction layers to lower decision and substrate execution layers. Circular dependencies across layers are strictly prohibited.

```
                   +-----------------------------------+
                   |       LAYER 1: RESEARCH OS        |
                   | (Hypothesis Synthesis & Discovery)|
                   +-----------------------------------+
                                     |
                                     | Validated Hypotheses & Extracted Principles
                                     v
                   +-----------------------------------+
                   |       LAYER 2: EIOS / EOS         |
                   | (Sensing, EFE & DAG Orchestration)|
                   +-----------------------------------+
                                     |
                                     | Execution DAGs & Opportunity Bids
                                     v
                   +-----------------------------------+
                   |          LAYER 3: AEAN            |
                   | (Swarm Bidding & Code Mutation)   |
                   +-----------------------------------+
                                     |
                                     | Action Signals & Outcome Telemetry
                                     v
                   +-----------------------------------+
                   |         LAYER 4: APODEX           |
                   | (World State, Causality & Beliefs)|
                   +-----------------------------------+
```

---

## Interface Contracts & Handoff Protocols

### 1. Research OS -> EIOS / EOS Interface
* **Method**: `EIOSKernel.register_research_hypothesis(hypothesis_dict: Dict[str, Any])`
* **Payload Structure**:
  ```python
  {
      "hypothesis_id": "HYP-2026-001",
      "statement": "Non-Gaussian Hawkes point processes improve task scheduling latency.",
      "confidence_score": 0.94,
      "p_value": 0.001,
      "extracted_principles": ["P-402", "P-408"],
      "status": "validated"
  }
  ```

### 2. EIOS / EOS -> AEAN Interface
* **Method**: `HiveMind.register_research_insight(insight_dict: Dict[str, Any])`
* **Payload Structure**:
  ```python
  {
      "insight_id": "INS-802",
      "title": "Adaptive EFE Routing Engine",
      "target_subsystem": "AEAN",
      "bidding_budget": 100.0,
      "required_capabilities": ["coder", "critic"]
  }
  ```

### 3. AEAN -> APODEX WorldModel Interface
* **Methods**:
  * `WorldModel.create_node(node_id: str, label: str, node_type: str, properties: Dict[str, Any])`
  * `WorldModel.update_belief(node_id: str, new_belief: float, evidence_weight: float)`
* **Payload Structure**:
  ```python
  {
      "node_id": "NODE-AEAN-EXEC-99",
      "label": "Code Mutation Verification",
      "node_type": "causal_action",
      "properties": {"mutated_file": "apodex/ai_eos/research/integration.py"},
      "belief_delta": +0.12
  }
  ```

### 4. Cross-Layer Orchestration Bridge
* **Component**: `ResearchToSystemBridge` in `apodex/ai_eos/research/integration.py`
* **Role**: Orchestrates end-to-end multi-layer active inference handoffs in a single atomic transaction without introducing circular dependencies.
