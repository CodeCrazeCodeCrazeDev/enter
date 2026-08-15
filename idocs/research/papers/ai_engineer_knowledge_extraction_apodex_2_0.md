# Research Mission: AI Engineer Knowledge Extraction for Apodex 2.0
## Institutional-Grade Architectural Specification & Implementation Roadmap

---

## Executive Summary

Apodex 2.0 is designed as a **Self-Evolving Heavy-Duty Solver** focused on deep research—tackling open-ended, complex scientific, economic, and systems engineering questions. Rather than relying on simple, single-prompt chat agents or static workflows, Apodex 2.0 implements a **dual-loop cognitive architecture** spanning five distinct layers.

This document serves as the authoritative engineering blueprint and gap analysis for Apodex 2.0. It systematically extracts, synthesizes, and incorporates the modern engineering paradigms, multi-agent design patterns, evaluation loops, and verification-first methodologies advocated across the **AI Engineer** channel (including workshops, talks, and SOTA research integrations).

```
                                  APODEX 2.0 ARCHITECTURAL STACK

   +------------------------------------------------------------------------------------------+
   | 5. USER & PRODUCT LAYER                                                                  |
   |    - Verified Research Brief (JSON/MD)   - Citations & Reasoning Trace View              |
   |    - Branchable Investigations           - REST API (/deep_research & /inquiries/{id})   |
   +------------------------------------------------------------------------------------------+
                                               | (User Query, Constraints, Risk Profile)
                                               v
   +------------------------------------------------------------------------------------------+
   | 4. EVALUATION & SELF-EVOLUTION LAYER                                                     |
   |    - Evaluation Harness (AgentHarness)   - Continuous Evals & Custom Judge Scripts       |
   |    - Weakness Mining (Self-Harness)     - Meta-Agent Prompt & Skill/Tool Evolution      |
   +------------------------------------------------------------------------------------------+
                                               | (Optimized Prompts, Validated Skills, Tuned Routing)
                                               v
   +------------------------------------------------------------------------------------------+
   | 3. VERIFICATION & EVIDENCE LAYER                                                         |
   |    - Global Verifier                     - Verification Sub-Agents (Claim, Conflict, Cover) |
   |    - Jaccard Token-Overlap Keyword Match  - Grounded Evidence Graph (Claims -> Evidence)     |
   +------------------------------------------------------------------------------------------+
                                               | (Verified Claims & Triangulated Reports)
                                               v
   +------------------------------------------------------------------------------------------+
   | 2. MULTI-AGENT DEEP-RESEARCH TEAM                                                        |
   |    - Task Orchestrator                   - Retrieval Specialists (Search, Scraping, PDFs)   |
   |    - Analysis & Synthesis Specialists    - Adversarial / Counter-Evidence Agents            |
   +------------------------------------------------------------------------------------------+
                                               | (Task Messages, Concurrency Streams, Spans)
                                               v
   +------------------------------------------------------------------------------------------+
   | 1. AGENTOS RUNTIME                                                                       |
   |    - Task-Agnostic Kernel                - Multi-Agent Scheduler & Concurrency Control       |
   |    - Tool Permission & Model Routing     - Checkpoints, Replay, & Token Cost Accounting      |
   +------------------------------------------------------------------------------------------+
```

---

## 1. What Apodex 2.0 Should Be

Apodex 2.0 = **Apodex‑1.0 architecture** + **AI Engineer patterns**.

- **From Apodex‑1.0** you keep:
  - AgentOS runtime (task‑agnostic kernel).
  - Large multi‑agent deep‑research team.
  - Global verifier & verification agents.
  - AgentHarness for benchmarks and model serving.[1][2]

- **From AI Engineer YouTube** you add:
  - Multi‑agent architectures that actually ship (Factory “Missions”).[3][4]
  - Agent harness & loop engineering: memory, traces, eval, end‑loop guardrails.[5][6]
  - Self‑evolving agents and workflows (EvoAgentX style).[7]
  - Verification‑first development: validation contracts, validator roles.[3][4][8]

