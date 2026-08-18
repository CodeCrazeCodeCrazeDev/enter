# Unified Cognitive Operating System Architecture Specification
**Version:** 2026.1.0
**Status:** Authoritative Architectural Standard
**Subsystems:** Research OS | AEAN | EIOS / EOS | APODEX

---

## 1. Executive Overview & First Principles

The **Unified Cognitive Operating System** unifies five previously distinct or overlapping subsystems—**Research OS, AEAN, EIOS, EOS, and APODEX**—into a single, four-layer hierarchical architecture. Rather than operating as disparate platforms with duplicate planners, memory silos, or conflicting execution engines, the system enforces a strict top-down cognitive flow.

### Core Architecture Axioms
1. **Unambiguous Single Responsibility:** Each capability (planning, world modeling, memory, execution, statistical research) resides in exactly one layer.
2. **Strict Downward Control Hierarchy:** Control flows downward from higher abstractions to lower runtime execution; observations and evidence flow upward.
3. **Decoupled Research and Runtime:** Hypotheses are generated, tested, and validated statistically in Layer 1 (Research OS) before candidate algorithms or prompt structures are promoted to production runtime in Layer 2 (AEAN) or Layer 3 (EIOS/EOS).
4. **Active Inference & Dynamic Governance:** Decisions are governed by Expected Free Energy (EFE) minimization, balancing pragmatic goal fulfillment with epistemic information gain.

---

## 2. Four-Layer Architecture Taxonomy

```
+-----------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS (Research Layer)                       |
|  Hypothesis Gen | Paper Ingestion | Statistical Power | Holm-Bonferroni | Provenance |
+-----------------------------------------------------------------------------------+
                                         | Hypothesis Promotion / Benchmarking
                                         v
+-----------------------------------------------------------------------------------+
|                   LAYER 2: AEAN (Cognitive Intelligence Layer)                     |
|  Active Inference EFE | Do-Calculus SCM | Graph-of-Thought | Swarm Debate / Consensus|
+-----------------------------------------------------------------------------------+
                                         | Strategic Intent & Operational Goals
                                         v
+-----------------------------------------------------------------------------------+
|              LAYER 3: EIOS / EOS (Strategic Execution & Orchestration Layer)      |
|  Multi-Timescale Loops | Opportunity Economics | Capital Allocation | Risk Gating |
+-----------------------------------------------------------------------------------+
                                         | Primitive Commands & Tool Invocations
                                         v
+-----------------------------------------------------------------------------------+
|                LAYER 4: APODEX (Decision & Skill Execution Substrate)             |
|  SkillRegistry | Protocol Runners | Causal World Model (WMC) | CMOS Memory | Safety|
+-----------------------------------------------------------------------------------+
```

---

## 3. Subsystem Detailed Specification

### Layer 1: Research OS (Research & Discovery Layer)
* **Canonical Path:** `apodex/research_os/`, `apodex/ai_eos/research/`
* **Responsibilities:**
  - Ingesting academic publications and structural knowledge bases (`AI_EOS_RESEARCH_DB.yaml`, `ALPHA_ALGO_100_NEW_RESEARCH.yaml`).
  - Formulating falsifiable hypotheses and calculating statistical power ($1 - \beta$).
  - Executing deterministic benchmark trials and applying Holm-Bonferroni corrections for multi-hypothesis testing.
  - Maintaining immutable lineage provenance: Paper $\rightarrow$ Principle $\rightarrow$ Architectural Hypothesis $\rightarrow$ Trial $\rightarrow$ Decision.

