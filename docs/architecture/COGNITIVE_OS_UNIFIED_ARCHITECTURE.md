# Unified Cognitive Operating System (Cognitive OS) Architecture Specification
## Canonical Blueprint for Unified Intelligence Layering (v1.2.0)

This document establishes the authoritative, layered architecture blueprint for the unified **Cognitive Operating System (Cognitive OS)**. It formally transitions the historical, siloed platforms (**Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX**) into a single, cohesive, non-duplicative substrate. Rather than operating as disjointed engines, these historical systems now exist strictly as **logical views** or **functional viewpoints** over a unified, 5-plane Cognitive Architecture.

---

## 1. System Interaction Topology (The 5-Plane Stack)

The Cognitive Operating System is organized into five decoupled, single-responsibility functional planes. Execution and data flow dynamically between these planes under the supervision of a central **Cognitive Kernel**.

```
                           Control Plane
           ┌──────────────────────────────────────────────┐
           │     Goals • Governance • Scheduler • Eval    │
           └──────────────────────┬───────────────────────┘
                                  │
                                  ▼
                           Cognitive Kernel
 ┌─────────────────────────────────────────────────────────────────────────┐
 │ Intentions │ Beliefs │ Planner │ World Model │ Memory │ Reasoner        │
 │ Simulator  │ Evaluator │ Learning Policy │ Uncertainty │ Resource       │
 └────────────────────────────────┬────────────────────────────────────────┘
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
    Knowledge Plane        Execution Plane          Learning Plane
 (Research OS / Literature)   (EOS / APODEX)     (Self-Evolution Engine)
 (Knowledge Graph)            (Worker Agents)     (Architecture Search)
 (Embeddings / DB)            (Sandbox / Tools)   (Capability Benchmarks)
```

---

## 2. First-Principles Subsystem Audits & Deconstruction

To maximize intelligence and simplicity, we critically analyze whether the five historical systems should remain independent or be completely unified:

1. **Research OS**: Historically maintained as an independent statistical research layer.
   - *First-Principles Verdict:* Research OS must **not** remain independent. It is merged into the **Knowledge Plane** (for literary corpus management, hypothesis graphs, and epistemic verification) and the **Execution Plane** (for sandboxed code execution and statistical trial runs).
2. **EOS (Entrepreneurial Operating System)**: Historically a procedural loop mimicking human meeting rhythms and company scorecards.
   - *First-Principles Verdict:* EOS must **not** exist separately from the execution engine. Manual scorecards are replaced by automated real-time performance telemetry. EOS is consolidated into the **Control Plane** (for goal specification and evaluation) and the **Execution Plane** (for dynamic capability deployment).
3. **AEAN (Autonomous Entrepreneurial Agent Network)**: Historically an agent swarm communicating via message passing.
   - *First-Principles Verdict:* AEAN is elevated from a mere subsystem to become the **Cognitive Kernel** itself. It provides the unified, continuous feedback loop of the entire Cognitive OS.
4. **APODEX**: Historically a quantitative business and trading assistant.
   - *First-Principles Verdict:* APODEX's core quantitative decision algorithms (e.g., Kelly Criterion allocation, shadow price tracking, game-theoretic Nash updates) are consolidated into the **Cognitive Plane** as core reasoning engines, and its tool wrappers are integrated into the **Execution Plane**.
5. **EIOS (Executive Intelligence Operating System)**: Historically a separate strategic decision and active inference framework.
   - *First-Principles Verdict:* EIOS disappears entirely as an independent product. Its active inference loops, Expected Free Energy minimization algorithms, and do-calculus interventions are absorbed directly into the **Cognitive Plane**.

---

## 3. The Central Cognitive Kernel & Optimization Objective

The **Cognitive Kernel** is the unified, continuously operating adaptive feedback loop of the platform. It is the **sole owner** and coordinator of the unified cognitive state:

*   **Goals & Intentions:** Maintains overall execution objectives and prioritizes intermediate sub-goals.
*   **Beliefs & Uncertainty:** Manages confidence-weighted facts and hypotheses, updating priors based on new observations.
*   **World Model:** Models the environment's state transition probabilities under potential actions.
*   **Planner & Reasoner:** Decomposes complex tasks (using HTN/MCTS) and resolves contradictions across collective paradigms.
*   **Memory & Simulation:** Manages Working, Episodic, Semantic, and Procedural memory while simulating pre-mortems.
*   **Evaluator & Learning Policy:** Conducts step-level credit assignment and extracts strategic insights.
*   **Resource Allocation & Meta-cognition:** Dynamically manages budget limits and detects token-wasting loops.

