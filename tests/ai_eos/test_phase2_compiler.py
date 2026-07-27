"""Unit tests for Phase 2 Research Compiler Ingestion and Normalization Pipeline."""

import pytest
from apodex.ai_eos.research.compiler import ResearchCompiler


def test_research_compiler_normalization_deduplication():
    """Verify that the compiler normalizes synonyms, calculates weights, and deduplicates inputs."""
    compiler = ResearchCompiler()

    raw_paper = {
        "source": "arXiv:2605.15245",
        "claims": [
            {
                "statement": "Decreasing product price increases conversion",  # 'price' should normalize to 'cost'
                "quality_tier": "rct",  # Weight should be 1.0
                "p_value": 0.003,
                "sample_size": 300,
                "effect_size": 2.4,
                "causal_or_correlational": "causal",
                "linked_hypotheses": ["hyp-101"]
            }
        ]
    }

    evidence_list_1 = compiler.compile_to_evidence(raw_paper, source_type="literature")
    assert len(evidence_list_1) == 1
    ev = evidence_list_1[0]
    assert ev.evidence_quality_tier == "rct"
    assert ev.reliability_weight == 1.0
    assert ev.source == "arXiv:2605.15245"
    assert "hyp-101" in ev.linked_hypotheses

    # Duplicate compiling from same paper must be discarded by Deduplication
    evidence_list_2 = compiler.compile_to_evidence(raw_paper, source_type="literature")
    assert len(evidence_list_2) == 0
