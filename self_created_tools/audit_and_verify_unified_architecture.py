#!/usr/bin/env python3
"""
self_created_tools/audit_and_verify_unified_architecture.py

Audits the 4-layer cognitive architecture specifications and validates the structural integrity
and importability of core layer modules in apodex/.
"""

import os
import sys
import importlib

# Ensure repository root is on PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REQUIRED_DOCS = [
    "docs/architecture/UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md",
    "docs/architecture/UNIFIED_DEPENDENCY_GRAPH.md",
    "docs/architecture/CAPABILITY_OWNERSHIP_MATRIX.md",
    "docs/architecture/PRIORITIZED_ROI_ROADMAP.md",
    "docs/architecture/SOTA_GAP_ANALYSIS_2026.md",
    "docs/architecture/PHASED_IMPLEMENTATION_PLAN.md",
    "docs/architecture/CONTINUOUS_EVOLUTION_STRATEGY.md",
]

CORE_MODULES = [
    "apodex.ai_eos.research.research_os",
    "apodex.research_os.statistical_validation",
    "apodex.arcs.kernel.kernel",
    "apodex.ai_eos.intelligence.eos_engine",
    "apodex.ai_eos.intelligence.computational_architecture",
    "apodex.aean.coordination.hive_mind",
    "apodex.ai_eos.research.integration",
    "apodex.world_model.domain.beliefs",
    "apodex.cognition.brain",
]

def main():
    print("=== Auditing Unified Architecture Documents & Subsystem Modules ===")

    # 1. Audit Documents
    print("\n1. Checking Architecture Documents:")
    doc_errors = False
    for doc_path in REQUIRED_DOCS:
        if not os.path.exists(doc_path):
            print(f" [FAIL] Missing: {doc_path}")
            doc_errors = True
        else:
            size = os.path.getsize(doc_path)
            if size < 200:
                print(f" [FAIL] Too small ({size} bytes): {doc_path}")
                doc_errors = True
            else:
                print(f" [PASS] Valid ({size} bytes): {doc_path}")

    if doc_errors:
        print("\n[ERROR] Document audit failed.")
        sys.exit(1)

    # 2. Audit Core Layer Imports
    print("\n2. Checking Core Layer Importability:")
    import_errors = False
    for mod_name in CORE_MODULES:
        try:
            importlib.import_module(mod_name)
            print(f" [PASS] Imported: {mod_name}")
        except Exception as e:
            print(f" [FAIL] Import error for {mod_name}: {e}")
            import_errors = True

    if import_errors:
        print("\n[ERROR] Core layer import audit failed.")
        sys.exit(1)

    print("\n[SUCCESS] Unified Architecture audit passed with 100% compliance!")

if __name__ == "__main__":
    main()
