# -*- coding: utf-8 -*-
"""
verify_architecture_docs.py: Verification script for cognitive OS architecture specifications.
"""

import os
import sys

REQUIRED_DOCS = [
    "docs/architecture/UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md",
    "docs/architecture/UNIFIED_DEPENDENCY_GRAPH.md",
    "docs/architecture/PRIORITIZED_ROI_ROADMAP.md",
    "docs/architecture/SOTA_GAP_ANALYSIS_2026.md",
    "docs/architecture/PHASED_IMPLEMENTATION_PLAN.md",
    "docs/architecture/CONTINUOUS_EVOLUTION_STRATEGY.md",
    "docs/architecture/CAPABILITY_OWNERSHIP_MATRIX.md"
]

def main():
    print("Verifying Cognitive OS Architecture Specifications...")
    missing = []
    for doc_path in REQUIRED_DOCS:
        if not os.path.exists(doc_path):
            missing.append(doc_path)
        else:
            size = os.path.getsize(doc_path)
            if size < 200:
                print(f"[WARN] File {doc_path} exists but is unexpectedly small ({size} bytes).")
            else:
                print(f"[OK] {doc_path} ({size} bytes)")

    if missing:
        print(f"\n[FAIL] Missing required specification documents: {missing}")
        sys.exit(1)

    print("\n[SUCCESS] All 7 Cognitive OS Architecture Specifications are verified and present!")

if __name__ == "__main__":
    main()
