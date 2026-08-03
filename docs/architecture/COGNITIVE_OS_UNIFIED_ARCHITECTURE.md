# Unified Cognitive Operating System (Cognitive OS) Architecture Specification
## Canonical Blueprint for Unified Intelligence Layering (v1.0.0)

This document establishes the authoritative, layered architecture blueprint for the unified **Cognitive Operating System (Cognitive OS)**. It formally transitions the historical, siloed platforms (**Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX**) into a single, cohesive, non-duplicative substrate. Rather than operating as disjointed engines, these historical systems now exist strictly as **logical views** or **functional viewpoints** over a shared 15-layer stack.

---

## 1. System Interaction Topology (The 15-Layer Stack)

The Cognitive Operating System is organized into fifteen clean, single-responsibility layers. Execution flows downwards from world perception to action execution, while governance, self-improvement, and evaluation act as continuous cross-cutting loops supervising every cycle.

```
       ┌─────────────────────────────────────────────────────────┐
 L14   │                GOVERNANCE LAYER                         │
       └──────────────────────────┬──────────────────────────────┘
                                  │ (continuous policy filter)
 L13   │              SELF-IMPROVEMENT LAYER                      │
       └──────────────────────────┬──────────────────────────────┘
                                  │ (playbook & weight updates)
 L12   │                EVALUATION LAYER                         │
       └──────────────────────────┬──────────────────────────────┘
                                  │ (performance & calibration)
       ┌──────────────────────────▼──────────────────────────────┐
 L11   │                EXECUTION LAYER                          │
       └──────────────────────────▲──────────────────────────────┘
                                  │ (isolated worker tools)
 L10   │                DECISION LAYER                           │
       └──────────────────────────▲──────────────────────────────┘
                                  │ (utility maximizer / utility)
  L9   │                SIMULATION LAYER                         │
       └──────────────────────────▲──────────────────────────────┘
                                  │ (pre-mortems / sandboxes)
  L8   │                PLANNING LAYER                           │
       └──────────────────────────▲──────────────────────────────┘
                                  │ (MCTS / HTN roadmap)
  L7   │                REASONING LAYER                          │
       └──────────────────────────▲──────────────────────────────┘
                                  │ (6-mind collective consensus)
  L6   │                WORLD MODEL                              │
       └──────────────────────────▲──────────────────────────────┘
                                  │ (E-K-C-T-U causal simulator)
  L5   │                MEMORY LAYER                             │
       └──────────────────────────▲──────────────────────────────┘
                                  │ (4-tier active memory)
  L4   │                KNOWLEDGE LAYER                          │
       └──────────────────────────▲──────────────────────────────┘
                                  │ (epistemic belief engine)
  L3   │                PERCEPTION LAYER                         │
       └──────────────────────────▲──────────────────────────────┘
                                  │ (raw signal scanning)
  L0   │                EXTERNAL WORLD                           │
       └─────────────────────────────────────────────────────────┘
```

---

## 2. Structural Layer Responsibilities & Boundaries

### L0: External World
*   **Responsibilities:** Real-world entities, external markets, competitor pricing pages, regulatory registries, ad platforms, financial payment rails, human consumers, and raw git repositories.
*   **Ownership:** System boundaries.
*   **Public Interfaces:** REST/gRPC APIs, webhook endpoints.

### L1: Perception Layer
*   **Responsibilities:** Continuous ingestion, semantic tokenization, and multi-modal sensory mapping of external signals. Converts messy HTML, PDF filings, and raw JSON into clean state representations.
*   **Ownership:** `apodex.aean.validation.perception`
*   **Dependencies:** None.
*   **Key Interface:**
    ```python
    class IPerceptionEngine(ABC):
        @abstractmethod
        async def parse_signal(self, raw_input: bytes, mime_type: str) -> SensoryObservation: ...
    ```

### L2: Knowledge Layer (KOS - Knowledge OS Substrate)
*   **Responsibilities:** Epistemic processing, belief updates, contradiction detection, and validation. Converts observations into versioned, confidence-weighted facts, beliefs, and hypotheses.
*   **Ownership:** `apodex.memory.semantic_memory` & `apodex.aean.ekg`
*   **Dependencies:** L1
*   **Key Interface:**
    ```python
    class IKnowledgeEngine(ABC):
        @abstractmethod
        def update_belief(self, belief_id: str, evidence: Evidence) -> Belief: ...
        @abstractmethod
        def detect_contradictions(self) -> List[Contradiction]: ...
    ```

### L3: Memory Layer (Multi-Tier Memory)
*   **Responsibilities:** Shared memory tiering across Working (local turn ReAct context), Episodic (execution trajectories), Semantic (persistent factual schemas), and Procedural (distilled SOP playbooks) memories.
*   **Ownership:** `apodex.memory.cmos` & `apodex.memory.services`
*   **Dependencies:** L2
*   **Key Interface:**
    ```python
    class IUnifiedMemoryService(ABC):
        @abstractmethod
        async def store_episode(self, episode: Episode) -> None: ...
        @abstractmethod
        async def retrieve_relevant_procedures(self, task_context: dict) -> List[Procedure]: ...
    ```

