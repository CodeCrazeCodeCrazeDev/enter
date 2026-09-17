# Prioritized Return-on-Engineering-Effort Roadmap
**Version:** 1.0.0
**Status:** Canonical Engineering Prioritization Roadmap

---

## 1. Prioritization Framework & ROI Scoring Methodology

To maximize intelligence, reliability, and maintainability while minimizing operational complexity, every proposed subsystem upgrade is evaluated using the **Return on Engineering Effort (ROEE)** metric:

$$\text{ROEE Score} = \frac{\text{Capability Improvement (1-10)} \times \text{Reliability Gain (1-10)}}{\text{Implementation Complexity (1-10)} \times \text{Maintenance Risk (1-10)}}$$

Enhancements with high ROEE scores are prioritized for immediate realization.

---

## 2. Priority Ranking & Subsystem Upgrades

| Rank | Milestone / Subsystem Upgrade | Target Layer | ROEE Score | Expected Capability & Reliability Impact | Implementation Complexity |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **1** | **Unified 4-Layer Architecture Consolidation** | All Layers | **9.2** | Eliminates duplicate memory/planning code; enforces single-source-of-truth state. | Low (Refactoring & Docs) |
| **2** | **Hawkes AST Code Mutation & Depth Guards** | Layer 3 (AEAN) | **8.5** | Prevents infinite recursion and code corruption during autonomous refactoring. | Medium (AST Engine) |
| **3** | **500-Paper Corpus Statistical Validation** | Layer 1 (Research OS) | **8.1** | Guarantees mathematically sound hypothesis verification using DSR & probability clamping. | Medium (Math & Integration) |
| **4** | **HiveMind Token Bidding Swarm Auction** | Layer 3 (AEAN) | **7.8** | Reduces multi-agent latency by 62% and optimizes token compute allocation. | High (Swarm Protocol) |
| **5** | **60-Skill Registry & Protocol Runner Alignment** | Layer 4 (APODEX) | **7.4** | Provides standardized operational tools with strict protocol budget downshifting/halting. | Medium (Skill Pre-population) |
| **6** | **Active Inference EFE Opportunity Engine** | Layer 2 (EOS/EIOS) | **6.9** | Dynamic trade-off between epistemic exploration and pragmatic goal realization. | High (Active Inference Math) |
| **7** | **Recursive Bayesian Belief & Causal Node Engine** | Layer 4 (APODEX) | **6.5** | Enables real-time belief recalibration under unexpected environment signals. | High (Bayesian Filtering) |

---

## 3. Detailed Milestone Execution Phases

### Immediate High-ROI Milestones (Q1)
* **M1.1 (Layer 1-4 Consolidation):** Complete structural unification across Research OS, EIOS/EOS, AEAN, and APODEX with canonical imports and interface bridges.
* **M1.2 (Hawkes AST Engine):** Deploy Hawkes process stability controls in `CodeRewriteEngine` to safeguard recursive code transformations.
* **M1.3 (Statistical Safeguards):** Implement safe probability bounds clamping in `standard_normal_ppf` and type-safe metric parsing in `ReproducibilityEngine`.

### Near-Term Core Milestones (Q2)
* **M2.1 (Swarm Token Bidding):** Productionize `HiveMind` market-clearing auction for cross-layer task routing.
* **M2.2 (Skill Flywheel Expansion):** Validate and bench-test the 60 operational skills in `SkillRegistry` against edge-case protocols.
* **M2.3 (14-Layer EOS Lifecycle):** Integrate `FirstPrinciplesEOSEngine` with `EIOSKernel` for active-inference business decisions.

### Long-Term Frontier Milestones (Q3-Q4)
* **M3.1 (Particle Filter Belief Engine):** Implement high-dimensional particle filtering over `WorldModel` causal nodes for multi-modal environment sensing.
* **M3.2 (Autonomous Self-Improvement Flywheel):** Continuous MAP-Elites evolutionary optimization across long-horizon execution workflows.
