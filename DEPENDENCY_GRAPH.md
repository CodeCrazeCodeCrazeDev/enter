# Unified Cognitive OS: Subsystem Dependency Graph

This document maps the structural boundaries, layer interactions, and directory-level dependency constraints of the **Unified Cognitive Operating System (Cognitive OS)** substrate.

---

## 1. Directory-Level & Layered Interaction Graph

```
========================================================================================
                                 [ Research OS ] (L4)
                                 - apodex/research_os/
                                 - apodex/ai_eos/research/
                                        │
                                        │ (References EKG & Updates Beliefs)
                                        ▼
                                    [ AEAN ] (L3)
                                    - apodex/aean/
                                    - apodex/world_model/
                                        │
                                        │ (Dispatches Plans to State Machines)
                                        ▼
                                  [ EIOS / EOS ] (L2)
                                  - apodex/ai_eos/
                                  - agent_harness/components/
                                        │
                                        │ (Launches Local Runs)
                                        ▼
                                   [ APODEX ] (L1)
                                   - apodex/skills/
                                   - agent_harness/core/
========================================================================================
```

---

## 2. Unidirectional Dependency Constraints

To prevent circular imports and architectural coupling as the platform evolves, the following constraints are programmatically and statically enforced:

1. **Upward Dependency Prohibition**: Lower layers must *never* import modules or access states defined in higher layers.
   - For example, `agent_harness/core/` (Layer 1) cannot import anything from `apodex/aean/` (Layer 3) or `apodex/research_os/` (Layer 4).
2. **Strict Subsystem Boundaries**: Overlapping capabilities are consolidated into canonical owners:
   - **Research & Hypothesis Validation**: Owned exclusively by Layer 4 (`apodex/research_os/`).
   - **World State & Causal Modeling**: Owned exclusively by Layer 3 (`apodex/world_model/`).
   - **Workflow & Lifecycle Gating**: Owned exclusively by Layer 2 (`apodex/ai_eos/`).
   - **Low-level Tool & Skill Execution**: Owned exclusively by Layer 1 (`apodex/skills/`).

---

## 3. Reference Specification

For detailed class-level signatures, interface definitions, SOTA gap comparisons, and the engineering implementation plan, refer to the master architecture document:

👉 **[docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md](docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md)**
