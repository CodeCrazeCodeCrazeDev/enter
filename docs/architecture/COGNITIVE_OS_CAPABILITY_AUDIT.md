# Cognitive OS Phase 1 — First-Principles Capability Audit & Ownership Matrix

This document provides a systematic first-principles capabilities audit of the Autonomous Economic Agent Network (AEAN) when built completely from scratch today, and contrasts those ideal capabilities against the existing repository components. It maps boundaries and establishes a singular, non-overlapping ownership matrix.

---

## 1. First-Principles Capabilities Audit Matrix

We map every capability needed by a world-class autonomous research and entrepreneurial intelligence. We contrast these requirements against the active file structures across AEAN, EIOS, EOS, APODEX, and Research OS.

| Capability ID | Functional Capability Area | Ideal First-Principles Expectation | Current Repository Status | Active Owner Module / File | Gap Analysis / Refinement Required |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CAP-01** | Hierarchical Task Planning | Recursive goal decomposition into a DAG of sub-tasks with programmatic limits | Partially Implemented | `apodex/planning/planner_executor.py` | Needs support for exact UCB-1 pruning and recursive deep HTN tree search. |
| **CAP-02** | Causal World Modeling | Directed causal graphs representing economic variables, confounding parents, and do-calculus | Partially Implemented | `apodex/world_model/world_model.py` | Causal links exist, but counterfactual logic must integrate with Pearl's structural equations. |
| **CAP-03** | Bayesian Belief Update | Real-time estimation of epistemic entropy and Expected Free Energy updates | Partially Implemented | `apodex/ai_eos/active_inference/engine.py` | Deployed; needs formal coupling to planner-evaluation gates. |
| **CAP-04** | Multi-Tier Persistent Memory | Separation of Episodic, Semantic, Procedural, and Working memory on transaction-safe SQLite | Partially Implemented | `apodex/memory/semantic_memory.py` & `apodex/memory/learning_memory.py` | Deployed and thread-safe; needs memory decay (Ebbinghaus) enforcement under query loads. |
| **CAP-05** | Multi-Agent Specialization & Debate | dynamic split-merge lifecycles, consensus protocols, and disagreement escalation | Partially Implemented | `apodex/ai_eos/intelligence/collective.py` | Core dynamic weighting exists, but split-merge lifecycles need rigorous definition. |
| **CAP-06** | Closed-Loop Scientific Discovery | Automatic hypothesis generation, literature scraping, containerized execution, and validation | Partially Implemented | `apodex/research_os/pipeline.py` & `apodex/research_os/statistical_validation.py` | Exact Normal CDF calls exist; literature indexing needs mapping to knowledge graphs. |
| **CAP-07** | Safe Self-Improvement & Rollback | Suitable score-driven gates, shadow rollouts, and automatic multi-tier rollbacks | Partially Implemented | `apodex/governance/architecture_verifier.py` & `apodex/evolution/production/orchestrator.py` | Implemented and hardened; needs formal alignment with multi-objective suitability metrics. |
| **CAP-08** | Long-Horizon Project Orchestration | Transactional multi-day DAG queues, parallel executors, and failure-checkpointing | Partially Implemented | `apodex/cognition/controller.py` & `apodex/planning/planner_executor.py` | Operational with HTN task graphs and topological sort executors. |

---

## 2. Capability Disposition & Elimination Matrix

To ensure zero duplicated responsibilities, we identify overlapping or duplicated components in the legacy codebases and assign them a clear resolution path.

| Component Path | Functionality | Disposition | Action / Justification |
| :--- | :--- | :--- | :--- |
| `AgentHarness/agent_harness/core/memory/emg_engine.py` | Experience Memory Graph | **ADAPTER** | Keep as a zero-duplication compatibility bridge pointing to `apodex/memory/emg_engine.py`. |
| `AgentHarness/agent_harness/core/memory/semantic_memory.py` | Semantic Database Memory | **ADAPTER** | Thin re-export inherit class pointing directly to `apodex/memory/semantic_memory.py`. |
| `AgentHarness/agent_harness/core/cost_tier.py` | Cost tier enum definitions | **ADAPTER** | Point legacy test suites directly to the canonical `CostTier` in the compatibility bridging layer. |
| `AgentHarness/agent_harness/core/runtime/verification/parallel.py` | Verification concurrency | **ADAPTER** | Bridge legacy orchestration tests to canonical `apodex/governance/parallel_verification.py`. |

---

## 3. Tier-0 Capability Ownership Matrix

Every Tier-0 operational layer inside the unified Cognitive Operating System has exactly one authoritative, non-overlapping owner file.

```
========================================================================================
   Tier-0 Capability Layer         Authoritative Owner Module Path
========================================================================================
1. Hierarchical Strategic Planning ───>  apodex/planning/planner_executor.py
2. Causal World Graph State     ───>  apodex/world_model/world_model.py
3. Active Inference & Bayesian priors ───>  apodex/ai_eos/active_inference/engine.py
4. Durable SQLite Memory (CMOS) ───>  apodex/memory/semantic_memory.py
5. Multi-Mind Orchestration & Debate ─>  apodex/ai_eos/intelligence/collective.py
6. Scientific Discovery & Stats  ───>  apodex/research_os/statistical_validation.py
7. Architectural Verification & Gates ─>  apodex/governance/architecture_verifier.py
8. Long-Horizon DAG Execution    ───>  apodex/cognition/controller.py
========================================================================================
```

No sub-agent or worker is permitted to bypass these designated owners. All communications must flow through explicit event propagation contracts.