### The Mathematical Optimization Objective Function
The Cognitive OS operates to maximize the expected long-term cumulative utility of the system over a planning horizon $T$:

$$J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^{T} \gamma^t \mathcal{U}(s_t, a_t) \right]$$

Where the instantaneous utility $\mathcal{U}(s_t, a_t)$ is formulated as:

$$\mathcal{U}(s_t, a_t) = w_1 \text{PlanSuccess}(s_t) + w_2 \text{ResearchQuality}(s_t) + w_3 \text{ReasoningAccuracy}(s_t) + w_4 \text{PredictionAccuracy}(s_t) + w_5 \text{ExecutionCompletion}(s_t) + w_6 \text{KnowledgeGrowth}(s_t) + w_7 \text{MemoryAccuracy}(s_t) - w_8 \text{Latency}(s_t) - w_9 \text{ComputeCost}(s_t) - w_{10} \text{ArchitectureComplexity}(s_t)$$

- **$\text{PlanSuccess}(s_t)$:** Ratio of successfully verified planning steps.
- **$\text{ResearchQuality}(s_t)$:** Epistemic coverage and statistical precision (DSR and adjusted p-values) of the hypothesis graph.
- **$\text{ReasoningAccuracy}(s_t)$:** Frequency of correct choices in adversarial and multi-agent deliberation.
- **$\text{PredictionAccuracy}(s_t)$:** Shannon entropy reduction velocity of world model transition estimates.
- **$\text{ExecutionCompletion}(s_t)$:** Ratio of successfully completed actions deployed to sandboxes or external systems.
- **$\text{KnowledgeGrowth}(s_t)$:** Successful ingestion and verification rate of new facts and research documents.
- **$\text{MemoryAccuracy}(s_t)$:** Hit-rate of semantic memory retrieval for past relevant experiences.
- **$\text{Latency}(s_t)$ / $\text{ComputeCost}(s_t)$:** Multi-objective penalty metrics for runtime duration and token expenditure.
- **$\text{ArchitectureComplexity}(s_t)$:** Metric scoring structural duplication, code coupling, and interface violations.

---

## 4. Singular Capability Ownership Matrix

To prevent duplication, we enforce a strict single-ownership rule across the planes:

| Functional Plane | Unified Component | Authoritative Implementation | Obsoleted Legacy Overlaps |
| :--- | :--- | :--- | :--- |
| **Control Plane** | Strategic Planner | `apodex.planning.planner_executor` | `agent_harness.core.runtime.orchestration.planner_executor` |
| **Control Plane** | Governance Core | `apodex.ai_eos.governance.gateway` | Bespoke inline safety logic |
| **Cognitive Plane** | Causal World Model | `apodex.world_model.world_model` | Custom causal models in AEAN/EIOS |
| **Cognitive Plane** | Persistent Memory | `apodex.memory.semantic_memory` / `cmos` | Custom SQLite schemas inside individual tasks |
| **Knowledge Plane** | Knowledge Graph | `apodex.aean.ekg` | Raw unstructured JSON mappings |
| **Execution Plane** | Multi-Agent Orchestrator | `apodex.orchestration.hierarchical` | Legacy ReAct loops in `AgentHarness` |
| **Infrastructure Plane**| Persistent Observability | `apodex.world_model.telemetry` | Scattered debug print statements |

---

## 5. Closed-loop Evolution Flow (The Continuous Loop)

The system leverages the 230-paper scientific corpus as an active driver of autonomous evolution. Every accepted paper is parsed for transferable engineering principles, translated into architectural hypotheses, simulated inside the digital twin, benchmarked, and deployed in shadow mode before final promotion.

```
  Research Corpus
         │
         ▼
  Knowledge Extraction (Engineering Principles)
         │
         ▼
  Architecture Proposal Generator (Hypothesis Engine)
         │
         ▼
  Simulation Sandbox (Pre-mortem Trials)
         │
         ▼
  Cognitive Benchmarks (PCI, BERV, CER, ASS)
         │
         ▼
  Shadow Deployment (Canary Verification)
         │
         ▼
  Promotion / Automatic Rollback on Regressions
```
