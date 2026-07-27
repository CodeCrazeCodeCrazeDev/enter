# AI-EOS Gap Analysis

This document identifies outstanding capabilities and structural/architectural conflicts identified during research evaluations.

## 1. Identified Capability Gaps
- **Traceback Path Repair (L1):** No automated graph repair is executed.
- **Calibrated Task Stopping (L1/L2):** Long-horizon agents get locked in context windows without automatic downshifting.
- **Decentralized Aspect-Verifiers (L3):** Verification is monolithic inside the current gateway structure.

## 2. Research Paralyzed or Restricted
- **Online RL VR (#99 DeepSeek-R1):** Unsuitable for real-time loops due to latency. Kept as offline SFT compiler datasets.
- **FunSearch/AlphaEvolve Evolution (#90):** Restricted to sandboxed Docker containers to prevent unauthorized filesystem access.
