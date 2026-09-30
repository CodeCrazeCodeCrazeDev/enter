# Unified Cognitive Operating System Dependency Graph & Interface Contracts
**Author:** Strategic Architecture Lead & AI Engineering Core
**Version:** 4.0.0 (2026 Sovereign Edition)

---

## 1. System Interaction Topology

The 4-layer architecture operates with strictly monotonic control flow downwards (Plan & Execute) and state/event feedback flow upwards (Observe & Learn).

```
+-----------------------------------------------------------------------+
|                       LAYER 1: RESEARCH OS                            |
|  - Paper Corpus Ingestion (IDs 1-600+)                                |
|  - Statistical Validation (DSR, Hawkes Non-Gaussian, AST Inspection)  |
|  - ResearchToSystemBridge Hypothesis Registration                     |
+-----------------------------------------------------------------------+
                                   |
                         (ResearchHypothesis)
                                   v
+-----------------------------------------------------------------------+
|                       LAYER 2: EIOS / EOS KERNEL                      |
|  - Active Inference DAG Compiler & Scheduler                          |
|  - Entrepreneurial Opportunity Tree & Capital Allocator               |
|  - Expected Free Energy (EFE) Expected Loss Minimizer                 |
+-----------------------------------------------------------------------+
                                   |
                           (EIOSDAGTaskNode)
                                   v
+-----------------------------------------------------------------------+
|                       LAYER 3: AEAN HIVEMIND                          |
|  - Token Economy Bidding Registry (HiveMind.bid_for_task)             |
|  - Multi-Agent Specialization Swarms (Coder, Proof, Risk, Architect)  |
|  - Graph-of-Thought (GoT) Reasoning & Code Synthesis                  |
+-----------------------------------------------------------------------+
                                   |
                      (ExecutionResultArtifact)
                                   v
+-----------------------------------------------------------------------+
|                       LAYER 4: APODEX WORLD MODEL                     |
|  - Causal Bayesian Graph (CausalNode, RelationEdge)                   |
|  - Recursive Bayesian Belief Propagation (BayesianBelief)             |
|  - Cognitive Brain & Safety/Governance Controller                     |
+-----------------------------------------------------------------------+
                                   |
                     (StateAnomaly / WorldModelDelta)
                                   v
             [ Feedback Loops to Layer 1 and Layer 2 ]
```

---

## 2. Strong Interface Contracts & Python Data Models

### Layer 1 -> Layer 2 Contract: `ResearchHypothesis`
```python
class ResearchHypothesis(BaseModel):
    hypothesis_id: str
    paper_title: str
    principle_name: str
    target_subsystem: Literal["AEAN", "EOS", "EIOS", "ResearchOS", "APODEX"]
    mathematical_proof_summary: str
    validation_status: Literal["proposed", "validated", "active", "rejected"]
    confidence_score: float = Field(ge=0.0, le=1.0)
    impl_module: str
```

### Layer 2 -> Layer 3 Contract: `EIOSDAGTaskNode`
```python
class EIOSDAGTaskNode(BaseModel):
    task_id: str
    hypothesis_id: str
    action_type: str
    expected_free_energy: float
    pragmatic_value: float
    epistemic_value: float
    required_specialization: str
    token_budget: float
    timeout_seconds: float = 30.0
```

### Layer 3 -> Layer 4 Contract: `ExecutionResultArtifact`
```python
class ExecutionResultArtifact(BaseModel):
    task_id: str
    agent_id: str
    status: Literal["success", "failure", "halted"]
    code_diff: Optional[str] = None
    observed_metrics: Dict[str, float]
    causal_updates: List[Dict[str, Any]]
    belief_delta: float
    execution_time_ms: float
```

### Layer 4 -> Layer 1/2 Feedback Contract: `StateAnomaly`
```python
class StateAnomaly(BaseModel):
    anomaly_id: str
    source_subsystem: str
    divergence_magnitude: float
    causal_node_affected: str
    suggested_hypothesis_query: str
    timestamp: float
```

---

## 3. Strict Non-Overlapping Zero-Duplication Policy

1. **No Duplicated Task Schedulers:** AEAN does NOT schedule system-wide workflows; scheduling is exclusively Layer 2's responsibility. AEAN only schedules internal agent sub-steps within its allocated task graph node.
2. **No Duplicated World Models:** Neither Research OS nor AEAN maintains a independent causal model. All causal states and Bayesian beliefs reside strictly in Layer 4 (`APODEX WorldModel`).
3. **No Duplicated Research Repositories:** Paper corpus principles and statistical hypothesis tools reside strictly in Layer 1 (`Research OS`).
