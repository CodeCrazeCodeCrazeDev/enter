from __future__ import annotations
from uuid import UUID, uuid4
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field
from .models import BaseArtifact

# =====================================================================
# Provenance Graph Subsystem (W3C PROV-O Standard)
# =====================================================================

class ProvenanceRelation(BaseModel):
    relation_id: UUID = Field(default_factory=uuid4)
    relation_type: str  # "WAS_GENERATED_BY" | "USED_DATASET" | "WAS_ATTRIBUTED_TO" | "DERIVED_FROM"
    source_uuid: UUID
    target_uuid: UUID


class ProvenanceEngine:
    """
    Constructs, models, and queries full execution lineages and artifact relationships,
    conforming strictly to the W3C PROV-O ontology.
    """

    def __init__(self) -> None:
        self.relations: List[ProvenanceRelation] = []

    def record_relation(self, rel_type: str, source: UUID, target: UUID) -> None:
        self.relations.append(ProvenanceRelation(
            relation_type=rel_type,
            source_uuid=source,
            target_uuid=target
        ))

    def get_generating_agent(self, artifact: BaseArtifact) -> str:
        """Returns the primary author/agent responsible for creating an artifact."""
        return artifact.author

    def trace_source_datasets(self, artifact_uuid: UUID) -> List[UUID]:
        """
        Recursively traces backward through WAS_GENERATED_BY, DERIVED_FROM,
        and USED_DATASET relations to return all raw source dataset or corpus UUIDs.
        """
        source_datasets: Set[UUID] = set()
        visited: Set[UUID] = set()

        def _dfs(curr_uuid: UUID) -> None:
            if curr_uuid in visited:
                return
            visited.add(curr_uuid)

            for rel in self.relations:
                if rel.source_uuid == curr_uuid:
                    if rel.relation_type in ["DERIVED_FROM", "WAS_GENERATED_BY"]:
                        _dfs(rel.target_uuid)
                    elif rel.relation_type == "USED_DATASET":
                        source_datasets.add(rel.target_uuid)

        _dfs(artifact_uuid)
        return list(source_datasets)

    def get_supporting_experiments(self, claim_uuid: UUID) -> List[UUID]:
        """Finds experiment result UUIDs that supported a specific claim."""
        experiments = []
        for rel in self.relations:
            if rel.source_uuid == claim_uuid and rel.relation_type == "DERIVED_FROM":
                experiments.append(rel.target_uuid)
        return experiments
