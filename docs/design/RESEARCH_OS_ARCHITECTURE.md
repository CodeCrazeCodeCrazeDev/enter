# Scientific Computing and Research Operating System (Research OS)
## Formal Architecture Specification (RFC-001)

This document defines the formal architecture, design specifications, and interfaces of the **Research Operating System (Research OS)**—a next-generation scientific computing platform that institutionalizes the scientific method. Research OS is fully decoupled from, and acts as a foundation layer for, execution clients like the Autonomous Economic Agent Network (AEAN).

---

## 1. Core Architectural Principles

Research OS is governed by five structural architectural axioms:
1. **The Scientific Kernel**: No assertion or claim can exist or propagate without rigorous adherence to the scientific method (Observation → Question → Literature Review → Hypothesis → Prediction → Experimentation → Analysis → Peer Review → Publication → Archive).
2. **Absolute Evidence-Centricity**: Information is never trusted by default. Every claim must carry traceable lineage, confidence scores, validation status, and source provenance leading back to concrete, immutable evidence nodes.
3. **Strict Separation of Concerns**: Core scientific infrastructure is decoupled from domain-specific workflows. The orchestrator never knows the physical details of storage backends, and agents are pluggable execution processors.
4. **Declarative Execution**: Workflows are defined using a declarative **Workflow Definition Language (WDL)** specifying nodes, parallel routes, loops, and governance gates.
5. **Event-Driven Concurrency**: Components are reactive and communicate exclusively via an asynchronous Event Bus, avoiding direct orchestration coupling.

---

## 2. Component Boundaries

Research OS is structured in six horizontal and vertical layers, guaranteeing that domain execution layers (e.g. AEAN) never own or bypass core research logic.

```
+---------------------------------------------------------------------------------+
|                                APPLICATION LAYER                                |
|        (AEAN Organism, AlphaAlgo Research, Healthcare, Robotics Labs)          |
+----------------------------------------+----------------------------------------+
                                         | Ingests publications/theories
                                         v
+---------------------------------------------------------------------------------+
|                                RESEARCH WORKFLOWS                               |
|        (AI Research, Quantitative Finance, Biology, Systems Engineering)        |
+----------------------------------------+----------------------------------------+
                                         | Orchestrates execution
                                         v
+----------------------------------------+----------------------------------------+
|                                PLUGIN RUNTIME                                   |
|   (Agent Plugins, Reviewers, Exec Backends, Evidence Providers, Exporters)      |
+-------------------+--------------------+--------------------+-------------------+
                    |                    |                    |
                    v                    v                    v
+-------------------+--------------------+--------------------+-------------------+
|      GOVERNANCE ENGINE                 |        EVENT BUS & METRICS             |
|  (Ethics, Security, Quality, Capital)  | (Decoupled metrics via subscriptions)  |
+-------------------+--------------------+--------------------+-------------------+
                    |                                         |
                    +--------------------+--------------------+
                                         | Interacts via
                                         v
+---------------------------------------------------------------------------------+
|                                REPOSITORY LAYER                                 |
|                  (Decouple storage engines from workflow tasks)                  |
+----------------------------------------+----------------------------------------+
                                         | Resolves queries
                                         v
+---------------------------------------------------------------------------------+
|                                 STORAGE ENGINE                                  |
| (Knowledge Graph  |  Vector DB  |  Doc Store  |  Relational DB  |  Artifact Store) |
+---------------------------------------------------------------------------------+
```

---

## 3. Artifact Schemas

All data produced or consumed in Research OS is defined as a typed, frozen, immutable **Artifact**. Every artifact is crytographically verifiable and strictly tracked.

### 3.1 Common Base Schema Header
Every artifact contains a standardized `Metadata` block:
```python
class ArtifactMetadata(BaseModel):
    uuid: UUID
    version: int
    lineage_parent_uuids: List[UUID]
    author: str  # "agent_name" or "human_id"
    timestamp: float
    confidence: float  # [0.0, 1.0]
    validation_status: str  # "PENDING" | "VALIDATED" | "FALSIFIED"
    digital_signature: str  # HMAC or SHA-256 integrity hash over content
    metadata_fields: Dict[str, Any]
```

