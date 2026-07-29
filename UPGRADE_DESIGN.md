# Upgrade Design Document: Next-Generation Research Orchestration (AgentHarness v2)

This document provides a highly detailed design specification for the ten architectural upgrades required to transition `AgentHarness` into a state-of-the-art research orchestration framework.

---

## 1. Unified Architecture Strategy

To prevent polluting the stable, standard `react_base` baseline, we introduce a brand-new next-generation pipeline under `agent_harness_v2`. This pipeline is built via `PipelineSpec` composition, meaning:
- Existing APIs and baseline execution are preserved with **100% backward compatibility**.
- All v2 capabilities are modular, isolated, and toggled via configuration parameters.
- Multi-Agent Orchestration, Graph-of-Thought, Plan-and-Act, Memory, and Verification components reside in clean, separate modules inside `agent_harness/core/v2` and can be enabled independently.

---

## 2. The Ten Upgrades: Detailed Specifications

### 1. Hierarchical Multi-Agent Orchestration
- **Why**: Flat single-agent loops suffer from rapid context window expansion as execution logs accumulate.
- **How**: Replace single-solver layout with a Hierarchical Topology:
  - **Master Orchestrator**: High-level planner. Receives user tasks, partitions them, and routes to Coordinators.
  - **Coordinator Agents**: Manages specific worker sub-groups (e.g., search team vs. code execution team). Aggregates and summarizes sub-agent states before reporting back to the Master, drastically pruning raw worker execution histories.
  - **Worker Agents**: Executes fine-grained tools (`web_fetch`, `run_python_code`).
- **Trade-offs**: Introduces minor coordination latency.
- **Expected Token Reduction**: up to **40-60%** for long-horizon research tasks.

### 2. Graph-of-Thought (GoT) Reasoning
- **Why**: Linear thinking locks the agent in a single, un-correctable line of inquiry.
- **How**: Thoughts are represented as nodes in a graph. Dependencies are modeled as directed edges.
  - Supports **Branching** (generating multiple distinct hypothetical sub-plans).
  - Supports **Merging** (combining verified facts from different branches).
  - Supports **Pruning** (discarding low-confidence or disproven branches).
- **Compatibility**: Integrated cleanly into the ReAct workflow by making linear steps a specialized single-chain graph.

### 3. Plan-and-Act Architecture
- **Why**: Executing tools within the same reasoning state pollutes the core planning context with hundreds of lines of webpage content.
- **How**: Separate planning from execution:
  - **Planner Node**: Retains only the strategic plan, current sub-goal, and verified facts. It remains completely free of raw tool logs.
  - **Executor Node**: Instantiates standard ReAct loops with tools to execute a specific plan node.
  - **Verifier Node**: Evaluates executor results before plan updates.

### 4. Persistent Semantic Memory
- **Why**: Pure chat history fails to retain persistent beliefs or verified facts across long contexts or multiple attempts.
- **How**: Implement a robust modular memory manager backing:
  - **Beliefs**: High-level hypotheses.
  - **Verified Facts**: Confirmed, double-checked pieces of data.
  - **Evidence**: Supporting text passages.
  - **Unresolved Questions**: Next research objectives.
  - Backed by SQLite by default, extensible to Vector DBs.

### 5. World Model
- **Why**: Searching and scraping repeatedly for overlapping topics wastes tokens and time.
- **How**: Maintain an evolving graph-based World Model representing:
  - **Knowledge Graph**: Core concepts and their connections.
  - **Entity Graph**: Discovered websites, metrics, and dates.
  - **Causal Graph**: "X causes Y" relationships discovered.
  - **Temporal Graph**: Timelines of events.
  - **Uncertainty Graph**: Areas of high noise or missing data.

### 6. Self-Improvement Flywheel
- **Why**: High-quality trajectories should be harvested to enable future SFT/Preference fine-tuning datasets.
- **How**: Establish a post-task pipeline:
  - Extract successful trajectories (fully verified answers).
  - Grade quality using a rigorous Trajectory Scorer.
  - Export only passing traces with full metadata (planner logs, tool usage, verifications, confidence) into JSONL files under `/trajectories`.

### 7. Parallel Verification
- **Why**: Verification during standard ReAct can stall execution.
- **How**: Parallel multi-domain verify trees:
  - Worker outputs are concurrently dispatched to **Domain Verifiers** (e.g., Code syntax verifier, Citation/fact check verifier, Consistency verifier).
  - A **Meta Verifier** collects all domain verdicts and combines them into a single score.

### 8. Meta Reasoner
- **Why**: Runtime failures, tool inefficiencies, and hallucination loops go undetected during long-horizon tasks.
- **How**: Run an oversight daemon that sits parallel to the loop:
  - Monitors token growth, tool utilization rates, and hallucination loops.
  - Injects optimization nudges or prompts the orchestrator to prune active branches.

### 9. Long-Term Learning Memory
- **Why**: Strategies that failed/succeeded in previous runs are lost on startup.
- **How**: Persist cross-session learning schemas in SQLite:
  - Store pairs of `(Task Category, Strategy, Outcome Score, Performance Stats)`.
  - On new task startup, query the Learning Memory to retrieve past successful plans or avoid known failing paths.

### 10. Active Learning
- **Why**: Static ReAct is passive and struggles to quantify confidence.
- **How**: Build uncertainty estimation into the World Model. When uncertainty is above a configured threshold, the Active Learner generates highly targeted search/extraction queries, updating the world model iteratively until confidence is satisfied.
