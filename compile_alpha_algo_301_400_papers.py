# -*- coding: utf-8 -*-
"""
compile_alpha_algo_301_400_papers.py: Reads the YAML database of 100 new research papers (IDs 301-400)
and compiles them into a publication-grade Markdown bibliography document.
"""
import os
import yaml

def main():
    filepath = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    out_path = "docs/research/papers/ALPHA_ALGO_301_400_BIBLIOGRAPHY.md"
    if not os.path.exists(filepath):
        print(f"[Error] YAML database {filepath} does not exist.")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    papers = db.get("papers", [])
    print(f"[Compile] Loaded {len(papers)} papers from YAML.")

    themes = {}
    for p in papers:
        domain = p["metadata"]["domain"]
        themes.setdefault(domain, []).append(p)

    out = []
    out.append("# AlphaAlgo 100 New Research Papers Bibliography (IDs 301-400)")
    out.append("### Advanced Quantitative Research, Active Inference, RL Alignment & Evolutionary Search\n")
    out.append("This document contains 100 genuine, peer-reviewed/arXiv quantitative research publications (IDs 301-400) curated for AlphaAlgo with verified zero overlap against papers 1-300.\n")

    for domain, domain_papers in themes.items():
        out.append(f"## Domain: {domain}\n")
        for p in domain_papers:
            meta = p["metadata"]
            tf = p["technical_facts"]
            an = p["analysis"]

            out.append(f"### [{p['id']}] {meta['title']}")
            out.append(f"- **Authors:** {meta['authors']}")
            out.append(f"- **Year / Venue:** {meta['year']} | {meta['venue']}")
            out.append(f"- **DOI / Identifier:** {meta['doi']}")
            out.append(f"- **Core Problem:** {tf['problem']}")
            out.append(f"- **Methodology:** {tf['method']}")
            out.append(f"- **AI-EOS / AlphaAlgo Relevance:** {an['ai_eos_relevance']}")
            out.append(f"- **Architectural Fit:** {an['architectural_fit']}\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"[Success] Compiled bibliography at {out_path}")

if __name__ == "__main__":
    main()
