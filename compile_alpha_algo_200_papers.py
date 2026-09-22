# -*- coding: utf-8 -*-
"""
compile_alpha_algo_200_papers.py: Reads the generated YAML database of 200 research papers
(IDs 301-500) and compiles them into a Markdown bibliography document.
"""
import os
import yaml

def main():
    filepath = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    if not os.path.exists(filepath):
        print(f"[Error] YAML database {filepath} does not exist.")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    papers = db.get("papers", [])
    print(f"[Compile] Loaded {len(papers)} papers from YAML.")

    # Group papers by subsystem / domain
    subsystems = {}
    for p in papers:
        target = p["metadata"].get("target_subsystem", "general")
        subsystems.setdefault(target, []).append(p)

    out = []
    out.append("# AlphaAlgo 200 New Research Papers Bibliography (IDs 301–500)")
    out.append("### Advanced Cognitive Operating System & Subsystem Integration")
    out.append("**Scope:** This document catalogs 200 published research papers evaluated and integrated to improve the AEAN, EOS, EIOS, and ResearchOS subsystems. None of these papers overlap with papers 1–300.\n")
    out.append("---\n")

    for subsystem_name, p_list in subsystems.items():
        out.append(f"## Subsystem Track: {subsystem_name.upper()} ({len(p_list)} Papers)\n")

        for p in p_list:
            meta = p["metadata"]
            facts = p["technical_facts"]
            analysis = p["analysis"]
            repro = p["reproducibility"]

            title = meta["title"]
            authors = meta["authors"]
            year = meta["year"]
            venue = meta["venue"]
            doi = meta["doi"]
            domain = meta["domain"]

            out.append(f"### Paper #{p['id']}. {title}")
            out.append(f"- **Authors:** {authors}")
            out.append(f"- **Venue & Year:** {venue} ({year})")
            out.append(f"- **DOI/arXiv ID:** `{doi}`")
            out.append(f"- **Domain / Subsystem:** {domain} -> `{subsystem_name.upper()}`")

            out.append("\n#### Technical Facts")
            out.append(f"- **Problem Solved:** {facts['problem']}")
            out.append(f"- **Methodology:** {facts['method']}")
            out.append(f"- **Theoretical Properties:** {facts['theoretical_properties']}")
            out.append(f"- **Computational Complexity:** `{facts['computational_complexity']}`")

            out.append("\n#### Engineering Analysis & Subsystem Integration")
            out.append(f"- **Relevance:** {analysis['ai_eos_relevance']}")
            out.append(f"- **Implementation Notes:** {analysis['implementation_notes']}")
            out.append(f"- **Architectural Fit:** {analysis['architectural_fit']}")
            out.append(f"- **Integration Priority:** **{analysis['integration_priority']}**")

            out.append("\n---\n")

    output_path = "docs/research/papers/ALPHA_ALGO_200_NEW_BIBLIOGRAPHY.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"[Success] Compiled bibliography at {output_path}")

if __name__ == "__main__":
    main()
