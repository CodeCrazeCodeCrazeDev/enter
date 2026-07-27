"""Memory & Knowledge Infrastructure Context implementation for SERO v2.

Implements the active Knowledge Operating System (KOS) substrate including the
Bayesian Belief Engine, Contradiction Detection Agent, and Theory Formation Loop.
"""

from __future__ import annotations
import math
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from ..interfaces.services import IKnowledgeInfrastructure
from ..infrastructure.persistence import InMemoryLedger
from ..domain.models import Hypothesis, Evidence, Theory, Contradiction

logger = logging.getLogger("sero.kos")


class IKGNode(BaseModel):
    """A node inside the Institutional Knowledge Graph (IKG)."""
    node_id: str
    node_type: str  # e.g. "paper", "experiment", "dataset", "feature", "model", "capability", "decision", "hypothesis", "evidence", "theory", "contradiction"
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

        # Dedicated KOS Ledgers
        self.hypotheses = InMemoryLedger[Hypothesis]()
        self.evidence_ledger = InMemoryLedger[Evidence]()
        self.theories = InMemoryLedger[Theory]()
        self.contradictions = InMemoryLedger[Contradiction]()

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
    # Bayesian Belief Engine
    # ------------------------------------------------------------------
    def update_hypothesis_belief(self, hypothesis_id: str, evidence: Evidence) -> None:
        """Perform standard conjugate Bayesian updating on the target Hypothesis posterior."""
        hyp = self.hypotheses.get(hypothesis_id)
        if not hyp:
            logger.warning(f"Failed to update belief: Hypothesis '{hypothesis_id}' not found.")
            return

        # Save evidence in ledger
        self.evidence_ledger.save(evidence.evidence_id, evidence)
        self.record_node(evidence.evidence_id, "evidence", {"source": evidence.source, "method": evidence.method})
        self.record_edge(hypothesis_id, evidence.evidence_id, "EVALUATED_BY")

        # Prior confidence
        prior = hyp.posterior_confidence

        # Evidence strength (using sample size and effect size to scale probability weight)
        p_val = float(evidence.strength.get("p_value", 0.05))
        sample_size = int(evidence.strength.get("sample_size", 100))
        effect_size = float(evidence.strength.get("effect_size", 1.0))

        # Reliability factor scaled by method type
        reliability_priors = {"pilot": 0.90, "experiment": 0.85, "simulation": 0.70, "literature": 0.60}
        reliability = reliability_priors.get(evidence.method, 0.50)

        # Compute Bayes update factor: success signal is inversely proportional to p_value
        success_ratio = 1.0 - p_val if p_val < 0.5 else p_val
        signal_weight = min(1.0, (sample_size / 200.0) * effect_size) * reliability

        # Posterior calculation
        posterior = prior * (1.0 + (success_ratio - prior) * signal_weight)
        hyp.posterior_confidence = min(1.0, max(0.0, posterior))

        # Record evidence mapping
        if p_val < 0.05:
            hyp.supporting_evidence.append(evidence.evidence_id)
        else:
            hyp.contradicting_evidence.append(evidence.evidence_id)

        self.hypotheses.save(hypothesis_id, hyp)

        # Reflect in standard IKG node confidence
        hyp_node = self.nodes.get(hypothesis_id)
        if hyp_node:
            hyp_node.confidence = hyp.posterior_confidence
            self.nodes.save(hypothesis_id, hyp_node)

        logger.info(f"Bayesian Belief Engine Updated: Hypothesis {hypothesis_id} posterior confidence shifted from {prior:.4f} to {hyp.posterior_confidence:.4f}")

    # ------------------------------------------------------------------
    # Contradiction Detection Agent
    # ------------------------------------------------------------------
    def detect_contradictions(self) -> List[Contradiction]:
        """Scan Hypothesis pairs for inconsistent or contradicting posterior beliefs."""
        logger.info("Executing Contradiction Detection Agent scanning over KOS substrate...")
        detected = []
        all_hyps = self.hypotheses.list_all()

        for i in range(len(all_hyps)):
            for j in range(i + 1, len(all_hyps)):
                h1 = all_hyps[i]
                h2 = all_hyps[j]

                # Logical/Belief contradiction check:
                # If they both represent opposite claims or are deeply linked but have conflicting confidence intervals
                # e.g., if one says success is 90% and the other says success is 10% on the same parameter space
                is_contradiction = (
                    h1.domain == h2.domain and
                    abs(h1.posterior_confidence - h2.posterior_confidence) > 0.40 and
                    h1.status == "active" and h2.status == "active"
                )

                if is_contradiction:
                    con_id = f"con_{str(h1.hypothesis_id)[:8]}_{str(h2.hypothesis_id)[:8]}"
                    contradiction = Contradiction(
                        contradiction_id=con_id,
                        node_a=str(h1.hypothesis_id),
                        node_b=str(h2.hypothesis_id),
                        detected_by="ContradictionDetectionAgent",
                        resolution_status="pending"
                    )
                    self.contradictions.save(con_id, contradiction)
                    self.record_node(con_id, "contradiction", {"node_a": contradiction.node_a, "node_b": contradiction.node_b})
                    self.record_edge(con_id, str(h1.hypothesis_id), "CONTRADICTS")
                    self.record_edge(con_id, str(h2.hypothesis_id), "CONTRADICTS")
                    detected.append(contradiction)
                    logger.warning(f"CONTRADICTION DETECTED between {h1.hypothesis_id} and {h2.hypothesis_id} in domain '{h1.domain}'!")

        return detected

    # ------------------------------------------------------------------
    # Theory Formation Loop
    # ------------------------------------------------------------------
    def promote_to_theories(self) -> List[Theory]:
        """Scan highly validated hypotheses and promote generalized explanatory models to Theory nodes."""
        logger.info("Executing Theory Formation Loop over validated KOS nodes...")
        promoted = []
        all_hyps = self.hypotheses.list_all()

        for hyp in all_hyps:
            # Generalization threshold: Hypothesis must survive multiple tests and have high posterior confidence
            if hyp.posterior_confidence > 0.80 and len(hyp.supporting_evidence) >= 2 and hyp.status in ["active", "registered", "validated"]:
                theory_id = f"theory_{str(hyp.hypothesis_id)[:8]}"

                # Auto-generate untested general predictions scoped beyond original context
                prediction_statement = f"Generalized expectation for domain {hyp.domain}: any subtask under this parameter space will achieve success with confidence > {hyp.posterior_confidence:.2f}"

                theory = Theory(
                    theory_id=theory_id,
                    statement=f"General explanatory theory derived from hypothesis: {hyp.statement or hyp.title}",
                    constituent_hypotheses=[str(hyp.hypothesis_id)],
                    predictive_scope=[prediction_statement],
                    confidence=hyp.posterior_confidence
                )
                self.theories.save(theory_id, theory)
                self.record_node(theory_id, "theory", {"statement": theory.statement})
                self.record_edge(theory_id, str(hyp.hypothesis_id), "CONSOLIDATES")

                # Promote hypothesis status
                hyp.status = "theory-promoted"
                self.hypotheses.save(str(hyp.hypothesis_id), hyp)

                promoted.append(theory)
                logger.info(f"PROMOTED HYPOTHESIS to Theory node: {theory_id} [confidence={theory.confidence:.4f}]")

        return promoted

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
