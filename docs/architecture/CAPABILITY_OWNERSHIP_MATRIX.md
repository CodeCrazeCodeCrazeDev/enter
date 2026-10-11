# Capability Ownership Matrix
## Single-Layer Ownership Mapping Across 16 Core Cognitive Capabilities

---

## 1. Executive Summary & Anti-Duplication Enforcement

To eliminate architectural overlap across Research OS, EIOS, EOS, AEAN, and APODEX, every core cognitive capability is strictly assigned to **exactly one primary owning layer**. Secondary layers interact only via explicit, asynchronous event contracts or read-only service interfaces.

---

## 2. Capability Ownership Matrix Table

| Cognitive Capability | Primary Owning Layer | Target Package / Module | Interfaces & Event Contracts | Strictly Prohibited in Other Layers |
|---|---|---|---|---|
| **1. Scientific Literature Review** | **Layer 1 (Research OS)** | `apodex.ai_eos.research.research_os` | `conduct_literature_review()`, `ALPHAALGO_*_PRINCIPLES` | Layers 2-4 MUST NOT perform raw academic paper ingestion. |
| **2. Formal Hypothesis Generation** | **Layer 1 (Research OS)** | `apodex.ai_eos.research.integration` | `register_research_hypothesis()`, `Hypothesis` | Layers 2-4 MUST NOT alter hypothesis p-values or statistical priors. |
| **3. Statistical Claim Validation** | **Layer 1 (Research OS)** | `apodex.research_os.statistical_validation` | `validate_hypothesis_statistically()` | Layers 2-4 MUST NOT override empirical verification outcomes. |
| **4. Opportunity Sensing ($EFE$)** | **Layer 2 (EIOS/EOS)** | `apodex.arcs.kernel.kernel` | `sense_opportunity_anomalies()`, `ExpectedFreeEnergy` | Layers 1, 3, 4 MUST NOT calculate venture-level $EFE$ anomalies. |
| **5. Workflow DAG Compilation** | **Layer 2 (EIOS/EOS)** | `apodex.ai_eos.intelligence.computational_architecture` | `compile_execution_dag()`, `WorkflowDAG` | Layers 1, 3, 4 MUST NOT build or reschedule strategic DAG nodes. |
| **6. Venture Unit Economics** | **Layer 2 (EIOS/EOS)** | `apodex.ai_eos.intelligence.eos_engine` | `evaluate_venture_unit_economics()`, `EOSState` | Layers 1, 3, 4 MUST NOT track LTV/CAC or financial payback parameters. |
| **7. GTM Strategy Simulation** | **Layer 2 (EIOS/EOS)** | `apodex.ai_eos.intelligence.eos_engine` | `GTMSystemSimulator`, `simulate_gtm_rollout()` | Layers 1, 3, 4 MUST NOT run market go-to-market loops. |
| **8. Multi-Agent Specialization** | **Layer 3 (AEAN)** | `apodex.orchestration.hierarchical` | `CoordinatorAgent`, `WorkerAgent`, `AgentInstance` | Layers 1, 2, 4 MUST NOT spawn low-level execution worker threads. |
| **9. HiveMind Token Bidding** | **Layer 3 (AEAN)** | `apodex.aean.coordination.hive_mind` | `bid_tasks_hivemind()`, `TokenAuction` | Layers 1, 2, 4 MUST NOT manage token bid allocations for tasks. |
| **10. Peer Negotiation & Arbitration**| **Layer 3 (AEAN)** | `apodex.aean.coordination.hive_mind` | `propose_contract()`, `arbitrate_dispute()` | Layers 1, 2, 4 MUST NOT execute agent-to-agent price bargaining. |
| **11. Procedural Tool Invention** | **Layer 3 (AEAN)** | `apodex.skills.runner` | `synthesize_procedural_skill()`, `ToolSchema` | Layers 1, 2, 4 MUST NOT package trajectory steps into tool schemas. |
| **12. Multi-Graph World Model** | **Layer 4 (APODEX)** | `apodex.world_model.world_model` | `WorldModel`, `CausalNode`, `RelationEdge` | Layers 1-3 MUST NOT maintain independent graph state data. |
| **13. SCM Pearl Do-Calculus** | **Layer 4 (APODEX)** | `apodex.cognition.brain` | `DeepCausalWorldModel.query_do_calculus()` | Layers 1-3 MUST NOT execute causal path pruning or do-calculus. |
| **14. Beta Conjugate Belief Updates**| **Layer 4 (APODEX)** | `apodex.cognition.brain` | `update_bayesian_belief()`, `BeliefState` | Layers 1-3 MUST NOT update conjugate prior $(\alpha, \beta)$ distributions. |
| **15. Multi-Tier Memory Consolidation**| **Layer 4 (APODEX)** | `apodex.cognition.brain` | `AdvancedMemoryEngine`, `apply_ebbinghaus_forgetting()`| Layers 1-3 MUST NOT run memory decay or consolidation cron loops. |
| **16. Immutable Safety Governance** | **Layer 4 (APODEX)** | `apodex.world_model.governance.approval` | `reviewed_at`, `ApprovalPolicy`, `SafetyCore` | Layers 1-3 MUST NOT modify immutable safety rules or bypass gates. |
