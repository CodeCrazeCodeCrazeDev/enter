from __future__ import annotations
from uuid import UUID
from typing import List

from .models import (
    BaseArtifact,
    ConceptNode,
    TheoryNode,
    ClaimNode,
    EvidenceNode,
    ContradictionNode,
)
from .storage import ResearchRepository
from .events import EventBus, BaseEvent

# =====================================================================
# Contradiction Event
# =====================================================================

class ContradictionDetected(BaseEvent):
    contradiction_uuid: UUID
    node_a: UUID
    node_b: UUID
    explanation: str


# =====================================================================
# Cognitive Knowledge Graph Layer
# =====================================================================

class ActiveKnowledgeGraph:
    """
    Cognitive layer wrapping physical storage. Coordinates theory promotion,
    deductive relation mapping, and automated contradiction detection.
    """

    def __init__(self, repository: ResearchRepository, event_bus: EventBus) -> None:
        self.repo = repository
        self.bus = event_bus

    def add_concept(self, name: str, definition: str) -> ConceptNode:
        node = ConceptNode(concept_name=name, definition=definition)
        node = node.with_signature()
        self.repo.save_artifact(node)
        return node

    def add_evidence(self, source_url: str, content: str, provenance: str) -> EvidenceNode:
        node = EvidenceNode(source_url=source_url, content=content, provenance=provenance)
        node = node.with_signature()
        self.repo.save_artifact(node)
        self._check_for_contradictions(node)
        return node

    def add_claim(self, assertion: str, evidence_ids: List[UUID], limitations: List[str] = None) -> ClaimNode:
        node = ClaimNode(
            assertion=assertion,
            evidence_ids=evidence_ids,
            known_limitations=limitations or []
        )
        node = node.with_signature()
        self.repo.save_artifact(node)
        self._check_for_contradictions(node)
        self._evaluate_theory_promotion()
        return node

    def _check_for_contradictions(self, new_node: BaseArtifact) -> None:
        """
        Deductive contradiction check.
        If a claim or evidence directly negates/contradicts an existing node (by simple keyword opposite
        matching, e.g. 'not', 'fails', 'improve' vs 'degrade' or identical names with mismatched scores),
        log a ContradictionNode into the graph and publish an event.
        """
        # Load all existing nodes of the same type
        if isinstance(new_node, ClaimNode):
            existing_claims = self.repo.list_artifacts_by_type(ClaimNode)
            new_text = new_node.assertion.lower()

            for old_claim in existing_claims:
                if old_claim.uuid == new_node.uuid:
                    continue

                old_text = old_claim.assertion.lower()
                # Simplified contradiction check: same core words but opposing polarity or explicit negative mismatch
                common_words = set(new_text.split()).intersection(set(old_text.split()))
                if len(common_words) >= 3:
                    is_neg_a = "not" in new_text or "fail" in new_text or "degrade" in new_text
                    is_neg_b = "not" in old_text or "fail" in old_text or "degrade" in old_text
                    if is_neg_a != is_neg_b:
                        # Contradiction found!
                        conflict = ContradictionNode(
                            conflict_node_a=old_claim.uuid,
                            conflict_node_b=new_node.uuid,
                            explanation=f"Logical clash detected between: '{old_claim.assertion}' and '{new_node.assertion}'."
                        ).with_signature()

                        self.repo.save_artifact(conflict)
                        self.repo.kg.add_edge(conflict.uuid, old_claim.uuid, "CONTRADICTS")
                        self.repo.kg.add_edge(conflict.uuid, new_node.uuid, "CONTRADICTS")

                        self.bus.publish(ContradictionDetected(
                            contradiction_uuid=conflict.uuid,
                            node_a=old_claim.uuid,
                            node_b=new_node.uuid,
                            explanation=conflict.explanation
                        ))

    def _evaluate_theory_promotion(self) -> None:
        """
        Theory Promotion Loop:
        Scans ClaimNodes. If a cluster of verified claims (e.g., confidence >= 0.8) are grounded in
        at least 2 evidence nodes, promote them into a single comprehensive TheoryNode.
        """
        claims = self.repo.list_artifacts_by_type(ClaimNode)
        promotable_claims = []

        for claim in claims:
            # Check validation, confidence threshold, and supporting evidence volume
            if claim.confidence >= 0.8 and len(claim.evidence_ids) >= 2:
                promotable_claims.append(claim)

        if len(promotable_claims) >= 2:
            # Ensure we haven't already promoted this exact combination of claims to a theory
            existing_theories = self.repo.list_artifacts_by_type(TheoryNode)
            promotable_uuids = set(c.uuid for c in promotable_claims)

            for theory in existing_theories:
                if set(theory.linked_claims) == promotable_uuids:
                    return # Already promoted

            # Promote!
            theory_node = TheoryNode(
                theory_name="Evolving Unified Core Theory",
                description="Formulated core framework generalizing highly supported semantic claims.",
                linked_claims=list(promotable_uuids)
            ).with_signature()

            self.repo.save_artifact(theory_node)
