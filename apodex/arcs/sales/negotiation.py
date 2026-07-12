from __future__ import annotations
import logging
from typing import Any, Dict

logger = logging.getLogger("arcs.sales.negotiation")


class NegotiationEngine:
    """Enterprise-grade negotiation agent and contract generator."""

    def __init__(self, base_annual_fee_cents: int = 1200000) -> None:
        self.base_annual_fee_cents = base_annual_fee_cents

    def negotiate_discount(self, requested_discount_pct: float) -> Dict[str, Any]:
        """Verify requested discount against compliance boundaries and compute final pricing."""
        logger.info(f"[Negotiation] Customer requested a {requested_discount_pct:.1%} discount on baseline annual fee.")

        # Risk assessment: cap discount at 35% without board exception
        if requested_discount_pct > 0.35:
            logger.warning("[Negotiation] Discount exceeds standard boundary of 35%! Capping to 35%.")
            final_discount = 0.35
        else:
            final_discount = requested_discount_pct

        final_fee = int(self.base_annual_fee_cents * (1.0 - final_discount))
        logger.info(f"[Negotiation] Final pricing negotiated: {final_fee} cents (Applied Discount: {final_discount:.1%})")

        return {
            "agreed_discount_pct": final_discount,
            "annual_fee_cents": final_fee,
            "monthly_installment_cents": final_fee // 12,
            "contract_approved": True
        }

    def generate_contract(self, company_name: str, deal_details: Dict[str, Any]) -> str:
        """Dynamically generate standard legally compliant SaaS contracts."""
        fee = deal_details.get("annual_fee_cents", self.base_annual_fee_cents)
        discount = deal_details.get("agreed_discount_pct", 0.0)

        contract_text = (
            f"SOFTWARE AS A SERVICE AGREEMENT\n"
            f"This agreement is entered into by Apodex and Client '{company_name}'.\n"
            f"1. SERVICES: Apodex grants a non-transferable license to access cognitive features.\n"
            f"2. FEES: Client shall pay {fee / 100:.2f} USD annually (Negotiated Discount: {discount:.1%}).\n"
            f"3. LIMITATION OF LIABILITY: Neither party shall be liable for indirect, incidental, "
            f"or consequential damages. Standard SLA limits apply.\n"
            f"4. GOVERNANCE: Both parties adhere to strict legal and compliance constraints."
        )
        logger.info(f"[Negotiation] Generated official corporate contract for '{company_name}'")
        return contract_text
