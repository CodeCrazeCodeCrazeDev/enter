from __future__ import annotations
from typing import Any, Callable, Dict, Type, TypeVar

T = TypeVar('T')


class DependencyContainer:
    """Production-grade lightweight Dependency Injection Container."""

    def __init__(self) -> None:
        self._singletons: Dict[Type[Any], Any] = {}
        self._transients: Dict[Type[Any], Callable[[], Any]] = {}

    def register_singleton(self, interface: Type[T], instance: T) -> None:
        """Register a persistent singleton service instance."""
        if not isinstance(instance, interface):
            raise TypeError(f"Instance does not implement {interface.__name__}")
        self._singletons[interface] = instance

    def register_transient(self, interface: Type[T], factory: Callable[[], T]) -> None:
        """Register a transient service factory resolved freshly on each request."""
        self._transients[interface] = factory

    def resolve(self, interface: Type[T]) -> T:
        """Resolve and return an instance satisfying the requested interface contract."""
        if interface in self._singletons:
            return self._singletons[interface]
        if interface in self._transients:
            factory = self._transients[interface]
            instance = factory()
            if not isinstance(instance, interface):
                raise TypeError(f"Factory output does not implement {interface.__name__}")
            return instance
        raise ValueError(f"Interface {interface.__name__} is not registered in the container.")
