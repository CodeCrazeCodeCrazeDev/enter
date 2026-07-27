# Scientific Evaluation and AQRI Gap Analysis: MemoHarness Integration Evaluation for AEAN

**Document ID:** AQRI-REV-2026-0042
**Subject Paper:** *MemoHarness: Agent Harnesses That Learn from Experience* (arXiv:2607.14159)
**Evaluator:** Jules, Lead Research Scientist, AEAN Metasystem Sub-Committee
**Status:** Preregistered Evaluation & Comparative Analysis
**EIOS Governance Directive:** Unified Cognitive OS and Frozen Baseline Preservation Under Evidence-Based improvement Protocol (arXiv:2605.15245)

---

## Executive Summary

This report delivers a rigorous, scientific evaluation of the *MemoHarness* framework (Huang et al., 2026) for potential integration into the Autonomous Entrepreneurial Agent Network (AEAN) cognitive meta-system. Operating as a research scientist within the Evidence-Based Self-Improving Organization (EIOS) protocol, we treat MemoHarness not as an architectural authority, but as a candidate body of evidence.

Our comparative analysis reveals that while the paper's core insights around structured harness decomposition and episodic-semantic experience dualism are sound, **the AEAN frozen baseline already contains superior, more generalized implementations of these concepts** (specifically through our AReaL execution protocol, 5-Tier Memory Architecture, SkillRegistry, and CMOS cognitive operators).

Consequently, we recommend **REJECTING** any broad structural changes to the core memory, skill registry, and control plane layers of the frozen AEAN baseline, while recommending **PROTOTYPING ONLY** for the case-specific test-time lexical-retrieval routing mechanism as an experimental plug-in inside our existing `SelfImprovementOrchestrator` under a preregistered AQRI validation protocol.

---

## Phase I — Scientific Evaluation of MemoHarness

### 1. Technical Paper Review & Architectural Claims
MemoHarness introduces an adaptive framework that optimizes an LLM's surrounding control layer (the "harness") rather than narrow prompts or pipelines. Its core thesis is that a single static global harness configuration is suboptimal across diverse tasks. Instead, MemoHarness proposes that an agent should learn from its execution history through a feedback loop, distilling global patterns and retrieving specific instance traces to dynamically adapt the harness at test time without gradient updates, test-time labels, or additional searches.

The paper claims three main contributions:
1. **Six-Dimensional Harness Space:** Decomposes the monolithic harness along the temporal flow of inference into distinct functional control surfaces: Context assembly ($D_1$), Tool interaction ($D_2$), Generation control ($D_3$), Orchestration ($D_4$), Memory management ($D_5$), and Output processing ($D_6$).
2. **Dual-Layer Experience Bank:** Accumulates per-case diagnostic execution entries (episodic layer) and extracts generalized cross-case regularities (semantic/distilled global patterns layer) via a periodic distillation operator.
3. **Test-Time Case Adaptation:** Specializes the search-derived global harness ($W^*$) to an individual test-case harness ($W(x_j)$) using retrieved experiences from the dual-layer bank, adhering to a "correctness-first" policy that uses execution cost (token count) solely as a tiebreaker.

### 2. Algorithm Extraction & Formal Mathematical Model

The MemoHarness workflow operates in two phases: **Training-Time Search (Phase A)** and **Test-Time Adaptation (Phase B)**.

```
+---------------------------------------------------------------------------------+
|                               PHASE A: SEARCH                                   |
|                                                                                 |
|  Initial Harness W_0 ---> Candidate W_t ---> Execute on D_search ---> Trace τ_i |
|                                ^                                        |       |
|                                |                                        v       |
|                        Update Search Policy <--- Distill Global G_t <-- Diagnose|
+---------------------------------------------------------------------------------+
                                                                          |
                                                                          v
+---------------------------------------------------------------------------------+
|                         PHASE B: TEST-TIME ADAPTATION                           |
|                                                                                 |
|  Test Case x_j ---> Retrieve Similar Successes (N^+) & Failures (N^-)           |
|                                |                                                |
|                                v                                                |
|  Global Harness W^* ---> Adaptation Operator ---> Specialized W(x_j)            |
|                                |                                                |
|                                v                                                |
|                         Run on Model ---> Final Output ŷ_j                      |
+---------------------------------------------------------------------------------+
```

