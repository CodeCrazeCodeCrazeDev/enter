# AI-EOS Typed Dependency Graph

This document tracks prerequisite relationships using typed dependency edges (`extends`, `complements`, `prerequisite`).

```mermaid
graph TD
    classDef foundational fill:#f9f,stroke:#333,stroke-width:2px;
    classDef enabling fill:#bbf,stroke:#333,stroke-width:2px;
    classDef optional fill:#dfd,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5;
    subgraph L1 [L1 (Recovery Layer)]
        P16[#16 Self-Rewarding Language M]
        P17[#17 Process-based Self-Reward]
        P18[#18 CREAM: Consistency Regula]
        P19[#19 Class-Conditional Self-Re]
        P20[#20 Self-Critiquing Models fo]
        P21[#21 Self-Refine: Iterative Re]
        P22[#22 Reflexion: Language Agent]
        P23[#23 SelFee: Iterative Self-Re]
        P24[#24 CRITIC: Large Language Mo]
        P25[#25 Generating Sequences by L]
        P26[#26 Automatically Correcting ]
        P27[#27 Large Language Models Can]
        P28[#28 On the Self-Verification ]
        P29[#29 Pride and Prejudice: LLM ]
        P30[#30 Distilled Self-Critique o]
        P31[#31 Learning from Self-Critiq]
        P32[#32 MAF: Multi-Aspect Feedbac]
        P119[#119 UltraHorizon: Benchmarkin]
        P120[#120 Long-Horizon-Terminal-Ben]
        P121[#121 SWE-Marathon: Can Agents ]
        P122[#122 Mem2ActBench: A Benchmark]
        P123[#123 Planner Matters! An Effic]
        P124[#124 When Robots Do the Chores]
        P125[#125 WebArena / WebVoyager Ben]
        P126[#126 Voyager: An Open-Ended Em]
        P127[#127 Sacerdoti / Classical PDD]
    end
    subgraph L2 [L2 (Harness Layer)]
        P1[#1 Awesome-Agent-Papers]
        P2[#2 Awesome-Agentic-Reasoning]
        P3[#3 self-correction-llm-paper]
        P4[#4 llm-self-correction-paper]
        P5[#5 Awesome-Self-Evolving-Age]
        P6[#6 A Survey of Process Rewar]
        P7[#7 Survey-of-Process-Reward-]
        P49[#49 Multi-Agent Collaboration]
        P50[#50 A Communication-Centric S]
        P51[#51 LLM-Based Multi-agent Sys]
        P52[#52 AutoGen: Enabling Next-Ge]
        P53[#53 MetaGPT: Meta Programming]
        P54[#54 CAMEL: Communicative Agen]
        P55[#55 ChatDev: Communicative Ag]
        P56[#56 Generative Agents: Intera]
        P57[#57 Why Do Multi-Agent LLM Sy]
        P58[#58 Coordination as an Archit]
        P59[#59 MultiAgentBench: Evaluati]
        P60[#60 AgentRxiv: Towards Collab]
        P61[#61 From Debate to Equilibriu]
        P62[#62 LLM Collaboration With Mu]
        P63[#63 LangMARL: Natural Languag]
        P64[#64 ReAct: Synergizing Reason]
        P65[#65 Tree of Thoughts: Deliber]
        P66[#66 Graph of Thoughts: Solvin]
        P67[#67 ReflAct: World-Grounded D]
        P68[#68 Pre-Act: Multi-Step Plann]
        P69[#69 SAND: Self-Taught Action ]
        P70[#70 Toolformer: Language Mode]
        P71[#71 ToolLLM: Facilitating Lar]
        P72[#72 HuggingGPT: Solving AI Ta]
        P73[#73 WebGPT: Browser-assisted ]
        P74[#74 LADDER (#9 relevance here]
        P128[#128 BabyAGI]
        P129[#129 AutoGPT]
        P130[#130 CrewAI / LangGraph / Task]
        P131[#131 Active Inference for Cogn]
        P132[#132 do-calculus SCMs for Caus]
        P133[#133 Modeling Ebbinghaus Memor]
        P134[#134 Multi-Mind Sycophancy Mit]
        P135[#135 Evaluating Autonomous Age]
        P136[#136 Step-Wise Process Verific]
        P137[#137 LADDER: Hierarchical Task]
        P138[#138 Large Language Models as ]
        P139[#139 Active Inference Expected]
        P140[#140 Deflated Sharpe Ratio and]
        P141[#141 Verifiable Rewards for Re]
        P142[#142 Sycophancy Detection and ]
        P143[#143 Structured Causal Models ]
        P144[#144 Ebbinghaus Memory Decay F]
        P145[#145 Step-by-Step Mathematical]
        P146[#146 Expected Free Energy and ]
        P147[#147 Generalization Boundaries]
        P148[#148 Recursive Self-Aggregatio]
        P149[#149 Constitutional AI Safety ]
        P150[#150 Scalable Oversight in Rei]
        P151[#151 GRPO: Group Relative Poli]
        P152[#152 Walk-Forward Cross-Valida]
        P153[#153 Genetic Program Synthesis]
        P154[#154 Expected Free Energy Appr]
        P155[#155 Multi-Mind Multi-Agent Or]
        P156[#156 Hendrycks Safety Benchmar]
        P157[#157 Bayesian Belief Propagati]
        P158[#158 Step-Wise Policy Training]
        P159[#159 LADDER Decomposition for ]
        P160[#160 Genetic Optimization of P]
        P161[#161 Expected Free Energy acti]
        P162[#162 Deflated Sharpe Ratio for]
        P163[#163 DeepSeek-R1 Replication: ]
        P164[#164 Constitutional Guidelines]
        P165[#165 Prover-Verifier Games for]
        P166[#166 Walk-Forward Split and No]
        P167[#167 Evolutionary Search over ]
        P168[#168 Variational Free Energy m]
        P169[#169 Multi-Agent SOP Integrati]
        P170[#170 Safety Case Formulation f]
        P171[#171 Ebbinghaus Forgetting Cur]
        P172[#172 Step-by-Step Rationale Bo]
        P173[#173 Strategic Backtracking in]
        P174[#174 Large Language Models as ]
        P175[#175 Epistemic Exploration vs ]
        P176[#176 Statistical Multi-Testing]
        P177[#177 Group Relative Policy Opt]
        P178[#178 Debate-Centric Alignment:]
        P179[#179 Constitutional AI for Aut]
        P180[#180 Walk-Forward Optimization]
        P181[#181 Self-Referential Code Rew]
        P182[#182 Expected Free Energy Acti]
        P183[#183 Standard Operating Proced]
        P184[#184 Hendrycks Safety Benchmar]
        P185[#185 Experience Memory Graph: ]
        P186[#186 Math Shepherd: Automated ]
        P187[#187 Strategic Hierarchical Ta]
        P188[#188 Thompson Sampling and Mul]
        P189[#189 Active Inference and Expe]
        P190[#190 DSR and Whites Reality Ch]
        P191[#191 DeepSeekMath: Pushing the]
        P192[#192 Constitutional Guidelines]
        P193[#193 Prover-Verifier Games for]
        P194[#194 Walk-Forward Cross-Valida]
        P195[#195 Genetic Programming and P]
        P196[#196 Active Inference and Vari]
        P197[#197 Multi-Agent SOP Integrati]
        P198[#198 Safety Case Formulation b]
        P199[#199 Ebbinghaus Memory Decay a]
        P200[#200 Step-by-Step Process Veri]
    end
    subgraph L3 [L3 (Governance Layer)]
        P33[#33 Lets Verify Step by Step]
        P34[#34 Math-Shepherd: Verify and]
        P35[#35 Process Reward Models Tha]
        P36[#36 ThinkPRM]
        P37[#37 GenPRM: Generative Proces]
        P38[#38 Unsupervised Process Rewa]
        P39[#39 A Survey of Process Rewar]
        P40[#40 MM-Verify: Enhancing Mult]
        P41[#41 Training Verifiers to Sol]
        P42[#42 LLM-Blender: Ensembling L]
        P43[#43 Multi-Agent Verification]
        P44[#44 Weaver: Weak-to-Strong Ge]
        P45[#45 ProcessBench: Identifying]
        P46[#46 Judging LLM-as-a-Judge wi]
        P47[#47 RewardBench: Evaluating R]
        P48[#48 Prover-Verifier Games Imp]
        P105[#105 Constitutional AI: Harmle]
        P106[#106 Training Language Models ]
        P107[#107 AI Safety via Debate]
        P108[#108 Scalable AI Safety via Do]
        P109[#109 Supervising Strong Learne]
        P110[#110 Scalable Agent Alignment ]
        P111[#111 Weak-to-Strong Generaliza]
        P112[#112 Weak-to-Strong Generaliza]
        P113[#113 Improving Weak-to-Strong ]
        P114[#114 An Alignment Safety Case ]
        P115[#115 Defining Scalable Oversig]
        P116[#116 Prover-Verifier Games Imp]
        P117[#117 Superintelligence: Paths,]
        P118[#118 Speculations Concerning t]
    end
    subgraph L4 [L4 (Discovery Layer)]
        P8[#8 Self-Reference in Large L]
        P9[#9 LADDER: Self-Improving LL]
        P10[#10 RISE: Recursive IntroSpEc]
        P11[#11 Recursive Self-Aggregatio]
        P12[#12 Self-Improvement in Multi]
        P13[#13 Recursive Self-Improvemen]
        P14[#14 STaR: Bootstrapping Reaso]
        P15[#15 Reinforced Self-Training ]
        P75[#75 The AI Scientist: Towards]
        P76[#76 The AI Scientist-v2: Work]
        P77[#77 Jr. AI Scientist and Its ]
        P78[#78 Kosmos: An AI Scientist f]
        P79[#79 Robin: A Multi-Agent Syst]
        P80[#80 DORA AI Scientist: Multi-]
        P81[#81 ResearchAgent: Iterative ]
        P82[#82 IdeaSynth: Iterative Rese]
        P83[#83 PaperBench: Evaluating AI]
        P84[#84 ResearcherBench: Evaluati]
        P85[#85 Emergent Autonomous Scien]
        P86[#86 Towards an AI Co-Scientis]
        P87[#87 PARNESS: A Paper Harness ]
        P88[#88 Can AI Conduct Autonomous]
        P89[#89 Deep Research of Deep Res]
        P90[#90 FunSearch: Mathematical D]
        P91[#91 AlphaEvolve: A Coding Age]
        P92[#92 Evolution Through Large M]
        P93[#93 AutoML-Zero: Evolving Mac]
        P94[#94 Eureka: Human-Level Rewar]
        P95[#95 CodeEvolve: An Open-Sourc]
        P96[#96 ShinkaEvolve / OpenEvolve]
        P97[#97 Illuminating Search Space]
        P98[#98 Large Language Models as ]
        P99[#99 DeepSeek-R1: Incentivizin]
        P100[#100 DeepSeekMath: Pushing the]
        P101[#101 Reinforcement Learning wi]
        P102[#102 100 Days After DeepSeek-R]
        P103[#103 Kimi k1.5: Scaling Reinfo]
        P104[#104 Tülu 3 / RLVR framing pap]
    end
    P3 -->|prerequisite| P4
    P1 -->|prerequisite| P5
    P2 -->|prerequisite| P6
    P6 -->|prerequisite| P7
    P5 -->|prerequisite| P8
    P8 -->|prerequisite| P9
    P8 -->|prerequisite| P10
    P2 -->|prerequisite| P11
    P6 -->|prerequisite| P12
    P8 -->|prerequisite| P13
    P3 -->|prerequisite| P14
    P14 -->|prerequisite| P15
    P14 -->|prerequisite| P16
    P16 -->|prerequisite| P17
    P21 -->|prerequisite| P18
    P21 -->|prerequisite| P19
    P21 -->|prerequisite| P20
    P3 -->|prerequisite| P21
    P21 -->|prerequisite| P22
    P21 -->|prerequisite| P23
    P21 -->|prerequisite| P24
    P21 -->|prerequisite| P25
    P21 -->|prerequisite| P26
    P21 -->|prerequisite| P27
    P21 -->|prerequisite| P28
    P21 -->|prerequisite| P29
    P21 -->|prerequisite| P30
    P21 -->|prerequisite| P31
    P21 -->|prerequisite| P32
    P6 -->|prerequisite| P33
    P33 -->|prerequisite| P34
    P33 -->|prerequisite| P35
    P33 -->|prerequisite| P36
    P33 -->|prerequisite| P37
    P33 -->|prerequisite| P38
    P33 -->|prerequisite| P39
    P33 -->|prerequisite| P40
    P33 -->|prerequisite| P41
    P33 -->|prerequisite| P42
    P33 -->|prerequisite| P43
    P33 -->|prerequisite| P44
    P33 -->|prerequisite| P45
    P33 -->|prerequisite| P46
    P33 -->|prerequisite| P47
    P33 -->|prerequisite| P48
    P53 -->|prerequisite| P49
    P53 -->|prerequisite| P50
    P53 -->|prerequisite| P51
    P53 -->|prerequisite| P52
    P1 -->|prerequisite| P53
    P53 -->|prerequisite| P54
    P53 -->|prerequisite| P55
    P53 -->|prerequisite| P56
    P22 -->|prerequisite| P57
    P53 -->|prerequisite| P58
    P53 -->|prerequisite| P59
    P53 -->|prerequisite| P60
    P53 -->|prerequisite| P61
    P53 -->|prerequisite| P62
    P53 -->|prerequisite| P63
    P2 -->|prerequisite| P64
    P64 -->|prerequisite| P65
    P64 -->|prerequisite| P66
    P64 -->|prerequisite| P67
    P64 -->|prerequisite| P68
    P64 -->|prerequisite| P69
    P64 -->|prerequisite| P70
    P64 -->|prerequisite| P71
    P64 -->|prerequisite| P72
    P64 -->|prerequisite| P73
    P64 -->|prerequisite| P74
    P75 -->|prerequisite| P75
    P75 -->|prerequisite| P76
    P75 -->|prerequisite| P77
    P75 -->|prerequisite| P78
    P75 -->|prerequisite| P79
    P75 -->|prerequisite| P80
    P75 -->|prerequisite| P81
    P75 -->|prerequisite| P82
    P75 -->|prerequisite| P83
    P75 -->|prerequisite| P84
    P75 -->|prerequisite| P85
    P75 -->|prerequisite| P86
    P75 -->|prerequisite| P87
    P75 -->|prerequisite| P88
    P75 -->|prerequisite| P89
    P33 -->|prerequisite| P90
    P90 -->|prerequisite| P91
    P90 -->|prerequisite| P92
    P90 -->|prerequisite| P93
    P90 -->|prerequisite| P94
    P90 -->|prerequisite| P95
    P90 -->|prerequisite| P96
    P90 -->|prerequisite| P97
    P90 -->|prerequisite| P98
    P33 -->|prerequisite| P99
    P99 -->|prerequisite| P100
    P99 -->|prerequisite| P101
    P99 -->|prerequisite| P102
    P99 -->|prerequisite| P103
    P99 -->|prerequisite| P104
    P1 -->|prerequisite| P105
    P105 -->|prerequisite| P106
    P105 -->|prerequisite| P107
    P105 -->|prerequisite| P108
    P105 -->|prerequisite| P109
    P105 -->|prerequisite| P110
    P105 -->|prerequisite| P111
    P105 -->|prerequisite| P112
    P105 -->|prerequisite| P113
    P105 -->|prerequisite| P114
    P105 -->|prerequisite| P115
    P105 -->|prerequisite| P116
    P105 -->|prerequisite| P117
    P105 -->|prerequisite| P118
    P125 -->|prerequisite| P119
    P125 -->|prerequisite| P120
    P125 -->|prerequisite| P121
    P125 -->|prerequisite| P122
    P125 -->|prerequisite| P123
    P125 -->|prerequisite| P124
    P125 -->|prerequisite| P125
    P125 -->|prerequisite| P126
    P125 -->|prerequisite| P127
    P128 -->|prerequisite| P129
    P128 -->|prerequisite| P130
    P128 -->|prerequisite| P131
    P128 -->|prerequisite| P132
    P128 -->|prerequisite| P133
    P128 -->|prerequisite| P134
    P128 -->|prerequisite| P135
    P128 -->|prerequisite| P136
    P128 -->|prerequisite| P137
    P128 -->|prerequisite| P138
    P128 -->|prerequisite| P139
    P128 -->|prerequisite| P140
    P128 -->|prerequisite| P141
    P128 -->|prerequisite| P142
    P128 -->|prerequisite| P143
    P128 -->|prerequisite| P144
    P128 -->|prerequisite| P145
    P128 -->|prerequisite| P146
    P128 -->|prerequisite| P147
    P128 -->|prerequisite| P148
    P128 -->|prerequisite| P149
    P128 -->|prerequisite| P150
    P128 -->|prerequisite| P151
    P128 -->|prerequisite| P152
    P128 -->|prerequisite| P153
    P128 -->|prerequisite| P154
    P128 -->|prerequisite| P155
    P128 -->|prerequisite| P156
    P128 -->|prerequisite| P157
    P128 -->|prerequisite| P158
    P128 -->|prerequisite| P159
    P128 -->|prerequisite| P160
    P128 -->|prerequisite| P161
    P128 -->|prerequisite| P162
    P128 -->|prerequisite| P163
    P128 -->|prerequisite| P164
    P128 -->|prerequisite| P165
    P128 -->|prerequisite| P166
    P128 -->|prerequisite| P167
    P128 -->|prerequisite| P168
    P128 -->|prerequisite| P169
    P128 -->|prerequisite| P170
    P128 -->|prerequisite| P171
    P128 -->|prerequisite| P172
    P128 -->|prerequisite| P173
    P128 -->|prerequisite| P174
    P128 -->|prerequisite| P175
    P128 -->|prerequisite| P176
    P128 -->|prerequisite| P177
    P128 -->|prerequisite| P178
    P128 -->|prerequisite| P179
    P128 -->|prerequisite| P180
    P128 -->|prerequisite| P181
    P128 -->|prerequisite| P182
    P128 -->|prerequisite| P183
    P128 -->|prerequisite| P184
    P128 -->|prerequisite| P185
    P128 -->|prerequisite| P186
    P128 -->|prerequisite| P187
    P128 -->|prerequisite| P188
    P128 -->|prerequisite| P189
    P128 -->|prerequisite| P190
    P128 -->|prerequisite| P191
    P128 -->|prerequisite| P192
    P128 -->|prerequisite| P193
    P128 -->|prerequisite| P194
    P128 -->|prerequisite| P195
    P128 -->|prerequisite| P196
    P128 -->|prerequisite| P197
    P128 -->|prerequisite| P198
    P128 -->|prerequisite| P199
    P128 -->|prerequisite| P200
```


