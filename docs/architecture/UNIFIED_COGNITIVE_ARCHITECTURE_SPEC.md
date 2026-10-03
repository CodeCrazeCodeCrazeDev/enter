# Unified Cognitive Operating System Architecture Specification

## 1. Executive Summary & Vision

The Unified Cognitive Operating System (UCOS) unifies five previously distinct subsystems—**Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX**—into a singular, highly integrated 4-layer cognitive platform. Rather than maintaining overlapping, redundant modules across isolated domains, UCOS structures autonomous intelligence into strict, hierarchical functional layers governed by **Active Inference** (Free Energy Principle), **Bayesian World Modeling**, and **Swarm Intelligence Bidding**.

```
+-----------------------------------------------------------------------+
|                    LAYER 1: RESEARCH OS (RESEARCH)                    |
| Literature Mining | Hypothesis Generation | Empirical Validation      |
+-----------------------------------------------------------------------+
                                   | (Hypothesis Handoff & Research Insights)
                                   v
+-----------------------------------------------------------------------+
|                LAYER 2: EIOS / EOS (EXECUTION & ORCHESTRATION)        |
| Active Inference Sensing | Expected Free Energy DAGs | Capital Allocation |
+-----------------------------------------------------------------------+
                                   | (Opportunity Tasks & Intent DAGs)
                                   v
+-----------------------------------------------------------------------+
|               LAYER 3: AEAN (COGNITIVE INTELLIGENCE & AGENTS)          |
| Swarm HiveMind | Token Bidding Registry | Multi-Agent Specialization   |
+-----------------------------------------------------------------------+
                                   | (Strategy Actions & Token-Bids)
                                   v
+-----------------------------------------------------------------------+
|               LAYER 4: APODEX (DECISION & PLATFORM ENGINE)            |
| Causal World Model | Bayesian Belief Networks | Telemetry & Security   |
+-----------------------------------------------------------------------+
```

---

## 2. Layer Taxonomy & Functional Responsibilities

### Layer 1: Research OS (The Research Layer)
* **Primary Scope:** Continuous scientific literature mining, empirical hypothesis generation, statistical validation ($p < 0.05$), AST rewrite proposal verification, and formal publication indexing.
* **Core Components:**
  - `ResearchOS`: Autonomous research orchestrator.
  - `ResearchIngestionPipeline`: Mining 600+ paper research corpus principles.
  - `CodeRewriteEngine`: AST verification with Hawkes process non-Gaussian call depth analysis.
  - `StatisticalValidationEngine`: Power calculation and cross-validation of empirical claims.
* **Outputs:** Validated research hypotheses ($H_{val}$) and transferable engineering principles.

### Layer 2: EIOS / EOS (The Execution & Orchestration Layer)
* **Primary Scope:** Opportunity anomaly sensing, Expected Free Energy (EFE) minimization, DAG workflow synthesis, capital allocation, and business lifecycle state transitions.
* **Core Components:**
  - `EIOSKernel`: Subsystem orchestration kernel executing Active Inference policy loops ($G = -D_{KL} + \text{Ambiguity}$).
  - `EOSEngine` & `EOSEngineFirstPrinciples`: Entrepreneurial Operating System engine governing the 11-stage company growth state machine, unit economics, customer lifecycle, and GTM dynamics.
  - `LearnableRoutingGateDispatcher`: Cost and performance dynamic DAG task router.
* **Outputs:** Intent DAGs, Opportunity Nodes, and Capital Allocation Decisions.

### Layer 3: AEAN (The Cognitive Intelligence Layer)
* **Primary Scope:** Multi-agent collective intelligence, swarm bidding registry, specialization agent teams (Executive, Operational, Technical), and pre-trade/post-trade strategy critics.
* **Core Components:**
  - `HiveMind`: Token bidding registry and agent coordination protocol.
  - `PAEANEngine` & `AREEngine`: Autonomous reasoning and evolution engines.
  - `EpistemicCritic` & `PretradeEvolutionValidator`: Strategy verification and risk gating.
* **Outputs:** Executed agent action plans, task bid resolutions, and evolutionary agent mutations.

### Layer 4: APODEX (The Decision & Execution Platform Layer)
* **Primary Scope:** Structural causal graph maintenance, recursive Bayesian belief updates ($P(\theta|X)$), event bus telemetry, safety policy enforcement, and execution state persistence.
* **Core Components:**
  - `WorldModel`: Causal graph containing `CausalNode` and `RelationEdge` entities.
  - `BayesianBeliefEngine`: Updating belief confidence from observation streams.
  - `ResearchToSystemBridge`: Unified cross-layer active inference state handoff orchestrator.
  - `SafetyManager` & `ApprovalGateway`: Security policy and execution permissioning.
* **Outputs:** Grounded world state, updated posterior belief distributions, and verified system execution logs.

---

## 3. The Unified Active Inference Cognitive Loop

The entire 4-layer system operates on a single continuous active inference loop:

1. **Epistemic Exploration (Layer 1):** Research OS mines domain anomalies and outputs validated hypothesis $H_k$.
2. **EFE Calculation & Sensing (Layer 2):** EIOS Kernel ingests $H_k$, calculates Expected Free Energy $G(a)$, and synthesizes execution DAG $D$.
3. **Swarm Bidding & Execution (Layer 3):** AEAN HiveMind auctions DAG nodes to specialized agents based on token stakes and confidence scores.
4. **Causal Perception & Belief Update (Layer 4):** APODEX executes actions, captures environmental feedback, updates causal nodes $N_c$ and Bayesian beliefs $B_b$, and provides state feedback back to Layer 1 and Layer 2.

```
       +-------------------------------------------------------+
       | 1. Epistemic Exploration (Research OS)                |
       +-------------------------------------------------------+
                                   | Hypothesis H_k
                                   v
       +-------------------------------------------------------+
       | 2. EFE Calculation & Intent DAG (EIOS / EOS)           |
       +-------------------------------------------------------+
                                   | Intent DAG D
                                   v
       +-------------------------------------------------------+
       | 3. Multi-Agent Bidding & Action Execution (AEAN)      |
       +-------------------------------------------------------+
                                   | Executed Actions
                                   v
       +-------------------------------------------------------+
       | 4. Causal & Bayesian Belief Update (APODEX WorldModel) |
       +-------------------------------------------------------+
                                   | Updated World State & Beliefs
                                   +---------------------------+
```

---

## 4. Key Architectural Guarantees

1. **Zero Capability Duplication:** Module responsibilities are strictly partitioned according to the 4-layer taxonomy.
2. **Explicit Typed Interfaces:** All cross-layer state handoffs use immutable Pydantic/SQLModel transport objects.
3. **Deterministic Governance:** Execution requires multi-tier safety approval and active inference threshold compliance ($p < 0.05$, $EFE \le \text{budget}$).
4. **Resilient Failure Recovery:** Automatic rollback and fallback handling across DAG nodes and world model state transactions.
