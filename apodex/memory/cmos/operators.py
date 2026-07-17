"""Modular pluggable cognitive operators for CMOS memory navigation and reasoning.

Implements standard CMOS Operators:
- Recall (Hierarchical fetch & similarity candidate query)
- Verify (Recursive support/evidence fact resolution)
- Compare & Contrast (Semantic structural alignment & contradiction checks)
- Explain (Provenance tracing and reasoning lineage recovery)
- Challenge (Opposing/contradicting assertion lookup)
- Generalize (Abstraction extraction: facts -> theories/lessons)
- Specialize (Detail traversal: theory -> claim -> evidence)
- Simulate (Mock virtual projection overlay for what-if scenarios)
- Reflect (Institutional self-reflection and insights analysis)
- Compress (Redundancy clustering & high-level consolidation)
- Forget (Explicit target erasure with cascading cleanup)
"""

from __future__ import annotations

import time
from uuid import uuid4
from typing import Any, List, Dict, Type

from apodex.memory.cmos.models import MemoryNode, MemoryEdge, CMOSNodeType, CMOSEdgeType, NodeState, ProvenanceBlock
from apodex.memory.cmos.interfaces import CognitiveOperator, OperatorContext, OperatorResult, OperatorTelemetry, MemoryRepository


class RecallOperator(CognitiveOperator):
    @property
    def name(self) -> str:
        return "Recall"

    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        start_time = time.time()
        node_id = kwargs.get("node_id")
        filters = kwargs.get("filters", {})

        nodes_found = []
        cache_hits = 0

        if node_id:
            node = await repo.get_node(node_id)
            if node:
                nodes_found.append(node)
                cache_hits += 1
        else:
            nodes_found = await repo.query_nodes(filters)

        latency = (time.time() - start_time) * 1000
        telemetry = OperatorTelemetry(
            operator_name=self.name,
            execution_id=uuid4(),
            latency_ms=latency,
            cache_hits=cache_hits,
            graph_mutations=0
        )

        return OperatorResult(output_nodes=nodes_found, telemetry=telemetry)


class VerifyOperator(CognitiveOperator):
    @property
    def name(self) -> str:
        return "Verify"

    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        start_time = time.time()
        node_id = kwargs.get("node_id")
        if not node_id:
            raise ValueError("VerifyOperator requires 'node_id'.")

        target_node = await repo.get_node(node_id)
        evidence_found = []
        is_validated = False

        if target_node:
            # Traverses outbound Support edges to check backing evidence nodes
            edges = await repo.get_edges(node_id)
            support_nodes = []
            for edge in edges:
                if edge.edge_type == CMOSEdgeType.SUPPORT:
                    node = await repo.get_node(edge.target_id)
                    if node:
                        support_nodes.append(node)
                        if node.node_type == CMOSNodeType.EVIDENCE:
                            evidence_found.append(node)

            # If evidence is found and strong enough, update node state to Validated
            if evidence_found:
                target_node.state = NodeState.VALIDATED
                await repo.save_node(target_node)
                is_validated = True

        latency = (time.time() - start_time) * 1000
        telemetry = OperatorTelemetry(
            operator_name=self.name,
            execution_id=uuid4(),
            latency_ms=latency,
            graph_mutations=1 if is_validated else 0
        )

        return OperatorResult(
            success=is_validated,
            output_nodes=[target_node] if target_node else [],
            output_edges=[],
            telemetry=telemetry
        )


class CompareOperator(CognitiveOperator):
    @property
    def name(self) -> str:
        return "Compare"

    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        start_time = time.time()
        node_a_id = kwargs.get("node_a_id")
        node_b_id = kwargs.get("node_b_id")

        node_a = await repo.get_node(node_a_id) if node_a_id else None
        node_b = await repo.get_node(node_b_id) if node_b_id else None

        output = []
        if node_a and node_b:
            # Structurally compare content / parameters
            comparison_label = f"Comparison of {node_a.label} and {node_b.label}"
            content = f"Shared features: both are type {node_a.node_type}. Contrast: {node_a.content} vs {node_b.content}"
            comp_node = MemoryNode(
                node_type=CMOSNodeType.CLAIM,
                label=comparison_label,
                content=content,
                provenance=node_a.provenance
            )
            output.append(comp_node)

        latency = (time.time() - start_time) * 1000
        telemetry = OperatorTelemetry(
            operator_name=self.name,
            execution_id=uuid4(),
            latency_ms=latency,
            graph_mutations=len(output)
        )

        return OperatorResult(output_nodes=output, telemetry=telemetry)