### Layer 2: AEAN (Autonomous Entrepreneurial Agent Network - Intelligence Layer)
* **Canonical Path:** `apodex/aean/`, `apodex/reasoning/`, `apodex/planning/`
* **Responsibilities:**
  - Active Inference Expected Free Energy (EFE) calculation:
    $$G(\pi) = -\sum_o q(o|\pi) \ln \frac{q(o|\pi)}{p(o)} + \sum_x q(x|\pi) \text{KL}\left(q(o|x) \,||\, p(o|x)\right)$$
  - Causal counterfactual reasoning using Pearl's Structural Causal Models (SCM) and $do(X=x)$ interventions.
  - Graph-of-Thought (GoT) multi-branch trajectory evaluation.
  - Multi-agent swarm debate with sycophancy mitigation via blind independent reflection.

### Layer 3: EIOS / EOS (Enterprise Operating System - Strategic Orchestration Layer)
* **Canonical Path:** `apodex/arcs/`, `apodex/ai_eos/intelligence/`
* **Responsibilities:**
  - Multi-timescale execution loops (Daily, Weekly, Quarterly, Annual horizon alignment).
  - Opportunity economics validation ($LTV / CAC > 3.0$, payback period $< 12$ months).
  - Lagrange shadow price capital allocation under finite compute/financial resource constraints:
    $$\max_{\mathbf{x}} \sum_i U_i(x_i) \quad \text{s.t.} \quad \sum_i c_i x_i \le B$$
  - Real-time risk gating and enterprise state-machine monitoring.

### Layer 4: APODEX (Decision & Skill Execution Substrate)
* **Canonical Path:** `apodex/skills/`, `apodex/world_model/`, `apodex/memory/`
* **Responsibilities:**
  - Centralized skill discovery and invocation via `SkillRegistry`.
  - Deterministic protocol execution and budget downshifting/halting.
  - World Model Engine (WMC) causal state updates and decay-weighted Bayesian belief propagation.
  - Cognitive Memory System (CMOS) tiering (Episodic, Semantic, Procedural, Working).
  - Safety, authorization, and audit logging.

---

## 4. Capability Ownership Matrix

| Capability / Function | Layer | Primary Module | Secondary / Supporting Module |
| :--- | :--- | :--- | :--- |
| Paper Ingestion & Ranking | Layer 1 | `apodex.research_os.research_ingestion` | `apodex.ai_eos.research.research_os` |
| Statistical Power & Holm-Bonferroni | Layer 1 | `apodex.research_os.statistical_validation` | `apodex.ai_eos.research.experiment_framework` |
| Active Inference (EFE Engine) | Layer 2 | `apodex.aean.coordination.hive_mind` | `apodex.reasoning.active_learning` |
| Causal Intervention ($do$-calculus) | Layer 2 | `apodex.arcs.kernel.kernel` | `apodex.world_model.world_model` |
| Graph-of-Thought Planning | Layer 2 | `apodex.reasoning.got` | `apodex.planning.planner` |
| Business Loop Orchestration | Layer 3 | `apodex.arcs.kernel.kernel` | `apodex.ai_eos.intelligence.eos_first_principles` |
| Capital & Resource Allocation | Layer 3 | `apodex.ai_eos.intelligence.computational_architecture` | `apodex.economics` |
| Skill Registration & Dispatch | Layer 4 | `apodex.skills.registry` | `apodex.skills.runner` |
| Causal World Model (WMC) | Layer 4 | `apodex.world_model.world_model` | `apodex.world_model.domain` |
| Memory Storage & Tiering (CMOS) | Layer 4 | `apodex.memory.cmos` | `apodex.memory.semantic_memory` |

---

## 5. Unified System Verification & Operational Limits

- **Memory Limit:** Peak RSS memory delta $\le 1.0 \text{ MB}$ per 10,000 cognitive execution cycles.
- **Latency Budget:** Loop execution latency $\le 0.005 \text{ seconds}$ per active inference evaluation.
- **Statistical Significance Threshold:** $\alpha = 0.05$ with Welch's t-test and Holm-Bonferroni family-wise error rate control.
- **Zero Cycle Constraint:** Zero circular dependencies between `apodex.research_os`, `apodex.aean`, `apodex.arcs`, and `apodex.skills`.
