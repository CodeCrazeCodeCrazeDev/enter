# Research Traceability Matrix & Paper Rejection Log
## Evidence-Based Integration and Validation of Foundational AI Research

This document tracks how scientific principles from foundational machine learning and agentic reasoning literature have been systematically integrated and validated across the Cognitive Operating System, alongside a log of rejected research directions.

---

## 1. Research-to-Code Traceability Matrix

### 1.1 Paper: Reflexion (arXiv:2303.11366)
*   **Evidence**: Demonstrates that agents using verbal self-reflection over failure traces improve task-solving accuracy on reasoning benchmarks from 57% to 83%.
*   **Transferable Principle**: Experience Memory Graphs (EMG) should record failure trajectories and derive natural-language corrective edit operations.
*   **Existing Gap**: Previous loops used stateless prompt rollbacks (line-popping) which caused repetitive errors.
*   **Hypothesis**: Graphical corrective paths computed from failure subgraphs will prevent repetitive tool errors and enable self-correction.
*   **Implementation**: Fully operationalized in `apodex/memory/emg_engine.py` and `tests/evolution/test_emg_memoharness.py`.
*   **Result**: Validated. The refiner generates corrective path mappings (e.g. inserting missed steps) and recovers.

### 1.2 Paper: LADDER (arXiv:2312.11542)
*   **Evidence**: Showcases that decomposing long-horizon goals into a recursive tree of sub-milestones reduces planning errors on complex tasks.
*   **Transferable Principle**: Separate strategic roadmap planning from isolated step execution to avoid context windup bloat.
*   **Existing Gap**: Monolithic ReAct loops combined high-level strategic reasoning with local tool-calling parameters in a single context window.
*   **Hypothesis**: Separating planners, executors, and inline verifiers reduces context pollution and lost attention.
*   **Implementation**: Implemented in `apodex/planning/planner_executor.py` and `tests/planner/test_planner.py`.
*   **Result**: Validated. Planner context remains stateless during step executions, reducing peak memory usage.

### 1.3 Paper: Let's Verify Step-by-Step (arXiv:2305.20050)
*   **Evidence**: Proves that step-level process verifiers (PRMs) yield significantly higher reasoning correctness (78% vs 52%) compared to outcome-level verifiers (ORMs).
*   **Transferable Principle**: Decompose holistic validation gates into granular, step-wise verification checks during runtime execution.
*   **Existing Gap**: Previous loops executed post-facto verification after task completion, allowing error cascades to go uncorrected during execution.
*   **Hypothesis**: Registering step-level verifiers against active roadmap items allows immediate self-correction and recovery.
*   **Implementation**: Implemented in `apodex/planning/planner_executor.py` (`PlanVerifier.verify`) and verified under robustness benchmarks.
*   **Result**: Validated. Confirmed inline detection of step failures and execution recovery under `test_adversarial_tool_failure_and_recovery`.

---

## 2. Research Rejection Log

We reject the blind integration of novel papers that introduce latency, safety, or scalability risks without adding measurable, first-principles engineering value.

| Paper | Concept evaluated | Primary Reason for Rejection | Trigger to Re-evaluate |
| :--- | :--- | :--- | :--- |
| **DeepSeek-R1 (arXiv:2501.12948)** | Online RL via GRPO step-wise reasoning on live loops. | Highly impractical. Real-time online reinforcement learning on agent execution loops introduces extreme GPU latency and compute saturation, making it unsuitable for live application runtimes. | The development of low-latency, edge-deployable distilled reasoning models capable of running local sub-second training. |
| **FunSearch (Nature 2023)** | Program search and mathematical discovery via evolutionary prompts. | Safety and sandbox boundaries. Running unconstrained code evolution loops directly on the host filesystem introduces extreme execution vulnerability. Restricted strictly to isolated virtual-machine layers. | Implementation of multi-tenant, hyper-isolated secure container runtimes (e.g., microVM or gVisor) bound with physical compute quotas. |
| **Generative Agents (arXiv:2304.03442)** | Continuous multi-agent social interaction and coordinate memory. | Excessive cost and token pollution. Simulating hundreds of background message exchanges for standard deterministic business workflows creates severe latency and financial cost without direct capability improvement. | Low-cost local small models with extremely fast warm-caches and minimal context footprint. |