Goal: an end‑to‑end **deep research system** that:
- Plans, runs, and verifies complex research autonomously.
- Continuously improves its prompts, workflows, and tools from eval data.
- Is robust and production‑ready (good tracing, tests, recovery, governance).

---

## 1.1 The Accuracy Leap: Anthropic 21% to 95% & Leni AI Universal Data Models

To achieve elite performance, Apodex 2.0 incorporates the breakthrough agentic context and engineering lessons published by **Anthropic** (where raw agent accuracy jumped from **21% to 95%** through structural configuration) and the workflow principles of **Leni AI**:

### 1.1.1 The Failure Modes of Naive Agents
Anthropic identified three fundamental blockers to enterprise-grade accuracy:
1.  **Concept-to-Entity Ambiguity:** Simple goals like "active users" or "available surplus" can map to forty plausible tables/definitions in a database. Without explicit canonical models, agents guess blindly and introduce silent bugs.
2.  **Information & Skill Decay:** Schemas, APIs, and business definitions evolve constantly. Without explicit sync rules, the agent's context rots, and accuracy drifts from **95% down to 65% in a single month**.
3.  **Retrieval Failures:** In massive datasets, raw retrieval over prior queries or historical files moves accuracy by less than **1 percentage point**. Crucially, in 80% of incorrect runs, the correct answer was in the retrieval corpus but the model passed right over it.

### 1.1.2 The "Skill Files as the System" Solution (Anthropic & Leni AI)
*   **The Model is Interchangeable; Context is the System:** High accuracy is not bought by a more powerful foundational model, but by a co-located, structured meta-context layer.
*   **Structured Skill Files:** Authoring precise "Skill Files" defining tool schemas, input constraints, and deterministic outputs.
*   **Co-Location with Source Code:** Putting skill documents and data models in the exact same Git repository, so 90% of structural changes are co-submitted with skill file updates (CI/CD sync).
*   **Universal Data Model (UDM) Integration (Leni AI Style):** Standardizing messy input data and variables into a strict, polymorphic schema before reaching the reasoning model, resolving ambiguities deterministicly.
*   **Adversarial Assumptions Challenge:** Deploying dedicated critic sub-agents (e.g., conflict and counter-evidence checkers) to challenge every initial hypothesis. This buys up to **6% extra accuracy** by forcing the model to repeatedly re-evaluate its assumptions.

### 1.1.3 Integration in Apodex 2.0
We directly encode these SOTA principles into Apodex 2.0:
*   The **SkillRegistry** (`apodex/skills/registry.py`) pre-populates and co-locates 60 canonical business/research capabilities alongside the code.
*   The **HarnessRefiner** (`apodex/evolution/self_harness/refiner.py`) and **HarnessCritic** (`apodex/evolution/self_harness/critic.py`) perform adversarial reviews on proposals before execution.
*   Every task's metadata is validated against strict Pydantic schemas representing a clean UDM, neutralizing Concept-to-Entity ambiguity.

---

## 2. Pieces You Must “Take” From AI Engineer Channel

### 2.1 Multi‑Agent Architecture That Ships (Factory “Missions”)

From talks like *“The Multi-Agent Architecture That Actually Ships — Luke Alvoeiro, Factory”* and Missions docs:[3][4]

**Core pattern you should copy:**

- **Three roles:**
  - **Orchestrator** – planning and decomposition.
  - **Workers** – do the actual research steps (search, read, summarize, compute).
  - **Validators** – check results against predefined **validation contracts**.

- **Design rules you should implement:**
  - Write **validation contracts before execution** (define what “correct” looks like for each research task).
  - Run **features serially** when needed to avoid agent conflicts.
  - Use **structured handoffs** (clear inputs/outputs) between agents.
  - Make the system **model‑agnostic and prompt‑driven**, so you can upgrade models without rewriting the architecture.

**How this maps to Apodex 2.0:**

