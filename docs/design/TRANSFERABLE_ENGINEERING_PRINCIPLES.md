# Transferable Engineering Principles for Autonomous Research OS

This document outlines the core engineering principles extracted from state-of-the-art research (Papers 1–400) and synthesized inside the evolved `AlphaAlgo` framework.

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

## Principles Extracted from Papers 301–400 Corpus

### Principle 5: Structural Causal SCM Guard & Continuous DAG Optimization
- **Source Papers**: Papers 301–315 (Pearl 2000, Peters et al. 2017, Zheng et al. 2018 - *DAGs with NO TEARS*)
- **Concept**: Systemic decisions and belief updates in the World Model must be structured as a directed acyclic graph (DAG) enforced with continuous acyclicity constraints $h(W) = \text{Tr}(e^{W \circ W}) - d = 0$.
- **Target Subsystem**: `APODEX World Model` & `ActiveInferencePlanner`.
- **Implementation**: Implemented in `AdvancedCausalEngine` and `WorldModel` to prevent cyclic causal feedback loops and evaluate counterfactual interventions $P(Y \mid \text{do}(X))$.

### Principle 6: Multi-Scale Active Inference with Dynamic Expected Free Energy (EFE) Routing
- **Source Papers**: Papers 316–330 (Friston et al. 2016, Parr & Friston 2017, Millidge et al. 2022)
- **Concept**: Balance epistemic curiosity (information gain / KL divergence from prior) and pragmatic utility (expected log loss minimization) dynamically across hierarchical temporal horizons.
- **Target Subsystem**: `Research OS` & `LearnableRoutingGateDispatcher`.
- **Implementation**: The EFE dispatcher routes tasks to specialized agents by minimizing expected free energy $G(\pi) = - \mathbb{E}_{q(o, \theta \mid \pi)}[\ln q(\theta \mid o, \pi) - \ln q(\theta \mid \pi)] - \mathbb{E}_{q(o \mid \pi)}[\ln p(o)]$.

### Principle 7: Hawkes Point Process Non-Gaussian Stability Checks for Code Rewrites
- **Source Papers**: Papers 331–345 (Hawkes 2018, Bacry et al. 2016, Solar-Lezama & Bodik 2018)
- **Concept**: Self-exciting code rewrite proposals in self-evolving loops exhibit non-Gaussian burstiness. AST transformations must be validated against recursive call depth and intensity jump thresholds to prevent runaway infinite recursion.
- **Target Subsystem**: `CodeRewriteEngine` (Research OS & AEAN HiveMind).
- **Implementation**: `CodeRewriteEngine.verify_proposal_ast` checks AST structure specifically within function scopes to bound recursive call depth and prevent non-Gaussian stability breaches.

### Principle 8: Trajectory Edit Path Alignment with Clipped Advantage Margins
- **Source Papers**: Papers 346–360 (Rafailov et al. 2024, Schulman et al. 2017, Zelikman et al. 2024)
- **Concept**: Fine-tune preference collection over sequential execution paths by calculating step-wise advantage margins and clipping advantages $\text{clip}(A_t, -\epsilon, \epsilon)$ to prevent reward scale inflation.
- **Target Subsystem**: `SFTPreferenceCollector` & `AEAN HiveMind`.
- **Implementation**: `SFTPreferenceCollector.collect_trajectory_preference` applies clipped advantage scaling over multi-step trajectory edit paths.

### Principle 9: Island-Based MAP-Elites Diversity Archives with Migration Gates
- **Source Papers**: Papers 361–375 (Pugh et al. 2016, Mouret & Clune 2015, Whitley et al. 1999)
- **Concept**: Maintain high-performing, diverse algorithmic workflow candidates across isolated island populations. Migrate top candidates across islands using quality-diversity elites archives and adaptive parameter mutation gates.
- **Target Subsystem**: `GeneticWorkflowOptimizer` (Research OS & AEAN HiveMind).
- **Implementation**: `GeneticWorkflowOptimizer` manages island populations with MAP-Elites archives, instant elite sorting on insertion, and type-checked mutation gates.

### Principle 10: Sycophancy-Proof Token Bidding for Multi-Agent Swarm Consensus
- **Source Papers**: Papers 376–390 (Gerkey & Matarić 2004, Conitzer & Perez 2024, Sandholm & Varian 2017)
- **Concept**: In multi-agent task allocation and deliberation, agents submit token bids proportional to their domain confidence and verifiable track record. Swarm consensus is aggregated using VCG-inspired mechanisms to suppress sycophancy and collusive bias.
- **Target Subsystem**: `AEAN HiveMind` (`TaskBiddingRegistry`).
- **Implementation**: The HiveMind auction engine evaluates agent bids against historical accuracy to assign execution tasks to high-reputation sub-agents.
