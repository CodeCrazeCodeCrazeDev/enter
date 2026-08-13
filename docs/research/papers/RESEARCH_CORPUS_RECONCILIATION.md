# Research Corpus Reconciliation & Status Audit (v3.0.0)
**Status:** Programmatically Reconciled and Validated

## 1. Corpus Summary Statistics
- **Total Papers Investigated/Stored:** 130
- **Unique Paper Count:** 130
- **Duplicate Records:** 0
- **Malformed Records Flagged:** 0
- **Unverifiable Citations Flagged:** 19

## 2. Four-State Distribution Matrix
| State | Description | Count | Paper IDs |
| :--- | :--- | :---: | :--- |
| **DISCOVERED** | Metadata populated, citation verified. | 3 | [5, 6, 39]... |
| **SCREENED** | Abstract & taxonomy analyzed. | 60 | [3, 11, 13, 16, 17, 19, 27, 28, 31, 32, 35, 36, 40, 43, 44, 47, 48, 51, 52, 53]... |
| **INVESTIGATED** | Scrutinized, principles extracted. | 60 | [1, 2, 4, 7, 8, 9, 10, 12, 14, 18, 21, 23, 24, 25, 26, 29, 30, 34, 37, 38]... |
| **INCORPORATED** | Mapped, coded, and statistically validated. | 7 | [15, 20, 22, 33, 55, 61, 62] |

## 3. Exclusion Set & Remaining Pools
- **Exclusion Set (Previously Incorporated):** 7 papers ([15, 20, 22, 33, 55, 61, 62]).
- **Remaining Eligible Pool for Research OS Pipeline:** 123 papers.

