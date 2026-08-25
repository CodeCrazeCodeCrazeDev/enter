# UNIFIED COGNITIVE OPERATING SYSTEM SPECIFICATION
## Architecting Autonomous Intelligence: Research OS, EIOS/EOS, AEAN, and APODEX as a Layered Operating System

---

## 1. Executive Summary & Foundational Architectural Paradigm

Modern autonomous AI platforms often suffer from structural redundancy, fragmented state management, and competing sub-agent control loops when designed as separate, loosely-coupled applications. To achieve long-horizon autonomous execution, institutional-grade reliability, and self-improving intelligence, **Research OS, EIOS, EOS, AEAN, and APODEX are unified into a single, cohesive 4-Layer Cognitive Operating System (Cognitive OS)**.

Rather than operating as five parallel systems with duplicate planners, memory stores, and decision engines, each system occupies an explicit, non-overlapping layer in the cognitive stack:

```
+-----------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS (Research Layer)                      |
| Literature Mining | Hypothesis Generation | Empirical Verification | Statistical Tests  |
+-----------------------------------------------------------------------------------+
                                         │  Active Research Directives & Tested Hypotheses
                                         ▼
+-----------------------------------------------------------------------------------+
|                   LAYER 2: EIOS / EOS (Execution & Orchestration Layer)           |
| Active Inference Sensing | Expected Free Energy | 13 Business Loops | Capital Alloc. |
+-----------------------------------------------------------------------------------+
                                         │  Strategic Directives & Context Envelopes
                                         ▼
+-----------------------------------------------------------------------------------+
|                      LAYER 3: AEAN (Cognitive Intelligence Layer)                  |
| Graph-of-Thought Reasoning | Swarm Debate | Active Learning | Multi-Agent Coordination|
+-----------------------------------------------------------------------------------+
                                         │  Validated Action Intents & Sub-Task Plans
                                         ▼
+-----------------------------------------------------------------------------------+
|                  LAYER 4: APODEX (Decision & Execution Platform Layer)            |
| Tool Sandbox | CMOS Ebbinghaus Memory | Causal Do-Calculus | Governance & Safety  |
+-----------------------------------------------------------------------------------+
```

