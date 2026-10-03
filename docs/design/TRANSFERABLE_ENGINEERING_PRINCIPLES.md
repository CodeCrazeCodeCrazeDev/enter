# Transferable Engineering Principles for Autonomous Cognitive Operating System

This document outlines the core engineering principles extracted from state-of-the-art research (spanning 500 published and peer-reviewed papers across 5 major corpora) and synthesized inside the APODEX unified cognitive operating system architecture.

---

## Baseline Harness Principles (Principles 1–4)

### Principle 1: Hexagonal Isolation of Strategic Planning
- **Concept**: Never pollute the strategic planning history with task execution outputs.
- **Implementation**: The `StrategicPlanner` compiles a frozen `Roadmap`, while the `TaskExecutor` processes individual steps. Output payloads are validated by a `PlanVerifier` and kept strictly isolated from the planner's memory.

### Principle 2: Multi-Tier Memory Consolidation
- **Concept**: Distinguish short-term context window history from persistent semantic memory.
- **Implementation**: Short-term history is compacted via sliding windows, while structured evidence cards, facts, and beliefs are persisted inside a SQLite semantic memory repository. High-confidence facts are promoted, and low-confidence ones are pruned to satisfy token budgets.

### Principle 3: Model-Collapse Guard via Quality Downsampling
- **Concept**: Automatically prevent self-generated SFT training datasets from causing recursive model degradation.
- **Implementation**: The `TrajectoryDatasetCompiler` tracks the ratio of self-generated vs. real trajectory traces. In strict mode, it raises errors on threshold breach; in relaxed mode, it downsamples self-generated data, keeping only high-scoring traces.

### Principle 4: Two-Level Credit Assignment
- **Concept**: Calculate both global trajectory success and progressive step-level contribution.
- **Implementation**: The `TwoLevelCreditAssignment` engine applies positive reinforcement ($1.0 \times \frac{i}{N}$) for successful steps, and progressive penalties ($-0.2 \times \frac{i}{N}$) for steps leading to failure.

---

## 200-Paper Research Corpus Extracted Engineering Principles (Papers 301–500)

### Principle 5: Closed-Loop Active Inference Hypothesis Validation (Research OS)
- **Target Subsystem**: `Research OS` (`apodex/ai_eos/research/`)
- **Concept**: Scientific hypothesis generation and experimentation must operate as an active inference loop under variational free energy minimization.
- **Implementation**: Registered hypotheses are evaluated against empirical ground truth yields, applying Deflated Sharpe Ratio (DSR) and White's Reality Check (WRC) adjustments to prevent selection bias and false discovery inflation. Validated hypotheses automatically propagate downstream to EIOS, EOS, and AEAN.

### Principle 6: Non-Gaussian Hawkes Point-Process Anomaly Sensing (EIOS Kernel)
- **Target Subsystem**: `EIOS Kernel` (`apodex/arcs/kernel/`)
- **Concept**: Real-time event sensing must model endogenous excitation and jump intensity without assuming Gaussian noise.
- **Implementation**: `EIOSKernel` registers Expected Free Energy (EFE) active inference sensing handlers over event DAGs. It detects point-process excitation spikes and microstructure noise, routing high-uncertainty events to active inference planners.

### Principle 7: First-Principles Entrepreneurial Decision Trees & Capital Allocation (EOS Engine)
- **Target Subsystem**: `EOS Engine` (`apodex/ai_eos/intelligence/`)
- **Concept**: Startup strategy and capital allocation should follow real-options decision trees, validating value hypotheses prior to growth scaling.
- **Implementation**: `EOSEngine` ingests validated research hypotheses, maps them to `OpportunityNode` trees, tracks customer lifecycle metrics (CAC, LTV, payback period), and performs dynamic capital downshifting when tail-risk or runway thresholds are approached.

### Principle 8: Sycophancy-Proof Token Bidding & Budget-Decayed Routing (AEAN HiveMind)
- **Target Subsystem**: `AEAN HiveMind` (`apodex/aean/coordination/`)
- **Concept**: Multi-agent task coordination requires competitive token bidding with sycophancy mitigation and financial budget decay.
- **Implementation**: `HiveMind` registers research insights into token bidding registries. `LearnableRoutingGateDispatcher` routes tasks to sub-agents based on Expected Free Energy (curiosity vs. pragmatic success) while enforcing strict financial budget limits.
