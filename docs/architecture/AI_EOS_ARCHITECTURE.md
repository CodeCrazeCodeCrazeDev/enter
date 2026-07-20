# AI-EOS — Autonomous Entrepreneurial Research & Execution Operating System
## Authoritative Architecture Specification & Contract (v1.0.0)

This is the canonical, binding architecture contract for AI-EOS. No code changes, subsystem implementations, or integrations may occur without conforming to the design patterns, bounded contexts, dependency boundaries, and API stability rules established in this contract.

---

## 1. Executive Summary & Ubiquitous Language

AI-EOS is the formal, full-lifecycle operating system superset that wraps and governs the Autonomous Economic Agent Network (AEAN), the Autonomous Research & Execution Core Systems (ARCS), the Organism Flywheel, and their underlying memory substrates. Rather than treating these layers as independent systems, AI-EOS acts as the master coordinating operating system.

### 1.1 Ubiquitous Language Definition

To establish absolute semantic alignment across all subsystems, agents, and operators, we define the following ubiquitous terms:

*   **Venture Cell**: The smallest isolated unit of business operation. Each Venture Cell maintains its own independent P&L, namespace, sub-agent composition, and local episodic memory.
*   **Belief State**: The probability distribution over market, customer, competitor, and regulatory states modeled by the system.
*   **Active Inference Loop**: The core decision process that jointly minimizes model uncertainty (epistemic value/information gain) and expected free energy (maximizing economic utility).
*   **Expected Free Energy ($G$)**: The objective function for a policy, combining expected economic utility, risk penalty, compute cost, and governance barriers.
*   **Research OS**: The scientific execution platform where venture hypotheses are registered, planned, sandboxed, and statistically validated before any capital is committed.
*   **Research Ledger**: An immutable, append-only chronological record of all registered hypotheses, executed experiments, and validated facts.
*   **Capability**: A modular, version-controlled, and audited behavior (prompt strategy, routing policy, tool invocation, or fine-tuned model) registered with the system.
*   **Capability Registry & Lineage**: The definitive, versioned database storing the origin, evidence, benchmarks, dependencies, risk scores, and approval/rollback records of all system Capabilities.
*   **Decision Provenance**: An immutable, cryptographically verifiable record detailing the evidence, assumptions, model versions, experiments, and approval chains behind a strategic decision.
*   **Meta-Governance**: The governing subsystem responsible for reviewing proposed architectural changes, measuring technical debt, and enforcing complexity budgets over the governance system itself.
*   **Institutional Knowledge Graph (IKG)**: A unified relational representation mapping research papers, experiments, datasets, features, models, capabilities, agents, venture cells, and decisions to provide complete multi-layered traceability.

---

## 2. Bounded Contexts, System Ownership & Context Map

AI-EOS decomposes its operations into exactly nine canonical Bounded Contexts, each with an explicit ownership boundary, inputs, outputs, and invariants.

```
       +-------------------------------------------------------------------------+
       |                               AI-EOS OS                                 |
       |                                                                         |
       |   +-----------------------+                    +--------------------+   |
       |   |       Research        |                    |     Executive      |   |
       |   |      Operating        | ──[Publishes]────> |    Intelligence    |   |
       |   |        System         |   (Research Ledger)|                    |   |
       |   +-----------+-----------+                    +---------+----------+   |
       |               |                                          |              |
       |       Updates |                                          | Orchestrates |
       |               v                                          v              |
       |   +-----------+-----------+                    +---------+----------+   |
       |   |        Memory &       |                    |     Execution      |   |
       |   |       Knowledge       | ◄──[Retrieves]─────|      Systems       |   |
       |   |     Infrastructure    |                    |    (AEAN/ARCS)     |   |
       |   +-----------+-----------+                    +---------+----------+   |
       |               ^                                          |              |
       |               | Updates (Proven Capabilities)            | Runs Inside  |
       |               |                                          v              |
       |   +-----------+-----------+                    +---------+----------+   |
       |   |   Frontier Cap/Model  | ◄──[Monitors]──────|      Sandbox       |   |
       |   |      Intelligence     |                    |    Environment     |   |
       |   +-----------------------+                    +--------------------+   |
       +-------------------------------------------------------------------------+
```

### 2.1 Bounded Context Definitions & Ownership

