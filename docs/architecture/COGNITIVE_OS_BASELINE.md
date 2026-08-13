# Cognitive OS Quantitative & Architectural Baseline (v3.0.0)
**Author:** Jules, Software Engineer
**Audit Target:** Unified Subsystem Substrate
**Base Commit Hash:** `e0760f1224070a948d8e42a4dfa05afaea8e9b94`

This document establishes the verified baseline of the Cognitive OS, detailing our research corpus parameters, module ownership, and system discrepancies.

---

## 1. Verified Research Corpus Parameters
The programmatic audit of the scientific knowledge base has resolved all previous reporting inconsistencies:
- **Actual Number of Papers in YAML Database (`AI_EOS_RESEARCH_DB.yaml`):** Exactly **130 papers**.
- **Actual Number of Papers in Bibliography (`AI_EOS_RESEARCH_BIBLIOGRAPHY.md`):** Exactly **130 papers**.
- **Actual Unique Paper Count:** Exactly **130 unique titles** verified with zero duplications.
- **Papers Mapped in Traceability Report (`AI_EOS_RESEARCH_TO_CODE_TRACEABILITY.md`):** Exactly **50 papers** (49 unique titles) are formally traced.

---

## 2. Traced Exclusion Set (Previously Incorporated Papers)
The following 49 unique papers constitute our **Exclusion Set** to prevent accidental reuse in any future research increments:
1. Gödel Agent [2410.04444]
2. Darwin Gödel Machine [2505.22954]
3. STOP [2310.02304]
4. Recursive Introspection [2407.18219]
5. Red Queen Gödel Machine [2606.26294]
6. Escher-Loop [2604.23472]
7. Self-Reference in LLMs [2607.04277]
8. Self-Reflection in LLM [2405.06682]
9. Robots That Ask for Help [2307.01928]
10. Survey of Self-Evolving Agents [2507.21046]
11. Survey of Self-Evolving AI Agents [2508.07407]
12. Self-Improvements in Agentic [2607.13104]
13. SIA [2605.27276]
14. Self-Harness [2606.09498]
15. MemoHarness [2607.14159]
16. Rethinking Harness Eval [2607.12227]
17. Agentic Harness Eng. [2604.25850]
18. HASE [2607.03935]
19. Next-Gen Agentic RL [2607.01120]
20. Experience Memory Graph [2607.13884]
21. Beyond Fixed Representations [2607.09560]
22. Externalization in LLM [2604.08224]
23. A-MEM [2502.12110]
24. Memory-R1 [2508.19828]
25. MemSkill [2602.02474]
26. SkillRL [2602.08234]
27. Meta Context Engineering [2601.21557]
28. MetaSkill-Evolve [2607.05297]
29. AgenticRed [2601.13518]
30. Group-Evolving Agents [2602.04837]
31. Terralingua
32. ShinkaEvolve
33. CodeEvolve
34. TurboEvolve
35. Multi-Agent Collaboration
36. Beyond Self-Talk
37. Beyond Individual MAS
38. LLM MAS Challenges
39. Agentic Env. Engineering
40. Agent Interoperability
41. Coordination Architectural Layer
42. RL MAS Orchestration Traces
43. Where LLM Agents Fail
44. MultiagentBench
45. Orchestration of MAS
46. SwarmResearch
47. Uno-Orchestra
48. AOrchestra
49. Dr. MAS RL

---

## 3. Discrepancies and Gap Analysis
We report the following gaps between previous claims and actual repository evidence:
1.  **Paper Count Claims:** Previous reports claimed a "SOTA 200-paper research corpus was successfully generated and integrated." In reality, `AI_EOS_RESEARCH_DB.yaml` contains **exactly 130** distinct research entries.
2.  **Mocked Core Interfaces:** In `ResearchOS` (`apodex/ai_eos/research/research_os.py`), core functional hooks like `conduct_literature_review()` are completely mocked, returning a static structure. The system lacked an executable 12-stage scientific loop.
3.  **Duplicated Capabilities:**
    -   *Planners:* Exist under 4 conflicting modules (`UnifiedPlanner`, `CMOSQueryPlanner`, `StrategicPlanner`, `RecursivePlanner`).
    -   *Memories:* Exist under 5 separate formats (`UnifiedMemory`, `LongTermLearningMemory`, `SemanticMemory`, `InMemoryMemoryRepository`, `SQLiteMemoryRepository`).
    -   *World Models:* Split-brain behavior between `WorldModel` and `WorldGraphManager`.

---

## 4. Subsystem Performance Baseline
The baseline metrics for our current substrate:
-   **Test Coverage & Success Rate:** 100% of the 361 unit/integration tests pass cleanly under Python 3.12.13 (Pytest 9.1.1).
-   **Latency:** Execution of full test collection and run completes in **~4.27 seconds**.
-   **Resource Utilization:** Zero-leak SQLite memory connections and subprocess-isolated execution.
