# AgentHarness Architectural Upgrade Implementation Roadmap - Enhanced

> ### ⚠️ DOCUMENT STATUS: CONSOLIDATED & UNIFIED
> This implementation roadmap has been fully consolidated into the authoritative, single-source-of-truth **Unified Cognitive Operating System Architecture Specification**.
>
> All development milestones, quantitative targets, and phased release schedules conform to the plan defined at:
> **[docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md](docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md)**

---

## 1. Safety Rules & Merge Criteria for Every Pull Request

To ensure that no regressions are introduced and that the framework remains production-grade throughout implementation:
*   **Rule 1**: Every PR must compile and run successfully.
*   **Rule 2**: Every PR must preserve $100\%$ backward compatibility with legacy flat ReAct workflows.
*   **Rule 3**: Every PR must include comprehensive Unit and Integration tests.
*   **Rule 4**: Every PR must be independently reversible without impacting baseline system dependencies.

---

## 2. High-ROI Phased Implementation Plan

Development is prioritized and rolled out across four distinct phases:

### Phase 1: Substrate Hardening & Core Reliability (Immediate)
*   **Milestones**: Consolidate the central `SkillRegistry` as a single source of truth; restore backward compatibility with legacy `agent_harness` test consumers.
*   **Quantitative Targets**: 100% test pass rate on existing 361 unit/integration tests; core loop execution reliability $> 99.8\%$; zero import cycles.

### Phase 2: Cognitive Integration (Months 1-2)
*   **Milestones**: Wire the `StrategicPlanner` hierarchical task decomposer (LADDER) and ToT search into the EIOS/EOS business loops.
*   **Quantitative Targets**: Planning accuracy improvement $\ge 35\%$; context window usage reduced by $\ge 40\%$ under HLE benchmarks.

### Phase 3: Research & World Model Optimization (Months 3-4)
*   **Milestones**: Connect the arXiv scraper under Layer 1 and deploy the E-K-C-T-U multi-graph world model under SQLite.
*   **Quantitative Targets**: Information gain per query increased by $\ge 50\%$; prediction error variance reduced below $0.05$.

### Phase 4: Autonomous Closed-Loop Self-Improvement (Months 5-6)
*   **Milestones**: Build the background SFT LoRA fine-tuning orchestrator, training specialized local agent weights on high-purity trace datasets.
*   **Quantitative Targets**: Multi-aspect win-rate against baseline models $\ge 72\%$; task completion time reduced by $\ge 30\%$.

For details on Knowledge ROI formulas, effort/impact metrics, and continuous evolution safety guidelines, refer to **[docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md](docs/architecture/UNIFIED_COGNITIVE_OS_ARCHITECTURE.md)**.
