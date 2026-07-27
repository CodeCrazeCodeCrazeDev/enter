from __future__ import annotations
from typing import Any, Generic, Type, TypeVar, Dict
from pydantic import BaseModel

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)


class BaseSkill(Generic[InputT, OutputT]):
    """First-class executable skill wrapper with Pydantic typed input/output schemas."""

    input_schema: Type[InputT]
    output_schema: Type[OutputT]

    async def execute(self, params: InputT, context: Dict[str, Any]) -> OutputT:
        """Run the skill's concrete action and return validated output."""
        raise NotImplementedError
