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
        P133[#133 Scalable Step-wise Proces]
        P137[#137 Efficient Causal Modeling]
        P141[#141 Adaptive Trajectory Plann]
        P145[#145 Autonomous Audit Telemetr]
        P149[#149 Distributed Scalable Over]
        P153[#153 Scalable Step-wise Proces]
        P157[#157 Efficient Causal Modeling]
        P161[#161 Adaptive Trajectory Plann]
        P165[#165 Autonomous Audit Telemetr]
        P169[#169 Distributed Scalable Over]
        P173[#173 Scalable Step-wise Proces]
        P177[#177 Efficient Causal Modeling]
        P181[#181 Adaptive Trajectory Plann]
        P185[#185 Autonomous Audit Telemetr]
        P189[#189 Distributed Scalable Over]
        P193[#193 Scalable Step-wise Proces]
        P197[#197 Efficient Causal Modeling]
        P201[#201 Adaptive Trajectory Plann]
        P205[#205 Autonomous Audit Telemetr]
        P209[#209 Distributed Scalable Over]
        P213[#213 Scalable Step-wise Proces]
        P217[#217 Efficient Causal Modeling]
        P221[#221 Adaptive Trajectory Plann]
        P225[#225 Autonomous Audit Telemetr]
        P229[#229 Distributed Scalable Over]
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
        P134[#134 Dynamic Active Inference ]
        P138[#138 Unified Resource Allocati]
        P142[#142 Structured DPO Optimizati]
        P146[#146 Recursive Reinforcement L]
        P150[#150 Consensus Game-Theoretic ]
        P154[#154 Dynamic Active Inference ]
        P158[#158 Unified Resource Allocati]
        P162[#162 Structured DPO Optimizati]
        P166[#166 Recursive Reinforcement L]
        P170[#170 Consensus Game-Theoretic ]
        P174[#174 Dynamic Active Inference ]
        P178[#178 Unified Resource Allocati]
        P182[#182 Structured DPO Optimizati]
        P186[#186 Recursive Reinforcement L]
        P190[#190 Consensus Game-Theoretic ]
        P194[#194 Dynamic Active Inference ]
        P198[#198 Unified Resource Allocati]
        P202[#202 Structured DPO Optimizati]
        P206[#206 Recursive Reinforcement L]
        P210[#210 Consensus Game-Theoretic ]
        P214[#214 Dynamic Active Inference ]
        P218[#218 Unified Resource Allocati]
        P222[#222 Structured DPO Optimizati]
        P226[#226 Recursive Reinforcement L]
        P230[#230 Consensus Game-Theoretic ]
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
        P131[#131 Optimal Context Consolida]
        P135[#135 Verifiable Self-Correctio]
        P139[#139 Bayesian SFT Bootstrappin]
        P143[#143 Provable Process Verifica]
        P147[#147 Strategic Ebbinghaus Deca]
        P151[#151 Optimal Context Consolida]
        P155[#155 Verifiable Self-Correctio]
        P159[#159 Bayesian SFT Bootstrappin]
        P163[#163 Provable Process Verifica]
        P167[#167 Strategic Ebbinghaus Deca]
        P171[#171 Optimal Context Consolida]
        P175[#175 Verifiable Self-Correctio]
        P179[#179 Bayesian SFT Bootstrappin]
        P183[#183 Provable Process Verifica]
        P187[#187 Strategic Ebbinghaus Deca]
        P191[#191 Optimal Context Consolida]
        P195[#195 Verifiable Self-Correctio]
        P199[#199 Bayesian SFT Bootstrappin]
        P203[#203 Provable Process Verifica]
        P207[#207 Strategic Ebbinghaus Deca]
        P211[#211 Optimal Context Consolida]
        P215[#215 Verifiable Self-Correctio]
        P219[#219 Bayesian SFT Bootstrappin]
        P223[#223 Provable Process Verifica]
        P227[#227 Strategic Ebbinghaus Deca]
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
        P132[#132 Robust Multi-Agent Coordi]
        P136[#136 Deep MCTS Exploration wit]
        P140[#140 Causal Program Synthesis ]
        P144[#144 Iterative Belief Propagat]
        P148[#148 Parallel Veto Governance ]
        P152[#152 Robust Multi-Agent Coordi]
        P156[#156 Deep MCTS Exploration wit]
        P160[#160 Causal Program Synthesis ]
        P164[#164 Iterative Belief Propagat]
        P168[#168 Parallel Veto Governance ]
        P172[#172 Robust Multi-Agent Coordi]
        P176[#176 Deep MCTS Exploration wit]
        P180[#180 Causal Program Synthesis ]
        P184[#184 Iterative Belief Propagat]
        P188[#188 Parallel Veto Governance ]
        P192[#192 Robust Multi-Agent Coordi]
        P196[#196 Deep MCTS Exploration wit]
        P200[#200 Causal Program Synthesis ]
        P204[#204 Iterative Belief Propagat]
        P208[#208 Parallel Veto Governance ]
        P212[#212 Robust Multi-Agent Coordi]
        P216[#216 Deep MCTS Exploration wit]
        P220[#220 Causal Program Synthesis ]
        P224[#224 Iterative Belief Propagat]
        P228[#228 Parallel Veto Governance ]
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
    P2 -->|prerequisite| P131
    P3 -->|prerequisite| P132
    P4 -->|prerequisite| P133
    P5 -->|prerequisite| P134
    P6 -->|prerequisite| P135
    P7 -->|prerequisite| P136
    P8 -->|prerequisite| P137
    P9 -->|prerequisite| P138
    P10 -->|prerequisite| P139
    P11 -->|prerequisite| P140
    P12 -->|prerequisite| P141
    P13 -->|prerequisite| P142
    P14 -->|prerequisite| P143
    P15 -->|prerequisite| P144
    P16 -->|prerequisite| P145
    P17 -->|prerequisite| P146
    P18 -->|prerequisite| P147
    P19 -->|prerequisite| P148
    P20 -->|prerequisite| P149
    P21 -->|prerequisite| P150
    P22 -->|prerequisite| P151
    P23 -->|prerequisite| P152
    P24 -->|prerequisite| P153
    P25 -->|prerequisite| P154
    P26 -->|prerequisite| P155
    P27 -->|prerequisite| P156
    P28 -->|prerequisite| P157
    P29 -->|prerequisite| P158
    P30 -->|prerequisite| P159
    P31 -->|prerequisite| P160
    P32 -->|prerequisite| P161
    P33 -->|prerequisite| P162
    P34 -->|prerequisite| P163
    P35 -->|prerequisite| P164
    P36 -->|prerequisite| P165
    P37 -->|prerequisite| P166
    P38 -->|prerequisite| P167
    P39 -->|prerequisite| P168
    P40 -->|prerequisite| P169
    P41 -->|prerequisite| P170
    P42 -->|prerequisite| P171
    P43 -->|prerequisite| P172
    P44 -->|prerequisite| P173
    P45 -->|prerequisite| P174
    P46 -->|prerequisite| P175
    P47 -->|prerequisite| P176
    P48 -->|prerequisite| P177
    P49 -->|prerequisite| P178
    P50 -->|prerequisite| P179
    P51 -->|prerequisite| P180
    P52 -->|prerequisite| P181
    P53 -->|prerequisite| P182
    P54 -->|prerequisite| P183
    P55 -->|prerequisite| P184
    P56 -->|prerequisite| P185
    P57 -->|prerequisite| P186
    P58 -->|prerequisite| P187
    P59 -->|prerequisite| P188
    P60 -->|prerequisite| P189
    P61 -->|prerequisite| P190
    P62 -->|prerequisite| P191
    P63 -->|prerequisite| P192
    P64 -->|prerequisite| P193
    P65 -->|prerequisite| P194
    P66 -->|prerequisite| P195
    P67 -->|prerequisite| P196
    P68 -->|prerequisite| P197
    P69 -->|prerequisite| P198
    P70 -->|prerequisite| P199
    P71 -->|prerequisite| P200
    P72 -->|prerequisite| P201
    P73 -->|prerequisite| P202
    P74 -->|prerequisite| P203
    P75 -->|prerequisite| P204
    P76 -->|prerequisite| P205
    P77 -->|prerequisite| P206
    P78 -->|prerequisite| P207
    P79 -->|prerequisite| P208
    P80 -->|prerequisite| P209
    P81 -->|prerequisite| P210
    P82 -->|prerequisite| P211
    P83 -->|prerequisite| P212
    P84 -->|prerequisite| P213
    P85 -->|prerequisite| P214
    P86 -->|prerequisite| P215
    P87 -->|prerequisite| P216
    P88 -->|prerequisite| P217
    P89 -->|prerequisite| P218
    P90 -->|prerequisite| P219
    P91 -->|prerequisite| P220
    P92 -->|prerequisite| P221
    P93 -->|prerequisite| P222
    P94 -->|prerequisite| P223
    P95 -->|prerequisite| P224
    P96 -->|prerequisite| P225
    P97 -->|prerequisite| P226
    P98 -->|prerequisite| P227
    P99 -->|prerequisite| P228
    P100 -->|prerequisite| P229
    P101 -->|prerequisite| P230
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

### #131 Optimal Context Consolidation in Long-Horizon Task Execution (Paper #131)
- **Relationship Type:** `prerequisite` target: `Paper #2`

### #132 Robust Multi-Agent Coordination via Process Reward Models (Paper #132)
- **Relationship Type:** `prerequisite` target: `Paper #3`

### #133 Scalable Step-wise Process Verification on the Pareto Frontier (Paper #133)
- **Relationship Type:** `prerequisite` target: `Paper #4`

### #134 Dynamic Active Inference for Self-Improving AI Systems (Paper #134)
- **Relationship Type:** `prerequisite` target: `Paper #5`

### #135 Verifiable Self-Correction for Autonomous Discovery (Paper #135)
- **Relationship Type:** `prerequisite` target: `Paper #6`

### #136 Deep MCTS Exploration with Step-Wise Process Verification (Paper #136)
- **Relationship Type:** `prerequisite` target: `Paper #7`

### #137 Efficient Causal Modeling across Decentralized Sub-agents (Paper #137)
- **Relationship Type:** `prerequisite` target: `Paper #8`

### #138 Unified Resource Allocation under Latency Constraints (Paper #138)
- **Relationship Type:** `prerequisite` target: `Paper #9`

### #139 Bayesian SFT Bootstrapping using Causal do-calculus (Paper #139)
- **Relationship Type:** `prerequisite` target: `Paper #10`

### #140 Causal Program Synthesis over Multi-Tier Memory Graphs (Paper #140)
- **Relationship Type:** `prerequisite` target: `Paper #11`

### #141 Adaptive Trajectory Planning in Long-Horizon Task Execution (Paper #141)
- **Relationship Type:** `prerequisite` target: `Paper #12`

### #142 Structured DPO Optimization via Process Reward Models (Paper #142)
- **Relationship Type:** `prerequisite` target: `Paper #13`

### #143 Provable Process Verification on the Pareto Frontier (Paper #143)
- **Relationship Type:** `prerequisite` target: `Paper #14`

### #144 Iterative Belief Propagation for Self-Improving AI Systems (Paper #144)
- **Relationship Type:** `prerequisite` target: `Paper #15`

### #145 Autonomous Audit Telemetry for Autonomous Discovery (Paper #145)
- **Relationship Type:** `prerequisite` target: `Paper #16`

### #146 Recursive Reinforcement Learning with Step-Wise Process Verification (Paper #146)
- **Relationship Type:** `prerequisite` target: `Paper #17`

### #147 Strategic Ebbinghaus Decay across Decentralized Sub-agents (Paper #147)
- **Relationship Type:** `prerequisite` target: `Paper #18`

### #148 Parallel Veto Governance under Latency Constraints (Paper #148)
- **Relationship Type:** `prerequisite` target: `Paper #19`

### #149 Distributed Scalable Oversight using Causal do-calculus (Paper #149)
- **Relationship Type:** `prerequisite` target: `Paper #20`

### #150 Consensus Game-Theoretic Debate over Multi-Tier Memory Graphs (Paper #150)
- **Relationship Type:** `prerequisite` target: `Paper #21`

### #151 Optimal Context Consolidation in Long-Horizon Task Execution (Paper #151)
- **Relationship Type:** `prerequisite` target: `Paper #22`

### #152 Robust Multi-Agent Coordination via Process Reward Models (Paper #152)
- **Relationship Type:** `prerequisite` target: `Paper #23`

### #153 Scalable Step-wise Process Verification on the Pareto Frontier (Paper #153)
- **Relationship Type:** `prerequisite` target: `Paper #24`

### #154 Dynamic Active Inference for Self-Improving AI Systems (Paper #154)
- **Relationship Type:** `prerequisite` target: `Paper #25`

### #155 Verifiable Self-Correction for Autonomous Discovery (Paper #155)
- **Relationship Type:** `prerequisite` target: `Paper #26`

### #156 Deep MCTS Exploration with Step-Wise Process Verification (Paper #156)
- **Relationship Type:** `prerequisite` target: `Paper #27`

### #157 Efficient Causal Modeling across Decentralized Sub-agents (Paper #157)
- **Relationship Type:** `prerequisite` target: `Paper #28`

### #158 Unified Resource Allocation under Latency Constraints (Paper #158)
- **Relationship Type:** `prerequisite` target: `Paper #29`

### #159 Bayesian SFT Bootstrapping using Causal do-calculus (Paper #159)
- **Relationship Type:** `prerequisite` target: `Paper #30`

### #160 Causal Program Synthesis over Multi-Tier Memory Graphs (Paper #160)
- **Relationship Type:** `prerequisite` target: `Paper #31`

### #161 Adaptive Trajectory Planning in Long-Horizon Task Execution (Paper #161)
- **Relationship Type:** `prerequisite` target: `Paper #32`

### #162 Structured DPO Optimization via Process Reward Models (Paper #162)
- **Relationship Type:** `prerequisite` target: `Paper #33`

### #163 Provable Process Verification on the Pareto Frontier (Paper #163)
- **Relationship Type:** `prerequisite` target: `Paper #34`

### #164 Iterative Belief Propagation for Self-Improving AI Systems (Paper #164)
- **Relationship Type:** `prerequisite` target: `Paper #35`

### #165 Autonomous Audit Telemetry for Autonomous Discovery (Paper #165)
- **Relationship Type:** `prerequisite` target: `Paper #36`

### #166 Recursive Reinforcement Learning with Step-Wise Process Verification (Paper #166)
- **Relationship Type:** `prerequisite` target: `Paper #37`

### #167 Strategic Ebbinghaus Decay across Decentralized Sub-agents (Paper #167)
- **Relationship Type:** `prerequisite` target: `Paper #38`

### #168 Parallel Veto Governance under Latency Constraints (Paper #168)
- **Relationship Type:** `prerequisite` target: `Paper #39`

### #169 Distributed Scalable Oversight using Causal do-calculus (Paper #169)
- **Relationship Type:** `prerequisite` target: `Paper #40`

### #170 Consensus Game-Theoretic Debate over Multi-Tier Memory Graphs (Paper #170)
- **Relationship Type:** `prerequisite` target: `Paper #41`

### #171 Optimal Context Consolidation in Long-Horizon Task Execution (Paper #171)
- **Relationship Type:** `prerequisite` target: `Paper #42`

### #172 Robust Multi-Agent Coordination via Process Reward Models (Paper #172)
- **Relationship Type:** `prerequisite` target: `Paper #43`

### #173 Scalable Step-wise Process Verification on the Pareto Frontier (Paper #173)
- **Relationship Type:** `prerequisite` target: `Paper #44`

### #174 Dynamic Active Inference for Self-Improving AI Systems (Paper #174)
- **Relationship Type:** `prerequisite` target: `Paper #45`

### #175 Verifiable Self-Correction for Autonomous Discovery (Paper #175)
- **Relationship Type:** `prerequisite` target: `Paper #46`

### #176 Deep MCTS Exploration with Step-Wise Process Verification (Paper #176)
- **Relationship Type:** `prerequisite` target: `Paper #47`

### #177 Efficient Causal Modeling across Decentralized Sub-agents (Paper #177)
- **Relationship Type:** `prerequisite` target: `Paper #48`

### #178 Unified Resource Allocation under Latency Constraints (Paper #178)
- **Relationship Type:** `prerequisite` target: `Paper #49`

### #179 Bayesian SFT Bootstrapping using Causal do-calculus (Paper #179)
- **Relationship Type:** `prerequisite` target: `Paper #50`

### #180 Causal Program Synthesis over Multi-Tier Memory Graphs (Paper #180)
- **Relationship Type:** `prerequisite` target: `Paper #51`

### #181 Adaptive Trajectory Planning in Long-Horizon Task Execution (Paper #181)
- **Relationship Type:** `prerequisite` target: `Paper #52`

### #182 Structured DPO Optimization via Process Reward Models (Paper #182)
- **Relationship Type:** `prerequisite` target: `Paper #53`

### #183 Provable Process Verification on the Pareto Frontier (Paper #183)
- **Relationship Type:** `prerequisite` target: `Paper #54`

### #184 Iterative Belief Propagation for Self-Improving AI Systems (Paper #184)
- **Relationship Type:** `prerequisite` target: `Paper #55`

### #185 Autonomous Audit Telemetry for Autonomous Discovery (Paper #185)
- **Relationship Type:** `prerequisite` target: `Paper #56`

### #186 Recursive Reinforcement Learning with Step-Wise Process Verification (Paper #186)
- **Relationship Type:** `prerequisite` target: `Paper #57`

### #187 Strategic Ebbinghaus Decay across Decentralized Sub-agents (Paper #187)
- **Relationship Type:** `prerequisite` target: `Paper #58`

### #188 Parallel Veto Governance under Latency Constraints (Paper #188)
- **Relationship Type:** `prerequisite` target: `Paper #59`

### #189 Distributed Scalable Oversight using Causal do-calculus (Paper #189)
- **Relationship Type:** `prerequisite` target: `Paper #60`

### #190 Consensus Game-Theoretic Debate over Multi-Tier Memory Graphs (Paper #190)
- **Relationship Type:** `prerequisite` target: `Paper #61`

### #191 Optimal Context Consolidation in Long-Horizon Task Execution (Paper #191)
- **Relationship Type:** `prerequisite` target: `Paper #62`

### #192 Robust Multi-Agent Coordination via Process Reward Models (Paper #192)
- **Relationship Type:** `prerequisite` target: `Paper #63`

### #193 Scalable Step-wise Process Verification on the Pareto Frontier (Paper #193)
- **Relationship Type:** `prerequisite` target: `Paper #64`

### #194 Dynamic Active Inference for Self-Improving AI Systems (Paper #194)
- **Relationship Type:** `prerequisite` target: `Paper #65`

### #195 Verifiable Self-Correction for Autonomous Discovery (Paper #195)
- **Relationship Type:** `prerequisite` target: `Paper #66`

### #196 Deep MCTS Exploration with Step-Wise Process Verification (Paper #196)
- **Relationship Type:** `prerequisite` target: `Paper #67`

### #197 Efficient Causal Modeling across Decentralized Sub-agents (Paper #197)
- **Relationship Type:** `prerequisite` target: `Paper #68`

### #198 Unified Resource Allocation under Latency Constraints (Paper #198)
- **Relationship Type:** `prerequisite` target: `Paper #69`

### #199 Bayesian SFT Bootstrapping using Causal do-calculus (Paper #199)
- **Relationship Type:** `prerequisite` target: `Paper #70`

### #200 Causal Program Synthesis over Multi-Tier Memory Graphs (Paper #200)
- **Relationship Type:** `prerequisite` target: `Paper #71`

### #201 Adaptive Trajectory Planning in Long-Horizon Task Execution (Paper #201)
- **Relationship Type:** `prerequisite` target: `Paper #72`

### #202 Structured DPO Optimization via Process Reward Models (Paper #202)
- **Relationship Type:** `prerequisite` target: `Paper #73`

### #203 Provable Process Verification on the Pareto Frontier (Paper #203)
- **Relationship Type:** `prerequisite` target: `Paper #74`

### #204 Iterative Belief Propagation for Self-Improving AI Systems (Paper #204)
- **Relationship Type:** `prerequisite` target: `Paper #75`

### #205 Autonomous Audit Telemetry for Autonomous Discovery (Paper #205)
- **Relationship Type:** `prerequisite` target: `Paper #76`

### #206 Recursive Reinforcement Learning with Step-Wise Process Verification (Paper #206)
- **Relationship Type:** `prerequisite` target: `Paper #77`

### #207 Strategic Ebbinghaus Decay across Decentralized Sub-agents (Paper #207)
- **Relationship Type:** `prerequisite` target: `Paper #78`

### #208 Parallel Veto Governance under Latency Constraints (Paper #208)
- **Relationship Type:** `prerequisite` target: `Paper #79`

### #209 Distributed Scalable Oversight using Causal do-calculus (Paper #209)
- **Relationship Type:** `prerequisite` target: `Paper #80`

### #210 Consensus Game-Theoretic Debate over Multi-Tier Memory Graphs (Paper #210)
- **Relationship Type:** `prerequisite` target: `Paper #81`

### #211 Optimal Context Consolidation in Long-Horizon Task Execution (Paper #211)
- **Relationship Type:** `prerequisite` target: `Paper #82`

### #212 Robust Multi-Agent Coordination via Process Reward Models (Paper #212)
- **Relationship Type:** `prerequisite` target: `Paper #83`

### #213 Scalable Step-wise Process Verification on the Pareto Frontier (Paper #213)
- **Relationship Type:** `prerequisite` target: `Paper #84`

### #214 Dynamic Active Inference for Self-Improving AI Systems (Paper #214)
- **Relationship Type:** `prerequisite` target: `Paper #85`

### #215 Verifiable Self-Correction for Autonomous Discovery (Paper #215)
- **Relationship Type:** `prerequisite` target: `Paper #86`

### #216 Deep MCTS Exploration with Step-Wise Process Verification (Paper #216)
- **Relationship Type:** `prerequisite` target: `Paper #87`

### #217 Efficient Causal Modeling across Decentralized Sub-agents (Paper #217)
- **Relationship Type:** `prerequisite` target: `Paper #88`

### #218 Unified Resource Allocation under Latency Constraints (Paper #218)
- **Relationship Type:** `prerequisite` target: `Paper #89`

### #219 Bayesian SFT Bootstrapping using Causal do-calculus (Paper #219)
- **Relationship Type:** `prerequisite` target: `Paper #90`

### #220 Causal Program Synthesis over Multi-Tier Memory Graphs (Paper #220)
- **Relationship Type:** `prerequisite` target: `Paper #91`

### #221 Adaptive Trajectory Planning in Long-Horizon Task Execution (Paper #221)
- **Relationship Type:** `prerequisite` target: `Paper #92`

### #222 Structured DPO Optimization via Process Reward Models (Paper #222)
- **Relationship Type:** `prerequisite` target: `Paper #93`

### #223 Provable Process Verification on the Pareto Frontier (Paper #223)
- **Relationship Type:** `prerequisite` target: `Paper #94`

### #224 Iterative Belief Propagation for Self-Improving AI Systems (Paper #224)
- **Relationship Type:** `prerequisite` target: `Paper #95`

### #225 Autonomous Audit Telemetry for Autonomous Discovery (Paper #225)
- **Relationship Type:** `prerequisite` target: `Paper #96`

### #226 Recursive Reinforcement Learning with Step-Wise Process Verification (Paper #226)
- **Relationship Type:** `prerequisite` target: `Paper #97`

### #227 Strategic Ebbinghaus Decay across Decentralized Sub-agents (Paper #227)
- **Relationship Type:** `prerequisite` target: `Paper #98`

### #228 Parallel Veto Governance under Latency Constraints (Paper #228)
- **Relationship Type:** `prerequisite` target: `Paper #99`

### #229 Distributed Scalable Oversight using Causal do-calculus (Paper #229)
- **Relationship Type:** `prerequisite` target: `Paper #100`

### #230 Consensus Game-Theoretic Debate over Multi-Tier Memory Graphs (Paper #230)
- **Relationship Type:** `prerequisite` target: `Paper #101`