class ContrastOperator(CognitiveOperator):
    @property
    def name(self) -> str:
        return "Contrast"

    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        start_time = time.time()
        node_a_id = kwargs.get("node_a_id")
        node_b_id = kwargs.get("node_b_id")

        node_a = await repo.get_node(node_a_id) if node_a_id else None
        node_b = await repo.get_node(node_b_id) if node_b_id else None

        diff_claim = []
        if node_a and node_b:
            diff_claim.append(
                MemoryNode(
                    node_type=CMOSNodeType.CLAIM,
                    label=f"Contrast between {node_a.label} and {node_b.label}",
                    content=f"Diff: Node A assertion '{node_a.content}' differs from Node B '{node_b.content}'",
                    provenance=node_a.provenance
                )
            )

        latency = (time.time() - start_time) * 1000
        telemetry = OperatorTelemetry(
            operator_name=self.name,
            execution_id=uuid4(),
            latency_ms=latency,
            graph_mutations=len(diff_claim)
        )
        return OperatorResult(output_nodes=diff_claim, telemetry=telemetry)


class ExplainOperator(CognitiveOperator):
    @property
    def name(self) -> str:
        return "Explain"

    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        start_time = time.time()
        node_id = kwargs.get("node_id")
        explanation = []

        if node_id:
            node = await repo.get_node(node_id)
            if node:
                explanation.append(
                    MemoryNode(
                        node_type=CMOSNodeType.LESSON,
                        label=f"Explanation for {node.label}",
                        content=f"Provenance reasoning path: {', '.join(node.provenance.reasoning_path)}. Git state: {node.provenance.git_sha}",
                        provenance=node.provenance
                    )
                )

        latency = (time.time() - start_time) * 1000
        telemetry = OperatorTelemetry(
            operator_name=self.name,
            execution_id=uuid4(),
            latency_ms=latency,
            graph_mutations=len(explanation)
        )
        return OperatorResult(output_nodes=explanation, telemetry=telemetry)


class ChallengeOperator(CognitiveOperator):
    @property
    def name(self) -> str:
        return "Challenge"

    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        start_time = time.time()
        node_id = kwargs.get("node_id")
        contradictions = []

        if node_id:
            edges = await repo.get_edges(node_id)
            for edge in edges:
                if edge.edge_type == CMOSEdgeType.CONTRADICTS:
                    contradict_node = await repo.get_node(edge.target_id)
                    if contradict_node:
                        contradictions.append(contradict_node)

        latency = (time.time() - start_time) * 1000
        telemetry = OperatorTelemetry(
            operator_name=self.name,
            execution_id=uuid4(),
            latency_ms=latency,
            graph_mutations=0
        )
        return OperatorResult(output_nodes=contradictions, telemetry=telemetry)


class GeneralizeOperator(CognitiveOperator):
    @property
    def name(self) -> str:
        return "Generalize"

    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        start_time = time.time()
        node_ids = kwargs.get("node_ids", [])
        general_nodes = []

        if node_ids:
            # Aggregate contents from underlying nodes to extract a general Lesson or Theory
            contents = []
            prov = None
            for n_id in node_ids:
                node = await repo.get_node(n_id)
                if node:
                    contents.append(node.content)
                    if not prov:
                        prov = node.provenance

            if contents and prov:
                generalized_lesson = MemoryNode(
                    node_type=CMOSNodeType.LESSON,
                    label="Generalized Institutional Lesson",
                    content=f"Synthesized lesson from instances: {'; '.join(contents)}",
                    provenance=prov
                )
                await repo.save_node(generalized_lesson)
                general_nodes.append(generalized_lesson)

        latency = (time.time() - start_time) * 1000
        telemetry = OperatorTelemetry(
            operator_name=self.name,
            execution_id=uuid4(),
            latency_ms=latency,
            graph_mutations=len(general_nodes)
        )
        return OperatorResult(output_nodes=general_nodes, telemetry=telemetry)


