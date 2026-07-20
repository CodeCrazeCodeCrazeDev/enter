"""Memory & Knowledge Infrastructure Context implementation for AI-EOS.

Implements the Institutional Knowledge Graph (IKG) and multi-tier memory models
with strict lineage tracking, temporal versioning, and confidence propagation.
"""

from __future__ import annotations
import logging
import math
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from ..interfaces.services import IKnowledgeInfrastructure
from ..infrastructure.persistence import InMemoryLedger

logger = logging.getLogger("ai_eos.memory")


class IKGNode(BaseModel):
    """A node inside the Institutional Knowledge Graph (IKG)."""
    node_id: str
    node_type: str  # e.g. "paper", "experiment", "dataset", "feature", "model", "capability", "decision"
    properties: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_retrieved_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = Field(1, ge=1)


class IKGEdge(BaseModel):
    """A directed edge inside the Institutional Knowledge Graph (IKG)."""
    edge_id: str = Field(default_factory=lambda: f"edge_{uuid4().hex[:12]}")
    source_id: str
    target_id: str
    relation_type: str  # e.g. "DEPENDS_ON", "EVALUATES", "SUPPORTS", "ORIGINATES_FROM"
    weight: float = Field(1.0, ge=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class KnowledgeInfrastructure(IKnowledgeInfrastructure):
    """Institutional Knowledge Graph and multi-tier memory infrastructure."""

    def __init__(self) -> None:
        self.nodes = InMemoryLedger[IKGNode]()
        self.edges = InMemoryLedger[IKGEdge]()
        # Keep historical versions for temporal versioning
        self.historical_nodes = InMemoryLedger[List[IKGNode]]()

    def record_node(self, node_id: str, node_type: str, properties: Dict[str, Any]) -> None:
        """Record or update a node in the IKG with temporal versioning."""
        existing = self.nodes.get(node_id)
        if existing:
            # Store existing version in history
            history = self.historical_nodes.get(node_id) or []
            history.append(existing.copy())
            self.historical_nodes.save(node_id, history)

            # Update with new version
            updated = IKGNode(
                node_id=node_id,
                node_type=node_type,
                properties=properties,
                confidence=existing.confidence,
                version=existing.version + 1,
                created_at=existing.created_at,
                last_retrieved_at=datetime.utcnow()
            )
            self.nodes.save(node_id, updated)
            logger.debug(f"Updated IKG Node: {node_id} to version {updated.version}")
        else:
            new_node = IKGNode(
                node_id=node_id,
                node_type=node_type,
                properties=properties,
                confidence=1.0,
                version=1,
                created_at=datetime.utcnow(),
                last_retrieved_at=datetime.utcnow()
            )
            self.nodes.save(node_id, new_node)
            logger.info(f"Recorded new IKG Node: {node_id} ({node_type})")

    def record_edge(self, source_id: str, target_id: str, relation_type: str, weight: float = 1.0) -> None:
        """Record a directed relation edge between two nodes."""
        edge_id = f"{source_id}:{target_id}:{relation_type}"
        edge = IKGEdge(
            edge_id=edge_id,
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            weight=weight
        )
        self.edges.save(edge_id, edge)
        logger.info(f"Recorded IKG Relation: {source_id} --[{relation_type}]--> {target_id}")

    # ------------------------------------------------------------------
    # Memory Decay Policy
    # ------------------------------------------------------------------
    def apply_memory_decay(self, decay_rate: float = 0.05) -> None:
        """Apply temporal exponential decay to the weights of all IKG edges based on idle days."""
        now = datetime.utcnow()
        for edge in self.edges.list_all():
            days_elapsed = (now - edge.created_at).total_seconds() / 86400.0
            decay_factor = math.exp(-decay_rate * days_elapsed)
            edge.weight = max(0.0, edge.weight * decay_factor)
            self.edges.save(edge.edge_id, edge)

    # ------------------------------------------------------------------
    # Confidence Propagation Algorithm
    # ------------------------------------------------------------------
    def propagate_confidence(self, node_id: str) -> None:
        """Propagate confidence updates from updated node downstream to dependents."""
        root_node = self.nodes.get(node_id)
        if not root_node:
            return

        visited = set()
        queue = [root_node]

        while queue:
            current = queue.pop(0)
            if current.node_id in visited:
                continue
            visited.add(current.node_id)

            # Find all outgoing edges from this node representing dependency chains
            # e.g., if target DEPENDS_ON source, then updates in source propagate to target
            for edge in self.edges.list_all():
                if edge.target_id == current.node_id and edge.relation_type == "DEPENDS_ON":
                    dependent = self.nodes.get(edge.source_id)
                    if dependent and dependent.node_id not in visited:
                        # Composite confidence calculation
                        old_conf = dependent.confidence
                        dependent.confidence = min(dependent.confidence, current.confidence * edge.weight)
                        if dependent.confidence != old_conf:
                            dependent.last_retrieved_at = datetime.utcnow()
                            self.nodes.save(dependent.node_id, dependent)
                            logger.info(f"Propagated confidence: {dependent.node_id} confidence updated from {old_conf:.4f} to {dependent.confidence:.4f}")
                            queue.append(dependent)

    # ------------------------------------------------------------------
    # Provenance Lineage Querying
    # ------------------------------------------------------------------
    def get_provenance_lineage(self, capability_id: str) -> List[Dict[str, Any]]:
        """Traverse the IKG upstream to fetch the complete trace of a capability's origins."""
        lineage = []
        visited = set()
        queue = [capability_id]

        while queue:
            curr_id = queue.pop(0)
            if curr_id in visited:
                continue
            visited.add(curr_id)

            node = self.nodes.get(curr_id)
            if node:
                lineage.append({
                    "node_id": node.node_id,
                    "node_type": node.node_type,
                    "properties": node.properties,
                    "confidence": node.confidence,
                    "version": node.version
                })

                # Traverse backwards (incoming links to current node representing 'ORIGINATES_FROM', 'DEPENDS_ON', etc.)
                for edge in self.edges.list_all():
                    if edge.source_id == curr_id:
                        queue.append(edge.target_id)

        return lineage
