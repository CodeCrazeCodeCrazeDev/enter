# Unified Cognitive Architecture Specification (AEAN / EIOS / EOS / APODEX / Research OS)

## Executive Summary & Architectural Directive

This document establishes the authoritative unified cognitive architecture for the autonomous intelligence platform comprising Research OS, EIOS, EOS, AEAN, and APODEX. Rather than treating these five systems as independent, loosely coupled projects, this specification unifies them into a single 4-layer cognitive operating system based on active inference, causal world modeling, and distributed multi-agent swarm orchestration.

By strictly adhering to a single layered architecture with explicit boundary contracts, this design eliminates functional duplication, technical debt, and synchronization bottlenecks across autonomous execution pipelines.

---

## The 4-Layer Taxonomy & Capability Boundaries

```
+-----------------------------------------------------------------------+
| LAYER 4: APODEX - DECISION & WORLD MODELING LAYER                     |
| Causal Graph Engine | Bayesian Belief Network | Active Inference EFE  |
+-----------------------------------------------------------------------+
                                  ^
                                  | Belief Updates & Decision Utility
                                  v
+-----------------------------------------------------------------------+
| LAYER 3: AEAN - COGNITIVE INTELLIGENCE LAYER                         |
| Swarm HiveMind | Capability Bidding | Market Mechanics | Memory Networks|
+-----------------------------------------------------------------------+
                                  ^
                                  | Strategy & Swarm Task Graphs
                                  v
+-----------------------------------------------------------------------+
| LAYER 2: EIOS / EOS - EXECUTION & ORCHESTRATION LAYER                  |
| DAG Kernel | Resource Bounding | Active Inference Sensing | Capital Loop |
+-----------------------------------------------------------------------+
                                  ^
                                  | Ingested Hypotheses & Evidence
                                  v
+-----------------------------------------------------------------------+
| LAYER 1: RESEARCH OS - RESEARCH & DISCOVERY LAYER                     |
| Empirical Discovery | Hypothesis Engine | Statistical Validation       |
+-----------------------------------------------------------------------+
```

### Layer 1: Research OS (Research & Discovery Layer)
- **Primary Responsibility:** Empirical scientific research, literature extraction, hypothesis generation, and statistical experimentation.
- **Key Modules:** `ResearchOS`, `LiteratureExtractor`, `HypothesisEngine`, `StatisticalValidator`.
- **Inputs:** Raw research papers, scientific datasets, domain corpus (e.g., 600-paper corpus), operational anomalies.
- **Outputs:** Rigorously validated hypotheses, transferable engineering principles, and empirical evidence.
- **Non-Responsibilities:** Does not directly allocate capital, dispatch real-time agent tasks, or maintain world model state.

### Layer 2: EIOS / EOS (Execution & Orchestration Layer)
- **Primary Responsibility:** Execution workflow orchestration, resource allocation, DAG scheduling, and entrepreneurial capital management.
- **Key Modules:** `EIOSKernel`, `EOSEngine`, `ExecutionScheduler`, `CapitalLoopEngine`.
- **Inputs:** Validated research hypotheses from Layer 1, strategic directives from Layer 3, belief distributions from Layer 4.
- **Outputs:** Scheduled task execution DAGs, active inference anomaly signals, capital/compute budget boundaries.
- **Non-Responsibilities:** Does not perform raw LLM prompt orchestration or direct Bayesian graph updates.

### Layer 3: AEAN (Cognitive Intelligence Layer)
- **Primary Responsibility:** Multi-agent collaboration, capability-based task bidding, cognitive memory retrieval, and autonomous software engineering.
- **Key Modules:** `HiveMind`, `SwarmOrchestrator`, `SemanticMemory`, `CodeRewriteEngine`, `GeneticWorkflowOptimizer`.
- **Inputs:** Task execution DAGs from Layer 2, causal state constraints from Layer 4.
- **Outputs:** Specialized agent task outputs, refactored codebase ASTs, multi-agent bidding resolution logs.
- **Non-Responsibilities:** Does not redefine top-level research goals or evaluate global Bayesian loss.

### Layer 4: APODEX (Decision & World Modeling Layer)
- **Primary Responsibility:** Causal world modeling, Bayesian belief updating, active inference Expected Free Energy (EFE) calculation, and long-horizon risk evaluation.
- **Key Modules:** `WorldModel`, `CausalEngine`, `BayesianBeliefNetwork`, `ActiveInferencePlanner`.
- **Inputs:** Observations, state changes, execution results from Layers 1, 2, and 3.
- **Outputs:** Updated world state estimates, prior probability distributions, EFE utility metrics guiding Layer 2 execution and Layer 3 bidding.
- **Non-Responsibilities:** Does not directly write source code or run individual pipeline tasks.

---

## Core Cognitive Mechanisms

### 1. Active Inference & Expected Free Energy (EFE)
The entire system minimizes Expected Free Energy $G(\pi)$ across policies $\pi$:
$$G(\pi) = -\mathbb{E}_{q(o, \theta |\pi)}[\ln p(o)] + \mathbb{E}_{q(\theta|\pi)}[D_{KL}(q(o|\theta) || p(o))] $$
where epistemic value drives exploratory research (Layer 1) and instrumental value drives capital/execution optimization (Layer 2 & 3), anchored by the APODEX world model (Layer 4).

### 2. Multi-Agent Swarm Bidding & Capability Routing
AEAN Layer 3 agents participate in sealed-bid second-price auctions for DAG nodes based on confidence, capability vectors, and current resource budgets.

### 3. Causal Bayesian Belief Refinement
APODEX Layer 4 maintains a directed acyclic causal graph $G = (V, E)$. Interventions $do(X = x)$ are evaluated via do-calculus before high-risk execution decisions are authorized by EOS Layer 2.

---

## Architectural Guarantees & Non-Functional Requirements

1. **Sub-second Cross-Layer State Handoffs:** Inter-layer messages via `ResearchToSystemBridge` achieve $<10\text{ms}$ latency.
2. **Institutional Reliability & Safety Gateways:** Zero unsafe execution without formal verification and sandbox validation.
3. **Continuous Self-Improvement Flywheel:** AST refactor proposals undergo strict statistical validation in Layer 1 before hot-swapping into Layer 3 execution routines.
