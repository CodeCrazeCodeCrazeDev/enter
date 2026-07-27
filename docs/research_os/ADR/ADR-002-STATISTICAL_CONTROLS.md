# ADR-002: Mandatory Multiple Hypothesis testing and DSR Controls

## Status
Approved

## Context
A major failure mode of traditional quantitative backtesting is the "file drawer problem" and "backtest overfitting." When a researcher (human or AI) executes multiple backtests, they generate a high volume of trials. The best-performing backtest is usually selected for promotion. However, if 100 random variations are tested, the best-performing one is highly likely to be a statistical fluke rather than a genuine economic anomaly.

Without adjusting for the number of trials ($N$) and the variance of those trials, the promoted strategies are highly likely to suffer severe performance degradation (or complete collapse) in live trading.

## Decision
We decide to make **Multiple Hypothesis Testing Adjustments** and **Deflated Sharpe Ratio (DSR)** mandatory statistical gates inside the Research OS:

1. **Multiple Testing Adjustments:** Every feature search or parameter optimization process must execute a multiple hypothesis correction. The system implements:
   * **Bonferroni Adjustment:** Used for highly conservative significance checking.
   * **Holm-Bonferroni Method:** Used for general sequential parameter sweeps.
   * **Benjamini-Hochberg FDR:** Used for large-scale feature mining.
2. **Deflated Sharpe Ratio (DSR):** Every experiment's final Sharpe Ratio must be deflated using Marcos López de Prado's DSR formulation. The DSR calculation must take as input:
   * The estimated Sharpe Ratio ($\widehat{\text{SR}}$).
   * The number of trials executed ($N$).
   * The variance of the Sharpe Ratios across all executed trials.
   * The skewness and kurtosis of the strategy returns.
3. **Threshold Gate:** No model can be promoted to the Model Registry unless its DSR satisfies:
   $$\text{DSR} \ge 0.95$$

## Consequences
* **Elimination of Overfitted Strategies:** Strategies that look profitable purely because of parameter search volume will be successfully filtered out.
* **Capital Protection:** Prevents the allocation of real-world capital to statistical noise.
* **Increased Research Transparency:** Forces researchers and agents to register the *exact number of trials* executed, eliminating the practice of hiding negative or failed runs.
* **Increased Computational Rigor:** Computing DSR and multiple testing corrections requires the system to maintain a complete history of all trial outcomes in the Experiment Registry, which enriches institutional memory.
