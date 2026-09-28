# Capability Ownership Matrix
**Document Version:** 2.0.0 (2026 Edition)
**Status:** Approved
**Principle:** Single-Capability Ownership (Zero Duplication)

---

## 1. Single Ownership Mapping Table

To eliminate redundant implementations across Research OS, EIOS, EOS, AEAN, and APODEX, every platform capability is assigned to exactly ONE owning layer. All other layers must consume this capability via the owning layer's exposed API.

| Capability Area | Owning Layer | Owning Subsystem / Module | Exposed API Contract |
|---|---|---|---|
| Literature Review & Principle Extraction | **Layer 1: Research OS** | `apodex.ai_eos.research.research_os` | `ResearchOS.conduct_literature_review()` |
| Empirical Hypothesis Generation | **Layer 1: Research OS** | `apodex.ai_eos.research.research_os` | `ResearchOS.generate_hypotheses()` |
| Statistical Validation (DSR & P-hacking) | **Layer 1: Research OS** | `apodex.ai_eos.research.statistical_validation` | `StatisticalValidation.validate_hypothesis()` |
| AST Code Rewriting & Hawkes Verification | **Layer 1: Research OS** | `apodex.ai_eos.research.integration` | `CodeRewriteEngine.verify_proposal_ast()` |
| Active Inference Sensing & Anomaly Detection | **Layer 2: EIOS Kernel** | `apodex.arcs.kernel.kernel` | `EIOSKernel.sense_opportunity_anomalies()` |
| Business Loop & Capital Allocation | **Layer 2: EOS Engine** | `apodex.ai_eos.intelligence.eos_engine` | `EOSEngine.ingest_validated_research()` |
| Company Growth State Machine | **Layer 2: EOS Engine** | `apodex.ai_eos.intelligence.eos_first_principles` | `CompanyGrowthStateMachine.transition_stage()` |
| Dynamic Execution DAG Compilation | **Layer 2: EIOS Kernel** | `apodex.arcs.kernel.kernel` | `EIOSKernel.compile_execution_dag()` |
| Multi-Agent Swarm Coordination | **Layer 3: AEAN** | `apodex.aean.coordination.hive_mind` | `HiveMind.register_agent()`, `bidding()` |
| Token Bidding & Task Allocation | **Layer 3: AEAN** | `apodex.aean.coordination.hive_mind` | `HiveMind.submit_bid()`, `dispatch()` |
| Active Inference Task Planning | **Layer 3: AEAN** | `apodex.ai_eos.intelligence.computational_architecture` | `ActiveInferencePlanner.plan_trajectory()` |
| Causal Graph & Counterfactual Modeling | **Layer 4: APODEX** | `apodex.world_model.world_model` | `WorldModel.create_node()`, `query()` |
| Recursive Bayesian Belief Networks | **Layer 4: APODEX** | `apodex.world_model.domain.beliefs` | `WorldModel.update_belief()` |
| Multi-Tier Memory Systems (CMOS) | **Layer 4: APODEX** | `agent_harness.core.memory` | `CMOSMemoryEngine.store_episodic()` |
| Tool & Sandbox Execution | **Layer 4: APODEX** | `apodex.skills.runner` | `SkillRunner.execute_tool()` |
| Safety & Compliance Governance | **Layer 4: APODEX** | `apodex.world_model.governance` | `GovernanceGuard.validate_execution()` |

---

## 2. Duplication Audit & Resolution Log

1. **Active Inference Sensing:**
   - *Previous Defect:* EIOS, EOS, and AEAN HiveMind each implemented custom active inference anomaly detectors.
   - *Resolution:* Consolidated under `EIOSKernel.sense_opportunity_anomalies()`. EOS and AEAN now register interest callbacks with `EIOSKernel`.

2. **Causal Node Creation:**
   - *Previous Defect:* EOS Engine created orphan Causal Nodes detached from APODEX WorldModel.
   - *Resolution:* EOS Engine delegates all causal graph operations to `WorldModel.create_node()` in Layer 4.

3. **Agent Task Allocation:**
   - *Previous Defect:* EIOS DAG Scheduler directly assigned agent threads, bypassing AEAN HiveMind token bidding.
   - *Resolution:* EIOS now emits compiled DAG task nodes to `HiveMind`, where specialized AEAN agents bid on and execute tasks.
