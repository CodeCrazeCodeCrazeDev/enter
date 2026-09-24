#!/usr/bin/env python3
"""
check_layer_imports.py

Audits module importability and structural integrity across Layer 1 (Research OS),
Layer 2 (EIOS/EOS), Layer 3 (AEAN HiveMind), and Layer 4 (APODEX WorldModel).
"""

import os
import sys
import importlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LAYER_MODULES = {
    "Layer 1 (Research OS)": [
        "apodex.ai_eos.research.research_os",
        "apodex.research_os.statistical_validation",
        "apodex.research_os.reproducibility",
    ],
    "Layer 2 (EIOS / EOS)": [
        "apodex.arcs.kernel.kernel",
        "apodex.ai_eos.intelligence.eos_engine",
        "apodex.ai_eos.intelligence.computational_architecture",
    ],
    "Layer 3 (AEAN)": [
        "apodex.aean.coordination.hive_mind",
        "apodex.ai_eos.research.integration",
    ],
    "Layer 4 (APODEX)": [
        "apodex.world_model.domain.entities",
        "apodex.world_model.domain.beliefs",
        "apodex.cognition.brain",
        "apodex.world_model.governance.approval",
    ],
}

def audit_layer_imports():
    print("=== Auditing 4-Layer System Imports ===")
    has_errors = False

    for layer_name, modules in LAYER_MODULES.items():
        print(f"\n[{layer_name}]")
        for mod in modules:
            try:
                importlib.import_module(mod)
                print(f"  [PASS] {mod}")
            except Exception as e:
                print(f"  [FAIL] {mod}: {e}")
                has_errors = True

    if has_errors:
        print("\n[ERROR] System layer import verification failed.")
        sys.exit(1)

    print("\n[SUCCESS] All 4 system layers imported cleanly with zero errors.")

if __name__ == "__main__":
    audit_layer_imports()
