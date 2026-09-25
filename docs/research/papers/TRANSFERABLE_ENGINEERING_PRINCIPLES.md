# Transferable Engineering Principles Synthesis (500-Paper Corpus)

This document synthesizes actionable, transferable engineering principles extracted across 500 published and arXiv research papers (IDs 1–500), mapping each principle directly to the four core subsystems of the Cognitive Operating System: **AEAN**, **EOS**, **EIOS**, and **ResearchOS**.

---

## Subsystem 1: AEAN (Multi-Agent Swarm & Cognitive Network)

### Principle AEAN-1: Monotonic Value Factorisation & Shapley Credit Assignment
- **Source Papers:** Rashid et al. (2018; 2020), Wang et al. (2020) [IDs 303, 308, 316]
- **Core Concept:** Factorise global swarm team reward $Q_{tot}$ into individual agent utilities $Q_i$ under monotonicity constraints $\frac{\partial Q_{tot}}{\partial Q_i} \ge 0$, using Shapley value decomposition for unbiased multi-agent credit assignment.
- **Target Integration:** `apodex/aean/coordination/hive_mind.py` (HiveMind token bidding and credit allocation).

### Principle AEAN-2: Graph Attention Communication & Targeted Relational Swarm Routing
- **Source Papers:** Jiang & Lu (2018), Das et al. (2019), Kool et al. (2019) [IDs 310, 311, 312]
- **Core Concept:** Dynamically weight message passing between active agents using graph attention weights $\alpha_{ij}$, routing task sub-goals to agents based on real-time capability match and communication bandwidth limits.
- **Target Integration:** `apodex/aean/core.py` and `apodex/aean/engines/paean.py`.

### Principle AEAN-3: Decentralized Tokenomics & Auction Bidding Mechanisms
- **Source Papers:** Cong et al. (2021), Nisan et al. (2007), Hartline & Lucier (2010) [IDs 314, 315, 330]
- **Core Concept:** Align sub-agent incentives using dynamic token bidding markets, where agents bid compute/utility tokens to claim strategy execution sub-tasks based on empirical domain success rates.
- **Target Integration:** `apodex/aean/coordination/hive_mind.py` (`register_research_insight` & token bidding registry).

---

## Subsystem 2: EOS (Entrepreneurial Operating System)

### Principle EOS-1: Bayesian Capital Staging & Real Options Staging
- **Source Papers:** Kerr et al. (2014), Gompers & Lerner (2001), Dixit & Pindyck (1994) [IDs 344, 347, 354]
- **Core Concept:** Treat venture investments as real options staged under market uncertainty, updating capital allocation budgets via Bayesian posterior updating as validated customer traction metrics emerge.
- **Target Integration:** `apodex/ai_eos/intelligence/eos_engine.py` & `apodex/arcs/capital/allocation_engine.py`.

### Principle EOS-2: Unit Economics & Cohort Retention Curve Quantification
- **Source Papers:** Fader et al. (2005), Balfour (2018), Gupta et al. (2004) [IDs 345, 349, 351]
- **Core Concept:** Quantify Product-Market Fit (PMF) through asymptotic cohort retention boundaries $R(t) \to \gamma > 0$ and Customer Lifetime Value to Customer Acquisition Cost ratios ($LTV:CAC \ge 3:1$).
- **Target Integration:** `apodex/ai_eos/intelligence/eos_first_principles.py`.

### Principle EOS-3: Strategic Enterprise Moats & Failure Mode Diagnostics
- **Source Papers:** Helmer (2016), Eisenmann (2021), Porter (1985) [IDs 352, 353, 360]
- **Core Concept:** Continuously evaluate enterprise moat strength across 7 powers (Network Effects, Switching Costs, Scale Economies, Counter-Positioning, Cornered Resource, Process Power, Brand) while monitoring early-stage failure modes.
- **Target Integration:** `apodex/ai_eos/intelligence/eos_engine.py` (`StrategicMoatEngine` & `FailureModeMonitor`).

---

## Subsystem 3: EIOS (Executive Intelligence Kernel)

