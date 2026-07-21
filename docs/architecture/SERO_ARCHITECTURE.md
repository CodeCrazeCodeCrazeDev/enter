# SERO — Sovereign Entrepreneurial Research Organization
## Authoritative Architecture Specification & Contract (v2.0.0)

This document specifies the canonical, binding architecture contract for **SERO (Sovereign Entrepreneurial Research Organization) v2**, elevating the system from a sequential feature workflow to a **Research-as-Primary-Abstraction Architecture**.

---

## 1. Executive Summary & Ubiquitous Language

SERO v2 transforms the meta-system into a scientifically-grounded organizational organism. Venture execution processes do not operate in a vacuum; they consume and feed a central, active **Knowledge Operating System (KOS)** substrate. Epistemic status, Bayesian belief updating, theory promotion, information-theoretic opportunity ranking, and organizational evolution are first-class primitives.

```
                    ┌─────────────────────────────────┐
                    │  IES — Institutional Evolution   │  (governs all below)
                    └────────────────┬────────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                             │
┌───────▼────────┐         ┌─────────▼─────────┐         ┌─────────▼────────┐
│  ROS            │◄───────►│  KOS               │◄───────►│  EIS              │
│  Research OS    │         │  Knowledge OS       │         │  Entrepreneurial  │
│                 │         │  (shared substrate)  │         │  Intelligence     │
└───────┬─────────┘         └─────────┬───────────┘         └─────────┬────────┘
        │                             │                                │
        └────────────────┬────────────┴───────────────┬────────────────┘
                          │                             │
                 ┌────────▼────────┐          ┌─────────▼────────┐
                 │  VES             │◄────────►│  POS              │
                 │  Venture         │          │  Portfolio OS      │
                 │  Execution       │          │  (capital + risk)  │
                 └──────────────────┘          └───────────────────┘
```

### 1.1 Ubiquitous Language Definition

*   **Hypothesis Node**: A core epistemic graph element containing a statement, domain, prior/posterior confidence, and linked supporting or contradicting evidence.
*   **Evidence Node**: A factual measurement (experiment, literature, pilot, observation) carrying an explicit statistical strength and a source-reliability prior.
*   **Theory Node**: A promoted general explanatory model built from validated hypotheses that makes novel, testable predictions.
*   **Contradiction Node**: A node representing identified logical or statistical inconsistency between hypotheses, auto-raised for chairman deliberation.
*   **Bayesian Belief Engine**: The active analytical core updating posterior confidence intervals upon the ingestion of any new Evidence node.
*   **Venture Execution System (VES)**: The operational arm executing the venture phases, consuming knowledge from KOS rather than generating beliefs from scratch.
*   **Portfolio Operating System (POS)**: The capital allocator managing both the Venture Portfolio (ROI-driven) and the Research Portfolio (Expected Discovery Value-driven).
*   **Institutional Evolution System (IES)**: The master organization manager executing agent lifecycles (spawning, splitting, retiring agents) and preserving doctrine.

---

## 2. Bounded Contexts & Ownership

SERO v2 organizes the meta-system into six major bounded contexts, with explicit boundaries and relational contracts.

### 2.1 Bounded Context Contracts

1.  **Knowledge Operating System (`sero.kos`)**
    *   *Owner*: Knowledge Operations Division.
    *   *Mission*: Expose the active knowledge graph and Bayesian updating core.
    *   *Invariants*: Referential integrity of evidence-hypothesis associations must be perfectly preserved.
2.  **Research Operating System (`sero.ros`)**
    *   *Owner*: Scientific Research Division.
    *   *Mission*: Conduct automated signal discovery, experimental design, and statistical validation.
    *   *Invariants*: Hypotheses can only be promoted to Theory status if multiple-testing correction is passed with $p < 0.05$.
3.  **Entrepreneurial Intelligence System (`sero.eis`)**
    *   *Owner*: Strategic Decision Division.
    *   *Mission*: Determine the economic form of validated opportunity clusters (build venture, license IP, open-source, publish).
4.  **Venture Execution System (`sero.ves`)**
    *   *Owner*: Venture Operations Division.
    *   *Mission*: Execute GTM, pricing, and operational funnels, consuming and updating the shared KOS substrate.
5.  **Portfolio Operating System (`sero.pos`)**
    *   *Owner*: Portfolio & Capital Division.
    *   *Mission*: Distribute capital proportionally based on risk-adjusted ROI and Expected Discovery Value.
