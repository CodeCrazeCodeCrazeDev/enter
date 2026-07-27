from __future__ import annotations
import logging
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger("arcs.integrations")


class AdapterMode(str, Enum):
    MOCK = "mock"
    SANDBOX = "sandbox"
    PRODUCTION = "production"


class BaseAdapter:
    """Base class for all execution surface adapters."""

    def __init__(self, mode: AdapterMode = AdapterMode.MOCK) -> None:
        self.mode = mode
        self.execution_log: List[Dict[str, Any]] = []

    def log_execution(self, method_name: str, args: Dict[str, Any], result: Dict[str, Any]) -> None:
        self.execution_log.append({
            "method": method_name,
            "args": args,
            "result": result,
            "mode": self.mode.value
        })


class CRMAdapter(BaseAdapter):
    async def upsert_contact(self, email: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        result = {"status": "success", "contact_id": f"crm_contact_{hash(email) % 10000}"}
        if self.mode == AdapterMode.PRODUCTION:
            logger.warning("[CRM - Production Mode] Direct production API upsert_contact called!")
        self.log_execution("upsert_contact", {"email": email, "properties": properties}, result)
        return result


class AdsAdapter(BaseAdapter):
    async def create_campaign(self, name: str, daily_budget_cents: int) -> Dict[str, Any]:
        result = {"status": "success", "campaign_id": f"ads_camp_{name.lower().replace(' ', '_')}"}
        if self.mode == AdapterMode.PRODUCTION:
            logger.warning("[Ads - Production Mode] Direct production API create_campaign called!")
        self.log_execution("create_campaign", {"name": name, "daily_budget_cents": daily_budget_cents}, result)
        return result


class EmailAdapter(BaseAdapter):
    async def send_email(self, recipient: str, subject: str, body: str) -> Dict[str, Any]:
        result = {"status": "sent", "email_id": f"mail_{recipient.split('@')[0]}_{hash(subject) % 1000}"}
        if self.mode == AdapterMode.PRODUCTION:
            logger.warning("[Email - Production Mode] Direct production API send_email called!")
        self.log_execution("send_email", {"recipient": recipient, "subject": subject}, result)
        return result


class PaymentsAdapter(BaseAdapter):
    async def charge_customer(self, customer_id: str, amount_cents: int) -> Dict[str, Any]:
        result = {"status": "success", "transaction_id": f"tx_pay_{uuid_short()}"}
        if self.mode == AdapterMode.PRODUCTION:
            logger.warning("[Payments - Production Mode] Direct production API charge_customer called!")
        self.log_execution("charge_customer", {"customer_id": customer_id, "amount_cents": amount_cents}, result)
        return result


class BankingAdapter(BaseAdapter):
    async def transfer_funds(self, from_account: str, to_account: str, amount_cents: int) -> Dict[str, Any]:
        result = {"status": "success", "transfer_id": f"bank_transfer_{uuid_short()}"}
        if self.mode == AdapterMode.PRODUCTION:
            logger.warning("[Banking - Production Mode] Direct production API transfer_funds called!")
        self.log_execution("transfer_funds", {"from_account": from_account, "to_account": to_account, "amount_cents": amount_cents}, result)
        return result


class AnalyticsAdapter(BaseAdapter):
    async def track_event(self, event_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        result = {"status": "tracked"}
        self.log_execution("track_event", {"event_name": event_name, "payload": payload}, result)
        return result


class SocialMediaAdapter(BaseAdapter):
    async def publish_post(self, channel: str, text: str) -> Dict[str, Any]:
        result = {"status": "published", "post_id": f"post_{channel}_{hash(text) % 10000}"}
        if self.mode == AdapterMode.PRODUCTION:
            logger.warning("[Social - Production Mode] Direct production API publish_post called!")
        self.log_execution("publish_post", {"channel": channel, "text": text}, result)
        return result


class DomainRegistrationAdapter(BaseAdapter):
    async def register_domain(self, domain_name: str) -> Dict[str, Any]:
        result = {"status": "registered", "domain": domain_name}
        if self.mode == AdapterMode.PRODUCTION:
            logger.warning("[Domain - Production Mode] Direct production API register_domain called!")
        self.log_execution("register_domain", {"domain_name": domain_name}, result)
        return result


class TrademarkSearchAdapter(BaseAdapter):
    async def search_trademark(self, term: str) -> Dict[str, Any]:
        result = {"available": True, "conflicts": []}
        self.log_execution("search_trademark", {"term": term}, result)
        return result


class LegalFilingAdapter(BaseAdapter):
    async def file_incorporation(self, company_name: str, state: str) -> Dict[str, Any]:
        result = {"status": "filed", "filing_id": f"file_{company_name.lower().replace(' ', '_')}"}
        if self.mode == AdapterMode.PRODUCTION:
            logger.warning("[Legal - Production Mode] Direct production API file_incorporation called!")
        self.log_execution("file_incorporation", {"company_name": company_name, "state": state}, result)
        return result


class ExecutionSurfaceRegistry:
    """Interchangeable Execution Surface Adapters Registry supporting Mock, Sandbox, and Production."""

    def __init__(self, mode: AdapterMode = AdapterMode.MOCK) -> None:
        self.mode = mode
        self.crm = CRMAdapter(mode)
        self.ads = AdsAdapter(mode)
        self.email = EmailAdapter(mode)
        self.payments = PaymentsAdapter(mode)
        self.banking = BankingAdapter(mode)
        self.analytics = AnalyticsAdapter(mode)
        self.social = SocialMediaAdapter(mode)
        self.domains = DomainRegistrationAdapter(mode)
        self.trademark = TrademarkSearchAdapter(mode)
        self.legal = LegalFilingAdapter(mode)

    def set_mode(self, mode: AdapterMode) -> None:
        self.mode = mode
        self.crm.mode = mode
        self.ads.mode = mode
        self.email.mode = mode
        self.payments.mode = mode
        self.banking.mode = mode
        self.analytics.mode = mode
        self.social.mode = mode
        self.domains.mode = mode
        self.trademark.mode = mode
        self.legal.mode = mode
        logger.info(f"Execution surface registry updated to mode: {mode.value}")


def uuid_short() -> str:
    import uuid
    return str(uuid.uuid4())[:8]
