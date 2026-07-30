# Cognitive Architecture Specification: AEAN Cognitive OS (Phase 0)

This document details the first-principles, high-integrity design for the unified Cognitive Operating System (Cognitive OS) of the Autonomous Economic Agent Network (AEAN). It supersedes all previous "brain" controller proposals, opting instead for a decoupled, event-driven service architecture orchestrated by a light-weight Cognitive Kernel communicating over a high-performance Shared Cognitive Bus.

---

## 1. Cognitive Capability Decomposition & Subsystem Justifications

### 1.1 Cognitive Kernel (Orchestrator)
- **Problem Solved**: Central coordination bottleneck and tight coupling of specialized intelligence modules.
- **Measurable Capability Improvement**: Pipeline orchestration latency is isolated and deterministic ($< 5\text{ ms}$ overhead).
- **Architectural Rationale**: Acts as a pure, stateless coordinator of the cognitive pipeline loop, directing resource allocation without implementing intelligence logic.
- **Computational Cost**: $O(1)$ routing complexity.
- **Maintenance Cost**: Minimal; does not change when capabilities or algorithms are upgraded.
- **Dependencies**: Shared Cognitive Bus.
- **Alternatives Considered**: Monolithic central loop state machine.
- **Rejection Reason**: Monoliths are highly brittle, prone to cascade failures, and difficult to test hermetically.

### 1.2 Planner
- **Problem Solved**: Long-horizon task decomposition and automatic recovery from execution failures during multi-day tasks.
- **Measurable Capability Improvement**: Goal-conditioned hierarchical task tree generation up to $100+$ steps with dynamic replanning.
- **Architectural Rationale**: Uses HTN for predictable domain-specific constraints, augmented with dynamic Tree of Thoughts search.
- **Computational Cost**: $O(B^D)$ where $B$ is the branching factor and $D$ is the depth. Bound by a maximum depth of 5.
- **Maintenance Cost**: Medium; requires maintaining domain-specific task schemas.
- **Dependencies**: Memory, World Model.
- **Alternatives Considered**: Pure reactive RL policies.
- **Rejection Reason**: Lacks multi-hour task consistency, lacks traceability, and is prone to infinite loops.

### 1.3 World Model
- **Problem Solved**: Accurate representation of internal and external uncertainty, competitor states, and causal consequence of actions.
- **Measurable Capability Improvement**: Prevents hallucinated action consequences by computing counterfactuals with Judea Pearl's do-calculus.
- **Architectural Rationale**: Continuous conjugate Bayesian updating of prior beliefs weighted by the reliability of incoming evidence.
- **Computational Cost**: $O(V + E)$ for DAG queries, where $V$ is variables and $E$ is causal edges.
- **Maintenance Cost**: High; requires rigorous validation of SCM coefficients.
- **Dependencies**: Memory, Evaluation Engine.
- **Alternatives Considered**: Direct LLM-based predictive querying.
- **Rejection Reason**: Highly uncalibrated probabilities, vulnerable to prompt injections, and lacks mathematical guarantees.

### 1.4 Memory Engine
- **Problem Solved**: Cognitive overload, prompt token saturation, and information decay over long execution horizons.
- **Measurable Capability Improvement**: Retrieves relevant past episodes under $50\text{ ms}$ and implements Ebbinghaus decay to consolidate knowledge.
- **Architectural Rationale**: Tri-partitioned (episodic, semantic, procedural) SQLite-backed vector and graph database with exponential forgetting curves.
- **Computational Cost**: $O(\log N)$ retrieval complexity.
- **Maintenance Cost**: Low.
- **Dependencies**: Shared Cognitive Bus.
- **Alternatives Considered**: Pinecone / Cloud-hosted Vector DBs.
- **Rejection Reason**: Offline requirement, network latency variability, and complex state synchronization.

### 1.5 Research Engine (Research Lab OS)
- **Problem Solved**: Autonomous scientific exploration, literature analysis, and systematic claim verification without human intervention.
- **Measurable Capability Improvement**: Automatic bibliography deconstruction, token similarity checks, and claim verification score outputs.
- **Architectural Rationale**: Implements batch-based ingestion, parsing, and automated replication checking.
- **Computational Cost**: Dependent on parser and execution duration.
- **Maintenance Cost**: Medium; requires maintaining parser rules.
- **Dependencies**: Planner, World Model.
- **Alternatives Considered**: Simple retrieval-augmented generation (RAG) search.
- **Rejection Reason**: Does not perform rigorous claim validation, lacks replication checks, and cannot detect scientific contradictions.

