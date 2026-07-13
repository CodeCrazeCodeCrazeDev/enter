# Apodex Meta-System Architectural Specification: Self-Improving AI System

This document specifies the architecture, data flows, design patterns, safety guardrails, cost-awareness, and user-control layers for **Apodex**—the self-evolving meta-system that wraps, observes, and continually improves the Autonomous Economic Agent Network (AEAN).

---

## 1. Unified Architecture & High-Level Goal

Apodex is designed around a **dual-loop self-improvement cognitive architecture** working on top of the AEAN execution framework. The high-level goal of Apodex is to continuously drive both short-term (in-session/cross-session) and long-term (structural and algorithmic) adaptation:

```
                                +---------------------------+
                                |        Human User         |
                                +-------------+-------------+
                                              ^
                                              | (Task Requests, Feedback, CLI Commands)
                                              v
+---------------------------------------------+---------------------------------------------+
|                                     AEAN TASK RUNTIME                                     |
|                                                                                           |
|          +-------------------+       (Executes)        +-------------------+              |
|          |    Task Agents    |  -------------------->  |       Tools       |              |
|          +---------+---------+                         +---------+---------+              |
+--------------------|---------------------------------------------|------------------------+
                     | (Traces, Errors, Metrics)                   | (Logs, Outcomes)
                     v                                             v
+-------------------------------------------------------------------------------------------+
|                                    APODEX META-SYSTEM                                     |
|                                                                                           |
|   +-----------------------------------------------------------------------------------+   |
|   |                         Experience Database + Cognition Base                      |   |
|   |  - Trace Logs  - Failure Signatures  - Performance Metrics  - Distilled Lessons   |   |
|   |  - Research Tickets  - Capability Deltas  - Personal Evolution Profiles (PEPs)    |   |
|   +----------+----------------------------------------------------+-------------------+   |
|              | (Weakness Indicators)                              | (Performance Gaps)    |
|              v                                                    v                       |
|   +------------------------------------+       Triggers       +-----------------------+   |
|   |      Harness Loop Controller       |  ----------------->  | Research Controller   |   |
|   |  (System Prompts, Routing, Tools)  |                      | (Weights & Algos)     |   |
|   +------------------+-----------------+                      +-----------+-----------+   |
|                      |                                                    |               |
|                      | (Proposes Diffs)                                   | (Proposes SFT/|
|                      v                                                    |  RL / Weights)|
|   +------------------+-----------------+                                  v               |
|   |      Safety & Guardrail Manager    |                      +-----------+-----------+   |
|   |  - Diff Verification               |                      | Experiment Sandbox    |   |
|   |  - Regression Evaluation Gate      |                      | - Docker Execution    |   |
|   +------------------+-----------------+                      | - Strict Quotas       |   |
|                      |                                        +-----------+-----------+   |
|                      | (Deploys Verified)                                 |               |
|                      |                                                    | (Creates PR)  |
|                      v                                                    v               |
|            [Staging / Production]                              [Git-Based Pull Request]   |
|                                                                - Human-in-the-Loop Gate   |
+-------------------------------------------------------------------------------------------+
```

---

## 2. Personal Evolution Layer (PEP)

Apodex personalizes its evolution per user using the **Personal Evolution Profile (PEP)**. The PEP is a persistent, versioned data object representing a user's task distribution, historical workflow performance, style guidelines, and budget constraints.

### 2.1 PEP Schema Definition

