# Architectural Gaps Analysis: Flat vs. Hierarchical Architectures

This document identifies major architectural duplication, hidden coupling, and performance bottlenecks in legacy flat ReAct orchestration setups, contrasting them against our newly integrated target framework.

---

## 1. Context Bloat and Attention Decay
- **Gap**: In flat single-agent systems, the agent is exposed to all tool messages sequentially. As a result, the context grows linearly, causing the model to lose reasoning attention and hallucinate tool parameters.
- **Resolution**: Implemented separate `StrategicPlanner` and `TaskExecutor` pipelines, keeping the planner's strategic history clean.

## 2. Brittle Infinite Loops (Echo Traps)
- **Gap**: Legacy loops had no active observation of tool parameters. If the model got stuck, it would call the same search query or compiler command indefinitely.
- **Resolution**: Introduced the `MetaReasonerObserver` which active-scans and breaks repetitive Echo Traps immediately.

## 3. Passive Amnesia vs. Active Memory
- **Gap**: Legacy compactors perform raw text truncation to satisfy context budgets, resulting in irreversible amnesia.
- **Resolution**: Implemented the SQLite `SemanticMemory` engine to actively consolidate and persist Evidence, Facts, and Beliefs across sessions.
