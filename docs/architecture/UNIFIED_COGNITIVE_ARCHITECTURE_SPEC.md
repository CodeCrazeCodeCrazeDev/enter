# Unified Cognitive Operating System Specification

## 1. Executive Summary & Architectural Directive

The **Unified Cognitive Operating System (Cognitive OS)** establishes a single, integrated architecture for long-horizon autonomous intelligence, scientific research, entrepreneurial reasoning, multi-agent collaboration, and institutional-grade execution.

Rather than maintaining Research OS, EIOS, EOS, AEAN, and APODEX as five separate, overlapping platforms, Cognitive OS unifies them into a **strict 4-Layer Cognitive Hierarchy**. Each layer possesses explicit responsibility boundaries, non-redundant capabilities, standardized event interfaces, and unified state representations.

```
+-----------------------------------------------------------------------------------+
| LAYER 4: APODEX PLATFORM LAYER (Decision Execution, World Model, Skill Registry)  |
+-----------------------------------------------------------------------------------+
                                         ^
                                         | Execution Directives & World State
                                         v
+-----------------------------------------------------------------------------------+
| LAYER 3: AEAN COGNITIVE INTELLIGENCE LAYER (Swarm, GoT Reasoning, Active Learning)|
+-----------------------------------------------------------------------------------+
                                         ^
                                         | Cognitive Strategies & Intent
                                         v
+-----------------------------------------------------------------------------------+
| LAYER 2: EIOS / EOS EXECUTION & ORCHESTRATION LAYER (Active Inference, 14 Layers)|
+-----------------------------------------------------------------------------------+
                                         ^
                                         | Validated Scientific Hypotheses
                                         v
+-----------------------------------------------------------------------------------+
| LAYER 1: RESEARCH OS SCIENTIFIC LAYER (Hypothesis Engine, Statistical Validation) |
+-----------------------------------------------------------------------------------+
```

---

## 2. Layer Taxonomy & Subsystem Responsibilities

### Layer 1: Scientific Research Layer (`ResearchOS`)
* **Primary Scope**: Scientific discovery, evidence synthesis, statistical validation, and falsifiable hypothesis generation.
* **Canonical Modules**: `apodex/ai_eos/research/research_os.py`, `apodex/ai_eos/research/integration.py`, `apodex/research_os/`.
* **Core Capabilities**:
  1. Literature review and knowledge graph querying (`conduct_literature_review`).
  2. Hypothesis formulation with explicit p-value bounds, Deflated Sharpe Ratio (DSR) metrics, and statistical power controls (`generate_falsifiable_hypothesis`).
  3. Experimental design and empirical verification via safe statistical validation.
* **Interfaces**: Exports `ValidatedHypothesis` events to Layer 2 via `export_validated_hypothesis_to_kernel`.

### Layer 2: Execution & Orchestration Layer (`EIOS` / `EOS`)
* **Primary Scope**: Active inference sensing, Expected Free Energy (EFE) minimization, 14-layer entrepreneurial computation, capital allocation, and business lifecycle execution.
* **Canonical Modules**: `apodex/arcs/kernel/kernel.py` (`EIOSKernel`), `apodex/ai_eos/intelligence/eos_engine.py` (`EOSEngine`), `apodex/ai_eos/intelligence/fourteen_layer_engine.py`.
* **Core Capabilities**:
  1. Active Inference sensing over research hypotheses where EFE is defined by Pragmatic Value plus Epistemic Information Gain:
     $$\text{EFE}(\pi) = -\mathbb{E}_{q(o|\pi)}[\ln p(o)] + \text{D}_{\text{KL}}(q(s|\pi) \parallel p(s))$$
  2. Pearl's Causal Do-Calculus interventions ($P(Y | \text{do}(X))$) for counterfactual business scenario analysis.
  3. 14-Layer Computational Architecture of Entrepreneurship (Reality Substrate to Meta-Learning).
  4. Advanced Kelly Criterion portfolio sizing and capital allocation.
* **Interfaces**: Consumes hypotheses from Layer 1, generates execution goals for Layer 3, and promotes validated ventures to Layer 4.

