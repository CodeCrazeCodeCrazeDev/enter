# Unified 4-Layer Cognitive Architecture Specification (AEAN / EIOS / EOS / APODEX)

**Document Version:** 1.0.0
**Status:** Authoritative Architectural Standard
**Target Architecture:** Single Layered Cognitive Operating System Taxonomy

---

## 1. Executive Summary & Architectural Rationale

To achieve institutional-grade autonomous intelligence, long-horizon goal execution, and continuous self-improvement, the historical paradigm of treating **Research OS**, **AEAN**, **EIOS**, **EOS**, and **APODEX** as distinct, partially overlapping platforms is hereby superseded.

When autonomous intelligence systems grow as independent platforms, they introduce logical duplication:
- Multiple world model managers competing for state representation.
- Overlapping active inference and planning loops.
- Fragmented memory systems and uncoordinated multi-agent swarms.
- Disjointed verification, safety, and governance checks.

This specification consolidates all cognitive processes into a **Single 4-Layer Unified Cognitive Operating System Architecture**. Each layer possesses explicit non-overlapping responsibilities, strict downward unidirectional dependency constraints, and standardized inter-layer contract schemas.

```
+-----------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS (Research Layer)                      |
|  - Academic Corpus Indexing & Jaccard Literature Discovery                         |
|  - Empirical Hypothesis Generation, Power Analysis & Holm-Bonferroni Verification |
|  - Scientific Provenance Tracing (Paper -> Principle -> Candidate Implementation)  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|               LAYER 2: AEAN (Cognitive Intelligence Layer)                         |
|  - Causal World Modeling (Pearl's Do-Calculus Structural Causal Models)          |
|  - Active Inference & Expected Free Energy Routing (Pragmatic + Epistemic)         |
|  - CMOS Epistemic Memory & Ebbinghaus Decay Optimization                         |
|  - Hive Mind Multi-Agent Swarm Debate & Sycophancy Mitigation                      |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|            LAYER 3: EIOS / EOS (Execution & Orchestration Layer)                  |
|  - Multi-Timescale Operational Loops & 13 Coupled Business Loops                   |
|  - EIOS Kernel Sense-Plan-Act Pipeline & Signal-to-Hypothesis Filtering           |
|  - Advanced Kelly Capital Allocation & Pareto-Optimal Multi-Objective Routing     |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|               LAYER 4: APODEX (Decision & Execution Layer)                        |
|  - Deterministic Skill Registry (60 Operational Skills) & Execution Runtime       |
|  - Self-Harness Observer & Runtime Verification Engine                            |
|  - Decision Fatigue Monitoring, Circuit Breakers & Tiered Governance Approval     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Layer Taxonomy & Non-Overlapping Responsibilities

### Layer 1: Research OS (Research Layer)
- **Primary Purpose:** Autonomous scientific discovery, literature synthesis, hypothesis generation, and experimental validation.
- **Canonical Owner:** `apodex/ai_eos/research/research_os.py`, `apodex/research_os/`
- **Core Responsibilities:**
  1. Indexing academic publication corpora (`AI_EOS_RESEARCH_DB.yaml`, `ALPHA_ALGO_100_NEW_RESEARCH.yaml`).
  2. Extracting transferable engineering principles via Ranked Jaccard Similarity and LLM extraction.
  3. Formulating falsifiable architectural hypotheses and computing required sample sizes via statistical power analysis ($\alpha = 0.05, \beta = 0.20$).
  4. Executing deterministic trials and applying Holm-Bonferroni corrections to prevent family-wise type I errors.
  5. Exporting validated research principles down to Layer 2 and Layer 3 via `export_validated_hypothesis_to_kernel()`.

### Layer 2: AEAN (Cognitive Intelligence Layer)
- **Primary Purpose:** Multi-agent reasoning, probabilistic world modeling, active inference state estimation, and long-term memory synthesis.
- **Canonical Owner:** `apodex/aean/`, `apodex/cognition/`, `apodex/world_model/`, `apodex/memory/`
- **Core Responsibilities:**
  1. Operating the Structural Causal Model (SCM) to evaluate interventions ($P(Y | do(X))$) without confounding bias.
  2. Computing Active Inference Expected Free Energy ($EFE = \text{Pragmatic Value} + \text{Epistemic Information Gain}$) to balance exploration and exploitation.
  3. Managing CMOS (Cognitive Memory Operating System) with Ebbinghaus memory retention decay curves ($R = e^{-t / S}$).
  4. Conducting Bayesian Swarm Debate with anti-sycophancy noise injection and Nash equilibrium resolution.

### Layer 3: EIOS / EOS (Execution & Orchestration Layer)
- **Primary Purpose:** Strategic decision-making, operational lifecycle management, and multi-timescale workflow orchestration.
- **Canonical Owner:** `apodex/arcs/kernel/`, `apodex/ai_eos/intelligence/`
- **Core Responsibilities:**
  1. Driving the 13 coupled business loops and 15-stage customer journey state machines.
  2. Evaluating opportunity economics and sizing capital allocations using the Advanced Kelly Criterion with drawdown risk constraints.
  3. Generating strategic action plans based on Active Inference directives received from Layer 2.
  4. Dispatching executable task specifications to Layer 4.

### Layer 4: APODEX (Decision & Execution Layer)
- **Primary Purpose:** Concrete skill invocation, tool execution, runtime safety guardrails, state verification, and governance.
- **Canonical Owner:** `apodex/skills/`, `apodex/harness/`, `apodex/protocols/`, `apodex/governance/`
- **Core Responsibilities:**
  1. Pre-populating and executing 60 production skills registered in the `SkillRegistry`.
  2. Observing turn-by-turn agent tool executions using `SelfHarnessObserver` and detecting repetitive loops or anomalies.
  3. Enforcing decision fatigue thresholds ($D_f$) and triggering cost-tier downshifting or credit halt protocol circuit breakers.
  4. Validating execution outcomes and writing immutable audit logs.

---

## 3. Elimination of Logical Duplication & Ownership Mapping

To eliminate overlap, capability ownership is strictly centralized:

| Capability Domain | Historical Duplication | Canonical Unified Owner | Layer |
|---|---|---|---|
| Academic Corpus & Principles | Duplicated in `agent_harness` and `research_os` | `apodex/ai_eos/research/research_os.py` | Layer 1 |
| World Modeling | Fragmented between `wmc` and `aean` | `apodex/world_model/world_model.py` | Layer 2 |
| Active Inference Routing | Reimplemented across 3 sub-packages | `apodex/arcs/kernel/kernel.py` | Layer 2/3 |
| Multi-Agent Coordination | Duplicated in `hive_mind` and `hierarchical` | `apodex/aean/coordination/hive_mind.py` | Layer 2 |
| Strategic Opportunity Sizing | Present in `eos_engine` and `computational_architecture` | `apodex/ai_eos/intelligence/eos_first_principles.py` | Layer 3 |
| Skill Execution & Registry | Overlapping runner definitions | `apodex/skills/registry.py` & `runner.py` | Layer 4 |
| Verification & Governance | Split between `safety` and `verifier` | `apodex/governance/approval.py` & `harness/` | Layer 4 |

---

## 4. Core Cognitive Systems Integration & Redesign

### 4.1 Planning & Long-Horizon Task Execution
- **Hierarchical Graph-of-Thought (GoT):** Tasks are decomposed into directed acyclic goal graphs ($G = (V, E)$).
- **Backtracking & Rollback:** When a node execution fails or violates active inference expectations, the state machine backtracks to the nearest stable Bayesian belief checkpoint in CMOS.

### 4.2 Multi-Agent Coordination & Sycophancy Mitigation
- **Swarm Debate with Blinded Peer Review:** Multi-agent swarms do not share consensus early. Agents formulate independent hypotheses, followed by adversarial critique with anti-sycophancy noise injection ($\sigma^2 = 0.15$).
- **Bayesian Nash Equilibrium Clearing:** Resolves agent disagreements by computing payoff matrices and finding dominant strategies under uncertainty.

### 4.3 Causal World Models & Active Inference
- **Do-Calculus Interventions:** Evaluates counterfactuals ($do(X = x)$) to isolate causal effects from observational noise.
- **Expected Free Energy (EFE):**
  $$\text{EFE}(a) = \sum_{o} P(o|a) \ln \frac{P(o|a)}{P(o)} + \mathbb{E}_{P(o|a)} \left[ D_{KL}(P(\theta|o,a) \parallel P(\theta|a)) \right]$$
  Balances goal achievement (Pragmatic Value) with curiosity/uncertainty reduction (Epistemic Gain).

### 4.4 Software Engineering Automation & Self-Improvement
- **Automated Self-Harness Observer:** Continuously tracks turn-by-turn LLM outputs, tool call repetition, and token budget consumption.
- **Empirical Hypothesis Testing Engine:** Self-improvement code patches are treated as experimental treatments ($T$) evaluated against control baseline ($C$) using Welch's t-test statistic:
  $$t = \frac{\bar{X}_T - \bar{X}_C}{\sqrt{\frac{s_T^2}{N_T} + \frac{s_C^2}{N_C}}}$$
  Promotions require $p < 0.05$ after Holm-Bonferroni adjustment.

---

## 5. Architectural Analysis

### 5.1 Rationale & Benefits
1. **Zero Logical Duplication:** Clear boundary separation prevents competing state machines and redundant LLM prompts.
2. **Deterministic Governance:** Tiered approval gates enforce safety checks before state modification.
3. **Rigorous Scientific Grounding:** Principles are explicitly traceable to peer-reviewed publications in `AI_EOS_RESEARCH_DB.yaml`.

### 5.2 Trade-Offs & Complexity Budget
- **Trade-Off:** Increased contract rigidity requires explicit Pydantic V2 schema definitions for all inter-layer messages.
- **Complexity Analysis:** Overall system message complexity decreases from $O(N^2)$ (unstructured cross-module calling) to $O(N)$ layered downward calls. Memory footprint remains bounded under Ebbinghaus decay ($O(M)$ active items).

### 5.3 Failure Modes & Recovery Strategies
- **Failure Mode 1: Active Inference Local Minima.**
  *Recovery:* Inject epistemic curiosity bias ($\beta_{epistemic} \leftarrow \beta_{epistemic} \times 2.0$) to force exploration.
- **Failure Mode 2: Governance Circuit Breaker Trigger.**
  *Recovery:* System automatically shifts to `CostTier.LOW` budget, downshifting reasoning complexity and freezing non-essential tool executions.

---

## 6. Migration & Validation Strategy

1. **Migration Plan:** Deprecate legacy adapters in `agent_harness/`, routing calls through `apodex/` core contracts.
2. **Validation Strategy:** Execute regression test suite covering unit, integration, and failure injection scenarios.
3. **Target Benchmark:** 100% test pass rate across all 397+ test modules with $< 0.01\text{s}$ execution latency per cognition loop iteration.
