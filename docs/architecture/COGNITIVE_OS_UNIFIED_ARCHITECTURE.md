# Unified Cognitive Operating System Architecture
## Authoritative Technical Specification & Scientific Blueprint (v2.5)

This document establishes the definitive, institutional-grade architectural specification for the unified Apodex Cognitive Operating System. It integrates five historically semi-overlapping systems—**Research OS**, **AEAN (Autonomous Entrepreneurial Research & Execution Operating System)**, **EIOS (Entrepreneurial Intelligence Operating System)**, **EOS (Entrepreneurial Operating System)**, and **APODEX (Trading & Decision Engine)**—into a single cohesive, decoupled, and horizontally scalable layered cognitive topology.

---

## 1. Unified Layered Cognitive OS Architecture

To eliminate architectural duplication and enforce clean separation of concerns, the platform is structured as a hierarchical five-layer operating system. Each layer exposes strict upward-facing APIs and depends exclusively on lower-level infrastructure.

```
+========================================================================+
|                        LAYER 5: APODEX                                 |
| (Decision, Trading, Portfolio Mgmt, Broker Interfaces, Execution)      |
+========================================================================+
                                 │ (Strategic and Capital Directives)
                                 ▼
+========================================================================+
|                        LAYER 4: RESEARCH OS                            |
| (Scientific Discovery, Experimentation, Hypothesis Engine, Evaluation) |
+========================================================================+
                                 │ (Validated Theories, Grounded Facts)
                                 ▼
+========================================================================+
|                        LAYER 3: AEAN                                   |
| (Reasoning, Planning, Multi-Tier Memory, World Model, Self-Improvement)|
+========================================================================+
                                 │ (Declarative Plans and Strategies)
                                 ▼
+========================================================================+
|                        LAYER 2: EIOS                                   |
| (Orchestration, Workflow Execution, Scheduling, Multi-Agent Coord)    |
+========================================================================+
                                 │ (Task Dispatches, Step Sequences)
                                 ▼
+========================================================================+
|                        LAYER 1: EOS                                    |
| (Runtime Infrastructure, Services, Messaging Bus, Observability, GRC)  |
+========================================================================+
```

### Layer Descriptions

1. **Layer 5: APODEX (Decision and Execution Layer)**
   - **Responsibility**: Real-world strategic selection, venture analysis, license orchestration, capital allocation, portfolio risk boundaries, broker interfaces, and market interaction. It models venture mandates and translates investment policy criteria into active research tasks.
2. **Layer 4: RESEARCH OS (Epistemic Discovery Layer)**
   - **Responsibility**: Formal hypothesis generation, experimental design, walk-forward validation, statistical correction (Bonferroni, Deflated Sharpe Ratio, data leakage checkers), and theory promotion. It acts as the "scientist", validating capabilities before promoting them into active system components.
3. **Layer 3: AEAN (Cognitive Intelligence Layer)**
   - **Responsibility**: High-level reasoning, Graph-of-Thought search, Expected Free Energy minimization (active inference), shared multi-tier memory consolidation (Working, Episodic, Semantic, Procedural), and continuous Multi-Graph World Modeling.
4. **Layer 2: EIOS (Orchestration and Workflow Layer)**
   - **Responsibility**: Compiling declarative strategic plans into execution DAGs, process coordination, thread-safe task scheduling, resource allocation, and multi-agent communication routing.
5. **Layer 1: EOS (Runtime and System Layer)**
   - **Responsibility**: Execution environments (sandboxed Docker, local runners), low-level database persistence, transactional safety boundaries, distributed event bus, messaging, observability/tracing, and GRC policies (Constitutional safety filters).

---

## 2. Capability Ownership Matrix

Every system capability is assigned exactly one authoritative owner. Duplication is strictly prohibited.

