# Transferable Engineering Principles Extracted from the 200-Paper (and 300-Paper) Research Corpus

This document catalogs actionable transferable engineering principles extracted from the 200-paper research corpus (`AI_EOS_RESEARCH_DB.yaml`) and the 100-paper AlphaAlgo corpus (`ALPHA_ALGO_100_NEW_RESEARCH.yaml`), systematically mapped to the core subsystems of the Cognitive Operating System: **AEAN**, **EOS**, **EIOS**, and **ResearchOS**.

---

## 1. AEAN (Autonomous Entrepreneurial Agent Network) Principles

### Principle AEAN-1: Graph-of-Thought (GoT) Deliberation & Non-Linear Reasoning
- **Source**: Papers on Tree-of-Thoughts and Graph-of-Thought agentic reasoning (IDs 2, 72, 73).
- **Core Concept**: Replace sequential linear execution loops with directed acyclic graphs (DAGs) of thought nodes. Enable speculative branching, merging, and backtracking over candidate execution trajectories.
- **Target Integration**: `agent_harness/core/runtime/reasoning/got.py` and `apodex/aean/coordination/hive_mind.py`.

### Principle AEAN-2: Sycophancy-Resistant Multi-Agent Swarm Debate
- **Source**: Papers on Multi-Agent Debate and Oversight Games (IDs 76, 78, 82).
- **Core Concept**: Enforce adversarial role assignments (e.g., Red Team / Skeptic vs. Proponent) during swarm deliberation to eliminate compliance bias and agreement traps in agent networks.
- **Target Integration**: `apodex/aean/coordination/hive_mind.py`.

### Principle AEAN-3: Expected Free Energy (EFE) Routing Gate
- **Source**: Papers on Active Inference Planning and Dynamic Routing (IDs 87, 88).
- **Core Concept**: Dispatch complex tasks to sub-agents by evaluating Expected Free Energy $EFE = \text{Pragmatic Value} + \text{Epistemic Value} - \text{Financial Cost}$, balancing historical task mastery with uncertainty reduction.
- **Target Integration**: `apodex/ai_eos/research/integration.py` (`LearnableRoutingGateDispatcher`).

---

## 2. EOS (Entrepreneurial Operating System) Principles

### Principle EOS-1: Multi-Timescale Coupled Growth Loops
- **Source**: Papers on Algorithmic Search and Strategic Optimization (IDs 105, 110, 115).
- **Core Concept**: Couple fast tactical execution loops (hourly telemetry and signal filtering) with slow strategic feedback loops (weekly capital re-allocation and long-term moat validation).
- **Target Integration**: `apodex/ai_eos/intelligence/eos_first_principles.py` and `apodex/ai_eos/intelligence/fourteen_layer_engine.py`.

### Principle EOS-2: Advanced Kelly Criterion Capital Allocation with Volatility Bounds
- **Source**: Quantitative Finance papers (IDs 201, 205, 210).
- **Core Concept**: Allocate capital across active growth opportunities according to fractional Kelly criterion adjusted for empirical variance and extreme tail drawdown risk parameters.
- **Target Integration**: `apodex/ai_eos/intelligence/computational_architecture.py`.

### Principle EOS-3: Counterfactual Opportunity Economics Validation
- **Source**: Papers on Structural Causal Models and Decision Fatigue (IDs 120, 125).
- **Core Concept**: Evaluate opportunity economics by comparing actual revenue return against synthetic counterfactual baselines using do-calculus interventions.
- **Target Integration**: `apodex/ai_eos/intelligence/eos_first_principles.py`.

---

## 3. EIOS (Entrepreneurial Intelligence Operating System) Kernel Principles

### Principle EIOS-1: Active Inference State Estimation & Surprise Minimization
- **Source**: Active Inference and Variational Free Energy papers (IDs 87, 90, 92).
- **Core Concept**: Continuous state sensing and perception via surprise minimization $F = \text{D}_{\text{KL}}(q(\theta) || p(\theta)) - \mathbb{E}_{q}[\log p(y|\theta)]$, dynamically aligning internal world models with environmental observations.
- **Target Integration**: `apodex/arcs/kernel/kernel.py`.

### Principle EIOS-2: Pearl's Do-Calculus Causal Interventions
- **Source**: Causal Reasoning and Intervention papers (IDs 94, 96).
- **Core Concept**: Execute structural interventions $\text{do}(X = x)$ to distinguish genuine causal drivers from spurious observational correlations in operational environments.
- **Target Integration**: `apodex/arcs/kernel/kernel.py`.

---

## 4. ResearchOS Principles

### Principle ResearchOS-1: Self-Referential Code Rewrite with GRC AST Verification
- **Source**: Papers on Self-Evolving Code and Gödel Agent frameworks (IDs 5, 131, 135).
- **Core Concept**: Enable autonomous code generation and inline patching guarded by strict AST parsing, static analysis, and temporary sandbox dry-run execution before committing mutations.
- **Target Integration**: `apodex/ai_eos/research/integration.py` (`CodeRewriteEngine`).

### Principle ResearchOS-2: Genetic Program Synthesis & Island-Based Workflow Mutation
- **Source**: Evolutionary Computation and ShinkaEvolve papers (IDs 140, 142, 145).
- **Core Concept**: Maintain diverse populations of agent workflow prompt templates and hyperparameters, executing MAP-Elites selection and Gaussian/semantic mutation to systematically discover high-fitness execution strategies.
- **Target Integration**: `apodex/ai_eos/research/integration.py` (`GeneticWorkflowOptimizer`).

### Principle ResearchOS-3: Reproducibility & Rigorous Statistical Significance Validation
- **Source**: Empirical Evaluation and Statistical Validation papers (IDs 150, 160, 170).
- **Core Concept**: Mandate Welch's t-test hypothesis verification with clamped probability PPF distributions and zero-division safeguards to validate empirical capability gains before system promotion.
- **Target Integration**: `apodex/research_os/statistical_validation.py` and `apodex/ai_eos/research/experiment_framework.py`.
