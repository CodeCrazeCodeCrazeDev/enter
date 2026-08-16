# Cognitive OS Subsystem Dependency Graph & Event Flow Specification

## 1. Top-Level System Directed Acyclic Graph (DAG)

The unified Cognitive Operating System enforces a strict top-down operational dependency DAG. Information, evidence, and strategy flow downstream from Research OS through AEAN and EIOS/EOS down to APODEX. Telemetry, observations, and runtime events flow upstream asynchronously.

```
                    +--------------------------------+
                    |       LAYER 1: RESEARCH OS     |
                    | (ResearchOS, HypothesisEngine) |
                    +--------------------------------+
                                    |
                        [P1: Literature / Empirical Cards]
                                    v
                    +--------------------------------+
                    |         LAYER 2: AEAN          |
                    |   (HiveMind, ActiveInference)  |
                    +--------------------------------+
                                    |
                        [P2: Cognitive Directives / Policies]
                                    v
                    +--------------------------------+
                    |      LAYER 3: EIOS / EOS       |
                    |   (EIOSKernel, EOSManager)     |
                    +--------------------------------+
                                    |
                        [P3: Execution Instructions / Substrate Tasks]
                                    v
                    +--------------------------------+
                    |        LAYER 4: APODEX         |
                    |  (CMOSEngine, SkillRegistry)   |
                    +--------------------------------+
```

---

## 2. Layer-by-Layer Interface Contracts & Interactions

### 2.1 Research OS $\to$ AEAN Interface Contract
- **Protocol**: Direct Async Invocations / Scientific Artifact Dispatch
- **Direction**: Downstream
- **Primary Method**: `ResearchOS.conduct_literature_review(query: str) -> List[EvidenceCard]`
- **Data Payload**: `EvidenceCard(paper_id, title, empirical_findings, transferable_principles, confidence_score)`
- **Behavior**: AEAN queries Research OS when facing unfamiliar decision domains or high uncertainty ($\text{Epistemic EFE} > \tau_{\text{uncertainty}}$). Research OS retrieves verified paper evidence from `AI_EOS_RESEARCH_DB.yaml` and returns synthesized principles.

### 2.2 AEAN $\to$ EIOS / EOS Interface Contract
- **Protocol**: Strategic Decision & Policy Dispatch
- **Direction**: Downstream
- **Primary Method**: `HiveMind.orchestrate_strategic_goal(goal_spec: Dict[str, Any]) -> PolicyDirective`
- **Data Payload**: `PolicyDirective(target_action, expected_free_energy, causal_intervention_path, swarm_consensus_ratio)`
- **Behavior**: AEAN evaluates candidate strategic actions using Expected Free Energy ($G(\pi)$) and Pearl's Do-Calculus. Once swarm consensus is reached, the optimal `PolicyDirective` is passed to the EIOS Kernel.

### 2.3 EIOS / EOS $\to$ APODEX Interface Contract
- **Protocol**: Substrate Task & Skill Execution Dispatch
- **Direction**: Downstream
- **Primary Method**: `EIOSKernel.execute_business_loop(loop_type: BusinessLoopType, params: Dict[str, Any]) -> LoopResult`
- **Data Payload**: `TaskExecutionSpec(skill_name, execution_context, safety_tier, memory_checkpoint_id)`
- **Behavior**: EIOS Kernel breaks down business loop targets (e.g., GTM optimization, financial arbitrage, product reinvention) into individual atomic skills registered inside APODEX `SkillRegistry`.

### 2.4 APODEX $\to$ Upper Layers Asynchronous Event Feedback
- **Protocol**: Event Bus / Telemetry Upstream Broadcasting
- **Direction**: Upstream
- **Primary Events**:
  - `RealityStateUpdatedEvent(entity_id, updated_state, confidence)`
  - `SkillExecutedEvent(skill_id, success, execution_time_ms, metrics)`
  - `SafetyGateTriggeredEvent(action_id, violation_type, risk_score)`
- **Behavior**: APODEX publishes runtime state updates to the event bus. Higher layers (AEAN, EIOS) subscribe to these events to dynamically update their latent belief state $q(\theta)$ and re-calibrate policies.

---

## 3. Module & Package Level Dependency Matrix

To ensure absolute architectural purity, the table below defines allowed and forbidden import dependencies across the `apodex/` codebase:

| Owning Module | Allowed Dependencies (Imports) | Strictly Forbidden Dependencies |
| :--- | :--- | :--- |
| `apodex.ai_eos.research` (Research OS) | Standard Library, `yaml`, `numpy`, `scipy` | `apodex.aean`, `apodex.arcs`, `apodex.skills` |
| `apodex.aean` (AEAN) | `apodex.ai_eos.research`, Standard Library, `pydantic` | `apodex.arcs`, `agent_harness` |
| `apodex.arcs` / `apodex.ai_eos.intelligence` (EIOS/EOS) | `apodex.aean`, `apodex.ai_eos.research`, `apodex.memory` | `agent_harness` |
| `apodex.memory` / `apodex.skills` (APODEX) | Standard Library, `pydantic`, `sqlmodel` | `apodex.aean`, `apodex.ai_eos` |
| `agent_harness` (Compatibility Layer) | `apodex.*` (Routing only) | Logic implementations |

---

## 4. Invariant Enforcement & Circular Dependency Prevention

1. **Static Analysis Rule**: The repository includes `scripts/validate_dependencies.py` to continuously verify that max dependency depth is $\le 6$ and that no circular imports exist.
2. **Adapter Neutrality Rule**: `agent_harness` adapters act purely as forwarding proxies to `apodex.*` canonical classes and MUST NOT contain domain state or business logic.
3. **Event Decoupling Rule**: All cross-layer notification flows MUST occur asynchronously via `EventPublisher` / `EventSubscriber` patterns, preventing blocking coupling across system tiers.