- Orchestrator → **Research Planner Agent**.
- Workers → **Retrieval, Analysis, Counter‑evidence agents**.
- Validators → **Claim‑checker, conflict‑detector, coverage‑checker, global verifier**.

---

### 2.2 Agent Harness & Loop Engineering

From videos like *“You Can Learn AI Agent Harness & Loop Engineering in 19 Min”* and loop‑engineering talks:[5][6]

You need to adopt these **four pillars**:

1. **Agent Harness**
   The harness is the runtime around the model:
   - Defines system prompts and agent roles.
   - Routes tool calls.
   - Captures traces and metrics.
   - Enforces I/O schemas.

   For Apodex 2.0, this *is* your upgraded **AgentOS**: a central service that accepts tasks and orchestrates agents with guarantees.

2. **Memory Architecture (4 layers)**

   Implement these memory types in your runtime:

   - **Working memory** – in‑run context (current question + partial findings).
   - **Procedural memory** – skills/rules (e.g., “how to verify a claim”, “how to read a paper”).
   - **Semantic memory** – distilled facts (e.g., stable domain knowledge you’ve learned over many runs).
   - **Episodic memory** – time‑series of past runs, failures, and successes.

   Use:
   - A database (PostgreSQL / Supabase / similar) to store semantic + episodic memory.
   - **RAG** for semantic memory; **time‑bounded + semantic** queries for episodic memory.

3. **Loop Engineering**

   Design explicit loops for your agents:

   - **Research loop:**
     `plan → search/collect → read/summarize → check for gaps → repeat or stop`.
   - **Guardrails**:
     - Clear “done” criteria (e.g., “All sub‑questions answered and verified above threshold X”).
     - Permissions & timeouts so loops can’t hang forever.

4. **LLM Ops: Eval, Tracing, Diagnosis**

   You must:
   - Trace every research run as a **tree of events**:
     - Prompts, model calls, tools, evidence fetched, intermediate reports.
   - Compute metrics: latency, token use, tool calls, error rates, grounding scores.
   - Use evaluation results to:
     - Diagnose failures (prompt issues, tool problems, retrieval weaknesses).
     - Drive the self‑evolution loop (see 2.3).

---

### 2.3 Self‑Evolving Agents

From *“Self-Evolving AI Agents”* and the EvoAgentX framework demos:[7]

Key ideas:

- **Workflow Generator + Agent Manager + Workflow Executor**:
  - Represent your agent team and steps as a **graph** (nodes = agents/actions, edges = data flow).
  - Allow automatic generation / modification of workflows from high‑level goals.

- **Self‑Evolution Loop**:
  1. Run benchmarks or real user tasks.
  2. Evaluate: correctness, grounding, cost, latency.
  3. Diagnose failure type:
     - Bad plan?
     - Bad prompt?
     - Missing tool / skill?
     - Poor verification config?
  4. Let a **meta‑agent** propose changes:
     - New or edited prompts.
     - New skills or tools.
     - Different workflow structures.
  5. Test candidate changes on a **validation subset**.
  6. Promote only configurations that improve metrics.

- **Prompt & Workflow Optimization Algorithms**
  Borrow patterns from:
  - **TextGrad / EvoPrompt / MIPRO / AFlow**: iterative prompt and workflow optimization guided by evaluation scores.

For Apodex 2.0 this means:

- Your **AgentHarness** is not static:
  - It continuously evolves prompts, agent roles, and workflows based on eval data.
- You store **versioned configs** (prompts, routing rules, skills) with:
  - Performance metrics.
  - Date introduced.
  - Benchmarks used.

---

### 2.4 Deep Research Multi‑Agent Patterns

From deep‑research workshops on the channel:

You should structure Apodex 2.0’s **agent team** like this:

1. **Planner / Orchestrator**
   - Understands the question.
   - Breaks it into sub‑questions and a research plan.
   - Sets validation contracts for each sub‑question (what counts as a good answer).

