from __future__ import annotations
from typing import Any, Dict
from apodex.world_model.interfaces.plugins import IWmcPlugin


class BaseWmcPlugin(IWmcPlugin):
    """Base abstract utility extending the plugin lifecycle."""

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def plugin_name(self) -> str:
        return self._name

    async def on_initialize(self, context: Dict[str, Any]) -> None:
        """Lifecycle initial hook."""
        pass

    async def on_shutdown(self) -> None:
        """Lifecycle final hook."""
        pass