```json
{
  "$schema": "https://apodex.ai/schemas/pep.v1.json",
  "user_id": "usr-9842",
  "version": 14,
  "last_updated": "2026-03-30T10:15:00Z",
  "typical_tasks": [
    {
      "domain": "coding",
      "frequency_weight": 0.6,
      "primary_languages": ["python", "typescript"]
    },
    {
      "domain": "math_reasoning",
      "frequency_weight": 0.3,
      "complexity": "high"
    },
    {
      "domain": "policy_analysis",
      "frequency_weight": 0.1
    }
  ],
  "evolution_history": {
    "effective_workflows": [
      {
        "task_domain": "coding",
        "workflow_id": "workflow_py_verification_v3",
        "improvement_ratio": 0.14
      }
    ],
    "effective_tools": ["python_compiler", "web_search"],
    "harness_edits_applied": ["prompt_json_strict_v2"]
  },
  "style_preferences": {
    "verbosity": "medium",
    "explanation_depth": "detailed",
    "citation_style": "inline_markdown",
    "exploration_mode": "balanced"
  },
  "cost_latency_preferences": {
    "profile_mode": "balanced",
    "max_cost_per_session_usd": 2.50,
    "latency_tolerance_sec": 45.0
  },
  "domain_vocabulary": {
    "Jules": "The core systems engineer agent responsible for verification.",
    "Apodex-H": "Heavy-duty solver mode leveraging multi-step reasoning trees.",
    "heavy-duty": "Tasks requiring deep mathematical analysis or code construction."
  },
  "evolution_controls": {
    "aggressiveness": {
      "coding": "Balanced",
      "math_reasoning": "Conservative",
      "policy_analysis": "Aggressive"
    },
    "pinned_behaviors": {
      "coding_style": "Do not modify the strict double-newline rule for coding formatting."
    }
  }
}
```

### 2.2 PEP Loading Sequence

At the initiation of any user session, the PEP is loaded as part of the execution context:

```
[User Session Starts] ──> [Fetch User ID] ──> [Query PEP Store] ──> [Compile Session Scaffolding]
```

1. **Query Store**: Retrieve the active PEP record from the persistent SQLite/NoSQL DB.
2. **Context Assembly**: The `HarnessLoopController` binds the style guidelines and domain vocabulary into the working configuration.
3. **Prompt Injection**: The loaded vocabulary mapping is appended to the system instructions to ensure proper interpretation of domain-specific terms (e.g., translating "heavy-duty" to invoke specific deep-reasoning agent ensembles).

### 2.3 PEP Update Lifecycle

The PEP is updated dynamically:
- **Immediate (Post-Task)**: After each task completes, the user satisfaction rating (e.g., thumbs up/down, edit distance of corrections) is evaluated alongside token and latency statistics. If a workflow successfully completes with lower-than-average latency, the workflow ID score is incremented.
- **Batch (End of Session)**: A background consolidation routine analyzes task clusters, extracts new domain terms used repeatedly by the user, and updates the `typical_tasks` frequency distribution.

### 2.4 PEP Execution Influence
- **System Prompt Initialization**: Style preferences (e.g., `citation_style`) and pinned behaviors are injected as structural rules into the system prompt.
- **Tool and Workflow Selection**: Workflows marked as highly effective for the current domain in PEP are automatically given higher routing priorities during planning.
- **Default Evolution Aggressiveness**: Tells the `HarnessLoopController` how fast to push changes. In "Conservative" domains, prompt modifications are blocked unless they show 100% success on the regression suite. In "Aggressive" domains, candidate changes can be shadow-tested live if they pass a 70% confidence threshold.

---

## 3. Transparent and User-Controllable Evolution

To ensure users remain in absolute control over how Apodex adapts, the platform introduces a comprehensive **Evolution Changelog**, **Control Panel**, and **One-Click Rollback** mechanism.

### 3.1 Evolution Changelog

All adjustments to prompts, routing, tools, or model weights are recorded in the changelog, which is auditable on demand or surfaced through gentle notification flags.

#### Changelog Schema

```json
{
  "changelog_id": "ev-log-1049",
  "timestamp": "2026-03-30T11:00:00Z",
  "change_type": "harness_prompt_update",
  "affected_capability": "coding_tool_use",
  "summary": "Added triple-backtick parsing validation rules to system prompt.",
  "metrics_before": {
    "success_rate": 0.88,
    "avg_tokens": 1420,
    "latency_seconds": 12.4
  },
  "metrics_after": {
    "success_rate": 0.96,
    "avg_tokens": 1250,
    "latency_seconds": 10.9
  },
  "context": "Prompt was edited automatically using TextGrad feedback in response to 3 consecutive markdown wrap exceptions."
}
```

### 3.2 Evolution Control Panel

Surfaced via CLI and GUI, this panel writes to the PEP:
- **Conservative Mode**: Updates are highly screened; requires manual PR merge.
- **Balanced Mode** (Default): Prompt changes are auto-approved; model weight changes require PR review.
- **Aggressive Mode**: Shadow deployments and prompt hot-swapping are fully automated.
- **Pinned Behavior**: Users can specify exact strings or behavioral constraints (e.g., `"Do not change how you do math processing"`) that the controllers are strictly forbidden from modifying.

