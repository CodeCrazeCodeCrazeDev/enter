# Research Integration Matrix
## SOTA Scientific-to-Code Traceability Chain (v3.0.0)

This matrix establishes the direct, verifiable chain from SOTA literature (arXiv publications) to active, production-grade components, benchmarks, and architectural decisions inside the Unified Cognitive OS.

---

## 1. Traceability Mapping

| Paper / Reference | Core Principle | Code Location | Validation Test | Architectural Decision |
| :--- | :--- | :--- | :--- | :--- |
| **Experience Memory Graph** (arXiv:2607.13884) | Graph-matched trajectory repair operations. | `apodex/memory/emg_engine.py` | `test_emg_memoharness.py` | Store failures and successful paths as directed graphs; compute graph-edit paths (`ADD_STEP`, `REPLACE_STEP`) to correct loops. |
| **MemoHarness** (arXiv:2607.14159) | Dual-layer experience bank & Jaccard query retrieval. | `apodex/memory/semantic_memory.py` | `test_semantic_memory.py` | Use Jaccard token overlap for high-fidelity semantic context matching, retrieving similar past successes to guide the active agent. |
| **SIA** (arXiv:2605.27276) | Double-lever (scaffold + weights) co-evolution. | `apodex/aean/core.py` | `test_aean.py` | Restrict model weight modifications to offline training sweeps, while actively optimizing runtime prompts/parameters. |
| **Self-Harness** (arXiv:2606.09498) | Weakness mining, proposal, and validation. | `apodex/evolution/self_harness/` | `test_self_harness.py` | Establish an automated self-correcting loop that scans traces for loop blocks and applies prompt modifications. |
| **Constitutional AI** (Anthropic) | Rule-based and policy-based self-regulation. | `apodex/aean/governance.py` | `test_governance.py` | Enforce immutable rule sets to block offensive content, excessive capital allocations, and prompt injections. |

---

## 2. Evidence-Backed Adoption Criteria

We mandate that no research principle is counted as "integrated" without satisfying three validation gates:
1.  **Direct Footprint**: Must have a concrete class or function implementation in the source tree.
2.  **Verifiable Benchmark**: Must have a dedicated unit or integration test verifying the principle.
3.  **Measurable Delta**: Must demonstrate a positive capability delta (e.g., lower Free Energy, higher success rates, or lower token footprint) compared to the pre-research baseline.
