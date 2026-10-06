#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_unified_cognitive_architecture.py: Audit script to verify documentation presence,
non-emptiness, and core layer module importability across the Unified Cognitive OS.
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

def check_docs() -> bool:
    print("=== Auditing Core Architecture Specifications ===")
    all_ok = True
    for doc in REQUIRED_DOCS:
        if not os.path.exists(doc):
            print(f"[FAIL] Missing required specification document: {doc}")
            all_ok = False
        else:
            size = os.path.getsize(doc)
            if size < 500:
                print(f"[FAIL] Specification document is too small ({size} bytes): {doc}")
                all_ok = False
            else:
                print(f"[OK] {doc} ({size} bytes)")
    return all_ok

def check_imports() -> bool:
    print("\n=== Auditing Core Layer Imports ===")
    try:
        import apodex.ai_eos.research.research_os
        import apodex.arcs.kernel.kernel
        import apodex.ai_eos.intelligence.eos_engine
        import apodex.aean.coordination.hive_mind
        import apodex.world_model.world_model
        from apodex.ai_eos.research.integration import ResearchToSystemBridge
        from apodex.ai_eos.intelligence import EOSEngine, EntrepreneurialIntelligenceOrchestrator
        print("[OK] All core cognitive OS modules imported successfully!")
        return True
    except Exception as e:
        print(f"[FAIL] Import error: {e}")
        return False

def main():
    docs_ok = check_docs()
    imports_ok = check_imports()

    if docs_ok and imports_ok:
        print("\nSUCCESS: All Unified Cognitive Architecture audits passed!")
        sys.exit(0)
    else:
        print("\nFAILURE: Unified Cognitive Architecture audit failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
