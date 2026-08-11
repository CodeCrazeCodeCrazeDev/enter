# Unified Cognitive OS Baseline Report

## Environment & Dependency Baseline
- **Baseline Commit Hash:** `e0760f1224070a948d8e42a4dfa05afaea8e9b94`
- **Runtime Environment:** pyenv Python 3.12.13
- **Primary Package Dependencies:**
  - NumPy: 2.5.2
  - Pydantic: 2.13.4
  - PyYAML: 6.0.3
  - SQLModel: 0.0.39
  - AioSQLite: 0.22.1
  - HTTPX: 0.28.1
  - Pytest: 9.1.1
  - Pytest-Asyncio: 1.4.0

## Empirical Testing Baseline
- **Pass Rate:** 100% of all 361 repository unit, integration, and regression tests passing.
- **Baseline Execution Time:** 6.01 seconds.
- **Latency / Throughput:** All deterministic simulation steps execute in < 2ms per cycle in local test environments.

## Qualitative Cognitive Capabilities Baseline
- **Planner (UnifiedPlanner):** Supports recursive task decomposition and Tree-of-Thoughts backtracking.
- **Memory (UnifiedMemory & CMOS):** Multi-tier semantic context retrieval with decay policies, and Experience Memory Graph (EMG) edit tracing.
- **World Model (UnifiedPredictiveModel):** Simulates strategy outcome expectations and updates failure offsets.
- **Governance (GovernanceLayer):** Implements legal and GRC policy checklists with parallel verifications.
