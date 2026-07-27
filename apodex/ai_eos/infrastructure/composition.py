"""Dependency Injection (DI) Container and Composition Platform for AI-EOS.

Coordinates service lifecycles, configuration mappings, feature flags, and dynamic registrations.
"""

from __future__ import annotations
import logging
import threading
from typing import Any, Dict, Type, TypeVar, Optional, List

T = TypeVar("T")

logger = logging.getLogger("ai_eos.composition")


class CompositionContainer:
    """Thread-safe Dependency Injection and Composition Container for AI-EOS."""

    _instance: Optional[CompositionContainer] = None
    _lock = threading.Lock()

    def __new__(cls) -> CompositionContainer:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._services = {}
                    cls._instance._feature_flags = {}
                    cls._instance._lifecycle_listeners = []
                    cls._instance._is_initialized = False
        return cls._instance

    def register(self, service_interface: Type[T], instance: T) -> None:
        """Register a concrete service implementation for a specific abstract interface."""
        with self._lock:
            key = f"{service_interface.__module__}.{service_interface.__name__}"
            self._services[key] = instance
            logger.info(f"Registered service contract: {key} -> {type(instance).__name__}")

    def resolve(self, service_interface: Type[T]) -> T:
        """Resolve a service instance corresponding to the abstract interface contract."""
        with self._lock:
            key = f"{service_interface.__module__}.{service_interface.__name__}"
            if key not in self._services:
                raise ValueError(f"Service contract '{key}' is not registered in the CompositionContainer.")
            return self._services[key]

    def has_service(self, service_interface: Type[Any]) -> bool:
        """Check if a service interface contract is registered."""
        key = f"{service_interface.__module__}.{service_interface.__name__}"
        return key in self._services

    # ------------------------------------------------------------------
    # Feature Flags & Config System
    # ------------------------------------------------------------------
    def set_feature_flag(self, flag: str, value: bool) -> None:
        """Set a dynamic operational feature flag."""
        with self._lock:
            self._feature_flags[flag] = value
            logger.info(f"Feature flag set: {flag} = {value}")

    def is_feature_enabled(self, flag: str, default: bool = False) -> bool:
        """Check if an operational feature flag is enabled."""
        return self._feature_flags.get(flag, default)

    # ------------------------------------------------------------------
    # Lifecycle Management
    # ------------------------------------------------------------------
    def register_lifecycle_listener(self, listener: Any) -> None:
        """Register a component that implements initialize() and shutdown()."""
        with self._lock:
            self._lifecycle_listeners.append(listener)

    def initialize_platform(self) -> None:
        """Initialize all registered lifecycle components sequentially."""
        with self._lock:
            if self._is_initialized:
                return
            logger.info("Initializing AI-EOS System Composition Platform...")
            for listener in self._lifecycle_listeners:
                if hasattr(listener, "initialize"):
                    listener.initialize()
            self._is_initialized = True
            logger.info("AI-EOS Platform successfully composed.")

    def shutdown_platform(self) -> None:
        """Shutdown all registered lifecycle components sequentially."""
        with self._lock:
            if not self._is_initialized:
                return
            logger.info("Shutting down AI-EOS System Composition Platform...")
            for listener in reversed(self._lifecycle_listeners):
                if hasattr(listener, "shutdown"):
                    listener.shutdown()
            self._is_initialized = False
            logger.info("AI-EOS Platform shutdown complete.")

    def reset(self) -> None:
        """Reset container state (for testing isolation)."""
        with self._lock:
            self._services.clear()
            self._feature_flags.clear()
            self._lifecycle_listeners.clear()
            self._is_initialized = False
            logger.info("CompositionContainer has been reset.")