| Major Capability | Layer | Canonical Owner Subsystem | Decoupled Responsibilities |
| :--- | :--- | :--- | :--- |
| **Capital Allocation** | Layer 5 | `apodex/ai_eos/portfolio/manager.py` | ROI-driven venture selection and expected discovery value allocations. |
| **Broker Interface** | Layer 5 | `apodex/ai_eos/intelligence/decision_engine.py` | Live trading, broker gateways, exchange execution. |
| **Hypothesis Engine** | Layer 4 | `apodex/research_os/hypothesis_engine.py` | Scientific hypothesis synthesis, ranking, walk-forward validation. |
| **Statistical Validation** | Layer 4 | `apodex/research_os/statistical_validation.py` | Bonferroni corrections, Deflated Sharpe Ratio (DSR), data leakage verification. |
| **Active Inference Planner** | Layer 3 | `apodex/ai_eos/active_inference/engine.py` | EFE (Expected Free Energy) calculations, curiosity-driven strategic selection. |
| **World Graph Engine** | Layer 3 | `apodex/world_model/world_model.py` | Persists multi-graph (Entity, Knowledge, Causal, Temporal, Uncertainty). |
| **Memory Consolidation** | Layer 3 | `apodex/memory/learning_memory.py` | Exponential decay, conjugate Beta-Binomial update, transfer of Episodic to Semantic. |
| **DAG Scheduler** | Layer 2 | `agent_harness/scheduling/scheduler.py` | Declarative WDL compilation, task status tracking, thread execution. |
| **Orchestrator Coordination** | Layer 2 | `agent_harness/core/v2/orchestrator.py` | Hierarchical Master-Coordinator-Worker communication. |
| **Constitutional Safety** | Layer 1 | `apodex/aean/governance.py` | Hendrycks safety filter checks, prompt invisibility audits. |
| **Event Bus Router** | Layer 1 | `apodex/ai_eos/infrastructure/event_bus.py` | Process-wide pub-sub distribution of structured transactional events. |
| **Sandboxed Execution** | Layer 1 | `apodex/ai_eos/validation/platform.py` | Chaos testing, isolated Docker runners, execution resource limiting. |

---

## 3. Structural Dependency Graph

```
             +---------------------------------------------+
             |                 APODEX                      |
             +----------------------+----------------------+
                                    |
                                    v
             +----------------------+----------------------+
             |               RESEARCH OS                   |
             +----------------------+----------------------+
                                    |
                                    v
             +----------------------+----------------------+
             |                  AEAN                       |
             +----------------------+----------------------+
                                    |
                                    v
             +----------------------+----------------------+
             |                  EIOS                       |
             +----------------------+----------------------+
                                    |
                                    v
             +----------------------+----------------------+
             |                  EOS                        |
             +---------------------------------------------+
```

### Strict Architectural Boundaries
- **No Upward Dependencies**: A lower layer (e.g., EOS) must never import from or reference a higher layer (e.g., AEAN).
- **No Horizontal Bypasses**: Layer-to-layer interaction should occur strictly through upward/downward interface contracts. Cross-talk is minimized.

---

## 4. Multi-Tier Shared Memory Architecture

Cognitive data is strictly separated by access speed, persistence duration, and relational topology, avoiding memory-bloat or context-window saturation.

```
+===============================================================================+
|                               MEMORY TIERING                                 |
+===============================================================================+
| TIER 1: Working Memory  | Transient context, ReAct loop traces, current turn |
|                         | - Scope: Session thread                            |
|                         | - Technology: Local RAM / SQLite transient         |
+-------------------------+-----------------------------------------------------+
| TIER 2: Episodic Memory | Task-specific traces, past execution runs           |
|                         | - Scope: Cross-session recovery                     |
|                         | - Technology: Relational SQLite DB (`trajectory`)   |
+-------------------------+-----------------------------------------------------+
| TIER 3: Semantic Memory | Factual knowledge, verified schemas, entity graphs   |
|                         | - Scope: Global system context                      |
|                         | - Technology: SQLiteMemoryRepository (Vector-Index) |
+-------------------------+-----------------------------------------------------+
| TIER 4: Procedural Mem  | Registered skills, validated python tool segments  |
|                         | - Scope: System capability registry                 |
|                         | - Technology: SkillRegistry (Pre-compiled modules)  |
+===============================================================================+
```

### Memory Consolidation Lifecycle (EPISODIC ──> SEMANTIC)
1. At task completion, the **Episodic Trace** is committed to the relational database.
2. An asynchronous background process (`MemoryConsolidationService`) parses the trace.
3. Common step sequences are analyzed using sequence-pattern mining via the **Experience Memory Graph (EMG) Engine**.
4. Discovered facts, domain vocabularies, and corrected causal relationships are indexed into **Semantic Memory**.
5. Repetitive successful paths are compiled into reusable tool segments and stored in the **Procedural Memory SkillRegistry**.

---

## 5. Agent Interaction Protocol

Interaction between specialized cognitive agents is governed by a strict, stateful communication model. Direct arbitrary messaging is prohibited.

