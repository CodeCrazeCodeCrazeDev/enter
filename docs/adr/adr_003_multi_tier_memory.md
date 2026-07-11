# ADR 003: Multi-Tier Persistent Memory (SQLite-Backed)

## Status
Approved

## Context
High-ceiling intelligence requires tracking working contexts, episodic execution traces, persistent facts, and cross-session strategies. Flat memory or pure in-memory caches cause irreversible amnesia on restart and cannot scale to support thousands of concurrent multi-agent runs.

## Decision
We design a unified **Multi-Tier Memory** subsystem located inside `apodex/memory/`. Memory is cleanly partitioned and backed by local-first persistence:

1. **Working Memory**: Transient context of the current turn (ReAct tool buffer).
2. **Episodic Memory**: Sequence of execution trajectories, specific events, and historical attempts.
3. **Semantic Memory**: Persistent factual schemas, beliefs, entity relations, and world graph snapshots, implemented using a local-first SQLite database (`SQLiteMemoryRepository`).
4. **Procedural Memory**: Skills, optimized code patterns, and registered tool actions.
5. **Long-Term Learning Memory**: Cross-session strategy store tracking task success ratios and learned insights.

Key mechanics:
- **Echo Trap Guard (E1)**: Detects repeated identical tool calls and raises intervention prompts.
- **Deduplication (E3)**: De-duplicates evidence cards based on source URLs and content hashes.
- **Semantic Token Consolidator (E3)**: Dynamically prunes lower-confidence facts and beliefs when total tokens (measured using `tiktoken`) exceed a strict threshold.
- **Model-Collapse Guard (E9)**: Automatically warnings or downsamples self-generated trajectories during dataset compilation to prevent semantic degradation.

## Alternatives Considered
- **NoSQL / Key-Value Stores (Redis)**: Great for low-latency caching but lacks relational query structures for entity resolution. Can be easily swapped in the future behind our repository interfaces.

## Consequences
- **Pros**:
  - Safe, local-first transactional storage.
  - Cognitive safety guards built-in to prevent infinite loops, goal drift, and memory bloat.
- **Cons**:
  - Thread synchronization must be handled carefully when using SQLite (mitigated via local-first connections).
