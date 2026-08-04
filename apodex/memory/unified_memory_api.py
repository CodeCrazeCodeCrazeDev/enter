from __future__ import annotations
import logging
import uuid
import threading
from datetime import datetime, UTC
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from apodex.arcs.world_graph import WorldGraph, EntityNode, RelationshipEdge, BeliefNode

logger = logging.getLogger("arcs.memory")


class MemoryType(str, Enum):
    SEMANTIC = "semantic"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"
    STRATEGIC = "strategic"
    COMPETITIVE = "competitive"
    NEGOTIATION = "negotiation"
    BRAND = "brand"
    FINANCIAL = "financial"
    INVESTOR = "investor"
    HIRING = "hiring"
    OPERATIONAL = "operational"
    MARKET = "market"
    SIMULATION = "simulation"
    FAILURE = "failure"
    TACIT = "tacit"
    SCIENTIFIC = "scientific"
    POLICY = "policy"


class MemoryEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MemoryType
    tenant_id: str
    context: Dict[str, Any] = Field(default_factory=dict)
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    belief: float = Field(default=0.5, ge=0.0, le=1.0)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    causal_links: List[str] = Field(default_factory=list)
    counterfactuals: Dict[str, Any] = Field(default_factory=dict)
    historical_outcomes: List[Dict[str, Any]] = Field(default_factory=list)


class UnifiedMemoryAPI:
    """Thread-safe Unified Memory API wrapping the central WorldGraph.

    Ensures consistent storage and traversal across all 11 memory types.
    """

    def __init__(self, world_graph: Optional[WorldGraph] = None) -> None:
        self.world_graph = world_graph or WorldGraph()
        self._lock = threading.Lock()

    def store_memory(self, entry: MemoryEntry) -> None:
        """Store a MemoryEntry into the central WorldGraph as an EntityNode."""
        with self._lock:
            # Create properties dict, merging context and metadata
            properties = {
                "tenant_id": entry.tenant_id,
                "timestamp": entry.timestamp.isoformat(),
                "belief": entry.belief,
                "confidence": entry.confidence,
                "causal_links": entry.causal_links,
                "counterfactuals": entry.counterfactuals,
                "historical_outcomes": entry.historical_outcomes,
                "context": entry.context,
                "payload": entry.payload,
            }

            node = EntityNode(
                node_id=entry.id,
                node_type=f"memory_{entry.type.value}",
                properties=properties
            )
            self.world_graph.add_node(node)
            logger.info(f"Stored memory: {entry.id} of type {entry.type.value} for tenant {entry.tenant_id}")

    def retrieve_memory(
        self,
        memory_type: MemoryType,
        tenant_id: Optional[str] = None,
        query_context: Optional[Dict[str, Any]] = None,
        limit: int = 10
    ) -> List[MemoryEntry]:
        """Query and filter memory nodes from the WorldGraph."""
        with self._lock:
            target_node_type = f"memory_{memory_type.value}"
            matches: List[MemoryEntry] = []

            for node in self.world_graph.nodes.values():
                if node.node_type != target_node_type:
                    continue

                props = node.properties
                # Filter by tenant if provided
                if tenant_id and props.get("tenant_id") != tenant_id:
                    continue

                # Filter by query context keys/values
                context_match = True
                if query_context:
                    node_context = props.get("context", {})
                    for k, v in query_context.items():
                        if node_context.get(k) != v:
                            context_match = False
                            break

                if context_match:
                    try:
                        timestamp = datetime.fromisoformat(props.get("timestamp"))
                    except Exception:
                        timestamp = datetime.now(UTC)

                    matches.append(
                        MemoryEntry(
                            id=node.node_id,
                            type=memory_type,
                            tenant_id=props.get("tenant_id", ""),
                            context=props.get("context", {}),
                            payload=props.get("payload", {}),
                            timestamp=timestamp,
                            belief=props.get("belief", 0.5),
                            confidence=props.get("confidence", 1.0),
                            causal_links=props.get("causal_links", []),
                            counterfactuals=props.get("counterfactuals", {}),
                            historical_outcomes=props.get("historical_outcomes", [])
                        )
                    )

            # Sort by timestamp descending
            matches.sort(key=lambda m: m.timestamp, reverse=True)
            return matches[:limit]

    def link_memories(self, source_id: str, target_id: str, relation_type: str, weight: float = 1.0) -> None:
        """Create a directed relational link between two memory items."""
        with self._lock:
            edge = RelationshipEdge(
                source_id=source_id,
                target_id=target_id,
                relation_type=relation_type,
                weight=weight,
                properties={}
            )
            self.world_graph.add_relation(edge)
            logger.info(f"Linked memory {source_id} --({relation_type})--> {target_id} [Weight: {weight}]")

    def add_memory_belief(self, belief_id: str, edge_id: str, probability: float, evidence: List[str]) -> None:
        """Attach a Bayesian belief score over a given relation edge."""
        with self._lock:
            belief = BeliefNode(
                belief_id=belief_id,
                target_edge_id=edge_id,
                probability=probability,
                evidence=evidence
            )
            self.world_graph.add_belief(belief)
            logger.info(f"Registered belief {belief_id} on edge {edge_id} with probability {probability:.2f}")
