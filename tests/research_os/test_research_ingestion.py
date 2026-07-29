# -*- coding: utf-8 -*-
"""
test_research_ingestion.py: Unit and integration tests for the automated
Batch-Based Research Ingestion & Validation Pipeline.
"""
from __future__ import annotations

import os
from apodex.research_os.research_ingestion import ResearchIngestionPipeline


def test_research_ingestion_batches_partition() -> None:
    """Verify the pipeline correctly loads and partitions the 100-paper corpus."""
    pipeline = ResearchIngestionPipeline()
    assert len(pipeline.papers) == 100

    batches = pipeline.get_batches(batch_size=20)
    assert len(batches) == 5
    assert all(len(b) == 20 for b in batches)


def test_research_ingestion_deconstruction() -> None:
    """Verify that a paper is deconstructed into correct metadata and deconstruction fields."""
    pipeline = ResearchIngestionPipeline()
    paper = pipeline.papers[0]
    deconstructed = pipeline.deconstruct_paper(paper)

    assert deconstructed["id"] == 201
    assert deconstructed["title"] is not None
    assert deconstructed["finding"] is not None
    assert deconstructed["mechanism"] is not None
    assert deconstructed["boundary_conditions"] is not None
    assert deconstructed["failure_modes"] is not None
    assert deconstructed["decision"] in ["ACCEPT", "REJECT"]


def test_research_ingestion_mismatch_detection() -> None:
    """Verify the pipeline successfully flags architectural and interface mismatches."""
    pipeline = ResearchIngestionPipeline()
    paper = pipeline.papers[0]
    deconstructed = pipeline.deconstruct_paper(paper)

    # Force mismatches in simulation configurations
    deconstructed["boundary_conditions"] = "T > 10"
    deconstructed["failure_modes"] = "regime switching problems"

    mock_existing_arch = {
        "min_returns_length": 5,
        "supports_regime_switching": False
    }

    mismatches = pipeline.detect_mismatch(deconstructed, mock_existing_arch)
    assert len(mismatches) == 2
    assert "Interface Gap" in mismatches[0]
    assert "Architectural Mismatch" in mismatches[1]


def test_research_ingestion_pipeline_run() -> None:
    """Verify that the end-to-end ingestion pipeline runs successfully and writes decisions."""
    dec_path = "docs/research/papers/ALPHA_ALGO_INGESTION_DECISIONS.yaml"
    if os.path.exists(dec_path):
        os.remove(dec_path)

    pipeline = ResearchIngestionPipeline(decisions_path=dec_path, benchmark_threshold=0.04)
    results = pipeline.run_pipeline()

    assert results["pipeline_status"] == "SUCCESS"
    assert len(results["batches_results"]) == 5
    assert os.path.exists(dec_path)

    # Load file and assert count
    import yaml
    with open(dec_path, "r", encoding="utf-8") as f:
        saved_data = yaml.safe_load(f)
    assert len(saved_data["batches_results"]) == 5
