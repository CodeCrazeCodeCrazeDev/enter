# ADR 015: Simulation Engine with Value-at-Risk (VaR) Estimation

## Status
Proposed

## Context
Executing large scale financial or business plans without probabilistic simulations of worst-case scenarios exposes the agent to catastrophic black swan losses.

## Decision
We implement a Monte Carlo-based Simulation Engine. It takes branching plan step paths, executes parallel universe rollouts, and estimates Value-at-Risk (VaR) parameters at a strict confidence level.

## Alternatives Considered
- **Direct LLM Scenario Generation (Rejected)**: Purely qualitative and uncalibrated risk metrics.

## Expected Benefits
- Computes portfolio VaR in $< 10\text{ ms}$.
- Accurate risk propagation across branching future pathways.

## Failure Modes
- **Extreme Variance Divergence**: Handled by capping outlier simulation step variance coefficients.

## Validation Plan
Verify computed VaR limits mathematically against a normal distribution cumulative density function.
