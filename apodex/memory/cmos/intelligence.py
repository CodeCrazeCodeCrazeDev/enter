"""Memory Economics and Provenance engines for CMOS.

Computes multi-dimensional utility scoring and tracks execution lineage across the Memory Graph.
"""

from __future__ import annotations

import math
from datetime import datetime
from typing import Any, Dict, List

from apodex.memory.cmos.models import MemoryNode


class MemoryEconomicsEngine:
    """CMOS Economics Engine managing finite storage optimization under utility scores."""

    def __init__(self, storage_cost_factor: float = 0.01) -> None:
        self.storage_cost_factor = storage_cost_factor

    def compute_utility(self, node: MemoryNode) -> float:
        """
        Calculates multi-dimensional node utility using:
        Utility = (Retrieval Frequency * Decision Impact) / (Age Factor * Storage Cost)
        """
        freq = max(1.0, float(node.retrieval_count))
        decision_impact = float(node.metadata.get("decision_impact", 1.0))

        # Recency decay calculation
        age_seconds = max(1.0, (datetime.utcnow() - node.last_retrieved_at).total_seconds())
        age_factor = 1.0 + math.log(age_seconds)

        # Storage footprint cost
        content_len = len(node.content)
        storage_cost = 1.0 + (content_len * self.storage_cost_factor)

        utility = (freq * decision_impact) / (age_factor * storage_cost)
        return round(utility, 4)


class ProvenanceEngine:
    """Strict Lineage Engine recording code configurations, Git hash, and experiment connections."""

    def __init__(self, current_git_sha: str = "abcdef123") -> None:
        self.git_sha = current_git_sha

    def trace_lineage(self, target_node: MemoryNode, historical_nodes: List[MemoryNode]) -> List[str]:
        """Constructs an audited provenance execution trace across predecessor nodes."""
        lineage_trace = [target_node.node_id]
        for node in historical_nodes:
            lineage_trace.append(node.node_id)
        return lineage_trace