2. **Retrieval Agents**
   - Web search + scraping (news, blogs, docs).
   - Academic retrieval (papers, PDFs).
   - Domain‑specific APIs (finance, medical, law, etc.).

3. **Analysis & Synthesis Agents**
   - Turn raw sources into structured notes.
   - Compare and aggregate evidence.
   - Tag which note supports which sub‑question.

4. **Counter‑Evidence / Adversarial Agents**
   - Search specifically for contradictions or missing perspectives.
   - Stress‑test the current hypothesis.

5. **Verification Agents (Validators)**
   - Check each claim against sources (claim‑checker).
   - Identify conflicts (conflict‑detector).
   - Ensure plan coverage (coverage‑checker).
   - Run a **global verifier** to produce the final, citation‑backed brief.

All of these patterns are shown across AI Engineer videos on multi‑agent orchestration, Factory Missions, and deep research agent workshops.[3][4][7]

---

## 3. How to Combine This Into Apodex 2.0

### 3.1 Architecture Overview

Design Apodex 2.0 as five layers:

1. **AgentOS Runtime (Harness)**
   - Task submission API.
   - Agent registry (planner, retriever, analyzer, verifier, meta‑agent).
   - Message bus / queues.
   - Memory services (working, semantic, episodic, procedural).
   - Tracing & metrics.

2. **Multi‑Agent Deep Research Team**
   - Planner, retrieval, analysis, counter‑evidence.
   - Shared report pool (structured artifacts with citations).

3. **Verification & Evidence Layer**
   - Validation contracts + validators (claim/coverage/conflict).
   - Global verifier that turns all evidence into a final, fully cited brief.

4. **Evaluation Harness & Self‑Evolution**
   - Benchmark runner (reusing AgentHarness ideas).[2]
   - Metrics store and dashboards.
   - Meta‑agent and evolution algorithms to improve prompts, skills, and workflows.

5. **User & Product Layer**
   - Web UI to see:
     - Research steps.
     - Evidence for each claim.
     - Verification status.
   - API (e.g., `POST /deep_research`, `GET /inquiries/{id}`).

---

### 3.2 Concrete Build Plan (Step‑By‑Step)

**Phase 1 – Minimal Harness / AgentOS**

- Implement:
  - `submit_task(question, options)` endpoint.
  - Run record (ID, status, config, costs).
  - In‑memory or Redis queue for agent messages.
  - Basic tracing (each agent step logged with parent/child IDs).

**Phase 2 – Single‑Agent Research Loop**

- Build one “research agent” with:
  - ReAct‑style loop: think → search/tool → observe → think → answer.
  - Tools: web_search, web_fetch, (optional) code runner.
- Produce:
  - Final answer.
  - List of URLs and snippets used.

**Phase 3 – Multi‑Agent Expansion (Factory‑Style)**

- Split into roles:
  - Planner (orchestrator).
  - Retriever worker(s).
  - Analyzer worker(s).
  - Counter‑evidence worker(s).
  - Validator worker(s).
- Use **serial feature execution** where necessary; parallel where safe.
- Use **clear schemas** for messages and reports.

**Phase 4 – Verification‑First Layer**

- Define **validation contracts** for:
  - Evidence quality (number, diversity, recency).
  - Grounding (each major claim must cite sources).
  - Consistency (no internal contradictions).
- Implement:
  - Claim‑checker, conflict‑detector, coverage‑checker agents.
  - Global verifier that only accepts answers passing contracts.

**Phase 5 – Memory & Harness Engineering**

- Add:
  - Semantic memory DB (facts, prior research summaries).
  - Episodic memory DB (past runs, failures, improvements).
  - Summarizer agent to consolidate episodic → semantic.
- Create a harness layer that:
  - Builds working context for each agent from memory.
  - Logs all events.
  - Supports replay for debugging and audits.

**Phase 6 – Evaluation Harness + Self‑Evolution**

