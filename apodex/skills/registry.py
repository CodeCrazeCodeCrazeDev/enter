from __future__ import annotations
from typing import Dict, Any, Type, Optional
from apodex.skills.base import BaseSkill

class SkillRegistry:
    """A central registry to register, discover, and resolve executable skills."""

    def __init__(self) -> None:
        self._skills: Dict[str, BaseSkill[Any, Any]] = {}

    def register(self, name: str, skill: BaseSkill[Any, Any]) -> None:
        self._skills[name] = skill

    def get(self, name: str) -> Optional[BaseSkill[Any, Any]]:
        return self._skills.get(name)

    def list_skills(self) -> list[str]:
        return list(self._skills.keys())


# Singleton instance for simple runtime lookup
skill_registry = SkillRegistry()
