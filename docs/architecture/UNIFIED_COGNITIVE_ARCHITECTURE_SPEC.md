# Unified Cognitive Architecture Specification
## AEAN / EIOS / EOS / APODEX Cognitive Operating System (4-Layer Taxonomy)

---

## 1. Executive Summary & First-Principles Foundation

The **Apodex Cognitive Operating System** unifies Research OS, EIOS, EOS, AEAN, and APODEX into a singular, integrated, 4-layer cognitive operating system. Rather than treating these subsystems as independent platforms with overlapping responsibilities, this architecture establishes strict non-overlapping layer boundaries, explicit communication interfaces, and unified Active Inference state handoffs.

### The Unified 4-Layer Taxonomy

```
+---------------------------------------------------------------------------------+
| LAYER 1: RESEARCH OS (Scientific & Research Subsystem)                          |
| - Literature Review & Paper Corpus Ingestion                                    |
| - Transferable Engineering Principle Extraction                                 |
| - Formal Hypothesis Formulation & Experimental Design                           |
| - Statistical Validation & Empirical Evidence Verification                      |
+---------------------------------------------------------------------------------+
                                       | Hypothesis H_i & Principles P_k
                                       v
+---------------------------------------------------------------------------------+
| LAYER 2: EIOS / EOS (Execution, Orchestration & Venture Engine Subsystem)       |
| - Continuous Opportunity Sensing & Anomaly Detection                             |
| - Active Inference Expected Free Energy (EFE) DAG Compilation                   |
| - Venture Capital Allocation & Unit Economics Optimization                      |
| - GTM Simulator & External Business Loop Execution                              |
+---------------------------------------------------------------------------------+
                                       | Execution Plan DAG & Directives
                                       v
+---------------------------------------------------------------------------------+
| LAYER 3: AEAN (Autonomous Economic Agent Network Subsystem)                      |
| - Multi-Agent Specialization & Lifecycle Management                             |
| - HiveMind Token Bidding & Auction-based Task Allocation                       |
| - Peer-to-Peer Negotiation, Arbitration & Contractual Settlement              |
| - Dynamic Skill Invention & Procedural Tool Synthesis                           |
+---------------------------------------------------------------------------------+
                                       | Trajectories & Observation Events
                                       v
+---------------------------------------------------------------------------------+
| LAYER 4: APODEX (World Model & Decision Substrate Subsystem)                   |
| - Multi-Graph Continuous World Model (E-K-C-T-U)                                |
| - Pearl Structural Causal Model (SCM) & Do-Calculus Interventions               |
| - Recursive Conjugate Bayesian Belief Updates (Beta/Gaussian)                  |
| - Multi-Tier Memory Consolidation (Working, Episodic, Semantic, Procedural)    |
| - Immutable Safety Core & Tiered Approval Governance                            |
+---------------------------------------------------------------------------------+
```

---

## 2. Layer Definitions, Capabilities & Interface Contracts

### 2.1 Layer 1: Research OS (Research Layer)
* **Single Responsibility**: Ingest academic literature, extract transferable engineering principles, synthesize hypotheses, design formal validation experiments, and verify scientific claims.
* **Non-Overlapping Boundaries**: Does NOT execute market operations, allocate venture capital, spawn execution agents, or manage world model graphs.
* **Formal Active Inference Interface**:
```python
class IResearchOSLayer(ABC):
    @abstractmethod
    def conduct_literature_review(self, query: str) -> List[ResearchPrinciple]:
        """Queries registered research corpus and synthesizes principles."""
        ...

    @abstractmethod
    def formulate_hypothesis(self, domain_context: Dict[str, Any]) -> Hypothesis:
        """Formulates testable hypotheses with epistemic prior bounds."""
        ...

    @abstractmethod
    def validate_hypothesis_statistically(
        self, hypothesis_id: str, empirical_results: Dict[str, Any]
    ) -> HypothesisValidationResult:
        """Runs t-tests/chi-squared tests to confirm hypothesis validity."""
        ...
```

### 2.2 Layer 2: EIOS / EOS (Execution & Venture Layer)
* **Single Responsibility**: Sense market opportunities via Active Inference Expected Free Energy ($G$), compile executable workflow DAGs, optimize unit economics, manage venture lifecycle transitions, and simulate GTM strategies.
* **Non-Overlapping Boundaries**: Does NOT conduct literature extraction, manage low-level agent auctions, or store persistent Bayesian world beliefs directly.
* **Formal Active Inference Interface**:
```python
class IEIOSEOSLayer(ABC):
    @abstractmethod
    def sense_opportunity_anomalies(self, hypotheses: List[Hypothesis]) -> List[OpportunityNode]:
        """Senses market anomalies and calculates Expected Free Energy (EFE)."""
        ...

    @abstractmethod
    def compile_execution_dag(self, opportunity: OpportunityNode) -> WorkflowDAG:
        """Compiles Active Inference directives into executable DAG workflows."""
        ...

    @abstractmethod
    def evaluate_venture_unit_economics(self, venture_state: Dict[str, Any]) -> UnitEconomicsReport:
        """Calculates LTV/CAC ratios, payback periods, and runway parameters."""
        ...
```

