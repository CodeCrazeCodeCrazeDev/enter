# Unified Cognitive OS Architecture Specification

## 1. Executive Summary & Architectural Vision

The **Unified Cognitive Operating System** integrates five historically distinct subsystems—**Research OS**, **AEAN (Autonomous Enterprise Agent Network)**, **EIOS (Entrepreneurial Intelligence Operating System)**, **EOS (Entrepreneurial Operating System)**, and **APODEX (Autonomous Intelligence & Execution Platform)**—into a single, multi-layered cognitive substrate.

Rather than running independent frameworks with overlapping responsibilities, the architecture strictly enforces a **4-Layer Decoupled Taxonomy**:

```
+-----------------------------------------------------------------------------------+
|                        1. RESEARCH OS (Research Layer)                            |
| Scientific discovery, empirical bibliography (200+ DB), hypothesis generation,     |
| statistical trial execution, Holm-Bonferroni corrections, provenance tracing.     |
+-----------------------------------------------------------------------------------+
                                        | (Falsifiable Hypotheses & Research Principles)
                                        v
+-----------------------------------------------------------------------------------+
|                   2. AEAN (Cognitive Intelligence Swarm Layer)                   |
| Active Inference (Expected Free Energy), Causal World Modeling (Pearl Do-Calculus)|
| Bayesian Nash Equilibrium, Graph-of-Thought reasoning, sycophancy mitigation.     |
+-----------------------------------------------------------------------------------+
                                        | (Emergent Plans & Optimal Policy Actions)
                                        v
+-----------------------------------------------------------------------------------+
|              3. EIOS / EOS (Execution & Orchestration Loop Layer)                 |
| 13 coupled business loops, 15-stage customer journey, 9 growth stages,            |
| real-time macro shock reaction, Lagrange shadow pricing, portfolio sizing.       |
+-----------------------------------------------------------------------------------+
                                        | (Task Directives & State Machines)
                                        v
+-----------------------------------------------------------------------------------+
|                   4. APODEX (Decision & Action Engine Layer)                      |
| 60-skill registry, multi-tier memory (CMOS/Semantic/Working), safety governance,   |
| AgentHarness runtime execution adapters, tool orchestration.                      |
+-----------------------------------------------------------------------------------+
```

---

## 2. Decoupled 4-Layer Taxonomy & Subsystem Responsibilities

### Layer 1: Research OS (Research Layer)
* **Canonical Path**: `apodex/ai_eos/research/research_os.py`
* **Core Responsibilities**:
  - Mainment and ingestion of the 200-paper `AI_EOS_RESEARCH_DB.yaml` and 100-paper `ALPHA_ALGO_100_NEW_RESEARCH.yaml` research database.
  - Generating falsifiable scientific hypotheses based on empirical research principles.
  - Power analysis and sample size estimation ($\beta = 0.80, \alpha = 0.05$).
  - Statistical hypothesis evaluation via Welch's t-test and Holm-Bonferroni multi-testing correction.
  - Provenance tracing mapping every runtime decision back to original research papers.

### Layer 2: AEAN (Cognitive Intelligence & Swarm Layer)
* **Canonical Path**: `apodex/aean/coordination/hive_mind.py`
* **Core Responsibilities**:
  - Active Inference trajectory evaluation optimizing Expected Free Energy ($G(\pi)$):
    $$G(\pi) = \text{Pragmatic Value} + \text{Epistemic Information Gain}$$
  - Pearl's Causal Do-Calculus interventional reasoning ($P(Y | do(X))$) to remove observational confounding.
  - Game-theoretic multi-agent clearing via Bayesian Nash Equilibrium auctions.
  - Sycophancy mitigation through adversarial peer review and Graph-of-Thought (GoT) exploration.

### Layer 3: EIOS / EOS (Execution & Orchestration Loop Layer)
* **Canonical Path**: `apodex/arcs/kernel/kernel.py` & `apodex/ai_eos/intelligence/eos_first_principles.py`
* **Core Responsibilities**:
  - Multi-timescale control loops (tactical hourly, strategic weekly, directional quarterly).
  - Opportunity anomaly detection across macroeconomic and microeconomic signals.
  - Advanced Kelly Criterion capital allocation with shadow price Lagrange bounds:
    $$f^* = \frac{p \cdot b - q}{b}$$
  - Macroeconomic shock response state machines and decision fatigue monitoring.

### Layer 4: APODEX (Decision & Action Engine Layer)
* **Canonical Path**: `apodex/skills/registry.py`, `apodex/memory/`, `agent_harness/`
* **Core Responsibilities**:
  - Pre-populated 60-skill registry for deterministic tool execution.
  - Unified Memory Architecture: Episodic Memory, Working Memory, Semantic Memory, and Cognitive Memory Operating System (`CMOS`).
  - Safety and governance guardrails with multi-tiered approval workflows.
  - Runtime execution adapters provided by `agent_harness`.

---

## 3. Mathematical Formulations & Control Theory

1. **Expected Free Energy (Active Inference)**:
   $$G(\pi) = -\mathbb{E}_{q(o, \theta | \pi)}[\ln p(o)] - \mathbb{E}_{q(\theta | \pi)}[D_{KL}(q(o | \theta, \pi) \parallel p(o | \theta))]$$
2. **Causal Do-Calculus Interventions**:
   $$P(Y | do(X = x)) = \sum_z P(Y | X = x, Z = z) P(Z = z)$$
3. **Ebbinghaus Memory Retention Decay**:
   $$R(t) = \exp\left(-\frac{t}{S}\right)$$
4. **Holm-Bonferroni Adjusted Significance**:
   $$p_{(i)} \le \frac{\alpha}{m - i + 1}$$

---

## 4. Institutional-Grade Reliability & Continuous Safety

- **Deterministic Fallbacks**: Every cognitive agent falls back gracefully to rule-based heuristics if LLM inference latency exceeds budget ($> 2.50\text{s}$).
- **State Corruptibility Defenses**: CMOS vector store verifies checksums on every memory fetch; invalid nodes are automatically pruned.
- **Complexity Budgeting**: Total runtime complexity bound strictly maintained at $O(N \log N)$ where $N$ is swarm size.
