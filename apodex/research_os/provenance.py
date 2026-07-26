from __future__ import annotations
import uuid
import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class PROVNode(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    properties: Dict[str, Any] = Field(default_factory=dict)


class PROVEntity(PROVNode):
    """An artifact, dataset, theory, or document produced during research."""
    type: str = "Entity"


class PROVActivity(PROVNode):
    """An action, run, compiled task, or peer-review process."""
    type: str = "Activity"


class PROVAgent(PROVNode):
    """An executing research sub-agent, LLM node, or human reviewer."""
    type: str = "Agent"


class ProvenanceEngine:
    """
    Implements W3C PROV-O compliant lineage and provenance tracking
    for all scientific research workflows.
    """

    def __init__(self) -> None:
        self.entities: Dict[uuid.UUID, PROVEntity] = {}
        self.activities: Dict[uuid.UUID, PROVActivity] = {}
        self.agents: Dict[uuid.UUID, PROVAgent] = {}
        # Directed relationships: (child_id, parent_id, relation_type)
        self.relations: List[tuple[uuid.UUID, uuid.UUID, str]] = []

    def record_entity(self, properties: Dict[str, Any]) -> PROVEntity:
        entity = PROVEntity(properties=properties)
        self.entities[entity.id] = entity
        return entity

    def record_activity(self, properties: Dict[str, Any]) -> PROVActivity:
        activity = PROVActivity(properties=properties)
        self.activities[activity.id] = activity
        return activity

    def record_agent(self, properties: Dict[str, Any]) -> PROVAgent:
        agent = PROVAgent(properties=properties)
        self.agents[agent.id] = agent
        return agent

    def assert_relation(self, source_id: uuid.UUID, target_id: uuid.UUID, relation_type: str) -> None:
        """
        Asserts a PROV-O relation (e.g., 'wasGeneratedBy', 'wasAssociatedWith', 'used').
        """
        self.relations.append((source_id, target_id, relation_type))

    def query_lineage(self, entity_id: uuid.UUID) -> List[Dict[str, Any]]:
        """Traverses the directed lineage graph backwards to find ancestral entities and activities."""
        lineage = []
        for src, tgt, rel in self.relations:
            if src == entity_id:
                lineage.append({
                    "ancestor_id": tgt,
                    "relation_type": rel,
                    "ancestor_type": "Activity" if tgt in self.activities else "Entity" if tgt in self.entities else "Agent"
                })
        return lineage
