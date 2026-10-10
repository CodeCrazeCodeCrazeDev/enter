# Transferable Engineering Principles for Autonomous Research OS & AI-EOS Architecture

This document outlines the core engineering principles extracted from state-of-the-art research (300 research publications across papers 1–500) and synthesized inside the evolved `AgentHarness` and `APODEX / AI-EOS` cognitive operating system.

---

## Principle 1: Hexagonal Isolation of Strategic Planning
- **Source Category**: Autonomous Planning & Reasoning
- **Target Subsystem**: `ResearchOS` / Strategic Planning
- **Concept**: Never pollute the strategic planning history with task execution outputs.
- **Implementation**: The `StrategicPlanner` compiles a frozen `Roadmap`, while the `TaskExecutor` processes individual steps. Output payloads are validated by a `PlanVerifier` and kept strictly isolated from the planner's memory.

## Principle 2: Multi-Tier Memory Consolidation
- **Source Category**: Cognitive Memory Architecture
- **Target Subsystem**: `CMOS` / `AgentHarness`
- **Concept**: Distinguish short-term context window history from persistent semantic memory.
- **Implementation**: Short-term history is compacted via sliding windows, while structured evidence cards, facts, and beliefs are persisted inside a SQLite semantic memory repository. High-confidence facts are promoted, and low-confidence ones are pruned to satisfy token budgets.

## Principle 3: Model-Collapse Guard via Quality Downsampling
- **Source Category**: Alignment & Self-Correction
- **Target Subsystem**: `DatasetCompiler` / SFT Alignment
- **Concept**: Automatically prevent self-generated SFT training datasets from causing recursive model degradation.
- **Implementation**: The `TrajectoryDatasetCompiler` tracks the ratio of self-generated vs. real trajectory traces. In strict mode, it raises errors on threshold breach; in relaxed mode, it downsamples self-generated data, keeping only high-scoring traces.

## Principle 4: Two-Level Credit Assignment
- **Source Category**: Reinforcement Learning & Credit Assignment
- **Target Subsystem**: `AEAN HiveMind` / SFT Collector
- **Concept**: Calculate both global trajectory success and progressive step-level contribution.
- **Implementation**: The `TwoLevelCreditAssignment` engine applies positive reinforcement ($1.0 \times \frac{i}{N}$) for successful steps, and progressive penalties ($-0.2 \times \frac{i}{N}$) for steps leading to failure.

## Principle 5: Active Inference Expected Free Energy (EFE) Task Bidding
- **Source Category**: Multi-Agent Consensus Protocols (Papers 301–340)
- **Target Subsystem**: `AEAN HiveMind`
- **Concept**: Sub-agents evaluate task assignment bids by balancing pragmatic value (historical domain success) and epistemic value (curiosity/uncertainty reduction).
- **Implementation**: Registered research insights from `Research OS` trigger automated token bidding across specialized HiveMind worker agents based on EFE utility scores ($EFE = \text{Pragmatic} + \text{Epistemic} - \text{Cost}$).

## Principle 6: Active Inference Opportunity Decision Trees
- **Source Category**: Entrepreneurial Operating System & Capital Allocation (Papers 341–380)
- **Target Subsystem**: `EOS Engine`
- **Concept**: Enterprise growth, product-market fit exploration, and capital allocation are framed as active inference state transitions over an `OpportunityGraph`.
- **Implementation**: `EOSEngine` ingests validated research hypotheses, constructs `OpportunityNode` trees, and routes venture capital to paths with highest expected free energy reduction and unit economic feasibility.

## Principle 7: Continuous Anomaly Sensing over Research Hypotheses
- **Source Category**: Continuous Sensing & Anomaly Detection (Papers 381–420)
- **Target Subsystem**: `EIOS Kernel`
- **Concept**: Real-time event streams are continuously evaluated using non-Gaussian Hawkes point processes and active inference anomaly thresholds.
- **Implementation**: `EIOSKernel.sense_opportunity_anomalies` continuously monitors active research hypotheses registered from `Research OS`, dynamically trigger execution DAG re-compilation upon detecting non-Gaussian state anomalies.

## Principle 8: Multi-Corpora Cross-Querying Literature Review
- **Source Category**: Autonomous Scientific Discovery (Papers 421–460)
- **Target Subsystem**: `Research OS`
- **Concept**: Literature review must query synthesized principles across all registered paper databases (IDs 1–500) via multi-field matching (title, domain, target subsystem, principle text).
- **Implementation**: `ResearchOS.conduct_literature_review` queries `ALPHAALGO_200_PRINCIPLES` alongside base principles, returning structured evidence, code implementation paths, and decision rationale.

## Principle 9: Interventional Causal Graph Belief Propagation
- **Source Category**: Causal World Modeling & Bayesian Belief Updates (Papers 461–500)
- **Target Subsystem**: `APODEX WorldModel`
- **Concept**: Cross-layer active inference state handoffs update structural causal nodes, relation edges, and Bayesian belief distributions.
- **Implementation**: During `ResearchToSystemBridge` handoffs, hypothesis validations and opportunity updates automatically create `CausalNode` instances, link causal edges, and update Bayesian beliefs inside `WorldModel`.