## Detailed Relationship Descriptions

### #2 Awesome-Agentic-Reasoning
- **Relationship Type:** `complements` target: `Paper #1`

### #3 self-correction-llm-papers
- **Relationship Type:** `complements` target: `Paper #1`

### #4 llm-self-correction-papers
- **Relationship Type:** `prerequisite` target: `Paper #3`

### #5 Awesome-Self-Evolving-Agents
- **Relationship Type:** `prerequisite` target: `Paper #1`

### #6 A Survey of Process Reward Models
- **Relationship Type:** `prerequisite` target: `Paper #2`

### #7 Survey-of-Process-Reward-Model repo
- **Relationship Type:** `prerequisite` target: `Paper #6`

### #8 Self-Reference in Large Language Models: The Introspection Threshold for Recursive Self-Improvement
- **Relationship Type:** `prerequisite` target: `Paper #5`

### #9 LADDER: Self-Improving LLMs Through Recursive Problem Decomposition
- **Relationship Type:** `prerequisite` target: `Paper #8`

### #10 RISE: Recursive IntroSpEction
- **Relationship Type:** `prerequisite` target: `Paper #8`

### #11 Recursive Self-Aggregation Unlocks Deep Thinking in LLMs
- **Relationship Type:** `prerequisite` target: `Paper #2`

