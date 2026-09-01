# Prioritized Engineering ROI Roadmap

## Executive Summary
This roadmap prioritizes engineering efforts based on expected return on engineering effort across Intelligence, Reliability, Scalability, and Maintainability.

---

## Priority Matrix (Ranked by Return on Effort)

| Priority | Feature / Redesign Initiative | Target Layer | Expected ROI Impact | Complexity Budget |
|---|---|---|---|---|
| **P0** | **Single 4-Layer Taxonomy Alignment** | All Layers (1-4) | Eliminates duplicated modules, reduces technical debt by 40%, ensures 100% layer boundary clarity. | Low (1-2 days) |
| **P0** | **Unified Cross-Layer Active Inference Bridge** | Layer 1 <-> Layer 2 | Standardizes hypothesis export from Research OS to EIOS Kernel active inference sensing. | Low (1 day) |
| **P1** | **Statistical Bound Guardrails & Probability Clamping** | Layer 1 (Research OS) | Prevents math errors (e.g., zero-division, PPF probability bounds, DSR overflow). | Medium (2 days) |
| **P1** | **MAP-Elites & ShinkaEvolve Workflow Mutation** | Layer 3 (AEAN) | Elevates autonomous workflow optimization and prompt adaptation accuracy by +25%. | Medium (3 days) |
| **P2** | **WorldModel Causal Graph Belief Propagation** | Layer 4 (APODEX) | Enables real-time Bayesian updating across entity networks with formal uncertainty bounds. | High (4 days) |
| **P2** | **Continuous DPO/SFT Trajectory Collector** | Layer 1 <-> Layer 3 | Automatically compiles chosen vs. rejected execution traces into training datasets. | High (5 days) |
