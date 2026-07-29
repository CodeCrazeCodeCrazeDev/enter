# Design Decision Matrix: Capability Upgrades

This document evaluates each of the capability upgrades implemented inside the evolved `AgentHarness` framework.

---

| Capability Upgrade | Why It Improves the System | Alternatives Considered | Trade-Offs | Complexity | Expected Engineering ROI |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hierarchical Orchestration** | Decomposes complex tasks, prevents context overload. | Flat ReAct loop. | More orchestrator messages, but significantly better long-horizon reasoning. | Medium | **High**: Overcomes step limit decay. |
| **Planner / Executor Isolation** | Prevents context pollution from large tool outputs. | Combined ReAct strategist/executor. | Small initial planning delay, but yields major token savings. | Low | **Very High**: Saves up to 40% token costs on long runs. |
| **Persistent Semantic Memory** | Avoids repetitive web searches, preserves insights. | Pure sliding window truncation. | Small database query overhead. | Medium | **High**: Eliminates redundant information gathering. |
| **Meta-Reasoner / Echo Trap** | Detects infinite tool-call repetitions and goal drift. | Static loop limits. | Minor turn-level evaluation overhead. | Low | **Very High**: Prevents infinite loop hangs. |
| **Model-Collapse Guard** | Prevents synthetic SFT datasets from degrading models. | Unfiltered data writing. | Drops low-scoring data, but preserves long-term model quality. | Low | **High**: Safeguards self-improving flywheel. |
| **Parallel Verification** | Inline consensus verification increases factual accuracy. | Post-facto offline judges. | Increases verification latency. | Medium | **High**: Eliminates early-stage logical errors. |
