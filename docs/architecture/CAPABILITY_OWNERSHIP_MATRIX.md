# Capability Ownership Matrix
## Single Authority Responsibility Mapping Across Layers

### 1. Primary Cognitive Domains & Single Authority Owners

To guarantee zero logical duplication across Research OS, EIOS, EOS, AEAN, and APODEX, every core system capability is explicitly mapped to exactly one canonical module owner.

```
+----------------------------+-----------------------------------+-----------------------------------+
| Cognitive Domain           | Canonical Owner Module            | Layer Assignment                  |
+----------------------------+-----------------------------------+-----------------------------------+
| Literature Review & Papers | apodex/ai_eos/research/           | Layer 1: Research OS              |
| Statistical Validation     | apodex/research_os/               | Layer 1: Research OS              |
| Genetic Code Rewrites      | apodex/ai_eos/research/           | Layer 1: Research OS              |
| Active Inference Sensing   | apodex/arcs/kernel/               | Layer 2: EIOS                     |
| Entrepreneurial Loops      | apodex/ai_eos/intelligence/       | Layer 2: EOS                      |
| 14-Layer Business Engine   | apodex/ai_eos/intelligence/       | Layer 2: EOS                      |
| Capital & Portfolio Sizing | apodex/cognition/                 | Layer 2: EOS / Layer 3: AEAN      |
| Multi-Agent Planning & GoT | apodex/planning/, apodex/cognition| Layer 3: AEAN                     |
| Multi-Graph World Model    | apodex/world_model/               | Layer 3: AEAN                     |
| Multi-Tier Memory (CMOS)   | apodex/memory/                    | Layer 3: AEAN                     |
| Skill & Tool Invention     | apodex/skills/                    | Layer 3: AEAN                     |
| Personal Evolution (PEP)   | apodex/execution/                 | Layer 4: APODEX Platform          |
| Governance & Safety Core   | apodex/governance/, apodex/safety/| Layer 4: APODEX Platform          |
| Verifiers & Critics        | apodex/meta/, apodex/reasoning/   | Layer 4: APODEX Platform          |
+----------------------------+-----------------------------------+-----------------------------------+
```

---

## 2. Elimination of Legacy Adapter Logical Duplication

The root-level `agent_harness/` package is maintained exclusively as a lightweight backward-compatibility adapter layer delegating all business logic directly to canonical modules in `apodex/`:

1. **Memory Adapters**: `agent_harness.core.memory` wraps `apodex.memory.emg_engine` and `apodex.memory.semantic_memory`.
2. **Orchestration Adapters**: `agent_harness.core.runtime.orchestration` wraps `apodex.cognition.brain` and `apodex.planning`.
3. **Reasoning Adapters**: `agent_harness.core.runtime.reasoning` wraps `apodex.reasoning`.
4. **Observer Adapters**: `agent_harness.components` wraps `apodex.evolution.self_harness`.

---

## 3. Subsystem Function Ownership Details

### Layer 1: Research OS
- **Canonical Method**: `ResearchOS.conduct_literature_review()`
  - Authority: Single source of truth for research query synthesis over `AI_EOS_RESEARCH_DB.yaml` and `ALPHA_ALGO_100_NEW_RESEARCH.yaml`.
- **Canonical Method**: `CodeRewriteEngine.propose_rewrite()`
  - Authority: Single source of truth for AST syntax validation and GRC linting.

### Layer 2: EIOS / EOS
- **Canonical Method**: `EIOSKernel.sense_opportunity_anomalies()`
  - Authority: Single source of truth for Active Inference EFE metric calculations.
- **Canonical Method**: `EOSEngine.ingest_validated_research()`
  - Authority: Single source of truth for integrating research hypotheses into active business execution state.

### Layer 3: AEAN
- **Canonical Method**: `CognitiveBrain.think()`
  - Authority: Single source of truth for multi-agent ReAct and GoT reasoning execution.
- **Canonical Method**: `SkillRegistry.get_skill()`
  - Authority: Single source of truth for strategic/operational skills and decay filtering.

### Layer 4: APODEX Platform
- **Canonical Method**: `SafetyCore.verify_action()`
  - Authority: Single source of truth for immutable safety boundary enforcement and tiered approval evaluation.
