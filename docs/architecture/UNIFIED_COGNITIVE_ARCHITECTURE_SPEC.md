# Unified 4-Layer Cognitive Operating System Architecture Specification
**Authoritative Architectural Standard for Autonomous Intelligence & Entrepreneurial Execution**
**Version:** 4.0.0 (Unified 2026 Release)
**Status:** Canonical Reference Specification

---

## Executive Overview

This specification establishes the unified architecture for the Autonomous Intelligence Platform, integrating **Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX** into a single, layered cognitive operating system.

Historically, these five subsystems operated as distinct software projects with overlapping responsibilities across memory management, multi-agent dispatch, planning, and domain state tracking. This architectural specification eliminates logical duplication and consolidates all platform operations into a **Unified 4-Layer Cognitive Architecture Taxonomy**:

```
+---------------------------------------------------------------------------------------+
| LAYER 1: SCIENTIFIC RESEARCH & HYPOTHESIS ENGINE (Research OS)                         |
| - Scientific Hypothesis Generation, Experimental Design & Literature Synthesis       |
| - Walk-Forward Validation, Deflated Sharpe Ratio (DSR), White's Reality Check        |
+---------------------------------------------------------------------------------------+
                                          | Active Inference State Handoff
                                          v
+---------------------------------------------------------------------------------------+
| LAYER 2: SENSING, EXECUTION & DECISION ENGINE (EIOS Kernel & EOS Engine)              |
| - Active Inference Sensing & Expected Free Energy (EFE) Minimization                  |
| - Entrepreneurial Opportunity Trees, Coupled Business Loops & Capital Allocation     |
+---------------------------------------------------------------------------------------+
                                          | Task DAGs & Strategic Directives
                                          v
+---------------------------------------------------------------------------------------+
| LAYER 3: COGNITIVE INTELLIGENCE & MULTI-AGENT SWARM (AEAN HiveMind)                   |
| - Agent Token Economics & Second-Price Resource Arbitration                           |
| - Non-Gaussian Hawkes Process Scheduling & Learnable EFE Routing Dispatchers           |
| - Graph-of-Thought (GoT) Multi-Path Reasoning & ShinkaEvolve Genetic Optimization     |
+---------------------------------------------------------------------------------------+
                                          | Tool Actions & Code Syntheses
                                          v
+---------------------------------------------------------------------------------------+
| LAYER 4: WORLD MODEL & EXECUTION PLATFORM (APODEX WorldModel & Runtime Engine)        |
| - Causal DAG Entity Graphs & Recursive Bayesian Belief Propagation                    |
| - Micro-VM Sandbox Execution, AST Linting & GRC Compliance Governance                 |
| - DPO Preference Trajectory Collection & Continuous Flywheel Learning                  |
+---------------------------------------------------------------------------------------+
```

---

## 1. Unified 4-Layer Architectural Taxonomy

### Layer 1: Scientific Research Layer (Research OS)
- **Canonical Module Location:** `apodex/ai_eos/research/` & `apodex/research_os/`
- **Core Purpose:** Formal scientific hypothesis discovery, experimental design, literature synthesis, and statistical verification.
- **Key Responsibilities:**
  1. **Hypothesis Registration & Lifecycle Management:** Captures domain hypotheses ($H_0$ vs $H_1$) with configurable significance thresholds ($\alpha$).
  2. **Automated Experimental Design:** Performs power analysis calculations ($n = 2(z_{\alpha/2} + z_{\beta})^2 / d^2$) to calculate required statistical sample size.
  3. **Walk-Forward Validation:** Evaluates hypothesis outcomes under out-of-sample temporal constraints.
  4. **Selection Bias Protection:** Applies Deflated Sharpe Ratio (DSR) and White's Reality Check (WRC) with Bonferroni alpha adjustments ($\alpha_{\text{corrected}} = \alpha / k$) to eliminate p-hacking in automated experiment loops.
  5. **Literature Review Synthesis:** Synthesizes structured knowledge vectors across active research namespaces.

### Layer 2: Sensing, Execution & Decision Layer (EIOS Kernel & EOS Engine)
- **Canonical Module Location:** `apodex/arcs/kernel/` & `apodex/ai_eos/intelligence/`
- **Core Purpose:** Active inference sensing, entrepreneurial reasoning, strategic decision-making, and macro execution DAG orchestration.
- **Key Responsibilities:**
  1. **Active Inference Sensing:** Measures environmental anomaly signals ($y_t$) against generative priors using Expected Free Energy ($G(\pi)$):
     $$G(\pi) = \text{Epistemic Uncertainty} + \text{Pragmatic Utility} - \text{Financial/Compute Cost}$$
  2. **First-Principles EOS Engine:** Executes coupled business loops (Demand Sensing, Narrative Engineering, Creative Production, Funnel Conversion, Capital Rebalancing).
  3. **Opportunity Decision Trees:** Evaluates commercial yield vs risk profiles and assigns capital allocation budgets across active initiatives.
  4. **14-Layer Computational Entrepreneurship Engine:** Coordinates lower-level operational engines from Reality Substrate up to Autonomous AI Entrepreneurship.