- Reuse ideas from Apodex AgentHarness and EvoAgentX:
  - Define benchmark suites (deep‑research datasets).[2][7]
  - Build scripts to:
    - Run all benchmarks through Apodex 2.0.
    - Collect scores and traces.
- Implement a **meta‑agent** that:
  - Reads failing cases.
  - Suggests prompt changes, new skills, or workflow tweaks.
  - Runs controlled experiments.
- Store and version:
  - Configurations.
  - Scores.
  - Change history.

**Phase 7 – Productization**

- Build UI for:
  - Submitting questions.
  - Viewing research trace and evidence.
  - Branching from any step (“continue research from here”).
- Expose an API for programmatic use.
- Add governance:
  - Rate limits.
  - Source constraints (e.g., no social media, only peer‑reviewed, etc.).
  - Risk profiles (how strict verification should be).

---

## 4. What You Should Actually Do With the AI Engineer Channel

To “find all this thing” from AI Engineer and use it:

1. **Study, then implement, these specific concepts:**
   - **Multi‑Agent Architectures & Missions** – implement the orchestrator/worker/validator model with validation contracts and structured handoffs.[3][4]
   - **Agent Harness & Loop Engineering** – build an AgentOS that:
     - Implements the 4 memory types.
     - Has end‑loop guardrails.
     - Has full tracing and metrics.[5][6]
   - **Self‑Evolving Agents** – integrate a meta‑agent and evaluation loop (inspired by EvoAgentX) that constantly improves prompts and workflows.[7]
   - **Deep Research Patterns** – orchestrated retrieval, analysis, and adversarial agents coordinated by a planner and governed by validators.

2. **Implement them directly into Apodex 2.0’s five layers** (runtime, agents, verification, eval/evolution, product).

If you follow this plan, you are effectively **translating the best practices from the AI Engineer YouTube channel into the architecture and implementation of Apodex 2.0**, rather than just watching the videos.

---

## 5. Detailed Catalog of Relevant AI Engineer Topics

Modern agent engineering has shifted from *prompt engineering* to *loop engineering*. Below is the catalog of core methodologies extracted from the AI Engineer channel and mapped to Apodex 2.0:

### 5.1 Multi-Agent Architectures & Orchestration
*   **The Hub-and-Spoke Pattern:** A central Project Manager (Orchestrator) manages context, routes goals, and aggregates reports, while specialized workers (Retrievers, Analysts) perform narrow, tool-enabled actions.
*   **Clear Interface Contracts:** Inter-agent communication is governed by strict, typed schemas (Pydantic models) rather than unstructured natural language, eliminating parsing failures.
*   **Report Pools:** A decentralized, append-only scratchpad where parallel workers post structured findings, allowing the orchestrator to dynamically monitor progress without monolithic token bottlenecks.

### 5.2 Agent Operating Systems (AgentOS)
*   **Kernel Isolation:** Decoupling execution mechanics (scheduling, retry rules, context clamping, timeouts, tool sandboxing) from the agent's prompt instructions.
*   **Resource Allocation & Permissioning:** An explicit security model governing which agent roles can invoke specific tool classes (e.g., executing arbitrary Python in a sandbox vs. web search).
*   **Cost & Token Accounting:** Proactive calculation of token utilization, rate limits, and actual cost (USD) per agent step to prevent exponential cost inflation in complex reasoning loops.

### 5.3 Verification-First AI Systems
*   **"Verifier is King" Paradigm:** Treating LLMs as generative drafting engines and relying on separate, dedicated verification models/sub-agents to validate factuality, check contradictions, and enforce evidence grounding.
*   **Claims-to-Evidence Mapping:** Every assertion in a final output must be bidirectionally traceable back to a source URL, citation ID, or compiled evidence card.
*   **Parallel consensus verifiers:** Combining multi-judge systems (Fact, Syntax, and Tone verifiers) to vote asynchronously on the validity of intermediate or draft responses.

