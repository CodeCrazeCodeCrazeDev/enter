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

## 200-Paper Corpus Extracted Principles (IDs 301–500)

### Principle 5: Non-Gaussian Hawkes Self-Excitation AST Recursion Check (Research OS)
- **Concept**: High-frequency order flow and self-referential code generation exhibit point-process clustering and self-excitation. Unbounded recursive AST modifications risk non-Gaussian explosion.
- **Implementation**: `CodeRewriteEngine.verify_proposal_ast` checks per-function recursion depth specifically rather than total AST name count, preventing false positives on frequent standard library calls while guaranteeing AST safety.

### Principle 6: Island MAP-Elites Migration Gateways (AEAN / Evolutionary Search)
- **Concept**: Population diversity in genetic workflow optimization suffers when elites are inserted without immediate re-sorting or when migration between islands is ungated.
- **Implementation**: `GeneticWorkflowOptimizer` enforces fitness-threshold migration gates between population islands and performs immediate re-sorting upon elite insertion.

### Principle 7: Advantage Margin Clipping in Trajectory Preference Datasets (AEAN / Alignment)
- **Concept**: Extreme advantage differences across multi-step trajectory traces cause gradient explosions in SFT/DPO loss during preference alignment.
- **Implementation**: `SFTPreferenceCollector` clips trajectory advantage margins to a maximum threshold (e.g., `[-10.0, 10.0]`), maintaining stable preference optimization.

### Principle 8: Budget-Decayed Expected Free Energy Task Routing (EIOS / Active Inference)
- **Concept**: Sub-agent task delegation using Expected Free Energy (EFE) must account for depleting financial budgets to prevent catastrophic cost overruns.
- **Implementation**: `LearnableRoutingGateDispatcher` dynamically scales pragmatic and epistemic EFE routing scores based on remaining financial budget ratios.

### Principle 9: Multi-Layer Active Inference State Handoff (EOS / System Bridge)
- **Concept**: Seamlessly connect scientific hypothesis validation with continuous market sensing, multi-agent execution, and causal world model updates.
- **Implementation**: `ResearchToSystemBridge` bridges Layer 1 Research OS hypotheses, Layer 2 EIOS sensing & EOS decisions, Layer 3 AEAN multi-agent execution, and Layer 4 WorldModel belief updates.