### #12 Self-Improvement in Multimodal Large Language Models: A Survey
- **Relationship Type:** `prerequisite` target: `Paper #6`

### #13 Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops
- **Relationship Type:** `prerequisite` target: `Paper #8`

### #14 STaR: Bootstrapping Reasoning with Reasoning
- **Relationship Type:** `prerequisite` target: `Paper #3`

### #15 Reinforced Self-Training (ReST) for Language Modeling
- **Relationship Type:** `prerequisite` target: `Paper #14`

### #16 Self-Rewarding Language Models
- **Relationship Type:** `prerequisite` target: `Paper #14`

### #17 Process-based Self-Rewarding Language Models
- **Relationship Type:** `prerequisite` target: `Paper #16`

### #18 CREAM: Consistency Regularized Self-Rewarding Language Models
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #19 Class-Conditional Self-Reward Mechanism for Improved Text-to-Image Models
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #20 Self-Critiquing Models for Assisting Human Evaluators
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #21 Self-Refine: Iterative Refinement with Self-Feedback
- **Relationship Type:** `prerequisite` target: `Paper #3`

### #22 Reflexion: Language Agents with Verbal Reinforcement Learning
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #23 SelFee: Iterative Self-Revising LLM Empowered by Self-Feedback Generation
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #24 CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #25 Generating Sequences by Learning to Self-Correct
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #26 Automatically Correcting Large Language Models: Surveying the Landscape of Diverse Automated Correction Strategies
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #27 Large Language Models Cannot Self-Correct Reasoning Yet
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #28 On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #29 Pride and Prejudice: LLM Amplifies Self-Bias in Self-Refinement
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #30 Distilled Self-Critique of LLMs with Synthetic Data: A Bayesian Perspective
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #31 Learning from Self-Critique and Refinement for Faithful LLM Summarization (SCRPO)
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #32 MAF: Multi-Aspect Feedback for Improving Reasoning in Large Language Models
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #33 Let's Verify Step by Step
- **Relationship Type:** `prerequisite` target: `Paper #6`

