"""Event Bus infrastructure implementation for AI-EOS.

Provides thread-safe pub-sub capabilities for routing Domain Events.
"""

from __future__ import annotations
import logging
import threading
from typing import Any, Callable, Dict, List, Type, TypeVar
from ..domain.events import DomainEvent
from ..interfaces.services import IEventBus

E = TypeVar("E", bound=DomainEvent)

logger = logging.getLogger("ai_eos.infrastructure.event_bus")


class EventBus(IEventBus):
    """Concrete thread-safe in-memory Event Bus implementing pub-sub routing."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[Any], Any]]] = {}
        self._lock = threading.Lock()

    def subscribe(self, event_type: Type[E], handler: Callable[[E], Any]) -> None:
        """Subscribe a callback handler to a specific domain event type."""
        with self._lock:
            key = f"{event_type.__module__}.{event_type.__name__}"
            if key not in self._subscribers:
                self._subscribers[key] = []
            self._subscribers[key].append(handler)
            logger.debug(f"Subscribed handler to event: {key}")

    def publish(self, event: DomainEvent) -> None:
        """Publish an event to all subscribed handlers."""
        key = f"{event.__class__.__module__}.{event.__class__.__name__}"
        logger.info(f"Publishing domain event: {key} [id={event.event_id}]")

        # Capture handlers under lock to avoid racing during modification
        with self._lock:
            handlers = list(self._subscribers.get(key, []))

        for handler in handlers:
            try:
                handler(event)
            except Exception as ex:
                logger.error(f"Error executing event handler {handler.__name__} for event {key}: {ex}", exc_info=True)
