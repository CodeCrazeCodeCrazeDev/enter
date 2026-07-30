# ADR 012: Deep Causal World Model with Judea Pearl's do-calculus

## Status
Proposed

## Context
Existing predictive models lack calibration, suffer from hallucinations, and cannot perform counterfactual or causal reasoning when simulating downstream effects of strategic decisions.

## Decision
We implement an explicit Deep Causal World Model employing conjugate Bayesian updating and Judea Pearl's do-calculus. It maps variables in a directed acyclic graph (DAG) representing the SCM (Structural Causal Model) and adjusts belief states via backdoor criteria interventions.

## Alternatives Considered
- **Direct LLM Prompt Projections (Rejected)**: No mathematical probabilistic calibration, vulnerable to hallucinated correlations instead of causation.

## Expected Benefits
- Mathematically grounded counterfactual estimation.
- Probabilistic prediction calibration error (MSE) $< 0.05$.

## Failure Modes
- **Causal Loop Detection**: Handled by DAG validation on edge registration.
- **Under-confidence**: Mitigated by updating belief confidence weights with high-quality evidence cards.

## Validation Plan
Run synthetic market intervention trials and verify against exact Bayesian update equations.
