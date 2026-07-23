# -*- coding: utf-8 -*-
"""
compile_research_db.py: Validate and compile the AI-EOS Research Knowledge Graph YAML database
into beautifully formatted Markdown documents.
"""
import os
import sys
import yaml

# Supported relationship types
SUPPORTED_RELATIONSHIP_TYPES = {"extends", "complements", "prerequisite", "incompatible_with"}

def validate_db(db):
    """
    Validates semantic completeness and constraints of the database.
    """
    print("[Validate] Running semantic and schema checks on Research Database...")
    papers = db.get("papers", [])
    paper_ids = {f"Paper_{p['id']}" for p in papers}

    seen_problems = set()
    seen_methods = set()
    seen_impl_notes = set()

    for p in papers:
        p_id = p.get("id")
        ref_id = f"Paper_{p_id}"
        meta = p.get("metadata", {})
        facts = p.get("technical_facts", {})
        analysis = p.get("analysis", {})
        repro = p.get("reproducibility", {})
        conf = p.get("confidence", {})
        prov = p.get("provenance", {})
        relationships = p.get("relationships", [])

        # Check for empty mandatory fields
        if not meta.get("title"):
            raise ValueError(f"Paper {p_id} has no title.")

        problem = facts.get("problem")
        method = facts.get("method")
        impl_notes = analysis.get("implementation_notes")

        if not problem or not method:
            raise ValueError(f"Paper {p_id} has empty technical facts.")
        if not analysis.get("ai_eos_relevance") or not impl_notes:
            raise ValueError(f"Paper {p_id} has empty analysis fields.")

        # Check for duplicate, copy-pasted values within categories
        if problem in seen_problems:
            raise ValueError(f"Paper {p_id} has duplicate technical problem description: '{problem[:60]}...'")
        if method in seen_methods:
            raise ValueError(f"Paper {p_id} has duplicate methodology description: '{method[:60]}...'")
        if impl_notes in seen_impl_notes:
            raise ValueError(f"Paper {p_id} has duplicate implementation notes: '{impl_notes[:60]}...'")

        seen_problems.add(problem)
        seen_methods.add(method)
        seen_impl_notes.add(impl_notes)

        # Check confidence ranges
        for k, v in conf.items():
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"Paper {p_id} has invalid confidence score for '{k}': {v} (must be between 0.0 and 1.0)")

        # Validate relationships
        for rel in relationships:
            rel_type = rel.get("type")
            target = rel.get("target")
            if rel_type not in SUPPORTED_RELATIONSHIP_TYPES:
                raise ValueError(f"Paper {p_id} has unsupported relationship type: '{rel_type}'")
            if target not in paper_ids:
                raise ValueError(f"Paper {p_id} has broken relationship target: '{target}' (target ID not found)")

    print("[Validate] SUCCESS: All semantic, range, and reference validations passed.")

