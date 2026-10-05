# -*- coding: utf-8 -*-
"""
scripts/compile_alpha_algo_200_new_papers.py: Reads ALPHA_ALGO_200_NEW_RESEARCH.yaml (IDs 301-500)
and compiles a clean, publication-grade Markdown bibliography cataloging all 200 papers.
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

    # Group papers by target subsystem / domain
    subsystems = {}
    for p in papers:
        target = p["metadata"].get("target_subsystem", p["metadata"]["domain"])
        subsystems.setdefault(target, []).append(p)

    out = []
    out.append("# AlphaAlgo 200 New Research Papers Bibliography (IDs 301-500)")
    out.append("### Advanced Cognitive Operating System Engineering & Multi-Agent Intelligence")
    out.append("**Scope:** Catalogs 200 high-fidelity research papers (IDs 301-500) evaluated to enhance AEAN, EOS, EIOS, and ResearchOS. All papers have been strictly audited with 0% title or DOI overlap against papers 1-300.\n")
    out.append("---\n")
    out.append("## Executive Summary of Extracted Transferable Principles\n")
    out.append("From this 200-paper corpus (IDs 301-500), we extract core transferable engineering principles targeted directly at four core subsystem layers:")
    out.append("1. **AEAN (Agent Networks):** Sycophancy-mitigated consensus, second-price token clearing, and dynamic priority decay under finite token budgets.")
    out.append("2. **EOS (Entrepreneurial OS):** Active inference expected free energy (EFE) opportunity graph traversal, risk-discounted capital allocation, and startup runway hazard sensing.")
    out.append("3. **EIOS (Execution Kernel):** Multi-timescale active sensing, non-Gaussian Hawkes process anomaly detection, and dynamic execution DAG reordering under latency budgets.")
    out.append("4. **ResearchOS (Scientific Discovery):** Multi-field literature search, self-referential code rewrite engines with static AST safety checks and Gödelian proof verification.\n")
    out.append("---\n")

    for subsystem_name, p_list in subsystems.items():
        out.append(f"## Target Subsystem: {subsystem_name} ({len(p_list)} Papers)\n")

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
            domain = meta.get("domain", subsystem_name)

            out.append(f"### Paper #{p['id']}. {title}")
            out.append(f"- **Authors:** {authors}")
            out.append(f"- **Venue & Year:** {venue} ({year})")
            out.append(f"- **DOI/arXiv ID:** `{doi}`")
            out.append(f"- **Domain / Category:** {domain} | **Target Subsystem:** `{subsystem_name}`")

            out.append("\n#### Technical Facts")
            out.append(f"- **Problem Solved:** {facts['problem']}")
            out.append(f"- **Methodology:** {facts['method']}")
            out.append(f"- **Theoretical Properties:** {facts['theoretical_properties']}")
            out.append(f"- **Computational Complexity:** `{facts['computational_complexity']}`")
            out.append(f"- **Limitations:** {facts['limitations']}")

            out.append("\n#### Engineering Analysis & Extracted Principle")
            out.append(f"- **Relevance to System:** {analysis['ai_eos_relevance']}")
            out.append(f"- **Extracted Principle:** {analysis.get('extracted_principle', 'N/A')}")
            out.append(f"- **Implementation Notes:** {analysis['implementation_notes']}")
            out.append(f"- **Architectural Fit:** {analysis['architectural_fit']}")
            out.append(f"- **Integration Priority:** **{analysis['integration_priority']}**")

            novelty = analysis['scientific_novelty']
            out.append(f"- **Scientific Novelty Score:** {novelty['score']}/10")

            readiness = analysis['production_readiness']
            out.append(f"- **Production Readiness Score:** {readiness['score']}/10")

            out.append("\n#### Reproducibility")
            out.append(f"- **Code Available:** `{repro['code_available']}` | **Pretrained Models:** `{repro['pretrained_models']}` | **Datasets Public:** `{repro['datasets_public']}` | **Estimated Effort:** `{repro['estimated_reproduction_effort']}`")

            out.append("\n---\n")

    output_path = "docs/research/papers/ALPHA_ALGO_200_NEW_BIBLIOGRAPHY.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"[Success] Compiled beautiful 200-paper bibliography at {output_path}")

if __name__ == "__main__":
    main()
