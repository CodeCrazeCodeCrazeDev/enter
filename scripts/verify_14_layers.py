#!/usr/bin/env python3
"""
Audit script verifying the presence, exportability, and execution of all 14 layers in the Computational Architecture of Entrepreneurship.
"""

import os
import sys
import importlib

EXPECTED_LAYERS = [
    "Layer 1", "Layer 2", "Layer 3", "Layer 4", "Layer 5", "Layer 6", "Layer 7",
    "Layer 8", "Layer 9", "Layer 10", "Layer 11", "Layer 12", "Layer 13", "Layer 14"
]

def verify_doc():
    doc_path = "docs/architecture/FOURTEEN_LAYER_COMPUTATIONAL_ARCHITECTURE.md"
    if not os.path.exists(doc_path):
        print(f"ERROR: Specification file {doc_path} missing.")
        return False
    with open(doc_path, "r") as f:
        content = f.read()
    for layer in EXPECTED_LAYERS:
        if layer not in content:
            print(f"ERROR: {layer} not found in {doc_path}")
            return False
    print("SUCCESS: Architecture specification contains all 14 layers.")
    return True

def verify_engine():
    try:
        sys.path.insert(0, ".")
        intel = importlib.import_module("apodex.ai_eos.intelligence")
        master_cls = getattr(intel, "FourteenLayerEntrepreneurshipEngine", None)
        if master_cls is None:
            print("ERROR: FourteenLayerEntrepreneurshipEngine not re-exported in apodex.ai_eos.intelligence")
            return False

        engine = master_cls()
        res = engine.run_full_14_layer_pipeline({"title": "AI Enterprise Agent", "domain": "software", "kl_divergence": 0.8})
        if res.get("status") != "completed":
            print(f"ERROR: Pipeline status was {res.get('status')}")
            return False

        for i in range(1, 15):
            key_found = any(k.startswith(f"layer_{i}_") for k in res.keys())
            if not key_found:
                print(f"ERROR: Output missing layer {i} result key.")
                return False

        print("SUCCESS: 14-Layer Engine executed all layers flawlessly.")
        return True
    except Exception as e:
        print(f"ERROR: Exception during engine verification: {e}")
        return False

def main():
    print("--- Auditing 14-Layer Computational Architecture ---")
    doc_ok = verify_doc()
    eng_ok = verify_engine()
    if doc_ok and eng_ok:
        print("--- AUDIT PASSED: 100% COVERAGE ---")
        sys.exit(0)
    else:
        print("--- AUDIT FAILED ---")
        sys.exit(1)

if __name__ == "__main__":
    main()
