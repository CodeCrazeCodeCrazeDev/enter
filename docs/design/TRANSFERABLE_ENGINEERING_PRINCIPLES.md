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

## Principle 5: Hawkes Non-Gaussian AST Call Depth Verification
- **Source**: Papers 301-320 (Market Microstructure & Non-Gaussian Stochastic Volatility)
- **Concept**: Prevent false-positive AST rejections in self-correcting code engines by scoping recursion depth calculations per function definition instead of counting aggregate AST-wide occurrences.
- **Implementation**: `CodeRewriteEngine.verify_proposal_ast` tracks per-function call stack depth using AST visitor nodes to ensure non-Gaussian Hawkes stability without rejecting standard library calls.

## Principle 6: Island MAP-Elites Migration Gate & Type-Safe Mutation
- **Source**: Papers 381-400 (Genetic Search & Meta-Evolution)
- **Concept**: Preserve genetic diversity and prevent population contamination by re-sorting island populations on elite insertion and checking bool types before int/float during parameter mutation.
- **Implementation**: `GeneticWorkflowOptimizer` enforces bool check precedence in `_mutate_parameters` and immediate sorting upon elite insertion in `perform_crossover_and_mutation`.

## Principle 7: Clipped Trajectory Advantage Margins
- **Source**: Papers 341-360 (Trajectory Preference Alignment & Process Supervised DPO)
- **Concept**: Prevent unbounded gradient explosion in trajectory preference collectors under high variance.
- **Implementation**: `SFTPreferenceCollector` applies asymmetric advantage clipping bounded within $[-2.0, 2.0]$ in `compute_advantages`.

## Principle 8: Budget-Decayed EFE Task Routing
- **Source**: Papers 321-340 (Active Inference & Epistemic Curiosity) & Papers 361-380 (Multi-Agent Swarm Bidding)
- **Concept**: Route complex agentic tasks according to Expected Free Energy (EFE) with continuous decay to prevent budget exhaustion and starvation.
- **Implementation**: `LearnableRoutingGateDispatcher` dynamically decays subagent budget capacity during task routing without zero-division errors.