### 3.3 One-Click Rollback

 Hoses can be rollbacked instantly if any performance degradation is observed.

#### API/CLI Examples

- Check the evolution log state:
  ```bash
  /evolution status
  ```
  *Output:*
  ```
  Active Scaffolding Version: v14.2
  Last modification: Added strict JSON instruction to Python compiler (Timestamp: 2026-03-30T11:00:00Z)
  Performance Delta: Success +8%, Latency -1.5s
  ```

- Rollback a specific capability to a previous version:
  ```bash
  /evolution rollback capability=coding version=2026-03-29T15:00:00Z
  ```

#### Internal Rollback Mechanics
1. **Reversion**: The `HarnessLoopController` extracts the historical configuration corresponding to the requested timestamp from the SQLite state ledger and hot-swaps it into active memory.
2. **Negative Signal Logging**: The rejected change configuration is marked as **blacklisted** in the `FailureSignature` store. The exact reason or trace that led to the rollback is clustered as a "user-rejected mutation".
3. **Blocking Re-proposals**: The evolution algorithm computes the semantic similarity of future candidate modifications against the blacklisted prompts; any proposed modification with >85% similarity is blocked automatically to prevent re-proposing rejected ideas.

---

## 4. Cost- and Latency-Aware Evolution

Self-improvement must not lead to exponential cost or resource inflation. Apodex embeds **Multi-Objective Cost-Aware Scoring** directly into both its loops.

### 4.1 Scoring Function

For any proposed modification $M$ (whether a prompt diff or a model-weights update), the overall suitability score $S(M)$ is computed as:

$$S(M) = w_q \cdot Q(M) - w_t \cdot T(M) - w_l \cdot L(M) + w_s \cdot Sat(M)$$

Where:
- $Q(M) \in [0, 1]$ is the task success/quality ratio evaluated against the regression suite.
- $T(M) \in [0, 1]$ is the normalized token volume ratio (candidate tokens vs. baseline).
- $L(M) \in [0, 1]$ is the normalized latency ratio (candidate runtime vs. baseline).
- $Sat(M) \in [0, 1]$ is the user satisfaction metric (reconstructed from thumbs up, edit distance, and task success history).
- $w_q, w_t, w_l, w_s$ are weight parameters.

#### Pseudocode Implementation

```python
def calculate_multi_objective_score(
    quality: float,        # 0.0 to 1.0 (test success rate)
    token_ratio: float,    # candidate_tokens / baseline_tokens
    latency_ratio: float,  # candidate_latency / baseline_latency
    satisfaction: float,   # 0.0 to 1.0 (user satisfaction)
    profile_mode: str      # 'max_quality', 'balanced', 'fast_cheap'
) -> float:
    # 1. Define default weights
    weights = {
        "max_quality": {"wq": 0.70, "wt": 0.05, "wl": 0.05, "ws": 0.20},
        "balanced":    {"wq": 0.40, "wt": 0.20, "wl": 0.20, "ws": 0.20},
        "fast_cheap":  {"wq": 0.15, "wt": 0.45, "wl": 0.30, "ws": 0.10}
    }

    w = weights.get(profile_mode, weights["balanced"])

    # 2. Compute score components (penalize ratio increases above 1.0)
    token_penalty = max(0.0, token_ratio - 1.0)
    latency_penalty = max(0.0, latency_ratio - 1.0)

    score = (
        w["wq"] * quality -
        w["wt"] * token_penalty -
        w["wl"] * latency_penalty +
        w["ws"] * satisfaction
    )
    return score
```

### 4.2 Cost Profile Constraints

- **`max_quality`**: Prioritizes logical capability. Acceptable token ratio up to $2.5\times$ (e.g., branching MCTS or large coordinator ensembles).
- **`balanced`**: Allows up to $1.2\times$ token or latency increases only if they yield at least a corresponding $+10\%$ quality improvement.
- **`fast_cheap`**: Enforces a strict ceiling on costs. Any proposed harness edit that expands token length by $>5\%$ or adds a tool step is automatically discarded.

