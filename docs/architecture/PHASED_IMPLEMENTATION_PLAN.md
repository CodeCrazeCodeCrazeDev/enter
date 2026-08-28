# Phased Implementation Plan & Objective Evaluation Criteria

## 1. Multi-Phase Roadmap Overview

The transformation of Research OS, EIOS, EOS, AEAN, and APODEX into a unified cognitive operating system is executed across four structured phases. Each phase defines objective success criteria, verification benchmarks, and complexity budgets.

```
+-----------------------------------------------------------------------------------+
| PHASE 1: Subsystem Unification & Authority Model Alignment                        |
|  - Eliminate duplicated capabilities across L1-L4.                                |
|  - Enforce single authority ownership via CAPABILITY_OWNERSHIP_MATRIX.md.          |
|  - Verify 100% backward compatibility via AgentHarness adapter layer.             |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
| PHASE 2: Scientific Research & Active Inference Integration                      |
|  - Deploy ResearchToSystemBridge for L1 -> L2 hypothesis transfer.                |
|  - Implement EFE Active Inference sensing in EIOS Kernel.                        |
|  - Embed 300-paper corpus principles into dynamic literature queries.              |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
| PHASE 3: Cognitive Memory & Swarm Optimization                                     |
|  - Operationalize CMOS / EMG multi-tier memory consolidation.                      |
|  - Deploy Graph-of-Thought (GoT) multi-agent swarm planners.                       |
|  - Validate Skill Flywheel auto-invention and trend skill decay.                  |
+-----------------------------------------------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
| PHASE 4: Autonomous Self-Improvement & Institutional Governance                    |
|  - Activate dual-loop self-improvement (Short-Term Harness + Long-Term Research).  |
|  - Compile SFT/DPO preference trajectory datasets.                                |
|  - Enforce Tiered Immutable Safety Core and multi-objective PEP cost routing.     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Phase Breakdown and Objective Verification Criteria

### Phase 1: Subsystem Unification & Authority Model Alignment
* **Deliverables**: Single Authority Ownership Matrix, Unified Architecture Spec, Unified Dependency Graph.
* **Objective Verification Criteria**:
  1. All legacy test suites pass with zero import errors (`PYTHONPATH=.:AgentHarness python3 -m pytest -q --import-mode=importlib`).
  2. Zero capability duplication confirmed by architectural static analysis.
* **Pass Threshold**: 100% test pass rate across 390+ unit and integration tests.

### Phase 2: Scientific Research & Active Inference Integration
* **Deliverables**: `ResearchToSystemBridge`, `EIOSKernel` EFE active inference sensing, statistical CDF/DSR mathematical protection.
* **Objective Verification Criteria**:
  1. Research hypotheses successfully exported to EIOS kernel and promoted to EOS.
  2. Active Inference EFE KL-divergence score exceeds baseline by $> 30\%$.
  3. Mathematical edge cases (DSR zero-division, PPF probability bounds) handled gracefully without floating point exceptions.
* **Pass Threshold**: Verified via `tests/research_os/test_alpha_algo_100_integration.py` and `tests/ai_eos/test_research_integration.py`.

### Phase 3: Cognitive Memory & Swarm Optimization
* **Deliverables**: Multi-Tier CMOS Memory, Graph-of-Thought (GoT) Planner, Skill Registry Flywheel.
* **Objective Verification Criteria**:
  1. Memory retrieval accuracy across 50-step execution histories $> 95\%$.
  2. GoT branching and pruning reduces redundant execution paths by $> 25\%$.
  3. Skill flywheel auto-populates strategic/operational skills and filters decayed signals after 7 days.
* **Pass Threshold**: Verified via `tests/world_model/test_skills_flywheel.py` and `tests/cognition/test_autonomous_institution.py`.

### Phase 4: Autonomous Self-Improvement & Governance
* **Deliverables**: Personal Evolution Profiles (PEP), Tiered Approval Governance, SFT/DPO Preference Dataset Collector.
* **Objective Verification Criteria**:
  1. DPO preference collector correctly compiles chosen/rejected execution trajectories based on computed advantage.
  2. Tier 4 safety rules veto unauthorized file modifications in shadow mode.
  3. Zero regressions on baseline performance benchmarks post-evolution.
* **Pass Threshold**: Verified via end-to-end integration test suite `tests/integration/test_cognitive_os_subsystems.py`.