6.  **Institutional Evolution System (`sero.ies`)**
    *   *Owner*: Systems Governance Council.
    *   *Mission*: Drive agent lifecycle modifications (spawn, merge, split, retire) and maintain the immutable audit trail.

---

## 3. The Shared Substrate: Knowledge OS (KOS)

Unlike isolated databases, the Knowledge OS functions as the meta-system's epistemic memory.

### 3.1 Epistemic Node Schema

#### Hypothesis Node
```json
{
  "hypothesis_id": "hyp-8902",
  "statement": "Decreasing product price by 10% increases volume by 25%",
  "domain": "pricing_elasticity",
  "prior_confidence": 0.50,
  "posterior_confidence": 0.72,
  "supporting_evidence": ["ev-9811"],
  "contradicting_evidence": ["ev-9812"],
  "dependent_hypotheses": ["hyp-3012"],
  "downstream_decisions": ["dec-7711"],
  "status": "active"
}
```

#### Evidence Node
```json
{
  "evidence_id": "ev-9811",
  "source": "paid_pilot_cell_A",
  "method": "experiment",
  "strength": {
    "effect_size": 2.1,
    "sample_size": 150,
    "p_value": 0.004
  },
  "causal_or_correlational": "causal",
  "linked_hypotheses": ["hyp-8902"],
  "timestamp": "2026-07-20T12:00:00Z",
  "decay_rate": 0.02
}
```

### 3.2 Bayesian Belief Engine

Upon ingestion of a new `Evidence` node, the posterior of the linked `Hypothesis` is updated:
*   A conjugate Beta-prior updating model is utilized for success ratios ($Beta(\alpha, \beta)$).
*   A Gaussian model is utilized for continuous parameter distributions (e.g., CAC, customer lifetime value).
*   *Calibration Audit*: The system monitors if the observed event rate matches its predicted confidence intervals (e.g., of events predicted with 70% confidence, do ~70% actually happen?).

---

## 4. Research Operating System (ROS)

The ROS acts as the scientific engine, discovering demand signals and executing experiments.

### 4.1 Blended Discovery Mathematics

Opportunity ranking uses a multi-objective composite priority scoring function:

$$Priority(opportunity) = \alpha \cdot E[commercial] + \beta \cdot ExpectedInformationGain(opportunity, KOS) + \gamma \cdot OptionValue(opportunity)$$

Where:
*   $E[commercial]$ represents expected commercial NPV.
*   $ExpectedInformationGain$ represents the predicted Kullback-Leibler (KL) divergence between prior and posterior beliefs over the hypothesis cluster.
*   $OptionValue$ is the estimated value of downstream venture choices unlocked by the discovery.
*   At Tier 1 (zero-cost), $\alpha$ dominates. At Tier 3 (revenue-funded), $\beta$ and $\gamma$ weights increase, enabling pure exploratory research.

---

## 5. Entrepreneurial Intelligence System (EIS)

EIS handles the transition from knowledge to action.

### 5.1 Meta-Economic Form Selection

When a hypothesis cluster achieves Theory status, EIS deliberates over its structural commercialization form:

*   **Build Venture**: Initiate the VES pipeline.
*   **License IP**: Export findings to external industry operators.
*   **Open-Source**: Release public libraries if defensive moats are low but ecosystem strategic value is high.
*   **Publish**: Output pure scientific writeups if implementation cost exceeds commercial EV.

---

## 6. Portfolio Operating System (POS)

Capital is managed across two distinct portfolios:
1.  **Venture Portfolio**: Capital is allocated to active Venture Cells based on risk-adjusted expected ROI.
2.  **Research Portfolio**: Capital is allocated to ROS exploratory signals based on **Expected Discovery Value** (modeled as the uncertainty-reduction capability that de-risks future high-tier venture cells).

---

## 7. Institutional Evolution System (IES)

IES governs the process of system self-evolution.

### 7.1 Agent Lifecycle Management

To adapt to changing market and research environments, IES can dynamically:
*   **Spawn**: Create specialized agents (e.g., pricing specialists) when a capability gap is detected.
*   **Merge**: Combine two sub-agents whose responsibilities overlap.
*   **Split**: Divide generalist agents into isolated specialists.
*   **Retire**: Deactivate underperforming or obsolete agents.

---

## 8. Measurable Phase Exit Criteria

