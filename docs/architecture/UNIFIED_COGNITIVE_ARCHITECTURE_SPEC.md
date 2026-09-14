# Unified Cognitive Operating System Architecture Specification

## 1. Executive Summary & Architectural Rationale

This specification establishes the single, unified 4-layer cognitive operating system taxonomy for **Research OS**, **EIOS**, **EOS**, **AEAN**, and **APODEX**. Rather than treating these components as five partially overlapping platforms, this architecture formalizes them into hierarchical layers of a singular autonomous intelligence platform.

### Key Architectural Principles
1. **Strict Single Responsibility**: Each subsystem occupies exactly one layer in the cognitive stack with zero logical or functional duplication.
2. **First-Principles Active Inference**: State estimation, planning, and sensing operate via Expected Free Energy (EFE) minimization across epistemic value (uncertainty reduction) and pragmatic value (goal achievement).
3. **Layered Handoff Protocol**: Upward flow provides belief updates and anomaly sensing; downward flow dispatches goals, DAG execution contracts, and capability policies.
4. **Institutional-Grade Reliability**: Multi-agent bidding, graph-of-thought verification, automated rollback on SLA breach, and deterministic regression replay ensure safe long-horizon operations.

---

## 2. The 4-Layer Cognitive Operating System Taxonomy

```
+-----------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS (Research Layer)                      |
|  - Quantitative Literature Ingestion & 500-Paper Corpus Principles                |
|  - Scientific Hypothesis Generation, Experimentation & Statistical Validation     |
|  - Transferable Engineering Principle Extraction & Code Rewrite Engine            |
+-----------------------------------------------------------------------------------+
                                          |
                        Hypothesis Handoff & Epistemic Beliefs
                                          v
+-----------------------------------------------------------------------------------+
|               LAYER 2: EIOS / EOS (Execution & Orchestration Layer)               |
|  - EIOS Kernel: Active Inference Sensing & Expected Free Energy (EFE) Minimization|
|  - EOS Engine: Founder State Machine, Opportunity Trees & Coupled Business Loops  |
|  - 14-Layer Computational Architecture Engine & Opportunity Routing              |
+-----------------------------------------------------------------------------------+
                                          |
                      Strategic Intent & Opportunity DAG Handoff
                                          v
+-----------------------------------------------------------------------------------+
|                  LAYER 3: AEAN (Cognitive Intelligence Layer)                     |
|  - HiveMind Multi-Agent Token Bidding Registry & Swarm Specialization            |
|  - Cognitive Brain, Graph-of-Thought (GoT) Reasoner & Active Learning Engine      |
|  - Genetic Workflow Optimizer & Island MAP-Elites Policy Search                   |
+-----------------------------------------------------------------------------------+
                                          |
                       Task Execution & Protocol Action Handoff
                                          v
+-----------------------------------------------------------------------------------+
|                 LAYER 4: APODEX (Decision & Execution Platform Layer)             |
|  - WorldModel Creator: Causal State Graph, Entities, Beliefs & Reality Substrate  |
|  - Skill Registry (60 Canonical Skills) & Protocol Runner                         |
|  - Cost Cutting Engine, Credit Halt Guardrails & Execution Infrastructure        |
+-----------------------------------------------------------------------------------+
```

### Layer Definitions

#### Layer 1: Research OS (Research Layer)
* **Canonical Responsibility**: Scientific hypothesis formulation, literature review querying over the 500-paper corpus, statistical validation (`standard_normal_ppf`, DSR calculation), and transferable principle extraction.
* **Key Components**: `ResearchOS`, `ResearchToSystemBridge`, `CodeRewriteEngine`, `StatisticalValidator`.

#### Layer 2: EIOS / EOS (Execution & Orchestration Layer)
* **Canonical Responsibility**: High-level entrepreneurial state machine orchestration, Active Inference sensing over research hypotheses, 14-layer computational engine routing, and coupled business loop simulation.
* **Key Components**: `EIOSKernel`, `FirstPrinciplesEOSEngine`, `FourteenLayerEntrepreneurialEngine`, `OpportunityDecisionTree`.

#### Layer 3: AEAN (Cognitive Intelligence Layer)
* **Canonical Responsibility**: Multi-agent coordination via token-bidding swarm registry, graph-of-thought search, active learning uncertainty decomposition, genetic workflow optimization, and cognitive brain reasoning.
* **Key Components**: `HiveMind`, `CognitiveBrain`, `GraphOfThoughtEngine`, `ActiveLearningEngine`, `GeneticWorkflowOptimizer`.

#### Layer 4: APODEX (Decision & Execution Platform Layer)
* **Canonical Responsibility**: World model entity/belief graph maintenance, reality substrate state, skill execution (60 canonical skills), protocol execution, budget/credit halt enforcement, and software engineering tool automation.
* **Key Components**: `WorldModel`, `SkillRegistry`, `ProtocolRunner`, `CostCuttingEngine`, `SafetyCore`.

---

## 3. Capability Ownership Matrix

To eliminate architectural duplication across subsystems, capability ownership is strictly partitioned:

