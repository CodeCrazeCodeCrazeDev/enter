# CAPABILITY OWNERSHIP MATRIX
## Single-Layer Ownership Mapping & Zero Duplication Guarantee

---

### Functional Responsibility Taxonomy

To prevent architectural overlap and capability duplication across Research OS, EIOS, EOS, AEAN, and APODEX, every core cognitive capability is assigned strictly to a **single owning layer**.

```
+-----------------------------------+---------------------------------------+---------------------+
| Capability Category               | Single Owning Layer                   | Primary Subsystem   |
+-----------------------------------+---------------------------------------+---------------------+
| Scientific Inquiry & Literature   | Layer 1: Research OS                  | Research OS         |
| Hypothesis & Statistical Tests    | Layer 1: Research OS                  | Research OS         |
| Opportunity Priority Scoring      | Layer 1: Research OS                  | Research OS         |
| Continuous Anomaly Sensing        | Layer 2: EIOS / EOS                   | EOS Engine          |
| Asynchronous Task DAG Compiler   | Layer 2: EIOS / EOS                   | EIOS Kernel         |
| Enterprise State Machine (11 Stg) | Layer 2: EIOS / EOS                   | EOS First-Princ.    |
| Capital Allocation & GTM Loops    | Layer 2: EIOS / EOS                   | EOS Engine          |
| Multi-Agent Bidding & Token Reg.  | Layer 3: AEAN                         | HiveMind            |
| EFE Learnable Routing Dispatcher | Layer 3: AEAN                         | Routing Gate        |
| Self-Referential Code AST Rewrites| Layer 3: AEAN                         | CodeRewriteEngine   |
| Island MAP-Elites Workflow Optim. | Layer 3: AEAN                         | GeneticOptimizer    |
| DPO Trajectory Preference Collect | Layer 3: AEAN                         | SFTCollector        |
| Causal DAG Graph & Relations      | Layer 4: APODEX                       | WorldModel          |
| Recursive Bayesian Belief Engine  | Layer 4: APODEX                       | Belief Engine       |
| Credit Halting & Rate Governance  | Layer 4: APODEX                       | Governance Engine   |
| Active Inference State Platform   | Layer 4: APODEX                       | Cognitive Platform  |
+-----------------------------------+---------------------------------------+---------------------+
```

---

### Detailed Capability Mapping & Interfaces

#### Layer 1: Research OS (Research Layer)
1. **Scientific Literature Ingestion**: Synthesis of research publications across academic domains (`ResearchOS.conduct_literature_review`).
2. **Hypothesis Formulation & Validation**: Registration of null hypotheses, sandbox walk-forward simulation, Deflated Sharpe Ratio (DSR), and White's Reality Check (`ResearchOS.register_hypothesis`, `ResearchOS.execute_experiment_simulation`).
3. **Discovery Opportunity Scoring**: Blended score calculation combining commercial value, expected information gain, and option value (`ResearchOS.score_opportunity`).

#### Layer 2: EIOS / EOS (Execution & Orchestration Layer)
4. **Continuous Anomaly Sensing**: Real-time market/system anomaly monitoring (`EOSEngine.run_continuous_sensing_cycle`).
5. **Asynchronous DAG Compilation**: Task dependency resolution and workflow DAG execution (`EIOSKernel.execute_dag`).
6. **Enterprise Growth State Machine**: 11-stage founder lifecycle simulation (`EOSEngineFirstPrinciples`).
7. **Capital & GTM Lifecycle Management**: Financial runway modeling, unit economics, and customer retention loops.

#### Layer 3: AEAN (Cognitive Intelligence Layer)
8. **HiveMind Multi-Agent Coordination**: Token-budgeted task bidding registry (`HiveMind.arbitrate`, `HiveMind.register_research_insight`).
9. **Learnable Routing Dispatcher**: EFE-driven task delegation to domain specialist agents (`LearnableRoutingGateDispatcher.route_task`).
10. **Self-Referential AST Code Rewriting**: Safe runtime code mutation and static security parsing (`CodeRewriteEngine.propose_rewrite`, `verify_proposal_ast`).
11. **Island MAP-Elites Genetic Synthesis**: Prompt template and workflow parameter evolution (`GeneticWorkflowOptimizer`).
12. **DPO Preference Trajectory Collection**: On-policy advantage estimation and dataset compilation (`SFTPreferenceCollector.compile_dpo_preference_pair`).

#### Layer 4: APODEX (Decision & Execution Platform Layer)
13. **Causal DAG World Model**: Directed entity-relationship graph ($G=(V,E)$) for counterfactual reasoning (`WorldModel.add_node`, `add_relation`).
14. **Recursive Bayesian Belief Engine**: Conjugate updating of system beliefs and hypothesis probabilities (`WorldModel.update_belief`).
15. **Credit Halting & Safety Governance**: Real-time rate limiting, financial credit caps, and compliance veto enforcement.
16. **Active Inference Decision Platform**: Central substrate orchestrating active inference state handoffs.

---

### Verification of Zero Duplication

All 16 capabilities have a single canonical owner and API entry point. No subsystem re-implements planning, memory, or multi-agent bidding outside its designated owning layer.
