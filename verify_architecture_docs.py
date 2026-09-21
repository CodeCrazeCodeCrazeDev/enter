#!/usr/bin/env python3
"""Verification script for the 7 required Cognitive Architecture specifications in docs/architecture/."""

from __future__ import annotations

import os
import sys

REQUIRED_DOCS = [
    "docs/architecture/UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md",
    "docs/architecture/UNIFIED_DEPENDENCY_GRAPH.md",
    "docs/architecture/PRIORITIZED_ROI_ROADMAP.md",
    "docs/architecture/SOTA_GAP_ANALYSIS_2026.md",
    "docs/architecture/PHASED_IMPLEMENTATION_PLAN.md",
    "docs/architecture/CONTINUOUS_EVOLUTION_STRATEGY.md",
    "docs/architecture/CAPABILITY_OWNERSHIP_MATRIX.md",
]

MIN_FILE_BYTES = 1000


def verify_architecture_docs() -> bool:
    print("=== Auditing Cognitive Architecture Documentation Specifications ===")
    all_passed = True

    for doc_path in REQUIRED_DOCS:
        if not os.path.exists(doc_path):
            print(f"[FAIL] Missing required document: {doc_path}")
            all_passed = False
            continue

        size = os.path.getsize(doc_path)
        if size < MIN_FILE_BYTES:
            print(f"[FAIL] Document {doc_path} is too small ({size} bytes < {MIN_FILE_BYTES} bytes)")
            all_passed = False
            continue

        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("#"):
            print(f"[FAIL] Document {doc_path} missing top-level H1 title header")
            all_passed = False
            continue

        print(f"[OK] Verified {doc_path} ({size} bytes)")

    if all_passed:
        print("\nSUCCESS: All 7 required Cognitive Architecture specifications verified successfully!")
        return True
    else:
        print("\nFAILURE: One or more architecture specifications failed verification.")
        return False


if __name__ == "__main__":
    success = verify_architecture_docs()
    sys.exit(0 if success else 1)