1.  **System Composition & Composition Platform Context (`ai_eos.composition`)**
    *   *Owner*: Systems Engineering Core.
    *   *Mission*: Provide thread-safe Dependency Injection (DI), plugin loading, lifecycle coordination, configuration schemas, and service resolution.
2.  **Research Operating System Context (`ai_eos.research`)**
    *   *Owner*: Chief Scientist Division.
    *   *Mission*: Manage scientific hypothesis testing, experiment execution inside Sandboxes, statistical verification, and recording outcomes to the immutable Research Ledger.
3.  **Memory & Knowledge Infrastructure Context (`ai_eos.memory`)**
    *   *Owner*: Data & Memory Operations Division.
    *   *Mission*: Manage T0-T4 multi-tier storage, provide hybrid semantic-structural retrieval, and maintain the Institutional Knowledge Graph (IKG).
4.  **Executive Intelligence Context (`ai_eos.executive`)**
    *   *Owner*: Executive & Portfolio Management Division.
    *   *Mission*: Resolve constrained multi-objective optimization (portfolio routing, budget allocation, opportunity ranking) and execute the Active Inference loop.
5.  **Execution Systems Interface Context (`ai_eos.execution`)**
    *   *Owner*: Platform Integration Division.
    *   *Mission*: Wrap the legacy AEAN `Organism` and ARCS service registry behind stable, decoupled execution adapters.
6.  **Frontier Capability & Model Intelligence Context (`ai_eos.capability`)**
    *   *Owner*: Applied Research & Capability Division.
    *   *Mission*: Discover, distill, validate, and promote external agent and model patterns into the central Capability Registry & Lineage Database.
7.  **Governance & Meta-Governance Context (`ai_eos.governance`)**
    *   *Owner*: Governance, Risk, & Compliance (GRC) Council.
    *   *Mission*: Enforce security, financial, legal, and ethical policy gates, and apply complexity budgets to the platform’s self-evolution.
8.  **Validation Platform Context (`ai_eos.validation`)**
    *   *Owner*: Quality Assurance & Reliability Division.
    *   *Mission*: Run continuous replay tests, chaos injection, performance profiling, and architectural conformance validation.
9.  **Progressive Deployment Context (`ai_eos.deployment`)**
    *   *Owner*: Operations & Release Division.
    *   *Mission*: Coordinate staged rollout (Sandbox -> Shadow -> Canary -> Production) and execute automated rollback on SLA degradation or metric drift.

---

## 3. Package Dependency & Allowed Import Rules

To prevent architectural erosion, circular dependencies, and high coupling, the system enforces strict import rules.

```
+-----------------------------------------------------------------------------------+
| ai_eos.composition                                                                |
+-----------------------------------------------------------------------------------+
       ▲
       │ (Imports composition only)
+-----------------------------------------------------------------------------------+
| ai_eos.domain & ai_eos.interfaces                                                 |
+-----------------------------------------------------------------------------------+
       ▲
       │ (Imports domain and interfaces only)
+-----------------------------------------------------------------------------------+
| ai_eos.research, ai_eos.memory, ai_eos.executive, ai_eos.capability, etc.        |
+-----------------------------------------------------------------------------------+
       ▲
       │ (Coordinates and implements adapters)
+-----------------------------------------------------------------------------------+
| ai_eos.execution (AEAN / ARCS Adapters)                                           |
+-----------------------------------------------------------------------------------+
```

### 3.1 Strict Dependency Rules

1.  **Domain Isolation**: Core domain objects (`ai_eos/domain/`) and service interfaces (`ai_eos/interfaces/`) must contain **zero** imports from infrastructure packages, database adapters, LLM clients, or concrete execution systems.
2.  **Top-Down Dependencies**: Higher-level orchestration modules (e.g. `ai_eos/executive/`) may only interact with lower-level subsystems (like `ai_eos/memory/` or `ai_eos/research/`) via their public interfaces. Direct imports of concrete class implementations from other contexts are strictly forbidden.
3.  **Composition Rules**: Only the Dependency Injection container (`ai_eos/composition/`) is permitted to import concrete class implementations across all contexts to register and wire them.
4.  **No Execution Contamination**: Neither `aean` nor `arcs` packages may directly import anything from `ai_eos`. All interactions must flow from AI-EOS to the execution backends via adapters.

