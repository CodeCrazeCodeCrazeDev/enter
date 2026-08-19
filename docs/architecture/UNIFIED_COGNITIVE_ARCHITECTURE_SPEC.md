# Unified Cognitive Operating System Architecture Specification
**Author:** Jules, Lead Architect & Software Engineer
**Status:** Canonical Approved Standard
**Version:** 2.0.0
**Target Architecture:** Research OS / AEAN / EIOS & EOS / APODEX

---

## Executive Summary & First-Principles Philosophy

The **Unified Cognitive Operating System (Cognitive OS)** represents a fundamental paradigm shift in autonomous AI engineering. Previously, complex agent systems suffered from "platform sprawl"—treating Research OS, EIOS (Entrepreneurial Operating System), EOS, AEAN (Autonomous Entrepreneurial Agent Network), and APODEX as independent, partially overlapping platforms. This logical fragmentation caused duplicate state representations, redundant planners, conflicting memory stores, and circular execution loops.

Cognitive OS unifies all five domains into a single **4-Layered Decoupled Cognitive Architecture**. Each layer possesses explicit, single-purpose responsibilities, rigorous mathematical guarantees, type-safe interface contracts, and non-overlapping execution domains:

```
+---------------------------------------------------------------------------------------------------+
| LAYER 1: RESEARCH OS — Scientific Discovery & Evidence Substrate                                 |
| - Paper/Empirical Corpus Processing, Automated Literature Ingestion, Hypothesis Generation         |
| - Controlled Experimentation, Statistical Power Analysis, Holm-Bonferroni Correction              |
+---------------------------------------------------------------------------------------------------+
                                                  | Evidence & Principles
                                                  v
+---------------------------------------------------------------------------------------------------+
| LAYER 2: AEAN — Cognitive Intelligence, Swarm Reasoning & Multi-Agent Coordination                |
| - Active Inference (Expected Free Energy minimization: Pragmatic + Epistemic value)               |
| - Swarm Debate & Sycophancy Mitigation, Pearl's Causal Do-Calculus Reasoning                      |
+---------------------------------------------------------------------------------------------------+
                                                  | Cognitive Intent & Directives
                                                  v
+---------------------------------------------------------------------------------------------------+
| LAYER 3: EIOS / EOS — Entrepreneurial Orchestration, Executive Control & Lifecycle Engine         |
| - Multi-Timescale Loops (Daily Operations to Multi-Year Pivot Cycles)                             |
| - Signal-to-Hypothesis Filters, 13 Coupled Business Loops, fractional Kelly Capital Allocation    |
+---------------------------------------------------------------------------------------------------+
                                                  | Structured Action Workflows
                                                  v
+---------------------------------------------------------------------------------------------------+
| LAYER 4: APODEX — Decision Engine, Skill Execution, World Model & Memory                          |
| - Skill Execution Engine & 60-Skill Registry, Experience Memory Graph (EMG)                       |
| - CMOS (Cognitive Memory Operating System), World Model Causal Graph (WMC), Hardware/Tool I/O     |
+---------------------------------------------------------------------------------------------------+
```

---

## 1. De-Duplication & Subsystem Capability Mapping

To achieve absolute modular purity, all duplicate responsibilities across legacy codebases have been audited, unified, and mapped to single canonical owners:

| Cognitive Capability | Legacy Locations | Canonical Layer Owner | Interface Method / Component |
| :--- | :--- | :--- | :--- |
| **Literature Search & Hypothesis Generation** | ResearchOS, AEAN, APODEX | **Layer 1: Research OS** | `ResearchOS.conduct_literature_review()`, `HypothesisEngine` |
| **Statistical Experimentation & Power Analysis** | ResearchOS, AEAN | **Layer 1: Research OS** | `ResearchOS.execute_controlled_trial()`, `Welch's t-test` |
| **Active Inference & EFE Planning** | AEAN, EIOS, APODEX | **Layer 2: AEAN** | `HiveMind.evaluate_efe()`, `ActiveInferencePlanner` |
| **Multi-Agent Consensus & Swarm Debate** | AEAN, EOS, ARCS | **Layer 2: AEAN** | `HiveMind.run_swarm_debate()` |
| **Causal Do-Calculus Interventions** | AEAN, EIOS, World Model | **Layer 2: AEAN** | `HiveMind.eval_causal_intervention()` |
| **Lifecycle State Machine & Business Loops** | EIOS, EOS, ARCS | **Layer 3: EIOS / EOS** | `EIOSKernel.process_lifecycle_step()`, `EOS Engine` |
| **Capital Allocation & Portfolio Sizing** | EOS, EIOS, ARCS | **Layer 3: EIOS / EOS** | `EIOSKernel.allocate_capital_fractional_kelly()` |
| **Tool Execution & Skill Flywheel** | APODEX, AEAN, Harness | **Layer 4: APODEX** | `SkillRunner.execute_skill()`, `SkillRegistry` |
| **Episodic, Semantic & Trajectory Memory** | APODEX, CMOS, Harness | **Layer 4: APODEX** | `CMOSMemoryManager`, `EMGEngine` |
| **World Model Graph & Causal Beliefs** | APODEX, World Model | **Layer 4: APODEX** | `WorldModel.update_beliefs()` |

