# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research (across 500+ quantitative publications) and synthesized inside the evolved `AgentHarness` and `APODEX` framework.

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

## Principle 5: Hawkes Self-Exciting Intensity Bounds for Order Flow & Code Mutation Rates
- **Concept**: Model event burstiness (order cancellations, code mutations, anomaly spikes) using non-Gaussian self-exciting point processes with strict intensity stability bounds.
- **Implementation**: In `CodeRewriteEngine`, mutation frequency is regulated via self-exciting Hawkes intensity decay parameters to prevent run-away code rewrites or execution loops.

## Principle 6: Active Inference Expected Free Energy (EFE) Task Routing
- **Concept**: Delegate tasks across specialized sub-agents by evaluating Expected Free Energy (EFE), balancing Pragmatic Value (historical success rate) and Epistemic Value (epistemic curiosity / surprise reduction) under financial token budget constraints.
- **Implementation**: `LearnableRoutingGateDispatcher` calculates `efe_routing_score = pragmatic_value + epistemic_value - cost_penalty` and dynamically routes tasks to optimal agents while decaying curiosity as uncertainty reduces.

## Principle 7: Advantage-Weighted Direct Preference Alignment with Clipped Trajectory Margins
- **Concept**: Construct DPO preference records over multi-turn agent action trajectories by computing temporal-difference advantages with clipped margin penalties to prevent reward scale inflation.
- **Implementation**: `SFTPreferenceCollector` evaluates cumulative discounted trajectory returns against value function expectations, pairing chosen vs. rejected traces with explicit margin tracking.

## Principle 8: Sycophancy-Robust Multi-Agent Peer Review Consensus
- **Concept**: Eliminate bias and sycophancy in multi-agent deliberation networks via Vickrey-Clarke-Groves (VCG) auction mechanisms, token bidding, and adversarial peer review probing.
- **Implementation**: `HiveMind` coordinates sub-agent token bidding and research hypothesis integration, ensuring transparent, budget-bounded execution and capital allocation.

## Principle 9: Island-Based MAP-Elites Program Synthesis & Workflow Mutation
- **Concept**: Maintain high quality-diversity archives of workflow parameters and prompt templates across isolated population islands.
- **Implementation**: `GeneticWorkflowOptimizer` executes island population initialization, Gaussian parameter mutation, crossover, and MAP-Elites routing sorted by fitness score.

## Principle 10: Self-Referential Code Rewrite Safety Isolation
- **Concept**: Guarantee safe runtime self-improvement and AST code mutation through multi-stage verification before committing code changes.
- **Implementation**: `CodeRewriteEngine` enforces path boundaries, AST syntax parsing, static security linting (disallowing `eval`, `exec`, `os.system`), and sandboxed dry-run simulation.
