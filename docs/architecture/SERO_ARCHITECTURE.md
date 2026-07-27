# SERO — Sovereign Entrepreneurial Research Organization
## Authoritative Architecture Specification & Contract (v2.1.0)
### AI-EOS — Complete Reference & Formal Specification (v1.0)

This is the canonical, binding architecture contract for **SERO (Sovereign Entrepreneurial Research Organization) v2.1**, elevating the system from a sequential feature workflow to a **Research-as-Primary-Abstraction Architecture** fully integrated with a **7-Stage Cognitive Lifecycle**, **Research Economics**, a **Multi-Paradigm Collective Intelligence Layer**, and the complete **AI-EOS Reference Stack**.

---

## 0. The Six Subsystems

```
                    ┌─────────────────────────────────┐
                    │  IES — Institutional Evolution   │  (governs all below)
                    └────────────────┬────────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                             │
┌───────▼────────┐         ┌─────────▼─────────┐         ┌─────────▼────────┐
│  ROS            │◄───────►│  KOS               │◄───────►│  EIS              │
│  Research OS    │         │  Knowledge OS       │         │  Entrepreneurial  │
│                 │         │  (shared substrate)  │         │  Intelligence     │
└───────┬─────────┘         └─────────┬───────────┘         └─────────┬────────┘
        │                             │                                │
        └────────────────┬────────────┴───────────────┬────────────────┘
                          │                             │
                 ┌────────▼────────┐          ┌─────────▼────────┐
                 │  VES             │◄────────►│  POS              │
                 │  Venture         │          │  Portfolio OS      │
                 │  Execution       │          │  (capital + risk)  │
                 └──────────────────┘          └───────────────────┘
```

**KOS is the substrate, not a peer node.** ROS writes theories and evidence into it; VES writes real-world outcomes into it; EIS reads it to decide what's worth pursuing; POS reads it to price risk. Nothing in the system holds private, ungraphed beliefs — that was v1's core flaw (memory without epistemics).

---

## 1. System-Wide Architecture

### 1.1 Layered Stack

```
L7  GOVERNANCE          Human Governance Council · Policy Engine · Kill-Switches · Audit Ledger
L6  META-COGNITION       Self-Improvement Engine · Meta-Learner · Architecture Search · Skill Library
L5  STRATEGY             Planning Engine (MCTS/LLM-hybrid) · Active Inference Loop · Portfolio Allocator
L4  SCIENTIFIC ENGINE    Hypothesis Generator · Experiment Designer · Causal Inference · Simulation Sandbox
L3  DOMAIN AGENT SOCIETY Discovery · Research · Brand/Product · GTM · Sales · Finance · Ops · Legal · Expansion
L2  WORLD MODEL          Market World Model · Competitor Model · Customer Behavior Model · Macro/Regulatory Model
L1  MEMORY               Episodic · Semantic · Procedural · Working Memory · Vector + Graph + Ledger stores
L0  DATA & TOOL FABRIC   Market data · Web/API access · Payment rails · Ad platforms · CRM · Accounting · Compliance
```

