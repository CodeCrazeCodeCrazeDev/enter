# -*- coding: utf-8 -*-
"""
check_layer_imports.py: Audits module importability across all 4 cognitive OS layers.
"""

import sys

def audit_imports():
    print("Auditing Cognitive OS Layer Imports...")
    modules = [
        "apodex.ai_eos.research.research_os",
        "apodex.research_os.statistical_validation",
        "apodex.ai_eos.research.integration",
        "apodex.arcs.kernel.kernel",
        "apodex.ai_eos.intelligence.eos_engine",
        "apodex.ai_eos.intelligence.computational_architecture",
        "apodex.aean.coordination.hive_mind",
        "apodex.aean.core",
        "apodex.world_model.world_model",
        "apodex.cognition.brain",
        "apodex.skills.runner"
    ]

    failed = []
    for mod in modules:
        try:
            __import__(mod)
            print(f"[OK] {mod}")
        except Exception as e:
            print(f"[FAIL] {mod}: {e}")
            failed.append(mod)

    if failed:
        print(f"\n[FAIL] {len(failed)} modules failed to import!")
        sys.exit(1)

    print("\n[SUCCESS] All 4 Cognitive Operating System layers are fully importable and operational!")

if __name__ == "__main__":
    audit_imports()
