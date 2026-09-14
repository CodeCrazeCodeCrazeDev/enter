#!/usr/bin/env python3
"""
Verification script for Cognitive Operating System architecture specifications.
Audits existence and minimum file size of all 6 required specifications under docs/architecture/.
"""

import os
import sys

REQUIRED_DOCS = [
    "UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md",
    "UNIFIED_DEPENDENCY_GRAPH.md",
    "PRIORITIZED_ROI_ROADMAP.md",
    "SOTA_GAP_ANALYSIS_2026.md",
    "PHASED_IMPLEMENTATION_PLAN.md",
    "CONTINUOUS_EVOLUTION_STRATEGY.md",
]

DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs", "architecture")

def verify_docs():
    print("=== Auditing Cognitive Operating System Architecture Specifications ===")
    missing_files = []
    undersized_files = []

    for doc in REQUIRED_DOCS:
        filepath = os.path.join(DOCS_DIR, doc)
        if not os.path.exists(filepath):
            missing_files.append(doc)
            print(f"❌ Missing: {doc}")
        else:
            size = os.path.getsize(filepath)
            if size < 500:
                undersized_files.append((doc, size))
                print(f"⚠️  Undersized: {doc} ({size} bytes)")
            else:
                print(f"✅ Verified: {doc} ({size} bytes)")

    if missing_files or undersized_files:
        print("\n❌ Verification Failed!")
        if missing_files:
            print(f"Missing files: {missing_files}")
        if undersized_files:
            print(f"Undersized files: {undersized_files}")
        sys.exit(1)

    print("\n🎉 All 6 Architecture Specifications verified successfully!")

if __name__ == "__main__":
    verify_docs()
