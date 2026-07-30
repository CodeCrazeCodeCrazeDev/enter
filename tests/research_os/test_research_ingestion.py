# -*- coding: utf-8 -*-
"""
test_research_ingestion.py: Unit and integration tests for the automated
Research Ingestion and Validation Pipeline.
"""
from __future__ import annotations

import os
import pytest
import yaml
from apodex.research_os.research_ingestion import ResearchIngestionPipeline


@pytest.fixture
def pipeline() -> ResearchIngestionPipeline:
    """Fixture for initializing ResearchIngestionPipeline."""
    papers_path = "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    decisions_path = "docs/research/papers/ALPHA_ALGO_INGESTION_DECISIONS.yaml"
    return ResearchIngestionPipeline(
        papers_yaml_path=papers_path,
        decisions_yaml_path=decisions_path
    )


def test_papers_loaded_successfully(pipeline: ResearchIngestionPipeline) -> None:
    """Verify that exactly 100 papers are successfully loaded from the YAML file."""
    assert len(pipeline.papers) == 100
    # Verify paper fields
    for paper in pipeline.papers:
        assert "id" in paper
        assert "metadata" in paper
        assert "technical_facts" in paper
        assert "analysis" in paper
        assert "reproducibility" in paper
        assert "confidence" in paper


def test_batch_partitioning(pipeline: ResearchIngestionPipeline) -> None:
    """Verify that papers are partitioned into exactly 5 batches of 20 papers."""
    batches = pipeline.partition_batches(batch_size=20)
    assert len(batches) == 5
    for batch in batches:
        assert len(batch) == 20


def test_pipeline_stages(pipeline: ResearchIngestionPipeline) -> None:
    """Test individual paper-level lifecycle evaluation stages."""
    paper = pipeline.papers[0]

    # 1. Deconstruct
    deconstructed = pipeline.deconstruct_paper(paper)
    assert deconstructed["title"] == paper["metadata"]["title"]
    assert "core_mechanism" in deconstructed
    assert "assumptions" in deconstructed

    # 2. Detect Mismatch
    mismatch = pipeline.detect_mismatches(paper, deconstructed)
    assert mismatch["has_mismatch"] is True
    assert "mismatch_type" in mismatch

    # 3. Design Improvements
    improvement = pipeline.design_improvements(paper, mismatch)
    assert "proposed_module" in improvement

    # 4. Benchmark
    benchmark = pipeline.benchmark_proposed_integration(paper, improvement)
    assert "simulated_sharpe_improvement" in benchmark
    assert "error_reduction_pct" in benchmark
    assert "is_viable" in benchmark

    # 5. Decision
    decision = pipeline.make_integration_decision(paper, benchmark)
    assert decision in ["ACCEPT", "REJECT", "ROLLBACK"]


def test_run_pipeline_execution(pipeline: ResearchIngestionPipeline) -> None:
    """Test end-to-end pipeline execution and output verification."""
    # Run the pipeline
    summary = pipeline.run_pipeline()

    assert summary["total_papers_ingested"] == 100
    assert summary["total_batches_processed"] == 5
    assert "summary_metrics" in summary
    assert "accepted" in summary["summary_metrics"]
    assert "rejected" in summary["summary_metrics"]
    assert "rolled_back" in summary["summary_metrics"]

    # Verify that decisions file is generated and matches
    assert os.path.exists(pipeline.decisions_yaml_path)
    with open(pipeline.decisions_yaml_path, "r", encoding="utf-8") as f:
        saved_data = yaml.safe_load(f)
        assert saved_data["total_papers_ingested"] == 100
        assert len(saved_data["batches"]) == 5

        # Verify batch 1 has 20 decisions
        first_batch = saved_data["batches"][0]
        assert first_batch["batch_size"] == 20
        assert len(first_batch["decisions"]) == 20

        # Verify decision fields inside log
        first_decision = first_batch["decisions"][0]
        assert "paper_id" in first_decision
        assert "title" in first_decision
        assert "lifecycle_evaluation" in first_decision
        assert "decision" in first_decision
        assert "justification" in first_decision


def test_bibliography_generated() -> None:
    """Verify that the generated Markdown bibliography matches expectations."""
    bib_path = "docs/research/papers/ALPHA_ALGO_100_NEW_BIBLIOGRAPHY.md"
    assert os.path.exists(bib_path)
    with open(bib_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "# AlphaAlgo 100 New Research Bibliography" in content
        assert "Strategic & Operational SOTA Research Corpus" in content
        # Check first paper and some content
        assert "Dynamic Cointegration Arbitrage with Deep Transformer Networks" in content
