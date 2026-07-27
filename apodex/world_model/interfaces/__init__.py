"""
WMC Interfaces Package
Defines the clean, abstract base contracts for WMC services, repositories, and plugins.
"""

from __future__ import annotations

from apodex.world_model.interfaces.services import IWorldModelService, ISemanticSearchService

__all__ = ["IWorldModelService", "ISemanticSearchService"]
