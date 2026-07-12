"""
WMC Architectural and Functional Conformance Test Suite
Validates configuration, domain models, dependency injection, events, governance, and structural isolation.
"""

from __future__ import annotations

import ast
import os
from datetime import datetime
from uuid import UUID, uuid4
import pytest
from pydantic import ValidationError

# WMC Core imports
from apodex.world_model.config import WorldModelCreatorConfig, RealityEngineConfig
from apodex.world_model.domain.entities import Entity
from apodex.world_model.domain.relationships import Relationship
from apodex.world_model.domain.beliefs import Belief
from apodex.world_model.domain.hypotheses import Hypothesis
from apodex.world_model.domain.timelines import Timeline, WorldGraphDelta
from apodex.world_model.domain.environments import EnvironmentVector
from apodex.world_model.domain.cognition import CognitiveProfile, AudienceCohort
from apodex.world_model.domain.economics import UnitEconomics, PriceElasticityCurve
from apodex.world_model.domain.simulation import SimulationRunContext
from apodex.world_model.dependency_injection import DependencyContainer
from apodex.world_model.registry import PluginRegistry
from apodex.world_model.factory import DomainModelFactory
from apodex.world_model.graph.world_graph import WorldGraphManager
from apodex.world_model.graph.traversal import GraphTraversalService
from apodex.world_model.graph.reasoning import GraphReasoningEngine
from apodex.world_model.graph.indexing import GraphIndexingService
from apodex.world_model.interfaces.engines import IWorldSimulationEngine
from apodex.world_model.orchestration.coordinator import WmcOrchestrationCoordinator
from apodex.world_model.governance.policy import PolicyRule, PolicyEnforcementFrame
from apodex.world_model.governance.approval import ApprovalRequest
from apodex.world_model.governance.audit import ImmutableAuditLedger
from apodex.world_model.governance.compliance import ComplianceAuditor
from apodex.world_model.events.schemas import (
    RealityStateUpdatedEvent,
    SimulationStepCompletedEvent,
    PolicyViolationDetectedEvent
)


# =====================================================================
# 1. Configuration Validation Tests
# =====================================================================

def test_config_validation():
    """Verify that WorldModelCreatorConfig validates correct and incorrect parameter structures."""
    # Valid config
    config = WorldModelCreatorConfig(
        tenant_id="tenant_123",
        active_environment="production",
        max_budget_limit_usd=150.0
    )
    assert config.tenant_id == "tenant_123"
    assert config.active_environment == "production"
    assert config.max_budget_limit_usd == 150.0
    assert config.reality_engine.execution_tier == "CHEAP"

    # Invalid config (missing required field)
    with pytest.raises(ValidationError):
        WorldModelCreatorConfig()  # type: ignore


# =====================================================================
# 2. Domain Validation & Logic Tests
# =====================================================================

def test_entity_updates():
    """Verify Entity metadata properties update and track alteration timestamps."""
    entity = Entity(name="Enterprise Co", entity_type="ORGANIZATION")
    assert entity.name == "Enterprise Co"
    original_updated_at = entity.updated_at

    # Update properties
    entity.update_property("market_cap_billions", 1.2)
    assert entity.properties["market_cap_billions"] == 1.2
    assert entity.updated_at >= original_updated_at


def test_recursive_bayesian_belief():
    """Verify that Belief model computes recursive updates according to Bayes rule."""
    belief = Belief(target_id=uuid4(), probability=0.6)
    assert belief.probability == 0.6

    # Update confidence given likelihood
    # P(B|E) = (P(E|B) * P(B)) / P(E)
    # where P(E) = P(E|B)P(B) + P(E|~B)P(~B) with default P(E|~B) = 0.5
    # P(E|B) = 0.8, P(B) = 0.6
    # P(E) = 0.8 * 0.6 + 0.5 * 0.4 = 0.48 + 0.20 = 0.68
    # P(B|E) = 0.48 / 0.68 = 0.70588...
    belief.update_confidence(likelihood=0.8, prior_probability=0.6)
    assert pytest.approx(belief.probability, rel=1e-4) == 0.70588


