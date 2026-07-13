from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict


class IWmcPlugin(ABC):
    """Abstract interface representing a WMC plugin extension point."""

    @property
    @abstractmethod
    def plugin_name(self) -> str:
        """The identifier of the plugin."""
        pass

    @abstractmethod
    async def on_initialize(self, context: Dict[str, Any]) -> None:
        """Lifecycle hook triggered when the plugin is loaded."""
        pass

    @abstractmethod
    async def on_shutdown(self) -> None:
        """Lifecycle hook triggered when the plugin is unloaded."""
        pass
