# Technical Debt Analysis: AgentHarness

This document logs architectural and structural technical debt in the existing baseline setup.

---

## 1. Lack of Modular Memory Abstraction
- **Debt**: Conversation history is passed as a raw array of dictionaries throughout `run_agent_loop` and `main_agent_node`.
- **Impact**: Any attempt to inject custom semantic memory, world-model graphs, or long-term caching requires invasive overrides of the core loop rather than simple plugin composition.

## 2. Rigid XML-based Tool Call Parser
- **Debt**: `tool_call_parser.py` is closely coupled with Qwen XML-style tags or standard qwen formats.
- **Impact**: Multi-agent orchestration with distinct roles or model providers that emit other tool-calling formats (e.g. native JSON schemas) might break.

## 3. Absence of Intermediate Event-Driven State Checks
- **Debt**: The `Scheduler` executes a synchronous sequence of nodes.
- **Impact**: No support for dynamically branching graph structures based on runtime signals (e.g. Meta Reasoner flagging planning failures).

## 4. Subprocess-Only Concurrency
- **Debt**: Parallelism is achieved solely by spawning OS processes.
- **Impact**: High overhead for small tasks, difficulty in sharing in-memory caches or learning memories across sessions without persistent databases.
