# Unified Cognitive Operating System Architecture Specification
**Authoritative Architectural Specification for Autonomous Intelligence**

---

## Executive Summary & Architectural Vision

This specification defines the unified 4-layer cognitive architecture integrating **Research OS**, **EIOS/EOS**, **AEAN**, and **APODEX** into a singular, high-assurance autonomous intelligence platform.

Rather than maintaining separate or partially overlapping systems, the platform operates as one unified cognitive engine structured across four hierarchically layered abstractions:

1. **Layer 1: Research OS (Research & Discovery Layer)**
   Scientific literature synthesis, paper corpus principle extraction, automated hypothesis generation, statistical validation (DSR, White's Reality Check), and AST-verified self-referential code synthesis.
2. **Layer 2: EIOS / EOS (Execution & Orchestration Layer)**
   Active Inference EFE anomaly sensing, DAG computational graph compilation, entrepreneurial first-principles reasoning, GTM system dynamics, company growth state machine, unit economics, runway management, and strategic moats.
3. **Layer 3: AEAN (Cognitive Intelligence Layer)**
   Multi-agent coordination, HiveMind token bidding, task decomposition, agent specialization, swarm negotiation, and collective intelligence routing.
4. **Layer 4: APODEX (Decision & Execution Platform Layer)**
   WorldModel causal graph, Bayesian belief updating, entity state persistence, skills flywheel execution, safety and GRC governance, and runtime infrastructure.

---

## 1. First-Principles Layer Taxonomy

```
+-----------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS (Research Layer)                      |
|  - Paper Corpus Principle Ingestion & Literature Synthesis                        |
|  - Automated Hypothesis Generation & Statistical Validation (DSR, WRC)            |
|  - Self-Referential AST Code Rewrite & Verification Engine                        |
+-----------------------------------------------------------------------------------+
                                         |
                                         v Validated Hypotheses & Engineering Principles
+-----------------------------------------------------------------------------------+
|                     LAYER 2: EIOS / EOS (Execution & Orchestration)               |
|  - EIOS Kernel: DAG Computational Pipeline & Active Inference EFE Sensing         |
|  - EOS Engine: Entrepreneurial State Machine, GTM Dynamics, Financial Runway      |
+-----------------------------------------------------------------------------------+
                                         |
                                         v Opportunistic Sub-Tasks & Execution Directives
+-----------------------------------------------------------------------------------+
|                     LAYER 3: AEAN (Cognitive Intelligence Layer)                  |
|  - HiveMind Token Bidding Registry & Multi-Agent Task Bidding                     |
|  - Swarm Negotiation, Sub-Agent Specialization & Parsimonious Routing             |
+-----------------------------------------------------------------------------------+
                                         |
                                         v Executable Micro-Actions & Skill Requests
+-----------------------------------------------------------------------------------+
|                  LAYER 4: APODEX (Decision & Execution Platform Layer)            |
|  - WorldModel Causal Graph & Recursive Bayesian Belief Updating                   |
|  - Skills Flywheel, GRC Safety Guardrails, & System Runtime Environment           |
+-----------------------------------------------------------------------------------+
```

---

## 2. Layer Specifications & Interfaces

### Layer 1: Research OS (Research Layer)
* **Primary Responsibility:** Scientific discovery, empirical literature synthesis, hypothesis generation, and rigorous statistical validation.
* **Key Components:**
  - `ResearchOS`: Literature review synthesis, experiment design (power analysis), statistical validation (White's Reality Check, Deflated Sharpe Ratio).
  - `CodeRewriteEngine`: AST-verified code mutation and GRC static security auditing.
  - `GeneticWorkflowOptimizer`: Island MAP-Elites prompt and genome evolutionary optimizer.
  - `SFTPreferenceCollector`: Temporal-difference advantage calculation for DPO trajectory compiler.
* **Input Interfaces:** Research domain queries, codebase AST files, experimental ground-truth yield vectors.
* **Output Interfaces:** Promoted `ValidatedHypothesis` and `ExtractedEngineeringPrinciple` records exported directly to Layer 2.

### Layer 2: EIOS / EOS (Execution & Orchestration Layer)
* **Primary Responsibility:** Active inference anomaly sensing, DAG task compilation, and first-principles entrepreneurial orchestration.
* **Key Components:**
  - `EIOSKernel`: Active Inference EFE sensing over research hypotheses, DAG task compilation and execution, node dependency graph processing.
  - `EOSEngine`: Ingestion of validated research, customer lifecycle simulation, GTM dynamics, financial runway tracking, and company growth state machine transition checks.
* **Input Interfaces:** Promoted hypotheses from Layer 1, market observation events from Layer 4.
* **Output Interfaces:** Opportunistic DAG task specifications and capital allocations passed to Layer 3.

### Layer 3: AEAN (Cognitive Intelligence Layer)
* **Primary Responsibility:** Swarm agent bidding, task decomposition, agent specialization, and parsimonious routing.
* **Key Components:**
  - `HiveMind`: Multi-agent token bidding registry, task bidding lifecycle, research insight registration.
  - `LearnableRoutingGateDispatcher`: EFE budget-bounded agent task routing minimizing surprise and financial expenditure.
* **Input Interfaces:** Sub-task requests and opportunity contracts from Layer 2.
* **Output Interfaces:** Bidding contracts, agent assignment decisions, and concrete skill execution orders sent to Layer 4.

### Layer 4: APODEX (Decision & Execution Platform Layer)
* **Primary Responsibility:** Causal world modeling, state persistence, skill execution, and runtime GRC safety.
* **Key Components:**
  - `WorldModel`: Causal graph nodes (`CausalNode`), recursive Bayesian belief updating (`BeliefState`), entity state persistence.
  - `CognitiveBrain`: High-level cognition, skill execution protocol runner, safety guardrails.
  - `ResearchToSystemBridge`: Active inference cross-layer state handoff orchestrator.
* **Input Interfaces:** Skill execution requests from Layer 3, raw external sensor events.
* **Output Interfaces:** State observation updates fed back into Active Inference loops across Layers 1, 2, and 3.

---

## 3. Active Inference & Closed-Loop Mathematics

The unified operating system minimizes Expected Free Energy ($\mathbf{G}$) across all four layers:

$$\mathbf{G}(\pi) = -\mathbb{E}_{q(o, \theta|\pi)}\left[ \log \frac{p(o, \theta)}{q(\theta|\pi)} \right] = \underbrace{\mathbb{E}_{q}[\log q(\theta|\pi) - \log p(\theta|o)]}_{\text{Epistemic Value (Information Gain)}} - \underbrace{\mathbb{E}_{q}[\log p(o)]}_{\text{Pragmatic Value (Commercial Utility)}}$$

1. **Layer 1** maximizes epistemic value via Bayesian hypothesis testing and Deflated Sharpe Ratio validation.
2. **Layer 2** balances pragmatic utility and epistemic exploration using the blended priority score:
   $$\text{Priority} = \alpha \cdot \mathbb{E}[\text{Commercial Value}] + \beta \cdot \text{InformationGain} + \gamma \cdot \text{OptionValue}$$
3. **Layer 3** evaluates sub-agent routing score using budget-bounded EFE:
   $$\text{Score}_a = \text{Epistemic}_a + \text{Pragmatic}_a - \lambda \cdot \text{Cost}_a$$
4. **Layer 4** updates Bayesian belief distributions over causal nodes:
   $$P(B_t \mid O_t) = \frac{P(O_t \mid B_t) P(B_t)}{\sum_k P(O_t \mid B_k) P(B_k)}$$

---

## 4. Verification and Compliance Standard

Every modification across the 4 layers must satisfy:
1. **Zero Capability Duplication:** All capability implementations must reside strictly within their designated owning layer as specified in `CAPABILITY_OWNERSHIP_MATRIX.md`.
2. **Explicit Cross-Layer Handoffs:** Handoffs between layers must pass through validated data structures via `ResearchToSystemBridge`.
3. **100% Test Coverage:** All integration contracts must be verified by automated test suites.
