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

## Principles Extracted from AlphaAlgo 301-400 Paper Corpus

## Principle 5: Non-Gaussian Hawkes Stability with Recursive Call Depth Limits
- **Concept**: Bound continuous-time branching processes and prevent unbounded recursive function calls in self-modifying AST code synthesis.
- **Implementation**: Enforce spectral radius limits ($\sum \alpha_{ij} / \beta_{ij} < 1.0$) and function-level recursive AST call depth verification in `CodeRewriteEngine`.

## Principle 6: MAP-Elites Island Migration Protocol with Sorted Population Invariance
- **Concept**: Maintain high diversity in high-dimensional workflow optimization without population degradation.
- **Implementation**: `GeneticWorkflowOptimizer` enforces island population re-sorting immediately on elite insertion and strict type checks (distinguishing `bool` from `int`/`float`) during parameter mutation.

## Principle 7: Advantage Margin Normalization in Trajectory Direct Preference Optimization
- **Concept**: Prevent reward signal collapse and logit explosion during offline preference learning over agent decision trajectories.
- **Implementation**: `SFTPreferenceCollector` applies clipped advantage margins to trajectory pairs before updating preference weights.

## Principle 8: Budget-Decayed Expected Free Energy Task Routing
- **Concept**: Balance epistemic curiosity and financial cost as operational resources decay.
- **Implementation**: `LearnableRoutingGateDispatcher` dynamically scales the cost penalty in Expected Free Energy (EFE) task routing based on remaining budget proportions.

## Principle 9: Multi-Field Cross-Domain Semantic Search for Literature Intelligence
- **Concept**: Provide comprehensive cross-domain discovery across research hypotheses, principles, and implementation targets.
- **Implementation**: `ResearchOS.conduct_literature_review` queries across paper categories, descriptions, titles, target subsystems, extracted principles, and implementation modules.
