from __future__ import annotations
import logging
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.finance.billing")


class UsageMeter(BaseModel):
    customer_id: uuid.UUID
    api_calls_made: int = 0
    storage_bytes: int = 0


class MeteredBillingSystem:
    """Enterprise-grade metered billing, subscription cycles, and invoice compilers."""

    def __init__(self) -> None:
        self.meters: Dict[uuid.UUID, UsageMeter] = {}
        self.billing_rate_per_call_cents: float = 0.002  # $2 per 1000 requests

    def record_usage(self, customer_id: uuid.UUID, calls_count: int, bytes_added: int = 0) -> UsageMeter:
        if customer_id not in self.meters:
            self.meters[customer_id] = UsageMeter(customer_id=customer_id)

        meter = self.meters[customer_id]
        meter.api_calls_made += calls_count
        meter.storage_bytes += bytes_added
        logger.debug(f"[Billing] Recorded usage for {customer_id}: +{calls_count} calls, +{bytes_added} bytes.")
        return meter

    def generate_invoice(self, customer_id: uuid.UUID, base_tier_cents: int) -> Dict[str, Any]:
        """Compile metered usage metrics into an invoice at cycle-end."""
        meter = self.meters.get(customer_id, UsageMeter(customer_id=customer_id))

        # Calculate metered overage charges
        metered_cents = int(meter.api_calls_made * self.billing_rate_per_call_cents)
        total_cents = base_tier_cents + metered_cents

        logger.info(f"[Billing] Compiled invoice for customer {customer_id}: Base={base_tier_cents} + Metered={metered_cents} = Total {total_cents} cents.")

        # Reset current cycle meter
        meter.api_calls_made = 0
        meter.storage_bytes = 0

        return {
            "invoice_id": uuid.uuid4(),
            "customer_id": customer_id,
            "base_fee_cents": base_tier_cents,
            "overage_cents": metered_cents,
            "total_amount_cents": total_cents,
            "due_date": datetime.utcnow() + timedelta(days=15),
            "status": "pending"
        }