### 2.3 Layer 3: AEAN (Autonomous Economic Agent Network Layer)
* **Single Responsibility**: Orchestrate specialized multi-agent teams, run token-bidding auctions for task allocation, execute peer negotiations, synthesize procedural skills, and enforce agent budget constraints.
* **Non-Overlapping Boundaries**: Does NOT alter SCM causal links directly, evaluate high-level venture stages, or generate scientific research papers.
* **Formal Active Inference Interface**:
```python
class IAEANLayer(ABC):
    @abstractmethod
    def bid_tasks_hivemind(self, dag_nodes: List[DAGNode]) -> Dict[str, AgentAssignment]:
        """Runs competitive token bidding among specialized agents."""
        ...

    @abstractmethod
    def execute_multi_agent_strategy(self, assignments: Dict[str, AgentAssignment]) -> StrategyExecutionTrace:
        """Executes assigned tasks concurrently and aggregates agent outputs."""
        ...

    @abstractmethod
    def synthesize_procedural_skill(self, trajectory: List[TrajectoryStep]) -> Optional[ToolSchema]:
        """Packages repetitive successful execution steps into reusable procedural tools."""
        ...
```

### 2.4 Layer 4: APODEX (World Model & Decision Substrate Layer)
* **Single Responsibility**: Maintain the persistent state of truth across 5 multi-graphs (Entity, Knowledge, Causal, Temporal, Uncertainty), run do-calculus counterfactuals, update Bayesian belief distributions, consolidate short/long-term memory, and enforce immutable safety policies.
* **Non-Overlapping Boundaries**: Does NOT compile high-level business plans, run agent bidding algorithms, or perform raw web scraping.
* **Formal Active Inference Interface**:
```python
class IAPODEXSubstrateLayer(ABC):
    @abstractmethod
    def query_do_calculus(self, intervention_var: str, value: float) -> Dict[str, float]:
        """Executes Judea Pearl do-operator (do(X = x)) over the Structural Causal Model."""
        ...

    @abstractmethod
    def update_bayesian_belief(self, belief_id: str, trials: int, successes: int) -> BeliefState:
        """Recursively updates Beta/Gaussian conjugate prior distributions."""
        ...

    @abstractmethod
    def consolidate_memory_tiers((self) -> ConsolidationReport:
        """Transfers episodic traces into semantic facts and long-term lessons."""
        ...
```

---

## 3. Closed-Loop Active Inference Mathematics

The platform operates as a unified **Active Inference System** minimizing Expected Free Energy ($G$):

$$G(\pi) = - \underbrace{\mathbb{E}_{q(o, \theta | \pi)} [\log p(o | \theta) - \log q(\theta | \pi)]}_{\text{Epistemic Value (Information Gain / Curiosity)}} - \underbrace{\mathbb{E}_{q(o | \pi)} [\log p(o)]}_{\text{Pragmatic Value (Goal Utility)}}$$

Where:
1. **Layer 1 (Research OS)** maximizes **Epistemic Value** by seeking research domains with high information entropy $\mathbb{H}[\theta]$.
2. **Layer 2 (EIOS/EOS)** balances Epistemic and Pragmatic goals to calculate option utility and compile optimal execution DAGs $\pi^* = \arg\min_{\pi} G(\pi)$.
3. **Layer 3 (AEAN)** executes action policies $\pi^*$ via market-based agent bidding while collecting real-world observation trajectories $o$.
4. **Layer 4 (APODEX)** updates the internal generative world model $p(o, \theta)$ via variational Bayesian update:

$$q^*(\theta) = \arg\min_{q} D_{\text{KL}}(q(\theta) \parallel p(\theta | o))$$

---

## 4. Architectural Non-Duplication Principles

1. **Single Source of Truth**: All state and belief distributions reside exclusively in **Layer 4 (APODEX World Model)**. Layers 1-3 read and publish state update events.
2. **Single Planning/Scheduling Subsystem**: DAG compilation is strictly owned by **Layer 2 (EIOS/EOS)**. Layer 3 agents execute DAG nodes without re-indexing task graphs.
3. **Single Multi-Agent Bidding Registry**: Token bidding and agent allocation are strictly owned by **Layer 3 (AEAN HiveMind)**.
4. **Single Research & Evidence Ingestion Engine**: Academic literature review and paper corpus extraction are strictly owned by **Layer 1 (Research OS)**.
