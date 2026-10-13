#!/usr/bin/env python3
"""
Verification script for the 14-Layer Computational Architecture of Entrepreneurship.
Audits layer imports, documentation, and end-to-end signal processing.
"""

import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath("."))

def main():
    print("=== Auditing 14-Layer Computational Architecture ===")

    # 1. Check documentation file
    doc_path = "docs/architecture/FOURTEEN_LAYER_COMPUTATIONAL_ARCHITECTURE.md"
    if not os.path.exists(doc_path):
        print(f"FAIL: Missing documentation at {doc_path}")
        sys.exit(1)

    with open(doc_path, "r", encoding="utf-8") as f:
        doc_content = f.read()

    required_sections = [f"Layer {i}:" for i in range(1, 15)]
    for req in required_sections:
        if req not in doc_content:
            print(f"FAIL: Documentation missing section '{req}'")
            sys.exit(1)

    print("✓ Documentation check passed (all 14 layers present).")

    # 2. Check Python exports
    try:
        from apodex.ai_eos.intelligence import (
            FourteenLayerEngine,
            WorldStateSignal,
            Layer1RealitySubstrate,
            Layer2OpportunityDiscovery,
            Layer3ProblemDiscovery,
            Layer4DecisionEngine,
            Layer5OpportunityEvaluation,
            Layer6ProductCreation,
            Layer7CustomerUnderstanding,
            Layer8Marketing,
            Layer9SalesEngine,
            Layer10GrowthEngine,
            Layer11CompetitionEngine,
            Layer12OrganizationalDesign,
            Layer13MetaLearning,
            Layer14AIEntrepreneurshipOrchestrator
        )
        print("✓ All 14 layer classes imported successfully.")
    except Exception as e:
        print(f"FAIL: Module import error: {e}")
        sys.exit(1)

    # 3. Check engine execution
    try:
        engine = FourteenLayerEngine()
        res = engine.process_world_signal({
            "title": "Verification Signal",
            "domain": "test_domain",
            "entropy": 1.0,
            "event_timestamps": [1.0, 2.0, 3.0]
        })
        if res.get("status") not in ("EXECUTED", "TERMINATED"):
            print(f"FAIL: Unexpected execution status '{res.get('status')}'")
            sys.exit(1)
        print("✓ FourteenLayerEngine pipeline executed successfully.")
    except Exception as e:
        print(f"FAIL: Engine execution error: {e}")
        sys.exit(1)

    print("\nALL 14-LAYER ARCHITECTURE AUDITS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
