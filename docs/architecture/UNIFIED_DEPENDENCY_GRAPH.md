# Unified Dependency Graph and Interface Standard
**Version:** 2026.1.0
**Scope:** Architectural Hierarchy, Interface Contracts, and Dependency Enforcement

---

## 1. Architectural Hierarchy Graph

```
                   +---------------------------------------+
                   |          LAYER 1: RESEARCH OS         |
                   |   (Research & Hypothesis Engine)     |
                   +---------------------------------------+
                                       |
                                       | Imports / Invokes via Spec
                                       v
                   +---------------------------------------+
                   |             LAYER 2: AEAN             |
                   |    (Cognitive Intelligence Layer)     |
                   +---------------------------------------+
                                       |
                                       | Emits Decisions / Intent
                                       v
                   +---------------------------------------+
                   |          LAYER 3: EIOS / EOS          |
                   |   (Strategic Execution & Governance)  |
                   +---------------------------------------+
                                       |
                                       | Dispatches Actions
                                       v
                   +---------------------------------------+
                   |            LAYER 4: APODEX            |
                   |     (Skill, Memory, WMC Substrate)    |
                   +---------------------------------------+
```

---

## 2. Strict Architectural Invariants & Import Rules

1. **Strict Downward Dependency Rule:** Layer $N$ may import or call Layer $N+1$, $N+2$, or $N+3$. Lower layers (e.g. Layer 4 APODEX) MUST NEVER import or call higher layers (e.g. Layer 1 Research OS or Layer 2 AEAN).
2. **Zero Cross-Layer Duplication:**
   - Planning logic belongs exclusively to Layer 2 (`apodex.reasoning.got` / `apodex.planning`).
   - World Modeling belongs exclusively to Layer 4 (`apodex.world_model`).
   - Skill execution belongs exclusively to Layer 4 (`apodex.skills`).
3. **No Circular Imports:** Any import resulting in a cycle (detected via `scripts/validate_dependencies.py`) constitutes a build-blocking violation.
4. **Adapter Isolation:** Legacy compatibility modules under `agent_harness/` or `apodex/harness/` are shim adapters only and must delegate directly to canonical layer implementations.

---

## 3. Explicit Layer Interface Contracts

### Layer 1 -> Layer 2 Interface Contract
* **Producer:** `apodex.research_os.statistical_validation`, `apodex.ai_eos.research.experiment_framework`
* **Consumer:** `apodex.aean.coordination.hive_mind`
* **Data Contract:** `ExperimentRecord`, `HypothesisValidationResult`
* **Payload Structure:**
  ```python
  class HypothesisValidationResult(BaseModel):
      hypothesis_id: str
      p_value: float
      t_statistic: float
      is_significant: bool
      effect_size: float
      promoted_to_runtime: bool
  ```

### Layer 2 -> Layer 3 Interface Contract
* **Producer:** `apodex.aean.coordination.hive_mind`, `apodex.reasoning.got`
* **Consumer:** `apodex.arcs.kernel.kernel`
* **Data Contract:** `CognitivePlanDirective`
* **Payload Structure:**
  ```python
  class CognitivePlanDirective(BaseModel):
      plan_id: str
      selected_path: list[str]
      expected_free_energy: float
      causal_intervention: dict[str, Any]
      confidence_interval: tuple[float, float]
  ```

### Layer 3 -> Layer 4 Interface Contract
* **Producer:** `apodex.arcs.kernel.kernel`, `apodex.ai_eos.intelligence.eos_first_principles`
* **Consumer:** `apodex.skills.registry`, `apodex.world_model.world_model`, `apodex.memory.cmos`
* **Data Contract:** `ExecutionCommand`
* **Payload Structure:**
  ```python
  class ExecutionCommand(BaseModel):
      command_id: str
      skill_name: str
      parameters: dict[str, Any]
      allocated_budget_usd: float
      risk_limit: float
  ```

---

## 4. Static Dependency Verification Script Integration

Dependency validation is automatically verified via `scripts/validate_dependencies.py`:
- Max dependency depth $\le 6$.
- Forbidden core-to-adapter connections strictly enforced.
- Circular import detection over all AST nodes in `apodex/`.
