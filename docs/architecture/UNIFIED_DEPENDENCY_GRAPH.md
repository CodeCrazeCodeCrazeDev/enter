# Unified Dependency Graph and State-Handoff Protocol
## Research OS / EIOS / EOS / AEAN / APODEX Layered Cognitive Architecture

### 1. System Layer Dependency Topology

```
+-------------------------------------------------------------------------------+
|                        LAYER 1: RESEARCH OS                                   |
|   (Literature Review, Principle Extraction, Hypothesis Validation)            |
+-------------------------------------------------------------------------------+
                                       |
                                       | ResearchHypothesis Handoff
                                       v
+-------------------------------------------------------------------------------+
|                      LAYER 2: EIOS / EOS ENGINE                               |
|   (Continuous Sensing, Active Inference EFE, DAG Compilation, Risk Gateway)   |
+-------------------------------------------------------------------------------+
                                       |
                                       | TaskOpportunity / Execution DAG
                                       v
+-------------------------------------------------------------------------------+
|                       LAYER 3: AEAN HIVEMIND                                  |
|   (Multi-Agent Bidding, Specialization, Evolution, Capability Distillation)   |
+-------------------------------------------------------------------------------+
                                       |
                                       | ExecutionOutcome & Telemetry
                                       v
+-------------------------------------------------------------------------------+
|                     LAYER 4: APODEX WORLDMODEL                                |
|   (Causal Graphs, Bayesian Belief Updates, Counterfactual Planning)            |
+-------------------------------------------------------------------------------+
                                       |
                                       | UncertaintyGap & Epistemic Feedback
                                       +----------------------------------------> (Loop back to Layer 1)
```

---

### 2. State-Handoff Data Schemas

#### Layer 1 -> Layer 2 Handoff Schema (`ResearchHypothesis`)
```python
class ResearchHypothesis(BaseModel):
    hypothesis_id: str
    paper_id: str
    title: str
    extracted_principle: str
    target_subsystem: str  # "EIOS", "EOS", "AEAN", "APODEX"
    confidence_score: float  # [0.0, 1.0]
    p_value: float  # Must be < 0.01 for validation
    status: str  # "draft", "validated", "active", "rejected"
```

#### Layer 2 -> Layer 3 Handoff Schema (`TaskOpportunity`)
```python
class TaskOpportunity(BaseModel):
    opportunity_id: str
    source_hypothesis_id: str
    required_capability: str
    priority_score: float
    token_budget: float
    efe_score: float  # Epistemic + Pragmatic Value
    dag_definition: Dict[str, Any]
```

#### Layer 3 -> Layer 4 Handoff Schema (`ExecutionOutcome`)
```python
class ExecutionOutcome(BaseModel):
    execution_id: str
    task_id: str
    winning_agent_id: str
    status: str  # "success", "failed"
    performance_metrics: Dict[str, float]
    telemetry_logs: List[str]
```

#### Layer 4 -> Layer 1 Handoff Schema (`UncertaintyGap`)
```python
class UncertaintyGap(BaseModel):
    gap_id: str
    causal_node_id: str
    epistemic_uncertainty: float
    variance: float
    recommended_topic: str
```
