# AgentHarness Bottleneck & Performance Analysis (Phase 1) - Enhanced

This document outlines the core operational, token-consumption, and scheduling bottlenecks discovered during the technical audit of the AgentHarness repository.

---

## 1. Context Growth & Token Hotspots

### The Issue
AgentHarness implements standard ReAct as a single linear message history. When high-volume search tools or web scrapers are executed, their complete outputs are appended directly to the short-term chat context.

```
+-------------------------------------------------------------+
| System Prompt                                               |
+-------------------------------------------------------------+
| User Query                                                  |
+-------------------------------------------------------------+
| Assistant: Call web_fetch                                   |
+-------------------------------------------------------------+
| Tool output: 120,000 characters of raw HTML fetched         | <--- Huge payload spike!
+-------------------------------------------------------------+
| Assistant: Parse data...                                    |
+-------------------------------------------------------------+
| Tool output: Next search...                                 | <--- Massive token bleed begins!
+-------------------------------------------------------------+
```

### Impacts
- **Exponential Token Bleed**: On every step after step $N$, the agent must re-read all historical HTML payloads, causing token consumption to grow quadratically:
  $$\text{Total Tokens} \propto O(T^2)$$
  where $T$ represents the turn length.
- **Compaction Trade-off**: The `KeepLastNToolResultsCompactor` mitigates this by replacing older tool messages with brief placeholders. However, this creates an **Information Loss Trap**: the agent loses historical details, gets confused, and repeatedly issues duplicate searches or code sandbox retries to retrieve the exact same data again.

---

## 2. DAG Scheduler Execution Bottlenecks

### The Issue
The current scheduler (`scheduler.py`) maps the execution of `PipelineSpec` nodes in a sequential, synchronous loop.
- **Sequential Verification Delay**: Verification steps are forced to execute sequentially, meaning each domain-specific judge is called one after another.
- **No Path Branching**: There is no capability to parallelize independent nodes (e.g., executing multiple search paths simultaneously).

---

## 3. Repeated Information Retrieval (Zero State Sharing)

### The Issue
The agent does not possess a structured local memory (such as a World Model or Causal Graph).
- Every query, fact, or entity discovered must be re-extracted or re-fetched from the web or sandbox files on subsequent turns.
- No cross-session memory is maintained, meaning the agent cannot learn successful strategies across different tasks.