#### A. Optimization State Space
Let $\mathcal{W}$ be the product space of the six functional dimensions:
$$\mathcal{W} = \prod_{d=1}^{6} \mathcal{W}^{(d)}$$
Where each $W = (W^{(1)}, \dots, W^{(6)}) \in \mathcal{W}$ is a discrete configuration tuple.

#### B. Execution Trajectory $\tau_i(W)$
For each case $x_i = (u_i, \phi_i, y_i^\star)$ executed under configuration $W$, the system logs:
$$\tau_i(W) = \bigl(y_i(W), \mathcal{M}_i(W), \kappa_i(W)\bigr)$$
where:
* $y_i(W)$ is the generated final prediction.
* $\mathcal{M}_i(W)$ captures invoked tools, intermediate traces, and parameters.
* $\kappa_i(W) = (n_i^{\mathrm{call}}, n_i^{\mathrm{tok}}, \ell_i)$ records call count, raw input/output tokens, and latency.

#### C. Correctness-First Objective Function
The secondary cost proxy $c_i(W)$ is defined strictly by token consumption:
$$c_i(W) = n_i^{\mathrm{tok}}(W)$$
The primary task reward is $r_i(W) = R(y_i(W), y_i^\star)$. Candidate selection uses a lexicographical ordering where reward is strictly maximized first, and token usage acts as a secondary tiebreaker:
$$W^\star \in \operatorname{arg\,max}_{\mathrm{lex},\, W_t \in \mathcal{C}_{\mathrm{feas}}} \bigl(\bar{r}_t, \, -\bar{c}_t\bigr)$$
$$\bar{r}_t = \frac{1}{n} \sum_{i=1}^{n} r_i(W_t), \quad \bar{c}_t = \frac{1}{n} \sum_{i=1}^{n} c_i(W_t)$$

#### D. Experience Bank Dual-Layer Schemas
The experience bank $\mathcal{B}_t$ is represented by the typed pair:
$$\mathcal{B}_t = (\mathcal{E}_t, \mathcal{G}_t)$$
* **Episodic Entry $\xi_i^{(t)} \in \mathcal{E}_t$:**
  $$\xi_i^{(t)} = \Bigl(i, \, t, \, \phi_i, \, W_t, \, \Delta_i^{(t)}, \, \tau_i(W_t), \, r_i(W_t), \, c_i(W_t), \, z_i^{(t)}\Bigr)$$
  where $\Delta_i^{(t)} = \Delta(W_t, W_i^{<t})$ is the configuration diff, and $z_i^{(t)}$ is the structured diagnosis containing success binary $s_i^{(t)}$, primary failure dimension $d_{i, \mathrm{prim}}^{(t)}$, and secondary dimensions $\mathcal{D}_{i, \mathrm{sec}}^{(t)}$.
* **Semantic Pattern $g_k \in \mathcal{G}_t$:**
  $$\mathcal{G}_t = \mathcal{G}_{t-1} \cup \mathrm{Distill}(\mathcal{E}_{\le t})$$
  Distilled via a pattern synthesizer operating on failure clusters over iterations.

#### E. Test-Time Adaptation Retrieval
Without iterative labels, an evaluation case $x = (u, \phi)$ triggers lexical/semantic neighborhood searches over $\mathcal{E}_T^+$ and $\mathcal{E}_T^-$ using instruction embeddings representation $\psi(u)$:
$$\rho_{\psi}(x, \xi) = \cos(\psi(u), \psi(u_{\xi}))$$
$$\mathcal{N}_K^+(x) = \operatorname{TopK}_{\xi \in \mathcal{E}_T^+} [\rho_{\psi}(x, \xi)], \quad \mathcal{N}_K^-(x) = \operatorname{TopK}_{\xi \in \mathcal{E}_T^-} [\rho_{\psi}(x, \xi)]$$
The adaptation controller generates the local case harness:
$$W(x) = \Pi_{\mathrm{test}}(W^\star, x, \mathcal{S}_{\mathrm{test}}(x))$$
$$\mathcal{S}_{\mathrm{test}}(x) = \bigl(\mathcal{N}_K^+(x), \, \mathcal{N}_K^-(x), \, \mathrm{Retrieve}(\mathcal{B}_T, Q_{\mathrm{test}}(x)), \, \mathcal{G}_T\bigr)$$

