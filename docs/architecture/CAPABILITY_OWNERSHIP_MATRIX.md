# Capability Ownership Matrix

## 1. Overview & Boundary Principles

To eliminate architectural duplication and ensure long-term maintainability, subsystem capabilities across the platform are strictly mapped to one of four layers. No subsystem may re-implement capabilities assigned to another layer.

---

## 2. Capability Ownership Mapping

| Capability Domain | Assigned Layer | Primary Module Implementation | Interface Standard |
| :--- | :--- | :--- | :--- |
| **Literature Mining & Principles Extraction** | Layer 1 (Research OS) | `apodex.ai_eos.research.research_os` | `ResearchHypothesis` / `CorpusPrinciple` |
| **AST Code Analysis & Rewrite Validation** | Layer 1 (Research OS) | `apodex.ai_eos.research.integration.CodeRewriteEngine` | `RewriteProposal` / `ASTValidationResult` |
| **Statistical Hypothesis Testing ($p$-value)** | Layer 1 (Research OS) | `apodex.research_os.statistical_validation` | `ValidationReport` |
| **Active Inference EFE Calculation** | Layer 2 (EIOS / EOS) | `apodex.arcs.kernel.kernel.EIOSKernel` | `EFEVector` / `ActiveInferenceState` |
| **Workflow DAG Compilation & Routing** | Layer 2 (EIOS / EOS) | `apodex.ai_eos.research.compiler.WorkflowCompiler` | `IntentDAG` / `ExecutionGraph` |
| **Entrepreneurial Growth State Machine** | Layer 2 (EIOS / EOS) | `apodex.ai_eos.intelligence.eos_first_principles` | `EOSState` / `LifecycleStage` |
| **Capital & Resource Allocation** | Layer 2 (EIOS / EOS) | `apodex.arcs.capital.allocation_engine` | `AllocationProposal` |
| **Multi-Agent Task Auction & Bidding** | Layer 3 (AEAN) | `apodex.aean.coordination.hive_mind.HiveMind` | `AgentBid` / `TaskAllocation` |
| **Swarm Agent Specialization & Execution** | Layer 3 (AEAN) | `apodex.arcs.agents.executive_agents` | `AgentAction` / `ExecutionResult` |
| **Strategy Pre-Trade & Risk Validation** | Layer 3 (AEAN) | `apodex.aean.validation.pretrade` | `RiskAuditResult` |
| **Causal Graph Node & Edge Storage** | Layer 4 (APODEX) | `apodex.world_model.world_model.WorldModel` | `CausalNode` / `RelationEdge` |
| **Recursive Bayesian Belief Updating** | Layer 4 (APODEX) | `apodex.world_model.domain.beliefs` | `BayesianBelief` / `Observation` |
| **Cross-Layer State Handoff Orchestration** | Layer 4 (APODEX) | `apodex.ai_eos.research.integration.ResearchToSystemBridge` | `UnifiedBridgeState` |
| **Telemetry, Safety & Audit Logging** | Layer 4 (APODEX) | `apodex.meta.safety_manager.SafetyManager` | `TelemetryRecord` / `AuditLog` |

---

## 3. Strict Layer Interaction Boundaries

1. **Layer 1 $\rightarrow$ Layer 2:** Research OS exports validated hypotheses ($H_{val}$) to EIOS Kernel via `EIOSKernel.register_research_hypothesis`.
2. **Layer 2 $\rightarrow$ Layer 3:** EIOS Kernel publishes synthesized execution DAGs to AEAN HiveMind via `HiveMind.register_research_insight`.
3. **Layer 3 $\rightarrow$ Layer 4:** AEAN Agents execute tasks and commit causal observations to APODEX WorldModel via `WorldModel.create_node` and `WorldModel.update_belief`.
4. **Layer 4 $\rightarrow$ Layer 1/2:** WorldModel streams updated posterior beliefs to Research OS and EIOS Kernel for active inference loop closure via `ResearchToSystemBridge`.