### 1.6 Simulation Engine
- **Problem Solved**: Risk estimation of proposed plans, exploring branching future scenarios, and calculating Value-at-Risk (VaR).
- **Measurable Capability Improvement**: Models $1,000+$ parallel branching futures under $10\text{ ms}$ and computes portfolio VaR at a $95\%$ confidence interval.
- **Architectural Rationale**: Statistical Monte Carlo simulation framework modeling payoffs as normal distributions.
- **Computational Cost**: $O(M \times N)$ where $M$ is sample count and $N$ is steps.
- **Maintenance Cost**: Low.
- **Dependencies**: World Model.
- **Alternatives Considered**: Pure qualitative LLM brainstorming.
- **Rejection Reason**: Qualitative forecasting is highly uncalibrated and lacks quantitative risk parameters.

### 1.7 Multi-Agent Runtime
- **Problem Solved**: Specialized domain expertise handling, and resolving multi-perspective disagreement without sycophancy.
- **Measurable Capability Improvement**: Dynamically splits, merges, spawns, or retires specialized agents based on execution bottlenecks.
- **Architectural Rationale**: Independent multi-agent runtime with programmatic turn-taking and turn-based voting debate pipelines.
- **Computational Cost**: Linear in agent count.
- **Maintenance Cost**: Medium; requires lifecycle tracking.
- **Dependencies**: Shared Cognitive Bus.
- **Alternatives Considered**: Static multi-agent swarms.
- **Rejection Reason**: Inefficient compute allocation, leads to redundant roles, and cannot self-prune.

### 1.8 Execution Engine
- **Problem Solved**: Safe execution of long-duration, multi-step code and workflow processes with checkpoints.
- **Measurable Capability Improvement**: Restarts interrupted workflows from the last valid checkpoint with $100\%$ accuracy.
- **Architectural Rationale**: Directed Acyclic Graph (DAG) executor with thread-safe SQLite persistence for task tracking.
- **Computational Cost**: $O(V + E)$ topological sort.
- **Maintenance Cost**: Medium; requires platform-specific integrations.
- **Dependencies**: Planner, Governance.
- **Alternatives Considered**: Thread-based sequential execution.
- **Rejection Reason**: Interruption results in full loss of state, with zero crash recovery.

### 1.9 Evaluation Engine
- **Problem Solved**: System regressions, cognitive drift, and lack of objective quality gates during self-improvement.
- **Measurable Capability Improvement**: Enforces automated pass/fail verification gates on every system upgrade.
- **Architectural Rationale**: Programmatic verification pipeline using standard metric baselines and test harness comparisons.
- **Computational Cost**: Constant verification overhead.
- **Maintenance Cost**: Low.
- **Dependencies**: Shared Cognitive Bus.
- **Alternatives Considered**: Pure manual unit testing.
- **Rejection Reason**: Incompatible with autonomous continuous self-evolution.

### 1.10 Governance Layer
- **Problem Solved**: Rogue agent execution, budget overruns, command injections, and safety violations.
- **Measurable Capability Improvement**: Vetoes actions exceeding limits or violating policies in $< 2\text{ ms}$.
- **Architectural Rationale**: Programmatic, non-bypassable validation filter with hard limits on budget and goal scopes.
- **Computational Cost**: $O(1)$ check.
- **Maintenance Cost**: Low.
- **Dependencies**: None.
- **Alternatives Considered**: LLM-based policy moderation.
- **Rejection Reason**: Highly non-deterministic, slow, and bypassable via jailbreaks.

### 1.11 Shared Cognitive Bus
- **Problem Solved**: Tight structural coupling of services and complex dependency routing.
- **Measurable Capability Improvement**: Message delivery latency $< 1\text{ ms}$ over memory-mapped queues.
- **Architectural Rationale**: High-performance, lightweight Pub-Sub event broker.
- **Computational Cost**: $O(1)$ publish overhead.
- **Maintenance Cost**: Very low.
- **Dependencies**: None.
- **Alternatives Considered**: Direct synchronous RPC / HTTP.
- **Rejection Reason**: Introduces circular dependencies, tight coupling, and cascade failures.

---

## 2. Detailed Interface Contracts & Budgets

