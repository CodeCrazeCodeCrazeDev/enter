# Phased Migration & Implementation Roadmap

## Overview

The transformation into the Unified Cognitive Operating System follows a 4-phase rollout strategy, engineered for zero downtime, zero capability regression, and deterministic backward compatibility.

---

## Phase Breakdown & Objective Criteria

### Phase 1: Substrate Hardening & Core Compatibility (Completed)
- **Primary Objective**: Establish root-level backward compatibility adapters and eliminate runtime deprecation warnings.
- **Key Deliverables**:
  - Restored `agent_harness` root compatibility package with dynamic `__path__` extender to `AgentHarness/agent_harness`.
  - Migrated naive `datetime.utcnow()` calls to timezone-aware `datetime.now(timezone.utc)` across all domain models and runners.
  - Resolved Pydantic V2 config deprecation warnings across core models.
- **Objective Evaluation Criteria**: 100% pass rate on legacy unit and integration test suite.

### Phase 2: Scientific Corpus Integration & Principle Ingestion (Completed)
- **Primary Objective**: Ingest, index, and register transferable engineering principles across 600+ research publications.
- **Key Deliverables**:
  - Registered `ALPHAALGO_100_PRINCIPLES`, `ALPHAALGO_200_PRINCIPLES`, `ALPHAALGO_301_400_PRINCIPLES`, `ALPHAALGO_401_500_PRINCIPLES`, and `ALPHAALGO_501_600_PRINCIPLES`.
  - Updated `ResearchOS.conduct_literature_review` to query multi-field research principles across category, target subsystem, paper title, and implementation module.
- **Objective Evaluation Criteria**: Zero paper title or DOI overlap across corpus database files audited by custom verification tools.

### Phase 3: Runtime Subsystem Enhancement & Cross-Layer Bridge (Completed)
- **Primary Objective**: Deploy production-ready enhancements across CodeRewriteEngine, GeneticWorkflowOptimizer, SFTPreferenceCollector, LearnableRoutingGateDispatcher, and ResearchToSystemBridge.
- **Key Deliverables**:
  - AST-based function call depth checking in `CodeRewriteEngine.verify_proposal_ast`.
  - Island MAP-Elites migration gates and population sorting in `GeneticWorkflowOptimizer`.
  - On-policy advantage estimation margins in `SFTPreferenceCollector`.
  - Active Inference EFE routing and financial budget limits in `LearnableRoutingGateDispatcher`.
  - End-to-end active inference handoff in `ResearchToSystemBridge`.
- **Objective Evaluation Criteria**: Verification via cross-layer integration test suites (`test_unified_cognitive_architecture_spec.py`).

### Phase 4: Continuous Flywheel & Institutional Autonomous Execution (Active)
- **Primary Objective**: Enable autonomous long-horizon execution, continuous self-improvement, and real-time world model belief updates.
- **Key Deliverables**:
  - SFT/DPO preference dataset auto-compilation from live agent runs.
  - Automated regression testing and architectural invariant verification scripts.
- **Objective Evaluation Criteria**: Zero capability regressions across all 397+ repository unit, integration, and performance benchmarks.
