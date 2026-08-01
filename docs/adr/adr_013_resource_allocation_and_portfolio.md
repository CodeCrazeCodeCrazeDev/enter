# ADR 013: Capital Allocation, Venture Portfolio, and Organizational Design

## Status
Approved

## Context
Legacy capital allocation uses stochastic division with heuristic 25% budget caps, failing to account for the opportunity cost of capital or systemic organizational bottlenecks.

## Decision
We implement a Bayesian Thompson Sampling Capital Allocator that optimizes Expected Discovery Value vs. ROI utility. It tracks dual shadow price variables (Lagrange multipliers $\lambda$) over process latencies to automatically isolate binding organizational constraints.

## Consequences
- **Pros:**
  - Maximizes long-term option value and capital efficiency of active exploration paths.
  - Provides early-warning bottleneck identification.
- **Cons:**
  - Requires continuous, high-fidelity latency and ledger telemetry.
