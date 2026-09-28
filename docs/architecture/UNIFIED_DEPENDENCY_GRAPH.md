# Unified Cognitive Operating System Dependency Graph
**Document Version:** 2.0.0 (2026 Edition)
**Status:** Approved

---

## 1. Directed Acyclic Dependency Structure

The Unified Cognitive Operating System enforces a strict top-down dependency hierarchy ($L_1 \rightarrow L_2 \rightarrow L_3 \rightarrow L_4$). Lower layers MUST NOT import higher layers. Upward communication occurs exclusively via asynchronous event observations and active inference feedback signals.

```
                  +-----------------------------------+
                  |      LAYER 1: RESEARCH OS         |
                  |  (apodex.ai_eos.research.*)       |
                  +-----------------------------------+
                                    |
                                    | Imports: Standard Libs, numpy, scipy, ast
                                    | Exports: Validated Hypothesis, Principles
                                    v
                  +-----------------------------------+
                  |       LAYER 2: EIOS / EOS         |
                  |  (apodex.arcs.kernel.*,           |
                  |   apodex.ai_eos.intelligence.*)  |
                  +-----------------------------------+
                                    |
                                    | Imports: Layer 1 Research OS
                                    | Exports: Active Inference DAGs, Value Objectives
                                    v
                  +-----------------------------------+
                  |          LAYER 3: AEAN            |
                  |  (apodex.aean.coordination.*,     |
                  |   apodex.aean.planning.*)         |
                  +-----------------------------------+
                                    |
                                    | Imports: Layer 2 EIOS/EOS Kernel
                                    | Exports: Swarm Tasks, Action Requests
                                    v
                  +-----------------------------------+
                  |        LAYER 4: APODEX            |
                  |  (apodex.world_model.*,           |
                  |   apodex.cognition.*,             |
                  |   apodex.skills.*)                |
                  +-----------------------------------+
                                    |
                                    | Imports: Layer 3 AEAN, Layer 2 EIOS, Layer 1 Research
                                    | Exports: Executed Tool Actions, Causal Updates
                                    v
                  +-----------------------------------+
                  |    CMOS & EVENT BUS FEEDBACK      |
                  |  (Asynchronous Observation Loop)  |
                  +-----------------------------------+
```

---

## 2. Layer Module Mapping & Import Hierarchy Rules

### Layer 1: Research OS
- **Package Path:** `apodex.ai_eos.research.*`
- **Modules:** `research_os.py`, `statistical_validation.py`, `integration.py`
- **Allowed Imports:** Python Standard Library, `numpy`, `scipy`, `ast`, `pydantic`.
- **Forbidden Imports:** `apodex.arcs.*`, `apodex.aean.*`, `apodex.world_model.*`.

### Layer 2: EIOS / EOS Kernel
- **Package Path:** `apodex.arcs.kernel.*`, `apodex.ai_eos.intelligence.*`
- **Modules:** `kernel.py`, `eos_engine.py`, `eos_first_principles.py`, `fourteen_layer_engine.py`
- **Allowed Imports:** Layer 1 (`apodex.ai_eos.research.*`), Standard Library, `sqlmodel`.
- **Forbidden Imports:** `apodex.aean.*`, `apodex.world_model.*`.

### Layer 3: AEAN Cognitive Intelligence
- **Package Path:** `apodex.aean.*`
- **Modules:** `coordination/hive_mind.py`, `planning/`, `agents/`
- **Allowed Imports:** Layer 2 (`apodex.arcs.kernel.*`, `apodex.ai_eos.intelligence.*`), Layer 1.
- **Forbidden Imports:** Direct execution of system tools (must execute via Layer 4 APODEX).

### Layer 4: APODEX Decision & Execution Platform
- **Package Path:** `apodex.world_model.*`, `apodex.cognition.*`, `apodex.skills.*`
- **Modules:** `world_model.py`, `brain.py`, `runner.py`
- **Allowed Imports:** Layer 3, Layer 2, Layer 1.
- **Role:** Platform foundation, Causal Graph maintainer, Tool sandbox executor, Memory storage engine.

---

## 3. Inter-Layer Interface Rules

1. **No Circular Dependencies:** Every module import statement is checked to ensure it points downward or strictly across allowed layer boundaries.
2. **Explicit State Hand-off Bridge:** Cross-layer transitions pass through `ResearchToSystemBridge` in `apodex.ai_eos.research.integration`.
3. **Asynchronous Feedback:** Feedback from Layer 4 tool executions to Layer 1/2 active inference algorithms is transmitted via events logged to CMOS memory and event buses.
