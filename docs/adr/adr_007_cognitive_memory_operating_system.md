# ADR 007: Cognitive Memory Operating System (CMOS)

## Status
Approved

## Purpose and Scope
The Cognitive Memory Operating System (CMOS) is designed as a next-generation first-class institutional memory and active cognitive computation substrate for Apodex. It elevates memory from a passive storage/retrieval database into an active, decision-making, and reasoning participant in long-horizon autonomous intelligence.

CMOS synthesizes and surpasses the core mechanics of two foundational paradigms:
1. **Remember When It Matters (Proactive Memory Agent)**: CMOS converts the concept of proactive, multi-phase memory management into persistent, structured background evolution and selective active memory intervention.
2. **From Passive Retrieval to Active Memory Navigation (NapMem)**: CMOS replaces standard vector/keyword searches with sequential, structured navigation across a multi-resolution hierarchical Memory Graph using specialized, registered cognitive operators.

CMOS runs as an independent cognitive service accessed via stable interfaces by the Cognitive System Controller (CSC) and other Apodex sub-systems (e.g., World Model, Research OS, Verification Swarm, Risk Engine).

## Ownership Boundaries
- **Cognitive System Controller (CSC)**: Remains the orchestrator of execution, reasoning, and planning. It interacts with CMOS to execute cognitive queries and retrieve synthesized contexts.
- **CMOS**: Authoritative over the validation, evolution, provenance, and economics of the institutional memory graph. It does *not* make business or autonomous decisions; it exposes active cognitive and memory services.
- **World Model**: Uses CMOS to project transient "what-if" counterfactual memories via memory simulation, ensuring temporary branches do not contaminate permanent institutional records until fully validated.

## Interfaces and Invariants
- **Pluggable Operator Registry**: All memory-reasoning operations are represented as polymorphic cognitive operators inheriting from a common interface (`CognitiveOperator`) and registered within the `OperatorRegistry`. Direct method-based calls like `memory.compare()` are forbidden.
- **Memory Query Planner**: Decouples natural-language or programmatic cognitive goals of the CSC from underlying graph traversal. The planner translates high-level objectives into executable query plans of sequential cognitive operators.
- **Temporal-Tiered Evolution**: Background maintenance tasks are partitioned into four distinct temporal buckets (Immediate, Short-term, Medium-term, Long-term) managed by an institutional `MemoryScheduler`.
- **Memory Invariant 1 (Strict Provenance)**: Every node or edge added to the Memory Graph must have immutable provenance fields (origin, timestamp, creator, confidence, evidence, git SHA, and experiment ID).
- **Memory Invariant 2 (Verification and Tracing)**: Every claim or belief must resolve back to verifiable evidence nodes or causal models. If supporting evidence is pruned or discredited, all downstream derived claims must undergo recursive confidence degradation.
- **Memory Invariant 3 (Finite Economic Capacity)**: System memory is finite and governed by a utility scoring formula combining retrieve frequency, decision impact, compression ratio, and storage cost. Obsolete knowledge is continuously pruned, archived, or compressed.

## Failure Model
- **Disconnection/Degradation**: If a remote storage repository or high-capacity vector model becomes unavailable, the repository layer automatically degrades to a local-first SQLite repository, and scoring defaults to cheap, localized heuristics.
- **Concept Drift**: When incoming evidence contradicts deeply rooted beliefs, CMOS logs a conflict node, triggers verification protocols, and flags the anomaly without corrupting historical assertions.
- **Hallucination / Goal Drift**: Operators must never mutate the stable institutional graph with unverified assertions. All speculative or tentative reasonings must run inside a sandbox-isolated virtual graph space (Memory Simulation).

## Performance Targets
- **Operator Execution Latency**: Local-first repository lookups and simple operator steps (e.g., `Recall`, `Verify`) must execute in under 100 milliseconds.
- **Token Economy (E3 Limit)**: Support packs built by CMOS must fit within user-defined context token budgets (strictly truncated to prevent context window overrun).
- **Storage Profile**: Clean decoupling of active graph memory and cold-storage archives ensures the hot working memory footprint is minimized.

## Non-Goals
- CMOS is not a general-purpose vector database wrapper.
- CMOS is not responsible for direct code generation, system shell execution, or high-level transaction orchestration.
- CMOS does not maintain conversational chat sessions directly; it processes execution traces, lessons, and claims derived from them.
