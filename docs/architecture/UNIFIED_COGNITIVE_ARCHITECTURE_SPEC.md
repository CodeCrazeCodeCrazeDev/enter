# Unified Cognitive Architecture Specification

## 1. Executive Summary & First Principles Architecture

The APODEX Cognitive Platform integrates **Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX World Model** into a single, unified 4-layer cognitive operating system. Rather than operating as isolated silos or competing frameworks, these five components form a strictly layered active inference loop designed for long-horizon autonomous execution, scientific research, entrepreneurial reasoning, and continuous self-improvement.

```
+-----------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS (Research Layer)                      |
| Scientific Literature Mining, Empirical Hypothesis Generation, & Statistical Test |
+-----------------------------------------------------------------------------------+
                                          |
                                          v  (Validated Hypotheses / Research Insights)
+-----------------------------------------------------------------------------------+
|                  LAYER 2: EIOS & EOS (Execution & Orchestration Layer)            |
| EIOS Kernel (Active Inference Sensing DAGs) & EOS Engine (Entrepreneurial State) |
+-----------------------------------------------------------------------------------+
                                          |
                                          v  (Opportunity Nodes & Execution Tasks)
+-----------------------------------------------------------------------------------+
|                 LAYER 3: AEAN (Cognitive Intelligence Layer)                      |
| HiveMind Coordination, Agent Token Bidding, Dynamic Sub-Agent Specialization     |
+-----------------------------------------------------------------------------------+
                                          |
                                          v  (Agent Actions & Environmental Observations)
+-----------------------------------------------------------------------------------+
|               LAYER 4: APODEX WORLD MODEL (Decision & Execution Layer)            |
| Causal DAG, Recursive Bayesian Belief Engines, Safety Governance & Runtime        |
+-----------------------------------------------------------------------------------+
```

---

## 2. Comprehensive Layer Breakdown

### Layer 1: Research OS (Research Layer)
* **Canonical Role:** Literature analysis, hypothesis generation, empirical code proposal generation, and statistical validation.
* **Core Responsibilities:**
  - Automated literature ingestion across multi-domain research corpora (600+ papers).
  - Extraction and indexing of transferable engineering principles.
  - Formulating empirical hypotheses with statistical power calculations (Deflated Sharpe Ratios, Benjamini-Hochberg FDR control).
  - AST code rewrite proposal generation and verification.
* **Interface Output:** Validated research hypotheses (`ResearchHypothesis`) and structured research insights handed off to Layer 2 via `ResearchToSystemBridge`.

### Layer 2: EIOS / EOS (Execution & Orchestration Layer)
* **Canonical Role:** Active inference environmental sensing, DAG task compilation, and entrepreneurial capital/resource allocation.
* **Core Responsibilities:**
  - **EIOS Kernel:** Active Inference Expected Free Energy (EFE) minimization, sensing opportunity anomalies, compiling execution DAGs.
  - **EOS Engine:** Managing the Entrepreneurial State Machine (Sensing, Building, GTM, Customer Lifecycle, Growth Stages, Moat Building, Failure Diagnostics).
* **Interface Output:** Structured opportunity nodes and active task execution specifications handed off to Layer 3.

### Layer 3: AEAN (Cognitive Intelligence Layer)
* **Canonical Role:** Multi-agent coordination, token-based work bidding, dynamic agent specialization, and collaborative task solving.
* **Core Responsibilities:**
  - **HiveMind Coordinator:** Decentralized bidding registry where specialized worker agents bid tokens based on capability and cost tier.
  - **Agent Specialization:** Dynamic role assignment for researchers, planners, code submitters, auditors, and safety monitors.
  - **Consensus & Peer Review:** Multi-agent voting and verification before state mutations.
* **Interface Output:** Tool execution results, code diffs, and environment observation payloads routed to Layer 4.

### Layer 4: APODEX (Decision Engine & Execution Platform Layer)
* **Canonical Role:** Causal world modeling, recursive Bayesian belief updating, runtime safety governance, and execution environment state management.
* **Core Responsibilities:**
  - **WorldModel Causal Engine:** Maintaining directed acyclic causal graphs (`CausalNode`, `RelationEdge`).
  - **Bayesian Belief Engine:** Updating belief distributions (`BeliefNode`) based on agent execution feedback.
  - **Governance & Approval:** Tiered safety authorization, risk threshold checks, and rollback/changelog management.
  - **Skills Flywheel:** Protocol execution and automatic skill abstraction.

---

## 3. Cross-Layer Active Inference Loop

1. **Sensing (Layer 1 -> Layer 2):** Research OS validates a new algorithmic principle or market hypothesis and registers it with the EIOS Kernel.
2. **Evaluation & Strategy (Layer 2):** EIOS Kernel evaluates Expected Free Energy (EFE) reduction. EOS Engine evaluates ROI, risk profiles, and capital allocation, outputting an action plan.
3. **Execution (Layer 3):** AEAN HiveMind auctions execution tasks to specialized agent clusters. Agents execute tools, code edits, or simulations.
4. **Belief Update & Reality Grounding (Layer 4):** Execution results update the APODEX WorldModel causal DAG and recursive Bayesian belief priors. Feedback flows back to Layer 1 for literature hypothesis refinement.
