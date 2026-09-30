# Unified Cognitive Architecture Specification
**Cognitive Operating System (Cognitive OS)**
*The authoritative engineering specification for a unified, non-duplicative, five-layer cognitive stack.*

---

## 1. Five-Layer Structural Blueprint

Cognitive OS unifies all platform components into five decoupled, explicit functional layers:

```
+----------------------------------------------------------------------------+
|                       LAYER 4: ECONOMIC GOVERNANCE                         |
|  - Canonical Owner: apodex/aean/governance.py                              |
|  - Capabilities: ConstitutionalFilter, Autonomy Tiers, Selection Auditing  |
+------------------------------------+---------------------------------------+
                                     |
                                     v
+------------------------------------+---------------------------------------+
|                      LAYER 3: INSTITUTIONAL RESEARCH                       |
|  - Canonical Owner: apodex/research_os/pipeline.py                         |
|  - Capabilities: Multiple Testing Correction, DSR, Block Bootstrapping      |
+------------------------------------+---------------------------------------+
                                     |
                                     v
+------------------------------------+---------------------------------------+
|                    LAYER 2: COGNITIVE ORCHESTRATION                        |
|  - Canonical Owner: apodex/cognition/controller.py                         |
|  - Capabilities: EFE Active Inference, UCB-1 MCTS Planning, SCM, Bus        |
+------------------------------------+---------------------------------------+
                                     |
                                     v
+------------------------------------+---------------------------------------+
|                     LAYER 1: EXECUTION & SIMULATION                        |
|  - Canonical Owner: apodex/memory/emg_engine.py                            |
|  - Capabilities: EMG Node Mining, SQLite Trajectory Store, Sandboxes       |
+------------------------------------+---------------------------------------+
                                     |
                                     v
+------------------------------------+---------------------------------------+
|                   LAYER 0: SUBSTRATE / ADAPTERS                            |
|  - Canonical Owner: AgentHarness (agent_harness/core/v2/)                   |
|  - Capabilities: Off-line Benchmarks, Legacy System Redirection            |
+----------------------------------------------------------------------------+
```

---

## 2. Singular Capability Ownership Model

To strictly prevent duplicate planners, world models, memory layers, and orchestrators, we define the following definitive boundaries:

### 2.1 Planning & Strategy Generation
- **Canonical Owner**: `apodex/cognition/planning/unified_planner.py`
- **Specification**: All high-level planning, hierarchical task decomposition, and MCTS tree search occur strictly here.
- **Rule**: No sub-agent or harness runner may generate independent plans. They must query the canonical planner.

### 2.2 World Modeling & State Snapshotting
- **Canonical Owner**: `apodex/world_model/world_model.py`
- **Specification**: Coordinates Entity, Knowledge, Causal, Temporal, and Uncertainty graphs under one consolidated model.
- **Rule**: Subsystems may only query or write events to this central service to modify belief parameters. Direct local dict mutation is prohibited.

### 2.3 Memory Systems
- **Canonical Owner**: `apodex/memory/semantic_memory.py`
- **Specification**: Relational, thread-safe SQLite-backed database holding semantic evidence, distilled episodes, and procedural skills.
- **Rule**: All persistent long-term knowledge must reside here, preventing local file-writing drift.

---

## 3. Explicit Interface Boundaries (APIs)

Every layer communicates strictly using explicitly specified contract types:

### 3.1 Causal Calculus Intervention API
```python
class ICausalInference(ABC):
    @abstractmethod
    def evaluate_scm_intervention(
        self,
        target_variable: str,
        intervention_value: float,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Pearl's backdoor-criterion do-calculus evaluator."""
        pass
```

### 3.2 Constitutional Filter API
```python
class IConstitutionalFilter(ABC):
    @abstractmethod
    def perform_selection_audit(
        self,
        agent_id: str,
        evidence_quality_tier: int,
        output_volume: int,
        calibration_accuracy: float,
        context_contains_evaluation_metrics: bool
    ) -> SelectionAuditReport:
        """Hendrycks safety audit filter preventing corner-cutting under pressure."""
        pass
```

### 3.3 Experience Memory Graph API
```python
class IEMGEngine(ABC):
    @abstractmethod
    def compute_graph_edit_path(
        self,
        failed_graph: ActionDecisionGraph,
        success_graph: ActionDecisionGraph
    ) -> List[EMGEditOp]:
        """Computes sequentially alignment edits (ADD_STEP, REPLACE_STEP, DELETE_STEP)."""
        pass
```

---

## 4. Conclusion & Migration Roadmap

By formalizing this unified layered Cognitive OS specification, we establish a robust structural hypothesis. Any proposed subsystem change must register its boundaries dynamically under this design, guaranteeing code cleanliness and long-horizon operational safety.
