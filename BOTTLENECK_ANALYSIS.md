# Bottleneck Analysis: AgentHarness

This document identifies the critical scaling, reasoning, and token-growth bottlenecks inherent in the baseline standard ReAct architecture.

---

## 1. Linear Context Expansion (The Infinite Scroll Problem)

### Symptom
As research tasks grow in horizon (e.g., 50+ turns, deep multi-query lookups), the chat history grows exponentially with raw webpage fetches and search results.

### Root Cause
- **Baseline ReAct**: Everything is kept in a single flat conversation.
- **Compactor Limitation**: Although the compactor removes raw content after `N` turns, the agent retains no semantic memory or structured knowledge of the compacted details. It must repeatedly re-retrieve identical information or guess, causing hallucinations.

---

## 2. Repeated Retrieval & Zero Cache Reuse

### Symptom
The agent fetches the same webpage or repeats similar search queries across different phases of research, blowing up both Jina/Serper APIs and LLM context costs.

### Root Cause
- No cross-turn persistent knowledge model or entity causal graphs.
- No semantic or persistent memory layer to store verified facts.

---

## 3. Flat Single-Agent Reasoning Bottleneck

### Symptom
One single agent is forced to perform long-term planning, coordinate tool invocations, verify its own work, and draft the final report. This leads to "agent fatigue," where planning precision degrades as execution history accumulates.

### Root Cause
- **No Division of Labor**: Planning is polluted by tool execution output, and verification is done by the same reasoning trace that executed the task (resulting in high confirmation bias).

---

## 4. Sequential Verification Bottleneck

### Symptom
If any verification or self-correction occurs, it happens synchronously inside the single ReAct loop, increasing turnaround latency.

### Root Cause
- No support for concurrent or multi-threaded verification pipelines.