### 3.2 Key Core Artifact Types
1. **ResearchProject**: Tracks active project state, funding allocation, and metrics goals.
2. **ResearchProposal**: Describes research goals, initial observations, and domain.
3. **ResearchQuestion**: Specific question under investigation.
4. **LiteratureCorpus**: Catalog of referenced papers, datasets, and patents.
5. **KnowledgeGapAnalysis**: Identified holes in current literature.
6. **Hypothesis**: Testable scientific assertion, with predicted expectations.
7. **ExperimentDesign**: Specifications, execution backend requirements, parameters, and code.
8. **ExperimentResult**: Raw metrics, execution traces, artifacts generated, logs.
9. **StatisticalReport**: Hypotheses validation status, p-values, deflated Sharpe ratio, etc.
10. **PeerReviewCritique**: Systematic evaluation from reviewer plugins.
11. **Publication**: Peer-reviewed reports, benchmarks, and external-facing papers.
12. **DecisionRecord / GovernanceDecision**: Audit log of governance panel votes, outcomes, and veto justifications.

---

## 4. Event Model

The Research OS Event Bus uses a publisher-subscriber model. Subscribing components compile institutional metrics without injecting analytics directly into execution paths.

### 4.1 Event Schemas
All events carry a unique sequence ID, timestamp, and actor details:

| Event Type | Payload | Trigger |
| :--- | :--- | :--- |
| `WorkflowStarted` | `workflow_id, domain, project_id` | At the initialization of a WDL execution. |
| `ArtifactCreated` | `artifact_id, artifact_type, author` | When any immutable artifact is committed to repository. |
| `ExperimentCompleted` | `experiment_id, backend, metrics, success`| When an experiment run finishes execution. |
| `ReviewFailed` | `review_id, artifact_id, critique_summary`| When a Peer Review Committee fails an artifact. |
| `GovernanceRejected` | `governance_id, board, reason` | When a Governance Board issues a veto or requested revision. |
| `PublicationAccepted` | `publication_id, citation_graph_id` | When a validated paper is successfully published and archived. |

---

## 5. Plugin Contracts

Every processing agent, execution engine, reviewer, and data loader is implemented as a **Plugin** registered with the core engine. This makes the system extremely customizable.

### 5.1 Abstract Interfaces

```python
class IAgentPlugin(ABC):
    """Protocol for processing units (formerly independent agents)."""
    @abstractmethod
    async def process(self, context: ExecutionContext, inputs: Dict[str, BaseArtifact]) -> BaseArtifact:
        pass

class IGovernancePlugin(ABC):
    """Interface for programmatic governance rules (e.g. Ethics, Capital)."""
    @abstractmethod
    async def review(self, context: ExecutionContext, artifact: BaseArtifact) -> GovernanceDecision:
        pass

class IExperimentBackend(ABC):
    """Pluggable backends for running scientific trials."""
    @abstractmethod
    async def execute(self, design: ExperimentDesign) -> ExperimentResult:
        pass

class IEvidenceProvider(ABC):
    """Abstract adapters for scientific search engines and paper databases."""
    @abstractmethod
    async def search(self, query: str) -> LiteratureCorpus:
        pass
```

---

## 6. Workflow Definition Language (WDL)

Workflows are described declaratively via YAML or JSON. This permits easy verification of research paths before running.

