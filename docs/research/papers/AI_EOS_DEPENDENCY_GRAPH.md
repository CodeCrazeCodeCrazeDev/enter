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
        P131[#131 Empirical Principles of R]
        P132[#132 Empirical Principles of R]
        P133[#133 Empirical Principles of T]
        P134[#134 Empirical Principles of S]
        P135[#135 Empirical Principles of M]
        P136[#136 Empirical Principles of P]
        P137[#137 Empirical Principles of G]
        P138[#138 Empirical Principles of S]
        P139[#139 Empirical Principles of A]
        P140[#140 Empirical Principles of T]
        P141[#141 Empirical Principles of A]
        P142[#142 Empirical Principles of D]
        P143[#143 Empirical Principles of P]
        P144[#144 Empirical Principles of E]
        P145[#145 Empirical Principles of R]
        P146[#146 Empirical Principles of R]
        P147[#147 Empirical Principles of S]
        P148[#148 Empirical Principles of S]
        P149[#149 Empirical Principles of M]
        P150[#150 Empirical Principles of A]
        P151[#151 Empirical Principles of O]
        P152[#152 Empirical Principles of M]
        P153[#153 Empirical Principles of R]
        P154[#154 Empirical Principles of R]
        P155[#155 Empirical Principles of T]
        P156[#156 Empirical Principles of S]
        P157[#157 Empirical Principles of M]
        P158[#158 Empirical Principles of P]
        P159[#159 Empirical Principles of G]
        P160[#160 Empirical Principles of S]
        P161[#161 Empirical Principles of A]
        P162[#162 Empirical Principles of T]
        P163[#163 Empirical Principles of A]
        P164[#164 Empirical Principles of D]
        P165[#165 Empirical Principles of P]
        P166[#166 Empirical Principles of E]
        P167[#167 Empirical Principles of R]
        P168[#168 Empirical Principles of R]
        P169[#169 Empirical Principles of S]
        P170[#170 Empirical Principles of S]
        P171[#171 Empirical Principles of M]
        P172[#172 Empirical Principles of A]
        P173[#173 Empirical Principles of O]
        P174[#174 Empirical Principles of M]
        P175[#175 Empirical Principles of R]
        P176[#176 Empirical Principles of R]
        P177[#177 Empirical Principles of T]
        P178[#178 Empirical Principles of S]
        P179[#179 Empirical Principles of M]
        P180[#180 Empirical Principles of P]
        P181[#181 Empirical Principles of G]
        P182[#182 Empirical Principles of S]
        P183[#183 Empirical Principles of A]
        P184[#184 Empirical Principles of T]
        P185[#185 Empirical Principles of A]
        P186[#186 Empirical Principles of D]
        P187[#187 Empirical Principles of P]
        P188[#188 Empirical Principles of E]
        P189[#189 Empirical Principles of R]
        P190[#190 Empirical Principles of R]
        P191[#191 Empirical Principles of S]
        P192[#192 Empirical Principles of S]
        P193[#193 Empirical Principles of M]
        P194[#194 Empirical Principles of A]
        P195[#195 Empirical Principles of O]
        P196[#196 Empirical Principles of M]
        P197[#197 Empirical Principles of R]
        P198[#198 Empirical Principles of R]
        P199[#199 Empirical Principles of T]
        P200[#200 Empirical Principles of S]
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

### #131 Empirical Principles of RSI Prompting in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #132 Empirical Principles of RSI Execution in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #133 Empirical Principles of Textual Feedback in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #134 Empirical Principles of Self-Correction in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #135 Empirical Principles of MCTS Verification in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #136 Empirical Principles of PRM Verification in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #137 Empirical Principles of Game Theory MAS in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #138 Empirical Principles of Swarm Research in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #139 Empirical Principles of Active Inference Planning in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #140 Empirical Principles of Task Planning in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #141 Empirical Principles of AI Scientist in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #142 Empirical Principles of Domain Discovery in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #143 Empirical Principles of Program Search in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #144 Empirical Principles of Evolutionary Search in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #145 Empirical Principles of RLVR / GRPO in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #146 Empirical Principles of RLVR in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #147 Empirical Principles of Safety Alignment in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #148 Empirical Principles of Safety Auditing in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #149 Empirical Principles of Memory Consolidation in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #150 Empirical Principles of Agent Recovery in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #151 Empirical Principles of Orchestration Routing in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #152 Empirical Principles of Multi-Agent Planning in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #153 Empirical Principles of RSI Prompting in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #154 Empirical Principles of RSI Execution in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #155 Empirical Principles of Textual Feedback in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #156 Empirical Principles of Self-Correction in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #157 Empirical Principles of MCTS Verification in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #158 Empirical Principles of PRM Verification in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #159 Empirical Principles of Game Theory MAS in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #160 Empirical Principles of Swarm Research in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #161 Empirical Principles of Active Inference Planning in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #162 Empirical Principles of Task Planning in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #163 Empirical Principles of AI Scientist in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #164 Empirical Principles of Domain Discovery in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #165 Empirical Principles of Program Search in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #166 Empirical Principles of Evolutionary Search in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #167 Empirical Principles of RLVR / GRPO in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #168 Empirical Principles of RLVR in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #169 Empirical Principles of Safety Alignment in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #170 Empirical Principles of Safety Auditing in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #171 Empirical Principles of Memory Consolidation in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #172 Empirical Principles of Agent Recovery in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #173 Empirical Principles of Orchestration Routing in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #174 Empirical Principles of Multi-Agent Planning in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #175 Empirical Principles of RSI Prompting in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #176 Empirical Principles of RSI Execution in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #177 Empirical Principles of Textual Feedback in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #178 Empirical Principles of Self-Correction in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #179 Empirical Principles of MCTS Verification in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #180 Empirical Principles of PRM Verification in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #181 Empirical Principles of Game Theory MAS in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #182 Empirical Principles of Swarm Research in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #183 Empirical Principles of Active Inference Planning in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #184 Empirical Principles of Task Planning in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #185 Empirical Principles of AI Scientist in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #186 Empirical Principles of Domain Discovery in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #187 Empirical Principles of Program Search in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #188 Empirical Principles of Evolutionary Search in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #189 Empirical Principles of RLVR / GRPO in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #190 Empirical Principles of RLVR in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #191 Empirical Principles of Safety Alignment in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #192 Empirical Principles of Safety Auditing in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #193 Empirical Principles of Memory Consolidation in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #194 Empirical Principles of Agent Recovery in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #195 Empirical Principles of Orchestration Routing in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #196 Empirical Principles of Multi-Agent Planning in High-Fidelity Systems v1
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #197 Empirical Principles of RSI Prompting in High-Fidelity Systems v2
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #198 Empirical Principles of RSI Execution in High-Fidelity Systems v3
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #199 Empirical Principles of Textual Feedback in High-Fidelity Systems v4
- **Relationship Type:** `prerequisite` target: `Paper #128`

### #200 Empirical Principles of Self-Correction in High-Fidelity Systems v5
- **Relationship Type:** `prerequisite` target: `Paper #128`