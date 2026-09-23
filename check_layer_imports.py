#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_layer_imports.py: Audits module importability and structural integrity across all 4 layers
of the unified cognitive operating system (Research OS, EIOS/EOS, AEAN, APODEX).
"""

import sys
import importlib

LAYER_MODULES = [
    ("Layer 1 Research OS", "apodex.ai_eos.research.integration"),
    ("Layer 1 Research OS", "apodex.ai_eos.research.research_os"),
    ("Layer 1 Research OS", "apodex.research_os"),
    ("Layer 2 EIOS Kernel", "apodex.arcs.kernel.kernel"),
    ("Layer 2 EOS Engine", "apodex.ai_eos.intelligence.eos_engine"),
    ("Layer 3 AEAN HiveMind", "apodex.aean.coordination.hive_mind"),
    ("Layer 4 APODEX WorldModel", "apodex.world_model.world_model"),
    ("Layer 4 CMOS Memory", "apodex.memory.cmos.operators"),
]

def main() -> int:
    print("=== Auditing Subsystem Module Importability Across 4 Layers ===")
    failures = []

    for layer, module_name in LAYER_MODULES:
        try:
            mod = importlib.import_module(module_name)
            print(f"[OK] {layer}: successfully imported {module_name}")
        except Exception as e:
            failures.append((layer, module_name, str(e)))
            print(f"[FAIL] {layer}: failed importing {module_name} -> {e}")

    if failures:
        print(f"\nAudit Failed! {len(failures)} layer import error(s).")
        return 1

    print("\nAudit Passed! All 4 cognitive operating system layers imported cleanly.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
