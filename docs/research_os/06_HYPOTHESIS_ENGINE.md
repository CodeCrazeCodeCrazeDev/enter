# 06. Hypothesis Engine: Generative and Structured Inquiry

In classical quantitative finance, hypotheses are often formulated ad-hoc by human intuition. In a world-class AI-assisted Quantitative Research Organization, we utilize a **Hypothesis Engine** that systematically generates, taxonomizes, and refines research propositions.

However, to prevent this engine from becoming a random search ("data mining") utility, it must operate within a strict, structured scientific framework.

---

## 1. Structured Hypothesis Taxonomy

Every hypothesis ($H_1$) registered in the system must map to a standardized, machine-readable schema. This ensures that the Hypothesis Engine is not just testing random formulas but is contributing to a structured body of knowledge.

### Taxonomy Attributes
1. **Economic Rationales:** Every hypothesis must declare its underlying economic driver:
   * `BEHAVIORAL_BIAS`: Exploiting human cognitive errors (e.g., loss aversion, disposition effect).
   * `MARKET_MICROSTRUCTURE`: Exploiting exchange mechanics, order flow imbalances, or liquidity constraints.
   * `MACRO_REGIME`: Exploiting interest rate shifts, economic cycles, or systemic policy changes.
   * `CROSS_ASSET_FLOW`: Exploiting hedging behaviors, index rebalancing, or capital flows.
2. **Predictive Target:** The specific mathematical variable the signal claims to predict (e.g., $5\text{-minute forward midprice return}$, $1\text{-day realized volatility}$).
3. **Null Hypothesis ($H_0$):** Explicitly stated criteria under which the hypothesis is considered disproven (e.g., "The mean return of the signal is statistically indistinguishable from zero after adjusting for transaction costs").

---

## 2. Generative Hypothesis Loop

The Hypothesis Engine runs as a continuous background cycle, structured as follows:

```
+-----------------------------------------------------------+
| 1. Knowledge Graph Scan                                   |
| - Identify low-confidence regions in the World Model      |
| - Identify highly profitable market segments              |
+---------------------------+-------------------------------+
                            |
                            v
+---------------------------+-------------------------------+
| 2. Scientific Synthesis                                   |
| - Ingest academic literature and market observations      |
| - Propose causal connections (e.g., A causes B)           |
+---------------------------+-------------------------------+
                            |
                            v
+---------------------------+-------------------------------+
| 3. Hypothesis Formulation                                 |
| - Generate machine-readable Hypothesis JSON               |
| - Declare Null Hypothesis and Expected Effect Size        |
+---------------------------+-------------------------------+
                            |
                            v
+---------------------------+-------------------------------+
| 4. Pre-Registration Gate                                  |
| - Validate structure and prevent duplicates               |
| - Save to immutable Hypothesis Registry                   |
+-----------------------------------------------------------+
```

---

## 3. Pre-Registration and Duplication Checks

Before a hypothesis is accepted into the registry:
* **Semantic Deduplication:** The engine runs semantic searches against the existing registry to ensure that a similar hypothesis (e.g., "moving average crossover on BTC") hasn't already been thoroughly explored or rejected.
* **Complexity Budget Audit:** Prevents the generation of overly complex, multi-parameter hypotheses that are structurally prone to overfitting. It enforces Occam's Razor: a simpler formulation with fewer parameters is always preferred.

Once pre-registered, the hypothesis is locked. Only after this point can researchers or AI agents construct experiments to test it. This strict sequence completely eliminates "HARKing" (Hypothesizing After the Results are Known).