---

## 4. Event Taxonomy & Versioning Strategy

AI-EOS operates as an event-driven meta-system. Every major state transition must publish a schema-conformant event to the central event bus.

### 4.1 Event Taxonomy

All events are fully serializable and inherit from a base `DomainEvent`.

*   `VentureCellCreatedEvent` (v1.0): Published when a new venture cell is initialized with a distinct memory namespace and initial capital allocation.
*   `HypothesisRegisteredEvent` (v1.0): Published when a new scientific hypothesis is registered in the Research OS.
*   `ExperimentExecutedEvent` (v1.0): Published when an experiment completes execution inside the Sandbox, carrying reproducibility hashes.
*   `FactValidatedEvent` (v1.0): Published when statistical validation confirms a hypothesis, making it a validated T2 Fact.
*   `CapabilityDiscoveredEvent` (v1.0): Published when the Frontier Capability Intelligence layer identifies a candidate capability.
*   `CapabilityPromotedEvent` (v1.0): Published when a capability clears all validation, sandboxing, and architecture governance checks, and is promoted to production.
*   `SLAExceptionDetectedEvent` (v1.0): Published when runtime monitors or validators detect performance, budget, or safety anomalies.
*   `CapabilityRolledBackEvent` (v1.0): Published when an automated rollback is triggered, reverting the system configuration and blacklisting the failed capability.

### 4.2 Versioning Strategy

*   **API / Code Versioning**: AI-EOS uses strict Semantic Versioning (SemVer 2.0.0). Breaking interface modifications require a major version bump.
*   **Event Schema Versioning**: Event payloads must carry a `schema_version` header. Schema changes must be backward-compatible (only adding optional fields). If a breaking change to an event schema is required, a new event class must be declared (e.g., `FactValidatedEventV2`).

---

## 5. Subsystem Product Specifications

To preserve explicit architectural boundaries, every subsystem of AI-EOS is treated as a first-class product with clear contracts.

### 5.1 Research Operating System
*   **Mission**: Standardize, record, and execute scientific venture and technical experiments under strict statistical controls to eliminate human bias.
*   **Inputs**: Proposed business hypotheses, parameter spaces, historical datasets, simulation parameters.
*   **Outputs**: Replicable experiment records, validated/refuted facts, reproducibility hashes, dataset lineages.
*   **Public API**:
    *   `register_hypothesis(hypothesis: Hypothesis) -> UUID`
    *   `plan_experiment(hypothesis_id: UUID, setup: Dict) -> UUID`
    *   `run_experiment(experiment_id: UUID) -> ExperimentOutcome`
    *   `validate_statistically(outcome_id: UUID) -> ValidationVerdict`
*   **Internal Invariants**:
    *   Experiments must run within fully isolated, resource-constrained Sandboxes.
    *   No experiment may write to the T2/T3 Memory layers unless its validation verdict passes White's Reality Check or multiple-testing corrections with $p < 0.05$.
*   **Performance Objectives**: Sandbox initialization in $<150\text{ ms}$; validation execution in $<200\text{ ms}$.
*   **Failure Modes**: Sandbox timeout, data leakage between training and testing sets, statistical under-powering.
*   **Observability**: Detailed step-by-step telemetry of sandbox resource utilization, training/testing loss curves, and validation p-values.

### 5.2 Memory, Knowledge Infrastructure & Institutional Knowledge Graph
*   **Mission**: Provide a highly organized, temporal-aware repository representing the system's absolute factual and procedural truth.
*   **Inputs**: Validated research artifacts, episodic logs, user preferences, external capability schemas, structural decisions.
*   **Outputs**: Multi-tier memory contexts (T0-T4), cross-referenced Institutional Knowledge Graph (IKG) nodes/edges.
*   **Public API**:
    *   `ingest_artifact(artifact: ResearchArtifact) -> None`
    *   `query_hybrid(query_string: str, filters: Dict) -> List[MemoryItem]`
    *   `get_knowledge_subgraph(center_id: str, depth: int) -> SubGraph`
    *   `propagate_confidence(node_id: UUID) -> None`
*   **Internal Invariants**:
    *   The IKG must enforce perfect relational referential integrity (no dangling edges).
    *   Every T2 Fact or T3 Scenario must maintain a complete lineage back to its originating `ResearchTicket` or `ExperimentExecutedEvent` source.
