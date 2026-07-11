from __future__ import annotations
import logging
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List

logger = logging.getLogger("arcs.treasury")


class IPaymentAdapter(ABC):
    """Abstract port representing a generic payment rail adapter (e.g., Stripe, Wise, Web3)."""

    @abstractmethod
    async def charge(self, amount_cents: int, currency: str, description: str) -> Dict[str, Any]:
        """Process an inbound payment transaction."""
        pass

    @abstractmethod
    async def disburse(self, amount_cents: int, currency: str, destination: str) -> Dict[str, Any]:
        """Disburse funds outbound to a recipient."""
        pass


class StripeAdapter(IPaymentAdapter):
    """Adapter for processing payments over Stripe."""

    async def charge(self, amount_cents: int, currency: str, description: str) -> Dict[str, Any]:
        logger.info(f"[Stripe] Processing charge of {amount_cents} {currency} ({description})")
        return {
            "gateway": "stripe",
            "transaction_id": f"ch_{uuid.uuid4().hex[:12]}",
            "status": "success",
            "amount_cents": amount_cents
        }

    async def disburse(self, amount_cents: int, currency: str, destination: str) -> Dict[str, Any]:
        logger.info(f"[Stripe] Executing transfer of {amount_cents} {currency} to bank destination '{destination}'")
        return {
            "gateway": "stripe",
            "payout_id": f"po_{uuid.uuid4().hex[:12]}",
            "status": "success"
        }


class StablecoinAdapter(IPaymentAdapter):
    """Adapter for processing decentralized stablecoin micropayments (USDC/USDT on-chain)."""

    async def charge(self, amount_cents: int, currency: str, description: str) -> Dict[str, Any]:
        logger.info(f"[Stablecoin] Directing transfer of {amount_cents / 100:.2f} USDC on-chain.")
        return {
            "gateway": "stablecoin",
            "transaction_id": f"0x{uuid.uuid4().hex}",
            "status": "success",
            "amount_cents": amount_cents
        }

    async def disburse(self, amount_cents: int, currency: str, destination: str) -> Dict[str, Any]:
        logger.info(f"[Stablecoin] Executing payout of {amount_cents / 100:.2f} USDC to address '{destination}'")
        return {
            "gateway": "stablecoin",
            "payout_id": f"0x{uuid.uuid4().hex}",
            "status": "success"
        }


class TreasuryGateway:
    """Multi-rail treasury gateway routing payments dynamically through registered adapters."""

    def __init__(self) -> None:
        self._adapters: Dict[str, IPaymentAdapter] = {}

    def register_adapter(self, rail_name: str, adapter: IPaymentAdapter) -> None:
        self._adapters[rail_name] = adapter
        logger.info(f"Registered payment adapter: {rail_name}")

    async def charge_invoice(self, amount_cents: int, currency: str, rail_name: str = "stripe") -> Dict[str, Any]:
        if rail_name not in self._adapters:
            raise ValueError(f"No adapter registered for financial rail: {rail_name}")
        adapter = self._adapters[rail_name]
        return await adapter.charge(amount_cents, currency, "ARCS Service Invoice")

    async def execute_payout(self, amount_cents: int, currency: str, destination: str, rail_name: str = "stripe") -> Dict[str, Any]:
        if rail_name not in self._adapters:
            raise ValueError(f"No adapter registered for financial rail: {rail_name}")
        adapter = self._adapters[rail_name]
        return await adapter.disburse(amount_cents, currency, destination)
