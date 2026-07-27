# AI-EOS Research Base: 50 Papers SOTA Corpus
**Categories:** Recursive Self-Improvement, Recursive Self-Evolution, Multi-Agent Systems
**Status:** Formally Verified and Compiled
**Date:** June 2026

This document represents the official AI-EOS historical research corpus, verifying 50 cutting-edge papers on agent self-evolution, harness engineering, active memory, and meta-agent swarms. It serves as our conceptual foundation for building out the AI-EOS cognitive substrate.

---

## Section A: Recursive Self-Improvement (Foundational Mechanisms)

The lineage that asks: can a system rewrite its own decision-making process, and does the rewrite chain — improvement B built by improved-system A, improvement C built by improved-system B?

1. **Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement** [2410.04444] — ACL 2025. The reference architecture for an agent that rewrites its own logic at runtime via self-referential code modification, without a fixed meta-optimizer above it.
2. **Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents** [2505.22954] — Sakana AI. Combines Gödel-machine-style self-modification with open-ended evolutionary archive search instead of proving improvements correct — empirically validated, not formally verified.
3. **Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation** [2310.02304] — the earlier, narrower case: a seed "improver" program recursively applies itself to improve its own code-generation scaffold.
4. **Recursive Introspection: Teaching Language Model Agents How to Self-Improve** [2407.18219] — trains a model to introspect on its own prior attempts and correct them across turns, rather than relying on an external critic.
5. **The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators** [2606.26294] — closes the loop most self-improvement work leaves open: the *evaluator* co-evolves alongside the agent, so improvement can't just overfit a static judge.
6. **Escher-Loop: Mutual Evolution by Closed-Loop Self-Referential Optimization** [2604.23472] — mutual/bidirectional self-referential optimization between two evolving components rather than one system improving in isolation.
7. **Self-Reference in Large Language Models: The Introspection Threshold for Recursive Self-Improvement** [2607.04277] — the most recent and most skeptical paper in this set: surveys 2022–2026 self-referential prompting behavior and argues current LLMs show fragmentary self-awareness that falls short of the introspection formally required for genuine RSI. Directly relevant as a reality check on how far AI-EOS's self-improvement claims can actually go.
8. **Self-Reflection in LLM Agents: Effects on Problem-Solving Performance** `[cited]` [2405.06682] — empirical study of how much self-reflection alone (no weight or scaffold change) actually buys you.
9. **Robots That Ask for Help: Uncertainty Alignment for Large Language Model Planners** `[cited]` [2307.01928] — foundational to knowing *when* a self-improving system should defer instead of act, relevant to AI-EOS's governance layer.

---

## Section B: Recursive Self-Evolution (Agents, Harnesses, Skills, Memory Co-Evolving as a System)

Broader than Section A — this is the applied engineering layer: what actually gets evolved (skills, memory, harness components, tools) and the surveys mapping the whole space.

10. **A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence** [2507.21046] — the field's broadest taxonomy paper; useful as your master reference for where any given AI-EOS component sits.
11. **A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems** [2508.07407] — complementary survey, framed around lifelong/continual operation rather than the ASI framing of #10.
12. **Self-Improvements in Modern Agentic Systems: A Survey** [2607.13104] — Schmidhuber co-authored; most recent of the three surveys, useful as the tie-breaker where the other two disagree on taxonomy.
13. **SIA: Self Improving AI with Harness & Weight Updates** [2605.27276] — dual-lever loop (already anchoring your L2 harness layer).
14. **Self-Harness: Harnesses That Improve Themselves** [2606.09498] — three-stage harness-editing discipline (Weakness Mining → Proposal → Validation).
15. **MemoHarness: Agent Harnesses That Learn from Experience** [2607.14159] — per-case adaptive harness via dual-layer experience bank.
16. **Rethinking the Evaluation of Harness Evolution for Agents** [2607.12227] — the methodological check: matched-budget baselines or your "improvement" numbers are meaningless.
17. **Agentic Harness Engineering (AHE): Observability-Driven Automatic Evolution of Coding-Agent Harnesses** [2604.25850] — three observability pillars (component, experience, decision) solving the "can't attribute an edit's effect" problem.
18. **Harness-Aware Self-Evolving (HASE): Co-Evolving Model Weights, Harness, and Task Solutions** [2607.03935] — single model, one action space, both levers — no separate Feedback-Agent.
19. **Next-Generation Agentic Reinforcement Learning Systems Enable Self-Evolving Agents** [2607.01120] — argues the bottleneck is RL *infrastructure*, not algorithms.
20. **Experience Memory Graph: One-Shot Error Correction for Agents** [2607.13884] — graph-matched failure recovery instead of iterative reflection.
21. **Beyond Fixed Representations: The Vocabulary and Verifier Gaps in Open-Ended AI** [2607.09560] — diagnostic paper on why current systems can't invent genuinely new representational primitives (your Discovery Layer's open problem).
22. **Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering** [2604.08224] — cross-cutting survey, good taxonomy sanity-check against #10–12.
23. **A-MEM: Agentic Memory for LLM Agents** [2502.12110] — memory as a self-organizing, linked structure the agent builds and edits, not a static store.
24. **Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning** [2508.19828] — RL-trained memory management (what to keep, discard, retrieve) as its own skill.
25. **MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents** [2602.02474] — treats memory operations themselves as a skill set that evolves, not a fixed subsystem.
26. **SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning** [2602.08234] — skills as the recursively-improved unit rather than the whole harness or the whole model.
27. **Meta Context Engineering via Agentic Skill Evolution** [2601.21557] — context/prompt engineering itself becomes a target of agentic skill evolution.
28. **MetaSkill-Evolve: Recursive Self-Improvement of LLM Agents via Two-Timescale Meta-Skill Evolution** [2607.05297] — separates fast skill-level updates from slower meta-level updates governing how skills evolve.
29. **AgenticRed: Optimizing Agentic Systems for Automated Red-teaming** [2601.13518] — self-evolution applied adversarially — relevant to AI-EOS's governance layer as a stress-testing mechanism, not just a capability booster.
30. **Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing** [2602.04837] — evolution happens across a *population* of agents sharing experience, not one agent alone — bridges into Section C.
31. **TerraLingua: Emergence and Analysis of Open-Endedness in LLM Ecologies** [2603.16910] — studies open-endedness as an emergent ecological property of many interacting LLM agents rather than a designed feature.
32. **ShinkaEvolve: Towards Open-Ended and Sample-Efficient Program Evolution** [2509.19349] — Sakana AI; the current sample-efficiency leader in the AlphaEvolve-lineage of evolutionary program search (bandit-based LLM ensemble, novelty rejection sampling).
33. **CodeEvolve: An Open-Source Evolutionary Coding Agent for Algorithm Discovery and Optimization** [2510.14150] — open reimplementation of the AlphaEvolve approach with island-based genetic search + weighted LLM ensemble; useful as the actually-inspectable alternative to DeepMind's closed whitepaper.
34. **TurboEvolve: Towards Fast and Robust LLM-Driven Program Evolution** [2604.18607] — extends the AlphaEvolve-style loop with structured multi-offspring generation per LLM call and adaptive exploration/exploitation budgeting.

