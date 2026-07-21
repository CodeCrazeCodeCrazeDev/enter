# SERO — Sovereign Entrepreneurial Research Organization
## Authoritative Architecture Specification & Contract (v2.1.0)
### KOS/ROS Formal Specification — v1.0

This document specifies the canonical, binding architecture contract and formal spec for **SERO (Sovereign Entrepreneurial Research Organization) v2.1**, elevating the system from a sequential feature workflow to a **Research-as-Primary-Abstraction Architecture** fully aligned to a **7-Stage Cognitive Lifecycle**, **Research Economics**, a **Multi-Paradigm Collective Intelligence Layer**, and a **Formal KOS/ROS Specification**.

---

## 1. Executive Summary & Ubiquitous Language

SERO v2.1 represents the ultimate convergence of cognitive science, research economics, and software engineering. Subsystems and agents do not merely execute tasks; they participate in a single, unified cognitive lifecycle that governs how knowledge is discovered, validated, commercialized, and compiled into the organization's collective intelligence substrate.

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

*   **Venture Cell**: The smallest isolated unit of business operation. Each Venture Cell maintains its own independent P&L, namespace, sub-agent composition, and local episodic memory.
*   **Belief State**: The probability distribution over market, customer, competitor, and regulatory states modeled by the system.
*   **Active Inference Loop**: The core decision process that jointly minimizes model uncertainty (epistemic value/information gain) and expected free energy (maximizing economic utility).
*   **Expected Free Energy ($G$)**: The objective function for a policy, combining expected economic utility, risk penalty, compute cost, and governance barriers.
*   **Research OS**: The scientific execution platform where venture hypotheses are registered, planned, sandboxed, and statistically validated before any capital is committed.
*   **Research Ledger**: An immutable, append-only chronological record of all registered hypotheses, executed experiments, and validated facts.
*   **Capability**: A modular, version-controlled, and audited behavior (prompt strategy, routing policy, tool invocation, or fine-tuned model) registered with the system.
*   **Capability Registry & Lineage**: The definitive, versioned database storing the origin, evidence, benchmarks, dependencies, risk scores, and approval/rollback records of all system Capabilities.
*   **Decision Provenance**: An immutable, cryptographically verifiable record detailing the evidence, assumptions, model versions, experiments, and approval chains behind a strategic decision.
*   **Meta-Governance**: The governing subsystem responsible for reviewing proposed architectural changes, measuring technical debt, and enforcing complexity budgets over the governance system itself.
*   **Institutional Knowledge Graph (IKG)**: A unified relational representation mapping research papers, experiments, datasets, features, models, capabilities, agents, venture cells, and decisions to provide complete multi-layered traceability.

---

## 2. Bounded Contexts & Ownership

SERO v2.1 decomposes its operations into exactly nine canonical Bounded Contexts, each with an explicit ownership boundary, inputs, outputs, and invariants.

1.  **System Composition & Composition Context (`sero.composition`)**
    *   *Owner*: Systems Engineering Core.
    *   *Mission*: Provide thread-safe Dependency Injection (DI), plugin loading, lifecycle coordination, and service resolution.
2.  **Knowledge Operating System Context (`sero.kos`)**
    *   *Owner*: Knowledge Operations Division.
    *   *Mission*: Expose the active knowledge graph, Bayesian updating, contradiction detection, and the Epistemic Risk query layers.
    *   *Invariants*: Referential integrity of evidence-hypothesis associations must be perfectly preserved.
3.  **Research Operating System Context (`sero.ros`)**
    *   *Owner*: Scientific Research Division.
    *   *Mission*: Conduct automated signal discovery, experimental design, Research Compiler ingestion, and statistical validation.
    *   *Invariants*: Hypotheses can only be promoted to Theory status if multiple-testing correction is passed with $p < 0.05$.
4.  **Entrepreneurial Intelligence System Context (`sero.eis`)**
    *   *Owner*: Strategic Decision Division.
    *   *Mission*: Determine the economic form of validated opportunity clusters (build venture, license IP, open-source, publish).
5.  **Venture Execution System Context (`sero.ves`)**
    *   *Owner*: Venture Operations Division.
    *   *Mission*: Execute GTM, pricing, and operational funnels, consuming and updating the shared KOS substrate.
6.  **Portfolio Operating System Context (`sero.pos`)**
    *   *Owner*: Portfolio & Capital Division.
    *   *Mission*: Distribute capital proportionally based on risk-adjusted expected ROI and Expected Discovery Value.
7.  **Institutional Evolution System Context (`sero.ies`)**
    *   *Owner*: Systems Governance Council.
    *   *Mission*: Drive agent lifecycle modifications (spawn, merge, split, retire) and maintain the immutable audit trail.
