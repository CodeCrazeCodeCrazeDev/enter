from __future__ import annotations
from typing import Dict, Type
from apodex.world_model.interfaces.plugins import IWmcPlugin


class PluginRegistry:
    """Central registry tracking active, validated plugins."""

    def __init__(self) -> None:
        self._plugins: Dict[str, Type[IWmcPlugin]] = {}

    def register_plugin(self, plugin_class: Type[IWmcPlugin]) -> None:
        """Register a custom plugin class."""
        # Instantiate a temporary copy to verify the name property exists
        temp_instance = plugin_class.__new__(plugin_class)
        try:
            name = temp_instance.plugin_name
        except AttributeError:
            raise ValueError("Plugin class must define 'plugin_name' property.")
        self._plugins[name] = plugin_class

    def get_plugin(self, name: str) -> Type[IWmcPlugin]:
        """Fetch a registered plugin by name."""
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' is not registered.")
        return self._plugins[name]