### #34 Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #35 Process Reward Models That Think
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #36 ThinkPRM
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #37 GenPRM: Generative Process Reward Model
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #38 Unsupervised Process Reward Models (uPRM)
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #39 A Survey of Process Reward Models: From Outcome Signals to Process Supervisions for LLMs
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #40 MM-Verify: Enhancing Multimodal Reasoning with Chain-of-Thought Verification
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #41 Training Verifiers to Solve Math Word Problems
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #42 LLM-Blender: Ensembling Large Language Models with Pairwise Comparison and Generative Fusion
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #43 Multi-Agent Verification
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #44 Weaver: Weak-to-Strong Generalization in Verification
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #45 ProcessBench: Identifying the First Erroneous Step in Solution Traces
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #46 Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #47 RewardBench: Evaluating Reward Models for Language Modeling
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #48 Prover-Verifier Games Improve Legibility of LLM Outputs
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #49 Multi-Agent Collaboration Mechanisms: A Survey of LLMs
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #50 A Communication-Centric Survey of LLM-Based Multi-Agent Systems
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #51 LLM-Based Multi-agent Systems: Frameworks, Evaluation, Open Challenges, and Research Frontiers
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #52 AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #53 MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework
- **Relationship Type:** `prerequisite` target: `Paper #1`

### #54 CAMEL: Communicative Agents for 'Mind' Exploration of Large-scale Language Model Society
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #55 ChatDev: Communicative Agents for Software Development
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #56 Generative Agents: Interactive Simulacra of Human Behavior
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #57 Why Do Multi-Agent LLM Systems Fail?
- **Relationship Type:** `prerequisite` target: `Paper #22`

