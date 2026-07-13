from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from apodex.world_model.domain.self_improvement import (
    EngineeringFinding,
    SelfImprovementProposal,
    BenchmarkReport
)


class IChiefArchitect(ABC):
    """Evaluates system architecture, circular dependencies, and approves proposals."""

    @abstractmethod
    async def evaluate_architecture(self) -> List[EngineeringFinding]:
        """Scan codebase imports and return architectural issues."""
        pass


class IResearchScientist(ABC):
    """Researches academic and open-source approaches to provide citations and trade-offs."""

    @abstractmethod
    async def research_topic(self, topic: str) -> List[str]:
        """Search literature and return academic paper/blog citations."""
        pass


class ISoftwareEngineer(ABC):
    """Generates structural patches, fixes code smells, and implements proposals."""

    @abstractmethod
    async def generate_patch(self, finding: EngineeringFinding) -> SelfImprovementProposal:
        """Create a targeted proposal with proposed code changes/diffs."""
        pass


class IQaEngineer(ABC):
    """Creates tests (unit, integration, regression, stress) to ensure coverage increases."""

    @abstractmethod
    async def generate_tests(self, proposal: SelfImprovementProposal) -> str:
        """Generate corresponding unit/integration test code."""
        pass


class ISecurityEngineer(ABC):
    """Audits code for secret exposure, injection, and permissions issues."""

    @abstractmethod
    async def audit_security(self) -> List[EngineeringFinding]:
        """Scan code for vulnerabilities and return findings."""
        pass


class IPerformanceEngineer(ABC):
    """Profiles latency, memory leaks, and redundant API calls."""

    @abstractmethod
    async def profile_performance(self) -> List[EngineeringFinding]:
        """Profile code paths and return optimization findings."""
        pass


class IDocumentationEngineer(ABC):
    """Maintains API documentation, keeping specs synced with code."""

    @abstractmethod
    async def sync_documentation(self, proposal: SelfImprovementProposal) -> str:
        """Update relevant technical documents based on structural changes."""
        pass


class IEvaluator(ABC):
    """Performs before/after benchmarking, ensuring changes are positive-yield."""

    @abstractmethod
    async def benchmark_proposal(self, proposal: SelfImprovementProposal) -> BenchmarkReport:
        """Execute sandboxed benchmarks and return a performance delta report."""
        pass
