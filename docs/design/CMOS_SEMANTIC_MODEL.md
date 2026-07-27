# CMOS Formal Semantic Model (Ontology)

This document defines the formal ontology, semantic taxonomy, identity/versioning rules, temporal properties, and logical invariants for the **Cognitive Memory Operating System (CMOS)**.

---

## 1. Node Taxonomy

To support autonomous, long-horizon research and self-improvement, CMOS establishes an explicit, polymorphic node taxonomy. Every node is registered with a global `node_type` and inherits a common base schema.

### 1.1 Core Nodes
*   `ClaimNode`: Stored independently of hypotheses. Represents a declarative assertion or conclusion derived from research or system execution (e.g., "Adaptive prompt version B improves pass rate by 12%").
*   `EvidenceNode`: Concrete, factual, raw observations, backtests, raw environment signals, system logs, or market data backing a claim.
*   `TheoryNode`: Coherent collections of hypotheses, rules, or domain behaviors representing a system-level schema.
*   `StrategyNode`: Represents a system or agent configuration, tool composition, prompt variant, or trading/reasoning protocol. A Strategy must contain:
    *   Assumptions (prerequisites)
    *   Supporting evidence
    *   Known failure modes
    *   Applicable regimes
    *   Historical performance metrics
*   `RegimeNode`: Environmental context or dynamic condition state (e.g., "Bull Market", "High Token Latency", "Docker Sandbox Isolation").
*   `ModelNode`: Concrete cognitive model definitions, weights references, neural net templates, symbolic rules, or RL policy signatures.
*   `DecisionNode`: Immutable record of a production or system action (e.g., "Promoted prompt variant C to main branch").
*   `LessonNode`: High-level institutional wisdom or generalized insights extracted from debugging or experiment cycles.
*   `FailureNode`: Detailed tracking of unexpected behavior, code execution timeouts, or failed validation attempts.
*   `HypothesisNode`: Formulations under active scientific investigation. Must specify falsifiability criteria, target metrics, and lineage.
*   `ExperimentNode`: Concrete test run details (parameters, code modifications, Git diffs, hardware logs, target results).

---

## 2. Edge Taxonomy

Edges are typed and represent explicit relationships, constraints, or flows between nodes.

*   `CausalEdge`: Indicates a cause-and-effect relationship (e.g., `RegimeNode` $\to$ `FailureNode`, or `ModelNode` $\to$ `DecisionNode`). Contains strength, treatment effect, and p-value metrics.
*   `SupportEdge`: Represents evidence or a sub-claim verifying/backing another node. Holds a positive weight value.
*   `ContradictsEdge`: Connects nodes representing mutually exclusive or opposing assertions.
*   `LineageEdge`: Maps version evolution or historical origin (e.g., `StrategyNode_v1` $\to$ `StrategyNode_v2`).
*   `TemporalEdge`: Represents chronological sequence or dependency (e.g., `Experiment_1` $\to$ `Decision_1`).

---

## 3. Provenance Semantics

Every node and edge must carry an immutable provenance block:
```json
{
  "origin": "string (e.g., system_component, user, or loop name)",
  "timestamp": "ISO 8601 UTC timestamp",
  "creator_id": "string (agent ID or user ID)",
  "confidence": "float [0.0, 1.0]",
  "git_sha": "string (representing code state)",
  "experiment_id": "optional UUID referencing the backing experiment",
  "reasoning_path": "list of node IDs navigated to produce this entity"
}
```

---

## 4. Identity and Versioning Rules

1.  **Identity Rule**: Nodes are identified by a UUID v4 or a deterministic namespace hash computed from the node's immutable fields (e.g., `sha256(content + creator_id + git_sha)`).
2.  **Versioning Rule**: Nodes are strictly immutable. If an assertion or strategy is updated:
    *   A new Node instance is created.
    *   A `LineageEdge` of type `SUPERSEDES` or `DERIVED_FROM` is drawn from the older node to the newer node.
    *   The older node's state is updated to `archived` or `superseded` in the metadata.

---

## 5. Confidence and Contradiction Semantics

### 5.1 Confidence Mechanics
*   **Initial Confidence**: Determined by source type (e.g., `EvidenceNode` = 1.0, `ClaimNode` from unverified LLM = 0.5).
*   **Propagation Rule**: The confidence of a `ClaimNode` is a function of its supporting nodes:
    $$\text{Confidence}(C) = \psi\left(\prod_{e \in \text{SupportEdges}} \text{Confidence}(e.\text{source})\right)$$
*   **Recursive Degradation**: If an `EvidenceNode` $E$ is deleted or refuted, its confidence falls to 0.0. All downstream `ClaimNode` and `TheoryNode` instances reachable via `SupportEdge` paths must trigger a recursive recalculation, automatically degrading their respective confidence scores.

### 5.2 Contradiction Mechanics
*   If a new node is inserted that has a `ContradictsEdge` to an active node, or if semantic similarity vectors reveal an opposing assertion, CMOS creates a `ConflictNode` (T0).
*   The `ConflictNode` initiates a validation trigger for the `MemoryScheduler` to schedule a `Verify` action, requiring the System to challenge or gather further evidence.

---

## 6. Temporal Semantics

*   **Temporal Decay**: Decaying knowledge (e.g., ad performance, system load, specific conversational context) undergoes exponential decay of its confidence score over time:
    $$C(t) = C_0 \cdot e^{-\lambda(t - t_0)}$$
    Where $\lambda$ is determined by the node category or domain half-life.
*   **Evergreen Stability**: Principles, structured code interfaces, and verified scientific assertions are flagged as `evergreen`, exempting them from temporal confidence decay.
