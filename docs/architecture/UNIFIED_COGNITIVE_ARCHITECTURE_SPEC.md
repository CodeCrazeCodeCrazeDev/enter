# Unified Cognitive Operating System Architecture Specification
**Document Version:** 2.0.0 (2026 Edition)
**Status:** Approved
**Taxonomy Paradigm:** Single 4-Layer Stratified Cognitive Platform

---

## 1. Executive Summary & First-Principles Redesign

### 1.1 Architectural Thesis
To achieve long-horizon autonomous execution, scientific discovery, entrepreneurial reasoning, and self-improvement with institutional-grade reliability, the autonomous platform must NOT operate as five separate, competing platforms (Research OS, EIOS, EOS, AEAN, APODEX).

Prior implementations suffered from duplicated responsibilities:
- **Duplicated Active Inference & Sensing:** EIOS, EOS Engine, and AEAN HiveMind each maintained distinct belief update loops.
- **Fragmented Causal Graphing:** APODEX WorldModel and EOS Opportunity Decision Tree maintained duplicate causal nodes.
- **Uncoordinated Task Execution:** AEAN Task Dispatcher and EIOS DAG Scheduler ran decoupled task queues.

**The Solution:** A unified, 4-layer stratified cognitive architecture with single-capability ownership and explicit, formal inter-layer contracts.

```
+-----------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS (Research Layer)                      |
|  - Literature Review & Principle Extraction (Paper Corpus DB 1-600)               |
|  - Empirical Hypothesis Generation & Statistical Validation (DSR, P-hacking Ctrl)  |
|  - Automated Code Mutation & AST Verification (Hawkes Stability)                  |
+-----------------------------------------------------------------------------------+
                                        | Validated Hypotheses & Engineering Principles
                                        v
+-----------------------------------------------------------------------------------+
|                   LAYER 2: EIOS / EOS (Execution & Business Layer)                |
|  - Active Inference Sensing & Anomaly Detection                                   |
|  - Business Loop Optimization & Capital Allocation State Machine                  |
|  - Dynamic DAG Compilation & Resource Scheduling                                  |
+-----------------------------------------------------------------------------------+
                                        | Execution DAGs & Value Objectives
                                        v
+-----------------------------------------------------------------------------------+
|                    LAYER 3: AEAN (Cognitive Intelligence Layer)                   |
|  - Multi-Agent Coordination & Specialized Swarms (HiveMind)                       |
|  - Token-Based Resource Bidding & Task Allocation                                 |
|  - Active Inference Planning & Active Learning Engine                             |
+-----------------------------------------------------------------------------------+
                                        | Action Intent & Task Commands
                                        v
+-----------------------------------------------------------------------------------+
|               LAYER 4: APODEX (Decision & Execution Platform Layer)               |
|  - World Model (Causal DAG, Bayesian Belief Networks, Counterfactuals)            |
|  - Tool & Code Execution Sandbox                                                 |
|  - Multi-Tier Memory (CMOS: Episodic, Semantic, EMG Action-Decision Graph)        |
|  - Safety, Compliance & Governance Guards                                         |
+-----------------------------------------------------------------------------------+
```

---

## 2. Formal Layer Contracts & Inter-Layer APIs

### 2.1 Layer 1 -> Layer 2 Hand-off Contract
`ResearchOS` validates scientific hypotheses and extracts engineering principles from literature, exporting them to `EIOS/EOS`:
```python
class ValidatedResearchHandoff(BaseModel):
    hypothesis_id: str
    paper_title: str
    extracted_principle: str
    confidence_score: float  # [0.0, 1.0]
    p_value: float           # < 0.01 required
    target_subsystem: str    # "EIOS", "EOS", "AEAN", "APODEX"
    implementation_module: str
```

### 2.2 Layer 2 -> Layer 3 Hand-off Contract
`EIOS/EOS` transforms validated hypotheses and market anomalies into executable Directed Acyclic Graphs (DAGs) for `AEAN`:
```python
class ExecutionDAGHandoff(BaseModel):
    dag_id: str
    objective_statement: str
    expected_free_energy: float
    nodes: List[DAGTaskNode]
    capital_budget: float
    priority_tier: int
```

### 2.3 Layer 3 -> Layer 4 Hand-off Contract
`AEAN` agents bid on task nodes, plan actions using active inference, and issue tool execution requests to `APODEX`:
```python
class ActionExecutionRequest(BaseModel):
    task_id: str
    agent_id: str
    tool_name: str
    tool_parameters: Dict[str, Any]
    causal_context: Dict[str, Any]
    safety_context: Dict[str, Any]
```

### 2.4 Layer 4 -> Layer 1/2/3 Feedback Loop
`APODEX` executes tools, records observation trajectories into CMOS (Cognitive Memory Operating System), updates Causal Nodes and Bayesian Beliefs in WorldModel, and sends active inference prediction errors back up the stack.

---

## 3. Core Cognitive Subsystems Integration

### 3.1 Long-Horizon Execution & Planning
- Long-horizon goals are decomposed by Layer 2 (`EIOS DAG Scheduler`) into structured task graphs.
- Layer 3 (`AEAN Active Inference Planner`) evaluates expected trajectories using Expected Free Energy (EFE = Pragmatic Value + Epistemic Value).
- Layer 4 (`APODEX WorldModel`) simulates step outcomes counterfactually prior to real-world execution.

### 3.2 World Modeling & Active Inference
- `APODEX WorldModel` maintains a unified Causal Graph $G = (V, E)$ and recursive Bayesian beliefs $P(\theta \mid y)$.
- Sensing anomalies in market or codebase environments trigger active inference updates in `EIOS Kernel`.

### 3.3 Multi-Agent Coordination & Swarms
- `AEAN HiveMind` manages specialized agent swarms (Researcher, Architect, Coder, Validator, Marketer, Operator).
- Token-based bidding allocates tasks based on agent specialization vectors and past performance metrics.

### 3.4 Multi-Tier Memory Systems (CMOS)
- **Episodic Memory:** Short-term execution trace buffer.
- **Semantic Memory:** Long-term vector-indexed concept graph.
- **EMG (Action-Decision Graph):** High-level decision trajectories linking active inference priors to outcome rewards.

---

## 4. Institutional-Grade Safety, Governance & Verification

1. **AST Verification & Hawkes Stability:** All automated code transformations are parsed via AST in `CodeRewriteEngine` to enforce Hawkes non-Gaussian recursive depth limits.
2. **P-Hacking Controls & Deflated Sharpe Ratio:** Statistical validation enforces Bonferroni corrections and DSR thresholds to prevent spurious discovery.
3. **Sandbox Isolation & Compliance Guards:** Tool calls in Layer 4 pass through safety filters ensuring immutable system invariants.