### 4.3 Practical Example: Routing Upgrade
An upgrade is proposed that wraps coding task execution in a triple-pass verifier loop:
- **Impact**: Quality $Q$ improves from $82\%$ to $90\%$. Latency $L$ increases by $150\%$ (ratio = 2.50). Token volume $T$ increases by $180\%$ (ratio = 2.80).
- **Evaluation**:
  - Under `max_quality`: The quality improvement and satisfaction override the penalties. Score remains positive. **Change is accepted**.
  - Under `fast_cheap`: The heavy token penalty ($0.45 \times 1.80 = 0.81$) and latency penalty ($0.30 \times 1.50 = 0.45$) completely dominate. Score becomes deeply negative. **Change is rejected**.

---

## 5. Hardened Safety: Immutable Core + Tiered Approval

To protect system integrity, Apodex partitions its operating configuration into an **Immutable Safety Core** and enforces a strict **Tiered Approval System**.

```
  +-------------------------------------------------------------+
  |                   IMMUTABLE SAFETY CORE                      |
  |  - Harm & Privacy Prompts   - Access Control & Tenancy      |
  |  - Critical Audit Logs      - Read-Only Configuration Store |
  +-------------------------------------------------------------+
                                 |
                                 v
  +-------------------------------------------------------------+
  |                   TIERED APPROVAL GATEWAY                   |
  |  [Tier 1: Auto]  ──> [Tier 2: Shadow]  ──> [Tier 3: Git PR] |
  +-------------------------------------------------------------+
```

### 5.1 Immutable Safety Core

Safety and security configurations are marked with `immutable: true` properties and stored in a read-only filesystem partition or protected database tables. These cannot be modified by any automated agent or execution loop.
- **Harm/Bias Policies**: Prompts governing ethical alignment and system safety.
- **Data Boundary Rules**: Tenant-isolation and database access controls.
- **Audit Logging Pipelines**: The components that report token, cost, and trace metrics.

### 5.2 Tiered Approval Policy Table

| Tier | Change Type | Approval Path | Requirement & Benchmarks |
| :--- | :--- | :--- | :--- |
| **Tier 1** | Tiny harness tweak (prompt text edit, minor routing value) | **Auto-Approve** | Run fast regression suite (100% success on cached tasks). |
| **Tier 2** | New tool definition or major workflow routing rewrite | **Shadow Mode** | Deploy in parallel "shadow mode" for 100 runs. Auto-promote if quality score is superior and zero errors occur. |
| **Tier 3** | Model architecture, weights, or training setup change | **Git Pull Request** | Run comprehensive benchmark suite (MMLU, HumanEval, MATH). Human engineer merge of PR required. |
| **Tier 4** | Anything touching safety policies or tenancy rules | **Multi-Party Gate** | Blocked for automation. Requires explicit manual cryptographic keys and multi-party sign-off. |

Every approval decision, including the specific tester agent, validation metrics, approval path, and timestamp, is cryptographically hashed and logged to the permanent auditing ledger.

---

## 6. Tight Harness–Research Feedback Loop

The Harness Loop and the Research Loop do not operate in isolation. They communicate explicitly through two structured artifacts: **Research Tickets** and **Capability Deltas**.

```
  +──────────────────────+                     +──────────────────────+
  | Harness Loop (Fast)  | ── Research Ticket ─> Research Loop (Slow) |
  | - Mines prompt/tool  |                     | - Computes recipes   |
  |   level bottlenecks  | <─ Capability Delta ─ - Runs sandbox trials  |
  +──────────────────────+                     +──────────────────────+
```

### 6.1 Research Tickets (Harness ──> Research)

Generated when the Harness Loop identifies a persistent error pattern that prompt optimizations or workflow rewrites fail to solve (e.g., repeated logic loops or failure of the base model to handle multi-step reasoning).

#### Research Ticket Schema

```json
{
  "ticket_id": "RT-2026-0042",
  "created_at": "2026-03-30T12:00:00Z",
  "failure_pattern": "Multi-hop causal reasoning fails on 3+ step chains in physical logic tasks.",
  "example_traces": [
    "tr-math-9042",
    "tr-math-9831"
  ],
  "user_impact": "high",
  "harness_attempts": [
    {
      "change": "Added step-by-step decomposition prompt guidelines",
      "result": "no_improvement"
    },
    {
      "change": "Added validation sub-agent",
      "result": "marginal_improvement"
    }
  ],
  "suggested_direction": "weight_level_reasoning_upgrade_via_sft"
}
```

