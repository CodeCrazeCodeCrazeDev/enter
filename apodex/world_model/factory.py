from __future__ import annotations
from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict

from apodex.world_model.domain.entities import Entity
from apodex.world_model.domain.relationships import Relationship
from apodex.world_model.domain.beliefs import Belief


class DomainModelFactory:
    """Factory providing quick, valid instantiations of core domain elements."""

    @staticmethod
    def create_entity(name: str, entity_type: str, properties: Dict[str, Any]) -> Entity:
        """Instantiate a validated Entity node."""
        return Entity(
            entity_id=uuid4(),
            name=name,
            entity_type=entity_type,
            properties=properties,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    @staticmethod
    def create_relationship(source_id: UUID, target_id: UUID, relation_type: str, weight: float = 1.0) -> Relationship:
        """Instantiate a validated Relationship edge."""
        return Relationship(
            relationship_id=uuid4(),
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            weight=weight
        )

    @staticmethod
    def create_belief(target_id: UUID, probability: float = 1.0) -> Belief:
        """Instantiate an epistemic Belief wrapper."""
        return Belief(
            belief_id=uuid4(),
            target_id=target_id,
            probability=probability,
            last_validated=datetime.utcnow()
        )