### 3. Critical Assessment of Strengths and Weaknesses

#### Design Assumptions
* **Assumption 1 (Sufficient Discrepancy):** Harness modifications alter task outcomes more predictably than underlying prompt template tweaks.
* **Assumption 2 (Local Cacheability):** Retrieved context is highly reusable across turns, preserving financial viability via prompt caching mechanisms.
* **Assumption 3 (Representational Separability):** The six control dimensions are orthogonal enough that changes to one (e.g., $D_3$ generation budget) can be optimized independently of others (e.g., $D_2$ tool settings).

#### Key Strengths
* **Structured Search Space:** Avoids the combinatorial explosion of editing unconstrained system prompts by focusing on six well-defined operational knobs.
* **Lexicographical Secondary Cost-Optimization:** Protects the agent from degrading its task quality in pursuit of cost cuts, which is highly aligned with safety principles.
* **Test-Time Customization without Retraining:** Enables individual tasks to become heavier or lighter based on empirical historical difficulty without updating model weights.

#### Hidden Weaknesses & Limits of the Paper
* **Tight Functional Coupling:** The claim of independent discrete editing is fragile. For instance, enabling external tools ($D_2$) changes the required prompt style ($D_1$), the maximum context length ($D_5$), and the validation patterns ($D_6$). Optimizing dimensions independently ignores cross-dimensional interaction terms, causing sub-optimal local minima.
* **Absence of Significance Testing:** The paper reports only point estimates for accuracy on a small Terminal-Bench subset (18 tasks). No statistical variances, confidence intervals, or p-values are calculated, risking overfitting to a tiny test split.
* **Heavy Dependence on Prompt Caching:** The cost-competitiveness of MemoHarness hinges entirely on aggressive prefix caching of retrieved historical traces (as shown by 13.32M cached tokens out of 14.18M in Table 4). In architectures or provider APIs where prefix caching is not supported, or when task order breaks cache locality, the cost increases by more than 200%, rendering it economically unfeasible.
* **Coarse Failure Mapping:** The diagnostic operator $g$ maps multi-step tool errors directly to coarse dimensions. This misses complex logic bugs where an error manifests in Output validation ($D_6$) but was caused by incorrect context assembly ($D_1$).

### 4. Computational and Memory Complexity Analysis

#### Memory Complexity
Let $|\mathcal{E}|$ be the number of episodic traces, and $|\mathcal{G}|$ be the count of distilled global rules. Each trace stores raw token sequences of length $L$.
* **Experience Bank Storage:** $\mathcal{O}(|\mathcal{E}| \cdot L + |\mathcal{G}|)$. For large-scale production agent fleets executing thousands of runs daily, direct episodic trace storage in the context window scales linearly and causes prompt-length inflation.
* **Context Overhead:** Retrieving $K_{\mathrm{succ}}$ and $K_{\mathrm{fail}}$ traces adds $\mathcal{O}((K_{\mathrm{succ}} + K_{\mathrm{fail}}) \cdot L)$ tokens to the prompt context. At $K = 10$, this easily introduces up to 50,000 extra context tokens per turn, increasing system prompt footprint dramatically.

#### Computational Complexity
* **Search Complexity:** $\mathcal{O}(T \cdot N \cdot C_{\mathrm{eval}})$ where $T$ is search rounds, $N$ is dataset size, and $C_{\mathrm{eval}}$ is the cost of running a full agent execution. This is extremely expensive ($\approx 180$ full multi-turn execution trajectories to evaluate a 10-round search on 18 tasks).
* **Test-Time Retrieval:** $\mathcal{O}(|\mathcal{E}| \cdot d)$ where $d$ is embedding dimensionality. This is negligible with local vector index storage but scales linearly with database growth.

---

## Phase II — AEAN Comparative Analysis & Gap Analysis

We compare the MemoHarness framework against the current, frozen architecture of the Autonomous Entrepreneurial Agent Network (AEAN) and World Model Creator (WMC).

