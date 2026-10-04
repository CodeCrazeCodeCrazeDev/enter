# Transferable Engineering Principles for Autonomous Research OS, AEAN, EOS & EIOS

This document outlines the core engineering principles extracted from state-of-the-art research (spanning papers 1–500, with primary focus on the 200-paper corpus IDs 301–500) and synthesized inside the unified cognitive operating system architecture.

---

## Principle 1: Hexagonal Isolation of Strategic Planning
- **Target Subsystem**: Research OS / AgentHarness
- **Concept**: Never pollute strategic planning history with task execution outputs.
- **Implementation**: The `StrategicPlanner` compiles a frozen `Roadmap`, while the `TaskExecutor` processes individual steps. Output payloads are validated by a `PlanVerifier` and kept strictly isolated from the planner's memory.

## Principle 2: Multi-Tier Memory Consolidation
- **Target Subsystem**: APODEX WorldModel / Memory Subsystem
- **Concept**: Distinguish short-term context window history from persistent semantic memory.
- **Implementation**: Short-term history is compacted via sliding windows, while structured evidence cards, facts, and beliefs are persisted inside a semantic memory repository. High-confidence facts are promoted, and low-confidence ones are pruned to satisfy token budgets.

## Principle 3: Model-Collapse Guard via Quality Downsampling
- **Target Subsystem**: Research OS / Alignment Engine
- **Concept**: Automatically prevent self-generated SFT training datasets from causing recursive model degradation.
- **Implementation**: The `TrajectoryDatasetCompiler` tracks the ratio of self-generated vs. real trajectory traces. In strict mode, it raises errors on threshold breach; in relaxed mode, it downsamples self-generated data, keeping only high-scoring traces.

## Principle 4: Two-Level Credit Assignment
- **Target Subsystem**: AEAN / Research OS
- **Concept**: Calculate both global trajectory success and progressive step-level contribution.
- **Implementation**: The `TwoLevelCreditAssignment` engine applies positive reinforcement ($1.0 \times \frac{i}{N}$) for successful steps, and progressive penalties ($-0.2 \times \frac{i}{N}$) for steps leading to failure.

---

## Evolved 200-Paper Corpus Transferable Principles (IDs 301–500)

### Principle 5: Active Inference Expected Free Energy (EFE) Anomaly Sensing
- **Target Subsystem**: EIOS Kernel (`apodex/arcs/kernel/`) & EOS Engine (`apodex/ai_eos/intelligence/`)
- **Papers**: 301–340 (Parr & Friston 2017; Millidge et al. 2020; Da Costa et al. 2022)
- **Concept**: Frame environmental sensing as variational free energy minimization balancing epistemic curiosity ($G_{\text{epistemic}}$) and pragmatic value ($G_{\text{pragmatic}}$).
- **Implementation**: The `EIOSKernel` computes Expected Free Energy over DAG workflow execution anomalies, triggering active sensing policies when epistemic uncertainty exceeds state thresholds.

### Principle 6: VCG Token Auction & Sycophancy-Proof Consensus
- **Target Subsystem**: AEAN Swarm Intelligence & HiveMind (`apodex/aean/coordination/`)
- **Papers**: 341–380 (Shoham & Leyton-Brown 2015; Conitzer & Sandholm 2006; Perez & Conitzer 2023)
- **Concept**: Ensure truthful token bidding in subagent task delegation and prevent sycophantic consensus in multi-agent deliberation networks.
- **Implementation**: The `HiveMind` uses Vickrey-Clarke-Groves (VCG) second-price sealed auctions for task bidding and filters subagent deliberation through adversarial peer-review verification.

### Principle 7: Deflated Sharpe Ratio & White's Reality Check Hypothesis Screening
- **Target Subsystem**: Research OS (`apodex/ai_eos/research/`)
- **Papers**: 381–420 (Wang & Leskovec 2023; Lopez de Prado 2014; White 2000; Gelman & Carlin 2014)
- **Concept**: Correct for multiple-testing selection bias and data leakage in continuous automated hypothesis discovery.
- **Implementation**: `ResearchOS.execute_experiment_simulation` applies Bonferroni-corrected significance thresholds, Deflated Sharpe Ratio (DSR) discounting based on total experiments run, and White's Reality Check for non-Gaussian walk-forward validation.

### Principle 8: Multi-Attribute Strategic Moat & Growth State Machine
- **Target Subsystem**: EOS Engine (`apodex/ai_eos/intelligence/`)
- **Papers**: 421–460 (Porter 1985; Gupta & Lehmann 2003; Blank 2006; Christensen 1997; Teece 2007)
- **Concept**: Formalize enterprise value creation via multi-attribute strategic moat scoring, B2B funnel system dynamics, and company growth phase transitions.
- **Implementation**: `EOSEngine` combines customer retention dynamics (hierarchical gamma-gamma model), go-to-market funnel simulations, and cash runway failure mode diagnostics into real-time opportunity decision trees.

### Principle 9: AST Invariant Self-Referential Code Modification & Sandbox Execution
- **Target Subsystem**: Research OS & Self-Improvement Engine (`apodex/ai_eos/research/integration.py`)
- **Papers**: 461–500 (Romera-Paredes & Real 2023; Engler & Chelf 2001; Lampson 1973; Yuan & Weston 2024)
- **Concept**: Safeguard self-referential code rewrites with static AST linting, GRC security rules checking, dry-run sandbox simulation, and budget-decayed active routing.
- **Implementation**: `CodeRewriteEngine` parses AST proposed snippets for dangerous calls (`eval`, `exec`, `os.system`), executes dry-run simulation in temp sandboxes, and commits modifications only under verified security invariants.
