# 05. Statistical Validation: Rigorous Significance Controls

In quantitative finance, backtest overfitting is the most common cause of failure. If a researcher runs enough backtests with different parameters or random combinations, they *will* find a strategy with a high Sharpe Ratio by pure chance.

The **AlphaAlgo Statistical Validation Layer** implements mathematical and statistical controls to filter out random anomalies, ensuring that promoted strategies possess genuine predictive power.

---

## 1. Multiple Hypothesis Testing Corrections

When testing multiple signals or parameter configurations, we must adjust our statistical significance thresholds. If we perform $N$ independent tests, the probability of obtaining at least one false positive (Type I error) at a significance level $\alpha = 0.05$ is:

$$P(\text{False Positive}) = 1 - (1 - \alpha)^N$$

If $N = 100$, this probability is $99.4\%$. To control the Family-Wise Error Rate (FWER) or False Discovery Rate (FDR), the Research OS implements:

### 1.1 Bonferroni Correction (Conservative)
Adjusts the target significance level to:

$$\alpha_{adj} = \frac{\alpha}{N}$$

A signal is only considered significant if its individual p-value satisfies $p \le \alpha_{adj}$.

### 1.2 Holm-Bonferroni Method (Step-down)
Less conservative than Bonferroni. Orders the p-values $p_1 \le p_2 \le \dots \le p_N$ and compares each $p_i$ to:

$$\alpha_{adj, i} = \frac{\alpha}{N - i + 1}$$

If the condition fails at step $k$, all subsequent hypotheses are rejected.

### 1.3 Benjamini-Hochberg (FDR Control)
Controls the proportion of false positives among the rejected hypotheses. Orders p-values and finds the largest index $k$ such that:

$$p_k \le \frac{k}{N} \cdot \alpha$$

Rejects all hypotheses $H_1, \dots, H_k$. This is ideal when exploring large pools of potential features.

---

## 2. Deflated Sharpe Ratio (DSR)

The **Deflated Sharpe Ratio (DSR)**, developed by Marcos López de Prado, adjusts the estimated Sharpe Ratio of a strategy to account for both backtest overfitting and the number of trials ($N$) executed during the search process.

DSR is computed as:

$$\text{DSR} = Z\left[ \frac{(\widehat{\text{SR}} - \text{SR}_0) \cdot \sqrt{T-1}}{\sqrt{1 - \widehat{\gamma}_3 \cdot \widehat{\text{SR}} + \frac{\widehat{\gamma}_4 - 1}{4} \cdot \widehat{\text{SR}}^2}} \right]$$

Where:
* $\widehat{\text{SR}}$ is the estimated Sharpe Ratio.
* $\text{SR}_0$ is the minimum acceptable Sharpe Ratio (accounting for the number of trials $N$ and the variance of Sharpe Ratios across those trials).
* $T$ is the number of trading observations.
* $\widehat{\gamma}_3, \widehat{\gamma}_4$ are the skewness and kurtosis of the returns.
* $Z$ is the cumulative standard normal distribution.

If the DSR falls below a strict threshold (typically $95\%$ or $0.95$ probability), the strategy is rejected, even if its raw Sharpe Ratio is high.

---

## 3. Probability of Backtest Overfitting (PBO)

PBO measures the likelihood that the strategy selected as "best" in-sample will underperform out-of-sample.

### Combinatorially Symmetric Cross-Validation (CSCV)
To compute PBO:
1. Divide the historical returns matrix of all $N$ tested strategies into $M$ equal-sized blocks.
2. Form all combinations of choosing $M/2$ blocks. This creates a balanced split of training and test sets.
3. For each combination, find the optimal parameter set in the training blocks, and measure its performance in the test blocks.
4. Calculate the rank of the selected parameter set in the test blocks.
5. **PBO** is the proportion of combinations where the selected strategy performs below the median out-of-sample.

The Research OS enforces a maximum allowable PBO (typically $\le 0.10$) for any production model.

---

## 4. Bootstrapping & Monte Carlo Robustness

To ensure strategy stability across alternative market realizations, we employ:

### 4.1 Stationary Block Bootstrap
To preserve the temporal dependency (autocorrelation) of financial time-series, we use the block bootstrap:
* Instead of sampling individual daily returns with replacement, we sample *blocks* of continuous returns of random lengths.
* We generate 1,000 bootstrapped histories and evaluate the model's Sharpe Ratio distribution.
* **Gate Requirement:** The $5\text{th}$ percentile of the bootstrapped Sharpe Ratios must be greater than 0.

### 4.2 Monte Carlo Parameter Perturbations
Randomly perturbs model parameters, transaction cost assumptions, and execution latencies. If minor parameter adjustments lead to catastrophic performance drops, the model is flagged as fragile and rejected.