### Layer 3: Cognitive Intelligence Layer (AEAN HiveMind)
- **Canonical Module Location:** `apodex/aean/` & `apodex/cognition/`
- **Core Purpose:** Multi-agent swarm orchestration, token-based compute resource arbitration, learnable task dispatching, and advanced reasoning.
- **Key Responsibilities:**
  1. **Agent Token Economics:** Implements second-price resource allocation where specialized agents submit bids ($B_i = \text{Priority} \times (0.5 + \text{EV})$) for finite compute tokens.
  2. **Non-Gaussian Hawkes Scheduling:** Models event self-excitation to prevent resource starvation during task cascades.
  3. **Learnable Routing Gate Dispatcher:** Matches incoming task complexity and domain context to optimal agent profiles using conjugate Bayesian parameter updates.
  4. **Graph-of-Thought (GoT) Reasoning:** Executes non-linear thought graph exploration with backtracking, contraction, and cycle verification.
  5. **Genetic Workflow Optimization (ShinkaEvolve):** Mutates and evaluates program genomes using MAP-Elites parameter space exploration.

### Layer 4: World Model & Execution Platform (APODEX WorldModel & Runtime)
- **Canonical Module Location:** `apodex/world_model/` & `apodex/execution/`
- **Core Purpose:** Platform state representation, persistent causal graph storage, micro-VM code execution, compliance governance, and continuous preference learning.
- **Key Responsibilities:**
  1. **Causal Graph Manager:** Tracks entities, attributes, and directional relationships ($E \xrightarrow{\text{causes}} E'$) with scalar edge weights.
  2. **Recursive Bayesian Belief Propagation:** Updates belief confidence ($P(B|E) = \frac{P(E|B)P(B)}{P(E)}$) as new empirical observations arrive.
  3. **Micro-VM Sandbox Execution:** Isolates tool execution and self-referential code rewrites inside AST-validated security boundaries.
  4. **DPO Preference Trajectory Logging:** Compiles trajectory traces into Advantage-weighted preference pairs ($A_t = G_t - V(s)$) for continuous model fine-tuning.
  5. **GRC Governance & Audit:** Enforces automated compliance gates, risk approvals, and deterministic audit trails.

---

## 2. Redesign of Core Cognitive Systems

### A. Planning & Scheduling
- **Redesign:** Transition from static linear sequential planners to dynamic, budget-bounded Active Inference Planners with Graph-of-Thought search and Hawkes process event scheduling.
- **Mechanism:** Tasks are modeled as probabilistic sub-goal graphs where each branch is scored by Expected Free Energy. Hawkes intensity functions ($\lambda(t) = \mu + \sum \alpha e^{-\beta(t - t_i)}$) dynamically shift queue priorities during load spikes.

### B. World Models & Simulation
- **Redesign:** Combine discrete relational schemas with continuous Bayesian belief states into a unified Causal Graph Manager (`WorldGraphManager`).
- **Mechanism:** Entities represent physical, financial, and agent states; directed edges encode causal dependency. Recursive Bayesian updates ensure real-time state re-estimation without full graph rebuilds.

### C. Multi-Agent Coordination & Communication
- **Redesign:** Replace unstructured peer-to-peer agent messaging with AEAN HiveMind token-based market arbitration.
- **Mechanism:** Agents bid compute tokens for task execution rights. Clearing prices are determined via second-price auction mechanics, guaranteeing parsimonious resource utilization.

### D. Memory Systems & Knowledge Management
- **Redesign:** Unified tri-layer memory architecture comprising Short-Term Context, Epistemic Semantic Memory, and Long-Term Trajectory Memory (CMOS).
- **Mechanism:** Memory records are indexed by vector embeddings, causal graph references, and temporal decay functions, supporting zero-loss retrieval across long-horizon executions.

### E. Software Engineering Automation & Self-Improvement
- **Redesign:** Integrated AST-validated Code Rewrite Engine with GRC security checks and genetic program synthesis.
- **Mechanism:** Code modifications undergo AST parsing, dangerous call elimination (`eval`/`os.system` blocking), dry-run compilation in micro-VM sandboxes, and walk-forward regression testing prior to main branch integration.

---

## 3. Capability Ownership Matrix (Elimination of Duplication)

| Functionality | Canonical Owner | Deprecated / Refactored Module |
| :--- | :--- | :--- |
| Hypothesis Registration & Validation | `apodex/ai_eos/research/research_os.py` | Legacy ad-hoc scripts in `AgentHarness` |
| Active Inference Sensing | `apodex/arcs/kernel/kernel.py` | Hardcoded mock observers |
| Entrepreneurial State Machine | `apodex/ai_eos/intelligence/eos_engine.py` | Standalone uncoordinated business loops |
| Multi-Agent Token Arbitration | `apodex/aean/coordination/hive_mind.py` | Manual priority queues |
| Causal State & Entity Storage | `apodex/world_model/graph/world_graph.py` | Isolated local state dicts |
| Self-Referential Code Rewrite | `apodex/ai_eos/research/integration.py` | Unchecked regex string replacements |

---

## 4. Technical Debt Elimination & Elimination Strategy

1. **Zero Mock Wrappers:** All execution loops, step decompositions, uncertainty measures, and worker summaries are dynamically derived using first-principles mathematical implementations.
2. **Backwards Compatibility Adapter Harness:** Deprecated imports from `agent_harness` route seamlessly to canonical `apodex` engines via thin compatibility adapters located in `agent_harness/`.
3. **Type Safety & Metric Clamping:** Probability values in statistical and Bayesian components are strictly clamped to $[10^{-12}, 1 - 10^{-12}]$ to prevent zero-division and numerical instability.
