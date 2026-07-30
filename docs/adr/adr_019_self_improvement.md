# ADR 019: Self-Improvement via Textual Backpropagation

## Status
Proposed

## Context
Standard agent prompt optimization is heuristic, manual, and does not align prompt gradients based on clear textual feedback of execution performance.

## Decision
We implement a Self-Improvement Engine that mimics textual backpropagation (TextGrad). Prompt configurations are refined by optimizing loss feedback strings paired with performance deltas.

## Alternatives Considered
- **Direct Genetic Prompt Swapping (Rejected)**: No gradient-like semantic direction, very high exploration cost.

## Expected Benefits
- Faster and highly targeted optimization of agent instructions.

## Failure Modes
- **Semantic Overfitting**: Mitigated by validating prompts against a diverse dataset of general tests.

## Validation Plan
Run prompt-feedback optimization cycles and measure target benchmark improvement scores.