| Capability | Canonical Owner Layer | Canonical Implementation Module | Disallowed Logical Duplicates |
| :--- | :--- | :--- | :--- |
| **Scientific Literature Review** | Layer 1 (Research OS) | `apodex.ai_eos.research.research_os` | AEAN local paper parsers |
| **Statistical Hypothesis Testing** | Layer 1 (Research OS) | `apodex.research_os.statistical_validation` | WorldModel local p-value checkers |
| **Active Inference Sensing (EFE)** | Layer 2 (EIOS Kernel) | `apodex.arcs.kernel.kernel` | AEAN local EFE loops |
| **Entrepreneurial State Machine** | Layer 2 (EOS Engine) | `apodex.ai_eos.intelligence.eos_first_principles` | APODEX local state machine |
| **14-Layer Business Engine** | Layer 2 (EOS Engine) | `apodex.ai_eos.intelligence.fourteen_layer_engine` | AEAN local business logic |
| **Multi-Agent Token Bidding** | Layer 3 (AEAN) | `apodex.aean.coordination.hive_mind` | EIOS local worker schedulers |
| **Graph-of-Thought Search** | Layer 3 (AEAN) | `agent_harness.core.runtime.reasoning.got` | APODEX local tree search |
| **Genetic Workflow Optimization** | Layer 3 (AEAN) | `apodex.evolution.workflow_optimizer` | Research OS local genetic algorithms |
| **World Model & Causal Graph** | Layer 4 (APODEX) | `apodex.world_model.world_model` | AEAN local entity graphs |
| **Skill Execution & Flywheel** | Layer 4 (APODEX) | `apodex.skills.registry` / `runner` | EOS local action executors |
| **Credit Halt & Budget Guard** | Layer 4 (APODEX) | `apodex.world_model.governance` | Layer 1/2 local credit counters |

---

## 4. Core Cognitive Subsystem Definitions & First-Principles Design

### 4.1 Planning & Scheduling
* **Design**: Hierarchical decomposition where Layer 2 EOS emits high-level opportunity DAGs, Layer 3 AEAN compiles DAG steps into active-learning worker subtasks, and Layer 4 APODEX schedules execution with strict cost-tier budgets.
* **Active Inference Planning**: Minimized Expected Free Energy:
  $$G(\pi) = -\mathbb{E}_{q(o,\theta|\pi)}[\ln p(o|\theta) - \ln q(o|\pi)] - \mathbb{E}_{q(\theta|\pi)}[\text{KL}(q(o|\pi) \parallel p(o))]$$

### 4.2 Long-Horizon Task Execution & Software Engineering Automation
* **Design**: Layer 1 `CodeRewriteEngine` generates non-Gaussian Hawkes stability patches derived from research papers (Papers 301-400), verified by Layer 3 `GraphOfThoughtEngine` and executed safely inside Layer 4 sandbox environments with automated rollback on test failure.

### 4.3 World Models & Simulation/Forecasting
* **Design**: Layer 4 `WorldModel` maintains Bayesian belief nodes ($P(\text{State} | \text{Evidence})$) and causal DAG edges. Layer 2 coupled business loops run Monte Carlo simulations against the WorldModel to forecast cash run-rate, customer churn, and market fit.

### 4.4 Multi-Agent Coordination & Swarm Communication
* **Design**: Layer 3 `HiveMind` implements competitive token bidding for task allocation. Specialized agents (Researcher, Architect, Engineer, Validator) submit bid scores based on capability alignment and epistemic confidence.

### 4.5 Memory Systems & Knowledge Management
* **Design**: Hierarchical memory topology:
  - **Episodic Trajectory Memory**: Step-by-step agent action histories (`LongTermLearningMemory`).
  - **Semantic Knowledge Infrastructure (IKG)**: Temporal graph nodes with confidence decay (`KnowledgeInfrastructure`).
  - **Cognitive Memory Operating System (CMOS)**: Compressed state snapshots with lossy/lossless tiering.

### 4.6 Safety, Governance & Self-Improvement
* **Design**: Layer 4 `SafetyCore` enforces hard credit halts, cost cutting tiers, and compliance checks. Layer 3 `GeneticWorkflowOptimizer` evolves prompt strategies and worker topology via Island MAP-Elites with edit path distance penalties.

---

## 5. Unified Cross-Layer Data Contracts

### 5.1 Research OS -> EIOS Kernel Handoff
```python
class ResearchHypothesisHandoff(BaseModel):
    hypothesis_id: str
    paper_citations: List[str]
    transferable_principles: List[str]
    epistemic_uncertainty: float
    statistical_p_value: float
    recommended_action: str
```

### 5.2 EIOS Kernel -> AEAN HiveMind Handoff
```python
class OpportunityDAGContract(BaseModel):
    opportunity_id: str
    target_layer_idx: int # 1..14
    efe_score: float
    subtasks: List[Dict[str, Any]]
    max_budget_usd: float
    sla_timeout_seconds: float
```

### 5.3 AEAN HiveMind -> APODEX Execution Handoff
```python
class SkillExecutionTask(BaseModel):
    task_id: str
    assigned_agent: str
    skill_name: str # From 60 canonical skills in SkillRegistry
    parameters: Dict[str, Any]
    causal_context_nodes: List[str]
```

---

## 6. Trade-offs, Failure Modes & Complexity Analysis

1. **Trade-off**: Active Inference EFE calculations introduce a ~15ms latency overhead per decision cycle in exchange for guaranteed epistemic exploration.
2. **Failure Mode**: Cascading uncertainty drift across layers. *Mitigation*: Hard p-value cutoff ($p < 0.05$) in Layer 1 before promote to Layer 2, and automatic budget downshifting in Layer 4.
3. **Complexity Budget**: $O(N \log N)$ multi-agent token bidding where $N \le 60$ agents, maintaining real-time execution bounds (<200ms per swarm allocation step).
