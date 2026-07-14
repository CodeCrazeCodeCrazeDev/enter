from __future__ import annotations
import asyncio
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from apodex.world_model.dependency_injection import DependencyContainer
from apodex.world_model.config import WorldModelCreatorConfig
from apodex.world_model.orchestration.self_improvement_coordinator import SelfImprovementFlywheelCoordinator
from apodex.world_model.domain.self_improvement import (
    EngineeringFinding,
    SelfImprovementProposal,
    BenchmarkReport
)
from apodex.world_model.interfaces.self_improvement import (
    IChiefArchitect,
    ISecurityEngineer,
    IPerformanceEngineer,
    ISoftwareEngineer,
    IResearchScientist,
    IQaEngineer,
    IEvaluator
)

logger = logging.getLogger("apodex.harness.feature_tests")


class FeatureTestRunner:
    """Agentic feature test runner simulating end-to-end multi-tenant, budget-sensitive, and progress-limiting scenarios."""

    def __init__(self) -> None:
        self.container = DependencyContainer()
        self._setup_mocks()

    def _setup_mocks(self) -> None:
        class TestArchitect(IChiefArchitect):
            async def evaluate_architecture(self) -> List[EngineeringFinding]:
                return [EngineeringFinding(
                    severity="HIGH",
                    category="CIRCULAR_DEPENDENCY",
                    file_path="apodex/world_model/world_model.py",
                    description="Circular dependency identified",
                    suggested_fix="Refactor imports"
                )]

        class TestSecurity(ISecurityEngineer):
            async def audit_security(self) -> List[EngineeringFinding]:
                return [EngineeringFinding(
                    severity="HIGH",
                    category="SECURITY_VULNERABILITY",
                    file_path="apodex/world_model/config.py",
                    description="Hardcoded API key detected",
                    suggested_fix="Move to env"
                )]

        class TestPerformance(IPerformanceEngineer):
            async def profile_performance(self) -> List[EngineeringFinding]:
                return []

        class TestSWE(ISoftwareEngineer):
            async def generate_patch(self, finding: EngineeringFinding) -> SelfImprovementProposal:
                return SelfImprovementProposal(
                    title=f"Fix for {finding.category}",
                    summary="Applied correction",
                    proposed_diff="diff file",
                    risks_analysis="None",
                    rollback_instructions="Revert"
                )

        class TestResearch(IResearchScientist):
            async def research_topic(self, topic: str) -> List[str]:
                return ["Paper CIT-101"]

        class TestQA(IQaEngineer):
            async def generate_tests(self, proposal: SelfImprovementProposal) -> str:
                return "def test_patch(): assert True"

        class TestEvaluator(IEvaluator):
            async def benchmark_proposal(self, proposal: SelfImprovementProposal) -> BenchmarkReport:
                return BenchmarkReport(
                    latency_delta_ms=-10.0,
                    token_cost_delta_usd=0.0,
                    accuracy_score_delta=0.01,
                    is_regression=False
                )

        self.container.register_singleton(IChiefArchitect, TestArchitect())
        self.container.register_singleton(ISecurityEngineer, TestSecurity())
        self.container.register_singleton(IPerformanceEngineer, TestPerformance())
        self.container.register_singleton(ISoftwareEngineer, TestSWE())
        self.container.register_singleton(IResearchScientist, TestResearch())
        self.container.register_singleton(IQaEngineer, TestQA())
        self.container.register_singleton(IEvaluator, TestEvaluator())

    async def run_scenario(self, tenant_id: str, tier: str, max_budget: float) -> SelfImprovementFlywheelCoordinator:
        config = WorldModelCreatorConfig(tenant_id=tenant_id, max_budget_limit_usd=max_budget)
        config.reality_engine.execution_tier = tier

        container_instance = DependencyContainer()
        # Duplicate mock services in new container instance to ensure isolation
        container_instance.register_singleton(WorldModelCreatorConfig, config)
        container_instance.register_singleton(IChiefArchitect, self.container.resolve(IChiefArchitect))
        container_instance.register_singleton(ISecurityEngineer, self.container.resolve(ISecurityEngineer))
        container_instance.register_singleton(IPerformanceEngineer, self.container.resolve(IPerformanceEngineer))
        container_instance.register_singleton(ISoftwareEngineer, self.container.resolve(ISoftwareEngineer))
        container_instance.register_singleton(IResearchScientist, self.container.resolve(IResearchScientist))
        container_instance.register_singleton(IQaEngineer, self.container.resolve(IQaEngineer))
        container_instance.register_singleton(IEvaluator, self.container.resolve(IEvaluator))

        coordinator = SelfImprovementFlywheelCoordinator(container=container_instance)
        await coordinator.execute_optimization_cycle()
        return coordinator