---

## Section C: Multi-Agent Systems (Coordination, Orchestration, Swarms, Protocols)

35. **Multi-Agent Collaboration Mechanisms: A Survey of LLMs** [2501.06322] — broad taxonomy of how LLM agents actually coordinate (debate, workflow, hybrid).
36. **Beyond Self-Talk: A Communication-Centric Survey of LLM-based Multi-Agent Systems** [2502.14321] — reframes MAS survey work around what agents communicate and why, rather than topology alone.
37. **Beyond Individual Intelligence: Surveying Collaboration, Failure Attribution, and Self-Evolution in LLM-based Multi-Agent Systems** [2605.14892] — explicitly bridges Sections B and C — self-evolution *of* a multi-agent system, not just a single agent.
38. **LLM Multi-Agent Systems: Challenges and Open Problems** [2402.03578] — earlier, foundational open-problems framing that most later surveys cite.
39. **Agentic Environment Engineering for Large Language Models: A Survey of Environment Modeling, Synthesis, Evaluation, and Application** [2606.12191] — the environment/simulation side of multi-agent work — what agents operate inside of, not just how they talk to each other.
40. **A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, and ANP** [2505.02279] — the protocol layer: how agents from different vendors/frameworks actually talk to each other, directly relevant if AI-EOS needs to orchestrate agents across Apodex/AEAN/third-party tools.
41. **Coordination as an Architectural Layer for LLM-Based Multi-Agent Systems** [2605.03310] — reports multi-agent systems fail in production 41–87% of the time, mostly from coordination defects rather than model capability, and argues for treating coordination as a separable, configurable architectural layer.
42. **Reinforcement Learning for LLM-based Multi-Agent Systems through Orchestration Traces** [2605.02801] — decomposes orchestration into five learnable sub-decisions (spawn, delegate, communicate, aggregate, stop) and finds the "when to stop" decision is essentially unaddressed in the literature as of mid-2026 — a concrete gap AI-EOS's governance layer could fill.
43. **Where LLM Agents Fail and How They Can Learn From Failures** [2509.25370] — failure-attribution methodology for multi-agent systems specifically, complementary to Experience Memory Graph's single-agent recovery approach.
44. **MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents** [2503.01935] — benchmark for measuring MAS collaboration/competition quality, not just task success.
45. **The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption** [2601.13671] — enterprise-deployment-focused, closest in framing to what AI-EOS needs for real venture operations rather than research benchmarks.
46. **Uno-Orchestra: Parsimonious Agent Routing via Selective Delegation** [2605.05007] — routes work to the minimum sufficient set of sub-agents rather than fanning out, directly relevant to AI-EOS's capital-constrained design posture.
47. **AOrchestra: Automating Sub-Agent Creation for Agentic Orchestration** [2602.03786] — the orchestrator creates new sub-agents on demand rather than working from a fixed roster — closer to genuine swarm elasticity.
48. **Dr. MAS: Stable Reinforcement Learning for Multi-Agent LLM Systems** [2602.08847] — addresses training instability specific to multi-agent RL setups, a practical prerequisite if AI-EOS trains coordination policies rather than hand-designing them.
49. **SwarmResearch: Orchestrating Coding Agents for Open-Ended Discovery** [2607.02807] — Shepherd Agent with global context steers a population of Search Agents each in isolated local context; diagnoses and fixes premature convergence to one approach.
50. **Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing** [2602.04837] — the clearest bridge paper between recursive self-evolution and multi-agent coordination.

---

## Architectural Mapping to AI-EOS

1. **Theoretical Boundaries (Section A)**: Clarifies bounds on recursive self-improvement capability and guards against over-asserting system awareness (via #7's introspection thresholds), informing L3 Governance checks.
2. **Evolutionary Levers (Section B)**: Powers our L2 Harness Layer, transitioning from simple prompt tuning to robust skill and program optimization (using #26–28 & #32–34 lineages).
3. **Multi-Agent Coordination (Section C)**: Integrates parsimonious routing and Shepherd-Search separation (#41, #46, #49) to support the L4 Discovery Layer swarm without premature convergence.
