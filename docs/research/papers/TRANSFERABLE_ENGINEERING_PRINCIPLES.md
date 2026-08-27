# Transferable Engineering Principles from 200-Paper AI-EOS Research Corpus

This document formalizes the core transferable engineering principles extracted from the 200-paper AI-EOS Research Corpus (`docs/research/papers/AI_EOS_RESEARCH_DB.yaml`). Each principle bridges academic research into executable architecture across the four core layers of the Cognitive Operating System:

1. **Layer 1: Research OS** (Autonomous Science Engine & Literature Review)
2. **Layer 2: EIOS Kernel & EOS** (Active Inference Sensing & Business Decision Loop Engine)
3. **Layer 3: AEAN** (Adaptive Evolutionary Agent Network & Multi-Agent Intelligence)
4. **Layer 4: APODEX Platform** (Execution, Memory, & Tooling Runtime)

---

## Principle 1: Active Inference & Expected Free Energy (EFE) Routing
- **Subsystems:** EIOS Kernel, ResearchOS, AEAN Routing
- **Foundational Research:** Papers #75-#90 (Active Inference, Curiosity-Driven Planning, Autonomous Science)
- **Concept:** Task routing and opportunity sensing are driven by minimizing Expected Free Energy (EFE), which balances Pragmatic Value (expected reward / success rate) and Epistemic Information Gain (curiosity / uncertainty reduction) subject to financial budget limits:
  $$\text{EFE} = \text{Epistemic Value} + \text{Pragmatic Value} - \text{Financial Cost Penalty}$$
- **Implementation:** Integrated into `LearnableRoutingGateDispatcher` in `apodex/ai_eos/research/integration.py` and `EIOSKernel` sensing in `apodex/arcs/kernel/kernel.py`.

## Principle 2: Pearl's Causal Do-Calculus & Counterfactual Intervention Analysis
- **Subsystems:** EOS Decision Engine, ResearchOS
- **Foundational Research:** Papers #130-#150 (Causal Reasoning, Counterfactual Auditing, SCM Interventions)
- **Concept:** Evaluate strategic interventions by computing structural causal model (SCM) do-interventions $P(Y \mid \text{do}(X))$ rather than observational correlations $P(Y \mid X)$, eliminating confounding factors during business loop optimization.
- **Implementation:** Integrated into `EOSEngine` hypothesis verification and `ResearchOS` experimental design.

## Principle 3: Self-Referential AST Code Rewrite & AST Security Verification
- **Subsystems:** AEAN Self-Evolution, ResearchOS
- **Foundational Research:** Papers #8-#15 (Self-Referential Code Generation, STOP, Gödel Machines, Self-Improvement)
- **Concept:** Enable autonomous code modification through AST syntax parsing, sandboxed dry-run simulation, and static security linting (GRC rule check preventing `eval`, `exec`, or un-sandboxed process spawns).
- **Implementation:** `CodeRewriteEngine` in `apodex/ai_eos/research/integration.py`.

## Principle 4: Genetic Workflow Mutation & MAP-Elites Quality Diversity
- **Subsystems:** AEAN Optimization, ResearchOS
- **Foundational Research:** Papers #90-#98 (ShinkaEvolve, FunSearch, Evolutionary Program Search)
- **Concept:** Evolve agent prompts and execution parameters via island-based genetic algorithms featuring Gaussian parameter mutation, semantic prompt mutation, and MAP-Elites fitness scoring.
- **Implementation:** `GeneticWorkflowOptimizer` in `apodex/ai_eos/research/integration.py`.

## Principle 5: Advantage Estimation & DPO Preference Record Synthesis
- **Subsystems:** AEAN Alignment, ResearchOS
- **Foundational Research:** Papers #16-#32, #99-#104 (Self-Rewarding AI, RLVR, GRPO, Preference Optimization)
- **Concept:** Compute temporal-difference advantage values across agent trajectories to synthesize high-margin chosen vs. rejected Direct Preference Optimization (DPO) records for offline alignment.
- **Implementation:** `SFTPreferenceCollector` in `apodex/ai_eos/research/integration.py`.

## Principle 6: Hexagonal Isolation of Strategic Planning from Execution
- **Subsystems:** AEAN Planning, EOS Strategy
- **Foundational Research:** Papers #64-#74 (Agentic Reasoning & Acting, Hexagonal Agent Systems)
- **Concept:** Keep strategic planning history strictly isolated from task execution outputs to prevent context contamination and context-window bloat. Strategic planners generate immutable roadmaps, while task executors process granular actions.
- **Implementation:** `StrategicPlanner` and `PlanVerifier` in AEAN cognitive architecture.

## Principle 7: Multi-Tier Memory Consolidation & Ebbinghaus Decay Filtering
- **Subsystems:** AEAN CMOS, ResearchOS Memory
- **Foundational Research:** Papers #119-#128 (Long-Horizon Agents, Memory Systems, MemoHarness)
- **Concept:** Separate short-term sliding context history from persistent SQLite semantic memory. Apply exponential Ebbinghaus decay to prune low-confidence or stale memory nodes while promoting high-utility evidence cards.
- **Implementation:** CMOS Memory Architecture in `apodex/memory/` and `agent_harness`.

## Principle 8: Model-Collapse Guard via Quality Downsampling
- **Subsystems:** AEAN Learning, ResearchOS Ingestion
- **Foundational Research:** Papers #1-#7, #105-#118 (Model-Collapse Prevention, Scalable Oversight)
- **Concept:** Automatically track the ratio of self-generated trajectory data vs. ground-truth traces. Downsample low-scoring self-generated traces or enforce strict threshold bounds to avoid recursive model collapse during self-training.
- **Implementation:** Trajectory compiler in `apodex/ai_eos/research/integration.py`.

## Principle 9: Two-Level Credit Assignment
- **Subsystems:** AEAN Multi-Agent Coordination, EOS Business Loops
- **Foundational Research:** Papers #49-#63 (Multi-Agent Systems, Credit Assignment)
- **Concept:** Combine overall trajectory outcome evaluation with progressive step-level contribution scoring ($+1.0 \times \frac{i}{N}$ for positive progress, $-0.2 \times \frac{i}{N}$ for step regressions).
- **Implementation:** Multi-agent credit engine in `apodex/aean/` and `agent_harness`.

## Principle 10: Multi-Agent Swarm Debate & Sycophancy Mitigation
- **Subsystems:** AEAN Swarm, ResearchOS Hypothesis Auditing
- **Foundational Research:** Papers #105-#118 (Scalable Oversight, Multi-Agent Debate, Constitutional AI)
- **Concept:** Mitigate compliance and sycophancy bias by conducting structured multi-agent cross-examination debate with adversarial red-teaming prior to promoting hypotheses or executing strategic business decisions.
- **Implementation:** Swarm debate protocols in `apodex/aean/coordination/hive_mind.py`.
