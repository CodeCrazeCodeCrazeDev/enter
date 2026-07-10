# AgentHarness Next-Generation Architectural Upgrade Design (Phase 2)

This document details the blueprint for the ten next-generation architectural upgrades designed to evolve AgentHarness into a state-of-the-art autonomous research orchestration framework.

---

## Upgrade 1: Hierarchical Multi-Agent Orchestration

### Motivation & Limitations
Current architecture uses flat orchestration (`react_base`), causing context window fatigue as the single agent absorbs raw tool results.

### Proposed Architecture
We will introduce a hierarchical structure:
```
       [Master Orchestrator]
                |
       [Coordinator Agent]
          /     |     \
   [Worker 1] [Worker 2] [Worker 3]
```
- **Coordinator Agents** manage groups of workers and summarize state updates upward.
- **Worker Agents** execute specific actions and return highly compact result payloads.

### API & Data Flow
- `HierarchicalOrchestrator` class inside `agent_harness/core/runtime/orchestration/hierarchical.py`.
- **Data Flow**: Master delegates to Coordinator -> Coordinator routes to specialized Worker -> Worker executes tool -> Coordinator summarizes -> Master receives clean summary.

### Backward Compatibility
Completely backward compatible. Existing flat ReAct pipelines bypass this hierarchical router and execute exactly as before.

---

## Upgrade 2: Planner / Executor Separation

### Motivation & Limitations
Currently, planning and execution are co-located in the same ReAct loop. High-level strategy becomes polluted by massive tool execution logs.

### Proposed Architecture
We separate the roles cleanly:
1. **Planner**: Pure strategic actor. Translates task request into a strategic roadmap (Planner prompt). No execution history.
2. **Executor**: Translates roadmap into specific tool invocations.
3. **Verifier**: Validates executor results against the strategy.

```
+------------+       +------------+       +------------+
|  Planner   | ----> |  Executor  | ----> |  Verifier  |
+------------+       +------------+       +------------+
```

### New Modules
- `agent_harness/core/runtime/orchestration/planner_executor.py`

---

## Upgrade 3: Persistent Semantic Memory

### Motivation & Limitations
Currently, AgentHarness loses historical context upon compaction. It has no conceptual memory of its beliefs, verified facts, or open questions.

### Proposed Architecture
Implement a class `SemanticMemory` that houses:
- **Beliefs**: High-level structural interpretations.
- **Verified Facts**: Assertions backed by tool evidence.
- **Evidence Cards**: References to document segments.
- **Unresolved Questions**: Ongoing discovery threads.

### Sequence Diagram
```
Agent -> SemanticMemory.add_fact(fact_data)
SemanticMemory -> LocalStore.persist()
Agent -> SemanticMemory.retrieve_context(query) -> list[Fact]
```

---

## Upgrade 4: World Model

### Motivation & Limitations
The agent currently performs redundant search queries because it cannot map dependencies between entities or causal events.

### Proposed Architecture
A persistent `WorldModel` class in `agent_harness/core/memory/world_model.py` representing:
- **Knowledge Graph**: Entities & relationships.
- **Causal Graph**: Inter-dependencies between steps.
- **Temporal/Uncertainty Graph**: Evolving belief states.

---

## Upgrade 5: Parallel Verification

### Motivation & Limitations
Current verification is serial and offline. High latency and slow error-trapping.

### Proposed Architecture
```
        [Worker Node]
              |
    +---------+---------+
    |                   |
[Domain Verifier A] [Domain Verifier B]
    |                   |
    +---------+---------+
              v
       [Meta Verifier]
```
- Domain verifiers run in parallel using `asyncio.gather`.
- The Meta Verifier synthesizes the reports into a final correctness confidence payload.

---

## Upgrade 6: Meta-Reasoner

### Motivation & Limitations
The framework lacks active performance analytics during a live run. Token waste or logic looping is not identified dynamically.

### Proposed Architecture
A background `MetaReasoner` observer that:
- Monitors context growth, token utilization, tool latency, and repetition rate.
- Automatically injects strategy recommendations (e.g., "Switching search query to avoid repetition") directly into the Coordinator's stream context.

---

## Upgrade 7: Long-Term Learning Memory

### Motivation & Limitations
When a research task completes, all strategic learnings (what worked and what failed) are permanently lost.

### Proposed Architecture
Implement `LongTermLearningMemory` storing:
- Successful roadmaps.
- Failed tool paths.
- Performance statistics.
Saved to disk across research sessions, enabling historical lookup.

---

## Upgrade 8: Self-Improvement Flywheel

### Motivation & Limitations
No mechanism for generating datasets or self-training trajectories from high-quality runs.

### Proposed Architecture
After successful execution runs:
- Generate fine-grained, verifiable trace trajectories.
- Score trajectories against rigorous correctness criteria.
- Persist high-quality, verified trajectories into a dataset format to support offline continual fine-tuning.

---

## Upgrade 9: Graph-of-Thought Reasoning

### Motivation & Limitations
Linear ReAct reasoning prevents branching or exploring alternative hypotheses.

### Proposed Architecture
Thoughts are represented as graph nodes in `GraphOfThoughtReasoningEngine`:
- **Branching**: Explores parallel routes.
- **Merging**: Combines findings from different branches.
- **Pruning**: Dead-ends are cleanly trimmed.

---

## Upgrade 10: Active Learning

### Motivation & Limitations
The agent acts passively, accepting prompts directly without measuring semantic confidence or proactively querying for clarifications when uncertain.

### Proposed Architecture
- Estimating semantic uncertainty throughout execution steps.
- If uncertainty is high, automatically draft targeted evidence queries and probe updated world states until a confidence threshold is satisfied.
