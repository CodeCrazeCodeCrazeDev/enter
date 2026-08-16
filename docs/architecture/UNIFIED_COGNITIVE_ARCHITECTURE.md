# Unified Cognitive Operating System Architecture Specification

## Executive Architectural Summary

This document establishes the authoritative, first-principles specification for the Unified Cognitive Operating System. The platform transitions from five historically overlapping subsystems (Research OS, AEAN, EIOS, EOS, and APODEX) into a single, cohesive, 4-layer cognitive operating system substrate. By consolidating overlapping domains and establishing strict boundary invariants, this architecture eliminates logical duplication, guarantees clear capability ownership, and enables long-horizon autonomous intelligence.

```
+-----------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS (Discovery & Evidence)                |
|  - Scientific Discovery Engine        - Multi-stage Hypothesis Filtering          |
|  - Active Literature Ingestion        - Statistical Validation & Power Analysis    |
+-----------------------------------------------------------------------------------+
                                          |
                                 Evidence & Principles
                                          v
+-----------------------------------------------------------------------------------+
|                     LAYER 2: AEAN (Cognitive Intelligence Layer)                  |
|  - Multi-Agent HiveMind Coordination  - Graph-of-Thought (GoT) Reasoning          |
|  - Active Inference & Expected Free Energy - Structural Causal Models (Do-Calculus) |
+-----------------------------------------------------------------------------------+
                                          |
                                Strategic Directives
                                          v
+-----------------------------------------------------------------------------------+
|                  LAYER 3: EIOS / EOS (Execution & Strategic Loops)                 |
|  - EIOS Kernel Orchestration          - 13 Strategic Business Flywheels           |
|  - Capital Allocation & Risk Gates     - Opportunity & Market Arbitrage Engine     |
+-----------------------------------------------------------------------------------+
                                          |
                              Substrate Instructions
                                          v
+-----------------------------------------------------------------------------------+
|                     LAYER 4: APODEX (Decision, Memory & Substrate)                |
|  - Dual-System CMOS Memory            - Skill Registry & Flywheel Execution       |
|  - Sandboxed Tool Runtime Execution   - Governance & Safety Guardrails            |
+-----------------------------------------------------------------------------------+
```

---

## 1. Architectural Taxonomy & Decoupled Layering

### Layer 1: Research OS (Scientific Discovery & Evidence Acquisition Layer)
- **Canonical Responsibility**: Autonomous scientific exploration, hypothesis formulation, literature discovery, rigorous statistical testing, and empirical evidence synthesis.
- **Key Subsystems**: Literature Indexing Engine, Hypothesis Generation & Filtering Engine, Holm-Bonferroni Trial Runner, Experiment Pipeline.
- **Boundary Invariant**: Research OS produces verified empirical principles and evidence cards. It never executes business loops, manages long-term memory state, or orchestrates agent task dispatching.

### Layer 2: AEAN (Cognitive Intelligence Layer)
- **Canonical Responsibility**: Multi-agent orchestration, active inference active goal resolution, causal reasoning, graph-based planning, and inter-agent coordination.
- **Key Subsystems**: HiveMind Coordinator, Graph-of-Thought (GoT) Planner, Active Inference Engine, Do-Calculus Causal Reasoner, Swarm Consensus Arbiter.
- **Boundary Invariant**: AEAN is the pure reasoning engine. It translates empirical research principles into active decision policies. It delegates runtime execution to EIOS/EOS and memory storage to APODEX.

### Layer 3: EIOS / EOS (Execution & Strategic Business Loop Layer)
- **Canonical Responsibility**: Unified entrepreneurial execution, opportunity scanning, capital allocation, risk management, and 13 strategic business loops.
- **Key Subsystems**: EIOS Kernel, EOS First-Principles Manager, Opportunity Arbitrage Engine, Portfolio Risk & Treasury Manager, GTM Channel Optimizer.
- **Boundary Invariant**: EOS manages high-level business logic, financial allocations, and multi-timescale strategic loops. It receives cognitive strategy from AEAN and relies on APODEX for tool execution and persistent state storage.

### Layer 4: APODEX (Decision, Memory & Substrate Execution Layer)
- **Canonical Responsibility**: Low-level runtime execution, sandboxed tool orchestration, dual-tier memory (CMOS/EMG/Semantic), skill registry, and safety/governance enforcement.
- **Key Subsystems**: CMOS Memory Engine, Skill Registry & Flywheel Runner, Tool Execution Engine, Safety Observer & Tiered Approval Gate.
- **Boundary Invariant**: APODEX provides physical substrate services to all higher layers. It possesses zero domain-specific business or research logic, serving as the deterministic, highly reliable execution engine.

---

## 2. Core Mathematical Formulations

### 2.1 Expected Free Energy (Active Inference)
To unify goal-directed planning under uncertainty, AEAN evaluates policies $\pi$ by minimizing Expected Free Energy $G(\pi)$:

