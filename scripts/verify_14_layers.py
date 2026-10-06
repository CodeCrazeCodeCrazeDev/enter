#!/usr/bin/env python3
"""
Audit script to verify the 14-Layer Computational Architecture of Entrepreneurship.
Checks importability, exports, layer coverage, and documentation presence.
"""

import sys
import os

def audit_14_layer_architecture() -> int:
    print("=== Auditing 14-Layer Computational Architecture of Entrepreneurship ===")

    # 1. Check specification file existence
    spec_path = "docs/architecture/FOURTEEN_LAYER_COMPUTATIONAL_ARCHITECTURE.md"
    if not os.path.exists(spec_path):
        print(f"FAILED: Specification file {spec_path} does not exist.")
        return 1

    with open(spec_path, "r", encoding="utf-8") as f:
        spec_content = f.read()

    if len(spec_content) < 1000:
        print(f"FAILED: Specification file {spec_path} is too short ({len(spec_content)} bytes).")
        return 1
    print(f"PASS: Architecture specification verified ({len(spec_content)} bytes).")

    # 2. Check engine imports and layer classes
    try:
        import apodex.ai_eos.intelligence as intel
    except Exception as e:
        print(f"FAILED: Import error for apodex.ai_eos.intelligence: {e}")
        return 1

    expected_classes = [
        "RealitySubstrateEngine",
        "OpportunityDiscoveryEngine",
        "ProblemDiscoveryEngine",
        "DecisionMakingEngine",
        "OpportunityEvaluationEngine",
        "ProductCreationEngine",
        "CustomerUnderstandingEngine",
        "MarketingEngine",
        "SalesEngine",
        "GrowthEngine",
        "CompetitionEngine",
        "OrganizationalDesignEngine",
        "MetaLearningEngine",
        "FourteenLayerEntrepreneurshipOrchestrator"
    ]

    for cls_name in expected_classes:
        if not hasattr(intel, cls_name):
            print(f"FAILED: Missing exported class '{cls_name}' in apodex.ai_eos.intelligence")
            return 1
        print(f"PASS: Exported class '{cls_name}' verified.")

    # 3. Test orchestrator execution
    try:
        orchestrator = intel.FourteenLayerEntrepreneurshipOrchestrator()
        test_signal = {
            "title": "Audit Test Enterprise",
            "domain": "software",
            "tam_cents": 200000000
        }
        res = orchestrator.run_full_14_layer_pipeline(test_signal)
        if res.get("status") != "SUCCESS":
            print(f"FAILED: Orchestrator pipeline returned status '{res.get('status')}'")
            return 1
        print("PASS: Orchestrator 14-layer pipeline executed successfully.")
    except Exception as e:
        print(f"FAILED: Orchestrator pipeline execution failed: {e}")
        return 1

    print("\nALL 14-LAYER ARCHITECTURE AUDITS PASSED SUCCESSFULLY!")
    return 0

if __name__ == "__main__":
    sys.exit(audit_14_layer_architecture())