### L4: World Model (Causal World Model)
*   **Responsibilities:** Maintaining the Continuous World Model comprising five integrated graphs (E-K-C-T-U: Entity, Knowledge, Causal, Temporal, Uncertainty). Predicts downstream state transitions under potential actions.
*   **Ownership:** `apodex.world_model`
*   **Dependencies:** L3
*   **Key Interface:**
    ```python
    class ICausalWorldModel(ABC):
        @abstractmethod
        async def estimate_state_transition(self, current_state: State, action: Action) -> StatePrediction: ...
        @abstractmethod
        def run_causal_inference(self, cause_id: str, effect_id: str) -> float: ...
    ```

### L5: Reasoning Layer (Multi-Mind Collective Intelligence)
*   **Responsibilities:** Multi-mind strategic deliberation combining six reasoning paradigms: Bayesian, Symbolic, Causal, Economic, Game-Theoretic, and Mechanistic. Establishes mathematical consensus on alternative paths.
*   **Ownership:** `apodex.cognition.meta_reasoner` & `apodex.reasoning`
*   **Dependencies:** L4
*   **Key Interface:**
    ```python
    class ICollectiveIntelligence(ABC):
        @abstractmethod
        async def deliberate(self, question: str, context: dict) -> DeliberationConsensus: ...
    ```

### L6: Planning Layer (Unified Strategic Planner)
*   **Responsibilities:** Long-horizon strategic path formulation, goal decomposition (Hierarchical Task Networks), and tree-based decision search (Monte Carlo Tree Search - MCTS) over predicted future transitions.
*   **Ownership:** `apodex.planning` & `apodex.cognition.planning`
*   **Dependencies:** L5
*   **Key Interface:**
    ```python
    class IStrategicPlanner(ABC):
        @abstractmethod
        async def generate_roadmap(self, overall_goal: str) -> StrategicRoadmap: ...
    ```

### L7: Simulation Layer (Simulation Sandbox / Digital Twin)
*   **Responsibilities:** Execution of synthetic sandbox "pre-mortems," Monte Carlo market trials, and price elasticity tests against synthetic agents before committing real capital.
*   **Ownership:** `apodex.world_model.domain.simulation`
*   **Dependencies:** L6
*   **Key Interface:**
    ```python
    class ISimulationSandbox(ABC):
        @abstractmethod
        async def simulate_pre_mortem(self, roadmap: StrategicRoadmap) -> SimulationReport: ...
    ```

### L8: Decision Layer (Utility & Capital Optimization Engine)
*   **Responsibilities:** Dynamic asset allocation, expected utility calculation, and Lagrange multiplier dual shadow pricing. Selects the optimal path on the multi-objective Pareto frontier.
*   **Ownership:** `apodex.ai_eos.portfolio` & `apodex.ai_eos.intelligence`
*   **Dependencies:** L7
*   **Key Interface:**
    ```python
    class IDecisionEngine(ABC):
        @abstractmethod
        def allocate_capital(self, candidate_ventures: List[Venture]) -> AllocationResult: ...
    ```

### L9: Execution Layer (Orchestration & Isolated Action)
*   **Responsibilities:** Orchestrating task execution via coordinator-worker agents. Dispatches isolated actions to specific tools (e.g., search, content-gen, code compile) while keeping the planning context clean.
*   **Ownership:** `apodex.orchestration` & `apodex.skills`
*   **Dependencies:** L8
*   **Key Interface:**
    ```python
    class IExecutionEngine(ABC):
        @abstractmethod
        async def dispatch_isolated_task(self, step: RoadmapStep) -> TaskResult: ...
    ```

### L10: Evaluation Layer (System Benchmark & Calibration Audit)
*   **Responsibilities:** Post-mortem evaluation, calibration auditing, dense subtask-level credit assignment, and factuality grounding verification.
*   **Ownership:** `apodex.cognition.dataset_generator` & `apodex.aean.validation`
*   **Dependencies:** L9
*   **Key Interface:**
    ```python
    class IEvaluationFramework(ABC):
        @abstractmethod
        def assign_credit(self, trajectory: Trajectory) -> CreditReport: ...
        @abstractmethod
        def audit_calibration(self) -> CalibrationReport: ...
    ```

### L11: Self-Improvement Layer (Meta-Learning & Prompt/Weight Optimization)
*   **Responsibilities:** Weakness mining across finished episodes, prompt refinement (EvoPrompt), tool invention, and supervised dataset curation to run offline weight training/fine-tuning.
*   **Ownership:** `apodex.evolution` & `apodex.cognition.learning`
*   **Dependencies:** L10
*   **Key Interface:**
    ```python
    class ISelfImprovementEngine(ABC):
        @abstractmethod
        async def mine_weaknesses(self, episodes: List[Episode]) -> List[Weakness]: ...
        @abstractmethod
        def compile_training_data(self) -> List[TrainingRecord]: ...
    ```

