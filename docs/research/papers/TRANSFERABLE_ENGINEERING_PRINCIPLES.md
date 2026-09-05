# Transferable Engineering Principles (Corpus IDs 301–500)

## Executive Summary
This document defines the core transferable engineering principles extracted from the 200-paper quantitative research corpus (IDs 301–500). Each principle is formally derived from peer-reviewed publications and mapped directly into target subsystems within the unified 4-layer cognitive architecture:
- **Layer 1: Research OS** (`apodex/ai_eos/research/` & `apodex/research_os/`)
- **Layer 2: EIOS Kernel & EOS Decision Engine** (`apodex/arcs/kernel/` & `apodex/ai_eos/intelligence/`)
- **Layer 3: AEAN Cognitive Intelligence** (`apodex/aean/` & `apodex/cognition/`)
- **Layer 4: APODEX Platform & WorldModel** (`apodex/world_model/` & `apodex/skills/`)

---

## Synthesis of Transferable Principles

### Principle 1: Non-Gaussian Hawkes Process Volatility Bounds
- **Source Papers:** Papers 461, 463, 465, 469, 471, 473, 477, 479, 481, 483, 489, 491, 499
- **Core Scientific Insight:** High-frequency mutation and trade traces exhibit non-Gaussian heavy-tailed jump dynamics. Standard linear intensity models underestimate tail risk during volatile code rewrite cascades.
- **Target Component:** `CodeRewriteEngine` (`apodex/ai_eos/research/integration.py`)
- **Engineering Implementation:** Incorporates non-Gaussian Hawkes stability checks during AST syntax validation and dry-run execution. Bounds maximum mutations per file dynamically based on observed AST mutation velocity and non-Gaussian variance.

### Principle 2: Causal Do-Calculus Interventions in Active Inference Routing
- **Source Papers:** Papers 462, 464, 466, 468, 470, 472, 474, 476, 478, 480, 482, 484, 486, 488, 490, 492, 494, 496, 498, 500
- **Core Scientific Insight:** Epistemic curiosity metrics in multi-agent routing gates can suffer from spurious correlations with token costs. Pearl & Bareinboim's Causal Do-Calculus ($P(Y | do(X))$) isolates true epistemic value from cost confounding.
- **Target Component:** `LearnableRoutingGateDispatcher` (`apodex/ai_eos/research/integration.py`)
- **Engineering Implementation:** Implements explicit do-calculus intervention score calculations ($EFE_{causal} = P(Y | do(agent)) - Cost Penalty$), guaranteeing cost-optimal agent selection without confounding epistemic surprise.

### Principle 3: Edit Trajectory Distance Penalization in Direct Preference Optimization
- **Source Papers:** Papers 381, 384, 386, 390, 393, 396, 398, 402, 404, 407, 410, 413, 417, 420
- **Core Scientific Insight:** When collecting preference pairs ($y_{chosen}$ vs $y_{rejected}$) over agent execution traces, unconstrained advantage estimation rewards bloated edit paths.
- **Target Component:** `SFTPreferenceCollector` (`apodex/ai_eos/research/integration.py`)
- **Engineering Implementation:** Penalizes trajectory advantage scores proportionally to edit path distance: $A_{step\_penalized} = A_t - \lambda \cdot ||\Delta action\_path||_2$, producing concise, high-efficiency chosen trajectories for DPO fine-tuning.

### Principle 4: Island MAP-Elites with Dynamic Migration Gates
- **Source Papers:** Papers 421, 422, 423, 425, 427, 430, 431, 434, 439, 444, 447, 451, 455, 460
- **Core Scientific Insight:** Single-population genetic optimizers plateau quickly due to premature convergence in prompt space. Island topologies with fitness-variance gated migration preserve diversity across quality-diversity archives.
- **Target Component:** `GeneticWorkflowOptimizer` (`apodex/ai_eos/research/integration.py`)
- **Engineering Implementation:** Implements island population structures with cross-island migration gates activated when local island fitness variance falls below threshold $\sigma^2_{min}$.

### Principle 5: Sycophancy-Robust Multi-Turn Deliberation & Active Inference Sensing
- **Source Papers:** Papers 301–340, 341–380
- **Core Scientific Insight:** Multi-agent panels under consensus pressure tend toward sycophantic alignment. Independent dual-agent verification combined with Expected Free Energy (EFE) minimization prevents compliance bias and aligns active hypotheses.
- **Target Components:** `ResearchOS` (`apodex/ai_eos/research/research_os.py`), `EIOSKernel` (`apodex/arcs/kernel/kernel.py`), `EOSEngine` (`apodex/ai_eos/intelligence/eos_engine.py`), and `HiveMind` (`apodex/aean/coordination/hive_mind.py`)
- **Engineering Implementation:**
  - `ResearchOS.conduct_literature_review`: Synthesizes literature and queries registered 200-paper principles.
  - `EIOSKernel`: Ingests scientific hypotheses from Research OS to sense opportunity anomalies via active inference EFE.
  - `EOSEngine`: Ingests validated research hypotheses into its active hypothesis engine for business execution decisions.