8.  **Validation Platform Context (`sero.validation`)**
    *   *Owner*: Quality Assurance & Reliability Division.
    *   *Mission*: Run continuous replay tests, chaos injection, performance profiling, and architectural conformance validation.
9.  **Progressive Deployment Context (`sero.deployment`)**
    *   *Owner*: Operations & Release Division.
    *   *Mission*: Coordinate staged rollout (Sandbox -> Shadow -> Canary -> Production) and execute automated rollback on SLA degradation or metric drift.

---

## 3. Data Schemas

### 3.1 Hypothesis

```typescript
Hypothesis {
  id: string                          // uuid
  statement: string
  domain: string                      // e.g. "pricing", "onboarding", "channel-fit"
  venture_id: string | null           // null if venture-agnostic / cross-cutting

  prior_confidence: float             // 0-1, set at creation
  posterior_confidence: float         // updated by Bayesian Belief Engine (§5)
  confidence_distribution: {          // not just a point estimate
    type: "beta" | "gaussian" | "dirichlet"
    params: object                    // e.g. {alpha, beta} for Beta
  }

  supporting_evidence: EvidenceRef[]
  contradicting_evidence: EvidenceRef[]
  dependent_hypotheses: HypothesisRef[]   // what this claim assumes
  downstream_decisions: DecisionRef[]     // what relies on this claim

  assumption_count: int               // derived: count of unproven dependent_hypotheses
  single_source_flag: bool            // derived: true if evidence_count == 1
  high_impact_low_evidence_flag: bool // derived, see §7.2

  status: "proposed" | "under_test" | "active" | "falsified" | "superseded" | "theory_promoted"
  created_at: timestamp
  last_updated: timestamp
}
```

### 3.2 Evidence

```typescript
Evidence {
  id: string
  source: string                      // URI, document ref, experiment id
  source_type: "experiment" | "observation" | "literature" | "simulation" | "interview" | "survey"

  evidence_quality_tier: "rct" | "natural_experiment" | "longitudinal" |
                          "survey" | "interview" | "opinion" | "synthetic"
                                       // ordinal, drives reliability_weight below

  reliability_weight: float           // 0-1, derived from quality_tier lookup table (§5.2),
                                       // manually overridable with logged justification

  strength: {
    effect_size: float | null
    sample_size: int | null
    interval: [float, float] | null   // CI or credible interval
    p_or_posterior: float | null
  }

  causal_or_correlational: "causal" | "correlational" | "unknown"
  linked_hypotheses: HypothesisRef[]

  replicated_by: EvidenceRef[]        // empty until independently replicated
  replication_status: "unreplicated" | "replicated" | "failed_replication"

  timestamp: timestamp
  decay_rate: float                   // relevance half-life, domain-dependent default
  current_relevance: float            // derived: decays over time, flags for review when < threshold
}
```

### 3.3 Theory

```typescript
Theory {
  id: string
  statement: string                   // general explanatory model
  constituent_hypotheses: HypothesisRef[]
  predictive_scope: Prediction[]      // untested implications, auto-queued as new Hypotheses

  confidence: float
  predictive_track_record: {          // NEW — round 4 refinement
    predictions_made: int
    predictions_confirmed: int
    predictions_falsified: int
    accuracy_rate: float              // confirmed / (confirmed + falsified)
  }

  promotion_criteria_met: {
    independent_evidence_count: int   // >= 2 required, from distinct source_types
    generalization_tested: bool       // has scope been tested outside origin context
    predictive_success_threshold_met: bool   // accuracy_rate >= 0.7 after >= 3 predictions
  }

  contradictions: ContradictionRef[]
  status: "draft" | "active" | "contradicted" | "retired"
}
```

### 3.4 Contradiction

```typescript
Contradiction {
  id: string
  node_a: HypothesisRef | TheoryRef
  node_b: HypothesisRef | TheoryRef
  detected_by: "contradiction_detection_agent" | "manual"
  detected_at: timestamp
  severity: "low" | "medium" | "high"      // derived from downstream_decisions impact
  resolution_status: "open" | "escalated" | "resolved"
  resolution_action: string | null
  routed_to: "chairman_agent" | "human_governance"  // high severity always routes to human
}
```

### 3.5 Typed Relationships

```typescript
Relationship {
  from: HypothesisRef | TheoryRef
  to: HypothesisRef | TheoryRef
  type: "supports" | "contradicts" | "causes" | "correlates" |
        "derived_from" | "generalizes" | "specializes" | "requires" |
        "duplicates" | "updates"
}
```

---

## 4. Research Compiler (KOS Ingestion Capability)

The Research Compiler converts raw materials (papers, transcripts, etc.) into structured, deduplicated, and normalized Evidence nodes, ensuring clean updates.

### 4.1 Ingestion Pipeline Flow

