# Unified Cognitive Operating System Architecture Specification
**Authoritative Architectural Specification for Autonomous Intelligence**
**Version:** 4.0.0
**Scope:** Research OS (Layer 1) | EIOS & EOS (Layer 2) | AEAN (Layer 3) | APODEX (Layer 4)

---

## Executive Summary

The Unified Cognitive Operating System establishes a single, integrated 4-layer cognitive architecture for autonomous scientific research, entrepreneurial decision-making, multi-agent collaboration, long-horizon planning, and self-improving execution.

Historical implementations suffered from fragmented domain boundaries and logical duplication across independent systems. Under this unified specification, Research OS, EIOS, EOS, AEAN, and APODEX are strictly re-architected as functional layers within one coherent cognitive operating system.

```
+-----------------------------------------------------------------------------------+
| LAYER 1: RESEARCH LAYER (Research OS)                                              |
| Literature Review | 500-Paper Corpus | Scientific Hypotheses | Empirical Validation  |
+-----------------------------------------------------------------------------------+
                                         | (Validated Hypotheses & Active Hypotheses)
                                         v
+-----------------------------------------------------------------------------------+
| LAYER 2: EXECUTION & ORCHESTRATION LAYER (EIOS Kernel & EOS Engine)               |
| Active Inference Sensing (EFE) | DAG Workflows | EOS State Machine | Capital Alloc   |
+-----------------------------------------------------------------------------------+
                                         | (Task DAGs & Bidding Requests)
                                         v
+-----------------------------------------------------------------------------------+
| LAYER 3: COGNITIVE INTELLIGENCE LAYER (AEAN HiveMind)                             |
| Multi-Agent Bidding | MAP-Elites Islands | Code AST Verification | SFT Preferences   |
+-----------------------------------------------------------------------------------+
                                         | (Executable Actions & Code Rewrites)
                                         v
+-----------------------------------------------------------------------------------+
| LAYER 4: DECISION & EXECUTION PLATFORM LAYER (APODEX WorldModel & Cognitive Brain)|
| Causal Graph Updates | Recursive Bayesian Beliefs | Skills Flywheel | Governance  |
+-----------------------------------------------------------------------------------+
```

---

## Section 1: First-Principles Architectural Rationale

### 1.1 First Principles of Cognition & Action
Autonomous cognitive systems operating under high epistemic uncertainty cannot rely on static heuristic workflows or uncoordinated LLM prompts. Cognition is fundamentally a variational free energy minimization problem across four distinct timescales:

1. **Epistemic Exploration (Layer 1):** Uncovering true causal structures through scientific literature, hypothesis testing, and statistical validation ($p < 0.05$, Deflated Sharpe Ratio $DSR > 1.0$).
2. **Dynamic Opportunistic Orchestration (Layer 2):** Sensing market and environmental anomalies via Active Inference, evaluating opportunity cost, allocating risk-weighted capital, and sequencing execution DAGs.
3. **Collective Agent Reasoning (Layer 3):** Coordinating specialized cognitive agents using market-based token bidding, genetic workflow optimization, and verified code rewrites.
4. **Persistent World Modeling & Execution (Layer 4):** Maintaining an explicit, unified causal graph ($G = (V, E)$), updating prior beliefs recursively via Bayesian inference, executing verified skills, and enforcing hard safety boundaries.

### 1.2 Elimination of Duplicate Capabilities
To eliminate logical redundancy across legacy modules:
- **Planners:** Legacy separate planners (Active Inference Planner, Active Learning Engine, PlannerExecutor) are consolidated into Layer 2 (EIOS Kernel Active Inference DAG Scheduler).
- **World Models:** Legacy isolated belief representations are unified into Layer 4 (`APODEX.WorldModel`), providing the single authoritative source of truth for reality states, causal graphs, and Bayesian beliefs.
- **Memories:** Fragmented memory stores are mapped into Layer 4 (`APODEX.CognitiveBrain` and CMOS infrastructure), eliminating fragmented semantic stores across agent harnesses.

---

## Section 2: Layer Boundaries & Interface Specifications

### 2.1 Layer 1: Research Layer (Research OS)
- **Primary Function:** Ingests scientific publications, registers transferable engineering principles (e.g., 500-paper AlphaAlgo research corpus), generates testable hypotheses, conducts empirical experiments, and computes statistical validation metrics.
- **Canonical Module Location:** `apodex.ai_eos.research` & `apodex.research_os`
- **Exposed Interfaces:**
  - `conduct_literature_review(query: str) -> List[ResearchPrinciple]`
  - `generate_scientific_hypothesis(domain: str) -> ResearchHypothesis`
  - `validate_hypothesis_empirically(hypothesis_id: str) -> StatisticalValidationResult`
  - `export_validated_hypothesis_to_kernel(hypothesis_id: str) -> Dict`
  - `promote_hypothesis_to_eos(hypothesis_id: str) -> Dict`

### 2.2 Layer 2: Execution & Orchestration Layer (EIOS Kernel & EOS Engine)
- **Primary Function:** Operates as the central execution kernel and entrepreneurial decision engine. Translates scientific hypotheses into executable active inference state graphs, senses environmental anomalies using Expected Free Energy (EFE), and enforces the 11-section EOS state machine and 14-layer entrepreneurial architecture.
- **Canonical Module Location:** `apodex.arcs.kernel` & `apodex.ai_eos.intelligence`
- **Exposed Interfaces:**
  - `register_research_hypothesis(hypothesis: ResearchHypothesis) -> str`
  - `sense_opportunity_anomalies(observations: Dict) -> List[OpportunityNode]`
  - `evaluate_active_inference_efe(state: Dict) -> ActiveInferencePlan`
  - `execute_workflow_dag(dag_id: str, payload: Dict) -> ExecutionResult`
  - `transition_eos_state(target_stage: EOSStage) -> StageTransitionResult`

