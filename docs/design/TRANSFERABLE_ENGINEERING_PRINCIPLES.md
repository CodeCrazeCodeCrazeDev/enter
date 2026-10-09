# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research and synthesized inside the evolved `AgentHarness` and `APODEX` framework.

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

## 200-Paper Research Corpus Extracted Engineering Principles (IDs 301 - 500)

This section synthesizes 200 transferable engineering principles extracted from papers 301 to 500, mapped directly to target system layers.

### 1. AEAN (Autonomous Entrepreneurial Agent Network) Principles
- **Second-Price Compute Token Clearing (Paper 401)**: Implements second-price sealed-bid arbitration in `HiveMind.arbitrate()` so agent clearing scores equal the next-highest bid, ensuring strategyproof token resource allocation.
- **Counterfactual Multi-Agent Credit Assignment (Paper 343)**: Evaluates sub-agent marginal token contribution by calculating expected counterfactual rewards across collaborative tasks.
- **Learnable Routing Gates for Agent Shepherding (Papers 341, 345)**: Routes high-complexity tasks to specialized agent profiles based on Expected Free Energy (EFE) scores while enforcing strict budget decay limits.
- **Stigmergic Token Pheromones (Papers 342, 416)**: Uses decaying token trace markers to attract specialized sub-agents to persistent workflow bottlenecks.
- **Dynamic Budget Downshifting (Paper 415)**: Automatically shifts token budget allocations down when total available compute token reserves drop below 20%.

### 2. EOS (Entrepreneurial Operating System) Principles
- **Real Options Portfolio Balancing (Papers 361, 362)**: Dynamically adjusts allocations between EDV Research (real options exploration) and ROI Venture execution based on real-time market uncertainty.
- **Multi-Factor Moat Quantification (Papers 364, 370)**: Computes composite moat durability scores combining network density, switching costs, brand trust, and cost advantages.
- **Insolvency Hazard Modeling & Failure Modes (Papers 365, 367)**: Evaluates corporate hazard rates from burn multiple, LTV:CAC ratios, and runway length to trigger automated reinvention mandates.
- **Deterministic Company Growth State Machine (Paper 366)**: Enforces milestone gates for venture transitions across Ideation, Product-Market Fit, Scaling, and Maturity.
- **Research Hypothesis Ingestion into Hypothesis Engine (Papers 304, 358)**: Ingests validated research hypotheses into posterior Beta distributions ($a/(a+b)$) for continuous active inference.

### 3. EIOS (Entrepreneurial Intelligence OS Kernel) Principles
- **Active Inference Anomaly Sensing (Papers 421, 428)**: Continuously senses environmental anomalies (z-score breaches in market streams) and converts them into active inference research hypotheses.
- **Deterministic Execution DAGs with Auto-Retry (Papers 371, 442, 443)**: Compiles high-level strategic goals into dependency-bound execution graphs (`ExecutionDAG`) with jittered exponential backoff fault recovery.
- **Hierarchical Variational Free Energy Minimization (Papers 301, 307)**: Tracks Variational Free Energy across organizational layers (Company -> Department -> Action) to minimize total systemic surprise.
- **Stateful Circuit Breakers (Paper 446)**: Halts failing execution nodes before cascading errors propagate across dependent workflow branches.

### 4. Research OS (Autonomous Science Engine) Principles
- **Deflated Sharpe Ratio & Selection Bias Corrections (Papers 381, 468)**: Corrects t-statistics and p-values for selection bias in multi-hypothesis experimental trials.
- **Multi-Field Literature Review Search (Papers 387, 462)**: Synthesizes scientific trends by searching across titles, authors, categories, target subsystems, and extracted principles.
- **AST-Constrained Metaprogramming & Self-Rewrite Guard (Papers 322, 329, 376)**: Enforces static security checks, no dangerous eval/exec calls, and AST recursive depth limits during self-referential code rewrites.
- **Island MAP-Elites Population Sorting (Paper 321)**: Re-sorts genetic genome populations immediately upon elite insertion to preserve top fitness candidates.
- **Cross-Layer Active Inference State Handoffs (Papers 480, 482, 500)**: Coordinates closed-loop state transitions between Research OS hypotheses, EIOS sensing, EOS decision trees, AEAN token bidding, and WorldModel belief updates.