*   **Performance Objectives**: Hybrid retrieval latency $<200\text{ ms}$ (P95); graph queries $<100\text{ ms}$.
*   **Failure Modes**: Graph cyclic loops, confidence saturation/underflow, namespace leakage across tenants.
*   **Observability**: Hit rate metrics, index compaction logs, and confidence decay analytics.

### 5.3 Executive Intelligence & Active Inference
*   **Mission**: Maximize portfolio economic utility while minimizing expected free energy (epistemic uncertainty and risk) through constrained mathematical optimization.
*   **Inputs**: Belief State, risk models, available venture capital, active opportunities, computed Expected Free Energy values.
*   **Outputs**: Portfolio allocation decisions, opportunity priorities, compute/budget guidelines, risk scores.
*   **Public API**:
    *   `compute_expected_free_energy(policy: Policy) -> float`
    *   `optimize_portfolio(capital_cents: int) -> PortfolioAllocation`
    *   `update_beliefs(observation: Observation) -> BeliefState`
*   **Internal Invariants**:
    *   Decisions must respect hard-gated risk/budget ceilings. No allocation may proceed if its computed risk penalty exceeds the Governance budget.
*   **Performance Objectives**: Active inference evaluation and optimization in $<300\text{ ms}$.
*   **Failure Modes**: Non-convergence of optimization, belief state drift, risk underestimation under high-entropy environments.
*   **Observability**: Active tracked belief entropy scores, optimization residual values, and expected vs. actual utility metrics.

---

## 6. Measurable Phase Exit Criteria

A phase of the AI-EOS implementation is not complete when its code is written; it is complete only when all objective criteria listed below are verified and satisfied.

| Phase | Core Deliverables | Verification Methodology | Mandatory Measurable Exit Criteria |
|---|---|---|---|
| **Phase 0** | Bounded context maps, system specification, and legacy documentation update. | Architectural audit. | 100% of bounded contexts documented; all ADRs accepted; legacy specifications mapped via traceability table. |
| **Phase 1** | DI container, event bus, config, state machine, deterministic IDs, and persistence layers. | Conformance tests. | Zero direct cross-package imports; 100% of DI registrations resolved; event bus publishes and consumes concurrently with zero message loss. |
| **Phase 2** | Hypothesis, Experiment, Dataset, Feature, Model, and Artifact registries with statistical validation. | Statistical tests. | Replicability verified via seed management; statistical validation successfully detects simulated data leakage and correctly filters spurious signals with $p < 0.05$. |
| **Phase 3** | T0-T4 Memory, IKG, provenance graph, temporal versioning, decay rules. | Traceability audit. | 100% of validated research artifacts mapped in IKG; provenance query successfully links a T2 fact back to its exact Sandbox experiment source. |
| **Phase 4** | Planning, active inference loop, Bayesian belief updates, and constrained multi-objective optimizer. | Mathematical simulation. | Decision-making policy successfully selects high-information-value exploratory actions in high-uncertainty scenarios and satisfies resource allocation budgets. |
| **Phase 5** | AEAN & ARCS adapters. | Integration verification. | Integration test executes a simulated flywheel run completely through the adapter layer with zero direct imports from internal execution packages. |
| **Phase 6** | Discovery-to-rollback pipelines, detailed Capability Registry and Lineage Database. | Sandbox test run. | Extracted capabilities successfully compiled and metadata records mapped; sandbox verifies capability isolation. |
| **Phase 7** | Policy gates, Architecture Governance, and Meta-Governance. | Attack simulation. | Attempts to inject duplicate or context-violating capabilities are blocked; complexity budget triggers alert upon artificial code volume expansion. |
| **Phase 8** | Replay, chaos, fault, security, and economic benchmarks. | Test suite execution. | 100% pass on regression and replay tests; system recovers gracefully from injected database/network failures within $<500\text{ ms}$. |
| **Phase 9** | Progressive rollout, capability/flag rollbacks, and kill switches. | Rollback simulation. | Simulated SLA degradation triggers complete automatic rollback to previous stable version within $<100\text{ ms}$. |

---

## 7. Architecture Decision Records (ADRs)

