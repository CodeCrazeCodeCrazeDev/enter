# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research (across 400 papers) and synthesized inside the evolved `AgentHarness` and `AlphaAlgo` framework.

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

## Principle 5: Hawkes Non-Gaussian Self-Excitation AST Validation (Papers 301-320)
- **Concept**: Model self-referential code rewrite proposals as non-Gaussian point processes with strict recursion limits.
- **Implementation**: `CodeRewriteEngine.verify_proposal_ast` tracks recursive AST call depth on rewritten code snippets to enforce bounded excitation stability and prevent infinite execution loops.

## Principle 6: Island MAP-Elites Migration Gating (Papers 381-400)
- **Concept**: Maintain high structural diversity across genetic workflow genomes via island-based MAP-Elites populations.
- **Implementation**: `GeneticWorkflowOptimizer` immediately re-sorts island population upon elite genome insertion and enforces strict type checking during mutation to prevent parameter corruption.

## Principle 7: Advantage Margin Clipped DPO Alignment (Papers 341-360)
- **Concept**: Bound preference margins in Direct Preference Optimization to prevent reward scale inflation and trajectory overfitting.
- **Implementation**: `SFTPreferenceCollector` applies min-max trajectory advantage margin clipping (`[-10.0, 10.0]`) to align multi-turn agent execution traces without reward drift.

## Principle 8: Budget-Decayed EFE Task Dispatching (Papers 321-340, 361-380)
- **Concept**: Route complex task workloads using Expected Free Energy (EFE) incorporating epistemic curiosity, pragmatic historical value, and decaying financial token budgets.
- **Implementation**: `LearnableRoutingGateDispatcher.route_task` dynamically computes active inference EFE scores while applying remaining budget multipliers to guarantee zero budget overrun.

## Principle 9: Multi-Field Literature Review Lookup (Papers 301-400 Synthesis)
- **Concept**: Query research principles across category, domain description, target subsystem, paper title, and implementation modules.
- **Implementation**: `ResearchOS.conduct_literature_review` indexes all 400 paper corpus principles for autonomous research synthesis.
