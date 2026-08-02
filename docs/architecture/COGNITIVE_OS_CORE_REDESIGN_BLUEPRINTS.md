# Cognitive OS Phase 3 — Core Cognitive Redesign & Architectural Blueprints

This document details the first-principles designs, algorithmic flowcharts, and concrete code blueprints for every core cognitive capability inside the Cognitive Operating System.

---

## 1. Planning Subsystem — Hierarchical Long-Horizon MCTS-HTN

### Design Principle
The planner combines **Hierarchical Task Networks (HTN)** for structured decomposition and **Monte Carlo Tree Search (MCTS)** for exploration under uncertainty.

```
                  +--------------------------------+
                  |     Goal: "Launch Venture"     |
                  +---------------+----------------+
                                  |
                                  v  [HTN Decomposition]
         +────────────────────────┴────────────────────────+
         ▼                                                 ▼
+-----------------+                               +-----------------+
|  "Research Market"|                             |   "Deploy Code" |
+--------+--------+                               +--------+--------+
         |                                                 |
         v  [UCT Scoring over branches]                    v  [Prune paths]
      Primitive Steps                                   Primitive Steps
```

### Mathematical Engine
The node selection employs the Upper Confidence Bound for Trees (UCT) metric:
$$UCT_i = \frac{W_i}{N_i} + C \sqrt{\frac{\ln N_p}{N_i}}$$
where:
* $W_i$ is the accumulated reward value of node $i$.
* $N_i$ is the visit count of node $i$.
* $N_p$ is the visit count of parent node $p$.

---

## 2. World Model Subsystem — Causal Structural Modeling

### Design Principle
The world model represents state using a dynamic, multi-graph architecture containing Entities, Facts, Causal variables, Temporal series, and Bayesian Uncertainty (E-K-C-T-U).

### Causal Interventions ($do$-calculus)
```
          (Z) Confounding Parent (e.g. Market Condition)
         /   \
        v     v
   Action(X) ──> Outcome(Y)

   Intervention: do(X = x) cuts the link Z -> X.
```

The probability distribution under intervention is calculated via the Backdoor Adjustment formula:
$$P(Y = y \mid do(X = x)) = \sum_z P(Y = y \mid X = x, Z = z) P(Z = z)$$

---

## 3. Memory Subsystem — CMOS SQLite & Decay-Compensated Recall

### Design Principle
Transactional sqlite durability prevents semantic decay and context bloating.

### Mathematical Ebbinghaus Retention
The retention probability $R(t)$ drops exponentially over time:
$$R(t) = \exp\left(-\frac{t}{S}\right)$$
Upon active recall matching, stability is reinforced:
$$S_{\text{reinforced}} = S_{\text{old}} \cdot \left(1 + \alpha \cdot (1 - R(t))\right)$$

---

## 4. Multi-Agent Subsystem — ConsensAgent & Disagreement Escalation

### Design Principle
Spawning agents dynamically on-demand and monitoring their consensus via Shannon entropy measures.

### Mathematical Dispute Disagreement Entropy
Let $p_{ij}$ represent normalized similarity weights between agent decisions. The dispute entropy $H$ is computed as:
$$H = -\sum_{i} \sum_{j \neq i} p_{ij} \log_2 p_{ij}$$

If $H > T_{\text{escalate}}$, the debate is immediately halted and escalated to human arbitration.

---

## 5. Research OS Subsystem — Automated Scientific Loops

### Design Principle
Operating like an autonomous, isolated lab executing: Literature Search $\to$ Hypothesis Discovery $\to$ Sandbox Experimentation $\to$ Exact $p$-value estimation.

### Exact Standard Normal Validation
To prevent division-by-zero or approximation drift, we calculate $p$-values using the exact Standard Normal Cumulative Distribution Function (CDF):
$$p = 2 \cdot \left(1 - \Phi\left(\left|\frac{\bar{x} - \mu_0}{s / \sqrt{n}}\right|\right)\right)$$

---

## 6. Self-Improvement Subsystem — Multi-Objective Suitability Gates

### Design Principle
The system must never modify active system rules or model parameters unless verified by a non-bypassable, multi-objective evaluation gateway.

### Mathematical Suitability Metric
$$S(M) = w_q Q(M) - w_t T(M) - w_l L(M) + w_s S_r(M)$$
where:
* $Q(M)$ is suite quality.
* $T(M)$ is relative token consumption.
* $L(M)$ is millisecond latency.
* $S_r(M)$ is safety rating.
* If $S(M) < 1.05 \cdot S(\text{baseline})$, the candidate modification is blacklisted and the system executes a safe transaction rollback.
