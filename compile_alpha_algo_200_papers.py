# -*- coding: utf-8 -*-
"""
compile_alpha_algo_200_papers.py: Compiles ALPHA_ALGO_200_NEW_RESEARCH.yaml into
docs/research/papers/ALPHA_ALGO_200_NEW_BIBLIOGRAPHY.md
"""
import yaml

def compile_bibliography():
    with open("docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml", "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    papers = db.get("papers", [])
    out = []
    out.append("# AlphaAlgo 200-Paper Quantitative & AI Research Bibliography (IDs 301-500)")
    out.append("### Single Source of Truth for Extracted Transferable Principles & Mathematical Foundations")
    out.append("**Core Areas:** Active Inference & Free Energy (301-340) | Multi-Agent Consensus & Swarms (341-380) | Causal Reasoning & SCMs (381-420) | RL Alignment & DPO (421-460) | Evolutionary Search & MAP-Elites (461-500)\n")
    out.append("---\n")

    for p in papers:
        p_id = p["id"]
        meta = p["metadata"]
        facts = p["technical_facts"]
        analysis = p["analysis"]
        repro = p["reproducibility"]
        conf = p["confidence"]

        out.append(f"## Paper #{p_id}: {meta['title']}")
        out.append(f"- **Authors:** {meta['authors']}")
        out.append(f"- **Venue & Year:** {meta['venue']} ({meta['year']})")
        out.append(f"- **Domain:** {meta['domain']} | **DOI:** `{meta['doi']}`")
        out.append("\n### Technical Facts")
        out.append(f"- **Problem Solved:** {facts['problem']}")
        out.append(f"- **Methodology:** {facts['method']}")
        out.append(f"- **Theoretical Properties:** {facts['theoretical_properties']}")
        out.append(f"- **Complexity:** `{facts['computational_complexity']}`")
        out.append(f"- **Limitations:** {facts['limitations']}")

        out.append("\n### AI Cognitive OS Engineering Analysis")
        out.append(f"- **Relevance:** {analysis['ai_eos_relevance']}")
        out.append(f"- **Implementation Notes:** {analysis['implementation_notes']}")
        out.append(f"- **Architectural Fit:** {analysis['architectural_fit']}")
        out.append(f"- **Integration Priority:** **{analysis['integration_priority']}**")
        out.append(f"- **Scientific Novelty Score:** {analysis['scientific_novelty']['score']}/10")
        out.append(f"- **Production Readiness Score:** {analysis['production_readiness']['score']}/10")
        out.append(f"- **Open Questions:** *{analysis['open_questions']}*")
        out.append("\n---\n")

    filepath = "docs/research/papers/ALPHA_ALGO_200_NEW_BIBLIOGRAPHY.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"[Success] Compiled 200-paper bibliography at {filepath}")

if __name__ == "__main__":
    compile_bibliography()