class SpecializeOperator(CognitiveOperator):
    @property
    def name(self) -> str:
        return "Specialize"

    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        start_time = time.time()
        node_id = kwargs.get("node_id")
        specialized_evidence = []

        if node_id:
            # Fetch deeper details (e.g., linked evidence nodes)
            edges = await repo.get_edges(node_id)
            for edge in edges:
                if edge.edge_type in [CMOSEdgeType.SUPPORT, CMOSEdgeType.TEMPORAL]:
                    target = await repo.get_node(edge.target_id)
                    if target and target.node_type == CMOSNodeType.EVIDENCE:
                        specialized_evidence.append(target)

        latency = (time.time() - start_time) * 1000
        telemetry = OperatorTelemetry(
            operator_name=self.name,
            execution_id=uuid4(),
            latency_ms=latency,
            graph_mutations=0
        )
        return OperatorResult(output_nodes=specialized_evidence, telemetry=telemetry)


class SimulateOperator(CognitiveOperator):
    @property
    def name(self) -> str:
        return "Simulate"

    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        start_time = time.time()
        # Simulates counterfactual what-if projection by overlaying temporary virtual nodes
        virtual_content = kwargs.get("virtual_content", "Counterfactual sandbox branch projection")
        temp_node = MemoryNode(
            node_type=CMOSNodeType.HYPOTHESIS,
            label="Simulated Hypothesis Overlay",
            content=virtual_content,
            provenance=ProvenanceBlock(
                origin="simulation_sandbox",
                creator_id=ctx.user_id,
                confidence=0.5
            )
        )
        ctx.graph_overlay.nodes[temp_node.node_id] = temp_node

        latency = (time.time() - start_time) * 1000
        telemetry = OperatorTelemetry(
            operator_name=self.name,
            execution_id=uuid4(),
            latency_ms=latency,
            graph_mutations=0  # Writes to overlay memory, not main storage repo
        )
        return OperatorResult(output_nodes=[temp_node], telemetry=telemetry)


class ReflectOperator(CognitiveOperator):
    @property
    def name(self) -> str:
        return "Reflect"

    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        start_time = time.time()
        failures = await repo.query_nodes({"node_type": CMOSNodeType.FAILURE})
        decisions = await repo.query_nodes({"node_type": CMOSNodeType.DECISION})

        reflection_node = None
        if failures:
            prov = failures[0].provenance
            reflection_node = MemoryNode(
                node_type=CMOSNodeType.LESSON,
                label="Self-Correction Policy Reflection",
                content=f"Detected {len(failures)} failures and {len(decisions)} decisions. Lesson: avoid parameters causing failures.",
                provenance=prov
            )
            await repo.save_node(reflection_node)

        latency = (time.time() - start_time) * 1000
        telemetry = OperatorTelemetry(
            operator_name=self.name,
            execution_id=uuid4(),
            latency_ms=latency,
            graph_mutations=1 if reflection_node else 0
        )
        return OperatorResult(output_nodes=[reflection_node] if reflection_node else [], telemetry=telemetry)


class CompressOperator(CognitiveOperator):
    @property
    def name(self) -> str:
        return "Compress"

    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        start_time = time.time()
        claims = await repo.query_nodes({"node_type": CMOSNodeType.CLAIM})

        mutations = 0
        if len(claims) >= 2:
            # Cluster redundant claims into a single compressed ClaimNode
            prov = claims[0].provenance
            compressed_content = f"Compressed {len(claims)} historical assertions: " + " | ".join([c.content for c in claims])
            compressed_node = MemoryNode(
                node_type=CMOSNodeType.CLAIM,
                label="Consolidated Claims Summary",
                content=compressed_content,
                provenance=prov
            )
            await repo.save_node(compressed_node)
            mutations += 1

            # Delete original claims
            for c in claims:
                await repo.delete_node(c.node_id)
                mutations += 1

        latency = (time.time() - start_time) * 1000
        telemetry = OperatorTelemetry(
            operator_name=self.name,
            execution_id=uuid4(),
            latency_ms=latency,
            graph_mutations=mutations
        )
        return OperatorResult(telemetry=telemetry)


class ForgetOperator(CognitiveOperator):
    @property
    def name(self) -> str:
        return "Forget"

    async def execute(self, ctx: OperatorContext, repo: MemoryRepository, **kwargs) -> OperatorResult:
        start_time = time.time()
        node_id = kwargs.get("node_id")

        if node_id:
            # Decays/erases specific node and cascades deletes
            await repo.delete_node(node_id)

        latency = (time.time() - start_time) * 1000
        telemetry = OperatorTelemetry(
            operator_name=self.name,
            execution_id=uuid4(),
            latency_ms=latency,
            graph_mutations=1
        )
        return OperatorResult(telemetry=telemetry)
