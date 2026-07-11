# ADR 004: Continuous Multi-Graph World Model (E-K-C-T-U)

## Status
Approved

## Context
Autonomous economic agents cannot operate on sequential text alone; they must maintain an structured understanding of their environment, entities, causal relationships, and Bayesian uncertainties to prevent repetitive searches and predict future outcomes.

## Decision
We build a continuous **Multi-Graph World Model** inside `apodex/world_model/` integrating five distinct sub-graphs:
- **Entity Graph ($G_E$)**: Physical/digital actors, competitors, products, and target markets.
- **Knowledge Graph ($G_K$)**: Verified factual assertions, beliefs, and observations.
- **Causal Graph ($G_C$)**: Directed state transitions mapping cause and effect.
- **Temporal Graph ($G_T$)**: Time-series logs and transition sequences.
- **Uncertainty Graph ($G_U$)**: Bayesian confidence bounds over relations and beliefs.

Key Features:
- Standardized entity nodes (`EntityNode`), relationship edges (`RelationshipEdge`), and beliefs (`BeliefNode`).
- Breadth-First-Search (BFS) pathfinding to discover chains of influence (e.g. Competitor -> Product -> Market).
- Continuous updating from raw environment observation events.

## Alternatives Considered
- **Traditional Relational Database**: Representing graphs with relational SQL joins. Rejected because recursive pathfinding and causal traversal is inefficient and syntactically complex in SQL.

## Consequences
- **Pros**:
  - Highly structured, non-linear reasoning foundation.
  - Supports causal inference, expected utility evaluation, and counterfactual query resolution.
- **Cons**:
  - Graph updates require lock management to prevent concurrent state corruption.