Every subsystem communicates via strongly typed, serialized message schemas. Below are the frozen API schemas for the core subsystems:

### 2.1 Shared Cognitive Bus Interface
```python
class EventMessage(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    topic: str
    sender: str
    payload: Dict[str, Any]
    timestamp: float

class ISaredCognitiveBus(ABC):
    @abstractmethod
    def publish(self, topic: str, sender: str, payload: Dict[str, Any]) -> None:
        """Latency Budget: < 1ms | Memory: < 1KB per message"""
        pass

    @abstractmethod
    def subscribe(self, topic: str, callback: Callable[[EventMessage], None]) -> None:
        pass
```

### 2.2 Planner Interface
```python
class IPlanner(ABC):
    @abstractmethod
    def plan(self, goal: StrategicGoal, state: Dict[str, Any]) -> ExecutionPlan:
        """
        Generates a structured execution plan.
        Latency Budget: < 500ms (Local models) / < 150ms (Heuristic trees)
        Memory Budget: < 10MB state space
        Invariants: Output plan steps must be topologically sorted.
        Failure Modes: Plan decomposition failures raise PlanDecompositionError.
        """
        pass
```

### 2.3 World Model Interface
```python
class IWorldModel(ABC):
    @abstractmethod
    def update_beliefs(self, variable: str, observation: float, evidence_quality: float) -> None:
        """
        Conjugate Bayesian updates.
        Invariants: Belief scores are strictly constrained between 0.0 and 1.0.
        Latency Budget: < 5ms
        """
        pass

    @abstractmethod
    def evaluate_causal_intervention(self, target: str, treatment: str, val: float) -> float:
        """Computes Judea Pearl do-calculus intervention values."""
        pass
```

### 2.4 Memory Engine Interface
```python
class IMemoryEngine(ABC):
    @abstractmethod
    def store(self, content: str, current_time: float) -> MemoryItem:
        """Stores memory item and initializes Ebbinghaus retention strength to 1.0."""
        pass

    @abstractmethod
    def retrieve(self, query: str, limit: int = 5) -> List[MemoryItem]:
        """Retrieves using Jaccard token similarity. Latency Budget: < 30ms."""
        pass
```

---

## 3. Data-Flow and Control-Flow Diagrams

### 3.1 Data-Flow Pipeline
```
[Environmental Inputs] ──► [World Model Bayesian Update]
                                    │
                                    ▼
[Epistemic Queries]   ◄── [Memory Engine Retrieval]
        │
        ▼
 [Active Planner] ─────► [HTN Decomposition] ──► [MCTS Optimization]
                                                      │
                                                      ▼
 [DAG Execution Queue]  ◄── [Simulation Engine (VaR Check)]
        │
        ▼
[Governance Policy Filter] (Clear / Veto)
        │
        ▼
   [Execution] ───────► [Post-Execution Measurement] ──► [Feedback Loop (TextGrad)]
```

### 3.2 Control-Flow and Failure Propagation Graph
```
        [Cognitive Kernel Loop]
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
 [Normal Execution]   [System Failure]
        │                   │
        ▼                   ▼
 [Success Metrics]     [Bus publishes FAILURE_EVENT]
        │                   │
        ▼                   ▼
 [Memory Save]        [Governance Veto / Rollback Strategy]
                            │
                            ▼
                      [Replan / Restore Last Checkpoint]
```

---

## 4. Evaluation and Benchmarking Strategy

All subsystems must pass objective mathematical benchmarks prior to any code integration:

1. **Planning System**:
   - *Benchmark*: Dynamic replanning test under unexpected runtime step failure.
   - *Success Criteria*: Success rate of $100\%$ on topological repair within $150\text{ ms}$.

2. **World Model**:
   - *Benchmark*: Counterfactual causal prediction vs actual simulated variables.
   - *Success Criteria*: Prediction calibration mean squared error (MSE) $< 0.05$.

3. **Memory Engine**:
   - *Benchmark*: Exponential decay Ebbinghaus consolidation simulation.
   - *Success Criteria*: Retained items must precisely match the theoretical decay curve: $S(t) = e^{-rt}$.

4. **Simulation Engine**:
   - *Benchmark*: Probabilistic rollout scenarios and Value-at-Risk calculation.
   - *Success Criteria*: VaR estimation error $< 1\%$ across $10,000$ Monte Carlo trials.