def test_timeline_immutability():
    """Verify that committed timelines are read-only and prevent structural deltas."""
    timeline = Timeline(name="sim_pessimistic")
    assert not timeline.is_committed

    delta = WorldGraphDelta(delta_type="ADD_ENTITY", target_id=uuid4(), payload={"name": "New Node"})
    timeline.add_delta(delta)
    assert len(timeline.deltas) == 1

    # Commit the timeline
    timeline.commit()
    assert timeline.is_committed

    # Attempting to add delta should now raise ValueError
    with pytest.raises(ValueError, match="Cannot append delta to a committed read-only timeline."):
        timeline.add_delta(delta)


# =====================================================================
# 3. Dependency Injection Tests
# =====================================================================

def test_di_container_and_registry():
    """Verify DI registration, type checks, resolving, and custom plugin registering."""
    container = DependencyContainer()

    # Mocking service interface
    class IMockEngine:
        pass

    class MockEngineImpl(IMockEngine):
        pass

    # Registering
    instance = MockEngineImpl()
    container.register_singleton(IMockEngine, instance)

    # Resolving
    resolved = container.resolve(IMockEngine)
    assert resolved is instance

    # Registering invalid type should fail
    with pytest.raises(TypeError):
        container.register_singleton(IMockEngine, "not_an_instance")  # type: ignore


# =====================================================================
# 4. Event Serialization Tests
# =====================================================================

def test_event_serialization():
    """Verify that domain events serialize to JSON and deserialize back cleanly."""
    event = RealityStateUpdatedEvent(
        update_id=uuid4(),
        affected_entity_ids=[uuid4(), uuid4()],
        new_relationships_asserted=[]
    )

    # Serialize to JSON
    json_data = event.json()
    assert "update_id" in json_data
    assert "affected_entity_ids" in json_data

    # Parse back
    parsed_event = RealityStateUpdatedEvent.parse_raw(json_data)
    assert parsed_event.update_id == event.update_id
    assert parsed_event.affected_entity_ids == event.affected_entity_ids
    assert parsed_event.version == "1.0.0"


# =====================================================================
# 5. Governance & Compliance Tests
# =====================================================================

@pytest.mark.asyncio
async def test_compliance_and_approval():
    """Verify policy auditing detects violations and manages human signature sign-offs."""
    # Configure rule frame
    rule_ethics = PolicyRule(rule_id="RULE_ETH_01", category="ETHICS", description="No deception in campaigns.")
    rule_brand = PolicyRule(rule_id="RULE_BRAND_01", category="BRAND", description="No competitor slandering.")
    frame = PolicyEnforcementFrame(tenant_id="tenant_1", rules=[rule_ethics, rule_brand])

    auditor = ComplianceAuditor(frame=frame)

    # Compliant prompt
    violations_clean = await auditor.audit_concept("A warm brand story highlighting customer satisfaction.", {})
    assert len(violations_clean) == 0

    # Violating prompt
    violations_dirty = await auditor.audit_concept("Deceive target audience regarding pricing terms and do competitor_slander.", {})
    assert len(violations_dirty) == 2
    assert "Violation of RULE_ETH_01" in violations_dirty[0]
    assert "Violation of RULE_BRAND_01" in violations_dirty[1]

    # Approval Request Workflow
    req = ApprovalRequest(tenant_id="tenant_1", stage=2, payload_type="CONCEPT", reason="Ethics violation")
    assert req.status == "PENDING"

    # Perform signature approval
    req.approve(reviewer_id="human_curator_1", signature="SIG_SHA256_CRYPT_SIGNATURE_0x1F")
    assert req.status == "APPROVED"
    assert req.reviewer_id == "human_curator_1"
    assert req.cryptographic_signature == "SIG_SHA256_CRYPT_SIGNATURE_0x1F"


# =====================================================================
# 6. Cryptographically Chained Audit Ledger Tests
# =====================================================================

