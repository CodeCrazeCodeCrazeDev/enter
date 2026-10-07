#!/usr/bin/env python3
"""Verification script for the 14-Layer Computational Architecture of Entrepreneurship."""

import os
import sys

def main():
    print("=== Auditing 14-Layer Computational Architecture ===")

    # 1. Audit Specification Document
    spec_path = "docs/architecture/FOURTEEN_LAYER_COMPUTATIONAL_ARCHITECTURE.md"
    if not os.path.exists(spec_path):
        print(f"FAIL: Specification document missing at {spec_path}")
        sys.exit(1)

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"SUCCESS: Specification document found ({len(content)} characters).")

    # Check for presence of all 14 layers in doc
    for layer in range(1, 15):
        pattern = f"Layer {layer}:"
        if pattern not in content:
            print(f"FAIL: Missing '{pattern}' in specification document.")
            sys.exit(1)

    print("SUCCESS: All 14 layer headings verified in specification document.")

    # 2. Audit Engine Module Import and Execution
    try:
        from apodex.ai_eos.intelligence.fourteen_layer_engine import FourteenLayerOrchestrator
        orchestrator = FourteenLayerOrchestrator()
        result = orchestrator.ingest_and_orchestrate(
            {"title": "Verification Audit Signal", "variables": ["a", "b"], "causal_edges": [("a", "b")]},
            budget_cents=100000_00
        )
        assert result["status"] == "orchestrated"
        print("SUCCESS: FourteenLayerOrchestrator executed successfully across all 14 layers.")
    except Exception as e:
        print(f"FAIL: Engine execution failed: {e}")
        sys.exit(1)

    print("\nALL 14-LAYER ARCHITECTURE AUDITS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