---

## 2. Layer Specifications & Mathematical Formulations

### Layer 1: Research OS (Scientific Discovery & Evidence Substrate)
*   **Responsibility:** Maintains the institutional knowledge graph (200+ unique research papers), ingests empirical findings, formulates falsifiable hypotheses, designs statistically powered trials, and applies Holm-Bonferroni multi-hypothesis corrections.
*   **Mathematical Principle:**
    Hypothesis promotion decision under statistical controls:
    $$\text{Promote}(H_i) = \mathbb{I}\left( p_i \le \frac{\alpha}{N - k + 1} \right) \land \mathbb{I}\left( \text{Power}(1-\beta) \ge 0.80 \right)$$
    where $\alpha = 0.05$, $N$ is total hypotheses tested, and $k$ is the rank order of $p_i$.

### Layer 2: AEAN (Cognitive Intelligence & Swarm Coordination)
*   **Responsibility:** Solves long-horizon planning under radical uncertainty using Expected Free Energy (EFE) minimization, Pearl's causal do-calculus, and multi-agent swarm consensus.
*   **Mathematical Principle:**
    Expected Free Energy $G(\pi)$ for policy selection:
    $$G(\pi) = -\underbrace{\mathbb{E}_{q(o,\theta|\pi)}[\ln p(o)]}_{\text{Pragmatic Value (Goal Utility)}} - \underbrace{\mathbb{E}_{q(\theta|\pi)}[D_{KL}(q(o|\theta,\pi) \parallel p(o))]}_{\text{Epistemic Value (Information Gain)}}$$
    Causal interventional query:
    $$P(Y \mid \text{do}(X = x)) = \sum_z P(Y \mid X = x, Z = z) P(Z = z)$$

### Layer 3: EIOS / EOS (Entrepreneurial Orchestration & Lifecycle Engine)
*   **Responsibility:** Manages 13 coupled business loops, multi-timescale executive control (daily tactical, weekly operational, quarterly strategic, multi-year pivot), signal-to-hypothesis conversion, and capital allocation.
*   **Mathematical Principle:**
    Fractional Kelly Criterion with Knightian uncertainty discount:
    $$f^* = \gamma \cdot \left( \frac{p \cdot R - (1 - p)}{R} \right) \cdot \left( 1 - \frac{\sigma_{posterior}^2}{\sigma_{max}^2} \right)$$
    where $p$ is posterior success probability, $R$ is reward-to-risk ratio, and $\gamma \in (0, 1]$ is the conservatism fraction.

### Layer 4: APODEX (Decision Engine, Skill Execution, World Model & Memory)
*   **Responsibility:** Low-level execution substrate housing the 60-skill registry, Cognitive Memory Operating System (CMOS), Experience Memory Graph (EMG), and World Model Causal Graph (WMC).
*   **Mathematical Principle:**
    Ebbinghaus Memory Decay with reinforcement re-consolidation:
    $$R(t) = \exp\left( -\frac{t}{S \cdot (1 + \ln(1 + \eta \cdot n)) } \right)$$
    where $S$ is memory stability, $\eta$ is reinforcement strength, and $n$ is recall frequency.

---

## 3. Strict Inter-Layer API Contracts

Communication between layers occurs exclusively via formal, type-safe Pydantic contracts. Direct cross-layer bypassing or circular calls are strictly prohibited.

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# Layer 1 -> Layer 2 Contract
class EvidencePayload(BaseModel):
    paper_id: int
    title: str
    transferable_principle: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    statistical_power: float

# Layer 2 -> Layer 3 Contract
class CognitiveDirective(BaseModel):
    directive_id: str
    expected_free_energy: float
    pragmatic_value: float
    epistemic_value: float
    causal_bottleneck_nodes: List[str]
    recommended_policy: Dict[str, Any]

# Layer 3 -> Layer 4 Contract
class WorkflowExecutionRequest(BaseModel):
    workflow_id: str
    target_skill: str
    parameters: Dict[str, Any]
    allocated_budget_usd: float
    max_latency_seconds: float

# Layer 4 -> Layer 3 Contract
class ExecutionResult(BaseModel):
    execution_id: str
    status: str  # SUCCESS, FAILED, HALTED
    actual_cost_usd: float
    execution_time_seconds: float
    metrics: Dict[str, Any]
    memory_updates: List[Dict[str, Any]]
```

---

## 4. Complexity & Resource Accounting Limits

To maintain institutional-grade scalability and sub-second loop response, the system enforces hard computational bounds:

1. **Layer Latency Budget:**
   - Layer 1 (Research OS): Asynchronous background batch / < 2.0s per hypothesis query.
   - Layer 2 (AEAN Swarm): < 500ms per EFE active inference decision turn.
   - Layer 3 (EIOS Kernel): < 100ms per business loop transition.
   - Layer 4 (APODEX Execution): < 50ms per skill step.
2. **Memory Footprint:** RSS delta shall not exceed 50 MB per 1,000 continuous execution cycles.
3. **Graph Traversal Limits:** Max graph traversal depth $d \le 6$, maximum sub-graph search nodes $N \le 10,000$.
