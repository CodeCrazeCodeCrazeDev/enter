# Self-Improvement Governance
## Automated Evolution Guardrails & Promotion Criteria (v3.0.0)

This document formalizes the safety guardrails, promotion gates, and policies governing the recursive self-improvement and evolution loops inside the Unified Cognitive OS.

---

## 1. The Closed-Loop Evolution Gating Pipeline

To prevent runaway modification loops, reward hacking, or cognitive regressions, any proposed prompt or parameter change must traverse a strict 3-tier promotion gate:

```
[Detect Weakness] ➔ Analyze traces, stuck turns, and token waste via EMG
       ↓
[Generate Fix]   ➔ Suggest prompt modifications or parameter updates
       ↓
[Gate 1: Pre-Commit Sandbox] ➔ Run regression test suite (100% pass mandatory)
       ↓
[Gate 2: Statistical Validation] ➔ Run shadow validation over past traces
       ↓
[Gate 3: Selective Canary] ➔ Deploy variant to 10% traffic; monitor SLA
       ↓
[Promotion to Production] ➔ Promote to 100% traffic and log to EvolutionChangelog
```

---

## 2. Immutable Evolutionary Guardrails

1.  **Strict Metric SLA Checks**: If the latency, error rate, or token cost of the evolved variant exceeds baseline levels by more than $15\%$, a rollback is automatically triggered.
2.  **No Modification of Core Rules**: The Constitutional Rules (`ConstitutionalRules`) are immutable. No self-evolution loop may modify capital limits, disclosure rules, or security block patterns.
3.  **Human Authority Override**: A human operator retains a physical "kill-switch" and can execute `/evolution rollback` via CLI/GUI to revert any configuration to a known stable git commit immediately.
4.  **Transaction-Safe Evolution Ledger**: All changes, metrics comparisons, and validation reports must be sourcing-logged to `EvolutionChangelog` inside the SQLite persistent database, ensuring perfect audibility.