def test_audit_ledger_chaining():
    """Verify that ImmutableAuditLedger cryptographically chains records using SHA-256 hashes."""
    ledger = ImmutableAuditLedger()

    # Append first block
    block_1 = ledger.append_record(actor_id="wmc_reality", action="INGEST_RSS", payload={"url": "http://fe.ed"})
    assert block_1.previous_block_hash == "0" * 64
    assert len(ledger.chain) == 1

    # Append second block
    block_2 = ledger.append_record(actor_id="wmc_gov", action="SIGN_APPROVAL", payload={"req_id": "req_123"})
    assert block_2.previous_block_hash == block_1.current_block_hash
    assert len(ledger.chain) == 2


# =====================================================================
# 7. Orchestration & Coordinator Tests
# =====================================================================

@pytest.mark.asyncio
async def test_orchestration_coordinator():
    """Verify that WmcOrchestrationCoordinator successfully triggers engine simulations and processes results."""
    container = DependencyContainer()

    # Stub/Mock implementation of Simulation Engine
    class DummySimulationEngine(IWorldSimulationEngine):
        async def create_branch(self, parent_timeline_id: UUID, name: str, branch_time: datetime) -> Timeline:
            return Timeline(timeline_id=uuid4(), parent_timeline_id=parent_timeline_id, name=name)

        async def step_simulation(self, context: SimulationRunContext) -> List[WorldGraphDelta]:
            return [
                WorldGraphDelta(delta_type="ADD_ENTITY", target_id=uuid4(), payload={"name": "Simulated Node"})
            ]

    container.register_singleton(IWorldSimulationEngine, DummySimulationEngine())

    coordinator = WmcOrchestrationCoordinator(container=container)
    parent_id = uuid4()

    # Run the coordinator pipeline
    timeline = await coordinator.run_scenario_simulation(
        parent_timeline_id=parent_id,
        scenario_name="market_surge_2027",
        hours_to_simulate=48.0
    )

    assert timeline.name == "market_surge_2027"
    assert timeline.parent_timeline_id == parent_id
    assert len(timeline.deltas) == 1
    assert timeline.deltas[0].delta_type == "ADD_ENTITY"


# =====================================================================
# 9. Self-Improvement Flywheel Tests
# =====================================================================

from apodex.world_model.domain.self_improvement import (
    EngineeringFinding,
    BenchmarkReport,
    SelfImprovementProposal
)
from apodex.world_model.interfaces.self_improvement import (
    IChiefArchitect,
    ISecurityEngineer,
    IPerformanceEngineer,
    ISoftwareEngineer,
    IResearchScientist,
    IQaEngineer,
    IEvaluator
)
from apodex.world_model.orchestration.self_improvement_coordinator import SelfImprovementFlywheelCoordinator


