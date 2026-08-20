# Strategic Architecture Specification: Unified Autonomous Cognitive Operating System (AEAN / EIOS / EOS / APODEX)

**Version:** 2.0.0
**Status:** Canonical Strategic Architecture Standard
**Target:** `docs/architecture/UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md`

---

## Executive Summary & Strategic Mandate

Historically, enterprise AI platforms treated **Research OS**, **EIOS (Entrepreneurial Intelligence Operating System)**, **EOS (Entrepreneurial Operating System)**, **AEAN (Autonomous Economic Agent Network)**, and **APODEX** as distinct, semi-autonomous platforms. This legacy separation created severe structural flaws:
1. **Logical Duplication:** Overlapping memory stores, redundant world graph representation, and split-brain causal engines.
2. **Context Fragmentation:** Contextual losses across inter-system API translation boundaries.
3. **Execution Latency:** Multi-tier wrapper overhead and redundant serialization cycles.

This document establishes the **Unified Autonomous Cognitive Operating System Architecture**. We abolish system boundaries that lack distinct computational responsibilities. The platform is reorganized into a single **4-Tier Layered Cognitive Operating System Taxonomy**:

```
+---------------------------------------------------------------------------------------------------+
| LAYER 4: SCIENTIFIC RESEARCH LAYER (Research OS)                                                 |
| Problem Discovery | Literature Ingestion | Hypothesis Formalization | Walk-Forward Experimentation   |
+---------------------------------------------------------------------------------------------------+
                                                  |  Hypotheses & Empirical Principles
                                                  v
+---------------------------------------------------------------------------------------------------+
| LAYER 3: COGNITIVE INTELLIGENCE LAYER (AEAN)                                                      |
| Multi-Agent Swarms | Active Inference (EFE) | Structural Causal Models | Graph-of-Thought Strategy   |
+---------------------------------------------------------------------------------------------------+
                                                  |  Optimized Plans & Causal Actions
                                                  v
+---------------------------------------------------------------------------------------------------+
| LAYER 2: EXECUTION & ORCHESTRATION LAYER (EIOS / EOS)                                             |
| Multi-Timescale Loops | Capital Allocation (Kelly) | Risk & Capacity Management | Governance (GRC)    |
+---------------------------------------------------------------------------------------------------+
                                                  |  Bounded Directives & Resource Budgets
                                                  v
+---------------------------------------------------------------------------------------------------+
| LAYER 1: DECISION, MEMORY & WORLD MODEL RUNTIME (APODEX)                                          |
| Unified Memory (Working/Episodic/Semantic/Procedural) | E-K-C-T-U Multi-Graph | Tool Execution Engine |
+---------------------------------------------------------------------------------------------------+
```

---

## 1. Unified 4-Layer System Taxonomy

### Layer 4: Scientific Research Layer (Research OS)
- **Primary Domain:** Truth discovery, empirical evidence acquisition, and scientific validation.
- **Key Responsibilities:**
  - Automated problem discovery across market, code, and operational feedback streams.
  - Academic literature ingestion, metadata extraction, and Jaccard-ranked evidence indexing (`AI_EOS_RESEARCH_DB.yaml`).
  - Falsifiable hypothesis formalization with pre-registered trial protocols.
  - Walk-forward backtesting, synthetic market simulation, and Holm-Bonferroni p-value corrections.
- **Outputs:** Verified scientific principles and empirical evidence nodes injected into Layer 3.

### Layer 3: Cognitive Intelligence Layer (AEAN)
- **Primary Domain:** Multi-agent reasoning, probabilistic inference, and strategic planning.
- **Key Responsibilities:**
  - Expected Free Energy (EFE) active inference routing, balancing Epistemic Information Gain against Pragmatic Utility.
  - Judea Pearl Structural Causal Model (SCM) do-calculus interventions and counterfactual estimations.
  - Multi-agent swarm debate (Proponent, Red-Team, Base-Rate agents) with Bayesian Nash equilibrium clearing.
  - Graph-of-Thought (GoT) path search for long-horizon task execution.
- **Outputs:** Evaluated causal intervention policies and strategic execution trees passed to Layer 2.