A phase of the SERO v2 implementation is not complete when its code is written; it is complete only when all objective criteria listed below are verified and satisfied.

| Phase | Core Deliverables | Verification Methodology | Mandatory Measurable Exit Criteria |
|---|---|---|---|
| **Phase 0** | Bounded context maps, system specification, and legacy documentation update. | Architectural audit. | 100% of bounded contexts documented; all ADRs accepted; legacy specifications mapped via traceability table. |
| **Phase 1** | DI container, event bus, config, state machine, deterministic IDs, and persistence layers. | Conformance tests. | Zero direct cross-package imports; 100% of DI registrations resolved; event bus publishes and consumes concurrently with zero message loss. |
| **Phase 2** | Active knowledge graph, Bayesian belief updating, contradiction detection, and theory loops. | Mathematical validation. | Correctly propagates confidence downstream and resolves contradictions via conjugate Beta/Gaussian updates. |
| **Phase 3** | Discovery Engine, opportunity ranking, and Autonomous Science writeups. | Simulation tests. | BLended mathematical opportunity scoring allocates priority correctly to high-information-value signal opportunities. |
| **Phase 4** | Meta-economic form decision framework. | Deliberation replay. | EIS selects build/license/open-source form correctly based on capital constraints. |
| **Phase 5** | Multi-Timescale Planning and Research Portfolio Management. | Portfolio allocation simulation. | POS distributes budget between venture and research portfolios correctly based on Expected Discovery Value. |
| **Phase 6** | Discovery-to-rollback pipelines, detailed Capability Registry and Lineage Database. | Sandbox test run. | Extracted capabilities successfully compiled and metadata records mapped; sandbox verifies capability isolation. |
| **Phase 7** | GRC gates, Meta-Governance, and IES Agent Lifecycle. | Chaos injection. | Spawning and splitting of agents executes successfully within complexity budgets under strict invariants. |
| **Phase 8** | Replay, chaos, fault, security, and economic benchmarks. | Test suite execution. | 100% pass on regression and replay tests; system recovers gracefully from injected database/network failures within $<500\text{ ms}$. |
| **Phase 9** | Progressive rollout, capability/flag rollbacks, and kill switches. | Rollback simulation. | Simulated SLA degradation triggers complete automatic rollback to previous stable version within $<100\text{ ms}$. |

---

## 9. Legacy Document Traceability & Status Matrix

To avoid documentation drift and maintain a clear, single source of truth, we establish the following traceability table:

| Document | Path | Status | Relationship & Traceability Guidance |
|---|---|---|---|
| **SERO_ARCHITECTURE** | `docs/architecture/SERO_ARCHITECTURE.md` | **Active / Authoritative** | The master, controlling architecture contract for SERO v2. Supersedes `AI_EOS_ARCHITECTURE.md`. |
| **AI_EOS_ARCHITECTURE** | `docs/architecture/AI_EOS_ARCHITECTURE.md` | **Superseded** | Fully superseded by the Research-as-Primary-Abstraction architecture of SERO v2. |
| **APODEX_SYSTEM_DESIGN** | `APODEX_SYSTEM_DESIGN.md` | **Partially Superseded** | Superseded on the master self-evolution flow by SERO Active Inference and Meta-Governance design. The basic Personal Evolution Profile (PEP) and Verifier node definitions remain valid as subcomponents of the memory and validation contexts. |
| **ARCS_ARCHITECTURE** | `ARCS_ARCHITECTURE.md` | **Subsystem** | Serves as the authoritative domain model for execution/revenue services within the ARCS execution context. Coordinates directly with `sero.ves`. |
| **AEAN_DESIGN** | `apodex/aean/README.md` | **Subsystem** | Serves as the authoritative specification of the 6-stage flywheel micro-cell execution loop. Coordinates directly with `sero.ves`. |
| **IMPLEMENTATION_ROADMAP**| `IMPLEMENTATION_ROADMAP.md` | **Historical Roadmap** | Superseded by the dependency-driven implementation phases of SERO v2. |
| **APODEX2_MEMORY_SYSTEM_DESIGN** | `docs/design/APODEX2_MEMORY_SYSTEM_DESIGN.md` | **Subsystem** | Serves as the technical specification of the underlying 5-tier memory models (T0-T4) and hybrid scoring formula. Maps directly to the `sero.kos` context. |

---

This contract is signed and approved. Any proposed deviation must be submitted through a formal ADR and approved before implementation.