### #58 Coordination as an Architectural Layer for LLM-Based Multi-Agent Systems / LumiMAS / The Six Sigma Agent
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #59 MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #60 AgentRxiv: Towards Collaborative Autonomous Research
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #61 From Debate to Equilibrium: Belief-Driven Multi-Agent LLM Reasoning via Bayesian Nash Equilibrium (ECON)
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #62 LLM Collaboration With Multi-Agent Reinforcement Learning (MAGRPO)
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #63 LangMARL: Natural Language Multi-Agent Reinforcement Learning
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #64 ReAct: Synergizing Reasoning and Acting in Language Models
- **Relationship Type:** `prerequisite` target: `Paper #2`

### #65 Tree of Thoughts: Deliberate Problem Solving with Large Language Models
- **Relationship Type:** `prerequisite` target: `Paper #64`

### #66 Graph of Thoughts: Solving Elaborate Problems with Large Language Models
- **Relationship Type:** `prerequisite` target: `Paper #64`

### #67 ReflAct: World-Grounded Decision Making in LLM Agents via Goal-State Reflection
- **Relationship Type:** `prerequisite` target: `Paper #64`

### #68 Pre-Act: Multi-Step Planning and Reasoning Improves Acting in LLM Agents
- **Relationship Type:** `prerequisite` target: `Paper #64`

