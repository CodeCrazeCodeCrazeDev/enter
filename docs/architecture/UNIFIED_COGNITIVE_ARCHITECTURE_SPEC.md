# Unified Cognitive Operating System Architecture Specification
**Author:** Jules (Autonomous Strategic Architecture Engineer)
**Version:** 2.0.0-UNIFIED
**Subsystems Unified:** Research OS, AEAN, EIOS / EOS, APODEX

---

## 1. Executive Summary & Paradigm Shift

The Unified Cognitive Operating System establishes a single, multi-layered cognitive paradigm for autonomous agency, continuous scientific discovery, entrepreneurial reasoning, and software engineering.

Historically, autonomous AI platforms operated as disjointed, partially overlapping subsystems:
- **Research OS** managed literature synthesis and experiment execution in isolation.
- **AEAN (Autonomous Entrepreneurship Agent Network)** handled multi-agent coordination and cognitive inference.
- **EIOS / EOS (Entrepreneurial Operating System)** controlled strategy loops, capital allocation, and business lifecycle state machines.
- **APODEX** executed tool calls, maintained long-term memory (CMOS/EMG), and handled runtime sandboxing.

### The Unified 4-Layer Cognitive Operating System Taxonomy
To eliminate logical redundancy, circular dependencies, and cognitive fragmentation, all responsibilities are decoupled into a **Single Layered Cognitive Stack**:

```
+-----------------------------------------------------------------------------------+
| LAYER 1: RESEARCH LAYER (Research OS)                                              |
| - Scientific Discovery Engine, Hypothesis Generation, Literature Jaccard Ranking   |
| - Statistical Power Analysis, Holm-Bonferroni & Deflated Sharpe Validation        |
| - Research Provenance Tracing (Paper -> Principle -> Hypothesis -> Decision)     |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| LAYER 2: COGNITIVE INTELLIGENCE LAYER (AEAN)                                      |
| - Active Inference Engine (Expected Free Energy minimization: Pragmatic + Epistemic)|
| - Causal World Model & Pearl's Do-Calculus Structural Causal Models (SCMs)        |
| - Multi-Agent Swarm Debate & Sycophancy Mitigation (Bayesian Nash Clearing)       |
| - Ebbinghaus Context Decay & Skill Flywheel (60 Operational/Strategic Skills)     |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| LAYER 3: ORCHESTRATION & STRATEGY LAYER (EIOS / EOS)                              |
| - Multi-Timescale Control Loops (T1 Execution -> T2 Iteration -> T3 Strategy)     |
| - Signal-to-Hypothesis Gating & Opportunity Anomaly Sensing                       |
| - Capital & Risk Allocation (Lagrange Shadow Pricing, Downshifting/Halting)       |
| - Entrepreneurial Lifecycle State Machines & Governance Gates                    |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| LAYER 4: EXECUTION & RUNTIME INFRASTRUCTURE LAYER (APODEX)                        |
| - Deterministic Sub-agent Execution & Tool Orchestration (Playwright, Bash, Git)  |
| - Multi-Tier Memory (CMOS Episodic / EMG Action-Decision Graph Engine)            |
| - Institutional Safety, Pre-commit Enforcement, and Rate-Limiting Governance     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core System Layering & Interface Specifications

### 2.1 Layer 1: Research OS (Research & Scientific Discovery)
- **Primary Responsibility:** Scientific hypothesis generation, literature indexing, statistical power calculations, walk-forward validation, and deflated Sharpe ratio analysis.
- **Input Interfaces:**
  - `register_hypothesis(title, statement, null_hypothesis, target_metric, alpha)`
  - `conduct_literature_review(domain_keyword)`
- **Output Interfaces:**
  - `execute_experiment_simulation(experiment_id, ground_truth_yield)` -> Returns validated or refuted hypothesis with exact $p$-value and deflated Sharpe ratio.

### 2.2 Layer 2: AEAN (Cognitive Intelligence)
- **Primary Responsibility:** Active inference decision routing, causal structural intervention, swarm consensus clearing, and skill synthesis.
- **Input Interfaces:**
  - `evaluate_action_efe(pragmatic_value, epistemic_information_gain)`
  - `apply_causal_intervention(variable, outcome)`
- **Output Interfaces:**
  - `resolve_swarm_consensus(agent_votes)` -> Cleared decision vector with sycophancy penalty.

### 2.3 Layer 3: EIOS / EOS (Orchestration & Strategy)
- **Primary Responsibility:** Multi-timescale feedback loops, capital downshifting/halting, opportunity scoring, and lifecycle stage transitions.
- **Input Interfaces:**
  - `sense_opportunity_anomalies(market_signals)`
  - `allocate_capital_opportunity(opportunity_id, budget)`
- **Output Interfaces:**
  - `evaluate_lifecycle_stage(business_metrics)` -> Returns active state transition (e.g. `SCALE_PHASE`).

### 2.4 Layer 4: APODEX (Decision & Execution Runtime)
- **Primary Responsibility:** Safe execution of tool operations, memory graph persistence (CMOS/EMG), and deterministic sub-agent sandboxing.
- **Input Interfaces:**
  - `execute_tool(tool_name, parameters)`
  - `retrieve_context(query, max_tokens)`
- **Output Interfaces:**
  - `ExecutionResult(status, logs, output_artifacts)`

---

## 3. Mathematical Foundations & Control Theory Formulations

### 3.1 Expected Free Energy (EFE) Active Inference
Actions are chosen by minimizing Expected Free Energy $G(\pi)$ for policy $\pi$:
$$G(\pi) = - \underbrace{\mathbb{E}_{q(o|\pi)}[\ln p(o)]}_{\text{Pragmatic Value (Utility)}} - \underbrace{\mathbb{E}_{q(\theta|\pi)}[D_{KL}(q(\theta|o,\pi) \parallel q(\theta|\pi))]}_{\text{Epistemic Information Gain}}$$

### 3.2 Deflated Sharpe Ratio & Holm-Bonferroni Multiple Testing
To eliminate backtest over-fitting during autonomous experiment execution:
$$DSR = \frac{\hat{\mu}}{\hat{\sigma} \sqrt{2 \ln(\max(2, N_{trials}))}}$$
$$p_{corrected} = p \times N_{trials} < \alpha_{Bonferroni}$$

---

## 4. Architectural Trade-offs & Failure Modes

| Subsystem Layer | Risk / Failure Mode | Mitigating Architectural Mechanism |
| :--- | :--- | :--- |
| **Research OS** | False discovery from multi-testing bias | Holm-Bonferroni correction & Deflated Sharpe Ratio thresholds |
| **AEAN** | Swarm sycophancy & echo chambers | Bayesian Nash Equilibrium clearing with compliance penalty factors |
| **EIOS / EOS** | Runaway capital allocation on failing hypotheses | Automated budget downshifting (25% stepdown) & hard circuit halting |
| **APODEX** | Long-context memory drift | Ebbinghaus exponential memory decay filtering & EMG graph pruning |

---

## 5. Migration & Consolidation Roadmap
1. **Adapter Elimination:** All legacy `agent_harness` calls redirect to canonical `apodex` modules via explicit compatibility adapters.
2. **Interface Harmonization:** Pure type-safe Pydantic V2 models across all layer boundaries.
3. **100% Test Validation:** Execution of 397 unit, integration, and performance benchmark tests confirming zero regressions.