### 6.1 Schema Specification
```yaml
workflow:
  id: "ai_hyperparameter_opt"
  domain: "ai_research"
  version: "1.0.0"
  stages:
    - id: "lit_review"
      type: "ingestion"
      provider: "semantic_scholar"
      required_artifacts: ["ResearchQuestion"]
      produced_artifacts: ["LiteratureCorpus"]
      transition_conditions:
        - condition: "LiteratureCorpus.confidence > 0.7"
          next_stage: "hypothesis_gen"

    - id: "hypothesis_gen"
      type: "generation"
      agent: "ExecutiveDirector"
      required_artifacts: ["LiteratureCorpus"]
      produced_artifacts: ["Hypothesis"]
      governance_gates:
        - board: "EthicsReviewBoard"
          on_reject: "terminate"
      transition_conditions:
        - condition: "success"
          next_stage: "experiment_design"

    - id: "experiment_design"
      type: "design"
      agent: "ExperimentScientist"
      required_artifacts: ["Hypothesis"]
      produced_artifacts: ["ExperimentDesign"]
      transition_conditions:
        - condition: "success"
          next_stage: "execution"

    - id: "execution"
      type: "experiment"
      backend: "ml_training_sandbox"
      required_artifacts: ["ExperimentDesign"]
      produced_artifacts: ["ExperimentResult"]
      failure_policy:
        retry_count: 3
        on_exhausted: "escalate_to_human"
      transition_conditions:
        - condition: "success"
          next_stage: "statistical_analysis"

    - id: "statistical_analysis"
      type: "analysis"
      agent: "Statistician"
      required_artifacts: ["ExperimentResult"]
      produced_artifacts: ["StatisticalReport"]
      transition_conditions:
        - condition: "StatisticalReport.p_value < 0.05"
          next_stage: "peer_review"
        - condition: "StatisticalReport.p_value >= 0.05"
          next_stage: "hypothesis_gen" # FEEDBACK LOOP

    - id: "peer_review"
      type: "review"
      board: "PeerReviewCommittee"
      required_artifacts: ["StatisticalReport"]
      produced_artifacts: ["PeerReviewCritique"]
      transition_conditions:
        - condition: "PeerReviewCritique.approved"
          next_stage: "publication"
        - condition: "not PeerReviewCritique.approved"
          next_stage: "experiment_design" # REVISION LOOP

    - id: "publication"
      type: "archive"
      agent: "PublicationEditor"
      required_artifacts: ["PeerReviewCritique"]
      produced_artifacts: ["Publication"]
      governance_gates:
        - board: "ScientificQualityBoard"
          on_reject: "request_revision"
```

---

## 7. Governance Model

Governance panels possess absolute binding authority to ensure ethical adherence and resource optimization.

### 7.1 Core Governance Boards
1. **Ethics Review Board**: Audits hypothesis generation and experimental goals (e.g. data privacy, safety boundaries).
2. **Scientific Quality Board**: Validates statistical soundess, statistical power, and p-value corrections (e.g. Bonferroni).
3. **Security Board**: Audits experiment code, sandbox execution limits, and dependency vulnerabilities.
4. **Capital & Resource Allocation Board**: Allocates CPU/GPU budgets and limits compute usage according to priorities.

### 7.2 Decision Outcomes
- **Approve**: Artifact is certified; workflow transitions to next phase.
- **Reject**: Workflow is permanently terminated or cancelled.
- **Request Revision**: Flow returns to an upstream state with explicit review notes attached.
- **Escalate**: Halts execution and notifies human review teams for key security/impact boundaries.
- **Suspend / Archive / Require Independent Review**: Structural holds for high-risk proposals.

---

## 8. Repository Interfaces

The Repository Layer acts as a secure proxy between workflows/agents and the underlying physical storage backends. No agent or workflow has direct database handles.

```python
class IResearchRepository(ABC):
    """Saves and loads all immutable scientific artifacts."""
    @abstractmethod
    def save_artifact(self, artifact: BaseArtifact) -> None:
        pass

    @abstractmethod
    def get_artifact(self, uuid: UUID) -> Optional[BaseArtifact]:
        pass

    @abstractmethod
    def list_artifacts_by_type(self, artifact_type: Type[T]) -> List[T]:
        pass

    @abstractmethod
    def get_lineage_tree(self, artifact_uuid: UUID) -> List[BaseArtifact]:
        pass
```

---

## 9. Knowledge Graph Ontology

The Knowledge Graph represents the institutional state of verified understanding, continuously evolving as claims are accepted, rejected, or contradicted.

