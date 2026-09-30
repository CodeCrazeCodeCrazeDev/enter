# ADR 018: Evaluation Engine for Autonomous Upgrades

## Status
Proposed

## Context
Continuous self-improvement is dangerous if system modifications are made without passing objective quality gates, leading to silent regressions and behavioral drift.

## Decision
We implement a dedicated, independent Evaluation Engine that enforces non-bypassable, automated verification gates. No self-modification proposals can be integrated without passing baseline checks.

## Alternatives Considered
- **Direct Code In-place Integration (Rejected)**: Extremely high regression risks and lack of recovery rollback hooks.

## Expected Benefits
- Guaranteed regression-free self-improvement upgrades.
- Complete performance traceability logs.

## Failure Modes
- **Upgrade Loop Hang**: Handled by setting strict evaluation timeout parameters.

## Validation Plan
Run upgrade verification pipeline simulation and ensure faulty upgrades are successfully blocked.
