# 09. Risk & Governance: Non-bypassable Promotion Gates

In a professional quantitative asset manager, risk management and operational governance are not optional post-research steps. They are built directly into the fabric of the platform.

The **AlphaAlgo Risk and Governance Subsystem** enforces immutable gatekeepers that prevent unvalidated, highly-leveraged, or overly-correlated models from reaching live execution.

---

## 1. Non-Bypassable Promotion Gates

A model cannot move from "Experimental" to "Production" state without passing a series of programmatic checks. These checks are hard-coded into the `GovernanceGateway` and cannot be overridden by researchers or agents.

```
       +---------------------------------------------+
       |             Candidate Model                 |
       +---------------------+-----------------------+
                             |
                             v
       +---------------------+-----------------------+
       |   Gate 1: Statistical Significance          |
       |   - DSR >= 0.95                             |
       |   - Multiple testing p-value adjusted       |
       +---------------------+-----------------------+
                             | PASS
                             v
       +---------------------+-----------------------+
       |   Gate 2: Robustness Check                  |
       |   - PBO <= 0.10                             |
       |   - Bootstrap 5th percentile Sharpe > 0     |
       +---------------------+-----------------------+
                             | PASS
                             v
       +---------------------+-----------------------+
       |   Gate 3: Risk & Correlation Limits         |
       |   - Max Correlation to existing port < 0.30 |
       |   - Estimated Max Drawdown within budget    |
       +---------------------+-----------------------+
                             | PASS
                             v
       +---------------------+-----------------------+
       |   Gate 4: Peer Review Consensus             |
       |   - Human + LLM Critic Approval Sign-off    |
       +---------------------+-----------------------+
                             | PASS
                             v
       +---------------------+-----------------------+
       |   Promoted to Live Model Registry           |
       +---------------------------------------------+
```

---

## 2. Immutable Cryptographic Audit Trails

All state transitions inside the Governance Gateway are logged to an append-only transaction ledger. Each entry is cryptographically signed using standard hash-chaining (similar to a block ledger or git commit log).

### Audit Log Fields
* `timestamp`: ISO-8601 UTC time.
* `event_type`: "HYPOTHESIS_REGISTERED" | "EXPERIMENT_COMPLETED" | "MODEL_PROMOTED" | "MODEL_SUSPENDED".
* `actor_id`: The ID of the researcher or agent who initiated the event.
* `artifact_id`: UUID of the associated hypothesis, experiment, or model.
* `previous_log_hash`: SHA-256 hash of the prior audit log entry.
* `current_entry_hash`: SHA-256 hash computed over this entry's fields + `previous_log_hash`.

This structure guarantees that no team member can retroactively alter experiment results, cover up failed runs, or bypass approval dates. It provides a complete, bulletproof audit trail for regulatory and compliance review.

---

## 3. Operational Risk Controls

In addition to static promotion checks, the Governance Gateway manages live risk limits:

* **Capacity Constraints:** Every strategy is assigned an estimated liquidity-based capacity limit. If the asset size allocated to the model exceeds this limit, the orchestrator triggers an automatic scale-down.
* **Correlation Caps:** To prevent systemic portfolio crowding, the system computes the correlation between the candidate model's historical returns and the active portfolio's returns. If the correlation exceeds $0.30$, the model is rejected or restricted to hedging allocations.
* **Fail-Safe Circuit Breakers:** If a model's live drawdown exceeds its backtest maximum drawdown limit (at a selected confidence interval, e.g., $99\%$ VaR), the live risk engine instantly halts the model and triggers an automated post-mortem investigation.
