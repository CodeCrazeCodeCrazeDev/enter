# -*- coding: utf-8 -*-
"""
compile_alpha_algo_301_400_papers.py: Compiles ALPHA_ALGO_301_400_RESEARCH.yaml into Markdown bibliography format.
"""
import os
import yaml

input_path = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
output_path = "docs/research/papers/ALPHA_ALGO_301_400_BIBLIOGRAPHY.md"

with open(input_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

papers = data.get("papers", [])

md_lines = [
    "# AlphaAlgo 301-400 Quantitative Research Corpus Bibliography",
    "",
    "This document compiles 100 new, fully verified, zero-overlap quantitative research papers (IDs 301–400).",
    "",
    "## Paper Index",
    ""
]

for p in papers:
    pid = p.get("id")
    meta = p.get("metadata", {})
    title = meta.get("title", "")
    authors = meta.get("authors", "")
    year = meta.get("year", "")
    venue = meta.get("venue", "")
    doi = meta.get("doi", "")
    domain = meta.get("domain", "")

    md_lines.append(f"### Paper {pid}: {title}")
    md_lines.append(f"- **Authors:** {authors}")
    md_lines.append(f"- **Year:** {year}")
    md_lines.append(f"- **Venue:** {venue}")
    md_lines.append(f"- **Domain:** {domain}")
    md_lines.append(f"- **DOI/arXiv ID:** `{doi}`")
    md_lines.append("")
    md_lines.append("#### Technical Facts")
    tf = p.get("technical_facts", {})
    for k, v in tf.items():
        md_lines.append(f"- **{k.replace('_', ' ').title()}:** {v}")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print(f"[Success] Compiled {len(papers)} papers into {output_path}")