### 1. Capability Overlap Analysis
Our existing AEAN architecture contains highly refined sub-systems that already implement or exceed the core paradigms of MemoHarness:

1. **Memory Tiering vs. Experience Bank:**
   * **MemoHarness:** Uses a dual-layer experience bank of episodic entries ($\mathcal{E}$) and distilled patterns ($\mathcal{G}$).
   * **AEAN / CMOS:** Implements a formalized, production-grade **5-Tier Memory Architecture** (T0 Working, T1 Episodic, T2 Semantic, T3 Decaying, T4 Procedural/Evergreen). Our T1 episodic store directly tracks execution traces, while our T2 semantic layer records distilled lessons and causal nodes.
2. **Harness Configuration vs. SkillRegistry & World Model Configuration:**
   * **MemoHarness:** Proposes six discrete knobs representing the harness space.
   * **AEAN / CMOS:** Features a central, programmatic **SkillRegistry** (with 60 specialized domain skills) and a unified declarative planning protocol (the **AReaL protocol** in `trajectory_areal.py`). AReaL manages step-level and turn-level constraints, tool gating, and budget downshifting directly at runtime, which is a superset of MemoHarness's discrete dimensions.
3. **Adaptive Routing vs. Personal Evolution Profile (PEP):**
   * **MemoHarness:** Adapts the harness via localized neighborhood retrieval of the closest success/failure traces.
   * **AEAN / CMOS:** Features a versioned, persistent **Personal Evolution Profile (PEP)** object that contains style preferences, cost-latency preferences, and vocabulary filters. This is paired with the `SelfImprovementOrchestrator` to automatically perform tiered approvals and rollbacks.

### 2. Missing, Redundant, and Conflicting Functionality

| Functional Component | MemoHarness Implementation | Existing AEAN Component | Evaluation Status |
| :--- | :--- | :--- | :--- |
| **Episodic Execution Recording** | Discrete execution entries with delta tracking ($\xi_i^{(t)}$) | T1 Episodic Memory + `AReaLDataProxy` / `ExecutionTrace` | **Redundant.** AEAN's traces are already fully structured and mapped onto a WorldGraph. |
| **Semantic Lesson Distillation** | Periodic pattern distillation operator ($\mathrm{Distill}$) | CMOS Memory Consolidation + `DistilledLesson` generation | **Redundant.** CMOS's scheduler runs active background consolidation of T1 into T2/T4. |
| **Harness Knob Representation (D1-D6)** | 6 discrete dimensions of pipeline control | AReaL Control Plane + `SkillRunner` / `ProtocolEngine` | **Equivalent.** AReaL represents runtime constraints (tokens, retries, prompts) via typed global params. |
| **Lexicographical Score Filter** | Lexicographical ordering on primary quality and token count | Suitability score formula $S(M)$ in PEP / Cost Profiles | **Inferior to AEAN.** MemoHarness uses raw token counts as a strict secondary tiebreaker. AEAN's suitability score $S(M)$ is a continuous multi-objective formula weighing quality, latency, token volume, and user satisfaction, offering better trade-off adjustments. |
| **Instance-level Retrieval of Failure Exemplars** | Retrieves top-K closest historical failed traces into the prompt | **None** (We retrieve semantic rules, but not direct raw trace sequences of past failures) | **Missing.** AEAN currently bypasses raw failure-trace context injection to preserve prompt windows and prevent LLM failure mimicry. |

### 3. Key Architectural Conflicts
1. **The Mimicry Threat (The Failure Re-Execution Conflict):**
   MemoHarness injects both success traces ($\mathcal{N}_K^+$) and raw failure traces ($\mathcal{N}_K^-$) into the adapter prompt. In high-parameter language models, injecting raw failure steps often causes **behavioral mimicry**, where the model incorrectly replicates the failure actions listed in its prompt context rather than avoiding them. AEAN's `SelfImprovementFlywheel` avoids this by translating failures into positive, declarative instructions (rules) stored in T2 Semantic memory, never injecting raw error traces directly into the execution context.
