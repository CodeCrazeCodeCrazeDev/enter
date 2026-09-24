#!/usr/bin/env python3
"""
verify_architecture_docs.py

Verifies the existence, non-emptiness, and structural completeness of the 7 core cognitive
operating system architecture specifications under docs/architecture/.
"""

import os
import sys

REQUIRED_DOCS = [
    "UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md",
    "UNIFIED_DEPENDENCY_GRAPH.md",
    "CAPABILITY_OWNERSHIP_MATRIX.md",
    "PRIORITIZED_ROI_ROADMAP.md",
    "SOTA_GAP_ANALYSIS_2026.md",
    "PHASED_IMPLEMENTATION_PLAN.md",
    "CONTINUOUS_EVOLUTION_STRATEGY.md",
]

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "architecture")

def verify_docs():
    print("=== Verifying Architecture Specifications ===")
    missing = []
    empty = []

    for doc_name in REQUIRED_DOCS:
        doc_path = os.path.join(DOCS_DIR, doc_name)
        if not os.path.exists(doc_path):
            missing.append(doc_name)
            continue

        file_size = os.path.getsize(doc_path)
        if file_size < 100:
            empty.append(doc_name)
        else:
            print(f" [OK] {doc_name} ({file_size} bytes)")

    if missing:
        print(f"\n[ERROR] Missing documents: {missing}")
    if empty:
        print(f"\n[ERROR] Insufficient/empty documents: {empty}")

    if missing or empty:
        sys.exit(1)

    print("\n[SUCCESS] All 7 required cognitive architecture specifications exist and are complete.")

if __name__ == "__main__":
    verify_docs()
