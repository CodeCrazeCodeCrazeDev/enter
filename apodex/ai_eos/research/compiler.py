"""Research Compiler implementation for SERO v2.1.

Converts raw documents, transcripts, and literature into structured, normalized, and quality-weighted Evidence nodes.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from uuid import uuid4

from ..domain.models import Evidence

logger = logging.getLogger("sero.ros.compiler")


class ResearchCompiler:
    """Ingests raw materials and compiles them into quality-scored, deduplicated Evidence nodes."""

    def __init__(self) -> None:
        self.evidence_cache: Dict[str, Evidence] = {}
        # Synonym table for mapping vocabulary drift cleanly
        self.synonym_table: Dict[str, str] = {
            "customer": "customer",
            "buyer": "customer",
            "user": "customer",
            "client": "customer",
            "cost": "cost",
            "price": "cost",
            "pricing": "cost"
        }

    def compile_to_evidence(self, raw_input: Dict[str, Any], source_type: str) -> List[Evidence]:
        """Convert raw input dictionary into structured and deduplicated Evidence nodes."""
        logger.info(f"Research Compiler ingesting raw item from {raw_input.get('source', 'unknown')}...")

        compiled_evidence = []
        raw_claims = raw_input.get("claims", [])

        for claim in raw_claims:
            statement = claim.get("statement", "").lower()

            # 1. Normalization: Map synonym terms onto canonical vocabulary
            normalized_words = []
            for word in statement.split():
                normalized_words.append(self.synonym_table.get(word, word))
            normalized_statement = " ".join(normalized_words)

            # Deduplication key based on source and normalized statement
            dedup_key = f"{raw_input.get('source')}:{normalized_statement}"
            if dedup_key in self.evidence_cache:
                logger.info(f"Research Compiler: Deduplicated existing evidence key '{dedup_key}'.")
                continue

            # 2. Quality Tier and Reliability Weight Determination
            quality_tier = claim.get("quality_tier", "survey")
            reliability_weights = {
                "rct": 1.0,
                "natural_experiment": 0.8,
                "longitudinal": 0.7,
                "survey": 0.5,
                "interview": 0.4,
                "opinion": 0.2,
                "synthetic": 0.15
            }
            reliability = reliability_weights.get(quality_tier, 0.50)

            # 3. Create Evidence node
            evidence_id = f"ev_compiled_{uuid4().hex[:8]}"
            evidence = Evidence(
                evidence_id=evidence_id,
                source=raw_input.get("source", "unknown"),
                source_type=source_type,
                evidence_quality_tier=quality_tier,
                reliability_weight=reliability,
                strength={
                    "p_value": claim.get("p_value", 0.05),
                    "sample_size": claim.get("sample_size", 100),
                    "effect_size": claim.get("effect_size", 1.0)
                },
                causal_or_correlational=claim.get("causal_or_correlational", "correlational"),
                linked_hypotheses=claim.get("linked_hypotheses", [])
            )

            # Cache and append
            self.evidence_cache[dedup_key] = evidence
            compiled_evidence.append(evidence)
            logger.info(f"Research Compiler: Compiled raw claim to Evidence node {evidence_id} with reliability {reliability:.2f}")

        return compiled_evidence