```
[Master Orchestrator]                     [Coordinator Agent]                      [Worker Agent]
         │                                         │                                      │
         │ 1. Dispatches Sub-goal (Goal, Budget)   │                                      │
         ├────────────────────────────────────────>│                                      │
         │                                         │ 2. Selects Specialized Worker        │
         │                                         ├─────────────────────────────────────>│
         │                                         │                                      │
         │                                         │ 3. Executes Tool (Sandboxed)         │
         │                                         │<─────────────────────────────────────┤
         │                                         │                                      │
         │                                         │ 4. Submits Result (Evidence Card)    │
         │                                         │<─────────────────────────────────────┤
         │                                         │                                      │
         │ 5. Returns Consolidated Report          │                                      │
         │<────────────────────────────────────────┤                                      │
```

---

## 6. System-Wide Event Model

Communication across layers uses an event-driven pub-sub architecture handled entirely by the `EventBus` in Layer 1.

### Structural Schema Definitions

#### 1. TaskCreatedEvent
- **Published By**: Layer 5 (APODEX)
- **Subscribed By**: Layer 2 (EIOS)
- **Schema**:
  ```json
  {
    "event_id": "evt_task_10821",
    "timestamp": 1785230401.52,
    "task_id": "task_re_441",
    "venture_id": "ven_08",
    "objective": "Evaluate optimal option trading volatility arbitrage routes.",
    "budget_limit_usd": 15.0,
    "max_iterations": 20
  }
  ```

#### 2. HypothesisProposedEvent
- **Published By**: Layer 4 (RESEARCH OS)
- **Subscribed By**: Layer 3 (AEAN)
- **Schema**:
  ```json
  {
    "event_id": "evt_hypo_302",
    "timestamp": 1785230412.11,
    "hypothesis_id": "hyp_908",
    "domain": "quantitative_finance",
    "claim": "Walk-forward volatility estimator out-performs standard GARCH under regime changes.",
    "confidence_prior": 0.50,
    "evidence_ids": ["ev_causal_01", "ev_causal_02"]
  }
  ```

#### 3. ExecutionTraceLoggedEvent
- **Published By**: Layer 2 (EIOS)
- **Subscribed By**: Layer 3 (AEAN) / Layer 1 (Observability)
- **Schema**:
  ```json
  {
    "event_id": "evt_trace_8820",
    "timestamp": 1785230455.99,
    "trajectory_id": "traj_9082",
    "step_id": "step_04",
    "action_taken": "web_fetch",
    "result_status": "success",
    "is_error": false,
    "tokens_consumed": 842,
    "latency_ms": 1240.0
  }
  ```

---

## 7. Decoupled Interface Contracts

Strict interface boundaries are defined as frozen Python abstract base classes.

### 1. Causal Inference Engine (Layer 3)
```python
class ICausalInferenceEngine(ABC):
    @abstractmethod
    def evaluate_scm_do_calculus(self, graph_data: dict, treatment: str, outcome: str) -> dict:
        """
        Applies Pearl's backdoor criteria SCM do-calculus interventions
        to resolve root causes inside the continuous world model.
        """
        pass
```

### 2. Bayesian Belief Engine (Layer 3)
```python
class IBayesianBeliefEngine(ABC):
    @abstractmethod
    def conjugate_update_beta(self, alpha: float, beta: float, successes: int, failures: int) -> tuple[float, float]:
        """
        Calculates conjugate Beta distribution updates weighted by evidence quality reliability scales.
        """
        pass
```

### 3. Expected Free Energy Planner (Layer 3)
```python
class IExpectedFreeEnergyPlanner(ABC):
    @abstractmethod
    def calculate_efe(self, action_distribution: list, belief_entropy: float, epistemic_value: float) -> float:
        """
        Approximates Expected Free Energy to drive active inference search paths.
        """
        pass
```

### 4. GRC Constitutional Filter (Layer 1)
```python
class IConstitutionalFilter(ABC):
    @abstractmethod
    def audit_safety_compliance(self, prompt: str, actions: list) -> bool:
        """
        Enforces Hendrycks safety audits, objective constraints, and operational entanglement checks.
        """
        pass
```

---

## 8. Data-Flow Specification

The data lifecycle within the Cognitive OS spans five distinct operational phases:

