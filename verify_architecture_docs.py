#!/usr/bin/env python3
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

def main():
    missing = []
    empty = []
    for filepath in REQUIRED_DOCS:
        if not os.path.exists(filepath):
            missing.append(filepath)
        elif os.path.getsize(filepath) < 100:
            empty.append(filepath)

    if missing or empty:
        print(f"Verification failed: missing={missing}, empty={empty}")
        sys.exit(1)

    print("Architecture docs verification passed successfully!")

if __name__ == "__main__":
    main()