#### Ticket Ingestion & Prioritization
1. **Creation**: When the `HarnessLoopController` records a failure signature with $>5$ occurrences and $0\%$ recovery after 3 distinct prompt mutation attempts, a ticket is generated.
2. **Prioritization**: The `ResearchController` ranks tickets by combining `user_impact` with frequency metrics. High-priority tickets trigger the generation of custom fine-tuning SFT recipes.

### 6.2 Capability Deltas (Research ──> Harness)

When the `ResearchLoopController` successfully completes a sandbox model training trial and promotes the new weights, it publishes a **Capability Delta** to the `HarnessLoopController`.

#### Capability Delta Schema

```json
{
  "model_version": "Apodex-1.1-math-beta",
  "released_at": "2026-03-30T15:00:00Z",
  "capabilities_delta": {
    "improved": ["multi-step math", "causal reasoning"],
    "unchanged": ["code synthesis", "browsing"],
    "regressed": []
  },
  "recommended_harness_changes": [
    "Enable math_verification_workflow_v2 when math_confidence < 0.8",
    "Route Python tasks to new_code_agent_v3"
  ]
}
```

#### Harness Integration & Regression Handling
1. **Scaffolding Update**: The `HarnessLoopController` consumes the delta and automatically modifies its routing schemas to point relevant mathematical tasks to the upgraded model endpoint.
2. **Regression Watchdog**: If a user's PEP metrics for "code synthesis" show a drop of $>5\%$ post-deployment, the watchdog instantly triggers a rollback of the model endpoint for that specific user's PEP, falling back to the previous stable model version.

---

## 7. Implementation Roadmap (Phased)

The implementation of the five Apodex upgrades is scheduled across four sequential, low-risk, and completely backward-compatible phases:

### Phase 1: Personalization Foundation
- **Deliverables**:
  - Implement `PersonalEvolutionProfile` schema, SQLite persistence layer, and session initialization hooks.
  - Implement basic experience tracking storing typical user task frequencies.

### Phase 2: User Control & Cost Profiles
- **Deliverables**:
  - Build the Evolution Changelog ledger and command-line `/evolution rollback` utilities.
  - Integrate multi-objective scoring calculations and hook PEP cost mode preferences (`max_quality`, `balanced`, `fast_cheap`) into active harness decisions.

### Phase 3: Hardened Safety & Immutable Core
- **Deliverables**:
  - Deploy the `SafetyGuardrailManager` featuring strict immutable configuration checks.
  - Establish the Tiered Approval pipeline (Tier 1 to Tier 3 gates) protecting safety-critical systems.

### Phase 4: Full Closed-Loop Feedback Integration
- **Deliverables**:
  - Establish the automated generation and ingestion of `ResearchTicket` and `CapabilityDelta` schemas.
  - Integrate the fast harness adaptation loop and slow research container trials in a unified production-grade feedback loop.

---

## 8. Concrete Worked Examples

### 8.1 User Personal Evolution Profile (PEP) Example

#### Profile: High-Value Systems Architect
```json
{
  "$schema": "https://apodex.ai/schemas/pep.v1.json",
  "user_id": "usr-arch-77",
  "version": 4,
  "last_updated": "2026-03-30T14:30:00Z",
  "typical_tasks": [
    {
      "domain": "coding",
      "frequency_weight": 0.8,
      "primary_languages": ["python"]
    }
  ],
  "evolution_history": {
    "effective_workflows": [
      {
        "task_domain": "coding",
        "workflow_id": "workflow_py_compiler_v2",
        "improvement_ratio": 0.18
      }
    ],
    "effective_tools": ["python_compiler"],
    "harness_edits_applied": ["prompt_strict_docstring"]
  },
  "style_preferences": {
    "verbosity": "low",
    "explanation_depth": "concise",
    "citation_style": "none",
    "exploration_mode": "direct"
  },
  "cost_latency_preferences": {
    "profile_mode": "fast_cheap",
    "max_cost_per_session_usd": 1.00,
    "latency_tolerance_sec": 15.0
  },
  "domain_vocabulary": {
    "Jules": "The system verification manager.",
    "Apodex-H": "Heavy-duty python compilation mode."
  },
  "evolution_controls": {
    "aggressiveness": {
      "coding": "Balanced"
    },
    "pinned_behaviors": {
      "docstring_format": "Always write docstrings using Google style format."
    }
  }
}
```

