# ADR-001: Research Pipeline-First Architecture

## Status
Approved

## Context
In the previous baseline architecture (inherited from Apodex/AEAN), the platform relied on a collection of autonomous AI agents communicating via an asynchronous event bus or heuristic planner-driven loops. While flexible, this model is highly fragile and unsuited for institutional scientific quantitative research. Agent-centric designs often introduce non-determinism, "runaway optimization" (agents rewriting prompt instructions or code to bypass constraints), and a complete lack of verifiable scientific state tracking.

To transform AlphaAlgo into a world-class Quantitative Research Organization, we must enforce rigorous, repeatable, and audited scientific inquiry.

## Decision
We decide to adopt a **Research Pipeline-First Architecture** as the non-negotiable operational layer of the Research OS.

1. **Deterministic Execution Sequence:** The system defines a fixed, sequential, and non-bypassable research lifecycle:
   `Research Question` $\rightarrow$ `Hypothesis Registry` $\rightarrow$ `Data Validation` $\rightarrow$ `Feature Engineering` $\rightarrow$ `Experiment Sandbox` $\rightarrow$ `Statistical Validation` $\rightarrow$ `Robustness Analysis` $\rightarrow$ `Scientific Review` $\rightarrow$ `Promotion Gate` $\rightarrow$ `Model Registry`.
2. **De-escalation of AI Agents:** AI agents (e.g., planners, generators, critics) are restricted to being **operators** inside specific pipeline stages. For example:
   * A generator agent can query the Hypothesis Registry and suggest a new hypothesis.
   * A coder agent can implement the feature code for a hypothesis.
   * An LLM critic can act as a voter inside the Peer-Review Gate.
3. **No Bypass Allowed:** Under no circumstances can any agent, model, or human bypass a pipeline stage or promotion gate. All state transitions must be logged and validated by deterministic software checks.

## Consequences
* **Improved Scientific Validity:** Since all experiments must start with a pre-registered hypothesis and pass exact statistical significance thresholds, we completely eliminate backtest overfitting and HARKing.
* **Predictability & Scalability:** Separating pure mathematical processing and state registries from LLM agents allows the computational core to scale deterministically using standard multi-processing, without agent overhead.
* **Enhanced Observability:** Every model in production is fully traceable to its original pre-registered hypothesis, feature definitions, and exact experiment logs.
* **Migration Simplicity:** Existing multi-agent modules can be incrementally refactored and wrapped inside clean pipeline operators without disrupting the core state registries.
