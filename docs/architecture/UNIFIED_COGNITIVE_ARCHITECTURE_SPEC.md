# Unified Cognitive Architecture Specification
## AEAN / EIOS / EOS / APODEX Cognitive Operating System (v2026.1)

---

## Executive Summary

This specification defines the first-principles architecture of the **Unified Cognitive Operating System**, an autonomous platform integrating **Research OS**, **EIOS Kernel**, **EOS Engine**, **AEAN HiveMind**, and **APODEX WorldModel**.

Rather than maintaining five disparate frameworks with overlapping boundaries, this architecture unifies all components into a single **4-Layer Cognitive Hierarchy**. Each layer possesses strict functional responsibilities, standard communication protocols, and formal state handoffs, eliminating architectural duplication and technical debt while maximizing long-horizon autonomy, scientific rigour, and operational reliability.

---

## 1. Architectural Taxonomy & Layered Structure

```
+-----------------------------------------------------------------------------------+
| LAYER 1: SCIENTIFIC RESEARCH & HYPOTHESIS DISCOVERY (Research OS)                 |
| - Literature ingestion & 600-paper principle extraction                            |
| - Hypothesis formulation, experimental design & active inference statistical tests|
+-----------------------------------------------------------------------------------+
                                         │
                   Hypothesis Handoff    │ Active Inference EFE Feedback
                                         ▼
+-----------------------------------------------------------------------------------+
| LAYER 2: AUTONOMOUS EXECUTION & SENSING ORCHESTRATION (EIOS Kernel / EOS Engine)   |
| - Opportunity graph construction & Hawkes process spike detection                 |
| - Capital allocation, continuous sensing DAGs & business growth state machine     |
+-----------------------------------------------------------------------------------+
                                         │
                   Strategy Delegation   │ Bidding Outcomes & EKG Updates
                                         ▼
+-----------------------------------------------------------------------------------+
| LAYER 3: MULTI-AGENT COGNITIVE INTELLIGENCE & BIDDING (AEAN HiveMind)             |
| - Token-based auction task allocation & PAEAN evolutionary search                 |
| - Pre-trade, epistemic & RGAE critics, specialized agent consensus                |
+-----------------------------------------------------------------------------------+
                                         │
                   Action Execution      │ Causal & Bayesian Belief Updates
                                         ▼
+-----------------------------------------------------------------------------------+
| LAYER 4: UNIFIED WORLD MODEL & DECISION SUBSTRATE (APODEX WorldModel & Brain)      |
| - Causal graph indexing, digital twin simulation & entity state tracking          |
| - Recursive Bayesian belief updating & multi-tier memory (CMOS / EMG)             |
+-----------------------------------------------------------------------------------+
```

### Layer 1: Research OS (Scientific Research Layer)
* **Primary Responsibility**: Automated scientific hypothesis formulation, paper ingestion, literature synthesis, and statistical validation.
* **Core Mechanisms**:
  - Research Ingestion Pipeline over paper databases (`ALPHA_ALGO_100` through `600`).
  - Active Inference statistical controls ($\alpha=0.05$, family-wise error rate control).
  - Automated experiment generation and statistical power calculation.
* **Outputs**: Formal `ValidatedHypothesis` and `ResearchInsight` objects.

### Layer 2: EIOS Kernel & EOS Engine (Execution & Orchestration Layer)
* **Primary Responsibility**: Opportunistic market/system sensing, execution DAG generation, capital/resource allocation, and business state machine transitions.
* **Core Mechanisms**:
  - Non-Gaussian Hawkes process anomaly sensing ($\lambda(t) = \mu + \sum \alpha e^{-\beta(t-t_i)}$).
  - Active Inference Expected Free Energy (EFE) task scheduling ($G(\pi) = \text{Ambiguity} + \text{Risk}$).
  - Capital allocation tree & growth state machine ($S_0 \to S_1 \to S_2 \to S_3$).
* **Outputs**: `OpportunityGraph`, `DAGExecutionPlan`, `CapitalAllocationDecision`.

### Layer 3: AEAN HiveMind (Cognitive Intelligence Layer)
* **Primary Responsibility**: Multi-agent task bidding, evolutionary search, epistemic verification, and specialized consensus.
* **Core Mechanisms**:
  - Token-based bidding auction mechanism for agent task assignment.
  - Empirical Knowledge Graph (EKG) and PAEAN evolutionary engine.
  - Epistemic, pre-trade, and Robust Generative Adversarial Evaluation (RGAE) critics.
