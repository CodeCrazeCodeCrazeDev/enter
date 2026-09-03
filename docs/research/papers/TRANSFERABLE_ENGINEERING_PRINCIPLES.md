# Transferable Engineering Principles Across Research Corpus (Papers 1-400)

This document catalogs the core transferable engineering principles extracted across 400 research papers, specifically detailing the 100 new papers (IDs 301 to 400) integrated into AlphaAlgo.

---

## Papers 301-400 Transferable Engineering Principles

### Principle 1: Non-Gaussian Hawkes Process Self-Excitation Stability
- **Source Papers:** Papers 301–320 (e.g., Bacry & Muzy 2014, Chavez-Demoulin et al. 2005)
- **Concept:** Self-referential code rewrites and order-flow mutations undergo exponential self-excitation loops resembling Hawkes point processes. Uncontrolled feedback cascades lead to mutation instabilities.
- **Engine Application:** Integrated into `CodeRewriteEngine.verify_hawkes_stability()` in `apodex/ai_eos/research/integration.py`. Applies a continuous-time spectral radius stability test ($\lambda < 1.0$) to halt volatile code rewrite cascades.

### Principle 2: Island MAP-Elites Quality-Diversity Migration Gating
- **Source Papers:** Papers 381–400 (e.g., Mouret & Clune 2020, Cully & Demiris 2017)
- **Concept:** Genetic search in high-dimensional agent workflows suffers from premature population convergence unless behavioral diversity is explicitly maintained in structured quality-diversity archives.
- **Engine Application:** Integrated into `GeneticWorkflowOptimizer.migrate_island_elites()` in `apodex/ai_eos/research/integration.py`. Uses multi-island MAP-Elites grids with fitness migration gates to preserve niche diversity.

### Principle 3: Trajectory Edit-Path Distance Penalties & Advantage Clipping
- **Source Papers:** Papers 341–360 (e.g., Schulman et al. 2017, Lightman et al. 2023)
- **Concept:** On-policy advantage estimation and DPO preference compilation over agent trajectory traces suffer from path noise and runaway variance on redundant steps.
- **Engine Application:** Integrated into `SFTPreferenceCollector.compile_dpo_preference_pair()` in `apodex/ai_eos/research/integration.py`. Computes edit-path Levenshtein distance penalties and applies advantage clipping ($|A_t| \le A_{max}$) to produce high-signal preference records.

### Principle 4: Causal Do-Calculus Interventions in Epistemic Task Routing
- **Source Papers:** Papers 321–340, 361–380 (e.g., Parr & Friston 2020, Perez & Conitzer 2024)
- **Concept:** Routing tasks purely on historical agent success leads to sycophancy bias and subagent cost overruns under tight financial constraints.
- **Engine Application:** Integrated into `LearnableRoutingGateDispatcher.route_task()` in `apodex/ai_eos/research/integration.py`. Combines Active Inference Expected Free Energy (EFE) with causal do-calculus intervention score updates and strict upper-bound financial budget checks.
