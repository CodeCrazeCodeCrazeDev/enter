"""Economic Knowledge Graph (EKG) — the central nervous system of AEAN.

The EKG is a living semantic substrate that every engine reads from and writes
to. It is intentionally domain-agnostic: nodes carry a ``node_type`` and an
arbitrary property bag, and edges are typed, directed and weighted. On top of
the raw graph the EKG maintains typed collections for the first-class economic
entities (demand signals, narratives, assets, micro-cells) so engines can query
them efficiently without walking the whole graph.

The design mirrors ``apodex.arcs.world_graph.WorldGraph`` but is specialised for
the compounding flywheel: every write is timestamped and appended to an event
log so the Research engine can mine patterns from historical outcomes.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .models import DemandSignal, MicroCell, MicroCellStatus, Narrative, VisualAsset

logger = logging.getLogger("aean.ekg")


class GraphNode(BaseModel):
    node_id: str
    node_type: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    relation: str
    weight: float = 1.0
    properties: Dict[str, Any] = Field(default_factory=dict)


class EKGEvent(BaseModel):
    """An append-only record of a write to the graph."""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    kind: str
    ref_id: str
    payload: Dict[str, Any] = Field(default_factory=dict)


class EconomicKnowledgeGraph:
    """Shared substrate connecting all six AEAN engines."""

    def __init__(self) -> None:
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        self._adjacency: Dict[str, List[GraphEdge]] = defaultdict(list)

        # Typed first-class collections.
        self.signals: Dict[str, DemandSignal] = {}
        self.narratives: Dict[str, Narrative] = {}
        self.assets: Dict[str, VisualAsset] = {}
        self.cells: Dict[str, MicroCell] = {}

        # Append-only event log for the Research engine.
        self.events: List[EKGEvent] = []

    # ------------------------------------------------------------------
    # Raw graph primitives
    # ------------------------------------------------------------------
    def upsert_node(self, node_id: str, node_type: str, **properties: Any) -> GraphNode:
        node = self.nodes.get(node_id)
        if node is None:
            node = GraphNode(node_id=node_id, node_type=node_type, properties=dict(properties))
            self.nodes[node_id] = node
        else:
            node.properties.update(properties)
        return node

    def add_edge(self, source_id: str, target_id: str, relation: str, weight: float = 1.0, **properties: Any) -> GraphEdge:
        for node_id in (source_id, target_id):
            if node_id not in self.nodes:
                self.upsert_node(node_id, "unknown")
        # Merge duplicates (same triple) by updating the weight.
        for edge in self._adjacency[source_id]:
            if edge.target_id == target_id and edge.relation == relation:
                edge.weight = weight
                edge.properties.update(properties)
                return edge
        edge = GraphEdge(source_id=source_id, target_id=target_id, relation=relation, weight=weight, properties=dict(properties))
        self.edges.append(edge)
        self._adjacency[source_id].append(edge)
        return edge

    def neighbors(self, node_id: str, relation: Optional[str] = None) -> List[GraphEdge]:
        edges = self._adjacency.get(node_id, [])
        if relation is None:
            return list(edges)
        return [e for e in edges if e.relation == relation]

    # ------------------------------------------------------------------
    # Typed writes (used by the engines)
    # ------------------------------------------------------------------
    def record_signal(self, signal: DemandSignal) -> None:
        self.signals[signal.signal_id] = signal
        self.upsert_node(f"market:{signal.market}", "market", name=signal.market)
        self.upsert_node(
            signal.signal_id,
            "demand_signal",
            strength=signal.strength,
            segment=signal.segment,
            tam_cents=signal.estimated_tam_cents,
        )
        self.add_edge(signal.signal_id, f"market:{signal.market}", "TARGETS", weight=signal.strength)
        self._log("demand_signal", signal.signal_id, {"strength": signal.strength, "market": signal.market})

    def record_narrative(self, narrative: Narrative) -> None:
        self.narratives[narrative.narrative_id] = narrative
        self.upsert_node(narrative.narrative_id, "narrative", theme=narrative.theme, resonance=narrative.predicted_resonance)
        self.add_edge(narrative.narrative_id, narrative.signal_id, "RESPONDS_TO", weight=narrative.predicted_resonance)
        self._log("narrative", narrative.narrative_id, {"resonance": narrative.predicted_resonance})

    def record_asset(self, asset: VisualAsset) -> None:
        self.assets[asset.asset_id] = asset
        self.upsert_node(asset.asset_id, "visual_asset", concept=asset.concept, predicted_ctr=asset.predicted_ctr)
        self.add_edge(asset.asset_id, asset.narrative_id, "RENDERS", weight=asset.predicted_ctr)
        self._log("visual_asset", asset.asset_id, {"predicted_ctr": asset.predicted_ctr})

    def record_cell(self, cell: MicroCell) -> None:
        self.cells[cell.cell_id] = cell
        self.upsert_node(
            cell.cell_id,
            "micro_cell",
            status=cell.status.value,
            allocated_cents=cell.allocated_cents,
            roi=cell.roi,
        )
        self.add_edge(cell.cell_id, cell.signal_id, "EXPLOITS", weight=1.0)
        self._log("micro_cell", cell.cell_id, {"status": cell.status.value, "roi": cell.roi})

    def _log(self, kind: str, ref_id: str, payload: Dict[str, Any]) -> None:
        self.events.append(EKGEvent(kind=kind, ref_id=ref_id, payload=payload))

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def active_cells(self) -> List[MicroCell]:
        return [c for c in self.cells.values() if c.status in (MicroCellStatus.ACTIVE, MicroCellStatus.SCALED)]

    def open_signals(self) -> List[DemandSignal]:
        """Signals that do not yet have a micro-cell exploiting them."""
        exploited = {c.signal_id for c in self.cells.values()}
        return [s for s in self.signals.values() if s.signal_id not in exploited]

    def narratives_for(self, signal_id: str) -> List[Narrative]:
        return [n for n in self.narratives.values() if n.signal_id == signal_id]

    def assets_for(self, narrative_id: str) -> List[VisualAsset]:
        return [a for a in self.assets.values() if a.narrative_id == narrative_id]

    def stats(self) -> Dict[str, int]:
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "signals": len(self.signals),
            "narratives": len(self.narratives),
            "assets": len(self.assets),
            "cells": len(self.cells),
            "events": len(self.events),
        }
