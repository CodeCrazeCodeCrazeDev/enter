# ADR 020: Non-Bypassable Governance Layer

## Status
Proposed

## Context
Rogue agent actions, security command injections, or budget overruns represent critical risk scenarios that cannot be left to non-deterministic model checks.

## Decision
We implement a hardcoded, non-bypassable programmatic Governance Layer. All proposed execution actions must pass hard-coded constraint schemas (budget limits, toxic command blacklist blocks) before dispatch.

## Alternatives Considered
- **LLM-based Moderation (Rejected)**: Highly non-deterministic, introduces heavy latency ($> 1\text{ s}$), and bypassable via jailbreaks.

## Expected Benefits
- Near-zero latency vetoes ($< 2\text{ ms}$).
- $100\%$ security and budget bounds enforcement.

## Failure Modes
- **Constraint Over-strictness**: Mitigated by defining clean, narrow-scoped venture exceptions.

## Validation Plan
Unit test with toxic command payloads and out-of-bound budget requests to ensure perfect veto enforcement.