```
                  +--------------------------+
                  |       ConceptNode        |
                  +------------+-------------+
                               |
                               | defines
                               v
                  +------------+-------------+
                  |       TheoryNode         | <----------+
                  +------------+-------------+            |
                               |                          | contradicts
                               | supported_by             |
                               v                          |
                  +------------+-------------+            |
  +-------------> |       ClaimNode          | -----------+
  |               +------------+-------------+
  |                            |
  | verified_by                | grounded_in
  |                            v
+--+---------+    +------------+-------------+
| Experiment |    |      EvidenceNode        |
+------------+    +--------------------------+
```

### 9.1 Ontological Nodes
* **ConceptNode**: Formal scientific vocabularies, definitions, and domains.
* **TheoryNode**: High-level conceptual frameworks (aggregations of claims).
* **ClaimNode**: Highly specific assertions (with confidence, verified date, limit constraints).
* **EvidenceNode**: Citations, raw observations, published third-party papers, or sandbox-tested outcomes.
* **ContradictionNode**: Active logical inconsistencies flagged between Claims or Evidence.

### 9.2 Relationship Edges
* `SUPPORTS` / `FALSIFIES` (Claim ➔ Claim, Evidence ➔ Claim)
* `CONTRADICTS` (Claim ➔ Claim)
* `DEPENDS_ON` (Experiment ➔ Theory)
* `GROUNDED_IN` (Claim ➔ Evidence)

---

## 10. Execution Semantics

Unlike simple pipeline DAGs, scientific discovery is iterative. The Workflow Engine supports:
1. **Concurrency**: Multiple hypotheses or experiment variants executing in parallel.
2. **Dynamic Conditional Execution**: Execution paths branching based on statistical criteria (e.g. standard deviation thresholds).
3. **Feedback Loops**: Looping back to hypothesis generation when predictions are falsified, or to experiment design on peer-review notes.
4. **Event-Driven Task Scheduling**: Tasks are scheduled dynamically by subscribing to `ArtifactCreated` events.

---

## 11. Failure Recovery & Rollback Policies

Scientific experiments are prone to physical failures or falsified hypotheses:
- **Sandbox Failures (Technical)**: Retries, alternative sandbox container instantiation, or escalation if compute budgets are exhausted.
- **Scientific Falsification (Logical Rollbacks)**: If an experiment falsifies a hypothesis (P-value > threshold), the hypothesis status is marked as `FALSIFIED`. An event `HypothesisFalsified` triggers a logical rollback, suspending all downstream experiment designs and prompting the `HypothesisGenerator` to propose a revision or competing hypothesis.

---

## 12. Security Model

Security is paramount in open-ended research systems:
- **Digital Integrity**: Every artifact is signed with an integrity hash matching its exact contents, preventing modification.
- **Auditable Lineage**: An immutable chain of parent UUIDs records the provenance of every single artifact.
- **Sandbox Confinement**: Code is run exclusively in isolated execution containers with hard restrictions on internet access, storage, and runtime duration.

---

## 13. Observability

To inspect the system state and evaluate institutional health:
- **Event Ledger**: An append-only table recording every event on the event bus.
- **Telemetry**: Running statistics on latency, compute cost (simulated or real), and memory token consumption.
- **Institutional Dashboard**: A programmatic summary computing the primary success indicators in real-time.

---

## 14. Testing Strategy

1. **Unit Tests**: Complete isolation test for metadata parsing, WDL validation, and repository layer operations.
2. **Contract Tests**: Verifying that plugin adapters strictly implement and respect interface boundaries.
3. **Loop-Simulation Tests**: Comprehensive executions of both AI Research and Quantitative Finance workflows to verify feedback loops and governance rejections.
4. **Chaos Testing**: Injecting failure states into backends (e.g., throwing mock compilation exceptions) to evaluate failure recovery.

---

## 15. Evolution & Versioning Strategy

- **Artifact Versioning**: Artifacts utilize incremental integers. When modified, a new copy is created with `version = parent.version + 1`, appending the parent's UUID to `lineage_parent_uuids`.
- **WDL Migration**: Workflows specify semantic version numbers (`x.y.z`). Execution states are tied to specific WDL versions to prevent run errors mid-workflow.
