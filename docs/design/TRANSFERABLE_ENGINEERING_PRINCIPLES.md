# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research (across papers 1-400) and synthesized inside the evolved `AgentHarness` and `AlphaAlgo` framework.

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

## Principle 5: AST-Isolated Self-Referential Code Rewriting with AST Recursive Call Depth Tracking (Papers 301-320, 381-400)
- **Concept**: Automated program synthesis and code modification must enforce strict AST tree compilation and local recursion depth boundaries before disk commitment.
- **Implementation**: The `CodeRewriteEngine` in `apodex/ai_eos/research/integration.py` parses proposed modifications into abstract syntax trees, checks for forbidden functions (`eval`, `exec`, `system`), and specifically tracks function-level recursive call depths to guarantee execution stability without false positives on standard library calls.

## Principle 6: Island MAP-Elites Migration Gates with Population Re-sorting (Papers 381-400)
- **Concept**: Population diversity in genetic program synthesis prevents premature convergence while maintaining elite quality across isolated sub-populations.
- **Implementation**: The `GeneticWorkflowOptimizer` executes island-based population tracking, applying MAP-Elites migration gates that immediately re-sort and re-rank the population when external elites are inserted, preserving fitness ordering across generations.

## Principle 7: Clipped Advantage Margins in Trajectory DPO (Papers 341-360)
- **Concept**: Off-policy preference tuning over LLM action sequences can suffer from reward inflation or extreme advantage variance.
- **Implementation**: The `SFTPreferenceCollector` computes step-wise temporal difference advantages $A_t = G_t - V(s)$ and applies advantage clipping thresholds to trajectory advantage margins $(\text{adv}_{\text{chosen}} - \text{adv}_{\text{rejected}})$, preventing gradient explosion during direct preference optimization.

## Principle 8: Budget-Decayed Expected Free Energy Task Routing (Papers 321-340, 361-380)
- **Concept**: Task routing in multi-agent networks must balance epistemic curiosity (information gain) and pragmatic utility against strict financial token/dollar budgets.
- **Implementation**: The `LearnableRoutingGateDispatcher` evaluates sub-agent candidates using an Active Inference EFE score ($\text{Score} = \text{Epistemic} + \text{Pragmatic} - \text{CostPenalty}$). When financial budget spend approaches limits, epistemic curiosity is decayed exponentially to prioritize high-confidence, low-cost execution.