### 2.3 Layer 3: Cognitive Intelligence Layer (AEAN HiveMind)
- **Primary Function:** Multi-agent collective reasoning, token bidding negotiation, genetic workflow optimization via MAP-Elites islands, AST-verified code rewrite generation, and preference optimization (SFT/DPO).
- **Canonical Module Location:** `apodex.aean.coordination` & `apodex.ai_eos.research.integration`
- **Exposed Interfaces:**
  - `register_research_insight(insight: Dict) -> str`
  - `submit_bidding_auction(task_spec: Dict) -> AgentAssignment`
  - `optimize_workflow_genetically(workflow: WorkflowSpec) -> OptimizedWorkflow`
  - `verify_proposal_ast(code: str) -> ASTVerificationResult`

### 2.4 Layer 4: Decision & Execution Platform Layer (APODEX WorldModel & Cognitive Brain)
- **Primary Function:** Authoritative state representation, causal node graph manipulation, recursive Bayesian belief updates ($\text{Prior} \to \text{Likelihood} \to \text{Posterior}$), skill protocol execution, credit/cost halting, and regulatory governance.
- **Canonical Module Location:** `apodex.world_model`, `apodex.cognition`, & `apodex.skills`
- **Exposed Interfaces:**
  - `update_entity_state(entity_id: str, new_state: Dict) -> Entity`
  - `update_bayesian_belief(belief_id: str, evidence: Dict) -> BeliefState`
  - `execute_skill_protocol(protocol_id: str, context: Dict) -> ProtocolResult`
  - `evaluate_governance_compliance(action: Action) -> ComplianceResult`

---

## Section 3: Cross-Layer Active Inference State Handoffs

State handoffs across the four layers follow an Active Inference cycle governed by Variational Free Energy ($F$) and Expected Free Energy ($G$).

```
[Layer 1 Research OS]
    | Scientific Hypothesis (H_i, Prior p(theta))
    v
[Layer 2 EIOS/EOS Kernel]
    | Active Inference State Sensing & EFE Evaluation
    | G(u) = - E_q[D_KL(q(o|u) || p(o))] - E_q[ln p(o)]
    v
[Layer 3 AEAN HiveMind]
    | Multi-Agent Bidding & Policy Selection (u*)
    | u* = argmin_u G(u)
    v
[Layer 4 APODEX WorldModel]
    | Execution, Realized Outcome (o_t), Causal & Bayesian Belief Update
    | P(theta | o_t) = p(o_t | theta) * p(theta) / p(o_t)
    v
[Feedback to Layer 1 Research OS Literature & Hypothesis Registry]
```

### 3.1 Mathematical Formulations

#### 1. Active Inference Expected Free Energy (EFE)
For policy selection $u$ at Layer 2:
$$G(u) = -\underbrace{\mathbb{E}_{q(o, s | u)}\left[ D_{\text{KL}}\left(q(s | o, u) \,||\, q(s | u)\right) \right]}_{\text{Epistemic Value (Information Gain)}} - \underbrace{\mathbb{E}_{q(o | u)}\left[ \ln p(o) \right]}_{\text{Pragmatic Value (Goal Realization)}}$$

#### 2. Hawkes Non-Gaussian Process Recursive Stability
To ensure code modification stability in Layer 3 during automated AST rewrites:
$$\lambda(t) = \mu_0 + \sum_{t_i < t} \alpha \, e^{-\beta (t - t_i)}$$
Where recursive call depth within function definitions is bounded by $D_{\text{max}} \le 10$ and branching factor $\le 5$.

#### 3. MAP-Elites Island Migration Gates
In Layer 3 workflow optimization, migration across elite islands is gated by fitness score $f_i$:
$$P(\text{migration}_{A \to B}) = \frac{1}{1 + e^{-\gamma (f_A - f_B)}}$$

#### 4. Safe Inverse CDF & Deflated Sharpe Ratio
In Layer 1 experiment validation:
$$Z_p = \text{clamp}\left( \Phi^{-1}(p), -5.0, 5.0 \right)$$
$$DSR = \Phi\left( \frac{(\hat{SR} - SR_0)\sqrt{N - 1}}{\sqrt{1 - \gamma_1 \hat{SR} + \frac{\gamma_2 - 1}{4} \hat{SR}^2}} \right)$$

---

## Section 4: Safety, Governance, and Compliance Frameworks

1. **Credit & Cost Halting:** Layer 4 monitors cost profiles and protocol execution budgets. If cumulative daily token or compute budget exceeds thresholds, execution drops to a downshifted safe mode or halts immediately.
2. **Tiered Approval Gates:** Structural modifications to Layer 2 state machine or Layer 4 causal graph require multi-agent consensus ($>80\%$ vote in Layer 3 HiveMind) and explicit verification passing.
3. **Timezone-Aware Temporal Consistency:** All timestamp logging across all 4 layers uses strict timezone-aware UTC objects (`datetime.now(timezone.utc)`), eliminating timezone ambiguity and Python 3.12 deprecation warnings.

---

## Section 5: Verification & Architectural Guarantees

This architecture guarantees:
- **Zero Capability Duplication:** Canonical single responsibility per layer.
- **Full Importability:** All modules import cleanly across all layers without circular dependencies.
- **Complete Test Coverage:** Every cross-layer handoff is validated via end-to-end integration tests (`tests/integration/test_unified_4layer_integration.py` and `tests/integration/test_unified_cognitive_os_e2e.py`).
