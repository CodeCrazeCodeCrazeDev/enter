"""Entrepreneurial Intelligence System (EIS) context."""

from .decision_engine import EntrepreneurialIntelligenceSystem
from .collective import CollectiveIntelligenceEngine
from .eos_first_principles import (
    EOSState,
    EOSStateMachine,
    OpportunityContext,
    OpportunityDecisionTree,
    BusinessLoopMetrics,
    CoupledBusinessLoopsEngine,
    CustomerLifecycleStage,
    CustomerLifecycleEngine,
    GrowthStage,
    GrowthStageClassifier,
    MoatAnalyzer as FirstPrinciplesMoatAnalyzer,
    FailureMode,
    FailureModeMonitor as FirstPrinciplesFailureModeMonitor,
    FirstPrinciplesEOSEngine,
)
