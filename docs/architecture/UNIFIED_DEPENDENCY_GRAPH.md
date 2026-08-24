# Unified Cognitive System Dependency Graph & Data Flow Schemas

## System Interaction Flow Architecture

```
                                  [ RESEARCH OS ]
                          (Layer 1: Research Layer)
                                      │
                         Hypothesis & Causal Priors
                                      │
                                      ▼
                                [ EOS / EIOS ]
                   (Layer 2: Orchestration & Decision Layer)
                                      │
                       Active Inference Policy & Goals
                                      │
                                      ▼
                                   [ AEAN ]
                   (Layer 3: Cognitive Intelligence Layer)
                                      │
                      Tool Execution & Skill Invocation
                                      │
                                      ▼
                                  [ APODEX ]
                    (Layer 4: Execution & Platform Layer)
```

---

## 1. Explicit Data Contracts Between Layers

### Contract 1.2: Layer 1 (Research OS) -> Layer 2 (EOS/EIOS)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ValidatedHypothesisPayload",
  "type": "object",
  "properties": {
    "hypothesis_id": { "type": "string" },
    "paper_id": { "type": "integer" },
    "principle_name": { "type": "string" },
    "p_value": { "type": "number", "maximum": 0.05 },
    "effect_size_cohen_d": { "type": "number" },
    "causal_dag_nodes": { "type": "array", "items": { "type": "string" } },
    "causal_dag_edges": { "type": "array", "items": { "type": "array" } }
  },
  "required": ["hypothesis_id", "paper_id", "p_value", "effect_size_cohen_d"]
}
```

### Contract 2.3: Layer 2 (EOS/EIOS) -> Layer 3 (AEAN)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ActiveInferenceDirective",
  "type": "object",
  "properties": {
    "directive_id": { "type": "string" },
    "target_goal": { "type": "string" },
    "efe_score": { "type": "number" },
    "epistemic_weight": { "type": "number" },
    "pragmatic_weight": { "type": "number" },
    "resource_budget_tokens": { "type": "integer" },
    "timeout_seconds": { "type": "number" }
  },
  "required": ["directive_id", "target_goal", "efe_score", "resource_budget_tokens"]
}
```

### Contract 3.4: Layer 3 (AEAN) -> Layer 4 (APODEX)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ToolExecutionRequest",
  "type": "object",
  "properties": {
    "request_id": { "type": "string" },
    "agent_id": { "type": "string" },
    "skill_name": { "type": "string" },
    "parameters": { "type": "object" },
    "approval_tier": { "type": "integer", "enum": [0, 1, 2] }
  },
  "required": ["request_id", "agent_id", "skill_name", "parameters", "approval_tier"]
}
```

---

## 2. Dynamic Operational Cycles

1. **Epistemic Exploration Cycle**:
   - `ResearchOS` extracts new findings from `AI_EOS_RESEARCH_DB.yaml`.
   - Hypothesis validated via Holm-Bonferroni correction ($p < 0.05$).
   - `ResearchOS` broadcasts validated priors to `EOS/EIOS`.

2. **Goal & Policy Generation Cycle**:
   - `EOS/EIOS` calculates Expected Free Energy: $G(a) = \alpha \cdot \text{InformationGain} + \beta \cdot \text{PragmaticUtility}$.
   - Optimal policy emitted as `ActiveInferenceDirective` to `AEAN`.

3. **Cognitive Reasoning & Execution Cycle**:
   - `AEAN` dispatches task to agent swarm.
   - Graph-of-Thought (GoT) evaluates candidate paths.
   - Skill flywheel executes required tools via `APODEX`.

4. **Feedback & Learning Cycle**:
   - `APODEX` streams telemetry back to `AEAN` memory systems (CMOS).
   - Skill success rates and execution logs update Bayesian world model in `EOS/EIOS`.
