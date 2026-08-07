# ADR 008: First-Principles Redesign and Integration of the Entrepreneurial Operating System (EOS)
**Status:** Approved
**Date:** August 2026
**Author:** Jules, Software Engineer

---

## 1. Context

The Entrepreneurial Operating System (EOS) specification presents a rigorous, first-principles reconstruction of how elite founders sense, validate, and compound enduring companies. Historically, entrepreneurship modeling was treated as a linear set of isolated modules or procedural skills (pricing, marketing, sales).

This ADR addresses the fundamental architectural question:
**"If our current cognitive subsystems (Research OS, AEAN, EIOS, EOS, APODEX) did not already exist, would we design them as separate, disconnected components today?"**

The answer is **No**. Under first-principles systems engineering, a unified Cognitive Operating System must treat opportunity sensing, hypothesis generation, GTM reasoning, pricing intelligence, and capital allocation as **native, shared cognitive capabilities of the primary execution kernel**, rather than isolated business plugins.

---

## 2. Decision

We decide to:
1. **Unify the Execution Substrate:** Converge all strategic reasoning and business feedback loops into the central `EIOSKernel` inside `apodex/arcs/kernel/kernel.py`.
2. **De-silo Capabilities:** Expose opportunity sensing, falsifiable hypothesis generation, validation economics, GTM channel-fit reasoning, moat analysis, lifecycle stage classification, and strategic reinvention reviews as native, first-class Python methods on `EIOSKernel`.
3. **Establish a Causal Active Inference Loop:** Govern the kernel's planning paths through explicit Expected Free Energy (EFE) minimization, and backpropagate failures to prevent model ossification.

---

## 3. Replacement Architecture

```
                  +-----------------------------------+
                  |            EIOSKernel             |
                  |  - Central Core of Cognitive OS   |
                  +-----------------+-----------------+
                                    |
     +------------------------------+------------------------------+
     |                              |                              |
     v                              v                              v
[Sensing Engine]            [Validation Engine]            [Strategic Planner]
- Anomalies & Shifts        - CAC, LTV & Payback           - GTM Channels & Moats
- Falsifiable Claims        - Capital Routing & Cost       - Lifecycle & Reinvention
```

### 3.1 Code Footprint Updates
We will inject these methods directly into the `EIOSKernel` inside `apodex/arcs/kernel/kernel.py` to ensure they are globally accessible to the Autonomous Agent Network:
* `sense_opportunity_anomalies`
* `generate_falsifiable_hypothesis`
* `validate_opportunity_economics`
* `allocate_capital_opportunity`
* `reason_gtm_channel`
* `analyze_moat_durability`
* `evaluate_lifecycle_stage`
* `trigger_reinvention_review`

---

## 4. Migration Strategy

1. **Phase 1: Substrate Upgrade:** Add the new native capabilities directly to the `EIOSKernel` class. Maintain backward compatibility with the existing `ExecutionDAG` scheduling methods.
2. **Phase 2: Test Convergence:** Build a complete test suite `tests/ai_eos/test_eos_unified_cognition.py` to verify each of these new native capabilities.
3. **Phase 3: Skill Deprecation:** Decommission procedural, hardcoded business skills in `apodex/skills/` and route them through the kernel's native capabilities.

---

## 5. Deprecation Plan

* **Step 1:** Mark legacy procedural business planning models in `apodex/ai_eos/intelligence/decision_engine.py` as deprecated.
* **Step 2:** Issue compiler warnings if external adapters attempt to invoke `EntrepreneurialIntelligenceSystem` directly instead of scheduling queries through `EIOSKernel`.
* **Step 3:** Fully retire legacy procedural paths in Version 2.0.0.
