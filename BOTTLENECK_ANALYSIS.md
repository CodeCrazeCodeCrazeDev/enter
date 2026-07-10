# AgentHarness Bottleneck Analysis (Phase 1)

This document provides a highly critical diagnostic analysis of the performance, throughput, and token consumption bottlenecks in the AgentHarness framework.

---

## 1. Context Growth & Token Hotspots

### The Issue
Because AgentHarness uses a flat ReAct setup for standard executions, the context grows linearly with every tool execution. A single fetch from a dense scientific page or a long-form Wikipedia document can inject 50,000+ tokens immediately.

```
Turn 1: User Request (1,000 tokens)
Turn 2: Search Result (5,000 tokens)
Turn 3: Raw HTML Fetch (80,000 tokens)  <-- Context Spike!
Turn 4: Next Search (87,000 tokens)      <-- Wasteful overhead repeats!
```

### Impacts
- **Token Bleed**: On every subsequent turn, the model has to re-read the massive HTML payload from Turn 3, leading to severe token waste.
- **Compactor Trade-off**: The `KeepLastNToolResultsCompactor` resolves this by truncating old tool outputs. However, truncation creates a **knowledge loss** bottleneck where the model forgets raw details it previously collected, causing it to run repetitive search queries (re-fetching the same page again).

---

## 2. Scheduler & DAG Execution Bottlenecks

### Sequential State Transition
The `MiniDAGRunner` executes nodes in a strictly sequential, single-threaded execution chain. If a pipeline requires 5 independent searches or verification steps, they are executed one after the other.
- **Latency Delay**: Under standard conditions, this introduces major artificial latencies, especially when dealing with slow web scrapers or high-latency LLM endpoints.

---

## 3. Repeated Information Search (Lack of Semantic World Model)

### The Issue
There is no centralized state model or memory base representing current beliefs, facts, and entities.
- If the agent needs to verify the structure of a chemical molecule across three separate files, it has to repeatedly run `grep` or `fetch_web` searches because it has no local, structured memory of what it already discovered.
- The agent repeatedly reasons over raw context instead of structured semantic graphs, causing cognitive overload.
