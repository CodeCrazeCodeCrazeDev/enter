# ADR 013: Tri-Partition Memory Engine with Ebbinghaus Forgetting Curves

## Status
Proposed

## Context
Standard RAG vector databases scale poorly, lead to token saturation, suffer from memory consolidation bloat, and do not prioritize procedural or episodic memory differently.

## Decision
We design a tri-partitioned Memory Engine (Episodic, Semantic, Procedural) integrated with an exponential Ebbinghaus forgetting decay curve. Retrieved memories are filtered using Jaccard token similarity over an offline relator db, decaying less-accessed fragments organically.

## Alternatives Considered
- **All-In-One Vector DB (Rejected)**: Lacks episodic/procedural classification, does not support decay, and leads to context pollution.

## Expected Benefits
- Retrieval latency $< 30\text{ ms}$.
- Context pollution reduced by over $80\%$ via active decay consolidation.

## Failure Modes
- **Memory Collision**: Handled by Jaccard overlap similarity matching thresholds.

## Validation Plan
Simulate memory retrieval queries after varied decay steps and evaluate curve fidelity.