### Layer 2: Execution & Orchestration Layer (EIOS / EOS)
- **Primary Domain:** Multi-timescale venture execution, resource allocation, and institutional governance.
- **Key Responsibilities:**
  - 13 coupled entrepreneurial feedback loops operating across micro ($10^{-1}\text{s}$), meso ($10^2\text{s}$), and macro ($10^5\text{s}$) timescales.
  - Fractional Kelly Criterion capital sizing discounted by Beta posterior confidence variance.
  - Real-time token consumption, latency, and financial budget enforcement (hard execution halts).
  - GRC (Governance, Risk, Compliance) policy evaluation and legal/constitutional veto gates.
- **Outputs:** Bounded operational directives and scheduled tool jobs dispatched to Layer 1.

### Layer 1: Decision, Memory & World Model Runtime (APODEX)
- **Primary Domain:** State persistence, environment perception, and physical tool execution.
- **Key Responsibilities:**
  - Unified Multi-Tier Memory: Working (ReAct buffer), Episodic (SQLite trajectory tables), Semantic (IKG graph), Procedural (skill registry).
  - Multi-Graph World Model (E-K-C-T-U): Entity ($G_E$), Knowledge ($G_K$), Causal ($G_C$), Temporal ($G_T$), Uncertainty ($G_U$).
  - Tool Invention & Execution Engine: Dynamic Python workflow compilation, sandbox sub-process isolation, and API adapters.
- **Outputs:** Environment state updates, trajectory logs, and execution outputs fed back up the stack.

---

## 2. Decoupled System Interfaces & Pydantic Contracts

Systems interact strictly through type-safe, asynchronous Pydantic contracts. Direct cross-layer class instantiation is forbidden.

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class EvidenceNode(BaseModel):
    paper_id: int
    title: str
    transferable_principle: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    empirical_p_value: float

class CausalInterventionRequest(BaseModel):
    intervention_target: str
    do_action: Dict[str, Any]
    expected_utility_threshold: float
    max_token_budget: int

class CapitalAllocationRequest(BaseModel):
    venture_id: str
    beta_alpha: float
    beta_beta: float
    estimated_roi: float
    max_capital_pool: float

class ExecutionDirective(BaseModel):
    directive_id: str
    target_skill: str
    parameters: Dict[str, Any]
    hard_timeout_seconds: float
    max_tokens: int
```

---

## 3. Core Mathematical Formulations

### 3.1 Active Inference & Expected Free Energy (EFE)
In Layer 3 (AEAN), action selection $a^*$ minimizes Expected Free Energy $G(a)$:

$$G(a) = - \underbrace{\mathbb{E}_{q(o|a)} [\log p(o)]}_{\text{Pragmatic Utility}} - \underbrace{\mathbb{E}_{q(s, o|a)} [\log q(s|o, a) - \log q(s|a)]}_{\text{Epistemic Information Gain}}$$

### 3.2 Fractional Kelly Capital Allocation
In Layer 2 (EOS), capital allocation fraction $f^*$ scales with posterior uncertainty derived from Beta distribution parameters $(\alpha, \beta)$:

$$\mu = \frac{\alpha}{\alpha + \beta}, \quad \sigma^2 = \frac{\alpha \beta}{(\alpha + \beta)^2 (\alpha + \beta + 1)}$$

$$f^* = \lambda \cdot \left( \mu - \frac{1 - \mu}{R} \right) \cdot \left( 1 - \sqrt{\sigma^2} \right)$$

where $R$ is the risk-adjusted return ratio and $\lambda \in (0, 1]$ is the fractional Kelly scale.

### 3.3 Dynamic Overlap Context Matching (MemoHarness)
In Layer 1 (APODEX), memory retrieval ranks historical episodes using Jaccard token overlap scaled by recency decay:

$$S(q, d) = \frac{|T_q \cap T_d|}{|T_q \cup T_d|} \cdot \exp\left(-\gamma \cdot \Delta t\right)$$

---

## 4. Safety, Governance, & Non-Degradation Guarantees

1. **Immutable Safety Core:** Tier 4 security and tenancy policies are hardcoded and protected from self-evolution modifications.
2. **Real-time Hard Halt:** Step-level interceptors terminate agent execution immediately if token footprint or latency limits are breached.
3. **Statistical Promotion Filter:** Proposed prompt/harness changes require Welch's t-test validation ($p < 0.05$) against frozen baselines in isolated sub-processes.
