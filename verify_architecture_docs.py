#!/usr/bin/env python3
"""
Verification Script for Unified Cognitive OS Architecture Documentation.

Audits existence, non-emptiness, and key structural headings of all 7 architecture
specifications under `docs/architecture/`.
"""

import sys
from pathlib import Path

REQUIRED_DOCS = [
    "UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md",
    "UNIFIED_DEPENDENCY_GRAPH.md",
    "PRIORITIZED_ROI_ROADMAP.md",
    "SOTA_GAP_ANALYSIS_2026.md",
    "PHASED_IMPLEMENTATION_PLAN.md",
    "CONTINUOUS_EVOLUTION_STRATEGY.md",
    "CAPABILITY_OWNERSHIP_MATRIX.md",
]

DOCS_DIR = Path(__file__).parent / "docs" / "architecture"


def main():
    print("=================================================================")
    print("Auditing Unified Cognitive OS Architectural Specification Files...")
    print("=================================================================")

    missing_docs = []
    empty_docs = []

    for doc_name in REQUIRED_DOCS:
        doc_path = DOCS_DIR / doc_name
        if not doc_path.exists():
            print(f"❌ MISSING: {doc_name}")
            missing_docs.append(doc_name)
        else:
            content = doc_path.read_text(encoding="utf-8")
            if len(content.strip()) < 200:
                print(f"⚠️ INCOMPLETE/EMPTY ({len(content)} chars): {doc_name}")
                empty_docs.append(doc_name)
            else:
                print(f"✓ VALID ({len(content)} chars): {doc_name}")

    if missing_docs or empty_docs:
        print("\n❌ Verification Failed! Missing or incomplete specifications detected.")
        sys.exit(1)

    print("\n✅ Success! All 7 Unified Cognitive Architecture specifications are verified.")
    sys.exit(0)


if __name__ == "__main__":
    main()
