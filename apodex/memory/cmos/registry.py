"""Central Pluggable Operator Registrar for CMOS.

Coordinates the instantiation and discovery of all modular Cognitive Operators.
"""

from __future__ import annotations

from typing import Dict, List, Type
from uuid import uuid4

from apodex.memory.cmos.interfaces import CognitiveOperator, OperatorRegistry


class CMOSOperatorRegistry(OperatorRegistry):
    """Memory Operator Registrar supporting extensible dynamic registration."""

    def __init__(self) -> None:
        self._operators: Dict[str, Type[CognitiveOperator]] = {}

    def register(self, op: Type[CognitiveOperator]) -> None:
        # Instantiate once to check name property
        instance = op()
        self._operators[instance.name.lower()] = op

    def get_operator(self, name: str) -> CognitiveOperator:
        op_cls = self._operators.get(name.lower())
        if not op_cls:
            raise KeyError(f"Operator '{name}' not found in the pluggable registry.")
        return op_cls()

    def list_operators(self) -> List[str]:
        return list(self._operators.keys())