### Layer 3: Cognitive Intelligence Layer (`AEAN`)
* **Primary Scope**: High-level cognitive reasoning, multi-agent swarm debate, Graph-of-Thought (GoT) search, active learning, and capability synthesis.
* **Canonical Modules**: `apodex/aean/coordination/hive_mind.py`, `apodex/planning/planner_executor.py`, `agent_harness/core/runtime/`.
* **Core Capabilities**:
  1. Multi-agent swarm coordination using Bayesian Nash Equilibrium clearing to eliminate sycophancy bias.
  2. Graph-of-Thought (GoT) topological decomposition and step-wise uncertainty evaluation.
  3. Active learning engine for contradiction verification and epistemic gap detection.
  4. Dynamic skill synthesis and capability evolution.
* **Interfaces**: Translates Layer 2 strategic goals into multi-agent task graphs and dispatches tool execution requests to Layer 4.

### Layer 4: Decision & Execution Platform Layer (`APODEX`)
* **Primary Scope**: Tool orchestration, skill execution, unified world graph state maintenance, governance, and safety enforcement.
* **Canonical Modules**: `apodex/skills/registry.py`, `apodex/world_model/world_model.py`, `apodex/execution/`, `apodex/world_model/governance/`.
* **Core Capabilities**:
  1. Skill Registry hosting 60+ production skills with strict execution runtime sandboxing.
  2. Unified World Graph (`WorldModel`) maintaining causal nodes, relational edges, entity tracking, and Bayesian belief updating.
  3. Tiered governance approval gateways, audit logs, and compliance enforcement.
* **Interfaces**: Receives task dispatches from Layer 3, executes skills, updates world model state, and provides real-time state feedback to all layers.

---

## 3. Elimination of Duplicated Capabilities & Interface Contracts

| Capability Domain | Legacy Duplication | Resolved Canonical Owner | Elimination Rationale |
| :--- | :--- | :--- | :--- |
| **Hypothesis Generation** | Shared across ResearchOS, AEAN, and EOS | **Layer 1: ResearchOS** | Ensures all hypotheses conform to strict statistical validation ($p < 0.05$, DSR clamping) before entering execution. |
| **Active Inference & EFE** | Duplicate implementations in EIOS and EOS | **Layer 2: EIOS Kernel / EOS Engine** | Single point of active inference sensing and EFE minimization. |
| **Multi-Agent Coordination** | Fragmented between AEAN Hive Mind and Harness Observer | **Layer 3: AEAN Hive Mind** | Centralizes Bayesian Nash Equilibrium clearing and swarm debate. |
| **Skill Execution & Registry** | Duplicate skill registries across skills and harness | **Layer 4: APODEX Skill Registry** | Enforces single source of truth for skill lookup, alias resolution, and runtime execution. |
| **World Graph State** | Dispersed world graph representations | **Layer 4: APODEX WorldModel** | Centralizes causal node graph and belief propagation across the platform. |

---

## 4. Multi-Tier Memory & World Model Integration

1. **Working Memory (Layer 3 & 4)**: Graph-of-Thought active context nodes with Ebbinghaus memory decay filter:
   $$R(t) = e^{-\frac{t}{S}}$$
2. **Episodic Memory (Layer 3)**: Action-Decision Graphs (ADG) recording execution trajectories, reward feedback, and counterfactuals.
3. **Semantic & Empirical Memory (Layer 1 & 2)**: 300-paper research corpus principles (`AI_EOS_RESEARCH_DB.yaml` and `ALPHA_ALGO_100_NEW_RESEARCH.yaml`), domain knowledge graphs, and causal models.
4. **World State (Layer 4)**: Real-time causal node network updated via Bayesian recursive updating:
   $$P(\theta | o) = \frac{P(o | \theta) P(\theta)}{P(o)}$$

---

## 5. Verification & Compliance Standards

* Non-cyclic DAG execution enforced across all 4 layers.
* Statistical significance ($p < 0.05$) required for Layer 1 hypothesis promotion.
* Expected Free Energy reduction required for Layer 2 execution plan approval.
* Zero sycophancy bias in Layer 3 swarm consensus via game-theoretic clearing.
* 100% test coverage and zero regression against the baseline test suite (`PYTHONPATH=.:AgentHarness python3 -m pytest -q --import-mode=importlib`).