2. **Context Window Inflation & Economic Efficiency:**
   Injecting multiple full episodic traces directly into the context window conflicts with the cost-tier boundaries defined in `CostTier` (CHEAP vs. EXPENSIVE). It violates the rule of maintaining a clean, compact prompt footprint on thin environments.
3. **Hexagonal Architecture Preservation:**
   MemoHarness tightly couples the controller to the execution environment. The AEAN architecture enforces a strict hexagonal structure where the domain model is entirely decoupled from external storage and adapters. Injecting raw physical trace structures directly into the runtime context violates this conformance boundary.

---

## Traceability Matrix: MemoHarness vs. AEAN Baseline

To enforce a strictly evidence-based comparison, we map the key contributions of the paper against the existing, frozen AEAN baseline:

| Paper Contribution | Already in AEAN | Better | Worse | Equivalent | Missing | Recommendation | Scientific Justification |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **6D Harness Space Decomposition** | **✓** (Partial) | | | **✓** | | **Keep Current** (AReaL) | AEAN's AReaL protocol and Cost-Tier gates already structure input, tools, decoding, workflow, and output validators. No reason to restrict to exactly 6 fixed dimensions. |
| **Episodic-Semantic Dual Bank** | **✓** | **✓** (AEAN is Better) | | | | **Keep Current** (5-Tier Memory) | Our 5-Tier Memory (T0-T4) is fully typed, maps onto the unified WorldGraph, and supports decay coefficients, offering superior retrieval depth. |
| **Distillation Operator ($\mathrm{Distill}$)** | **✓** | **✓** (AEAN is Better) | | | | **Keep Current** (CMOS Consolidation) | CMOS consolidation includes causal link assertion and Bayesian uncertainty adjustments, which are mathematically more robust than simple pattern lists. |
| **Top-K Lexical/Semantic Trace Retrieval** | | | | | **✓** | **Reject Direct Injection; Prototype as Router** | Directly injecting full raw failure traces degrades performance via mimicry. Prototyping as a routing parameter search is safe. |
| **Lexicographical Selection Rule** | **✓** | **✓** (AEAN is Better) | | | | **Keep Current** ($S(M)$ Suitability) | AEAN's continuous multi-objective score ($S(M)$) prevents performance cliffs better than discrete lexicographical splits. |
| **Test-time Adaptation without Labels** | **✓** (Partial) | | | **✓** | | **Prototype Experimentally** | Implement a lightweight adapter plugin that selects existing AReaL parameters based on neighborhood tasks. |

---

## Phase III — AQRI Hypothesis Generation

To maintain the absolute integrity of our frozen EIOS baseline, any proposed integration of MemoHarness concepts must be treated as a scientific hypothesis to be tested under strict AQRI evaluation protocols. No changes will be merged into the production baseline unless the null hypothesis ($H_0$) is statistically rejected with a confidence level of $\alpha = 0.05$.

### Hypothesis 1: Raw Failure-Trace Injection (The Mimicry Threat)
* **$H_0$ (Null Hypothesis):** Injecting raw, historical failure traces ($\mathcal{N}_K^-$) into the runtime context window produces no change or reduces the agent's task success rate compared to retrieving declarative avoidance rules.
* **$H_1$ (Alternative Hypothesis):** Injecting raw, historical failure traces ($\mathcal{N}_K^-$) statistically increases task recovery rates without causing behavioral mimicry.
* **Effect Size Threshold:** $\ge 5\%$ absolute increase in task success rate.
* **Validation Substrate:** `tests/evolution/test_self_harness.py` simulating multi-turn command-line failures.

### Hypothesis 2: 6D Discrete Space vs. AReaL Continuous Adaptation
* **$H_0$ (Null Hypothesis):** Restricting the harness optimization search space to the six functional dimensions of MemoHarness does not improve optimization convergence speed or task quality compared to the continuous AReaL control plane.
* **$H_1$ (Alternative Hypothesis):** The 6-Dimensional functional decomposition reduces the number of search rounds required to find an optimal system configuration by at least $20\%$ while maintaining equivalent accuracy.
* **Effect Size Threshold:** Cohen's $d \ge 0.5$ on convergence rate.

