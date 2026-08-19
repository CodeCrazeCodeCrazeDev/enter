# Unified Cognitive Operating System Dependency Graph & Communication Specification
**Author:** Jules, Lead Architect & Software Engineer
**Status:** Canonical Approved Standard
**Version:** 2.0.0
**Target Architecture:** Research OS / AEAN / EIOS & EOS / APODEX

---

## Executive Summary

This specification establishes the strict directional dependency rules, event streaming channels, asynchronous communication protocols, and isolation constraints across the 4-layer Cognitive Operating System taxonomy.

By enforcing a **strict unidirectional acyclic flow** for execution directives and an **asynchronous event-driven flow** for sensory feedback and learning signals, the Cognitive OS eliminates circular dependencies, deadlock conditions, and race conditions.

---

## 1. System-Wide Directional Dependency Topology

```
                  +-----------------------------------+
                  |      LAYER 1: RESEARCH OS         |
                  | (Scientific Discovery & Evidence) |
                  +-----------------------------------+
                                    |
                                    | (1) Injects Scientific Evidence & Principles
                                    v
                  +-----------------------------------+
                  |         LAYER 2: AEAN             |
                  | (Cognitive Intelligence & Swarm)  |
                  +-----------------------------------+
                                    |
                                    | (2) Emits Cognitive Directives & EFE Policies
                                    v
                  +-----------------------------------+
                  |       LAYER 3: EIOS / EOS         |
                  | (Orchestration & Executive Control|
                  +-----------------------------------+
                                    |
                                    | (3) Dispatches Skill Execution Workflows
                                    v
                  +-----------------------------------+
                  |         LAYER 4: APODEX           |
                  | (Decision Engine, Memory, World)  |
                  +-----------------------------------+
                                    |
                                    | (4) Sensory Telemetry & Execution Feedback
                                    + - - - - - - - - - - - - - - - - - - - - - - - +
                                                                                    |
  +---------------------------------------------------------------------------------+
  |
  v
+-----------------------------------------------------------------------------------+
|                            ASYNC EVENT FEEDBACK BUS                               |
| - Execution Outcome Events -> Layer 3 (Updates Business State)                    |
| - Surprise / Prediction Errors -> Layer 2 (Updates Bayesian Beliefs)              |
| - Empirical Benchmark Failures -> Layer 1 (Invalidates Literature Principles)     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Directional Call Flow Rules & Inter-Layer Isolation

### Rule 1: Monotonic Downward Directives
Direct synchronous method calls are strictly constrained to move **downward** from Layer $N$ to Layer $N+1$:
- Layer 1 (`ResearchOS`) may invoke Layer 2 (`AEAN HiveMind`) to pass verified evidence or evaluate hypothesis suitability.
- Layer 2 (`AEAN`) may invoke Layer 3 (`EIOSKernel`) to dispatch cognitive directives or active inference policies.
- Layer 3 (`EIOS / EOS`) may invoke Layer 4 (`SkillRunner` / `APODEX`) to execute skill workflows and tool actions.
- Layer 4 (`APODEX`) **shall never** directly import or synchronously invoke Layer 1, 2, or 3.

### Rule 2: Asynchronous Upward Feedback
Information flow moving **upward** (from Layer 4 back to Layers 3, 2, and 1) occurs exclusively via the **Asynchronous Event Feedback Bus**:
- **Layer 4 -> Layer 3:** Dispatches `SkillExecutionCompleted` or `SkillExecutionFailed` events. Layer 3 updates its business loop state machine and financial balance.
- **Layer 4 -> Layer 2:** Dispatches `PredictionErrorObserved` events. Layer 2 computes the Bayesian surprise score ($S = |o - \hat{o}|$) and updates active inference priors.
- **Layer 4 -> Layer 1:** Dispatches `EmpiricalTrialOutcome` events. Layer 1 logs experiment replication status and updates p-values using Welch's t-test.

### Rule 3: Zero Horizontal Duplication
No capability shall exist across multiple layers. For example:
- Causal do-calculus exists *only* in Layer 2 (`apodex/aean/coordination/hive_mind.py`).
- Skill registration exists *only* in Layer 4 (`apodex/skills/registry.py`).
- Literature ingestion exists *only* in Layer 1 (`apodex/ai_eos/research/research_os.py`).

---

## 3. Communication Protocols & Interface Contracts

| Boundary | Communication Pattern | Transport / Format | SLA / Max Latency |
| :--- | :--- | :--- | :--- |
| **Layer 1 -> Layer 2** | In-Memory Async / Query | In-Memory Python Pydantic Object | < 2000 ms |
| **Layer 2 -> Layer 3** | Directive Stream / Message Queue | Async RPC / JSON Schema | < 500 ms |
| **Layer 3 -> Layer 4** | Workflow Dispatcher | Async Task Queue / Pydantic | < 100 ms |
| **Layer 4 -> Event Bus** | Event Streaming | In-Memory Async Publisher / SQLite WAL | < 10 ms |

---

## 4. Static Dependency Integrity Rules & Enforcement

To prevent architectural drift and circular dependencies, the static analyzer `scripts/validate_dependencies.py` enforces the following checks on every pull request:

1. **Circular Import Prohibition:** Zero circular import cycles detected across `apodex/`.
2. **Maximum Dependency Depth:** Depth of import chain shall be $d \le 6$.
3. **Core-to-Adapter Isolation:** Core modules (`apodex/`) shall not import adapter harness layers (`AgentHarness/`).
4. **Single Source of Truth:** Core classes (`ResearchOS`, `HiveMind`, `EIOSKernel`, `SkillRunner`, `WorldModel`) must have exactly one canonical definition file.