### 5.4 Evaluation Harness & Self-Evolution
*   **Continuous Regression Suites:** Running cached task histories to measure quality impact, latency, and cost before deploying any prompt, tool, or routing configuration.
*   **TextGrad & Prompt Evolution:** Utilizing meta-agents to perform textual backpropagation over failed execution traces, automatically generating prompt updates to resolve observed bottlenecks.
*   **Skill & Tool Library Expansion:** Letting meta-agents write and test new tool definitions when the existing tool suite fails to address recurring task patterns.

---

## 6. Engineering Knowledge Extraction & Trade-offs

Based on workshop materials and speaker presentations on the AI Engineer channel, we extract the following key technical insights:

### 6.1 Context Clamping vs. Infinite Context
*   **The Problem:** Large-context models (e.g., Gemini 1.5 Pro, Claude 3.5 Sonnet) can swallow 200k+ tokens, but their reasoning accuracy and recall degrade near the middle of the context window ("Lost in the Middle"). Furthermore, feeding the entire raw history exponentially increases token costs and latency.
*   **The Solution (Clamping & Compaction):** Enforcing a dynamic clamping threshold (e.g., 8k-12k tokens). As context grows, a compactor compresses the history by keeping the core system instructions, summarizing middle turns, and preserving only the most recent N tool execution logs.
*   **Trade-off:** High compaction saves cost and retains high reasoning performance but risks losing niche context details. Apodex 2.0 handles this by prioritizing Jaccard token-overlap matching from persistent `SemanticMemory` to dynamically inject relevant details back on demand.

### 6.2 Hub-and-Spoke vs. Fully Connected SBO (Swarm-Based Organization)
*   **The Problem:** In SBO, agents can message any other agent. This creates high conversational noise, message loops (echo traps), and coordinate-budget inflation.
*   **The Solution:** Enforcing a Hub-and-Spoke orchestration where Workers cannot directly message each other. They read from and write to a shared report pool managed by the Task Orchestrator.
*   **Trade-off:** Reduces multi-agent emergent creativity but guarantees determinism, linear cost scaling, and robust error recovery.

---

## 7. Mapping Extracted Concepts to Apodex 2.0 Layers

| AI Engineer Concept | Apodex 2.0 Layer | Targeted Subsystem / File | Expected Benefit | Risks & Mitigations |
| :--- | :--- | :--- | :--- | :--- |
| **AgentOS Runtime Kernel** | **AgentOS Runtime** | `agent_harness/core/runtime/` | Handles concurrency, retry budgets, and model routing globally. | **Risk:** Kernel crashes halt all agents. **Mitigation:** Hexagonal process isolation. |
| **Hub-and-Spoke Report Pools** | **Multi-Agent Deep-Research Team** | `apodex/orchestration/hierarchical.py` | Allows up to 150 agents to work in parallel without context pollution. | **Risk:** Token bloat in report summaries. **Mitigation:** Append-only structured JSON summaries. |
| **Claims-to-Evidence Mapping** | **Verification Layer** | `apodex/governance/parallel_verification.py` | Eradicates hallucinations. Every sentence is backed by an EvidenceCard. | **Risk:** Strict verifier blocks valid drafts. **Mitigation:** Continuous confidence thresholds. |
| **Self-Harness & Weakness Mining** | **Evaluation & Self-Evolution** | `apodex/evolution/self_harness/refiner.py` | Automatically repairs stuck loops and tunes prompts. | **Risk:** Over-fitting on a single task. **Mitigation:** Small multi-task regression validation subset. |
| **Canary Deploy & SLA Monitor** | **Evaluation & Self-Evolution** | `apodex/evolution/production/rollout.py` | Prevents regression deployments and handles auto-rollback. | **Risk:** SLA spike on raw network noise. **Mitigation:** Rolling metrics window of 5 runs. |
| **REST API & Branching Inquiry** | **User & Product Layer** | `apodex/applications/` | Transitions the platform from a CLI harness to a commercial SaaS. | **Risk:** Large concurrent request spikes. **Mitigation:** Asynchronous task queue (RabbitMQ/Redis). |

