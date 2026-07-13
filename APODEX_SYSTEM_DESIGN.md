# Apodex Meta-System Architectural Specification: Self-Improving AI System

This document specifies the architecture, data flows, design patterns, safety guardrails, and implementation roadmap for **Apodex**—the overarching meta-system that wraps, observes, and continually improves the Autonomous Economic Agent Network (AEAN).

---

## 1. Unified Architecture & High-Level Goal

Apodex introduces a **dual-loop self-improvement cognitive architecture** on top of the AEAN execution framework. The high-level goal of Apodex is to continuously drive both short-term (in-session/cross-session) and long-term (structural and algorithmic) adaptation:

```
                                +---------------------------+
                                |        Human User         |
                                +-------------+-------------+
                                              ^
                                              | (Task Requests & Feedback)
                                              v
+---------------------------------------------+---------------------------------------------+
|                                     AEAN TASK RUNTIME                                     |
|                                                                                           |
|          +-------------------+       (Executes)        +-------------------+              |
|          |    Task Agents    |  -------------------->  |       Tools       |              |
|          +---------+---------+                         +---------+---------+              |
+--------------------|---------------------------------------------|------------------------+
                     | (Traces, Errors, Metrics)                   | (Logs, Outcomes)
                     v                                             v
+-------------------------------------------------------------------------------------------+
|                                    APODEX META-SYSTEM                                     |
|                                                                                           |
|   +-----------------------------------------------------------------------------------+   |
|   |                         Experience Database + Cognition Base                      |   |
|   |  - Trace Logs  - Failure Signatures  - Performance Metrics  - Distilled Lessons   |   |
|   +----------+----------------------------------------------------+-------------------+   |
|              | (Weakness Indicators)                              | (Performance Gaps)    |
|              v                                                    v                       |
|   +------------------------------------+       Triggers       +-----------------------+   |
|   |      Harness Loop Controller       |  ----------------->  | Research Controller   |   |
|   |  (System Prompts, Routing, Tools)  |                      | (Weights & Algos)     |   |
|   +------------------+-----------------+                      +-----------+-----------+   |
|                      |                                                    |               |
|                      | (Proposes Diffs)                                   | (Proposes SFT/|
|                      v                                                    |  RL / Weights)|
|   +------------------+-----------------+                                  v               |
|   |      Safety & Guardrail Manager    |                      +-----------+-----------+   |
|   |  - Diff Verification               |                      | Experiment Sandbox    |   |
|   |  - Regression Evaluation Gate      |                      | - Docker Execution    |   |
|   +------------------+-----------------+                      | - Strict Quotas       |   |
|                      |                                        +-----------+-----------+   |
|                      | (Deploys Verified)                                 |               |
|                      |                                                    | (Creates PR)  |
|                      v                                                    v               |
|            [Staging / Production]                              [Git-Based Pull Request]   |
|                                                                - Human-in-the-Loop Gate   |
+-------------------------------------------------------------------------------------------+
```

---

## 2. Core Components

### 2.1 Core Task Models / Agents
The primary task execution layer is governed by AEAN's multi-agent system, composed of specialized roles (such as `CoordinatorAgent` and `WorkerAgent`). They perform standard ReAct loop turns, leverage registered toolsets, and generate execution traces.

### 2.2 Harness Loop Controller (Short-Term adaptation)
- **Role**: Operates on a short timescale (seconds to hours). It detects inefficiencies, error rates, and user corrections from recent sessions and proposes low-risk, reversible, diff-style changes to agent scaffolding (system prompts, tool descriptions, and routing parameters).
- **Core Mechanism**: Weakness mining, local candidate proposal, fast validation against a mini-benchmark, and hot-swapping agent parameters.

### 2.3 Research Loop Controller (Long-Term evolution)
- **Role**: Operates on a long timescale (hours to weeks). It analyzes historical performance data, identifies systemic gaps, designs model-weight adaptations (SFT fine-tuning datasets, DPO / RL post-training algorithms), and runs resource-bounded training/eval experiments.
- **Core Mechanism**: Automatic recipe compilation, sandbox trial execution, regression checking, and pull-request generation.

