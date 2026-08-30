# Unified Cognitive Architecture Specification
**Subsystems:** Research OS | EIOS | EOS | AEAN | APODEX
**Version:** 4.0.0-UNIFIED
**Status:** Canonical Strategic Blueprint

---

## 1. Executive Summary & Architectural Rationale

Historically, cognitive software platforms treat research engines, execution frameworks, multi-agent orchestrators, and tool runtime environments as disjoint systems. This separation creates severe architectural defects:
1. **Logical Duplication:** Duplicate planning engines, disconnected memory stores, and overlapping state machines across subsystems.
2. **Brittle Context Handoffs:** Loss of statistical and epistemic context when hypotheses transition from scientific discovery to runtime execution.
3. **Incoherent Decision-Making:** Misalignment between strategic resource allocation (EOS) and agent task execution (AEAN).

This specification resolves these defects by establishing a single, unified **4-Layer Cognitive Operating System Taxonomy**. Rather than maintaining five disconnected platforms, **Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX** are explicitly mapped into four strictly non-overlapping, integrated architectural layers:

```
+-----------------------------------------------------------------------------------+
| LAYER 4: DECISION & PLATFORM EXECUTION (APODEX)                                   |
| - Skill Flywheel Execution Engine    - Governance & Compliance Gateway            |
| - Automated Software Engineering    - Sandboxed Tool Runtime                     |
+-----------------------------------------------------------------------------------+
                                        ^
                                        | (Skill Requests & Tool Execution)
                                        v
+-----------------------------------------------------------------------------------+
| LAYER 3: COGNITIVE INTELLIGENCE (AEAN)                                             |
| - HiveMind Multi-Agent Swarm          - Graph-of-Thought (GoT) Reasoning          |
| - CMOS Tiered Memory Subsystem       - World Model Counterfactual Simulator       |
+-----------------------------------------------------------------------------------+
                                        ^
                                        | (DAG Task Dispatch & Cognitive State)
                                        v
+-----------------------------------------------------------------------------------+
| LAYER 2: EXECUTION & ORCHESTRATION (EIOS / EOS)                                   |
| - EOS Strategic State Machine         - Active Inference EFE Sensing (EIOS Kernel) |
| - Dynamic Resource & Budget Allocator - Institutional Risk & SLA Control Engine   |
+-----------------------------------------------------------------------------------+
                                        ^
                                        | (Hypothesis Ingestion & EFE Signals)
                                        v
+-----------------------------------------------------------------------------------+
| LAYER 1: SCIENTIFIC RESEARCH & HYPOTHESIS DISCOVERY (Research OS)                 |
| - Corpus Ingestion Pipeline          - Statistical Validation Engine              |
| - Active Inference Hypothesis Generator - Literature Review Synthesis             |
+-----------------------------------------------------------------------------------+
```

---

## 2. Layered Architecture & Subsystem Mapping

### Layer 1: Scientific Research & Hypothesis Discovery Layer (Research OS)
- **Primary Responsibility:** Autonomous scientific inquiry, literature ingestion across 400+ research papers, empirical statistical validation, and causal hypothesis generation.
- **Canonical Subsystem:** `apodex.research_os` & `apodex.ai_eos.research`
- **Key Modules:**
  - `ResearchOS`: Ingests literature, synthesizes domain principles via `conduct_literature_review()`.
  - `StatisticalValidationEngine`: Computes Deflated Sharpe Ratio (DSR), Welch's t-tests, and probability-clamped normal distribution bounds (`standard_normal_ppf`).
  - `ResearchToSystemBridge`: Formally translates validated hypotheses into Active Inference priors.
- **Eliminated Duplication:** Removed redundant ad-hoc research parsers in AEAN and EOS.

### Layer 2: Execution & Orchestration Layer (EIOS / EOS)
- **Primary Responsibility:** Strategic decision state machine, environmental anomaly sensing, budget allocation, and active inference Expected Free Energy (EFE) minimization.
- **Canonical Subsystems:** `apodex.arcs.kernel` (EIOS) & `apodex.ai_eos.intelligence` (EOS)
- **Key Modules:**
  - `EIOSKernel`: Senses environmental anomalies and calculates epistemic/pragmatic value components ($EFE = \text{Ambiguity} + \text{Risk}$).
  - `EOSEngine` & `ComputationalArchitectureOfEntrepreneurship`: 14-layer computational engine handling corporate lifecycle transitions, risk thresholds, and capital allocation.
  - `LearnableRoutingGateDispatcher`: Routes tasks dynamically based on causal do-calculus interventions and budget constraints.
- **Eliminated Duplication:** Consolidated disparate planners into unified Active Inference EFE scheduler.

### Layer 3: Cognitive Intelligence Layer (AEAN)
- **Primary Responsibility:** Swarm multi-agent coordination, Graph-of-Thought (GoT) reasoning, long-term cognitive memory, and counterfactual world modeling.
- **Canonical Subsystem:** `apodex.aean` & `apodex.cognition`
- **Key Modules:**
  - `HiveMind`: Token-bidding multi-agent auction registry with sycophancy mitigation.
  - `CognitiveBrain` & `GraphOfThoughtEngine`: Executes structured reasoning DAGs with self-contradiction detection.
  - `CMOS` (Cognitive Memory Operating System): Epistemic, semantic, and procedural memory with Ebbinghaus forgetting decay ($R = e^{-t / S}$).
  - `WorldModel`: Counterfactual state trajectory simulation and credit halt enforcement.
