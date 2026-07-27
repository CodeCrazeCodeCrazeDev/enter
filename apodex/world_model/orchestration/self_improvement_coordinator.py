from __future__ import annotations
from datetime import datetime
import copy
import hashlib
import logging
import re
from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4

from apodex.world_model.dependency_injection import DependencyContainer
from apodex.world_model.config import WorldModelCreatorConfig
from apodex.world_model.domain.self_improvement import (
    EngineeringFinding,
    SelfImprovementProposal,
    BenchmarkReport
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
# Upgraded additions
from apodex.world_model.world_model import WorldModel
from apodex.world_model.graph.searcheyes_models import PerceptionKnowledgeChain, PKCHop
from apodex.skills.registry import skill_registry
from apodex.skills.implementations import (
    RunFastSecurityScanInput,
    FindRelatedFilesAndTestsInput,
    GenerateCodePatchInput,
    RunTestSuiteInput,
    SummarizeBenchmarkResultsInput
)
from apodex.harness.schemas.protocol_spec import ProtocolSpec, StepSpec
from apodex.protocols.loader import ProtocolLoader

logger = logging.getLogger("apodex.world_model.self_improvement")

COST_WEIGHTS = {
    "expensive_agent_call": {"tokens": 4000, "usd": 0.06, "latency_ms": 1200.0},
    "standard_call": {"tokens": 1500, "usd": 0.015, "latency_ms": 400.0},
    "lightweight_rules_call": {"tokens": 50, "usd": 0.0005, "latency_ms": 10.0},
    "skipped_or_cached": {"tokens": 0, "usd": 0.0, "latency_ms": 0.0},
}


class SelfImprovementFlywheelCoordinator:
    """Orchestrates the multi-agent self-improving engineering organization with layered cost optimization."""

    # Static in-memory cache to persist entries across instances/sessions
    _global_cache: Dict[str, SelfImprovementProposal] = {}

    def __init__(self, container: DependencyContainer) -> None:
        self.container = container

        # Resolve configuration gracefully with robust fallback
        try:
            self.config = self.container.resolve(WorldModelCreatorConfig)
            tier_from_config = "CHEAP"
            if hasattr(self.config, "reality_engine") and hasattr(self.config.reality_engine, "execution_tier"):
                tier_from_config = self.config.reality_engine.execution_tier
            self.current_tier = tier_from_config
        except Exception:
            # Fallback to EXPENSIVE for backward compatibility in legacy tests
            logger.warning(
                "Failed to resolve WorldModelCreatorConfig from container; "
                "falling back to default config and EXPENSIVE tier.",
                exc_info=True,
            )
            self.config = WorldModelCreatorConfig(tenant_id="default_tenant")
            self.config.reality_engine.execution_tier = "EXPENSIVE"
            self.current_tier = "EXPENSIVE"

        self.tenant_id = self.config.tenant_id if hasattr(self.config, "tenant_id") else "default_tenant"

        # Initialize tracking state
        self.cumulative_cost_usd = 0.0
        self.cumulative_tokens = 0
        self.cumulative_latency_ms = 0.0
        self.execution_log: List[Dict[str, Any]] = []

        # Part 1 Integration: Graph model trace log
        self.world_model = WorldModel()

    @classmethod
    def flush_cache(cls) -> None:
        """Flushes the static in-memory proposal cache."""
        cls._global_cache.clear()

    def _generate_cache_key(self, finding: EngineeringFinding, tenant_id: str, tier: str) -> str:
        """Generates a rich, robust, isolated cache key preventing cross-tenant and CHEAP->EXPENSIVE pollution."""
        content_str = f"{finding.category}:{finding.file_path}:{finding.line_number or ''}:{finding.description}"
        fingerprint = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
        return f"{tenant_id}:{tier}:{finding.category}:{fingerprint}"

    def _charge_operation(self, op_type: str, details: str = "") -> bool:
        """
        Record and charge the simulated cost.
        Returns False if the hard budget ceiling is reached (blocking further charges).
        """
        weight = COST_WEIGHTS.get(op_type, COST_WEIGHTS["skipped_or_cached"])
        cost_usd = weight["usd"]
        tokens = weight["tokens"]
        latency = weight["latency_ms"]

        max_budget = getattr(self.config, "max_budget_limit_usd", 100.0)

        # 1. Hard ceiling check
        if self.cumulative_cost_usd + cost_usd > max_budget:
            # Emit structured budget_halt log
            print(f"[EVENT: budget_halt] Cumulative cost {self.cumulative_cost_usd + cost_usd:.4f}$ exceeds budget limit {max_budget}$. Halting.")
            self.execution_log.append({
                "event": "budget_halt",
                "cumulative_cost_usd": self.cumulative_cost_usd,
                "offending_cost_usd": cost_usd,
                "timestamp": datetime.utcnow().isoformat(),
                "details": details
            })
            return False

        self.cumulative_cost_usd += cost_usd
        self.cumulative_tokens += tokens
        self.cumulative_latency_ms += latency

        # 2. Dynamic downshift check (< 30% remaining budget)
        remaining_budget = max_budget - self.cumulative_cost_usd
        if remaining_budget < 0.3 * max_budget and self.current_tier != "CHEAP":
            old_tier = self.current_tier
            self.current_tier = "CHEAP"
            print(f"[EVENT: budget_downshift] Remaining budget {remaining_budget:.4f}$ is less than 30% of limit {max_budget}$. Downshifting {old_tier} -> CHEAP.")
            self.execution_log.append({
                "event": "budget_downshift",
                "old_tier": old_tier,
                "new_tier": "CHEAP",
                "cumulative_cost_usd": self.cumulative_cost_usd,
                "timestamp": datetime.utcnow().isoformat(),
                "details": details
            })

        return True

    async def _run_fast_security_scan(self) -> List[EngineeringFinding]:
        """Fast regex based security scan utilizing run_fast_security_scan skill."""
        skill = skill_registry.get("run_fast_security_scan")
        if not skill:
            return []
        output = await skill.execute(RunFastSecurityScanInput(), {"container": self.container})
        return output.findings

    async def execute_optimization_cycle(self) -> List[SelfImprovementProposal]:
        """
        Runs a complete self-improvement optimization cycle wrapped under a protocol.
        """
        # Load declarative protocol spec
        import os
        schema_path = "apodex/harness/schemas/code_improvement_protocol.yaml"
        if os.path.exists(schema_path):
            with open(schema_path, "r", encoding="utf-8") as f:
                yaml_str = f.read()
            protocol = ProtocolLoader.load_from_yaml(yaml_str)
        else:
            # Sane default configuration spec if file doesn't exist
            protocol = ProtocolSpec(
                protocol_id="code_improvement_protocol",
                name="Fallback Protocol",
                k_steps=5,
                downshift_after_steps_without_progress=3,
                halt_after_steps_without_progress=5,
                steps=[
                    StepSpec(step_id="security_scan", skill_name="run_fast_security_scan", anchors_to_hit=["ANCHOR_RAN_SECURITY_SCAN"]),
                    StepSpec(step_id="triage", skill_name="find_related_files_and_tests", anchors_to_hit=["ANCHOR_FOUND_RELEVANT_FILES"]),
                    StepSpec(step_id="patch", skill_name="generate_code_patch", anchors_to_hit=["ANCHOR_GENERATED_PATCH"]),
                    StepSpec(step_id="qa_test", skill_name="run_test_suite", anchors_to_hit=["ANCHOR_RAN_TESTS"]),
                    StepSpec(step_id="benchmark", skill_name="summarize_benchmark_results", anchors_to_hit=["ANCHOR_EVALUATED_PATCH"])
                ]
            )

        proposals: List[SelfImprovementProposal] = []
        findings: List[EngineeringFinding] = []

        # Track the active PKC trace
        trace = PerceptionKnowledgeChain()
        self.world_model.register_pkc_trace(trace)

        # -------------------------------------------------------------
        # Protocol-Driven Multi-Step Execution Loop
        # -------------------------------------------------------------
        # Configurable anchors progress tracking
        k_limit = protocol.k_steps
        downshift_limit = protocol.downshift_after_steps_without_progress
        halt_limit = protocol.halt_after_steps_without_progress
        min_progress = protocol.progress_rate_threshold

        steps_executed = 0
        total_anchors_hit_set = set()
        steps_since_last_new_anchor = 0

        # Pre-cache or gather potential findings
        # ARCHITECT: Skipped entirely in CHEAP tier
        if self.current_tier != "CHEAP":
            try:
                architect = self.container.resolve(IChiefArchitect)
                if self._charge_operation("expensive_agent_call", "IChiefArchitect evaluate_architecture"):
                    findings.extend(await architect.evaluate_architecture())
                    total_anchors_hit_set.add("ANCHOR_FOUND_RELEVANT_FILES")
            except Exception:
                logger.exception("IChiefArchitect.evaluate_architecture failed.")

        # SECURITY finding gather
        if self.current_tier == "CHEAP":
            if self._charge_operation("lightweight_rules_call", "Lightweight regex-based security audit"):
                findings.extend(await self._run_fast_security_scan())
                total_anchors_hit_set.add("ANCHOR_RAN_SECURITY_SCAN")
        else:
            try:
                security_eng = self.container.resolve(ISecurityEngineer)
                if self._charge_operation("expensive_agent_call", "ISecurityEngineer audit_security"):
                    findings.extend(await security_eng.audit_security())
                    total_anchors_hit_set.add("ANCHOR_RAN_SECURITY_SCAN")
            except Exception:
                logger.exception("ISecurityEngineer.audit_security failed.")

        # PERFORMANCE: Profile performance under all tiers
        try:
            performance_eng = self.container.resolve(IPerformanceEngineer)
            cost_type = "lightweight_rules_call" if self.current_tier == "CHEAP" else "standard_call"
            if self._charge_operation(cost_type, "IPerformanceEngineer profile_performance"):
                findings.extend(await performance_eng.profile_performance())
        except Exception:
            logger.exception("IPerformanceEngineer.profile_performance failed.")

        if not findings:
            # Log clear status/error before returning
            self.execution_log.append({
                "status": "APPROVED",
                "message": "No findings found during audit.",
                "timestamp": datetime.utcnow().isoformat()
            })
            return proposals

        # Priority Sort
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        findings.sort(key=lambda f: severity_order.get(f.severity, 4))
        target_finding = findings[0]

        # -------------------------------------------------------------
        # Isolated Caching Refactor
        # -------------------------------------------------------------
        cache_key = self._generate_cache_key(target_finding, self.tenant_id, self.current_tier)
        if cache_key in self._global_cache:
            if self._charge_operation("skipped_or_cached", f"Isolated Cache Hit for key {cache_key}"):
                # Ensure deep copies to callers to avoid shared mutable objects
                cached_proposal = copy.deepcopy(self._global_cache[cache_key])
                # We do NOT mutate cached entry status upon cache hit
                proposals.append(cached_proposal)
                self.execution_log.append({
                    "status": "CACHE_HIT",
                    "proposal_id": str(cached_proposal.proposal_id),
                    "timestamp": datetime.utcnow().isoformat()
                })
            return proposals

        # Execute protocol steps mapping to skills
        proposal: Optional[SelfImprovementProposal] = None

        for step in protocol.steps:
            skill = skill_registry.get(step.skill_name)
            if not skill:
                # Log INFRA_ERROR precisely
                self.execution_log.append({
                    "status": "INFRA_ERROR",
                    "error": f"Missing required skill: {step.skill_name}",
                    "timestamp": datetime.utcnow().isoformat()
                })
                return proposals

            steps_executed += 1

            # Progress tracking (Part 4 Credit / Downshift logic)
            new_anchors_hit = [a for a in step.anchors_to_hit if a not in total_anchors_hit_set]
            if new_anchors_hit:
                total_anchors_hit_set.update(new_anchors_hit)
                steps_since_last_new_anchor = 0
            else:
                steps_since_last_new_anchor += 1

            # Determine downshift or halt conditions based on progress-to-cost anchors
            if steps_since_last_new_anchor >= downshift_limit and self.current_tier == "EXPENSIVE":
                old_tier = self.current_tier
                self.current_tier = "CHEAP"
                self.execution_log.append({
                    "event": "anchor_progress_downshift",
                    "old_tier": old_tier,
                    "new_tier": "CHEAP",
                    "steps_without_progress": steps_since_last_new_anchor,
                    "timestamp": datetime.utcnow().isoformat()
                })

            if steps_since_last_new_anchor >= halt_limit:
                print(f"[EVENT: budget_halt] Anchor progress halted for {steps_since_last_new_anchor} steps. Triggering budget_halt.")
                self.execution_log.append({
                    "event": "budget_halt",
                    "status": "BUDGET_HALTED",
                    "reason": "Halted due to lack of anchor progress",
                    "timestamp": datetime.utcnow().isoformat()
                })
                return proposals

            # Record PKC trace hop (SearchEyes framework)
            hop = PKCHop(
                step_index=steps_executed,
                node_id=f"step:{step.step_id}",
                node_type="protocol_step",
                anchors_hit=step.anchors_to_hit,
                cost_usd=0.01 if self.current_tier != "CHEAP" else 0.001,
                timestamp=datetime.utcnow().isoformat()
            )
            trace.add_hop(hop)

            # Execution logic mapping
            if step.skill_name == "run_fast_security_scan":
                # Already executed finding gathering above; skip or perform lightweight check
                self._charge_operation("lightweight_rules_call", "Skill run_fast_security_scan")

            elif step.skill_name == "find_related_files_and_tests":
                charge_type = "lightweight_rules_call" if self.current_tier == "CHEAP" else "standard_call"
                if not self._charge_operation(charge_type, "Skill find_related_files_and_tests"):
                    return proposals
                # Execute skill
                await skill.execute(
                    FindRelatedFilesAndTestsInput(category=target_finding.category, file_path=target_finding.file_path),
                    {"container": self.container}
                )

            elif step.skill_name == "generate_code_patch":
                charge_type = "standard_call" if self.current_tier == "CHEAP" else "expensive_agent_call"
                if not self._charge_operation(charge_type, "Skill generate_code_patch"):
                    return proposals
                out = await skill.execute(
                    GenerateCodePatchInput(finding=target_finding),
                    {"container": self.container}
                )
                proposal = out.proposal

                # IResearchScientist sub-call: Generate academic citations (Skipped in CHEAP tier)
                if self.current_tier != "CHEAP":
                    try:
                        researcher = self.container.resolve(IResearchScientist)
                        if self._charge_operation("standard_call", "IResearchScientist research_topic"):
                            citations = await researcher.research_topic(f"optimization of {target_finding.category}")
                            proposal.research_citations.extend(citations)
                    except Exception:
                        logger.exception("IResearchScientist.research_topic failed; continuing.")
                else:
                    self._charge_operation("skipped_or_cached", "Skipped research scientist in CHEAP tier")

            elif step.skill_name == "run_test_suite":
                if not proposal:
                    continue
                # Skipped in CHEAP tier
                if self.current_tier != "CHEAP":
                    if self._charge_operation("standard_call", "Skill run_test_suite"):
                        out = await skill.execute(
                            RunTestSuiteInput(proposal=proposal),
                            {"container": self.container}
                        )
                        proposal.summary += f"\n[QA Test Generated]\n{out.test_code}"
                else:
                    self._charge_operation("skipped_or_cached", "Skipped QA test generation in CHEAP tier")

            elif step.skill_name == "summarize_benchmark_results":
                if not proposal:
                    continue
                charge_type = "lightweight_rules_call" if self.current_tier == "CHEAP" else "standard_call"
                if not self._charge_operation(charge_type, "Skill summarize_benchmark_results"):
                    return proposals

                try:
                    out = await skill.execute(
                        SummarizeBenchmarkResultsInput(proposal=proposal),
                        {"container": self.container}
                    )
                    report = out.report
                    proposal.benchmark_report = report

                    if not report.is_regression:
                        proposal.status = "EVALUATED"
                        # Cache isolated deep copy of proposal
                        self._global_cache[cache_key] = copy.deepcopy(proposal)
                    else:
                        proposal.status = "REJECTED"
                except Exception:
                    # Log EVALUATOR_ERROR precisely
                    self.execution_log.append({
                        "status": "EVALUATOR_ERROR",
                        "error": "Failed during benchmark execution",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                    proposal.status = "REJECTED"

        if proposal:
            proposals.append(proposal)

        return proposals