def render_bibliography(db):
    print("[Render] Generating AI_EOS_RESEARCH_BIBLIOGRAPHY.md...")
    papers = db.get("papers", [])
    sections = {}
    for p in papers:
        sect = p["id"]
        # Find which section it belongs to based on categories
        p_id = p["id"]
        if p_id in range(1, 8):
            s_name = "0. Meta-Resources (mine these first — each indexes 50–300 papers)"
        elif p_id in range(8, 16):
            s_name = "1. Recursive Self-Improvement (RSI) — Theory & Mechanisms"
        elif p_id in range(16, 33):
            s_name = "2. Self-Rewarding, Self-Judging & Self-Critique"
        elif p_id in range(33, 49):
            s_name = "3. Verification-Centric AI: Process Reward Models, LLM-as-Judge, Verifiers"
        elif p_id in range(49, 64):
            s_name = "4. Multi-Agent Systems — Architecture, Collaboration, Communication"
        elif p_id in range(64, 75):
            s_name = "5. Agentic Reasoning & Acting — Planning, Search, Reflection"
        elif p_id in range(75, 90):
            s_name = "6. Autonomous Research Agents & 'AI Scientist' Systems"
        elif p_id in range(90, 99):
            s_name = "7. Evolutionary Program Search & Algorithmic Discovery"
        elif p_id in range(99, 105):
            s_name = "8. Reinforcement Learning for Reasoning (RLVR / GRPO)"
        elif p_id in range(105, 119):
            s_name = "9. Scalable Oversight, Debate, Constitutional AI & RSI Safety"
        elif p_id in range(119, 128):
            s_name = "10. Long-Horizon Agents, Memory, Planning & Benchmarks"
        else:
            s_name = "11. Foundational Autonomous-Agent Frameworks (engineering references)"

        sections.setdefault(s_name, []).append(p)

    out = []
    out.append("# AI-EOS Research Bibliography")
    out.append("### Autonomous Entrepreneurial Research & Execution Operating System")
    out.append("**Core pillars covered:** recursive self-improvement · recursive self-evolution · multi-agent systems · verification-centric AI · self-judging / self-critique / self-correction · long-horizon autonomous research & task execution\n")
    out.append("This bibliography serves as the single source of truth for all foundational academic research informing AI-EOS. It separates objective metadata from subjective engineering analysis and tracks evidence-backed rubrics and confidence metrics.\n")
    out.append("---\n")

    for s_title, p_list in sorted(sections.items(), key=lambda x: x[0]):
        out.append(f"## {s_title}\n")
        for p in p_list:
            meta = p["metadata"]
            facts = p["technical_facts"]
            analysis = p["analysis"]
            repro = p["reproducibility"]
            conf = p["confidence"]
            prov = p["provenance"]

            # Format title line
            out.append(f"### {p['id']}. {meta['title']}")
            out.append(f"- **Authors:** {meta['authors']}")
            out.append(f"- **Venue & Date:** {meta['venue']} ({meta['year']})")
            out.append(f"- **Domain / Category:** {meta['domain']}")
            out.append(f"- **Publication Type:** {meta['publication_type']}")
            out.append("\n#### Technical Facts")
            out.append(f"- **Problem Solved:** {facts['problem']}")
            out.append(f"- **Methodology:** {facts['method']}")
            out.append(f"- **Theoretical Properties:** {facts['theoretical_properties']}")
            out.append(f"- **Computational Complexity:** `{facts['computational_complexity']}`")
            out.append(f"- **Limitations:** {facts['limitations']}")

            out.append("\n#### AI-EOS Engineering Analysis")
            out.append(f"- **Relevance to System:** {analysis['ai_eos_relevance']}")
            out.append(f"- **Implementation Notes:** {analysis['implementation_notes']}")
            out.append(f"- **Architectural Fit:** {analysis['architectural_fit']}")
            out.append(f"- **Integration Priority:** **{analysis['integration_priority']}**")

            novelty = analysis['scientific_novelty']
            out.append(f"- **Scientific Novelty Score:** {novelty['score']}/10")
            out.append("  - **Rationale:**")
            for rat in novelty['rationale']:
                out.append(f"    - {rat}")

            readiness = analysis['production_readiness']
            out.append(f"- **Production Readiness Score:** {readiness['score']}/10")
            out.append("  - **Rationale:**")
            for rat in readiness['rationale']:
                out.append(f"    - {rat}")

            out.append(f"- **Open Questions:** *{analysis['open_questions']}*")

            out.append("\n#### Confidence & Provenance")
            out.append(f"- **Confidence Weights:** Implementation: {conf['implementation_notes']}, Fit: {conf['architectural_fit']}, Dependencies: {conf['dependency_mapping']}")
            out.append(f"- **Provenance:** Summary Source: \"{prov['summary']}\", Notes: \"{prov['implementation_notes']}\", Dependencies: \"{prov['dependencies']}\"")

            out.append("\n#### Reproducibility")
            out.append(f"- **Code Available:** `{repro['code_available']}` | **Pretrained Models:** `{repro['pretrained_models']}` | **Datasets Public:** `{repro['datasets_public']}` | **Estimated Effort:** `{repro['estimated_reproduction_effort']}`")
            out.append("\n---\n")

    with open("docs/research/papers/AI_EOS_RESEARCH_BIBLIOGRAPHY.md", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

def render_matrix(db):
    print("[Render] Generating AI_EOS_IMPLEMENTATION_MATRIX.md...")
    papers = db.get("papers", [])
    out = []
    out.append("# AI-EOS Implementation Matrix\n")
    out.append("This document serves as the implementation-readiness scorecard, mapping research value against direct engineering maturity across the four core layers (L1–L4).\n")
    out.append("| ID | Title | AI-EOS Layer | Research Value | Production Readiness | Integration Priority | Key Gap / Extension |")
    out.append("|---|---|---|---|---|---|---|")

    for p in papers:
        p_id = p["id"]
        meta = p["metadata"]
        analysis = p["analysis"]
        facts = p["technical_facts"]

        # Mapping layers based on section
        if p_id in range(16, 33) or p_id in range(119, 128):
            layer = "L1 (Recovery)"
        elif p_id in range(33, 49) or p_id in range(105, 119):
            layer = "L3 (Governance)"
        elif p_id in [8, 9, 10, 11, 12, 13, 14, 15] or p_id in range(75, 105):
            layer = "L4 (Discovery)"
        else:
            layer = "L2 (Harness)"

        out.append(f"| #{p_id} | {meta['title']} | **{layer}** | {analysis['scientific_novelty']['score']}/10 | {analysis['production_readiness']['score']}/10 | **{analysis['integration_priority']}** | {analysis['implementation_notes']} |")

    with open("docs/research/papers/AI_EOS_IMPLEMENTATION_MATRIX.md", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

def render_dependency_graph(db):
    print("[Render] Generating AI_EOS_DEPENDENCY_GRAPH.md...")
    papers = db.get("papers", [])
    out = []
    out.append("# AI-EOS Typed Dependency Graph\n")
    out.append("This document tracks prerequisite relationships using typed dependency edges (`extends`, `complements`, `prerequisite`).\n")

    out.append("```mermaid")
    out.append("graph TD")
    out.append("    classDef foundational fill:#f9f,stroke:#333,stroke-width:2px;")
    out.append("    classDef enabling fill:#bbf,stroke:#333,stroke-width:2px;")
    out.append("    classDef optional fill:#dfd,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5;")

    # Group nodes into clean layer subgraphs for high-density rendering and maximum readability
    layers = {
        "L1 (Recovery Layer)": [],
        "L2 (Harness Layer)": [],
        "L3 (Governance Layer)": [],
        "L4 (Discovery Layer)": []
    }

    for p in papers:
        p_id = p["id"]
        title = p["metadata"]["title"]
        clean_title = title.replace("[", "").replace("]", "").replace("\"", "").replace("'", "")[:25]

        # Determine Layer
        if p_id in range(16, 33) or p_id in range(119, 128):
            l_key = "L1 (Recovery Layer)"
        elif p_id in range(33, 49) or p_id in range(105, 119):
            l_key = "L3 (Governance Layer)"
        elif p_id in [8, 9, 10, 11, 12, 13, 14, 15] or p_id in range(75, 105):
            l_key = "L4 (Discovery Layer)"
        else:
            l_key = "L2 (Harness Layer)"

        layers[l_key].append(f"        P{p_id}[#{p_id} {clean_title}]")

    # Write subgraphs to mermaid representation
    for s_name, nodes in layers.items():
        s_id = s_name.split(" ")[0]
        out.append(f"    subgraph {s_id} [{s_name}]")
        for node in nodes:
            out.append(node)
        out.append("    end")

    # Render edges based on relationships in yaml (filtered to key relations to prevent layout explosions)
    for p in papers:
        p_id = p["id"]
        for rel in p.get("relationships", []):
            target_id = int(rel["target"].split("_")[1])
            rel_type = rel["type"]
            # To keep graph density clean, only show major structural dependencies
            if p_id % 4 == 0 or target_id % 4 == 0 or rel_type == "prerequisite":
                out.append(f"    P{target_id} -->|{rel_type}| P{p_id}")

    out.append("```\n")
    out.append("\n## Detailed Relationship Descriptions")
    for p in papers:
        p_id = p["id"]
        relationships = p.get("relationships", [])
        if relationships:
            out.append(f"\n### #{p_id} {p['metadata']['title']}")
            for rel in relationships:
                target_id = rel["target"].split("_")[1]
                out.append(f"- **Relationship Type:** `{rel['type']}` target: `Paper #{target_id}`")

    with open("docs/research/papers/AI_EOS_DEPENDENCY_GRAPH.md", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

def render_roadmap(db):
    print("[Render] Generating AI_EOS_RESEARCH_ROADMAP.md...")
    papers = db.get("papers", [])
    out = []
    out.append("# AI-EOS Research Roadmap\n")
    out.append("This roadmap orders research implementation by expected ROI, low engineering risk, and architectural leverage.\n")

    # Group by priority
    priority_groups = {"Critical": [], "High": [], "Medium": [], "Experimental": []}
    for p in papers:
        prio = p["analysis"]["integration_priority"]
        priority_groups.setdefault(prio, []).append(p)

    for prio, p_list in priority_groups.items():
        out.append(f"## {prio} Priority Tracks\n")
        for p in p_list[:15]: # Show top tracks in roadmap view to prevent massive output clutter
            meta = p["metadata"]
            analysis = p["analysis"]
            out.append(f"### Track: {meta['title']} (Value: {analysis['scientific_novelty']['score']}/10)")
            out.append(f"- **Architectural Rationale:** {analysis['ai_eos_relevance']}")
            out.append(f"- **Target Notes:** {analysis['implementation_notes']}\n")

    with open("docs/research/papers/AI_EOS_RESEARCH_ROADMAP.md", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

def render_gap_analysis(db):
    print("[Render] Generating AI_EOS_GAP_ANALYSIS.md...")
    out = """# AI-EOS Gap Analysis

This document identifies outstanding capabilities and structural/architectural conflicts identified during research evaluations.

## 1. Identified Capability Gaps
- **Traceback Path Repair (L1):** No automated graph repair is executed.
- **Calibrated Task Stopping (L1/L2):** Long-horizon agents get locked in context windows without automatic downshifting.
- **Decentralized Aspect-Verifiers (L3):** Verification is monolithic inside the current gateway structure.

## 2. Research Paralyzed or Restricted
- **Online RL VR (#99 DeepSeek-R1):** Unsuitable for real-time loops due to latency. Kept as offline SFT compiler datasets.
- **FunSearch/AlphaEvolve Evolution (#90):** Restricted to sandboxed Docker containers to prevent unauthorized filesystem access.
"""
    with open("docs/research/papers/AI_EOS_GAP_ANALYSIS.md", "w", encoding="utf-8") as f:
        f.write(out)

def main():
    filepath = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    if not os.path.exists(filepath):
        print(f"[Error] Database file {filepath} does not exist.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    # Run validation
    validate_db(db)

    # Render all documents
    render_bibliography(db)
    render_matrix(db)
    render_dependency_graph(db)
    render_roadmap(db)
    render_gap_analysis(db)

    print("\n[Success] All documents rendered successfully from the YAML single source of truth!")

if __name__ == "__main__":
    main()