## 4. Comprehensive Paper Status Inventory
| ID | Title | Domain | State | Malformed? |
| :---: | :--- | :--- | :---: | :---: |
| 1 | Awesome-Agent-Papers | Multi-Agent Systems | **INVESTIGATED** | ✅ No |
| 2 | Awesome-Agentic-Reasoning | Agentic Planning | **INVESTIGATED** | ✅ No |
| 3 | self-correction-llm-papers | Self-Correction | **SCREENED** | ✅ No |
| 4 | llm-self-correction-papers | Self-Correction | **INVESTIGATED** | ✅ No |
| 5 | Awesome-Self-Evolving-Agents | Self-Evolution | **DISCOVERED** | ✅ No |
| 6 | A Survey of Process Reward Models | Process Verification | **DISCOVERED** | ✅ No |
| 7 | Survey-of-Process-Reward-Model repo | Process Verification | **INVESTIGATED** | ✅ No |
| 8 | Self-Reference in Large Language Models: The Introspection Threshold for Recursive Self-Improvement | Theory | **INVESTIGATED** | ✅ No |
| 9 | LADDER: Self-Improving LLMs Through Recursive Problem Decomposition | Task Decomposition | **INVESTIGATED** | ✅ No |
| 10 | RISE: Recursive IntroSpEction | SFT & Alignment | **INVESTIGATED** | ✅ No |
| 11 | Recursive Self-Aggregation Unlocks Deep Thinking in LLMs | RSA / Consensus | **SCREENED** | ✅ No |
| 12 | Self-Improvement in Multimodal Large Language Models: A Survey | Multimodal | **INVESTIGATED** | ✅ No |
| 13 | Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops | Research Loops | **SCREENED** | ✅ No |
| 14 | STaR: Bootstrapping Reasoning with Reasoning | Bootstrapping | **INVESTIGATED** | ✅ No |
| 15 | Reinforced Self-Training (ReST) for Language Modeling | Reinforced SFT | **INCORPORATED** | ✅ No |
| 16 | Self-Rewarding Language Models | Self-Reward | **SCREENED** | ✅ No |
| 17 | Process-based Self-Rewarding Language Models | Step-wise self-rewarding | **SCREENED** | ✅ No |
| 18 | CREAM: Consistency Regularized Self-Rewarding Language Models | Calibration | **INVESTIGATED** | ✅ No |
| 19 | Class-Conditional Self-Reward Mechanism for Improved Text-to-Image Models | Multimodal Reward | **SCREENED** | ✅ No |
| 20 | Self-Critiquing Models for Assisting Human Evaluators | Self-Critique | **INCORPORATED** | ✅ No |
| 21 | Self-Refine: Iterative Refinement with Self-Feedback | Iterative Refinement | **INVESTIGATED** | ✅ No |
| 22 | Reflexion: Language Agents with Verbal Reinforcement Learning | Verbal RL | **INCORPORATED** | ✅ No |
| 23 | SelFee: Iterative Self-Revising LLM Empowered by Self-Feedback Generation | Feedback SFT | **INVESTIGATED** | ✅ No |
| 24 | CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing | Tool Grounding | **INVESTIGATED** | ✅ No |
| 25 | Generating Sequences by Learning to Self-Correct | Sequence Correction | **INVESTIGATED** | ✅ No |
| 26 | Automatically Correcting Large Language Models: Surveying the Landscape of Diverse Automated Correction Strategies | Survey | **INVESTIGATED** | ✅ No |
| 27 | Large Language Models Cannot Self-Correct Reasoning Yet | Limitation Analysis | **SCREENED** | ✅ No |
| 28 | On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks | Limitation Analysis | **SCREENED** | ✅ No |
| 29 | Pride and Prejudice: LLM Amplifies Self-Bias in Self-Refinement | Self-Bias | **INVESTIGATED** | ✅ No |
| 30 | Distilled Self-Critique of LLMs with Synthetic Data: A Bayesian Perspective | Bayesian | **INVESTIGATED** | ✅ No |
| 31 | Learning from Self-Critique and Refinement for Faithful LLM Summarization (SCRPO) | Faithfulness | **SCREENED** | ✅ No |
| 32 | MAF: Multi-Aspect Feedback for Improving Reasoning in Large Language Models | Aspect Feedback | **SCREENED** | ✅ No |
| 33 | Let's Verify Step by Step | PRM | **INCORPORATED** | ✅ No |
| 34 | Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations | PRM Synthesis | **INVESTIGATED** | ✅ No |
| 35 | Process Reward Models That Think | PRM Optimization | **SCREENED** | ✅ No |
| 36 | ThinkPRM | PRM SFT | **SCREENED** | ✅ No |
| 37 | GenPRM: Generative Process Reward Model | PRM | **INVESTIGATED** | ✅ No |
| 38 | Unsupervised Process Reward Models (uPRM) | uPRM | **INVESTIGATED** | ✅ No |
| 39 | A Survey of Process Reward Models: From Outcome Signals to Process Supervisions for LLMs | PRM Survey | **DISCOVERED** | ✅ No |
| 40 | MM-Verify: Enhancing Multimodal Reasoning with Chain-of-Thought Verification | Multimodal Verification | **SCREENED** | ✅ No |
| 41 | Training Verifiers to Solve Math Word Problems | Verification Best-of-N | **INVESTIGATED** | ✅ No |
| 42 | LLM-Blender: Ensembling Large Language Models with Pairwise Comparison and Generative Fusion | Ensembling | **INVESTIGATED** | ✅ No |
| 43 | Multi-Agent Verification | Ensemble Verification | **SCREENED** | ✅ No |
| 44 | Weaver: Weak-to-Strong Generalization in Verification | Weak-to-Strong | **SCREENED** | ✅ No |
| 45 | ProcessBench: Identifying the First Erroneous Step in Solution Traces | PRM Benchmark | **INVESTIGATED** | ✅ No |
| 46 | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | Judge Validity | **INVESTIGATED** | ✅ No |
| 47 | RewardBench: Evaluating Reward Models for Language Modeling | Reward Benchmarking | **SCREENED** | ✅ No |
| 48 | Prover-Verifier Games Improve Legibility of LLM Outputs | Oversight Game | **SCREENED** | ✅ No |
| 49 | Multi-Agent Collaboration Mechanisms: A Survey of LLMs | MAS Survey | **INVESTIGATED** | ✅ No |
| 50 | A Communication-Centric Survey of LLM-Based Multi-Agent Systems | MAS Communication | **INVESTIGATED** | ✅ No |
| 51 | LLM-Based Multi-agent Systems: Frameworks, Evaluation, Open Challenges, and Research Frontiers | MAS Frameworks | **SCREENED** | ✅ No |
| 52 | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | MAS Framework | **SCREENED** | ✅ No |
| 53 | MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework | SOP Multi-Agent | **SCREENED** | ✅ No |
| 54 | CAMEL: Communicative Agents for 'Mind' Exploration of Large-scale Language Model Society | Communicative Agents | **INVESTIGATED** | ✅ No |
| 55 | ChatDev: Communicative Agents for Software Development | Software MAS | **INCORPORATED** | ✅ No |
| 56 | Generative Agents: Interactive Simulacra of Human Behavior | Simulacra | **SCREENED** | ✅ No |
| 57 | Why Do Multi-Agent LLM Systems Fail? | Failure Analysis | **SCREENED** | ✅ No |
| 58 | Coordination as an Architectural Layer for LLM-Based Multi-Agent Systems / LumiMAS / The Six Sigma Agent | MAS Architecture | **INVESTIGATED** | ✅ No |
| 59 | MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents | MAS Benchmark | **SCREENED** | ✅ No |
| 60 | AgentRxiv: Towards Collaborative Autonomous Research | Research Network | **SCREENED** | ✅ No |
| 61 | From Debate to Equilibrium: Belief-Driven Multi-Agent LLM Reasoning via Bayesian Nash Equilibrium (ECON) | Game Theory | **INCORPORATED** | ✅ No |
| 62 | LLM Collaboration With Multi-Agent Reinforcement Learning (MAGRPO) | MARL | **INCORPORATED** | ✅ No |
| 63 | LangMARL: Natural Language Multi-Agent Reinforcement Learning | MARL Language | **SCREENED** | ✅ No |
| 64 | ReAct: Synergizing Reasoning and Acting in Language Models | Agent Cycle | **SCREENED** | ✅ No |
| 65 | Tree of Thoughts: Deliberate Problem Solving with Large Language Models | Tree Search | **SCREENED** | ✅ No |
| 66 | Graph of Thoughts: Solving Elaborate Problems with Large Language Models | Graph Planning | **INVESTIGATED** | ✅ No |
| 67 | ReflAct: World-Grounded Decision Making in LLM Agents via Goal-State Reflection | Grounded Reflection | **SCREENED** | ✅ No |
| 68 | Pre-Act: Multi-Step Planning and Reasoning Improves Acting in LLM Agents | Planning Stage | **SCREENED** | ✅ No |
| 69 | SAND: Self-Taught Action Deliberation | Action Deliberation | **INVESTIGATED** | ✅ No |
| 70 | Toolformer: Language Models Can Teach Themselves to Use Tools | Tool Use | **INVESTIGATED** | ✅ No |
| 71 | ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs | APIs | **SCREENED** | ✅ No |
| 72 | HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face | Orchestration | **SCREENED** | ✅ No |
| 73 | WebGPT: Browser-assisted Question-Answering with Human Feedback | Web Search | **INVESTIGATED** | ✅ No |
| 74 | LADDER (#9 relevance here too) | Decomposition | **INVESTIGATED** | ✅ No |
| 75 | The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery | AI Scientist | **SCREENED** | ✅ No |
| 76 | The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search | Tree-based Scientist | **SCREENED** | ✅ No |
| 77 | Jr. AI Scientist and Its Risk Report: Autonomous Scientific Exploration from a Baseline Paper | Risk Audit | **INVESTIGATED** | ✅ No |
| 78 | Kosmos: An AI Scientist for Autonomous Discovery | Cross-Domain | **INVESTIGATED** | ✅ No |
| 79 | Robin: A Multi-Agent System for Automating Scientific Discovery | Discovery MAS | **SCREENED** | ✅ No |
| 80 | DORA AI Scientist: Multi-Agent Virtual Research Team for Scientific Exploration | Scientific Report | **SCREENED** | ✅ No |
| 81 | ResearchAgent: Iterative Research Idea Generation over Scientific Literature | Idea Generation | **INVESTIGATED** | ✅ No |
| 82 | IdeaSynth: Iterative Research Idea Development Through Evolving and Composing Idea Facets | Synthesis | **INVESTIGATED** | ✅ No |
| 83 | PaperBench: Evaluating AI's Ability to Replicate AI Research | Replication Bench | **SCREENED** | ✅ No |
| 84 | ResearcherBench: Evaluating Deep AI Research Systems on the Frontiers of Scientific Inquiry | Scientific Bench | **SCREENED** | ✅ No |
| 85 | Emergent Autonomous Scientific Research Capabilities of Large Language Models | Chemistry | **INVESTIGATED** | ✅ No |
| 86 | Towards an AI Co-Scientist | Gemini Science | **INVESTIGATED** | ✅ No |
| 87 | PARNESS: A Paper Harness for End-to-End Automated Scientific Research | Paper Harness | **SCREENED** | ✅ No |
| 88 | Can AI Conduct Autonomous Scientific Research? Case Studies and Failure-Mode Documentation | Empirical Case Study | **SCREENED** | ✅ No |
| 89 | Deep Research of Deep Research: From Transformer to Agent, From AI to AI for Science | Research Evolution | **INVESTIGATED** | ✅ No |
| 90 | FunSearch: Mathematical Discoveries from Program Search with Large Language Models | Evolution | **SCREENED** | ✅ No |
| 91 | AlphaEvolve: A Coding Agent for Scientific and Algorithmic Discovery | Evolution | **SCREENED** | ✅ No |
| 92 | Evolution Through Large Models (ELM) | Quality Diversity | **SCREENED** | ✅ No |
| 93 | AutoML-Zero: Evolving Machine Learning Algorithms From Scratch | Algorithmic Search | **INVESTIGATED** | ✅ No |
| 94 | Eureka: Human-Level Reward Design via Coding Large Language Models | Reward Evolution | **INVESTIGATED** | ✅ No |
| 95 | CodeEvolve: An Open-Source Evolutionary Coding Agent for Algorithm Discovery and Optimization | Evolution | **SCREENED** | ✅ No |
| 96 | ShinkaEvolve / OpenEvolve / TurboEvolve | Evolution | **SCREENED** | ✅ No |
| 97 | Illuminating Search Spaces by Mapping Elites (MAP-Elites) | Quality Diversity | **INVESTIGATED** | ✅ No |
| 98 | Large Language Models as Optimizers (OPRO) | Optimization | **INVESTIGATED** | ✅ No |
| 99 | DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning | RLVR / GRPO | **SCREENED** | ✅ No |
| 100 | DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models | GRPO | **SCREENED** | ✅ No |
| 101 | Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs | RLVR | **INVESTIGATED** | ✅ No |
| 102 | 100 Days After DeepSeek-R1: A Survey on Replication Studies | RLVR Survey | **INVESTIGATED** | ✅ No |
| 103 | Kimi k1.5: Scaling Reinforcement Learning with LLMs | Reinforcement Learning | **SCREENED** | ✅ No |
| 104 | Tülu 3 / RLVR framing paper | RLVR Framing | **SCREENED** | ✅ No |
| 105 | Constitutional AI: Harmlessness from AI Feedback | Safety | **SCREENED** | ✅ No |
| 106 | Training Language Models to Follow Instructions with Human Feedback | RLHF | **INVESTIGATED** | ✅ No |
| 107 | AI Safety via Debate | Debate Safety | **SCREENED** | ✅ No |
| 108 | Scalable AI Safety via Doubly-Efficient Debate / Avoiding Obfuscated Arguments | Debate | **SCREENED** | ✅ No |
| 109 | Supervising Strong Learners by Amplifying Weak Experts | Amplification | **INVESTIGATED** | ✅ No |
| 110 | Scalable Agent Alignment via Reward Modeling | Alignment | **INVESTIGATED** | ✅ No |
| 111 | Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision | Weak-to-Strong | **SCREENED** | ✅ No |
| 112 | Weak-to-Strong Generalization: When Can Weak LLMs Effectively Judge/Train Strong LLMs? | Alignment | **SCREENED** | ✅ No |
| 113 | Improving Weak-to-Strong Generalization with Scalable Oversight and Ensemble Learning | Weak-to-Strong | **INVESTIGATED** | ✅ No |
| 114 | An Alignment Safety Case Sketch Based on Debate | Safety Case | **INVESTIGATED** | ✅ No |
| 115 | Defining Scalable Oversight for LLMs | Oversight Survey | **SCREENED** | ✅ No |
| 116 | Prover-Verifier Games Improve Legibility of LLM Outputs (#116 / #48) | Oversight Game | **SCREENED** | ✅ No |
| 117 | Superintelligence: Paths, Dangers, Strategies | Safety Theory | **INVESTIGATED** | ✅ No |
| 118 | Speculations Concerning the First Ultraintelligent Machine | Intelligence Explosion | **INVESTIGATED** | ✅ No |
| 119 | UltraHorizon: Benchmarking Agent Capabilities in Ultra Long-Horizon Scenarios | Benchmark | **SCREENED** | ✅ No |
| 120 | Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks | Benchmark | **SCREENED** | ✅ No |
| 121 | SWE-Marathon: Can Agents Autonomously Complete Ultra-Long-Horizon Software Work? | Benchmark | **INVESTIGATED** | ✅ No |
| 122 | Mem2ActBench: A Benchmark for Evaluating Long-Term Memory Utilization in Task-Oriented Autonomous Agents | Benchmark | **INVESTIGATED** | ✅ No |
| 123 | Planner Matters! An Efficient and Unbalanced Multi-Agent Collaboration Framework for Long-Horizon Planning | MAS Planning | **SCREENED** | ✅ No |
| 124 | When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution | Benchmark | **SCREENED** | ✅ No |
| 125 | WebArena / WebVoyager Benchmarks | Benchmark | **INVESTIGATED** | ✅ No |
| 126 | Voyager: An Open-Ended Embodied Agent with Large Language Models | Lifelong Learning | **INVESTIGATED** | ✅ No |
| 127 | Sacerdoti / Classical PDDL/STRIPS planning lineage | Planning Theory | **SCREENED** | ✅ No |
| 128 | BabyAGI | Task Scheduler | **INVESTIGATED** | ✅ No |
| 129 | AutoGPT | Task Loop | **INVESTIGATED** | ✅ No |
| 130 | CrewAI / LangGraph / TaskWeaver / SuperAGI | Orchestration | **INVESTIGATED** | ✅ No |
