# UNIFIED DEPENDENCY GRAPH AND INTERFACE SPECIFICATION

---

## 1. System-Wide Dependency DAG

The unified 4-layer Cognitive Operating System enforces a strict directed acyclic dependency graph (DAG) for operational call paths, paired with an asynchronous upward telemetry and active inference observation feedback loop.

```
                  +-----------------------------------+
                  |   LAYER 1: RESEARCH OS LAYER      |
                  |  - Literature DB (200 Papers)     |
                  |  - Experiment Engine              |
                  |  - Statistical Validation         |
                  +-----------------+-----------------+
                                    |
                         Hypothesis | Validated Principles
                         Promotion  | (ResearchToSystemBridge)
                                    v
                  +-----------------------------------+
                  |   LAYER 2: EIOS / EOS LAYER       |
                  |  - Active Inference Sensing       |
                  |  - 13 Coupled Business Loops      |
                  |  - Capital Allocation             |
                  +-----------------+-----------------+
                                    |
                         Strategic  | Context Envelope
                         Directives | & EFE Budgets
                                    v
                  +-----------------------------------+
                  |    LAYER 3: AEAN COGNITION LAYER  |
                  |  - Graph-of-Thought Decomposition |
                  |  - Swarm Debate & Active Learning |
                  |  - Skill Registry                 |
                  +-----------------+-----------------+
                                    |
                         Action     | Tool Invocations
                         Intents    | & SCM Interventions
                                    v
                  +-----------------------------------+
                  |  LAYER 4: APODEX PLATFORM LAYER   |
                  |  - CMOS Ebbinghaus Memory         |
                  |  - Sandboxed Execution Runtime    |
                  |  - Pearl Do-Calculus Engine       |
                  +-----------------+-----------------+
                                    |
                         Telemetry, | Trajectory Cards,
                         Obs. Logs  | & Ebbinghaus Decay
                                    v
                  +-----------------------------------+
                  | UPWARD TELEMETRY & FEEDBACK LOOP  |
                  | Re-feeds into Research OS (L1)    |
                  | & Active Inference Sensing (L2)   |
                  +-----------------------------------+
```

---

## 2. Layer Interface Contracts

### 2.1 Research OS -> EIOS / EOS (Layer 1 -> Layer 2 Interface)
* **Contract Class**: `apodex.ai_eos.research.integration.ResearchToSystemBridge`
* **Data Flow**:
  * Inputs: `HypothesisRecord` (Hypothesis ID, target parameter, proposed adjustment, experimental metric).
  * Outputs: `ActiveInferenceState` (Updated priors, expected variance, confidence threshold).
* **Guarantees**: Parameters are updated in Layer 2 **only** if Welch's t-test achieves $p < 0.01$ and $DSR > 1.0$.

### 2.2 EIOS / EOS -> AEAN (Layer 2 -> Layer 3 Interface)
* **Contract Class**: `apodex.ai_eos.intelligence.eos_first_principles.StrategicDirectiveEnvelope`
* **Data Flow**:
  * Inputs: `Directive` (Target business loop name, EFE token allocation, risk envelope).
  * Outputs: `ExecutionStatus` (Success probability, GoT plan tree ID, resource consumption).
* **Guarantees**: No direct execution of tools by Layer 2. Directives must be converted into GoT plan nodes by Layer 3.

### 2.3 AEAN -> APODEX (Layer 3 -> Layer 4 Interface)
* **Contract Class**: `apodex.execution.ExecutionIntent`
* **Data Flow**:
  * Inputs: `ActionIntent` (Tool ID, arguments, causal intervention vector $do(X)$).
  * Outputs: `ToolResult` (Output payload, execution time, cost tier consumed, memory card ID).
* **Guarantees**: All tool calls pass through Pearl's Do-Calculus counterfactual check before sandbox execution.

---

## 3. Active Inference Perception-Action Closed Loop

The active inference loop coordinates information across all four layers using the Expected Free Energy ($EFE$) formula:

$$\mathcal{G}(\pi) = \underbrace{-\mathbb{E}_{q(o|\pi)}[\ln p(o)]}_{\text{Pragmatic Value (Goal Realization)}} + \underbrace{\mathbb{E}_{q(\theta|\pi)}[D_{KL}(q(\theta|o,\pi) \,||\, q(\theta|\pi))]}_{\text{Epistemic Information Gain (Uncertainty Reduction)}}$$

1. **Perception (L4 -> L2 -> L1)**: APODEX captures trajectory telemetry and logs memory cards. EIOS updates internal state priors $q(\theta)$. Research OS monitors statistical anomalies.
2. **Decision (L2 -> L3)**: EIOS evaluates policies $\pi$ to minimize $\mathcal{G}(\pi)$ and emits strategic directives to AEAN.
3. **Reasoning & Planning (L3)**: AEAN builds Graph-of-Thought candidates, performs Bayesian Nash swarm debate, and selects highest-utility action paths.
4. **Execution (L3 -> L4)**: AEAN passes execution intents to APODEX, which executes tools and updates the CMOS memory graph.

---

## 4. Architectural Rules Preventing Dependency Cycles and Duplication

1. **Strict Downward Invocation**: Layer $N$ may invoke functions in Layer $N+1$ or $N+2$. Layer $N+1$ may **never** directly invoke synchronous functions in Layer $N$.
2. **Asynchronous Upward State Handoff**: Upward communication happens exclusively via event logs, telemetry streams, and memory database reads.
3. **No Horizontal Sibling Duplication**: Modules inside the same layer must share common infrastructure (e.g., all memory components inside Layer 4 use `CMOSMemoryEngine`).