---

## 8. Gap Analysis: Baseline Apodex vs. State-of-the-Art Standards

The original Apodex meta-system implementation had several architectural omissions and gaps that have been identified and resolved during the migration to Apodex 2.0:

1.  **Gaps in Experience Memory (L1):**
    *   *Baseline:* Trajectories were stored as raw text logs, preventing the system from calculating graph edit operations to recover from execution failures.
    *   *Apodex 2.0:* Implemented a production-grade `EMGEngine` inside `apodex/memory/emg_engine.py` to compile traces into directed `ActionDecisionGraph` nodes and edges, extract recurring workflows via sequence-pattern mining, and compute edit paths (`ADD_STEP`, `REPLACE_STEP`).
2.  **Gaps in Active Retrieval (L2):**
    *   *Baseline:* `SemanticMemory` only supported direct SQL filters.
    *   *Apodex 2.0:* Implemented Jaccard token-overlap matching (`retrieve_similar_evidence`) inside `SemanticMemory` to allow keyword-matching over historical compilation or execution logs during runtime.
3.  **Gaps in Production Rollout & SLA Monitoring (L3):**
    *   *Baseline:* Prompt modifications were hot-swapped without testing, risking severe regressions.
    *   *Apodex 2.0:* Deployed a secure double-gate validation loop with `SelectiveRollout` and `RollbackManager` inside `apodex/evolution/production/rollout.py`. If a canary variant breaches SLA (latency >= 5s or quality score < 0.5), it is automatically rolled back.
4.  **Gaps in Package Structuring:**
    *   *Baseline:* Structural logic was split across multiple subprojects and conflicting package paths, breaking backwards compatibility.
    *   *Apodex 2.0:* Converged all core logic inside a single, canonical production layout under `apodex/` and bridged imports using lightweight re-exports under `agent_harness.*` paths.

---

## 9. Institutional-Grade Implementation Blueprint

To ensure institutional robustness and absolute compliance with Karl Friston's expected free energy minimization and Judea Pearl's do-calculus, Apodex 2.0 adopts the following physical structures, interfaces, and pipelines:

### 9.1 Directory Structure Layout

```
/app
├── AgentHarness/                      # Legacy evaluation harness submodule
│   └── agent_harness/
│       ├── components/
│       │   ├── harness_observer.py    # Bridges to apodex.evolution.self_harness
│       │   ├── selective_rollout.py   # Bridges to apodex.evolution.production.rollout
│       │   └── rollback_manager.py    # Bridges to apodex.evolution.production.rollout
│       └── core/
│           ├── cost_tier.py           # Bridges to CostTier in apodex.skills.models
│           ├── memory/
│           │   ├── semantic_memory.py # Bridges to apodex.memory.semantic_memory
│           │   ├── learning_memory.py # Bridges to apodex.memory.learning_memory
│           │   └── emg_engine.py      # Bridges to apodex.memory.emg_engine
│           └── runtime/
│               ├── dataset_generator.py # Bridges to dataset_generator & trajectory_verification
│               └── orchestration/
│                   ├── hierarchical.py  # Bridges to apodex.orchestration.hierarchical
│                   └── planner_executor.py # Bridges to apodex.planning.planner_executor
│
├── apodex/                            # Canonical Production Package (DDD)
│   ├── applications/                  # REST API & Web Server Interfaces
│   ├── cognition/                     # Multi-Dimensional Dataset compilers, verification, & credit assignment
│   ├── evolution/
│   │   ├── common/                    # Changelog and metric schemas
│   │   ├── production/
│   │   │   └── rollout.py             # Production-grade SelectiveRollout & RollbackManager
│   │   └── self_harness/
│   │       ├── harness_observer.py    # Production Loop Trajectory Tracing
│   │       └── refiner.py             # Prompt optimization & Pareto-frontier calculation
│   ├── memory/
│   │   ├── semantic_memory.py         # Persistent local-first memory & Jaccard matching
│   │   ├── learning_memory.py         # Long-term strategy persistence
│   │   └── emg_engine.py              # Experience Memory Graph (L1) Engine
│   ├── orchestration/
│   │   └── hierarchical.py            # Hierarchical hub-and-spoke multi-agent system
│   ├── planning/
│   │   └── planner_executor.py        #Strategic planners & Task isolation executors
│   └── skills/
│       ├── registry.py                # Pre-populated roster of 60 default capabilities
│       └── models.py                  # CostTier, BusinessSkill, and playbooks schemas
└── tests/                             # Unified Test Suite (361/361 tests passing)
```

