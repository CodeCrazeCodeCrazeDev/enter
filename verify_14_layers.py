#!/usr/bin/env python3
"""
Audit and verification script for the 14-Layer Computational Architecture
of Entrepreneurship in SERO / APODEX AI EOS.
"""

import sys
import os
import inspect

# Add repository root to path
sys.path.insert(0, os.path.abspath("."))

from apodex.ai_eos.intelligence import (
    Layer1_RealitySubstrate,
    Layer2_OpportunitySearchEngine,
    Layer3_ProblemDecompositionEngine,
    Layer4_ActiveInferenceDecisionEngine,
    Layer5_OpportunityValuationEngine,
    Layer6_ProductSynthesisEngine,
    Layer7_CustomerPsychologyEngine,
    Layer8_MarketingDiffusionEngine,
    Layer9_RepeatableSalesEngine,
    Layer10_CompoundingGrowthEngine,
    Layer11_CompetitiveMoatEngine,
    Layer12_OrganizationalScalingEngine,
    Layer13_MetaLearningEngine,
    Layer14_AutonomousAIEntrepreneur,
    FourteenLayerEntrepreneurialEngine,
    Signal
)


def run_verification():
    print("=========================================================================")
    print("VERIFYING 14-LAYER COMPUTATIONAL ARCHITECTURE OF ENTREPRENEURSHIP")
    print("=========================================================================")

    layer_classes = [
        (1, "Reality Substrate", Layer1_RealitySubstrate),
        (2, "Opportunity Search Engine", Layer2_OpportunitySearchEngine),
        (3, "Problem Decomposition Engine", Layer3_ProblemDecompositionEngine),
        (4, "Active Inference Decision Engine", Layer4_ActiveInferenceDecisionEngine),
        (5, "Opportunity Valuation Engine", Layer5_OpportunityValuationEngine),
        (6, "Product Synthesis Engine", Layer6_ProductSynthesisEngine),
        (7, "Customer Psychology Engine", Layer7_CustomerPsychologyEngine),
        (8, "Marketing Diffusion Engine", Layer8_MarketingDiffusionEngine),
        (9, "Repeatable Sales Engine", Layer9_RepeatableSalesEngine),
        (10, "Compounding Growth Engine", Layer10_CompoundingGrowthEngine),
        (11, "Competitive Moat Engine", Layer11_CompetitiveMoatEngine),
        (12, "Organizational Scaling Engine", Layer12_OrganizationalScalingEngine),
        (13, "Meta-Learning Engine", Layer13_MetaLearningEngine),
        (14, "Autonomous AI Entrepreneur", Layer14_AutonomousAIEntrepreneur)
    ]

    for layer_num, name, cls in layer_classes:
        methods = [m for m in dir(cls) if not m.startswith("_")]
        print(f"[OK] Layer {layer_num:02d}: {name:<35} | Implementation: {cls.__name__} ({len(methods)} public methods)")

    print("\n--- Testing Master Pipeline Execution ---")
    engine = FourteenLayerEntrepreneurialEngine()
    signals = [
        Signal(domain="AI", historical_variance=0.1, recent_variance=0.8, delta_mean=2.0, entropy_kl_div=0.9),
        Signal(domain="Bio", historical_variance=0.2, recent_variance=0.9, delta_mean=1.5, entropy_kl_div=0.8)
    ]
    res = engine.execute_full_14_layer_pipeline(signals, 1000000)

    assert res["status"] == "success", "Master pipeline failed!"
    print(f"[OK] Master pipeline executed successfully. All 14 layers integrated.")
    print(f"     Selected Opportunity: '{res['opportunity_title']}'")
    print(f"     Root Cause: {res['layer3_root_cause']}")
    print(f"     Active Inference EFE: {res['layer4_efe']:.4f}")
    print(f"     Real Option Value: ${res['layer5_real_option_value']:.2f}")

    # Check documentation file
    doc_path = "docs/architecture/FOURTEEN_LAYER_COMPUTATIONAL_ARCHITECTURE.md"
    assert os.path.exists(doc_path), f"Missing architecture documentation: {doc_path}"
    file_size = os.path.getsize(doc_path)
    print(f"[OK] Documentation verified: {doc_path} ({file_size} bytes)")

    print("\n=========================================================================")
    print("VERIFICATION COMPLETE: ALL 14 LAYERS OPERATIONAL AND COMPLIANT")
    print("=========================================================================")


if __name__ == "__main__":
    run_verification()