### Principle EIOS-1: Hierarchical Active Inference & Expected Free Energy Minimization
- **Source Papers:** Friston et al. (2017; 2024), Pezzulo et al. (2018), Parr & Friston (2019) [IDs 371, 374, 375, 500]
- **Core Concept:** Drive executive decision-making by minimizing Expected Free Energy $G(\pi) = - \text{Epistemic Value} - \text{Pragmatic Value}$, balancing information seeking (epistemic curiosity) with goal directed action (pragmatic utility).
- **Target Integration:** `apodex/arcs/kernel/kernel.py` (`EIOSKernel`) & `apodex/arcs/causal/active_inference.py`.

### Principle EIOS-2: Precision-Weighted Uncertainty Propagation & Anomaly Sensing
- **Source Papers:** Parr & Friston (2017), Chandola et al. (2009), Liu et al. (2008) [IDs 373, 376, 392]
- **Core Concept:** Weight sensory anomalies across execution DAG nodes by precision $\Pi = \Sigma^{-1}$, dynamically isolating high-variance operational signals from true systemic execution flaws.
- **Target Integration:** `apodex/arcs/kernel/kernel.py` (`sense_opportunity_anomalies`).

### Principle EIOS-3: Structural Causal Models for Root Cause Diagnostics
- **Source Papers:** Pearl (2009), Peters et al. (2017), Runge et al. (2019) [IDs 379, 389, 458]
- **Core Concept:** Perform do-calculus interventions on structural causal graphs to attribute execution bottlenecks and revenue anomalies to root cause node variables.
- **Target Integration:** `apodex/arcs/causal/causal_engine.py` & `apodex/ai_eos/intelligence/computational_architecture.py`.

---

## Subsystem 4: Research OS (Autonomous Scientific OS)

### Principle ROS-1: Self-Referential Rewriting with AST Linting (STOP / Gödel)
- **Source Papers:** Zelikman et al. (2023), Schmidhuber (1987), Leroy (2009) [IDs 401, 412, 432]
- **Core Concept:** Enable language agents to generate self-referential code rewrites, verifying structural syntax via AST parsing, GRC security rule checking, and sandbox dry-run execution.
- **Target Integration:** `apodex/ai_eos/research/integration.py` (`CodeRewriteEngine`).

### Principle ROS-2: Evolutionary Program Synthesis & MAP-Elites Workflow Mutation
- **Source Papers:** Leang et al. (2024), Mouret & Clune (2015), Stanley et al. (2017) [IDs 402, 429, 430]
- **Core Concept:** Maintain diverse populations of agent program genomes using MAP-Elites quality-diversity search, mutating prompt instructions and numerical parameters to evolve high-performing workflows.
- **Target Integration:** `apodex/ai_eos/research/integration.py` (`GeneticWorkflowOptimizer`).

### Principle ROS-3: Clipped Advantage Estimation & SFT/DPO Preference Compiler
- **Source Papers:** Rafailov et al. (2023; 2024), Ouyang et al. (2022) [IDs 403, 428]
- **Core Concept:** Calculate temporal-difference advantage values $A_t = G_t - V(s)$ over multi-step trajectory traces, compiling chosen vs. rejected execution pairs for direct preference optimization.
- **Target Integration:** `apodex/ai_eos/research/integration.py` (`SFTPreferenceCollector`).

### Principle ROS-4: Budget-Bounded Learnable Routing Gates (Uno-Orchestra)
- **Source Papers:** Wang et al. (2024), Schick et al. (2023) [IDs 404, 420]
- **Core Concept:** Route tasks to specialized sub-agents by evaluating Expected Free Energy scores minus token financial costs, dynamically falling back to low-cost agents when token budgets decay.
- **Target Integration:** `apodex/ai_eos/research/integration.py` (`LearnableRoutingGateDispatcher`).

### Principle ROS-5: Deflated Sharpe Ratio & White's Reality Check Validation
- **Source Papers:** Bailey & Lopez de Prado (2014), White (2000), Stodden et al. (2013) [IDs 416, 417, 418]
- **Core Concept:** Correct for multiple testing selection bias and non-Gaussian return distributions during hypothesis validation using Bonferroni-adjusted alpha levels and Deflated Sharpe Ratios.
- **Target Integration:** `apodex/ai_eos/research/research_os.py` (`execute_experiment_simulation`).
