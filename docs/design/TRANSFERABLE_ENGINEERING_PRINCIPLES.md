# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research and synthesized inside the evolved `AgentHarness` framework and `AlphaAlgo` cognitive operating system.

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

## Principles Extracted from Papers 301-400

## Principle 5: AST Hawkes Process Call Depth Control in Code Rewriting
- **Concept**: High-frequency self-referential code rewriting can trigger infinite recursion or stack overflows under non-Gaussian Hawkes process intensity spikes.
- **Implementation**: `CodeRewriteEngine.verify_proposal_ast` analyzes function definitions in AST nodes and tracks maximum recursive function call depth, vetoing proposals exceeding configured depth limits.

## Principle 6: Island MAP-Elites Migration & Diversity Preservation
- **Concept**: Evolutionary program synthesis requires maintaining Pareto diversity frontiers across sub-agent islands to prevent premature convergence.
- **Implementation**: `GeneticWorkflowOptimizer` applies MAP-Elites migration gates that automatically re-sort population genomes on elite insertion, maintaining high multi-objective fitness diversity.

## Principle 7: Clipped Trajectory Advantage Margins for DPO Preference Alignment
- **Concept**: Unbounded advantage margins during multi-turn trajectory preference collection lead to reward scale inflation and unstable DPO policy gradients.
- **Implementation**: `SFTPreferenceCollector` applies asymmetric margin clipping to advantage estimates before constructing chosen vs. rejected preference pairs.

## Principle 8: Budget-Decayed Expected Free Energy (EFE) Task Routing
- **Concept**: Active Inference Expected Free Energy (EFE) routing must balance epistemic curiosity against hard financial budget bounds.
- **Implementation**: `LearnableRoutingGateDispatcher` incorporates dynamic budget-decay scaling into EFE task routing, automatically downshifting to cost-optimal agents as spending approaches financial limits.