---

### 8.2 Harness Change Lifecycle Example

#### 1. Proposed Change
- **Target**: `usr-arch-77` standard coding prompt configuration.
- **Diff proposed**: Add automated typing verification rules.
  ```diff
  <<<<<<< BEFORE
  You are a coding assistant. Write clean python code.
  =======
  You are a coding assistant. Write clean python code.
  CRITICAL: Always include python type hints for all function arguments and return values.
  >>>>>>> AFTER
  ```

#### 2. Evaluation
- **Regression suite run**: Passed 100%.
- **Token Ratio**: 1.01 (negligible prompt size increase).
- **Latency Ratio**: 1.00.
- **Estimated Quality**: +4% typing correctness.
- **Calculated Score (under `fast_cheap` profile)**:
  $$S = (0.15 \times 0.04) - (0.45 \times 0.01) - 0.0 + (0.10 \times 1.0) = 0.006 - 0.0045 + 0.1 = 0.1015 \quad (\text{Positive})$$

#### 3. Decision & Log
- **Decision**: Deployed (Hot-swapped into memory).
- **Changelog Entry**:
  ```json
  {
    "changelog_id": "ev-log-1050",
    "timestamp": "2026-03-30T14:40:00Z",
    "change_type": "harness_prompt_update",
    "affected_capability": "coding_type_hints",
    "summary": "Added strict python type hint instruction to system prompt.",
    "metrics_before": { "success_rate": 0.91, "avg_tokens": 1100, "latency_seconds": 8.2 },
    "metrics_after": { "success_rate": 0.95, "avg_tokens": 1111, "latency_seconds": 8.2 }
  }
  ```

---

### 8.3 Ticket & Delta Evolution Round-Trip Example

#### 1. Research Ticket Generation (Harness ──> Research)
The coding assistant repeatedly fails to compile complex multi-agent event dispatching routines. Prompt edits have failed to resolve this.
```json
{
  "ticket_id": "RT-2026-0043",
  "created_at": "2026-03-30T15:00:00Z",
  "failure_pattern": "Failed to compile multi-agent event loop dispatching structures due to asynchronous thread-safety logic errors.",
  "example_traces": ["tr-async-8042", "tr-async-8099"],
  "user_impact": "high",
  "harness_attempts": [
    { "change": "Instructed model to use asyncio.Lock()", "result": "no_improvement" }
  ],
  "suggested_direction": "SFT fine-tuning on safe concurrent asyncio paradigms"
}
```

#### 2. Research Loop Model Upgrade (Sandbox Experiment)
The `ResearchController` ingests `RT-2026-0043`. It extracts 200 high-quality asyncio event-dispatching patterns and executes a LoRA fine-tuning trial.
- **Trial**: `trial_lora_async_04`
- **Result**: MATH and general coding benchmarks pass. Asyncio thread-safety compiling success rate jumps by $+32\%$.

#### 3. Capability Delta (Research ──> Harness)
Upon validation, the model weights are promoted. The following delta is dispatched to the `HarnessLoopController`:
```json
{
  "model_version": "Apodex-1.1-async-v2",
  "released_at": "2026-03-30T18:00:00Z",
  "capabilities_delta": {
    "improved": ["asynchronous python compiling", "event dispatching logic"],
    "unchanged": ["standard coding", "math_reasoning"],
    "regressed": []
  },
  "recommended_harness_changes": [
    "Route all tasks containing 'asyncio' or 'event loop' keyword queries to Apodex-1.1-async-v2 model endpoint."
  ]
}
```

#### 4. Harness Adjustment
The `HarnessLoopController` parses the recommended changes and instantly updates its routing tables. Any subsequent asynchronous coding requests from `usr-arch-77` are seamlessly dispatched to the new `Apodex-1.1-async-v2` model, successfully resolving the persistent compilation errors.
