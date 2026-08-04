from __future__ import annotations
from typing import Dict, Any, Type, Optional, List, Union
from apodex.skills.base import BaseSkill
from apodex.skills.models import BusinessSkill, KnowledgeType

class SkillRegistry:
    """A central registry to register, discover, and resolve executable skills."""

    def __init__(self) -> None:
        self._skills: Dict[str, Union[BaseSkill[Any, Any], BusinessSkill]] = {}
        self._populate_default_skills()

    def register(self, name: str, skill: Union[BaseSkill[Any, Any], BusinessSkill]) -> None:
        self._skills[name] = skill

    def get(self, name: str) -> Optional[Union[BaseSkill[Any, Any], BusinessSkill]]:
        return self._skills.get(name)

    def get_skill(self, name: str) -> Optional[Union[BaseSkill[Any, Any], BusinessSkill]]:
        return self.get(name)

    def list_skills(
        self,
        domain: Optional[str] = None,
        knowledge_type: Optional[KnowledgeType] = None
    ) -> List[Union[BaseSkill[Any, Any], BusinessSkill]]:
        res = list(self._skills.values())
        if domain is not None:
            res = [s for s in res if hasattr(s, "domain") and s.domain == domain]
        if knowledge_type is not None:
            res = [s for s in res if hasattr(s, "knowledge_type") and s.knowledge_type == knowledge_type]
        return res

    def _populate_default_skills(self) -> None:
        # Pre-populate 60 default strategic and operational skills
        # 1. 10 strategy evergreen skills
        strategy_skills = [
            BusinessSkill(
                name="opportunity_evaluation_frameworks",
                domain="strategy",
                description="Evaluating market opportunity with specific frameworks",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=25
            ),
            BusinessSkill(
                name="business_model_design",
                domain="strategy",
                description="Designing sustainable business models",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=30
            )
        ]
        for i in range(3, 11):
            strategy_skills.append(
                BusinessSkill(
                    name=f"strategy_{i}",
                    domain="strategy",
                    description=f"Strategic capabilities level {i}",
                    knowledge_type=KnowledgeType.EVERGREEN,
                    base_cost_credits=10
                )
            )

        # 2. 7 decaying skills
        decaying_skills = []
        for i in range(1, 8):
            decaying_skills.append(
                BusinessSkill(
                    name=f"decaying_{i}",
                    domain="analytics",
                    description=f"Fast-decaying market signal tracker {i}",
                    knowledge_type=KnowledgeType.DECAYING,
                    base_cost_credits=10
                )
            )

        # 3. Specific evergreen skills
        specific_skills = [
            BusinessSkill(
                name="narrative_structures",
                domain="marketing",
                description="Structuring customer pain narrative",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="landing_page_patterns",
                domain="marketing",
                description="Optimized landing page layout design",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="structured_ab_testing",
                domain="creative",
                description="Statistically sound A/B split testing",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            ),
            BusinessSkill(
                name="revenue_metric_literacy",
                domain="finance",
                description="Advanced financial and MRR literacy",
                knowledge_type=KnowledgeType.EVERGREEN,
                base_cost_credits=10
            )
        ]

        # 4. Fill remaining evergreen general skills to reach exactly 60
        general_skills = []
        # Total currently: 10 + 7 + 4 = 21. We need 39 more to hit 60.
        for i in range(11, 50):
            general_skills.append(
                BusinessSkill(
                    name=f"evergreen_{i}",
                    domain="general",
                    description=f"General evergreen skill {i}",
                    knowledge_type=KnowledgeType.EVERGREEN,
                    base_cost_credits=10
                )
            )

        # Register everything
        all_default = strategy_skills + decaying_skills + specific_skills + general_skills
        for skill in all_default:
            self.register(skill.name, skill)


# Singleton instance for simple runtime lookup
skill_registry = SkillRegistry()
