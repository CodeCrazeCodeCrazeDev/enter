# Prioritized ROI Roadmap

## Executive Summary

This roadmap prioritizes system engineering initiatives based on Expected Return on Engineering Effort (ROEE), defined as:

$$\text{ROEE} = \frac{\Delta \text{Capability} + \Delta \text{Reliability} + \Delta \text{Maintainability}}{\text{Engineering Cost} \times \text{Architectural Complexity}}$$

All technical initiatives are ranked into four phased execution waves to maximize near-term stability while enabling long-horizon autonomous intelligence.

---

## Phased Implementation Roadmap

```
+-----------------------------------------------------------------------------------+
| PHASE 1: CORE UNIFICATION & ANTI-DUPLICATION (Immediate Impact / High ROEE)       |
| - Unified 4-layer taxonomy (Research OS -> EIOS/EOS -> AEAN -> APODEX)            |
| - Capability ownership matrix enforcement & legacy adapter consolidation          |
| - Pydantic V2 migration & timezone-aware UTC datetime standardisation             |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| PHASE 2: CROSS-LAYER ACTIVE INFERENCE HANDOFFS (High Capability / Med ROEE)        |
| - Unified state bridge (`ResearchToSystemBridge`) implementation                   |
| - Research OS hypothesis -> EIOS Kernel active inference sensing                  |
| - EIOS DAG tasks -> AEAN HiveMind token bidding & swarm allocation                |
| - Swarm execution -> APODEX WorldModel Bayesian belief updates                    |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| PHASE 3: SELF-IMPROVEMENT & CONTINUOUS LEARNING FLYWHEEL (High Intelligence / Med)|
| - Non-Gaussian Hawkes recursive call depth checks in AST patch verification       |
| - Island MAP-Elites migration gates with instant re-sorting                      |
| - Learnable routing gate dispatcher with budget-decayed task allocation           |
| - Clipped trajectory advantage margin in SFT preference feedback                  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| PHASE 4: AUTONOMOUS AI ENTREPRENEURSHIP & INSTITUTIONAL SCALING (Max Autonomy)    |
| - Full 14-layer computational architecture engine operationalization               |
| - End-to-end autonomous business sensing, product generation, and GTM simulation    |
| - Continuous 600+ paper research corpus extraction & automated integration        |
+-----------------------------------------------------------------------------------+
```

---

## Detailed Milestone Breakdown

| Phase | Priority Initiative | Primary Subsystem | Expected Impact | ROEE Score |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | Formalize 4-Layer Spec & Ownership Matrix | Architecture Docs | Eliminates architectural duplication and circular dependencies. | **9.8 / 10** |
| **Phase 1** | Resolve Deprecations & UTC Datetime Standardisation | System-wide (`apodex/`) | Eliminates runtime warnings and prevents naive/aware comparison crashes. | **9.5 / 10** |
| **Phase 2** | Implement `ResearchToSystemBridge` | `apodex/ai_eos/research/` | Seamless active inference state handoff across scientific research & business logic. | **9.2 / 10** |
| **Phase 2** | Connect Research Insights to HiveMind Bidding | `apodex/aean/coordination/` | Direct translation of research breakthroughs into agent execution capability bids. | **8.9 / 10** |
| **Phase 3** | Enhance AST Verification with Hawkes Recursive Depth | `apodex/ai_eos/research/` | Prevents infinite recursion and code corruption during autonomous patching. | **8.7 / 10** |
| **Phase 3** | Safe Probability Bounds & DSR Edge-Case Safeguards | `apodex/research_os/` | Guarantees statistical validity during hypothesis testing. | **8.5 / 10** |
| **Phase 4** | 14-Layer Computational Architecture Engine | `apodex/ai_eos/intelligence/` | Realizes end-to-end autonomous entrepreneurship from reality to meta-learning. | **8.1 / 10** |
| **Phase 4** | Unified 5-Layer End-to-End Integration Suite | `tests/integration/` | End-to-end verification across research, sensing, swarms, and world modeling. | **8.0 / 10** |
