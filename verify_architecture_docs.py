#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_architecture_docs.py: Audits existence and completeness of all required
cognitive operating system architecture specifications under docs/architecture/.
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
    "docs/architecture/CAPABILITY_OWNERSHIP_MATRIX.md",
]

def main() -> int:
    print("=== Auditing Cognitive Architecture Documentation ===")
    missing = []
    too_small = []

    for path in REQUIRED_DOCS:
        if not os.path.exists(path):
            missing.append(path)
            print(f"[FAIL] Missing file: {path}")
        else:
            size = os.path.getsize(path)
            if size < 500:
                too_small.append((path, size))
                print(f"[FAIL] File too small ({size} bytes): {path}")
            else:
                print(f"[OK] {path} ({size} bytes)")

    if missing or too_small:
        print("\nAudit Failed! Some architecture specifications are missing or incomplete.")
        return 1

    print("\nAudit Passed! All 7 architecture specifications are present and verified.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