### L12: Governance Layer (Immutable Safety & Multi-Tier Approval)
*   **Responsibilities:** Enforcing immutable system invariants, budget-coordination safety limits, tenancy boundary verification, non-waivable human approvals on irreversible steps, and automated rollback actions.
*   **Ownership:** `apodex.ai_eos.governance` & `apodex.world_model.governance`
*   **Dependencies:** All layers (cross-cutting)
*   **Key Interface:**
    ```python
    class IGovernanceFramework(ABC):
        @abstractmethod
        def check_invariant(self, proposed_action: Action) -> SafetyAudit: ...
        @abstractmethod
        def execute_rollback(self, changelog_entry: ChangelogEntry) -> RollbackReport: ...
    ```

---

## 3. Consolidation of Core Capabilities (Singular Ownership Matrix)

To eliminate technical debt, duplicated planners, registries, and memory subsystems from v1, the platform mandates a singular canonical owner for each key capability.

| Unified System Component | Canonical Module Owner | Obsoleted/Deprecating Duplicates (Merged or Eliminated) |
| :--- | :--- | :--- |
| **One Strategic Planner** | `apodex.planning.planner_executor` | `agent_harness.core.runtime.orchestration.planner_executor` |
| **One Causal World Model**| `apodex.world_model.world_model` | Multi-level models inside legacy EIOS, custom graphs in AEAN. |
| **One Memory Subsystem** | `apodex.memory.semantic_memory` & `cmos` | Separate databases inside EIOS, custom memory in AgentHarness. |
| **One Execution Engine**  | `apodex.orchestration.hierarchical` | Scattered procedural ReAct loops, bespoke terminal executors. |
| **One Scheduler**         | `apodex.world_model.orchestration.scheduler` | Custom loops in `AgentHarness/scheduling`. |
| **One Evaluation Engine** | `apodex.cognition.trajectory_verification` | Evaluators scattered across tests and individual task agents. |
| **One Governance Core**   | `apodex.ai_eos.governance.gateway` | Gating scripts inside individual validation folders. |
| **One Orchestration Layer**| `apodex.orchestration.hierarchical` | Bespoke agent-coordination logic inside `aean/coordination`. |
| **One Knowledge Graph**   | `apodex.aean.ekg` | Isolated entity lists, raw JSON dumps. |
| **One Simulation Sandbox**| `apodex.world_model.domain.simulation` | Mock evaluation scripts. |
| **One Capability Registry**| `apodex.skills.registry` | Hardcoded skill dictionaries, bespoke command mappings. |
| **One Metrics System**    | `apodex.world_model.telemetry` | Custom log wrappers, inline timing code. |

---

## 4. Multi-Mind Layer Interaction & Collaboration Flow

```
   Perception Layer           Knowledge OS Substrate        Causal World Model              Planner                   Governance
┌────────────────────┐        ┌────────────────────┐       ┌──────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Ingest Raw Signal  ├───────►│ Extract Evidence   │       │ Update Relations │       │ Decompose Task  │       │ Verify Safety   │
│ (Sensory Input)    │        │ & Update Beliefs   │       │ & Transition     │       │ via HTN / MCTS  │       │ Limits & Budget │
└────────────────────┘        └─────────┬──────────┘       │ Probability      │       └────────┬────────┘       └────────▲────────┘
                                        │                  └────────▲─────────┘                │                         │
                                        │                           │                          │                         │
                                        ▼                           │                          ▼                         │
                               ┌─────────────────┐                  │                 ┌────────┴────────┐                │
                               │ Identify        ├──────────────────┘                 │ Run Simulation  ├────────────────┘
                               │ Contradictions  │                                    │ Sandbox (Pre-M) │
                               └─────────────────┘                                    └─────────────────┘
```

Every deliberation cycle executes an iterative consensus process across the six minds:
1. **Perception Engine (L1)** publishes a parsed event signal.
2. **Knowledge OS (L2)** performs a Bayesian Belief Update, updating belief strength priors. If a conflict occurs, a `Contradiction` is raised and resolved by the `MetaReasonerObserver`.
3. **Causal World Model (L4)** updates causal transition linkages, adjusting the probability distributions of downstream consequences.
4. **Strategic Planner (L6)** receives a goal, decomposing it into structured steps ($RoadmapStep$). It runs MCTS or HTN trees over the World Model.
5. **Simulation Sandbox (L7)** performs a Monte Carlo pre-mortem of the candidate roadmap to measure risk.
6. **Decision Engine (L8)** scores the roadmap's Expected Utility and shadow price capital requirements, ensuring compliance with strict capital-efficiency constraints.
7. **Governance Core (L12)** audits the selected actions against immutable safety invariants before allowing execution.