```
Raw input (paper | patent | interview transcript | market report | filing | reviews)
   ↓
[Extraction]        — pull claims, numbers, effect sizes (no raw copyright text)
   ↓
[Normalization]      — map extracted claims onto existing domain vocabulary synonyms
   ↓
[Deduplication]      — check against existing Evidence nodes to avoid double-counting
   ↓
[Conflict Resolution] — if a claim contradicts existing Evidence, raise a Contradiction
   ↓
[Evidence Node Creation] — assign quality_tier and calculate reliability_weight
   ↓
[Hypothesis Update]  — Bayesian Belief Engine triggered on all linked hypotheses
```

---

## 5. Bayesian Belief Engine

The Bayesian Belief Engine performs standard conjugate updates to propagate evidence.

### 5.1 Update Rule

For a Hypothesis with Beta(α, β) posterior:

```
On new Evidence e with reliability_weight w and directional strength s (support=+1/contradict=-1):
  α_new = α + (w × s_positive_component)
  β_new = β + (w × s_negative_component)
  posterior_confidence = α_new / (α_new + β_new)
```

For continuous estimates (CAC, elasticity), standard conjugate normal updates are performed.

### 5.2 Reliability Weight Lookup Table

| evidence_quality_tier | default reliability_weight |
|---|---|
| rct | 1.0 |
| natural_experiment | 0.8 |
| longitudinal | 0.7 |
| survey | 0.5 |
| interview | 0.4 |
| opinion | 0.2 |
| synthetic | 0.15 |

---

## 6. Contradiction Detection & Routing

```
on_evidence_added(e: Evidence):
  for h in e.linked_hypotheses:
    for h2 in KOS.hypotheses where h2.domain == h.domain and h2.id != h.id:
      if semantic_overlap(h, h2) > threshold and posterior_confidence(h) and posterior_confidence(h2) are inconsistent:
        create Contradiction(node_a=h, node_b=h2, severity=compute_severity(h, h2))
        if severity == "high": route_to_human_governance()
        else: route_to_chairman_agent()
```

---

## 7. Epistemic Risk (KOS Query Layer)

Four queries run on a schedule to surface false certainty and blind-spots:

### 7.1 Calibration Audit

Runs monthly, comparing recorded decision confidences against actual success outcomes:

```
audit_calibration():
  for each confidence bucket (e.g. 60-70%, 70-80%):
    realized_rate = count(DecisionRecord where confidence_at_decision in bucket and outcome.realized == true) / count(in bucket)
    flag if |realized_rate - bucket_midpoint| > 0.15
```

### 7.2 High-Impact / Low-Evidence Flag

Identifies unproven assumptions that have a high operational impact:

```
flag_high_impact_low_evidence():
  return Hypothesis where downstream_decisions.count >= impact_threshold AND supporting_evidence.count <= 1
```

### 7.3 Assumption Count / Depth

Recursively counts the depth of unproven dependent hypotheses supporting any active decision.

### 7.4 Ignorance Registry (Composite View)

Consolidates unproven high-impact nodes and sparse-evidence domains, automatically boosting their Expected Information Gain score inside Discovery Mathematics.

---

## 8. State Machines & Subsystem API Contracts

### 8.1 Hypothesis to Theory Promotion State Machine

```
proposed → under_test → active
                            │
                            ├── evidence accumulates, Bayesian updates continue
                            │
                            ▼
                    promotion_check (all required):
                      - independent_evidence_count >= 2, distinct source_types
                      - generalization_tested == true
                      - predictive_success_threshold_met == true
                        (>= 3 predictions made, accuracy_rate >= 0.7)
                            │
                            ▼
                    theory_promoted  →  Theory.status = "draft"
                                          → predictive_scope generates new Hypotheses
                                          → Theory.status = "active" once first prediction confirms
```

---

## 9. Explicitly Deferred (with stated trigger)

The following items are deferred from the build scope, only to be constructed when their specific trigger conditions are met:

| Deferred Item | Trigger to Build |
|---|---|
| **Formal Ontology** | Contradiction Detection false-positive rate exceeds 20% (semantic drift artifacts), OR the normalization synonym table exceeds 200 entries. |
| **Standalone Epistemic Risk Subsystem** | Epistemic Risk query layers require advanced cross-hypothesis blind-spot inference that basic queries cannot express. |
| **Multi-Level World Models as Separate Systems** | A single domain's update cadence or data source differs so heavily from others that coupling them causes stale-data errors. |
| **Full Scientific-Institution Layer** | Multiple independent human researchers/reviewers exist, requiring actual headcount and complex proper-scoring metrics (e.g., CRPS) to be meaningful. |

---

This contract is signed and approved. Any proposed deviation must be submitted through a formal ADR and approved before implementation.