### ADR-001: Active Inference Approximation Policy
*   **Context**: Implementing a full, biologically-inspired variational free energy optimization is computationally prohibitive for a fast-response agent operating system.
*   **Decision**: AI-EOS will implement a high-precision, production-grade active inference approximation. The executive policy will optimize a composite objective function combining expected utility, risk penalty, compute cost, and governance limits, and update its belief state using discrete Bayesian conjugate updates.
*   **Consequences**: Drastically reduced computational latency, high mathematical transparency, and easily configurable cost mode profiles (`max_quality`, `balanced`, `fast_cheap`).

### ADR-002: Separated Research OS and Execution Environments
*   **Context**: Execution engines (AEAN/ARCS) run on rapid, noisy, and stochastic real-world signals (clicks, CTR, etc.). Integrating raw execution outputs directly into memory introduces behavioral drift and noise.
*   **Decision**: All knowledge generation must flow through the **Research OS** first. Hypotheses are registered and evaluated under strict statistical validation (multiple-testing correction, deflated metrics). Only validated and verified artifacts are promoted to Memory.
*   **Consequences**: The memory layer acts as a pristine, high-confidence repository of verified truths, eliminating hallucinations and preventing the system from scaling based on correlational noise.

### ADR-003: Core Metadata Capability Registry
*   **Context**: As the system self-evolves, tracking which sub-agent is running what configuration, which prompt version, and what origin/evidence supports the deployment becomes incredibly complex.
*   **Decision**: AI-EOS mandates a centralized, immutable Capability Registry. Every discovered or distilled capability (from local files, papers, or external codebases) is assigned a unique Capability ID with comprehensive origin, benchmark, risk, dependency, and owner metadata before deployment.
*   **Consequences**: Perfect auditability, instant rollback capabilities, and explicit capability lifecycle tracking.

### ADR-004: Continuous Architecture & Meta-Governance
*   **Context**: Continuous self-evolution can easily lead to spaghetti code, duplication of functions, and ballooning complexity that erodes bounded contexts.
*   **Decision**: Establish a non-bypassable Meta-Governance and Architecture Governance subsystem. Every proposed change (prompt variant, routing path, tool registration) must answer specific architectural coupling checks and fit within a strict complexity budget before staging.
*   **Consequences**: Strong architectural boundaries that remain clean and manageable across infinite self-evolution cycles.

---

## 8. Legacy Document Traceability & Status Matrix

To avoid documentation drift and maintain a clear, single source of truth, we establish the following traceability table:

| Document | Path | Status | Relationship & Traceability Guidance |
|---|---|---|---|
| **AI_EOS_ARCHITECTURE** | `docs/architecture/AI_EOS_ARCHITECTURE.md` | **Active / Authoritative** | The master, controlling architecture contract for AI-EOS. Under this system, AEAN and ARCS are coordinated execution subsystems. |
| **APODEX_SYSTEM_DESIGN** | `APODEX_SYSTEM_DESIGN.md` | **Partially Superseded** | Superseded on the master self-evolution flow by AI-EOS Active Inference and Meta-Governance design. The basic Personal Evolution Profile (PEP) and Verifier node definitions remain valid as subcomponents of the memory and validation contexts. |
| **ARCS_ARCHITECTURE** | `ARCS_ARCHITECTURE.md` | **Subsystem** | Serves as the authoritative domain model for execution/revenue services within the ARCS execution context. Coordinates directly with `ai_eos.execution`. |
| **AEAN_DESIGN** | `apodex/aean/README.md` | **Subsystem** | Serves as the authoritative specification of the 6-stage flywheel micro-cell execution loop. Coordinates directly with `ai_eos.execution`. |
| **IMPLEMENTATION_ROADMAP**| `IMPLEMENTATION_ROADMAP.md` | **Historical Roadmap** | Superseded by the dependency-driven 10-phase sequence outlined in `AI_EOS_ARCHITECTURE.md`. |
| **APODEX2_MEMORY_SYSTEM_DESIGN** | `docs/design/APODEX2_MEMORY_SYSTEM_DESIGN.md` | **Subsystem** | Serves as the technical specification of the underlying 5-tier memory models (T0-T4) and hybrid scoring formula. Maps directly to the `ai_eos.memory` context. |

---

This contract is signed and approved. Any proposed deviation must be submitted through a formal ADR and approved before implementation.
