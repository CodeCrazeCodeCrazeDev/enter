# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research and synthesized inside the evolved `AgentHarness` framework.

---

## Principle 1: Hexagonal Isolation of Strategic Planning
- **Concept**: Never pollute the strategic planning history with task execution outputs.
- **Implementation**: The `StrategicPlanner` compiles a frozen `Roadmap`, while the `TaskExecutor` processes individual steps. Output payloads are validated by a `PlanVerifier` and kept strictly isolated from the planner's memory.

## Principle 2: Multi-Tier Memory Consolidation
- **Concept**: Distinguish short-term context window history from persistent semantic memory.
- **Implementation**: Short-term history is compacted via sliding windows, while structured evidence cards, facts, and beliefs are persisted inside a SQLite semantic memory repository. High-confidence facts are promoted, and low-confidence ones are pruned to satisfy token budgets.

## Principle 3: Model-Collapse Guard via Quality Downsampling
- **Concept**: Automatically prevent self-generated SFT training datasets from causing recursive model degradation.
- **Implementation**: The `TrajectoryDatasetCompiler` tracks the ratio of self-generated vs. real trajectory traces. In strict mode, it raises errors on threshold breach; in relaxed mode, it downsamples self-generated data, keeping only high-scoring traces.

## Principle 4: Two-Level Credit Assignment
- **Concept**: Calculate both global trajectory success and progressive step-level contribution.
- **Implementation**: The `TwoLevelCreditAssignment` engine applies positive reinforcement ($1.0 \times \frac{i}{N}$) for successful steps, and progressive penalties ($-0.2 \times \frac{i}{N}$) for steps leading to failure.

---

## Synthesis of 200-Paper Corpus Principles (IDs 301–500)

The 200-paper research corpus (IDs 301–500) expands transferable engineering principles across four primary cognitive subsystems: `aean`, `eos`, `eios`, and `researchos`.

### Subsystem: AEAN (Autonomous Agent Swarms)
- **Principle 5: Sycophancy-Resilient Token Bidding & Adversarial Deliberation Networks**
  - **Source Papers**: Papers 421, 423, 429, 458
  - **Concept**: Prevent sycophantic consensus collapses in multi-agent networks through dual-judge audit logs and token bidding mechanisms.
  - **Implementation**: `AEAN` token benders apply adversarial deliberation filters to verify sub-agent claims before granting compute resources.

### Subsystem: EOS (Entrepreneurial Operating System)
- **Principle 6: Non-Gaussian Hawkes Self-Exciting Order Flow & Inventory Risk Bounds**
  - **Source Papers**: Papers 302, 304, 310, 320
  - **Concept**: Model continuous liquidity cascades and volatility clustering using non-Gaussian Hawkes point processes.
  - **Implementation**: `CodeRewriteEngine` and `EOSEngine` enforce inventory risk limits and non-Gaussian AST recursion bounds.

### Subsystem: EIOS (Sensing Kernel & Active Inference)
- **Principle 7: Expected Free Energy (EFE) Budget-Decayed Task Routing**
  - **Source Papers**: Papers 341, 345, 350, 360, 375
  - **Concept**: Route perception and active inference sensing tasks based on Epistemic Value (curiosity) and Pragmatic Value bounded by financial/token budgets.
  - **Implementation**: `LearnableRoutingGateDispatcher` updates agent epistemic curiosity dynamically using Bayesian Beta updates and EFE scoring.

### Subsystem: ResearchOS (Autonomous Scientific OS)
- **Principle 8: Island MAP-Elites Workflow Mutation & Trajectory DPO Margin Clipping**
  - **Source Papers**: Papers 381, 382, 391, 461, 486
  - **Concept**: Perform evolutionary program synthesis using island-isolated MAP-Elites populations and clip trajectory DPO advantage margins to stabilize preference alignment.
  - **Implementation**: `GeneticWorkflowOptimizer` sorts island populations upon elite insertion, and `SFTPreferenceCollector` applies advantage bounds.
