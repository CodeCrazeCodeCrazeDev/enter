# Repository-Wide Architectural Audit
## First-Principles Assessment of the 5-Subsystem Cognitive OS (v3.0.0)

This audit evaluates all active components in the codebase, assessing their core responsibilities, dependency mappings, and capability values.

---

## 1. Unified Subsystems Audit

We evaluate each of the five core subsystems under ten rigorous, first-principles questions:
1.  **What responsibility does it own?**
2.  **Why does that responsibility exist?**
3.  **Who consumes it?**
4.  **What state does it own?**
5.  **What interfaces does it expose?**
6.  **What other components does it depend on?**
7.  **Is another component performing the same responsibility?**
8.  **Does it provide measurable capability?**
9.  **Is it production-critical, experimental, compatibility-only, or obsolete?**
10. **What evidence proves its value?**

---

### 1.1 Research OS (`apodex/research_os/` & `apodex/ai_eos/research/`)
1.  **Responsibility**: Owns the scientific discovery and literature compilation loop.
2.  **Why**: Serves as the primary vehicle for open-ended innovation, literature harvesting, and theory building.
3.  **Consumers**: `ExecutiveOptimizer` and `EIOSKernel`.
4.  **State**: Owns the 200-paper scientific database (`AI_EOS_RESEARCH_DB.yaml`) and registered experimental histories.
5.  **Interfaces**: `register_hypothesis()`, `create_experiment()`, `score_opportunity()`, `design_experiment()`.
6.  **Dependencies**: `KnowledgeInfrastructure` and `SemanticMemory`.
7.  **Overlaps**: None. It is the sole scientific discovery engine.
8.  **Measurable Capability**: Reduces overall system belief entropy and updates hypothesis confidence scores.
9.  **Status**: **Production-critical**.
10. **Evidence**: Evaluated under `test_e2e_sero_lifecycle.py` and `test_scientific_discovery_and_evolution.py`.

---

### 1.2 EIOS / EREOS (`apodex/arcs/`)
1.  **Responsibility**: Owns the active inference routing, multi-mind debate, and master scheduling.
2.  **Why**: Coordinates cascading agent societies and schedules complex goal-directed execution DAGs.
3.  **Consumers**: Human operators and portfolio allocation systems.
4.  **State**: Owns active debate transcripts, Free Energy parameters, and compiled DAG nodes.
5.  **Interfaces**: `execute_dag()`, `evaluate_with_multi_mind()`, `run_collective_intelligence_debate()`.
6.  **Dependencies**: `WorldGraph` and `UnifiedPlanner`.
7.  **Overlaps**: None. Serves as the master coordinator.
8.  **Measurable Capability**: Minimizes Expected Free Energy, resolves multi-agent conflicts, and coordinates multi-step tasks.
9.  **Status**: **Production-critical**.
10. **Evidence**: Validated in `test_active_inference_hierarchy` and `test_collective_intelligence_and_venture_studio`.

---

### 1.3 EOS (`apodex/ai_eos/`)
1.  **Responsibility**: Owns the business metrics, unit economics modeling, and venture lifecycles.
2.  **Why**: Keeps the entire system financially grounded and prevents capital-allocation bubbles.
3.  **Consumers**: `VentureExecutionSystem` and `PortfolioOperatingSystem`.
4.  **State**: Owns cash reserves, LTV/CAC ratios, and venture cell statuses.
5.  **Interfaces**: `allocate_portfolio_capital()`, `plan_multi_timescale()`, `evaluate_opportunity_form()`.
6.  **Dependencies**: `KnowledgeInfrastructure` and `SystemEconomics`.
7.  **Overlaps**: None.
8.  **Measurable Capability**: Maximizes portfolio net worth, enforces cash reserves, and mitigates financial risk.
9.  **Status**: **Production-critical**.
10. **Evidence**: Verified in `test_e2e_sero_lifecycle.py`.

---

### 1.4 AEAN (`apodex/aean/`)
1.  **Responsibility**: Owns agent-level tools, Thompson-sampling bandit execution, and local content/outreach filtering.
2.  **Why**: Executes concrete, day-to-day transaction steps and micro-actions.
3.  **Consumers**: `EIOSKernel` and `VentureExecutionSystem`.
4.  **State**: Owns local bandit rewards, EKG signals, and constitutional violation counts.
5.  **Interfaces**: `review_allocation()`, `review_content()`, `compute_optimal_price_cents()`, `run()`.
6.  **Dependencies**: `EconomicKnowledgeGraph` and `LLMAdapter`.
7.  **Overlaps**: None.
8.  **Measurable Capability**: Executes targeted marketing outreach, manages pricing markups, and blocks security injections.
9.  **Status**: **Production-critical**.
10. **Evidence**: Thoroughly tested under `test_aean.py`.

---

### 1.5 APODEX (`apodex/`)
1.  **Responsibility**: The underlying computational substrate (database, scheduling, evaluation, and tool invention).
2.  **Why**: Provides the base infrastructure, subprocess isolation, and evaluation testbeds.
3.  **Consumers**: All higher-level functional planes and layers.
4.  **State**: Owns SQLite transaction connections and file I/O operations.
5.  **Interfaces**: `MiniDAG`, `SQLiteMemoryRepository`, `TaskExecutor`, `PlanVerifier`.
6.  **Dependencies**: `pydantic`, `sqlite3`, `asyncio`.
7.  **Overlaps**: None.
8.  **Measurable Capability**: Provides transaction safety, subprocess execution, and evaluation benchmark scores.
9.  **Status**: **Production-critical**.
10. **Evidence**: Proven across the entire repository test suite.
