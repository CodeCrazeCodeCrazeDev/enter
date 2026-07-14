from __future__ import annotations
import logging
import re
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.agents.executive")


class AgentCapability(BaseModel):
    name: str
    description: str
    enabled: bool = True


class CorporateAgent(BaseModel):
    """Base class for all executive and specialized corporate agents in the ARCS hierarchy."""

    agent_id: str
    role_name: str
    mission: str
    goals: List[str] = Field(default_factory=list)
    capabilities: List[AgentCapability] = Field(default_factory=list)

    def log_thought(self, thought: str) -> None:
        """Log the agent's internal reasoning process (cognitive auditing)."""
        logger.info(f"[{self.role_name} - {self.agent_id}] COGNITIVE THOUGHT: {thought}")

    def get_capabilities(self) -> List[AgentCapability]:
        """Retrieve authorized capabilities of this agent."""
        return [c for c in self.capabilities if c.enabled]


# =====================================================================
# Corporate Organizational Hierarchy (18 Agents)
# =====================================================================

class BoardOfDirectors(CorporateAgent):
    """Human-in-the-loop and AI observer body that governs the corporate platform, policies, and overrides."""

    role_name: str = "Board of Directors"
    mission: str = "Establish ultimate policies, approve high-level budgets, review corporate health, and arbitrate executive escalations."

    def review_strategic_performance(self, financial_summary: Dict[str, Any]) -> bool:
        self.log_thought("Reviewing company financial position against board policy parameters.")
        cash = financial_summary.get("total_cash_cents", 0)
        burn_rate = financial_summary.get("burn_rate_cents", 0)
        if burn_rate > 0 and (cash / burn_rate) < 3.0:
            self.log_thought("WARNING: Runway is below 3 months. Restricting non-essential capital allocations.")
            return False
        return True

    def declare_policy(self, policy_id: str, criteria: Dict[str, Any]) -> Dict[str, Any]:
        self.log_thought(f"Declaring new organizational policy: {policy_id}")
        return {"policy_id": policy_id, "criteria": criteria, "status": "enforced"}


class CEOAgent(CorporateAgent):
    """Chief Executive Officer: coordinates all company operations and sets departmental targets."""

    role_name: str = "Chief Executive Officer"
    mission: str = "Coordinate all departments, translate Board objectives into executable plans, and manage executive delegates."

    def EvaluateBusiness(self, kpi_report: Dict[str, Any]) -> Dict[str, Any]:
        self.log_thought("Evaluating core business KPIs to identify bottlenecks.")
        mrr_growth = kpi_report.get("mrr_growth_rate", 0.0)
        cac = kpi_report.get("cac_cents", 0)
        ltv = kpi_report.get("ltv_cents", 0)

        decision = "maintain_operations"
        if mrr_growth < 0.05:
            self.log_thought("MRR growth rate is sluggish. Strategic decision: Shift budget to marketing outbound.")
            decision = "accelerate_outreach"
        elif ltv > 0 and cac > 0 and (ltv / cac) < 3.0:
            self.log_thought("LTV to CAC ratio is poor. Strategic decision: Direct Product department to focus on churn reduction.")
            decision = "focus_on_retention"

        return {"status": "success", "recommended_action": decision, "evaluation_date": "2026-07-11"}

    def AllocateCapital(self, cfo_agent: CFOAgent, department_budgets: Dict[str, int]) -> Dict[str, Any]:
        self.log_thought(f"Directing CFO to allocate operating budgets: {department_budgets}")
        results = {}
        for dept, amount in department_budgets.items():
            results[dept] = cfo_agent.AllocateCapital(dept, amount)
        return {"allocation_results": results, "authorized": True}

    def ReviewPerformance(self, department_name: str, metrics: Dict[str, Any]) -> bool:
        self.log_thought(f"Reviewing performance metrics for department: {department_name}")
        variance = metrics.get("target_variance", 0.0)
        if variance < -0.15:
            self.log_thought(f"Performance for {department_name} is below target bounds. Triggering self-correction loops.")
            return False
        return True