### #69 SAND: Self-Taught Action Deliberation
- **Relationship Type:** `prerequisite` target: `Paper #64`

### #70 Toolformer: Language Models Can Teach Themselves to Use Tools
- **Relationship Type:** `prerequisite` target: `Paper #64`

### #71 ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs
- **Relationship Type:** `prerequisite` target: `Paper #64`

### #72 HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face
- **Relationship Type:** `prerequisite` target: `Paper #64`

### #73 WebGPT: Browser-assisted Question-Answering with Human Feedback
- **Relationship Type:** `prerequisite` target: `Paper #64`

### #74 LADDER (#9 relevance here too)
- **Relationship Type:** `prerequisite` target: `Paper #64`

### #75 The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #76 The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #77 Jr. AI Scientist and Its Risk Report: Autonomous Scientific Exploration from a Baseline Paper
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #78 Kosmos: An AI Scientist for Autonomous Discovery
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #79 Robin: A Multi-Agent System for Automating Scientific Discovery
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #80 DORA AI Scientist: Multi-Agent Virtual Research Team for Scientific Exploration
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #81 ResearchAgent: Iterative Research Idea Generation over Scientific Literature
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #82 IdeaSynth: Iterative Research Idea Development Through Evolving and Composing Idea Facets
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #83 PaperBench: Evaluating AI's Ability to Replicate AI Research
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #84 ResearcherBench: Evaluating Deep AI Research Systems on the Frontiers of Scientific Inquiry
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #85 Emergent Autonomous Scientific Research Capabilities of Large Language Models
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #86 Towards an AI Co-Scientist
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #87 PARNESS: A Paper Harness for End-to-End Automated Scientific Research
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #88 Can AI Conduct Autonomous Scientific Research? Case Studies and Failure-Mode Documentation
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #89 Deep Research of Deep Research: From Transformer to Agent, From AI to AI for Science
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #90 FunSearch: Mathematical Discoveries from Program Search with Large Language Models
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #91 AlphaEvolve: A Coding Agent for Scientific and Algorithmic Discovery
- **Relationship Type:** `prerequisite` target: `Paper #90`

### #92 Evolution Through Large Models (ELM)
- **Relationship Type:** `prerequisite` target: `Paper #90`

### #93 AutoML-Zero: Evolving Machine Learning Algorithms From Scratch
- **Relationship Type:** `prerequisite` target: `Paper #90`

### #94 Eureka: Human-Level Reward Design via Coding Large Language Models
- **Relationship Type:** `prerequisite` target: `Paper #90`

### #95 CodeEvolve: An Open-Source Evolutionary Coding Agent for Algorithm Discovery and Optimization
- **Relationship Type:** `prerequisite` target: `Paper #90`

### #96 ShinkaEvolve / OpenEvolve / TurboEvolve
- **Relationship Type:** `prerequisite` target: `Paper #90`

### #97 Illuminating Search Spaces by Mapping Elites (MAP-Elites)
- **Relationship Type:** `prerequisite` target: `Paper #90`

### #98 Large Language Models as Optimizers (OPRO)
- **Relationship Type:** `prerequisite` target: `Paper #90`

### #99 DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #100 DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models
- **Relationship Type:** `prerequisite` target: `Paper #99`

### #101 Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs
- **Relationship Type:** `prerequisite` target: `Paper #99`

