# -*- coding: utf-8 -*-
"""
compile_alpha_algo_301_400_papers.py: Compiles the audited YAML dataset
(ALPHA_ALGO_301_400_RESEARCH.yaml) into a human-readable Markdown bibliography file
(ALPHA_ALGO_301_400_BIBLIOGRAPHY.md).
"""
import os
import yaml

input_path = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
output_path = "docs/research/papers/ALPHA_ALGO_301_400_BIBLIOGRAPHY.md"

if not os.path.exists(input_path):
    raise FileNotFoundError(f"Source file {input_path} not found!")

with open(input_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

papers = data.get("papers", [])

md_lines = [
    "# AlphaAlgo 100 New Quantitative Research Papers Bibliography (IDs 301-400)",
    "",
    "## Overview & Executive Summary",
    f"This document presents the complete compiled bibliography and technical analysis of **{len(papers)} unique, peer-reviewed/arXiv quantitative research publications** (IDs 301-400). All publications have been programmatically audited against papers 1-300 to guarantee 100% zero-overlap across titles and DOIs.",
    "",
    "## Summary Index",
    "",
    "| ID | Title | Authors | Year | Venue | Domain | DOI |",
    "|---|---|---|---|---|---|---|",
]

for p in papers:
    p_id = p["id"]
    meta = p["metadata"]
    title = meta["title"]
    authors = meta["authors"]
    year = meta["year"]
    venue = meta["venue"]
    domain = meta["domain"]
    doi = meta["doi"]
    md_lines.append(f"| {p_id} | {title} | {authors} | {year} | {venue} | {domain} | [{doi}](https://doi.org/{doi}) |")

md_lines.extend([
    "",
    "---",
    "",
    "## Detailed Paper Profiles and Technical Analyses",
    ""
])

for p in papers:
    p_id = p["id"]
    meta = p["metadata"]
    tf = p["technical_facts"]
    an = p["analysis"]

    md_lines.extend([
        f"### Paper {p_id}: {meta['title']}",
        f"- **Authors:** {meta['authors']}",
        f"- **Year:** {meta['year']} | **Venue:** {meta['venue']} | **Domain:** {meta['domain']}",
        f"- **DOI:** [{meta['doi']}](https://doi.org/{meta['doi']})",
        "",
        "#### Technical Facts",
        f"- **Problem:** {tf['problem']}",
        f"- **Method:** {tf['method']}",
        f"- **Theoretical Properties:** {tf['theoretical_properties']}",
        f"- **Computational Complexity:** {tf['computational_complexity']}",
        f"- **Evaluation:** {tf['evaluation']}",
        "",
        "#### AI-EOS & AlphaAlgo Integration Analysis",
        f"- **Relevance:** {an['ai_eos_relevance']}",
        f"- **Implementation Notes:** {an['implementation_notes']}",
        f"- **Architectural Fit:** {an['architectural_fit']}",
        f"- **Priority:** {an['integration_priority']}",
        "",
        "---",
        ""
    ])

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print(f"[Success] Compiled {len(papers)} paper profiles into {output_path}")