```
[External Prompt/Event]
         │
         ▼
[1. Strategy Generation (Layer 3)] ──> Evaluates expected free energy (EFE) via World Model
         │
         ▼
[2. Plan Compilation (Layer 2)]    ──> Compiles strategic paths into a declarative Workflow (WDL)
         │
         ▼
[3. Distributed Dispatch (Layer 2)]  ──> Dispatches individual task nodes to isolated sandboxed Worker Agents
         │
         ▼
[4. Event Sourcing Log (Layer 1)]  ──> Persists execution trajectories and performance metrics to local relational DB
         │
         ▼
[5. Memory Consolidation (Layer 3)]──> Sweeps completed traces, extracts semantic insights, updates the World Graph
```

---

## 9. Control-Flow Specification

The execution control lifecycle utilizes hierarchical orchestration to prevent deadlocks, loops, and token waste.

```
       +---------------------------------------------+
       |             Master Orchestrator             |
       +----------------------+----------------------+
                              |
                     [Evaluates Turn Limit]
                              |
                     +--------v--------+
                     |  Meta Reasoner  | (Detects Echo Traps / Loops)
                     +--------+--------+
                              |
                    [Within Limits & Safe]
                              |
                     +--------v--------+
                     |   Task Executor | (Executes tool / sub-goal)
                     +--------+--------+
                              |
                     +--------v--------+
                     |  Safety Monitor | (Enforces SLA Latency / Constitutional Guard)
                     +-----------------+
```

---

## 10. Unified Repository Layout

```
/app
├── agent_harness/                  # LAYER 2: Orchestration and Workflow Compilation
│   ├── core/
│   │   ├── messages.py             # Communication message models
│   │   ├── tool.py                 # Tool wrappers
│   │   ├── loop_types.py           # ReAct loop state models
│   │   ├── runtime/
│   │   │   └── loop/               # Low-level ReAct execution controllers
│   │   └── v2/                     # Hierarchical orchestrator and memory graphs
│   └── scheduling/
│       └── scheduler.py            # WDL schedule DAG execution engine
├── apodex/
│   ├── ai_eos/                     # SYSTEM CORE
│   │   ├── active_inference/       # LAYER 3: Epistemic planners and EFE models
│   │   ├── intelligence/           # LAYER 5: SCM do-calculus, venture engines
│   │   ├── portfolio/              # LAYER 5: Portfolio Manager, capital allocations
│   │   ├── research/               # LAYER 4: Research OS compilers, hypothesis generators
│   │   ├── memory/                 # LAYER 3: Knowledge Graph, Bayesian Belief Engine
│   │   ├── validation/             # LAYER 1: Chaos testing and sandbox execution
│   │   └── governance/             # LAYER 1: GRC Gateway, specialized agent rosters
│   ├── memory/                     # LAYER 3: Semantic memory & SQLite databases
│   ├── world_model/                # LAYER 3: Entity, Knowledge, Causal, Temporal, Uncertainty graphs
│   └── aean/                       # LAYER 5: Executive multi-agent engines (ADE, ARE, AVIE)
├── docs/                           # Documentation
│   └── architecture/               # System architectures & design guidelines
└── tests/                          # 100% offline unit & integration test bed
```

---

## 11. Phased Migration Roadmap & Evaluation Criteria

To implement this unified layered architecture without destabilizing production, migrations are staged in three distinct waves with objective gate criteria.

```
+=============================================================================+
|                      PHASED MIGRATION TIMELINE                              |
+=============================================================================+
| PHASE 1: Substrate Hardening (COMPLETED)                                    |
| - Relational trajectory SQLite database, Thread-safe memory locks           |
| - Gate Criteria: 100% thread safety, zero RAM leaks over 10,000 steps       |
+-----------------------------------------------------------------------------+
| PHASE 2: Capability Ownership Separation (ACTIVE)                           |
| - Isolate capabilities into Layer 1 to Layer 5 canonical directories        |
| - Eliminate duplicate modules, replace legacy imports with Compatibility     |
|   Adapters (Legacy API -> Compatibility Adapter -> Canonical APODEX)         |
| - Gate Criteria: Compile complete ownership audit list; zero direct files   |
|   duplicated. Legacy tests pass perfectly.                                  |
+-----------------------------------------------------------------------------+
| PHASE 3: Multi-Objective Benchmarking and Adapter Removal                   |
| - Run complete performance audits comparing Adapter latency and token weight |
|   against baseline run scenarios.                                           |
| - Deprecate and remove Compatibility Adapters completely.                   |
| - Gate Criteria: Complete removal of legacy bridging packages, latency      |
|   penalty <= 1.05x, throughput improved by 1.2x.                            |
+=============================================================================+
```
