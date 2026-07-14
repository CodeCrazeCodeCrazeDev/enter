from __future__ import annotations
from datetime import datetime
import hashlib
import logging
import re
from typing import List, Dict, Any, Optional
from uuid import UUID

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

logger = logging.getLogger("apodex.world_model.self_improvement")

# Production-grade cost weight configuration (not hard-coded magic numbers)
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

        # Initialize tracking state
        self.cumulative_cost_usd = 0.0
        self.cumulative_tokens = 0
        self.cumulative_latency_ms = 0.0
        self.execution_log: List[Dict[str, Any]] = []

    @classmethod
    def flush_cache(cls) -> None:
        """Flushes the static in-memory proposal cache."""
        cls._global_cache.clear()

    def _generate_cache_key(self, finding: EngineeringFinding) -> str:
        """Generates a rich, robust cache key from category and fingerprint of finding content."""
        content_str = f"{finding.category}:{finding.file_path}:{finding.line_number or ''}:{finding.description}"
        fingerprint = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
        return f"{finding.category}:{fingerprint}"

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

    def _run_fast_security_scan(self) -> List[EngineeringFinding]:
        """A fast, non-LLM, regex-based security audit of the codebase."""
        findings = []
        files_to_scan = [
            "apodex/world_model/config.py",
            "apodex/world_model/orchestration/coordinator.py"
        ]

        patterns = {
            "eval_usage": (r"\beval\s*\(", "Potential unsafe eval() call found in codebase."),
            "exec_usage": (r"\bexec\s*\(", "Potential unsafe exec() call found in codebase."),
            "api_key_leak": (r"(api_key|password|secret|token)\s*=\s*['\"][a-zA-Z0-9_\-]+['\"]", "Potential hardcoded credentials found in codebase."),
        }

        for path in files_to_scan:
            try:
                import os
                if not os.path.exists(path):
                    continue
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                for key, (pattern, msg) in patterns.items():
                    if re.search(pattern, content):
                        findings.append(EngineeringFinding(
                            severity="HIGH",
                            category="SECURITY_VULNERABILITY",
                            file_path=path,
                            description=msg,
                            suggested_fix="Load configuration dynamically and avoid static/unsafe executions."
                        ))
            except OSError:
                logger.warning("Fast security scan could not read '%s'; skipping.", path, exc_info=True)
        return findings

    async def execute_optimization_cycle(self) -> List[SelfImprovementProposal]:
        """
        Runs a complete self-improvement optimization cycle:
        1. Gathers architectural, security, and performance findings (cost-optimized).
        2. Selects the highest priority finding.
        3. Generates a targeted fix/patch proposal with academic research citations.
        4. Drafts QA test coverage.
        5. Benchmarks the proposed solution, verifying it is positive-yield.
        """
        proposals: List[SelfImprovementProposal] = []

        # 1. Gather audit findings from specialized agents with Tier Gating
        findings: List[EngineeringFinding] = []

        # ARCHITECT: Skipped entirely in CHEAP tier
        if self.current_tier != "CHEAP":
            try:
                architect = self.container.resolve(IChiefArchitect)
                if self._charge_operation("expensive_agent_call", "IChiefArchitect evaluate_architecture"):
                    findings.extend(await architect.evaluate_architecture())
            except Exception:
                logger.exception("IChiefArchitect.evaluate_architecture failed; skipping architecture findings.")

        # SECURITY: Replaced with ultra-fast regex scanning in CHEAP tier (not fully skipped)
        if self.current_tier == "CHEAP":
            if self._charge_operation("lightweight_rules_call", "Lightweight regex-based security audit"):
                findings.extend(self._run_fast_security_scan())
        else:
            try:
                security_eng = self.container.resolve(ISecurityEngineer)
                if self._charge_operation("expensive_agent_call", "ISecurityEngineer audit_security"):
                    findings.extend(await security_eng.audit_security())
            except Exception:
                logger.exception("ISecurityEngineer.audit_security failed; skipping security findings.")

        # PERFORMANCE: Profile performance under all tiers
        try:
            performance_eng = self.container.resolve(IPerformanceEngineer)
            cost_type = "lightweight_rules_call" if self.current_tier == "CHEAP" else "standard_call"
            if self._charge_operation(cost_type, "IPerformanceEngineer profile_performance"):
                findings.extend(await performance_eng.profile_performance())
        except Exception:
            logger.exception("IPerformanceEngineer.profile_performance failed; skipping performance findings.")

        if not findings:
            return proposals

        # 2. Select the highest-severity finding
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        findings.sort(key=lambda f: severity_order.get(f.severity, 4))

        # Consistent with legacy logic: process only the top highest priority finding
        target_finding = findings[0]

        # 3. Check local in-memory proposal cache
        cache_key = self._generate_cache_key(target_finding)
        if cache_key in self._global_cache:
            # Highly optimized: Return cached proposal immediately (0 cost!)
            if self._charge_operation("skipped_or_cached", f"In-memory Cache Hit for key {cache_key}"):
                cached_proposal = self._global_cache[cache_key]
                cached_proposal.status = "EVALUATED"
                proposals.append(cached_proposal)
            return proposals

        # 4. Generate a software fix proposal
        try:
            swe = self.container.resolve(ISoftwareEngineer)
            charge_type = "standard_call" if self.current_tier == "CHEAP" else "expensive_agent_call"
            if not self._charge_operation(charge_type, "ISoftwareEngineer generate_patch"):
                return proposals
            proposal = await swe.generate_patch(target_finding)
        except Exception:
            logger.exception("ISoftwareEngineer.generate_patch failed; aborting optimization cycle.")
            return proposals

        # 5. Gather research-driven citations (Skipped in CHEAP tier)
        if self.current_tier != "CHEAP":
            try:
                researcher = self.container.resolve(IResearchScientist)
                if self._charge_operation("standard_call", "IResearchScientist research_topic"):
                    citations = await researcher.research_topic(f"optimization of {target_finding.category}")
                    proposal.research_citations.extend(citations)
            except Exception:
                logger.exception("IResearchScientist.research_topic failed; proceeding without research citations.")
        else:
            self._charge_operation("skipped_or_cached", "Skipped research scientist in CHEAP tier")

        # 6. Generate unit/integration tests (Skipped in CHEAP tier)
        if self.current_tier != "CHEAP":
            try:
                qa = self.container.resolve(IQaEngineer)
                if self._charge_operation("standard_call", "IQaEngineer generate_tests"):
                    test_code = await qa.generate_tests(proposal)
                    proposal.summary += f"\n[QA Test Generated]\n{test_code}"
            except Exception:
                logger.exception("IQaEngineer.generate_tests failed; proceeding without generated tests.")
        else:
            self._charge_operation("skipped_or_cached", "Skipped QA test generation in CHEAP tier")

        # 7. Benchmark and evaluate the proposal to protect budget and prevent regressions
        try:
            evaluator = self.container.resolve(IEvaluator)
            charge_type = "lightweight_rules_call" if self.current_tier == "CHEAP" else "standard_call"
            if not self._charge_operation(charge_type, "IEvaluator benchmark_proposal"):
                return proposals
            report = await evaluator.benchmark_proposal(proposal)
            proposal.benchmark_report = report

            if not report.is_regression:
                proposal.status = "EVALUATED"
                # Cache the successfully evaluated proposal!
                self._global_cache[cache_key] = proposal
            else:
                proposal.status = "REJECTED"
        except Exception:
            logger.exception("IEvaluator.benchmark_proposal failed; marking proposal as REJECTED.")
            proposal.status = "REJECTED"

        proposals.append(proposal)
        return proposals