* **Outputs**: `AgentStrategy`, `BiddingResult`, `VerifiedCodePatch`.

### Layer 4: APODEX WorldModel & Cognitive Brain (Decision & World Model Substrate)
* **Primary Responsibility**: Causal state representation, predictive digital twin simulation, recursive Bayesian belief updating, and unified memory management.
* **Core Mechanisms**:
  - Causal graph traversal & indexing (`CausalNode`, `RelationEdge`).
  - Recursive Bayesian belief updates ($P(H|E) = \frac{P(E|H)P(H)}{P(E)}$).
  - CMOS (Cognitive Memory Operating System) & EMG (Epistemic Memory Graph).
* **Outputs**: `WorldStateUpdate`, `BeliefState`, `PredictiveSimulationResult`.

---

## 2. Active Inference Closed-Loop Execution

The system operates on a unified Active Inference loop minimizing Variational Free Energy ($F$) and Expected Free Energy ($G$):

$$\mathcal{F}(q, y) = \mathbb{E}_{q(\vartheta)}[\ln q(\vartheta) - \ln p(\vartheta, y)]$$

$$G(\pi) = \sum_\tau \left( \underbrace{\mathbb{E}_{q(o_\tau|\pi)}[\ln q(o_\tau|\pi) - \ln p(o_\tau)]}_{\text{Risk / Pragmatic Value}} + \underbrace{\mathbb{E}_{q(s_\tau|\pi)}[H(p(o_\tau|s_\tau))]}_{\text{Ambiguity / Epistemic Value}} \right)$$

1. **Sense (Layer 2)**: EIOS Kernel senses anomalies via Hawkes point processes and converts observations into Active Inference state signals.
2. **Predict & Evaluate (Layer 4)**: APODEX WorldModel runs digital twin simulations to calculate epistemic value and pragmatic risk.
3. **Hypothesize (Layer 1)**: Research OS formulates literature-backed hypotheses when ambiguity exceeds thresholds ($H(p) > \tau_{\text{ambiguity}}$).
4. **Coordinate & Execute (Layer 3)**: AEAN HiveMind bids out execution tasks to specialized agents using token-based auctions.
5. **Update Beliefs (Layer 4)**: Action outcomes update the causal graph and Bayesian beliefs in APODEX WorldModel.

---

## 3. Long-Horizon Planning & Self-Improvement

* **Island MAP-Elites Migration**: Multi-island genetic workflow optimization preserves diversity across strategy space.
* **Code Rewrite Engine**: Self-modifying code generation with non-Gaussian Hawkes recursive AST call depth checks to prevent infinite recursion or unbounded stack growth.
* **Clips Trajectory Advantage Margins**: SFT preference collector enforces clipped advantage bounds to maintain policy stability during long-horizon task execution.

---

## 4. Safety, Governance, and Reliability Controls

1. **Pre-Trade & Compliance Gates**: Every capital decision or code commit passes strict pre-execution policy checks (`PretradeCritic`, `ComplianceValidator`).
2. **Tiered Approval Workflow**: High-risk actions (capital expenditures $> \$10k$, core kernel rewrites) trigger human-in-the-loop or multi-signatory consensus.
3. **Automatic Rollback & Fail-Safe**: State changes are checkpointed in APODEX WorldModel. Failed executions automatically trigger rollback protocols.

---

## 5. Summary Matrix of Layer Responsibilities

| Subsystem Layer | Primary Input | Core Algorithm / Framework | Primary Output |
|---|---|---|---|
| **Layer 1: Research OS** | Academic Papers, Corpus DB | Active Inference Statistical Tests, Literature Ingestion | Validated Hypotheses, Research Insights |
| **Layer 2: EIOS / EOS** | Validated Hypotheses, Market Signals | Non-Gaussian Hawkes Sensing, EFE DAG Scheduler | Opportunity Graphs, Growth State Machine |
| **Layer 3: AEAN HiveMind** | DAG Execution Tasks, Bids | Token Bidding Registry, PAEAN Evolutionary Search | Bidding Allocations, Executed Agent Strategies |
| **Layer 4: APODEX WorldModel** | Execution Results, Environmental Signals | Causal Indexing, Recursive Bayesian Updating | Belief States, World Model Graph Updates |
