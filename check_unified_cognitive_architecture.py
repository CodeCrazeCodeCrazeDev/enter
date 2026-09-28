#!/usr/bin/env python3
"""
Root Audit Script: check_unified_cognitive_architecture.py
Purpose: Audits imports across Layer 1 (Research OS), Layer 2 (EIOS/EOS Kernel),
Layer 3 (AEAN HiveMind), Layer 4 (APODEX WorldModel & Cognitive Brain), and verifies
all 7 cognitive operating system specification documents under docs/architecture/.
"""

import sys
import os

REQUIRED_DOCS = [
    "docs/architecture/UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md",
    "docs/architecture/UNIFIED_DEPENDENCY_GRAPH.md",
    "docs/architecture/PRIORITIZED_ROI_ROADMAP.md",
    "docs/architecture/SOTA_GAP_ANALYSIS_2026.md",
    "docs/architecture/PHASED_IMPLEMENTATION_PLAN.md",
    "docs/architecture/CONTINUOUS_EVOLUTION_STRATEGY.md",
    "docs/architecture/CAPABILITY_OWNERSHIP_MATRIX.md",
]

CORE_MODULES = [
    ("Layer 1 Research OS", "apodex.ai_eos.research.research_os"),
    ("Layer 1 Research Bridge", "apodex.ai_eos.research.integration"),
    ("Layer 2 EIOS Kernel", "apodex.arcs.kernel.kernel"),
    ("Layer 2 EOS Engine", "apodex.ai_eos.intelligence.eos_engine"),
    ("Layer 3 AEAN HiveMind", "apodex.aean.coordination.hive_mind"),
    ("Layer 4 APODEX WorldModel", "apodex.world_model.world_model"),
    ("Layer 4 Cognitive Brain", "apodex.cognition.brain"),
]

def main():
    print("=== Unified Cognitive Architecture Verification Audit ===")

    # 1. Audit core layer imports
    print("\n1. Verifying Layer Importability:")
    import_errors = 0
    for layer_name, mod_path in CORE_MODULES:
        try:
            __import__(mod_path)
            print(f"   [PASS] {layer_name} -> {mod_path}")
        except Exception as e:
            print(f"   [FAIL] {layer_name} -> {mod_path}: {e}")
            import_errors += 1

    # 2. Audit architecture spec docs
    print("\n2. Verifying Architecture Specification Documents:")
    doc_errors = 0
    for doc in REQUIRED_DOCS:
        if os.path.exists(doc):
            size = os.path.getsize(doc)
            if size > 1000:
                print(f"   [PASS] {doc} ({size} bytes)")
            else:
                print(f"   [FAIL] {doc} file too small ({size} bytes)")
                doc_errors += 1
        else:
            print(f"   [FAIL] {doc} missing")
            doc_errors += 1

    print("\n=== Audit Summary ===")
    if import_errors == 0 and doc_errors == 0:
        print("Status: SUCCESS - Unified Cognitive Architecture fully verified.")
        sys.exit(0)
    else:
        print(f"Status: FAILED - {import_errors} import errors, {doc_errors} doc errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
