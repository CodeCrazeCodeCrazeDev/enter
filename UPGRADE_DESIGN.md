# AgentHarness Next-Generation Architectural Upgrade Design (Phase 2) - Enhanced

This document provides the complete, professional, production-grade architectural upgrade blueprint for AgentHarness, covering all ten next-generation capabilities.

---

## Upgrade 1: Hierarchical Multi-Agent Orchestration

### Motivation & Current Limitations
The standard flat ReAct loop (`react_base`) mixes strategic reasoning and low-level search details. This leads to massive context bloating and cognitive dilution.

### Proposed Architecture
We will decouple execution context into a three-tier tree structure:
```
           +----------------------+
           |  MasterOrchestrator  |  <-- Allocates high-level tasks
           +-----------+----------+
                       |
                       v
           +----------------------+
           |   CoordinatorAgent   |  <-- Summarizes worker state upward
           +-----------+----------+
                       |
             +---------+---------+
             v                   v
      +--------------+    +--------------+
      | SearchWorker |    | SandboxWorker|  <-- Execute atomic actions
      +--------------+    +--------------+
```

### Sequence Flow
1. `MasterOrchestrator` receives a complex research prompt.
2. It instantiates a `CoordinatorAgent` with specific sub-goals.
3. The Coordinator spawns a specialized `WorkerAgent` (e.g. `SearchWorker`).
4. `SearchWorker` executes web actions, receives the raw text, and returns a high-level summary of findings to the `CoordinatorAgent`.
5. The `CoordinatorAgent` merges the worker findings and passes a clean, aggregated state report to the `MasterOrchestrator`.

### API Changes & New Modules
- **New Module**: `agent_harness/core/runtime/orchestration/hierarchical.py`
- **Class**: `class HierarchicalOrchestrator(BaseOrchestrator)`
- **Class**: `class CoordinatorAgent(BaseAgent)`
- **Class**: `class WorkerAgent(BaseAgent)`

### Impact & Backward Compatibility
- **Token Reduction**: Expected $\approx 45\%$ token footprint reduction by isolating raw scraping payloads within short-lived worker threads.
- **Compatibility**: Perfect. Existing single-solver pipelines bypass this hierarchy entirely.

---

## Upgrade 2: Planner / Executor Separation

### Motivation & Current Limitations
Mixing planner and executor tasks makes strategy highly vulnerable to transient tool-level failures (such as a parsing warning or empty web search page).

### Proposed Architecture
Clear demarcation of roles:
1. **Planner**: Pure strategist. No direct tool access. Receives task requirements and returns a step-by-step Execution Roadmap.
2. **Executor**: Action-only. Executes tools to fulfill the roadmap segments.
3. **Verifier**: Cross-checks executor outputs against the planner strategy.

```
+-----------+                +------------+                +------------+
|  Planner  | -- roadmap --> |  Executor  | -- outputs --> |  Verifier  |
+-----------+                +------------+                +------------+
```

### API Changes & New Modules
- **New Module**: `agent_harness/core/runtime/orchestration/planner_executor.py`
- **Interface**: `class StrategicPlanner`, `class TaskExecutor`, `class PlanVerifier`

---

## Upgrade 3: Persistent Semantic Memory

### Motivation & Current Limitations
Compaction wipes out historical knowledge, leading to informational amnesia and duplicate search actions.

### Proposed Architecture
Implement a structured memory base independent of raw chat records.
- Stored as high-fidelity structured data in local files or a lightweight memory database.

```
       [SemanticMemory]
        /      |       \
[Beliefs]  [Facts]  [Questions]
```

### Data Schema
- **Beliefs**: Evolving hypotheses.
- **Facts**: Proven statements accompanied by evidence cards.
- **Evidence Cards**: Content snippets linked to sources.
- **Unresolved Questions**: Strategic targets.

### Sequence Flow
```
Executor -> SemanticMemory.add_fact(Fact(assertion="...", evidence_id="src_1"))
Planner -> SemanticMemory.retrieve_beliefs() -> returns high-level strategy context
```

---

## Upgrade 4: World Model

### Motivation & Current Limitations
The agent does not model relationships between entities, causal sequences, or uncertainties dynamically.

### Proposed Architecture
A continuous graph model structured as `class WorldModel`:
- **Knowledge/Entity Graph**: Links actors and entities.
- **Causal Graph**: Inter-dependencies between steps.
- **Uncertainty Graph**: Highlights gaps in information.

### API Changes & New Modules
- **New Module**: `agent_harness/core/memory/world_model.py`
- **Interface**: `class WorldModel`, `class RelationEdge`, `class CausalNode`

---

## Upgrade 5: Parallel Verification

### Motivation & Current Limitations
Verification is slow, serial, and post-facto.

### Proposed Architecture
Concurrent validation:
- **Domain Verifiers**: Parallel specialized models checking factual accuracy, logic consistency, and code syntax concurrently using `asyncio.gather`.
- **Meta Verifier**: Evaluates and consolidates domain reports.

```
                      +-------------------+
                      |   Worker Output   |
                      +---------+---------+
                                |
             +------------------+------------------+
             |                                     |
             v                                     v
+------------------------+             +------------------------+
| Domain Verifier (Fact) |             | Domain Verifier (Code) |
+------------+-----------+             +-----------+------------+
             |                                     |
             +------------------+------------------+
                                v
                      +-------------------+
                      |   Meta Verifier   |
                      +-------------------+
```

---

## Upgrade 6: Meta-Reasoner

### Motivation & Current Limitations
The system runs blind; it cannot detect token waste or logical looping traps during execution.

### Proposed Architecture
An oversight observer (`class MetaReasonerObserver`) that monitors context growth, token utilization, and loop patterns.
- **Autocorrection**: Dynamically alters Coordinator's instruction context when loops are identified.

---

## Upgrade 7: Long-Term Learning Memory

### Motivation & Current Limitations
Learnings are lost after individual task completion.

### Proposed Architecture
A persistent strategy registry (`class LongTermLearningMemory`) storing successfully completed roadmaps and failed trajectories to guide future tasks.

---

## Upgrade 8: Self-Improvement Flywheel

### Motivation & Current Limitations
No automated method to generate fine-tuning datasets from successful runs.

### Proposed Architecture
A post-execution processor:
- Analyzes successful trajectories.
- Validates trace steps.
- Formats and writes high-quality runs into clean, training-ready JSONL datasets.

---

## Upgrade 9: Graph-of-Thought Reasoning

### Motivation & Current Limitations
Linear ReAct restricts exploration of alternative hypotheses.

### Proposed Architecture
A non-linear thought tree engine (`class GraphOfThoughtEngine`):
- Nodes represent thoughts.
- Edges represent logical relationships.
- Supports branching, merging, and pruning.

---

## Upgrade 10: Active Learning

### Motivation & Current Limitations
Passive prompt execution with zero estimation of semantic uncertainty.

### Proposed Architecture
An active learning loop:
- Computes entropy/uncertainty metrics of current beliefs.
- If uncertainty exceeds a threshold, automatically drafts targeted queries to update the world model until the confidence threshold is satisfied.
