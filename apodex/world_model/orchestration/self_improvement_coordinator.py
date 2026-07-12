from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from apodex.world_model.dependency_injection import DependencyContainer
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


class SelfImprovementFlywheelCoordinator:
    """Orchestrates the multi-agent self-improving engineering organization."""

    def __init__(self, container: DependencyContainer) -> None:
        self.container = container

    async def execute_optimization_cycle(self) -> List[SelfImprovementProposal]:
        """
        Runs a complete self-improvement optimization cycle:
        1. Gathers architectural, security, and performance findings.
        2. Selects the highest priority finding.
        3. Generates a targeted fix/patch proposal with academic research citations.
        4. Drafts QA test coverage.
        5. Benchmarks the proposed solution, verifying it is positive-yield.
        """
        proposals = []

        # 1. Gather audit findings from specialized agents
        findings: List[EngineeringFinding] = []

        try:
            architect = self.container.resolve(IChiefArchitect)
            findings.extend(await architect.evaluate_architecture())
        except Exception:
            pass  # Keep going if architect is not registered

        try:
            security_eng = self.container.resolve(ISecurityEngineer)
            findings.extend(await security_eng.audit_security())
        except Exception:
            pass

        try:
            performance_eng = self.container.resolve(IPerformanceEngineer)
            findings.extend(await performance_eng.profile_performance())
        except Exception:
            pass

        if not findings:
            return proposals

        # 2. Select the highest-severity finding
        # Sort findings: CRITICAL > HIGH > MEDIUM > LOW
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        findings.sort(key=lambda f: severity_order.get(f.severity, 4))
        target_finding = findings[0]

        # 3. Generate a software fix proposal
        swe = self.container.resolve(ISoftwareEngineer)
        proposal = await swe.generate_patch(target_finding)

        # 4. Gather research-driven citations to back up the recommendation
        try:
            researcher = self.container.resolve(IResearchScientist)
            citations = await researcher.research_topic(f"optimization of {target_finding.category}")
            proposal.research_citations.extend(citations)
        except Exception:
            pass

        # 5. Generate unit/integration tests to ensure coverage increases
        try:
            qa = self.container.resolve(IQaEngineer)
            test_code = await qa.generate_tests(proposal)
            # Log or register generated test code
            proposal.summary += f"\n[QA Test Generated]\n{test_code}"
        except Exception:
            pass

        # 6. Benchmark and evaluate the proposal to protect budget and prevent regressions
        evaluator = self.container.resolve(IEvaluator)
        report = await evaluator.benchmark_proposal(proposal)

        proposal.benchmark_report = report
        if not report.is_regression:
            proposal.status = "EVALUATED"
        else:
            proposal.status = "REJECTED"

        proposals.append(proposal)
        return proposals
