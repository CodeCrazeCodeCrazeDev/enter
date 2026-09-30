# ADR 016: Adaptive Multi-Agent Runtime & Dispute Debate

## Status
Proposed

## Context
Standard multi-agent swarms have rigid roles, suffer from sycophancy, can get stuck in agreement feedback loops, and waste compute.

## Decision
We implement an adaptive Multi-Agent Runtime. Agents are spawned, split, merged, or retired dynamically based on workload characteristics. Disagreements are settled using turn-based debate protocols with independent, randomized voting to mitigate sycophancy.

## Alternatives Considered
- **Static Multi-Agent Swarms (Rejected)**: Causes high duplication of responsibility, cannot scale down dynamically, and suffers from sycophancy.

## Expected Benefits
- Zero duplicate agent roles.
- Highly resilient dispute resolution and objective decision consensus.

## Failure Modes
- **Debate Deadlock**: Prevented by applying a max turn-taking limit and falling back to a weighted majority vote.

## Validation Plan
Run debates with simulated biased agents and measure alignment convergence.