### 2.4 Experience Database + Cognition Base
- **Role**: The unified knowledge base of "lessons learned" across both loops.
- **Data Layers**:
  - **Trace Database**: Low-level JSON traces of all task executions.
  - **Failure Signature Store**: Clusterings of common error messages and tool failure modes.
  - **Recipe Store**: Historical configurations of the agent harnesses (system prompts, weights) mapped to success scores.
  - **Distilled Lessons Base**: High-level semantic "dos and don'ts" generated by LLM evaluators to prevent repeating past failures.

### 2.5 Safety and Guardrail Manager
- **Role**: Enforces critical constraints and no-edit zones, ensuring neither loop degrades system behavior or violates safety directives.
- **Core Mechanism**: Syntactic diff checks, static schema verification, local regression suites, and enforcement of immutable configuration attributes.

---

## 3. System Data Flows

### 3.1 User ↔ Task Agent ↔ Tools
1. **User** submits a task request (e.g., "Implement a binary search tree in Python") to the `CoordinatorAgent`.
2. `CoordinatorAgent` generates a roadmap and delegates segments to a `WorkerAgent`.
3. `WorkerAgent` executes registered `Tools` (e.g., code interpreter, compiler, search).
4. **Tools** return execution outcomes (success/error/stdout) back to the `WorkerAgent`.
5. Upon completion, the final result is delivered to the **User**.

### 3.2 Task Agent ↔ Harness Controller
1. The **Task Agent** publishes its complete execution trace (actions, observations, prompt structures) and final performance metrics to the **Experience Database**.
2. **Harness Controller** scans the database, mining for weaknesses (e.g., tool-call syntax errors, looping thinking tags).
3. If a weakness is found, the **Harness Controller** proposes a target scaffolding modification.
4. The proposed change is sent to the **Safety and Guardrail Manager** for rapid validation.
5. Once validated, the new configuration is pushed to the **Task Agent's** active config.

### 3.3 Harness Controller ↔ Research Controller
1. When the **Harness Controller** exhausts prompt/routing-level solutions for a recurring failure mode (e.g., the model repeatedly fails to resolve complex mathematical formulas despite prompt updates), it logs a "Cognitive Bottleneck" event in the **Experience Database**.
2. **Research Controller** listens to these events and decides to trigger a structural adaptation (e.g., compiling a supervised fine-tuning dataset to teach the model a new domain skill).

### 3.4 Research Controller ↔ Training/Eval Infrastructure
1. **Research Controller** extracts successful trace datasets from the **Experience Database** and compiles a training recipe.
2. It launches an isolated, resource-bounded **Experiment Sandbox** (Docker).
3. The sandbox executes model fine-tuning or RL optimization.
4. The newly generated model is evaluated against a comprehensive evaluation suite.
5. If the new model outperforms the current baseline without introducing regressions, a **Git Pull Request** containing the new model weight references and training metrics is automatically submitted for human review.

---

## 4. Reference Projects Mapping (Design Library)

Apodex borrows specific design patterns from the 60 reference projects, plugging them into corresponding subsystems:

### 4.1 Group 1: AI-for-AI Research Systems (ASI-Evolve-like)
*Applied to the **Research Loop Controller** and sandbox trial mechanisms:*
- **ASI-Evolve & AutoResearch**: Implements the closed-loop cycle of script editing, sandbox running, and performance-based model promotion.
- **The AI Scientist & AI Scientist-v2**: Inspires the automated research proposal step and literature/belief search within our `ScientificHypothesisEngine`.
- **SEAL**: Directs the automated generation of targeted self-edits and fine-tuning datasets from execution failures.
- **Darwin Gödel Machine & Agent0**: Pattern of recursive self-modification where controllers can modify their own utility functions and sub-component routines.
- **STOP & MLR-Copilot**: Inspires the use of metaprompting pipelines to design, write, and refine ML training/evaluation configurations.

