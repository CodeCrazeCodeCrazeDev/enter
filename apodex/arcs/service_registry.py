from __future__ import annotations
import logging
import threading
from typing import Any, Dict, Type, TypeVar, Optional

T = TypeVar("T")

logger = logging.getLogger("arcs.service_registry")


class ServiceRegistry:
    """Thread-safe Dependency Injection and Service Registry for ARCS and Apodex platform services."""

    _instance: Optional[ServiceRegistry] = None
    _lock = threading.Lock()

    def __new__(cls) -> ServiceRegistry:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._services = {}
        return cls._instance

    def register(self, service_type: Type[T], instance: T) -> None:
        """Register a service instance for a specific type/interface."""
        with self._lock:
            key = f"{service_type.__module__}.{service_type.__name__}"
            self._services[key] = instance
            logger.info(f"Registered service: {key} -> {type(instance).__name__}")

    def resolve(self, service_type: Type[T]) -> T:
        """Resolve a service instance of the requested type/interface.

        Raises:
            ValueError: If the service type is not registered.
        """
        with self._lock:
            key = f"{service_type.__module__}.{service_type.__name__}"
            if key not in self._services:
                raise ValueError(f"Service '{key}' is not registered in the ServiceRegistry.")
            return self._services[key]

    def has_service(self, service_type: Type[Any]) -> bool:
        """Check if a service type is registered."""
        key = f"{service_type.__module__}.{service_type.__name__}"
        return key in self._services

    def reset(self) -> None:
        """Clear all registered services."""
        with self._lock:
            self._services.clear()
            logger.info("ServiceRegistry has been reset.")
