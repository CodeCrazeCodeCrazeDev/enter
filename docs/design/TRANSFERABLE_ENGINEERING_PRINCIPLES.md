# Transferable Engineering Principles for Autonomous Research & Cognitive Operating Systems

This document synthesizes core transferable engineering principles extracted across 500 published research papers (IDs 1–500) and outlines their target subsystem mappings across **AEAN**, **EOS**, **EIOS**, and **Research OS**.

---

## 1. Subsystem Mapping & Conceptual Taxonomy

| Subsystem | Core Role in Unified Architecture | Primary Extracted Principles |
|---|---|---|
| **Research OS (L1)** | Scientific Hypothesis Generation, AST Rewriting, Statistical Validation | Self-Referential AST Mutation under Hawkes Non-Gaussian Bounds, Deflated Sharpe Ratio (DSR) & White's Reality Check (WRC), Literature Review Principle Search |
| **EIOS Kernel (L2)** | Active Inference Sensing, Task Execution Kernel, EFE DAG Scheduler | Active Inference Sensing via Expected Free Energy ($G(\pi)$), Precision-Weighted Anomaly Detection, Real-time Opportunity State Handoffs |
| **EOS Engine (L2/L4)** | Entrepreneurial Decision Engine, Capital Allocation, State Machine | Coupled Business Loops, Growth Stage Classification, Causal Moat Graph Reasoning, Unit Economics Free Energy Optimization |
| **AEAN (L3)** | Adaptive Autonomous Engineering Agent Network, Swarm Coordination | Swarm Token Bidding, MAP-Elites Island Migration Gates, Clipped Trajectory Advantage Margins (DPO), Shepherd Routing |

---

## 2. Core Extracted Principles (500-Paper Corpus)

### Principle 1: Hexagonal Isolation of Strategic Planning
- **Source Papers**: Attias (2003), Jennings & Wooldridge (1998)
- **Target Subsystem**: Research OS / AEAN
- **Concept**: Never pollute strategic planning history with execution outputs.
- **Implementation**: The `StrategicPlanner` compiles a frozen `Roadmap`, while the `TaskExecutor` processes individual steps. Output payloads are validated by a `PlanVerifier` and kept strictly isolated from planner memory.

### Principle 2: Multi-Tier Memory Consolidation
- **Source Papers**: Friston et al. (2017), Blei et al. (2003)
- **Target Subsystem**: Research OS / EIOS
- **Concept**: Distinguish short-term context window history from persistent semantic memory.
- **Implementation**: Short-term history is compacted via sliding windows, while structured evidence cards, facts, and beliefs are persisted inside a SQLite semantic memory repository. High-confidence facts are promoted, and low-confidence ones are pruned to satisfy token budgets.

### Principle 3: Model-Collapse Guard via Quality Downsampling
- **Source Papers**: Rafailov et al. (2023), Lambert et al. (2024)
- **Target Subsystem**: Research OS / AEAN
- **Concept**: Prevent self-generated training datasets from causing recursive model degradation.
- **Implementation**: Track the ratio of self-generated vs. real trajectory traces. Downsample self-generated data in relaxed mode or raise errors in strict mode when threshold is breached.

### Principle 4: Dynamic Swarm Token Bidding
- **Source Papers**: Cramton et al. (2006), Sandholm & Suri (2003), Smith (1980)
- **Target Subsystem**: AEAN HiveMind
- **Concept**: Resource allocation and task priority assignment via competitive token auctions among specialized agents.
- **Implementation**: Agents submit bids containing agent ID, token offer, and execution priority. High-priority tasks are awarded to the highest bidding agent while maintaining token budget constraints.

### Principle 5: Active Inference Sensing via Expected Free Energy
- **Source Papers**: Friston (2010), Parr & Friston (2019), Tschantz et al. (2020)
- **Target Subsystem**: EIOS Kernel
- **Concept**: Minimization of Expected Free Energy ($G(\pi) = \text{Epistemic Risk} + \text{Pragmatic Cost}$) drives continuous opportunity sensing and task DAG compilation.
- **Implementation**: Compute EFE for sensing signals; trigger opportunity anomalies when EFE exceeds threshold $\gamma_{efe} = 0.65$.

### Principle 6: Island MAP-Elites Migration Gates
- **Source Papers**: Mouret & Clune (2015), Pugh et al. (2016), Cantu-Paz (2000)
- **Target Subsystem**: AEAN / Research OS Workflow Evolution
- **Concept**: Quality diversity optimization via structured grid archives and fitness-sorted island migration gates.
- **Implementation**: Maintain population islands with MAP-Elites grids. Migrate elite genomes between islands only when fitness exceeds target threshold percentile.

### Principle 7: Clipped Trajectory Advantage Margins for DPO
- **Source Papers**: Peng et al. (2020), Rafailov et al. (2023), Shao & Peng (2025)
- **Target Subsystem**: Research OS / AEAN Preference Collection
- **Concept**: Prevent scale inflation in Direct Preference Optimization (DPO) training pairs by clipping trajectory advantage margins $[\Delta_{min}, \Delta_{max}]$.
- **Implementation**: Clamp advantage margin $\Delta = A_{\text{chosen}} - A_{\text{rejected}}$ between $-5.0$ and $+5.0$ before synthesizing chosen/rejected DPO dataset pairs.

### Principle 8: Non-Gaussian Hawkes AST Recursion Bounds
- **Source Papers**: Bacry et al. (2013), Cont & Stoikov (2011), Hawkes (1971)
- **Target Subsystem**: Research OS Code Rewrite Engine
- **Concept**: Self-exciting point processes model recursive function call intensity to detect non-Gaussian execution instability in AST rewrites.
- **Implementation**: Track function recursion depth within AST definitions and enforce branching ratio $\eta = \frac{\alpha}{\mu} < 1.0$ to guarantee stability.

### Principle 9: 14-Layer Computational Architecture & State Handoffs
- **Source Papers**: Thiel (2014), Blank (2006), Coase (1937), Zheng & Wu (2026)
- **Target Subsystem**: EOS Engine / Unified Operating System
- **Concept**: First-principles multi-layer state transitions from hypothesis validation (L1) to active sensing (L2), swarm bidding (L3), and world model entity updates (L4).
- **Implementation**: `ResearchToSystemBridge` coordinates active inference state handoffs across all layers.
