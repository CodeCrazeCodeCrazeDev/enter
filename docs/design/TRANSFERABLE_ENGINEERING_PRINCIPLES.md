# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research and synthesized inside the evolved `AgentHarness` and AlphaAlgo Research OS framework.

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

## Principle 5: Non-Gaussian Hawkes AST Call-Rate Bounds (Papers 301-320)
- **Concept**: Prevent self-modifying AST rewriting from runaway recursive cascades by enforcing non-Gaussian self-exciting Hawkes intensity thresholds and function-level AST call depth checks.
- **Implementation**: `CodeRewriteEngine.verify_proposal_ast` evaluates AST recursion call depth per function definition and enforces non-Gaussian Hawkes stability bounds before committing code rewrites.

## Principle 6: Island MAP-Elites Migration Sorting Gates (Papers 321-340)
- **Concept**: Preserve phenotypic and parameter diversity across evolutionary program synthesizers by gating migration between island populations and immediately re-sorting demes upon elite insertion.
- **Implementation**: `GeneticWorkflowOptimizer` enforces quality-diversity migration gates and maintains sorted population invariants during genome crossover and island migration.

## Principle 7: Advantage Margin Clipping for Trajectory Preference Alignment (Papers 341-360)
- **Concept**: Prevent reward scale inflation and policy overshoot during DPO/SFT trajectory preference compilation by applying clipped advantage margin bounds.
- **Implementation**: `SFTPreferenceCollector.compile_dpo_preference_pair` calculates temporal-difference advantage values and clips preference margins within defined bounds `[-clip_margin, clip_margin]`.

## Principle 8: Budget-Decayed Expected Free Energy (EFE) Task Routing (Papers 361-380)
- **Concept**: Route complex tasks across specialized agents using Active Inference EFE scores weighted by exponential financial budget decay.
- **Implementation**: `LearnableRoutingGateDispatcher.route_task` incorporates dynamic budget decay factors into epistemic curiosity and pragmatic success trade-offs.

## Principle 9: Multi-Field Namespace Literature Synthesis & Research Principle Registration (Papers 381-400)
- **Concept**: Enable autonomous Research OS to conduct literature reviews across multiple fields (`category`, `description`, `target_subsystem`, `paper_title`, `extracted_principle`, `impl_module`).
- **Implementation**: `ResearchOS.conduct_literature_review` queries registered research principles across all relevant metadata fields and maps whitespace opportunities to target subsystems.
