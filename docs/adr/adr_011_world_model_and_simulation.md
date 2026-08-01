# ADR 011: World Model, Market, and Customer Simulation

## Status
Approved

## Context
The legacy stochastic transition model runs flat linear updates with unclipped variables, leading to parameter drift and unphysical simulation regimes.

## Decision
We implement a Causal World Model Graph that maps environment variables onto structured structural causal equations ($Y = f(X, U)$). This is coupled with a Monte Carlo simulator executing 1,000 parallel customer agent trajectories using non-linear willingness-to-pay and retention decay distributions.

## Consequences
- **Pros:**
  - Eliminates parameter drift and ensures mathematically valid simulations.
  - Enables counterfactual and scenario-tree planning before real capital spend.
- **Cons:**
  - Higher computational overhead for multi-sample path simulations.
