# Transferable Engineering Principles for Autonomous Research OS & AlphaAlgo

This document outlines the core engineering principles extracted from the 300-paper quantitative research corpus (IDs 1–300) and synthesized inside the evolved `AgentHarness` framework and AlphaAlgo Research OS.

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

## Principle 5: Microstructure Noise Clamping & Hawkes Point Process Filtering
- **Concept**: High-frequency order book and sensor signals contain non-Gaussian fat tails and self-exciting volatility bursts.
- **Implementation**: AlphaAlgo Research OS incorporates Hawkes process self-excitation kernel bounds and variance-scaling filters inside `statistical_validation.py` to prevent false discovery during high-volatility backtesting.

## Principle 6: Active Inference & Expected Free Energy Routing
- **Concept**: Balance pragmatic value (goal achievement) and epistemic value (information gain / curiosity) in autonomous research navigation.
- **Implementation**: Decision pathways evaluate $EFE = \text{Pragmatic Value} + \beta \times \text{Epistemic Information Gain}$, guiding hypothesis generation and routing sub-agents to areas of highest unmodeled uncertainty.

## Principle 7: Sycophancy-Robust Dual-Agent Verification
- **Concept**: Single LLM judges tend towards sycophantic agreement, inflating performance metrics during peer review.
- **Implementation**: Multi-mind deliberation networks deploy adversarial peer review and Bayesian Nash equilibrium clearing to enforce dominant-strategy incentive compatibility and eliminate sycophancy bias.

## Principle 8: Quality-Diversity MAP-Elites Program Synthesis
- **Concept**: Classical evolutionary search collapses into local minima; maintaining a diverse behavioral archive produces robust programs.
- **Implementation**: Genetic workflow mutation isolates sub-populations into parallel islands and maintains a MAP-Elites grid, producing high-performing and structurally diverse trading rules and execution scripts.