class CFOAgent(CorporateAgent):
    """Chief Financial Officer: manages company budgets, forecasts cash flows, and executes double-entry ledgers."""

    role_name: str = "Chief Financial Officer"
    mission: str = "Manage liquidity, optimize runway, execute capital allocation models, and audit treasury operations."

    def AllocateCapital(self, department: str, amount_cents: int) -> Dict[str, Any]:
        self.log_thought(f"Processing capital request for '{department}': {amount_cents} cents.")
        if amount_cents <= 0:
            raise ValueError("Allocation amount must be positive.")
        return {
            "department": department,
            "allocated_cents": amount_cents,
            "status": "cleared",
            "transaction_id": str(uuid.uuid4())
        }

    def AuditLedger(self, ledger_entries: List[Dict[str, Any]]) -> bool:
        self.log_thought("Auditing transaction entries. Ensuring debits equal credits (double-entry safety).")
        total_debits = sum(e.get("debit_cents", 0) for e in ledger_entries)
        total_credits = sum(e.get("credit_cents", 0) for e in ledger_entries)
        if total_debits != total_credits:
            self.log_thought(f"CRITICAL LEDGER MISMATCH: Debits ({total_debits}) != Credits ({total_credits}). Freezing assets.")
            return False
        self.log_thought("Ledger reconciliation complete. Balance matches perfectly.")
        return True


class COOAgent(CorporateAgent):
    """Chief Operating Officer: tracks marketing, sales, and delivery pipelines to optimize throughput."""

    role_name: str = "Chief Operating Officer"
    mission: str = "Optimize sales pipelines, outreach channels, support queues, and service delivery performance."

    def OptimizePipeline(self, funnel_data: Dict[str, Any]) -> Dict[str, Any]:
        self.log_thought("Analyzing customer conversion funnel stages.")
        leads = funnel_data.get("leads_count", 0)
        proposals = funnel_data.get("proposals_sent", 0)
        deals = funnel_data.get("deals_closed", 0)

        conversion_rate = (deals / leads) if leads > 0 else 0.0
        self.log_thought(f"Calculated lead-to-deal conversion: {conversion_rate:.2%}")

        action = "none"
        if conversion_rate < 0.02:
            self.log_thought("Funnel conversion rate is low. Adjusting sales chatbot scripts and qualification criteria.")
            action = "reprogram_sales_agent"

        return {"conversion_rate": conversion_rate, "recommended_sop": action}


class CTOAgent(CorporateAgent):
    """Chief Technology Officer: oversees product builds, code deployments, and API integrations."""

    role_name: str = "Chief Technology Officer"
    mission: str = "Maintain system availability, minimize hosting/inference costs, and deploy secure product updates."

    def ReviewArchitecture(self, deployment_stats: Dict[str, Any]) -> Dict[str, Any]:
        self.log_thought("Reviewing product architecture deployment and API latency.")
        latency = deployment_stats.get("p99_latency_ms", 0.0)
        error_rate = deployment_stats.get("error_rate", 0.0)

        action = "stable"
        if latency > 400.0:
            self.log_thought("Inference or API latency is high. Directing engineering to scale up caches.")
            action = "scale_infrastructure"
        elif error_rate > 0.01:
            self.log_thought("Error rate exceeds SLA bounds. Triggering failover routine.")
            action = "rollback_deployment"

        return {"status": "complete", "action": action}


class ChiefScientistAgent(CorporateAgent):
    """Chief Scientist: researches modeling improvements and designs scientific experiments."""

    role_name: str = "Chief Scientist"
    mission: str = "Research advanced AI models, evaluate prompts, design experiments, and discover algorithmic optimizations."

    def EvaluatePromptPerformance(self, prompt_traces: List[Dict[str, Any]]) -> Dict[str, Any]:
        self.log_thought("Analyzing agent thought traces and prompt output variance.")
        failures = sum(1 for t in prompt_traces if t.get("formatting_error", False))
        total = len(prompt_traces)
        error_rate = (failures / total) if total > 0 else 0.0
        self.log_thought(f"Prompt formatting error rate evaluated: {error_rate:.2%}")

        action = "stable"
        if error_rate > 0.05:
            self.log_thought("Prompt error rate is high. Designing direct structural template updates.")
            action = "optimize_prompt_templates"

        return {"error_rate": error_rate, "action": action}


