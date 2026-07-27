"""In-memory thread-safe state persistence ledger for AI-EOS.

Acts as the underlying storage repository for Venture Cells, Hypotheses, and Capabilities.
"""

from __future__ import annotations
import threading
from typing import Any, Dict, List, Optional, TypeVar, Generic
from uuid import UUID

T = TypeVar("T")


class InMemoryLedger(Generic[T]):
    """Generic, thread-safe in-memory ledger representing a clean storage core."""

    def __init__(self) -> None:
        self._store: Dict[Any, T] = {}
        self._lock = threading.Lock()

    def save(self, key: Any, item: T) -> None:
        with self._lock:
            self._store[key] = item

    def get(self, key: Any) -> Optional[T]:
        with self._lock:
            return self._store.get(key)

    def list_all(self) -> List[T]:
        with self._lock:
            return list(self._store.values())

    def delete(self, key: Any) -> Optional[T]:
        with self._lock:
            return self._store.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()
