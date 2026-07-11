from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr


class TenantCreateRequest(BaseModel):
    name: str
    api_key_hash: str


class TenantResponse(BaseModel):
    id: uuid.UUID
    name: str
    status: str
    created_at: datetime


class CustomerOnboardRequest(BaseModel):
    email: str
    currency: str = "USD"


class CustomerResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    email: str
    kyc_status: str
    currency: str
    balance_cents: int
    status: str
    created_at: datetime


class ProductCreateRequest(BaseModel):
    name: str
    description: str
    pricing_type: str
    amount_cents: int
    currency: str = "USD"


class ProductResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    description: str
    pricing_type: str
    amount_cents: int
    currency: str
    status: str
    created_at: datetime


class InvoiceCreateRequest(BaseModel):
    customer_id: uuid.UUID
    amount_cents: int
    currency: str = "USD"
    due_at: datetime


class InvoiceResponse(BaseModel):
    id: uuid.UUID
    customer_id: uuid.UUID
    tenant_id: uuid.UUID
    amount_cents: int
    currency: str
    status: str
    due_at: datetime
    paid_at: Optional[datetime]
    created_at: datetime


class LedgerEntryRequest(BaseModel):
    account_code: str
    debit_cents: int = 0
    credit_cents: int = 0
    description: str


class LedgerTransactionRequest(BaseModel):
    entries: List[LedgerEntryRequest]
    description: str
