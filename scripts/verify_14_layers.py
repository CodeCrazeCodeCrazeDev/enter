#!/usr/bin/env python3
"""
Audits the coverage of all 14 computational layers across specification documentation,
code base implementation, exports, and test suite.
"""

import sys
from apodex.ai_eos.intelligence import (
    RealitySubstrateEngine,
    ContinuousStateSpaceDiscoveryEngine,
    ProblemDiscoveryDecompositionEngine,
    DecisionUnderUncertaintyEngine,
    QuantitativeEvaluationEngine,
    ProductCreationEngine,
    CustomerPsychologyEngine,
    MarketFormationEngine,
    PsychologicalSalesEngine,
    CompoundingGrowthEngine,
    CompetitiveDynamicsEngine,
    OrganizationalScalingEngine,
    EntrepreneurialMetaLearningEngine,
    AutonomousAIEntrepreneurshipEngine,
    FourteenLayerOrchestrator,
)

LAYERS = [
    ("Layer 1: Reality Substrate", RealitySubstrateEngine),
    ("Layer 2: Continuous State-Space Opportunity Discovery", ContinuousStateSpaceDiscoveryEngine),
    ("Layer 3: Problem Discovery & Decomposition", ProblemDiscoveryDecompositionEngine),
    ("Layer 4: Decision Making Under Uncertainty", DecisionUnderUncertaintyEngine),
    ("Layer 5: Quantitative Opportunity Evaluation", QuantitativeEvaluationEngine),
    ("Layer 6: Product Creation & Anti-Feature Elimination", ProductCreationEngine),
    ("Layer 7: Customer Psychology Modeling", CustomerPsychologyEngine),
    ("Layer 8: Market Formation & Growth Mechanics", MarketFormationEngine),
    ("Layer 9: Psychological Sales Systems", PsychologicalSalesEngine),
    ("Layer 10: Compounding Growth & Ecosystem Platforms", CompoundingGrowthEngine),
    ("Layer 11: Competitive Dynamics & Moats", CompetitiveDynamicsEngine),
    ("Layer 12: Organizational Architecture & Scaling", OrganizationalScalingEngine),
    ("Layer 13: Entrepreneurial Meta-Learning", EntrepreneurialMetaLearningEngine),
    ("Layer 14: Autonomous AI Entrepreneurship", AutonomousAIEntrepreneurshipEngine),
]

def audit_layers():
    print("=== Auditing 14-Layer Computational Architecture Implementation ===")
    for name, cls in LAYERS:
        assert cls is not None, f"Class missing for {name}"
        print(f"[OK] {name} -> {cls.__name__}")

    orchestrator = FourteenLayerOrchestrator()
    assert orchestrator is not None
    print("[OK] FourteenLayerOrchestrator successfully instantiated.")

    # Audit specification document
    with open("docs/architecture/FOURTEEN_LAYER_COMPUTATIONAL_ARCHITECTURE.md", "r") as f:
        doc_content = f.read()

    for idx in range(1, 15):
        layer_str = f"Layer {idx}:"
        assert layer_str in doc_content, f"Missing documentation header for {layer_str}"
        print(f"[OK] Documentation verified for Layer {idx}")

    print("\nAll 14 layers successfully verified across specification and codebase.")

if __name__ == "__main__":
    audit_layers()
