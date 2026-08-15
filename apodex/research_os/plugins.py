from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from uuid import UUID
from .models import (
    BaseArtifact,
    ExperimentDesign,
    ExperimentResult,
    LiteratureCorpus,
    DecisionRecord,
)

# =====================================================================
# Abstract Plugin Interfaces
# =====================================================================

class IAgentPlugin(ABC):
    """Protocol for active processing units (domain scientists, statisticians, etc.)."""

    @abstractmethod
    def name(self) -> str:
        """Name of the plugin."""
        pass

    @abstractmethod
    async def process(
        self,
        inputs: Dict[str, BaseArtifact],
        lineage_parents: List[UUID],
        author: str
    ) -> BaseArtifact:
        """Processes typed input artifacts and produces an immutable child artifact."""
        pass


class IGovernancePlugin(ABC):
    """Interface for authoritative policy controllers and boards."""

    @abstractmethod
    def board_name(self) -> str:
        """Name of the governing panel."""
        pass

    @abstractmethod
    async def audit(self, artifact: BaseArtifact) -> DecisionRecord:
        """Evaluates an artifact against policy rules, returning a binding decision."""
        pass


class IExperimentBackend(ABC):
    """Interface for backends executing scientific simulations or training loops."""

    @abstractmethod
    def backend_name(self) -> str:
        """Name of the execution sandbox environment."""
        pass

    @abstractmethod
    async def run(self, design: ExperimentDesign) -> ExperimentResult:
        """Runs the experiment described by design, returning results and metrics."""
        pass


class IEvidenceProvider(ABC):
    """Interface for literature engines and external data indexing services."""

    @abstractmethod
    def provider_name(self) -> str:
        """Name of the literature database provider."""
        pass

    @abstractmethod
    async def search_corpus(self, query: str) -> LiteratureCorpus:
        """Searches scientific libraries and returns structured literature datasets."""
        pass


# =====================================================================
# Plugin Registry
# =====================================================================

class PluginRegistry:
    """Central registry managing the discovery, loading, and registration of plugins."""

    def __init__(self) -> None:
        self._agents: Dict[str, IAgentPlugin] = {}
        self._governance_boards: Dict[str, IGovernancePlugin] = {}
        self._experiment_backends: Dict[str, IExperimentBackend] = {}
        self._evidence_providers: Dict[str, IEvidenceProvider] = {}

    def register_agent(self, plugin: IAgentPlugin) -> None:
        self._agents[plugin.name()] = plugin

    def get_agent(self, name: str) -> Optional[IAgentPlugin]:
        return self._agents.get(name)

    def register_governance(self, plugin: IGovernancePlugin) -> None:
        self._governance_boards[plugin.board_name()] = plugin

    def get_governance(self, board_name: str) -> Optional[IGovernancePlugin]:
        return self._governance_boards.get(board_name)

    def register_experiment_backend(self, plugin: IExperimentBackend) -> None:
        self._experiment_backends[plugin.backend_name()] = plugin

    def get_experiment_backend(self, name: str) -> Optional[IExperimentBackend]:
        return self._experiment_backends.get(name)

    def register_evidence_provider(self, plugin: IEvidenceProvider) -> None:
        self._evidence_providers[plugin.provider_name()] = plugin

    def get_evidence_provider(self, name: str) -> Optional[IEvidenceProvider]:
        return self._evidence_providers.get(name)