@pytest.mark.asyncio
async def test_self_improvement_flywheel_cycle():
    """Verify that SelfImprovementFlywheelCoordinator runs a complete multi-agent engineering optimization cycle."""
    container = DependencyContainer()

    # Register mock specialized agents to handle the self-improvement tasks
    class MockArchitect(IChiefArchitect):
        async def evaluate_architecture(self) -> List[EngineeringFinding]:
            return [
                EngineeringFinding(
                    severity="HIGH",
                    category="CIRCULAR_DEPENDENCY",
                    file_path="apodex/world_model/domain/timelines.py",
                    description="Circular dependency detected between timelines and environments",
                    suggested_fix="Refactor environments to separate file and use interfaces"
                )
            ]

    class MockSecurity(ISecurityEngineer):
        async def audit_security(self) -> List[EngineeringFinding]:
            # Returns a lower severity issue
            return [
                EngineeringFinding(
                    severity="MEDIUM",
                    category="SECURITY_VULNERABILITY",
                    file_path="apodex/world_model/config.py",
                    description="API Key defaults are stored as strings",
                    suggested_fix="Load keys from OS environment variable"
                )
            ]

    class MockPerformance(IPerformanceEngineer):
        async def profile_performance(self) -> List[EngineeringFinding]:
            return []

    class MockSWE(ISoftwareEngineer):
        async def generate_patch(self, finding: EngineeringFinding) -> SelfImprovementProposal:
            return SelfImprovementProposal(
                title="Fix domain circular dependencies",
                summary=f"Addressed issue: {finding.description}",
                proposed_diff="--- timeline.py\n+++ timeline.py\n...",
                risks_analysis="Low risk, backwards compatible",
                rollback_instructions="Revert git commit",
                associated_finding_id=finding.finding_id
            )

    class MockResearch(IResearchScientist):
        async def research_topic(self, topic: str) -> List[str]:
            return ["Friston, K. (2010). 'The free-energy principle: a unified brain theory?' Nature Reviews Neuroscience."]

    class MockQA(IQaEngineer):
        async def generate_tests(self, proposal: SelfImprovementProposal) -> str:
            return "def test_timeline_isolated_imports():\n    assert True"

    class MockEvaluator(IEvaluator):
        async def benchmark_proposal(self, proposal: SelfImprovementProposal) -> BenchmarkReport:
            return BenchmarkReport(
                latency_delta_ms=-15.4,  # Performance improvement
                token_cost_delta_usd=-0.002,  # Cost savings
                is_regression=False
            )

    # Register singletons in container
    container.register_singleton(IChiefArchitect, MockArchitect())
    container.register_singleton(ISecurityEngineer, MockSecurity())
    container.register_singleton(IPerformanceEngineer, MockPerformance())
    container.register_singleton(ISoftwareEngineer, MockSWE())
    container.register_singleton(IResearchScientist, MockResearch())
    container.register_singleton(IQaEngineer, MockQA())
    container.register_singleton(IEvaluator, MockEvaluator())

    # Initialize and execute Flywheel Coordinator
    coordinator = SelfImprovementFlywheelCoordinator(container=container)
    proposals = await coordinator.execute_optimization_cycle()

    # Validate output
    assert len(proposals) == 1
    proposal = proposals[0]
    assert proposal.title == "Fix domain circular dependencies"
    assert "Friston, K. (2010)" in proposal.research_citations[0]
    assert "def test_timeline_isolated_imports" in proposal.summary
    assert proposal.status == "EVALUATED"
    assert proposal.benchmark_report is not None
    assert proposal.benchmark_report.latency_delta_ms == -15.4
    assert not proposal.benchmark_report.is_regression


# =====================================================================
# 8. Architectural Conformance Tests (Structural Boundary Checks)
# =====================================================================

def test_architectural_conformance_isolation():
    """
    Enforces architectural boundary checks:
    - The domain layer (apodex/world_model/domain/) MUST NEVER import from:
      - orchestration
      - governance
      - graph
      - interfaces
      - external databases (neo4j, sqlite3, pg, etc.)
    """
    domain_dir = "apodex/world_model/domain/"
    assert os.path.exists(domain_dir), "Domain package directory does not exist!"

    forbidden_imports = {
        "orchestration",
        "governance",
        "graph",
        "interfaces",
        "neo4j",
        "sqlite3",
        "psycopg2",
        "sqlalchemy",
        "sqlmodel"
    }

    # Analyze Python AST of every file under domain/
    for root, _, files in os.walk(domain_dir):
        for file in files:
            if not file.endswith(".py"):
                continue

            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=filepath)

            for node in ast.walk(tree):
                # 1. Check direct imports (e.g., import graph)
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_module = alias.name.split(".")[0]
                        assert imported_module not in forbidden_imports, (
                            f"Architectural Violation: '{filepath}' imports forbidden module '{alias.name}'!"
                        )

                # 2. Check from-imports (e.g., from graph import WorldGraph)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imported_module = node.module.split(".")[0]
                        # If importing from apodex.world_model.*
                        if "apodex" in node.module and "world_model" in node.module:
                            parts = node.module.split(".")
                            # e.g., parts = ['apodex', 'world_model', 'graph']
                            if len(parts) > 2:
                                imported_module = parts[2]

                        assert imported_module not in forbidden_imports, (
                            f"Architectural Violation: '{filepath}' from-imports forbidden module '{node.module}'!"
                        )