### #102 100 Days After DeepSeek-R1: A Survey on Replication Studies
- **Relationship Type:** `prerequisite` target: `Paper #99`

### #103 Kimi k1.5: Scaling Reinforcement Learning with LLMs
- **Relationship Type:** `prerequisite` target: `Paper #99`

### #104 Tülu 3 / RLVR framing paper
- **Relationship Type:** `prerequisite` target: `Paper #99`

### #105 Constitutional AI: Harmlessness from AI Feedback
- **Relationship Type:** `prerequisite` target: `Paper #1`

### #106 Training Language Models to Follow Instructions with Human Feedback
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #107 AI Safety via Debate
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #108 Scalable AI Safety via Doubly-Efficient Debate / Avoiding Obfuscated Arguments
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #109 Supervising Strong Learners by Amplifying Weak Experts
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #110 Scalable Agent Alignment via Reward Modeling
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #111 Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #112 Weak-to-Strong Generalization: When Can Weak LLMs Effectively Judge/Train Strong LLMs?
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #113 Improving Weak-to-Strong Generalization with Scalable Oversight and Ensemble Learning
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #114 An Alignment Safety Case Sketch Based on Debate
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #115 Defining Scalable Oversight for LLMs
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #116 Prover-Verifier Games Improve Legibility of LLM Outputs (#116 / #48)
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #117 Superintelligence: Paths, Dangers, Strategies
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #118 Speculations Concerning the First Ultraintelligent Machine
- **Relationship Type:** `prerequisite` target: `Paper #105`

### #119 UltraHorizon: Benchmarking Agent Capabilities in Ultra Long-Horizon Scenarios
- **Relationship Type:** `prerequisite` target: `Paper #125`

### #120 Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks
- **Relationship Type:** `prerequisite` target: `Paper #125`

### #121 SWE-Marathon: Can Agents Autonomously Complete Ultra-Long-Horizon Software Work?
- **Relationship Type:** `prerequisite` target: `Paper #125`

### #122 Mem2ActBench: A Benchmark for Evaluating Long-Term Memory Utilization in Task-Oriented Autonomous Agents
- **Relationship Type:** `prerequisite` target: `Paper #125`

### #123 Planner Matters! An Efficient and Unbalanced Multi-Agent Collaboration Framework for Long-Horizon Planning
- **Relationship Type:** `prerequisite` target: `Paper #125`

### #124 When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution
- **Relationship Type:** `prerequisite` target: `Paper #125`

### #125 WebArena / WebVoyager Benchmarks
- **Relationship Type:** `prerequisite` target: `Paper #125`

### #126 Voyager: An Open-Ended Embodied Agent with Large Language Models
- **Relationship Type:** `prerequisite` target: `Paper #125`

### #127 Sacerdoti / Classical PDDL/STRIPS planning lineage
- **Relationship Type:** `prerequisite` target: `Paper #125`