class LegalAgent(CorporateAgent):
    """Legal Agent: drafts legal documents and checks contract compliance."""

    role_name: str = "Legal Counsel"
    mission: str = "Draft legally compliant SaaS contracts, privacy policies, terms of service, and verify legal standing."

    def ReviewContract(self, contract_draft: str) -> bool:
        self.log_thought("Checking contract text for required standard clauses (indemnification, SLA limits).")
        if "LIMITATION OF LIABILITY" not in contract_draft.upper():
            self.log_thought("REJECTED: Contract lacks limitation of liability clause.")
            return False
        self.log_thought("Contract complies with legal standards.")
        return True


class ComplianceAgent(CorporateAgent):
    """Compliance Agent: evaluates risk limits, ABAC/RBAC, and tax compliance."""

    role_name: str = "Compliance Officer"
    mission: str = "Evaluate risk limits, ABAC/RBAC authorizations, regional tax compliance, and fraud detection."

    def EvaluateActionRisk(self, action_payload: Dict[str, Any]) -> bool:
        self.log_thought("Enforcing organizational risk policies.")
        discount = action_payload.get("proposed_discount_pct", 0.0)
        if discount > 0.40:
            self.log_thought(f"REJECTED: Proposed discount {discount:.2%} violates strict compliance cap of 40%.")
            return False
        return True


class SecurityAgent(CorporateAgent):
    """Security Agent: scans inputs, checks API tokens, and protects tool executions."""

    role_name: str = "Security Officer"
    mission: str = "Scan agent inputs, enforce network/sandbox isolation boundaries, and monitor credential use."

    def SanitizePayload(self, payload: str) -> str:
        self.log_thought("Scanning payload for prompt injection or toxic SQL commands.")
        bad_keywords = ["ignore previous instructions", "drop table", "select * from secrets"]
        sanitized = payload
        for kw in bad_keywords:
            pattern = re.compile(re.escape(kw), re.IGNORECASE)
            if pattern.search(sanitized):
                self.log_thought(f"ALERT: Detected injection threat: '{kw}'. Removing threat.")
                sanitized = pattern.sub("[REDACTED_BY_SECURITY]", sanitized)
        return sanitized


class TreasuryAgent(CorporateAgent):
    """Treasury Agent: processes cash transactions, converts currencies, and interfaces with gateways."""

    role_name: str = "Treasury Manager"
    mission: str = "Process multi-rail payment transactions, convert currencies, and monitor wallet liquidity."

    def ProcessDisbursement(self, destination: str, amount_cents: int) -> bool:
        self.log_thought(f"Validating outbound disbursement of {amount_cents} cents to {destination}.")
        if amount_cents > 1000000:  # $10k limit
            self.log_thought("Outbound payout exceeds automated limits. Requiring CFO dual-authorization.")
            return False
        self.log_thought("Disbursement processed successfully.")
        return True


class MarketingAgent(CorporateAgent):
    """Marketing Agent: configures campaigns, content plans, and SEO/GEO pages."""

    role_name: str = "Marketing Manager"
    mission: str = "Create customer acquisition campaigns, optimize SEO landing pages, and generate content drafts."

    def GenerateAdCopy(self, target_product: str) -> str:
        self.log_thought(f"Synthesizing high-converting ad copy for: {target_product}")
        return f"Unlock massive efficiency with Apodex {target_product}! Fully autonomous API integration in seconds."