### Hypothesis 3: Lexicographical Sorting vs. Suitability Weighted Scoring $S(M)$
* **$H_0$ (Null Hypothesis):** MemoHarness's lexicographical selection rule (Equation 16) produces the same or higher inference costs (tokens/latency) for equivalent accuracy levels compared to AEAN's suitability score $S(M)$.
* **$H_1$ (Alternative Hypothesis):** Lexicographical selection produces a Pareto-optimal configuration that lowers average dollar-cost per task by at least $10\%$ with zero degradation in success rate.
* **Effect Size Threshold:** $\ge 10\%$ reduction in non-cached token usage.

---

## Phase IV — Final Scientific Recommendation

Based on the rigorous gap analysis and comparative evaluation, we present the following final recommendation to the AEAN Governance Board:

$$\text{Final Recommendation: } \mathbf{ADOPT\ WITH\ SIGNIFICANT\ MODIFICATIONS\ (EXPERIMENTAL\ ONLY)}$$

### Core Decisions
1. **REJECT: Core Memory Integration.** Do NOT integrate or adopt the MemoHarness "Experience Bank" structure. AEAN's **5-Tier Memory Architecture** and **CMOS system** are functionally superior, highly optimized, and structurally immune to the context leakage patterns of MemoHarness. Replacing or modifying our memory schemas would introduce severe regressions.
2. **REJECT: Raw Trace Prompt Injection.** Do NOT inject raw execution histories of past failed trials ($\mathcal{N}_K^-$) into the active prompt window. This is a scientific hazard that induces mimicry behavior in medium-sized models (such as the local Apodex-1.0-4B model). Instead, continue using CMOS's method of distilling failures into declarative rules and constraints.
3. **PROTOTYPE EXPERIMENTALLY: Test-Time Routing Adapter.** Adopt, solely as an experimental plug-in within our `SelfImprovementOrchestrator`, a **Case-Specific Adapter Module**. This module will perform lexical neighbor lookups on incoming task features ($\phi_j$) against historical metadata and dynamically downshift or adjust AReaL control parameters (e.g., maximum retries, routing structures, or context limits) based on similarity. This preserves the frozen baseline while exploring MemoHarness's case-adaptation gains.

---

## Phase V — Conditional Implementation & AQRI Benchmark Plan

Any implementation of the experimental Case-Specific Adapter is strictly conditional. It must be developed as an isolated plugin, evaluated against our frozen baseline, and demonstrate statistically significant improvements under the following AQRI Benchmark design before graduation to production.