### 1.2 Governing Principles (inherited from AEAN, generalized)
1. **Capital-gated expansion** — no subsystem activates above its funded tier until the upstream loop has proven itself economically (analogous to the 14-day profitable-loop gate, generalized to "N days of positive unit economics" per venture).
2. **Verifiable reward over vibes** — every agent loop that can be graded against a real-world signal (PnL, conversion, retention, CAC:LTV) is trained/selected via verifiable reward (GRPO-style), not subjective LLM self-scoring alone.
3. **Simulate before spending** — every action with real capital or reputational cost must pass through the Simulation Sandbox and a causal pre-mortem before execution.
4. **Human-in-the-loop at irreversibility boundaries** — capital deployment, legal commitments, brand-identity lock-in, hiring, and pricing changes above a materiality threshold are non-waivable gates (same posture as ADGS's non-waivable human approval gate in AlphaAlgo).
5. **One venture, one microfish loop, one owner-agent** — each business unit is a bounded "venture cell" with its own P&L, agent team, and memory namespace, orchestrated but not entangled with siblings until portfolio-level capital allocation decisions are made.

### 1.3 Core Cross-Cutting Systems

| System | Function | Notes |
|---|---|---|
| **World Model** | Learned/structured simulator of market dynamics, competitor responses, customer behavior, macro conditions | Analogous to FWAM's world-state-estimation layer, generalized from markets to entrepreneurship |
| **Memory Hierarchy** | Episodic (venture event logs), Semantic (market/domain knowledge graph), Procedural (playbooks, SOPs distilled from wins/losses), Working (active venture context) | Vector DB + knowledge graph + append-only ledger; namespaced per venture cell, federated at portfolio level |
| **Planning Engine** | Long-horizon plan generation and revision using tree search over the World Model + LLM proposal/critique loop | Same lineage as the Verdict Engine's specialist→peer-review→chairman deliberation pattern |
| **Simulation Sandbox** | Digital-twin economy: synthetic customers, competitors, ad auctions, price-response curves | Used for pre-mortems, A/B pre-testing, capital-at-risk estimation before live spend |
| **Causal Engine** | Distinguishes correlation from causation in growth/marketing/pricing signals | Structural causal models + double ML + uplift modeling |
| **Governance Layer** | ADGS-style tiered gates: capital permission tiers, mandatory "paper trading" period for new ventures, non-waivable human approval on irreversible actions | Directly reusable from AlphaAlgo's ADGS design |
| **Self-Improvement Engine** | Mines closed venture loops for what worked, updates procedural memory, proposes agent/prompt/architecture changes | Governed by the same expansion-gate discipline — no self-modification ships without passing its own validation loop |

---

## 2. Cross-Cutting Agent Registry

| Agent | Role | Reports To |
|---|---|---|
| Opportunity Scout | Continuous signal scanning for emerging demand | Discovery Orchestrator |
| Market Research Analyst | TAM/SAM/SOM, industry structure, Porter's Five Forces automation | Discovery Orchestrator |
| Competitor Intelligence Agent | Competitive landscape mapping, positioning gap analysis | Discovery Orchestrator |
| Customer Discovery Agent | Synthetic + real interview design, JTBD extraction | Discovery Orchestrator |
| Idea Synthesis Agent | Combines signals into scored venture hypotheses | Validation Orchestrator |
| Business Model Architect | Canvas generation, unit economics modeling | Validation Orchestrator |
| Financial Modeling Agent | Forecasting, scenario/sensitivity analysis | Validation Orchestrator |
| Brand Strategist / Namer | Naming, positioning, verbal/visual identity briefs | Build Orchestrator |
| Product Architect | Feature prioritization, MVP scoping | Build Orchestrator |
| Pricing Strategist | Price sensitivity modeling, packaging | Build Orchestrator |
| Codegen/MVP Agent | Ships MVP (interfaces with Jules for paste-ready build instructions) | Build Orchestrator |
| GTM Strategist | Channel selection, launch sequencing | GTM Orchestrator |
| Content Generation Agent | Copy, SEO content, ad creative | GTM Orchestrator |
| SEO Agent | Technical + content SEO, keyword/topic graphs | GTM Orchestrator |
| Paid Media Agent | Bid/budget optimization across ad platforms | GTM Orchestrator |
| Social/Community Agent | Organic social, community management | GTM Orchestrator |
| Sales Funnel Agent | Funnel design, CRO experiments | Revenue Orchestrator |
| CRM/Automation Agent | Lead scoring, sequencing, handoffs | Revenue Orchestrator |
| Customer Support Agent | Tier-1 support, escalation triage | Revenue Orchestrator |
| Revenue Optimization Agent | Pricing/upsell/churn interventions | Revenue Orchestrator |
| Fundraising Agent | Deck generation, investor targeting, data room prep | Capital Orchestrator |
| Capital Allocation Agent | Portfolio-level capital routing across venture cells | Capital Orchestrator |
| Risk Analyst Agent | Venture and portfolio risk scoring | Capital Orchestrator |
| Expansion Strategist | New-market entry analysis, localization | Expansion Orchestrator |
| Org Design Agent | Role definition, hiring plans | Ops Orchestrator |
| Legal/Compliance Agent | Regulatory scanning, contract/entity drafting for counsel review | Ops Orchestrator |
| KPI/Telemetry Agent | Metrics pipeline, anomaly detection | Ops Orchestrator |
| Experimentation Agent | A/B test design, sequential testing, power analysis | Scientific Engine |
| Self-Improvement Agent | Playbook distillation, architecture proposals | Meta-Cognition Layer |

Each Orchestrator is a chairman-agent pattern (specialists propose → peer-review agents critique → chairman decides), reusing the Verdict Engine pattern from AlphaAlgo.

---

## 3. Model Stack

| Category | Purpose | Examples of Technique |
|---|---|---|
| Frontier LLM (reasoning/generation) | Strategy synthesis, copywriting, deliberation | Claude-class models as chairman + specialist agents |
| Small/distilled LLMs | High-volume low-cost tasks (tagging, classification, first-pass content) | Tier-1 zero-cost default models |
| Forecasting models | Demand, revenue, churn, macro trend forecasting | Temporal fusion transformers, N-BEATS, classical ARIMA/Prophet as cheap baselines |
| Optimization | Pricing, budget allocation, portfolio capital allocation | Convex/mixed-integer optimization, Bayesian optimization for hyperparameter-like business levers |
| Reinforcement Learning | Ad bidding, funnel sequencing, dynamic pricing | Offline RL + verifiable-reward online fine-tuning (GRPO-style) |
| Causal AI | Marketing attribution, pricing elasticity, feature-impact estimation | Structural causal models, double machine learning, synthetic control, uplift trees |
| World Models | Market/customer/competitor simulation | Learned dynamics models in the spirit of Cosmos/V-JEPA2/DreamerV3, scoped down to structured business-simulation state spaces |
| Embedding/Retrieval | Semantic memory, competitor/document search | Dense retrieval + knowledge graph hybrid |
| Anomaly Detection | KPI monitoring, fraud/risk flags | Statistical process control + learned anomaly scoring |
| Experimentation Statistics | A/B and sequential testing | Bayesian bandits, sequential probability ratio tests, CUPED variance reduction |

---

## 4. Required Datasets (by domain)

- **Macro/industry**: government statistics, trade data, industry reports, patent filings, job postings (demand signal proxy)
- **Competitor**: pricing pages, review sites, ad libraries, hiring pages, funding databases
- **Customer**: survey/interview transcripts (synthetic + real), support tickets, session analytics, review mining
- **Marketing performance**: ad platform APIs, SEO rank tracking, content engagement, email/CRM event streams
- **Financial**: internal ledger/accounting exports, comparable-company financials, capital markets data
- **Legal/regulatory**: jurisdictional statute databases, regulatory filings, compliance requirement libraries
- **Internal**: closed-loop venture outcome logs (the single highest-value proprietary dataset — this is what the Self-Improvement Engine trains on)

---

## 5. Lifecycle Phases

### Phase 0 — Opportunity Discovery & Market Research
*   **Objectives:** Continuously surface and rank venture-worthy demand signals; convert raw signal into scientifically grounded market understanding.
*   **Agents:** Opportunity Scout, Market Research Analyst, Competitor Intelligence Agent, Customer Discovery Agent
*   **Models:** LLM signal extraction/classification, trend forecasting models, embedding-based clustering for whitespace detection, causal AI for demand-driver isolation
*   **Research methodologies:** Porter's Five Forces, TAM/SAM/SOM triangulation, JTBD interviews, complaint mining, patent/hiring-signal analysis.
*   **Decision frameworks:** Opportunity scoring matrix (market size × growth rate × pain intensity × competitive white space × capital required × time-to-signal); kill/pursue/park classification
*   **Validation metrics:** Signal recurrence rate, interview saturation point, willingness-to-pay indicators, competitor response latency.
*   **Automation workflows:** Scheduled scan → signal dedup/cluster → scored opportunity backlog → weekly ranked shortlist surfaced to human governance.
*   **Human approval gates:** Selection of which opportunities enter the Validation phase (capital-relevant decision — non-waivable).
*   **Failure modes:** False-positive demand signals from SEO/ad noise; survivorship bias; synthetic panel drift.
*   **Risk management:** Cross-validate synthetic findings against minimum real-user samples; source diversity.
*   **Feedback loops:** Outcomes feed back into scoring-matrix weights.
*   **Self-improvement:** Scout's source-weighting is retrained on historical success.

### Phase 1 — Idea Validation, Business Model & Financial Modeling
*   **Objectives:** Convert a scored opportunity into a validated, fundable business hypothesis with a defensible model and numbers.
*   **Agents:** Idea Synthesis Agent, Business Model Architect, Financial Modeling Agent
*   **Models:** LLM hypothesis generation/critique, Monte Carlo financial simulation, forecasting models, causal AI sensitivity.
*   **Research methodologies:** Lean Startup validation loops, Business Model Canvas automation, scenario-based financial modeling (base/bull/bear), pre-mortem analysis.
*   **Decision frameworks:** Unit economics gate ($CAC:LTV \ge \text{threshold}$, payback period $\le \text{threshold}$), capital-efficiency scoring vs. tier budget, Verdict Engine deliberation.
*   **Validation metrics:** Landing-page conversion, pre-order conversion, projected gross margin, break-even timeline, NPV sensitivity.
*   **Automation workflows:** Smoke-test pages + spend budget → conversion telemetry → auto-updated financial model → recommendation.
*   **Human approval gates:** Capital commitment to build MVP; entity formation; legal/IP commitment.
*   **Failure modes:** Model overfitting; smoke-test conversion inflation; ignoring regulatory cost.
*   **Risk management:** Tiered capital permissions; mandatory downside-scenario sign-off.
*   **Feedback loops:** Actual vs. modeled unit economics retrains Financial Agent priors.
*   **Self-improvement:** Business Model canvas templates evolve based on historical survival.

### Phase 2 — Brand, Product & Pricing Design
*   **Objectives:** Design the venture's identity, MVP, and pricing architecture.
*   **Agents:** Brand Strategist/Namer, Product Architect, Pricing Strategist, Codegen/MVP Agent
*   **Models:** LLM naming/positioning, feature-prioritization optimization, price-sensitivity modeling (Van Westendorp conjoint simulation), RL for pricing.
*   **Research methodologies:** Positioning-map construction, name testing, JTBD MVP scoping, conjoint analysis.
*   **Decision frameworks:** Brand scorecard; MVP scope = minimum features resolving top-3 validated JTBD; value-metric pricing anchors.
*   **Validation metrics:** Recall/preference scores, trademark clearance, build cost vs. budget, conversion elasticity.
*   **Automation workflows:** Brand brief → trademark screen → spec → verified paste-ready build instructions to Jules.
*   **Human approval gates:** Final brand identity lock-in; pricing model launch above threshold.
*   **Failure modes:** Trademark collision; scope creep; pricing anchored without elasticity data.
*   **Risk management:** Mandatory trademark clearance; scope frozen against written JTBD contract.
*   **Feedback loops:** Post-launch recall and pricing conversion data retrains models.
*   **Self-improvement:** Scoping heuristics distilled into Product Architect playbooks.

### Phase 3 — Go-To-Market & Marketing Execution
*   **Objectives:** Launch demand generation across owned, earned, and paid channels.
*   **Agents:** GTM Strategist, Content Generation Agent, SEO Agent, Paid Media Agent, Social/Community Agent
*   **Models:** LLM content, RL ad-bid optimization, channel demand forecasting, causal multi-touch attribution.
*   **Research methodologies:** Channel-fit analysis, content-gap topic-graph research, creative multi-armed bandits.
*   **Decision frameworks:** Channel prioritization by CAC efficiency; budget allocated via Bayesian bandit with online reallocation.
*   **Validation metrics:** CAC by channel, content organic growth, ad CTR/CVR, share of voice.
*   **Automation workflows:** Calendar → content/ad generation → scheduled publish → real-time monitoring → budget reallocation.
*   **Human approval gates:** Total spend ceiling; brand-voice review at scale; regulatory claims review.
*   **Failure modes:** Attribution misreading; creative fatigue; SEO self-cannibalization.
*   **Risk management:** Hard spend caps; automatic pause on negative ROAS; causal attribution.
*   **Feedback loops:** Attribution-verified performance updates prioritization.
*   **Self-improvement:** Winning creative patterns compiled to playbooks.

### Phase 4 — Sales, Customer Acquisition & Revenue Optimization
*   **Objectives:** Convert demand into revenue and continuously optimize the revenue engine.
*   **Agents:** Sales Funnel Agent, CRM/Automation Agent, Customer Support Agent, Revenue Optimization Agent, Experimentation Agent
*   **Models:** RL for funnel sequencing, LLM support/sales, causal churn isolation, Bayesian A/B testing.
*   **Research methodologies:** Funnel conversion diagnostics, cohort retention analysis, churn causal analysis, CRO experiments.
*   **Decision frameworks:** Experiment prioritization ($lift \times confidence \times ease$); gated by minimum power requirements.
*   **Validation metrics:** Funnel conversion by stage, $CAC:LTV$, churn rate, NPS/CSAT, experiment win-rate.
*   **Automation workflows:** Experiment queue → sequential testing → CRM triggers → support ticket triage with human escalation.
*   **Human approval gates:** Pricing changes above threshold; legal customer communications; refund exceptions.
*   **Failure modes:** Peeking/false-positive experiments; support support failures; short-term over-optimization.
*   **Risk management:** Sequential testing corrections (SPRT/CUPED); mandatory human escalation sentiments.
*   **Feedback loops:** Outcomes logged to KOS and used to update belief priors.
*   **Self-improvement:** Prioritization heuristics retrained on realized experiment ROI.

### Phase 5 — Capital, Finance & Portfolio Management
*   **Objectives:** Prepare and execute fundraising, allocate capital across venture cells, monitor financial performance and risk.
*   **Agents:** Fundraising Agent, Capital Allocation Agent, Risk Analyst Agent, Financial Modeling Agent
*   **Models:** Portfolio optimization, forecasting runway, causal capital-efficiency attribution, risk classifiers.
*   **Research methodologies:** Investor fit targeting, data room prep, scenario-based runway modeling, portfolio correlated-risk.
*   **Decision frameworks:** Capital allocated by risk-adjusted return; fundraising pursued on internal benchmarks.
*   **Validation metrics:** Burn multiple, runway months, capital efficiency, portfolio Sharpe ratio.
*   **Automation workflows:** Health dashboard → auto tier-eligibility → capital reallocation proposals → fundraising drafts.
*   **Human approval gates:** ALL capital deployment above Tier 1; external fundraising; inter-venture capital transfer (non-waivable).
*   **Failure modes:** Overallocation on noisy signals; correlated risk underestimation; overstating traction.
*   **Risk management:** Mandatory validation period; correlation analysis; fact-checking claims against ledger.
*   **Feedback loops:** Realized ROI feeds return-forecasting model.
*   **Self-improvement:** Risk-adjustment weights recalibrated against outcomes.

### Phase 6 — Operations, Organization, Legal & Compliance
*   **Objectives:** Keep the venture operationally sound, properly staffed/structured, and legally compliant as it scales.
*   **Agents:** Org Design Agent, Legal/Compliance Agent, KPI/Telemetry Agent
*   **Models:** LLM contract drafting, regulatory-change classifiers, anomaly detection, span-of-control optimization.
*   **Research methodologies:** Regulatory scanning, org benchmarking, KPI-tree construction.
*   **Decision frameworks:** Hire only on validated growth constraint; legal actions routed to counsel for sign-off.
*   **Validation metrics:** Compliance audit pass rate, KPI tree predictive accuracy, operational cost ratio, role utilization.
*   **Automation workflows:** Regulatory scan → Legal Agent → draft update → human review → dashboard updates.
*   **Human approval gates:** All legal filings, contracts, and regulatory submissions (non-waivable); hiring decisions.
*   **Failure modes:** Missing jurisdiction-specific nuance; KPI tree drift; premature hiring.
*   **Risk management:** Legal Agent output advisory-only; KPI tree causal validity re-tested.
*   **Feedback loops:** Compliance incidents feed scanning model sensitivity.
*   **Self-improvement:** Headcount-trigger heuristics refined against resolved constraints.

### Phase 7 — Expansion & Scaling (Multinational)
*   **Objectives:** Replicate validated venture loops into new markets/geographies/segments without breaking capital discipline.
*   **Agents:** Expansion Strategist, Market Research Analyst, Legal/Compliance Agent, Capital Allocation Agent
*   **Models:** Transfer-learning applied to World Model, localized demand forecasting, causal transferability isolation.
*   **Research methodologies:** New-market opportunity scoring, localization gap analysis, phased pilot entry.
*   **Decision frameworks:** New market receives Tier 2/3 capital only after pilot-scale profitable-loop validation.
*   **Validation metrics:** Localized $CAC:LTV$, regulatory clearance time, pilot unit economics vs. benchmark.
*   **Automation workflows:** Candidate scored → pilot cell spun up with localized inputs → phase pipeline re-run.
*   **Human approval gates:** Entry into new legal jurisdiction; cross-border capital movement; entity formation abroad.
*   **Failure modes:** Assuming 1:1 playbook transfer; underestimating localization cost; currency risk.
*   **Risk management:** Every expansion cell treated as a new, unproven venture with independent gating.
*   **Feedback loops:** Cross-market performance differentials feed transferability estimates.
*   **Self-improvement:** Build increasingly accurate playbook transferability model across market pairs.

### Phase 8 — Continuous Learning, Strategic Planning & Self-Improvement (Meta-Layer)
*   **Objectives:** Ensure the entire system gets measurably better at entrepreneurship over time, not just at running any single venture.
*   **Agents:** Self-Improvement Agent, all Orchestrators, Governance Council
*   **Models:** Meta-learning over closed outcomes, agent/prompt architecture search, active-inference planning.
*   **Research methodologies:** Retrospective post-mortems/pre-mortems, playbook distillation, sandbox architecture experiments.
*   **Decision frameworks:** Self-modification must simulate favorably, pass shadow trial, and receive human governance sign-off.
*   **Validation metrics:** Portfolio success rate, time-to-validation trend, capital efficiency, forecast calibration.
*   **Automation workflows:** Closed cell → retrospective → distilled lessons to memory → proposals generated.
*   **Human approval gates:** All production self-modification (new agents, changed capital thresholds) (non-waivable).
*   **Failure modes:** Reward hacking; overfitting playbooks; runaway self-modification loops.
*   **Risk management:** Hard-coded invariants; kill-switch retained by human Governance Council at all times.
*   **Feedback loops:** This is the master feedback loop — every other phase terminates here.
*   **Self-improvement:** Recursive, bounded self-evolution of venture running, never governance.

---

## 6. KOS/ROS Formal Specification — v1.0

### 6.1 Epistemic Graph Data Schemas

```typescript
Hypothesis {
  id: string                          // uuid
  statement: string
  domain: string                      // e.g. "pricing", "onboarding", "channel-fit"
  venture_id: string | null           // null if venture-agnostic / cross-cutting

  prior_confidence: float             // 0-1, set at creation
  posterior_confidence: float         // updated by Bayesian Belief Engine
  confidence_distribution: {          // not just a point estimate
    type: "beta" | "gaussian" | "dirichlet"
    params: object                    // e.g. {alpha, beta} for Beta
  }

  supporting_evidence: EvidenceRef[]
  contradicting_evidence: EvidenceRef[]
  dependent_hypotheses: HypothesisRef[]   // what this claim assumes
  downstream_decisions: DecisionRef[]     // what relies on this claim

  assumption_count: int               // derived: count of unproven dependent_hypotheses
  single_source_flag: bool            // derived: true if evidence_count == 1
  high_impact_low_evidence_flag: bool // derived, see §6.5

  status: "proposed" | "under_test" | "active" | "falsified" | "superseded" | "theory_promoted"
  created_at: timestamp
  last_updated: timestamp
}

Evidence {
  id: string
  source: string                      // URI, document ref, experiment id
  source_type: "experiment" | "observation" | "literature" | "simulation" | "interview" | "survey"

  evidence_quality_tier: "rct" | "natural_experiment" | "longitudinal" |
                          "survey" | "interview" | "opinion" | "synthetic"

  reliability_weight: float           // 0-1, derived from quality_tier lookup table,
                                       // manually overridable with logged justification

  strength: {
    effect_size: float | null
    sample_size: int | null
    interval: [float, float] | null   // CI or credible interval
    p_or_posterior: float | null
  }

  causal_or_correlational: "causal" | "correlational" | "unknown"
  linked_hypotheses: HypothesisRef[]

  replicated_by: EvidenceRef[]        // empty until independently replicated
  replication_status: "unreplicated" | "replicated" | "failed_replication"

  timestamp: timestamp
  decay_rate: float                   // relevance half-life, domain-dependent default
  current_relevance: float            // derived: decays over time, flags for review when < threshold
}

Theory {
  id: string
  statement: string                   // general explanatory model
  constituent_hypotheses: HypothesisRef[]
  predictive_scope: Prediction[]      // untested implications, auto-queued as new Hypotheses

  confidence: float
  predictive_track_record: {
    predictions_made: int
    predictions_confirmed: int
    predictions_falsified: int
    accuracy_rate: float              // confirmed / (confirmed + falsified)
  }

  promotion_criteria_met: {
    independent_evidence_count: int   // >= 2 required, from distinct source_types
    generalization_tested: bool       // has scope been tested outside origin context
    predictive_success_threshold_met: bool   // accuracy_rate >= 0.7 after >= 3 predictions
  }

  contradictions: ContradictionRef[]
  status: "draft" | "active" | "contradicted" | "retired"
}

Contradiction {
  id: string
  node_a: HypothesisRef | TheoryRef
  node_b: HypothesisRef | TheoryRef
  detected_by: "contradiction_detection_agent" | "manual"
  detected_at: timestamp
  severity: "low" | "medium" | "high"      // derived from downstream_decisions impact
  resolution_status: "open" | "escalated" | "resolved"
  resolution_action: string | null
  routed_to: "chairman_agent" | "human_governance"  // high severity always routes to human
}

Relationship {
  from: HypothesisRef | TheoryRef
  to: HypothesisRef | TheoryRef
  type: "supports" | "contradicts" | "causes" | "correlates" |
        "derived_from" | "generalizes" | "specializes" | "requires" |
        "duplicates" | "updates"
}

DecisionRecord {
  id: string
  decision: string
  supporting_hypotheses: HypothesisRef[]
  confidence_at_decision: float
  rejected_alternatives: string[]
  rationale: string
  made_by: "agent" | "human"
  outcome: {
    realized: bool
    actual_result: string | null
    confidence_in_hindsight: float | null   // populated post-hoc, feeds calibration audit
  }
}

Experiment {
  id: string
  hypothesis_tested: HypothesisRef
  design: {
    method: string
    sample_size_planned: int
    power: float
    pre_registered: bool              // hypothesis/threshold locked before data collection
  }
  status: "designed" | "running" | "complete" | "aborted"
  result_evidence: EvidenceRef | null
}
```

### 6.2 Research Compiler (KOS Ingestion Pipeline)

Converts raw documents/materials into clean Evidence nodes.

```
Raw input (paper | patent | transcript | market report | filing | reviews)
   ↓
[Extraction]        — pull claims, numbers, effect sizes (no raw copyright text)
   ↓
[Normalization]      — map extracted claims onto existing domain vocabulary synonyms
   ↓
[Deduplication]      — check against existing Evidence nodes to avoid double-counting
   ↓
[Conflict Resolution] — if a claim contradicts existing Evidence, raise a Contradiction
   ↓
[Evidence Node Creation] — assign quality_tier and calculate reliability_weight
   ↓
[Hypothesis Update]  — Bayesian Belief Engine triggered on all linked hypotheses
```

### 6.3 Bayesian Belief Engine

For a Hypothesis with Beta(α, β) posterior:

```
On new Evidence e with reliability_weight w and directional strength s (support=+1/contradict=-1):
  α_new = α + (w × s_positive_component)
  β_new = β + (w × s_negative_component)
  posterior_confidence = α_new / (α_new + β_new)
```

Reliability Weight Lookup defaults:
*   `rct`: 1.0
*   `natural_experiment`: 0.8
*   `longitudinal`: 0.7
*   `survey`: 0.5
*   `interview`: 0.4
*   `opinion`: 0.2
*   `synthetic`: 0.15

### 6.4 Contradiction Detection & Routing

```
on_evidence_added(e: Evidence):
  for h in e.linked_hypotheses:
    for h2 in KOS.hypotheses where h2.domain == h.domain and h2.id != h.id:
      if semantic_overlap(h, h2) > threshold and posterior_confidence(h) and posterior_confidence(h2) are inconsistent:
        create Contradiction(node_a=h, node_b=h2, severity=compute_severity(h, h2))
        if severity == "high": route_to_human_governance()
        else: route_to_chairman_agent()
```

### 6.5 Epistemic Risk (KOS Query Layer)

*   **Calibration Audit**: Monthly schedule, flagging any bucket miscalibration $> 0.15$:
    ```
    audit_calibration():
      for each confidence bucket (60-70%, 70-80%...):
        realized_rate = count(DecisionRecord where confidence_at_decision in bucket and outcome.realized == true) / count(in bucket)
        flag if |realized_rate - bucket_midpoint| > 0.15
    ```
*   **High-Impact / Low-Evidence Flag**:
    ```
    flag_high_impact_low_evidence():
      return Hypothesis where downstream_decisions.count >= impact_threshold AND supporting_evidence.count <= 1
    ```
*   **Assumption Depth**: Recursively counts the depth of unproven dependent hypotheses.
*   **Ignorance Registry (View)**: Unions unproven high-impact nodes and sparse-evidence domains, automatically boosting their Expected Information Gain score inside Discovery Mathematics.

---

## 7. The 7 Cognitive Stages

Every major execution or adaptative lifecycle in SERO v2.1 maps directly onto seven discrete, measurable cognitive stages, aligning technical operations with biological cognitive frameworks.

1.  **Imagine**: The creative generation phase. Generates candidate opportunity signals, hypothesis spaces, and alternative tactical scenarios.
2.  **Plan**: The modeling and forecasting phase. Evaluates consequences inside the simulation sandbox, estimates NPV and Information Gain, and allocates budget and compute.
3.  **Experiment**: The active intervention phase. Executes sandbox trials, physical testing pilots, or multi-armed ad campaigns under strict seed controls.
4.  **Learn**: The analytical reflection phase. Measures prediction error (forecast vs. measurement), computes Bayes posterior updates, and extracts factual assertions.
5.  **Generalize**: The inductive promotion phase. Synthesizes validated hypotheses into generalized Theory nodes, mapping predictive scopes across venture boundaries.
6.  **Teach**: The propagation and distribution phase. Compiles playbooks, updates the shared substrate, and deploys distilled system capabilities to active agents.
7.  **Govern**: The regulatory filter phase. Evaluates risk limits, security safety, legal compliance, complexity budgets, and architectural coupling conformance.

---

## 8. Research Economics & Knowledge ROI

SERO v2.1 introduces strict quantitative metrics representing **Knowledge ROI** ($K_{ROI}$):

*   **Cost per Validated Theory** ($C_{VT}$): Total Research Portfolio budget spent divided by the number of hypotheses successfully promoted to general Theory status.
*   **Cost per Uncertainty Reduction** ($C_{UR}$): Total research spend divided by the sum of belief entropy reduction ($\Delta H$) achieved across all KOS Hypothesis nodes.
*   **Cost per Reusable Insight** ($C_{RI}$): Cost divided by the count of playbooks and capabilities successfully distilled and adopted by multiple downstream Venture Cells.
*   **Cost per Future Venture Unlocked** ($C_{VU}$): Research spend divided by the number of high-tier commercial Venture Cells launched directly on top of promoted KOS Theories.

---

## 9. Multi-Paradigm Collective Intelligence Layer

SERO v2.1 routes all complex strategic decisions through a multi-mind **Collective Intelligence Layer** representing **six distinct reasoning paradigms**:

1.  **Bayesian Reasoner**: Thinks probabilistically. Updates conversion and success priors, and models expected information gain and belief entropy.
2.  **Symbolic Reasoner**: Thinks in strict logic and rules. Enforces schema validations, bounded context constraints, and invariant rules.
3.  **Causal Reasoner**: Thinks in causes and counterfactuals. Distinguishes correlation from causation using structural causal path models.
4.  **Economic Reasoner**: Thinks in unit economics and capital optimization. Maximizes P&L margins, LTV, and capital efficiency ratios.
5.  **Game-Theoretic Reasoner**: Thinks in payoffs and competitive equilibria. Analyzes competitor reactions, ad auctions, and pricing game strategies.
6.  **Mechanistic Reasoner**: Thinks in physical/operational flows. Scans step-by-step API responses, latency budgets, and system bottleneck paths.

The consensus score emerges from combining these six dimensions.

---

## 10. Explicitly Deferred (with stated trigger)

The following items are deferred from the build scope, only to be constructed when their specific trigger conditions are met:

| Deferred Item | Trigger to Build |
|---|---|
| **Formal Ontology** | Contradiction Detection false-positive rate exceeds 20% (semantic drift artifacts), OR the normalization synonym table exceeds 200 entries. |
| **Standalone Epistemic Risk Subsystem** | Epistemic Risk query layers require advanced cross-hypothesis blind-spot inference that basic queries cannot express. |
| **Multi-Level World Models as Separate Systems** | A single domain's update cadence or data source differs so heavily from others that coupling them causes stale-data errors. |
| **Full Scientific-Institution Layer** | Multiple independent human researchers/reviewers exist, requiring actual headcount and complex proper-scoring metrics (e.g., CRPS) to be meaningful. |

---

This contract is signed and approved. Any proposed deviation must be submitted through a formal ADR and approved before implementation.