### #129 AutoGPT
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #130 CrewAI / LangGraph / TaskWeaver / SuperAGI
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #131 Active Inference for Cognitive Operating Systems via Variational Free Energy Minimization
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #132 do-calculus SCMs for Causal Interventions in Autonomous Multi-Agent Workflows
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #133 Modeling Ebbinghaus Memory Decay in SQLite-backed Semantic Memory Databases
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #134 Multi-Mind Sycophancy Mitigation via Recursive Self-Aggregation Consensus
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #135 Evaluating Autonomous Agent Robustness with Hendrycks Safety Audits
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #136 Step-Wise Process Verification and Math Shepherd PRM in Complex Planning Tasks
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #137 LADDER: Hierarchical Task Decomposition and Tree of Thoughts Search Backtracking
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #138 Large Language Models as Optimizers: Evolutionary Code and Prompt Generation
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #139 Active Inference Expected Free Energy Routing inside Multi-Agent Collaboration Networks
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #140 Deflated Sharpe Ratio and White's Reality Check for Walk-Forward Validation
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #141 Verifiable Rewards for Reinforcement Learning in Agentic Code Synthesis
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #142 Sycophancy Detection and Mitigation via Multi-Agent Constitutional Debate
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #143 Structured Causal Models for Multi-Agent Failure Mode Localization and Repair
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #144 Ebbinghaus Memory Decay Functions for Forgetting and Re-consolidating Agent Experiences
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #145 Step-by-Step Mathematical Verifiers with Generative Reward Modeling
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #146 Expected Free Energy and Pragmatic Utility Balancing in Portfolio Optimization
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #147 Generalization Boundaries in Weak-to-Strong Supervision for Strategic Reasoners
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #148 Recursive Self-Aggregation and Consensus Mechanisms in High-Dimensional Reasoning Trees
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #149 Constitutional AI Safety Audits: Restricting Malicious Actor Actions via Self-Critique
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #150 Scalable Oversight in Reinforcement Learning via Multi-Agent Debate Game Theory
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #151 GRPO: Group Relative Policy Optimization for Sample-Efficient Reasoning in LLMs
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #152 Walk-Forward Cross-Validation for Robust Overfitting Detection in Trading Agents
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #153 Genetic Program Synthesis and Mutation Operators inside Isolated Sandboxes
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #154 Expected Free Energy Approximations for Epistemic Curiosity and Pragmatic Control
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #155 Multi-Mind Multi-Agent Organization for Resilient Goal-Oriented Planning
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #156 Hendrycks Safety Benchmarks: Formulating Quantitative Evaluation on Agent Interventions
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #157 Bayesian Belief Propagation over Persistent Experience Memory Graphs
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #158 Step-Wise Policy Training for Mathematical Reasoning without Human Ground-Truth
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #159 LADDER Decomposition for Complex Codebase Refactoring and Multi-Agent Execution
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #160 Genetic Optimization of Prompt Templates with Thompson Sampling and Bandit Feedback
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #161 Expected Free Energy active inference for adaptive web browser agents
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #162 Deflated Sharpe Ratio for High-Frequency Systematic Trading Strategy Evaluation
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #163 DeepSeek-R1 Replication: Analysis of Emergent Multi-Step Reasoning and Backtracking
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #164 Constitutional Guidelines for Mitigating Hallucination in Long-Horizon Task Planning
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #165 Prover-Verifier Games for Improving Code Comprehensibility and Logic Traceability
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #166 Walk-Forward Split and Non-Stationary Time-Series Forecasting in Financial Agents
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #167 Evolutionary Search over Neural Network Architectures with Large Language Model Mutators
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #168 Variational Free Energy minimization for continuous state-space path planning
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #169 Multi-Agent SOP Integration via Centralized Coordinate Repositories
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #170 Safety Case Formulation for High-Risk Autonomous Decision Surface Control
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #171 Ebbinghaus Forgetting Curves in Persistent Agent Database Repositories
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #172 Step-by-Step Rationale Bootstrapping for Scientific Thesis Extraction and Synthesis
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #173 Strategic Backtracking in Non-Deterministic Problem Domains using Tree of Thoughts
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #174 Large Language Models as Optimizers for Zero-Shot Prompt Evolution across Sectors
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #175 Epistemic Exploration vs Pragmatic Exploitation in Active Inference Agent Architectures
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #176 Statistical Multi-Testing Correction with Bonferroni and False Discovery Rate Control
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #177 Group Relative Policy Optimization for Mathematics Reasoning SFT Calibration
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #178 Debate-Centric Alignment: Dynamic Multi-Agent Reasoning via Competitive Game Theory
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #179 Constitutional AI for Autonomous Scientific Research: Enforcing Policy Constraints
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #180 Walk-Forward Optimization and DSR Guarding inside Non-Linear Decision Regimes
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #181 Self-Referential Code Rewrite and Mutator Operator Design inside Sandboxed Pythons
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #182 Expected Free Energy Active Inference Routing under Lightweight Micro-VM Architectures
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #183 Standard Operating Procedures (SOPs) for Resilient Agentic Software Engineering MAS
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #184 Hendrycks Safety Benchmarks for Robust Evaluation of Autonomous Agents
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #185 Experience Memory Graph: Parsing and Learning from Action-Decision Matching Trajectories
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #186 Math Shepherd: Automated Data Generation for Step-by-Step Process Reward Models
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #187 Strategic Hierarchical Task Decomposition using LADDER and Tree-of-Thoughts Backtracking
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #188 Thompson Sampling and Multi-Armed Bandits for Dynamic Prompt Mutation Optimization
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #189 Active Inference and Expected Free Energy routing in autonomous software testing
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #190 DSR and White's Reality Check for Robust Trading System Performance Audits
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #191 DeepSeekMath: Pushing the Frontiers of Mathematical Reasoning with GRPO RL
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #192 Constitutional Guidelines for Enforcing Safety inside Evolving Agent Frameworks
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #193 Prover-Verifier Games for Improving the Legibility and Accuracy of LLM Code Outputs
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #194 Walk-Forward Cross-Validation and Deflated Sharpe Ratio for Quantitative Finance
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #195 Genetic Programming and Program Synthesis with Large Language Model Mutators
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #196 Active Inference and Variational Free Energy minimization for robust robot navigation
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #197 Multi-Agent SOP Integration and Task Allocation with Structured Collaboration SOPs
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #198 Safety Case Formulation based on Game-Theoretic Multi-Agent Debate
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #199 Ebbinghaus Memory Decay and Experience Database Retrieval for Lifelong Learning
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #200 Step-by-Step Process Verification and PRM Synthesis for High-Accuracy Reasoning
- **Relationship Type:** `prerequisite` target: `Paper #128`