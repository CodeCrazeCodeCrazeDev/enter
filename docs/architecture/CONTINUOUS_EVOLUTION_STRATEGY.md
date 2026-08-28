# Continuous Evolution Strategy & Governance Framework

## 1. Dual-Loop Self-Improvement Architecture

The unified Cognitive Operating System continuously learns and adapts through a closed dual-loop meta-system that prevents performance degradation while driving self-improvement.

```
                          +-----------------------------------+
                          |     User & Session Execution      |
                          +-----------------+-----------------+
                                            |
                                            v
                          +-----------------+-----------------+
                          |  Execution Trajectory Recorder   |
                          +-----------------+-----------------+
                                            |
                    +-----------------------+-----------------------+
                    |                                               |
                    v                                               v
+---------------------------------------+       +---------------------------------------+
| SHORT-TERM HARNESS EVOLUTION LOOP     |       | LONG-TERM RESEARCH TRAINING LOOP      |
|                                       |       |                                       |
| - Fast-loop prompt optimization       |       | - Trajectory advantage estimation     |
| - Scaffolding & workflow tuning       |       | - SFT / DPO dataset compilation       |
| - TextGrad / EvoPrompt mutations      |       | - Bounded model fine-tuning           |
| - Real-time error patch generation    |       | - Candidate model weight promotion    |
+---------------------------------------+       +---------------------------------------+
                    |                                               |
                    v                                               v
+---------------------------------------------------------------------------------------+
|                       EXPERIENCE DATABASE & COGNITION BASE                            |
|  - Consolidated Episodic Memory    - SFT Trajectory Archives                          |
|  - Validated Fact Graph            - Blacklisted Prompt Mutations                      |
+---------------------------------------------------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                    TIERED GOVERNANCE & IMMUTABLE SAFETY CORE                          |
|  - Tier 1: Auto-Approved Prompt Tweaks                                                |
|  - Tier 2: Shadow Mode Tool & Workflow Rewrites                                       |
|  - Tier 3: PR + Benchmark Approval for Model Weights                                  |
|  - Tier 4: Cryptographically Signed Tenancy & Security Policies                       |
+---------------------------------------------------------------------------------------+
```

---

## 2. On-Policy Advantage Estimation & DPO Preference Collection

### 2.1 Advantage Computation
During multi-step task execution, trajectory steps are recorded into `SFTPreferenceCollector` (`apodex/ai_eos/research/integration.py`). Temporal-difference advantage values are calculated as:

$$A_t = G_t - V(s_t) = \sum_{j=0}^{T-t} \gamma^j r_{t+j} - \hat{E}[r]$$

### 2.2 SFT / DPO Trajectory Synthesis
When alternative execution paths are explored for the same prompt goal:
1. Cumulative trajectory advantages $\sum A_t^{(A)}$ and $\sum A_t^{(B)}$ are compared.
2. The path yielding higher net advantage is designated as the **Chosen Response**, while the alternative is marked as the **Rejected Response**.
3. Trajectory pairs are saved into JSONL preference datasets formatted for direct Direct Preference Optimization (DPO) fine-tuning.

---

## 3. Tiered Governance & Safety Protection

To guarantee institutional-grade reliability, all automated mutations are regulated by a four-tier approval system:

```
+--------+------------------------------------+------------------------------------+
| Tier   | Change Category                    | Authorization & Validation Requirement|
+--------+------------------------------------+------------------------------------+
| Tier 1 | Prompt text & instruction tweaks   | Auto-approved if benchmark score >= 0|
| Tier 2 | Tool schemas & workflow routing    | Shadow mode validation (10 runs)   |
| Tier 3 | Model weights & fine-tuning        | Automated benchmark PR + human review|
| Tier 4 | Tenancy & immutable security rules | Cryptographically signed manual sign-off|
+--------+------------------------------------+------------------------------------+
```

---

## 4. Anti-Regression & Continuous Validation Guards

1. **Automated Regression Test Suite**: Every proposed prompt or workflow update must run against the full 397-test suite. Any assertion failure triggers an immediate automatic rollback.
2. **One-Click Rollback & Blacklisting**: If user satisfaction drops or runtime errors spike post-deployment, `RollbackManager` restores the previous verified checkpoint and adds the mutated prompt variant to an immutable blacklist.
3. **Multi-Objective Cost Balance**: Updates are scored via Personal Evolution Profiles (PEP) to ensure quality gains do not violate user token or latency constraints ($S(M) = w_q Q - w_t T - w_l L + w_s Sat$).