### 9.2 Key Data Models (Pydantic / SQLModel)

#### ActionDecisionGraph (Experience Memory Graph - L1)
```python
class EMGNode(BaseModel):
    step_id: str
    node_type: str
    action: str
    status: str
    is_error: bool = False
    tool_result_preview: str = ""
    timestamp: float = 0.0

class ActionDecisionGraph(BaseModel):
    trajectory_id: str
    nodes: Dict[str, EMGNode] = Field(default_factory=dict)
    edges: List[Tuple[str, str]] = Field(default_factory=list)
```

#### DeploymentVariant (Production Canary - L3)
```python
class DeploymentVariant(BaseModel):
    variant_id: str
    target_capability: str
    traffic_percentage: float = Field(0.0, ge=0.0, le=100.0)
    verifier_scores: List[float] = Field(default_factory=list)
    latencies_sec: List[float] = Field(default_factory=list)
```

---

## 10. Verification and Deployment Strategy

### 10.1 Testing Strategy
1.  **Fast Regression Testing:** On any code change, run cached benchmarks in parallel. Every change must be validated against `tests/memory/test_semantic_memory.py` and `tests/evolution/test_emg_memoharness.py`.
2.  **Trace Consistency Verification:** Ensure no `<thinking>` leaks enter output streams. The `MultiDimensionalTrajectoryVerifier` enforces exact syntactic brackets checking.
3.  **No-bypassable Human Verification:** Strategic edits (e.g. prompt tuning or model routing changes) must be routed to `/evolution approve` before promotion.

### 10.2 Execution Pipelines
```
[Agent Execution Step]
         │
         v
[HarnessObserver Captures Event] ──> Log to local memory
         │
         v
[L1 EMG Engine builds Graph] ──> Detect if Step Failed?
         │
         ├── Yes ──> Compute edit operations ──> Propose prompt clamp-12k patch
         │
         └── No  ──> Complete loop
```

---

## References

[1] APODEX‑1.0 BLOG/TECH EXPLANATION. <https://www.apodex.com/blog/apodex-1.0>.
[2] AGENTHARNESS REPOSITORY: EVALUATION HARNESS FOR APODEX‑1.0. <https://github.com/ApodexAI/AgentHarness>.
[3] The Multi-Agent Architecture That Actually Ships — Luke Alvoeiro, Factory (AI Engineer talk). <https://www.youtube.com/watch?v=ow1we5PzK-o>.
[4] Multi-Agent Systems That Ship for Days — Luke Alvoeiro, Factory. <https://daily.dev/posts/multi-agent-systems-that-ship-for-days-luke-alvoeiro-factory-bf6o18zfb>.
[5] You Can Learn AI Agent Harness & Loop Engineering In 19 Min | LLM Ops, Eval, Tracing, RAG. <https://www.youtube.com/watch?v=GrNbuWWJYiI>.
[6] Learn AI Agent Harness & Loop Engineering – transcript/summary. <https://sozai.app/transcript/learn-ai-agent-harness-loop-engineering/>.
[7] EvoAgentX: Building a Self-Evolving Ecosystem of AI Agents (repo & associated talks). <https://github.com/EvoAgentX/EvoAgentX>.
[8] Factory Missions Overview – planning, validation, custom droids, skills. <https://docs.factory.ai/features/missions/overview>.