- **Eliminated Duplication:** Unified memory architectures under CMOS, deprecating isolated memory stores.

### Layer 4: Decision & Platform Execution Layer (APODEX)
- **Primary Responsibility:** Operational decision execution, skill protocol execution, safety gateway enforcement, and automated software engineering.
- **Canonical Subsystem:** `apodex.skills` & `apodex.governance`
- **Key Modules:**
  - `SkillRegistry` & `SkillRunner`: Pre-populated registry of 60 operational skills executed with step-by-step state tracking.
  - `InstitutionalGovernanceGateway`: Tiered approval routing, cost profiling, SLA rollback mechanics, and compliance audit logging.
  - `CodeRewriteEngine`: Automated software synthesis and self-healing refactoring with Non-Gaussian Hawkes stability bounds.
- **Eliminated Duplication:** Mapped all low-level tool calls to the central `SkillRegistry`.

---

## 3. Core Cognitive System Capabilities

### 3.1 Long-Horizon Autonomous Execution & Planning Under Uncertainty
The unified system uses Active Inference (Friston et al.) to formulate planning as variational inference. At Layer 2, `EIOSKernel` computes Expected Free Energy ($G(\pi)$) for candidate policies $\pi$:
$$G(\pi) = \sum_\tau \left( D_{\text{KL}}[q(o_\tau | \pi) || p(o_\tau)] + \mathbb{E}_{q(s_\tau | \pi)}[H(q(o_\tau | s_\tau))] \right)$$
where the first term represents **Risk** (pragmatic goal seeking) and the second term represents **Ambiguity** (epistemic exploration).

### 3.2 World Modeling & Counterfactual Forecasting
`WorldModel` in Layer 3 maintains probabilistic belief states over system environment states $S_t$. Before executing action $A_t$ in Layer 4:
1. Counterfactual trajectories are simulated across $K$ Monte Carlo rollouts.
2. Anomaly likelihood is evaluated against safety bounds.
3. Credit Halt guards trigger automatic rollback if predicted loss exceeds allocation thresholds.

### 3.3 Multi-Agent Swarm Collaboration (HiveMind)
`HiveMind` eliminates multi-agent sycophancy and collusion through sealed token-bidding auctions:
- Agents bid on task execution based on local capability confidence scores.
- Cross-agent consensus requires independent verification, preventing information cascade failures.

### 3.4 Tiered Memory & Ebbinghaus Decay (CMOS)
Memory retention rate $R(t)$ is governed by:
$$R(t) = \exp\left(-\frac{t}{S \cdot (1 + \Delta_{\text{epistemic}})}\right)$$
High-value verified scientific insights from Layer 1 inflate strength parameter $S$, shielding critical knowledge from decay while pruning noise.

---

## 4. Subsystem Interface Contracts

```python
# Layer 1 -> Layer 2 Handoff
class ScientificHypothesisPayload(BaseModel):
    hypothesis_id: str
    paper_citations: List[str]
    transferable_principles: List[str]
    dsr_score: float  # Deflated Sharpe Ratio >= 0.95
    p_value: float    # Welch's t-test p < 0.01

# Layer 2 -> Layer 3 Task Dispatch
class OrchestrationTaskDAG(BaseModel):
    task_id: str
    active_inference_efe: float
    allocated_budget_usd: float
    max_latency_ms: float
    required_agent_roles: List[str]

# Layer 3 -> Layer 4 Execution Request
class SkillExecutionDirective(BaseModel):
    skill_name: str
    params: Dict[str, Any]
    governance_tier: str # "auto", "human_in_loop", "strict"
    timeout_seconds: float
```

---

## 5. Architectural Quality Attributes & Complexity Budgets

| Attribute | Baseline | Target Unified OS | Verification Method |
| :--- | :--- | :--- | :--- |
| **Cross-Layer Latency** | 450 ms | **< 45 ms** | End-to-end integration benchmarks |
| **Statistical Validity** | Ad-hoc | **DSR >= 0.95 / Welch p < 0.01** | `StatisticalValidationEngine` unit test |
| **Context Memory Efficiency** | 42% retention | **94% precision @ 10k steps** | Ebbinghaus decay simulation suite |
| **Multi-Agent Sycophancy** | 28% compliance bias | **< 2% compliance bias** | HiveMind counter-factual debate test |
| **System Reliability** | SLA breaches on drift | **0 breach (Automated SLA Rollback)** | `InstitutionalGovernanceGateway` test |

---

## 6. Migration & Deprecation Strategy

1. **Adapter Elimination:** Deprecate legacy harness wrapper adapters in `agent_harness` by routing calls directly to Layer 1–4 canonical engines in `apodex/`.
2. **Schema Alignment:** Standardize all state representations onto Pydantic V2 `ConfigDict(arbitrary_types_allowed=True)`.
3. **Registry Centralization:** All operational actions MUST execute through Layer 4 `SkillRegistry`. Direct tool invocations outside the registry are prohibited.
