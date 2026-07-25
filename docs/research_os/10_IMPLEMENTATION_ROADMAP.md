# 10. Implementation Roadmap: Incremental Migration Strategy

To transition AlphaAlgo from its current baseline to the redesigned **Research Operating System**, we must adopt an **incremental migration strategy**. Big-bang rewrites are highly risky and often lead to operational failure.

This roadmap outlines a three-phased migration plan that replaces legacy components without disrupting existing trading research pipelines.

---

## Phase 1: Foundational Registries and Metadata (Short-Term: Weeks 1-4)

The goal of Phase 1 is to establish the core data models, registries, and the immutable configuration hashing mechanism.

### Key Milestones
1. **Define Core Data Models:** Implement the Pydantic schemas for `Hypothesis`, `Dataset`, `Experiment`, `Model`, and `ValidationReport` under `apodex/research_os/models.py`.
2. **Implement Thread-Safe registries:** Implement persistent, sqlite-backed registries under `apodex/research_os/registries.py` to store and query hypotheses, features, datasets, and experiments.
3. **Establish Declarative Hashing:** Deploy the SHA-256 configuration hashing algorithms to guarantee unique and cached experiment executions.
4. **Deploy Phase 1 Unit Tests:** Establish rigorous tests in `tests/research_os/` verifying that registries correctly reject duplicate configuration hashes and maintain immutability.

### Legacy Code Integration
* Existing `ResearchEngine` in `apodex/aean/coordination/research.py` is refactored: its output is redirected to write structured records to the new registries rather than returning transient list objects.

---

## Phase 2: Statistical Verification and Bias Filters (Medium-Term: Weeks 5-12)

The goal of Phase 2 is to inject mathematical discipline and eliminate data leakage, look-ahead bias, and overfitting.

### Key Milestones
1. **Deploy Data Validation Engine:** Write PIT and calendar-alignment validators to sanitize raw historical data feeds prior to model ingestion.
2. **Implement Statistical Validation Layer:** Code the multiple hypothesis correction methods (Bonferroni, Holm-Bonferroni, Benjamini-Hochberg) and the **Deflated Sharpe Ratio (DSR)** calculator.
3. **Deploy CSCV and PBO calculators:** Implement Combinatorially Symmetric Cross-Validation and the Block Bootstrap to run out-of-sample robustness checks.
4. **Integrate into Pipeline Runner:** Establish the `ResearchPipelineOrchestrator` to automatically execute these statistical gates post-experiment.

---

## Phase 3: Non-Bypassable Governance and Production Promoters (Long-Term: Weeks 13+)

The goal of Phase 3 is to lock down the promotion gates and implement the cryptographic audit trail.

### Key Milestones
1. **Deploy Cryptographic Audit Log:** Implement hash-chained event logging inside the Governance Gateway.
2. **Enforce Gatekeepers:** Wire up the programmatic limits (DSR $\ge 0.95$, PBO $\le 0.10$, Correlation Cap $\le 0.30$) into the final promotion stage.
3. **Deploy Peer-Review Protocols:** Implement the joint human-AI consensus voting mechanisms and generate standardized `DecisionRecords`.
4. **Integrate with Live Execution:** Connect the Model Registry to the production execution layers (under `apodex/execution/`), allowing automated hot-swapping of promoted models and graceful shutdown of degraded models.