$$G(\pi) = -\underbrace{\mathbb{E}_{q(o, \theta|\pi)}[\ln p(o|\theta) - \ln q(\theta|\pi)]}_{\text{Epistemic Value (Information Gain)}} - \underbrace{\mathbb{E}_{q(o|\pi)}[\ln p(o)]}_{\text{Pragmatic Value (Goal Utility)}}$$

Where:
- $o$ represents environment observations (market signals, test outcomes, system metrics).
- $\theta$ represents latent world model parameters.
- $p(o)$ denotes preferred target distributions (e.g., target ROI, low risk, high test coverage).

### 2.2 Structural Causal Do-Calculus Interventions
Causal inference in AEAN and EIOS evaluates intervention probabilities $P(Y|\text{do}(X=x))$ via Pearl's adjustment formula over direct causal parents $PA_X$:

$$P(Y|\text{do}(X=x)) = \sum_{z} P(Y|X=x, PA_X=z) P(PA_X=z)$$

This guarantees that strategic decisions (e.g., capital reallocation or prompt refactoring) isolate true causal impact from confounded observational correlations.

### 2.3 Ebbinghaus Memory Decay
Memory retention $R(t)$ within APODEX CMOS memory decays non-linearly according to elapsed time $t$ and stability factor $S$:

$$R(t) = \exp\left(-\frac{t}{S}\right)$$

When an item is retrieved or revalidated, $S$ updates as $S_{\text{new}} = S_{\text{old}} \cdot (1 + c \cdot \text{retrieval\_utility})$.

---

## 3. Interface Contracts & Eradication of Duplication

To eliminate logical duplication, capability ownership is strictly partitioned as follows:

| Capability Domain | Canonical Single Owner | Previous Duplicate Modules (Deprecating/Refactored) | Interface Contract Method |
| :--- | :--- | :--- | :--- |
| **Research & Literature** | `Layer 1: Research OS` (`apodex.ai_eos.research`) | Scattered paper loaders across `apodex.cognition` | `ResearchOS.conduct_literature_review(query)` |
| **Active Inference & Causal Reasoning** | `Layer 2: AEAN` (`apodex.aean.coordination`) | Duplicate active inference in `apodex.arcs.kernel` | `HiveMind.evaluate_policy_efe(policy, world_state)` |
| **Business Loops & Opportunities** | `Layer 3: EIOS / EOS` (`apodex.ai_eos.intelligence`) | Redundant business logic in `agent_harness` | `EIOSKernel.process_opportunity_pipeline(opp)` |
| **Memory & Storage (CMOS/EMG)** | `Layer 4: APODEX` (`apodex.memory`) | Isolated memory classes in `agent_harness.core.memory` | `CMOSEngine.query_semantic_memory(query)` |
| **Skill Registry & Tool Execution** | `Layer 4: APODEX` (`apodex.skills`) | Fragmented tool runners in `apodex.planning` | `SkillRegistry.execute_skill(skill_id, params)` |

---

## 4. Failure Modes, Trade-offs & Complexity Budget

### 4.1 Failure Modes & Mitigations
1. **Sycophancy & Swarm Compliance Bias**:
   - *Failure Mode*: Multi-agent swarms converge on sub-optimal decisions due to consensus bias.
   - *Mitigation*: Swarm debate protocol in AEAN enforces randomized devil's advocate roles and Bayesian Nash equilibrium clearing.
2. **Context Memory Bloat**:
   - *Failure Mode*: Context window exhaustion in long-horizon tasks.
   - *Mitigation*: Automatic Ebbinghaus memory pruning in APODEX CMOS reduces context memory footprint by over 50% without loss of key evidence.
3. **Cascading Tool Failures**:
   - *Failure Mode*: Sequential tool crashes causing task failure in long-horizon execution.
   - *Mitigation*: APODEX Tiered Approval and Rollback Manager isolates faults and rewinds state to last known good checkpoint.

### 4.2 Complexity Analysis
- **Time Complexity**: Policy evaluation via GoT & Active Inference operates in $O(K \cdot D)$ where $K$ is the beam width and $D$ is the depth horizon.
- **Space Complexity**: Memory retention scales as $O(N)$ with active Ebbinghaus decay bounding total stored memory nodes $N \le N_{\text{max}}$.

---

## 5. Verification Invariants

1. **Strict Layer Directionality**: Calls flow strictly top-down (Layer 1 $\to$ Layer 2 $\to$ Layer 3 $\to$ Layer 4) or bottom-up via events. Zero horizontal or circular cross-layer dependencies.
2. **Single Responsibility Principle**: Each capability has exactly one canonical owning package in `apodex/`.
3. **100% Backward Compatibility**: Legacy imports under `agent_harness.*` route seamlessly through thin adapters to canonical `apodex` implementations.
