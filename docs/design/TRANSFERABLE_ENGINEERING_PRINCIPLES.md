# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research and synthesized inside the evolved `AgentHarness` framework and AlphaAlgo.

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

## Principles Extracted from AlphaAlgo 301-400 Research Corpus

## Principle 5: Hawkes AST Call Depth Verification (Papers 302, 383)
- **Concept**: Non-Gaussian Hawkes self-exciting processes require recursion call-depth stability checks to prevent self-referential stack overflow during code mutation.
- **Implementation**: `CodeRewriteEngine.verify_proposal_ast` analyzes function definition call trees in proposed code ASTs, enforcing a maximum AST recursion call depth limit to guarantee safe execution.

## Principle 6: MAP-Elites Island Migration Gates & Parameter Safeguards (Papers 382, 389, 390)
- **Concept**: Quality diversity search in genetic workflows requires immediate re-sorting of island populations upon elite insertion and parameter mutation bounding.
- **Implementation**: `GeneticWorkflowOptimizer` re-sorts island populations descending by fitness score whenever new elites are created or migrated, and guards parameter types against non-physical negative values.

## Principle 7: Clipped Trajectory Advantage Margin Bounds (Papers 341, 342, 354)
- **Concept**: Off-policy DPO trajectory preference tuning requires advantage margin bounds to prevent extreme advantage differentials from causing gradient explosion.
- **Implementation**: `SFTPreferenceCollector.compile_dpo_preference_pair` applies smooth hyperbolic tangent advantage margin clipping (`math.tanh(margin / 5.0) * 5.0`) to keep training signals bounded.

## Principle 8: Budget-Decayed Expected Free Energy Task Routing (Papers 327, 377)
- **Concept**: Active inference task dispatchers operating under finite financial budgets must incorporate exponential budget decay into EFE utility scores.
- **Implementation**: `LearnableRoutingGateDispatcher.route_task` applies a exponential budget decay factor $\exp(-1.5 \cdot \text{spent} / \text{limit})$ to high-cost agent EFE scores, ensuring smooth Pareto-optimal agent transitions.

## Principle 9: Multi-Field Semantic Knowledge Graph Querying (Paper 392)
- **Concept**: Research Operating System literature synthesis should perform multi-field semantic matching across scientific knowledge graphs rather than returning static templates.
- **Implementation**: `ResearchOS.conduct_literature_review` queries registered research principles across category, description, target subsystem, paper title, and extracted principle fields.
