# Cognitive OS Directed Dependency Graph

## 1. Top-Down Decoupled Dependency Topology

To eliminate circular dependencies and architectural duplication, the system strictly enforces a Directed Acyclic Graph (DAG) dependency flow across all four primary cognitive layers:

```
[Layer 1: Research OS]
       |
       v
[Layer 2: AEAN Swarm]
       |
       v
[Layer 3: EIOS / EOS]
       |
       v
[Layer 4: APODEX Execution & Harness]
```

### Invariant Rules:
1. **Strict Downward Flow**: Higher layers may import and call lower layers; lower layers MUST NEVER import from higher layers.
2. **Zero Lateral Import Cycles**: Modules within the same layer interact via event buses or abstraction protocols, avoiding tight cross-file couplings.
3. **Root Compatibility Adapter Isolation**: The `agent_harness` module acts purely as a backward-compatibility runtime adapter for tests and external runners. Core `apodex` logic does not depend on `agent_harness`.

---

## 2. Explicit Data Contracts & Communication Protocols

### Data Contract A: Research OS -> AEAN Swarm
* **Data Contract Structure**: `HypothesisRecord`
  - `hypothesis_id`: UUID
  - `paper_provenance`: List[str] (e.g. `["Paper #142", "Paper #188"]`)
  - `causal_intervention`: Dict[str, float]
  - `expected_free_energy_delta`: float
  - `p_value`: float

### Data Contract B: AEAN Swarm -> EIOS / EOS Loop
* **Data Contract Structure**: `SwarmConsensusDirective`
  - `directive_id`: UUID
  - `hypothesis_ref`: UUID
  - `active_inference_efe`: float
  - `bayesian_nash_price`: float
  - `policy_action`: str
  - `confidence_score`: float

### Data Contract C: EIOS / EOS Loop -> APODEX Engine
* **Data Contract Structure**: `ExecutionTaskDirective`
  - `task_id`: UUID
  - `loop_source`: str (e.g. `"CapitalAllocationLoop"`)
  - `skill_id`: str (e.g. `"allocate_capital_opportunity"`)
  - `payload`: Dict[str, Any]
  - `governance_verified`: bool
  - `rollback_checkpoint`: str

---

## 3. Import Restriction Matrix

| Subsystem Package | May Import From | Forbidden Imports |
| :--- | :--- | :--- |
| `apodex/ai_eos/research` | Standard Lib, NumPy, SciPy | `aean`, `arcs`, `skills`, `agent_harness` |
| `apodex/aean` | `ai_eos/research`, Standard Lib | `arcs`, `skills`, `agent_harness` |
| `apodex/arcs` | `aean`, `ai_eos/research`, Standard Lib | `skills`, `agent_harness` |
| `apodex/skills` & `memory` | `arcs`, `aean`, `ai_eos/research`, Standard Lib | `agent_harness` |