### Key Principles:
1. **Single Responsibility per Layer**: Every cognitive operation (planning, sensing, memory retention, reasoning, execution) has exactly one canonical owner.
2. **Explicit Upstream/Downstream Interfaces**: Information flows strictly via typed interface handshakes (`ResearchToSystemBridge`, `ActiveInferenceState`, `ThoughtNode`, `MemoryCard`).
3. **Unified Active Inference Loop**: Perception and action across all layers minimize Expected Free Energy ($EFE = \text{Pragmatic Value} + \text{Epistemic Information Gain}$).
4. **Empirical Grounding**: System code and architectural parameters evolve exclusively via statistically validated scientific experiments (Welch's t-test $p < 0.01$).

---

## 2. Layer-by-Layer Subsystem Architecture

### 2.1 Layer 1: Research OS (Research Layer)

**Primary Ownership**: Scientific inquiry, academic paper database ingestion (`AI_EOS_RESEARCH_DB.yaml`), hypothesis generation, experimental setup, and statistical validation.

* **Components**:
  * `LiteratureReviewEngine`: Conducts semantic searches across academic publications and extracts transferable engineering principles.
  * `HypothesisGenerator`: Formulates falsifiable scientific hypotheses regarding platform performance, strategy, or algorithmic parameters.
  * `ExperimentRunner`: Executes controlled $A/B$ or multi-seed ablation experiments against baseline platforms.
  * `StatisticalValidationEngine`: Computes Student/Welch t-statistics, degrees of freedom, $p$-values, and Deflated Sharpe Ratios ($DSR$) to prevent false discovery.
* **Non-Overlapping Boundary**: Research OS does **not** execute runtime business tasks or tool calls directly; it produces validated scientific principles and hypothesis promotions consumed by Layer 2 and Layer 3.

### 2.2 Layer 2: EIOS / EOS (Execution & Orchestration Layer)

**Primary Ownership**: Strategic domain modeling, market/opportunity sensing, active inference routing, enterprise lifecycle governance, capital allocation, and business loop state machines.

* **Components**:
  * `EIOSKernel`: Operates the active inference perception loop, calculating Expected Free Energy ($EFE$) over opportunity states and sensing anomalies in environmental signals.
  * `EOSIntelligenceEngine`: Coordinates 13 coupled business loops (Product-Market Fit, Unit Economics, GTM Channel, Moat Durability, Reinvention, etc.) and the 14-Layer Computational Architecture of Entrepreneurship.
  * `CapitalAllocationEngine`: Manages Advanced Kelly Criterion portfolio sizing, risk limits, and downshifting/halting protocols.
* **Non-Overlapping Boundary**: EOS/EIOS handles high-level strategic state transitions and resource allocations, delegating individual multi-step reasoning plans to Layer 3 (AEAN).

### 2.3 Layer 3: AEAN (Cognitive Intelligence Layer)

**Primary Ownership**: Multi-agent orchestration, Graph-of-Thought ($GoT$) reasoning, Bayesian Nash swarm debate, active learning uncertainty reduction, and skill execution.

* **Components**:
  * `GraphOfThoughtEngine`: Decomposes complex strategic directives into directed acyclic graphs ($DAGs$) of thought nodes with dynamic branch pruning and backtracking.
  * `SwarmCoordinationEngine`: Facilitates multi-agent debate and consensus using Bayesian Nash Equilibrium clearing to eliminate sycophancy and confirmation bias.
  * `ActiveLearningEngine`: Quantifies epistemic uncertainty across action spaces and routes high-uncertainty tasks for exploration.
  * `SkillRegistry`: Pre-populates and executes operational cognitive skills with standard input/output interface contracts.
* **Non-Overlapping Boundary**: AEAN does **not** manage low-level sandboxed execution tools or persistent database drivers; it emits validated execution intents to Layer 4 (APODEX).

### 2.4 Layer 4: APODEX (Decision & Execution Platform Layer)

**Primary Ownership**: Low-level tool runtime execution, sandboxed code execution, CMOS memory management with Ebbinghaus decay, causal SCM interventions, safety checks, and telemetry logging.

* **Components**:
  * `CMOSMemoryEngine`: Implements multi-tier episodic/semantic memory with exponential Ebbinghaus retention decay ($S(t) = e^{-t/\tau}$) and Jaccard context retrieval.
  * `CausalInterventionEngine`: Evaluates Pearl's Do-Calculus ($P(Y | do(X))$) to compute counterfactual outcomes prior to state modification.
  * `ToolExecutionSandbox`: Safely executes code, shell commands, and external integrations with strict resource budgets and rate limits.
  * `GovernanceAndSafetyCore`: Enforces multi-tier approval policies, credit/cost halts, and audit logging.
* **Non-Overlapping Boundary**: APODEX acts strictly as the secure runtime platform, exposing pure execution primitives and state storage services to higher layers.

---

## 3. Capability Ownership & Duplication Elimination Matrix

| Capability Domain | Canonical Layer | Primary Subsystem | Replaced / Unified Duplicate Systems |
| :--- | :--- | :--- | :--- |
| **Literature & Principle Ingestion** | Layer 1 | `ResearchOS.LiteratureReviewEngine` | Removed duplicate literature engines in AEAN/EOS |
| **Statistical Experimentation** | Layer 1 | `ResearchOS.StatisticalValidationEngine` | Unified experiment trackers into single `ExperimentRecord` |
| **Market Sensing & Active Inference**| Layer 2 | `EIOSKernel.ActiveInference` | Replaced fragmented sensing modules across APODEX/AEAN |
| **Business State Machine (13 Loops)**| Layer 2 | `EOSIntelligenceEngine` | Consolidated business logic out of agent runtime |
| **Multi-Agent Swarm Debate** | Layer 3 | `AEAN.SwarmCoordinationEngine` | Unified duplicate swarm protocols |
| **Graph-of-Thought Reasoning** | Layer 3 | `AEAN.GraphOfThoughtEngine` | Consolidated planner engines |
| **Ebbinghaus Memory & CMOS** | Layer 4 | `APODEX.CMOSMemoryEngine` | Replaced legacy memory adapters across harness |
| **Tool Sandbox & Pearl Causal SCM** | Layer 4 | `APODEX.CausalInterventionEngine` | Centralized tool execution and counterfactual checks |

---

## 4. Interfaces and Data Handshakes

### 4.1 Research OS -> EOS/EIOS Bridge (`ResearchToSystemBridge`)
```python
class ResearchToSystemBridge:
    def export_validated_hypothesis_to_kernel(
        self, hypothesis_id: str, effect_size: float, p_value: float
    ) -> ActiveInferenceState:
        """Pushes statistically confirmed principles into EIOS active inference priors."""
        ...
```

### 4.2 EIOS/EOS -> AEAN Handshake
```python
class StrategicDirectiveEnvelope:
    directive_id: str
    target_loop: str  # e.g., 'UnitEconomics', 'GTMChannel'
    efe_budget: float
    constraints: Dict[str, Any]
    active_priors: List[float]
```

### 4.3 AEAN -> APODEX Execution Handshake
```python
class ExecutionIntent:
    intent_id: str
    thought_node_id: str
    tool_name: str
    tool_args: Dict[str, Any]
    do_calculus_intervention: Optional[Dict[str, Any]]
    safety_tier: str
```

---

## 5. Non-Functional Guarantees & Verification Strategy

1. **Deterministic State Transitions**: State transitions within Layer 2 state machines and Layer 3 GoT nodes are fully traceable via deterministic UUIDs and execution logs.
2. **Resource & Token Budgeting**: Every strategic directive carries explicit token and latency budgets down-shifted dynamically upon threshold breaches.
3. **100% Empirical Verification**: Every code modification across all 4 layers must pass the complete unit, integration, and performance test suite with zero regressions.