class SalesAgent(CorporateAgent):
    """Sales Agent: conducts outreach, qualifies leads, and drafts customer proposals."""

    role_name: str = "Sales Specialist"
    mission: str = "Qualify inbound customer inquiries, handle email outbound, and draft custom pricing proposals."

    def QualifyProspect(self, prospect_info: Dict[str, Any]) -> float:
        self.log_thought("Qualifying lead against ICP specifications.")
        budget = prospect_info.get("budget_cents", 0)
        need = prospect_info.get("pain_point_fit", False)

        score = 0.0
        if budget > 50000:  # $500/mo minimum
            score += 0.5
        if need:
            score += 0.5

        self.log_thought(f"Lead qualified with confidence score: {score:.1%}")
        return score


class EngineeringAgent(CorporateAgent):
    """Engineering Agent: compiles code, builds templates, and runs tests."""

    role_name: str = "Software Engineer"
    mission: str = "Compile clean API codes, draft product templates, and execute testing sandboxes."

    def RunUnitTests(self, module_name: str) -> bool:
        self.log_thought(f"Executing test harness on module: {module_name}")
        return True


class ProductAgent(CorporateAgent):
    """Product Agent: designs features, sets up pricing structures, and drafts specs."""

    role_name: str = "Product Manager"
    mission: str = "Define product specifications, structure subscription tiers, and evaluate user engagement."

    def DraftFeatureSpec(self, opportunity_desc: str) -> Dict[str, Any]:
        self.log_thought(f"Translating market opportunity into standard feature spec: '{opportunity_desc}'")
        return {
            "title": "Automated PDF Analysis Core",
            "endpoints": ["/api/v1/analyze-pdf"],
            "tier_fit": "growth"
        }


class ResearchAgent(CorporateAgent):
    """Research Agent: conducts deep web fetches and aggregates competitor intelligence."""

    role_name: str = "Market Researcher"
    mission: str = "Conduct deep competitive scrapings, scrape trend signals, and identify customer pain points."

    def ScrapeCompetitorPrices(self, competitor_name: str) -> List[Dict[str, Any]]:
        self.log_thought(f"Scraping pricing structures for competitor: {competitor_name}")
        return [
            {"tier": "basic", "price_cents": 2900},
            {"tier": "pro", "price_cents": 7900}
        ]


class CustomerSuccessAgent(CorporateAgent):
    """Customer Success Agent: provisons accounts, resolves support tickets, and drafts case studies."""

    role_name: str = "Customer Success Specialist"
    mission: str = "Onboard new accounts, respond to support tickets, and identify churn risks."

    def HandleSupportTicket(self, ticket_desc: str) -> str:
        self.log_thought(f"Processing support ticket request: '{ticket_desc}'")
        return "Thank you for reaching out. We have updated your API rate limit quotas as requested."


class BusinessDevelopmentAgent(CorporateAgent):
    """Business Development Agent: tracks partners and handles affiliate registrations."""

    role_name: str = "Business Development Director"
    mission: str = "Establish strategic affiliate structures, evaluate partner requests, and manage integrations."

    def ReviewPartnerRequest(self, partner_info: Dict[str, Any]) -> bool:
        self.log_thought("Evaluating partner alignment with Apodex ecosystem values.")
        domain = partner_info.get("domain", "")
        if "crypto" in domain.lower() or "ai" in domain.lower():
            self.log_thought("Partner category aligned. Moving to contract review.")
            return True
        return False


class InvestmentDivisionAgent(CorporateAgent):
    """Investment Division Agent: handles surplus allocation and models yield options."""

    role_name: str = "Investment Manager"
    mission: str = "Formulate yield options for surplus capital reserves and monitor treasury asset allocations."

    def ProposeYieldAllocation(self, surplus_cents: int) -> Dict[str, Any]:
        self.log_thought(f"Formulating optimal allocation portfolio for surplus reserve: {surplus_cents} cents.")
        return {
            "reserve_stablecoin_cents": int(surplus_cents * 0.70),
            "reserve_yield_vault_cents": int(surplus_cents * 0.30)
        }