### 4.2 Group 2: Self-Improving Harness / Agent-Scaffolding (Continual Harness-like)
*Applied to the **Harness Loop Controller** and in-session/cross-session adaptation:*
- **Continual Harness**: Reset-free online adaptation of the runtime environment (hot-swapping system configs without restarting the session).
- **Self-Harness & Meta-Harness**: Dual-agent pattern where a meta-agent acts as an auditor mining task-agent failures and proposing micro-harness fixes.
- **Reflexion & Self-Refine**: Natural language self-correction loops. We incorporate `SelfReflectionService` to audit execution steps post-run and compile structured "lessons learned".
- **ADAS & AFlow**: Pattern of adaptive acquisition and packaging of successful task sequences into structured, reusable tool schemas (implemented via AEAN's `Tool Invention` service).

### 4.3 Group 3: Prompt / Policy Optimization & Evolution
*Applied to prompt evolution and TextGrad-style optimization:*
- **Promptbreeder & EvoPrompt**: Implements genetic algorithms to cross-breed and mutate system prompts based on task performance metrics.
- **TextGrad**: Directs the use of natural language "gradients" (text critique of failed traces) backpropagated to refine specific lines of instruction prompts.
- **PromptAgent**: Employs Monte Carlo Tree Search (MCTS) over prompt modifications to find strategic system prompt structures.
- **LLMs as Optimizers (OPRO)**: Formulates the optimization problem as a text prompt where the meta-agent receives a history of past prompts and scores to generate superior candidates.

### 4.4 Group 4: RL / Self-Play / Test-Time Self-Improvement
*Applied to active learning and post-training feedback loop:*
- **Self-Rewarding Language Models**: Equips the evaluation pipeline with an autonomous reward-modeling schema to automatically label generated datasets.
- **Agent Q & Absolute Zero**: Guides the incorporation of MCTS search and self-play exploration within simulated market environments.
- **R-Zero**: Establishes self-play environments to iteratively improve reasoning capabilities on top of baseline models without human labels.

---

## 5. Concrete Definition of the Dual Loops

### 5.1 Long-Term Research Loop (ASI-Evolve‑style)
Designed to run asynchronously with strict resource boundaries:

```
[Trigger / Schedule] ──> [Propose Changes] ──> [Sandbox Experiment] ──> [Benchmark Eval] ──> [Git PR / Human Gate]
```

1. **Input**: Trace logs, accumulated failure signatures, planning errors, and current training configurations.
2. **Propose Candidate Changes**: The `ResearchLoopController` evaluates performance gaps. It proposes structural adaptations:
   - Hyperparameter shifts (e.g., adjusting temperature curves or learning rates).
   - Fine-Tuning SFT datasets compiled from high-reward traces.
   - RL/DPO training recipes to suppress frequent logical hallucinations.
3. **Run Bounded Experiments**: Spins up an isolated Docker container with locked GPU/CPU quotas and blocked internet access. The container runs the training/fine-tuning script.
4. **Evaluate Results**: The new model artifact is subjected to a deep evaluation benchmark suite (e.g., tests for code generation, mathematical reasoning, safety alignment, and regression detection).
5. **Store Trial Details**: Trial parameters, logs, evaluation charts, and a natural language analysis ("lesson learned" during the trial) are persisted to the **Experience Database**.
6. **Promotion**: If the new model meets the promotion criteria (non-regression, +5% metric increase), the system auto-generates a Pull Request containing the config changes and model references.

### 5.2 Short-Term Harness Loop (Continual Harness‑style)
Designed to run online during active sessions:

```
[Live Session Logs] ──> [Weakness Mining] ──> [Harness Proposal] ──> [Fast Validation] ──> [Hot Deploy & Log]
```

1. **Input**: Live trace events, error outputs, tool timeouts, and direct user corrections.
2. **Weakness Mining**: Cluster and match raw errors against failure templates (e.g., "JSON parsing failed on tool execution", "Model hallucinated a tool name").
3. **Harness Proposal**: A prompt optimization agent (using EvoPrompt and TextGrad principles) proposes targeted edits to the agent's system prompt or tool descriptions.
4. **Rapid Validation**: Runs a fast regression suite (e.g., 10-20 cached hard tasks) to confirm the new prompt fixes the current error without breaking general capabilities.
5. **Deploy & Log**:
   - Updates the agent's in-memory scaffolding configuration (Hot Swap).
   - Saves both the successful edit and failed trial attempts in the **Experience Database**.

---

## 6. Safety, Control, and Cost Management

### 6.1 Immutable Guardrails (No-Edit Zones)
Certain files and prompt definitions are declared **immutable**:
- Core system safety constraints (e.g., ethical guidelines, data privacy controls).
- The schemas and signatures of critical core tools.
- Verification tests in the regression suite.
*The Safety and Guardrail Manager blocks any harness edit or research proposal that attempts to alter these defined zones.*

### 6.2 Small, Reversible, Diff-Style Changes
- All harness edits are proposed as Git-like patch diffs.
- The `HarnessLoopController` retains a configuration stack. If any runtime error or degradation is observed post-deployment, the system instantly triggers an automated rollback to the last known stable state.

### 6.3 Regression Testing Blocking Rules
Before any prompt or model is promoted:
- It must pass $100\%$ of the designated **Regression Suite**. Any failure in a legacy capability blocks the proposal immediately.
- The evaluation must maintain or improve the baseline performance score.

### 6.4 Compute Budgets and Quotas
To prevent runaway loops and runaway cloud costs:
- **Daily Financial Quotas**: Maximum API token spend limits enforced per agent loop session.
- **Research Loop CPU/GPU Quota**: Hard timeouts (e.g., maximum 2 hours wall-clock time per SFT fine-tuning run) and a cap on concurrent sandbox containers.

### 6.5 Human Approval Protocol
Apodex enforces a clear hierarchy of promotion:
1. **Low-Risk Changes** (e.g., minor prompt wording optimizations): Automatically validated and hot-swapped into the `Staging` configuration layer.
2. **High-Risk Changes** (e.g., model weight replacement, structural routing edits):
   - The system generates a Git Pull Request containing the full evaluation report.
   - An asynchronous webhook triggers a Slack/Discord notification with a summary of the change.
   - A human engineer must review and merge the PR to promote the changes to the `Production` branch.

---

## 7. Phased Implementation Roadmap

Apodex's meta-system is scheduled for implementation over four distinct, low-risk, and backward-compatible phases:

```
  Phase 1: Instrumentation & Logging MVP
  └── Phase 2: Continual Harness Adaptation
      └── Phase 3: AutoResearch Loop MVP
          └── Phase 4: Integrated Dual-Loop Core & Safety Monitoring
```

### Phase 1: Logging + Basic Harness-Loop MVP
- **Objective**: Establish the telemetry layer and initial prompt optimization loop.
- **Deliverables**:
  - Instrumentation hooks in AEAN ReAct loops to output standard JSON trace payloads.
  - Basic `ExperienceDatabase` storing traces.
  - A simple weakness miner that detects tool invocation syntax errors.

### Phase 2: Full Continual Harness-style Adaptation
- **Objective**: Implement online, reset-free harness hot-swapping and TextGrad/EvoPrompt routines.
- **Deliverables**:
  - Full `HarnessLoopController` capable of mutative prompt editing.
  - Local fast validation suite to screen proposed prompt edits.
  - Automated configuration rollbacks upon performance degradation.

### Phase 3: AutoResearch-style Research Loop MVP
- **Objective**: Launch the long-term weights/algorithms adaptation pipeline.
- **Deliverables**:
  - `ResearchLoopController` proposing SFT datasets from high-reward trace logs.
  - Isolated Docker experiment sandbox runner with locked resource limits.
  - Automatic evaluation pipeline testing fine-tuned candidate models against standard datasets.

### Phase 4: Integrated Two-Loop System with Safety & Monitoring
- **Objective**: Fully link the loops, implement the overarching `SafetyGuardrailManager`, and deploy human-in-the-loop PR generation.
- **Deliverables**:
  - Unified `ExperienceDatabase` serving both loops.
  - Automatic escalation of unresolved harness issues to the research loop.
  - Git PR generator and webhook notifications for promotion gates.
  - Rigorous budget limits and immutable zone guards.

---

## 8. Concrete Worked Examples

### 8.1 Harness Edit Diff Example (Coding Assistant Prompt Optimization)
*Domain: Python Coding Assistant tool utilization instruction.*

#### Before: Initial Prompt Config
```json
{
  "system_prompt": "You are a coding assistant. Use the `python_compiler` tool to compile your code. Format your tool call in JSON.",
  "tools": {
    "python_compiler": {
      "description": "Compiles and executes Python code. Input must be raw code.",
      "parameters": {
        "code": "string"
      }
    }
  }
}
```

#### Weakness Detected (Experience Database Log)
- **Signature**: `ToolCallParserException: Received invalid markdown code blocks instead of pure JSON parameter.`
- **Trace Analysis**: The model wrote `{"code": "```python\nprint('hello')\n```"}` which failed the strict JSON schema validation.

#### Proposed Harness Edit Diff (After Prompt Optimization)
```diff
<<<<<<< BEFORE
You are a coding assistant. Use the `python_compiler` tool to compile your code. Format your tool call in JSON.
=======
You are a coding assistant. Use the `python_compiler` tool to compile your code.
Format your tool call in pure JSON.

CRITICAL: Do NOT wrap the value of the "code" parameter in markdown code blocks (e.g., do not use triple backticks ```python ... ``` inside the JSON string). Write raw python code directly as a standard JSON string.
>>>>>>> AFTER
```

#### Validation Result
- **Fast Eval Score**: $100\%$ on 15 cached Python coding tasks (no syntax errors).
- **Outcome**: Swapped into Staging.

---

### 8.2 Research Trial Example (Reasoning-Finetuned Model Promotion)
*Domain: Mathematical reasoning optimization on competitive math benchmark tasks.*

#### 1. Change Proposal
- **ID**: `trial_089`
- **Hypothesis**: "Fine-tuning the base LLM on 5,000 high-quality, step-by-step thinking traces collected from successful complex multi-turn math episodes will reduce mathematical reasoning errors and step-skipping."
- **Recipe**: LoRA fine-tuning (rank 16, alpha 32) on `base-model-v2` using the curated dataset.

#### 2. Experiment Setup
- **Compute Budget**: Max 2 hours on a single isolated H100 GPU container. No external network access allowed.
- **Training Job Command**:
  ```bash
  python -m apodex.train.finetune_lora \
    --base_model "models/base-model-v2" \
    --train_data "data/curated_traces_math.jsonl" \
    --epochs 3 \
    --lr 2e-4 \
    --output_dir "sandbox/output/trial_089"
  ```

#### 3. Evaluation & Decision
- **Evaluation Results**:
  | Metric | Baseline Model | Trial 089 Candidate Model | Status |
  | :--- | :--- | :--- | :--- |
  | **MATH Benchmark (Acc)** | 62.4% | 68.8% | **Pass (+6.4%)** |
  | **GSM8K (Acc)** | 81.2% | 83.1% | **Pass (+1.9%)** |
  | **Regression (General Coding)**| 74.5% | 74.4% | **Pass (Within 0.5% margin)**|
  | **Safety / Alignment Score** | 99.1% | 99.2% | **Pass** |

- **Decision**: Candidate model passes all criteria. Generate automated Git PR to merge model weights configuration.

#### 4. Stored "Lesson Learned" in Experience Database
```json
{
  "trial_id": "trial_089",
  "status": "successful_candidate_promoted",
  "proposed_change": "LoRA fine-tuning on math-specific multi-turn reasoning traces",
  "metrics": {
    "math_improvement_pct": 6.4,
    "regression_detected": false
  },
  "distilled_lesson": "Training on complete thinking trajectories (specifically retaining the <think> ... </think> formatting from successful episodes) significantly increases logical consistency on complex, multi-step math problems without degrading baseline coding capabilities. Fine-tuning learning rates should remain below 3e-4 to prevent representation drift."
}
```
