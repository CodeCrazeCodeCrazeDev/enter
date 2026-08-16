# Phased Implementation Plan & Evaluation Criteria Specification

## Executive Summary

This specification outlines the 5-phase structured roadmap for migrating, evaluating, and operating the Unified Cognitive Operating System. Every implementation phase is gated by strict empirical criteria, statistical power requirements, and zero-regression automated benchmarks.

```
+-----------------------------------------------------------------------------------+
| PHASE 1: SUBSTRATE HARDENING & DECOUPLING                                        |
| - Adapter Freeze & Backward Compatibility Guarantee                               |
| - Dependency Graph Depth Normalization (Depth <= 6, Zero Circular Imports)        |
+-----------------------------------------------------------------------------------+
                                          |
                                Gate: 100% Test Pass Rate (397 tests)
                                          v
+-----------------------------------------------------------------------------------+
| PHASE 2: ACTIVE INFERENCE & CAUSAL CORE INTEGRATION                              |
| - Expected Free Energy (EFE) Decision Engine Integration in AEAN                 |
| - Structural Causal Model (Do-Calculus) Engine Integration in EIOS Kernel        |
+-----------------------------------------------------------------------------------+
                                          |
                                Gate: EFE Calibration Gain > 0.30 & Latency <= 0.005s
                                          v
+-----------------------------------------------------------------------------------+
| PHASE 3: MEMORY COMPACTION & SKILL FLYWHEEL EXPANSION                             |
| - Dual-Tier CMOS Ebbinghaus Pruning Activation in APODEX                          |
| - Skill Registry Pre-population & Flywheel Runner Benchmarking                    |
+-----------------------------------------------------------------------------------+
                                          |
                                Gate: Context Token Bloat Reduction >= 50%
                                          v
+-----------------------------------------------------------------------------------+
| PHASE 4: AUTONOMOUS RESEARCH & HYPOTHESIS TESTING                                 |
| - Research OS 200-Paper Knowledge Base Ingestion Engine                         |
| - Holm-Bonferroni Hypothesis Gating & Multi-Seed Trial Execution                  |
+-----------------------------------------------------------------------------------+
                                          |
                                Gate: Family-wise Error Rate alpha <= 0.05
                                          v
+-----------------------------------------------------------------------------------+
| PHASE 5: ENTREPRENEURIAL BUSINESS FLYWHEELS & LIVE DEPLOYMENT                    |
| - 13 Strategic Business Loops Activation                                          |
| - Continuous Evolution & Self-Improvement Governance Loop                         |
+-----------------------------------------------------------------------------------+
                                          |
                                Gate: Positive Simulated Portfolio ROI & Zero Safety Violations
                                          v
```

---

## 1. Detailed Phase Specifications & Objective Gates

### Phase 1: Substrate Hardening & Decoupling
- **Scope**: Freeze legacy adapters (`agent_harness`), eliminate circular dependencies, and establish strict package boundary limits.
- **Key Modules**: `agent_harness/*`, `scripts/validate_dependencies.py`.
- **Objective Evaluation Gate**:
  - `PYTHONPATH=.:AgentHarness pytest` MUST pass 100% of unit and integration tests (397/397 passing).
  - Maximum package import depth MUST be $\le 6$.
  - Zero circular imports detected by static dependency analyzer.

### Phase 2: Active Inference & Causal Core Integration
- **Scope**: Integrate Expected Free Energy ($G(\pi)$) policy selection into AEAN HiveMind and Pearl Do-Calculus causal interventions into EIOS Kernel.
- **Key Modules**: `apodex/aean/coordination/hive_mind.py`, `apodex/arcs/kernel/kernel.py`.
- **Objective Evaluation Gate**:
  - Active Inference policy calibration accuracy MUST improve by $\ge +0.30$ KL-divergence score over baseline heuristic planners.
  - Causal Do-Calculus adjustment MUST reduce budget overestimation error by $\ge 10\%$.
  - Single-step decision latency MUST remain $\le 0.005\text{s}$.

### Phase 3: Memory Compaction & Skill Flywheel Expansion
- **Scope**: Activate non-linear Ebbinghaus decay pruning ($R(t) = \exp(-t/S)$) in APODEX CMOS memory and pre-populate 60 strategic skills in `SkillRegistry`.
- **Key Modules**: `apodex/memory/cmos/cmos_engine.py`, `apodex/skills/registry.py`.
- **Objective Evaluation Gate**:
  - Memory compaction MUST reduce active context token footprint by $\ge 50.0\%$.
  - Memory retrieval recall for high-utility nodes MUST maintain $\ge 98.0\%$ accuracy.
  - Skill execution success rate across flywheel protocols MUST reach $100\%$.

### Phase 4: Autonomous Research & Hypothesis Testing
- **Scope**: Operationalize Research OS 200-paper knowledge engine, dynamic literature review, and Holm-Bonferroni statistical trial gating.
- **Key Modules**: `apodex/ai_eos/research/research_os.py`, `compile_research_db.py`.
- **Objective Evaluation Gate**:
  - Family-wise error rate ($\alpha$) MUST be bounded at $\le 0.05$ across all hypothesis trials.
  - Provenance traceability MUST be $100\%$ mapped from paper -> principle -> architectural change -> benchmark result.
  - Zero duplicate paper records or DOI overlaps across the 200-paper database.

### Phase 5: Entrepreneurial Business Flywheels & Self-Improvement
- **Scope**: Execute 13 strategic business loops under EIOS Kernel, multi-agent swarm debate, capital allocation, and self-referential code evolution.
- **Key Modules**: `apodex/ai_eos/intelligence/computational_architecture.py`, `apodex/aean/coordination/hive_mind.py`.
- **Objective Evaluation Gate**:
  - Swarm debate protocol MUST eliminate compliance bias ($0\%$ sycophancy collapse).
  - Portfolio risk gates MUST halt execution when drawdown exceeds threshold ($\text{Max Drawdown} \le 15\%$).
  - Self-improvement rewrites MUST achieve statistically significant improvement ($p < 0.05$ via Welch's t-test) before promotion.

---

## 2. Statistical Controls & Benchmarking Guidelines

All performance evaluations MUST adhere to the following statistical protocols:

1. **Multi-Seed Testing**: Every benchmark trial MUST be executed across a minimum of $N = 10$ distinct random seeds.
2. **Welch's T-Test Verification**: Hypothesis tests comparing candidate changes against baseline MUST evaluate Welch's t-statistic:
   $$t = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$
   Candidate changes are only eligible for promotion if $p < 0.05$ and effect size (Cohen's $d$) $> 0.5$.
3. **Automated Rollback Trigger**: If a promoted change degrades primary benchmark metrics by $> 2.0\%$ in live execution, APODEX Rollback Manager MUST automatically restore state to the previous checkpoint.
