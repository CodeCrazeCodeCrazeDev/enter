# World Model Creator (WMC) Mathematical Frameworks
## Formal Formulations of Simulation, Cognition, and Causal Inference

---

## 1. Causal Structural Models (SCM) & Intervention Calculus

To model non-linear cause-and-effect relationships rather than simple statistical correlations, the World Model Creator (WMC) utilizes **Structural Causal Models (SCMs)** and Pearl’s **$\text{do}$-calculus**.

### 1.1 Structural Equations
A world state is defined by a set of endogenous variables $V = \{Y_1, Y_2, \dots, Y_n\}$ and exogenous background noise variables $U = \{U_1, U_2, \dots, U_n\}$. The state transitions and variable dependencies are governed by a set of structural equations:

$$Y_i = f_i(Pa(Y_i), U_i)$$

where $Pa(Y_i) \subset V$ represents the direct causal parent nodes of $Y_i$ in the World Graph, and $U_i$ are independent, identically distributed noise components representing unobserved background influences.

### 1.2 Interventions ($\text{do}$-Calculus)
To simulate a hypothetical scenario or strategy (e.g., assessing the impact of raising product price), the simulation engine performs a causal intervention, replacing a structural equation with a fixed value:

$$\text{do}(Y_k = y^*)$$

Mathematically, this intervention modifies the joint probability distribution of the world graph by deleting the causal links from $Pa(Y_k)$ to $Y_k$:

$$P(V \setminus \{Y_k\} \mid \text{do}(Y_k = y^*)) = \prod_{i \neq k} P(Y_i \mid Pa(Y_i))$$

This equation allows the WMC to calculate downstream effects without polluting the data with historical bias or non-causal correlations.

### 1.3 Counterfactuals
Counterfactual reasoning answers questions of the form: *"Given that outcome $Y=y$ occurred under actions $X=x$, what would $Y$ have been had $X$ been $x^*$?"*
The WMC resolves this using the three-step Pearlian process:
1. **Abduction:** Update the probability of the exogenous variables $U$ based on the observed evidence: $P(U \mid Y=y, X=x)$.
2. **Action:** Perform the intervention by replacing the structural equations of $X$ with the counterfactual action: $\text{do}(X = x^*)$.
3. **Prediction:** Compute the probability distribution of the target variable $Y$ under the modified structural model using the updated exogenous distribution: $P(Y^* \mid \text{do}(X=x^*))$.

---

## 2. Active Inference & Free Energy Formulations

The **Human Cognition Engine** and **Audience Intelligence Engine** simulate agent behaviors and belief updates using **Active Inference** (derived from Friston's Free Energy Principle). Under this framework, simulated humans choose actions that minimize their internal **Variational Free Energy** ($F$) and select strategies that minimize **Expected Free Energy** ($G$).

### 2.1 Variational Free Energy
A simulated agent maintains an internal generative model $q(s)$ over hidden, unobserved states of the world $s$, while receiving sensory observations $o$. The Variational Free Energy $F$ measures the discrepancy between the agent’s internal beliefs and the external reality:

$$F = D_{KL}(q(s) \parallel p(s)) - \int q(s) \ln p(o \mid s) \, ds$$

where:
- $D_{KL}$ is the Kullback-Leibler divergence (representing relative entropy).
- $p(s)$ is the prior distribution of hidden world states.
- $p(o \mid s)$ is the likelihood mapping hidden states to sensory inputs.

Minimizing $F$ is equivalent to maximizing the model evidence (lowering surprise), causing the simulated human to update their internal beliefs to align with their experiences.

### 2.2 Expected Free Energy and Policy Selection
Agents choose a plan or "policy" $\pi$ (such as continuing to use a SaaS tool or switching to a competitor) by evaluating the Expected Free Energy $G(\pi)$ over a future simulation horizon $\tau \in \{1, \dots, T\}$:

$$G(\pi) \approx \sum_{\tau} \left[ D_{KL}(q(o_{\tau} \mid \pi) \parallel p(o_{\tau})) + \mathbb{E}_{q(o_{\tau} \mid \pi)} [D_{KL}(q(s_{\tau} \mid o_{\tau}, \pi) \parallel q(s_{\tau} \mid \pi))] \right]$$

This formulation naturally balances two operational imperatives:
1. **Instrumental Value (First Term):** Pragmatic value. Minimizes the distance between predicted observations $q(o_{\tau} \mid \pi)$ and preferred target states $p(o_{\tau})$ (e.g., maintaining low operating costs).
2. **Epistemic Value (Second Term):** Information gain. Maximizes the expected resolution of uncertainty regarding the hidden states of the world.

The probability of an agent selecting a specific policy $\pi$ is then computed using a softmax distribution:

$$P(\pi) = \sigma(-\gamma G(\pi)) = \frac{\exp(-\gamma G(\pi))}{\sum_{\pi'} \exp(-\gamma G(\pi'))}$$

where $\gamma$ is a precision parameter representing the agent's confidence or cognitive alertness.

---

## 3. Bayesian Belief Updating

Every belief node $B$ in the World Graph represents an epistemic confidence score. When new real-world data points or simulation outcomes ($E$) are registered, the belief is updated recursively using **Bayesian Inference**:

$$P(B \mid E) = \frac{P(E \mid B) \cdot P(B)}{P(E)}$$

where:
- $P(B)$ is the prior belief confidence.
- $P(E \mid B)$ is the likelihood of observing evidence $E$ given that belief $B$ is true.
- $P(E)$ is the marginal likelihood of the evidence:

$$P(E) = P(E \mid B)P(B) + P(E \mid \neg B)P(\neg B)$$

### 3.1 Epistemic vs. Aleatoric Uncertainty
To handle complex, volatile simulation spaces, the WMC separates uncertainty into two distinct categories:

1. **Aleatoric Uncertainty ($\sigma^2_{alea}$):** Irreducible, statistical noise inherent in the physical or economic system (e.g., currency market fluctuations). Modeled using probabilistic variance parameters inside structural equations.
2. **Epistemic Uncertainty ($\sigma^2_{epist}$):** Reducible uncertainty due to lack of information or system knowledge (e.g., unknown competitor product pricing). Modeled as the entropy of the prior belief distribution:

$$H(B) = -\sum_{i} P(B_i) \log_2 P(B_i)$$

The active simulation loops target regions of high epistemic uncertainty, running directed counterfactual tests to collect data and reduce system entropy over time.