### 1. Calibration Metrics
To ensure the adapter does not introduce overconfidence or unstable routing decisions, we measure:
* **Expected Calibration Error (ECE):**
  $$\mathrm{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{N} \left| \mathrm{acc}(B_m) - \mathrm{conf}(B_m) \right|$$
  Measures the mismatch between predicted probability of success and actual execution success.
* **Brier Score:**
  $$\mathrm{BS} = \frac{1}{N} \sum_{i=1}^{N} (f_i - o_i)^2$$
  Assesses the overall accuracy of the adapter's difficulty prediction.
* **Log Loss:** Penalizes highly confident incorrect routing decisions.

### 2. Reliability Metrics
* **Success Rate:** Total completed tasks divided by total attempts.
* **Recovery Rate:** Percentage of tasks that encounter an intermediate command failure but recover to a successful outcome.
* **Robustness Score:** Variance in success rate across task domains (Terminal-Bench, FinanceAgent, LiveCodeBench).

### 3. Efficiency Metrics
* **Token Overhead (Cached vs. Non-Cached):** Direct measurement of prefix cache hits and prompt window size.
* **Latency ($\ell$):** End-to-end task duration in milliseconds.
* **Compute Cost ($C$):** Actual API dollar cost based on model pricing models.

### 4. Adaptation Metrics
* **Novel Task Performance:** Execution accuracy on datasets completely held out from the search bank (e.g., SWE-Bench Pro).
* **Cross-Domain Generalization:** Success rate of the adapted harness under model swaps (e.g., transferring from GPT-5.3-Codex search to Claude-Sonnet-4.6 execution).

### 5. Statistical Verification Protocol
To prevent "p-hacking" and ensure scientific robustness, the benchmark execution will perform:
* **Bootstrapping:** Resample the 18-task evaluation split $B = 10,000$ times to estimate stable confidence intervals for all accuracy differences.
* **Bayesian Factor Analysis:** Compare the posterior distribution of success rates under the adapted configuration against the baseline, computing the Bayes Factor ($BF_{10}$) to verify that the evidence strongly favors the alternative hypothesis ($BF_{10} > 10$).
* **Power Analysis:** Ensure the sample run volume provides a statistical power of $1 - \beta \ge 0.80$ at a significance level of $\alpha = 0.05$.

---

## Draft Implementation Architecture (Isolated Adapter Plugin)

Should the experimental validation begin, the following isolated adapter components will be defined in a non-disruptive namespace (e.g., `apodex/evolution/self_harness/memoharness_plugin.py`), fully decoupled from the core control plane:

```python
"""
Experimental Case-Specific Adapter Plugin (MemoHarness-style).
Maintains strict decoupling from frozen AEAN memory, skill registries, and loops.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import numpy as np

class AdaptiveHarnessConfig(BaseModel):
    """Local, ephemeral parameters adapted for a single case run."""
    max_retries: int = 5
    retry_delay_seconds: float = 2.0
    enable_detailed_traces: bool = False
    context_pruning_limit: int = 120000
    downshift_gating: bool = True

class ExperimentalCaseAdapter:
    """
    Isolated MemoHarness adapter. Operates on top of the existing AReaL Control Plane
    by adjusting ephemeral execution parameters based on case similarity,
    entirely avoiding modifications to core structures.
    """
    def __init__(self, historical_metadata: List[Dict[str, Any]]):
        self.history = historical_metadata

    def calculate_similarity(self, current_features: Dict[str, Any], historical_case: Dict[str, Any]) -> float:
        """Lexical similarity score over task domain, instruction tags, and length."""
        domain_match = 1.0 if current_features.get("domain") == historical_case.get("domain") else 0.0
        instruction_len_diff = abs(len(current_features.get("instruction", "")) - len(historical_case.get("instruction", "")))
        len_penalty = np.exp(-instruction_len_diff / 100.0)
        return 0.7 * domain_match + 0.3 * len_penalty

    def adapt_configuration(self, task_input: Dict[str, Any], global_defaults: Dict[str, Any]) -> AdaptiveHarnessConfig:
        """
        Retrieves the top historical cases to adapt control settings.
        Follows a strict safety policy: defaults to global baseline if history is sparse.
        """
        similarities = [
            (self.calculate_similarity(task_input, h), h)
            for h in self.history
        ]
        # Sort by similarity descending
        similarities.sort(key=lambda x: x[0], reverse=True)

        # Filter neighborhoods
        top_matches = [item for sim, item in similarities[:3] if sim > 0.6]

        if not top_matches:
            # Revert instantly to frozen baseline defaults (Safe-fallback)
            return AdaptiveHarnessConfig()

        # Inspect past failures in neighborhood to adjust safety limits
        failures_in_neighborhood = sum(1 for item in top_matches if not item.get("success", True))

        adapted = AdaptiveHarnessConfig(
            max_retries=7 if failures_in_neighborhood > 1 else 5,
            retry_delay_seconds=4.0 if failures_in_neighborhood > 1 else 2.0,
            enable_detailed_traces=failures_in_neighborhood > 0,
            context_pruning_limit=150000 if failures_in_neighborhood > 0 else 120000,
            downshift_gating=failures_in_neighborhood == 0
        )
        return adapted
```

This ensures that the core `trajectory_areal.py` and `EvolutionControlPlane` are never altered directly, preserving the frozen baseline while allowing isolated AQRI verification.

---

## Conclusion
The *MemoHarness* paper represents an interesting step forward in prompt-free adaptation, but its claims of superiority must be heavily qualified. In an enterprise system like AEAN governed by EIOS, we already possess a superior 5-tier memory abstraction and the multi-objective suitability metric $S(M)$. Directly adopting the paper's prompt-injection techniques would introduce serious mimicry and window-inflation regressions.

By defining clear AQRI hypotheses and keeping any implementation restricted to an isolated routing adapter plugin, we respect our frozen baseline while ensuring that any future integration is driven strictly by objective, reproducible, and statistically significant empirical evidence.
